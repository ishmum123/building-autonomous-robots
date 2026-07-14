# Why Sensor Fusion Works

## The Problem

No single sensor is perfect. How can several imperfect sensors become more trustworthy?

## Thinking

Before we name anything, ask yourself:

- What would happen if the missing piece were absent?
- What is the simplest system that could show this effect?
- Can you draw the interaction before reading the answer?

## Discovery

Combining sensors with different strengths reduces overall uncertainty.

## Implementation

We build a minimal `sensor fusion` model in Python.

Source: [`python/chapter24/main.py`](https://github.com/ishmum123/building-autonomous-robots/blob/main/python/chapter24/main.py)  ·  [view in browser](assets/simulations/chapter24/sim.py)

Run the implementation:

```bash
python python/chapter24/main.py
```

## Simulation

Source: [`simulations/chapter24/sim.py`](https://github.com/ishmum123/building-autonomous-robots/blob/main/simulations/chapter24/sim.py)  ·  [view in browser](assets/simulations/chapter24/sim.py)

Run the chapter simulation:

```bash
python simulations/chapter24/sim.py
```

A browser version is available at [`browser/chapter24/index.html`](https://github.com/ishmum123/building-autonomous-robots/blob/main/browser/chapter24/index.html)  ·  [run live](assets/browser/chapter24/index.html).

## Exercises

1. Change one parameter in the simulation and predict what will happen.
2. Draw the system before and after the discovery.
3. Name one real-world device that depends on this idea and one way it can fail.

## Engineering Notes

Real systems add noise, latency, and power limits. The model we built is the simplest version; real `sensor fusion` designs trade accuracy, cost, and reliability.

---

**Continue → [Why Kalman Filters Exist](25-why-kalman-filters-exist.md)**
