# Why Obstacles Change Everything

## The Problem

The straight-line path is blocked. How does a goal become a constraint?

## Thinking

Before we name anything, ask yourself:

- What would happen if the missing piece were absent?
- What is the simplest system that could show this effect?
- Can you draw the interaction before reading the answer?

## Discovery

Obstacles turn free space into a constrained decision problem.

## Implementation

We build a minimal `obstacle avoidance` model in Python.

Source: [`python/chapter41/main.py`](https://github.com/ishmum123/building-autonomous-robots/blob/main/python/chapter41/main.py)  ·  [view in browser](assets/simulations/chapter41/sim.py)

Run the implementation:

```bash
python python/chapter41/main.py
```

## Simulation

Source: [`simulations/chapter41/sim.py`](https://github.com/ishmum123/building-autonomous-robots/blob/main/simulations/chapter41/sim.py)  ·  [view in browser](assets/simulations/chapter41/sim.py)

Run the chapter simulation:

```bash
python simulations/chapter41/sim.py
```

A browser version is available at [`browser/chapter41/index.html`](https://github.com/ishmum123/building-autonomous-robots/blob/main/browser/chapter41/index.html)  ·  [run live](assets/browser/chapter41/index.html).

## Exercises

1. Change one parameter in the simulation and predict what will happen.
2. Draw the system before and after the discovery.
3. Name one real-world device that depends on this idea and one way it can fail.

## Engineering Notes

Real systems add noise, latency, and power limits. The model we built is the simplest version; real `obstacle avoidance` designs trade accuracy, cost, and reliability.

---

**Continue → [Why State Matters](42-why-state-matters.md)**
