# Why Wind Wins

## The Problem

Your delivery drone is holding a GPS waypoint above a building rooftop — stationary in calm air, rock solid. Then a gust hits. A 7 m/s side wind (a typical gust at building height) applies a lateral force of roughly 3 N to the drone's 1.5 kg body. The drone accelerates sideways at 2 m/s².

In 0.5 seconds, the drone is moving at 1 m/s sideways and has drifted 0.25 m. The GPS detects the drift and the position controller commands a correction: tilt the drone into the wind, generate thrust to push back. The correction starts — but the position controller runs at 10 Hz, and 100 ms elapsed before the first correction. Another 100–200 ms for the attitude controller to execute the tilt. By the time corrective thrust is generating, the drone has drifted 0.5 m and is moving at 1.5 m/s.

The correction overshoots — the drone tilts hard into the wind, decelerates past the target, and oscillates around the waypoint. The next gust hits mid-oscillation and compounds the error. Near a building edge, a 1.5 m drift in 0.5 seconds is the difference between a delivery and a crash.

Any outdoor autonomous vehicle must:

- Reject wind disturbances faster than they accumulate to unsafe magnitudes
- Handle sustained winds (not just gusts) without constant oscillation
- Not rely on perfect knowledge of wind speed and direction to reject wind
- Remain stable in wind gusts that have complex, unsteady structure (turbulence, wake vortices)

## What Would You Try?

- A drone hovering in wind constantly tilts into the wind to produce the corrective thrust. Is this tilt itself a problem? What causes the oscillation around the waypoint?
- If you could predict a gust 0.5 seconds before it hit, you could apply a correction earlier. Is there a way to measure wind before it moves the drone?
- Sustained wind requires a sustained tilt to hover in place. The position PID's integral term accumulates and builds a sustained correction. Is this a feature or a bug of integral control?

## Failed Attempts

### Attempt 1: Faster position control loop — react before drift becomes large

The problem is the 100 ms GPS update delay. Speed up the position control loop. Use the IMU-derived velocity estimate (from GPS/IMU fusion, Chapter 24) instead of waiting for GPS updates. Run the position loop at 100 Hz instead of 10 Hz.

This helps with gusts — the inner loop can react within 10 ms instead of 100 ms. But "react" means: detect the velocity change after the wind has already accelerated the drone. Even at 100 Hz, the first detection happens at the first sample after the gust, by which time the drone has been pushed for 10 ms at 2 m/s² → 0.02 m/s velocity and 0.0001 m displacement. Each reaction is still after the fact.

Moreover, the velocity-feedback loop must be tuned with a bandwidth well below the attitude loop to maintain cascade stability (Chapter 17). Running the position loop at 100 Hz requires the attitude loop at ≥ 1,000 Hz — feasible but stresses the controller architecture. And fast position loops with high gain can excite structural vibrations in the airframe, creating new instabilities.

Faster reactive control reduces the impact of disturbances but cannot eliminate the fundamental delay between disturbance onset and correction.

### Attempt 2: Feedforward wind compensation — measure wind, correct for it

Mount a pitot tube (airspeed sensor) on the drone to measure relative wind speed and direction. When the sensor detects a 7 m/s gust from the north, immediately command a north tilt to pre-compensate before the wind moves the drone.

The pitot tube works well in steady laminar flow. But gusts near buildings have turbulent, multi-directional structure — the gust arriving from one direction contains eddies rotating in three dimensions. The pitot tube measures the integrated wind vector at its mounting point, which may not match the force on the drone 50 ms later when the gust structure evolves. Feedforward computed from an imperfect model of a complex disturbance produces partial corrections — better than nothing, but not full rejection.

More critically: the pitot tube response is fast, but the correction chain is not. Wind detected → compute required tilt → send to attitude controller → attitude controller executes → airframe tilts → corrective thrust develops. This chain takes 100–200 ms. The gust has evolved significantly in that time. Feedforward with a long actuation delay corrects for the wind that was present 200 ms ago, not the wind present now.

### Attempt 3: High-gain position PID with large integral term

The integral term in the position PID accumulates drift error over time and applies a sustained correction. In sustained wind, the integral builds up until the drone holds a permanent tilt into the wind. The larger the integral gain, the faster this happens.

Increase integral gain K_i significantly. The drone corrects sustained wind faster — the integral builds to the steady-state correction tilt in 5 seconds instead of 30 seconds.

The problem: a high integral gain overshoots. When a gust starts, the integral begins accumulating rapidly. When the gust ends, the integral has wound up to a large value — the drone is tilted 15° into wind that no longer exists, and it accelerates in the wind direction until the integral discharges. Each gust/lull cycle produces overshoot in both phases. With realistic gusty wind (gusts lasting 1–3 seconds), the high-integral drone oscillates continuously and never stabilizes.

There's a fundamental tension: integral gain fast enough to track gusts produces oscillation during lulls. Integral gain slow enough to avoid oscillation is too slow to track gusts.

## The Discovery

All three approaches treat wind as an external disturbance to react to after it arrives. The failed attempts can't escape the physics: aerodynamic force produces acceleration, acceleration produces velocity, velocity produces position error, error drives correction — each step takes time.

The insight is that a quadcopter's aerodynamic drag is itself a disturbance-rejection mechanism. When the drone tilts into the wind to hold position, the drone is moving through the air at the wind speed (relative airspeed = wind speed − drone speed). The aerodynamic drag on the tilted body acts against the wind direction — the drone is aerodynamically stable in that tilt. The more it tilts, the more drag it produces, up to the point where drag force equals wind force.

But this passive drag is too weak for fast gusts — the drone must **tilt actively and hold that tilt**, using its attitude controller to maintain a specific tilt angle that produces the correct corrective force. The question is: how do you know the right tilt angle quickly?

The answer comes from integrating position error correctly. The inner loop (attitude, running at 200 Hz) is already fast enough to hold any commanded tilt instantaneously. The position loop's job is to decide the right tilt. Instead of waiting for GPS position error, the outer loop can work from **velocity error**: if the drone is moving at 0.5 m/s east due to wind, command a westward tilt proportional to the eastward velocity. Velocity feedback (from GPS/IMU fusion) has far lower latency than position feedback, because velocity error develops in milliseconds while position error takes seconds to build to detectable size.

**Velocity-feedforward plus position-feedback cascade**: the outer position loop generates a velocity setpoint (how fast to move toward the target). A velocity controller then generates the tilt angle to achieve that velocity, including implicit disturbance rejection from the fast velocity feedback loop. Wind that pushes the drone sideways is detected immediately as a velocity error and immediately resisted, before it builds into position error.

This is the standard architecture of professional autopilots: nested velocity and position loops, with the velocity loop running fast enough to reject gusts. The integral term in the velocity loop provides the sustained tilt for sustained wind — but because it's in the inner velocity loop (faster dynamics), it accumulates and discharges faster, with less overshoot.

## Try It

<iframe src="../assets/browser/chapter29/index.html" width="100%" height="460" style="border:1px solid var(--md-default-fg-color--lightest);border-radius:8px;"></iframe>

[open in a new tab](../assets/browser/chapter29/index.html)

Before changing anything, predict:

- Apply a sustained 5 m/s wind with position-only feedback. How far does the drone drift before the integral correction holds it in place?
- Switch to velocity-feedback mode. How does the time to stabilize compare after the same wind onset?
- Apply a sharp gust (5 m/s for 1 second, then gone). Compare the overshoot in position-feedback vs. velocity-feedback modes when the gust ends.

## Implementation

`browser/chapter29/index.html` uses two `PID` instances (`pidX`, `pidY`) for position hold and applies a step-function wind via `getWind(t)` — on between `WIND_START = 120` and `WIND_END = 300` ticks, zero otherwise. Linear drag is applied inline as `vel.mul(-0.5)`. The sim simplifies aerodynamics to a step disturbance and linear damping — enough to show how the integral term accumulates to cancel a sustained wind offset. `browser/common/engine.js` provides `Quadcopter` and `PID`.

## When It Breaks

**Building wake vortex.** Airflow around a tall building creates a wake of rotating air on the downwind side. A drone descending through the edge of this wake encounters rapidly alternating headwind and tailwind — effectively ±10 m/s wind in 100 ms intervals. This exceeds the bandwidth of any velocity controller: the gust changes direction faster than the drone can respond. The result is uncontrollable oscillation and eventual loss of position. This is why commercial drone delivery operations prohibit flight within 2–3 building-heights downwind of tall structures. Amazon and Wing have both encountered this during urban corridor testing.

**Integral reset on mode switch.** When a drone switches from manual control (where the human is compensating for wind) to autonomous hold (where the controller takes over), the position and velocity integral terms start at zero. If there's a sustained 8 m/s wind, the integral must accumulate before the drone can hold position — during which time the drone drifts visibly, sometimes alarming operators into switching back to manual. Real autopilots initialize the integral at the value needed to hold current state by measuring the stick inputs the pilot was making just before handover.

## Transfer

- **Ship dynamic positioning**: offshore vessels use GPS and wind/current sensors to maintain position in rough seas. DP systems run velocity controllers for surge, sway, and yaw — exactly the three-loop architecture (position → velocity → thrust). The integral term in the velocity loop builds the sustained engine output needed to hold station in 3-knot currents.
- **Wind-compensated crane operations**: harbor cranes lifting containers from ships in wind run active compensation to prevent payload swing. The payload velocity is controlled, not just position — again, the velocity feedback loop is faster than any position-based scheme.
- **Aircraft crosswind landing**: landing in a crosswind requires a crab angle into the wind (heading ≠ ground track) maintained until just before touchdown, then a kick to align with the runway. Autopilot crosswind modes compute the required crab angle from measured ground speed vs. airspeed vector — velocity-level wind compensation.

Exercises:

1. A drone is pushed by a 6 m/s crosswind. Its drag coefficient C_D × A = 0.02 m² and mass is 1.5 kg. At what tilt angle does the horizontal thrust component equal the aerodynamic drag force? (Air density ρ = 1.2 kg/m³.)
2. A position PID with K_i = 0.1 s⁻¹ is holding against a 6 N wind force. How long does it take the integral to build enough tilt to reject the wind, if the proportional term alone generates only 2 N of corrective force initially?
3. Explain why velocity feedback rejects wind gusts faster than position feedback, using the concept of "what error is generated in the first 50 ms after a gust starts."

---

**Continue → [Why Autopilots Exist](30-why-autopilots-exist.md)**
