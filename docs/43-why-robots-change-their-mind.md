# Why Robots Change Their Mind

## The Problem

A drone has a planned path to a delivery point 800 m away, computed 3 seconds ago. The plan was optimal given the map at the time. Now, 200 m into the flight, its lidar detects a construction crane — not on the map — directly in the planned path at 400 m range.

Option 1: Stop and replan from scratch. A* on the full 500 × 500 grid takes 180 ms. The drone decelerates, hangs stationary, waits 180 ms, then resumes. Acceptable for slow ground robots; a hovering drone burns energy proportional to time and is vulnerable to wind during the hover.

Option 2: Keep flying on the original plan, treating the crane as a transient false detection. The plan was optimal; 3 seconds of sensor data shouldn't override it. This is disaster — the drone flies into the crane.

Option 3: Trigger obstacle avoidance and swerve. The swerve avoids the immediate obstacle but puts the drone on an arbitrary new trajectory that may not lead to the goal, may enter other obstacles, and may violate flight corridor restrictions.

A robot that can plan once and execute forever is fragile. A robot that replans perfectly each time an obstacle appears is slow. The tradeoff:

- Plan quality degrades as the world changes — time since planning is a liability
- Replanning from scratch is expensive — full search is O(cells) regardless of what changed
- Reactive avoidance is fast but plan-unaware — may trade one collision risk for another
- Doing nothing is never acceptable in a changing world

## What Would You Try?

- You have the old plan stored. The crane is a new obstacle that invalidates some nodes in the existing plan. Could you patch the existing plan rather than starting over?
- The new obstacle makes only 20 cells of your path infeasible. The remaining 780 m is fine. Could you plan a detour for just the blocked segment and reconnect to the original path?
- What information from the old A* search (the closed set, the g-values) could you reuse to speed up replanning, rather than discarding it and starting fresh?

## Failed Attempts

### Attempt 1: Replan from scratch with every new observation

Every 100 ms, receive updated sensor data. Re-run A* from current position to goal on the latest map. Follow the first segment of the new plan. Repeat.

This is provably optimal for each snapshot of the world. It fails on latency and compute. On a 500 × 500 grid with frequent changes, each replan takes 50–200 ms. If the drone moves at 15 m/s, 200 ms of planning corresponds to 3 m of flight — without an updated command. At high speed, even 50 ms latency causes the drone to overshoot turn points. And many replans are unnecessary: the obstacle is 400 m away; the next 5 m of path is unchanged. Replanning from scratch discards all prior computation even when almost nothing changed.

### Attempt 2: Only replan when the path is blocked

Monitor the planned path for upcoming obstacles. If the next 30 m is clear, continue executing. If it's blocked, trigger a replan.

This is better — replanning only when necessary. It breaks on near-miss scenarios: an obstacle appears 5 m to the right of the planned path. The path isn't blocked — it's still technically free. But the 2 m safety margin on the right is now violated. The drone continues flying 5 m from the obstacle at 15 m/s. A gust moves the obstacle or the drone laterally 3 m. Collision. The binary "blocked / not blocked" test doesn't model the margin erosion that precedes an actual block.

### Attempt 3: Local reactive avoidance with no replanning

When an obstacle is detected within 20 m, apply a repulsive force (potential field) to swerve away. When out of immediate range, resume following the global plan.

Local reactive avoidance is fast — it responds in under 10 ms. It fails at the intersection with the global plan: after swerving right to avoid the crane, the drone is now 30 m off the original path. Resuming the original plan requires flying 30 m back to rejoin it — which may go through or near the crane. The global plan doesn't know about the local swerve. The local swerve doesn't know about the global plan. The combination produces oscillation: swerve away, rejoin toward plan, swerve away again. This is the local-global coupling problem that reactive-only planning inherits.

## The Discovery

All three failures stem from treating planning and execution as separate phases rather than a continuous loop.

The insight: the old search computation contains useful information that doesn't become invalid just because one part of the map changed. Specifically, **D* Lite** (Focused Dynamic A*) maintains the A* search tree and marks nodes inconsistent when the map changes. On each replanning cycle, it re-expands only the inconsistent nodes — nodes whose g-values changed because an edge was added or removed. In the crane example, only the ~50 cells near the crane need re-expansion; the other 249,950 cells are still valid from the old search.

The formal property: D* Lite's replanning cost is proportional to the number of cells whose optimal path cost changed — not the total number of cells. For small localized changes (one new obstacle), replanning is fast. For large changes (whole section of map changes), it degrades toward full A*. But most real-world changes are local.

Combined with a safety margin check (replan when clearance drops below threshold, not just when path is blocked), D* Lite gives a planning loop that:
1. Plans the full path at startup
2. Executes while monitoring path clearance and new obstacles
3. Replans only the invalidated portions when the world changes
4. Returns to execution in under 10 ms for typical changes

This is **anytime replanning**: the planner can always return the best plan found so far, and improves it as compute time allows.

## Try It

<iframe src="../assets/browser/chapter43/index.html" width="100%" height="460" style="border:1px solid var(--md-default-fg-color--lightest);border-radius:8px;"></iframe>

[open in a new tab](../assets/browser/chapter43/index.html)

Before changing anything, predict:

- Place a new obstacle on the drone's path while it's flying. Does full-replan stop the drone noticeably? Does D* Lite? What is the difference in replanning cell count?
- Move the obstacle slowly across the path (dynamic obstacle). Does the drone successfully track around it, or does it get trapped between the moving obstacle and a wall?
- Set replanning threshold to require minimum 5 m clearance (instead of 0). Does the drone now replan earlier, keeping itself further from obstacles? What cost does this have in path efficiency?

## Implementation

`browser/common/engine.js` provides `Grid` and `astar`. `browser/chapter43/index.html` runs two robots: the stubborn robot follows `origPath = astar(gridA, START, GOAL)` computed once and ignores a new obstacle (tracked by `blockedA` flag), while the replanning robot calls `replanPath = astar(gridB, curPos, GOAL)` fresh from its current position when the obstacle appears at `obstFrame`. A strip plot compares steps taken by each; the cost of replanning versus the cost of stubbornness is directly observable. The sim uses full replanning — no incremental D* Lite.

## When It Breaks

**Rapid environment change exceeds replanning rate.** If obstacles appear and move faster than the replanning cycle completes, the plan is always stale. A drone flying through a flock of birds (20+ moving obstacles at 10 m/s) must react at the obstacle avoidance timescale (10–50 ms), not the planning timescale (100–500 ms). For very dynamic environments, planning gives way to reactive control entirely, with planning used only for high-level goal routing. The planning horizon shrinks to seconds rather than minutes.

**Premature commitment in narrow corridors.** If the robot commits to a corridor during execution, and a new obstacle appears at the far end of the corridor, the robot is now in a dead end — no room to turn around, obstacle ahead. D* Lite will correctly compute the new path (back out of corridor and take the other route), but the physical reversal may be infeasible if momentum is high or the corridor is too narrow to reverse in. Planning systems address this by maintaining a short-horizon "what if this turns out to be a dead end" escape path alongside the main plan.

## Transfer

- **Air traffic management**: aircraft file flight plans hours in advance. When weather, military airspace, or congestion invalidates a segment, air traffic control issues a "reroute" that modifies only the affected segment — exactly D* Lite's incremental repair. Full re-routing from scratch would produce inconsistent plans across connected airspace sectors.
- **Supply chain disruption recovery**: a logistics plan for shipping goods involves thousands of sequenced legs. When a port closes (analogous to an obstacle), only the plans that route through that port need replanning — logistics software replans the affected routes while the unaffected routes continue executing.
- **Autonomous vehicle lane changes**: a car following a highway plan detects a slow truck ahead. Rather than replanning the entire route, it plans a local lane change maneuver that reconnects to the existing global route — the same local patch + global reconnect pattern as D* Lite.

Exercises:

1. An A* search over a 200 × 200 grid produced a closed set of 15,000 cells. A new wall of 10 cells appears on the path. D* Lite needs to re-expand only cells whose g-values changed. If the wall creates a detour that raises g-values for 200 cells, what fraction of the full grid does D* Lite re-expand compared to starting from scratch?
2. A drone executes a 500 m path at 10 m/s. Full replanning takes 150 ms. During each replan, the drone flies on the old plan. A new obstacle at 50 m range appears when the drone is 100 m away. How far does the drone travel before the new plan is ready, and what is the remaining distance to the obstacle when the new plan takes effect?
3. Design a replanning policy for a drone that distinguishes between (a) an obstacle that blocks the planned path entirely, (b) an obstacle that reduces path margin below 3 m, and (c) an obstacle that appears behind the drone (already passed). What action should each trigger?

---

**Continue → [Why Following Isn't Understanding](44-why-following-isnt-understanding.md)**
