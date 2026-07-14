# Why Robots Need Senses

## The Problem

You have a robot arm that packages goods on an assembly line. You program it precisely: reach 30 cm forward, rotate wrist 90°, close gripper, retract. The arm is powered by stepper motors — each step command corresponds to exactly 1.8° of rotation. You've calculated exactly how many steps equal 30 cm extension and 90° rotation. The program runs perfectly in testing.

Day one in production: the arm misses the package 20% of the time. By end of shift, it's missing 60% of the time. The arm has slowly accumulated a small positional error — maybe 0.3° per joint per hour of operation due to motor heating, belt stretch, and vibration. Over 8 hours and thousands of cycles, 0.3° per joint becomes 3°. Multiply across the arm's four joints and the gripper is off by several centimeters. Packages fall, the line stops.

You could recalibrate every hour. But the robot runs 24/7, three shifts. Recalibration means stopping production. A more fundamental problem: you've built a robot that has no idea where it actually is.

Any autonomous robot must:

- Know its own state (position, orientation, velocity) at all times, not just at startup
- Detect when the world has changed — objects moved, obstacles appeared, targets shifted
- Close the loop between commanded action and actual result — verify the command had the intended effect
- Recover from cumulative errors that any physical system accumulates over time

## What Would You Try?

- You know exactly how many steps you've sent each motor. Shouldn't that tell you exactly where the arm is? What can make that calculation wrong over time?
- A blind person walking through a known building can navigate fairly well, but eventually bumps into a chair that was moved. What does this tell you about the limits of memory versus real-time sensing?
- If you had a camera watching the arm, what information could you extract that the motor commands alone couldn't tell you?

## Failed Attempts

### Attempt 1: Perfect calibration — measure everything upfront

Before deployment, characterize every source of error. Measure the exact distance-per-step for each motor under load. Map the thermal expansion coefficients of the arm linkages. Model belt stretch as a function of force. Pre-load all this into a lookup table and apply corrections automatically.

This works initially. The calibration table reduces errors from 3 cm to 0.5 cm over an 8-hour shift. But the calibration was made with new belts. After 2 weeks, the belts have stretched further. After a month, a joint bearing wears slightly, introducing a new backlash of 0.4 mm. After 3 months, a technician replaces one motor with a slightly different model — same specs on paper, different actual step size. Each change silently breaks the calibration. The table doesn't know it's wrong.

Physical systems change. The calibration that was perfect last week is wrong today. A model of the machine is not the machine.

### Attempt 2: Dead reckoning — integrate commands over time

Track position by summing every commanded move. If you commanded "move 30 cm forward," update your internal position by +30 cm. This is standard in stepper-motor CNC machines and works well for short sequences.

Run the packaging arm through 10,000 cycles. Stepper motors can miss steps under load — a heavy package creates more torque than expected and the motor skips one step. The dead-reckoning position says "30.000 cm" but the actual position is 29.982 cm. After 10,000 cycles with occasional skipped steps, the accumulated error is 2 cm. The robot is confidently executing commands based on a position that's 2 cm off — and it has no mechanism to discover this.

Dead reckoning errors compound monotonically. There's no correction signal because the system never checks whether commanded moves actually happened.

### Attempt 3: Mechanical hard stops for homing

Allow error to accumulate during operation, but periodically drive the arm against a fixed mechanical stop to reset position. The stop is at a known location; touching it resets the position counter to zero. This is called homing.

A CNC router does this every startup. It works. But the packaging arm runs 24/7 — homing requires stopping operation and taking the arm off-task. Homing every hour means roughly 5% downtime. On a high-volume line, 5% downtime is hundreds of thousands of dollars per year.

More fundamentally, homing only resets position — it doesn't tell you about obstacles, misaligned packages, or changed environmental conditions. A homed arm with perfect position tracking still can't detect that someone placed a foreign object in the workspace.

## The Discovery

Each approach treated the robot's position as something you *calculate* from commands. But position — like all physical quantities — is something you *measure* from the world.

The failed attempts shared a common premise: that commanding an action reliably produces that action. They fail because that premise is false in physics. Thermal expansion, wear, missed steps, belt stretch, vibration — all are ways the world deviates from the command. A system that only sends commands and never checks results is open-loop: it cannot know what it achieved.

The solution is to add **sensors** that read the world directly, not through the filtered lens of "I commanded X, therefore X happened."

An encoder on each joint reads actual joint angle — regardless of what was commanded. A force sensor in the gripper detects whether the package was actually gripped or whether the fingers closed on air. A vision system verifies the arm is at the expected position in 3D space. These sensors don't rely on the command history — they read the current physical reality.

With sensors, the controller closes a loop: command a move → measure the result → compute the error → correct. The correction can happen at millisecond timescales, before errors accumulate. And sensors can detect things no command model anticipates: a package shifted on the belt, an unexpected obstacle, a joint that's binding.

Sensors don't eliminate the need for good control logic. But they make the controller's world model accurate — and without accuracy, no amount of control logic can compensate.

## Try It

<iframe src="../assets/browser/chapter19/index.html" width="100%" height="460" style="border:1px solid var(--md-default-fg-color--lightest);border-radius:8px;"></iframe>

[open in a new tab](../assets/browser/chapter19/index.html)

Before changing anything, predict:

- The simulation shows a robot navigating a corridor with and without sensing. At what point in the open-loop run does the error become critical?
- Add sensor noise to the sensing mode. How much noise can the sensing mode tolerate before it performs similarly to open-loop?
- An obstacle appears midway through the run. Which mode detects it? Which mode can avoid it?

## Implementation

`browser/common/engine.js` maintains a ground-truth state (actual position, orientation) separate from the commanded state (integrated motor commands). In open-loop mode, the robot uses only commanded state. In sensing mode, the robot reads from the ground-truth state with optional noise. `browser/chapter19/index.html` overlays both trajectories to make the divergence visible.

## When It Breaks

**Sensor failure silently reverts to open-loop.** A robot that uses sensor data gracefully degrades if the sensor fails — but only if it knows the sensor has failed. An encoder that reads a fixed value after its cable is pinched looks like a working encoder reporting no motion. The robot now has wrong sensor data, which is worse than no sensor data. Real systems implement sensor health monitoring: if an encoder reads zero velocity while a large current flows, the sensor may be failed. Fault detection is as important as the sensing itself.

**Sensing latency causes oscillation.** A camera-based vision system for position feedback might have 50–100 ms of latency (capture → processing → position estimate). Feeding this delayed measurement into a fast control loop is like driving a car using a rearview mirror: the correction is based on where you were, not where you are. Latency-induced phase lag can cause the control loop to oscillate at the latency frequency. Vision-servo systems spend significant engineering effort reducing and compensating for pipeline latency.

## Transfer

- **Surgical robots**: da Vinci and similar systems use force sensors on the instrument tips to give the surgeon haptic feedback — without it, surgeons have accidentally torn tissue they couldn't feel through the rigid linkage. Sensing closes the force loop that direct manipulation provides naturally.
- **Self-driving cars**: a car with GPS-only navigation has no awareness of lane markings, pedestrians, or stopped vehicles. Camera and lidar sensors provide the real-time world model that pre-built maps cannot.
- **Human balance**: proprioceptive sensors (muscle spindles, joint position sensors) give your nervous system continuous real-time joint angle data. Neuropathy that destroys these sensors causes severe gait instability even in people with intact motor function — the commands go out but nothing confirms they worked.

Exercises:

1. A stepper motor arm runs 5,000 cycles per shift. Each cycle has a 0.01% probability of skipping one step (each step = 0.02 mm). After one shift, what is the expected accumulated position error? After one week of three shifts?
2. An encoder reads actual joint angle with ±0.1° noise. A motor command model predicts joint angle with ±0.5° drift per 1,000 cycles. After 10,000 cycles with feedback, what is the expected position error? Without feedback?
3. Describe two distinct scenarios where a robot with sensors fails while a robot without sensors would succeed.

---

**Continue → [Why Accelerometers Lie](20-why-accelerometers-lie.md)**
