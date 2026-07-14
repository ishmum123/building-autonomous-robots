# Why Robots Need Goals

## The Problem

A robot can move, but without a goal any motion is as good as another. Why do goals matter?

## Thinking

Before we name anything, ask yourself:

- What would happen if the missing piece were absent?
- What is the simplest system that could show this effect?
- Can you draw the interaction before reading the answer?

## Discovery

Goals translate intent into a measure of success.

## Implementation

We will build a minimal `objective function` model in Python.

Open `python/chapter40/main.py` and follow the step-by-step construction.

## Simulation

Run the chapter simulation:

```bash
python simulations/chapter40/sim.py
```

A browser version is available at `browser/chapter40/index.html`.

## Exercises

1. Change one parameter in the simulation and predict what will happen.
2. Draw the system before and after the discovery.
3. Name one real-world device that depends on this idea and one way it can fail.

## Engineering Notes

Real systems add noise, latency, and power limits. The model we built is the simplest version; real `objective function` designs trade accuracy, cost, and reliability.

---

**Continue → Why Obstacles Change Everything**
