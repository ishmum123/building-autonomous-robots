# Why Everything Oscillates

## The Problem

Your robot arm vibrates after each move. Your quadcopter wobbles when it tries to hold altitude. Your motor controller causes the robot base to rock back and forth at 3 Hz. Your PID loop makes the temperature in the hot-end hunt above and below the setpoint continuously.

These are all different systems — mechanical, electrical, thermal — but they share a symptom: the output oscillates around the desired value rather than settling to it.

You try adjusting gains. Sometimes you can reduce the oscillation frequency but not stop it. Sometimes reducing one gain stops oscillation but the system becomes sluggish. It feels like you're fighting a ghost — there's a tendency toward oscillation baked into the physics.

Any model that explains oscillation must explain:

- Why oscillation happens even in systems with no intentional periodicity
- What determines the oscillation frequency (it's always some specific value, not random)
- Why adding damping reduces oscillation but not necessarily speed
- Why the same control gain works fine in one system and causes runaway in another

## What Would You Try?

- A spring with a mass attached bounces when released. What would happen if there were no gravity and no friction — would it ever stop? What energy transfers between each bounce?
- A thermostat overshoots. The room gets too hot, the thermostat turns off the heater, the room cools too far, the heater turns on again. Does the room temperature oscillate? Why?
- A DC motor controller notices the motor is going too slow and applies more power. The motor speeds up — and overshoots. The controller brakes. The motor slows — and undershoots. Is this the same phenomenon as the thermostat?

## Failed Attempts

### Attempt 1: Oscillation is caused by noise

The system is being perturbed by external vibrations, electrical noise, or random disturbances. If you isolate the system better, oscillation will stop.

Install vibration isolation mounts. Add capacitors to filter electrical noise. Run the system in a quiet environment.

The oscillation continues. In fact, you can set up a simple spring-mass in a perfectly quiet environment — no disturbances — and it oscillates indefinitely (in theory) after a single initial displacement. The oscillation isn't driven by external noise. It's intrinsic.

The failure reveals: oscillation doesn't require external forcing. It arises from the system's own dynamics — specifically from the interplay between energy storage and energy release.

### Attempt 2: Oscillation is caused by the feedback loop's delay

The controller reads the current value, computes an error, and applies a correction — but by the time the correction arrives, the system has already moved. The correction is always responding to where the system *was*, not where it is. This lag causes overshoot, which triggers the next correction in the opposite direction.

This is real and important — delay definitely destabilizes feedback systems. But it's only part of the story. A spring-mass system with no feedback at all oscillates. A perfectly responsive (zero-delay) feedback controller can still produce oscillation if the gain is too high. Delay makes oscillation worse, but isn't the only cause.

The failure reveals: oscillation in systems with energy storage doesn't require delay. The energy itself is the source. Delay is an amplifying factor, not the root cause.

### Attempt 3: Oscillation is caused by excessive gain

Turn down the control gain and oscillation stops. Turn it up and oscillation starts. Clearly high gain causes oscillation.

This is empirically true but mechanistically incomplete. Why does high gain cause oscillation? Because with high gain, a small error produces a large corrective force. That large force overshoots. Now there's an error in the opposite direction. High gain again produces a large corrective force. The system resonates.

But "just reduce gain" isn't a full answer — it trades oscillation for sluggishness. And it doesn't explain why there's always a specific frequency to the oscillation, or why that frequency depends on mass and spring stiffness, not on gain.

The failure reveals: oscillation frequency is determined by the system's energy storage properties (mass and compliance), not by control gain. Gain determines whether oscillation grows or decays; the frequency is fixed by physics.

## The Discovery

Every system that can store energy in two different forms will exchange energy between them — and this exchange has a natural rhythm. In a spring-mass system: kinetic energy (½mv²) and potential energy (½kx²) trade back and forth. When the mass moves fastest (through equilibrium), potential energy is zero. When the mass is at maximum displacement, kinetic energy is zero. All energy is kinetic, then all potential, then all kinetic — and the cycle repeats.

The rate of this exchange — the natural frequency — is fixed by the ratio of energy storage to energy inertia: **ω_n = √(k/m)**. A stiffer spring (higher k) gives faster exchange. More mass (higher m) gives slower exchange. Neither the amplitude nor the initial conditions change the frequency.

Every mechanical vibration problem, every electrical resonance (inductor-capacitor), every thermal oscillation, every hydraulic instability is the same phenomenon: two forms of energy storage with a natural exchange frequency.

Without dissipation, this exchange continues forever. Real systems have friction, resistance, or thermal loss — **damping** — that bleeds energy out of each cycle. With enough damping, the system returns to rest. Without enough, oscillation is sustained or grows.

This is **simple harmonic motion**: x(t) = A·cos(ω_n·t + φ) in the undamped case. In a damped system: x(t) = A·e^(−ζω_n·t)·cos(ω_d·t + φ), where ζ is the damping ratio and ω_d = ω_n·√(1−ζ²) is the damped frequency.

## Try It

<iframe src="../assets/browser/chapter17/index.html" width="100%" height="460" style="border:1px solid var(--md-default-fg-color--lightest);border-radius:8px;"></iframe>

[open in a new tab](../assets/browser/chapter17/index.html)

Before changing anything, predict:

- If you double the spring stiffness, what happens to the oscillation frequency?
- If you double the mass, what happens to the frequency? To the amplitude over time?
- What value of damping makes the system return to rest in the minimum time without crossing zero?

## Implementation

`browser/common/engine.js` provides `Body` and `Vec`. The oscillator ODE is inline in `browser/chapter17/index.html`'s `stepMass(mass, c)` function: `spring = -k * disp`, `damp = -c * mass.vel.x`, then `mass.addForce(new Vec(spring + damp, 0))` and `mass.step(0.016)`. The slider variables `k`, `cUnder`, and `cOver` map to spring stiffness and damping coefficients, run side-by-side to show underdamped oscillation vs overdamped creep.

## When It Breaks

**Resonance amplification.** Every mechanical structure has natural frequencies. If a periodic driving force (a motor, a vibration source, a rotating imbalance) happens to operate at the structure's natural frequency, even a tiny input is amplified into a large oscillation. The Tacoma Narrows Bridge (1940) collapsed because wind vortex shedding frequency matched the bridge's torsional natural frequency. Robot motors spinning near a robot frame's structural mode frequency cause the same phenomenon, just at smaller scale.

**Nonlinear stiffness changing resonant frequency.** The analysis assumes a linear spring (k constant). Real springs — rubber mounts, flexible robot joints, cable tension — have stiffness that varies with displacement. As amplitude changes, natural frequency shifts. This is why nonlinear systems can exhibit chaotic oscillation: the resonance frequency is amplitude-dependent and the system can be driven into progressively more complex behavior.

## Transfer

- **LC circuits**: an inductor stores energy in a magnetic field; a capacitor stores energy in an electric field. Connected together, energy oscillates between them at ω = 1/√(LC) — electrical resonance. Radio receivers use this to select specific frequencies.
- **Quartz crystal oscillators**: a quartz crystal's mechanical resonant frequency (from piezoelectricity) is used as the frequency reference in all electronic clocks and microprocessors. The crystal's quality factor Q is so high that it oscillates with extraordinary precision — a few parts per million per year.
- **Earthquake-isolated buildings**: the building sits on damped spring isolators tuned so the building's natural frequency is below the typical earthquake frequency band. The building moves with the ground at a different rate, reducing structural stress.

Exercises:

1. A pendulum has length L = 0.5 m. What is its natural frequency? What length gives exactly 1 Hz?
2. A robot joint has effective stiffness k = 500 N/m and effective mass m = 0.2 kg. What is its natural frequency? If the control loop samples at 100 Hz, is this mode within the controller's bandwidth?
3. A damped oscillator has ω_n = 10 rad/s and ζ = 0.1. Calculate the damped frequency ω_d. How many oscillation cycles does it take for the amplitude to drop to 50% of its initial value?

---

**Continue → [Why Feedback Changes Everything](18-why-feedback-changes-everything.md)**
