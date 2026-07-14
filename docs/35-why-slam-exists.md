# Why SLAM Exists

## The Problem

An autonomous vehicle is being deployed in a new city for the first time. No pre-built map exists. GPS is unavailable in the downtown canyon. The car must drive safely from the depot to the hotel — through streets it has never seen — and must know its position relative to obstacles well enough to stay in its lane.

Localization (chapter 34) requires a map to tell you where you are. Map building (chapter 32) requires knowing where you are to mark sensor readings in the right place. You have neither. You can't build a map without knowing your position. You can't find your position without a map.

This appears to be an irresolvable chicken-and-egg:

- No map → lidar readings can't be placed in a consistent coordinate frame
- No position → even correct landmark observations can't be accumulated correctly
- Errors compound: wrong position → wrong map → worse position estimates from wrong map
- And you can't go away and think about it — the car is moving now, other vehicles are present, decisions are needed in milliseconds

## What Would You Try?

- You start driving and the lidar sees a distinctive building corner. You don't know where you are, but you know the building corner is 12 m ahead at 30° left. What do you know relative to your *current* position, even without knowing your absolute position?
- After driving 50 m and turning, you see the same building corner again — now 18 m behind at 45° right. Without knowing your absolute position, can you determine how far you've traveled and in what direction?
- If you observed 10 such landmarks during the drive, and the observations from your current position are consistent with your observations from 50 m back, what does that tell you about your estimate of the 50 m trajectory?

## Failed Attempts

### Attempt 1: Build the map first, then localize

Send a survey vehicle with GPS through every street to build a centimeter-accurate map. Then deploy the autonomous vehicle and localize within it using lidar scan matching.

This works — it's what Waymo does in geofenced cities. It fails the stated problem: no pre-built map, new city, GPS unavailable. The survey approach requires weeks of data collection and GPS-quality positioning during the survey. If GPS is unavailable in the deployment zone, the survey fails too. And in rapidly changing environments (construction zones, disaster areas, unknown indoor spaces), no pre-built map exists or remains valid. Waymo's current geofenced approach explicitly doesn't handle the "deploy anywhere" scenario.

### Attempt 2: Localize from dead reckoning, build the map from the dead-reckoned trajectory

Use wheel odometry and IMU to estimate position. Place each lidar reading in the map based on the dead-reckoned position at that time. After driving the full route, you have a map of the environment built from your (approximate) trajectory.

The map will be wrong by exactly as much as dead reckoning drifts (chapter 33). After 1 km in a downtown canyon, the dead-reckoned position has drifted 5–10 m. The map has the same building placed 5 m from where it actually is. When the vehicle later tries to localize against this map, it encounters contradictions: the lidar sees the building at a position inconsistent with where the map says it should be. The localization fails.

Worse, the map error is highest at the end of the trajectory where you've traveled furthest. When the vehicle returns to the starting point, the map says "start position is over there" — 10 m from where it actually is. The start position is wrong because the map was built on a drifting trajectory.

### Attempt 3: Loop closure as a one-time correction

Drive the full route. When you return to a previously-seen location (loop closure), measure the position discrepancy between your dead-reckoned position and where you must actually be (since you recognize the landmark). Apply this as a single correction to the end of the trajectory.

Correcting only the endpoint is wrong. The trajectory error accumulated gradually over the entire loop. Shifting only the endpoint creates a "kink" in the trajectory — the path is now broken at the correction point. The landmarks placed from the last 20% of the trajectory (near the loop closure) are correctly corrected, but the landmarks from the middle of the trajectory still have the old errors. The map remains inconsistent.

And if there are multiple loop closures, each correction shifts a different endpoint. The corrections are mutually inconsistent: fixing loop closure A partially breaks the map near loop closure B.

## The Discovery

The three attempts fail because they treat position and map as separate estimates updated sequentially. Simultaneous Localization and Mapping recognizes that they are a **single joint state** and must be estimated together.

The insight: when you see a landmark, you learn something about the relationship between your position and the landmark's position — not about either individually. Call this a **constraint**. After driving 50 m and seeing the same landmark from a new angle, you have a second constraint. These two constraints together are stronger than either alone: they jointly constrain both your trajectory and the landmark's position.

Now imagine returning to a previously-visited location. You have a new constraint: your current position and your past position are related by a full loop. This loop closure constraint connects the end of your trajectory to the start. You can **distribute** the error correction across the entire trajectory, not just at the endpoint. Landmarks are repositioned consistently throughout the whole map.

This is **SLAM — Simultaneous Localization and Mapping**: maintain a joint probability distribution over robot trajectory and landmark positions. Add constraints as observations arrive. When a loop closure is detected, propagate the correction backward through the full trajectory via a least-squares adjustment or a factor graph. The result is a globally consistent map and a trajectory that is consistent with all observed constraints simultaneously.

The formal structure is a **pose graph**: nodes are robot poses at each timestep, edges are constraints (odometry between consecutive poses, landmark observations, loop closures). Optimization minimizes the total constraint violation across the graph. GraphSLAM and iSAM are the dominant modern algorithms.

## Try It

<iframe src="../assets/browser/chapter35/index.html" width="100%" height="460" style="border:1px solid var(--md-default-fg-color--lightest);border-radius:8px;"></iframe>

[open in a new tab](../assets/browser/chapter35/index.html)

Before changing anything, predict:

- Run with only dead reckoning (no SLAM). Drive a full loop back to start. How large is the map distortion at the endpoint compared to the start?
- Enable SLAM with loop closure detection. Drive the same loop. When the vehicle recognizes the starting landmark, watch what happens to the entire map — does the correction apply only at the endpoint, or does it ripple backward?
- Increase odometry noise. Does SLAM still produce a consistent map? At what noise level does SLAM fail to converge to a good map even with loop closures?

## Implementation

`browser/chapter35/index.html` implements a 2D pose graph SLAM. Each vehicle pose is a node; odometry edges connect consecutive nodes; loop closure edges connect poses that observe the same landmark. `browser/common/engine.js` runs Gauss-Newton minimization on the pose graph at each loop closure event. Watch the node positions shift during optimization — the global consistency update distributes loop closure correction across all nodes proportionally to edge strength, not just at the closure point. Compare the map before and after the first loop closure to see global consistency emerge.

## When It Breaks

**False positive loop closure.** If the SLAM system declares a loop closure when two different-but-similar locations are mistaken for the same place, it adds a wrong constraint to the pose graph. The optimizer then distorts the entire trajectory to satisfy this wrong constraint — the map is globally wrong in a way that looks consistent locally. In large-scale LiDAR SLAM, a false loop closure can "fold" an entire neighborhood onto itself, destroying the map. Place recognition algorithms use conservative thresholds and multi-stage verification precisely because a false positive is worse than a missed true positive.

**Dynamic environments break the static-world assumption.** SLAM assumes the world is static while the map is being built. In a busy street, parked cars become landmarks — then drive away. The map then has "ghost landmarks" at positions where cars used to be. The vehicle localizes partially against ghost landmarks, producing position errors that worsen as ghost density increases. Dynamic SLAM (tracking moving objects separately from static structure) is an active research area; no complete solution exists for dense urban environments with heavy traffic.

**Computational cost of large-scale optimization.** Pose graph optimization is O(n³) in the naive case for n nodes. A vehicle driving for 8 hours at 1 pose/second generates 28,800 nodes. Full graph optimization becomes too slow for real-time use. Incremental solvers (iSAM2) exploit the sparse structure of the pose graph — most nodes only connect to nearby nodes — to update only the affected subgraph after each new constraint, achieving near-real-time performance. But in very long missions (days, not hours), even incremental methods require periodic graph compression.

## Transfer

- **ORB-SLAM on smartphones**: modern AR frameworks (Apple ARKit, Google ARCore) run visual SLAM using the phone camera as the only sensor. As you walk around a room, the phone builds a sparse map of corner features and simultaneously estimates camera pose within it. Loop closure keeps the AR overlay from drifting when you walk a circle.
- **Underwater mapping**: AUVs (autonomous underwater vehicles) map the seafloor using sonar SLAM. GPS is unavailable underwater; dead reckoning drifts significantly over multi-hour dives. Loop closures occur when the AUV completes a survey lawnmower pattern and returns over previously-mapped terrain. The MBARI Monterey Canyon seafloor maps were built this way.
- **Space exploration**: NASA's Mars rovers use a visual odometry SLAM variant to navigate unknown terrain. The rover doesn't have a pre-built map of Martian rocks; it builds one in real time from stereo cameras, with loop closure occurring when it recognizes a distinctive rock formation from an earlier position.

Exercises:

1. A vehicle drives a 500 m square loop. Dead reckoning accumulates 10 m of total position error uniformly around the loop. At loop closure, SLAM distributes this error evenly across all 4 sides. What is the maximum map error at any point after the correction, compared to before?
2. A pose graph has 100 nodes connected in a chain (path) plus one loop-closure edge connecting node 1 to node 100. The loop closure measures that the vehicle is 5 m off from where dead reckoning says. In an optimal solution, which nodes change position most — those near node 1 and 100, those in the middle, or all equally?
3. A visual SLAM system mistakes corridor A for corridor B (false loop closure), adding a wrong constraint that says the vehicle is 30 m to the east of where it actually is. Describe what the optimized trajectory looks like and how a human would detect the error when inspecting the map.

---

**Continue → [Why Planning Is Hard](36-why-planning-is-hard.md)**
