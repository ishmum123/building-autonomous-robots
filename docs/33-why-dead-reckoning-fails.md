# Why Dead Reckoning Fails

## The Problem

A submarine leaves Pearl Harbor on a classified mission. GPS doesn't work underwater. The sub navigates by dead reckoning: track speed and heading from inertial sensors, integrate to get position. After 3 days at sea, it needs to be within 500 m of a rendezvous point to receive a communication buoy.

The ship's inertial measurement unit has a gyro drift rate of 0.01 °/hour — extremely good by consumer standards. After 72 hours, heading error is 0.72°. At a transit speed of 15 knots (28 km/h), 72 hours of travel covers 2,000 km. A 0.72° heading error over 2,000 km produces a lateral position error of 25 km. The sub misses the rendezvous by 50 times the required tolerance.

And 0.01 °/hour is high-end military IMU quality. Consumer-grade gyros drift 1–10 °/hour. Any robot, drone, or vehicle navigating by inertial sensors alone faces this constraint:

- Small errors in rate measurements accumulate via integration into large position errors
- Position error grows with time — there is no equilibrium
- The drift rate is a property of the hardware; you can't compensate what you don't measure
- No combination of better integration math fixes a biased or noisy sensor

## What Would You Try?

- You have a gyro that drifts 0.01 °/hour and an accelerometer with a 0.01 m/s² bias. After 10 minutes of integrating these to get position, what is the rough position error from each? After 1 hour?
- Could you estimate the gyro bias from the sensor data itself? Under what conditions could you detect that the gyro is reading something other than true rotation rate?
- Dead reckoning works well for short time periods. At what time horizon does a high-quality IMU become unreliable, and what does "unreliable" mean precisely?

## Failed Attempts

### Attempt 1: Use higher-quality sensors

Buy better IMUs — military-grade fiber optic gyros with 0.001 °/hour drift instead of 0.01. This pushes the position error down by 10×. The sub example goes from 25 km to 2.5 km of error after 72 hours.

2.5 km is still five times the allowable error. Better sensors delay the problem but don't eliminate it. Error accumulation is unbounded: given enough time, even the best IMU produces arbitrarily large position error. And high-quality IMUs cost $50,000+ per unit — impractical for consumer drones. The fundamental problem is integration of a biased or noisy signal: no amount of hardware quality changes the mathematical fact that the error grows monotonically.

### Attempt 2: Calibrate the bias before the mission

Measure the gyro's bias before departing by holding it stationary and observing the output — it should read zero in a stationary frame. Subtract the measured bias from all subsequent readings.

This removes the static bias measured at room temperature in the lab. But IMU bias drifts with temperature, vibration, aging, and magnetic environment. A gyro bias calibrated at 20°C changes when the submarine descends into 4°C deep water. A drone's IMU bias shifts when the motors heat up nearby electronics. The calibrated bias is correct at the moment of calibration and wrong by a growing amount afterward. Temperature-compensated calibration tables help but don't eliminate the problem — they reduce the drift rate, which again delays rather than solves.

### Attempt 3: Integrate more carefully with higher-rate sampling

The standard integration X(t) = X(t-1) + V·Δt is first-order (Euler integration). Switch to fourth-order Runge-Kutta or higher-order methods that better approximate the true trajectory under changing velocity.

This reduces integration error from numerical approximation — but that's a different error from sensor noise. If the gyro is producing a reading of ω + ε_noise + ε_bias, no numerical integration scheme makes ε_noise or ε_bias disappear. They still accumulate. Higher-order integration is useful when the sensor is perfect and the trajectory is rapidly curving; it doesn't help when the sensor has a constant bias. Confusing numerical integration error with sensor error is a common mistake — they look similar in simulation but have completely different solutions.

## The Discovery

All three attempts treat dead reckoning as a problem of sensor quality or numerical method. They fail because the underlying problem is structural: **integration turns bounded sensor error into unbounded position error**.

The fix isn't better integration — it's periodic correction from an external reference that is not subject to accumulation. Measurements of the world — a GPS fix, a landmark match, a star sighting — give you position error directly, not velocity error. Correcting position error directly doesn't require integrating anything: you observe where you are, compare to where you think you are, and correct the discrepancy.

This leads to the architecture that actually works: dead reckoning fills the gaps between external fixes (where no other sensor is available), while external fixes reset the accumulated error before it grows too large. The allowable time between fixes is determined by the acceptable error budget and the IMU drift rate — a constraint that can be computed in advance.

The error accumulation formula for a gyro with drift rate σ is: position error ≈ (1/2) · σ · v · t², where v is speed and t is time since last fix. Working this formula backwards gives the maximum allowable fix interval for any required accuracy. This is **aided inertial navigation** — the foundation of every modern navigation system that must work in GPS-denied conditions.

## Try It

<iframe src="../assets/browser/chapter33/index.html" width="100%" height="460" style="border:1px solid var(--md-default-fg-color--lightest);border-radius:8px;"></iframe>

[open in a new tab](../assets/browser/chapter33/index.html)

Before changing anything, predict:

- Run pure dead reckoning for 60 seconds. Does position error grow linearly, quadratically, or randomly? Plot the error magnitude over time and observe the shape.
- Add a GPS fix every 10 seconds. How much does this reduce the maximum position error compared to pure dead reckoning? Try 30-second fix intervals — is the error the same as dead reckoning over 30 seconds?
- Increase the gyro drift rate by 10×. Does the position error grow 10× faster, or by a different factor?

## Implementation

`browser/chapter33/index.html` integrates dead-reckoning position inline: `drX += addNoise(trueVel, velNoise)` each tick, and resets to `gpsX = addNoise(trueX, 1.5)` every `GPS_RATE = 60` ticks. `browser/common/engine.js` provides `addNoise`; the integration and GPS correction are both inline in the HTML. The strip plot shows dead-reckoned position diverging between fixes and snapping back on each GPS update — the core mechanism of aided inertial navigation.

## When It Breaks

**GPS fix interruption in urban canyons.** Self-driving vehicles and delivery drones in dense urban environments lose GPS for 5–30 second stretches as buildings block satellite signals. Dead reckoning fills the gap — but the vehicle is moving at 15 m/s. A 30-second gap with consumer IMU drift of 1°/hour produces roughly 2 m of position error. For a lane-keeping system with 3.5 m lanes, this is marginal. Waymo and Cruise supplement IMU dead reckoning with wheel odometry and camera-based visual odometry to keep gap error below 0.3 m.

**Magnetic interference corrupts heading.** Magnetometers are often used alongside gyros to correct heading drift (geomagnetic north provides an absolute heading reference). Near steel structures, power lines, or other vehicles, the local magnetic field is distorted — the magnetometer reads a wrong heading, and correcting the gyro to this wrong reference makes things worse than gyro drift alone. The 2009 Perlan glider accident (loss of control) was partly attributed to corrupted compass readings near electrical equipment.

## Transfer

- **Ship navigation before GPS**: maritime navigators used celestial sights (star fixes) twice daily to reset accumulated dead reckoning error. The navigator's job was precisely managing when to take a fix and computing the error budget between fixes — the same calculus as aided inertial navigation.
- **Mars rover navigation**: Curiosity and Perseverance navigate with wheel odometry (dead reckoning) between visual landmark matches. On smooth rock, wheel odometry error is low; on slippery sand, wheel slip causes large dead reckoning errors. The rover's onboard SLAM (visual odometry) provides the periodic correction.
- **Pedestrian indoor navigation**: smartphones use IMU dead reckoning to navigate inside buildings where GPS is unavailable, but position error accumulates quickly. WiFi positioning and known staircase/elevator transitions provide the periodic resets that keep indoor navigation usable.

Exercises:

1. A gyro drifts 0.1 °/hour. A drone flies at 10 m/s. Estimate the position error (lateral deviation) after (a) 5 minutes, (b) 30 minutes, (c) 2 hours. At what time does error exceed 10 m?
2. If the allowable position error is 5 m and the gyro drift is 0.5 °/hour at a speed of 5 m/s, what is the maximum allowable interval between GPS fixes?
3. A calibration at 20°C measures a gyro bias of 0.05 °/s. At 5°C the bias becomes 0.08 °/s. If the drone flies for 10 minutes at 5°C using the 20°C calibration, what heading error accumulates from the uncorrected bias difference?

---

**Continue → [Why Robots Get Lost](34-why-robots-get-lost.md)**
