# Why Following Isn't Understanding

## The Problem

A robotic warehouse arm has been trained by watching a human worker demonstrate the pick-and-place task 500 times. The robot records every joint angle, every velocity, every torque at 1 kHz. After training, it reproduces the demonstrated trajectory with millimeter accuracy in the training environment.

A new box arrives — 2 cm taller than the training examples. The robot reaches down, grabs 2 cm above the top of the box (where the training data said to go), and closes its gripper on air. The package falls.

The training data contained the answer for the training distribution. The task in deployment is outside the training distribution by 2 cm. The robot knew nothing about what it was doing — it was tracing a memorized curve through joint space.

Behavior cloning (recording and replaying demonstrations) fails in predictable ways:

- Trajectory memorization is distribution-specific — it works only near the training examples
- Small variations compound: errors early in the sequence shift the robot off the training trajectory, causing larger deviations later
- No representation of the goal — the robot can't adapt because it doesn't know what it's trying to achieve
- Human demonstrations encode task knowledge implicitly; the robot records kinematics, not intent

## What Would You Try?

- Instead of recording joint angles, what if you recorded the sequence of goals the human was pursuing? "Reach for the box," "grip firmly," "lift vertically," "place on conveyor." Could a robot use this description to handle a 2 cm taller box?
- When a human expert picks up an unusual box, they visually assess it and adjust their grip. What would the robot need to perceive and reason about to do the same?
- Behavior cloning compares what the robot does to what the human did. Could you instead compare what the robot achieves to what the human achieved — and correct based on the outcome rather than the motion?

## Failed Attempts

### Attempt 1: Collect more demonstrations covering more variations

Record 10,000 demonstrations spanning all box heights, widths, and orientations. The robot now has training data covering the 2 cm height variation — and the 5 cm one, and the 10 cm one.

This is dataset expansion, and it improves generalization within the covered range. It fails at the boundary: a box 1 cm outside the largest training example fails, as does a box in an unusual corner orientation not in the training set. The fundamental problem — the robot doesn't know what it's doing, only what shape of motion to reproduce — persists. Extrapolation beyond the training distribution degrades toward random behavior. And collecting 10,000 demonstrations is expensive; the same effort spent on understanding the task structure would generalize further.

### Attempt 2: Add error correction — DAgger (Dataset Aggregation)

Run the robot using the cloned policy. When it deviates from the intended behavior, a human corrects it and records the correction. Add the correction to the training set. Retrain. Repeat.

DAgger improves over pure behavior cloning because it specifically samples the robot's failure modes and adds recovery data. The robot learns to recover from errors, not just to reproduce the nominal trajectory. But it still fundamentally learns mappings from observations to motor commands without representing why. The recovering behavior is also a learned curve — one that works for the specific deviations encountered during training. A deviation pattern not seen during DAgger training still produces failure. DAgger is empirically better than plain cloning but has the same structural limitation.

### Attempt 3: Encode the goal as a reward signal and use reinforcement learning

Define a reward function (positive reward for successful placement, zero otherwise) and let the robot explore and learn from outcomes. With enough trials, RL will find a policy that achieves the reward reliably.

RL learns policies that achieve goals rather than policies that mimic demonstrations — a fundamental improvement. But it requires reward specification, which is hard. "Successful placement" sounds simple but edge cases proliferate: is 1 cm off center a success? What if the box lands but tips over 5 seconds later? Sparse rewards (only at the end of a successful trial) make credit assignment extremely hard — the robot doesn't know which part of its behavior caused the success. Dense reward shaping (partial credit for arm being near the box) introduces its own failures: the robot discovers reward-hacking behaviors (touching the box without gripping, tapping the conveyor). RL requires either a perfect reward function or extensive shaping work that itself encodes task knowledge.

## The Discovery

All three attempts are trying to teach the robot *what to do* in different ways. The deeper problem is that the robot has no representation of *what it is trying to achieve*. A human expert adjusts to the 2 cm tall box because they understand the goal: "get the box from A to B without dropping it." The adaptation is a consequence of pursuing the goal, not a memorized response to the height variation.

The insight: **separate the goal representation from the behavior policy**. If the robot explicitly represents the goal state (box at target position, upright, within tolerance), it can evaluate any trajectory against the goal and adjust. This is the architecture of model-based control: maintain a model of the task and the world, reason about how proposed actions affect goal achievement, and choose actions that improve goal achievement rather than that match a template.

For manipulation specifically, this leads to **task and motion planning (TAMP)**: represent the high-level task as a sequence of goals (grasp box → lift → move → place), plan motions that achieve each goal given the current perceived scene (which includes the actual box height), and adapt each motion to the current perception. The "understanding" is in the explicit goal representation, not in the memorized motion.

The formal principle: **imitation alone cannot learn the causal structure of a task**. Only a policy that reasons about goals can generalize to the goal's invariants — in this case, "box at target location" — rather than memorizing surface regularities of the demonstration.

## Try It

<iframe src="../assets/browser/chapter39/index.html" width="100%" height="460" style="border:1px solid var(--md-default-fg-color--lightest);border-radius:8px;"></iframe>

[open in a new tab](../assets/browser/chapter39/index.html)

Before changing anything, predict:

- Train behavior cloning on a robot navigating a fixed maze. Now shift the maze walls by 20 cm. Does the cloned policy succeed, partially succeed, or fail entirely?
- Compare a goal-directed policy (navigate to position X) versus a behavior-cloned policy on the same shifted maze. Which adapts, and by how much do outcomes differ?
- Increase the distribution shift (move walls progressively further from training). At what shift magnitude does behavior cloning catastrophically fail versus the goal-directed policy?

## Implementation

`browser/chapter39/index.html` runs two `Body` instances: `rA` (the path follower) replays fixed x-positions from `TRAIN_PATH = Array.from({length:300}, (_, i) => 20 + i * 0.9)` with no y-correction; `rB` (the goal-directed drone) uses `pidB = new PID(6, 0.05, 0.8, TRACK_Y)` to hold y regardless of disturbance. A `slopeForce` slider and `perturbTime` slider introduce a lateral force after a set number of ticks — the distribution shift. The follower drifts off-track; the PID-driven robot corrects. Both controllers are inline in the HTML; `browser/common/engine.js` provides `Body`, `PID`, and `drawBody`.

## When It Breaks

**Goal representation errors are silent.** A goal-directed system is only as good as its goal model. If the goal is defined as "gripper closes at height Z" but the real goal is "gripper securely holds object," a high-stiffness material that requires higher grip force than modeled causes the robot to think it achieved the goal while the object slips. Model-based goal achievement can fail just as silently as cloning — the robot is confident and wrong, just about its world model rather than its trajectory.

**Distribution shift is universal in the real world.** Even goal-directed systems fail when their world model is far from reality. A robot trained in simulation with perfect object geometry fails in the real world with imperfectly shaped objects. Sim-to-real transfer failures occur even in goal-directed systems that "understand" tasks — they understand them in the simulated world, which differs from the real world. The 2022 Boston Dynamics Atlas parkour demonstrations required months of sim-to-real tuning even though the robot's controller explicitly represented dynamic goals.

## Transfer

- **Language models and task understanding**: large language models trained on text generate plausible-sounding next tokens (behavior cloning on text). They fail systematic reasoning tasks (math, logic) because they mimic the surface form of correct answers rather than reasoning about goals. Chain-of-thought prompting forces explicit goal decomposition — the same principle as TAMP's goal hierarchy.
- **Autopilot systems in aviation**: early autopilots followed pre-programmed flight profiles (behavior cloning). Modern fly-by-wire systems maintain explicit goals (target altitude, speed, heading) and compute control inputs that achieve them given current state — goal-directed control. The 2009 Air France 447 accident involved pilots who had learned autopilot-following behaviors and struggled when the autopilot disengaged and they had to fly by goal-directed reasoning.
- **Surgical robot teleoperation vs. autonomy**: teleoperated surgical robots (da Vinci) record and replay the surgeon's motion — behavior cloning. Proposed autonomous surgical systems must instead plan to achieve tissue manipulation goals given variable anatomy — the structural difference between cloning and understanding.

Exercises:

1. A behavior-cloned robot makes a 0.5° heading error at each of 100 steps. Assuming errors accumulate without correction, what is the lateral deviation from the intended path after 100 steps of 0.1 m each?
2. A goal-directed robot is 2 m from the goal. At each step it computes heading toward the goal and moves 0.1 m. The environment shifts the goal 0.5 m sideways at step 10. How many additional steps does the robot take to reach the new goal position, compared to the behavior-cloned robot which continues on the old heading?
3. Describe a task (not pick-and-place) where behavior cloning would work reliably, and one where it would fail. What property of the first task makes cloning sufficient?

---

**Continue → [Why Robots Need Goals](40-why-robots-need-goals.md)**
