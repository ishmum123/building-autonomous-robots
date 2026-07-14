# Why State Matters

## The Problem

Two identical drones receive the same sensor reading: altitude = 50 m, airspeed = 10 m/s, battery = 40%. They should do different things.

Drone A is descending through 50 m toward a landing pad on a 2% battery decline rate. At the current rate, it has 8 minutes of flight time remaining. The landing pad is 90 seconds away. The right action: continue descent on the current approach.

Drone B is at 50 m on a delivery mission 6 minutes flight time from the depot. At 40% battery and a 4% per-minute consumption rate (it's fighting headwind), it has 10 minutes remaining — barely enough to complete the delivery and return. A wind gust has raised consumption. The right action: abort delivery and return to depot immediately.

Identical sensor readings. Opposite correct actions. The sensor reading is the same; the **state** is not. State includes everything the robot needs to know to choose the right action — including history, context, and information that sensors can't directly observe.

Without state representation:

- Two situations that look identical receive identical responses — which is wrong when the situations differ in history or context
- The robot can't reason about future consequences of current actions
- Every control decision is a pure reflex: input → output, with no memory of anything before
- Hidden variables (battery drain rate, mission phase, accumulated positional drift) are invisible to a stateless controller

## What Would You Try?

- What information, beyond current sensor readings, would you need to make the right decision for both drones above? Is that information directly observable, or must it be inferred?
- If you can't observe the battery drain *rate* directly (only current level), how would you estimate it? What inputs would you need and over what time window?
- A drone enters a tunnel where GPS fails. The tunnel exit is 200 m ahead. While in the tunnel, what state must the drone maintain to know where it is when GPS resumes?

## Failed Attempts

### Attempt 1: Memoryless reactive control (pure reflex)

The controller maps sensor readings directly to motor commands with no internal state. At each timestep: read sensors, compute action, execute.

This works for simple stabilization tasks: a hovering drone needs only current IMU readings to compute stabilizing motor commands. It fails for any task with temporal structure. "Land when battery is low" requires knowing the drain rate, which requires memory of past readings. "Return to base if delivery takes more than 10 minutes" requires knowing when the delivery started. "Don't fly the same route twice if it was blocked before" requires memory of past routes. All of these require state. A memoryless controller can't implement them — it has no yesterday.

### Attempt 2: Log sensor readings and search history when needed

Don't maintain a running state estimate. Instead, store all sensor readings in a log. When a decision needs historical context, search the log.

This is functionally equivalent to maintaining state, but computationally worse: searching a growing log for the last GPS fix, or the mission start time, or the maximum altitude reached, is O(log length) each time. And many state variables are implicit in the raw sensor log — battery drain rate requires subtracting two readings and dividing by the time elapsed, which isn't directly stored. Deriving battery drain rate from a log of 10,000 readings requires a full scan. Real-time control can't afford this latency. The log is also infinite — sensors produce data at 1 kHz; after 10 minutes, the log has 600,000 entries per sensor. State is the efficient summary of the log that preserves all decision-relevant information.

### Attempt 3: Use a finite state machine (FSM) with fixed states

Define the robot's state as one of a fixed set: IDLE, TAKING_OFF, CRUISING, APPROACHING, LANDING, EMERGENCY. Transitions between states are triggered by sensor thresholds. Each state has a fixed control law.

FSMs work for simple sequential tasks. They fail when the "same" state has different correct behaviors depending on history. Both drones in the problem above are in the CRUISING state — same FSM state, different correct actions. The FSM can't represent the difference because both drones are at altitude, moving forward, with 40% battery. The FSM has no representation of *how the drone got to 40% battery* or *what phase of mission* is underway. Extending the FSM adds states (CRUISING_OUTBOUND, CRUISING_RETURN, CRUISING_HEADWIND) but the number of states needed grows combinatorially with the number of distinguishable contexts.

## The Discovery

The three approaches fail because they try to avoid the cost of maintaining state — either by being stateless, by deferring to a log, or by pre-enumerating a fixed set of states. All three encounter the same wall: the robot needs context that a raw sensor reading can't provide.

The insight: define **state** formally as the minimal summary of all past inputs that is sufficient to predict the optimal future action. This is the Markov property: given the state, the future is independent of the past. The state is not the same as the sensor reading — it's a derived representation that captures what matters.

For the drone problem, the state includes: current position, velocity, attitude, battery level, battery drain rate (derived from history), mission phase (outbound/return), time since mission start, and accumulated dead reckoning uncertainty. None of these is directly observable from a single sensor reading. Together they determine the correct action.

State is maintained by a **state estimator** running continuously: at each timestep, the estimator takes the current sensor readings and the previous state and produces an updated state. The Kalman filter (chapter 25) is the canonical state estimator for continuous dynamics. For discrete mission context (outbound/return, phase), a simple counter or timer suffices. The full robot state is the combination: continuous estimated state plus discrete mission context.

**State space** — the set of all possible states — is what the planner operates in, not sensor space. An action is chosen based on the current state. Two situations with the same sensor reading but different states receive different actions. This is the right architecture.

## Try It

<iframe src="../assets/browser/chapter42/index.html" width="100%" height="460" style="border:1px solid var(--md-default-fg-color--lightest);border-radius:8px;"></iframe>

[open in a new tab](../assets/browser/chapter42/index.html)

Before changing anything, predict:

- Run the memoryless controller with two drones at identical current sensor readings but different histories. Do they make the same decision? Is that decision correct for both?
- Enable the state estimator with derived variables (drain rate, mission phase). Do the two drones now make different decisions? What specific state variable distinguishes them?
- Corrupt the state estimator (add noise to drain rate estimate). At what error level does the "abort delivery" decision trigger at the wrong time?

## Implementation

`browser/chapter42/index.html` simulates two drones with identical current sensor readings but different histories, comparing a memoryless reactive controller versus a state-aware controller. `browser/common/engine.js` maintains a rolling window of sensor history to compute derived state variables (drain rate = Δbattery / Δtime over last 60 seconds; mission elapsed time; phase flag). The control law reads from the full state vector; watch the decision diverge between drones even as their instantaneous sensor readings remain identical.

## When It Breaks

**State estimation lag hides real-time changes.** Battery drain rate computed over a 60-second window is slow to respond to sudden load changes: a motor failure doubles drain rate instantaneously, but the 60-second estimate changes slowly. For fast-changing state variables, the estimation window must be short (at the cost of noise) or the system must also monitor instantaneous anomalies. Combining short-window anomaly detection with long-window average estimation covers both: catch sudden changes and track trends.

**Infinite state spaces require approximation.** If the state includes the full history of all sensor readings (relevant for some sequential decision problems), the state space is infinite. Practical systems bound state history by a fixed window or summarize it with a finite-dimensional vector (e.g., a learned encoder in neural network-based controllers). The approximation introduces error: the summarized state may not preserve all decision-relevant information. Designing state representations that are both compact and sufficient is one of the central challenges of robot learning.

## Transfer

- **Air traffic control radar returns**: an aircraft transponder sends altitude and speed — the same reading two aircraft can share. ATC distinguishes them by a squawk code (identity state), filed flight plan (mission state), and history of previous transmissions (trajectory state). Without state, identical transponder readings would be indistinguishable.
- **Medical ICU monitoring**: a patient's blood pressure reading of 90/60 is a medical emergency in a post-surgery patient who started at 120/80 (state change) but may be normal for a patient whose baseline is 90/60 (state context). ICU alarms that trigger on absolute values rather than delta from baseline produce false alarms. State-aware monitoring uses the patient's history.
- **Financial fraud detection**: a transaction of $1,000 is suspicious in an account normally transacting $50, but normal for an account regularly transacting $10,000. Fraud detection systems maintain customer state (spending history, geographic pattern) and classify transactions relative to that state — stateless absolute-threshold rules produce too many false positives.

Exercises:

1. A drone's battery reads 40% at t=10 min and 28% at t=16 min. Compute the drain rate in % per minute. At this rate, how many minutes of flight remain? What is the point-of-no-return distance if the drone travels at 10 m/s and the depot is at the starting point?
2. An FSM for drone delivery needs to distinguish: mission phase (outbound/return), weather condition (calm/windy), and battery state (high/medium/low). How many FSM states are needed to represent all combinations? If you add a fourth dimension (GPS quality: good/degraded), how does the state count change?
3. The Markov property says: given the current state, past observations carry no additional information for future decisions. Give an example where this is approximately true for a flying drone and one where it is false (where knowing a longer history would change the optimal decision).

---

**Continue → [Why Estimation Beats Measurement](43-why-estimation-beats-measurement.md)**
