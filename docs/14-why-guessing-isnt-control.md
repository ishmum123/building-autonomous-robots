# Why Guessing Isn't Control

## The Problem

You send the same motor command twice and get different results. Why does a fixed plan fail?

## Thinking

Before we name anything, ask yourself:

- What would happen if the missing piece were absent?
- What is the simplest system that could show this effect?
- Can you draw the interaction before reading the answer?

## Discovery

Without measurement, a controller cannot correct disturbances.

## Simulation

Run the chapter simulation in your browser:

- Source: [`browser/chapter14/index.html`](https://github.com/ishmum123/building-autonomous-robots/blob/main/browser/chapter14/index.html)
- Live demo: [assets/browser/chapter14/index.html](assets/browser/chapter14/index.html)

The demo is a self-contained HTML page with a tiny JavaScript physics engine. Open it directly or through the site link above.

## Exercises

1. Change one parameter in the simulation and predict what will happen.
2. Draw the system before and after the discovery.
3. Name one real-world device that depends on this idea and one way it can fail.

## Engineering Notes

Real systems add noise, latency, and power limits. The model we built is the simplest version; real `open loop control` designs trade accuracy, cost, and reliability.

---

**Continue → [Why Errors Accumulate](15-why-errors-accumulate.md)**
