# Why One PID Isn't Enough

## The Problem

A drone can hold altitude but drifts horizontally. Why does one controller fail to govern everything?

## Thinking

Before we name anything, ask yourself:

- What would happen if the missing piece were absent?
- What is the simplest system that could show this effect?
- Can you draw the interaction before reading the answer?

## Discovery

Nested controllers handle different time scales and variables.

## Implementation

We build a minimal `cascade control` model in Python.

Source: [`python/chapter17/main.py`](https://github.com/ishmum123/building-autonomous-robots/blob/main/python/chapter17/main.py)  ·  [view in browser](assets/simulations/chapter17/sim.py)

Run the implementation:

```bash
python python/chapter17/main.py
```

## Simulation

Source: [`simulations/chapter17/sim.py`](https://github.com/ishmum123/building-autonomous-robots/blob/main/simulations/chapter17/sim.py)  ·  [view in browser](assets/simulations/chapter17/sim.py)

Run the chapter simulation:

```bash
python simulations/chapter17/sim.py
```

A browser version is available at [`browser/chapter17/index.html`](https://github.com/ishmum123/building-autonomous-robots/blob/main/browser/chapter17/index.html)  ·  [run live](assets/browser/chapter17/index.html).

## Exercises

1. Change one parameter in the simulation and predict what will happen.
2. Draw the system before and after the discovery.
3. Name one real-world device that depends on this idea and one way it can fail.

## Engineering Notes

Real systems add noise, latency, and power limits. The model we built is the simplest version; real `cascade control` designs trade accuracy, cost, and reliability.

---

**Continue → [Why Quadcopters Need Two Brains](18-why-quadcopters-need-two-brains.md)**
