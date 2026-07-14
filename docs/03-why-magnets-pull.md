# Why Magnets Pull

## The Problem

You need to build an actuator that can exert force across a gap — no physical contact, no moving linkages. Solenoid valves, motor bearings, magnetic encoders all depend on this. Before you can build any of them, you need to understand how a force can jump across empty space.

A permanent magnet pulls a steel nail from 5 cm away. Nothing visible connects them. The nail accelerates toward the magnet even in vacuum. This shouldn't work if forces require contact — and yet it does, reliably.

Any explanation must satisfy:

- It must work in vacuum (no air as medium)
- It must explain why the force has direction (attraction vs repulsion)
- It must explain why some metals respond and others don't
- It must explain why the force weakens with distance but doesn't cut off sharply

## What Would You Try?

- If forces require contact, what "invisible contact" could explain a magnet pulling through air? Draw what you think might be there.
- A magnet attracts a nail but repels another magnet's north pole. How does your proposed mechanism produce both behaviors from the same object?
- A copper coin doesn't respond to a permanent magnet. An iron nail does. What property distinguishes them?

## Failed Attempts

### Attempt 1: Something invisible touches the nail

The most intuitive model: there must be invisible filaments or particles streaming from the magnet that physically grab the nail. Like invisible hands.

This fails experimentally in multiple ways. The force persists in complete vacuum. More importantly, the force is *bidirectional* — if you hold the nail still, the magnet is pulled toward the nail with the same force. Invisible filaments would have to push and pull simultaneously. And they'd have to radiate outward in all directions simultaneously to explain why the nail is attracted regardless of which side faces the magnet.

The failure reveals: if the mechanism is contact-based, it requires contact in every direction at once — which is indistinguishable from saying there's a *region* around the magnet where space itself is altered.

### Attempt 2: Gravity explains it

Magnets and nails attract. Gravity makes things attract. Maybe magnetism is a form of gravity, or gravity is stronger near magnets.

This breaks immediately: magnets repel. Two north poles push apart with measurable force. Gravity never repels. Also, a magnet hung from a string aligns north-south regardless of local topography — it's not responding to nearby mass. And aluminum is heavy but completely nonmagnetic; iron is denser than aluminum but responds strongly.

The failure reveals: whatever causes magnetic attraction also causes repulsion depending on orientation. Gravity has no orientation dependence. Magnetism requires a concept gravity lacks: *polarity*.

### Attempt 3: Any metal should respond

Iron responds. Steel responds. You might guess the property is "electrical conductor" — metals conduct electricity, so they should respond to magnetic forces.

Take a copper rod and a magnet. No attraction. Aluminum? No attraction. Yet both conduct electricity far better than iron. Now take a ceramic magnet (not a metal at all) — it attracts iron perfectly well. The conducting property is irrelevant.

The failure reveals: the responding property is not conductivity. Iron's atoms have unpaired electrons whose magnetic moments align within microscopic *domains*. Copper and aluminum have paired electrons — their moments cancel. Without domains that can align, no net force.

## The Discovery

Every failed attempt circled the same insight: the magnet must alter *the space around it* in a way that exerts force on susceptible materials regardless of contact, direction, or medium.

The alteration is the **magnetic field** — a vector quantity defined at every point in space, even vacuum. The field radiates outward from the magnet's poles, curving from north to south. Where the field lines are dense, the field is strong; where they spread, it's weak. This naturally explains the distance dependence (lines spread as 1/r²) and the directionality (lines have orientation, giving attraction and repulsion).

The susceptibility of iron (but not copper) follows from domain structure: iron's unpaired electron spins make atoms into tiny dipoles that align with an external field, amplifying it locally and experiencing a net force toward regions of stronger field. Copper's paired electrons have no net dipole to align.

Formally: the magnetic flux density **B** (in Tesla) is the vector field; force on a magnetic dipole is **F** = ∇(**m** · **B**), where **m** is the dipole moment. Permanent magnets have a fixed **m**; soft iron acquires a temporary **m** by domain alignment.

## Try It

<iframe src="../assets/browser/chapter03/index.html" width="100%" height="460" style="border:1px solid var(--md-default-fg-color--lightest);border-radius:8px;"></iframe>

[open in a new tab](../assets/browser/chapter03/index.html)

Before changing anything, predict:

- If you double the distance between the magnet and the nail, does the force halve, quarter, or change by some other factor?
- If you flip the magnet around, what changes about the force on the nail?
- What happens to the field lines between two north poles vs a north and a south pole?

## Implementation

`browser/common/engine.js` models the magnetic field as a dipole potential and computes force via the field gradient. `browser/chapter03/index.html` renders field lines as streamlines and lets you place ferromagnetic objects to observe attraction/repulsion. The engine's `Body` primitive carries a magnetic moment property that drives field-mediated forces.

## When It Breaks

**Field interference between motors.** Two brushless motors mounted close together generate overlapping magnetic fields. Depending on orientation, they can attract or repel each other's rotors, producing vibration at harmonics of the rotation speed. Drone frames space motors deliberately to minimize cross-coupling.

**Ferromagnetic contamination.** A magnetic encoder on a robot joint reads the field from a small permanent magnet mounted to the shaft. Any iron filings or nearby ferromagnetic material distort the field and produce position reading errors. The 2003 Mars Exploration Rover had magnetic dust collectors specifically to study this effect on Mars — and to protect instruments from ferrous contamination.

## Transfer

- **MRI machines**: the patient's hydrogen nuclei are magnetic dipoles; a strong external field aligns them; RF pulses tip them out of alignment; they precess back and emit measurable signals. The entire imaging chain depends on the same dipole-in-a-field physics.
- **Magnetic bearings**: industrial compressors use electromagnets to levitate the shaft, eliminating mechanical contact and friction. Requires active feedback control because the equilibrium is unstable — any displacement increases the field gradient toward that side.
- **Credit card stripes**: the magnetic coating stores data as regions of opposite field polarity (domains). The read head detects transitions between regions.

Exercises:

1. A permanent magnet's field drops as 1/r³ for a dipole (not 1/r²). At 10 cm it exerts 1 N. Estimate the force at 20 cm and at 30 cm.
2. Design a simple magnetic encoder that converts shaft angle to a voltage signal. What property of the field do you measure, and what limits the angular resolution?
3. Two identical magnets are mounted on parallel rails, free to slide. Predict the equilibrium configuration (positions and orientations) and explain why it's stable or unstable.

---

**Continue → [Why Electricity Can Push](04-why-electricity-can-push.md)**
