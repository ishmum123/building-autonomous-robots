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

We will build a minimal `feedback loop` model in Python.

Open `python/chapter13/main.py` and follow the step-by-step construction.

## Simulation

Run the chapter simulation:

```bash
python simulations/chapter13/sim.py
```

A browser version is available at `browser/chapter13/index.html`.

## Exercises

1. Change one parameter in the simulation and predict what will happen.
2. Draw the system before and after the discovery.
3. Name one real-world device that depends on this idea and one way it can fail.

## Engineering Notes

Real systems add noise, latency, and power limits. The model we built is the simplest version; real `feedback loop` designs trade accuracy, cost, and reliability.

---

**Continue → Why Guessing Isn't Control**
