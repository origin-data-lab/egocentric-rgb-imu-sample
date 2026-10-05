#!/usr/bin/env python3
"""Independent verification of an Origin Data Lab public RGB+IMU sample package.

Usage:  python3 verify_odl_sample.py <package_dir>
Needs:  numpy, opencv-python (only for the visual-inertial lag check)

Checks
  1. SHA-256 manifest
  2. Per-stream timestamp statistics (rate, intervals, gaps, duplicates, monotonicity)
  3. Cross-stream consistency (app-level timestamps vs native timestamps, value ratios)
  4. Visual-inertial lag: correlates per-frame global image motion (phase correlation)
     with integrated native gyroscope rotation, and reports the IMU time shift that
     best explains the video motion. A well-aligned package should peak near 0 ms.
"""
import csv, hashlib, math, os, statistics as st, sys

import numpy as np

PKG = sys.argv[1] if len(sys.argv) > 1 else "."
SENS = os.path.join(PKG, "sensors")


def pct(a, p):
    a = sorted(a); k = (len(a) - 1) * p; f = math.floor(k); c = math.ceil(k)
    return a[f] + (a[c] - a[f]) * (k - f)


def load(name):
    with open(os.path.join(SENS, name)) as f:
        return list(csv.DictReader(f))


def check_manifest():
    print("== 1. SHA-256 manifest")
    ok = True
    with open(os.path.join(PKG, "checksums.sha256")) as f:
        for line in f:
            h, p = line.split(None, 1); p = p.strip()
            with open(os.path.join(PKG, p), "rb") as g:
                actual = hashlib.sha256(g.read()).hexdigest()
            ok &= actual == h
            print(f"  {'OK  ' if actual == h else 'FAIL'} {p}")
    listed = {l.split(None, 1)[1].strip() for l in open(os.path.join(PKG, "checksums.sha256"))}
    present = {os.path.relpath(os.path.join(r, f), PKG) for r, _, fs in os.walk(PKG) for f in fs}
    extra = present - listed - {"checksums.sha256"}
    print("  unlisted files:", sorted(extra) or "none")
    return ok


def stream_stats(files):
    print("== 2. Stream statistics (from sensor_timestamp_ns)")
    for fn in files:
        rows = load(fn)
        t = [int(r["sensor_timestamp_ns"]) for r in rows]
        d = [(b - a) / 1e6 for a, b in zip(t, t[1:])]
        span = (t[-1] - t[0]) / 1e9
        print(f"  {fn}: n={len(t)} rate={(len(t)-1)/span:.3f}Hz mean={st.mean(d):.4f} "
              f"median={st.median(d):.4f} p95={pct(d,.95):.4f} p99={pct(d,.99):.4f} "
              f"max={max(d):.4f}ms >20ms={sum(x>20 for x in d)} >50ms={sum(x>50 for x in d)} "
              f">100ms={sum(x>100 for x in d)} dup={sum(x==0 for x in d)} nonmono={sum(x<0 for x in d)}")


def cross_stream():
    print("== 3. Cross-stream consistency (app-level vs native)")
    for s in ("accelerometer", "gyroscope"):
        A = {int(r["sensor_timestamp_ns"]): r for r in load(f"app_level_{s}_clip.csv")}
        N = {int(r["sensor_timestamp_ns"]): r for r in load(f"native_{s}_clip.csv")}
        common = set(A) & set(N)
        ratios = [float(N[t][a]) / float(A[t][a]) for t in common for a in "xyz" if abs(float(A[t][a])) > 1e-3]
        print(f"  {s}: app timestamps found in native = {len(common)}/{len(A)}; "
              f"native/app value ratio min={min(ratios):.6f} max={max(ratios):.6f}")


def visual_inertial_lag():
    print("== 4. Visual-inertial lag (gyro vs image motion)")
    import cv2
    cap = cv2.VideoCapture(os.path.join(PKG, "capture", "video_preview_aligned_19p55s.mp4"))
    fps = cap.get(cv2.CAP_PROP_FPS)
    prev = win = None; mot = []
    while True:
        ok, f = cap.read()
        if not ok:
            break
        g = cv2.cvtColor(cv2.resize(f, (480, 270)), cv2.COLOR_BGR2GRAY).astype(np.float32)
        if win is None:
            win = cv2.createHanningWindow(g.shape[::-1], cv2.CV_32F)
        mot.append(cv2.phaseCorrelate(prev, g, win)[0] if prev is not None else (0.0, 0.0))
        prev = g
    v = np.array(mot)[1:]
    rows = load("native_gyroscope_clip.csv")
    tcol = "t_clip_ms" if "t_clip_ms" in rows[0] else "t_video_ms"
    t = np.array([float(r[tcol]) for r in rows]) / 1000
    G = np.array([[float(r[a]) for a in "xyz"] for r in rows])
    cs = np.cumsum(G * np.diff(np.r_[t[0], t])[:, None], 0)
    fk = np.arange(len(mot)) / fps

    def r2(shift_ms, a0=0, a1=None):
        ang = np.stack([np.interp(fk - shift_ms / 1000, t, cs[:, i]) for i in range(3)], 1)
        gp = np.diff(ang, axis=0)[a0:a1]; vv = v[a0:a1]
        X = np.c_[gp, np.ones(len(gp))]
        p = X @ np.linalg.lstsq(X, vv, rcond=None)[0]
        return 1 - ((vv - p) ** 2).sum() / ((vv - vv.mean(0)) ** 2).sum()

    best = max(range(-1500, 1501, 2), key=r2)
    print(f"  column used: {tcol}")
    print(f"  best shift = {best} ms (R2={r2(best):.3f}); R2 at 0 ms = {r2(0):.3f}")
    n = len(v); q = n // 4
    for w in range(4):
        a0, a1 = w * q, (w + 1) * q if w < 3 else n
        bw = max(range(best - 100, best + 101, 2), key=lambda s: r2(s, a0, a1))
        print(f"  window {w} ({a0/fps:.1f}-{a1/fps:.1f}s): best {bw} ms, R2={r2(bw, a0, a1):.3f}")
    print("  Interpretation: negative shift = IMU timestamps are LATE relative to video by |shift|;"
          " correct with t_video_corrected = t_video + shift.")


if __name__ == "__main__":
    check_manifest()
    stream_stats(sorted(f for f in os.listdir(SENS) if f.endswith(".csv")))
    cross_stream()
    visual_inertial_lag()
