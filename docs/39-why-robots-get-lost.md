# Why Robots Get Lost

## The Problem

A hospital robot is delivering medications on floor 3. Its map shows four identical-looking corridors branching from the central hub — same width, same wall color, same length, same overhead lighting. The robot turned left at the last junction. It knows it turned left. But the sensor reading in this corridor is indistinguishable from the reading in the corridor three junctions back, which also required a left turn.

The robot's belief about its position has fractured: there are now four plausible positions it could occupy. Its map says "deliver to room 312, third door on the right." But which corridor is it in? If it's wrong, it knocks on a patient's door and hands medication to the wrong person.

This is the localization problem — not sensor failure, not dead reckoning drift, but structural ambiguity:

- Some environments contain places that look identical from the inside
- Sensor data alone can't distinguish them without additional context
- Past motion history contains the key — but only if it was tracked carefully
- A single wrong step can propagate through the full belief into a confident wrong position

## What Would You Try?

- The robot has turned left twice in a row to reach the current corridor. Of the four corridors in the hub, which ones are reachable by two left turns from the starting point? Does this narrow it down?
- You could add distinctive visual markers (colored tape, QR codes) to each corridor. This solves the ambiguity. Why might this be undesirable, and what if a marker is removed or covered?
- If the robot is equally likely to be in corridor A, B, C, or D, and it moves forward 2 meters and sees a specific door pattern, and this pattern is unique to corridor B, what should happen to its beliefs?

## Failed Attempts

### Attempt 1: Track position precisely enough that ambiguity never arises

Use high-resolution wheel encoders and an IMU to maintain exact position relative to starting point. If the robot knows it started at (0,0) and has moved with exact precision, it knows its map coordinates exactly — no ambiguity possible.

This is exactly dead reckoning (chapter 38), and it fails for the same reason: error accumulates. After 30 minutes of hospital rounds, 10-cm wheel slip from linoleum scuffs, and occasional spinning in place, the position estimate has drifted by 1–2 m. In a 1.5 m wide corridor, a 2 m position error means the robot's belief is a full corridor away from where it actually is. At that point, it thinks it's turning correctly while being in the wrong arm of the hub.

### Attempt 2: Match the current sensor reading to every location in the map

At each step, compare the current lidar scan to the expected scan at every grid cell in the map. Score each cell by how well the reading matches. The best-matching cell is the estimated position.

This is scan matching, and it works when the environment is distinctive enough. The hospital hub is specifically the case where it fails: the four corridors produce nearly identical scores because they are geometrically symmetric. The algorithm returns four equally-scored candidates. Picking the highest-scoring cell by a small margin gives you a fragile, unstable estimate that flips between corridors when the scores fluctuate with sensor noise. The algorithm is correct in principle; the environment simply contains an unresolvable ambiguity under current sensor input.

### Attempt 3: Maintain only a single best-estimate position

Run the scan matcher; when it returns a close tie between two corridors, pick one arbitrarily and commit. Then navigate using that committed estimate.

This is overconfident localization — sometimes called the "kidnapped robot" problem when the committed estimate is far from truth. Once committed to the wrong corridor, subsequent sensor readings are interpreted in the context of that wrong corridor. The robot is now building a wrong local model that makes the wrong corridor look like the right one, because the model predicts what it would see in the wrong corridor and confirms it. The system is confident and wrong, and the error doesn't self-correct — it entrenches.

## The Discovery

The three attempts fail because they try to collapse the robot's uncertainty into a single position before the data supports it. Premature commitment to one location in an ambiguous environment leads to the worst possible outcome: confident wrongness.

The insight: represent the robot's position not as a point but as a **probability distribution over all plausible positions**. When the environment is ambiguous, the distribution is multimodal — multiple peaks, one per plausible location. Don't collapse it. Carry all the peaks forward.

As the robot moves, each peak predicts where it would be after that motion — and the peaks spread slightly (uncertainty grows from odometry noise). When a new sensor reading arrives, it's scored against each peak: peaks that predict the wrong reading get downweighted; peaks in the right location get upweighted. After enough distinctive observations, only one peak survives.

This is **Monte Carlo Localization (MCL)**, also called the particle filter: represent the belief as a set of "particles" (position hypotheses), each weighted by its likelihood given recent sensor data. Resample: particles in wrong locations get eliminated; particles in right locations get duplicated. The distribution converges when the sensor data is informative.

The key property: the algorithm holds its uncertainty rather than eliminating it prematurely. In ambiguous environments, MCL correctly represents that the robot doesn't know which corridor it's in — and the distribution automatically resolves when distinctive evidence arrives.

## Try It

<iframe src="../assets/browser/chapter39/index.html" width="100%" height="460" style="border:1px solid var(--md-default-fg-color--lightest);border-radius:8px;"></iframe>

[open in a new tab](../assets/browser/chapter39/index.html)

Before changing anything, predict:

- Start the robot in the symmetric hub. Watch the particle cloud. Does it converge immediately, or does it remain spread across multiple corridors? What drives the convergence?
- Increase corridor symmetry (make corridors more identical). At maximum symmetry, does the particle filter ever converge, or does it remain ambiguous indefinitely?
- "Kidnap" the robot — teleport it to a new location while the filter thinks it's somewhere else. Watch how quickly the particle cloud recovers versus a single-estimate tracker.

## Implementation

`browser/chapter39/index.html` runs a real Monte Carlo Localization loop over a 1D corridor with four door landmarks. All three MCL steps live in the sim:

- `mclPredict`: each of the N particles advances by the commanded motion plus `gaussianRandom(motionNoise)`, spreading the cloud.
- `mclWeight`: for each visible door (within `SENSOR_RANGE`), the robot takes a noisy range measurement; each particle is scored via `gaussianLikelihood` — a Gaussian centered on the predicted range from that particle. Weights are normalized.
- `mclResample`: systematic resampling rebuilds the particle array proportional to weights, eliminating low-weight particles and duplicating high-weight ones.

`mclEstimate` computes the weighted mean of all particles. The left canvas shows dead-reckoning drift (noisy odometry, no corrections); the right shows the particle cloud (dot opacity and size reflect weight) converging to the true position as doors come into view. The strip plot compares absolute error of both estimates over time.

## When It Breaks

**Particle deprivation in highly constrained environments.** If the particle filter has converged to a wrong location and has very few particles near the true location, a distinctive observation that should update the belief finds no particles with good scores — all surviving particles are in the wrong place. The filter can't recover because the particles needed for recovery were resampled away. This is particle deprivation, and it's the MCL analogue of the committed-single-estimate failure. Adaptive sampling (adding random particles when filter confidence is inconsistent with observations) mitigates this.

**Symmetric environments never resolve.** An infinitely long corridor with no features is genuinely unresolvable — no amount of particle filtering determines position along the corridor without an absolute reference. The US Pentagon building is famous for this: its five identical corridors plus five identical rings mean visitors genuinely can't localize without landmarks. Robots deployed in truly symmetric environments (long underground tunnels, uniform pipe networks) require artificial landmarks or external positioning systems.

## Transfer

- **GPS positioning with multiple satellite geometries**: GPS works by finding the position that best explains signal timing from multiple satellites simultaneously. When satellite geometry is poor (all satellites in one part of the sky), the position estimate is a long ellipse of uncertainty — exactly the ambiguous posterior of MCL in a symmetric corridor. Good PDOP (position dilution of precision) = a compact posterior.
- **Medical imaging diagnosis under ambiguity**: radiologists maintain multiple diagnostic hypotheses simultaneously rather than committing to a single diagnosis early. They update each hypothesis as new images or lab results arrive — the same multimodal belief update as MCL. Premature diagnostic commitment is a named failure mode in medicine.
- **Criminal investigation**: detectives who commit to a prime suspect early exhibit confirmation bias — interpreting all new evidence in the context of the existing belief, exactly like a particle filter that has converged to a wrong location. Good investigative practice explicitly maintains multiple suspect hypotheses and updates them with evidence.

Exercises:

1. A particle filter has 200 particles spread across 4 equally-likely corridors. After one distinctive sensor reading that matches only corridor B, all particles in corridors A, C, D get weight 0.05 and particles in B get weight 0.8. How many particles will be in corridor B after resampling (approximately)?
2. The robot moves forward 1 m with odometry noise of ±0.1 m (1σ). Each of 100 particles receives a displacement sampled from N(1.0, 0.1²). After 10 such steps, how wide (1σ) is the position distribution if no sensor updates occur?
3. Describe a real indoor environment where MCL would converge quickly and one where it would remain ambiguous indefinitely. What geometric property distinguishes them?

---

**Continue → [Why SLAM Exists](40-why-slam-exists.md)**
