# Why Three Wires Are Better Than Two

## The Problem

A single wire can only push one direction. How do we create a smooth rotating field?

## Thinking

Before we name anything, ask yourself:

- What would happen if the missing piece were absent?
- What is the simplest system that could show this effect?
- Can you draw the interaction before reading the answer?

## Discovery

Three phased currents create a continuously rotating magnetic field.

## Implementation

We will build a minimal `three-phase field` model in Python.

Open `python/chapter09/main.py` and follow the step-by-step construction.

## Simulation

Run the chapter simulation:

```bash
python simulations/chapter09/sim.py
```

A browser version is available at `browser/chapter09/index.html`.

## Exercises

1. Change one parameter in the simulation and predict what will happen.
2. Draw the system before and after the discovery.
3. Name one real-world device that depends on this idea and one way it can fail.

## Engineering Notes

Real systems add noise, latency, and power limits. The model we built is the simplest version; real `three-phase field` designs trade accuracy, cost, and reliability.

---

**Continue → Why Motors Need Conductors**
