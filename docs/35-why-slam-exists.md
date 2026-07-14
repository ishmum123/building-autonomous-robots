# Why SLAM Exists

## The Problem

You need a map to localize, but you need to localize to build a map. How do you do both?

## Thinking

Before we name anything, ask yourself:

- What would happen if the missing piece were absent?
- What is the simplest system that could show this effect?
- Can you draw the interaction before reading the answer?

## Discovery

SLAM solves mapping and localization jointly.

## Implementation

We build a minimal `SLAM` model in Python.

Source: [`python/chapter35/main.py`](https://github.com/ishmum123/building-autonomous-robots/blob/main/python/chapter35/main.py)  ·  [view in browser](assets/simulations/chapter35/sim.py)

Run the implementation:

```bash
python python/chapter35/main.py
```

## Simulation

Source: [`simulations/chapter35/sim.py`](https://github.com/ishmum123/building-autonomous-robots/blob/main/simulations/chapter35/sim.py)  ·  [view in browser](assets/simulations/chapter35/sim.py)

Run the chapter simulation:

```bash
python simulations/chapter35/sim.py
```

A browser version is available at [`browser/chapter35/index.html`](https://github.com/ishmum123/building-autonomous-robots/blob/main/browser/chapter35/index.html)  ·  [run live](assets/browser/chapter35/index.html).

## Exercises

1. Change one parameter in the simulation and predict what will happen.
2. Draw the system before and after the discovery.
3. Name one real-world device that depends on this idea and one way it can fail.

## Engineering Notes

Real systems add noise, latency, and power limits. The model we built is the simplest version; real `SLAM` designs trade accuracy, cost, and reliability.

---

**Continue → [Why Planning Is Hard](36-why-planning-is-hard.md)**
