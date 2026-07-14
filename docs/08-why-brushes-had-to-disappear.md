# Why Brushes Had to Disappear

## The Problem

Brushes spark, wear out, and limit speed. How can we eliminate them?

## Thinking

Before we name anything, ask yourself:

- What would happen if the missing piece were absent?
- What is the simplest system that could show this effect?
- Can you draw the interaction before reading the answer?

## Discovery

Electronic switching can replace mechanical brushes.

## Implementation

We build a minimal `brushless motor` model in Python.

Run the implementation:

```bash
python python/chapter08/main.py
```

## Simulation

Run the chapter simulation:

```bash
python simulations/chapter08/sim.py
```

A browser version is available at `browser/chapter08/index.html`.

## Exercises

1. Change one parameter in the simulation and predict what will happen.
2. Draw the system before and after the discovery.
3. Name one real-world device that depends on this idea and one way it can fail.

## Engineering Notes

Real systems add noise, latency, and power limits. The model we built is the simplest version; real `brushless motor` designs trade accuracy, cost, and reliability.

---

**Continue → [Why Three Wires Are Better Than Two](09-why-three-wires-are-better-than-two.md)**
