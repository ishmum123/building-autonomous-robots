"""Minimal robotics simulation engine used throughout the curriculum.

No external dependencies are required. If matplotlib is available, plots can be
saved; otherwise results are printed as text.
"""

from __future__ import annotations

import math
import random
from dataclasses import dataclass, field
from typing import Callable, Iterable, List, Optional, Tuple

try:
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    HAS_MATPLOTLIB = True
except Exception:  # pragma: no cover
    HAS_MATPLOTLIB = False


@dataclass
class Vec:
    x: float = 0.0
    y: float = 0.0

    def __add__(self, other: Vec) -> Vec:
        return Vec(self.x + other.x, self.y + other.y)

    def __sub__(self, other: Vec) -> Vec:
        return Vec(self.x - other.x, self.y - other.y)

    def __mul__(self, scalar: float) -> Vec:
        return Vec(self.x * scalar, self.y * scalar)

    def __rmul__(self, scalar: float) -> Vec:
        return self * scalar

    def __truediv__(self, scalar: float) -> Vec:
        return Vec(self.x / scalar, self.y / scalar)

    def length(self) -> float:
        return math.hypot(self.x, self.y)

    def dot(self, other: Vec) -> float:
        return self.x * other.x + self.y * other.y

    def rotate(self, angle: float) -> Vec:
        c, s = math.cos(angle), math.sin(angle)
        return Vec(self.x * c - self.y * s, self.x * s + self.y * c)

    def __repr__(self) -> str:
        return f"Vec({self.x:.3f}, {self.y:.3f})"


@dataclass
class Body:
    name: str
    pos: Vec = field(default_factory=Vec)
    vel: Vec = field(default_factory=Vec)
    angle: float = 0.0
    angular_vel: float = 0.0
    mass: float = 1.0
    radius: float = 0.5
    color: str = "#1976d2"
    forces: List[Vec] = field(default_factory=list)
    torque: float = 0.0

    def clear_forces(self) -> None:
        self.forces.clear()
        self.torque = 0.0

    def add_force(self, force: Vec) -> None:
        self.forces.append(force)

    def add_torque(self, torque: float) -> None:
        self.torque += torque

    def step(self, dt: float) -> None:
        total = sum(self.forces, Vec())
        acc = total / self.mass
        self.vel = self.vel + acc * dt
        self.pos = self.pos + self.vel * dt
        self.angular_vel += self.torque / (0.5 * self.mass * self.radius**2) * dt
        self.angle += self.angular_vel * dt


@dataclass
class PID:
    kp: float
    ki: float
    kd: float
    setpoint: float = 0.0
    integral: float = field(default=0.0, init=False)
    last_error: float = field(default=0.0, init=False)
    output_limit: Optional[Tuple[float, float]] = None

    def reset(self) -> None:
        self.integral = 0.0
        self.last_error = 0.0

    def update(self, measurement: float, dt: float) -> float:
        error = self.setpoint - measurement
        self.integral += error * dt
        derivative = (error - self.last_error) / dt if dt > 0 else 0.0
        self.last_error = error
        output = self.kp * error + self.ki * self.integral + self.kd * derivative
        if self.output_limit:
            lo, hi = self.output_limit
            output = max(lo, min(hi, output))
        return output


class World:
    def __init__(self, dt: float = 0.01, gravity: Vec = None):
        self.dt = dt
        self.gravity = gravity if gravity is not None else Vec(0, -9.81)
        self.bodies: List[Body] = []
        self.time = 0.0
        self.history: dict = {"time": [], "bodies": {}}

    def add(self, body: Body) -> None:
        self.bodies.append(body)

    def record(self) -> None:
        self.history["time"].append(self.time)
        for b in self.bodies:
            self.history["bodies"].setdefault(b.name, []).append(
                (b.pos.x, b.pos.y, b.angle)
            )

    def step(self, steps: int = 1, record: bool = True) -> None:
        for _ in range(steps):
            for b in self.bodies:
                b.add_force(b.mass * self.gravity)
                b.step(self.dt)
                b.clear_forces()
            self.time += self.dt
            if record:
                self.record()

    def body(self, name: str) -> Optional[Body]:
        for b in self.bodies:
            if b.name == name:
                return b
        return None


class Quadcopter:
    """Simplified quadcopter model in 2D (pitch and altitude)."""

    def __init__(self, mass: float = 1.0, arm: float = 0.2, drag: float = 0.1):
        self.body = Body("quad", pos=Vec(0, 1), mass=mass, radius=0.15)
        self.arm = arm
        self.drag = drag
        self.motor = [0.0, 0.0]  # left, right

    def set_motors(self, left: float, right: float) -> None:
        self.motor = [left, right]

    def step(self, dt: float) -> None:
        total_thrust = sum(self.motor)
        self.body.add_force(Vec(0, total_thrust))
        # Pitch torque from differential thrust
        torque = (self.motor[1] - self.motor[0]) * self.arm
        self.body.add_torque(torque)
        # Linear drag opposes velocity
        self.body.add_force(self.body.vel * -self.drag)
        self.body.step(dt)
        self.body.clear_forces()


# ---------- Sensors ----------


def add_noise(value: float, std: float) -> float:
    return value + random.gauss(0, std)


class Accelerometer:
    """Measures specific force: gravity + linear acceleration + noise."""

    def __init__(self, noise_std: float = 0.05):
        self.noise_std = noise_std

    def read(self, body: Body, gravity: Vec = Vec(0, -9.81)) -> Vec:
        acc = gravity + sum(body.forces, Vec()) / body.mass
        return Vec(add_noise(acc.x, self.noise_std), add_noise(acc.y, self.noise_std))


class Gyroscope:
    def __init__(self, noise_std: float = 0.01, bias: float = 0.0):
        self.noise_std = noise_std
        self.bias = bias

    def read(self, body: Body) -> float:
        return add_noise(body.angular_vel + self.bias, self.noise_std)


class GPS:
    def __init__(self, noise_std: float = 0.3, update_rate: int = 10):
        self.noise_std = noise_std
        self.update_rate = update_rate
        self._counter = 0

    def read(self, body: Body) -> Optional[Vec]:
        self._counter += 1
        if self._counter % self.update_rate != 0:
            return None
        return Vec(add_noise(body.pos.x, self.noise_std), add_noise(body.pos.y, self.noise_std))


# ---------- Plotting ----------


def save_plot(
    times: List[float],
    series: dict,
    title: str,
    filename: str = "output.png",
    xlabel: str = "Time (s)",
) -> None:
    if not HAS_MATPLOTLIB:
        print(f"[matplotlib not installed; skipping plot for {title}]")
        return
    plt.figure(figsize=(6, 3))
    for label, values in series.items():
        plt.plot(times, values, label=label)
    plt.title(title)
    plt.xlabel(xlabel)
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(filename)
    plt.close()
    print(f"Saved plot: {filename}")


# ---------- Planning ----------


class Grid:
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.obstacles: set = set()

    def block(self, x: int, y: int) -> None:
        self.obstacles.add((x, y))

    def neighbors(self, node: Tuple[int, int]) -> Iterable[Tuple[int, int]]:
        x, y = node
        for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < self.width and 0 <= ny < self.height and (nx, ny) not in self.obstacles:
                yield (nx, ny)

    def heuristic(self, a: Tuple[int, int], b: Tuple[int, int]) -> float:
        return abs(a[0] - b[0]) + abs(a[1] - b[1])


def astar(grid: Grid, start: Tuple[int, int], goal: Tuple[int, int]) -> Optional[List[Tuple[int, int]]]:
    import heapq

    open_set = [(0.0, start)]
    came_from: dict = {}
    g_score = {start: 0.0}
    f_score = {start: grid.heuristic(start, goal)}

    while open_set:
        _, current = heapq.heappop(open_set)
        if current == goal:
            path = [current]
            while current in came_from:
                current = came_from[current]
                path.append(current)
            return path[::-1]

        for neighbor in grid.neighbors(current):
            tentative = g_score[current] + 1
            if tentative < g_score.get(neighbor, float("inf")):
                came_from[neighbor] = current
                g_score[neighbor] = tentative
                f_score[neighbor] = tentative + grid.heuristic(neighbor, goal)
                heapq.heappush(open_set, (f_score[neighbor], neighbor))
    return None


# ---------- Estimation ----------


class Kalman1D:
    """One-dimensional Kalman filter for a constant-velocity model."""

    def __init__(self, process_noise: float = 0.01, measurement_noise: float = 0.1):
        self.x = 0.0  # estimate
        self.p = 1.0  # error variance
        self.q = process_noise
        self.r = measurement_noise

    def predict(self, dt: float = 1.0, velocity: float = 0.0) -> None:
        self.x += velocity * dt
        self.p += self.q

    def update(self, measurement: float) -> None:
        k = self.p / (self.p + self.r)
        self.x += k * (measurement - self.x)
        self.p = (1 - k) * self.p


# ---------- Convenience runners ----------


def run_until(world: World, condition: Callable[[World], bool], max_time: float = 10.0) -> None:
    while world.time < max_time:
        world.step(1, record=True)
        if condition(world):
            break
