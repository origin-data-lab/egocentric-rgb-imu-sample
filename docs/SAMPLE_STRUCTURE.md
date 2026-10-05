# Evaluation Sample Structure

The complete Origin Data Lab public evaluation package is organized as follows:

```text
OriginDataLab_Public_Egocentric_RGB_IMU_Sample/
├── capture/
│   └── video_preview_aligned_19p55s.mp4
├── sensors/
│   ├── app_level_accelerometer_clip.csv
│   ├── app_level_gyroscope_clip.csv
│   ├── native_accelerometer_clip.csv
│   └── native_gyroscope_clip.csv
├── annotations/
│   ├── interaction_events.json
│   └── task_structure.json
├── metadata/
│   └── capture_metadata_public.json
├── quality/
│   ├── integrity_report.json
│   └── verification_output.txt
├── tools/
│   └── verify_odl_sample.py
├── checksums.sha256
├── DATA_CARD.md
├── LICENSE.md
└── README.md
```

## capture/

Public RGB preview: `1920 x 1080`, `30 fps`, `587 frames`, `19.567 s`, no audio.

## sensors/

Contains native and application-level accelerometer and gyroscope streams. Separate paths allow evaluation of sampling characteristics and cross-stream consistency.

## annotations/

Contains structured task and interaction metadata for the public excerpt.

## metadata/

Contains sanitized public capture metadata. Exact location, collector identifiers, internal capture identifiers, and absolute Unix arrival timestamps are excluded.

## quality/

Contains integrity and verification evidence associated with the release.

## tools/

Contains the Python verifier used to reproduce key integrity, stream, cross-stream, and visual-inertial checks.

## checksums.sha256

Provides SHA-256 hashes for the released package payload.

## Distribution

This GitHub repository intentionally focuses on verification tooling and technical documentation. The complete video and sensor payload is distributed separately through the dataset release channel.
