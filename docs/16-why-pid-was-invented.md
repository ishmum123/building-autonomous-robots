# Why PID Was Invented

## The Problem

Proportional control leaves offset; integral control is slow; derivative control is noisy. How do we combine them?

## Thinking

Before we name anything, ask yourself:

- What would happen if the missing piece were absent?
- What is the simplest system that could show this effect?
- Can you draw the interaction before reading the answer?

## Discovery

PID blends proportional, integral, and derivative responses.

## Implementation

We will build a minimal `PID controller` model in Python.

Open `python/chapter16/main.py` and follow the step-by-step construction.

## Simulation

Run the chapter simulation:

```bash
python simulations/chapter16/sim.py
```

A browser version is available at `browser/chapter16/index.html`.

## Exercises

1. Change one parameter in the simulation and predict what will happen.
2. Draw the system before and after the discovery.
3. Name one real-world device that depends on this idea and one way it can fail.

## Engineering Notes

Real systems add noise, latency, and power limits. The model we built is the simplest version; real `PID controller` designs trade accuracy, cost, and reliability.

---

**Continue → Why One PID Isn't Enough**
