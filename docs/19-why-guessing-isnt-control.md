# Why Guessing Isn't Control

## The Problem

Chapter 18 introduced feedback — measuring speed and correcting the error. It felt like the complete solution. But something is missing.

You build a robot that must drive exactly 2 meters forward and stop. You have a speed feedback controller that holds 0.5 m/s perfectly. You run the motor for exactly 4 seconds (2 m ÷ 0.5 m/s = 4 s). Stop.

Measure: the robot is at 1.85 meters. You try again. 1.92 meters. Again: 1.88 meters.

The speed is controlled. The time is controlled. But position is wrong. And the error is different every time.

The speed controller can't see position. It measures speed and corrects speed. There's no position feedback. Without position measurement, the robot is integrating speed over time and hoping the integral equals the target distance — which it approximately does, but never exactly.

Any position control must:

- Drive the robot to a specific position, not just hold a specific speed
- Correct position error, not just speed error
- Handle cases where the same command produces different positions (motor variation, surface variation, slip)
- Not accumulate errors across multiple moves

## What Would You Try?

- You have a speed controller that works. Can you build a position controller *on top of* it, using it as a black box?
- The robot doesn't know where it is. What would you need to add to the robot to let it know?
- If you added an encoder (measures wheel rotation) and a compass (measures heading), could you determine position? What could still go wrong?

## Failed Attempts

### Attempt 1: Calibrate time-to-distance precisely

The robot moves at a known speed. Run it for precisely the right duration to cover the target distance. The calibration test shows 4.02 seconds gives exactly 2 meters. Program 4.02 seconds.

This works on day one. On day two: the floor is slightly rougher and the robot travels 1.94 meters in 4.02 seconds. On day three: the battery is 80% charged and the speed controller compensates but the actual speed drifts slightly — 2.06 meters. And if the robot must navigate a non-trivial path, the time integration error from each segment adds up.

The failure reveals: time integration of speed is an open-loop estimate of position, not a measurement of it. Even with perfect speed control, any speed uncertainty integrates into growing position uncertainty.

### Attempt 2: Count wheel rotations (dead reckoning)

Attach a rotary encoder to the drive wheel. Each encoder tick is a known distance. Count ticks, multiply by distance-per-tick, get position. This is **odometry** or **dead reckoning**.

This is far better than time integration and is standard on real robots. But it accumulates error: any wheel slip during acceleration adds phantom distance; any encoder skip misses real distance; surface irregularities cause microvariations in effective wheel radius; turning maneuvers accumulate heading error. Over 2 meters, odometry error might be 2–3%. Over 20 meters, it might be 20–30 cm. Over 200 meters, the robot may be completely lost.

The failure reveals: odometry is *relative* position estimation — it knows how far it has moved but not where it started, and errors in every step accumulate without correction. There's no mechanism to discover and correct the drift.

### Attempt 3: Add a forward model (simulate the system)

Build a mathematical model of the robot: given motor commands, predict the resulting motion. Run the model in parallel with the robot. The model predicts where the robot should be; if the real robot matches the model, assume position is correct.

This sounds clever but is equivalent to dead reckoning with extra steps. The model is only as good as its parameters (motor constant, wheel radius, friction). Any mismatch between model and reality accumulates. And the model has no way to detect when reality has diverged — it has no connection to the ground truth.

The failure reveals: a model without external reference is self-confirming. It tells you what *should* have happened, not what *did* happen. Control requires measurement of reality, not prediction of it.

## The Discovery

All three attempts computed position from the motor's inputs — how long it ran, how many times the wheel turned, what the model predicted. None of them measured position directly.

The gap between "measuring inputs" and "measuring position" is the distinction between **open-loop** and **closed-loop position control**. Speed control in Chapter 18 was closed-loop because it measured the *output* (speed). Position control requires measuring the *output* (position) and feeding that back.

For the warehouse robot, this means adding a position sensor: a camera with landmark recognition, ultrasonic beacons, laser rangefinder against known walls, or GPS outdoors. The sensor provides ground truth. The controller computes position error = target − measured, and applies a correction — not to the motor directly, but to the speed setpoint, which is itself feedback-controlled. This is a **cascade controller**: an outer position loop sets the speed target for an inner speed loop.

The fundamental insight is: **you cannot control what you do not measure**. Any quantity that matters to the mission must be in the feedback loop. Speed control without position sensing produces accurate speed but drifting position. Position sensing closes the loop that speed sensing leaves open.

Formally: in state space, the robot's state is (position, velocity). A controller that only measures velocity controls one state variable and is open-loop in the other. Full state feedback requires measuring (or estimating) all state variables that matter.

## Try It

<iframe src="../assets/browser/chapter19/index.html" width="100%" height="460" style="border:1px solid var(--md-default-fg-color--lightest);border-radius:8px;"></iframe>

[open in a new tab](../assets/browser/chapter19/index.html)

Before changing anything, predict:

- The simulation shows a robot with open-loop position control and one with closed-loop. Apply a random disturbance to both. How does each respond over time?
- If the position sensor has 2 cm of noise, what does the position error look like under feedback control? Is it better or worse than open-loop?
- What happens to closed-loop position control if the sensor fails mid-move?

## Implementation

`browser/common/engine.js` provides `Body`, `PID`, and `Vec`. `browser/chapter19/index.html` creates two `Body` instances (`guesser` and `measurer`) and one `PID(kp, 0.05, 0.3, TARGET)`. Each frame the guesser receives a fixed `Vec(fixedForce, 0)` plus the wind `gust(t)`, while the measurer calls `pid.update(measurer.pos.x, 0.016)` for its force command. Both bodies receive the same gust, making the divergence between open-loop drift and closed-loop correction directly comparable.

## When It Breaks

**Sensor lag introducing position error.** A position sensor with latency τ reports where the robot *was* τ seconds ago. At 0.5 m/s with 100 ms sensor lag, the feedback loop is correcting for a position error measured 5 cm back. At high speed this lag causes systematic overshoot — the controller always thinks the robot is behind where it actually is, and overcorrects. This is particularly acute in camera-based localization with image processing delay.

**Aliasing between position estimates.** If the robot uses two sensors with disagreeing position estimates (e.g., odometry and GPS), the fusion algorithm must decide which to trust and how to blend them. A naive fusion that averages the two can produce a position estimate that matches neither, confusing the controller. The Kalman filter was designed specifically to handle this problem.

## Transfer

- **CNC machines**: a CNC mill must position its tool to ±0.01 mm. Stepper motors (open-loop) are acceptable for some work; servo motors with linear encoders (closed-loop position feedback) are required for precision. The distinction is exactly position feedback vs. none.
- **Surgical robots**: a da Vinci surgical arm must hold a position accurately in the presence of the surgeon's hand tremor (filtered out) and tissue forces (disturbances). Position feedback at millisecond rates makes this possible.
- **Mars rovers**: GPS doesn't work on Mars. Curiosity and Perseverance use stereo cameras and visual odometry to estimate position on Mars, accumulating error that is periodically reset by triangulating against known landmarks in orbital imagery.

Exercises:

1. A robot uses odometry with 2% distance error and 0.5° per meter heading error. After a 10-meter straight run and a 90° turn and another 10-meter run, estimate the position error in x and y.
2. Design a cascade controller for position control: the outer loop outputs a speed setpoint, the inner loop controls speed. If the inner loop has bandwidth 10 Hz, what is the maximum outer loop bandwidth for stability?
3. A GPS sensor provides position with 1 m accuracy at 1 Hz. Wheel encoders provide relative position with 1% error at 100 Hz. Describe (without equations) how you would combine these to get the best position estimate at 100 Hz.

---

**Continue → [Why Errors Accumulate](20-why-errors-accumulate.md)**
