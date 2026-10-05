# Public Data Schema

This document describes the public sensor representation used in the Origin Data Lab Egocentric RGB + IMU Evaluation Sample v1.0.3.

## Sensor Streams

The package contains four CSV streams:

```text
sensors/
├── app_level_accelerometer_clip.csv
├── app_level_gyroscope_clip.csv
├── native_accelerometer_clip.csv
└── native_gyroscope_clip.csv
```

The verification utility uses `sensor_timestamp_ns` for rate, interval, duplicate, monotonicity, and cross-stream timestamp analysis.

## Timeline

`t_clip_ms` represents the public excerpt timeline. It is sensor-event-time-derived and incorporates the software visual-inertial timing correction used for this package. The same timeline meaning is used across all four released CSV streams.

## Timestamp Semantics

`sensor_timestamp_ns` is an Android sensor-event timestamp with nanosecond-resolution representation. Nanosecond-resolution representation must not be interpreted as nanosecond synchronization accuracy.

## Accelerometer

Application-level accelerometer values are represented in `g`.

Native accelerometer values are strongly supported as `m/s²` by the observed native/application scale relationship. For all 2,001 matching application-level timestamps:

```text
native/app ratio = 9.806650–9.806651
```

## Gyroscope

Gyroscope values are represented as `rad/s`. For all 1,998 matching application-level timestamps:

```text
native/app ratio = 1.000000
```

## Coordinate Frame

Public metadata identifies the coordinate frame as:

```text
Android device default; portrait source reference
```

The source video was `1080 x 1920` portrait. The public preview is `1920 x 1080`, transformed 90° counterclockwise without crop or stretch. IMU axes were not rotated to match the transformed preview.

## Scope

This schema documents this public evaluation sample. Buyer-specific production projects may use different sensors, rates, coordinate transforms, annotations, metadata, and export formats.
