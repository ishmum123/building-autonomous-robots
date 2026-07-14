# Why Feedback Changes Everything

## The Problem

You close your eyes while walking and drift. How does measuring where you are change what you can do?

## Thinking

Before we name anything, ask yourself:

- What would happen if the missing piece were absent?
- What is the simplest system that could show this effect?
- Can you draw the interaction before reading the answer?

## Discovery

Feedback compares goal to reality and corrects the difference.

## Implementation

We build a minimal `feedback loop` model in Python.

Source: [`python/chapter13/main.py`](https://github.com/ishmum123/building-autonomous-robots/blob/main/python/chapter13/main.py)  ·  [view in browser](assets/simulations/chapter13/sim.py)

Run the implementation:

```bash
python python/chapter13/main.py
```

## Simulation

Source: [`simulations/chapter13/sim.py`](https://github.com/ishmum123/building-autonomous-robots/blob/main/simulations/chapter13/sim.py)  ·  [view in browser](assets/simulations/chapter13/sim.py)

Run the chapter simulation:

```bash
python simulations/chapter13/sim.py
```

A browser version is available at [`browser/chapter13/index.html`](https://github.com/ishmum123/building-autonomous-robots/blob/main/browser/chapter13/index.html)  ·  [run live](assets/browser/chapter13/index.html).

## Exercises

1. Change one parameter in the simulation and predict what will happen.
2. Draw the system before and after the discovery.
3. Name one real-world device that depends on this idea and one way it can fail.

## Engineering Notes

Real systems add noise, latency, and power limits. The model we built is the simplest version; real `feedback loop` designs trade accuracy, cost, and reliability.

---

**Continue → [Why Guessing Isn't Control](14-why-guessing-isnt-control.md)**
