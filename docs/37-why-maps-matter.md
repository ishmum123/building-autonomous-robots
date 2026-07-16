# Why Maps Matter

## The Problem

A warehouse robot receives a task: move a pallet from bay A7 to bay C12. It has a lidar that scans 360 degrees every 100 ms. It can see 8 meters in every direction. The warehouse is 60 meters wide.

The robot starts moving. After 4 meters it detects a wall to its right, a forklift ahead, and an open aisle to the left. It turns left. Three meters later it detects another wall. It has no idea whether this is the same wall or a different one. It has no idea how far it is from C12. It circles the same aisle twice before running its battery down.

The lidar gives accurate local geometry. Without a map, that geometry is useless beyond the immediate moment:

- No memory of where walls were 10 seconds ago — every scan is the first scan
- No sense of global position — current sensor data doesn't say where you are in the building
- No path connectivity — can't reason about which sequence of aisles leads to C12
- No persistent model for other agents to share — every robot must rediscover everything

## What Would You Try?

- The robot can measure the distance to the nearest wall at any angle. How would you use a sequence of such measurements, taken while the robot moves, to reconstruct the shape of the warehouse?
- Two robots are working in the same warehouse. Could they share their local sensor readings to collectively build a picture faster than either alone? What would need to be true for this to work?
- A shelf gets moved. The map from last week is now wrong in one aisle. How should the robot detect this, and should it update the whole map or only the affected region?

## Failed Attempts

### Attempt 1: React only to current sensor readings

Navigate by reflex: if lidar shows obstacle ahead, turn away from it. If goal direction is clear, go forward. No memory, no map — pure reactive control.

This works in a sparse, simple environment: a hallway with one turn. It fails the moment the environment has loops, dead ends, or globally disconnected paths. The robot can spend hours oscillating in a symmetric room because the sensor reading at position A looks identical to the sensor reading at position B — and there's no state that distinguishes them. The warehouse navigation failure above is exactly this: the robot can't learn from where it has already been.

### Attempt 2: Record a sequence of sensor readings tied to motor commands

Instead of building a spatial model, store a log: "moved forward 2 m, saw wall at 3 m to right; turned 45° left, saw open space ahead; moved 3 m…" Replay this log to navigate the same path again.

This is rote memorization of a specific trajectory. It fails on the first deviation: a forklift parked in the recorded path causes the robot to stop. It can't reason about an alternative route because the log contains no geometry — just a sequence of commands. And a new destination requires a new recording from scratch. The log is a path, not a model. Navigating to any goal requires a model.

### Attempt 3: Use a global coordinate grid and mark obstacles as the robot finds them

Build a 2D occupancy grid: a large bitmap where each cell is "free", "occupied", or "unknown". When the lidar detects a wall, mark those cells occupied. Mark the cells the robot drove through as free. Navigate to the goal by finding a path through free cells.

This works — it's essentially the right approach — but breaks in one critical way: it assumes you know where you are in the grid when you mark cells. If the robot's position estimate drifts (wheel slip, imperfect odometry), it marks walls in the wrong grid cells. The map becomes inconsistent: the same physical wall appears in two places, the "free" cells overlap with actual walls. A map built on a bad position estimate is worse than no map — it confidently routes the robot into walls.

## The Discovery

The three attempts reveal a dependency that can't be eliminated: **you need a position estimate to build a map, and you need a map to improve your position estimate**. This appears circular — it is. But there's a way to carry both forward together.

The key insight from the occupancy grid failure: don't record individual sensor points as if they were ground truth. Record them as *evidence* — each sensor return raises the probability that a particular cell is occupied and lowers it for nearby cells. Then the map is a probabilistic model, not a hard record. As the robot moves and re-observes the same wall from a different angle, the probability updates. Measurement errors don't create contradictions — they create uncertainty that resolves with more observations.

The map as a probabilistic evidence accumulator — combined with a position estimate that is also uncertain and updated from landmarks in the map — is the foundation of **simultaneous localization and mapping**, which we'll build in chapter 40. But the core insight is here: a map is not a photo of the world. It is a probabilistic model, built incrementally, that gets better with every scan rather than becoming more wrong.

## Try It

<iframe src="../assets/browser/chapter37/index.html" width="100%" height="460" style="border:1px solid var(--md-default-fg-color--lightest);border-radius:8px;"></iframe>

[open in a new tab](../assets/browser/chapter37/index.html)

Before changing anything, predict:

- Run the reactive-only robot for 60 seconds. Does it ever reach the goal? Does it revisit the same aisle more than once, and how can you tell?
- Enable map building. Watch the occupancy grid fill in as the robot explores. Where does it first go wrong — and is the error from sensor noise, position drift, or something else?
- Add some odometry drift (wheel slip slider). Does the map remain consistent, or do walls start appearing in two places? At what drift level does the map become useless?

## Implementation

`browser/common/engine.js` provides `Grid` and `astar`. `browser/chapter37/index.html` creates `gridA = new Grid(COLS, ROWS)` and `gridB = new Grid(COLS, ROWS)`, runs a random walk on `gridA` (using a `dirs` array, checking `Grid.isBlocked`), and plans a path on `gridB` with `pathB = astar(gridB, [0, 0], [COLS-1, ROWS-1])`. The sim shows the difference between undirected exploration and goal-directed path planning on the same grid structure; `drawGrid` and `drawGridPath` render both side by side.

## When It Breaks

**Dynamic environments destroy static maps.** An occupancy grid assumes the world doesn't change after being mapped. In a warehouse with forklifts, the map from 10 minutes ago may have free cells where a forklift is now parked. A robot trusting an old map routes into the forklift. Amazon fulfillment centers address this by running continuous re-mapping with short map lifetimes and distinguishing static structure (shelves, walls) from dynamic objects (robots, human workers) — a two-layer map with different update rates.

**Map resolution versus memory tradeoff.** A 0.05 m resolution grid for a 100 × 100 m warehouse requires 4 million cells. For 3D mapping (multi-story building, flying drone), a 0.05 m voxel grid for a 100 × 100 × 10 m space requires 80 million voxels — hundreds of megabytes just for the map. Octomap and similar sparse representations solve this by storing only non-empty cells, but they still face fundamental memory scaling limits for large outdoor environments.

## Transfer

- **Autonomous vehicle HD maps**: self-driving cars maintain pre-built high-definition maps of road geometry, lane markings, and traffic signs — then localize within them using lidar. The map is built offline with survey vehicles; the car's real-time task is matching current lidar scans to the pre-built map to find its centimeter-level position.
- **Surgical robotics workspace modeling**: robotic surgery systems build a 3D model of the organ surface during the procedure from stereo camera images, then navigate tool paths relative to that model. Without the map, every tool movement is blind.
- **Search and rescue drones**: when a drone enters a collapsed building, it builds a 3D volumetric map of passable corridors in real time, marking explored versus unexplored volumes, so operators can direct it systematically rather than by remote video alone.

Exercises:

1. A 50 × 50 m warehouse uses a 0.1 m grid. How many cells does the map require? If each cell stores a single byte, how large is the map in memory?
2. A lidar returns a reading at 4.3 m at bearing 35°. Convert this to a grid cell (x, y) if the robot is at grid position (250, 250) facing north. Assume 0.1 m cells.
3. The log-odds update adds 0.4 for each occupied hit and subtracts 0.2 for each free-space sweep. A cell starts at log-odds 0 (50/50). After 3 occupied hits and 2 free sweeps, what is the cell's log-odds and corresponding probability?

---

**Continue → [Why Dead Reckoning Fails](38-why-dead-reckoning-fails.md)**
