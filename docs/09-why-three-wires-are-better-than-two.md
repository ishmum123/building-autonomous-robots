# Why Three Wires Are Better Than Two

## The Problem

You've decided to build a brushless motor (Chapter 8). The stator has coils; the rotor has permanent magnets. The controller energizes the coils to pull the rotor forward. But how many coils do you need, and how should they be arranged?

Start with the simplest case: one coil, two wires. Current flows in, creates a field, pulls the magnet. When the magnet reaches alignment, you switch current direction to push it past. This works — it's basically a solenoid with a rotating target.

But every time you switch, there's a moment of zero torque (at alignment, the geometry provides no turning force). With one coil, the motor pulses. You can hear the torque ripple. For a quadcopter spinning at 8000 RPM, this pulsation is a mechanical vibration transmitted to the frame — noise and structural stress at every revolution, thousands of times per second.

Any multi-coil design must:

- Produce torque throughout the full rotation with minimal dead zones
- Use the minimum number of phases that achieves smooth rotation
- Allow the controller to know which coil to energize when
- Not require arbitrarily many wires (more wires = heavier, more complex)

## What Would You Try?

- If one coil produces torque ripple at alignment, what would two coils placed 180° apart do? Sketch the combined torque vs. angle.
- Two coils 180° apart: when coil A is at its zero-torque point (at alignment), where is coil B? What is coil B's torque at that moment?
- Is there a number of phases where the torque ripple completely cancels? What geometry produces this?

## Failed Attempts

### Attempt 1: Two coils, 180° apart, two extra wires

Place a second coil exactly opposite the first. When coil A passes through zero torque (alignment), coil B is 180° away — at maximum torque position. Alternate: when A is energized, B is off, and vice versa.

Two-phase works! Torque ripple is significantly reduced. But it's not eliminated: there are still moments where neither coil is at its peak, and the combined torque dips between commutation events. The remaining ripple frequency doubles (two dips per revolution instead of one), making it higher pitched but still present.

More critically: two coils with separate windings means 4 wires to the motor (two per coil). The return path requires either a separate wire or a common ground. Four-wire motors exist but are mechanically awkward — the wire bundle to the stator is heavy and the controller needs 4 power stages rather than 3.

The failure reveals: going from 1 to 2 phases improves smoothness but doesn't eliminate ripple, and the 4-wire configuration is mechanically clumsy.

### Attempt 2: Many coils (12, 24, 48...) for maximum smoothness

If two is better than one, more must be better. Put 12 coils evenly spaced. Each coil is energized in sequence. Torque ripple approaches zero as coil count grows.

This works electrically — DC servo motors with 12+ coils exist and are extremely smooth. But each coil pair needs independent power switching. 12 coils means 12 independent driver stages, 24+ transistors, complex wiring, significant weight and cost. For a motor that must weigh under 50 grams on a quadcopter arm, a 12-phase driver is absurd.

The failure reveals: smoothness and complexity are in direct tension. There should be a minimum number of phases that achieves "good enough" smoothness without combinatorial explosion of hardware.

### Attempt 3: Three coils, 120° apart, all sharing a common return wire

If two coils leave a ripple and many coils are impractical, try three. Place three coils evenly at 120° intervals. Run three wires out, connected to a common neutral point inside the motor (star/Y configuration). Now only 3 wires are needed.

Surprisingly, this is nearly optimal. The three torque contributions are:
- Coil A: τ_A = T_max · sin(θ)
- Coil B: τ_B = T_max · sin(θ + 120°)
- Coil C: τ_C = T_max · sin(θ + 240°)

Their sum: τ_total = T_max · [sin(θ) + sin(θ+120°) + sin(θ+240°)] = 0... but wait.

The sum of three equal sinusoids 120° apart is identically zero. This seems catastrophic — but the trick is that you don't energize all three simultaneously with the same current. You energize them with *phase-shifted currents*: I_A = I_max·sin(ωt), I_B = I_max·sin(ωt+120°), I_C = I_max·sin(ωt+240°). Now the torques combine to give constant total torque.

The failure reveals the actual question: it's not about how many coils but about how you time the currents. With three-phase sinusoidal currents 120° apart, total torque is constant with zero ripple — in theory. And only 3 wires needed.

## The Discovery

The third attempt succeeds when you realize the insight that three sinusoidal currents 120° apart, driving three coils 120° apart, produce a magnetic field that *rotates continuously* rather than switching in steps. The rotor chases the rotating field.

This is the **rotating magnetic field**: three stationary coils, fed with three sinusoids 120° out of phase, create a field that sweeps around the stator smoothly. The rotor magnets lock to this field and rotate with it — like a compass needle following a rotating external magnet.

Three is the minimum number of phases that achieves a continuously rotating field with no dead zones. Fewer than three always leaves gaps. More than three work but require more hardware for diminishing returns (the next improvement would be 5-phase or 6-phase, used in some precision servo systems).

Formally: for three-phase balanced currents and coils at 120° separation, the resultant field amplitude is constant at (3/2)·I_max·B_per_amp and rotates at the frequency of the supply. This is three-phase AC — the same principle that powers industrial motors worldwide.

## Try It

<iframe src="../assets/browser/chapter09/index.html" width="100%" height="460" style="border:1px solid var(--md-default-fg-color--lightest);border-radius:8px;"></iframe>

[open in a new tab](../assets/browser/chapter09/index.html)

Before changing anything, predict:

- The simulation shows the combined field vector from all three coils. As current phases advance, which way does the field vector rotate?
- If one of the three phases is disconnected (one wire breaks), what happens to the rotating field? To the torque?
- What does the rotor do if the field rotates faster than it can follow?

## Implementation

`browser/common/engine.js` provides `Body` (for the rotor) and `addTorque`. The three-phase logic is inline in `browser/chapter09/index.html`: each frame `phA = amplitude * Math.sin(t)`, `phB = amplitude * Math.sin(t + 2.094)`, `phC = amplitude * Math.sin(t + 4.189)`, then `rotor.addTorque(phA + phB + phC)` and `rotor.step(0.016)`. The summed torque is nearly constant because the three sinusoids 120° apart sum to zero ripple — visible in the strip plot.

## When It Breaks

**Phase loss.** If one of the three wires breaks or a MOSFET fails in the controller, the motor runs on two phases. The rotating field becomes pulsating rather than continuously rotating: peak torque drops, torque ripple spikes, vibration increases. The motor may still turn at low load but sounds rough. Industrial motor protection relays detect phase imbalance and shut down the motor.

**Field-rotor slip (in induction motors).** In brushless DC motors the rotor magnets lock to the rotating field — no slip. In induction motors (which use the same rotating field principle), the rotor must slip behind the field to induce currents that produce torque. Running an induction motor near synchronous speed gives low torque, not high efficiency. Control systems must maintain the right slip frequency, which varies with load.

## Transfer

- **Power grid distribution**: the global AC power grid uses three-phase for exactly this reason — three-phase power has constant instantaneous power delivery (the sum of three phase-shifted sinusoids), while single-phase fluctuates. Data centers and heavy industry run three-phase.
- **Stepper motors**: a 2-phase stepper uses the same two-phase principle from Attempt 1 — deliberately using the discrete positions (steps) rather than trying to eliminate them. The pulsation is a feature, not a bug, enabling precise position control without a position sensor.
- **Brushless gimbal motors**: camera stabilization gimbals use 3-phase BLDC motors run with sinusoidal current (not trapezoidal) for ultra-smooth rotation that doesn't transmit vibration to the camera. The smoothness depends critically on three-phase balance.

Exercises:

1. Three coils are placed at 0°, 120°, 240°. At t=0, current in coil A is I_max, coil B is −I_max/2, coil C is −I_max/2. Calculate the direction and relative magnitude of the combined field.
2. A 6-pole BLDC (3 pole pairs) rotates at 1800 RPM. What frequency of three-phase AC does the controller supply? (Pole pairs × mechanical RPM / 60 = electrical Hz.)
3. A three-phase motor suddenly loses one phase mid-operation. The motor is driving a constant load. Describe the mechanical and electrical behavior over the next few seconds.

---

**Continue → [Why Motors Need Conductors](10-why-motors-need-conductors.md)**
