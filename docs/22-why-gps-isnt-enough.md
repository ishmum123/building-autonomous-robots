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

We will build a minimal `GPS` model in Python.

Open `python/chapter22/main.py` and follow the step-by-step construction.

## Simulation

Run the chapter simulation:

```bash
python simulations/chapter22/sim.py
```

A browser version is available at `browser/chapter22/index.html`.

## Exercises

1. Change one parameter in the simulation and predict what will happen.
2. Draw the system before and after the discovery.
3. Name one real-world device that depends on this idea and one way it can fail.

## Engineering Notes

Real systems add noise, latency, and power limits. The model we built is the simplest version; real `GPS` designs trade accuracy, cost, and reliability.

---

**Continue → [Why Sensors Disagree](23-why-sensors-disagree.md)**
