# Why A* Works

## The Problem

A delivery drone must fly from its depot on the east side of the city to a rooftop on the west side. The city map is a 500 × 500 grid of 5 m cells — 250,000 cells. Some cells are occupied by buildings. The drone needs the shortest path in under 50 ms so it can replan frequently.

Checking every cell (BFS): 250,000 expansions in the worst case. BFS processes them in distance order from the start — it expands a full circle that grows outward, even in directions pointing away from the goal. When the goal is in the northwest corner and the drone is in the southeast, BFS spends most of its time expanding cells to the south and east — away from where the goal is.

Dijkstra's algorithm (weighted BFS) has the same problem: it processes cells in order of cost from start, which is distance from start, not progress toward goal. A 500 × 500 grid with the goal far from start can require expanding 200,000+ cells before reaching it. At 250,000 cells, even fast computers take hundreds of milliseconds.

The fundamental waste:

- BFS/Dijkstra don't use any information about where the goal is
- They expand cells based entirely on past cost (from start)
- Cells far from the goal in the wrong direction are expanded as eagerly as cells near the goal
- Search time scales with the explored area, not path length

## What Would You Try?

- You know the goal is to the northwest. Before expanding any cell, which cells are most likely to be on the shortest path? Could you prioritize expanding those first?
- Euclidean distance to the goal is easy to compute for any cell. Can you use this as a guide for which cell to expand next? What might go wrong with this guide?
- Greedy best-first search always expands the cell with smallest straight-line distance to goal. Is the path it finds guaranteed to be shortest? What kind of maze would break it?

## Failed Attempts

### Attempt 1: Breadth-first search (BFS) — explore everything uniformly

Expand cells in FIFO order from the start. The first path that reaches the goal is guaranteed to be shortest (in unweighted grids).

BFS finds the optimal path but explores a circle that grows in all directions, including directly away from the goal. On a 500 × 500 grid with start at (500, 0) and goal at (0, 500), BFS expands roughly half the grid before reaching the goal. When the path is 700 cells long, BFS expands ~100,000 cells. A* on the same grid expands roughly 1,000. The ratio gets worse as the grid gets larger. BFS is optimal but not efficient.

### Attempt 2: Greedy best-first search — always expand toward the goal

Priority queue ordered by h(n) = straight-line distance to goal. Always expand the cell closest to the goal (ignoring how expensive it was to get there).

Greedy best-first search is fast when the path is clear and roughly straight. It fails at mazes. Consider a U-shaped barrier between start and goal: greedy search drives straight toward the gap, reaches the near side of the U, and then the cells with smallest h(n) are inside the U — far from the goal in straight-line terms. The algorithm searches the entire interior of the U before backtracking. Worse, if the optimal path requires going away from the goal to reach a gap in the wall (detour), greedy search may never find it — it always prefers moving toward the goal, even when the right move is temporarily away.

Greedy best-first is fast but not optimal and not even complete in some graphs.

### Attempt 3: Weighted BFS with a bad heuristic

Use a heuristic h(n) that overestimates the true distance to goal — for example, h(n) = 2 × Euclidean distance. This is an **inadmissible** heuristic. The priority queue now orders cells by g(n) + h(n) where h overestimates.

The search runs fast because the overestimate strongly biases expansion toward the goal. But it may skip the optimal path. Specifically: if the true shortest path goes 10 steps north before heading west, but a longer path going directly west has lower g + 2h scores along its route, the algorithm commits to the longer direct path without ever considering the northern detour. The result is a suboptimal path that's returned as if it were optimal. If the system announces "minimum-cost route found" but the path is actually 15% longer than optimal, and this feeds into fuel calculations, the drone runs short.

An inadmissible heuristic breaks the optimality guarantee without indicating that it has done so.

## The Discovery

BFS wastes effort exploring away from the goal. Greedy search finds bad paths because it ignores sunk cost. A bad heuristic produces wrong answers silently.

The insight that resolves all three: combine both costs explicitly. For each cell n, compute:

- **g(n)**: true cost from start to n (what we know)
- **h(n)**: estimated cost from n to goal (what we guess)
- **f(n) = g(n) + h(n)**: estimated total cost of a path through n

Expand cells in order of increasing f(n). This balances past cost (g) with future estimate (h). Cells that are cheap to reach *and* close to the goal get expanded first. Cells that are cheap to reach but far from goal wait; cells close to goal but expensive to reach also wait.

The key constraint: h(n) must be **admissible** — it must never overestimate the true remaining cost. On a 4-connected grid (moves up, down, left, right), Manhattan distance |Δx| + |Δy| is admissible — and it is the tight choice, since no path can beat it. Euclidean straight-line distance is also admissible (it never overestimates), just looser on such a grid; the simulation uses Manhattan. With an admissible heuristic, A* is guaranteed to find the optimal path while expanding far fewer cells than BFS.

**Why A* is optimal with admissible h**: when A* expands the goal node, f(goal) = g(goal) + 0 = actual path cost. If any other path existed with lower cost, some node on that path would have lower f than g(goal) and would have been expanded first — contradiction. The admissibility constraint ensures no cheaper path exists unchecked.

In practice: on the 500 × 500 grid, A* with an admissible heuristic typically expands 1–5% of cells that BFS expands. The speedup grows with grid size and heuristic quality.

## Try It

<iframe src="../assets/browser/chapter37/index.html" width="100%" height="460" style="border:1px solid var(--md-default-fg-color--lightest);border-radius:8px;"></iframe>

[open in a new tab](../assets/browser/chapter37/index.html)

Before changing anything, predict:

- Watch BFS expand cells outward from the start. How many cells does it expand before reaching the goal in an open grid versus a maze? Compare to A*.
- Place a U-shaped obstacle. Which algorithm gets trapped in the U and how does it recover?
- Set the heuristic weight to 2.0 (inadmissible). Does the path change? Is the inadmissible path shorter, longer, or the same as the admissible one?

## Implementation

`browser/chapter37/index.html` defines both search algorithms inline: `bfsSearch` (lines 27–47) and `astarTracked` (lines 50–74). Both call `grid.neighbors(cur)` and `grid.heuristic(nb, goal)` from `browser/common/engine.js`; engine's `astar` is not used. Expanded cells are shaded blue on each side, and a `saving %` metric shows how many fewer cells A* expands than BFS. The `wallCol` slider adjusts the obstacle column. No greedy best-first variant is present — the comparison is BFS versus A*.

## When It Breaks

**Inadmissible heuristic trades optimality for speed.** Weighted A* uses h'(n) = w × h(n) with w > 1. This is inadmissible but finds paths faster. The guarantee weakens: the path is at most w times the optimal cost. For a drone in time-critical replanning (chapter 38), a 10% longer path found in 5 ms beats the optimal path found in 200 ms. Weighted A* is widely used in practice, but the bound w must be chosen knowing the acceptable suboptimality.

**Memory exhaustion on large maps.** A* stores all generated nodes in memory (open set + closed set). For a 10,000 × 10,000 outdoor map at 1 m resolution, A* can generate 10⁸ nodes — gigabytes of memory. IDA* (iterative deepening A*) uses O(path length) memory by re-expanding nodes at increasing f-cost bounds, at the cost of redundant computation. Memory-constrained planning on large outdoor maps is an active engineering tradeoff.

## Transfer

- **GPS turn-by-turn navigation**: Google Maps and Waze use A* variants (with road distance heuristics) on continental road networks with tens of millions of nodes. The heuristic is straight-line driving distance; preprocessing techniques like contraction hierarchies reduce search time to under 1 ms for cross-country routes.
- **Protein folding structure prediction**: AlphaFold's early predecessors used heuristic search to find low-energy protein conformations — each conformation is a node, energy is the cost, and the heuristic estimates remaining folding energy. The problem is higher-dimensional but the search structure is the same.
- **Puzzle solving (15-puzzle, Rubik's cube)**: IDA* with pattern database heuristics is the basis for optimal puzzle solvers. A Rubik's cube has 4.3 × 10¹⁹ states — only a strong heuristic makes optimal solution tractable.

Exercises:

1. On an 8-connected grid (diagonal moves allowed), the admissible heuristic is the Chebyshev distance: max(|Δx|, |Δy|). A cell is at (3, 7) and the goal is at (10, 2). Compute h (Chebyshev), g (assume 8 steps traveled), and f.
2. A* expands cells in f-order. Two cells have f = 15: cell A has g = 5, h = 10; cell B has g = 12, h = 3. Which cell is closer to the goal? Which cell was cheaper to reach? Which should A* expand first if there's a tie — and does the tie-breaking rule affect optimality?
3. A 1000 × 1000 grid with the goal in the corner. BFS expands 400,000 cells; A* with Euclidean heuristic expands 8,000. If each expansion takes 2 µs, compute planning time for each. What speedup factor does A* achieve, and how does this scale if you double the grid to 2000 × 2000?

---

**Continue → [Why Robots Change Their Mind](38-why-robots-change-their-mind.md)**
