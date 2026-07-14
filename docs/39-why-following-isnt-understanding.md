# Why Following Isn't Understanding

## The Problem

A robot copies a human's path perfectly but fails in a new room. Why?

## Thinking

Before we name anything, ask yourself:

- What would happen if the missing piece were absent?
- What is the simplest system that could show this effect?
- Can you draw the interaction before reading the answer?

## Discovery

Following trajectories does not generalize to new situations.

## Implementation

We build a minimal `behavior cloning` model in Python.

Source: [`python/chapter39/main.py`](https://github.com/ishmum123/building-autonomous-robots/blob/main/python/chapter39/main.py)  ·  [view in browser](assets/simulations/chapter39/sim.py)

Run the implementation:

```bash
python python/chapter39/main.py
```

## Simulation

Source: [`simulations/chapter39/sim.py`](https://github.com/ishmum123/building-autonomous-robots/blob/main/simulations/chapter39/sim.py)  ·  [view in browser](assets/simulations/chapter39/sim.py)

Run the chapter simulation:

```bash
python simulations/chapter39/sim.py
```

A browser version is available at [`browser/chapter39/index.html`](https://github.com/ishmum123/building-autonomous-robots/blob/main/browser/chapter39/index.html)  ·  [run live](assets/browser/chapter39/index.html).

## Exercises

1. Change one parameter in the simulation and predict what will happen.
2. Draw the system before and after the discovery.
3. Name one real-world device that depends on this idea and one way it can fail.

## Engineering Notes

Real systems add noise, latency, and power limits. The model we built is the simplest version; real `behavior cloning` designs trade accuracy, cost, and reliability.

---

**Continue → [Why Robots Need Goals](40-why-robots-need-goals.md)**
