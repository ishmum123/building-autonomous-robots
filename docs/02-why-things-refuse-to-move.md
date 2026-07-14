# Why Things Refuse to Move

## The Problem

You've built a robot arm. The motor is powerful enough — you checked the spec sheet. You send full current. The arm twitches and stops. The payload barely moved.

You add a gearbox to multiply torque. The arm lifts — but slowly, agonizingly slowly. You tune your controller to ramp up faster. The arm accelerates for half a second, then overshoots and oscillates. Everything that should help seems to make a different thing worse.

Something fundamental is fighting you, and it's not friction — the bearings are smooth and you can push the unloaded arm with one finger.

Any solution has to account for:

- The same motor produces different accelerations depending on what's attached
- Removing friction doesn't remove the resistance
- The resistance scales with how quickly you try to change speed, not with how fast things move
- No material change fixes it — it's a property of mass itself

## What Would You Try?

- If you removed all friction from the joints and bearings, would the arm accelerate instantly when you apply torque? Why or why not?
- Two identical arms, one carrying 500 g, one carrying 2 kg. Both get the same motor command. Describe what you expect to see at t=0, t=0.5s, t=2s.
- Is there a physical reason a more powerful motor can't solve this problem completely?

## Failed Attempts

### Attempt 1: Bigger motor

The arm won't move fast enough. The fix is obvious: more torque. Swap the motor for one twice as powerful.

The arm now accelerates twice as fast. But the problem hasn't been solved — it's been scaled. The 2 kg payload still takes a finite time to reach speed, and if you double the payload again, you're back to the same struggle. You can never buy your way out with raw power because the amount of power needed scales with the mass and the acceleration you demand simultaneously (P = F × v = m × a × v).

The failure reveals: motor power and payload mass are locked in a permanent ratio. The fundamental issue isn't lack of power; it's that mass requires energy to be accelerated and that takes time.

### Attempt 2: Eliminate friction

A well-oiled arm on a frictionless surface should respond instantly to any force, right? Friction is what makes things hard to move.

Put the robot arm on air bearings: essentially zero friction. Apply a small torque. The arm accelerates — but slowly. Same problem. Apply ten times the torque. It accelerates ten times as fast. Friction was never the cause. Something else is scaling exactly with the force you apply.

The failure reveals: inertia and friction are orthogonal. Friction creates a constant resistive force regardless of acceleration. Inertia creates a resistive force proportional to acceleration. Eliminating friction leaves inertia completely intact — in fact, now you can measure inertia cleanly.

### Attempt 3: Fast-ramp the current

If the issue is slow response, ramp up motor current faster. Apply maximum current at t=0 rather than stepping up gently.

The arm does move faster initially. But on a heavy payload, maximum current for an instant barely starts the motion — and if you're trying to reach a precise position, the arm accelerates so hard it blows past the target and the controller has to fight back. The problem shifted from "slow" to "unstable."

The failure reveals: the issue is not signal shaping — it is the physical reality that acceleration accumulates into velocity which accumulates into position. You cannot get a massive object to a precise position quickly without managing the energy you've put into it. Inertia stores kinetic energy during acceleration and demands it back during deceleration.

## The Discovery

Every attempt failed for the same reason: mass doesn't just sit there passively — it *actively resists any change in its state of motion*. An arm at rest resists starting. An arm moving at speed resists stopping. The resistance isn't mechanical; it's a fundamental property of matter.

The size of the resistance is exactly proportional to how fast you try to change the velocity. Double the acceleration demand, double the resistive force. This is why Attempt 1 worked but only temporarily — more motor torque bought more acceleration, but the ratio of force to acceleration stayed constant. That constant is the mass.

This means a robot arm with a 2 kg payload genuinely requires twice the torque to achieve the same acceleration as one with a 1 kg payload. No amount of engineering eliminates this. The only legitimate response is to *know the mass* and *plan the motion accordingly* — which is why trajectory planning exists.

Formally: **F = m·a** (Newton's second law). Inertia is mass m. The rotational equivalent: **τ = I·α**, where I is the moment of inertia and α is angular acceleration.

## Try It

<iframe src="../assets/browser/chapter02/index.html" width="100%" height="460" style="border:1px solid var(--md-default-fg-color--lightest);border-radius:8px;"></iframe>

[open in a new tab](../assets/browser/chapter02/index.html)

Before changing anything, predict:

- If you triple the mass of the simulated object and apply the same force, how does the time to reach a target speed change?
- At what mass does the controller start to struggle? Is there a threshold, or a gradual degradation?
- If you could remove all friction but keep the mass, how does the motion profile change?

## Implementation

`browser/common/engine.js` tracks each `Body`'s momentum and applies `F = ma` each timestep via Euler integration. `browser/chapter02/index.html` lets you vary mass and applied force and observe the resulting acceleration. The engine separates friction (velocity-dependent clamping) from inertia (mass × acceleration) so both effects are visible independently.

## When It Breaks

**Inertia at joint transitions.** A robot arm changes its effective moment of inertia as it extends and retracts. A controller tuned for the arm fully retracted (low I) may cause violent oscillation when the arm is fully extended (high I). Industrial robots use real-time inertia estimation or conservative gains that work across the full range.

**Payload surprises.** A warehouse robot may pick up packages ranging from 0.1 kg to 30 kg without prior knowledge of the weight. If the controller assumes light payload and the package is heavy, the motor command sends far less current than needed, the arm sags, and position error accumulates. Amazon's Sparrow arm uses torque sensing to estimate payload inertia before each pick.

## Transfer

- **Car braking distances**: a loaded truck requires far longer to stop than an empty one at the same speed — same deceleration demand, far higher inertia means far higher required force and distance.
- **Spacecraft attitude control**: reaction wheels on a satellite spin up to rotate the spacecraft; the satellite's moment of inertia determines how fast that works. Cassini's attitude control thrusters were sized around the spacecraft's known inertia tensor.
- **Human reflexes**: catching a thrown ball requires your arm to accelerate quickly; your brain pre-programs the motion because feedback loops are too slow to react mid-flight. The mass of your arm sets the minimum reaction time.

Exercises:

1. A motor produces 0.5 N·m of torque through a gearbox with 20:1 ratio. The robot arm has a moment of inertia of 0.04 kg·m². What angular acceleration results? How long to reach 2 rad/s from rest?
2. An arm's moment of inertia doubles when extended. If the controller applies constant torque, sketch the angular velocity profile as the arm extends from retracted to fully extended mid-motion.
3. Why does adding a counterweight to a robot arm reduce the required motor torque but not the required motor power during fast moves? What does the counterweight actually change?

---

**Continue → [Why Magnets Pull](03-why-magnets-pull.md)**
