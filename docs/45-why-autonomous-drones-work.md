# Why Autonomous Drones Work

## The Problem

How do sensing, planning, control, and state estimation come together to fly by themselves?

## Thinking

Before we name anything, ask yourself:

- What would happen if the missing piece were absent?
- What is the simplest system that could show this effect?
- Can you draw the interaction before reading the answer?

## Discovery

Autonomy is the closed loop of sensing, thinking, and acting.

## Implementation

We build a minimal `full autonomy stack` model in Python.

Source: [`python/chapter45/main.py`](https://github.com/ishmum123/building-autonomous-robots/blob/main/python/chapter45/main.py)  ·  [view in browser](assets/simulations/chapter45/sim.py)

Run the implementation:

```bash
python python/chapter45/main.py
```

## Simulation

Source: [`simulations/chapter45/sim.py`](https://github.com/ishmum123/building-autonomous-robots/blob/main/simulations/chapter45/sim.py)  ·  [view in browser](assets/simulations/chapter45/sim.py)

Run the chapter simulation:

```bash
python simulations/chapter45/sim.py
```

A browser version is available at [`browser/chapter45/index.html`](https://github.com/ishmum123/building-autonomous-robots/blob/main/browser/chapter45/index.html)  ·  [run live](assets/browser/chapter45/index.html).

## Exercises

1. Change one parameter in the simulation and predict what will happen.
2. Draw the system before and after the discovery.
3. Name one real-world device that depends on this idea and one way it can fail.

## Engineering Notes

Real systems add noise, latency, and power limits. The model we built is the simplest version; real `full autonomy stack` designs trade accuracy, cost, and reliability.

---

**Continue → the next discovery**
