# Why Motors Spin

## The Problem

You have a magnet and a coil. How do you turn a brief push into continuous rotation?

## Thinking

Before we name anything, ask yourself:

- What would happen if the missing piece were absent?
- What is the simplest system that could show this effect?
- Can you draw the interaction before reading the answer?

## Discovery

A motor switches current at the right moment to keep turning.

## Implementation

We will build a minimal `motor` model in Python.

Open `python/chapter06/main.py` and follow the step-by-step construction.

## Simulation

Run the chapter simulation:

```bash
python simulations/chapter06/sim.py
```

A browser version is available at `browser/chapter06/index.html`.

## Exercises

1. Change one parameter in the simulation and predict what will happen.
2. Draw the system before and after the discovery.
3. Name one real-world device that depends on this idea and one way it can fail.

## Engineering Notes

Real systems add noise, latency, and power limits. The model we built is the simplest version; real `motor` designs trade accuracy, cost, and reliability.

---

**Continue → Why Motors Stop**
