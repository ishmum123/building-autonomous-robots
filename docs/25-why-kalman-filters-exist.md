# Why Kalman Filters Exist

## The Problem

You're tracking a drone flying a straight horizontal path at constant velocity. Your radar gives position measurements every 100 ms with ±2 m noise. You want the smoothest, most accurate position estimate possible to hand off to an intercept calculation.

Simple approach: average the last 10 measurements. This reduces noise by √10 — noise drops from ±2 m to ±0.63 m. 

But the drone turns. The running average takes 10 measurements (1 second) to "forget" the old straight-line readings and adapt to the new direction. During the turn, your averaged estimate is a full second behind the actual position — potentially 15 m of lag at typical drone speeds. The radar is accurate but your estimator is slow.

You cut the window to 3 measurements — faster adaptation, but noise only reduces by √3 (±1.15 m). Every shorter window makes you noisier; every longer window makes you slower to react. There's no window length that gives you both.

And this is the simple case — constant velocity on a flat plane. Real navigation involves 3D position, 3D velocity, 3D attitude: 9 state variables. Some change fast (attitude), some change slowly (horizontal position). A fixed window can't adapt to different dynamics across different state variables.

Any optimal state estimator must:

- Produce the minimum-variance estimate at every timestep — no estimator with the same information can do better
- Track dynamics: use knowledge of *how the state changes over time* to predict where it will be next
- Update efficiently when measurements arrive, without re-processing all past data
- Handle the tradeoff between trusting the model and trusting the measurement on a principled basis, not by fixed parameters

## What Would You Try?

- The drone was at position X one step ago and had velocity V. You haven't received a measurement yet. What is your best guess of its current position? How confident should you be?
- A new measurement arrives and says the drone is at X + 1.5 m from your prediction. Your model says it should be at X. The measurement noise is ±2 m and your prediction uncertainty is ±1 m. Should you trust the measurement or the model more? By how much?
- After many updates with no measurement, does your uncertainty about the state grow, shrink, or stay the same? Why?

## Failed Attempts

### Attempt 1: Ignore the model — raw smoothing only

Use only measurements. Smooth them with a moving average or low-pass filter. This is a "measurement-only" estimator.

The moving average problem is already stated: fixed window = fixed tradeoff between noise and lag. A low-pass filter with fixed cutoff frequency has the same problem. If the drone's dynamics change — it suddenly accelerates — the filter has no way to know. It treats the sudden position change as noise and smooths it away. The estimate lags the truth by as much as the filter's time constant.

Worse, this approach ignores information you already have. You know the drone has mass: it can only accelerate so fast. You know it was moving at velocity V. The laws of physics say its next position is approximately X + V·Δt. Ignoring this and relying only on measurements discards information — you are guaranteed to produce a suboptimal estimate.

### Attempt 2: Trust the model completely — pure prediction, no measurements

Given initial position X₀ and velocity V₀, propagate forward using the physics model: X(t) = X₀ + V₀·t. Correct for any known forces (gravity, commanded thrust). Don't use noisy measurements at all.

This is dead reckoning: it works initially (when X₀ and V₀ are accurate) but drifts continuously. Any model error — unmodeled drag, wind, motor asymmetry — accumulates into position error without bound. After 30 seconds, even a small unmodeled acceleration of 0.01 m/s² produces a 4.5 m position error.

The model knows physics but doesn't know the world. Real forces on the drone include wind, turbulence, and battery voltage variations — none of which are in the "drone with constant velocity" model. Without measurements to correct model errors, any physical model drifts.

### Attempt 3: Weighted average of model and measurement at each step

At each timestep, compute a predicted position from the model. Receive a measurement. Take a weighted average: estimate = α × prediction + (1 − α) × measurement, where α is a fixed blend factor (e.g., 0.7).

This is better — it uses both model and measurement. But the fixed α is the same problem as the fixed window. During free flight with good model accuracy, α = 0.7 is reasonable: trust model 70%. After a sharp turn that the model didn't anticipate, the model is temporarily wrong; the measurement is more trustworthy. But α is fixed at 0.7 — you can't increase measurement trust because you don't know the model is wrong.

The fixed-α approach also doesn't track uncertainty. After 5 seconds of no measurements, the model prediction has drifted; your uncertainty is now higher — but the estimator doesn't know that and keeps blending at 70/30 as if it were just as confident as at startup.

## The Discovery

The three approaches fail because they use fixed parameters (window, cutoff, blend factor α) when the right parameters change every timestep.

The insight that breaks the deadlock: represent the state estimate not as a single number but as a **probability distribution** — specifically, a Gaussian with a mean (best estimate) and a variance (uncertainty). Both evolve with each prediction and update.

**Predict step**: use the dynamics model to project the estimate forward in time. The mean moves with the physics: X̂ = X̂_prev + V·Δt. The uncertainty grows, because the model is imperfect — unmodeled forces add noise. Uncertainty after predict = model uncertainty + process noise.

**Update step**: a measurement arrives. It is itself a Gaussian with mean = reading and variance = measurement noise σ². Now perform the optimal Bayesian update — multiply the prior distribution (from predict) with the measurement likelihood. This gives a new Gaussian:

- **Kalman gain**: K = P_prior / (P_prior + R), where P_prior is the predicted uncertainty and R is the measurement noise variance.
- **Updated mean**: X̂ = X̂_prior + K × (measurement − X̂_prior)
- **Updated uncertainty**: P = (1 − K) × P_prior

The Kalman gain K is the key: when P_prior is large (model uncertainty high, perhaps after GPS outage), K → 1 — trust the measurement fully. When R is large (measurement is noisy), K → 0 — trust the model more. The blend factor is computed automatically from the current uncertainty estimates at every step. No fixed α.

After many predict steps without measurement, P_prior grows → K grows → the estimator automatically gives more weight to the next measurement that arrives. After a good measurement, P shrinks → K shrinks → next prediction is trusted more. The filter self-tunes to the data.

This is the **Kalman filter**, developed by Rudolf Kálmán in 1960. It is the minimum mean-square error estimator for linear systems with Gaussian noise — no other algorithm with the same information can produce a lower-variance estimate. Apollo mission computers used Kalman filters for lunar trajectory estimation. Every modern aircraft navigation system, GPS receiver, and smartphone sensor hub uses variants of it.

The filter doesn't eliminate uncertainty. It tracks it — and uses it to optimally weight model versus measurement at every instant.

## Try It

<iframe src="../assets/browser/chapter25/index.html" width="100%" height="460" style="border:1px solid var(--md-default-fg-color--lightest);border-radius:8px;"></iframe>

[open in a new tab](../assets/browser/chapter25/index.html)

Before changing anything, predict:

- Increase measurement noise R. Does the Kalman estimate become closer to the model prediction or to the raw measurements? What happens to the Kalman gain K?
- Simulate a GPS outage (no measurements for 5 seconds). Does the filter's position estimate freeze, drift, or slowly diverge? Watch the uncertainty (P) during the outage.
- Set the process noise Q very high (model is untrustworthy). Does the filter now effectively ignore the model and just follow measurements? What does the Kalman gain do?

## Implementation

`browser/common/engine.js` provides `Kalman1D` for the predict-update cycle. `browser/chapter25/index.html` creates `kf = new Kalman1D(procNoise, measNoise)`, calls `kf.predict(1, VEL)` each tick and `kf.update(lastMeas)` on each noisy reading, then reads `kf.x` for the estimate. The strip plot shows raw measurement, Kalman estimate, and truth — the smoothing effect is visible immediately. The sim tracks covariance in `kf.p` but does not render a ±1σ envelope; the key insight — that a model-informed estimate beats raw measurement — is fully visible in the three-line comparison.

## When It Breaks

**Model mismatch (divergence).** The Kalman filter assumes the process noise Q correctly describes how much the model is wrong. If the drone performs a maneuver not in the model — a sudden sharp bank — the actual position deviates from prediction by more than Q predicts. The filter assigns the discrepancy to measurement noise, trusts the model too much, and slowly diverges. A filter that diverges becomes overconfident — P becomes very small (low uncertainty) while the actual error grows large. Divergence is insidious because the filter reports high confidence while being wrong. Adaptive Kalman filters estimate Q online by monitoring the innovation sequence.

**Non-Gaussian noise breaks optimality.** The Kalman filter is optimal only for Gaussian noise. GPS multipath produces non-Gaussian, heavy-tailed noise — occasional large outliers. A single 20 m multipath jump corrupts the Kalman state because the filter gives it significant weight (it's not expecting outliers). Robust Kalman extensions detect outliers by checking if the innovation (measurement minus prediction) exceeds several σ, and downweight or reject outlying measurements. This is called Mahalanobis distance gating.

## Transfer

- **Apollo 11 lunar navigation**: the Kalman filter was central to Apollo guidance computer software, written by MIT Instrumentation Laboratory. The filter fused star tracker measurements, ground radar, and onboard IMU to maintain trajectory accuracy during the 3-day trans-lunar coast.
- **Tesla Autopilot and every modern ADAS**: the sensor fusion pipeline in self-driving systems is essentially an extended Kalman filter (EKF) or unscented Kalman filter (UKF) applied to 3D tracking of surrounding vehicles — predicting their trajectories and updating from camera/radar measurements.
- **Financial state estimation**: the Kalman filter is used to estimate hidden economic state variables (e.g., inflation rate trends, yield curve factors) from noisy market observations — the mathematical structure of "model + noisy measurement" applies directly.

Exercises:

1. A Kalman filter has P_prior = 4 m² and measurement noise R = 1 m². Compute the Kalman gain K. If the measurement reads 12 m and the prediction is 10 m, what is the updated estimate?
2. After the update in exercise 1, what is the updated uncertainty P_posterior? Is it smaller than P_prior and smaller than R? Why must the fused uncertainty always be less than either input alone?
3. A drone undergoes constant acceleration that the Kalman filter model doesn't know about. Describe how the innovation sequence (measurement minus prediction) would behave over time, and what this signature could be used to detect.

---

**Continue → [Why Four Motors Beat One](26-why-four-motors-beat-one.md)**
