# Why Estimation Beats Measurement

## The Problem

A drone is trying to hold position at (50.0, 50.0) m. Its GPS reports position every second with ±3 m noise. At time t=10 s, GPS reads (52.1, 49.3) — 2.3 m east of the target. The controller corrects by flying 2.3 m west. At t=11 s, GPS reads (48.7, 50.4) — now 1.3 m west. It corrects east. The drone zigzags around the target, never settling.

At each step the controller trusts the raw measurement. At each step the measurement is noisy. The controller is chasing noise.

Now consider the same drone with a second sensor: an IMU that measures velocity at 100 Hz. Between GPS readings, the drone's velocity has been near-zero (it was commanded to hover). IMU says it moved about 0.1 m during the last second — far less than the 2.3 m GPS jump suggests. The GPS reading is probably dominated by noise. The true position is likely within 0.3 m of (50.0, 50.0), not at (52.1, 49.3).

No single measurement tells you the truth. **Estimation combines all available information — sensor models, dynamics models, past history — to produce the most informed inference about the true state:**

- Raw measurement noise can be orders of magnitude larger than the true signal variation
- Multiple sensors with independent noise can be combined to reduce effective noise
- A dynamics model constrains what positions are physically reachable — a constraint no sensor provides alone
- Confidence in the estimate (uncertainty) is as important as the estimate itself

## What Would You Try?

- You have GPS (1 Hz, ±3 m) and IMU velocity (100 Hz, ±0.01 m/s). How would you combine them? Which do you trust more at any given moment, and does that change over time?
- Between GPS readings, the drone must still know its position. How do you use velocity measurements to fill the gaps? What limits how long you can fill gaps this way?
- The drone has been hovering with almost no commanded motion for 5 seconds. A GPS reading shows 4 m of movement. Should you trust the reading or discount it? On what basis?

## Failed Attempts

### Attempt 1: Use only the highest-accuracy sensor

GPS with 3 m noise is worse than a good IMU-aided system. Replace GPS with a high-precision lidar altimeter (±0.01 m vertical) and camera-based horizontal positioning (±0.1 m). Use these alone.

Best-sensor-only ignores redundancy. When the lidar is blocked by rain, the positioning system fails completely. When the camera loses texture (uniform floor), horizontal position is unavailable. Single-sensor systems have single-sensor failure modes. The value of multiple sensors is not just accuracy — it's robustness: when one fails, others maintain the estimate. GPS + IMU + barometer + lidar together provide more reliable positioning than any single high-accuracy sensor, because the failure modes are independent.

### Attempt 2: Average all sensor readings at each timestep

At each timestep, average all available sensor readings. GPS says (52.1, 49.3); vision says (50.2, 50.1); IMU dead reckoning says (50.1, 50.0). Average: (50.8, 49.8).

Simple averaging ignores sensor noise differences. GPS is ±3 m; vision is ±0.1 m; IMU dead reckoning is ±0.2 m over this window. A simple average weights them equally — giving GPS (30× worse than vision) equal influence. The optimal combination should weight each sensor inversely by its variance. Naive averaging over-weights bad sensors and under-weights good ones. Worse, averaging sensors with different update rates is undefined: GPS updates at 1 Hz, IMU at 100 Hz. What do you average at 100 Hz when GPS has given one reading in the last second?

### Attempt 3: Trust the most recent reading, regardless of source

Whenever a new reading arrives, update position to that reading. Most recent reading is most current.

This produces the zigzag behavior in the problem statement. "Most recent" is not "most informative." A GPS reading from 0.1 seconds ago with 3 m noise is less informative about true position than an IMU-based prediction from 0.01 seconds ago with 0.2 m uncertainty. Recency is not accuracy. And the "most recent reading" approach can't use information from multiple sensors simultaneously — it sees only the last one. If GPS updates at 1 Hz and IMU at 100 Hz, this approach throws away 99 out of 100 IMU readings.

## The Discovery

All three approaches fail to use available information optimally: the first ignores redundancy, the second ignores noise levels, the third ignores history.

The insight (from chapter 25, applied specifically here): the optimal combination of multiple noisy measurements is a **weighted average where each weight is proportional to the inverse of the measurement's variance**. This is the BLUE (Best Linear Unbiased Estimator) for static problems. For dynamic problems with a motion model, it's the Kalman filter.

For the GPS + IMU case specifically: **predict** the position using IMU velocity integration (high rate, low latency, but drifts); **update** with GPS when it arrives (low rate, high latency, but absolute). The Kalman gain automatically computes how much to trust each — and that trust changes over time based on accumulated uncertainty.

This beats any single measurement because:

1. **Redundancy**: independent noise sources partially cancel when combined optimally
2. **Complementarity**: IMU is good at short-term, high-rate dynamics; GPS is good at long-term absolute reference. Neither alone is sufficient; together they cover each other's failure modes
3. **Uncertainty tracking**: the estimate comes with an uncertainty (covariance P), which tells you how confident to be — and drives downstream decisions

The broader principle: **estimation is inference, not measurement**. A measurement is a raw sensor reading. An estimate is the posterior distribution over the true state given all available information. Every decision should be made from estimates, not raw measurements — because only estimates incorporate everything you know.

## Try It

<iframe src="../assets/browser/chapter43/index.html" width="100%" height="460" style="border:1px solid var(--md-default-fg-color--lightest);border-radius:8px;"></iframe>

[open in a new tab](../assets/browser/chapter43/index.html)

Before changing anything, predict:

- Compare raw GPS versus Kalman-filtered GPS for a hovering drone. Does the filtered position track nearer to truth? What happens to the controller's zigzag behavior?
- Disable GPS (simulate outage). Does the estimate immediately collapse, or does the IMU integration maintain useful accuracy for some seconds? How does uncertainty (P) grow during the outage?
- Add a large GPS outlier (multipath spike: GPS reads 15 m off truth). Does the filter absorb it, or does it corrupt the estimate? Compare the response of a raw-measurement controller versus the Kalman filter.

## Implementation

`browser/chapter43/index.html` runs GPS + IMU fusion with a discrete Kalman filter, showing the raw GPS readings, the IMU dead-reckoning position, and the fused estimate simultaneously. `browser/common/engine.js` implements the standard predict-update cycle as in chapter 25, extended to 2D position + velocity state. The uncertainty ellipse (1σ covariance) is rendered around the estimate — watch it shrink on GPS update and grow during GPS outage. The position controller uses the filtered state, not raw GPS, and the reduction in control chattering is visible.

## When It Breaks

**Correlated sensor errors break the independence assumption.** The Kalman filter assumes GPS and IMU errors are uncorrelated. In an aircraft, GPS signal multipath is worst near the ground (runway) — the same time that vibration is high, which corrupts the IMU accelerometers. Both sensors degrade simultaneously, in the same direction. The filter assumes these are independent events and fuses them with false confidence. Aircraft navigation systems address this with integrity monitoring — comparing the two estimates; if they disagree beyond a threshold, the fusion result is flagged as unreliable.

**Filter tuning is fragile.** The Kalman filter requires accurate Q (process noise) and R (measurement noise) matrices. These are usually determined by offline calibration. If the real-world noise changes (GPS degrades in urban canyons, IMU noise increases with temperature), the tuned filter is wrong. An overconfident Q makes the filter slow to track real motion. An overconfident R makes the filter chase noise. Adaptive filters (estimating Q and R online from the innovation sequence) are more robust but add complexity and can themselves be miscalibrated.

## Transfer

- **Weather forecasting ensemble methods**: modern weather prediction runs 50+ simulations with different initial conditions and model parameters. The ensemble mean is the estimate; the ensemble spread is the uncertainty. No single simulation is trusted — the optimal forecast is the weighted combination. This is estimation over measurements in the sense that no single simulation output is taken as true.
- **MRI image reconstruction**: raw MRI signals are noisy k-space measurements. The final image is a maximum-likelihood estimate of tissue density given all acquired k-space data — not any individual measurement. Compressed sensing MRI reduces scan time by acquiring fewer measurements and using estimation to recover the full image from them.
- **Radio telescope aperture synthesis**: VLBI (Very Long Baseline Interferometry) combines observations from telescopes on different continents to estimate the brightness distribution of a distant radio source. No single telescope has sufficient resolution; the estimate from their combination (as implemented in the 2019 first-ever black hole image) exceeds what any individual measurement could provide.

Exercises:

1. GPS has noise σ_GPS = 3 m. Vision has noise σ_vision = 0.2 m. Compute the optimal fusion weights (proportional to 1/σ²). If GPS reads 52 m and vision reads 50.1 m, what is the fused estimate?
2. The fused estimate in exercise 1 has combined uncertainty σ_fused. Compute σ_fused using the formula 1/σ²_fused = 1/σ²_GPS + 1/σ²_vision. Compare σ_fused to each individual sensor's noise. Is the fused estimate better than both individually?
3. During a 10-second GPS outage, the drone uses IMU dead reckoning with velocity noise 0.05 m/s per second (random walk). After 10 seconds, what is the 1σ position uncertainty from dead reckoning? (Hint: position uncertainty from velocity random walk grows as σ_position = σ_vel × √t × Δt.)

---

**Continue → [Why Decisions Need Models](44-why-decisions-need-models.md)**
