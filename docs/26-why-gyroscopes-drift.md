# Why Gyroscopes Drift

## The Problem

Your drone's attitude controller depends on knowing which way is "up" — or equivalently, the drone's roll and pitch angles. You've learned that accelerometers are confused by motion (Chapter 25), so you decide to use a gyroscope instead. A gyroscope measures angular rate — how fast the drone is rotating — with impressive precision. Integrate the rate over time to get angle. Simple.

You test it on a bench. The gyroscope reads 0.003°/s when the drone is perfectly stationary. You integrate for 10 minutes. Your angle estimate drifts 1.8° — the gyro "saw" rotation that never happened.

You fly the drone indoors, no GPS. After 90 seconds of flight, the drone's heading estimate is off by 15°. The drone thinks it's flying north; it's actually flying northwest. It slowly spirals away.

You check the spec sheet: your gyro has a "bias stability" of 10°/hour. That sounds small — and it is, for one hour. But the quadcopter attitude controller needs angle estimates accurate to 0.5° or better at all times. At 10°/hour, the gyro accumulates that 0.5° error in 3 minutes.

Any gyro-based orientation system must:

- Account for bias drift — the non-zero output even when rotation rate is zero
- Compensate for drift that changes with temperature (gyro bias is temperature-dependent)
- Provide accurate long-term orientation, not just accurate rate at one instant
- Do all this while the drone is also experiencing real rapid rotations of ±500°/s

## What Would You Try?

- A ruler that slowly shrinks over time gives accurate measurements for a few seconds but diverges over minutes. How is a drifting gyroscope similar? What would you need to "recalibrate" it?
- Accelerometers can sense gravity direction even though they're confused during acceleration. Is there a physical reference that a gyroscope always has access to — something like what gravity is for accelerometers?
- You have gyro data (accurate in the short term, drifting long term) and accelerometer data (accurate in the long term on average, noisy/wrong during rapid motion). How might these complement each other?

## Failed Attempts

### Attempt 1: Calibrate bias at startup and subtract it

Before every flight, hold the drone perfectly still for 10 seconds. Average the gyro output during that window — this is the current bias. Subtract this bias from all future readings.

On a cold morning, the measured bias is 0.4°/s. After 5 minutes of flight, the drone has warmed up; the gyro's bias has shifted to 0.6°/s. You're subtracting 0.4°/s but the true bias is now 0.6°/s — leaving a residual 0.2°/s uncorrected. After 5 minutes, that's a 60° heading error. The drone has spiraled out of sight.

MEMS gyroscope bias is strongly temperature-dependent — a typical coefficient is 0.1°/s/°C. A drone motor heats the electronics by 15–20°C during flight. Static calibration captures the cold bias; it doesn't predict the warm bias. The calibration is already wrong by the time it matters.

### Attempt 2: Continuous bias correction using the vehicle's known dynamics

If the drone is commanded to hover (zero angular rate), any gyro reading is bias. Measure the gyro output during hover phases and continuously update the bias estimate.

This works during gentle hovering. But "commanded to zero rotation rate" doesn't mean "actually at zero rotation rate" — wind gusts push the drone; the attitude controller applies corrections; the drone is never truly still. The "known dynamics" assumption is violated during any actual flight. Worse: if the bias correction is running continuously, it may mistake a real slow rotation for bias and subtract it — causing the attitude controller to not respond to actual slow drifts because they're being filtered out as "bias."

### Attempt 3: High-frequency sampling reduces integration error

Maybe the drift is worse at low sample rates. If you sample at 8,000 Hz instead of 1,000 Hz, you integrate the rate signal more accurately. Trapezoidal integration at 8 kHz should drastically reduce the accumulated error.

The sample rate is not the limiting factor. Bias drift is not an aliasing error — it's a physical property of the gyroscope. The MEMS proof mass inside the gyroscope has a tiny, persistent asymmetry (manufacturing variation) that produces a non-zero output independent of rotation. Sampling faster just gives you more samples of the wrong answer. The bias is still there at 8 kHz; it integrates just as badly, just in smaller steps that sum to the same total.

Higher sample rate helps with *dynamic* accuracy (tracking fast rotations) but does nothing for *static* accuracy (long-term heading stability). The two are different error sources.

## The Discovery

The fundamental problem with a gyroscope is that integration is a one-way street: the gyroscope tells you how fast you're rotating, and you accumulate that into an angle. But integration has no "memory" for where true zero is — any persistent offset in the rate signal grows without bound.

The gyroscope is accurate in the short term because bias drift is slow (millidegrees per second). The accelerometer is accurate in the long term because gravity is a fixed external reference. They fail on opposite timescales.

The complementary structure is the discovery: use the gyro for short-term tracking (where it's accurate) and the accelerometer's gravity reference for long-term correction (where it's accurate). Neither alone is sufficient. Together, they cover each other's blind spots.

Concretely: integrate the gyroscope rate to get short-term angle. Independently, compute the gravity vector direction from the accelerometer — this is long-term reliable (gravity doesn't drift). Use the difference between the gyro-derived angle and the accelerometer-derived gravity direction to estimate and correct the gyro bias online, continuously during flight.

This is **complementary filtering**: the gyro handles high-frequency, fast motion (where the accelerometer is wrong); the accelerometer handles low-frequency, slow trend (where the gyro drifts). The filter combines them with a frequency crossover: trust gyro above some frequency, trust accelerometer below it.

The gyro drift doesn't go away — but it's now continuously corrected by the gravity reference whenever the drone isn't accelerating heavily. Formal name: **gyroscope bias estimation** via complementary or Kalman filter. The more sophisticated version (Chapter 30) tracks not just the angle but the *bias itself* as a state variable, estimating it and subtracting it continuously.

## Try It

<iframe src="../assets/browser/chapter26/index.html" width="100%" height="460" style="border:1px solid var(--md-default-fg-color--lightest);border-radius:8px;"></iframe>

[open in a new tab](../assets/browser/chapter26/index.html)

Before changing anything, predict:

- With only the gyro (no correction), how long before the angle estimate diverges by 5°? By 45°?
- Enable the accelerometer correction. What happens to the drift rate? Does it go to zero or just reduce?
- Apply rapid rotations. Does the accelerometer correction help or hurt during the rapid motion phase? Why?

## Implementation

`browser/common/engine.js` models the gyroscope as rate + bias + noise, where bias is a slow random walk. The accelerometer provides a noisy gravity vector. `browser/chapter26/index.html` runs both a pure-gyro integration and a complementary filter in parallel, displaying both angle estimates against ground truth to show when each diverges.

## When It Breaks

**Temperature shock defeats bias estimation.** If the drone moves rapidly between environments — indoor to outdoor in winter — the gyro temperature changes faster than the bias estimator can track. Hobby drone crashes in cold weather sometimes trace to a sudden gyro bias shift after the vehicle exits a warm building. Sophisticated IMUs include on-chip temperature sensors and store a calibration curve (bias vs. temperature) measured in the factory, applying corrections in real time. Budget IMUs without this feature can have 2–5°/s apparent bias shifts across a 20°C temperature range.

**Vibration causes gyro resonance.** MEMS gyroscopes work by detecting Coriolis force on a vibrating proof mass. External vibration at the proof mass resonant frequency (typically 10–30 kHz for consumer MEMS) directly excites the sensing axis and produces a false angular rate signal. Most quadcopter frame vibrations are below 1 kHz, but poorly damped propeller harmonics can reach higher. This is why flight controllers are often mounted on vibration-damped standoffs — reducing the mechanical coupling between motor vibration and the gyro proof mass.

## Transfer

- **Ring laser gyroscopes**: aircraft inertial navigation uses optical gyroscopes that work by sensing the Sagnac effect (interference of light paths rotating in opposite directions). They have essentially zero bias drift and no moving parts — but cost tens of thousands of dollars. Consumer MEMS gyros cost $2; optical gyros cost $20,000.
- **Inertial navigation in submarines**: submarines navigate without GPS for weeks at a time using precision gyroscopes and accelerometers. Even with the best available hardware (drift < 0.001°/hour), they must occasionally surface or use SLAM with seafloor terrain to correct accumulated position error.
- **Spinning tops and gyroscopic stabilizers**: a Steadicam camera stabilizer uses the gyroscopic resistance of a spinning flywheel to suppress camera shake. The flywheel maintains its orientation in space (precessing slowly) — this is the mechanical analog of integrating angular rate, with the same slow-drift property.

Exercises:

1. A gyroscope has a bias stability of 5°/hour and a noise density of 0.1°/s/√Hz at 100 Hz sample rate. After 10 minutes of integration, what are the expected contributions to angle error from (a) bias and (b) random walk (integrate noise)?
2. A complementary filter combines gyro and accelerometer with time constant τ = 1 second. Describe what happens to each input signal in a frequency band above and below 1 Hz.
3. Why can a gyroscope accurately measure yaw (rotation about vertical axis) while an accelerometer cannot correct yaw drift (even though it corrects roll and pitch drift)?

---

**Continue → [Why GPS Isn't Enough](27-why-gps-isnt-enough.md)**
