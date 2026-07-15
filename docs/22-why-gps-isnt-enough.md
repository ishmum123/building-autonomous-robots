# Why GPS Isn't Enough

## The Problem

You're programming a drone to fly a delivery route through a city: takeoff from a rooftop, navigate between buildings, land on a specific doorstep. You equip it with a GPS receiver. The GPS gives you position anywhere on Earth to within a few meters. Problem solved?

The drone departs. Flying in open air, everything works — GPS fixes at 10 Hz, position accurate to ±2 m, controller holds the route well. Then the drone enters a narrow street between two 20-story glass buildings.

The GPS continues to report fixes. The position jumps erratically — 8 m north, then suddenly 12 m east, then back. The drone, faithfully following GPS, veers into a wall. It's not a software bug. The GPS receiver is working exactly as designed.

Later analysis: the satellite signals were bouncing off the glass facades before reaching the antenna. The receiver saw multiple copies of the same signal, arriving at slightly different times via different reflection paths. Each copy computed to a slightly different position. The receiver averaged them into a wrong answer — confidently wrong.

In dense urban environments, any navigation system must:

- Detect when GPS position is unreliable, not just absent
- Continue operating when GPS signals are blocked (tunnels, underground parking, indoor)
- Update fast enough to control a vehicle moving at 5–10 m/s (GPS at 10 Hz gives position every 1 m of travel — too coarse for obstacle avoidance)
- Not use GPS-derived position directly for safety-critical decisions without verification

## What Would You Try?

- GPS tells you where you are, but with a delay and uncertain accuracy. Can you use the GPS position from 100 ms ago to control the drone right now? What goes wrong as speed increases?
- The drone is flying through a tunnel with no GPS signal. For how long can the IMU (accelerometer + gyroscope) provide useful position estimates? What happens after that?
- If GPS gives position every 100 ms but the attitude controller needs updates every 5 ms, how do you fill the gap?

## Failed Attempts

### Attempt 1: Rely entirely on GPS, trust all fixes

The GPS receiver reports position — use it directly in the control loop. If the GPS is wrong, the drone goes to the wrong place. Simple: GPS is generally reliable, so this should work most of the time.

"Most of the time" is not good enough when "the rest of the time" means flying into walls. In urban canyons, GPS multipath (signal reflection) can produce errors of 10–50 m while the receiver reports a valid fix with no flag indicating a problem. The receiver's internal quality metric (DOP — dilution of precision) may still look acceptable. The controller has no way to distinguish a good fix from a multipath-corrupted one.

Near tall buildings, GPS accuracy degrades to ±50 m in the worst cases while appearing to work. This isn't a GPS failure — it's GPS being used outside its design environment.

### Attempt 2: Use GPS only — but at high update rate

Consumer GPS updates at 1–10 Hz. Industrial GPS can update at 20–50 Hz, and RTK (real-time kinematic) GPS achieves centimeter accuracy at up to 20 Hz. Upgrade to RTK and the accuracy and update rate problems both go away.

RTK GPS requires a fixed base station within a few kilometers transmitting correction data. The correction link is a radio link — it can be blocked, have latency, or fail. Without the base station correction, RTK degrades to standard GPS accuracy. Near metal structures, RTK can still suffer multipath because the error source (reflections) is upstream of the correction system.

More fundamentally, RTK GPS is $500–$5,000 per unit. For a delivery drone that costs $800 total, equipping it with RTK is not economically viable. And RTK still provides no coverage underground or indoors.

### Attempt 3: GPS + radio beacon for indoor coverage

Install radio beacons at fixed locations throughout the delivery zone. The drone uses time-of-flight from known beacons to triangulate position indoors, switching from GPS outside to beacon-based positioning inside.

Infrastructure cost: each beacon installation requires power, weatherproofing, and precise survey of its position. Coverage requires overlapping beacon networks with no single-point failures. The system only works within the infrastructure envelope. Any building the drone needs to enter that isn't pre-equipped with beacons is inaccessible.

More critically: installing fixed infrastructure for every delivery location defeats the purpose of autonomous drones. A practical solution must work in places where no infrastructure was pre-installed.

## The Discovery

The failed attempts treat GPS as something to augment or replace. The real insight is subtler: GPS is valuable and should be used — but only for what it's actually good at.

GPS is good at: providing absolute position reference with low drift over long time periods (hours). It is bad at: high update rate, accuracy near reflective surfaces, coverage without sky view, robustness to single-point satellite failures.

IMU (accelerometers + gyroscopes) is good at: high-rate (1,000 Hz) relative motion tracking with excellent short-term accuracy. It is bad at: long-term accuracy (drift accumulates over minutes), absolute position reference.

These are complementary failure modes. The fix isn't to find a single sensor that does everything — it's to design a system that uses each sensor for exactly what it does well.

**GPS provides the long-term absolute reference** — correcting IMU drift every time a reliable fix is available.
**IMU provides the short-term, high-rate motion tracking** — filling in between GPS updates and bridging GPS outages.

During a GPS outage (tunnel, bridge underpass), the IMU takes over: the last known GPS position plus IMU-integrated displacement gives current position. After 10–30 seconds of IMU-only navigation, the error may be 1–3 m (acceptable for many applications). When GPS returns, it snaps the accumulated error back to ground truth.

This is **GPS/INS integration** — the standard architecture for aviation, autonomous vehicles, and precision agriculture. The GPS provides position but not velocity or short-term accuracy; the INS provides velocity, attitude, and high-rate updates. Together they provide continuous, accurate, robust navigation.

## Try It

<iframe src="../assets/browser/chapter22/index.html" width="100%" height="460" style="border:1px solid var(--md-default-fg-color--lightest);border-radius:8px;"></iframe>

[open in a new tab](../assets/browser/chapter22/index.html)

Before changing anything, predict:

- The drone enters a GPS-denied zone. How long before the IMU-only position estimate exceeds 1 m error? 5 m?
- Apply simulated GPS multipath (position jumps). Does the GPS-only controller follow the jumps? Does the GPS/IMS integrated controller? Why does it differ?
- Increase vehicle speed from 2 m/s to 10 m/s. How does this change the impact of GPS latency on control performance?

## Implementation

`browser/common/engine.js` provides `Body`, `GPS`, and `addNoise`. The `GPS` class adds Gaussian noise at a configurable `updateRate` and returns `null` on skipped frames; `browser/chapter22/index.html` calls `gps.read(drone)` and holds the last non-null fix as the GPS estimate. Dead-reckoning is inline: `drEstX += (drone.vel.x + imuBias) * 0.016`, accumulating bias each frame. The strip plot shows GPS error (staircase pattern between fixes) vs dead-reckoning error (linear drift), making the complementary failure modes visible without a separate multipath or coverage-map layer.

## When It Breaks

**GPS multipath in urban canyons.** Tall glass and metal buildings reflect satellite signals, causing the receiver to see the same satellite at multiple apparent positions. Modern GPS receivers use advanced signal processing to partially mitigate multipath, but dense urban environments (Manhattan, central Tokyo) still produce position errors of 5–20 m in the worst cases. Some cities have deployed ground-based augmentation systems (GBAS) to broadcast differential corrections that partially compensate.

**GPS jamming and spoofing.** GPS signals at the Earth's surface are extremely weak (−130 dBm). A cheap $30 GPS jammer (illegal in most countries but widely sold) can block GPS over a 100-meter radius. More dangerously, a spoofer can transmit fake GPS signals at higher power, causing receivers to compute a completely wrong position with no indication of the deception. Iranian forces captured a US RQ-170 surveillance drone in 2011 by allegedly spoofing its GPS — commanding it to land in Iranian territory while the drone's navigation believed it was landing at its home base.

## Transfer

- **Commercial aviation GPS/IRS integration**: all commercial aircraft use inertial reference systems (IRS) blended with GPS. The IRS handles short-term accuracy and attitude; GPS handles long-term position. During GPS outage, aircraft switch to IRS-only, which provides acceptable accuracy for trans-oceanic navigation for about 15–20 minutes before requiring another position fix (historically provided by star tracker or VOR).
- **Autonomous vehicles**: Tesla, Waymo, and others use GPS as one of many positioning inputs, blended with lidar map-matching, visual odometry, and wheel odometry. GPS alone doesn't have lane-level accuracy; map-matched lidar achieves ±10 cm in good conditions.
- **Search and rescue**: hikers in steep mountain valleys lose GPS lock when few satellites are visible above the horizon (poor geometric dilution of precision). Satellite messenger devices that rely purely on GPS can fail to report position in exactly the terrain where search and rescue is most needed.

Exercises:

1. A drone at 10 m/s uses GPS updating at 5 Hz. How far does the drone travel between GPS updates? At what speed does GPS-only position control become inadequate for a 1 m position accuracy requirement?
2. A GPS/IMU system has IMU drift of 0.1 m/s² bias and receives GPS corrections every 10 seconds. What is the maximum position error at the moment just before the next GPS correction arrives?
3. Explain why multipath errors are particularly problematic in urban canyons compared to open fields, using the geometry of satellite signal paths.

---

**Continue → [Why Sensors Disagree](23-why-sensors-disagree.md)**
