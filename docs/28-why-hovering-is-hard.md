# Why Hovering Is Hard

## The Problem

A quadcopter must fight gravity exactly. Why does it sink or climb?

## Thinking

Before we name anything, ask yourself:

- What would happen if the missing piece were absent?
- What is the simplest system that could show this effect?
- Can you draw the interaction before reading the answer?

## Discovery

Hover requires balancing thrust against weight in real time.

## Implementation

We will build a minimal `altitude control` model in Python.

Open `python/chapter28/main.py` and follow the step-by-step construction.

## Simulation

Run the chapter simulation:

```bash
python simulations/chapter28/sim.py
```

A browser version is available at `browser/chapter28/index.html`.

## Exercises

1. Change one parameter in the simulation and predict what will happen.
2. Draw the system before and after the discovery.
3. Name one real-world device that depends on this idea and one way it can fail.

## Engineering Notes

Real systems add noise, latency, and power limits. The model we built is the simplest version; real `altitude control` designs trade accuracy, cost, and reliability.

---

**Continue → Why Wind Wins**
