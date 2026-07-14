# Why Four Motors Beat One

## The Problem

One propeller can lift but also spins the body. How do four motors solve this?

## Thinking

Before we name anything, ask yourself:

- What would happen if the missing piece were absent?
- What is the simplest system that could show this effect?
- Can you draw the interaction before reading the answer?

## Discovery

Four motors provide lift and counter-torque simultaneously.

## Implementation

We build a minimal `quadcopter actuation` model in Python.

Source: [`python/chapter26/main.py`](https://github.com/ishmum123/building-autonomous-robots/blob/main/python/chapter26/main.py)  ·  [view in browser](assets/simulations/chapter26/sim.py)

Run the implementation:

```bash
python python/chapter26/main.py
```

## Simulation

Source: [`simulations/chapter26/sim.py`](https://github.com/ishmum123/building-autonomous-robots/blob/main/simulations/chapter26/sim.py)  ·  [view in browser](assets/simulations/chapter26/sim.py)

Run the chapter simulation:

```bash
python simulations/chapter26/sim.py
```

A browser version is available at [`browser/chapter26/index.html`](https://github.com/ishmum123/building-autonomous-robots/blob/main/browser/chapter26/index.html)  ·  [run live](assets/browser/chapter26/index.html).

## Exercises

1. Change one parameter in the simulation and predict what will happen.
2. Draw the system before and after the discovery.
3. Name one real-world device that depends on this idea and one way it can fail.

## Engineering Notes

Real systems add noise, latency, and power limits. The model we built is the simplest version; real `quadcopter actuation` designs trade accuracy, cost, and reliability.

---

**Continue → [Why Quadcopters Flip](27-why-quadcopters-flip.md)**
