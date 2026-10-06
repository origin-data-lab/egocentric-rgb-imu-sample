# Egocentric RGB + IMU Evaluation Sample

**First-party technical evidence from Origin Data Lab**

> Real-world egocentric RGB + IMU capture with measured sensor characteristics, software-derived temporal alignment, structured metadata, and reproducible integrity checks.

[![Origin Data Lab](https://img.shields.io/badge/Origin_Data_Lab-Physical_AI_Data-111827?style=for-the-badge)](https://origindatalab.io/)
![Sample](https://img.shields.io/badge/Sample-v1.0.3-2563EB?style=for-the-badge)
![Verifier](https://img.shields.io/badge/Verifier-Python-3776AB?style=for-the-badge)
![Verification](https://img.shields.io/badge/Verification-PASS-16A34A?style=for-the-badge)

---

## At a Glance

| Capture | Measured value |
|---|---:|
| RGB preview | **1920 x 1080** |
| Frame rate | **30 fps** |
| Frames | **587** |
| Public excerpt | **19.567 s** |
| Native accelerometer | **410.641 Hz** |
| Native gyroscope | **410.641 Hz** |
| App-level accelerometer | **102.353 Hz** |
| App-level gyroscope | **102.162 Hz** |
| Audio | **Not included** |

**Task category:** food preparation  
**Environment:** domestic kitchen  
**Capture country:** South Korea  
**Sample type:** capability demonstration

---

## What This Repository Is

This repository is the technical companion to Origin Data Lab's public **Egocentric RGB + IMU Evaluation Sample**.

It makes the sample inspectable rather than asking evaluators to rely only on capability claims.

This repository provides:

- the Python verification utility used on the public package;
- recorded verification output;
- documentation of the public data structure;
- timestamp and temporal-alignment methodology;
- explicit limitations and non-claims.

The complete evaluation payload — video, IMU streams, task annotations, public metadata, integrity records, and checksums — is distributed separately from this code repository.

---

## Verified Measurements

The included verifier computes timestamp statistics directly from `sensor_timestamp_ns`.

| Stream | Samples | Measured rate | Maximum interval | Duplicates | Non-monotonic |
|---|---:|---:|---:|---:|---:|
| App-level accelerometer | 2,001 | **102.353 Hz** | 21.9177 ms | 0 | 0 |
| App-level gyroscope | 1,998 | **102.162 Hz** | 21.9177 ms | 0 | 0 |
| Native accelerometer | 8,028 | **410.641 Hz** | 2.4360 ms | 0 | 0 |
| Native gyroscope | 8,028 | **410.641 Hz** | 2.4360 ms | 0 | 0 |

### Cross-stream consistency

- Accelerometer timestamp matches: **2,001 / 2,001**
- Native/app accelerometer scale ratio: **9.806650–9.806651**
- Gyroscope timestamp matches: **1,998 / 1,998**
- Native/app gyroscope value ratio: **1.000000**

These are measured values from the released sample, not nominal device specifications.

---

## Temporal Alignment

RGB and IMU in this public excerpt are **software-aligned**.

The package does **not** claim hardware synchronization, frame-level synchronization, or sub-frame synchronization.

### Post-correction pre-release checks

| Check | Result |
|---|---:|
| Visual-inertial Method A | **0 ms**, R² = **0.798** |
| Visual-inertial Method B | **+6 ms**, Pearson r = **0.929** |
| Method A quarter-window shifts | **−4, −2, 0, +2 ms** |
| Stated alignment uncertainty | **within one 30 fps video frame (33 ms)** |

These are **in-sample pre-release visual-inertial checks**.

See **[Timing Validation](docs/TIMING_VALIDATION.md)** for methodology and interpretation.

---

## Reproduce the Verification

The verifier checks:

1. SHA-256 manifest integrity
2. Per-stream timestamp statistics
3. Duplicate and non-monotonic timestamps
4. Application/native cross-stream consistency
5. Visual-inertial lag between image motion and native gyroscope motion

### Requirements

```bash
pip install numpy opencv-python
```

### Run

```bash
python tools/verify_odl_sample.py /path/to/OriginDataLab_Public_Egocentric_RGB_IMU_Sample
```

**[View recorded v1.0.3 verification output](examples/verification_output.txt)**

---

## Evaluation Package Structure

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

See **[Sample Structure](docs/SAMPLE_STRUCTURE.md)** and **[Data Schema](docs/DATA_SCHEMA.md)**.

---

## Coordinate & Unit Notes

The source device orientation was portrait. The public video preview was transformed **90° counterclockwise without crop or stretch** into landscape orientation. The IMU axes were **not rotated to match the transformed video preview**.

Public metadata identifies the coordinate frame as:

> Android device default; portrait source reference

For this released sample:

- native accelerometer values are strongly supported as **m/s²** by the 9.80665 cross-stream scale relationship;
- application-level accelerometer values are represented in **g**;
- gyroscope values are represented as **rad/s**.

---

## What This Sample Demonstrates

**Egocentric RGB capture**  
→ **Native + application-level IMU**  
→ **Sensor-event timestamps**  
→ **Software-derived temporal alignment**  
→ **Structured task / interaction metadata**  
→ **Integrity verification**  
→ **Reproducible technical evaluation**

This is a capability demonstration, not a claim that every Origin Data Lab project uses identical hardware, rates, schemas, or synchronization methods. Production configurations are defined against customer requirements.

---

## Explicit Non-Claims

This sample does **not** claim:

- hardware synchronization between RGB and IMU;
- guaranteed frame-level synchronization;
- sub-frame synchronization;
- universal sensor rates across devices;
- held-out validation of the alignment procedure;
- production readiness for a specific robot policy;
- VLA readiness or world-model readiness without buyer-specific validation.

The stated timing uncertainty for this public excerpt is **within one 30 fps video frame (33 ms)**.

---

## Privacy

The public evaluation excerpt removes or excludes audio, exact location, collector identifiers, absolute Unix arrival timestamps, and internal capture identifiers.

Public release of field data remains subject to applicable rights, consent, privacy, and project-specific requirements.

---

## Technical Documentation

| Document | Purpose |
|---|---|
| [Data Schema](docs/DATA_SCHEMA.md) | Public RGB/IMU fields and stream semantics |
| [Timing Validation](docs/TIMING_VALIDATION.md) | Alignment methodology and limitations |
| [Sample Structure](docs/SAMPLE_STRUCTURE.md) | Evaluation package organization |
| [Verification Output](examples/verification_output.txt) | Recorded verifier output |
| [Verifier](tools/verify_odl_sample.py) | Reproducible verification utility |

---

## Origin Data Lab

Origin Data Lab produces real-world multimodal training data for **Physical AI, robotics, and embodied AI**.

Our work spans field sourcing, worker onboarding, capture operations, sensor and metadata pipelines, QC, recapture, structured delivery, and customer-specific production workflows.

**[Technical Field Note — Egocentric RGB + IMU Task Sample](https://origindatalab.io/technical-field-notes/egocentric-rgb-imu-task-sample.html)**  
**[Origin Data Lab](https://origindatalab.io/)**

---

## Dataset Access

The complete evaluation payload is available through Origin Data Lab's Hugging Face dataset release.

**Dataset:** https://huggingface.co/datasets/origin-data-lab/egocentric-rgb-imu-sample

---

<sub>Origin Data Lab · Real-world multimodal data infrastructure for Physical AI and robotics.</sub>
