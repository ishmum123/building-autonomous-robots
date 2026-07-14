# Why Copper Becomes a Magnet

## The Problem

You want a motor that can be switched on and off, varied in strength, and pointed in any direction. Permanent magnets are too rigid — fixed field, fixed direction, no control. You need a magnet you can tune.

The clue is in what we already know: current in a wire creates a force on nearby magnets. So current affects magnetic fields. Can current *create* one?

A single copper wire suspended near a compass will deflect the needle slightly when current flows. That's a real magnetic field from an electrical conductor. But it's weak — far too weak for any practical motor. Getting from "slight compass deflection" to "useful actuator" requires understanding what amplifies the effect.

Any design must:

- Produce a field strong enough to exert useful force on iron or another coil
- Be switchable (on/off with the current)
- Be tunable (field strength controllable by current)
- Be directable (field axis set by geometry, not by material properties)

## What Would You Try?

- A single wire creates a weak field. How would you get more field from the same current?
- If the field comes from the moving charges in the wire, what happens to the field when you stop the current? What does this tell you about where the field is "stored"?
- The field from a straight wire circles around it. How do you turn that circular field into a useful directional field for a motor?

## Failed Attempts

### Attempt 1: Copper is just a weaker permanent magnet

A permanent magnet holds its field after you remove the external field. Maybe copper is similar — maybe current "charges" it magnetically and you could turn off the power and keep the field.

Test: run high current through a copper bar for an hour. Cut the power. Hold the bar near a compass. No deflection. The field vanishes with the current. Try again with iron filings on a table — nothing.

But here's the subtlety: run current through the copper while it's inside a coil of iron wire. Cut the power. Now the iron near the coil *is* slightly magnetized — but the copper bar isn't. The copper was never the magnet; it was creating conditions for the iron to magnetize.

The failure reveals: copper (and all non-ferromagnetic conductors) have no unpaired electron spins to form persistent domains. The field exists only while charges are moving. This is actually *better* for control — it means field strength tracks current precisely, with no hysteresis.

### Attempt 2: More voltage means stronger field

Voltage drives current, current makes field, so more voltage should make stronger field. Double the voltage for double the field.

This is almost right but misses a critical constraint. Put 24V across a short copper rod with 0.01Ω resistance: you get 2400A, and the rod glows red before you measure any field. The field depends on current, not voltage. Voltage drives current through whatever resistance the circuit has. For a given wire, doubling voltage and doubling resistance gives the same current and the same field — with twice the heat.

The failure reveals: field strength scales with current × turns in the coil. To get strong field efficiently, you want many turns (to multiply the current's effect) while keeping resistance low. This is the core tension in electromagnet design: more turns means more wire means more resistance.

### Attempt 3: A single straight wire is enough

The compass deflected. Why not just use a long straight wire?

The field around a straight wire is circular — it wraps around the wire. At any point in space, the field direction is tangential to a circle centered on the wire. This is geometrically useless for pushing a rotor: the field lines are perpendicular to the radial direction from the wire, so an iron core placed next to the wire would be pulled sideways, not toward it.

More quantitatively: the field from a straight wire drops as 1/r (slowly), but its geometry means all the field lines at any single point in space from different wire segments partially cancel each other. Winding the wire into a helix (solenoid) makes all segments' contributions add in the same direction along the axis.

The failure reveals: geometry is as important as current magnitude. A solenoid concentrates the field into a useful axial direction; a straight wire scatters it radially. Inside the solenoid, field contributions from all N turns add constructively: B ≈ μ₀nI, where n is turns per meter.

## The Discovery

The straight-wire attempt was closest but missed the superposition principle. Every segment of a current-carrying conductor contributes a tiny field at every point in space. For a randomly wound wire, contributions partially cancel. For a carefully wound solenoid, contributions add.

The key insight: you're not making copper magnetic. You're using the motion of electrons to create the *same kind of field* that a permanent magnet has — a dipole field with a north end and a south end — but through geometry and current rather than through material properties.

Wind N turns of wire into a coil, pass current I: you get a magnetic dipole with moment m = NIA (N turns, current I, area A). The field inside the coil is B = μ₀NI/L for a solenoid of length L. Switch the current direction, the dipole flips. Vary I, B tracks it linearly. This is the **electromagnet** — controllable, reversible, and scalable.

## Try It

<iframe src="../assets/browser/chapter05/index.html" width="100%" height="460" style="border:1px solid var(--md-default-fg-color--lightest);border-radius:8px;"></iframe>

[open in a new tab](../assets/browser/chapter05/index.html)

Before changing anything, predict:

- If you double the number of turns while keeping current the same, does the field double, quadruple, or something else?
- If you double the current while keeping turns the same, what changes?
- What happens to the field direction when you reverse the current? What happens to the force on a nearby iron nail?

## Implementation

`browser/common/engine.js` models the solenoid as a stack of circular current loops, summing their Biot-Savart contributions along the axis. `browser/chapter05/index.html` renders field lines and lets you vary turn count and current to observe the B-field, exercising the `Vec` field summation primitive and the dipole force model built on top.

## When It Breaks

**Saturation of the iron core.** Add an iron core to a solenoid and the field can jump 1000× (due to iron's high permeability). But iron saturates: above a certain field strength, all domains are already aligned and adding more current adds no more B. A motor designed for 1A operation that accidentally runs at 3A gains almost nothing in field strength but wastes 9× the copper heat (P = I²R).

**Inductance delays current.** A solenoid resists changes in current due to self-inductance (L = μ₀N²A/ℓ). Switch it on and current takes time τ = L/R to reach steady state. For a high-turn, low-resistance coil this lag can be milliseconds — long enough to ruin high-speed motor control. Brushless motor controllers must account for winding inductance in their timing.

## Transfer

- **MRI scanner coils**: superconducting solenoids running at ~150 A create 1.5–7 T fields. The design challenge is the same: maximum field from minimum wire volume, constrained by resistance (solved by superconductivity) and saturation (solved by using air core, no iron).
- **Relay switches**: an electromagnet pulls a ferromagnetic lever to open or close a circuit. Used for over a century to let a weak signal control a high-current circuit — the same N × I × geometry principle, applied to a switch.
- **Transformers**: two coils wound around the same iron core. The field from one coil (primary) threads through the secondary, inducing a voltage proportional to the turns ratio. The same superposition that makes solenoids efficient makes transformers work.

Exercises:

1. A solenoid has 500 turns, length 10 cm, diameter 2 cm, and carries 0.5 A. Estimate the field at the center using B = μ₀NI/L. What current would produce 0.1 T?
2. Adding an iron core (relative permeability μᵣ = 1000) multiplies the field by μᵣ. But the core saturates at 1.5 T. What current in the 500-turn solenoid would saturate it?
3. An electromagnet in a relay must switch on in under 1 ms. The coil has L = 10 mH and R = 5Ω. What supply voltage is needed to reach 90% of steady-state current in 1 ms? (Use τ = L/R.)

---

**Continue → [Why Motors Spin](06-why-motors-spin.md)**
