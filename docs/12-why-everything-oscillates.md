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

We will build a minimal `oscillation` model in Python.

Open `python/chapter12/main.py` and follow the step-by-step construction.

## Simulation

Run the chapter simulation:

```bash
python simulations/chapter12/sim.py
```

A browser version is available at `browser/chapter12/index.html`.

## Exercises

1. Change one parameter in the simulation and predict what will happen.
2. Draw the system before and after the discovery.
3. Name one real-world device that depends on this idea and one way it can fail.

## Engineering Notes

Real systems add noise, latency, and power limits. The model we built is the simplest version; real `oscillation` designs trade accuracy, cost, and reliability.

---

**Continue → [Why Feedback Changes Everything](13-why-feedback-changes-everything.md)**
