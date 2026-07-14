# Why GPS Isn't Enough

## The Problem

GPS tells you where you are, but with delay and uncertainty. Why can't a drone rely only on it?

## Thinking

Before we name anything, ask yourself:

- What would happen if the missing piece were absent?
- What is the simplest system that could show this effect?
- Can you draw the interaction before reading the answer?

## Discovery

Global positioning is low rate and unreliable near obstacles.

## Implementation

We build a minimal `GPS` model in Python.

Source: [`python/chapter22/main.py`](https://github.com/ishmum123/building-autonomous-robots/blob/main/python/chapter22/main.py)  ·  [view in browser](assets/simulations/chapter22/sim.py)

Run the implementation:

```bash
python python/chapter22/main.py
```

## Simulation

Source: [`simulations/chapter22/sim.py`](https://github.com/ishmum123/building-autonomous-robots/blob/main/simulations/chapter22/sim.py)  ·  [view in browser](assets/simulations/chapter22/sim.py)

Run the chapter simulation:

```bash
python simulations/chapter22/sim.py
```

A browser version is available at [`browser/chapter22/index.html`](https://github.com/ishmum123/building-autonomous-robots/blob/main/browser/chapter22/index.html)  ·  [run live](assets/browser/chapter22/index.html).

## Exercises

1. Change one parameter in the simulation and predict what will happen.
2. Draw the system before and after the discovery.
3. Name one real-world device that depends on this idea and one way it can fail.

## Engineering Notes

Real systems add noise, latency, and power limits. The model we built is the simplest version; real `GPS` designs trade accuracy, cost, and reliability.

---

**Continue → [Why Sensors Disagree](23-why-sensors-disagree.md)**
