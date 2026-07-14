// Minimal 2D simulation engine for browser demos.
const Vec = (x=0, y=0) => ({x, y});
const add = (a, b) => ({x: a.x+b.x, y: a.y+b.y});
const sub = (a, b) => ({x: a.x-b.x, y: a.y-b.y});
const mul = (v, s) => ({x: v.x*s, y: v.y*s});
const len = (v) => Math.hypot(v.x, v.y);

class Body {
  constructor(name, x=0, y=0, mass=1, radius=10) {
    this.name = name;
    this.pos = Vec(x, y);
    this.vel = Vec();
    this.acc = Vec();
    this.mass = mass;
    this.radius = radius;
    this.forces = [];
  }
  clear() { this.forces = []; }
  add(f) { this.forces.push(f); }
  step(dt) {
    let fx=0, fy=0;
    for (const f of this.forces) { fx += f.x; fy += f.y; }
    this.acc = {x: fx/this.mass, y: fy/this.mass};
    this.vel = add(this.vel, mul(this.acc, dt));
    this.pos = add(this.pos, mul(this.vel, dt));
  }
}

class PID {
  constructor(kp, ki, kd, setpoint=0) {
    this.kp=kp; this.ki=ki; this.kd=kd; this.setpoint=setpoint;
    this.integral=0; this.last=0;
  }
  update(meas, dt) {
    const e = this.setpoint - meas;
    this.integral += e*dt;
    const d = (e-this.last)/dt;
    this.last = e;
    return this.kp*e + this.ki*this.integral + this.kd*d;
  }
}

function drawArrow(ctx, from, to, color) {
  ctx.strokeStyle = color; ctx.fillStyle = color; ctx.lineWidth = 2;
  ctx.beginPath(); ctx.moveTo(from.x, from.y); ctx.lineTo(to.x, to.y); ctx.stroke();
  const ang = Math.atan2(to.y-from.y, to.x-from.x);
  ctx.beginPath();
  ctx.moveTo(to.x, to.y);
  ctx.lineTo(to.x-8*Math.cos(ang-Math.PI/6), to.y-8*Math.sin(ang-Math.PI/6));
  ctx.lineTo(to.x-8*Math.cos(ang+Math.PI/6), to.y-8*Math.sin(ang+Math.PI/6));
  ctx.fill();
}

function drawBody(ctx, b, color='#1976d2') {
  ctx.fillStyle = color;
  ctx.beginPath(); ctx.arc(b.pos.x, b.pos.y, b.radius, 0, Math.PI*2); ctx.fill();
}
