# Why Errors Accumulate

## The Problem

Small mistakes in direction add up over a long walk. How do tiny errors become huge errors?

## Thinking

Before we name anything, ask yourself:

- What would happen if the missing piece were absent?
- What is the simplest system that could show this effect?
- Can you draw the interaction before reading the answer?

## Discovery

Errors integrate over time, so a controller must remove steady bias.

## Implementation

We will build a minimal `integration drift` model in Python.

Open `python/chapter15/main.py` and follow the step-by-step construction.

## Simulation

Run the chapter simulation:

```bash
python simulations/chapter15/sim.py
```

A browser version is available at `browser/chapter15/index.html`.

## Exercises

1. Change one parameter in the simulation and predict what will happen.
2. Draw the system before and after the discovery.
3. Name one real-world device that depends on this idea and one way it can fail.

## Engineering Notes

Real systems add noise, latency, and power limits. The model we built is the simplest version; real `integration drift` designs trade accuracy, cost, and reliability.

---

**Continue → [Why PID Was Invented](16-why-pid-was-invented.md)**
