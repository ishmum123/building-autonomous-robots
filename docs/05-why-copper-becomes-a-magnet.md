# Why Copper Becomes a Magnet

## The Problem

A plain piece of copper does not attract iron, but wrap it with current and it does. Why?

## Thinking

Before we name anything, ask yourself:

- What would happen if the missing piece were absent?
- What is the simplest system that could show this effect?
- Can you draw the interaction before reading the answer?

## Discovery

Electric current creates a magnetic field.

## Implementation

We build a minimal `electromagnet` model in Python.

Source: [`python/chapter05/main.py`](https://github.com/ishmum123/building-autonomous-robots/blob/main/python/chapter05/main.py)  ·  [view in browser](assets/simulations/chapter05/sim.py)

Run the implementation:

```bash
python python/chapter05/main.py
```

## Simulation

Source: [`simulations/chapter05/sim.py`](https://github.com/ishmum123/building-autonomous-robots/blob/main/simulations/chapter05/sim.py)  ·  [view in browser](assets/simulations/chapter05/sim.py)

Run the chapter simulation:

```bash
python simulations/chapter05/sim.py
```

A browser version is available at [`browser/chapter05/index.html`](https://github.com/ishmum123/building-autonomous-robots/blob/main/browser/chapter05/index.html)  ·  [run live](assets/browser/chapter05/index.html).

## Exercises

1. Change one parameter in the simulation and predict what will happen.
2. Draw the system before and after the discovery.
3. Name one real-world device that depends on this idea and one way it can fail.

## Engineering Notes

Real systems add noise, latency, and power limits. The model we built is the simplest version; real `electromagnet` designs trade accuracy, cost, and reliability.

---

**Continue → [Why Motors Spin](06-why-motors-spin.md)**
