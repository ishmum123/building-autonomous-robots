# Why Planning Is Hard

## The Problem

A robotic arm must move a mug from a kitchen counter to a shelf — without hitting the microwave, the faucet, the backsplash, or the mug's own handle as the arm rotates. The arm has 6 joints. Each joint can rotate within a range of about 300°. The path through configuration space — the space of all possible joint angle combinations — must stay entirely within the collision-free region.

Discretize each joint into 1000 positions. The number of joint configurations is 1000⁶ = 10¹⁸. Exhaustive search over all configurations at 10⁹ operations per second would take 10⁹ seconds — 31 years. For a 6-DOF arm. A humanoid robot has 30+ joints.

And this ignores dynamics. Trajectories must be smooth (no joint can teleport), time-constrained, and energy-efficient. The "find any safe path" version is already intractable. The "find the shortest, smoothest, safest path" version is much harder:

- Configuration space is high-dimensional — dimensionality grows with number of joints
- Collision-free regions are non-convex — the geometry of obstacles creates irregular holes in config space
- The shortest path through a non-convex space may be globally far from the locally-shortest
- Dynamic constraints couple joint positions: the arm's inertia at joint 1 depends on the angle at joint 2

## What Would You Try?

- You can check whether any single joint configuration collides with an obstacle in a few milliseconds. Can you use this ability to build a path, even without knowing the full structure of the configuration space?
- The robot doesn't need to find the globally shortest path — just a safe, executable one. Does relaxing optimality make the problem tractable?
- Humans don't plan every joint angle explicitly when reaching for a mug. They move toward the goal and adjust. Could that strategy work for a robot, and when does it fail?

## Failed Attempts

### Attempt 1: Grid search over configuration space

Discretize configuration space into a grid. Build a graph where each node is a discretized configuration and edges connect adjacent nodes. Search the graph with BFS or Dijkstra.

The exponential scaling shown above makes this infeasible for more than 3–4 joints. Even at coarse resolution (100 positions per joint, 6 joints), the grid has 10¹² nodes. Memory alone is prohibitive: 10¹² nodes × 8 bytes each = 8 terabytes. The approach that works in 2D maps (chapter 37) doesn't scale to high-dimensional robot arms. Curse of dimensionality is not a slogan — it's a concrete exponential blowup.

### Attempt 2: Gradient descent in configuration space

Start at the current joint configuration. Compute the gradient of a potential field: obstacles repel, goal attracts. Move the joints in the direction that decreases potential energy. This is potential field planning.

Potential field planning is fast and memory-free — it doesn't need to store any graph. It fails at local minima: if the robot finds a configuration where the attractive force from the goal and repulsive forces from obstacles exactly balance, it stops moving. These local minima are common in complex scenes — a narrow passage between two obstacles can form a saddle point that traps the planner even though a path exists. The robot sits frozen 10 cm from the goal because a chair leg creates a repulsion equal to the goal's attraction. In the kitchen scenario, the mug's own handle and the backsplash together create numerous local minima.

### Attempt 3: Rapidly-Exploring Random Trees (RRT) without any heuristic

Sample random configurations uniformly in configuration space. Find the nearest node in the existing tree. Extend toward the sample by a fixed step size. If the extended configuration is collision-free, add it to the tree. Repeat until the tree reaches the goal.

Basic RRT is actually a reasonable approach — it avoids the exponential grid and escapes local minima by random exploration. But without any bias toward the goal, it explores the configuration space uniformly. In a 6D space where the goal occupies 0.001% of the volume, the probability of sampling near the goal is 0.001%. The planner takes millions of samples and hours of compute to find a path that a more informed search would find in seconds. Uniform random trees are complete (will eventually find a path if one exists) but not efficient.

## The Discovery

Grid search fails from exponential memory; potential fields fail from local minima; unbiased random trees fail from inefficiency. The common theme: each approach is missing information about the problem structure.

The insight that breaks the deadlock: you don't need to discretize the full space in advance. You can **sample** configurations on demand and build a tree that grows toward the goal — combining random exploration (to escape local minima) with goal-biased sampling (to be efficient). Sample a random configuration, but with probability 0.05–0.1, sample the goal configuration directly. This small goal bias dramatically reduces average time to find a path because the tree grows toward the goal rather than spreading uniformly.

The result is **RRT-Connect** or **bidirectional RRT**: grow two trees simultaneously, one from start and one from goal, and try to connect them. Bidirectional search halves the effective distance the planner must cover, and goal bias ensures neither tree wastes effort on irrelevant regions.

For arms and complex robots, planning is inherently probabilistic and approximate — probabilistically complete algorithms that find *a* safe path quickly, then smooth and shorten it in post-processing. Path shortcutting (randomly replacing curve segments with shorter straight-line segments, checking collision) recovers most of the optimality lost during exploration.

## Try It

<iframe src="../assets/browser/chapter36/index.html" width="100%" height="460" style="border:1px solid var(--md-default-fg-color--lightest);border-radius:8px;"></iframe>

[open in a new tab](../assets/browser/chapter36/index.html)

Before changing anything, predict:

- Watch the potential field planner in a scene with a narrow passage between two obstacles. Does it get stuck, and if so, where relative to the passage?
- Compare RRT with 0% goal bias versus 10% goal bias in the same scene. Which finds a path faster? Does the 0% version always find a path eventually?
- Add a local minimum (symmetric obstacle arrangement) to the potential field scene. Can you find an obstacle configuration that traps the gradient planner indefinitely?

## Implementation

`browser/common/engine.js` provides `Grid`, `astar`, `drawGrid`, `drawGridPath`, and `drawPoint`. `browser/chapter36/index.html` runs two robots on the same grid: the left robot uses inline `greedyPos(step)` (moves toward the goal each step, halts if `grid.isBlocked`), while the right robot plans with `path = astar(grid, START, GOAL)`. The `wallLen` slider adjusts a vertical wall obstacle; greedy gets trapped behind it while A* routes around. The side-by-side comparison makes the optimality gap concrete without any RRT or heat map.

## When It Breaks

**Narrow passages in configuration space.** Even RRT struggles when the collision-free region has a narrow passage — a configuration space corridor much thinner than the typical sample step size. The probability of sampling into the passage is proportional to its volume, which may be tiny. A robot arm threading a needle through a narrow gap between two shelves creates exactly this: the valid configurations for the elbow are a thin slice of joint space. Bridge sampling and Visibility PRM variants specifically address narrow passages by biasing samples near obstacle surfaces.

**Moving obstacles invalidate precomputed paths.** Planning for a static scene produces a static plan. When a human walks into the robot's workspace, the precomputed path intersects a new obstacle. The robot must either stop and replan (latency) or continuously compute a new plan. Replanning with RRT from scratch takes 100–500 ms — fast for a slow arm, not for a drone avoiding a bird. Dynamic planning approaches (chapter 38) address this but introduce their own complexity.

## Transfer

- **Drug discovery molecular docking**: computing whether a drug molecule fits into a protein binding site is a planning problem in the molecule's configuration space (position, orientation, and bond rotations). The same dimensionality curse applies — the molecule has 10+ degrees of freedom, the binding pocket has complex geometry, and random sampling with bias toward the pocket is the standard approach.
- **Surgical robot trajectory planning**: da Vinci robotic surgery requires tool paths that avoid anatomical structures not in the surgical target. Planning is done in a 3D volumetric map of the patient's anatomy with the same configuration space obstacles as a robotic arm — but re-planning must be fast enough to track a beating heart.
- **Video game NPC pathfinding**: game characters navigate 3D worlds with complex geometry. They use simplified configuration spaces (2D footprint + orientation) and navigation meshes rather than full 6D config space, because the planning must run in under a millisecond for hundreds of characters simultaneously.

Exercises:

1. A 3-DOF planar robot arm has joints with 360°, 180°, and 90° ranges. If grid-sampled at 10 positions per degree, how many nodes does the configuration space grid contain? Compare this to a 2D floor-plan grid of a 50 × 50 m room at 0.1 m resolution.
2. A potential field planner has attractive gain k_att = 1.0 and repulsive gain k_rep = 2.0 from an obstacle. The goal is 3 m ahead; an obstacle is 0.5 m to the left. Compute the x and y components of the net force and determine whether the planner moves toward or away from the goal.
3. An RRT runs with 5% goal-bias sampling. If each sample takes 1 ms to generate and collision-check, and on average it takes 2,000 samples to find a path, how long does planning take? If you increase goal bias to 30%, the sample count drops to 500 but each sample takes 2 ms (more complex nearest-neighbor computation). Which is faster overall?

---

**Continue → [Why A* Works](37-why-astar-works.md)**
