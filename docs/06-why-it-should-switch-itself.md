# Why It Should Switch Itself

## The Problem

Every gate you've built so far needs your hand. Flip a switch. Connect a wire. Press a button. That works for one switch, operated once. But a robot needs to respond to conditions you can't anticipate, faster than you can react, in places your hand can't reach.

Your motor speed changes as the terrain changes — you need the switch to react in milliseconds, not the second it takes your hand to move. Your remote control sends a tiny signal: you need that signal to operate a gate controlling a much larger power. You need to be in ten places simultaneously, none of them physically accessible.

Any self-operating gate must satisfy:

- A small input controls a large output — the control signal does not need to supply the output power
- Switching speed is limited by electronics, not by mechanics or human reaction time
- No moving parts to wear out
- The mechanism is reversible: the gate can be open or closed as many times as needed

## What Would You Try?

- You have a gate. What could drive it? Another electrical signal — a small current instructing the gate to open or close for a big current.
- Imagine a switch that is held open by a spring but pulled closed by a magnet. If that magnet is an electromagnet (a coil of wire), what controls the magnet? A current. So a current in one circuit controls a switch in another.
- Take this further: what if the gate material itself responded to a tiny electrical signal — not mechanically, but atomically?

## Failed Attempts

### Attempt 1: Use a human as the gate

For slow processes — turn on a heater when the room gets cold, open a valve when the tank fills — a human operator checking periodically is acceptable. They observe, decide, act.

But a human checks at best once a second, and only one thing at a time. A DC motor commutates thousands of times per second. A radio signal arrives in nanoseconds. A computer executes millions of decisions per second. Human-operated gates scale to exactly one human.

The failure reveals: the bottleneck is the interface between observation and action. Any gate that requires a human to notice and respond is limited by human attention and reaction time, not by physics.

### Attempt 2: Use the current itself to flip a latch

Run a large current through a special path that — once started — latches itself on. The signal starts it; it maintains itself. Gate logic: one tiny pulse, self-sustaining flow.

This works, and the thyristor (SCR) is exactly this device. But a latch without a way to unlatch is a one-shot trigger, not a gate you can open and close arbitrarily. To turn it off you must remove the power entirely. That limits what you can build: you can trigger things, not control them continuously. A motor you can start but not stop isn't useful.

The failure reveals: a gate needs both transitions — open and close — under independent control. A latch only gives you one.

### Attempt 3: A mechanical relay

An electromagnet, energized by a small control current, pulls a lever that closes a high-current contact. The relay. This is the first self-operating gate, invented before semiconductors existed. Telephone exchanges used millions of them.

The relay works. A few milliamps in the coil controls amps in the contact. The control circuit and the switched circuit are physically separate — a small sensor signal can control mains voltage without danger.

But a relay is still mechanical. Its contact bounces on closure (a few milliseconds of chatter). It has operating speed limited to milliseconds (not microseconds). It wears — the contacts arc and pit, just like a manual switch. At 1000 operations per day, a relay rated for 10 million cycles lasts 27 years; at 10 million operations per day (common in industrial automation), it fails in a day. And it's large, heavy, and makes a clicking noise.

The failure reveals: mechanical gates solve the signal-amplification problem but not the speed and longevity problem. What you need is a gate that switches in nanoseconds, never wears, and has no moving parts.

## The Discovery

The semiconductor junction you met in the diode has a third option beyond "conduct forward" and "block reverse." Introduce a third terminal that controls the height of the barrier itself — and you have a gate that a tiny voltage or current can open and close without any moving part.

This is the **transistor**. A small current or voltage applied to the control terminal (the *base* or *gate*) modulates how easily current flows between the two main terminals (the *collector/emitter* or *source/drain*). At the control signal, the gate is open; without it, closed. Switching in nanoseconds, millions of times per second, for decades without wear.

The consequences cascade:

**Amplification.** A 1 mA control current can modulate 1 A of output current. A weak microphone signal can drive a speaker. A radio antenna signal can control motor power. The transistor is an amplifier whenever you use it in its partial-on region.

**Logic.** Run the transistor fully on or fully off — never between. Now "on" is 1 and "off" is 0. Wire several transistors together so that one transistor's output is another's input and you have decisions made of electricity. AND, OR, NOT — every logical operation is a configuration of transistors.

**Scale.** Two transistors fit in a relay's footprint. Two billion fit on a modern processor chip. The relay solved self-switching. The transistor solved *scale*.

The brushed DC motor of chapter 14 fails because its mechanical commutator — a switch running at thousands of operations per minute — wears. The brushless motor replaces those mechanical switches with transistors switching in microseconds. The same insight that lets a radio signal control a motor also lets a motor run without brushes.

And the glimpse that all of this implies: enough transistors switching fast enough, arranged to combine their logic, can represent any computation. The robot's motor controller, its sensor processor, its navigation algorithm — all are transistors switching, guided by transistors switching, built on the same physical insight: a tiny trickle of electricity can open and close a gate on a large flow, without any hand required.

## Try It

<iframe src="../assets/browser/chapter06/index.html" width="100%" height="460" style="border:1px solid var(--md-default-fg-color--lightest);border-radius:8px;"></iframe>

[open in a new tab](../assets/browser/chapter06/index.html)

Before changing anything, predict:

- Below the threshold (0.5 mA), what do you expect the main channel current to be? Above it?
- If the gain is 50, what main current do you expect at a control current of 1 mA?
- Press Blink — the control current pulses automatically. What does this show about hands-free switching?

## Implementation

The sim (`browser/chapter06/index.html`, using `browser/common/engine.js` and `browser/common/ui.js`) models an NPN transistor gating a 12 V main channel into a load. A slider sets the control current (0–2 mA); below the 0.5 mA threshold the transistor is off and main current is zero; above threshold it enters a proportional region with a fixed gain of 50, capped by the load's saturation current. A Blink button pulses the control automatically to demonstrate hands-free switching. A strip plot traces the tiny control current alongside the large main current; metrics display I_control (mA), I_main (A), and computed gain.

## When It Breaks

**Transistors fail from heat, not wear.** Unlike relays, transistors have no moving parts and no contact wear. But they dissipate power (P = V_CE × I_C in the on-state; larger during switching transitions). Exceed the thermal limit — even briefly — and the junction structure is destroyed, permanently. Heat sinks, thermal paste, and derating curves exist entirely because of this: a transistor that survives at 25°C ambient may fail at 85°C if not derated.

**Relays fail from arcing and bounce.** The mechanical contact bounces on closure — in digital circuits, a single button press can register as dozens of events in the few milliseconds of bounce. Contact arc on opening erodes metal over time. Both failures have software or hardware workarounds (debouncing, snubber circuits), but they don't go away — they're the mechanical nature of the device.

## Transfer

- **H-bridge motor driver**: four transistors arranged so that two at a time can connect the motor in either polarity, allowing forward, reverse, and brake. The transistors switch in microseconds; the motor changes direction in milliseconds. This is the gate configuration that makes a robot steerable.
- **PWM speed control**: a transistor switched on and off thousands of times per second, with the on-time fraction (duty cycle) varying. The motor sees an average voltage proportional to duty cycle. Speed control without any variable resistor — pure switching. You'll build this in the motor chapters.
- **CPU inside the robot's flight controller**: a billion transistors, each switching between 0 and 1 at a billion times per second, computing PID outputs, sensor fusion, and navigation decisions in real time. The physics is the same transistor you just met, repeated at a scale that requires electron microscopy to see.

Exercises:

1. A transistor has a current gain (β) of 100. The control current is 2 mA. What is the maximum output current? If the output circuit is 12 V and the load is 60 Ω, is the transistor in saturation (fully on) or linear operation?
2. A relay is rated 10 million operations at 5 A. A robot uses it to switch a motor at 5 Hz (5 operations per second). How long before the relay reaches end-of-life? How does this compare to a transistor, which has no wear-related operation count?
3. Design a circuit where a light sensor (produces 0–3.3 V) turns on a 12 V, 2 A motor when the room goes dark. What components do you need? Where does the transistor fit, and why can't the light sensor drive the motor directly?

---

**Continue → [Why Wheels Move](07-why-wheels-move.md)**

You can command power with power — a tiny signal opens a gate on any flow you choose. Now make that flow move the world.
