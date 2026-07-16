# Why One PID Isn't Enough

## The Problem

You've equipped your drone with a single PID controller that commands motor throttle directly from position error. You want to fly the drone to a waypoint 50 meters north. The controller sees the drone is 50 m off target and outputs maximum throttle. The drone tilts forward and accelerates.

Here's the problem: the drone is now moving at 12 m/s and the waypoint is only 5 meters away. The single controller still sees 5 m of error — it's still outputting forward thrust. The drone blows through the waypoint, now it's 5 m past it on the other side, controller reverses — the drone oscillates back and forth around the target indefinitely, every overshoot as bad as the last.

You dial down the gain to reduce oscillation. Now the drone creeps toward the target and barely overshoots. But "barely overshoots" at low gain means responding slowly to a 10 m/s crosswind gust. The drone gets blown far off course before the sluggish controller corrects.

Any robust position control system must:

- Respond quickly to large disturbances without overshooting
- Handle position and velocity simultaneously — knowing *where* and *how fast* the vehicle is moving
- Not require the same gain to work well at slow approach speeds and at high speeds
- Remain stable across the full operating envelope (hover, cruise, aggressive maneuvering)

## What Would You Try?

- A single controller must produce one output (throttle) from one input (position error). But position and velocity are different things — one is where you are, one is how fast you're moving there. Can one PID "see" both at once?
- When a drone is 5 m away but moving at 12 m/s toward the target, what should the controller do? What information would tell you to start decelerating?
- Imagine two specialists: one whose only job is keeping the drone pointed the right direction, and another whose only job is deciding which direction to point. Could they work together without colliding?

## Failed Attempts

### Attempt 1: One PID, velocity from derivative term

The PID derivative term differentiates position error, which is essentially velocity. So a single PID *already knows* velocity — the D term is velocity feedback. Just tune K_d high enough to dampen the overshoot.

Set K_d = 2.0. The overshoot reduces significantly on a clean run. Then a small gust pushes the drone slightly off course — the position sensor noise spikes. The derivative of that noise spike is enormous: a 0.3 m position jump in 50 ms = 6 m/s apparent velocity. K_d = 2.0 fires a 12 N correction for a sensor artifact. The drone lurches.

More fundamentally: the derivative term sees the *rate of change of error*, not the true vehicle velocity. If the wind is also changing the setpoint (in a mission with moving targets), the derivative term conflates target motion with vehicle velocity. And the single loop must work at all speeds: the gain that damps a 12 m/s approach smoothly is far too aggressive for a 0.5 m/s hover adjustment.

### Attempt 2: Lower gain plus feed-forward velocity

Add a feed-forward term: command = K_p × position_error + K_ff × desired_velocity. The desired velocity is computed from a trajectory planner that tells the drone how fast it should be moving toward the target. This bypasses the overshoot problem — the drone "knows" to decelerate because the trajectory says so.

This works beautifully on the planned trajectory. But feed-forward only corrects expected errors. A lateral wind gust isn't in the trajectory plan. The position drifts sideways; the feed-forward term adds nothing because the gust wasn't planned. The low-gain proportional term corrects slowly. Meanwhile the drone has drifted 3 m laterally while "perfectly following" its planned velocity profile.

Feed-forward is not feedback. It doesn't close the loop against real-world disturbances — it just pre-shapes the command. Any deviation from the plan requires the proportional term to fix, and a low proportional gain means slow correction.

### Attempt 3: High-frequency single PID sampling faster

Maybe the problem is loop rate. If the controller reads position 500 times per second instead of 50, it catches velocity changes before they cause overshoot — effectively the same as a faster derivative.

Faster sampling does help, marginally. But the fundamental issue isn't sampling rate — it's that position and orientation are different physical quantities with different dynamics. The drone's position changes slowly (it has mass, it accelerates and decelerates over seconds). Its tilt angle changes fast (the rotors can change attitude in 50–100 ms). A single controller that updates throttle from position error can't simultaneously respond to tilt dynamics fast enough to maintain stability, because the tilt time constant is 10–20x faster than the position time constant. Sample at 500 Hz and the position loop becomes unstable on its own before it can help with attitude.

## The Discovery

The three failed attempts keep running into the same wall: position and attitude have different time constants. Position changes over seconds; attitude changes over tenths of a second. One controller running at one rate cannot span that gap.

The fix isn't a smarter single controller — it's two controllers running at different rates, each doing what it's suited for.

The **inner loop** controls attitude (tilt angle): it runs fast (50–200 Hz), reads tilt from the IMU, and commands differential motor speed to maintain the desired angle. Its only job is to make the drone point where it's told.

The **outer loop** controls position: it runs slower (5–20 Hz), reads position from GPS/vision, and outputs a *desired tilt angle* as its command. It doesn't directly control motors — it tells the inner loop where to point.

The coupling is the key insight: to move forward, a drone must tilt forward. The outer (position) loop commands "tilt 5° forward." The inner (attitude) loop executes "tilt to exactly 5°." The outer loop doesn't need to know anything about motor dynamics. The inner loop doesn't need to know anything about position. Each loop is tunable independently.

This is **cascaded control** (cascade PID). The output of the outer controller is the setpoint of the inner controller. Each loop is stable on its own; the cascade is stable because the inner loop is fast enough to be essentially instantaneous from the outer loop's perspective.

## Try It

<iframe src="../assets/browser/chapter22/index.html" width="100%" height="460" style="border:1px solid var(--md-default-fg-color--lightest);border-radius:8px;"></iframe>

[open in a new tab](../assets/browser/chapter22/index.html)

Before changing anything, predict:

- If you make the outer (position) loop gain too high, what happens? Does the drone overshoot? Does it oscillate? Why does the inner loop not save it?
- Compare single-loop and cascade modes with the same disturbance applied. Which recovers faster? Which has more overshoot?
- Try destabilizing the inner loop (very low or very high attitude gain). Does the outer loop behavior change even though the disturbance is only on position?

## Implementation

`browser/common/engine.js` provides `Body`, `PID`, and `Vec`. `browser/chapter22/index.html` creates three `PID` instances (`pidSingle`, `pidAlt`, `pidLat`) and two `Body` instances (`droneA`, `droneB`). The cascade wiring is inline: `stepDroneB` computes `fY = -pidAlt.update(d.pos.y, 0.016)` and `fX = pidLat.update(d.pos.x, 0.016)` independently, then applies them as separate force components. The side-by-side layout shows why a single `pidSingle` on x-position fails to control altitude while the two-controller cascade reaches the target.

## When It Breaks

**Inner loop saturation limits outer loop authority.** If a large position error causes the outer loop to command a tilt angle exceeding what the inner loop can achieve (e.g., 45° when the airframe physically limits to 30°), the outer loop is effectively open: its output is being clipped before it reaches the plant. Integral windup in the outer loop accumulates during saturation, causing overshoot when the inner loop un-saturates. Proper implementation requires the outer loop to know the inner loop's saturation limits.

**Bandwidth separation assumption fails in aggressive maneuvers.** Cascade control relies on the inner loop being much faster than the outer loop — typically a 5–10x ratio in time constants. In aggressive racing quadcopter maneuvers (full-flip, power dive), the outer loop commands change fast enough to excite inner loop dynamics. The "inner loop looks instantaneous" assumption breaks down; the two loops interact and can destabilize each other. Professional FPV racing controllers use much more aggressive inner-loop tuning and tighter bandwidth ratios to handle this.

## Transfer

- **Ship autopilots**: heading control (outer loop) commands rudder angle setpoint; a separate rudder servo loop (inner loop) tracks that angle precisely. The heading controller doesn't need a model of hydraulic rudder dynamics.
- **CNC machine tools**: a position controller (outer) commands velocity setpoint to a velocity controller (inner), which commands current to a current controller (innermost). Three cascaded loops, each tuned to its own time constant.
- **Human motor control**: your cerebellum runs a fast inner loop managing muscle force and joint stiffness; your motor cortex runs a slow outer loop planning trajectory to the target. You don't consciously control individual muscle fibers.

Exercises:

1. An outer-loop position PID has bandwidth 2 Hz. What is the minimum recommended inner-loop bandwidth for stable cascade operation? Express as a ratio and explain the physical reason.
2. Cascade control is sometimes described as "control of a controller." Explain what this means and why the inner setpoint is a better output for the outer loop than a direct motor command would be.
3. A cascade system oscillates at 8 Hz. You suspect the inner loop. How would you test this hypothesis by temporarily disabling the outer loop?

---

**Continue → [Why Quadcopters Need Two Brains](23-why-quadcopters-need-two-brains.md)**
