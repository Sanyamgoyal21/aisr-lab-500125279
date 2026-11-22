"""Exercises E4 and E5 (MANUAL.md Section 9), without editing the library files.

E4: change the kuka_mini scale and find the smallest KUKA that still succeeds.
    For each scale: task coverage (Part 1 method) and task-space success (Part 3 method).
E5: move kuka_mini's base 0.15 m towards the task (base_pos = (0.15, 0, 0)) and repeat Part 3.
    The cube/goal stay where they were in the world; observations stay in the robot's own base frame.

    python experiments/08_exercises_E4_E5.py
    python experiments/08_exercises_E4_E5.py --episodes 20 --scales 0.7 0.75 0.8 0.85 0.9 1.0
"""

import argparse
import importlib

import _common  # noqa: F401  (makes xembody importable, sets Agg backend)
import numpy as np
import pybullet as p

from xembody import EMBODIMENTS, expert_action
from xembody import world as world_mod
from xembody.rollout import evaluate, print_table, results_path, summarise, write_csv

part1 = importlib.import_module("01_explore_embodiments")
POLICY = lambda obs, joints: expert_action(obs)  # noqa: E731
SEEDS = None


def coverage(robot_name, x_shift=0.0):
    """Share of the 90 task-grid points reachable tool-down (robot-frame grid shifted by -x_shift)."""
    w = world_mod.World(robot_name)
    rb = w.stations[0].robot
    grid = part1.task_grid() - np.array([x_shift, 0.0, 0.0])
    cov = float(np.mean([part1.ik_reachable(rb, t) for t in grid]))
    w.close()
    return cov


def run_e4(scales):
    original = EMBODIMENTS["kuka_mini"]["scale"]
    rows = []
    try:
        for s in scales:
            EMBODIMENTS["kuka_mini"]["scale"] = s
            cov = coverage("kuka_mini")
            res = summarise(evaluate("kuka_mini", POLICY, SEEDS))
            rows.append(dict(scale=s, reach_est_m=0.945 * s, task_coverage=cov, **res))
            print(f"  scale {s:.2f}: coverage {cov:.0%}, success {res['success_rate']:.0%}", flush=True)
    finally:
        EMBODIMENTS["kuka_mini"]["scale"] = original
    cols = ["scale", "reach_est_m", "task_coverage", "success_rate", "mean_steps", "median_error_cm"]
    print_table(rows, cols, f"E4: kuka_mini scale sweep ({len(SEEDS)} task-space episodes per scale)")
    write_csv(results_path("E4_scale_sweep.csv"), rows, ["n", *cols])
    ok = [r["scale"] for r in rows if r["success_rate"] >= 0.95]
    print("Smallest scale with >= 95% success:", min(ok) if ok else "none tested")
    return rows


def run_e5(offset=(0.15, 0.0, 0.0)):
    offset = np.array(offset, dtype=float)
    Station = world_mod.Station
    orig_init, orig_reset, orig_cube = Station.__init__, Station.reset, Station.cube_position

    def init(self, robot_name, client, origin=(0, 0, 0)):
        orig_init(self, robot_name, client, origin)
        # move only the robot: re-place its base and record the new base position
        new_base = self.origin + offset
        _, orn = p.getBasePositionAndOrientation(self.robot.uid, physicsClientId=client)
        p.resetBasePositionAndOrientation(self.robot.uid, new_base.tolist(), orn, physicsClientId=client)
        self.robot.base_pos = new_base

    def reset(self, rng):
        orig_reset(self, rng)
        self.goal = self.goal - offset          # goal expressed in the robot's frame

    def cube_position(self):
        return orig_cube(self) - offset          # cube expressed in the robot's frame

    rows = []
    try:
        base = summarise(evaluate("kuka_mini", POLICY, SEEDS))
        rows.append(dict(setup="base_pos=(0,0,0)", task_coverage=coverage("kuka_mini"), **base))
        Station.__init__, Station.reset, Station.cube_position = init, reset, cube_position
        moved = summarise(evaluate("kuka_mini", POLICY, SEEDS))
        rows.append(dict(setup=f"base_pos=({offset[0]:.2f},0,0)",
                         task_coverage=coverage("kuka_mini", x_shift=offset[0]), **moved))
    finally:
        Station.__init__, Station.reset, Station.cube_position = orig_init, orig_reset, orig_cube
    far = np.hypot(0.60 - offset[0], 0.25)
    cols = ["setup", "task_coverage", "success_rate", "mean_steps", "median_error_cm"]
    print_table(rows, cols, f"E5: kuka_mini base moved towards the task ({len(SEEDS)} episodes each)")
    print(f"Farthest task point from the moved base: {far:.3f} m")
    write_csv(results_path("E5_base_moved.csv"), rows, ["n", *cols])
    return rows


def main():
    global SEEDS
    ap = argparse.ArgumentParser()
    ap.add_argument("--episodes", type=int, default=20)
    ap.add_argument("--scales", type=float, nargs="+", default=[0.7, 0.75, 0.8, 0.85, 0.9, 0.95, 1.0])
    args = ap.parse_args()
    SEEDS = [3000 + i for i in range(args.episodes)]   # same seeds as Part 3
    print("E4 ...")
    run_e4(args.scales)
    print("\nE5 ...")
    run_e5()
    print("\nSaved results/E4_scale_sweep.csv and results/E5_base_moved.csv")


if __name__ == "__main__":
    main()
