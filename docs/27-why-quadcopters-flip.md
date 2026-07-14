# Why Quadcopters Flip

## The Problem

You're tuning a quadcopter attitude controller. Roll and pitch seem stable. Yaw works. You decide to test a fast roll maneuver: command 45° roll to the right in 0.5 seconds.

The drone rolls right — then continues rolling past 90°, past 180°, completely inverts, and crashes into the floor. Total time: 0.8 seconds. The controller applied a roll correction the whole time. The IMU confirmed the drone reached 180°. The controller should have reversed the correction. It did — but 0.3 seconds too late, after the drone was already past the point of no return.

You look at the logs. The attitude controller was running at 100 Hz. The commands looked correct. The problem wasn't the controller logic or the update rate. Something in the physics was working against you.

Any robust attitude control system must:

- Handle the nonlinearity of large-angle rotations — angles don't add linearly
- Avoid gimbal lock: the loss of a rotational degree of freedom at specific orientations
- Represent orientation in a way that doesn't have singularities (mathematical undefined points)
- Execute controlled flips reliably, not accidentally

## What Would You Try?

- You roll 90° right, then pitch 90° forward. Where are you pointing? Now do the same operations in reverse: pitch forward 90°, then roll right 90°. Are you pointing the same direction? Why not?
- At exactly 90° pitch (nose straight up), what does "roll" mean? Can you still roll independently from yaw in this position?
- If the controller represents orientation as three separate angles (roll, pitch, yaw), what happens mathematically when pitch reaches exactly ±90°?

## Failed Attempts

### Attempt 1: Euler angles for attitude representation — simple and intuitive

Represent the drone's orientation as three angles: roll (φ), pitch (θ), yaw (ψ). Store these as three numbers. Update each by integrating the corresponding angular rate from the gyroscope.

This is intuitive and easy to display. Pilots think in roll/pitch/yaw. Euler angles work perfectly for small-angle maneuvers, which is most quadcopter flight.

But rotation in 3D is not commutative: roll-then-pitch produces a different orientation than pitch-then-roll. When Euler angles are updated sequentially (φ += φ̇·Δt, θ += θ̇·Δt), the sequential integration implicitly assumes a specific rotation order. For small angles, the order doesn't matter much. For large angles (aggressive maneuvers, 90° tilts), the order produces significant errors. The integrated angle does not correctly represent the actual 3D orientation.

Worse: when pitch θ reaches ±90° (nose straight up or straight down), the Euler angle update equations contain a division by cos(θ). At θ = 90°, cos(θ) = 0 — division by zero. The controller produces NaN (not-a-number) for roll and yaw rates. The IMU integration crashes, the attitude estimate is lost, and the drone falls. This is **gimbal lock** — a mathematical singularity that makes Euler angles unrepresentable at certain orientations.

### Attempt 2: Limit pitch to safe range, prevent the singularity

Add software limits: clamp pitch to ±85°. The drone will never reach the gimbal lock singularity.

This works for normal quadcopter operation, which rarely exceeds ±45° pitch. But the limit is a patch that doesn't address the underlying representation failure. If a wind gust pushes the drone to 86° pitch, the clamp fires — the attitude controller now disagrees with the IMU about what the drone's actual pitch is. The controller commands a correction back from 85° (its clamped belief) but the drone is actually at 86°. The error is small, but it breaks the closed-loop guarantee.

More importantly, you've now ruled out an entire class of useful maneuvers. Aerobatic drones, flipping drones, and applications requiring full 3D orientation (pointing a camera straight up or down) cannot work with a ±85° pitch limit. A representation with an artificial singularity is not suitable for a fully autonomous 3D vehicle.

### Attempt 3: Increase update rate to "outrun" the singularity

The flip happens because at 100 Hz, the controller is late by 0.3 seconds. Run at 1,000 Hz. The latency decreases to 0.03 seconds. Aggressive maneuvers complete before the singularity region causes problems.

Faster helps with latency. It doesn't fix the singularity. At 1,000 Hz, if the drone pitches to 89° and a gust pushes it one more degree, the Euler update equations still divide by cos(89°) ≈ 0.017 — amplifying angular rate noise by 60x. The controller output goes wildly wrong in 1 ms instead of 10 ms.

Speed doesn't eliminate mathematical singularities. It just moves them to faster timescales where they're harder to debug.

## The Discovery

The three attempts reveal that Euler angles are the wrong tool for the job, not a slightly imperfect right tool.

Rotations in 3D form a mathematical group — called SO(3) — with specific properties. Any representation of a 3D rotation using three numbers must have at least one singularity (by a theorem in topology: you cannot map a sphere onto a plane without tearing it). Euler angles chose specific singularity locations (pitch = ±90°). No choice of three numbers can avoid singularities entirely.

The fix: use a representation with more numbers. A rotation matrix uses 9 numbers to represent a 3D rotation without singularities — but it's expensive to update and enforce (it must remain orthogonal: R^T R = I). Four numbers suffice: a **quaternion**.

A quaternion is a 4-component number: q = (w, x, y, z), where w = cos(θ/2) and (x, y, z) = sin(θ/2) × (axis unit vector). The rotation axis and angle are encoded in a form that:

- Has no singularities: every 3D rotation is represented (twice, as q and −q represent the same rotation — "double cover" — but that's harmless)
- Updates by multiplication, not addition: q_new = q_old × δq (where δq is the incremental rotation from gyro data). Multiplication is well-defined everywhere.
- Normalizes trivially: enforce |q| = 1 after each update to prevent numerical drift

The attitude controller works in quaternion space: error quaternion = target_q × inverse(current_q). The error quaternion's vector part (x, y, z) is proportional to the rotation axis and angle needed to correct the attitude. Drive the motors to make this error quaternion approach (1, 0, 0, 0) — the identity rotation.

Flips are now mathematically straightforward: the drone passes through 90° and 180° continuously without any singularity. The Kalman filter tracking the quaternion state passes through all values of q without division by zero. Controlled 360° rolls, loops, and flips become numerically identical to any other rotation.

## Try It

<iframe src="../assets/browser/chapter27/index.html" width="100%" height="460" style="border:1px solid var(--md-default-fg-color--lightest);border-radius:8px;"></iframe>

[open in a new tab](../assets/browser/chapter27/index.html)

Before changing anything, predict:

- Command a 45° roll with Euler angle control. Does it complete cleanly? Now command 90°. Does the system behave differently?
- Switch to quaternion control and command a 180° roll (a flip). Does it complete? Does the controller lose track of orientation?
- Command pitch to exactly 90° (nose straight up) with both representations. What happens to the Euler controller's yaw response in this configuration?

## Implementation

`browser/common/engine.js` implements two parallel attitude estimators: one using Euler angle integration and one using quaternion multiplication. Gyroscope rates are integrated via dq/dt = 0.5 × q × [0, ω_x, ω_y, ω_z]. The quaternion is renormalized every update. The attitude controller error in quaternion mode is the vector part of (q_target)* × q_current. `browser/chapter27/index.html` shows both representations simultaneously during aggressive maneuvers.

## When It Breaks

**Quaternion unwinding.** Because q and −q represent the same rotation, the shortest path from q to −q in quaternion space is not always the shortest physical rotation. A controller driving from current orientation q to target orientation −q (same physical angle, opposite sign) will rotate the drone 360° the long way around instead of making no change. This must be detected by checking the sign of the dot product q_current · q_target; if negative, negate q_target before computing error. Many early quadcopter firmware implementations missed this and caused violent 360° spins when crossing the q/−q boundary.

**High-rate gyro integration drift.** Quaternion integration assumes small incremental rotations: δq ≈ [1, ω·Δt/2]. This first-order approximation is accurate for Δt < 1 ms and typical rotation rates. For very fast rotations (competition FPV drones at 2,000°/s) at 1 ms integration steps (1 kHz), the approximation introduces significant errors. Higher-order integration (Runge-Kutta, or computing δq exactly using the rotation-matrix exponential) is needed to maintain attitude accuracy during aggressive maneuvers.

## Transfer

- **Spacecraft attitude control**: the Apollo Guidance Computer used direction cosine matrices (rotation matrices, 9 elements) for attitude, avoiding Euler angles entirely. Modern spacecraft firmware uses quaternions; NASA's Generalized Attitude Control System (GACS) is quaternion-based.
- **3D game engines**: Unity, Unreal Engine, and virtually all professional game engines use quaternions internally for 3D rotation, even when displaying Euler angles to artists. The Transform.rotation field in Unity is a quaternion; the inspector shows Euler angles as a convenience.
- **Robotic surgery**: the da Vinci surgical robot's wrist joint can rotate continuously without singularities because its control software uses quaternion-based kinematics. This is essential for procedures requiring full 3D rotation of surgical instruments inside a body cavity.

Exercises:

1. A quadcopter is at pitch θ = 89°. Using Euler angle integration with a 1 kHz update rate, a 10°/s pitch rate is applied. Compute the roll angle update equation at this pitch angle and explain what happens numerically.
2. Convert the rotation "45° around the Z-axis" to a quaternion. What are the four components (w, x, y, z)?
3. Two quaternions q₁ = (0.707, 0.707, 0, 0) and q₂ = (−0.707, −0.707, 0, 0). Do they represent the same physical rotation? How should a controller detect and handle this ambiguity?

---

**Continue → [Why Hovering Is Hard](28-why-hovering-is-hard.md)**
