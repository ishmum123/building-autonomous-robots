# Why Motors Stop

## The Problem

A motor spins fast when free and slows under load. What fights the motion?

## Thinking

Before we name anything, ask yourself:

- What would happen if the missing piece were absent?
- What is the simplest system that could show this effect?
- Can you draw the interaction before reading the answer?

## Discovery

Friction and back-electromotive force oppose rotation.

## Simulation

Run the chapter simulation in your browser:

- Source: [`browser/chapter07/index.html`](https://github.com/ishmum123/building-autonomous-robots/blob/main/browser/chapter07/index.html)
- Live demo: [assets/browser/chapter07/index.html](assets/browser/chapter07/index.html)

The demo is a self-contained HTML page with a tiny JavaScript physics engine. Open it directly or through the site link above.

## Exercises

1. Change one parameter in the simulation and predict what will happen.
2. Draw the system before and after the discovery.
3. Name one real-world device that depends on this idea and one way it can fail.

## Engineering Notes

Real systems add noise, latency, and power limits. The model we built is the simplest version; real `back-emf and friction` designs trade accuracy, cost, and reliability.

---

**Continue → [Why Brushes Had to Disappear](08-why-brushes-had-to-disappear.md)**
