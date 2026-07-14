# Why Robots Need Senses

## The Problem

A robot with motors but no sensors bumps into walls. Why is measurement necessary for autonomy?

## Thinking

Before we name anything, ask yourself:

- What would happen if the missing piece were absent?
- What is the simplest system that could show this effect?
- Can you draw the interaction before reading the answer?

## Discovery

Sensors close the loop between the world and the controller.

## Simulation

Run the chapter simulation in your browser:

- Source: [`browser/chapter19/index.html`](https://github.com/ishmum123/building-autonomous-robots/blob/main/browser/chapter19/index.html)
- Live demo: [assets/browser/chapter19/index.html](assets/browser/chapter19/index.html)

The demo is a self-contained HTML page with a tiny JavaScript physics engine. Open it directly or through the site link above.

## Exercises

1. Change one parameter in the simulation and predict what will happen.
2. Draw the system before and after the discovery.
3. Name one real-world device that depends on this idea and one way it can fail.

## Engineering Notes

Real systems add noise, latency, and power limits. The model we built is the simplest version; real `sensor` designs trade accuracy, cost, and reliability.

---

**Continue → [Why Accelerometers Lie](20-why-accelerometers-lie.md)**
