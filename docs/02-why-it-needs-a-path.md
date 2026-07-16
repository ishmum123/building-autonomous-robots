# Why It Needs a Path

## The Problem

You have your two handles — voltage and current. Now try to use them. Connect your pile to something and watch what happens: current leaks through the wooden table, through your fingers if you touch it, through the damp air on a humid day. It seems to go wherever it wants.

This is a problem. A flow that goes everywhere is a flow you can't control. You want it here, driving this device. Not there, warming your fingers or burning through the insulation.

Any solution must satisfy:

- Current flows exactly where you intend and nowhere else
- You can route it around corners, through confined spaces, over long distances
- The routing material doesn't steal the energy you're trying to deliver
- When the path gets bigger or smaller, you can predict how that changes the flow

## What Would You Try?

- Touch the terminals of a small battery to a metal spoon, a wooden stick, a glass rod, a piece of copper pipe. Notice: some complete the connection, some don't. What's the pattern?
- The metal that doesn't resist much is a conductor. The material that blocks it is an insulator. Now: how do you use one to carry and the other to confine?
- A pipe carries water. A fat pipe carries more per moment than a thin pipe at the same pressure. Does the same logic apply to your flow?

## Failed Attempts

### Attempt 1: Wrap the path in something dry

Electricity seems to need moisture to leak. On a dry day the sparks are sharper but also more contained. Maybe just keep everything dry — use dry wood, dry air, dry hands.

This predicts: perfectly dry conditions eliminate leakage entirely; humidity is the enemy; any dry material can serve as a barrier.

Experimentally: dry wood still conducts enough to drain a battery overnight. Dry air is an excellent barrier at low voltages — but push to a few thousand volts and it sparks anyway. The leakage doesn't disappear; it just shifts thresholds. Dryness is not a reliable barrier.

The failure reveals: "conducting" and "blocking" aren't about moisture — they're properties of the material itself. Some materials have many charges free to move (metals especially); some have almost none free to move at all (glass, rubber, dry ceramics). The difference is built into atomic structure, not surface condition.

### Attempt 2: Use any metal — they're all conductors

Metals conduct. Pick the cheapest: iron. Wind your path out of iron wire.

Iron works — current does flow. But the wire gets hot, the battery drains faster than expected, and at the end less current arrives at the device than left the source. Something is eating the push along the way.

Compare iron to copper: copper wire of the same length and thickness runs cool and delivers almost all the current. Silver wire is slightly better still — but costs ten times as much. Iron, by comparison, wastes roughly six times more push per meter.

The failure reveals: not all conductors are equal. The property that matters is **resistivity** — how much resistance a meter-long, one-millimeter-square rod of the material offers. Copper sits at 1.7 × 10⁻⁸ Ω·m; silver at 1.6 × 10⁻⁸ (barely better, dramatically more expensive); iron at 10 × 10⁻⁸. For practical wiring, copper is the answer: near-best conductor, available in large quantities, cheap enough to run through walls.

### Attempt 3: Make the wire as thin as possible to save material

Wire is expensive and heavy. Use the thinnest gauge that still carries the signal.

A thin wire saves copper. But connect it to a motor drawing real current and the wire heats up — sometimes to glowing, sometimes past the point where the insulation melts. The path itself becomes a heater, wasting the push you meant to deliver.

The failure reveals: wire cross-section isn't about saving material — it's about capacity. A thin path offers more resistance (R = ρL/A: smaller area A → larger resistance). More resistance means more push wasted as heat per amp of flow. Double the cross-section, halve the resistance. A thicker wire isn't luxury; it's how much flow the path can safely carry. This is why electrical codes specify minimum wire gauge for every current level: not aesthetics, but the physics of how much a path fights back.

## The Discovery

Two categories of material, opposite properties, used together:

**Conductors** — materials where charges move freely when pushed. Metals are the main family: their outer electrons are loosely held and drift in response to any voltage. Copper is the standard because it combines very low resistivity with abundance and workability. Silver is marginally better but 50× more expensive; gold is used at contact surfaces to resist corrosion, not for bulk conduction; aluminum is used for power lines (lower conductivity, but lighter and cheaper per amp per kilometer of long runs).

**Insulators** — materials where charges are bound tightly in place. Glass, rubber, most plastics, dry ceramics, most wood. When you push on them with ordinary voltages, nothing moves. The same atomic structure that holds charges fixed makes them excellent barriers: electrons can't jump from atom to atom.

The trick: use a conductor to carry the flow where you want it, surrounded by an insulator to keep it from going anywhere else. This is a **wire** — copper inside, plastic outside. The copper handles the flow; the plastic handles the confinement. The combination lets you route current across a room, around corners, through walls, with no significant loss and no leakage into the world.

Wire thickness sets how much flow the path can carry. Undersized wire doesn't block current — it heats up trying to carry it, and becomes a fire hazard. Every conductor has a current rating, not because it stops working above that rating, but because it starts destroying itself.

## Try It

<iframe src="../assets/browser/chapter02/index.html" width="100%" height="460" style="border:1px solid var(--md-default-fg-color--lightest);border-radius:8px;"></iframe>

[open in a new tab](../assets/browser/chapter02/index.html)

Before changing anything, predict:

- With copper wire and insulation OFF, where does current go — all to the lamp, or does some leak away?
- If you switch the wire to wood, what happens to lamp brightness? Why?
- Turning insulation ON removes the leak path. Does lamp current increase, decrease, or stay the same?

## Implementation

The sim (`browser/chapter02/index.html`, using `browser/common/engine.js` and `browser/common/ui.js`) shows a voltage source feeding a lamp through a copper or wood wire, with an optional parallel leak path to ground. A voltage slider (1–12 V) sets the source; a toggle switches between copper (high conductance) and wood (near-zero); a second toggle adds or removes insulation, which eliminates the leak path entirely. Animated orange dots flow along the main wire proportional to lamp current; red dots travel the dashed leak arc when insulation is off. A strip plot traces lamp vs. leak current over time; metrics show I_lamp (mA), I_leak (mA), and lamp brightness as a percentage.

## When It Breaks

**Insulation breakdown at high voltage.** Every insulator has a dielectric strength — a maximum voltage per millimeter before it stops blocking and sparks through. Rubber might handle 10 kV/mm; air handles about 3 kV/mm. This is why high-voltage equipment uses thick, specially rated insulation, and why a damaged wire jacket is a fire and electrocution risk at mains voltage.

**Thin wire on high current.** A wire at its current limit is already running at the edge. Any brief overload — a motor starting, a short circuit — can melt the copper or char the insulation before any protection device responds. This is why fuses and breakers exist: not to protect the device, but to protect the wire.

## Transfer

- **Coaxial cable**: a central copper conductor, a plastic dielectric layer, a copper braid outer conductor, then an outer jacket. Geometry chosen so the signal can't leak out and outside interference can't get in — conductor and insulator working together in two directions simultaneously.
- **Printed circuit boards**: thin copper traces etched into precise paths on a fiberglass (insulating) board. The trace width encodes the current rating; a trace too thin for its load chars brown and fails.
- **Overhead power lines**: aluminum cable steel-reinforced (ACSR), no insulation — air is the insulator. The towers are ceramic-insulted at the attachment points to prevent current from taking the path through the steel tower and into the ground.

Exercises:

1. A 10-meter copper wire (1.7 × 10⁻⁸ Ω·m) has a 2 mm² cross-section. Calculate its resistance. Now the same run in iron (10 × 10⁻⁸ Ω·m). How much more push is wasted in the iron run if 3 A flows?
2. You need to carry 20 A over 5 meters. Standard copper wire ratings (American Wire Gauge): 14 AWG handles 15 A, 12 AWG handles 20 A, 10 AWG handles 30 A. Why does using 10 AWG when you only need 20 A still make engineering sense?
3. A spark jumps a 2 mm air gap. Air's dielectric strength is about 3 kV/mm. What voltage does this imply? What does this tell you about the minimum insulation thickness needed for a 600 V circuit?

---

**Continue → [Why You'd Bottle It](03-why-youd-bottle-it.md)**
