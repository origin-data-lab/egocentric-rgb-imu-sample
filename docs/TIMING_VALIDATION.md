# Timing Validation

## Scope

The public RGB + IMU excerpt uses **software-derived temporal alignment**.

Origin Data Lab does not claim hardware synchronization, guaranteed frame-level synchronization, or sub-frame synchronization for this sample.

## Timeline Construction

The released timing process consists of:

1. recording-start Unix anchor;
2. application-arrival / sensor-event median offset;
3. visual-inertial refinement;
4. publication of a common `t_clip_ms` interpretation.

The visual-inertial refinement applied to the source session was **−446 ms**. This corrected the source capture-session offset before publication.

## Post-Correction Validation

### Method A — Packaged Verifier

The included verifier compares per-frame global image motion with integrated native gyroscope rotation.

```text
Best shift:       0 ms
R² at best shift: 0.798
R² at 0 ms:       0.798
```

| Window | Best shift | R² |
|---|---:|---:|
| 0.0–4.9 s | −4 ms | 0.833 |
| 4.9–9.7 s | −2 ms | 0.788 |
| 9.7–14.6 s | 0 ms | 0.891 |
| 14.6–19.5 s | +2 ms | 0.820 |

### Method B — Pre-release Cross-check

```text
Best shift: +6 ms
Pearson r:  0.929
```

Across the pre-release checks, observed window shifts were approximately **−4 ms to +8 ms**.

## Stated Uncertainty

Origin Data Lab conservatively states alignment uncertainty as **within one 30 fps video frame (33 ms)**.

Near-zero software-derived residual estimates must not be represented as hardware synchronization accuracy.

## Validation Scope

These checks are visual-inertial, performed on the released excerpt, in-sample, and pre-release. They are not held-out validation and do not establish hardware synchronization.

## Safe Description

> The public RGB + IMU excerpt is software-aligned using capture-session time anchors and visual-inertial refinement. Residual offset was approximately 0 to +6 ms in pre-release checks, with stated alignment uncertainty within one 30 fps video frame (33 ms).

Do not describe this sample as hardware synchronized, frame synchronized, or sub-frame synchronized.
