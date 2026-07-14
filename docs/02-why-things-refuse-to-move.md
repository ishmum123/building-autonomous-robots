# Why Things Refuse to Move

## The Problem

You push a heavy crate. It does not budge. Why does the world resist changes in motion?

## Thinking

Before we name anything, ask yourself:

- What would happen if the missing piece were absent?
- What is the simplest system that could show this effect?
- Can you draw the interaction before reading the answer?

## Discovery

Objects resist changes in velocity. This property is called inertia.

## Implementation

We build a minimal `inertia` model in Python.

Source: [`python/chapter02/main.py`](https://github.com/ishmum123/building-autonomous-robots/blob/main/python/chapter02/main.py)  ·  [view in browser](assets/simulations/chapter02/sim.py)

Run the implementation:

```bash
python python/chapter02/main.py
```

## Simulation

Source: [`simulations/chapter02/sim.py`](https://github.com/ishmum123/building-autonomous-robots/blob/main/simulations/chapter02/sim.py)  ·  [view in browser](assets/simulations/chapter02/sim.py)

Run the chapter simulation:

```bash
python simulations/chapter02/sim.py
```

A browser version is available at [`browser/chapter02/index.html`](https://github.com/ishmum123/building-autonomous-robots/blob/main/browser/chapter02/index.html)  ·  [run live](assets/browser/chapter02/index.html).

## Exercises

1. Change one parameter in the simulation and predict what will happen.
2. Draw the system before and after the discovery.
3. Name one real-world device that depends on this idea and one way it can fail.

## Engineering Notes

Real systems add noise, latency, and power limits. The model we built is the simplest version; real `inertia` designs trade accuracy, cost, and reliability.

---

**Continue → [Why Magnets Pull](03-why-magnets-pull.md)**
