# Why Quadcopters Need Two Brains

## The Problem

You've built a quadcopter and implemented a single feedback loop: GPS position in, motor commands out. The drone should hold position at (0, 0, 5m). The wind pushes it to (2, 0, 5m). The controller sees 2 m of error and increases front motor thrust to fly back.

Fifteen seconds later, the drone has returned to (0.1, 0, 5m) — nearly correct on position. But it's tilted 25° forward. The front motors are working hard, rear motors barely running. The battery is draining fast. A gust hits from the side and the drone tips over completely.

The problem: the position controller doesn't know the drone's orientation. It commanded "fly left" by increasing left motors — but never verified the drone was actually level. Position control and attitude control are completely different physical tasks running on completely different timescales. A controller that tries to do both at once does neither well.

Any stable flight system must:

- Keep the vehicle upright (attitude) at 50–200 Hz — tipping takes less than half a second
- Hold position (navigation) at 1–20 Hz — position drift is slower
- Allow these two objectives to pursue different goals simultaneously without fighting each other
- Handle the coupling: to move horizontally you must tilt, so position control *requires* attitude control as a tool

## What Would You Try?

- Staying upright and staying in place are both "control problems" — but on different timescales. Can the same controller handle both without compromising on either?
- A drone tilts 30° forward in response to a wind gust. How quickly must the attitude controller react before the drone falls? How does this compare to the speed at which position changes?
- If the position controller's output could be a desired tilt angle rather than a motor command, what would the attitude controller need to do with that? Why might this be cleaner than the position controller commanding motors directly?

## Failed Attempts

### Attempt 1: One fast controller handles both

Run the control loop at 200 Hz — fast enough to stabilize attitude. Use GPS position error to generate motor commands directly, at the same 200 Hz rate.

GPS updates at 10 Hz. So for 19 out of every 20 controller cycles, the position error is stale — the controller is repeating the same command it sent 100 ms ago. When the GPS does update, the jump in measured position (from measurement noise alone, ±1 m for consumer GPS) causes a sudden large change in the motor command. The drone jerks.

Meanwhile, at 200 Hz the controller is trying to respond to position *and* attitude simultaneously. When a gust tilts the drone 10°, the position error is still 0 (the drone hasn't moved yet) — so the position controller does nothing about the tilt. The drone continues tilting. By the time position error builds up from the tilt, the drone is already at 30° and falling.

One fast loop reading slow position data misses attitude dynamics entirely.

### Attempt 2: One slow controller handles both

Reverse approach: slow down to 10 Hz to match the GPS update rate. At each update, compute motor commands from position error plus some tilt compensation based on the IMU.

The IMU tilt compensation helps — the controller now knows the drone is tilting. But at 10 Hz, the control loop takes 100 ms to respond. Drone angular dynamics have a natural frequency around 5–10 Hz — meaning the drone can complete a significant tilt within one controller cycle. A drone starting to tip at 10°/s will be at 11° by the time the next control command fires. At 20°, control authority starts to diminish. At 45°, the drone is falling.

Attitude dynamics are simply too fast for a 10 Hz loop. Running both at 10 Hz is running attitude control at a frequency below the instability threshold.

### Attempt 3: One controller with separate gains per axis

Instead of one setpoint and one output, use a 6-dimensional controller: three position axes, three orientation axes. Tune separate gains for position (slow) and orientation (fast). The controller runs at 200 Hz but only uses the GPS data when it's fresh.

This is closer, but the coupling breaks it. To move north (increase X position), the controller increases front motor speed. This also increases the pitch angle — the drone tilts backward from the torque imbalance. The 6D controller now has both a position error (still haven't moved north yet) and an attitude error (pitched back) — and both are driving the same motors. The corrections interfere. Increase front motor to move north; now pitched backward, so controller adds pitch correction (decrease front, increase rear) which fights the north command. The drone barely moves and oscillates in attitude.

A single controller can't independently command position and attitude when both use the same actuators — unless the output space is formally decoupled.

## The Discovery

The three attempts keep failing because they try to solve a fundamentally coupled problem in one place. The coupling has a specific structure though: to move in a direction, the drone must tilt in that direction. This means position control *requires* attitude control as a subroutine, not as a competitor.

Once you see this, the architecture becomes obvious: make the position controller's output the attitude controller's setpoint.

**Attitude loop** (inner, 100–200 Hz): reads the IMU (roll, pitch, yaw angles and rates). Computes motor differential to drive the drone toward the commanded attitude. Knows nothing about GPS. Runs fast enough to catch any tipping before it compounds. Output: four motor throttle values.

**Position loop** (outer, 5–20 Hz): reads GPS and barometer. Computes the tilt angle that would produce the desired acceleration toward the waypoint. Outputs a roll setpoint, pitch setpoint, and total thrust command — which become the inputs to the attitude loop.

The coupling is now handled explicitly: "to move north, I need to pitch forward 8° — attitude loop, please achieve 8° pitch." The attitude loop treats "8° pitch" exactly like any other setpoint. The position loop doesn't care how the motors achieve 8° — it just verifies the drone ends up where it should be.

Each loop is independently stable. The position loop can be slow because it only needs to update as fast as position changes — and the inner loop makes the attitude response look essentially instantaneous at those timescales. This is the **two-loop quadcopter architecture**: inner attitude loop, outer position loop, connected by attitude setpoints.

## Try It

<iframe src="../assets/browser/chapter23/index.html" width="100%" height="460" style="border:1px solid var(--md-default-fg-color--lightest);border-radius:8px;"></iframe>

[open in a new tab](../assets/browser/chapter23/index.html)

Before changing anything, predict:

- If you disable the attitude loop and let the position loop command motors directly, how does the drone's behavior change when a tilt disturbance is applied?
- Slow the attitude loop update rate from 200 Hz to 20 Hz. Does the drone remain stable? At what rate does it start to tip uncontrollably?
- Apply a constant sideways wind. Which loop corrects it — inner, outer, or both? What does each loop "see" as its error?

## Implementation

`browser/common/engine.js` provides `Quadcopter`, `PID`, and `Vec`. `browser/chapter23/index.html` wires the two loops inside `stepB(q, altPid, attPid)`: it calls `altPid.update(q.body.pos.y, 0.016)` for the altitude command and `attPid.update(q.body.angle, 0.016)` for the torque correction, then passes both to `q.setMotors(baseThrust - torqueCmd, baseThrust + torqueCmd)`. The left panel (`stepA`) runs altitude-only so both panels start with the same 0.3 rad tilt; the side-by-side shows how the attitude PID (`attB`) damps the tilt while the altitude-only drone spirals away.

## When It Breaks

**Attitude loop failure causes immediate crash.** If the attitude loop fails (sensor fault, software exception, computation overload), the position loop's attitude setpoint goes unexecuted. The drone is now in open-loop attitude — any tilt goes uncorrected. Time to crash from hover: typically under 1 second. Real autopilots implement attitude loop health monitoring with immediate motor kill on failure, because a free-falling drone is safer than an uncontrolled one.

**Bandwidth separation degraded by aggressive outer loop.** When a user commands a fast position change (e.g., racing mode, sharp waypoint transition), the outer loop generates a large, fast-changing attitude setpoint. If the attitude loop's bandwidth is not at least 5–10x higher than the outer loop command rate, the attitude loop cannot track the setpoint — effectively, the inner loop is the bottleneck. Racing drones handle this by running inner loops at 8 kHz and tuning extremely aggressive inner-loop gains, accepting some noise amplification as the price of responsiveness.

## Transfer

- **Helicopter fly-by-wire**: early helicopters required pilots to manually manage both heading and position. Modern fly-by-wire helicopters have an inner attitude stabilization loop so the pilot commands attitude angle, not rotor pitch — radically reducing workload.
- **Submarine depth control**: an inner buoyancy/trim loop maintains level attitude; an outer depth loop commands the angle to dive or surface. A submarine that tried to control depth without first controlling attitude would immediately start rotating.
- **Robotic arms**: joint angle control (inner loop) executes Cartesian end-effector position commands (outer loop). The Cartesian planner doesn't need to know motor dynamics.

Exercises:

1. The outer position loop for a quadcopter runs at 10 Hz and commands pitch angles up to ±20°. What minimum inner loop bandwidth (in Hz) is required to ensure the attitude tracks the position command without introducing more than 10° of lag?
2. A single-loop controller is replaced by a two-loop cascade. Name two benefits and one new failure mode introduced by the cascade architecture.
3. Explain why the tilt angle commanded by the position loop scales with the horizontal acceleration needed, not the horizontal position error directly.

---

**Continue → [Why Robots Need Senses](24-why-robots-need-senses.md)**
