# Why Accelerometers Lie

## The Problem

You're building an altitude-hold system for your drone. To hold altitude, you need to know if the drone is moving up or down. GPS updates too slowly (10 Hz) for tight altitude control, and barometers are noisy. An accelerometer seems perfect — it measures acceleration, and if you integrate twice you get position. At 1,000 Hz, you'll know exactly how the drone is moving through the air.

You test it indoors. You place the drone on a flat bench. The accelerometer reads 9.81 m/s² — straight up. The drone isn't moving. It's not accelerating. Why is it reading 9.81 m/s²?

You try to compensate: subtract 9.81 m/s² (gravity) from the reading. Now it reads 0 m/s². Good. You fly the drone. For the first few seconds, altitude integration looks reasonable. After 30 seconds, the integrated altitude says the drone is 40 meters high. It's actually at 5 meters. The integration has drifted wildly.

You try tilting the drone on the bench without lifting it. The accelerometer reading changes — it's no longer 9.81 m/s² straight up. But the drone hasn't moved. Why does tilting the drone change the acceleration reading even though the drone isn't accelerating?

Any accelerometer-based motion system must account for:

- The 9.81 m/s² gravity component that is always present, in any direction depending on tilt
- The impossibility of separating gravity from true acceleration using only accelerometer data
- Rapid error accumulation from integration of even tiny constant biases
- The sensor's response to vibration, which aliases into false acceleration signals

## What Would You Try?

- Your phone knows which way is "up" even when you tilt it. It uses an accelerometer for this. But how can "up" be determined from acceleration if the phone is also moving?
- If you knew the exact tilt of the drone at all times, could you correctly subtract gravity from the accelerometer reading? Where would you get tilt information?
- An accelerometer in free fall (drop it off a table) reads exactly zero. But the drone is accelerating at 9.81 m/s² downward. What does this tell you about what an accelerometer actually measures?

## Failed Attempts

### Attempt 1: Subtract gravity and double-integrate for position

The drone is level. The accelerometer reads 9.81 m/s² up. Subtract 9.81 m/s². Remaining signal: true acceleration. Integrate twice for position. This is dead reckoning from acceleration.

The problem emerges in the first 10 seconds of flight. An accelerometer has a bias error — a small, nearly constant offset from its true value. A typical MEMS accelerometer has a bias of 0.01–0.1 m/s² (after calibration). Integrate a 0.05 m/s² bias over 30 seconds once: velocity error = 1.5 m/s. Integrate again for position: 22.5 m of position error. From a sensor that reads "almost right" at every single moment.

Double integration is an error amplifier. The velocity error grows linearly in time; position error grows quadratically. After 1 minute, a 0.05 m/s² bias creates a position error of ~90 m. The drone is on the ground; the integrator says it's 90 m underground.

### Attempt 2: Use the gravity vector to infer tilt and subtract it

When the drone tilts, the gravity component distributes across the accelerometer's X, Y, and Z axes. If you can compute the tilt angle from those components — by finding the direction of the 9.81 m/s² gravity vector — you can subtract gravity correctly.

This works when the drone is stationary. The accelerometer reads a pure gravity vector; its direction tells you tilt precisely. But when the drone is accelerating horizontally, the horizontal acceleration adds to the horizontal component of the gravity vector. The sensor reads gravity + horizontal_acceleration. If you assume the reading is pure gravity, you compute the wrong tilt angle — you think you're tilting when you're actually accelerating, and vice versa.

During a 0.5 m/s² horizontal acceleration (a gentle cruise), the false tilt inferred is about 2.9°. This 2.9° false tilt then produces a false gravity subtraction error, which feeds back into the altitude estimation. Fast, sustained horizontal flight produces persistent false altitude readings even if the drone isn't climbing or descending.

### Attempt 3: High-pass filter to remove gravity

Gravity is a DC (zero-frequency) signal. True dynamic accelerations are higher frequency. Apply a high-pass filter to the accelerometer signal — this removes the constant gravity component, leaving only actual motion.

For vibration analysis, this works. But for navigation, the motions you care about — slow climbs, gentle tilts, gradual acceleration — are also low-frequency. The high-pass filter removes them along with gravity. You've filtered out exactly the information you needed.

Set the cutoff frequency to 0.1 Hz to preserve slow motions. Now the filter takes 10 seconds to fully suppress a gravity change caused by tilting. During a tilt maneuver, the gravity component bleeds through for 10 seconds before being suppressed. You've traded one problem (gravity aliasing) for another (transient gravity contamination for every maneuver).

## The Discovery

The three attempts fail because they're trying to separate two things that an accelerometer fundamentally cannot separate.

An accelerometer doesn't measure acceleration. It measures **specific force** — the non-gravitational force per unit mass acting on the proof mass inside the sensor. Gravity is an inertial force; in general relativity, a free-falling object is in an inertial frame and feels no force. The accelerometer in free fall reads zero because in Einstein's framework, free fall is the natural state — no force is acting.

When the drone sits on a bench, the bench pushes up on the drone to prevent it from free-falling. That's a real force of 9.81 m/s² upward — and the accelerometer correctly reads it. When the drone tilts, the direction of that support force changes relative to the sensor axes.

This means: **the accelerometer reading = (true_acceleration − gravity_vector) in the sensor frame**.

You cannot solve this equation for true_acceleration without knowing gravity_vector, and you cannot know gravity_vector without knowing tilt, and you cannot know tilt from the accelerometer alone (because accelerating horizontally produces the same sensor reading as tilting). The system is underdetermined.

The fix requires a second, independent source of tilt information — a gyroscope. A gyroscope measures rotation rate, not force; it's not confused by gravity or linear acceleration. With tilt from the gyroscope, you can correctly rotate the gravity vector into the sensor frame and subtract it from the accelerometer reading. The remaining signal is true linear acceleration, suitable (briefly) for dead reckoning.

"Briefly" — because gyroscopes drift too (Chapter 21). But that's a separate problem.

## Try It

<iframe src="../assets/browser/chapter20/index.html" width="100%" height="460" style="border:1px solid var(--md-default-fg-color--lightest);border-radius:8px;"></iframe>

[open in a new tab](../assets/browser/chapter20/index.html)

Before changing anything, predict:

- When the simulated drone is level and stationary, what does the accelerometer read? When it tilts 30° without moving, what does it read?
- Try integrating the "corrected" accelerometer output (gravity subtracted) for position. How quickly does the position estimate drift?
- Enable a gyroscope to provide tilt. Does gravity subtraction become accurate? Does the double-integrated position still drift?

## Implementation

`browser/common/engine.js` simulates the accelerometer as specific force: `accel = (true_accel - gravity_rotated_to_body_frame)`. The simulation includes a configurable bias offset and Gaussian noise. `browser/chapter20/index.html` shows both the raw accelerometer reading and the ground-truth acceleration to illustrate the specific force / gravity aliasing relationship.

## When It Breaks

**Vibration aliasing.** Quadcopter motors and propellers vibrate at frequencies from 50 to 400 Hz. MEMS accelerometers sample at 1–8 kHz; their analog bandwidth extends well past motor vibration frequencies. Vibration produces large-amplitude noise in the raw accelerometer signal that doesn't average to zero — mechanical resonances in the frame cause rectification, where symmetric vibration in acceleration space produces asymmetric readings due to sensor nonlinearity. ArduPilot flight controllers dedicate significant software effort to vibration filtering because vibration-contaminated accelerometers cause altitude oscillations and crashes in otherwise well-tuned vehicles.

**Sustained acceleration produces sustained tilt illusion.** A drone flying a sustained circular orbit is constantly accelerating centripetally. The accelerometer reads the centripetal acceleration as an apparent tilt. A naive attitude estimator using accelerometers for gravity reference will compute a wrong tilt during the turn, leading to a wrong gravity subtraction, leading to wrong velocity integration. This is why aircraft attitude systems use gyroscopes as the primary reference and accelerometers only as a long-term correction (Chapter 24).

## Transfer

- **Inertial navigation systems (INS)**: aircraft and missiles use accelerometers on precision-machined gyro-stabilized platforms to keep the sensor axes always aligned with inertial space — eliminating the rotation problem entirely. MEMS-based strapdown INS integrates gyro data to maintain the rotation matrix in software.
- **Smartphone step counting**: pedometers detect the periodic 1–2 Hz acceleration signature of walking rather than integrating for absolute position — a much more noise-robust use of the same sensor.
- **Apollo lunar module**: the LM had no GPS; it relied on a laser altimeter and INS for the final descent. The accelerometers needed sub-milli-g bias stability over the entire descent burn to maintain position accuracy within landing site tolerances.

Exercises:

1. An accelerometer has a bias of 0.02 m/s². Starting from rest, integrate twice for position over 60 seconds. What is the position error? At what point in time does the error exceed 1 m?
2. The drone tilts 15° while accelerating forward at 1 m/s². Draw the force diagram and compute what the accelerometer reads on each axis (X forward, Z up) in the body frame.
3. Explain why a free-falling accelerometer reads zero, even though the object is accelerating at 9.81 m/s² toward the Earth. What does this imply about the equivalence principle?

---

**Continue → [Why Gyroscopes Drift](21-why-gyroscopes-drift.md)**
