# Why PID Was Invented

## The Problem

You're controlling the temperature of an industrial oven that must hold exactly 200°C to cure composite panels for aircraft wings. Too cold: the resin doesn't cure fully, panels fail structural tests, the batch is scrapped. Too hot: the resin burns, same outcome. The cost per batch: $40,000.

You have a heater you can throttle from 0–100% and a thermocouple reading temperature every 100 ms. You already know feedback control (Chapter 13): measure the error, drive the heater proportional to how far you are from 200°C. That should work. Except:

Monday: oven warms up nicely but stabilizes at 193°C. Seven degrees short — the resin undercures.
Tuesday: you raise the proportional gain. The oven overshoots to 218°C, then rings back and forth for 20 minutes before settling. One panel burns.
Wednesday: a technician opens the oven door briefly. A cold draft drops temperature to 170°C. The controller slams heater to 100% and overshoots again.

Any viable temperature controller must:

- Eliminate the persistent offset that proportional-only control leaves
- Respond fast to sudden disturbances without triggering large oscillations
- Damp out oscillations quickly once they start
- Work across the full operating range, not just at one setpoint

## What Would You Try?

- Proportional control leaves a steady-state offset. If you can't increase gain without oscillating, what else could drive the error to zero over time?
- The oven overshoots after a disturbance. What information about the *rate of change* of temperature would tell you a correction was about to go too far?
- Before you read the answer: if you had to combine three separate correction signals — one for the current error, one for the accumulated past error, one for the rate of change — what would each contribute, and could they interfere with each other?

## Failed Attempts

### Attempt 1: Proportional control with high gain

The obvious fix for steady-state offset is to turn up the gain. If K_p is large enough, even a tiny error produces a large correction — surely that drives the oven to exactly 200°C?

It does reduce the offset. At K_p = 2, the oven holds at 193°C (7°C error). At K_p = 5, it holds at 198°C (2°C error). Good trend. At K_p = 10, it holds at 199°C but now overshoots to 212°C on startup before settling. At K_p = 20, the system oscillates continuously — every time heater fires hard it overshoots, then heater cuts off completely, temperature drops, heater fires hard again. The oven never settles.

The fundamental reason: proportional control alone always has a non-zero steady-state error (the error is what's *driving* the correction — when error goes to zero, the heater turns off, and with any heat loss the oven cools again). Increasing gain trades smaller steady-state error for reduced stability margin. You can't have both without adding something else.

### Attempt 2: Integral control alone

If steady-state error is the problem, accumulate it. Keep a running sum of all past errors. Drive the heater with that sum. When the oven is 7°C too cold for 10 seconds, the accumulated error is 70°C·s — a large, growing signal that will push the heater harder until temperature reaches setpoint.

This works — eventually. But watch what happens at startup: the oven starts cold, the integral accumulates thousands of degree-seconds of error over several minutes, and by the time temperature reaches 200°C the integral term is enormous. The heater stays at 100% long after the target is reached. The oven shoots to 230°C before the integral starts to unwind. Unwinding takes just as long as it took to accumulate — another few minutes of overshoot. This is integral windup, and it's severe.

Integral-only control is also inherently slow by design: it responds to accumulated past error, not present error. For a sudden disturbance — door opens — the response is sluggish because there's no direct reaction to the current gap.

### Attempt 3: Derivative control alone

Instead of reacting to the error, react to how fast the error is changing. If temperature is dropping rapidly — rate = −3°C/s — increase heater now, before the error gets large. If temperature is rising rapidly toward setpoint, back off early so you don't overshoot.

Derivative control is the best predictor: it knows where the error is *heading*. But derivative of what? The error signal from a thermocouple contains measurement noise — small, rapid fluctuations of ±0.5°C. The derivative of noise is enormous. A thermocouple noise spike of 1°C over one 100 ms sample = 10°C/s apparent rate. The derivative term reacts to this as if the oven were heating at 10°C/s and cuts heater output drastically. The controller "sees" false disturbances that don't exist and fights them. A system running derivative-only control on a noisy sensor thrashes its actuator and never stabilizes.

Worse: derivative control has zero steady-state gain. When the error is constant (even a large constant offset), the derivative is zero, so the derivative term contributes nothing. It cannot eliminate steady-state error at all.

## The Discovery

Each attempt failed in a distinct way, and the failures are complementary:

- Proportional responds to *present* error — fast and direct, but leaves a steady-state residual and can oscillate at high gain.
- Integral responds to *past accumulated* error — eliminates offset, but slow, overshoots on startup, and winds up during saturation.
- Derivative responds to *future trend* (rate of change) — predicts and damps overshoot, but amplifies noise and contributes nothing at steady state.

No single term is complete. But the failures don't overlap — each term plugs the hole the others leave. The residual offset that proportional leaves is exactly what integral is designed to eliminate. The overshoot that integral causes is exactly what derivative is designed to predict and damp. The noise that derivative amplifies can be filtered without destroying its predictive benefit.

Combine all three and each compensates for the others' weakness:

**u(t) = K_p · e(t) + K_i · ∫e(τ)dτ + K_d · de/dt**

The controller output u(t) is the heater throttle. K_p scales the present error, K_i scales the accumulated history, K_d scales the rate of change. Tune the three gains to balance response speed, steady-state accuracy, and noise sensitivity.

This is the **PID controller** — Proportional-Integral-Derivative. Invented in the 1910s for ship steering, formalized for industrial use in 1942. Still the most widely deployed control algorithm in the world: an estimated 90% of industrial control loops run PID. Not because it's theoretically optimal but because its three terms map directly onto three physically intuitive failure modes — and fixing all three at once works.

## Try It

<iframe src="../assets/browser/chapter16/index.html" width="100%" height="460" style="border:1px solid var(--md-default-fg-color--lightest);border-radius:8px;"></iframe>

[open in a new tab](../assets/browser/chapter16/index.html)

Before changing anything, predict:

- With only the P term active (I and D at zero), can the oven ever reach exactly 200°C? What does the steady-state error depend on?
- Add the I term. On startup, does the oven overshoot 200°C? Why does the overshoot happen even though the target was reached?
- Add the D term. Does the overshoot reduce? What happens to the noise on the heater output signal?

## Implementation

`browser/common/engine.js` implements the PID update as three parallel running calculations: proportional (current error), integral (Euler-accumulated error sum, clamped to prevent windup), and derivative (backward difference of error, optionally low-pass filtered). `browser/chapter16/index.html` lets you enable each term independently and inject step disturbances to observe how each contributes to the response.

## When It Breaks

**Integral windup.** When the heater is saturated at 100% (during startup or after a large disturbance), the plant cannot respond to the integral term — but the integral keeps accumulating. When the oven finally reaches setpoint, the integral has grown so large that it takes minutes to discharge, causing a long overshoot. Real implementations clamp the integral when the actuator saturates. Many deployed PID systems skip this fix and suffer periodic large overshoots.

**Derivative noise amplification.** The D term differentiates the error signal. Sensor noise that looks like ±0.5°C at 10 Hz becomes ±50°C/s in derivative form — large enough to dominate the control output and cause actuator chatter. Real implementations either filter the derivative term (introducing phase lag that reduces stability) or apply the derivative to the measured output only (not to the setpoint step), trading noise immunity for slightly slower setpoint tracking.

## Transfer

- **Cruise control**: automotive ECUs use PID to hold speed on hills — proportional for immediate response, integral to eliminate offset (which pure throttle-position control would leave), derivative to anticipate grade changes.
- **Industrial chemical reactors**: reactor temperature control is a classic PID application where integral windup during catalyst addition events has caused runaway reactions — the real cost of skipping anti-windup logic.
- **Insulin pumps**: closed-loop insulin delivery (artificial pancreas) uses PID-like control to regulate blood glucose; the derivative term predicts glucose trend from CGM data to prevent overshoot hypoglycemia.

Exercises:

1. A PID controller has K_p = 3, K_i = 0.5, K_d = 0.8. The error over three consecutive 100 ms steps is: 10°C, 7°C, 4°C. Compute the control output at step 3 (assume integral sum = 10 + 7 = 17 before this step).
2. Integral windup occurs when the actuator saturates. Describe an anti-windup scheme and explain why it prevents the overshoot without affecting normal operation.
3. You are tuning a PID controller manually using the Ziegler-Nichols step response method. Describe the procedure and what physical measurements it requires.

---

**Continue → [Why One PID Isn't Enough](17-why-one-pid-isnt-enough.md)**
