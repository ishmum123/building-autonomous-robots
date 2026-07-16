# Why Motors Spin

## The Problem

You have an electromagnet (a coil carrying current) and a permanent magnet. You know they attract and repel. You want them to produce continuous rotation, not just a single snap to alignment and stop.

The trap is obvious in hindsight: if you just hold current constant, the electromagnet snaps to align with the permanent magnet and sits there. You get one twitch of rotation, then magnetic lock. The rotor is pinned to the stator like a compass needle to north.

Getting continuous rotation means somehow defeating this locking tendency — making the electromagnet always present a repulsion or attraction that is *slightly ahead* of where the rotor currently is, so there's always torque pulling it forward.

Any design must:

- Produce torque in the same direction regardless of rotor angle
- Avoid locking the rotor to a fixed position
- Scale — higher current should mean higher torque throughout the rotation
- Work continuously without burning up the switching mechanism

## What Would You Try?

- If the electromagnet locks to the permanent magnet, what would happen if you reversed the electromagnet's polarity just as the rotor reaches alignment? Sketch the sequence.
- Is there a rotor angle where switching current direction would produce no torque? What should happen at that exact moment?
- Could you use a mechanical linkage to flip current direction automatically as the shaft rotates?

## Failed Attempts

### Attempt 1: Constant current, just push through

If the electromagnet isn't strong enough, maybe we just apply more current. The torque will overpower the locking tendency.

At any current level, the physics doesn't change: the torque on a dipole in a field is τ = m × B × sin(θ), where θ is the angle between them. At θ = 0 (aligned), sin(0) = 0 — torque is zero regardless of current. The rotor reaches alignment with some angular velocity, overshoots slightly, gets pulled back, and oscillates to rest at alignment. More current gives faster approach but the same zero-torque lockup at the end.

The failure reveals: torque is geometrically zero at alignment, independent of current magnitude. The problem is topological, not a matter of power.

### Attempt 2: Use a spring to push it past alignment

If the rotor locks at alignment, add a mechanical spring that kicks it past the deadpoint. The electromagnet then pulls it around to the next half-rotation.

This produces two strokes of rotation per cycle but fails at high speed: the spring and rotor form a resonant system that only works efficiently at one particular speed (the spring's natural frequency). Below or above that speed, the spring is either too early or too late. Early sewing machine motors actually tried spring-assisted designs — they were speed-sensitive and difficult to control.

The failure reveals: a passive mechanical element can't adapt to the rotor's instantaneous position. The switching needs to be position-triggered, not time-triggered.

### Attempt 3: Switch current on a timer

Set up a relay or switch to flip current direction at a fixed frequency — say, 60 Hz. At low motor speeds, this is too fast: the current flips before the rotor reaches alignment and it gets pulled backward. At high speeds, too slow: the rotor overshoots alignment and the attraction becomes braking.

The failure reveals: the switching must track the rotor's actual angle, not the clock. The commutation event must be triggered by position, not time. Something mechanical needs to read the shaft angle and trigger the switch.

## The Discovery

All three failures converged on the same requirement: the current direction must flip at the exact moment the rotor passes through the alignment point — the point of zero torque. Before that point, one polarity maximizes forward torque. After that point, the opposite polarity maximizes forward torque.

The solution is to couple the switching mechanism directly to the shaft. Attach a split ring (commutator) to the shaft and let spring-loaded contacts (brushes) ride on it. As the shaft rotates, the split ring sweeps past the brushes and swaps the coil connections at exactly the right angle — automatically, without any sensor or logic.

This is the DC motor: a coil (rotor/armature), a commutator attached to the same shaft, and brushes that deliver current. The commutator ensures the electromagnet always presents the same magnetic face to the stator regardless of rotor angle. Torque is approximately constant throughout the rotation (with some ripple from the geometry).

Formally: torque τ = NBIA per coil turn, where N is turns, B is field, I is current, A is coil area. With proper commutation, this torque acts continuously in the same direction. Power P = τω.

## Try It

<iframe src="../assets/browser/chapter12/index.html" width="100%" height="460" style="border:1px solid var(--md-default-fg-color--lightest);border-radius:8px;"></iframe>

[open in a new tab](../assets/browser/chapter12/index.html)

Before changing anything, predict:

- At what shaft angle does the commutator switch? What is the torque at that exact instant?
- If you increase the number of coil segments (and commutator segments), how does the torque ripple change?
- What happens if the brushes are mechanically offset from the optimal switching angle?

## Implementation

`browser/common/engine.js` provides `Body` and drawing helpers. The commutation logic is inline in `browser/chapter12/index.html`: each frame `phase = Math.floor(t / commutePeriod) % 2` selects the torque direction, `torque = phase === 0 ? pushStrength : -pushStrength`, and angular velocity is updated as `angVel += (torque + drag) * 0.016` using plain scalar integration. The sim makes the commutation event visible as the discrete phase-A/phase-B color switch on the rotor arrows.

## When It Breaks

**Commutation sparking.** The coil is inductive (it's a solenoid). When the commutator switches, the current doesn't stop instantly — inductance tries to maintain it. The energy dumps across the air gap between brush and commutator as a spark. At high speeds and currents this arc erodes the commutator surface and degrades brushes rapidly. Carbon deposits or pitting reduces contact quality, increasing resistance and causing more sparking — a self-reinforcing failure mode.

**Brush bounce at speed.** At high RPM, the brushes skip across the commutator segments rather than maintaining steady contact. The resulting intermittent current connection causes torque ripple, electrical noise, and commutator wear. This is one of the speed limits of DC motors and drove the development of brushless designs (Chapter 14).

## Transfer

- **Alternators in cars**: the opposite conversion — mechanical rotation produces electrical current via the same rotating coil and commutator (or slip rings), but now you're generating AC from the spinning armature.
- **Tape recorder motors**: early tape machines required constant-speed motors; the commutator geometry was precision-machined to minimize torque ripple that would cause "wow and flutter" in playback speed.
- **Windshield wipers**: a DC motor with a cam mechanism that switches direction at each end of travel — essentially a two-position commutator that reverses the motor rather than the current.

Exercises:

1. A DC motor has 12 commutator segments. Over one full rotation, how many times does the current direction switch in each coil? Sketch the torque vs. angle curve for 2-segment and 12-segment commutators.
2. A motor brushes are offset 10° from the optimal switching angle. Qualitatively, how does this affect torque at low speed vs. high speed (where back-EMF changes the optimal angle)?
3. You want to reverse a DC motor's rotation direction. What are two ways to do it, and what are the tradeoffs?

---

**Continue → [Why Motors Stop](13-why-motors-stop.md)**
