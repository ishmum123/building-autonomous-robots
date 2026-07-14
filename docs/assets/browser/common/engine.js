// Minimal 2D robotics simulation engine for browser demos.
// Mirrors the Python common.engine API as closely as practical.

class Vec {
  constructor(x = 0, y = 0) {
    this.x = x;
    this.y = y;
  }

  add(v) { return new Vec(this.x + v.x, this.y + v.y); }
  sub(v) { return new Vec(this.x - v.x, this.y - v.y); }
  mul(s) { return new Vec(this.x * s, this.y * s); }
  div(s) { return new Vec(this.x / s, this.y / s); }
  length() { return Math.hypot(this.x, this.y); }
  dot(v) { return this.x * v.x + this.y * v.y; }

  rotate(angle) {
    const c = Math.cos(angle), s = Math.sin(angle);
    return new Vec(this.x * c - this.y * s, this.x * s + this.y * c);
  }

  static from(v) {
    return v instanceof Vec ? v : new Vec(v.x, v.y);
  }
}

class Body {
  constructor(name, x = 0, y = 0, options = {}) {
    this.name = name;
    this.pos = new Vec(x, y);
    this.vel = new Vec();
    this.angle = options.angle || 0;
    this.angularVel = options.angularVel || 0;
    this.mass = options.mass || 1.0;
    this.radius = options.radius || 10;
    this.color = options.color || '#1976d2';
    this.forces = [];
    this.torque = 0;
  }

  clearForces() {
    this.forces = [];
    this.torque = 0;
  }

  addForce(f) {
    this.forces.push(Vec.from(f));
  }

  addTorque(t) {
    this.torque += t;
  }

  step(dt) {
    let total = new Vec();
    for (const f of this.forces) total = total.add(f);
    const acc = total.div(this.mass);
    this.vel = this.vel.add(acc.mul(dt));
    this.pos = this.pos.add(this.vel.mul(dt));
    const moi = 0.5 * this.mass * this.radius * this.radius;
    this.angularVel += (this.torque / moi) * dt;
    this.angle += this.angularVel * dt;
  }
}

class PID {
  constructor(kp, ki, kd, setpoint = 0, options = {}) {
    this.kp = kp;
    this.ki = ki;
    this.kd = kd;
    this.setpoint = setpoint;
    this.outputLimit = options.outputLimit || null;
    this.integral = 0;
    this.lastError = 0;
  }

  reset() {
    this.integral = 0;
    this.lastError = 0;
  }

  update(measurement, dt) {
    const error = this.setpoint - measurement;
    this.integral += error * dt;
    const derivative = dt > 0 ? (error - this.lastError) / dt : 0;
    this.lastError = error;
    let output = this.kp * error + this.ki * this.integral + this.kd * derivative;
    if (this.outputLimit) {
      output = Math.max(this.outputLimit[0], Math.min(this.outputLimit[1], output));
    }
    return output;
  }
}

class World {
  constructor(dt = 0.01, gravity = new Vec(0, -9.81)) {
    this.dt = dt;
    this.gravity = Vec.from(gravity);
    this.bodies = [];
    this.time = 0;
    this.history = { time: [], bodies: {} };
  }

  add(body) {
    this.bodies.push(body);
  }

  body(name) {
    return this.bodies.find(b => b.name === name) || null;
  }

  record() {
    this.history.time.push(this.time);
    for (const b of this.bodies) {
      if (!this.history.bodies[b.name]) this.history.bodies[b.name] = [];
      this.history.bodies[b.name].push({ x: b.pos.x, y: b.pos.y, angle: b.angle });
    }
  }

  step(steps = 1, record = true) {
    for (let i = 0; i < steps; i++) {
      for (const b of this.bodies) {
        b.addForce(this.gravity.mul(b.mass));
        b.step(this.dt);
        b.clearForces();
      }
      this.time += this.dt;
      if (record) this.record();
    }
  }
}

class Quadcopter {
  constructor(mass = 1.0, arm = 0.2, drag = 0.1) {
    this.body = new Body('quad', 0, 1, { mass, radius: 0.15, color: '#1976d2' });
    this.arm = arm;
    this.drag = drag;
    this.motor = [0, 0];
  }

  setMotors(left, right) {
    this.motor = [left, right];
  }

  step(dt) {
    const totalThrust = this.motor[0] + this.motor[1];
    this.body.addForce(new Vec(0, totalThrust));
    this.body.addTorque((this.motor[1] - this.motor[0]) * this.arm);
    this.body.addForce(this.body.vel.mul(-this.drag));
    this.body.step(dt);
    this.body.clearForces();
  }
}

function gaussianRandom(std = 1) {
  // Box-Muller
  const u = 1 - Math.random();
  const v = Math.random();
  return std * Math.sqrt(-2 * Math.log(u)) * Math.cos(2 * Math.PI * v);
}

function addNoise(value, std) {
  return value + gaussianRandom(std);
}

class Accelerometer {
  constructor(noiseStd = 0.05) {
    this.noiseStd = noiseStd;
  }

  read(body, gravity = new Vec(0, -9.81)) {
    let total = new Vec();
    for (const f of body.forces) total = total.add(f);
    const acc = gravity.add(total.div(body.mass));
    return new Vec(addNoise(acc.x, this.noiseStd), addNoise(acc.y, this.noiseStd));
  }
}

class Gyroscope {
  constructor(noiseStd = 0.01, bias = 0) {
    this.noiseStd = noiseStd;
    this.bias = bias;
  }

  read(body) {
    return addNoise(body.angularVel + this.bias, this.noiseStd);
  }
}

class GPS {
  constructor(noiseStd = 0.3, updateRate = 10) {
    this.noiseStd = noiseStd;
    this.updateRate = updateRate;
    this._counter = 0;
  }

  read(body) {
    this._counter++;
    if (this._counter % this.updateRate !== 0) return null;
    return new Vec(addNoise(body.pos.x, this.noiseStd), addNoise(body.pos.y, this.noiseStd));
  }
}

class Grid {
  constructor(width, height) {
    this.width = width;
    this.height = height;
    this.obstacles = new Set();
  }

  block(x, y) {
    this.obstacles.add(`${x},${y}`);
  }

  isBlocked(x, y) {
    return this.obstacles.has(`${x},${y}`);
  }

  neighbors(node) {
    const [x, y] = node;
    const result = [];
    for (const [dx, dy] of [[1, 0], [-1, 0], [0, 1], [0, -1]]) {
      const nx = x + dx, ny = y + dy;
      if (nx >= 0 && nx < this.width && ny >= 0 && ny < this.height && !this.isBlocked(nx, ny)) {
        result.push([nx, ny]);
      }
    }
    return result;
  }

  heuristic(a, b) {
    return Math.abs(a[0] - b[0]) + Math.abs(a[1] - b[1]);
  }
}

function astar(grid, start, goal) {
  const startKey = start.join(',');
  const goalKey = goal.join(',');
  const openSet = [[0, startKey, start]];
  const cameFrom = new Map();
  const gScore = new Map([[startKey, 0]]);
  const fScore = new Map([[startKey, grid.heuristic(start, goal)]]);

  while (openSet.length > 0) {
    openSet.sort((a, b) => a[0] - b[0]);
    const [, currentKey, current] = openSet.shift();
    if (currentKey === goalKey) {
      const path = [current];
      let key = currentKey;
      while (cameFrom.has(key)) {
        const prev = cameFrom.get(key);
        path.push(prev);
        key = prev.join(',');
      }
      return path.reverse();
    }

    for (const neighbor of grid.neighbors(current)) {
      const nKey = neighbor.join(',');
      const tentative = (gScore.get(currentKey) || Infinity) + 1;
      if (tentative < (gScore.get(nKey) || Infinity)) {
        cameFrom.set(nKey, current);
        gScore.set(nKey, tentative);
        fScore.set(nKey, tentative + grid.heuristic(neighbor, goal));
        openSet.push([fScore.get(nKey), nKey, neighbor]);
      }
    }
  }
  return null;
}

class Kalman1D {
  constructor(processNoise = 0.01, measurementNoise = 0.1) {
    this.x = 0;
    this.p = 1;
    this.q = processNoise;
    this.r = measurementNoise;
  }

  predict(dt = 1, velocity = 0) {
    this.x += velocity * dt;
    this.p += this.q;
  }

  update(measurement) {
    const k = this.p / (this.p + this.r);
    this.x += k * (measurement - this.x);
    this.p = (1 - k) * this.p;
  }
}

// ---------- Drawing helpers ----------

function toScreenX(worldX, canvasWidth, scale = 40, offset = 0) {
  return canvasWidth / 2 + worldX * scale + offset;
}

function toScreenY(worldY, canvasHeight, scale = 40, offset = 0) {
  return canvasHeight - 40 - worldY * scale + offset;
}

function drawArrow(ctx, from, to, color = '#4caf50') {
  ctx.strokeStyle = color;
  ctx.fillStyle = color;
  ctx.lineWidth = 2;
  ctx.beginPath();
  ctx.moveTo(from.x, from.y);
  ctx.lineTo(to.x, to.y);
  ctx.stroke();
  const angle = Math.atan2(to.y - from.y, to.x - from.x);
  ctx.beginPath();
  ctx.moveTo(to.x, to.y);
  ctx.lineTo(to.x - 8 * Math.cos(angle - Math.PI / 6), to.y - 8 * Math.sin(angle - Math.PI / 6));
  ctx.lineTo(to.x - 8 * Math.cos(angle + Math.PI / 6), to.y - 8 * Math.sin(angle + Math.PI / 6));
  ctx.fill();
}

function drawBody(ctx, body, options = {}) {
  const color = options.color || body.color;
  const radius = options.radius || body.radius;
  ctx.fillStyle = color;
  ctx.beginPath();
  ctx.arc(body.pos.x, body.pos.y, radius, 0, Math.PI * 2);
  ctx.fill();

  // orientation line
  ctx.strokeStyle = '#fff';
  ctx.lineWidth = 2;
  ctx.beginPath();
  ctx.moveTo(body.pos.x, body.pos.y);
  ctx.lineTo(
    body.pos.x + radius * Math.cos(body.angle),
    body.pos.y + radius * Math.sin(body.angle)
  );
  ctx.stroke();
}

function drawGrid(ctx, grid, options = {}) {
  const cell = options.cell || 30;
  const ox = options.ox || 0;
  const oy = options.oy || 0;
  ctx.strokeStyle = '#ddd';
  ctx.lineWidth = 1;
  for (let x = 0; x <= grid.width; x++) {
    ctx.beginPath();
    ctx.moveTo(ox + x * cell, oy);
    ctx.lineTo(ox + x * cell, oy + grid.height * cell);
    ctx.stroke();
  }
  for (let y = 0; y <= grid.height; y++) {
    ctx.beginPath();
    ctx.moveTo(ox, oy + y * cell);
    ctx.lineTo(ox + grid.width * cell, oy + y * cell);
    ctx.stroke();
  }
  ctx.fillStyle = '#333';
  for (const key of grid.obstacles) {
    const [x, y] = key.split(',').map(Number);
    ctx.fillRect(ox + x * cell + 1, oy + y * cell + 1, cell - 2, cell - 2);
  }
}

function drawGridPath(ctx, path, options = {}) {
  if (!path || path.length === 0) return;
  const cell = options.cell || 30;
  const ox = options.ox || 0;
  const oy = options.oy || 0;
  ctx.strokeStyle = '#4caf50';
  ctx.lineWidth = 3;
  ctx.beginPath();
  ctx.moveTo(ox + path[0][0] * cell + cell / 2, oy + path[0][1] * cell + cell / 2);
  for (let i = 1; i < path.length; i++) {
    ctx.lineTo(ox + path[i][0] * cell + cell / 2, oy + path[i][1] * cell + cell / 2);
  }
  ctx.stroke();
}

function drawPoint(ctx, x, y, color = '#e91e63', radius = 4) {
  ctx.fillStyle = color;
  ctx.beginPath();
  ctx.arc(x, y, radius, 0, Math.PI * 2);
  ctx.fill();
}
