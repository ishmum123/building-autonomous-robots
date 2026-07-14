# Why A* Works

## The Problem

You could explore every path, but that is too slow. How do you search smartly?

## Thinking

Before we name anything, ask yourself:

- What would happen if the missing piece were absent?
- What is the simplest system that could show this effect?
- Can you draw the interaction before reading the answer?

## Discovery

A* uses a heuristic to focus search toward the goal.

## Simulation

Run the chapter simulation in your browser:

- Source: [`browser/chapter37/index.html`](https://github.com/ishmum123/building-autonomous-robots/blob/main/browser/chapter37/index.html)
- Live demo: [assets/browser/chapter37/index.html](assets/browser/chapter37/index.html)

The demo is a self-contained HTML page with a tiny JavaScript physics engine. Open it directly or through the site link above.

## Exercises

1. Change one parameter in the simulation and predict what will happen.
2. Draw the system before and after the discovery.
3. Name one real-world device that depends on this idea and one way it can fail.

## Engineering Notes

Real systems add noise, latency, and power limits. The model we built is the simplest version; real `A* search` designs trade accuracy, cost, and reliability.

---

**Continue → [Why Robots Change Their Mind](38-why-robots-change-their-mind.md)**
