#!/usr/bin/env python3
"""Generate browser/chapterXX/index.html simulations from JS snippets."""

from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BROWSER_ROOT = ROOT / "browser"
COMMON_ENGINE = BROWSER_ROOT / "common" / "engine.js"

CHAPTERS = [
    {"num": 1, "title": "Why Wheels Move", "key": "A wheel only moves when a force, friction, and a constraint work together."},
    {"num": 2, "title": "Why Things Refuse to Move", "key": "Objects resist changes in velocity. This property is called inertia."},
    {"num": 3, "title": "Why Magnets Pull", "key": "A magnetic field transfers force across a distance."},
    {"num": 4, "title": "Why Electricity Can Push", "key": "A current in a magnetic field experiences a mechanical force."},
    {"num": 5, "title": "Why Copper Becomes a Magnet", "key": "Electric current creates a magnetic field."},
    {"num": 6, "title": "Why Motors Spin", "key": "A motor switches current at the right moment to keep turning."},
    {"num": 7, "title": "Why Motors Stop", "key": "Friction and back-electromotive force oppose rotation."},
    {"num": 8, "title": "Why Brushes Had to Disappear", "key": "Electronic switching can replace mechanical brushes."},
    {"num": 9, "title": "Why Three Wires Are Better Than Two", "key": "Three phased currents create a continuously rotating magnetic field."},
    {"num": 10, "title": "Why Motors Need Conductors", "key": "Conductors shape where current flows and therefore where force is produced."},
    {"num": 11, "title": "Why Faster Isn't Better", "key": "Aggressive control causes overshoot and oscillation."},
    {"num": 12, "title": "Why Everything Oscillates", "key": "Energy trades between storage and motion, producing oscillation."},
    {"num": 13, "title": "Why Feedback Changes Everything", "key": "Feedback compares goal to reality and corrects the difference."},
    {"num": 14, "title": "Why Guessing Isn't Control", "key": "Without measurement, a controller cannot correct disturbances."},
    {"num": 15, "title": "Why Errors Accumulate", "key": "Errors integrate over time, so a controller must remove steady bias."},
    {"num": 16, "title": "Why PID Was Invented", "key": "PID blends proportional, integral, and derivative responses."},
    {"num": 17, "title": "Why One PID Isn't Enough", "key": "Nested controllers handle different time scales and variables."},
    {"num": 18, "title": "Why Quadcopters Need Two Brains", "key": "Attitude control and position control are separate but coupled loops."},
    {"num": 19, "title": "Why Robots Need Senses", "key": "Sensors close the loop between the world and the controller."},
    {"num": 20, "title": "Why Accelerometers Lie", "key": "Accelerometers measure specific force, not pure acceleration."},
    {"num": 21, "title": "Why Gyroscopes Drift", "key": "Integration of noisy rate measurements accumulates bias."},
    {"num": 22, "title": "Why GPS Isn't Enough", "key": "Global positioning is low rate and unreliable near obstacles."},
    {"num": 23, "title": "Why Sensors Disagree", "key": "Every sensor has noise, bias, and a different frame of reference."},
    {"num": 24, "title": "Why Sensor Fusion Works", "key": "Combining sensors with different strengths reduces overall uncertainty."},
    {"num": 25, "title": "Why Kalman Filters Exist", "key": "A Kalman filter optimally blends prediction and measurement."},
    {"num": 26, "title": "Why Four Motors Beat One", "key": "Four motors provide lift and counter-torque simultaneously."},
    {"num": 27, "title": "Why Quadcopters Flip", "key": "Differential thrust creates torques that change attitude."},
    {"num": 28, "title": "Why Hovering Is Hard", "key": "Hover requires balancing thrust against weight in real time."},
    {"num": 29, "title": "Why Wind Wins", "key": "Controllers must reject external disturbances faster than they grow."},
    {"num": 30, "title": "Why Autopilots Exist", "key": "An autopilot handles fast stabilization so the human commands intent."},
    {"num": 31, "title": "Why Drones Crash", "key": "Safety margins and fail-safe logic are as important as control."},
    {"num": 32, "title": "Why Maps Matter", "key": "A map turns raw sensor data into a reusable model of the world."},
    {"num": 33, "title": "Why Dead Reckoning Fails", "key": "Integrating velocity accumulates error without bounds."},
    {"num": 34, "title": "Why Robots Get Lost", "key": "Ambiguity arises when different places look identical."},
    {"num": 35, "title": "Why SLAM Exists", "key": "SLAM solves mapping and localization jointly."},
    {"num": 36, "title": "Why Planning Is Hard", "key": "Planning searches a high-dimensional space of possible motions."},
    {"num": 37, "title": "Why A* Works", "key": "A* uses a heuristic to focus search toward the goal."},
    {"num": 38, "title": "Why Robots Change Their Mind", "key": "Replanning updates decisions when the world changes."},
    {"num": 39, "title": "Why Following Isn't Understanding", "key": "Following trajectories does not generalize to new situations."},
    {"num": 40, "title": "Why Robots Need Goals", "key": "Goals translate intent into a measure of success."},
    {"num": 41, "title": "Why Obstacles Change Everything", "key": "Obstacles turn free space into a constrained decision problem."},
    {"num": 42, "title": "Why State Matters", "key": "The right action depends on hidden state, not just current input."},
    {"num": 43, "title": "Why Estimation Beats Measurement", "key": "State estimation infers the most likely true state from noisy data."},
    {"num": 44, "title": "Why Decisions Need Models", "key": "A model lets the robot predict outcomes and choose the best sequence."},
    {"num": 45, "title": "Why Autonomous Drones Work", "key": "Autonomy is the closed loop of sensing, thinking, and acting."},
]

# Chapter-specific JS simulation code. Each snippet runs inside a page that already
# declares `const canvas = ...; const ctx = ...;` and loads `../common/engine.js`.
CHAPTER_JS = {
    1: """
const groundY = 250;
const wheel = new Body('wheel', 50, groundY - 20, { mass: 1, radius: 20, color: '#1976d2' });
const target = new Body('target', 400, groundY - 5, { mass: 1, radius: 5, color: '#4caf50' });
let step = 0;
function draw() {
  ctx.clearRect(0, 0, canvas.width, canvas.height);
  ctx.fillStyle = '#8d6e63';
  ctx.fillRect(0, groundY, canvas.width, canvas.height - groundY);
  wheel.clearForces();
  wheel.addForce(new Vec(80, 0));      // push
  wheel.addForce(wheel.vel.mul(-8));   // friction/damping
  wheel.step(0.016);
  drawBody(ctx, wheel);
  drawBody(ctx, target);
  drawArrow(ctx, {x: wheel.pos.x - 25, y: wheel.pos.y}, {x: wheel.pos.x + 25, y: wheel.pos.y}, '#ff9800');
  ctx.fillStyle = '#333';
  ctx.fillText(`Speed: ${wheel.vel.x.toFixed(2)} px/s`, 10, 20);
  step++;
  requestAnimationFrame(draw);
}
draw();
""",
    2: """
const groundY = 250;
const crate = new Body('crate', 50, groundY - 30, { mass: 10, radius: 30, color: '#795548' });
function draw() {
  ctx.clearRect(0, 0, canvas.width, canvas.height);
  ctx.fillStyle = '#8d6e63';
  ctx.fillRect(0, groundY, canvas.width, canvas.height - groundY);
  crate.clearForces();
  crate.addForce(new Vec(50, 0)); // gentle push
  crate.step(0.016);
  drawBody(ctx, crate);
  drawArrow(ctx, {x: crate.pos.x - 35, y: crate.pos.y}, {x: crate.pos.x + 35, y: crate.pos.y}, '#ff9800');
  ctx.fillStyle = '#333';
  ctx.fillText(`Velocity: ${crate.vel.x.toFixed(3)} px/s (heavy object barely moves)`, 10, 20);
  requestAnimationFrame(draw);
}
draw();
""",
    3: """
const magnet = new Body('magnet', 100, 150, { mass: 2, radius: 20, color: '#e53935' });
const nail = new Body('nail', 500, 150, { mass: 0.5, radius: 8, color: '#607d8b' });
function draw() {
  ctx.clearRect(0, 0, canvas.width, canvas.height);
  const delta = magnet.pos.sub(nail.pos);
  const dist = Math.max(delta.length(), 20);
  const force = delta.div(dist).mul(30000 / (dist * dist));
  nail.clearForces();
  nail.addForce(force);
  nail.step(0.016);
  drawBody(ctx, magnet);
  drawBody(ctx, nail);
  drawArrow(ctx, nail.pos, magnet.pos, '#e53935');
  ctx.fillStyle = '#333';
  ctx.fillText(`Distance: ${dist.toFixed(1)} px`, 10, 20);
  requestAnimationFrame(draw);
}
draw();
""",
    4: """
const wire = new Body('wire', 300, 240, { mass: 0.2, radius: 8, color: '#ff9800' });
let current = false;
setInterval(() => { current = !current; }, 1500);
function draw() {
  ctx.clearRect(0, 0, canvas.width, canvas.height);
  ctx.strokeStyle = '#333'; ctx.lineWidth = 2;
  ctx.beginPath(); ctx.moveTo(150, 150); ctx.lineTo(450, 150); ctx.stroke();
  ctx.fillStyle = '#333'; ctx.fillText('Magnetic field (into page)', 200, 130);
  wire.clearForces();
  if (current) wire.addForce(new Vec(0, -120));
  wire.step(0.016);
  if (wire.pos.y < 80) { wire.pos.y = 80; wire.vel.y = 0; }
  drawBody(ctx, wire);
  if (current) drawArrow(ctx, {x: wire.pos.x, y: wire.pos.y + 25}, {x: wire.pos.x, y: wire.pos.y - 25}, '#4caf50');
  ctx.fillStyle = '#333';
  ctx.fillText(current ? 'Current ON: wire jumps' : 'Current OFF: wire falls', 10, 20);
  requestAnimationFrame(draw);
}
draw();
""",
    5: """
const coil = new Body('coil', 150, 150, { mass: 1, radius: 22, color: '#ff9800' });
const nail = new Body('nail', 500, 150, { mass: 0.3, radius: 7, color: '#607d8b' });
let t = 0;
function draw() {
  ctx.clearRect(0, 0, canvas.width, canvas.height);
  const current = t > 120 ? 2 : 0;
  if (current > 0) {
    const delta = coil.pos.sub(nail.pos);
    const dist = Math.max(delta.length(), 20);
    const force = delta.div(dist).mul(20000 / (dist * dist));
    nail.clearForces();
    nail.addForce(force);
  } else {
    nail.clearForces();
  }
  nail.step(0.016);
  drawBody(ctx, coil);
  drawBody(ctx, nail);
  ctx.fillStyle = '#333';
  ctx.fillText(current ? 'Current ON: coil becomes a magnet' : 'Current OFF: nail sits still', 10, 20);
  t++;
  requestAnimationFrame(draw);
}
draw();
""",
    6: """
const coil = new Body('coil', 300, 150, { mass: 0.5, radius: 20, color: '#1976d2' });
let t = 0;
function draw() {
  ctx.clearRect(0, 0, canvas.width, canvas.height);
  const phase = t % 100;
  const push = phase < 50 ? 40 : -40;
  coil.clearForces();
  coil.addForce(new Vec(push, 0));
  coil.step(0.016);
  drawBody(ctx, coil);
  drawArrow(ctx, {x: coil.pos.x - (push > 0 ? -30 : 30), y: coil.pos.y}, {x: coil.pos.x + (push > 0 ? 30 : -30), y: coil.pos.y}, '#ff9800');
  ctx.fillStyle = '#333';
  ctx.fillText('Commutation flips the push to keep rotation going', 10, 20);
  t++;
  requestAnimationFrame(draw);
}
draw();
""",
    7: """
const motor = new Body('motor', 300, 150, { mass: 0.5, radius: 25, color: '#1976d2' });
let speed = 0;
function draw() {
  ctx.clearRect(0, 0, canvas.width, canvas.height);
  const voltage = 5;
  const backEmf = 0.8 * speed;
  const current = voltage - backEmf;
  const torque = 0.1 * current;
  const friction = -0.02 * speed;
  speed += (torque + friction) * 0.016;
  motor.angle += speed * 0.016;
  drawBody(ctx, motor);
  ctx.fillStyle = '#333';
  ctx.fillText(`Speed: ${speed.toFixed(2)} rad/s (saturates due to back-EMF + friction)`, 10, 20);
  requestAnimationFrame(draw);
}
draw();
""",
    8: """
const rotor = new Body('rotor', 300, 150, { mass: 0.5, radius: 25, color: '#1976d2' });
function draw() {
  ctx.clearRect(0, 0, canvas.width, canvas.height);
  const sector = Math.floor((rotor.angle / (Math.PI / 3)) % 6);
  const torque = sector % 2 === 0 ? 5 : -5;
  rotor.clearForces();
  rotor.addTorque(torque);
  rotor.step(0.016);
  drawBody(ctx, rotor);
  ctx.fillStyle = '#333';
  ctx.fillText(`Sector ${sector}: electronic commutation replaces brushes`, 10, 20);
  requestAnimationFrame(draw);
}
draw();
""",
    9: """
const rotor = new Body('rotor', 300, 150, { mass: 0.5, radius: 25, color: '#1976d2' });
let t = 0;
function draw() {
  ctx.clearRect(0, 0, canvas.width, canvas.height);
  const f = Math.sin(t) + Math.sin(t + 2.094) + Math.sin(t + 4.189);
  rotor.clearForces();
  rotor.addTorque(2 * f);
  rotor.step(0.016);
  drawBody(ctx, rotor);
  // phase indicators
  for (let i = 0; i < 3; i++) {
    const v = Math.sin(t + i * 2.094);
    ctx.fillStyle = v > 0 ? '#4caf50' : '#e53935';
    ctx.fillRect(50 + i * 40, 250 - v * 30, 20, v * 30);
  }
  ctx.fillStyle = '#333';
  ctx.fillText('Three phased currents create a rotating field', 10, 20);
  t += 0.08;
  requestAnimationFrame(draw);
}
draw();
""",
    10: """
const motor = new Body('motor', 300, 150, { mass: 0.5, radius: 25, color: '#1976d2' });
let speed = 0;
const resistance = 1, voltage = 5, turns = 50;
function draw() {
  ctx.clearRect(0, 0, canvas.width, canvas.height);
  const current = voltage / resistance;
  const torque = 0.02 * turns * current;
  const damping = -0.05 * speed;
  speed += (torque + damping) * 0.016;
  motor.angle += speed * 0.016;
  drawBody(ctx, motor);
  ctx.fillStyle = '#333';
  ctx.fillText(`Turns: ${turns}  Current: ${current.toFixed(1)}A  Speed: ${speed.toFixed(2)} rad/s`, 10, 20);
  requestAnimationFrame(draw);
}
draw();
""",
    11: """
const plant = new Body('plant', 50, 150, { mass: 1, radius: 12, color: '#1976d2' });
const target = new Body('target', 500, 150, { mass: 1, radius: 6, color: '#4caf50' });
const pid = new PID(8.0, 0, 0, target.pos.x);
function draw() {
  ctx.clearRect(0, 0, canvas.width, canvas.height);
  plant.clearForces();
  const u = pid.update(plant.pos.x, 0.016);
  plant.addForce(new Vec(u, 0));
  plant.step(0.016);
  drawBody(ctx, target);
  drawBody(ctx, plant);
  ctx.fillStyle = '#333';
  ctx.fillText(`High gain is fast but overshoots (position ${plant.pos.x.toFixed(1)})`, 10, 20);
  requestAnimationFrame(draw);
}
draw();
""",
    12: """
const mass = new Body('mass', 300, 150, { mass: 1, radius: 12, color: '#1976d2' });
let t = 0;
const k = 10, c = 0.1;
function draw() {
  ctx.clearRect(0, 0, canvas.width, canvas.height);
  const displacement = mass.pos.x - 300;
  const spring = -k * displacement;
  const damper = -c * mass.vel.x;
  mass.clearForces();
  mass.addForce(new Vec(spring + damper, 0));
  mass.step(0.016);
  ctx.strokeStyle = '#999'; ctx.lineWidth = 2;
  ctx.beginPath(); ctx.moveTo(300, 150); ctx.lineTo(mass.pos.x, mass.pos.y); ctx.stroke();
  drawBody(ctx, mass);
  ctx.fillStyle = '#333';
  ctx.fillText(`Mass-spring system oscillates (displacement ${displacement.toFixed(1)})`, 10, 20);
  t++;
  requestAnimationFrame(draw);
}
draw();
""",
    13: """
const plant = new Body('plant', 50, 150, { mass: 1, radius: 12, color: '#1976d2' });
const target = new Body('target', 500, 150, { mass: 1, radius: 6, color: '#4caf50' });
const pid = new PID(1.0, 0.1, 0.5, target.pos.x);
function draw() {
  ctx.clearRect(0, 0, canvas.width, canvas.height);
  plant.clearForces();
  const u = pid.update(plant.pos.x, 0.016);
  plant.addForce(new Vec(u, 0));
  plant.step(0.016);
  drawBody(ctx, target);
  drawBody(ctx, plant);
  ctx.fillStyle = '#333';
  ctx.fillText(`Feedback corrects the error (position ${plant.pos.x.toFixed(1)})`, 10, 20);
  requestAnimationFrame(draw);
}
draw();
""",
    14: """
const plant = new Body('plant', 50, 150, { mass: 1, radius: 12, color: '#1976d2' });
const target = new Body('target', 500, 150, { mass: 1, radius: 6, color: '#4caf50' });
let t = 0;
function draw() {
  ctx.clearRect(0, 0, canvas.width, canvas.height);
  plant.clearForces();
  plant.addForce(new Vec(30, 0)); // fixed open-loop force
  if (t > 200 && t < 400) plant.addForce(new Vec(-25, 0)); // unmeasured disturbance
  plant.step(0.016);
  drawBody(ctx, target);
  drawBody(ctx, plant);
  ctx.fillStyle = '#333';
  ctx.fillText('Open loop: same command, different result under disturbance', 10, 20);
  t++;
  requestAnimationFrame(draw);
}
draw();
""",
    15: """
let trueX = 50, estX = 50;
const trueVel = 1.0, estVel = 1.02;
function draw() {
  ctx.clearRect(0, 0, canvas.width, canvas.height);
  trueX += trueVel * 0.016 * 10;
  estX += estVel * 0.016 * 10;
  if (trueX > canvas.width) { trueX = 50; estX = 50; }
  drawPoint(ctx, trueX, 120, '#4caf50', 6);
  drawPoint(ctx, estX, 180, '#e53935', 6);
  ctx.fillStyle = '#333';
  ctx.fillText(`True (green) vs estimated (red): tiny bias grows into large error`, 10, 20);
  requestAnimationFrame(draw);
}
draw();
""",
    16: """
const plant = new Body('plant', 50, 150, { mass: 1, radius: 12, color: '#1976d2' });
const target = new Body('target', 500, 150, { mass: 1, radius: 6, color: '#4caf50' });
const pid = new PID(1.0, 0.2, 0.5, target.pos.x);
function draw() {
  ctx.clearRect(0, 0, canvas.width, canvas.height);
  plant.clearForces();
  const u = pid.update(plant.pos.x, 0.016);
  plant.addForce(new Vec(u, 0));
  plant.step(0.016);
  drawBody(ctx, target);
  drawBody(ctx, plant);
  ctx.fillStyle = '#333';
  ctx.fillText(`PID blends P, I, and D (position ${plant.pos.x.toFixed(1)})`, 10, 20);
  requestAnimationFrame(draw);
}
draw();
""",
    17: """
const drone = new Body('drone', 50, 240, { mass: 1, radius: 12, color: '#1976d2' });
const target = new Body('target', 500, 80, { mass: 1, radius: 6, color: '#4caf50' });
const altPid = new PID(5.0, 0.1, 1.0, target.pos.y);
const posPid = new PID(0.5, 0, 0.1, target.pos.x);
function draw() {
  ctx.clearRect(0, 0, canvas.width, canvas.height);
  drone.clearForces();
  drone.addForce(new Vec(posPid.update(drone.pos.x, 0.016), altPid.update(drone.pos.y, 0.016)));
  drone.step(0.016);
  drawBody(ctx, target);
  drawBody(ctx, drone);
  ctx.fillStyle = '#333';
  ctx.fillText(`One PID for altitude, another for lateral position`, 10, 20);
  requestAnimationFrame(draw);
}
draw();
""",
    18: """
const quad = new Quadcopter(1.0);
quad.body.pos = new Vec(50, 240);
const target = new Body('target', 500, 80, { mass: 1, radius: 6, color: '#4caf50' });
const altPid = new PID(5.0, 0.1, 1.0, target.pos.y);
const attitudePid = new PID(2.0, 0, 0.5, 0);
function draw() {
  ctx.clearRect(0, 0, canvas.width, canvas.height);
  const thrust = altPid.update(quad.body.pos.y, 0.016);
  const torque = attitudePid.update(quad.body.angle, 0.016);
  quad.setMotors(thrust - torque, thrust + torque);
  quad.step(0.016);
  drawBody(ctx, target);
  drawBody(ctx, quad.body);
  ctx.fillStyle = '#333';
  ctx.fillText(`Inner attitude loop + outer altitude loop`, 10, 20);
  requestAnimationFrame(draw);
}
draw();
""",
    19: """
const robot = new Body('robot', 50, 240, { mass: 1, radius: 12, color: '#1976d2' });
const wall = new Body('wall', 500, 240, { mass: 100, radius: 15, color: '#795548' });
function draw() {
  ctx.clearRect(0, 0, canvas.width, canvas.height);
  robot.clearForces();
  robot.addForce(new Vec(40, 0));
  robot.step(0.016);
  if (robot.pos.x > wall.pos.x - 25) {
    robot.pos.x = wall.pos.x - 25;
    robot.vel.x = 0;
  }
  drawBody(ctx, robot);
  drawBody(ctx, wall);
  ctx.fillStyle = '#333';
  ctx.fillText('Without sensors, the robot cannot see the wall coming', 10, 20);
  requestAnimationFrame(draw);
}
draw();
""",
    20: """
const body = new Body('body', 300, 150, { mass: 1, radius: 20, color: '#1976d2' });
const accel = new Accelerometer(0.02);
function draw() {
  ctx.clearRect(0, 0, canvas.width, canvas.height);
  body.clearForces();
  const reading = accel.read(body, new Vec(0, -9.81));
  drawBody(ctx, body);
  drawArrow(ctx, body.pos, body.pos.add(reading.mul(4)), '#e53935');
  ctx.fillStyle = '#333';
  ctx.fillText(`Accelerometer reads gravity even when still: (${reading.x.toFixed(2)}, ${reading.y.toFixed(2)})`, 10, 20);
  requestAnimationFrame(draw);
}
draw();
""",
    21: """
const body = new Body('body', 300, 150, { mass: 1, radius: 20, color: '#1976d2' });
body.angularVel = 0.1;
const gyro = new Gyroscope(0.01, 0.005);
let trueAngle = 0, estAngle = 0;
function draw() {
  ctx.clearRect(0, 0, canvas.width, canvas.height);
  trueAngle += body.angularVel * 0.016;
  estAngle += gyro.read(body) * 0.016;
  body.angle = trueAngle;
  drawBody(ctx, body);
  ctx.fillStyle = '#333';
  ctx.fillText(`True angle: ${trueAngle.toFixed(2)} rad  Integrated gyro: ${estAngle.toFixed(2)} rad (drift)`, 10, 20);
  requestAnimationFrame(draw);
}
draw();
""",
    22: """
const drone = new Body('drone', 50, 150, { mass: 1, radius: 10, color: '#1976d2' });
drone.vel = new Vec(1.5, 0.5);
const gps = new GPS(0.5, 20);
let fixes = [];
function draw() {
  ctx.clearRect(0, 0, canvas.width, canvas.height);
  drone.pos = drone.pos.add(drone.vel.mul(0.5));
  if (drone.pos.x > canvas.width) drone.pos.x = 50;
  const fix = gps.read(drone);
  if (fix) fixes.push(fix);
  if (fixes.length > 20) fixes.shift();
  drawBody(ctx, drone);
  for (const f of fixes) drawPoint(ctx, f.x, f.y, '#e53935', 3);
  ctx.fillStyle = '#333';
  ctx.fillText(`GPS is low-rate and noisy (${fixes.length} recent fixes shown)`, 10, 20);
  requestAnimationFrame(draw);
}
draw();
""",
    23: """
const trueVal = 300;
function draw() {
  ctx.clearRect(0, 0, canvas.width, canvas.height);
  const a = addNoise(trueVal, 20);
  const b = addNoise(trueVal, 50);
  drawPoint(ctx, trueVal, 150, '#4caf50', 8);
  drawPoint(ctx, a, 120, '#1976d2', 6);
  drawPoint(ctx, b, 180, '#e53935', 6);
  ctx.fillStyle = '#333';
  ctx.fillText(`True (green), sensor A (blue), sensor B (red): different sensors disagree`, 10, 20);
  requestAnimationFrame(draw);
}
draw();
""",
    24: """
const trueVal = 300;
function draw() {
  ctx.clearRect(0, 0, canvas.width, canvas.height);
  const fast = addNoise(trueVal, 30);
  const slow = addNoise(trueVal, 5);
  const fused = 0.2 * fast + 0.8 * slow;
  drawPoint(ctx, trueVal, 150, '#4caf50', 8);
  drawPoint(ctx, fast, 100, '#1976d2', 5);
  drawPoint(ctx, slow, 200, '#ff9800', 5);
  drawPoint(ctx, fused, 150, '#e53935', 7);
  ctx.fillStyle = '#333';
  ctx.fillText(`Fused estimate (red) is closer to truth (green) than either raw sensor`, 10, 20);
  requestAnimationFrame(draw);
}
draw();
""",
    25: """
const kf = new Kalman1D(0.01, 0.5);
let truePos = 0;
const path = [];
function draw() {
  ctx.clearRect(0, 0, canvas.width, canvas.height);
  truePos += 0.5;
  const measurement = truePos + (Math.random() - 0.5) * 1.5;
  kf.predict(1, 0.5);
  kf.update(measurement);
  path.push({ true: truePos, est: kf.x, meas: measurement });
  if (path.length > 200) path.shift();
  ctx.strokeStyle = '#4caf50'; ctx.beginPath(); ctx.moveTo(0, 250 - path[0].true / 2);
  for (let i = 1; i < path.length; i++) ctx.lineTo(i * 3, 250 - path[i].true / 2); ctx.stroke();
  ctx.strokeStyle = '#e53935'; ctx.beginPath(); ctx.moveTo(0, 250 - path[0].meas / 2);
  for (let i = 1; i < path.length; i++) ctx.lineTo(i * 3, 250 - path[i].meas / 2); ctx.stroke();
  ctx.strokeStyle = '#1976d2'; ctx.lineWidth = 2; ctx.beginPath(); ctx.moveTo(0, 250 - path[0].est / 2);
  for (let i = 1; i < path.length; i++) ctx.lineTo(i * 3, 250 - path[i].est / 2); ctx.stroke();
  ctx.fillStyle = '#333';
  ctx.fillText(`Kalman (blue) blends prediction and noisy measurement`, 10, 20);
  requestAnimationFrame(draw);
}
draw();
""",
    26: """
const quad = new Quadcopter(1.0);
quad.body.pos = new Vec(300, 200);
function draw() {
  ctx.clearRect(0, 0, canvas.width, canvas.height);
  quad.setMotors(8, 8); // equal thrust cancels torque
  quad.step(0.016);
  drawBody(ctx, quad.body);
  drawArrow(ctx, {x: quad.body.pos.x - 15, y: quad.body.pos.y + 25}, {x: quad.body.pos.x - 15, y: quad.body.pos.y - 15}, '#4caf50');
  drawArrow(ctx, {x: quad.body.pos.x + 15, y: quad.body.pos.y + 25}, {x: quad.body.pos.x + 15, y: quad.body.pos.y - 15}, '#4caf50');
  ctx.fillStyle = '#333';
  ctx.fillText(`Equal thrust: lift with no net torque (pitch ${quad.body.angle.toFixed(2)})`, 10, 20);
  requestAnimationFrame(draw);
}
draw();
""",
    27: """
const quad = new Quadcopter(1.0);
quad.body.pos = new Vec(300, 150);
function draw() {
  ctx.clearRect(0, 0, canvas.width, canvas.height);
  quad.setMotors(5, 10); // right motor stronger
  quad.step(0.016);
  drawBody(ctx, quad.body);
  drawArrow(ctx, {x: quad.body.pos.x - 15, y: quad.body.pos.y + 15}, {x: quad.body.pos.x - 15, y: quad.body.pos.y - 5}, '#ff9800');
  drawArrow(ctx, {x: quad.body.pos.x + 15, y: quad.body.pos.y + 35}, {x: quad.body.pos.x + 15, y: quad.body.pos.y - 15}, '#4caf50');
  ctx.fillStyle = '#333';
  ctx.fillText(`Differential thrust flips the drone (pitch ${quad.body.angle.toFixed(2)})`, 10, 20);
  requestAnimationFrame(draw);
}
draw();
""",
    28: """
const quad = new Quadcopter(1.0);
quad.body.pos = new Vec(300, 240);
const pid = new PID(4.0, 0.2, 1.0, 80);
function draw() {
  ctx.clearRect(0, 0, canvas.width, canvas.height);
  const thrust = pid.update(quad.body.pos.y, 0.016);
  quad.setMotors(thrust, thrust);
  quad.step(0.016);
  ctx.strokeStyle = '#4caf50'; ctx.setLineDash([5, 5]);
  ctx.beginPath(); ctx.moveTo(0, 80); ctx.lineTo(canvas.width, 80); ctx.stroke(); ctx.setLineDash([]);
  drawBody(ctx, quad.body);
  ctx.fillStyle = '#333';
  ctx.fillText(`Hovering balances thrust against gravity (altitude ${quad.body.pos.y.toFixed(1)})`, 10, 20);
  requestAnimationFrame(draw);
}
draw();
""",
    29: """
const quad = new Quadcopter(1.0);
quad.body.pos = new Vec(300, 150);
const pid = new PID(2.0, 0.1, 0.5, 0);
let t = 0;
function draw() {
  ctx.clearRect(0, 0, canvas.width, canvas.height);
  const wind = (t > 180 && t < 420) ? new Vec(40, 0) : new Vec(0, 0);
  quad.body.addForce(wind);
  const torque = pid.update(quad.body.angle, 0.016);
  quad.setMotors(8 - torque, 8 + torque);
  quad.step(0.016);
  drawBody(ctx, quad.body);
  if (wind.x !== 0) drawArrow(ctx, {x: 50, y: 150}, {x: 120, y: 150}, '#e53935');
  ctx.fillStyle = '#333';
  ctx.fillText(`Feedback rejects wind disturbances (pitch ${quad.body.angle.toFixed(2)})`, 10, 20);
  t++;
  requestAnimationFrame(draw);
}
draw();
""",
    30: """
const quad = new Quadcopter(1.0);
quad.body.pos = new Vec(300, 150);
const targetPitch = 0.2;
const pid = new PID(3.0, 0, 0.8, targetPitch);
function draw() {
  ctx.clearRect(0, 0, canvas.width, canvas.height);
  const torque = pid.update(quad.body.angle, 0.016);
  quad.setMotors(8 - torque, 8 + torque);
  quad.step(0.016);
  drawBody(ctx, quad.body);
  ctx.strokeStyle = '#4caf50'; ctx.setLineDash([5, 5]);
  const x2 = quad.body.pos.x + 60 * Math.cos(targetPitch);
  const y2 = quad.body.pos.y + 60 * Math.sin(targetPitch);
  ctx.beginPath(); ctx.moveTo(quad.body.pos.x, quad.body.pos.y); ctx.lineTo(x2, y2); ctx.stroke(); ctx.setLineDash([]);
  ctx.fillStyle = '#333';
  ctx.fillText(`Autopilot holds target pitch ${targetPitch.toFixed(1)} (current ${quad.body.angle.toFixed(2)})`, 10, 20);
  requestAnimationFrame(draw);
}
draw();
""",
    31: """
const quad = new Quadcopter(1.0);
quad.body.pos = new Vec(300, 100);
const pid = new PID(4.0, 0.1, 1.0, 100);
let t = 0;
function draw() {
  ctx.clearRect(0, 0, canvas.width, canvas.height);
  const thrust = pid.update(quad.body.pos.y, 0.016);
  if (t > 300) quad.setMotors(0, thrust); // motor failure
  else quad.setMotors(thrust, thrust);
  quad.step(0.016);
  drawBody(ctx, quad.body);
  ctx.fillStyle = '#333';
  ctx.fillText(t > 300 ? `Motor failure: drone loses control` : `Normal hover`, 10, 20);
  t++;
  requestAnimationFrame(draw);
}
draw();
""",
    32: """
const grid = new Grid(12, 8);
for (let x = 4; x < 8; x++) grid.block(x, 3);
function draw() {
  ctx.clearRect(0, 0, canvas.width, canvas.height);
  drawGrid(ctx, grid, { cell: 40, ox: 60, oy: 20 });
  ctx.fillStyle = '#333';
  ctx.fillText(`Map turns sensor observations into a reusable model (${grid.obstacles.size} obstacles)`, 10, 20);
  requestAnimationFrame(draw);
}
draw();
""",
    33: """
let trueX = 50, estX = 50;
const trueVel = 1.0;
function draw() {
  ctx.clearRect(0, 0, canvas.width, canvas.height);
  const noisyVel = addNoise(trueVel, 0.05);
  trueX += trueVel * 0.5;
  estX += noisyVel * 0.5;
  if (trueX > canvas.width) { trueX = 50; estX = 50; }
  drawPoint(ctx, trueX, 120, '#4caf50', 6);
  drawPoint(ctx, estX, 180, '#e53935', 6);
  ctx.fillStyle = '#333';
  ctx.fillText(`Dead reckoning drifts as noisy velocity integrates`, 10, 20);
  requestAnimationFrame(draw);
}
draw();
""",
    34: """
function draw() {
  ctx.clearRect(0, 0, canvas.width, canvas.height);
  ctx.fillStyle = '#795548';
  ctx.fillRect(50, 120, 200, 60);
  ctx.fillRect(350, 120, 200, 60);
  ctx.fillStyle = '#333';
  ctx.fillText(`Sensor: "long corridor, no features"`, 220, 110);
  ctx.fillText(`Location A`, 120, 160);
  ctx.fillText(`Location B`, 420, 160);
  ctx.fillText(`Two different places look identical: localization ambiguity`, 120, 220);
  requestAnimationFrame(draw);
}
draw();
""",
    35: """
const landmarks = [[2, 0], [5, 0], [8, 0]];
let robotX = 1.0;
function draw() {
  ctx.clearRect(0, 0, canvas.width, canvas.height);
  ctx.fillStyle = '#1976d2';
  ctx.fillRect(robotX * 40 + 50, 150, 12, 12);
  ctx.fillStyle = '#4caf50';
  for (const lm of landmarks) {
    ctx.beginPath(); ctx.arc(lm[0] * 40 + 50, 150, 6, 0, Math.PI * 2); ctx.fill();
  }
  ctx.fillStyle = '#333';
  ctx.fillText(`Robot measures landmarks relative to itself; SLAM builds both map and pose`, 10, 20);
  requestAnimationFrame(draw);
}
draw();
""",
    36: """
const grid = new Grid(12, 8);
for (let x = 3; x < 8; x++) grid.block(x, 2);
const path = astar(grid, [0, 0], [11, 7]);
let progress = 0;
function draw() {
  ctx.clearRect(0, 0, canvas.width, canvas.height);
  drawGrid(ctx, grid, { cell: 40, ox: 20, oy: 10 });
  drawGridPath(ctx, path, { cell: 40, ox: 20, oy: 10 });
  if (path && progress < path.length) {
    const [x, y] = path[progress];
    drawPoint(ctx, 20 + x * 40 + 20, 10 + y * 40 + 20, '#1976d2', 8);
    if (progress % 5 === 0) progress++;
  }
  ctx.fillStyle = '#333';
  ctx.fillText(`Planning searches a high-dimensional space for a safe path`, 10, 20);
  requestAnimationFrame(draw);
}
draw();
""",
    37: """
const grid = new Grid(14, 10);
for (let y = 0; y < 8; y++) grid.block(6, y);
const path = astar(grid, [0, 0], [13, 9]);
let progress = 0;
function draw() {
  ctx.clearRect(0, 0, canvas.width, canvas.height);
  drawGrid(ctx, grid, { cell: 34, ox: 20, oy: 10 });
  drawGridPath(ctx, path, { cell: 34, ox: 20, oy: 10 });
  if (path && progress < path.length) {
    const [x, y] = path[progress];
    drawPoint(ctx, 20 + x * 34 + 17, 10 + y * 34 + 17, '#1976d2', 7);
    if (progress % 4 === 0) progress++;
  }
  ctx.fillStyle = '#333';
  ctx.fillText(`A* uses a heuristic to search efficiently toward the goal`, 10, 20);
  requestAnimationFrame(draw);
}
draw();
""",
    38: """
const grid = new Grid(10, 10);
let path = astar(grid, [0, 0], [9, 9]);
let t = 0;
function draw() {
  ctx.clearRect(0, 0, canvas.width, canvas.height);
  if (t === 150) { grid.block(7, 7); path = astar(grid, [0, 0], [9, 9]); }
  drawGrid(ctx, grid, { cell: 30, ox: 30, oy: 10 });
  drawGridPath(ctx, path, { cell: 30, ox: 30, oy: 10 });
  ctx.fillStyle = '#333';
  ctx.fillText(t > 150 ? 'Obstacle appeared: robot replanned' : 'Original plan', 10, 20);
  t++;
  requestAnimationFrame(draw);
}
draw();
""",
    39: """
const robot = new Body('robot', 50, 240, { mass: 1, radius: 10, color: '#1976d2' });
const trainingPath = Array.from({length: 300}, (_, i) => 50 + i * 1.5);
let i = 0;
function draw() {
  ctx.clearRect(0, 0, canvas.width, canvas.height);
  if (i < trainingPath.length) {
    const target = trainingPath[i];
    robot.clearForces();
    robot.addForce(new Vec(5 * (target - robot.pos.x), 0));
    robot.addForce(new Vec(-2, 0)); // unexpected slope not in training
    robot.step(0.016);
    i++;
  }
  drawBody(ctx, robot);
  ctx.strokeStyle = '#4caf50'; ctx.setLineDash([5, 5]);
  ctx.beginPath(); ctx.moveTo(50, 240); ctx.lineTo(500, 240); ctx.stroke(); ctx.setLineDash([]);
  ctx.fillStyle = '#333';
  ctx.fillText(`Following a memorized path fails when the environment changes`, 10, 20);
  requestAnimationFrame(draw);
}
draw();
""",
    40: """
const state = 100, goal = 500;
function draw() {
  ctx.clearRect(0, 0, canvas.width, canvas.height);
  drawPoint(ctx, state, 150, '#1976d2', 8);
  drawPoint(ctx, goal, 150, '#4caf50', 8);
  ctx.strokeStyle = '#999'; ctx.setLineDash([5, 5]);
  ctx.beginPath(); ctx.moveTo(state, 150); ctx.lineTo(goal, 150); ctx.stroke(); ctx.setLineDash([]);
  ctx.fillStyle = '#333';
  ctx.fillText(`Cost to goal: ${Math.abs(goal - state)} — goals translate intent into a measure of success`, 10, 20);
  requestAnimationFrame(draw);
}
draw();
""",
    41: """
const grid = new Grid(12, 8);
grid.block(5, 0); grid.block(5, 1); grid.block(5, 2);
const path = astar(grid, [0, 0], [11, 0]);
function draw() {
  ctx.clearRect(0, 0, canvas.width, canvas.height);
  drawGrid(ctx, grid, { cell: 40, ox: 20, oy: 40 });
  drawGridPath(ctx, path, { cell: 40, ox: 20, oy: 40 });
  ctx.fillStyle = '#333';
  ctx.fillText(`Obstacles turn a straight-line goal into a constrained search`, 10, 20);
  requestAnimationFrame(draw);
}
draw();
""",
    42: """
function draw() {
  ctx.clearRect(0, 0, canvas.width, canvas.height);
  ctx.fillStyle = '#333';
  ctx.fillText('Sensor reading: low battery voltage', 200, 80);
  ctx.fillStyle = '#e53935';
  ctx.fillRect(100, 120, 80, 80);
  ctx.fillStyle = '#4caf50';
  ctx.fillRect(420, 120, 80, 80);
  ctx.fillStyle = '#fff';
  ctx.fillText('Low', 125, 165);
  ctx.fillText('OK', 450, 165);
  ctx.fillStyle = '#333';
  ctx.fillText('Same input, different hidden state → different correct action', 120, 240);
  requestAnimationFrame(draw);
}
draw();
""",
    43: """
const kf = new Kalman1D(0.01, 1.0);
let trueVal = 0;
const path = [];
function draw() {
  ctx.clearRect(0, 0, canvas.width, canvas.height);
  trueVal += 0.5;
  const z = addNoise(trueVal, 1.0);
  kf.predict(1, 0.5);
  kf.update(z);
  path.push({ true: trueVal, raw: z, est: kf.x });
  if (path.length > 250) path.shift();
  ctx.strokeStyle = '#4caf50'; ctx.beginPath(); ctx.moveTo(0, 250 - path[0].true);
  for (let i = 1; i < path.length; i++) ctx.lineTo(i * 2.4, 250 - path[i].true); ctx.stroke();
  ctx.strokeStyle = '#e53935'; ctx.beginPath(); ctx.moveTo(0, 250 - path[0].raw);
  for (let i = 1; i < path.length; i++) ctx.lineTo(i * 2.4, 250 - path[i].raw); ctx.stroke();
  ctx.strokeStyle = '#1976d2'; ctx.lineWidth = 2; ctx.beginPath(); ctx.moveTo(0, 250 - path[0].est);
  for (let i = 1; i < path.length; i++) ctx.lineTo(i * 2.4, 250 - path[i].est); ctx.stroke();
  ctx.fillStyle = '#333';
  ctx.fillText(`State estimation (blue) is often more reliable than a raw measurement (red)`, 10, 20);
  requestAnimationFrame(draw);
}
draw();
""",
    44: """
const grid = new Grid(8, 8);
let bestThrust = 0, bestCost = Infinity;
const candidates = [6, 7, 8, 9, 10];
let idx = 0;
function draw() {
  ctx.clearRect(0, 0, canvas.width, canvas.height);
  drawGrid(ctx, grid, { cell: 30, ox: 30, oy: 20 });
  if (idx < candidates.length) {
    const thrust = candidates[idx];
    const cost = Math.abs(thrust - 8.2); // simulate model prediction
    if (cost < bestCost) { bestCost = cost; bestThrust = thrust; }
    idx++;
  }
  ctx.fillStyle = '#333';
  ctx.fillText(`Model-based search: best thrust ${bestThrust} (error ${bestCost.toFixed(2)})`, 10, 20);
  requestAnimationFrame(draw);
}
draw();
""",
    45: """
const quad = new Quadcopter(1.0);
quad.body.pos = new Vec(50, 240);
const gps = new GPS(0.3, 30);
const altPid = new PID(4.0, 0.1, 1.0, 80);
const posPid = new PID(0.5, 0, 0.1, 500);
function draw() {
  ctx.clearRect(0, 0, canvas.width, canvas.height);
  const fix = gps.read(quad.body);
  const xMeas = fix ? fix.x : quad.body.pos.x;
  const thrust = altPid.update(quad.body.pos.y, 0.016);
  const torque = posPid.update(xMeas, 0.016);
  quad.setMotors(thrust - torque, thrust + torque);
  quad.step(0.016);
  ctx.strokeStyle = '#4caf50'; ctx.setLineDash([5, 5]);
  ctx.beginPath(); ctx.moveTo(0, 80); ctx.lineTo(canvas.width, 80); ctx.stroke(); ctx.setLineDash([]);
  ctx.beginPath(); ctx.moveTo(500, 0); ctx.lineTo(500, canvas.height); ctx.stroke();
  drawBody(ctx, quad.body);
  if (fix) drawPoint(ctx, fix.x, quad.body.pos.y, '#e53935', 4);
  ctx.fillStyle = '#333';
  ctx.fillText(`Full autonomy: GPS sensing + planning target + control loop`, 10, 20);
  requestAnimationFrame(draw);
}
draw();
""",
}


HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Chapter {num:02d}: {title}</title>
<style>
  body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; text-align: center; margin: 0; padding: 1rem; background: #fff; }}
  h1 {{ font-size: 1.4rem; margin-bottom: 0.2rem; }}
  .key {{ color: #555; max-width: 600px; margin: 0 auto 1rem auto; font-size: 0.95rem; }}
  canvas {{ border: 1px solid #ccc; background: #fafafa; display: block; margin: 0 auto; }}
  .home {{ margin-top: 1rem; font-size: 0.85rem; }}
</style>
</head>
<body>
<h1>Chapter {num:02d}: {title}</h1>
<p class="key">{key}</p>
<canvas id="sim" width="600" height="300"></canvas>
<script src="../common/engine.js"></script>
<script>
const canvas = document.getElementById('sim');
const ctx = canvas.getContext('2d');
{js}
</script>
<p class="home"><a href="../../index.html">← Home</a></p>
</body>
</html>
"""


def generate():
    if not COMMON_ENGINE.exists():
        raise FileNotFoundError(f"Shared engine not found: {COMMON_ENGINE}")
    BROWSER_ROOT.mkdir(parents=True, exist_ok=True)
    (BROWSER_ROOT / "common").mkdir(parents=True, exist_ok=True)

    for ch in CHAPTERS:
        num = ch["num"]
        d = BROWSER_ROOT / f"chapter{num:02d}"
        d.mkdir(parents=True, exist_ok=True)
        js = CHAPTER_JS[num]
        html = HTML_TEMPLATE.format(num=num, title=ch["title"], key=ch["key"], js=js)
        (d / "index.html").write_text(html, encoding="utf-8")
        print(f"Generated browser/chapter{num:02d}/index.html")


if __name__ == "__main__":
    generate()
