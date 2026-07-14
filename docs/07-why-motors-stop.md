# Why Motors Stop

## The Problem

Your robot is supposed to hold a constant speed of 1 m/s. You run it unloaded on a smooth floor: it reaches 1 m/s and maintains it. Then you attach a 500 g payload and the speed drops to 0.7 m/s without any change in the motor command. You increase the command — speed comes back up. Add more payload: drops again.

Meanwhile, you notice the motor draws more current when loaded than when unloaded. And on a steep ramp, the motor may draw so much current it trips the protection circuit.

Something is actively opposing the motor as load increases. It's not just that the motor loses power — something measurable increases its resistance to motion.

Any model of the motor must explain:

- Why speed drops under load even with constant voltage
- Why current rises when speed drops
- Why there is a maximum no-load speed the motor cannot exceed
- Why the system reaches a steady state (not infinite acceleration or deceleration)

## What Would You Try?

- If you could measure current at zero speed (motor stalled) and at maximum no-load speed, what would you predict for each? Sketch I vs ω.
- The motor has a coil spinning in a magnetic field. From Chapter 4, moving conductors in magnetic fields experience forces — but also generate voltages. Could the spinning coil *generate* a voltage that opposes the driving voltage?
- If friction were the only thing slowing the motor under load, would current increase or stay constant? What does actual current increase tell you?

## Failed Attempts

### Attempt 1: Friction increases with speed

The motor slows under load. Friction is the usual cause of things slowing. Maybe bearing friction increases at higher torque, slowing the motor.

But bearing friction should be roughly constant — it doesn't depend on electrical current. Yet we observe current increasing as speed decreases under load. These two facts are linked in a way that friction alone can't explain: something about the motor's *electrical* state is changing as speed changes.

Also: if it were purely friction, you'd expect the motor to eventually stop entirely under sufficient load. But stall current (motor at zero speed) is extremely high — often 5-10× the rated running current. This isn't what friction predicts.

The failure reveals: the opposing mechanism is coupled to the motor's electrical circuit, not just its mechanical bearings.

### Attempt 2: The load adds resistance to the circuit

More load → less speed → as if the circuit has more resistance. Maybe the motor's internal resistance increases somehow?

This doesn't hold up. Motor resistance is a fixed property of the copper windings (R = ρL/A). It doesn't change with load. And if resistance were the issue, you'd expect current to stay constant as you change speed (since V = IR with constant R). But we see current *increase* as speed decreases — the opposite of what more resistance would predict.

The failure reveals: Ohm's law isn't the complete picture. Something else in the circuit is opposing the supply voltage at running speed but not at stall.

### Attempt 3: Mechanical friction grows with torque

Under load, you need more torque. Torque comes from current (τ = NBIA). More current means more force, which means more friction at the bearings and brushes. So friction torque grows proportionally to load, canceling any speed increase.

This produces a torque-speed curve with the right shape but predicts that at zero load, zero current flows (because there's nothing to oppose). In reality, a no-load motor still draws a small current to overcome bearing friction and move its own rotor inertia. More critically, at no load, the motor has a maximum speed — a hard speed limit that current can't push past. Friction growth doesn't predict any speed ceiling.

The failure reveals: there must be an effect that grows with speed itself and opposes the supply voltage — creating a speed limit when it equals the supply.

## The Discovery

The rotating coil inside the motor is a conductor moving in a magnetic field. From Chapter 4, moving conductors in magnetic fields experience forces. By symmetry, moving conductors also *generate* voltages — this is electromagnetic induction (the inverse of the Lorentz force).

As the motor speeds up, the coil cuts field lines faster, generating a voltage that opposes the supply voltage. This is **back-EMF** (back-electromotive force): V_back = kω, where k is the motor's velocity constant and ω is the angular velocity.

The actual current in the motor circuit is I = (V_supply − V_back) / R = (V_supply − kω) / R.

At zero speed: V_back = 0, so I = V_supply/R (maximum current, maximum torque — this is stall current).
As speed increases: V_back grows, current falls, torque falls.
At no-load maximum speed: V_back ≈ V_supply, current ≈ 0, torque ≈ 0.

Under load, the motor must produce torque, which requires current, which requires a gap between supply voltage and back-EMF — meaning the motor slows until V_back drops enough to allow the required current. The steady-state speed under any given load is set by this electrical equilibrium.

## Try It

<iframe src="../assets/browser/chapter07/index.html" width="100%" height="460" style="border:1px solid var(--md-default-fg-color--lightest);border-radius:8px;"></iframe>

[open in a new tab](../assets/browser/chapter07/index.html)

Before changing anything, predict:

- At maximum no-load speed, what is the motor current? What determines this speed?
- If you double the supply voltage but keep the same load, does the speed double?
- Where does the motor run most efficiently — near stall, near no-load, or somewhere in between?

## Implementation

`browser/common/engine.js` models motor dynamics as a first-order electrical system: V_supply − kω − IR = L·dI/dt, with mechanical dynamics τ_motor − τ_friction − τ_load = I·dω/dt. `browser/chapter07/index.html` plots the torque-speed curve and shows where the operating point settles for a given load, exercising the coupled electrical-mechanical state variables in the engine.

## When It Breaks

**Stall current destruction.** At stall (ω = 0), back-EMF is zero and current is limited only by winding resistance. For a motor rated at 2A running current, stall current might be 15A. Sustained stall overheats and destroys windings in seconds. Robot joints that hit hard stops without current limiting are a common failure mode; industrial drives use stall detection or current foldback to prevent this.

**Speed regulation under varying load.** Because motor speed depends on back-EMF = V_supply − IR, any current variation (from load change) directly changes speed. A robot requiring precise constant-speed motion cannot rely on open-loop voltage control — speed varies with every load change. This is why closed-loop speed control (feedback from an encoder) is nearly universal in precision applications.

## Transfer

- **Power drills**: the torque-speed curve explains why a drill "bogs down" under heavy load — back-EMF drops, current surges, torque increases to match the load, at a lower speed. The drill doesn't stall until the load torque exceeds the stall torque.
- **Electric vehicles**: regenerative braking uses the motor as a generator. When you brake, back-EMF exceeds supply voltage, current reverses, and the motor pushes energy back into the battery. The same back-EMF that limits motor speed here becomes the energy recovery mechanism.
- **Fan laws**: a centrifugal fan's load (air resistance) scales as ω². The motor's torque-speed curve intersects this quadratic load curve at the operating point. This is why fan speed is so sensitive to duct restrictions.

Exercises:

1. A motor has R = 1Ω, k = 0.05 V·s/rad, and supply voltage 12V. Calculate: (a) stall current and torque, (b) no-load speed, (c) current at ω = 100 rad/s.
2. An elevator motor must hold 200 N·m of torque at 50 rpm continuously. Using the stall-to-no-load speed relationship, estimate what supply voltage is needed to keep the motor in its efficient operating range (not too near stall or no-load).
3. Back-EMF is proportional to speed. Design a simple speed sensor using just a motor's own back-EMF. What measurement do you make, and what limits its accuracy at very low speeds?

---

**Continue → [Why Brushes Had to Disappear](08-why-brushes-had-to-disappear.md)**
