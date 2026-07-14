# Why Accelerometers Lie

## The Problem

An accelerometer reads gravity even when sitting still. How can the same sensor be wrong and right?

## Thinking

Before we name anything, ask yourself:

- What would happen if the missing piece were absent?
- What is the simplest system that could show this effect?
- Can you draw the interaction before reading the answer?

## Discovery

Accelerometers measure specific force, not pure acceleration.

## Implementation

We build a minimal `accelerometer` model in Python.

Run the implementation:

```bash
python python/chapter20/main.py
```

## Simulation

Run the chapter simulation:

```bash
python simulations/chapter20/sim.py
```

A browser version is available at `browser/chapter20/index.html`.

## Exercises

1. Change one parameter in the simulation and predict what will happen.
2. Draw the system before and after the discovery.
3. Name one real-world device that depends on this idea and one way it can fail.

## Engineering Notes

Real systems add noise, latency, and power limits. The model we built is the simplest version; real `accelerometer` designs trade accuracy, cost, and reliability.

---

**Continue → [Why Gyroscopes Drift](21-why-gyroscopes-drift.md)**
