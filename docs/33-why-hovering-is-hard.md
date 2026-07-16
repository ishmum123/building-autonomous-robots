# Why Hovering Is Hard

## The Problem

A quadcopter weighs 800 grams. Each motor-propeller combination produces some thrust depending on speed. To hover, total thrust must exactly equal weight: 4 × F_motor = mg = 0.8 × 9.81 = 7.85 N. Each motor must produce 1.96 N.

You look up the motor's thrust curve: at 50% throttle, it produces 1.96 N. You set all four motors to 50% throttle and let go. The drone should hover. It doesn't — it climbs slowly, then accelerates upward, then crashes into the ceiling.

The problem: "50% throttle = 1.96 N" was measured on a test stand with fully charged batteries. The battery voltage when you tested the motors was 16.8V; it's now 15.2V (40% discharged). At 15.2V, 50% throttle produces only 1.7 N per motor — total thrust 6.8 N, less than the 7.85 N needed. The drone sinks.

You correct — raise throttle until it hovers. But hovering perfectly requires actively countering every perturbation: a brief gust, the battery discharging, blade efficiency changes as temperature rises, all continuously change the exact throttle needed for neutral lift. And at the same time, the attitude controller is continuously adjusting individual motor speeds for roll and pitch correction — perturbing the total thrust as a side effect.

Stable hover requires:

- Continuous altitude control that compensates for all unmeasured disturbances
- Decoupled altitude and attitude control — fixing altitude shouldn't disturb attitude and vice versa
- Fast response: an unstabilized quadcopter falls 20 cm in 0.2 seconds — the controller must react in tens of milliseconds
- Resistance to accumulated integral error that causes the drone to slowly climb or sink over minutes

## What Would You Try?

- Hovering requires thrust = weight exactly. If you had to set a fixed throttle and couldn't change it, how close could you get? What would still cause drift?
- The altitude controller adjusts total throttle to hold altitude. The attitude controller also adjusts motor speeds. When the attitude controller changes two motors to roll left, what happens to total thrust?
- If the drone is sinking slowly at 0.1 m/s and you increase throttle slightly, will it stop sinking immediately? What lag exists between command and altitude response?

## Failed Attempts

### Attempt 1: Fixed throttle at the hover point, no altitude feedback

Calibrate once: find the throttle setting that produces hover on the bench with a fresh battery. Program this as a constant. "Hover" without any altitude sensing.

This works for about 30 seconds. The battery discharges slightly; hover throttle drifts. A small disturbance perturbs altitude; with no feedback, the perturbation is never corrected. After 2 minutes, the drone has drifted 3 meters vertically from its intended altitude.

Fixed throttle hover is not a stable equilibrium — it's a marginally stable one. Any perturbation accumulates. Real hovering requires active correction.

### Attempt 2: Altitude hold via barometer feedback only

Add a barometer (air pressure sensor). Altitude estimate from barometric pressure. Run a PID controller: error = target_altitude − barometric_altitude; adjust total throttle proportionally.

The barometer has ±0.5 m noise. A proportional controller with gain high enough to reject disturbances amplifies this noise into throttle oscillations of ±5% — visible as constant up-down bobbing at 1–2 Hz. The drone "breathes" — constantly hunting the target altitude within a ±0.5 m band.

Worse: the barometer is sensitive to airflow from the propellers. In calm air, the propeller downwash creates a local pressure region below the drone that reads as the drone being slightly higher than it is. The altitude controller responds by reducing throttle — the drone is actually lower than it thinks, so it slowly sinks while reducing throttle. This "barometric depression from prop wash" is a known problem in consumer drones; some DJI Phantom firmware has explicit compensation for it.

### Attempt 3: Altitude hold via double-integrated accelerometer

Chapter 25 showed accelerometer double-integration drifts badly. But in a hover context, you're not trying to recover absolute position — just hold relative altitude. Keep the drone at the same altitude it was at when you pressed "hold." The integral drift adds a constant velocity, which the PID can correct...

The accelerometer bias drift (0.05 m/s² after calibration) produces 1.5 m/s of velocity error after 30 seconds. The velocity error is indistinguishable from actual velocity — the controller will try to correct what looks like a 1.5 m/s descent by increasing throttle steadily. The integrating throttle causes the drone to climb continuously. The "altitude hold" drifts upward at increasing rate.

Additionally, the altitude controller's throttle corrections feed back into the accelerometer: changing throttle changes vertical acceleration, which changes the accelerometer reading, which changes the throttle. With even slight lag, this loop oscillates.

## The Discovery

The three attempts share a common problem: each altitude sensor has a specific deficiency that, used alone, causes a specific failure mode. Barometer noise causes bobbing; accelerometer bias causes drift. Fixed throttle has no disturbance rejection.

The right architecture combines altitude and velocity sensing with complementary filters — echoing the gyroscope/accelerometer fusion of Chapter 26, but for vertical axis:

**Barometer provides altitude** — absolute, long-term stable, low-rate (±0.5 m noise at 10–50 Hz). Good for long-term altitude reference, bad for fast response.

**Accelerometer provides vertical acceleration** — high-rate (1 kHz), no long-term reference, drifts. Good for fast disturbance detection, bad for long-term tracking.

**Fuse them**: integrate accelerometer data at high rate for short-term vertical velocity; use barometer readings (when not disturbed by prop wash) to correct accelerometer drift at low rate. The altitude PID controller runs on this fused estimate, which is both fast and stable.

The second key insight: the **altitude controller must account for attitude**. When the drone tilts 20° for a horizontal maneuver, the four motors point slightly sideways — total vertical thrust decreases by cos(20°) ≈ 0.94, so 6% less vertical force. The drone starts sinking. The altitude controller must compensate for tilt by increasing total thrust: total_thrust = (mg + altitude_correction) / cos(tilt_angle). At 45° tilt, this doubles the required thrust — aggressive horizontal maneuvers require significant altitude compensation or the drone descends during the maneuver.

This "tilt compensation" is the coupling between attitude and altitude control. A quadcopter is not a pure altitude-control problem — attitude and altitude are physically coupled by the tilted thrust vector.

## Try It

<iframe src="../assets/browser/chapter33/index.html" width="100%" height="460" style="border:1px solid var(--md-default-fg-color--lightest);border-radius:8px;"></iframe>

[open in a new tab](../assets/browser/chapter33/index.html)

Before changing anything, predict:

- Set hover mode to "fixed throttle." Apply a brief upward push. Does the drone return to the original altitude, settle at a new altitude, or continue rising?
- Enable barometer-only altitude hold. Add simulated prop-wash pressure effect. Does the drone sink? Why?
- Enable tilt compensation. Command a 30° roll (bank). Without tilt compensation, does the drone descend during the bank? With compensation, does it hold altitude?

## Implementation

`browser/common/engine.js` provides `Quadcopter` and `PID`. `browser/chapter33/index.html` runs two drones: the left applies a fixed thrust with no feedback; the right runs `pidB = new PID(kpAlt, kiAlt, 1.0, TARGET_Y)`, computing `thrustCmd = -pidB.update(qB.body.pos.y, 0.016)` each tick and calling `qB.setMotors(thrustCmd/2, thrustCmd/2)`. The comparison makes the core point visible: fixed thrust produces unstable altitude, PID feedback holds a hover target.

## When It Breaks

**Integral windup during altitude saturation.** When the drone is at the throttle ceiling (100% all motors) — near maximum altitude or too heavy — the altitude PID's integral term keeps accumulating error. If the load then decreases (drops a payload), the integral has wound up to a large positive value. The drone shoots upward rapidly, overshoots by several meters, and oscillates badly before the integral unwinds. Altitude controllers require integral clamping at actuator limits exactly as temperature PIDs do (Chapter 21).

**Ground effect: approaching hover efficiency changes near the ground.** Within one rotor-diameter of the ground (~20–30 cm for consumer drones), propeller efficiency increases significantly: the ground deflects downwash back upward, reducing induced velocity and increasing effective thrust for the same motor speed. As the drone descends through this region during landing, the same throttle suddenly generates more thrust — the drone "cushions" and decelerates. Without ground effect compensation, the altitude controller sees apparent excess thrust near the ground and reduces throttle, causing the drone to drop hard onto the landing surface. This effect also destabilizes altitude hold when hovering near flat surfaces.

## Transfer

- **Helicopter hover**: helicopters maintain hover using cyclic control for horizontal drift and collective control for altitude — exactly the separate altitude/attitude control architecture. A key difference is that helicopter rotor speed is fixed; altitude is controlled by collective pitch (blade angle), not motor speed.
- **Submarine neutral buoyancy**: a submarine hovering at depth maintains its buoyancy within a narrow band (fill/vent ballast tanks) while using diving planes for small altitude corrections — the same hybrid of coarse long-term reference and fine fast correction.
- **Harrier jump jet**: the Harrier's vertical hover mode was notoriously difficult before computer assistance. The pilot had to manually balance four thrust nozzles and throttle to maintain altitude and attitude simultaneously — a task that proved cognitively overwhelming without autostabilization. The AV-8B Harrier II introduced digital flight control to handle this coupling, reducing pilot workload.

Exercises:

1. A quadcopter at 20° tilt hover requires what fraction more thrust than level hover? At 45° tilt? What is the maximum tilt angle for a drone whose motors can produce 150% of hover thrust?
2. The altitude barometer has 0.5 m noise (1σ). The PID proportional gain for altitude is K_p = 2 m/s per meter of error. What is the RMS vertical velocity command due to barometer noise alone?
3. Design a simple algorithm to detect ground effect: what sensor signals change as the drone descends within one rotor-diameter of the ground, and how could these be used to trigger a throttle adjustment?

---

**Continue → [Why Wind Wins](34-why-wind-wins.md)**
