# Why Feedback Changes Everything

## The Problem

Your robot is supposed to hold a steady speed of 0.5 m/s while delivering packages through a warehouse. You program the motor to output exactly the power that corresponds to 0.5 m/s on a flat floor. 

On Monday: a slight uphill slope. The robot slows to 0.4 m/s.
On Tuesday: you add a 2 kg package. The robot slows to 0.35 m/s.
On Wednesday: battery drops to 70%. The robot slows to 0.32 m/s.

None of these disturbances were in your model. The controller doesn't know about them. It just keeps outputting the same command. The robot delivers packages 10 minutes late. The variable speed means it sometimes collides with shelving it was calibrated to avoid.

Any robust speed control must:

- Maintain target speed regardless of slope, load, or battery state
- Not require the programmer to know every possible disturbance in advance
- Respond in real time, not just correct after the fact
- Not overcorrect (creating oscillation as in Chapter 16)

## What Would You Try?

- If you measured the speed and compared it to your target, you'd know when you're off. What would you do with that information?
- The robot is going 0.1 m/s too slow. How much should you increase power? Does the answer depend on anything?
- If you increase power whenever speed is low and decrease it whenever speed is high, will the system always converge to the target? What could go wrong?

## Failed Attempts

### Attempt 1: Calibrate perfectly once

Measure the robot's speed at every power setting on a flat floor with no payload. Build a lookup table: target speed → motor command. Program this table into the controller.

This works perfectly in exactly the calibration conditions. Add any payload: lookup table gives wrong answer. Floor changes slope: wrong answer. Battery drains: wrong answer. Wheels wear down: wrong answer.

You extend the approach: calibrate for every combination of payload, floor angle, and battery level. The calibration matrix has hundreds of entries. You spend a week building it. Day one: a wheel picks up some dirt and changes its rolling resistance. The matrix is wrong again.

The failure reveals: the real world has more variables than any lookup table can capture, and those variables change over time. A controller that doesn't read the current state can't respond to the current reality.

### Attempt 2: Add a disturbance model

Measure the disturbances explicitly. Add a slope sensor (IMU), a payload scale, a battery voltage monitor. Compute the expected speed impact of each disturbance and add a feed-forward correction.

This works much better — measured disturbances are corrected. But any *unmeasured* disturbance still causes drift. And each new sensor adds cost, weight, complexity, and a new failure mode. When the slope sensor drifts, the correction makes things worse than no correction at all. Adding sensors forever is not a scalable strategy.

The failure reveals: you can never measure every disturbance. The fundamental limit is that you're modeling the world rather than reading the outcome. What you actually care about — the speed — is already measurable. Why not just measure that?

### Attempt 3: Measure speed and add a fixed correction

Read current speed. If speed is below target by 0.1 m/s, add some fixed amount to the motor command. Leave it there.

This corrects the speed — the motor command increases, speed goes up. But it doesn't stop at the target. The correction was sized for a 0.1 m/s error. As the robot approaches target speed, the error is less than 0.1 m/s, but the correction is still the full fixed amount. The robot overshoots.

Alternatively: the correction is small enough to avoid overshoot, but then it never quite reaches target — a persistent small error remains because the correction was sized for a large error.

The failure reveals: a fixed correction is only right for one specific error magnitude. What's needed is a correction that *scales with the current error* — large correction when far off, small correction when nearly there.

## The Discovery

Every failed attempt avoided the key question: what is the current error? 

Attempt 1 never asked. Attempt 2 asked about causes instead of symptoms. Attempt 3 asked once and stopped.

The actual solution asks continuously: what is the difference between where I want to be and where I am right now? And uses that difference — the **error** — to drive the correction at every instant.

This is **feedback control**: measure the output, compare to the target (compute error), generate a correction proportional to the error, apply the correction, then measure again. The loop closes: output → measurement → comparison → correction → output. Endlessly.

With proportional feedback: motor_command = baseline + K_p × (target_speed − measured_speed). When speed is low, error is positive, command increases. When speed is too high, error is negative, command decreases. The system doesn't need to know *why* speed is wrong — slope, payload, battery, wheel wear — it only needs to know *that* speed is wrong and by how much.

The magic: every disturbance the calibration approach needed to model explicitly is now handled *automatically* by the error signal. The feedback loop sees the effect of all disturbances in the single measurement.

The cost: feedback can oscillate (Chapter 16). The gain K_p must be chosen carefully — high enough to respond quickly, low enough to avoid overshoot. But this is a tunable tradeoff, not a fundamental barrier.

Formally: a proportional feedback controller with plant gain G and controller gain K has closed-loop transfer function: T = KG/(1+KG). As KG → ∞, T → 1 (perfect tracking). As K → 0, T → 0 (no response). The gain-bandwidth product is the fundamental design constraint.

## Try It

<iframe src="../assets/browser/chapter18/index.html" width="100%" height="460" style="border:1px solid var(--md-default-fg-color--lightest);border-radius:8px;"></iframe>

[open in a new tab](../assets/browser/chapter18/index.html)

Before changing anything, predict:

- With proportional-only feedback, can the system ever reach exactly the target speed, or will there always be a small steady-state error? Why?
- If you double the feedback gain K_p, does settling time halve? What happens to overshoot?
- Apply a step disturbance (sudden slope change). How does the feedback response differ from an open-loop response to the same disturbance?

## Implementation

`browser/common/engine.js` provides `Body`, `PID`, and `Vec`. `browser/chapter18/index.html` creates `openPlant` and `closedPlant` as `Body` instances and one `PID(kp, 0.1, 0.4, TARGET)`. Each frame the open-loop side applies a fixed `Vec(20, 0)` plus disturbance and drag, while the closed-loop side calls `pid.update(closedPlant.pos.x, 0.016)` for its force. A periodic `disturbance(t)` function drives both plants identically, making the feedback correction visible against the open-loop drift.

## When It Breaks

**Sensor noise amplification.** The feedback loop responds to the error signal. If the sensor measuring speed has noise, the controller treats noise as real error and applies corrections. High gain amplifies noise into actuator chatter — the motor command fluctuates rapidly even when speed is correct. This is why derivative control (which amplifies high-frequency noise) must be filtered, and why sensor quality matters as much as controller design.

**Latency-induced instability.** Feedback assumes you can measure the output and apply correction faster than the system can change. If the measurement-to-correction delay (sensor lag + computation time + actuator response) approaches the system's natural period, the correction always arrives one half-cycle late — and reinforces the error rather than correcting it. This is the phase margin problem in control theory. WiFi-controlled robots that must route commands through a cloud server often fail for exactly this reason.

## Transfer

- **Body temperature regulation**: your hypothalamus compares core temperature to 37°C and adjusts heat generation (shivering) and heat dissipation (sweating) based on the error. Pure feedback, no model of why temperature changed.
- **Cruise control in cars**: the ECU reads current speed, compares to set speed, adjusts throttle proportionally. Handles hills, headwinds, and grade changes automatically — a commercial product built on this exact mechanism.
- **Fly-by-wire aircraft**: the pilot's input is a *desired aircraft attitude*, not a direct control surface command. A computer measures actual attitude, computes error, and drives control surfaces accordingly. This is why modern airliners can fly at the edge of stall — the feedback loop corrects faster than a human pilot could.

Exercises:

1. A feedback controller has K_p = 5 and plant gain G = 0.4. What is the steady-state error as a fraction of a step input? (Use T = KG/(1+KG).)
2. The same system has a sensor that adds Gaussian noise with σ = 0.05 m/s. At K_p = 5, what is the RMS actuator command fluctuation due to noise alone? At K_p = 20?
3. Design a feedback controller for a thermostat heating a room. The room cools at 1°C per minute with heater off; heater adds 2°C per minute when fully on. Proportional control with what gain gives critical damping?

---

**Continue → [Why Guessing Isn't Control](19-why-guessing-isnt-control.md)**
