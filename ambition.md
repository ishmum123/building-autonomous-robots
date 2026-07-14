# PROJECT_AMBITION.md

# Building Autonomous Robots From Scratch

> **Learn robotics the way humanity could have invented it.**

---

# Mission

This project is **not** a robotics textbook.

It is **not** a robotics reference.

It is **not** a collection of tutorials.

It is an **engineering journey**.

The goal is to rebuild every important invention in robotics from first principles until a complete autonomous robot naturally emerges.

By the end of the curriculum, the reader should understand **why every subsystem exists**, not merely how to use it.

---

# Inspiration

This project aims to do for robotics what **Build a Large Language Model (From Scratch)** by Sebastian Raschka did for LLMs.

Not by copying the content.

By adopting the philosophy.

Every chapter should feel like building one more piece of an enormous machine.

The reader should constantly think:

> "Wait... I actually built that."

---

# Core Philosophy

The curriculum follows six immutable rules.

## Rule 1

Every discovery begins with a problem.

Never begin with a definition.

Bad:

> A brushless motor is...

Good:

> We have a problem. Brushes wear out. How could we eliminate them?

---

## Rule 2

Every discovery introduces exactly one major idea.

Readers should never learn two unrelated concepts simultaneously.

---

## Rule 3

Every discovery ends with something that moves.

Motion creates motivation.

Examples:

* a rolling wheel
* a spinning motor
* a balancing robot
* a flying drone

Every chapter should produce a visible result.

---

## Rule 4

No black boxes.

If we later use

PID()

the reader has already implemented one.

If we later use

KalmanFilter()

the reader has already derived one.

Nothing appears magically.

---

## Rule 5

Always discover before naming.

Vocabulary comes after intuition.

Readers should already understand the idea before learning its formal name.

---

## Rule 6

Every abstraction must have been implemented manually once.

Libraries are introduced only after readers appreciate why they exist.

---

# Educational Style

This project should feel closer to:

* Crafting Interpreters
* Build a Large Language Model (From Scratch)
* The Rust Book

than a university textbook.

The tone should be conversational.

Curiosity-driven.

Problem-solving.

Never encyclopedic.

---

# Reader Experience

Reading should feel like participating in humanity's inventions.

Every chapter should answer

> Suppose nobody had invented this before.

How could we?

---

# Discovery Structure

Every discovery follows the same template.

## 1 Problem

Present a real engineering problem.

No theory.

Only constraints.

---

## 2 Thinking

Guide the reader.

Ask questions.

Encourage predictions.

Never immediately reveal the answer.

---

## 3 Discovery

Allow the solution to emerge naturally.

Only now introduce terminology.

---

## 4 Implementation

Build it.

Python first.

Readable.

Minimal dependencies.

---

## 5 Simulation

Every chapter contains an executable simulation.

Initially:

Python

Eventually:

Browser-based interactive simulations.

---

## 6 Exercises

Exercises extend the idea.

Not rote memorization.

Real engineering thought experiments.

---

## 7 Engineering Notes

Explain how real systems differ.

Examples:

"We built a brushed motor.

Real drones use brushless motors because..."

---

## 8 Continue

Every chapter naturally leads into the next.

Readers should always want to continue.

---

# Naming Convention

Never use generic chapter names.

Prefer mysteries.

Good:

Why Wheels Move

Why Things Refuse to Move

Why Magnets Pull

Why Brushes Had to Disappear

Why PID Was Invented

Why Sensors Disagree

Why Robots Get Lost

Bad:

Motors

Control Systems

Sensors

Localization

---

# Repository Structure

```
building-autonomous-robots/

docs/

discoveries/

browser/

cpp/

assets/

diagrams/

tools/

.github/
```

The repository should resemble a software project rather than a book.

---

# Technology Stack

Current

* Markdown
* MkDocs
* Material for MkDocs

Future

* Astro
* TypeScript
* Interactive Canvas simulations
* WebAssembly (optional)
* SVG animations
* Mermaid diagrams

The website should eventually become an interactive textbook.

---

# Simulation Philosophy

Simulations are first-class citizens.

The lesson explains the simulation.

Not the other way around.

Every simulation should be understandable.

No giant frameworks.

Minimal code.

Visual.

Interactive.

---

# Long-Term Curriculum

## Part I

Motion

Why Wheels Move

Why Things Refuse to Move

Why Magnets Pull

Why Electricity Can Push

Why Copper Becomes a Magnet

Why Motors Spin

Why Motors Stop

Why Brushes Had to Disappear

Why Three Wires Are Better Than Two

Why Motors Need Conductors

---

## Part II

Control

Why Faster Isn't Better

Why Everything Oscillates

Why Feedback Changes Everything

Why Guessing Isn't Control

Why Errors Accumulate

Why PID Was Invented

Why One PID Isn't Enough

Why Quadcopters Need Two Brains

---

## Part III

Sensing

Why Robots Need Senses

Why Accelerometers Lie

Why Gyroscopes Drift

Why GPS Isn't Enough

Why Sensors Disagree

Why Sensor Fusion Works

Why Kalman Filters Exist

---

## Part IV

Flight

Why Four Motors Beat One

Why Quadcopters Flip

Why Hovering Is Hard

Why Wind Wins

Why Autopilots Exist

Why Drones Crash

---

## Part V

Thinking

Why Maps Matter

Why Dead Reckoning Fails

Why Robots Get Lost

Why SLAM Exists

Why Planning Is Hard

Why A* Works

Why Robots Change Their Mind

---

## Part VI

Autonomy

Why Following Isn't Understanding

Why Robots Need Goals

Why Obstacles Change Everything

Why State Matters

Why Estimation Beats Measurement

Why Decisions Need Models

Why Autonomous Drones Work

---

# Quality Bar

Every discovery should be good enough that someone discovering it independently would think:

> "This is better than most robotics textbooks."

Never optimize for quantity.

Always optimize for understanding.

---

# Final Principle

We are not teaching robotics.

We are teaching people to invent robotics.

