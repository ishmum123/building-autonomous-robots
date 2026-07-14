# Why A* Works

## The Problem

You could explore every path, but that is too slow. How do you search smartly?

## Thinking

Before we name anything, ask yourself:

- What would happen if the missing piece were absent?
- What is the simplest system that could show this effect?
- Can you draw the interaction before reading the answer?

## Discovery

A* uses a heuristic to focus search toward the goal.

## Implementation

We build a minimal `A* search` model in Python.

Source: [`python/chapter37/main.py`](https://github.com/ishmum123/building-autonomous-robots/blob/main/python/chapter37/main.py)  ·  [view in browser](assets/simulations/chapter37/sim.py)

Run the implementation:

```bash
python python/chapter37/main.py
```

## Simulation

Source: [`simulations/chapter37/sim.py`](https://github.com/ishmum123/building-autonomous-robots/blob/main/simulations/chapter37/sim.py)  ·  [view in browser](assets/simulations/chapter37/sim.py)

Run the chapter simulation:

```bash
python simulations/chapter37/sim.py
```

A browser version is available at [`browser/chapter37/index.html`](https://github.com/ishmum123/building-autonomous-robots/blob/main/browser/chapter37/index.html)  ·  [run live](assets/browser/chapter37/index.html).

## Exercises

1. Change one parameter in the simulation and predict what will happen.
2. Draw the system before and after the discovery.
3. Name one real-world device that depends on this idea and one way it can fail.

## Engineering Notes

Real systems add noise, latency, and power limits. The model we built is the simplest version; real `A* search` designs trade accuracy, cost, and reliability.

---

**Continue → [Why Robots Change Their Mind](38-why-robots-change-their-mind.md)**
