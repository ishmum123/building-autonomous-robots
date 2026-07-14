# Why Planning Is Hard

## The Problem

There are infinite paths from here to there. How do you choose a safe one?

## Thinking

Before we name anything, ask yourself:

- What would happen if the missing piece were absent?
- What is the simplest system that could show this effect?
- Can you draw the interaction before reading the answer?

## Discovery

Planning searches a high-dimensional space of possible motions.

## Implementation

We will build a minimal `motion planning` model in Python.

Open `python/chapter36/main.py` and follow the step-by-step construction.

## Simulation

Run the chapter simulation:

```bash
python simulations/chapter36/sim.py
```

A browser version is available at `browser/chapter36/index.html`.

## Exercises

1. Change one parameter in the simulation and predict what will happen.
2. Draw the system before and after the discovery.
3. Name one real-world device that depends on this idea and one way it can fail.

## Engineering Notes

Real systems add noise, latency, and power limits. The model we built is the simplest version; real `motion planning` designs trade accuracy, cost, and reliability.

---

**Continue → [Why A* Works](37-why-astar-works.md)**
