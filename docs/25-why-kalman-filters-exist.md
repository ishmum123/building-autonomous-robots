# Why Kalman Filters Exist

## The Problem

You have a model and noisy measurements. How do you trust each just enough?

## Thinking

Before we name anything, ask yourself:

- What would happen if the missing piece were absent?
- What is the simplest system that could show this effect?
- Can you draw the interaction before reading the answer?

## Discovery

A Kalman filter optimally blends prediction and measurement.

## Simulation

Run the chapter simulation in your browser:

- Source: [`browser/chapter25/index.html`](https://github.com/ishmum123/building-autonomous-robots/blob/main/browser/chapter25/index.html)
- Live demo: [assets/browser/chapter25/index.html](assets/browser/chapter25/index.html)

The demo is a self-contained HTML page with a tiny JavaScript physics engine. Open it directly or through the site link above.

## Exercises

1. Change one parameter in the simulation and predict what will happen.
2. Draw the system before and after the discovery.
3. Name one real-world device that depends on this idea and one way it can fail.

## Engineering Notes

Real systems add noise, latency, and power limits. The model we built is the simplest version; real `Kalman filter` designs trade accuracy, cost, and reliability.

---

**Continue → [Why Four Motors Beat One](26-why-four-motors-beat-one.md)**
