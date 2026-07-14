# Why Motors Need Conductors

## The Problem

You're designing the stator windings for a brushless motor. You need to pass as much current as possible through the coils to maximize torque (τ ∝ NIA), while keeping the motor from overheating and destroying itself.

The tradeoff is immediate: more current means more torque, but also more heat (P = I²R). The winding resistance determines how much heat each amp of current generates. Cut resistance and you can run more current for the same temperature rise.

But winding resistance isn't a free variable. It depends on the wire material (resistivity ρ), the wire cross-section (A), and the total wire length (L = N·turns·circumference). You can't independently optimize all of these.

Any winding design must:

- Minimize resistive heating at the required operating current
- Fit within the stator slot geometry (limited cross-sectional area)
- Carry the current without insulation breakdown
- Remain mechanically stable under thermal cycling and vibration

## What Would You Try?

- Motor resistance R = ρL/A. If you double the wire diameter (quadrupling cross-section), what happens to resistance per unit length? What happens to the maximum number of turns that fit in the slot?
- If you switch from copper wire (ρ = 1.7×10⁻⁸ Ω·m) to aluminum (ρ = 2.8×10⁻⁸ Ω·m), how does that change the resistance for the same geometry?
- A motor coil is simultaneously a magnetic field source and a resistor. What determines whether a given coil produces more torque or more heat for each watt of input power?

## Failed Attempts

### Attempt 1: Use iron wire for the windings

Iron wire conducts electricity. Iron is also magnetic. If the coil wire itself is ferromagnetic, maybe the field is stronger because the wire itself contributes to the magnetic flux. Two benefits from one material.

Test this: wind two identical coils, one copper wire, one iron wire. Drive the same current through each. Measure the field.

The field is essentially the same (both driven by current, not by wire material). But the resistance is wildly different: iron's resistivity is ~10×10⁻⁸ Ω·m — almost 6× higher than copper. The iron coil dissipates 6× more heat for the same current. The small (and largely imaginary) magnetic contribution from the iron's permeability doesn't compensate.

The failure reveals: winding conductor choice is about resistivity, not about magnetism. The field comes from the current; the material just needs to carry that current with minimum loss.

### Attempt 2: Use thicker wire to reduce resistance

Thicker wire has lower resistance (R = ρL/A, bigger A → smaller R). Run more current for the same temperature. More current → more torque.

The problem is the slot fill factor. The stator slots have a fixed total area. Thicker wire means fewer turns fit in the slot. Torque is proportional to NI (turns × current). If you double wire diameter (4× cross-section), resistance per turn drops 4×, allowing 2× current. But you fit only ¼ as many turns. Net change: NI goes from N·I to (N/4)·(2I) = NI/2 — the torque *halves*.

The right analysis: for a fixed slot area, the product N·I (amp-turns) is constrained by total fill and current density. More turns of thin wire or fewer turns of thick wire can give the same amp-turns, but copper fill efficiency matters more than either choice alone.

The failure reveals: winding optimization is about maximizing amp-turns per unit heat, not maximizing either N or I alone. The slot fill factor (fraction of slot area occupied by copper) is the key design parameter.

### Attempt 3: Use superconducting wire for zero resistance

If resistance causes all the problems, eliminate resistance. Superconductors have exactly zero resistance below their critical temperature.

Superconducting motors exist and are extraordinary — very high power density, no resistive heating. But they require cooling to cryogenic temperatures (typically 4–77 K depending on material). A robot motor operating at liquid helium temperatures is a science project, not an engineering product. The cooling infrastructure outweighs the motor by orders of magnitude.

More fundamentally: even at zero DC resistance, superconductors have AC losses in time-varying fields (from flux vortex motion). A motor's changing currents mean the windings aren't truly dissipationless in practice. And the critical current density of superconductors still limits the maximum current before they quench (suddenly become resistive), which is catastrophic.

The failure reveals: zero resistance isn't achievable in practical operating conditions. The problem reduces to: given copper (the best common conductor) and real slot geometry, how do you wind it to maximize torque per watt of heat?

## The Discovery

Every failed attempt circled the same fundamental constraint: in a fixed slot, the heat generated per unit torque is set by the current density in the copper, not by any single design variable.

The insight is that resistive loss P = I²R = (I·L)²ρ/(A·L) = J²·ρ·(slot volume), where J is current density. For a fixed slot volume and fixed allowable temperature rise, the maximum allowable current density J_max constrains how much amp-turns you can pack in.

Given this constraint, the right answer is copper (lowest ρ among practical room-temperature conductors), wound to maximize the **copper fill factor** (fraction of slot area that's actual conductor, not insulation, air gaps, or winding bobbin). High fill factor means: round wires fit poorly (gaps between cylinders), so precision motors use **rectangular (square) wire** that tessellates without gaps; or **Litz wire** for high-frequency applications; or **hairpin windings** for EV motors (copper bars inserted and welded, achieving near-100% fill).

The formal constraint is: for a slot of cross-sectional area A_slot, maximum amp-turns = J_max · (k_fill · A_slot), where k_fill is the fill factor. Good hand-winding achieves ~40%; hairpin winding achieves ~70–80%.

## Try It

<iframe src="../assets/browser/chapter10/index.html" width="100%" height="460" style="border:1px solid var(--md-default-fg-color--lightest);border-radius:8px;"></iframe>

[open in a new tab](../assets/browser/chapter10/index.html)

Before changing anything, predict:

- If you increase wire diameter in the sim, does peak torque go up or down? Why?
- What fill factor does the simulation achieve with round wire vs. square wire?
- At what point does increasing conductor cross-section give no further benefit in torque?

## Implementation

`browser/common/engine.js` computes torque from amp-turns and resistive loss from current density. `browser/chapter10/index.html` visualizes the slot cross-section and lets you vary wire gauge and winding pattern, showing how fill factor, resistance, current, and resulting torque all interact.

## When It Breaks

**Thermal runaway at sustained load.** Copper resistance increases with temperature (~0.4%/°C). If cooling is insufficient, high current heats the wire, resistance rises, for the same voltage more power dissipates as heat (P = V²/R — wait, P = I²R; for voltage-limited drives, current drops as R rises, reducing torque — but for current-limited drives with thermal runaway, insulation melts before current drops). The insulation (typically polyimide rated to 180°C) fails before the copper melts. Motor is destroyed by insulation failure, not melting wire.

**Eddy currents in solid conductors at high frequency.** At high electrical frequencies, current in a solid conductor concentrates at the surface (skin effect). A 1 mm diameter wire has a skin depth of ~66 μm at 1 kHz. The inner conductor carries no current — effective resistance increases dramatically. High-frequency drives (FOC at high switching frequency) in motors with solid copper windings see elevated AC resistance. Litz wire (many individually insulated fine strands twisted together) breaks up the eddy currents.

## Transfer

- **Transformer windings**: power transformers use copper or aluminum windings around a ferromagnetic core. The same fill factor and copper vs. aluminum tradeoff applies; high-power transformers use copper because the smaller cross-section for the same resistance reduces core window area.
- **MRI gradient coils**: large coils that must switch enormous currents quickly. They use water-cooled copper conductors because no other conductor sustains the required current density without melting. The cooling infrastructure dominates the magnet assembly size.
- **Fuses**: a wire designed to fail at a specific current density. The conductor cross-section is chosen so I²R at the rated blow current melts the fuse wire in a defined time — the same physics engineered as a feature rather than a constraint.

Exercises:

1. A slot has area 4 mm². Round wire with k_fill = 0.45 is used. The conductor is copper (ρ = 1.7×10⁻⁸ Ω·m). If wire diameter is 0.3 mm and the slot length is 20 mm, estimate total copper resistance and achievable amp-turns at 4 A/mm² current density.
2. A motor is rewound with the same gauge wire but the insulation thickness is doubled (for higher voltage). How does this affect fill factor and maximum amp-turns?
3. An EV motor uses hairpin windings with k_fill = 0.75 compared to a conventional wound motor with k_fill = 0.45. For the same slot geometry and temperature limit, how much more torque can the hairpin motor produce?

---

**Continue → [Why Faster Isn't Better](11-why-faster-isnt-better.md)**
