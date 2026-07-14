# Why Robots Change Their Mind

## The Problem

A new obstacle appears after you planned a path. What should the robot do?

## Thinking

Before we name anything, ask yourself:

- What would happen if the missing piece were absent?
- What is the simplest system that could show this effect?
- Can you draw the interaction before reading the answer?

## Discovery

Replanning updates decisions when the world changes.

## Implementation

We will build a minimal `replanning` model in Python.

Open `python/chapter38/main.py` and follow the step-by-step construction.

## Simulation

Run the chapter simulation:

```bash
python simulations/chapter38/sim.py
```

A browser version is available at `browser/chapter38/index.html`.

## Exercises

1. Change one parameter in the simulation and predict what will happen.
2. Draw the system before and after the discovery.
3. Name one real-world device that depends on this idea and one way it can fail.

## Engineering Notes

Real systems add noise, latency, and power limits. The model we built is the simplest version; real `replanning` designs trade accuracy, cost, and reliability.

---

**Continue → Why Following Isn't Understanding**
