# Why Errors Accumulate

## The Problem

Chapter 18 showed that feedback eliminates the effect of disturbances on speed. Chapter 19 showed you need position feedback to control position. Now you have both.

The robot has a proportional speed controller and a proportional position controller in a cascade. You run it to a 2-meter target. It gets to 1.96 meters and stops. A 4 cm error. You run it again — same result. The error is repeatable, which means it's not noise. Something systematic is wrong.

You add weight to the robot. The error gets larger: 7 cm. You run it uphill. Error: 11 cm. The pattern is clear: there is a persistent, steady-state error that scales with the constant forces opposing the robot (gravity on a slope, extra weight, rolling resistance). Proportional feedback is not eliminating it.

Any position controller that must hold or reach a precise target must:

- Drive position error to zero, not just reduce it
- Handle steady constant disturbances (gravity, friction, constant loads) that don't go away
- Not oscillate while doing so
- Remain stable when the disturbance suddenly disappears

## What Would You Try?

- A proportional controller applies correction proportional to error. At steady state, the correction exactly balances the disturbance. What does this mean the error *must* be at steady state?
- If the error must be non-zero to sustain a correction force, how could you modify the controller to sustain a correction force even when error is zero?
- A memory-less controller can only respond to current error. What kind of memory would let it "remember" accumulated past error?

## Failed Attempts

### Attempt 1: Increase proportional gain

The steady-state error is 4 cm. The correction force is K_p × 4 cm. That correction exactly balances the disturbance. If you double K_p, the same correction force is produced by only 2 cm of error. Steady-state error halves.

Keep increasing K_p: error approaches zero. But the system becomes increasingly oscillatory (Chapter 16). High K_p means a large correction for any small error — including the overshoot of trying to correct. At some gain, the system becomes unstable. You're trading steady-state accuracy for transient instability.

More fundamentally: no finite K_p ever achieves zero steady-state error when there's a constant disturbance. There will always be *some* residual error producing the correction force. Zero error requires infinite gain, which means infinite instability.

The failure reveals: proportional control has an inherent steady-state error under constant load. The error is not a tuning problem; it's a structural property of the controller. No gain setting resolves it.

### Attempt 2: Add a constant feed-forward term

If you know the disturbance — say, the weight of the payload creates a known friction force — add a constant offset to the motor command. The feed-forward exactly cancels the known disturbance, leaving the proportional controller to handle only deviations.

This works for *known, fixed* disturbances. But:
- The payload weight changes every delivery
- The floor slope changes room by room
- The wheel friction changes as wheels wear

Any feed-forward that isn't updated in real time is just a one-time calibration — which is Attempt 1 from Chapter 18. And now you've added complexity (you must measure or estimate the disturbance) without solving the general problem.

The failure reveals: feed-forward requires knowledge of the disturbance in advance. A controller that doesn't know the disturbance identity can't feed it forward. We need a mechanism that accumulates knowledge of the disturbance from observing its effect.

### Attempt 3: Sample-and-hold: memorize the correction that worked

When the system reaches steady state, latch the current motor command and hold it. Now the motor command doesn't depend on current error — it's the value that worked last time.

Run again. The motor holds the latched value. If conditions are identical to last time, it works. But load changes: the latched value is now wrong, and there's nothing to update it. The error persists because the holding mechanism is not connected to the current state.

The failure reveals: what's needed is not a stored value from the past run, but a value that is *continuously updated by current error*. It should grow when error is positive, shrink when error is negative, and stabilize when error is zero — which means it stores the *integral* of error over time.

## The Discovery

Every approach failed because they tried to cancel the disturbance with a fixed value. The disturbance is constant but unknown, and its effect — a persistent error — is exactly the signal you need to drive the correction.

The key insight from Attempt 3: the correction needed to cancel a constant disturbance is itself a constant. If you could *accumulate* error over time, the accumulated sum would grow until it's large enough to cancel the disturbance — and then stop growing (because error becomes zero). The accumulated value stays large enough to cancel the disturbance even after the error reaches zero.

This is the **integral term**: I_term(t) = K_i × ∫₀ᵗ error(τ) dτ.

When there's a constant error: the integral grows continuously. The correction grows. The error shrinks. As error shrinks, the integral grows more slowly. When error reaches zero, the integral stops changing — but it has already accumulated enough value to cancel the disturbance exactly.

The integral "charges up" against any constant error and holds that charge indefinitely. As long as conditions don't change, the stored integral value exactly cancels the disturbance, leaving zero steady-state error.

This is why integral control (the "I" in PID) is essential for any system that must precisely hold a target against constant forces: motor control fighting gravity, temperature control fighting ambient heat loss, pressure control fighting a constant leak. Adding I to a proportional controller eliminates steady-state error — at the cost of a slower, more oscillatory response (Chapter 21 will address how to balance all three terms).

Formally: total controller output = K_p·e(t) + K_i·∫e(t)dt. The integral term has dimensions of (output units × time) and acts like an accumulator that removes steady-state bias.

## Try It

<iframe src="../assets/browser/chapter20/index.html" width="100%" height="460" style="border:1px solid var(--md-default-fg-color--lightest);border-radius:8px;"></iframe>

[open in a new tab](../assets/browser/chapter20/index.html)

Before changing anything, predict:

- With only P control and a constant uphill slope, what is the steady-state position error? Does it depend on K_p?
- When you enable integral action, how long does it take for the accumulated integral to cancel the slope disturbance?
- If the robot reaches the top of the hill and the slope becomes flat, what happens to the stored integral? What does the robot do?

## Implementation

`browser/common/engine.js` is not involved in the control logic here; this sim uses plain scalar state variables. `browser/chapter20/index.html` maintains `trueX`, `estXNone`, and `estXCorr` as scalars, integrating `(trueVel + velBias) * 0.016 * 10` each frame for the biased estimate, and applying a proportional correction `correctionGain * (trueX - estXCorr)` every 60 frames to mimic a GPS fix. The strip plot overlays all three traces to make accumulating drift visible against the periodic correction.

## When It Breaks

**Integrator windup.** If the robot is blocked from reaching its target (physically stopped against a wall, or actuator saturated), the error remains non-zero and the integral accumulates without limit — "winds up." When the block is removed, the integral has charged to an enormous value that drives the system far past the target before unwinding. Anti-windup schemes clamp the integral when the actuator is saturated, preventing this.

**Integrating away valid signals.** The integral averages out everything, including legitimate sudden changes. If the target position changes rapidly, the integral "remembers" where it used to be and resists the new target — dragging the response behind. Systems that must track fast-changing setpoints (like a gun turret tracking a fast aircraft) are sometimes run without integral control, accepting small steady-state error to avoid integral lag.

## Transfer

- **Thermostat with integral action**: a thermostat with only proportional control holds a room at 70°F when it's 68°F outside but 71°F when it's 40°F outside (steady-state error from the larger heat loss). Adding integral action keeps the room at exactly 70°F regardless of outdoor temperature — the integral charges up to compensate for greater heat loss.
- **Aircraft altitude hold**: altitude autopilot must hold a target altitude despite updrafts and downdrafts. Proportional-only would leave the plane at slightly wrong altitude under any constant vertical air movement. Integral term maintains exact altitude regardless.
- **Chemical process pH control**: pH systems have very slow dynamics. Proportional control with zero steady-state pH error requires infinite gain (impractical). Integral control slowly accumulates reagent addition to hit the target pH exactly, even though the disturbance (feed concentration) is constantly changing.

Exercises:

1. A PI controller (no derivative) has K_p = 3 and K_i = 0.5. A constant disturbance of 10 units is applied. What steady-state error does the P term produce? What does the I term accumulate over 10 seconds to exactly cancel it?
2. Integrator windup: the actuator is saturated at 100 units. The error is 20 units and K_i = 2. The integral charges for 30 seconds before the disturbance is removed. How large is the integral value at that point, and what does this imply for the overshoot when the block is removed?
3. A system has fast disturbances (changing 10× per second) and slow bias (a constant offset). Design a hybrid controller: proportional for fast response, integral for slow bias, with a low-pass filter on the error before integration. What cutoff frequency separates "fast" from "slow" in this context?

---

**Continue → [Why PID Was Invented](21-why-pid-was-invented.md)**
