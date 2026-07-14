# Why State Matters

## The Problem

Two robots receive the same sensor reading but should act differently. Why?

## Thinking

Before we name anything, ask yourself:

- What would happen if the missing piece were absent?
- What is the simplest system that could show this effect?
- Can you draw the interaction before reading the answer?

## Discovery

The right action depends on hidden state, not just current input.

## Implementation

We will build a minimal `state representation` model in Python.

Open `python/chapter42/main.py` and follow the step-by-step construction.

## Simulation

Run the chapter simulation:

```bash
python simulations/chapter42/sim.py
```

A browser version is available at `browser/chapter42/index.html`.

## Exercises

1. Change one parameter in the simulation and predict what will happen.
2. Draw the system before and after the discovery.
3. Name one real-world device that depends on this idea and one way it can fail.

## Engineering Notes

Real systems add noise, latency, and power limits. The model we built is the simplest version; real `state representation` designs trade accuracy, cost, and reliability.

---

**Continue → Why Estimation Beats Measurement**
