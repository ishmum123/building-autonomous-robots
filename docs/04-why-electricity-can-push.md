# Why Electricity Can Push

## The Problem

A wire jumps when current flows near a magnet. How can invisible electrons create motion?

## Thinking

Before we name anything, ask yourself:

- What would happen if the missing piece were absent?
- What is the simplest system that could show this effect?
- Can you draw the interaction before reading the answer?

## Discovery

A current in a magnetic field experiences a mechanical force.

## Implementation

We build a minimal `electromagnetic force` model in Python.

Source: [`python/chapter04/main.py`](https://github.com/ishmum123/building-autonomous-robots/blob/main/python/chapter04/main.py)  ·  [view in browser](assets/simulations/chapter04/sim.py)

Run the implementation:

```bash
python python/chapter04/main.py
```

## Simulation

Source: [`simulations/chapter04/sim.py`](https://github.com/ishmum123/building-autonomous-robots/blob/main/simulations/chapter04/sim.py)  ·  [view in browser](assets/simulations/chapter04/sim.py)

Run the chapter simulation:

```bash
python simulations/chapter04/sim.py
```

A browser version is available at [`browser/chapter04/index.html`](https://github.com/ishmum123/building-autonomous-robots/blob/main/browser/chapter04/index.html)  ·  [run live](assets/browser/chapter04/index.html).

## Exercises

1. Change one parameter in the simulation and predict what will happen.
2. Draw the system before and after the discovery.
3. Name one real-world device that depends on this idea and one way it can fail.

## Engineering Notes

Real systems add noise, latency, and power limits. The model we built is the simplest version; real `electromagnetic force` designs trade accuracy, cost, and reliability.

---

**Continue → [Why Copper Becomes a Magnet](05-why-copper-becomes-a-magnet.md)**
