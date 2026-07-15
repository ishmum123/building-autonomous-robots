# Why Four Motors Beat One

## The Problem

You want to build the simplest possible flying robot — one motor, one propeller, straight up. The propeller spins and generates lift. When lift equals weight, the vehicle hovers. Elegant and minimal.

You build it. The motor spins up. The vehicle rises — and immediately begins spinning in the opposite direction to the propeller, faster and faster, until it's a blurred, uncontrollable top. Before it reaches hover altitude, it's spinning at 60 RPM and losing altitude.

You add a tail rotor, like a helicopter. Now it stops spinning — but the tail rotor consumes 10–15% of total power just to cancel the torque that isn't being used to lift anything. And the tail rotor only works in one axis; to move forward or sideways, you need to tilt the main rotor disk, which requires a swashplate mechanism with dozens of moving parts.

Any multi-degree-of-freedom flying vehicle must:

- Generate enough lift to support its weight
- Cancel all net torques so the vehicle doesn't spin uncontrolled
- Control attitude (roll, pitch, yaw) independently
- Do all of this with a mechanically simple actuator system that can respond quickly

## What Would You Try?

- Every spinning propeller creates a reaction torque on the frame. With one propeller spinning clockwise, the frame wants to spin counterclockwise. What would cancel this torque without a dedicated tail rotor?
- If you had two propellers spinning in opposite directions, what happens to the net torque? What about lift?
- With four propellers — two pairs spinning opposite directions — how many independent quantities can you control by varying their speeds? List them.

## Failed Attempts

### Attempt 1: One motor, one propeller — add a tail rotor

The helicopter solution. A large main rotor provides lift; a small tail rotor provides yaw torque to counteract the main rotor's reaction. This works — it's how every helicopter from the 1940s to today operates.

But the tail rotor uses 10–15% of engine power and provides no lift. For a drone, this is a significant efficiency penalty. The tail rotor is a mechanically separate system with its own motor, gearbox, and control linkage — another failure point. A tail rotor failure is typically fatal for a helicopter; it enters an uncontrolled spin that pilots have only seconds to manage (a procedure called autorotation, which doesn't always work at low altitude).

The bigger issue: to move forward, a helicopter tilts its main rotor disk using a swashplate — a mechanically complex assembly of cyclic and collective pitch controls. This works in full-scale helicopters where the expense is justified. In a 250 g drone, a swashplate mechanism would weigh more than everything else combined and would fail within hours from vibration.

### Attempt 2: Two counter-rotating motors on a single axis

Stack two propellers on the same shaft, spinning in opposite directions (coaxial counter-rotating). The torques cancel. Two propellers on one axis provide more lift than one for the same diameter.

Torques cancel — the yaw problem is solved. But now you have no way to control yaw: both propellers are on the same axis, their torques are always equal and opposite, and you can't vary one without varying the other. To tilt for forward flight, you'd need to tilt the entire coaxial assembly, which requires... another swashplate or a servo mechanism. The mechanical simplicity isn't achieved.

This design exists (some professional drones use it for compact size), but it requires variable pitch propellers to control yaw — the mechanical complexity just moved to a different place.

### Attempt 3: Fixed-pitch propellers arranged on a rigid cross — vary individual speeds

Instead of varying pitch, vary speed. Put four fixed-pitch propellers at the corners of an X frame, two spinning clockwise (CW) and two counter-clockwise (CCW), diagonally opposite. Now each motor can be driven independently at different speeds.

This is the actual quadcopter design — and it works. But why exactly four? Could you do it with three?

A tricopter has three motors. Two spin CW, one spins CCW (or some combination). Torques don't balance: two CW motors plus one CCW motor = net torque of (1 CW) unless you vary their speeds, which complicates things. Tricopters solve yaw by adding a tilting rear motor on a servo — again, mechanical complexity. The servo is slow and introduces vibration.

Three fixed motors on a rigid frame: you have 3 control inputs (three speeds) but need 4 independent control outputs (total thrust, roll torque, pitch torque, yaw torque). The system is underactuated — you cannot independently control all four outputs.

## The Discovery

The tricopter calculation reveals the math: to independently control roll, pitch, yaw, and total thrust, you need at least 4 independent actuators. Three motors give 3 degrees of freedom — enough for roll, pitch, and thrust, or pitch, yaw, and thrust, but not all four simultaneously.

Four motors at the corners of an X-frame, two CW (front-left, rear-right) and two CCW (front-right, rear-left), provide exactly 4 independent control inputs. Here's what each combination of speed changes does:

- **All four increase equally**: more total thrust → climb
- **Front pair decrease, rear pair increase**: nose tilts up (pitch control) → fly backward
- **Left pair decrease, right pair increase**: right side tilts down (roll control) → fly right
- **CW pair increase, CCW pair decrease** (diagonally): net torque in one yaw direction → yaw control

Each of these four movements uses all four motors simultaneously — no motor is "idle" for any maneuver. The design is **fully actuated**: all four degrees of freedom can be controlled independently, at the same time.

The fixed-pitch propeller is key to efficiency: no swashplate, no variable pitch, no servos. Speed-variable fixed-pitch props respond in under 50 ms and are mechanically simple enough to weigh a few grams. The entire quadcopter actuation system is four brushless motors and four propellers — nothing else moves.

## Try It

<iframe src="../assets/browser/chapter26/index.html" width="100%" height="460" style="border:1px solid var(--md-default-fg-color--lightest);border-radius:8px;"></iframe>

[open in a new tab](../assets/browser/chapter26/index.html)

Before changing anything, predict:

- Set all four motors to equal speed. Does the vehicle spin in yaw? Does it lift symmetrically?
- Increase front-left and rear-right speed (the CW pair) while keeping CCW motors fixed. What happens to yaw? What happens to total thrust?
- Simulate a single motor failure (set one motor to zero). Can the remaining three motors maintain altitude? Maintain attitude?

## Implementation

`browser/common/engine.js` provides the `Quadcopter` class; `browser/chapter26/index.html` creates `qA = new Quadcopter(1.0)` and `qB = new Quadcopter(1.0)`, drives the single-motor case with `qA.setMotors(thrustLevel, 0)` and the balanced case with `qB.setMotors(thrustLevel/2, thrustLevel/2)`. The sim passes thrust directly — the thrust-vs-speed relationship is conceptual framing; the important result (balanced motors stabilize tilt) is visible in the strip plot comparing `'single motor spin°'` versus `'balanced tilt°'`.

## When It Breaks

**Motor failure leaves the vehicle underactuated.** A quadcopter with one motor failed has only three actuators. As the tricopter analysis showed, three actuators cannot independently control all four degrees of freedom. The vehicle will spin uncontrollably in yaw unless clever algorithms exploit the remaining three motors asymmetrically — accepting a constant yaw rate and using that rotation for cyclic control authority. This "spinning recovery" mode has been demonstrated in research (notably by Raffaello D'Andrea's group at ETH Zurich) but requires high-rate sensing and is not in consumer firmware.

**Propeller aerodynamic interference.** Propellers in downwash from adjacent propellers lose efficiency. In standard X-frame quadcopter geometry, the rear propellers fly in the disturbed air from the front propellers during forward flight. This reduces rear motor efficiency, requiring rear motors to spin faster to maintain the same thrust — creating a slight persistent torque imbalance that the attitude controller must constantly correct. At high forward speeds (>10 m/s), the interference becomes significant enough to require different front/rear thrust coefficients.

## Transfer

- **Reaction wheels on satellites**: spacecraft attitude control uses three orthogonal reaction wheels (spinning masses) to control roll, pitch, and yaw — the same principle: N actuators to control N degrees of freedom, using torque rather than thrust.
- **Omnidirectional ground robots**: mecanum wheel robots use four independently driven wheels with angled rollers to achieve full 2D translation plus rotation without steering — three degrees of freedom from four actuators in the same fully-actuated design philosophy.
- **Octocopters**: 8-motor configurations are used for heavy lift and redundancy. With 8 actuators and 4 degrees of freedom, the system is over-actuated — there are multiple motor speed combinations that produce the same vehicle motion, allowing control even after a motor fails.

Exercises:

1. A quadcopter must produce roll torque τ_roll = 0.1 N·m, with zero net yaw and zero net pitch. Express the required difference in thrust between left and right motor pairs. Assume motor spacing L = 0.2 m.
2. Why can't a single-motor helicopter produce yaw control using only the main rotor? What would need to change about the main rotor to enable yaw control without a tail rotor?
3. A hexacopter (6 motors) has two actuators more than needed to control 4 DOF. Describe one advantage this over-actuation provides for fault tolerance.

---

**Continue → [Why Quadcopters Flip](27-why-quadcopters-flip.md)**
