# Why Decisions Need Models

## The Problem

You can react to the present, but the best action depends on the future. How?

## Thinking

Before we name anything, ask yourself:

- What would happen if the missing piece were absent?
- What is the simplest system that could show this effect?
- Can you draw the interaction before reading the answer?

## Discovery

A model lets the robot predict outcomes and choose the best sequence.

## Implementation

We will build a minimal `model predictive control` model in Python.

Open `python/chapter44/main.py` and follow the step-by-step construction.

## Simulation

Run the chapter simulation:

```bash
python simulations/chapter44/sim.py
```

A browser version is available at `browser/chapter44/index.html`.

## Exercises

1. Change one parameter in the simulation and predict what will happen.
2. Draw the system before and after the discovery.
3. Name one real-world device that depends on this idea and one way it can fail.

## Engineering Notes

Real systems add noise, latency, and power limits. The model we built is the simplest version; real `model predictive control` designs trade accuracy, cost, and reliability.

---

**Continue → [Why Autonomous Drones Work](45-why-autonomous-drones-work.md)**
