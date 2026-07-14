# Why Maps Matter

## The Problem

A robot can sense walls but gets lost without remembering them. Why does memory help?

## Thinking

Before we name anything, ask yourself:

- What would happen if the missing piece were absent?
- What is the simplest system that could show this effect?
- Can you draw the interaction before reading the answer?

## Discovery

A map turns raw sensor data into a reusable model of the world.

## Implementation

We will build a minimal `map representation` model in Python.

Open `python/chapter32/main.py` and follow the step-by-step construction.

## Simulation

Run the chapter simulation:

```bash
python simulations/chapter32/sim.py
```

A browser version is available at `browser/chapter32/index.html`.

## Exercises

1. Change one parameter in the simulation and predict what will happen.
2. Draw the system before and after the discovery.
3. Name one real-world device that depends on this idea and one way it can fail.

## Engineering Notes

Real systems add noise, latency, and power limits. The model we built is the simplest version; real `map representation` designs trade accuracy, cost, and reliability.

---

**Continue → [Why Dead Reckoning Fails](33-why-dead-reckoning-fails.md)**
