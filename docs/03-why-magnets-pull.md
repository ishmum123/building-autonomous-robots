# Why Magnets Pull

## The Problem

A magnet and a nail attract each other through empty space. What is happening between them?

## Thinking

Before we name anything, ask yourself:

- What would happen if the missing piece were absent?
- What is the simplest system that could show this effect?
- Can you draw the interaction before reading the answer?

## Discovery

A magnetic field transfers force across a distance.

## Implementation

We build a minimal `magnetic field` model in Python.

Source: [`python/chapter03/main.py`](https://github.com/ishmum123/building-autonomous-robots/blob/main/python/chapter03/main.py)  ·  [view in browser](assets/simulations/chapter03/sim.py)

Run the implementation:

```bash
python python/chapter03/main.py
```

## Simulation

Source: [`simulations/chapter03/sim.py`](https://github.com/ishmum123/building-autonomous-robots/blob/main/simulations/chapter03/sim.py)  ·  [view in browser](assets/simulations/chapter03/sim.py)

Run the chapter simulation:

```bash
python simulations/chapter03/sim.py
```

A browser version is available at [`browser/chapter03/index.html`](https://github.com/ishmum123/building-autonomous-robots/blob/main/browser/chapter03/index.html)  ·  [run live](assets/browser/chapter03/index.html).

## Exercises

1. Change one parameter in the simulation and predict what will happen.
2. Draw the system before and after the discovery.
3. Name one real-world device that depends on this idea and one way it can fail.

## Engineering Notes

Real systems add noise, latency, and power limits. The model we built is the simplest version; real `magnetic field` designs trade accuracy, cost, and reliability.

---

**Continue → [Why Electricity Can Push](04-why-electricity-can-push.md)**
