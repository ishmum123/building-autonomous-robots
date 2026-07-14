# Why Obstacles Change Everything

## The Problem

A drone needs to fly from point A to point B, 500 m apart. In free space — no obstacles — the solution is trivial: fly straight. Minimum distance, minimum time, minimum energy. A single arithmetic computation.

Now add a 20 m tall building directly in between. The drone can't fly through it. It must go around — left, right, or over. Left adds 80 m. Right adds 60 m. Over adds 15 m but requires more energy to climb and descend, and wind is stronger at altitude. The optimal path is now a calculation involving geometry, energy, and weather.

Now add 50 buildings in a dense urban canyon. The space of possible routes explodes. Some routes that look short on a 2D map are blocked in 3D. The "go over" option is sometimes available and sometimes not. Going around one building may take you into another.

What obstacles actually do to the problem:

- Convert a direct-path problem into a combinatorial routing problem
- Create non-convexity: a slight deviation from the optimal path can lead to a much worse path
- Introduce topology: some goal configurations are reachable only through specific obstacle gaps
- Make the problem sensitive to small positional errors — 1 m error near a tight corridor means collision

## What Would You Try?

- In a 2D map with rectangular obstacles, how would you find the shortest path? Could you reduce it to a graph problem?
- Obstacles have different costs: a crowded plaza is passable but requires slow flight; a restricted airspace is forbidden entirely. How do you represent obstacles of different severity in your path computation?
- If two obstacles are 10 cm apart and your drone is 30 cm wide, the corridor is infeasible regardless of what the geometric path suggests. How do you account for robot size when checking whether a path is safe?

## Failed Attempts

### Attempt 1: Treat obstacles as hard walls and shortest-path through the free cells

On a 2D grid, mark obstacle cells as impassable. Run A* through the free cells. This finds the shortest collision-free path.

This is correct at the grid level but ignores robot size. A drone with a 0.3 m body that flies through a 0.4 m gap between two buildings has 0.05 m clearance on each side — below any reasonable safety margin. Geometric shortest path in free space treats the drone as a point. The drone is not a point. Point-robot paths through tight corridors translate to clearance-zero paths for the real vehicle.

**Configuration space inflation** (Minkowski sum of robot body with obstacles) solves this by expanding every obstacle by the robot's radius, then treating the robot as a point. But inflation must match the robot's actual geometry. A cylindrical drone inflated by radius r is approximately correct; a complex-shaped drone with a protruding camera arm requires shape-specific inflation. Simple circle inflation underestimates safe clearance for elongated robots.

### Attempt 2: Assign soft costs to dangerous regions — penalize proximity

Instead of treating obstacles as binary (passable/impassable), add a proximity cost: cells within 5 m of an obstacle are penalized by 10× their base cost; cells within 2 m by 100×. A* naturally avoids high-cost cells.

Soft cost obstacles keep robots away from obstacles gracefully. They fail when the only route passes through a high-cost region — the algorithm finds the minimum-cost path which does pass through the penalized zone, but the cost function didn't make it impassable. A route requiring a 2 m clearance path gets taken if it has the lowest total cost, even if the proximity penalty is high. Soft costs make obstacles expensive but not forbidden — in a tight environment, the planner will grudgingly take the high-cost path because it's the only one. The penalty must be set high enough that the route is always rejected when clearance is too low, which makes the cost function parameter-sensitive.

### Attempt 3: Grow obstacles by a fixed buffer (conservative inflation)

Inflate every obstacle by 5 m. Now a drone flying through the inflated free space has at least 5 m clearance from every obstacle surface. Safe by construction.

Conservative inflation guarantees safety but destroys navigability in dense environments. A city block with buildings 8 m apart: inflated by 5 m each side, the gap is 8 - 10 = -2 m — the corridor disappears entirely. The planner declares the path infeasible. The real path exists: 8 m > drone width, the corridor is physically passable. By being too conservative, the planner treats navigable space as impassable. The choice of inflation radius is critical: too small is unsafe, too large is unnecessarily restrictive. The right value depends on localization accuracy, sensor noise, and wind — not a fixed constant.

## The Discovery

The three failures all set a fixed clearance policy — zero clearance (point robot), soft cost (negotiable clearance), or fixed buffer (constant clearance). None of them adapt to the actual uncertainty in the robot's position.

The correct approach: **clearance should be proportional to position uncertainty**. If the drone's position is known to ±0.1 m (precise GPS, calm air), a 0.3 m clearance is sufficient for a 0.3 m drone. If position uncertainty is ±1 m (GPS denied, high wind), the same drone needs 1.3 m clearance to guarantee safety with high probability.

This leads to **uncertainty-aware configuration space**: inflate obstacles not by a fixed buffer but by the robot's current 3σ position uncertainty. As uncertainty grows (dead reckoning drift, GPS outage), the effective obstacle boundary expands — and corridors that were passable become infeasible. The robot then plans more conservatively, automatically, without explicit programmer rules.

Formally: the configuration space obstacle C_obs(t) = geometric obstacle ⊕ robot body ⊕ 3σ(t) position uncertainty, where σ(t) grows during GPS outage and shrinks on fix. Planning happens in the current C_obs(t), producing paths that are safe given current uncertainty.

This is the robotics interpretation of **risk-aware planning**: the plan reflects the actual risk given current state knowledge, not an assumed worst-case or best-case scenario.

## Try It

<iframe src="../assets/browser/chapter41/index.html" width="100%" height="460" style="border:1px solid var(--md-default-fg-color--lightest);border-radius:8px;"></iframe>

[open in a new tab](../assets/browser/chapter41/index.html)

Before changing anything, predict:

- With zero inflation, does the point-robot path actually collide with obstacles when the finite-size drone follows it? At what obstacle density does this first happen?
- Increase position uncertainty (GPS off slider). Do previously-valid narrow corridors become infeasible? Does the drone's planned route become more conservative?
- Set uncertainty to maximum. Are there environments where no path exists under maximum inflation but a path exists under minimum inflation? Can the drone wait for a GPS fix to reduce uncertainty?

## Implementation

`browser/chapter41/index.html` shows the geometric obstacles alongside the inflated configuration space obstacles, updated in real time as position uncertainty changes. `browser/common/engine.js` computes the Minkowski sum of each obstacle with a circle of radius = robot_radius + 3σ_position. Watch the obstacle boundaries expand and contract as uncertainty changes — and watch the planner reroute when a previously-feasible corridor becomes occupied by the expanded obstacle boundary. The visualization renders both the geometric boundary (static) and the configuration space boundary (dynamic) simultaneously.

## When It Breaks

**Unknown obstacle geometry.** Configuration space inflation assumes you know the geometry of every obstacle. A lidar-mapped obstacle has uncertainty in its boundary location: the wall is known to ±0.1 m. The inflation must account for this geometric uncertainty plus position uncertainty — the total is larger than either alone. In disaster response environments (collapsed buildings), obstacle geometry is known only approximately, and inflation must be correspondingly conservative, reducing navigable space further.

**Moving obstacles require dynamic configuration space.** A pedestrian is an obstacle whose position is time-varying. A static configuration space represents the pedestrian as a fixed obstacle — but the pedestrian moves. Time-extended planning represents the trajectory in space-time (x, y, t) and plans in that space, treating the pedestrian's predicted trajectory as a space-time obstacle. This is computationally expensive and error-prone: pedestrian intent is uncertain, and the predicted trajectory is wrong as soon as the pedestrian changes direction.

## Transfer

- **Marine vessel traffic separation**: shipping lanes are defined as exclusion zones (configuration space obstacles) around reefs, shallows, and other hazard areas. The lane width accounts for vessel size plus a safety margin proportional to navigation uncertainty in that area. Historically, the margin was set by maritime experience; modern systems compute it from AIS positioning accuracy.
- **Radiation exclusion zones**: nuclear facilities define exclusion zones (configuration space obstacles for humans) around radioactive sources. The zone boundary is the geometric source location plus a margin proportional to measurement uncertainty of the source strength. The configuration space concept appears directly in radiation safety standards.
- **Urban air mobility corridors**: proposed UAM (Urban Air Mobility) frameworks define flyable corridors through cities. Corridor width accounts for vehicle size, navigation uncertainty, and wind variability — exactly the uncertainty-aware inflation problem. The FAA's BVLOS (beyond-visual-line-of-sight) drone regulations specify minimum clearances that scale with vehicle dimensions and operational conditions.

Exercises:

1. A drone has a 0.4 m radius. Its position uncertainty is 1σ = 0.3 m. What is the minimum obstacle clearance in the geometric map for a 99.7% (3σ) safety guarantee? If two buildings are 3 m apart, what is the minimum corridor width for safe passage?
2. Configuration space inflation with a 1 m buffer makes a 5 m corridor infeasible. The real corridor is 5 m wide and the drone is 0.3 m wide. What position uncertainty would justify a 1 m buffer? Is this buffer appropriate?
3. A city block has 12 buildings arranged in a grid with 4 m gaps between them. The drone is 0.3 m radius with 0.5 m position uncertainty. Which corridors are feasible after inflation? How does the answer change if position uncertainty increases to 2 m?

---

**Continue → [Why State Matters](42-why-state-matters.md)**
