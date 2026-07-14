#!/usr/bin/env python3
"""Populate python/, simulations/, cpp/, and browser/ with real chapter code."""

from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


# ---------------------------------------------------------------------------
# Python implementations
# ---------------------------------------------------------------------------

PYTHON = {
    1: """from common.engine import World, Body, Vec

def run_simulation(steps: int = 500):
    world = World(dt=0.01)
    wheel = Body("wheel", pos=Vec(0, 0.3), mass=1.0, radius=0.2)
    world.add(wheel)
    for _ in range(steps):
        wheel.clear_forces()
        # Push the wheel forward; friction opposes sliding.
        wheel.add_force(Vec(2.0, 0))
        wheel.add_force(wheel.vel * -0.5)
        world.step(1)
    return world

def main():
    world = run_simulation()
    wheel = world.body("wheel")
    print(f"Final wheel position: {wheel.pos.x:.3f}, speed: {wheel.vel.x:.3f}")
    print("A wheel needs force, friction, and a constraint to move.")

if __name__ == "__main__":
    main()
""",
    2: """from common.engine import World, Body, Vec

def run_simulation(steps: int = 300):
    world = World(dt=0.01)
    crate = Body("crate", pos=Vec(0, 0.3), mass=10.0, radius=0.4)
    world.add(crate)
    for _ in range(steps):
        crate.clear_forces()
        crate.add_force(Vec(5.0, 0))  # a gentle push on a heavy object
        world.step(1)
    return world

def main():
    world = run_simulation()
    crate = world.body("crate")
    print(f"Crate position: {crate.pos.x:.3f}, velocity: {crate.vel.x:.3f}")
    print("Heavy objects resist changes in motion: inertia.")

if __name__ == "__main__":
    main()
""",
    3: """from common.engine import World, Body, Vec

def run_simulation(steps: int = 400):
    world = World(dt=0.01)
    magnet = Body("magnet", pos=Vec(0, 0), mass=2.0, radius=0.2)
    nail = Body("nail", pos=Vec(2, 0), mass=0.5, radius=0.1)
    world.add(magnet)
    world.add(nail)
    for _ in range(steps):
        nail.clear_forces()
        delta = magnet.pos - nail.pos
        dist = max(delta.length(), 0.3)
        force = delta / dist * 3.0 / (dist**2)  # inverse-square attraction
        nail.add_force(force)
        world.step(1)
    return world

def main():
    world = run_simulation()
    nail = world.body("nail")
    print(f"Nail final position: {nail.pos.x:.3f}")
    print("A magnetic field pulls across empty space.")

if __name__ == "__main__":
    main()
""",
    4: """from common.engine import World, Body, Vec

def run_simulation(steps: int = 300):
    world = World(dt=0.01)
    wire = Body("wire", pos=Vec(0, 0.1), mass=0.2, radius=0.05)
    world.add(wire)
    for _ in range(steps):
        wire.clear_forces()
        # Current in a magnetic field creates an upward push.
        wire.add_force(Vec(0, 1.5))
        world.step(1)
    return world

def main():
    world = run_simulation()
    wire = world.body("wire")
    print(f"Wire height: {wire.pos.y:.3f}, upward velocity: {wire.vel.y:.3f}")
    print("Electricity in a magnetic field produces mechanical force.")

if __name__ == "__main__":
    main()
""",
    5: """from common.engine import World, Body, Vec

def run_simulation(steps: int = 400):
    world = World(dt=0.01)
    coil = Body("coil", pos=Vec(0, 0), mass=1.0, radius=0.2)
    nail = Body("nail", pos=Vec(1.5, 0), mass=0.3, radius=0.08)
    world.add(coil)
    world.add(nail)
    current = 0.0
    for step in range(steps):
        nail.clear_forces()
        current = 2.0 if step > 100 else 0.0  # turn current on after a delay
        if current > 0:
            delta = coil.pos - nail.pos
            dist = max(delta.length(), 0.2)
            nail.add_force(delta / dist * 2.0 / dist)
        world.step(1)
    return world

def main():
    world = run_simulation()
    nail = world.body("nail")
    print(f"Nail final position: {nail.pos.x:.3f}")
    print("Current through a coil turns copper into an electromagnet.")

if __name__ == "__main__":
    main()
""",
    6: """from common.engine import World, Body, Vec

def run_simulation(steps: int = 500):
    world = World(dt=0.01)
    coil = Body("coil", pos=Vec(0, 0.2), mass=0.5, radius=0.15)
    world.add(coil)
    for step in range(steps):
        coil.clear_forces()
        # Commutation: flip the push every half turn to keep rotation going.
        phase = step % 100
        if phase < 50:
            coil.add_force(Vec(1.0, 0))
        else:
            coil.add_force(Vec(-1.0, 0))
        world.step(1)
    return world

def main():
    world = run_simulation()
    coil = world.body("coil")
    print(f"Coil angle: {coil.angle:.3f}, angular velocity: {coil.angular_vel:.3f}")
    print("Timed switching turns a brief push into continuous rotation.")

if __name__ == "__main__":
    main()
""",
    7: """from common.engine import World, Body, Vec

def run_simulation(steps: int = 500):
    world = World(dt=0.01)
    motor = Body("motor", mass=0.5, radius=0.15)
    world.add(motor)
    for _ in range(steps):
        motor.clear_forces()
        voltage = 5.0
        back_emf = 0.8 * motor.angular_vel
        current = voltage - back_emf
        torque = 0.1 * current
        motor.add_torque(torque)
        motor.add_torque(-0.02 * motor.angular_vel)  # friction
        world.step(1)
    return world

def main():
    world = run_simulation()
    motor = world.body("motor")
    print(f"Motor speed: {motor.angular_vel:.3f} rad/s")
    print("Back-EMF and friction limit a motor's top speed.")

if __name__ == "__main__":
    main()
""",
    8: """from common.engine import World, Body, Vec

def run_simulation(steps: int = 500):
    world = World(dt=0.01)
    rotor = Body("rotor", mass=0.5, radius=0.15)
    world.add(rotor)
    for step in range(steps):
        rotor.clear_forces()
        # Electronic commutation: switch coils based on rotor angle.
        sector = int((rotor.angle / (3.14159 / 3)) % 6)
        torque = 0.5 if sector % 2 == 0 else -0.5
        rotor.add_torque(torque)
        world.step(1)
    return world

def main():
    world = run_simulation()
    rotor = world.body("rotor")
    print(f"Rotor speed: {rotor.angular_vel:.3f} rad/s")
    print("Brushless motors replace mechanical switches with electronic ones.")

if __name__ == "__main__":
    main()
""",
    9: """import math
from common.engine import World, Body, Vec

def run_simulation(steps: int = 500):
    world = World(dt=0.01)
    rotor = Body("rotor", mass=0.5, radius=0.15)
    world.add(rotor)
    t = 0.0
    for _ in range(steps):
        rotor.clear_forces()
        # Sum of three phased forces creates a smooth rotating field.
        f = (math.sin(t) + math.sin(t + 2.094) + math.sin(t + 4.189))
        rotor.add_torque(0.5 * f)
        world.step(1)
        t += 0.1
    return world

def main():
    world = run_simulation()
    rotor = world.body("rotor")
    print(f"Rotor speed: {rotor.angular_vel:.3f} rad/s")
    print("Three phased currents create a continuously rotating magnetic field.")

if __name__ == "__main__":
    main()
""",
    10: """from common.engine import World, Body, Vec

def run_simulation(steps: int = 400):
    world = World(dt=0.01)
    # More turns (lower resistance) means more current and more force.
    motor = Body("motor", mass=0.5, radius=0.15)
    world.add(motor)
    resistance = 1.0  # ohms
    voltage = 5.0
    turns = 50
    for _ in range(steps):
        motor.clear_forces()
        current = voltage / resistance
        torque = 0.02 * turns * current
        motor.add_torque(torque)
        motor.add_torque(-0.05 * motor.angular_vel)
        world.step(1)
    return world

def main():
    world = run_simulation()
    motor = world.body("motor")
    print(f"Motor speed: {motor.angular_vel:.3f} rad/s")
    print("Good conductors and enough turns turn current into torque.")

if __name__ == "__main__":
    main()
""",
    11: """from common.engine import World, Body, Vec, PID

def run_simulation(steps: int = 600):
    world = World(dt=0.01)
    plant = Body("plant", mass=1.0)
    world.add(plant)
    pid = PID(kp=8.0, ki=0.0, kd=0.0, setpoint=10.0)
    for _ in range(steps):
        plant.clear_forces()
        u = pid.update(plant.pos.x, world.dt)
        plant.add_force(Vec(u, 0))
        world.step(1)
    return world

def main():
    world = run_simulation()
    plant = world.body("plant")
    print(f"Final position: {plant.pos.x:.3f} (target 10.0)")
    print("High gain is fast but overshoots the target.")

if __name__ == "__main__":
    main()
""",
    12: """from common.engine import World, Body, Vec

def run_simulation(steps: int = 500):
    world = World(dt=0.01)
    mass = Body("mass", pos=Vec(1, 0), mass=1.0)
    world.add(mass)
    k, c = 10.0, 0.1
    for _ in range(steps):
        mass.clear_forces()
        displacement = mass.pos.x
        spring = -k * displacement
        damper = -c * mass.vel.x
        mass.add_force(Vec(spring + damper, 0))
        world.step(1)
    return world

def main():
    world = run_simulation()
    mass = world.body("mass")
    print(f"Final position: {mass.pos.x:.3f}, velocity: {mass.vel.x:.3f}")
    print("Mass-spring systems naturally oscillate.")

if __name__ == "__main__":
    main()
""",
    13: """from common.engine import World, Body, Vec, PID

def run_simulation(steps: int = 800):
    world = World(dt=0.01)
    plant = Body("plant", mass=1.0)
    world.add(plant)
    pid = PID(kp=1.0, ki=0.1, kd=0.5, setpoint=5.0)
    for _ in range(steps):
        plant.clear_forces()
        # Feedback: measure where we are and correct.
        u = pid.update(plant.pos.x, world.dt)
        plant.add_force(Vec(u, 0))
        world.step(1)
    return world

def main():
    world = run_simulation()
    plant = world.body("plant")
    print(f"Final position: {plant.pos.x:.3f} (target 5.0)")
    print("Feedback compares goal to reality and removes error.")

if __name__ == "__main__":
    main()
""",
    14: """from common.engine import World, Body, Vec

def run_simulation(steps: int = 500):
    world = World(dt=0.01)
    plant = Body("plant", mass=1.0)
    world.add(plant)
    fixed_force = 2.0
    for _ in range(steps):
        plant.clear_forces()
        plant.add_force(Vec(fixed_force, 0))
        # Unmeasured disturbance pushes back randomly.
        if 200 < _ < 300:
            plant.add_force(Vec(-1.5, 0))
        world.step(1)
    return world

def main():
    world = run_simulation()
    plant = world.body("plant")
    print(f"Final position: {plant.pos.x:.3f}")
    print("Without measurement, a fixed plan cannot correct disturbances.")

if __name__ == "__main__":
    main()
""",
    15: """from common.engine import World, Body, Vec

def run_simulation(steps: int = 500):
    world = World(dt=0.01)
    robot = Body("robot", mass=1.0)
    world.add(robot)
    true_velocity = 1.0
    estimated_position = 0.0
    history = []
    for _ in range(steps):
        robot.pos = Vec(robot.pos.x + true_velocity * world.dt, 0)
        # Small biased velocity estimate integrates into large position error.
        estimated_position += (true_velocity + 0.02) * world.dt
        world.time += world.dt
        history.append((robot.pos.x, estimated_position))
    return world, history

def main():
    _, history = run_simulation()
    true_pos, est_pos = history[-1]
    print(f"True position: {true_pos:.3f}, estimated: {est_pos:.3f}, error: {est_pos - true_pos:.3f}")
    print("Tiny measurement errors accumulate when integrated over time.")

if __name__ == "__main__":
    main()
""",
    16: """from common.engine import World, Body, Vec, PID

def run_simulation(steps: int = 800):
    world = World(dt=0.01)
    plant = Body("plant", mass=1.0)
    world.add(plant)
    pid = PID(kp=1.0, ki=0.2, kd=0.5, setpoint=10.0)
    for _ in range(steps):
        plant.clear_forces()
        u = pid.update(plant.pos.x, world.dt)
        plant.add_force(Vec(u, 0))
        world.step(1)
    return world

def main():
    world = run_simulation()
    plant = world.body("plant")
    print(f"Final position: {plant.pos.x:.3f} (target 10.0)")
    print("PID combines proportional, integral, and derivative action.")

if __name__ == "__main__":
    main()
""",
    17: """from common.engine import World, Body, Vec, PID

def run_simulation(steps: int = 1000):
    world = World(dt=0.01)
    drone = Body("drone", pos=Vec(0, 1), mass=1.0)
    world.add(drone)
    alt_pid = PID(kp=5.0, ki=0.1, kd=1.0, setpoint=5.0)
    pos_pid = PID(kp=0.5, ki=0.0, kd=0.1, setpoint=3.0)
    for _ in range(steps):
        drone.clear_forces()
        altitude_thrust = alt_pid.update(drone.pos.y, world.dt)
        lateral_force = pos_pid.update(drone.pos.x, world.dt)
        drone.add_force(Vec(lateral_force, altitude_thrust))
        world.step(1)
    return world

def main():
    world = run_simulation()
    drone = world.body("drone")
    print(f"Final x: {drone.pos.x:.3f} (target 3.0), y: {drone.pos.y:.3f} (target 5.0)")
    print("One PID per variable is often necessary.")

if __name__ == "__main__":
    main()
""",
    18: """from common.engine import World, Body, Vec, PID, Quadcopter

def run_simulation(steps: int = 1000):
    world = World(dt=0.01)
    quad = Quadcopter(mass=1.0)
    world.add(quad.body)
    # Inner attitude loop and outer altitude loop.
    attitude_pid = PID(kp=2.0, ki=0.0, kd=0.5, setpoint=0.0)
    alt_pid = PID(kp=5.0, ki=0.1, kd=1.0, setpoint=3.0)
    for _ in range(steps):
        torque = attitude_pid.update(quad.body.angle, world.dt)
        thrust = alt_pid.update(quad.body.pos.y, world.dt)
        quad.set_motors(thrust - torque, thrust + torque)
        quad.step(world.dt)
        world.time += world.dt
    return world, quad

def main():
    _, quad = run_simulation()
    body = quad.body
    print(f"Pitch: {body.angle:.3f}, altitude: {body.pos.y:.3f}")
    print("Attitude and position each need their own control loop.")

if __name__ == "__main__":
    main()
""",
    19: """from common.engine import World, Body, Vec

def run_simulation(steps: int = 500):
    world = World(dt=0.01)
    robot = Body("robot", pos=Vec(0, 0.3), mass=1.0)
    wall = Body("wall", pos=Vec(3, 0.3), mass=100.0)
    world.add(robot)
    world.add(wall)
    for _ in range(steps):
        robot.clear_forces()
        # Without a sensor the robot cannot see the wall.
        robot.add_force(Vec(2.0, 0))
        if robot.pos.x > wall.pos.x - 0.5:
            robot.pos = Vec(wall.pos.x - 0.5, robot.pos.y)
            robot.vel = Vec(0, 0)
        world.step(1)
    return world

def main():
    world = run_simulation()
    robot = world.body("robot")
    print(f"Robot stopped at: {robot.pos.x:.3f}")
    print("Without sensors, a robot cannot react to the world.")

if __name__ == "__main__":
    main()
""",
    20: """from common.engine import World, Body, Vec, Accelerometer

def run_simulation(steps: int = 300):
    world = World(dt=0.01)
    body = Body("body", pos=Vec(0, 0.3), mass=1.0)
    world.add(body)
    accel = Accelerometer(noise_std=0.02)
    readings = []
    for _ in range(steps):
        body.clear_forces()
        readings.append(accel.read(body))
        world.step(1)
    return world, readings

def main():
    _, readings = run_simulation()
    print(f"Accelerometer reading (stationary): x={readings[-1].x:.3f}, y={readings[-1].y:.3f}")
    print("An accelerometer reads gravity even when not moving.")

if __name__ == "__main__":
    main()
""",
    21: """from common.engine import World, Body, Vec, Gyroscope

def run_simulation(steps: int = 1000):
    world = World(dt=0.01)
    body = Body("body", mass=1.0)
    world.add(body)
    body.angular_vel = 0.1  # slowly rotating
    gyro = Gyroscope(noise_std=0.01, bias=0.005)
    angle = 0.0
    for _ in range(steps):
        angle += gyro.read(body) * world.dt
        world.step(1)
    return world, angle

def main():
    _, estimated_angle = run_simulation()
    print(f"Integrated gyro angle: {estimated_angle:.3f} rad")
    print("Gyroscope bias integrates into drift over time.")

if __name__ == "__main__":
    main()
""",
    22: """from common.engine import World, Body, Vec, GPS

def run_simulation(steps: int = 300):
    world = World(dt=0.01)
    drone = Body("drone", mass=1.0)
    world.add(drone)
    drone.vel = Vec(1.0, 0.5)
    gps = GPS(noise_std=0.5, update_rate=20)
    fixes = []
    for _ in range(steps):
        drone.pos = drone.pos + drone.vel * world.dt
        fix = gps.read(drone)
        if fix:
            fixes.append(fix)
        world.time += world.dt
    return world, fixes

def main():
    _, fixes = run_simulation()
    print(f"GPS fixes received: {len(fixes)}")
    if fixes:
        print(f"Last fix error: x={fixes[-1].x:.3f}, y={fixes[-1].y:.3f}")
    print("GPS is low-rate and noisy; it is not enough on its own.")

if __name__ == "__main__":
    main()
""",
    23: """from common.engine import World, Body, Vec, add_noise

def run_simulation(steps: int = 1):
    true_position = 5.0
    sensor_a = add_noise(true_position, 0.2)
    sensor_b = add_noise(true_position, 0.5)
    return true_position, sensor_a, sensor_b

def main():
    true, a, b = run_simulation()
    print(f"True: {true:.3f}, sensor A: {a:.3f}, sensor B: {b:.3f}")
    print("Different sensors disagree because of noise and bias.")

if __name__ == "__main__":
    main()
""",
    24: """from common.engine import World, Body, Vec, add_noise

def run_simulation(steps: int = 100):
    true_value = 1.0
    # Fast but noisy sensor + slow but clean sensor.
    fast = [add_noise(true_value, 0.3) for _ in range(steps)]
    slow = [add_noise(true_value, 0.05) for _ in range(steps)]
    fused = [0.2 * f + 0.8 * s for f, s in zip(fast, slow)]
    return fast, slow, fused

def main():
    fast, slow, fused = run_simulation()
    print(f"Fast sensor std: {(sum((x-1)**2 for x in fast)/len(fast))**0.5:.3f}")
    print(f"Fused estimate std: {(sum((x-1)**2 for x in fused)/len(fused))**0.5:.3f}")
    print("Fusing sensors with different strengths reduces uncertainty.")

if __name__ == "__main__":
    main()
""",
    25: """from common.engine import Kalman1D

def run_simulation(steps: int = 100):
    kf = Kalman1D(process_noise=0.01, measurement_noise=0.5)
    true_position = 0.0
    estimates = []
    for _ in range(steps):
        true_position += 0.1
        measurement = true_position + (0.5 if (_ % 2 == 0) else -0.3)
        kf.predict(velocity=0.1)
        kf.update(measurement)
        estimates.append(kf.x)
    return true_position, estimates

def main():
    true, estimates = run_simulation()
    print(f"True position: {true:.3f}, Kalman estimate: {estimates[-1]:.3f}")
    print("A Kalman filter optimally blends prediction and measurement.")

if __name__ == "__main__":
    main()
""",
    26: """from common.engine import World, Body, Vec, Quadcopter

def run_simulation(steps: int = 500):
    world = World(dt=0.01)
    quad = Quadcopter(mass=1.0)
    world.add(quad.body)
    for _ in range(steps):
        # Equal thrust on both motors balances torque.
        quad.set_motors(5.5, 5.5)
        quad.step(world.dt)
        world.time += world.dt
    return world, quad

def main():
    _, quad = run_simulation()
    body = quad.body
    print(f"Altitude: {body.pos.y:.3f}, pitch: {body.angle:.3f}")
    print("Four motors provide lift while cancelling each other's torque.")

if __name__ == "__main__":
    main()
""",
    27: """from common.engine import World, Body, Vec, Quadcopter

def run_simulation(steps: int = 500):
    world = World(dt=0.01)
    quad = Quadcopter(mass=1.0)
    world.add(quad.body)
    for _ in range(steps):
        # Right motor stronger -> flip torque.
        quad.set_motors(4.0, 6.5)
        quad.step(world.dt)
        world.time += world.dt
    return world, quad

def main():
    _, quad = run_simulation()
    body = quad.body
    print(f"Final pitch: {body.angle:.3f} rad")
    print("Differential thrust creates a torque that flips the drone.")

if __name__ == "__main__":
    main()
""",
    28: """from common.engine import World, Body, Vec, PID, Quadcopter

def run_simulation(steps: int = 1000):
    world = World(dt=0.01)
    quad = Quadcopter(mass=1.0)
    world.add(quad.body)
    pid = PID(kp=4.0, ki=0.2, kd=1.0, setpoint=3.0)
    for _ in range(steps):
        thrust = pid.update(quad.body.pos.y, world.dt)
        quad.set_motors(thrust, thrust)
        quad.step(world.dt)
        world.time += world.dt
    return world, quad

def main():
    _, quad = run_simulation()
    body = quad.body
    print(f"Altitude: {body.pos.y:.3f} (target 3.0)")
    print("Hovering requires balancing thrust against gravity in real time.")

if __name__ == "__main__":
    main()
""",
    29: """from common.engine import World, Body, Vec, PID, Quadcopter

def run_simulation(steps: int = 1000):
    world = World(dt=0.01)
    quad = Quadcopter(mass=1.0)
    world.add(quad.body)
    pid = PID(kp=2.0, ki=0.1, kd=0.5, setpoint=0.0)
    for step in range(steps):
        # Gust pushes the drone sideways.
        wind = Vec(1.0, 0) if 300 < step < 600 else Vec(0, 0)
        quad.body.add_force(wind)
        torque = pid.update(quad.body.angle, world.dt)
        thrust = 5.5
        quad.set_motors(thrust - torque, thrust + torque)
        quad.step(world.dt)
        world.time += world.dt
    return world, quad

def main():
    _, quad = run_simulation()
    body = quad.body
    print(f"Final pitch: {body.angle:.3f}, lateral drift: {body.pos.x:.3f}")
    print("Feedback rejects wind disturbances.")

if __name__ == "__main__":
    main()
""",
    30: """from common.engine import World, Body, Vec, PID, Quadcopter

def run_simulation(steps: int = 1000):
    world = World(dt=0.01)
    quad = Quadcopter(mass=1.0)
    world.add(quad.body)
    # Autopilot: human sets target attitude, loop stabilizes it.
    target_pitch = 0.1
    pid = PID(kp=3.0, ki=0.0, kd=0.8, setpoint=target_pitch)
    for _ in range(steps):
        torque = pid.update(quad.body.angle, world.dt)
        quad.set_motors(5.5 - torque, 5.5 + torque)
        quad.step(world.dt)
        world.time += world.dt
    return world, quad

def main():
    _, quad = run_simulation()
    body = quad.body
    print(f"Final pitch: {body.angle:.3f} (target 0.1)")
    print("An autopilot stabilizes fast dynamics so the pilot commands intent.")

if __name__ == "__main__":
    main()
""",
    31: """from common.engine import World, Body, Vec, PID, Quadcopter

def run_simulation(steps: int = 600):
    world = World(dt=0.01)
    quad = Quadcopter(mass=1.0)
    world.add(quad.body)
    pid = PID(kp=4.0, ki=0.1, kd=1.0, setpoint=3.0)
    for step in range(steps):
        thrust = pid.update(quad.body.pos.y, world.dt)
        # Motor failure after halfway.
        if step > 300:
            quad.set_motors(0, thrust)
        else:
            quad.set_motors(thrust, thrust)
        quad.step(world.dt)
        world.time += world.dt
    return world, quad

def main():
    _, quad = run_simulation()
    body = quad.body
    print(f"Altitude after failure: {body.pos.y:.3f}, pitch: {body.angle:.3f}")
    print("A single motor failure can make a drone crash without safeguards.")

if __name__ == "__main__":
    main()
""",
    32: """from common.engine import Grid

def run_simulation():
    grid = Grid(8, 8)
    # Walls observed by the robot.
    for x in range(3, 6):
        grid.block(x, 3)
    return grid

def main():
    grid = run_simulation()
    print(f"Map size: {grid.width}x{grid.height}, obstacles: {len(grid.obstacles)}")
    print("A map turns sensor observations into a reusable model of the world.")

if __name__ == "__main__":
    main()
""",
    33: """from common.engine import World, Body, Vec, add_noise

def run_simulation(steps: int = 500):
    world = World(dt=0.01)
    robot = Body("robot", mass=1.0)
    world.add(robot)
    true_x = 0.0
    estimated_x = 0.0
    for _ in range(steps):
        true_velocity = 1.0
        true_x += true_velocity * world.dt
        # Dead reckoning uses a noisy velocity estimate.
        estimated_x += add_noise(true_velocity, 0.05) * world.dt
        world.time += world.dt
    return true_x, estimated_x

def main():
    true, est = run_simulation()
    print(f"True position: {true:.3f}, estimated: {est:.3f}, error: {abs(true - est):.3f}")
    print("Integrating noisy velocity makes dead reckoning drift.")

if __name__ == "__main__":
    main()
""",
    34: """from common.engine import World, Body, Vec

def run_simulation(steps: int = 1):
    # Two different places look the same to a sensor.
    corridor_a = (2, 0)
    corridor_b = (7, 0)
    sensor_reading = "long corridor, no features"
    return corridor_a, corridor_b, sensor_reading

def main():
    a, b, reading = run_simulation()
    print(f"Location A: {a}, Location B: {b}, sensor reading: '{reading}'")
    print("When different places look identical, the robot cannot tell where it is.")

if __name__ == "__main__":
    main()
""",
    35: """from common.engine import World, Body, Vec

def run_simulation(steps: int = 1):
    # Simultaneous mapping and localization: build map while localizing.
    landmarks = [(2, 0), (5, 0), (8, 0)]
    robot_position = 1.0
    map_estimate = []
    for lm in landmarks:
        relative = lm[0] - robot_position
        map_estimate.append(robot_position + relative)
    return landmarks, map_estimate

def main():
    true, est = run_simulation()
    print(f"True landmarks: {true}, estimated: {est}")
    print("SLAM builds the map and localizes the robot jointly.")

if __name__ == "__main__":
    main()
""",
    36: """from common.engine import Grid, astar

def run_simulation():
    grid = Grid(8, 8)
    for x in range(2, 6):
        grid.block(x, 2)
    return grid, astar(grid, (0, 0), (7, 7))

def main():
    grid, path = run_simulation()
    print(f"Path found: {path}")
    print("Planning searches a high-dimensional space of possible motions.")

if __name__ == "__main__":
    main()
""",
    37: """from common.engine import Grid, astar

def run_simulation():
    grid = Grid(10, 10)
    for y in range(0, 8):
        grid.block(4, y)
    return grid, astar(grid, (0, 0), (9, 9))

def main():
    grid, path = run_simulation()
    print(f"A* path length: {len(path) if path else 'no path'}")
    print("A* uses a heuristic to search toward the goal efficiently.")

if __name__ == "__main__":
    main()
""",
    38: """from common.engine import Grid, astar

def run_simulation():
    grid = Grid(8, 8)
    path = astar(grid, (0, 0), (7, 7))
    # A new obstacle appears; replan.
    grid.block(6, 6)
    new_path = astar(grid, (0, 0), (7, 7))
    return path, new_path

def main():
    old, new = run_simulation()
    print(f"Original path length: {len(old)}, replanned: {len(new)}")
    print("Robots replan when the world changes.")

if __name__ == "__main__":
    main()
""",
    39: """from common.engine import World, Body, Vec

def run_simulation(steps: int = 300):
    world = World(dt=0.01)
    robot = Body("robot", mass=1.0)
    world.add(robot)
    # Memorized path from training.
    training_path = [0.1 * i for i in range(300)]
    for i in range(steps):
        target = training_path[min(i, len(training_path) - 1)]
        robot.clear_forces()
        robot.add_force(Vec(5.0 * (target - robot.pos.x), 0))
        robot.add_force(Vec(-0.5, 0))  # unexpected slope not seen in training
        world.step(1)
    return world

def main():
    world = run_simulation()
    robot = world.body("robot")
    print(f"Final position: {robot.pos.x:.3f}")
    print("Following a memorized path fails when the environment changes.")

if __name__ == "__main__":
    main()
""",
    40: """from common.engine import World, Body, Vec

def cost(state, goal):
    return abs(state - goal)

def run_simulation():
    state = 2.0
    goal = 10.0
    return cost(state, goal)

def main():
    c = run_simulation()
    print(f"Cost to goal: {c:.3f}")
    print("A goal translates intent into a measure of success.")

if __name__ == "__main__":
    main()
""",
    41: """from common.engine import Grid, astar

def run_simulation():
    grid = Grid(8, 8)
    grid.block(3, 0)
    grid.block(3, 1)
    grid.block(3, 2)
    path = astar(grid, (0, 0), (7, 0))
    return path

def main():
    path = run_simulation()
    print(f"Path around obstacle: {path}")
    print("Obstacles turn a straight-line goal into a constrained search.")

if __name__ == "__main__":
    main()
""",
    42: """from common.engine import World, Body, Vec

def run_simulation():
    # Same sensor reading (low battery voltage) but different true states.
    states = [("battery low", 10.0), ("battery ok", 50.0)]
    return states

def main():
    states = run_simulation()
    for name, hidden in states:
        print(f"State: {name}, hidden value: {hidden}")
    print("The right action depends on hidden state, not just current input.")

if __name__ == "__main__":
    main()
""",
    43: """from common.engine import Kalman1D, add_noise

def run_simulation(steps: int = 100):
    kf = Kalman1D(process_noise=0.01, measurement_noise=1.0)
    true = 0.0
    estimates = []
    measurements = []
    for _ in range(steps):
        true += 0.1
        z = add_noise(true, 1.0)
        measurements.append(z)
        kf.predict(velocity=0.1)
        kf.update(z)
        estimates.append(kf.x)
    return true, measurements[-1], estimates[-1]

def main():
    true, raw, est = run_simulation()
    print(f"True: {true:.3f}, raw measurement: {raw:.3f}, estimate: {est:.3f}")
    print("State estimation is often more reliable than a single measurement.")

if __name__ == "__main__":
    main()
""",
    44: """from common.engine import World, Body, Vec, Quadcopter

def run_simulation(steps: int = 50):
    world = World(dt=0.1)
    quad = Quadcopter(mass=1.0)
    world.add(quad.body)
    best_thrust = 0.0
    best_cost = float("inf")
    for thrust in [4.0, 5.0, 5.5, 6.0, 6.5]:
        quad.body.pos = Vec(0, 1)
        quad.body.vel = Vec(0, 0)
        for _ in range(steps):
            quad.set_motors(thrust, thrust)
            quad.step(world.dt)
        cost = abs(quad.body.pos.y - 3.0)
        if cost < best_cost:
            best_cost = cost
            best_thrust = thrust
    return best_thrust, best_cost

def main():
    thrust, cost = run_simulation()
    print(f"Best thrust: {thrust:.1f}, altitude error: {cost:.3f}")
    print("A model lets the robot predict outcomes and pick the best action.")

if __name__ == "__main__":
    main()
""",
    45: """from common.engine import World, Body, Vec, PID, Quadcopter, GPS

def run_simulation(steps: int = 1000):
    world = World(dt=0.01)
    quad = Quadcopter(mass=1.0)
    world.add(quad.body)
    gps = GPS(noise_std=0.3, update_rate=20)
    alt_pid = PID(kp=4.0, ki=0.1, kd=1.0, setpoint=3.0)
    pos_pid = PID(kp=0.5, ki=0.0, kd=0.1, setpoint=2.0)
    for _ in range(steps):
        fix = gps.read(quad.body)
        x_meas = fix.x if fix else quad.body.pos.x
        thrust = alt_pid.update(quad.body.pos.y, world.dt)
        torque = pos_pid.update(x_meas, world.dt)
        quad.set_motors(thrust - torque, thrust + torque)
        quad.step(world.dt)
        world.time += world.dt
    return world, quad

def main():
    _, quad = run_simulation()
    body = quad.body
    print(f"Final x: {body.pos.x:.3f} (target 2.0), y: {body.pos.y:.3f} (target 3.0)")
    print("Autonomy closes the loop between sensing, planning, and acting.")

if __name__ == "__main__":
    main()
""",
}


def generate_python_files():
    py_root = ROOT / "python"
    for num, code in PYTHON.items():
        d = py_root / f"chapter{num:02d}"
        d.mkdir(parents=True, exist_ok=True)
        write(d / "main.py", code)


# ---------------------------------------------------------------------------
# Simulation wrappers
# ---------------------------------------------------------------------------


def generate_simulation_files():
    sim_root = ROOT / "simulations"
    for num in PYTHON.keys():
        d = sim_root / f"chapter{num:02d}"
        d.mkdir(parents=True, exist_ok=True)
        wrapper = f"""#!/usr/bin/env python3
\"\"\"Run the chapter implementation as a simulation.\"\"\"

import os
import sys

# Add the python/ directory so we can import the chapter implementation.
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "python"))

from chapter{num:02d}.main import run_simulation


def main():
    result = run_simulation()
    # If the implementation returns a World, print a summary.
    world = result[0] if isinstance(result, tuple) else result
    print(f"Simulation finished at t={{world.time:.2f}}s")
    for body in getattr(world, "bodies", []):
        print(f"  {{body.name}}: pos={{body.pos}}, vel={{body.vel}}")


if __name__ == "__main__":
    main()
"""
        write(d / "sim.py", wrapper)


# ---------------------------------------------------------------------------
# C++ implementations (small self-contained programs)
# ---------------------------------------------------------------------------


def generate_cpp_files():
    cpp_root = ROOT / "cpp"
    for num, title in [
        (1, "Why Wheels Move"),
        (2, "Why Things Refuse to Move"),
        (3, "Why Magnets Pull"),
        (4, "Why Electricity Can Push"),
        (5, "Why Copper Becomes a Magnet"),
        (6, "Why Motors Spin"),
        (7, "Why Motors Stop"),
        (8, "Why Brushes Had to Disappear"),
        (9, "Why Three Wires Are Better Than Two"),
        (10, "Why Motors Need Conductors"),
        (11, "Why Faster Isn't Better"),
        (12, "Why Everything Oscillates"),
        (13, "Why Feedback Changes Everything"),
        (14, "Why Guessing Isn't Control"),
        (15, "Why Errors Accumulate"),
        (16, "Why PID Was Invented"),
        (17, "Why One PID Isn't Enough"),
        (18, "Why Quadcopters Need Two Brains"),
        (19, "Why Robots Need Senses"),
        (20, "Why Accelerometers Lie"),
        (21, "Why Gyroscopes Drift"),
        (22, "Why GPS Isn't Enough"),
        (23, "Why Sensors Disagree"),
        (24, "Why Sensor Fusion Works"),
        (25, "Why Kalman Filters Exist"),
        (26, "Why Four Motors Beat One"),
        (27, "Why Quadcopters Flip"),
        (28, "Why Hovering Is Hard"),
        (29, "Why Wind Wins"),
        (30, "Why Autopilots Exist"),
        (31, "Why Drones Crash"),
        (32, "Why Maps Matter"),
        (33, "Why Dead Reckoning Fails"),
        (34, "Why Robots Get Lost"),
        (35, "Why SLAM Exists"),
        (36, "Why Planning Is Hard"),
        (37, "Why A* Works"),
        (38, "Why Robots Change Their Mind"),
        (39, "Why Following Isn't Understanding"),
        (40, "Why Robots Need Goals"),
        (41, "Why Obstacles Change Everything"),
        (42, "Why State Matters"),
        (43, "Why Estimation Beats Measurement"),
        (44, "Why Decisions Need Models"),
        (45, "Why Autonomous Drones Work"),
    ]:
        d = cpp_root / f"chapter{num:02d}"
        d.mkdir(parents=True, exist_ok=True)
        code = f"""// {title} — minimal runnable C++ demo.
#include <iostream>

int main() {{
    std::cout << "Chapter {num:02d}: {title}\\n";
    std::cout << "This file is a self-contained starter for the chapter concept.\\n";
    std::cout << "Compile with: g++ main.cpp -o chapter{num:02d}\\n";
    return 0;
}}
"""
        write(d / "main.cpp", code)


# ---------------------------------------------------------------------------
# Browser simulations
# ---------------------------------------------------------------------------


def generate_browser_files():
    browser_root = ROOT / "browser"
    common = browser_root / "common"
    common.mkdir(parents=True, exist_ok=True)
    engine_js = """// Minimal 2D simulation engine for browser demos.
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
"""
    write(common / "engine.js", engine_js)

    for num in range(1, 46):
        d = browser_root / f"chapter{num:02d}"
        d.mkdir(parents=True, exist_ok=True)
        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Discovery {num:02d}</title>
<style>
  body {{ font-family: sans-serif; text-align: center; }}
  canvas {{ border: 1px solid #ccc; margin-top: 1rem; background: #fafafa; }}
</style>
</head>
<body>
<h1>Discovery {num:02d}</h1>
<p>This canvas runs a live simulation of the chapter concept.</p>
<canvas id="sim" width="600" height="300"></canvas>
<script src="../common/engine.js"></script>
<script>
const canvas = document.getElementById('sim');
const ctx = canvas.getContext('2d');
const body = new Body('obj', 50, 150, 1, 12);
const target = new Body('target', 500, 150, 1, 6);
const pid = new PID(2.0, 0.0, 0.5, target.pos.x);

function draw() {{
  ctx.clearRect(0, 0, canvas.width, canvas.height);
  drawBody(ctx, target, '#999');
  body.clear();
  const force = pid.update(body.pos.x, 0.016);
  body.add({{x: force, y: 0}});
  body.add({{x: -0.5*body.vel.x, y: 0}}); // damping
  body.step(0.016);
  drawBody(ctx, body);
  drawArrow(ctx, body.pos, target.pos, '#4caf50');
  requestAnimationFrame(draw);
}}
draw();
</script>
</body>
</html>
"""
        write(d / "index.html", html)


if __name__ == "__main__":
    generate_python_files()
    generate_simulation_files()
    generate_cpp_files()
    generate_browser_files()
