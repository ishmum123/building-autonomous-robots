# Why Sensors Disagree

## The Problem

Your drone carries two position sensors: a GPS receiver and a downward-facing optical flow camera that tracks ground features. They should both report the same position. They don't.

GPS says the drone is at (0.0, 0.0). Optical flow says it's at (0.8, −0.3). Two sensors measuring the same physical quantity — the drone's horizontal position — disagree by nearly a meter.

Which one is correct? You need to know immediately, because the drone's position controller is waiting for a position estimate to decide whether to apply a correction. If you use the GPS, you're potentially commanding against a correct optical flow reading. If you use the optical flow, you're potentially chasing a measurement error in the camera.

This isn't a broken sensor. Both sensors are working correctly. They're measuring different things and reporting them as the same thing.

Any multi-sensor navigation system must:

- Understand *why* sensors disagree before deciding how to combine them
- Distinguish sensor noise (random, averages out) from sensor bias (systematic, doesn't average out)
- Handle sensors with different update rates, different reference frames, and different physical quantities
- Know when to trust each sensor and how much — not a binary choice but a continuous weighting

## What Would You Try?

- Two sensors disagree by 0.8 m. You know both are "probably working." What would you need to know about each sensor to decide which to trust more?
- A sensor that's been accurate all morning suddenly reads 5 m off. Is it more likely to be a transient noise spike or a systematic failure? How would you tell the difference?
- If one sensor is fast but noisy, and another is slow but stable, can you define a combination that's both fast and stable? What tradeoffs does it require?

## Failed Attempts

### Attempt 1: Always use the "better" sensor

You know GPS is generally more accurate in open areas. Designate GPS as primary; ignore optical flow. If GPS fails, fall back to optical flow.

Flying indoors, GPS is unavailable — multipath makes the readings jump erratically. The fallback triggers; optical flow takes over. Optical flow works well on textured floors. On a white polished concrete floor (low texture), the camera can't track features; it reports drift at 0 m/s while the drone is slowly drifting sideways at 0.3 m/s. The fallback chose a sensor that happens to be wrong in this exact environment.

Designating "better" sensors ignores context-dependence. GPS is better outdoors, worse indoors. Optical flow is better on textured ground, worse on uniform surfaces. Altitude matters too: optical flow accuracy degrades at altitude because ground features appear smaller. There is no universally better sensor — only sensors that are better in specific conditions.

### Attempt 2: Average all sensor readings

If GPS says 0.0 and optical flow says 0.8, use 0.4. Take the average of all available sensors at every timestep.

When both sensors are reporting correctly (just with different noise levels), averaging improves accuracy — averaging reduces variance. But the GPS here has a multipath spike: its true value is 0.0, its reading is 2.5. Optical flow is correct at 0.8. The average is 1.65 — farther from the truth than either individual sensor. Averaging doesn't help when one sensor is systematically wrong; it pulls the estimate toward the wrong value.

Averaging also has no weighting by reliability. A barometer with 0.5 m altitude noise and a precision lidar with 0.02 m altitude noise get equal weight. The average is dominated by the barometer's noise. You've thrown away the information contained in the sensors' relative accuracy.

### Attempt 3: Majority vote — use the median

Three sensors: GPS (0.0), optical flow (0.8), visual odometry (0.2). The median is 0.2 — visual odometry. This discards the GPS outlier (0.0 was correct, but looks outlier-ish) and the optical flow reading and picks the "middle" sensor.

With three sensors and one outlier, majority voting works well. But with two sensors, there is no majority — the vote ties. And the median doesn't scale sensibly with noise: a sensor with 0.1 m noise and a sensor with 2 m noise vote equally in a majority scheme. The most accurate sensor might be in the minority on any given timestep purely by chance, and majority vote would discard it.

Majority voting also assumes the "wrong" sensor is clearly an outlier. When sensors disagree because they measure different things (GPS in the air vs. optical flow that tracks ground features at different heights), none of them is simply "wrong" — they're all providing different information that must be reconciled.

## The Discovery

The failed attempts treat sensor disagreement as a problem to be resolved by picking a winner. The insight is that disagreement is *information*.

Why do GPS and optical flow disagree? Because they have different error sources:

- GPS noise is random (±1 m, varies each reading, satellite geometry changes slowly)
- GPS bias in multipath environments is systematic (the reflection geometry creates a persistent offset)
- Optical flow error scales with altitude (at 5 m height, 1 pixel error = larger distance than at 1 m height)
- Optical flow has no global reference — it measures *displacement*, not absolute position; any starting error persists

Sensor noise is random — it averages out over multiple measurements. Sensor bias is systematic — it doesn't average out.

The correct approach is to model each sensor's error structure explicitly. For each sensor, estimate: what is its expected noise level? What is its expected bias? Under what conditions does it fail? Assign a **weight** to each sensor's reading proportional to its expected accuracy in the current conditions.

When sensors disagree by more than their expected noise, one of them may have a bias (GPS multipath, optical flow on uniform surface). The disagreement itself becomes a signal: if GPS and optical flow suddenly diverge after agreeing for 10 minutes, one of them has likely changed in reliability. A threshold on the disagreement magnitude can trigger a fault check.

This probabilistic approach — treating each sensor's reading as a sample from a probability distribution, and combining distributions optimally — is **sensor fusion**, the topic of Chapter 24. The disagreement between sensors is not a problem; it is data about the sensors' relative reliability.

## Try It

<iframe src="../assets/browser/chapter23/index.html" width="100%" height="460" style="border:1px solid var(--md-default-fg-color--lightest);border-radius:8px;"></iframe>

[open in a new tab](../assets/browser/chapter23/index.html)

Before changing anything, predict:

- Two sensors disagree by 1 m. Sensor A has noise σ = 0.5 m; Sensor B has noise σ = 0.2 m. Which sensor is more likely to be correct? What weights should the fusion use?
- Sensor A suddenly jumps to 5 m off while Sensor B stays constant. How long before a threshold test on disagreement detects this as an anomaly?
- Add a third sensor with high noise. Does the position estimate improve or degrade compared to two sensors? Why?

## Implementation

`browser/common/engine.js` provides `addNoise` to generate each sensor reading: `sA = addNoise(trueVal + biasA, noiseA)` and `sB = addNoise(trueVal + biasB, noiseB)`, with `noiseA`, `biasA`, `noiseB`, and `biasB` as slider-controlled parameters. The bias can be switched on mid-run to simulate multipath or surface-type changes. `browser/chapter23/index.html` plots sensor A, sensor B, and ground truth on a strip plot — the visual spread between the two lines shows why disagreement is inevitable and why it depends on noise and bias independently.

## When It Breaks

**Reference frame mismatch.** GPS reports position in WGS84 (Earth-centered, Earth-fixed coordinates, converted to latitude/longitude). Optical flow reports displacement relative to a local tangent plane. Lidar SLAM reports position in a local map frame. Converting between frames requires knowing the transformation — if the transformation is wrong (e.g., baro altitude slightly off, so the height of the floor map is wrong), sensors will appear to disagree even though both are measuring correctly. Frame misalignment is a common cause of sensor "disagreement" in multi-sensor systems.

**Time synchronization mismatch.** A vehicle moving at 5 m/s with 50 ms of timestamp misalignment between sensors experiences 0.25 m of apparent disagreement that's purely from timing. If the fusion algorithm assumes all sensor readings are simultaneous, it computes a wrong position. Industrial systems use hardware timestamping (PPS signals) to synchronize all sensors to a common time base. Consumer systems often rely on software timestamps, introducing jitter that manifests as phantom sensor disagreement.

## Transfer

- **Aircraft redundancy**: commercial aircraft have three independent air data computers (ADCs) reporting airspeed and altitude. In 2009, Air France 447 crashed when two of three pitot tubes iced over and reported different airspeeds; the flight computers couldn't determine which one was correct. The fusion system was designed for random failures, not correlated failures (all pitots failed for the same reason — ice).
- **Medical vital signs**: an ICU patient may have ECG (heart rate), pulse oximeter (SpO2), and arterial line (direct blood pressure) all measuring cardiac function. When they disagree, clinical staff assess which reading makes sense given the patient's clinical state — contextual, weighted disagreement resolution exactly like optimal sensor fusion.
- **Earthquake early warning**: seismic networks use dozens of geographically distributed sensors. A single sensor might read a large local noise event; the network uses spatial consensus — sensors that agree despite being separated by hundreds of km are likely measuring a real earthquake.

Exercises:

1. Three sensors report position: A = 10.2 m, B = 10.8 m, C = 9.9 m. Sensor A has σ = 0.5 m, B has σ = 0.3 m, C has σ = 0.4 m. Compute the noise-weighted average position estimate.
2. Sensor B suddenly reads 15.0 m while A and C remain around 10 m. At what reading value does B become a statistical outlier at the 3σ level? Should it be excluded from the fusion?
3. Explain why systematic bias is more dangerous than random noise in a sensor fusion system, and describe one method to detect sensor bias online.

---

**Continue → [Why Sensor Fusion Works](24-why-sensor-fusion-works.md)**
