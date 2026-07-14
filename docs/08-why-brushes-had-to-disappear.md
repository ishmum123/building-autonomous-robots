# Why Brushes Had to Disappear

## The Problem

Your robot has been running for six months. The motors start cutting out intermittently. You open one up and find the commutator scored with deep grooves, the brushes worn down to stubs, and black carbon dust packed into every crevice. The motor still works — but for how long?

This is the predictable endpoint of every brushed DC motor: the mechanical contact that makes commutation possible also destroys itself. Brushes press against the rotating commutator ring with spring force. Every revolution, the brush slides across a gap between segments and sparks. Every spark removes material. At 3000 RPM, a motor completes 50 revolutions per second — 50 sparks per second per brush, millions per day.

In a consumer toy, this is acceptable. In a surgical robot, a satellite attitude controller, or a quadcopter motor that weighs 30 grams and must run at 10,000 RPM, it is not.

Any replacement design must:

- Eliminate physical contact between the switching element and the rotor
- Still perform current commutation — switching which coil is powered based on rotor angle
- Operate at higher speeds without mechanical speed limits
- Produce at least as much torque per unit weight

## What Would You Try?

- The brush's job is to deliver current to the rotating coil while also switching which direction the current flows based on shaft angle. Can you separate these two jobs and eliminate one physically?
- If the coils don't need to rotate, what would have to rotate instead?
- A Hall-effect sensor detects magnetic field direction electronically. How could it tell you when to switch current, without any mechanical contact with the shaft?

## Failed Attempts

### Attempt 1: Better brushes — longer-lasting materials

The obvious fix: if carbon brushes wear out, use something harder. Precious metal brushes (gold, silver, platinum) have been tried in high-reliability applications. They last longer.

But the fundamental problem isn't material hardness — it's the spark. Every time a brush crosses a commutator gap, the coil's inductance tries to maintain current flow after contact breaks. That energy releases as an arc. The arc is hotter than any brush material can resist indefinitely. Better materials delay but don't eliminate the failure. And "longer-lasting" brushes are often more expensive than a new motor.

The failure reveals: the material is not the problem. The arc is the problem. The arc exists because you're interrupting an inductive current mechanically. The only fix is to eliminate the mechanical interruption.

### Attempt 2: Sealed brush-commutator in inert gas

Sparks need oxygen to sustain. Run the motor in a nitrogen or argon atmosphere — no oxidation, no erosion, no failure.

Some precision instruments have used this approach (sealed servo motors with inert atmosphere). It works — dramatically extended brush life. But: the motor must be hermetically sealed; cannot vent heat as easily (thermal management becomes critical); impossible to service; adds mass and cost; fails catastrophically when the seal breaks.

Fundamentally, you've treated the symptom (oxidation) not the cause (mechanical contact). The brushes still wear from mechanical friction even without sparking. And you still can't run at 30,000 RPM because of centrifugal forces on the commutator segments.

The failure reveals: hermetic sealing is an engineering patch. The only real solution eliminates physical contact entirely.

### Attempt 3: Move the magnets to the rotor, keep coils fixed

The core problem is delivering current to a rotating coil. What if the coil doesn't rotate? Fix the coil to the stator; move the permanent magnets to the rotor. Now no electrical connection to the rotating part is needed.

This immediately solves the contact problem. But it creates a new question: if the coil is fixed, how does the current switch at the right moment? The commutator was mechanically coupled to the shaft — it knew exactly when to switch because it *was* the shaft. Now you need to know shaft angle without any physical connection to the shaft.

This is the crucial realization. The failure reveals: you've separated the commutation problem from the contact problem. Contact is now solved. You still need position-aware switching — but it can be done electronically, since the coil is stationary and the electronics can be outside the motor entirely.

## The Discovery

The third attempt wasn't a failure at all — it was the solution in disguise. Once the coils are fixed to the stator, the mechanical commutator is no longer needed. Electronic switches (transistors, later MOSFETs) replace the brushes and commutator. A position sensor (Hall-effect sensors responding to the rotor magnets, or back-EMF zero-crossing detection) replaces the mechanical position coupling.

The result is the **brushless DC motor (BLDC)**: stator coils, permanent magnet rotor, no mechanical contact, electronic commutation. Three coils are arranged 120° apart (more on why in Chapter 9). A controller reads rotor position and energizes the coils in sequence to always pull the magnets toward the next position.

Advantages: no wear, no sparking, higher speeds (only limited by bearings and rotor balance), better thermal management (windings on the outside, magnets on the inside), higher efficiency (no brush friction loss, lower resistance path).

Cost: the motor requires a controller (an ESC — electronic speed controller) that would be unneeded for a brushed motor. And the control logic is more complex.

## Try It

<iframe src="../assets/browser/chapter08/index.html" width="100%" height="460" style="border:1px solid var(--md-default-fg-color--lightest);border-radius:8px;"></iframe>

[open in a new tab](../assets/browser/chapter08/index.html)

Before changing anything, predict:

- In a BLDC motor, the controller must know rotor position before deciding which coil to energize. What happens if position sensing lags by 10°?
- If the electronic switches fail to commutate (stuck on one coil), what does the motor do?
- How does the torque ripple of a 3-coil BLDC compare to the DC motor from Chapter 6?

## Implementation

`browser/common/engine.js` provides the core physics; `browser/chapter08/index.html` implements electronic commutation: a position-reading loop selects the active coil pair based on rotor angle, applies the Lorentz torque, and steps the simulation. The commutation table (6 states for 3 coils) replaces the mechanical commutator from Chapter 6's sim.

## When It Breaks

**Demagnetization under excessive current.** Brushless motors use rare-earth permanent magnets (NdFeB). Very high current pulses through the stator coils create opposing fields strong enough to partially demagnetize the rotor magnets — permanently reducing motor constant k and torque. This is irreversible. Drone motors that survive crashes are sometimes "soft" afterwards due to demagnetization.

**Controller timing failure.** BLDC motors depend entirely on the controller commutating at the right angle. If the controller loses position (e.g., back-EMF sensing fails at very low speeds, or Hall sensors are damaged), it sends current to the wrong coils. The result is braking torque rather than driving torque, or no torque at all. The motor makes a grinding or stuttering sound and may lock up.

## Transfer

- **Hard disk drives**: the spindle motor is a BLDC motor running at 5400–15000 RPM. The read head would crash if the motor had any torque ripple from brush contact. BLDC with precise commutation is mandatory.
- **Electric toothbrushes**: the motor is inside a sealed handle that can be submerged in water — impossible with brushes. BLDC through a hermetic shell, driven magnetically.
- **Tesla Model 3 rear motor**: actually an induction motor (not BLDC) but uses the same principle of no rotor electrical connections; the stator fields induce rotor currents electromagnetically. The same problem (contact) solved differently.

Exercises:

1. A brushless motor has 14 pole pairs and runs at 3000 RPM. How many electrical commutation events per second does the ESC perform? (Hint: each mechanical revolution requires 14 × 6 = 84 commutation steps for a 3-phase motor.)
2. Hall sensors for BLDC commutation are typically placed 120° apart around the stator. Design the 6-state commutation table: for each combination of Hall sensor outputs (high/low), which coil pair is active?
3. An outrunner BLDC motor (magnets on the outside, spinning) vs. an inrunner (magnets on the inside). What are the tradeoffs in torque, speed, and form factor? Which would you choose for a quadcopter arm motor?

---

**Continue → [Why Three Wires Are Better Than Two](09-why-three-wires-are-better-than-two.md)**
