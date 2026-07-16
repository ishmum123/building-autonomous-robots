# Why Sensor Fusion Works

## The Problem

Your quadcopter carries a GPS receiver (position, ±2 m noise, 10 Hz), a barometer (altitude, ±0.5 m noise, 50 Hz), and an IMU with accelerometer and gyroscope (acceleration and angular rate, ±0.05 m/s² noise, 1000 Hz). Each sensor tells you something. None of them tell you everything. Together, they cover the full state of the drone (position, velocity, attitude) — but how?

The naïve approach: use GPS for horizontal position, barometer for altitude, gyroscope for attitude angles, accelerometer for linear velocity. Assign each sensor to one state variable. This actually works until it doesn't:

GPS drops out under a bridge. The horizontal position estimate freezes at the last GPS reading. The drone drifts laterally at 0.5 m/s; after 10 seconds of GPS outage, the frozen position is 5 m off. The drone crashes into the abutment while the controller insists it's holding position.

A sensor network where each sensor "owns" one state variable fails whenever any sensor fails. Any robust navigation system must:

- Maintain accurate estimates even when individual sensors drop out
- Combine redundant information (two sensors measuring overlapping quantities) to produce better-than-either-alone accuracy
- Propagate information across state variables (e.g., a velocity measurement improves a position estimate, and vice versa)
- Quantify its own uncertainty — knowing "I don't know" is as important as knowing the state

## What Would You Try?

- GPS measures position directly. The IMU measures acceleration, which is the second derivative of position. Can an acceleration measurement tell you anything about position? Over what timescale?
- You have two thermometers measuring the same room temperature. One reads 21.2°C, the other reads 21.8°C. Each has ±0.3°C noise. What is your best estimate of the true temperature? Is it one of them, or something else?
- If your GPS estimate has uncertainty ±2 m and your dead-reckoned (IMU-only) position has uncertainty ±0.5 m, which should you trust more? Does the answer change if the GPS had a valid fix 5 seconds ago versus 5 minutes ago?

## Failed Attempts

### Attempt 1: Assign each sensor a dedicated state variable

GPS owns horizontal position (X, Y). Barometer owns altitude (Z). Gyroscope owns attitude (roll, pitch, yaw). Accelerometer owns velocity (after integration).

This breaks at every sensor boundary. When GPS fails, the horizontal position estimate freezes. When the barometer has a spike (a gust of wind through the pressure port can cause 5 hPa spikes, equal to ~40 m of false altitude change), altitude control goes wild. There's no cross-checking: if the GPS says the drone is at 10 m east and the accelerometer's velocity integral says it's moving west at 0.5 m/s for 10 seconds, they'll disagree by 5 m with no mechanism to reconcile.

More importantly, information is left on the table. If the barometer says altitude is constant and the IMU's vertical acceleration channel shows zero net movement — both are saying the drone is not climbing, from different physical measurement principles. The fixed-assignment approach uses only one of these; the other is wasted.

### Attempt 2: Vote on each state variable using all available sensors

For altitude: average the barometer reading, the GPS altitude, and twice-integrated accelerometer altitude. Take three readings of "altitude" from three different sensors and median-vote or average them.

GPS altitude accuracy is ±5–10 m (far worse than horizontal GPS accuracy — the vertical geometry is poorly conditioned because all satellites are above the horizon). Twice-integrated accelerometer drifts at ~90 m per minute (Chapter 25). The barometer is ±0.5 m but has spike errors.

Averaging a ±0.5 m barometer with a ±10 m GPS and a wildly drifting IMU does not give ±0.5 m result — it gives something worse than the barometer alone. The accurate sensor is being polluted by the inaccurate ones. Averaging only helps when all sources have similar reliability. When they differ by an order of magnitude, averaging is counterproductive.

### Attempt 3: Use only the most accurate sensor for each state at each timestep

Rank sensors by accuracy. For altitude: barometer is best (±0.5 m), so always use barometer; ignore GPS altitude and IMU vertical. For horizontal position: GPS is best outdoors; optical flow is best indoors; switch between them based on environment detection.

This is a hybrid scheme — assign sensors dynamically rather than statically. It works in many practical applications. But it has a hard discontinuity: when you switch from GPS to optical flow, there's often a position "jump" because the two sensors have accumulated different offsets. And "switching" means discarding information at the moment of switch — during the switch, you have data from both sensors and you're using neither simultaneously.

The fundamental issue remains: information is not propagated optimally. If the barometer says altitude is dropping rapidly at 1 m/s and the GPS just gave a position fix 100 ms ago, these together constrain your vertical velocity and altitude better than either alone. You shouldn't have to pick one.

## The Discovery

All three approaches fail to answer a crucial question: what is the *best estimate* of the state given *all* available information simultaneously?

Consider the two thermometers. One reads 21.2°C (σ = 0.3°C). Another reads 21.8°C (σ = 0.3°C). The best estimate is not 21.2°C, not 21.8°C, and not simply (21.2 + 21.8)/2 = 21.5°C. The best estimate is the **noise-weighted average**: since both sensors have equal noise, the simple average 21.5°C happens to be correct. But if Sensor A has σ = 0.1°C and Sensor B has σ = 0.5°C, the best estimate is 0.96 × 21.2°C + 0.04 × 21.8°C = 21.22°C — almost entirely trusting Sensor A, with a tiny Sensor B contribution.

The weight assigned to each sensor is inversely proportional to its variance: w_i = (1/σ_i²) / Σ(1/σ_j²). This is the **minimum-variance unbiased estimator** for combining independent measurements. The resulting estimate has lower variance than either sensor alone: 1/σ_fused² = 1/σ_A² + 1/σ_B². Two sensors measuring the same thing always produces a better estimate than either alone, with gains proportional to the ratio of their variances.

For navigation, the state vector is multi-dimensional (position, velocity, attitude — 9+ variables) and sensors measure combinations of these variables. The GPS measures position. The IMU's accelerometer measures the second derivative of position. These are linked: if you know position and its second derivative, you can infer velocity better than from either alone.

This is **sensor fusion**: combine all available measurements, weighted by their uncertainties, to produce a minimum-variance estimate of the full state vector. The result:
- Is more accurate than any single sensor
- Gracefully degrades when a sensor fails (its weight decreases but others compensate)
- Propagates information across state variables (acceleration measurements constrain position)
- Carries its own uncertainty estimate, so the system always knows how confident it is

Formally, sensor fusion solves the inverse problem: given noisy observations of functions of the state, what state best explains all observations simultaneously? The Kalman filter (Chapter 30) does this optimally for linear, Gaussian systems.

## Try It

<iframe src="../assets/browser/chapter29/index.html" width="100%" height="460" style="border:1px solid var(--md-default-fg-color--lightest);border-radius:8px;"></iframe>

[open in a new tab](../assets/browser/chapter29/index.html)

Before changing anything, predict:

- Disable GPS. Does the fused position estimate immediately jump, or does it degrade gracefully? How many seconds before it becomes unusable?
- Set IMU noise to very high. Does the fused estimate degrade immediately, or does the fusion automatically reduce the IMU's weight?
- Two sensors have equal noise and both measure the same quantity. Does fusing them give twice the accuracy (half the noise), exactly √2 improvement, or something else?

## Implementation

`browser/chapter29/index.html` fuses IMU and GPS using a weighted blend: `fusedEst = fusedEst * (1 - fusionW) + gpsMeas * fusionW`, where `fusionW` is a slider and GPS updates arrive at `GPS_RATE = 30` ticks. The sim simplifies noise-weighted fusion to a single tunable blend weight — enough to show that leaning toward the lower-noise sensor reduces overall error. A strip plot compares absolute errors for IMU, GPS, and fused estimates; `browser/common/engine.js` supplies `addNoise` for both sensor models.

## When It Breaks

**Model mismatch corrupts the fusion.** The noise weight w_i = 1/σ_i² assumes you know σ_i correctly. If the GPS noise model says ±2 m but multipath is producing ±10 m errors, the fusion assigns GPS 25x more weight than it deserves. The fusion output is dominated by a bad reading that was labeled as a good reading. Robust fusion requires online noise estimation — continuously verifying that the sensor's actual error matches the model. Innovation monitoring (checking whether the GPS reading is consistent with what the filter predicted) can detect model mismatch.

**Correlated sensor failures.** Sensor fusion gains assume sensors fail independently. In a real drone, all sensors are mounted on the same board, powered by the same battery, and experience the same vibration. A severe vibration event can simultaneously corrupt the IMU (mechanical resonance), the barometer (pressure port vibration), and GPS (antenna cable connection). All sensors degrade together; the fusion algorithm that expected independent failures has no remaining independent sensors to weight against each other. Designing for correlated failures requires physically diverse sensor placement or different sensing modalities (not just different sensors measuring the same way).

## Transfer

- **Weather forecasting**: numerical weather prediction combines satellite observations, weather balloon soundings, surface stations, and aircraft weather reports — each with known noise characteristics — to produce an optimal initial state estimate for the forecast model. This is formal sensor fusion at planetary scale.
- **Medical imaging**: PET-CT scanners fuse positron emission tomography (metabolic activity) with X-ray computed tomography (anatomical structure). Neither alone gives complete information; the registered fusion identifies tumors that are metabolically active within specific anatomical locations.
- **The NASA Mars rovers**: Spirit, Opportunity, and Perseverance use visual odometry, wheel odometry, IMU, and star trackers to maintain position on Mars — where GPS doesn't exist. The redundancy and fusion architecture allowed Spirit to continue operating for 6 years when one wheel failed, because the fusion system compensated for the bad odometry from the dragging wheel.

Exercises:

1. Sensor A measures position with σ_A = 1 m. Sensor B measures position with σ_B = 3 m. Both read 5.0 m and 6.0 m respectively. Compute the noise-weighted fused estimate and its uncertainty σ_fused.
2. After GPS dropout, an IMU-only system drifts at 0.1 m/s (velocity error due to bias). If the fusion reduces GPS weight to zero, how does the fused position uncertainty evolve over time? Sketch the uncertainty growth curve.
3. Explain the difference between fusing sensors that measure the *same* physical quantity and fusing sensors that measure *different* physical quantities that are mathematically related. Which is more powerful? Why?

---

**Continue → [Why Kalman Filters Exist](30-why-kalman-filters-exist.md)**
