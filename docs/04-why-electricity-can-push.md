# Why Electricity Can Push

## The Problem

You have a coil of wire and a magnetic field. You know current flows through wire. You know magnets exert forces. Can you make the wire move?

In 1820 Hans Christian Ørsted noticed a compass needle deflecting near a current-carrying wire. In 1821 Michael Faraday hung a wire in a magnetic field, connected a battery, and watched the wire swing. This is the moment that made every electric motor possible.

The challenge isn't getting wire to move. It's understanding *why* it moves — specifically enough to predict which direction, how much force, and what geometry makes it most efficient.

Any explanation must satisfy:

- Explains why the force is perpendicular to both the current and the field
- Explains why a static wire with static current in a static field still moves (no time-varying anything required)
- Explains why more current produces more force, and longer wire in the field produces more force
- Explains why flipping the current direction reverses the force direction

## What Would You Try?

- Current in a wire creates heat. Could the force just be thermal expansion pushing the wire? How would you test this?
- The magnet already exerts forces on ferromagnetic objects. Maybe the current magnetizes the wire? Predict what this theory implies about force direction.
- Draw the wire, the magnetic field lines, and your best guess for the force direction. Then rotate the wire 90°. Does your model correctly predict how the force changes?

## Failed Attempts

### Attempt 1: Current makes heat, heat makes motion

Current definitely heats the wire. Hot things expand. Maybe the wire bends from thermal expansion when current flows.

This would predict: the wire deforms slowly as it heats; force is in a random direction depending on which side is hotter; the force is proportional to current squared (since heating ∝ I²R); reversing current changes nothing (heat is symmetric).

In Faraday's experiment: the wire moves instantly, in a specific direction, force is proportional to I (not I²), and reversing current reverses the direction immediately. Thermal expansion predicts every wrong thing.

The failure reveals: the force is not thermal. It's directional in a way that depends on the sign and magnitude of current, not just its magnitude squared.

### Attempt 2: Current magnetizes the wire; the magnet pulls the wire

Current-carrying wires create magnetic fields (we'll prove this next chapter). So maybe the wire becomes a temporary magnet and the external field attracts it — just like an iron nail.

This predicts: the force should pull the wire toward either pole of the external magnet (attraction); reversing the current should reverse the polarity of the induced magnetism but then the wire would still be attracted (now the other end is closer to the other pole); force should be along the line connecting wire to magnet.

Experimentally: a wire in a uniform field (neither pole closer) still moves, and moves perpendicular to the field, not toward either pole. And the force direction is perpendicular to the wire, not along it.

The failure reveals: the force mechanism is not magnetic attraction between induced and external dipoles. It's something geometrically different — the force is always perpendicular to both the wire and the field simultaneously.

### Attempt 3: The force is along the current direction

Current flows along the wire. Forces might flow along the current. So the wire should be pushed forward along its own axis — squeezed in the direction it's already pointing.

This would predict: a straight wire would be pushed end-to-end; a loop of wire would compress or expand like a spring; the geometry of the magnetic field wouldn't change the direction.

Experimentally: the wire moves sideways — perpendicular to both its own axis and the external field. A horizontal wire in a horizontal field pointing north moves vertically. Rotate the field to point east and the same wire moves north. The force direction tracks the cross product of current direction and field direction, not either one alone.

The failure reveals: the force is a *cross product* — a vector perpendicular to both inputs. This is geometrically unlike any force we've seen so far. It cannot be along either the current or the field.

## The Discovery

All three attempts failed for the same reason: they assumed the force would be along one of the inputs. But the magnetic force on a current is always perpendicular to both — it's the defining signature of what physicists would later call the Lorentz force.

The physical picture: the external magnetic field exerts a sideways push on the moving charges inside the wire. Those charges are constrained to move along the wire (they can't escape), so the sideways push transfers to the wire itself. The direction is perpendicular to the current direction and perpendicular to the field direction simultaneously — exactly a cross product.

This is why a coil of wire in a magnetic field produces torque: each segment of wire experiences a force perpendicular to itself, and if the forces on opposite sides of the coil point in opposite directions, the result is rotation. This is the operating principle of every DC motor ever built.

Formally: **F** = I(**L** × **B**), where I is the current, **L** is the vector along the wire (length and direction), and **B** is the magnetic flux density. The magnitude is F = BIL·sin(θ), maximum when wire is perpendicular to field.

## Try It

<iframe src="../assets/browser/chapter04/index.html" width="100%" height="460" style="border:1px solid var(--md-default-fg-color--lightest);border-radius:8px;"></iframe>

[open in a new tab](../assets/browser/chapter04/index.html)

Before changing anything, predict:

- If you rotate the wire so it's parallel to the magnetic field instead of perpendicular, what happens to the force?
- If you reverse the current direction, which direction does the wire move?
- If you double the current and halve the wire length in the field, does the force change?

## Implementation

`browser/common/engine.js` provides `Body`, `Vec`, and `addForce`. The force calculation is inline in `browser/chapter04/index.html`: when current is on, it calls `wire.addForce(new Vec(0, -liftForce))` where `liftForce` is the slider value, then `wire.step(0.016)`. The sim simplifies F = I(L×B) to a scalar vertical force controlled by a slider — enough to show how current magnitude governs whether the wire lifts or falls, with the cross-product direction shown as on-canvas annotation text.

## When It Breaks

**Force drops to zero at zero angle.** A motor coil aligned with the magnetic field (not perpendicular) produces zero torque — the cross product vanishes. This is the "dead zone" at commutation points in DC motors. Brushed motors use physical commutators to switch current direction before reaching this point; brushless motors use electronic switching timed to the rotor position.

**Back-EMF limits current at speed.** As the wire moves through the field, it generates a back-electromagnetic force (back-EMF) opposing the current. At high speed, back-EMF nearly equals the supply voltage, so actual current — and therefore actual force — drops sharply. This is why motors have a maximum no-load speed and why heavily loaded motors draw far more current than lightly loaded ones.

## Transfer

- **Rail guns**: a conducting projectile sits in rails carrying high current; the magnetic field from the rails themselves provides **B**; the Lorentz force accelerates the projectile. The US Navy experimented with 10 MJ railguns before switching to conventional munitions.
- **Maglev trains**: linear motor coils in the track create a traveling magnetic wave; the train's onboard magnets experience Lorentz force along the track direction, providing propulsion without contact.
- **Galvanometers**: a small coil in a precise field deflects proportionally to current. The original instrument for measuring tiny currents — and the working principle of every analog meter movement.

Exercises:

1. A 5 cm wire carries 2 A in a 0.3 T field. The wire is perpendicular to the field. Calculate the force. Now the wire is at 30° to the field — recalculate.
2. Sketch a rectangular coil in a uniform magnetic field. Mark the forces on each segment. Why does the coil experience torque and not just translation?
3. A railgun uses 1 MA of current across a 10 cm gap in a 1 T field. Estimate the force on the projectile. What engineering challenges does this number imply?

---

**Continue → [Why Copper Becomes a Magnet](05-why-copper-becomes-a-magnet.md)**
