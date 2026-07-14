# Why Quadcopters Flip

## The Problem

If one motor spins faster, the drone tilts or flips. Why?

## Thinking

Before we name anything, ask yourself:

- What would happen if the missing piece were absent?
- What is the simplest system that could show this effect?
- Can you draw the interaction before reading the answer?

## Discovery

Differential thrust creates torques that change attitude.

## Implementation

We build a minimal `torque imbalance` model in Python.

Source: [`python/chapter27/main.py`](https://github.com/ishmum123/building-autonomous-robots/blob/main/python/chapter27/main.py)  ·  [view in browser](assets/simulations/chapter27/sim.py)

Run the implementation:

```bash
python python/chapter27/main.py
```

## Simulation

Source: [`simulations/chapter27/sim.py`](https://github.com/ishmum123/building-autonomous-robots/blob/main/simulations/chapter27/sim.py)  ·  [view in browser](assets/simulations/chapter27/sim.py)

Run the chapter simulation:

```bash
python simulations/chapter27/sim.py
```

A browser version is available at [`browser/chapter27/index.html`](https://github.com/ishmum123/building-autonomous-robots/blob/main/browser/chapter27/index.html)  ·  [run live](assets/browser/chapter27/index.html).

## Exercises

1. Change one parameter in the simulation and predict what will happen.
2. Draw the system before and after the discovery.
3. Name one real-world device that depends on this idea and one way it can fail.

## Engineering Notes

Real systems add noise, latency, and power limits. The model we built is the simplest version; real `torque imbalance` designs trade accuracy, cost, and reliability.

---

**Continue → [Why Hovering Is Hard](28-why-hovering-is-hard.md)**
