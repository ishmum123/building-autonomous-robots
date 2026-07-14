# Why Dead Reckoning Fails

## The Problem

You estimate position by counting steps, but after a while you are wrong. Why?

## Thinking

Before we name anything, ask yourself:

- What would happen if the missing piece were absent?
- What is the simplest system that could show this effect?
- Can you draw the interaction before reading the answer?

## Discovery

Integrating velocity accumulates error without bounds.

## Implementation

We build a minimal `dead reckoning` model in Python.

Source: [`python/chapter33/main.py`](https://github.com/ishmum123/building-autonomous-robots/blob/main/python/chapter33/main.py)  ·  [view in browser](assets/simulations/chapter33/sim.py)

Run the implementation:

```bash
python python/chapter33/main.py
```

## Simulation

Source: [`simulations/chapter33/sim.py`](https://github.com/ishmum123/building-autonomous-robots/blob/main/simulations/chapter33/sim.py)  ·  [view in browser](assets/simulations/chapter33/sim.py)

Run the chapter simulation:

```bash
python simulations/chapter33/sim.py
```

A browser version is available at [`browser/chapter33/index.html`](https://github.com/ishmum123/building-autonomous-robots/blob/main/browser/chapter33/index.html)  ·  [run live](assets/browser/chapter33/index.html).

## Exercises

1. Change one parameter in the simulation and predict what will happen.
2. Draw the system before and after the discovery.
3. Name one real-world device that depends on this idea and one way it can fail.

## Engineering Notes

Real systems add noise, latency, and power limits. The model we built is the simplest version; real `dead reckoning` designs trade accuracy, cost, and reliability.

---

**Continue → [Why Robots Get Lost](34-why-robots-get-lost.md)**
