# Why Everything Oscillates

## The Problem

A spring with a weight bounces forever in theory. Why do systems swing back and forth?

## Thinking

Before we name anything, ask yourself:

- What would happen if the missing piece were absent?
- What is the simplest system that could show this effect?
- Can you draw the interaction before reading the answer?

## Discovery

Energy trades between storage and motion, producing oscillation.

## Implementation

We build a minimal `oscillation` model in Python.

Source: [`python/chapter12/main.py`](https://github.com/ishmum123/building-autonomous-robots/blob/main/python/chapter12/main.py)  ·  [view in browser](assets/simulations/chapter12/sim.py)

Run the implementation:

```bash
python python/chapter12/main.py
```

## Simulation

Source: [`simulations/chapter12/sim.py`](https://github.com/ishmum123/building-autonomous-robots/blob/main/simulations/chapter12/sim.py)  ·  [view in browser](assets/simulations/chapter12/sim.py)

Run the chapter simulation:

```bash
python simulations/chapter12/sim.py
```

A browser version is available at [`browser/chapter12/index.html`](https://github.com/ishmum123/building-autonomous-robots/blob/main/browser/chapter12/index.html)  ·  [run live](assets/browser/chapter12/index.html).

## Exercises

1. Change one parameter in the simulation and predict what will happen.
2. Draw the system before and after the discovery.
3. Name one real-world device that depends on this idea and one way it can fail.

## Engineering Notes

Real systems add noise, latency, and power limits. The model we built is the simplest version; real `oscillation` designs trade accuracy, cost, and reliability.

---

**Continue → [Why Feedback Changes Everything](13-why-feedback-changes-everything.md)**
