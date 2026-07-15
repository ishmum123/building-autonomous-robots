# Why Drones Crash

## The Problem

A delivery drone is carrying a package across a city on a calm day. At 80 m altitude, one of its four motors loses 30% power due to a failing ESC. The drone immediately tilts 12 degrees. The flight controller senses the tilt, commands the other three motors to compensate — and draws them to 100% output. Twelve seconds later, a second motor, now thermally stressed, fails completely. The drone falls.

The motor didn't fail suddenly. It degraded over 40 flight hours. There was a log of rising current draw, rising temperature, and intermittent vibration spikes. Nobody looked at it.

Small failures become crashes when:

- Compensation logic removes all safety margins — one failure causes another
- No fault is monitored until it becomes catastrophic
- Control authority is already saturated before a second fault occurs
- Recovery procedures require airspeed or altitude the drone doesn't have

## What Would You Try?

- A motor loses 20% thrust. The controller compensates perfectly and the drone flies level. Has the failure been "handled"? What has changed about the drone's ability to handle the *next* fault?
- You could detect vibration anomalies, rising motor temperature, or asymmetric current draw. At what point does any of these alone tell you a crash is imminent?
- If the flight controller can detect that one motor is underperforming, what should it do differently — if anything — before a second failure occurs?

## Failed Attempts

### Attempt 1: Assume failures are instantaneous and independent

The simplest model: motors are either working or not. Design the controller to handle any single-motor failure by redistributing thrust to the remaining motors. Test it in simulation with clean step-function failures. It works.

In practice, failures are gradual and correlated. A motor's winding insulation degrades over heat cycles — it runs hotter, which stresses adjacent components, which run hotter. ESC failures raise bus voltage transiently, stressing other ESCs. When the first motor finally fails hard, the system is already degraded everywhere. The assumption of independence turns out to be wrong for the worst case: the cascade.

### Attempt 2: Monitor everything and alarm on any anomaly

Add sensors for motor temperature, vibration, current draw, and voltage. Alert when any reading exceeds a fixed threshold.

A well-maintained drone in summer generates temperature anomalies constantly — ambient air is hot, hard climbs are hot. Fixed thresholds produce so many false alarms that operators disable them or ignore them. The drone that crashed had 47 temperature threshold alerts in its logs from the previous week. The operator had stopped checking. When the critical anomaly appeared, it looked identical to the 47 non-events before it. False alarm saturation is a known human-factors failure mode, documented in aviation accidents long before drones existed.

### Attempt 3: Land immediately on any anomaly

React conservatively: at the first sign of motor trouble, command an emergency landing.

This is safe for a warehouse drone flying over open ground. For an urban delivery drone at 80 m over a crowded street, immediate descent may be more dangerous than continuing to the nearest landing zone. "Land immediately" also doesn't distinguish between a 2% thrust loss (negligible) and 30% (serious). Uniform response to non-uniform faults wastes redundancy and mission time without preventing the cases that actually matter.

## The Discovery

The three attempts fail for the same reason: they treat each fault in isolation without tracking what the fault *does to the system's remaining margins*.

The insight: monitor not just the fault, but the **remaining control authority** after compensation. A single motor at 80% is a nuisance. A single motor at 80% with a second motor at 90% means the controller is already at 95% of maximum to hold level flight. The system has no margin left for wind, gusts, or the next fault.

This leads to a **fault-margin architecture**: instead of alarming on raw sensor values, continuously compute how much authority the system has left assuming the current fault is permanent. If remaining authority drops below a threshold (say, 15%), trigger a graduated response — reduce speed, reduce mission payload, begin routing to the nearest safe landing zone — while the current fault is still manageable. Don't wait for the second failure.

The formal engineering concept is **graceful degradation with margin tracking**: the system degrades function proportionally to available resources, rather than attempting full performance until collapse. Real implementations combine health monitoring with replanning so the drone automatically reduces mission scope as reliability decreases.

## Try It

<iframe src="../assets/browser/chapter31/index.html" width="100%" height="460" style="border:1px solid var(--md-default-fg-color--lightest);border-radius:8px;"></iframe>

[open in a new tab](../assets/browser/chapter31/index.html)

Before changing anything, predict:

- Reduce one motor to 70% maximum thrust. Does the drone immediately crash, or does it compensate? Now reduce a second motor to 85%. What happens to the remaining motors' output levels?
- Set the anomaly detection threshold very tight. How often does it trigger on a healthy, hovering drone? What happens to the crash rate when operators ignore frequent false alarms?
- Enable the margin-tracking mode. At what remaining-authority percentage does the drone begin routing to a landing zone, and does this prevent the cascade failure?

## Implementation

`browser/chapter31/index.html` runs two `Quadcopter` instances and injects a binary motor failure at `failTime`: once triggered, the failed motor contribution is set to zero — `q.setMotors(lm, thr)` where `lm = failed ? 0 : thr`. The two PIDs (`pidA`, `pidB`) show how one drone recovers and the other does not, depending on its tuning margin. The sim simplifies fault handling to an on/off motor drop — enough to show how a single actuator loss can cascade when remaining motors are already near their limits. `browser/common/engine.js` provides `Quadcopter` and `PID`.

## When It Breaks

**Sensor failure masquerading as motor health.** If the current sensor reporting motor load fails or drifts, the margin tracker reads healthy margins while the drone is actually degraded. The 2009 Air France 447 accident involved pitot tubes (airspeed sensors) icing over — the autopilot's "health" looked normal to itself while flying with false airspeed. Drones face the same failure mode: a stuck-at-nominal sensor is more dangerous than a failed one, because it produces false confidence.

**Unknown fault correlations in new hardware.** Margin tracking requires knowing what faults are correlated — which components stress which others under load. For a new drone design with novel motor-ESC combinations, these correlations are unknown. Thermal stress tests and accelerated life testing can characterize them, but early in a design's life the correlation model is wrong. Amazon's first delivery drone generations went through multiple redesigns after field motors failed in patterns not predicted by bench tests.

## Transfer

- **Aviation multi-engine failure procedures**: commercial pilots train for engine-out scenarios specifically because the first engine loss saturates margins that a second loss then exceeds. Multi-engine rating training is built around recognizing asymmetric thrust and preventing the secondary loss.
- **Nuclear plant defense-in-depth**: reactor safety design requires that no single failure causes a critical event, and no two independent failures together cause one either. The Three Mile Island accident involved a series of individually recoverable faults that compounded because operators didn't track remaining safety margin.
- **Medical device fault tolerance**: implantable cardiac defibrillators monitor battery health, lead impedance, and sensing accuracy independently — and systematically reduce pacing rate rather than failing hard when any margin drops.

Exercises:

1. A quadrotor has four motors each capable of producing 0–100% thrust. In hover it uses 60% average. Motor 1 fails to 40% max. What is the maximum additional thrust the remaining three can provide, and what fraction of original hover margin remains?
2. An operator sees 50 temperature-threshold anomaly alerts per week, of which 1 is real. If they check 10% of alerts, what is the probability they catch the real one? What threshold false-alarm rate would make checking worthwhile?
3. Design a graduated response policy for a delivery drone with 4 motors. At what remaining-authority levels would you (a) slow down, (b) route to nearest landing zone, (c) immediately descend?

---

**Continue → [Why Maps Matter](32-why-maps-matter.md)**
