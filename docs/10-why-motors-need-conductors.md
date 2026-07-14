# Why Motors Need Conductors

## The Problem

A motor coil must carry current without turning into a heater. What makes a good winding?

## Thinking

Before we name anything, ask yourself:

- What would happen if the missing piece were absent?
- What is the simplest system that could show this effect?
- Can you draw the interaction before reading the answer?

## Discovery

Conductors shape where current flows and therefore where force is produced.

## Implementation

We build a minimal `winding` model in Python.

Source: [`python/chapter10/main.py`](https://github.com/ishmum123/building-autonomous-robots/blob/main/python/chapter10/main.py)  ·  [view in browser](assets/simulations/chapter10/sim.py)

Run the implementation:

```bash
python python/chapter10/main.py
```

## Simulation

Source: [`simulations/chapter10/sim.py`](https://github.com/ishmum123/building-autonomous-robots/blob/main/simulations/chapter10/sim.py)  ·  [view in browser](assets/simulations/chapter10/sim.py)

Run the chapter simulation:

```bash
python simulations/chapter10/sim.py
```

A browser version is available at [`browser/chapter10/index.html`](https://github.com/ishmum123/building-autonomous-robots/blob/main/browser/chapter10/index.html)  ·  [run live](assets/browser/chapter10/index.html).

## Exercises

1. Change one parameter in the simulation and predict what will happen.
2. Draw the system before and after the discovery.
3. Name one real-world device that depends on this idea and one way it can fail.

## Engineering Notes

Real systems add noise, latency, and power limits. The model we built is the simplest version; real `winding` designs trade accuracy, cost, and reliability.

---

**Continue → [Why Faster Isn't Better](11-why-faster-isnt-better.md)**
