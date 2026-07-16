# Why Faster Isn't Better

## The Problem

Your robot arm needs to move to a target position. You have a motor with plenty of power. You command maximum speed. The arm shoots toward the target — and blows past it. You reverse the command. It overshoots the other way. After three or four oscillations it finally settles.

You try again with less power. The arm creeps toward the target, takes twice as long, but settles smoothly on the first approach.

This feels wrong. More power, more speed — shouldn't that be strictly better? The fast arm covers the distance in half the time. Why does it take longer to *settle*?

Something about the relationship between speed and control is not what it seems. Getting there fast and getting there precisely are not the same problem, and pursuing one can actively undermine the other.

Any control design must:

- Reach the target within an acceptable position error
- Settle without sustained oscillation
- Work across different target distances (not just one fixed trajectory)
- Not require arbitrarily long settling time

## What Would You Try?

- If the arm overshoots the target, is that a problem with the motor or with the controller's decision about when to slow down?
- Sketch the position vs. time curve for: (a) maximum speed command until arrival, then brake; (b) gradual deceleration starting halfway through. Which arrives first? Which settles first?
- Is there a speed above which settling becomes impossible regardless of how smart the braking is?

## Failed Attempts

### Attempt 1: Full speed ahead, brake hard at arrival

Command maximum torque the entire way. When position = target, reverse torque to stop.

The arm arrives at the target with maximum velocity. Braking requires decelerating the arm's inertia. For the same torque used to accelerate, the deceleration distance equals the acceleration distance (assuming symmetric torque limits). If the arm is already at the target when braking begins, it needs to travel one "braking distance" past the target before stopping — and then the position error is a full braking distance in the wrong direction. The arm is now at -1 braking distance and must repeat the process. Oscillation is guaranteed.

The failure reveals: arriving at the target with non-zero velocity guarantees overshoot. The velocity must be zero, or very nearly zero, precisely at the target. This requires starting to brake *before* arrival.

### Attempt 2: Start braking at the halfway point

A symmetric profile: accelerate for the first half of the distance, decelerate for the second half. This minimizes the time to reach the target with zero final velocity — the classic "bang-bang" or trapezoidal velocity profile.

This works perfectly for a *single fixed distance* in a system with no perturbation. But in practice: if a disturbance bumps the arm mid-motion, the halfway point is wrong; if the payload changes, the braking distance changes; if the initial position is slightly off, the final position is slightly off with no opportunity to correct. The control has no feedback — it trusts a pre-computed trajectory and any error accumulates without correction.

The failure reveals: pre-planned profiles are open-loop. They can be perfectly timed in theory but cannot respond to reality. A robot that actually needs to reach a precise position in the presence of disturbances needs to be measuring position continuously and adjusting commands accordingly.

### Attempt 3: Proportional control — command speed proportional to remaining distance

Instead of fixed commands, use feedback: command = k × (target - current_position). The closer to the target, the slower the commanded speed. Simple, elegant.

At large distance: high commanded speed (good — moves fast). At small distance: low commanded speed (good — approaches gently). Seems to solve both problems.

The catch: inertia. Even though the *command* drops as the arm approaches the target, the arm has accumulated velocity from the fast approach phase. The actual speed is not the commanded speed — it is whatever the motor and inertia produce in response to the command history. Near the target, the command says "go slow" but the arm is still going fast. The arm overshoots — less than in Attempt 1, but still overshoots. The gain k determines the trade: high k means fast approach but overshoots; low k means slow approach but settles cleanly.

The failure reveals: proportional control ignores velocity. The arm's actual state includes both position and velocity. A controller that only knows position is missing half the picture.

## The Discovery

Every attempt failed because velocity was ignored. The arm at maximum speed crossing the target doesn't care what the position command says — it will continue moving until torque changes momentum. You can't command position; you can only command acceleration (via torque), which changes velocity, which changes position.

The implication: to smoothly arrive at a target, the arm needs to be *slowing down* as it approaches. The ideal profile has velocity exactly proportional to the remaining distance — so as distance → 0, velocity → 0 simultaneously. This is exponential approach: position error decays like e^(-t/τ).

Achieving this requires knowing both current position and current velocity. With only position feedback (proportional control), the controller reacts too late. A controller that also considers velocity can dampen the approach: if the arm is moving fast toward the target, reduce commanded torque earlier.

This is **damping**: a force that opposes velocity, not position error. The system has two energy stores (potential = position error × spring-like restoring force, kinetic = ½mv²) and needs dissipation to drain kinetic energy before arrival. Without dissipation, energy sloshes between potential and kinetic — oscillation. With sufficient damping, kinetic energy is drained before overshooting.

Formally: the response of a second-order system is characterized by the damping ratio ζ. At ζ < 1 (underdamped): oscillation before settling. At ζ = 1 (critically damped): fastest settling without overshoot. At ζ > 1 (overdamped): no overshoot but slower than critical. Maximum speed during approach must be budget against settling time via ζ.

## Try It

<iframe src="../assets/browser/chapter16/index.html" width="100%" height="460" style="border:1px solid var(--md-default-fg-color--lightest);border-radius:8px;"></iframe>

[open in a new tab](../assets/browser/chapter16/index.html)

Before changing anything, predict:

- At what gain does the system transition from underdamped (oscillating) to overdamped (creeping)?
- If you increase mass (more inertia), does the same gain give more or less damping?
- What is the minimum settling time achievable, and what parameters determine it?

## Implementation

`browser/common/engine.js` provides `Body`, `PID`, and `Vec`. `browser/chapter16/index.html` creates two `Body` and two `PID` instances (`pidA` with `kpLow`, `pidB` with `kpHigh`), then each frame calls `plantA.addForce(new Vec(pidA.update(plantA.pos.x, 0.016), 0))`, applies a fixed drag `plantA.addForce(plantA.vel.mul(-0.5))`, and steps with `plantA.step(0.016)`. The side-by-side layout shows how raising `kp` from ~1.5 to ~8 turns a smooth approach into persistent oscillation.

## When It Breaks

**Structural resonance excited by control bandwidth.** If the robot arm has a flexible joint or link, the control system can excite its mechanical resonant frequency. The arm controller tries to correct position error — but its corrections arrive at the flexible mode's resonant frequency, pumping energy into vibration rather than damping it. This is input shaping's entire purpose: design the motion profile to have zero spectral energy at the structural resonance frequency.

**Actuator saturation.** The analysis above assumes the motor can deliver any commanded torque. Real motors saturate at peak torque. A critically damped controller designed around linear motor behavior becomes underdamped when the motor saturates during the deceleration phase — it can't brake as hard as assumed, so it overshoots. Anti-windup strategies in the controller address this.

## Transfer

- **Car suspension tuning**: the suspension spring stores energy, the damper dissipates it. Underdamped suspension (like a sports car with stiff springs and weak dampers) bounces over bumps. Overdamped suspension (too much damping) makes the car feel sluggish. Critically damped gives the fastest return to level without bounce.
- **Galvanometer in instruments**: a D'Arsonval movement (needle meter) needs critical damping so the needle settles to the true reading without oscillating. Manufacturers add small eddy-current damping vanes specifically for this.
- **Camera autofocus**: the lens must move from current distance to target focus distance as fast as possible without hunting. Voice coil actuators in autofocus systems use critically-damped trajectories computed from measured scene distance.

Exercises:

1. A spring-mass system has m = 0.5 kg and k = 200 N/m. What is the undamped natural frequency ω_n? What damping coefficient c gives critical damping (ζ = 1)?
2. A proportional controller with gain K_p gives a closed-loop natural frequency of 10 rad/s but ζ = 0.3 (underdamped). Adding derivative gain K_d changes ζ to 1.0 without changing ω_n. Qualitatively, what is K_d doing?
3. A 5 kg robot arm must move 0.2 m and settle within 1 mm in under 0.5 s. Estimate the minimum required peak torque assuming a trapezoidal velocity profile with symmetric acceleration and deceleration phases.

---

**Continue → [Why Everything Oscillates](17-why-everything-oscillates.md)**
