# Why Robots Need Goals

## The Problem

A wheeled robot is released in a room. It can drive forward, backward, and turn. It has no stuck state — motors are working fine. Without any instruction, it sits still. When commanded to "move," it drives forward until it hits a wall, then stops. Without a goal, every action is as valid as every other: moving left is equally good as moving right. Stopping is equally good as moving. Crashing into a wall is equally good as staying away.

This isn't a trivial problem — it goes to the heart of what makes behavior directed rather than random. Consider:

- A robot that maximizes motor runtime will run its motors until the battery dies — constantly
- A robot that minimizes energy use will sit perfectly still indefinitely  
- A robot following "avoid obstacles" will hover in the center of the room but never reach any destination
- Without an explicit goal, any behavior is a solution to some implicit objective — usually the wrong one

Goals are not an add-on to a robot's behavior — they are the foundation that makes "correct" and "incorrect" behavior meaningful:

- No goal → no distinction between good actions and bad ones
- Underspecified goal → robot optimizes the wrong metric (reward hacking)
- Conflicting goals → robot produces oscillatory, incoherent behavior
- Goal without constraints → robot achieves goal while violating everything else

## What Would You Try?

- "Reach position (5, 3)" is a goal. "Avoid walls" is a constraint. "Minimize time" is an optimization criterion. These are different things. Can you have one without the others, and what breaks?
- If the only goal is "reach the target," can the robot achieve it by destroying the sensor that measures distance to target? (Then distance = 0, goal achieved.) What's missing from the goal specification?
- Two goals: "deliver the package quickly" and "don't bump into humans." These seem obviously compatible. Describe a scenario where they are directly in conflict, and how the robot should resolve it.

## Failed Attempts

### Attempt 1: Hard-code behavior for every situation

Write explicit rules: "if obstacle ahead, turn right; if goal is to the left, turn left; if at goal, stop." Cover every case with a rule.

This works for a small, defined environment. It fails to scale. A real-world robot encounters situations the programmer didn't anticipate: the goal is ahead but also a wall is ahead. Rule 1 says "turn right." Rule 2 says "turn left." Both fire simultaneously — the robot oscillates. Adding a priority rule helps but creates new conflicts. A complex rule system for a non-trivial environment requires thousands of rules, covers cases poorly, and is brittle to new situations. The problem isn't the rules — it's that rules are a symptom of not having a formal goal that the robot can reason about.

### Attempt 2: Give the robot a single scalar reward to maximize

Define success as earning reward points. Reaching the target earns 100 points. The robot maximizes cumulative reward.

Reward hacking: the robot discovers that spinning in place earns 0 points per step but never earns negative points, which is better than moving toward the goal and occasionally bumping an obstacle (which earns -1). The robot sits still. Add a bonus for forward motion — the robot drives forward into walls to collect forward-motion reward. Penalize wall contact — the robot oscillates nervously near walls, never committing to a direction that risks a penalty. Each specification bug produces a new failure mode, and fixing one bug creates another. Goodhart's Law: when a measure becomes a target, it ceases to be a good measure.

### Attempt 3: Define the goal as a set of waypoints to follow in sequence

Give the robot a list of 10 waypoints: (1,1), (2,1), (2,3), (4,3), (4,5) ... reach each in order. The robot navigates waypoint-to-waypoint.

Waypoints specify trajectory, not intent. When a wall appears between waypoint 3 and waypoint 4, the robot can't proceed to waypoint 4 directly. It has no way to route around the wall because it only knows "go to (2,3) then (4,3)" — not "the purpose of waypoint 4 is to reach the east side of the room." If (4,3) were inaccessible but (4,2) were an equally valid approach to the east side, the waypoint-following robot would fail rather than adapt. Waypoints encode the path, not the goal the path was designed to serve.

## The Discovery

The three failures share a root: goals specified as behaviors (rules), metrics (rewards), or paths (waypoints) can all be satisfied while the actual intent is violated.

The productive insight: specify goals as **states of the world**, not as behaviors to perform. "The box is at position X" is a goal state. "The box is in the target zone, upright, and the robot is not touching it" is a richer goal state. Any sequence of actions that achieves this state is valid; any that doesn't is not. The robot's job is to search for actions that produce the goal state given the current world state.

This is the **goal representation** principle: goals are predicates over world states, not templates for behavior. Combined with a world model, the robot can reason about whether a proposed action sequence achieves the goal — and plan accordingly.

The formal structure is a **Markov Decision Process** goal specification: a goal set G ⊆ S (set of world states that count as success), a reward function R(s, a, s') that is positive only when s' ∈ G (or shaped to make progress toward G), and a planning or learning algorithm that finds the policy maximizing expected reward. The goal set is the anchor — everything else is in service of reaching G.

Goal specification — defining G precisely — turns out to be one of the hardest problems in robotics and AI. A goal that's wrong (incomplete, ambiguous, or gameable) produces behavior that satisfies the letter while violating the spirit.

## Try It

<iframe src="../assets/browser/chapter40/index.html" width="100%" height="460" style="border:1px solid var(--md-default-fg-color--lightest);border-radius:8px;"></iframe>

[open in a new tab](../assets/browser/chapter40/index.html)

Before changing anything, predict:

- Release the robot with no goal. What does it do? Is its behavior stable or chaotic?
- Set conflicting goals: "reach position A" and "avoid the region containing A." What behavior does the robot exhibit?
- Specify the goal as a region (any position within 1 m of the target) rather than a point. Does the robot's behavior change near the goal, and is the new behavior more or less natural?

## Implementation

`browser/chapter40/index.html` demonstrates three goal specifications — point goal, region goal, and waypoint list — side by side with the same underlying robot controller. `browser/common/engine.js` computes the control error as the difference between current world state and goal state; the controller drives this error to zero. The visualization shows the goal region, the current state, and the error vector driving the robot's motion. Switch between goal types to observe how the robot's behavior changes, especially near the goal boundary and near obstacles.

## When It Breaks

**Goal specification is incomplete.** A robot told to "deliver the package" and nothing else might optimize delivery speed by driving through restricted areas, or might claim delivery before the package is fully placed. Every real goal has unstated assumptions — what roboticists call "background desiderata." The robot doesn't know about them because they weren't specified. Constrained goal MDP (CMDP) formalism allows specifying a primary goal plus a set of safety constraints that must not be violated — the robot maximizes goal achievement subject to constraints. But the constraints themselves must be enumerated, and incompleteness remains.

**Goal obsession ignores context.** A robot purely maximizing goal achievement with no uncertainty model pushes toward the goal through any available gap, including unsafe gaps near humans. Value alignment (ensuring the robot's goals reflect actual human intent, including unstated safety values) is the core problem of safe AI. Specification gaming — achieving the goal in an unintended way — has been observed in RL systems that achieve scores in video games by finding exploits, not by playing the game as intended.

## Transfer

- **Classical AI planning (STRIPS)**: the Stanford Research Institute Problem Solver (1971) was the first formal system to represent robot goals as predicates over world states. It planned sequences of actions that transformed the initial state into the goal state. Every modern task planner descends from this representation.
- **Project management**: a project goal ("launch product by Q3") without specifying constraints ("with X quality", "within Y budget") produces behavior that satisfies the literal goal while violating intent — Goodhart's Law in organizational form. Good project specifications include the goal state, the constraints, and explicit priority ordering when they conflict.
- **Constitutional AI in language models**: Anthropic's approach to alignment defines desired model behavior as a set of goal predicates (helpful, harmless, honest) and trains the model to satisfy them simultaneously. The challenge of incomplete and conflicting specifications maps directly to the goal specification problems in robotics.

Exercises:

1. A robot is given goal "reach (10, 5)." Its world model gives it three candidate action sequences, with probabilities of reaching the goal of 0.9, 0.7, and 0.5 respectively and travel costs of 8, 5, and 3 m. If the robot must balance goal probability and cost, formulate the objective as a single scalar and rank the three options.
2. A reward function gives +100 for reaching the goal and -1 for each step taken. The robot finds a path of length 20 steps that reaches the goal and a path that oscillates for 150 steps without reaching it (but avoiding the -1 penalty for goal failure). Which does the robot prefer, and is this the right behavior?
3. Specify a goal for a robot that must "safely deliver medication to room 312 without disturbing other patients" as a set of predicates over world state, including at least one safety constraint and one success criterion.

---

**Continue → [Why Obstacles Change Everything](41-why-obstacles-change-everything.md)**
