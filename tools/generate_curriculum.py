#!/usr/bin/env python3
"""Generate the full Building Autonomous Robots curriculum scaffold."""

import os
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
GITHUB_BASE = "https://github.com/ishmum123/building-autonomous-robots/blob/main"

CHAPTER_SEEDS = [
    # Part I — Motion
    {
        "title": "Why Wheels Move",
        "key": "wheel",
        "problem": "You have built a wheel. It is round and it rolls, but left alone on flat ground it does not move. What is missing?",
        "idea": "A wheel only moves when a force, friction, and a constraint work together.",
    },
    {
        "title": "Why Things Refuse to Move",
        "key": "inertia",
        "problem": "You push a heavy crate. It does not budge. Why does the world resist changes in motion?",
        "idea": "Objects resist changes in velocity. This property is called inertia.",
    },
    {
        "title": "Why Magnets Pull",
        "key": "magnetic field",
        "problem": "A magnet and a nail attract each other through empty space. What is happening between them?",
        "idea": "A magnetic field transfers force across a distance.",
    },
    {
        "title": "Why Electricity Can Push",
        "key": "electromagnetic force",
        "problem": "A wire jumps when current flows near a magnet. How can invisible electrons create motion?",
        "idea": "A current in a magnetic field experiences a mechanical force.",
    },
    {
        "title": "Why Copper Becomes a Magnet",
        "key": "electromagnet",
        "problem": "A plain piece of copper does not attract iron, but wrap it with current and it does. Why?",
        "idea": "Electric current creates a magnetic field.",
    },
    {
        "title": "Why Motors Spin",
        "key": "motor",
        "problem": "You have a magnet and a coil. How do you turn a brief push into continuous rotation?",
        "idea": "A motor switches current at the right moment to keep turning.",
    },
    {
        "title": "Why Motors Stop",
        "key": "back-emf and friction",
        "problem": "A motor spins fast when free and slows under load. What fights the motion?",
        "idea": "Friction and back-electromotive force oppose rotation.",
    },
    {
        "title": "Why Brushes Had to Disappear",
        "key": "brushless motor",
        "problem": "Brushes spark, wear out, and limit speed. How can we eliminate them?",
        "idea": "Electronic switching can replace mechanical brushes.",
    },
    {
        "title": "Why Three Wires Are Better Than Two",
        "key": "three-phase field",
        "problem": "A single wire can only push one direction. How do we create a smooth rotating field?",
        "idea": "Three phased currents create a continuously rotating magnetic field.",
    },
    {
        "title": "Why Motors Need Conductors",
        "key": "winding",
        "problem": "A motor coil must carry current without turning into a heater. What makes a good winding?",
        "idea": "Conductors shape where current flows and therefore where force is produced.",
    },
    # Part II — Control
    {
        "title": "Why Faster Isn't Better",
        "key": "overshoot",
        "problem": "You command a motor to full speed. It zooms past the target. Why is maximum response not maximum control?",
        "idea": "Aggressive control causes overshoot and oscillation.",
    },
    {
        "title": "Why Everything Oscillates",
        "key": "oscillation",
        "problem": "A spring with a weight bounces forever in theory. Why do systems swing back and forth?",
        "idea": "Energy trades between storage and motion, producing oscillation.",
    },
    {
        "title": "Why Feedback Changes Everything",
        "key": "feedback loop",
        "problem": "You close your eyes while walking and drift. How does measuring where you are change what you can do?",
        "idea": "Feedback compares goal to reality and corrects the difference.",
    },
    {
        "title": "Why Guessing Isn't Control",
        "key": "open loop control",
        "problem": "You send the same motor command twice and get different results. Why does a fixed plan fail?",
        "idea": "Without measurement, a controller cannot correct disturbances.",
    },
    {
        "title": "Why Errors Accumulate",
        "key": "integration drift",
        "problem": "Small mistakes in direction add up over a long walk. How do tiny errors become huge errors?",
        "idea": "Errors integrate over time, so a controller must remove steady bias.",
    },
    {
        "title": "Why PID Was Invented",
        "key": "PID controller",
        "problem": "Proportional control leaves offset; integral control is slow; derivative control is noisy. How do we combine them?",
        "idea": "PID blends proportional, integral, and derivative responses.",
    },
    {
        "title": "Why One PID Isn't Enough",
        "key": "cascade control",
        "problem": "A drone can hold altitude but drifts horizontally. Why does one controller fail to govern everything?",
        "idea": "Nested controllers handle different time scales and variables.",
    },
    {
        "title": "Why Quadcopters Need Two Brains",
        "key": "attitude and position control",
        "problem": "A quadcopter must stay upright and also stay in place. Are these the same problem?",
        "idea": "Attitude control and position control are separate but coupled loops.",
    },
    # Part III — Sensing
    {
        "title": "Why Robots Need Senses",
        "key": "sensor",
        "problem": "A robot with motors but no sensors bumps into walls. Why is measurement necessary for autonomy?",
        "idea": "Sensors close the loop between the world and the controller.",
    },
    {
        "title": "Why Accelerometers Lie",
        "key": "accelerometer",
        "problem": "An accelerometer reads gravity even when sitting still. How can the same sensor be wrong and right?",
        "idea": "Accelerometers measure specific force, not pure acceleration.",
    },
    {
        "title": "Why Gyroscopes Drift",
        "key": "gyroscope",
        "problem": "A gyroscope gives perfect short-term rotation but drifts over minutes. Why?",
        "idea": "Integration of noisy rate measurements accumulates bias.",
    },
    {
        "title": "Why GPS Isn't Enough",
        "key": "GPS",
        "problem": "GPS tells you where you are, but with delay and uncertainty. Why can't a drone rely only on it?",
        "idea": "Global positioning is low rate and unreliable near obstacles.",
    },
    {
        "title": "Why Sensors Disagree",
        "key": "sensor disagreement",
        "problem": "Two sensors report different positions. Which one is correct?",
        "idea": "Every sensor has noise, bias, and a different frame of reference.",
    },
    {
        "title": "Why Sensor Fusion Works",
        "key": "sensor fusion",
        "problem": "No single sensor is perfect. How can several imperfect sensors become more trustworthy?",
        "idea": "Combining sensors with different strengths reduces overall uncertainty.",
    },
    {
        "title": "Why Kalman Filters Exist",
        "key": "Kalman filter",
        "problem": "You have a model and noisy measurements. How do you trust each just enough?",
        "idea": "A Kalman filter optimally blends prediction and measurement.",
    },
    # Part IV — Flight
    {
        "title": "Why Four Motors Beat One",
        "key": "quadcopter actuation",
        "problem": "One propeller can lift but also spins the body. How do four motors solve this?",
        "idea": "Four motors provide lift and counter-torque simultaneously.",
    },
    {
        "title": "Why Quadcopters Flip",
        "key": "torque imbalance",
        "problem": "If one motor spins faster, the drone tilts or flips. Why?",
        "idea": "Differential thrust creates torques that change attitude.",
    },
    {
        "title": "Why Hovering Is Hard",
        "key": "altitude control",
        "problem": "A quadcopter must fight gravity exactly. Why does it sink or climb?",
        "idea": "Hover requires balancing thrust against weight in real time.",
    },
    {
        "title": "Why Wind Wins",
        "key": "disturbance rejection",
        "problem": "A gust pushes the drone sideways. How can it stay where it was told to be?",
        "idea": "Controllers must reject external disturbances faster than they grow.",
    },
    {
        "title": "Why Autopilots Exist",
        "key": "autopilot",
        "problem": "A human cannot balance a flying machine hundreds of times per second. What takes over?",
        "idea": "An autopilot handles fast stabilization so the human commands intent.",
    },
    {
        "title": "Why Drones Crash",
        "key": "failure mode",
        "problem": "Batteries die, motors fail, and sensors freeze. Why do small failures become crashes?",
        "idea": "Safety margins and fail-safe logic are as important as control.",
    },
    # Part V — Thinking
    {
        "title": "Why Maps Matter",
        "key": "map representation",
        "problem": "A robot can sense walls but gets lost without remembering them. Why does memory help?",
        "idea": "A map turns raw sensor data into a reusable model of the world.",
    },
    {
        "title": "Why Dead Reckoning Fails",
        "key": "dead reckoning",
        "problem": "You estimate position by counting steps, but after a while you are wrong. Why?",
        "idea": "Integrating velocity accumulates error without bounds.",
    },
    {
        "title": "Why Robots Get Lost",
        "key": "localization ambiguity",
        "problem": "A corridor looks the same in two places. How does a robot know which place it is?",
        "idea": "Ambiguity arises when different places look identical.",
    },
    {
        "title": "Why SLAM Exists",
        "key": "SLAM",
        "problem": "You need a map to localize, but you need to localize to build a map. How do you do both?",
        "idea": "SLAM solves mapping and localization jointly.",
    },
    {
        "title": "Why Planning Is Hard",
        "key": "motion planning",
        "problem": "There are infinite paths from here to there. How do you choose a safe one?",
        "idea": "Planning searches a high-dimensional space of possible motions.",
    },
    {
        "title": "Why A* Works",
        "key": "A* search",
        "problem": "You could explore every path, but that is too slow. How do you search smartly?",
        "idea": "A* uses a heuristic to focus search toward the goal.",
    },
    {
        "title": "Why Robots Change Their Mind",
        "key": "replanning",
        "problem": "A new obstacle appears after you planned a path. What should the robot do?",
        "idea": "Replanning updates decisions when the world changes.",
    },
    # Part VI — Autonomy
    {
        "title": "Why Following Isn't Understanding",
        "key": "behavior cloning",
        "problem": "A robot copies a human's path perfectly but fails in a new room. Why?",
        "idea": "Following trajectories does not generalize to new situations.",
    },
    {
        "title": "Why Robots Need Goals",
        "key": "objective function",
        "problem": "A robot can move, but without a goal any motion is as good as another. Why do goals matter?",
        "idea": "Goals translate intent into a measure of success.",
    },
    {
        "title": "Why Obstacles Change Everything",
        "key": "obstacle avoidance",
        "problem": "The straight-line path is blocked. How does a goal become a constraint?",
        "idea": "Obstacles turn free space into a constrained decision problem.",
    },
    {
        "title": "Why State Matters",
        "key": "state representation",
        "problem": "Two robots receive the same sensor reading but should act differently. Why?",
        "idea": "The right action depends on hidden state, not just current input.",
    },
    {
        "title": "Why Estimation Beats Measurement",
        "key": "state estimation",
        "problem": "Sensors are noisy, yet robots act confidently. Where does the confidence come from?",
        "idea": "State estimation infers the most likely true state from noisy data.",
    },
    {
        "title": "Why Decisions Need Models",
        "key": "model predictive control",
        "problem": "You can react to the present, but the best action depends on the future. How?",
        "idea": "A model lets the robot predict outcomes and choose the best sequence.",
    },
    {
        "title": "Why Autonomous Drones Work",
        "key": "full autonomy stack",
        "problem": "How do sensing, planning, control, and state estimation come together to fly by themselves?",
        "idea": "Autonomy is the closed loop of sensing, thinking, and acting.",
    },
]

PART_RANGES = [
    ("Part I — Motion", 1, 10),
    ("Part II — Control", 11, 18),
    ("Part III — Sensing", 19, 25),
    ("Part IV — Flight", 26, 31),
    ("Part V — Thinking", 32, 38),
    ("Part VI — Autonomy", 39, 45),
]


def slugify(title: str) -> str:
    """Create a URL-safe slug from a chapter title."""
    title = title.replace("*", "star")
    title = title.replace("'", "")
    return re.sub(r"[^a-z0-9]+", "-", title.lower().strip()).strip("-")


def chapter_dir(num: int) -> str:
    return f"chapter{num:02d}"


def next_title(chapters, index: int) -> str:
    if index < len(chapters) - 1:
        return chapters[index + 1]["title"]
    return "the next discovery"


def next_slug(chapters, index: int) -> str | None:
    if index < len(chapters) - 1:
        return f"{index + 2:02d}-{slugify(chapters[index + 1]['title'])}.md"
    return None


def generate_docs(chapters):
    docs_root = ROOT / "docs"
    docs_root.mkdir(exist_ok=True)
    for i, ch in enumerate(chapters, start=1):
        slug = f"{i:02d}-{slugify(ch['title'])}.md"
        path = docs_root / slug
        if path.name == "01-why-wheels-move.md":
            # Preserve the hand-written first chapter.
            continue
        nt = next_title(chapters, i - 1)
        ns = next_slug(chapters, i - 1)
        continue_line = f"**Continue → [{nt}]({ns})**" if ns else f"**Continue → {nt}**"
        content = f"""# {ch['title']}

## The Problem

{ch['problem']}

## Thinking

Before we name anything, ask yourself:

- What would happen if the missing piece were absent?
- What is the simplest system that could show this effect?
- Can you draw the interaction before reading the answer?

## Discovery

{ch['idea']}

## Implementation

We build a minimal `{ch['key']}` model in Python.

Source: [`python/{chapter_dir(i)}/main.py`]({GITHUB_BASE}/python/{chapter_dir(i)}/main.py)  ·  [view in browser](assets/simulations/{chapter_dir(i)}/sim.py)

Run the implementation:

```bash
python python/{chapter_dir(i)}/main.py
```

## Simulation

Source: [`simulations/{chapter_dir(i)}/sim.py`]({GITHUB_BASE}/simulations/{chapter_dir(i)}/sim.py)  ·  [view in browser](assets/simulations/{chapter_dir(i)}/sim.py)

Run the chapter simulation:

```bash
python simulations/{chapter_dir(i)}/sim.py
```

A browser version is available at [`browser/{chapter_dir(i)}/index.html`]({GITHUB_BASE}/browser/{chapter_dir(i)}/index.html)  ·  [run live](assets/browser/{chapter_dir(i)}/index.html).

## Exercises

1. Change one parameter in the simulation and predict what will happen.
2. Draw the system before and after the discovery.
3. Name one real-world device that depends on this idea and one way it can fail.

## Engineering Notes

Real systems add noise, latency, and power limits. The model we built is the simplest version; real `{ch['key']}` designs trade accuracy, cost, and reliability.

---

{continue_line}
"""
        path.write_text(content, encoding="utf-8")


def generate_discoveries(chapters):
    disc_root = ROOT / "discoveries"
    disc_root.mkdir(exist_ok=True)
    for i, ch in enumerate(chapters, start=1):
        slug = f"{i:02d}-{slugify(ch['title'])}.md"
        path = disc_root / slug
        nt = next_title(chapters, i - 1)
        ns = next_slug(chapters, i - 1)
        continue_link = f"[{nt}](../docs/{ns})" if ns else nt
        content = f"""# {ch['title']} — Discovery Notes

- **Problem:** {ch['problem']}
- **Key idea:** {ch['idea']}
- **Python:** [`python/{chapter_dir(i)}/main.py`]({GITHUB_BASE}/python/{chapter_dir(i)}/main.py)
- **Simulation:** [`simulations/{chapter_dir(i)}/sim.py`]({GITHUB_BASE}/simulations/{chapter_dir(i)}/sim.py)
- **Browser sim:** [`browser/{chapter_dir(i)}/index.html`]({GITHUB_BASE}/browser/{chapter_dir(i)}/index.html)
- **Continue:** {continue_link}
"""
        path.write_text(content, encoding="utf-8")


def generate_python_stubs(chapters):
    py_root = ROOT / "python"
    py_root.mkdir(exist_ok=True)
    for i, ch in enumerate(chapters, start=1):
        d = py_root / chapter_dir(i)
        d.mkdir(exist_ok=True)
        path = d / "main.py"
        content = f"""#!/usr/bin/env python3
\"\"\"{ch['title']} — minimal implementation stub.\"\"\"


def main():
    print("Chapter {i:02d}: {ch['title']}")
    # Implement the core idea from this chapter here.
    # Start with the simplest version that demonstrates the discovery.


if __name__ == "__main__":
    main()
"""
        path.write_text(content, encoding="utf-8")


def generate_cpp_stubs(chapters):
    cpp_root = ROOT / "cpp"
    cpp_root.mkdir(exist_ok=True)
    for i, ch in enumerate(chapters, start=1):
        d = cpp_root / chapter_dir(i)
        d.mkdir(exist_ok=True)
        path = d / "main.cpp"
        content = f"""// {ch['title']} — minimal implementation stub.
#include <iostream>

int main() {{
    std::cout << "Chapter {i:02d}: {ch['title']}\n";
    // Implement the core idea from this chapter here.
    return 0;
}}
"""
        path.write_text(content, encoding="utf-8")


def generate_browser_stubs(chapters):
    browser_root = ROOT / "browser"
    browser_root.mkdir(exist_ok=True)
    for i, ch in enumerate(chapters, start=1):
        d = browser_root / chapter_dir(i)
        d.mkdir(exist_ok=True)
        path = d / "index.html"
        content = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>{ch['title']}</title>
<style>
  body {{ font-family: sans-serif; text-align: center; }}
  canvas {{ border: 1px solid #ccc; margin-top: 1rem; }}
</style>
</head>
<body>
<h1>{ch['title']}</h1>
<p>Browser simulation placeholder. Replace the canvas script with the chapter-specific interaction.</p>
<canvas id="sim" width="400" height="300"></canvas>
<script>
const canvas = document.getElementById('sim');
const ctx = canvas.getContext('2d');
let t = 0;
function draw() {{
  ctx.clearRect(0, 0, canvas.width, canvas.height);
  ctx.beginPath();
  ctx.arc(200 + Math.cos(t)*80, 150 + Math.sin(t)*40, 10, 0, Math.PI*2);
  ctx.fillStyle = '#1976d2';
  ctx.fill();
  t += 0.05;
  requestAnimationFrame(draw);
}}
draw();
</script>
</body>
</html>
"""
        path.write_text(content, encoding="utf-8")


def generate_simulations(chapters):
    sim_root = ROOT / "simulations"
    sim_root.mkdir(exist_ok=True)
    for i, ch in enumerate(chapters, start=1):
        d = sim_root / chapter_dir(i)
        d.mkdir(exist_ok=True)
        readme = d / "README.md"
        readme.write_text(
            f"# {ch['title']} — Simulation\n\n"
            f"Run `python sim.py` to launch the chapter simulation.\n",
            encoding="utf-8",
        )
        sim = d / "sim.py"
        content = f"""#!/usr/bin/env python3
\"\"\"{ch['title']} — simulation stub.\"\"\"


def run():
    print("Chapter {i:02d}: {ch['title']}")
    print("Implement the simulation for this discovery here.")
    print("Key idea: {ch['idea']}")


if __name__ == "__main__":
    run()
"""
        sim.write_text(content, encoding="utf-8")


def generate_mkdocs_nav(chapters):
    lines = [
        "site_name: Building Autonomous Robots From Scratch",
        "theme:",
        "  name: material",
        "plugins:",
        "  - search",
        "nav:",
        "  - Home: index.md",
        "  - Philosophy: philosophy.md",
        "  - Roadmap: roadmap.md",
    ]
    for part_name, start, end in PART_RANGES:
        lines.append(f"  - {part_name}:")
        for i in range(start, end + 1):
            ch = chapters[i - 1]
            slug = f"{i:02d}-{slugify(ch['title'])}.md"
            lines.append(f"      - {ch['title']}: {slug}")
    (ROOT / "mkdocs.yml").write_text("\n".join(lines) + "\n", encoding="utf-8")


def generate_roadmap(chapters):
    lines = ["# Roadmap", ""]
    for part_name, start, end in PART_RANGES:
        lines.append(f"## {part_name}")
        lines.append("")
        for i in range(start, end + 1):
            ch = chapters[i - 1]
            mark = "x" if i == 1 else " "
            slug = f"{i:02d}-{slugify(ch['title'])}.md"
            lines.append(f"- [{mark}] [{ch['title']}]({slug})")
        lines.append("")
    (ROOT / "docs" / "roadmap.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def generate_index(chapters):
    lines = [
        "# Building Autonomous Robots From Scratch",
        "",
        "Learn robotics the way humanity could have invented it.",
        "",
        "Not by memorizing formulas.",
        "",
        "Not by copying tutorials.",
        "",
        "By rebuilding every invention from first principles.",
        "",
        "Every discovery begins with a question.",
        "",
        "Every discovery ends with something that moves.",
        "",
        "## Start",
        "",
        f"- Read: [Discovery 01 — {chapters[0]['title']}](01-{slugify(chapters[0]['title'])}.md)",
        "",
        "## Roadmap",
        "",
    ]
    for part_name, start, end in PART_RANGES:
        lines.append(f"- {part_name}")
        for i in range(start, end + 1):
            ch = chapters[i - 1]
            mark = "x" if i == 1 else " "
            slug = f"{i:02d}-{slugify(ch['title'])}.md"
            lines.append(f"  - [{mark}] [{ch['title']}]({slug})")
    lines.extend(["", "[View the full roadmap](roadmap.md)"])
    (ROOT / "docs" / "index.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def generate_asset_links(chapters):
    """Create symlinks under docs/assets/ so MkDocs serves sim/browser files."""
    assets_sim = ROOT / "docs" / "assets" / "simulations"
    assets_browser = ROOT / "docs" / "assets" / "browser"
    assets_sim.mkdir(parents=True, exist_ok=True)
    assets_browser.mkdir(parents=True, exist_ok=True)
    for i, _ch in enumerate(chapters, start=1):
        cdir = chapter_dir(i)
        # simulations symlink
        sim_src = ROOT / "simulations" / cdir / "sim.py"
        sim_link_dir = assets_sim / cdir
        sim_link_dir.mkdir(parents=True, exist_ok=True)
        sim_link = sim_link_dir / "sim.py"
        if sim_link.exists() or sim_link.is_symlink():
            sim_link.unlink()
        sim_link.symlink_to(os.path.relpath(sim_src, sim_link_dir))
        # browser symlink
        browser_src = ROOT / "browser" / cdir / "index.html"
        browser_link_dir = assets_browser / cdir
        browser_link_dir.mkdir(parents=True, exist_ok=True)
        browser_link = browser_link_dir / "index.html"
        if browser_link.exists() or browser_link.is_symlink():
            browser_link.unlink()
        browser_link.symlink_to(os.path.relpath(browser_src, browser_link_dir))


def main():
    generate_docs(CHAPTER_SEEDS)
    generate_discoveries(CHAPTER_SEEDS)
    generate_python_stubs(CHAPTER_SEEDS)
    generate_cpp_stubs(CHAPTER_SEEDS)
    generate_browser_stubs(CHAPTER_SEEDS)
    generate_simulations(CHAPTER_SEEDS)
    generate_mkdocs_nav(CHAPTER_SEEDS)
    generate_roadmap(CHAPTER_SEEDS)
    generate_index(CHAPTER_SEEDS)
    generate_asset_links(CHAPTER_SEEDS)

    # Ensure top-level asset directories exist.
    (ROOT / "assets").mkdir(exist_ok=True)
    (ROOT / "assets" / ".gitkeep").write_text("")
    (ROOT / "diagrams").mkdir(exist_ok=True)
    (ROOT / "diagrams" / ".gitkeep").write_text("")


if __name__ == "__main__":
    main()
