# Why the Path Fights Back

## The Problem

You have a stored source and a wire to carry the flow. Connect them and watch: the source drains faster than you predicted. The wire warms up. The device at the other end receives less push than the source claims to provide.

Energy is disappearing. The wire is taking it. You didn't design the wire to do that — it was supposed to just carry the flow — but it's consuming push on the way.

Any account of this must satisfy:

- Explains where the missing push goes (and why it always appears as heat)
- Gives a quantitative relation between push, flow, and how much each length of path resists
- Explains why the heating scales much faster than the current (double the current, more than double the heat)
- Explains how to design for it: if the wire always heats, can you control where and how much?

## What Would You Try?

- The wire heats regardless of material — but more for iron, less for copper. What property of the material determines this?
- You have a fixed source. A long wire wastes more push than a short one. A thick wire wastes less than a thin one. What single formula captures both?
- If the heating is unavoidable, flip the question: can you engineer the path to heat a *specific* place a *specific* amount — and use that heat as the product?

## Failed Attempts

### Attempt 1: The push just leaks into the air

Energy disappears from the wire — maybe it radiates away, like light from a hot surface. Surround the wire with a perfect insulator and the loss should stop.

This would predict: a perfectly insulated wire delivers push with zero loss; energy disappears through the outer surface, not inside the material.

Experimentally: a well-insulated wire runs *hotter* than an uninsulated one (less heat escapes, same generation inside) and the source still drains at the same rate. The loss is inside, not at the surface. Insulation keeps the heat from escaping; it can't stop the heat from being generated.

The failure reveals: the energy isn't leaking into the air — it's being converted to heat *within the conducting material itself*, by the very act of carrying the current.

### Attempt 2: Push and flow losses are proportional

More current means more heating. So heat must scale linearly with current — double the current, double the heating.

In 1840 James Prescott Joule ran careful experiments with measured currents, measured resistances, and calorimeters to capture every bit of heat. The result: heating is proportional to the current *squared*, not the current. P = I²R, not P = IR. This means doubling the current produces four times the heating; tripling it produces nine times.

The failure reveals: the relation isn't linear because current both drives the push and *responds to* resistance — more current also fights more resistance, compounding the effect.

### Attempt 3: Resistance varies unpredictably with conditions

Heat changes everything. Maybe resistance changes with temperature in a way that's too complex to model. Just measure it empirically case by case.

Georg Simon Ohm did something simpler. In 1827 he held temperature constant, varied the voltage across a wire, and measured the resulting current. The relationship was perfectly linear: double the voltage, double the current; triple the voltage, triple the current. The ratio V/I was constant — the same for any voltage applied to the same wire. He called it resistance.

V = I × R. Ohm's law. The resistance R is a property of the specific path (its material, length, and cross-section), not of the voltage or current passing through it.

The failure reveals: resistance isn't mysterious. It's constant (at constant temperature) and predictable. The heating follows directly: P = I²R = V²/R = V × I — all equivalent, choose the form with known quantities.

## The Discovery

Every conducting path resists. That resistance converts push into heat. The conversion is exact and unavoidable: P = I²R watts, always, wherever current flows through resistance.

This seems like only bad news. But flip the question: if you *must* lose push to heat somewhere in the circuit, why not choose where? Make the narrow, high-resistance section exactly where you want heat — and put it in something useful.

If you wind a thin, high-resistance wire into a coil and seal it inside an oven, you have a **heating element**. If you take an even thinner wire and seal it inside a glass bulb with no oxygen (so it can't burn), it heats until it glows. An **incandescent bulb**. Edison didn't invent electricity — he engineered a path narrow enough to glow, durable enough to last, in an environment controlled enough not to burn.

The same insight in the other direction: if heat is always proportional to I²R, and you want to send power long distances without losing it to heat, you want *small* current through *small* resistance. But small current at useful power means *large* voltage (P = V × I). This is why power lines run at hundreds of kilovolts: for the same power delivered, high voltage means low current, and low current means I²R losses that are tiny.

These passive resistances now have a name: **resistors**. You choose their value to control how much current flows where, to drop voltage across a specific point, or to set up precise ratios. Every electronics circuit is partly a set of deliberate resistances placed to control how push and flow distribute.

## Try It

<iframe src="../assets/browser/chapter04/index.html" width="100%" height="460" style="border:1px solid var(--md-default-fg-color--lightest);border-radius:8px;"></iframe>

[open in a new tab](../assets/browser/chapter04/index.html)

Before changing anything, predict:

- If you double the resistance while keeping voltage the same, does the power dissipated double or halve?
- At what combination of voltage and resistance does the wire element glow in the sim? Is it current or voltage that determines glow?
- Two resistors in series carry the same current. The first is 10 Ω, the second is 100 Ω. Which one dissipates more heat — and by how much?

## Implementation

The sim presents a circuit with an adjustable resistor element — a visual wire that changes color from black through red to orange-white as power dissipation increases. Sliders control voltage and resistance; calculated current, power (P = V²/R), and temperature (via a simple thermal model) are displayed in real time. A second panel shows the Ohm's law triangle: drag any two quantities and the third is computed.

## When It Breaks

**Everything in electronics is a heat budget.** Every component has a power rating — the maximum P = I²R it can dissipate without destroying itself. Exceed it and the component fails, usually irreversibly. Resistors are rated in watts (1/8 W, 1/4 W, 1 W...); wires in amperes; transistors in watts with derating curves for temperature. If your design assumes components run cool, it's wrong — every resistor, every wire, every switch gets warmer as current flows.

**Bulb burnout is the resistance winning.** An incandescent filament operates at 2500°C because it must to produce visible light. At that temperature the tungsten slowly evaporates, thinning the filament. Thinner means higher resistance; higher resistance means even more concentrated heat at that spot; the filament burns through there first. Every bulb carries its own cause of death in its design.

## Transfer

- **Wire gauge standards**: national electrical codes specify minimum wire gauge (cross-section) for every current level — not to prevent the wire from breaking, but to keep I²R heating below the level that ignites insulation. The limit is thermal, not mechanical.
- **Fuses**: a thin metal element designed to melt at a known current. The fuse is intentionally the weakest thermal link in the circuit — it sacrifices itself before the wiring or device reaches its failure temperature.
- **Electric stoves and kettles**: the resistance of the heating element is chosen to dissipate exactly the rated wattage at mains voltage. P = V²/R → R = V²/P. A 1000 W kettle at 230 V needs R = 52.9 Ω. The engineering is in choosing a resistance wire alloy (Nichrome: high resistivity, high melting point) and forming it to achieve exactly that value.

Exercises:

1. A 220 Ω resistor has a ¼ W power rating. What is the maximum voltage you can apply across it without exceeding its rating? Maximum current?
2. You transmit 10 kW over a wire with 1 Ω total resistance. Calculate I²R loss at 100 V (so 100 A) vs. 10,000 V (so 1 A). What fraction of power is lost in each case?
3. An incandescent bulb rated "60 W at 120 V" is connected to 60 V instead. Assuming resistance is constant, what power does it now dissipate? (In reality filament resistance changes with temperature — why would the actual power be even lower than your calculation?)

---

**Continue → [Why You Need a Gate](05-why-you-need-a-gate.md)**
