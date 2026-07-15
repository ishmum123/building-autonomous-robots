# Why Decisions Need Models

## The Problem

A drone is on a delivery mission: fly to building B, drop package, return to depot. Battery is at 55%. The depot is 4 minutes away; the delivery takes 2 minutes; return is 4 minutes. Total needed: 6 minutes. At 55%, the drone has approximately 8 minutes remaining — plenty.

Midway to the delivery, the drone enters a headwind. Battery drain rate jumps from 5% per minute to 9% per minute. Now it has 55 - (3 minutes × 9%) = 28% remaining at delivery. Return takes 4 minutes at 7% drain in tailwind. Required: 28%. It barely makes it back on fumes — with 0% to spare if the wind estimate is wrong.

A reactive controller sees: battery = 55%, current goal = deliver package. It has no information about what will happen to the battery over the next 6 minutes. It makes the right decision for the current moment, which is the wrong decision for the 6-minute mission.

Good decisions require looking ahead:

- The consequence of any action unfolds over time — next second, next minute, next flight leg
- Current sensor readings don't tell you future states; only a model does
- The right action now may depend entirely on what's expected to happen later
- Without a model, reactive control can be locally optimal and globally catastrophic

## What Would You Try?

- Before deciding whether to continue the delivery, what information would you need about the future? Could you compute that information from current sensor readings and a physics model?
- The wind model is uncertain — it might increase, decrease, or stay constant. How do you make a good decision when the future you're predicting is itself uncertain?
- "Continue if you can make it back" sounds like a simple rule. But "can make it back" requires knowing the return wind, return altitude profile, and future battery behavior — all of which require a model. What is the simplest model that captures the essential risk?

## Failed Attempts

### Attempt 1: Reactive threshold rules

Program conservative fixed rules: "abort mission if battery below 40%." This ensures the drone always has margin.

Fixed thresholds fail both ways. 40% in a strong headwind may be insufficient (the scenario above: needed 28%, had 28%, zero margin). 40% in a tailwind with short return may be excessive (abort a feasible mission unnecessarily). The optimal threshold depends on context — wind, distance, altitude, drone load — all of which vary. A fixed threshold is the wrong abstraction: it's a policy pretending to be a decision, ignoring all the contextual information that makes the threshold either too conservative or insufficient.

### Attempt 2: Greedy myopic optimization

At each step, choose the action that produces the best immediate outcome (maximum progress toward goal, minimum energy per meter). Never look ahead.

Greedy control is locally optimal. It fails when locally-optimal moves lead to bad global outcomes. Continuing delivery at maximum speed in a headwind minimizes time-to-delivery (greedy optimum) but maximizes battery drain rate, leaving less margin for return. The greedy controller never considers that the energy spent in the next 2 minutes determines whether it survives the 4 minutes after that. This is the standard failure of greedy algorithms: they optimize the first move without considering that the first move changes the options available for all subsequent moves.

### Attempt 3: Use a lookup table of pre-computed policies

Pre-compute the optimal action for every possible state (battery level, distance to goal, wind speed, distance to depot). Store in a table. At runtime, look up current state and execute.

This is the **value function / policy table** approach from dynamic programming — and it's formally correct. It breaks on state space size. The state space for this drone problem has: battery (100 levels) × distance to goal (500 levels) × wind speed (50 levels) × distance to depot (500 levels) × wind direction (36 levels) = 450,000,000 entries. With 4-byte floats, the table requires 1.8 GB of memory and takes days to compute. For higher-dimensional state spaces (full 3D position, velocity, attitude, wind vector), precomputed tables are computationally infeasible.

## The Discovery

Fixed thresholds ignore context. Greedy control ignores consequences. Full lookup tables are computationally intractable. All three fail to answer the core question: *what will happen if I take this action?*

The productive answer: use a **model** to simulate the consequences of candidate actions forward in time, evaluate the outcomes, and choose the action with the best predicted outcome. This is **Model Predictive Control (MPC)**: at each timestep, solve a finite-horizon optimization problem using a model of the dynamics.

For the drone:
1. **Model**: given current battery level B, speed v, wind w, predict B(t+Δt) = B - drain_rate(v, w) × Δt
2. **Horizon**: simulate 8 minutes ahead (delivery + return)
3. **Evaluate**: predict whether battery reaches zero before depot
4. **Decide**: if predicted return battery < 15% (safety margin), abort now; else continue

The model doesn't need to be perfect. A battery model accurate to ±20% is sufficient to distinguish "8 minutes of flight remaining" from "3 minutes remaining." Model accuracy must be commensurate with the decision quality required, not perfect.

MPC recomputes this optimization every second with updated sensor readings. If wind drops, the model updates, the prediction improves, and the decision reflects current conditions. If wind increases, the model catches it early and triggers abort before the battery reaches a critical level.

The formal name is **receding horizon control**: optimize over a fixed future window that "recedes" forward at each timestep, always planning over the same time horizon but with updated initial conditions.

## Try It

<iframe src="../assets/browser/chapter44/index.html" width="100%" height="460" style="border:1px solid var(--md-default-fg-color--lightest);border-radius:8px;"></iframe>

[open in a new tab](../assets/browser/chapter44/index.html)

Before changing anything, predict:

- Fly with reactive control in a headwind that builds gradually. At what battery level does the reactive controller abort — and does the drone make it back safely?
- Enable MPC. In the same headwind scenario, at what battery level and physical location does MPC trigger the abort? Is it earlier or later than reactive control?
- Set wind prediction to very uncertain (wide error bars on wind model). Does MPC become more or less conservative? Does it ever fail to abort when it should?

## Implementation

`browser/chapter44/index.html` runs `qA` (reactive) and `qB` (model-based) as `Quadcopter` instances. The reactive drone uses bang-bang logic — `thrust = distToGnd < reactThresh ? high : low` — controlled by `altPidA = new PID(2.0, 0.02, 0.5, TARGET_Y)`; the model-based drone uses the smoother `altPidB = new PID(4.0, 0.05, 1.2, TARGET_Y)`. A `modelHorizon` slider is present in the UI but does not drive any sim logic. The sim simplifies the model-based concept to PID tuning versus bang-bang — enough to show that anticipating dynamics produces smoother descent. `browser/common/engine.js` provides `Quadcopter` and `PID`.

## When It Breaks

**Model error causes overconfident decisions.** MPC trusts its model. If the battery model underestimates drain at low temperature (cold batteries have lower capacity), MPC predicts adequate return margin but the drone lands short. The solution is to include uncertainty in the model — robust MPC optimizes over the worst-case model realization within an uncertainty set, guaranteeing safety even when the model is wrong by a known amount. But robust MPC is more conservative and can become infeasible if the uncertainty set is too large.

**Short prediction horizon misses slow-building problems.** If MPC's horizon is 2 minutes and the mission is 10 minutes, it can't predict that the tailwind on the outbound leg will be a headwind on the return. The model looks fine for the first 2 minutes, so MPC continues. This is why horizon length must be commensurate with the task timescale. In practice, MPC users must think carefully about what can go wrong beyond the prediction window — and handle it with separate constraints or safety margins that don't depend on the model.

## Transfer

- **Self-driving car trajectory prediction**: autonomous vehicles run a short-horizon MPC every 50 ms to predict the motion of surrounding vehicles over the next 3 seconds and choose a safe trajectory. The "model" is a constant-velocity prediction for other vehicles; control updates are fast enough to recover from model errors. Waymo and Cruise's trajectory planners are MPC variants.
- **Chemical process control**: MPC was developed in the 1970s for chemical plant control (distillation columns, reactors) where process dynamics are slow, models are available from first principles, and the cost of suboptimal control is lost product or safety violations. Shell's IDCOM and DMC systems, deployed in refineries from 1974, are the earliest large-scale MPC deployments.
- **Sports strategy under uncertainty**: a tennis player choosing whether to serve aggressively (higher ace rate, higher fault rate) or conservatively (lower fault rate, easier to return) is running a mental MPC: model the opponent's return probability under each strategy, predict outcomes over the set, choose strategy that maximizes expected games won. The "model" is their knowledge of the opponent.

Exercises:

1. A drone's battery is at 60%. Wind model predicts 8% per minute drain for 3 minutes to delivery, then 5% per minute for 4 minutes on return. Predict the battery level at delivery and at depot return. What is the safety margin?
2. The wind model is uncertain: drain rate is 8% ± 2% per minute (uniform distribution). Compute the worst-case battery at return under the worst wind (10% drain rate throughout). Is the mission safe under worst-case?
3. MPC runs at 1 Hz with a 2-minute horizon and each forward simulation takes 20 ms. How many forward simulations run per second? What fraction of compute budget does MPC consume, and what constraint does this place on the simulation complexity?

---

**Continue → [Why Autonomous Drones Work](45-why-autonomous-drones-work.md)**
