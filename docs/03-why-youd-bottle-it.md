# Why You'd Bottle It

## The Problem

You have voltage and current. You have a wire to carry them. Now the question is *when*. Your source — a voltaic pile, a hand-cranked generator — is only useful while it's connected and operating. The moment you disconnect it, everything stops. The flow doesn't wait. It doesn't linger in the wire.

But your robot can't always be tethered to a generator. A device that only works when plugged in to a large source isn't useful in the field. You need to carry the push with you — pick it up somewhere, carry it somewhere else, release it on demand.

Any storage mechanism must satisfy:

- Stores enough to be useful, not just a brief flash
- Releases it in a controlled, predictable way
- Can be charged, carried, discharged, charged again
- Doesn't dump all its stored energy at once in the act of measurement

## What Would You Try?

- The flow is in motion. To store it, your instinct is to catch some moving thing. What if you kept it moving in a loop?
- Alternatively: the push is the useful part. What if you didn't try to store the flow at all — just preserve the *pressure* that would produce flow if a path existed?
- Volta's pile is stacked metal discs separated by wet cardboard. It produces push as long as the chemical reaction runs. What's happening chemically, and could you reverse it?

## Failed Attempts

### Attempt 1: Keep it flowing in a loop

Current is moving charges. Moving charges have momentum. Run the current in a closed loop with no resistance and it should keep going forever — no need to recharge.

This predicts: a perfectly conducting loop, once started, circulates current indefinitely. You've stored the flow itself.

Experimentally: all real conductors have some resistance. Even a very small resistance bleeds the energy out as heat over time. More practically: even if you could freeze the current in place, extracting it is the problem — the moment you open the loop to connect a device, the flow stops. You've built a very brief source, not storage. And even in theory, the energy stored in a current loop (the magnetic energy ½LI²) is tiny compared to the energy stored in a chemical battery of similar size.

The failure reveals: storing the *flow* is the wrong target. The flow is the useful output, not the thing to preserve.

### Attempt 2: Coil the wire — store it in the field

A current creates a magnetic field around it. That field stores energy. Wind a lot of wire into a tight coil (an *inductor*) and a lot of field energy sits in the space around it. When you disconnect the source, the field collapses and the energy... goes back into a current. Briefly.

This works — briefly. The problem is "briefly." The magnetic field collapses in microseconds. The energy is real but the *duration* is useless for powering anything that takes more than a moment to operate. You've stored electromagnetic energy, but you can't sustain it.

The failure reveals: magnetic energy storage requires continuous current flow to maintain the field. Stop the current and the field — and its stored energy — vanish nearly instantly. Not a battery replacement.

### Attempt 3: Catch lightning in a jar

Lightning is enormous energy. In 1745 Ewald von Kleist and Pieter van Musschenbroek independently discovered that a glass jar, lined inside and out with metal foil, could be charged with a static electricity machine and retain a powerful shock. The Leyden jar. This is real storage — the energy sits there waiting, and you can retrieve it.

But charge a Leyden jar as large as you can make from a thunderstorm and then try to light a lamp for an evening. The jar delivers its entire charge in a single violent flash — typically in under a millisecond. The *total* energy stored is real, but the *rate* of release is uncontrollable. You get one instant of blinding brightness, then nothing.

The failure reveals: you can't catch lightning in a jar and use it slowly. What you've discovered is genuine storage of the *push* (voltage) — but with no mechanism to control the *rate* of release. You need storage that releases at a controlled rate, not all at once.

## The Discovery

Two solutions, two compromises, two completely different engineering stories:

**Store the push on two plates.** Two metal surfaces, separated by an insulator, with opposite charges on each face. The charges can't cross the insulator — so the push (voltage) remains, waiting. Connect a path and current flows — only until the imbalance equalizes, then stops. This stores energy quickly, releases it quickly, and can do so millions of times without degradation. Your invention has a name: **capacitor**. The Leyden jar was the first one. A modern ceramic capacitor stores far less energy than a battery of the same size, but it charges and discharges in microseconds.

**Store the push in chemistry.** Two different metals in a chemical solution undergo a spontaneous reaction that separates charges — pushing positive charges to one terminal and negative to the other, maintaining the push as long as the chemical reaction continues. Volta's insight was that the reaction at the metal-solution interface is the source of the push. Reverse the reaction (by pushing current back in the wrong direction) and you reload the chemical potential. A battery. Galvani's frog leg twitched because dissimilar metals in biological tissue form exactly this kind of cell. Your **battery** stores much more energy than a capacitor, releases it over hours, and can (usually) be recharged.

Neither solution is better — they're different. Capacitors handle short bursts; batteries handle sustained loads. Modern systems use both: a battery for steady supply, capacitors to absorb sudden current spikes the battery can't respond to fast enough.

## Try It

<iframe src="../assets/browser/chapter03/index.html" width="100%" height="460" style="border:1px solid var(--md-default-fg-color--lightest);border-radius:8px;"></iframe>

[open in a new tab](../assets/browser/chapter03/index.html)

Before changing anything, predict:

- If you double the capacitor's plate area, does it store twice the charge, twice the voltage, or both?
- A battery and a capacitor both read 9 V. Connect each to the same load. How do their discharge curves differ?
- If a battery loses voltage under load (sags), what does that tell you about its internal resistance?

## Implementation

The sim runs two parallel discharge scenarios side by side: a capacitor (exponential decay, fast) and a battery model (roughly flat voltage until near-empty, then rapid drop). Sliders control initial charge, load resistance, and capacitor plate area. A shared time axis lets you compare the voltage-over-time curves directly. The battery model uses a simple internal-resistance approximation: V_terminal = V_emf − I × R_internal.

## When It Breaks

**Voltage sag under load.** Every real battery has internal resistance. When you draw current, the terminal voltage drops: V_terminal = V_emf − I × R_internal. A "12 V" battery delivering 10 A through a 0.1 Ω internal resistance actually provides 11 V. Under heavy load the sag can be severe enough to reset electronics that need a stable 5 V.

**Self-discharge.** Neither capacitors nor batteries hold their charge forever. Capacitors leak through their dielectric; batteries react slowly even with no external path. A fully charged lithium cell loses roughly 1–2% per month at rest. A supercapacitor (very large capacitance, low voltage) can self-discharge in days. Storage that "stores forever" doesn't exist.

## Transfer

- **Camera flash**: a capacitor charges slowly from a small battery over a second, then dumps everything into the flash tube in microseconds — far more power than the battery alone could deliver that quickly.
- **Electric vehicle regenerative braking**: the motor runs as a generator during braking, pushing current back into the battery. Recharging is just forcing the chemical reaction backward, exactly as Volta's analysis predicted.
- **Uninterruptible power supply (UPS)**: a battery holds the push ready; when mains power fails the battery takes over in milliseconds. The capacitors on the circuit boards smooth the transition — battery can't respond in microseconds, capacitor can.

Exercises:

1. A 100 µF capacitor is charged to 12 V. How much energy is stored (E = ½CV²)? If you discharge it into a 100 Ω resistor, roughly how long until the voltage drops to 4.4 V (one time constant τ = RC)?
2. A lithium-ion cell has 3.7 V nominal voltage and 2000 mAh capacity. How much energy does it store in joules? A 100 W load draws how many amps at 3.7 V, and how long would this cell power it?
3. Why does a battery's terminal voltage sag more under heavy loads but recover when the load is removed? Design an experiment to measure the internal resistance of a AA battery using only a multimeter and a known resistor.

---

**Continue → [Why the Path Fights Back](04-why-the-path-fights-back.md)**
