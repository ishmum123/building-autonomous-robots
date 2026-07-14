# Why Wheels Move

## The Problem

Your robot has a motor. The motor spins. The wheel spins. The robot doesn't move.

You watch the wheel blur at 300 RPM and the chassis sits perfectly still on the tile floor. All that energy is going nowhere — into heat in the bearing, into vibration, into noise. The wheel is doing everything right. The robot is doing nothing.

Any solution has to satisfy:

- The wheel must translate its rotation into forward motion of the whole robot
- The force must come from the wheel-floor contact, not from pushing off a wall
- The solution must work even if the motor is completely enclosed (no external push)
- It must scale — faster spin should mean faster travel

## What Would You Try?

- The motor clearly makes the wheel spin. What connects "spinning" to "moving forward"? Sketch the forces at the contact patch.
- If you put the robot on ice, what would change? Why?
- What property of the floor does the robot depend on that it never explicitly controls?

## Failed Attempts

### Attempt 1: Spin faster

The wheel is moving. The robot isn't. Obvious fix: more RPM.

You crank the voltage. The wheel screams. The robot still doesn't move — in fact it's worse now. On a smooth tile the wheel starts polishing the floor, and the chassis rocks slightly from the reaction torque but translates nowhere.

The failure reveals: speed is irrelevant if the contact patch has nothing to push against. The wheel surface is moving backward relative to the floor, but unless the floor pushes back forward, Newton's third law has nothing to work with.

### Attempt 2: Use a smooth wheel for less rolling resistance

Less friction should mean less wasted energy, so the wheel rolls more freely. Install precision bearings, smooth rubber, smooth floor.

Now the wheel spins with almost zero resistance — and the robot still doesn't move. In fact it's easier than ever to hold the chassis still while the wheel turns beneath it.

The failure reveals the hidden double role of friction: there's *rolling resistance* (bad, opposes motion) and *traction* (good, is the mechanism of motion). Minimizing all friction kills traction along with drag.

### Attempt 3: Make the wheel bigger

Bigger wheel, more contact area, more grip. Intuitive.

A larger radius does increase the footprint, but static friction force depends on the normal load and the coefficient of friction — not on contact area for rigid bodies. More importantly, the same motor torque spread over a larger radius produces *less* tangential force at the contact patch (F = τ/r). The robot pushes backward against the floor with less force, so the floor's forward reaction is smaller.

The failure reveals: traction scales with normal force × friction coefficient, and increasing radius without increasing normal force or grip coefficient actually makes the force budget worse.

## The Discovery

Every failed attempt circled the same gap: the wheel can only move the robot if the floor pushes the robot forward. For that to happen, the wheel surface must push the floor backward at the contact patch, and the floor must resist that push — statically. No slip.

The mechanism is **static friction at the contact patch**. The wheel tries to slide backward against the floor. Static friction prevents the slide and, by reaction, pulls the floor backward under the wheel — which is indistinguishable from pushing the robot forward. As long as the torque doesn't exceed the friction limit (μₛ × normal force), the contact point is momentarily stationary while the wheel rolls forward over it.

This is why: ice → no motion; sand → partial motion; rubber on asphalt → full motion. The surface isn't just a platform. It's the engine's other half.

Formally: the tractive force F = min(τ/r, μₛ·N), where τ is motor torque, r is wheel radius, μₛ is the static friction coefficient, and N is the normal load.

## Try It

<iframe src="../assets/browser/chapter01/index.html" width="100%" height="460" style="border:1px solid var(--md-default-fg-color--lightest);border-radius:8px;"></iframe>

[open in a new tab](../assets/browser/chapter01/index.html)

Before changing anything, predict:

- If you double the motor torque, does the robot go twice as fast? What limits it?
- If you reduce the friction coefficient to near zero, what does the wheel do instead of moving the robot?
- At what torque value does the wheel start slipping? Can you find it experimentally?

## Implementation

The simulation runs on `browser/common/engine.js`, which provides `Vec`, `Body`, and `World` primitives. `browser/chapter01/index.html` exercises the friction contact model: the engine computes the tangential impulse at the contact point each timestep and clamps it to μ·N, switching between static and kinetic modes when slip begins.

## When It Breaks

**Traction loss under acceleration.** When a robot accelerates hard, weight transfers rearward. On a rear-wheel-drive configuration this helps; on front-wheel-drive it unloads the driven wheels and causes wheelspin — the exact failure from Attempt 1, now caused by geometry rather than motor power. Formula Student teams manage this with ballast placement.

**Friction varies with surface.** A delivery robot calibrated for concrete will spin its wheels on wet tile or polished hardwood. The 2004 DARPA Grand Challenge failures included robots that drove confidently off-road but lost traction in shallow sand because calibration assumed harder surfaces.

## Transfer

- **Rock-climbing shoes**: the stiffer the sole, the less it conforms to the surface, the less friction available — opposite of the "smooth is better" intuition.
- **Aircraft braking**: anti-lock brakes on planes prevent wheel lockup specifically because sliding friction is lower than static friction; keeping the wheel rolling maintains maximum stopping force.
- **Conveyor belt drives**: the belt moves material because static friction between belt and package exceeds the package's inertial resistance — same contact-patch logic, applied to linear transport.

Exercises:

1. A robot weighs 2 kg. The rubber-on-tile friction coefficient is 0.6. What is the maximum tractive force before the wheel slips? How much torque does that require for a 5 cm radius wheel?
2. Design a wheel for a robot that must operate on both wet grass and dry concrete. What properties must the tread have, and what tradeoffs does each choice impose?
3. A four-wheel robot has all wheels driven. If one wheel loses traction (patches of ice), how does the robot behave, and how would you modify the control to compensate?

---

**Continue → [Why Things Refuse to Move](02-why-things-refuse-to-move.md)**
