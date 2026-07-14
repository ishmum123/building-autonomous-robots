# Why Autopilots Exist

## The Problem

A human cannot balance a flying machine hundreds of times per second. What takes over?

## Thinking

Before we name anything, ask yourself:

- What would happen if the missing piece were absent?
- What is the simplest system that could show this effect?
- Can you draw the interaction before reading the answer?

## Discovery

An autopilot handles fast stabilization so the human commands intent.

## Implementation

We will build a minimal `autopilot` model in Python.

Open `python/chapter30/main.py` and follow the step-by-step construction.

## Simulation

Run the chapter simulation:

```bash
python simulations/chapter30/sim.py
```

A browser version is available at `browser/chapter30/index.html`.

## Exercises

1. Change one parameter in the simulation and predict what will happen.
2. Draw the system before and after the discovery.
3. Name one real-world device that depends on this idea and one way it can fail.

## Engineering Notes

Real systems add noise, latency, and power limits. The model we built is the simplest version; real `autopilot` designs trade accuracy, cost, and reliability.

---

**Continue → [Why Drones Crash](31-why-drones-crash.md)**
