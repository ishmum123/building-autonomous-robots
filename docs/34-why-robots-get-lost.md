# Why Robots Get Lost

## The Problem

A corridor looks the same in two places. How does a robot know which place it is?

## Thinking

Before we name anything, ask yourself:

- What would happen if the missing piece were absent?
- What is the simplest system that could show this effect?
- Can you draw the interaction before reading the answer?

## Discovery

Ambiguity arises when different places look identical.

## Implementation

We will build a minimal `localization ambiguity` model in Python.

Open `python/chapter34/main.py` and follow the step-by-step construction.

## Simulation

Run the chapter simulation:

```bash
python simulations/chapter34/sim.py
```

A browser version is available at `browser/chapter34/index.html`.

## Exercises

1. Change one parameter in the simulation and predict what will happen.
2. Draw the system before and after the discovery.
3. Name one real-world device that depends on this idea and one way it can fail.

## Engineering Notes

Real systems add noise, latency, and power limits. The model we built is the simplest version; real `localization ambiguity` designs trade accuracy, cost, and reliability.

---

**Continue → Why SLAM Exists**
