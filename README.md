# aisr-lab-500125279

Laboratory work for **CSAI4014 Algorithms for Intelligent Systems and Robotics (AISR)**,
School of Computer Science, UPES Dehradun. Autumn Semester 2026–27.

| | |
|---|---|
| **Name** | Sanyam Goyal |
| **SAP ID** | 500125279 |
| **Programme / batch** | B.Tech CSE (AI & ML), Semester VII, Batch B2 |
| **Lab partner(s)** | None |
| **Course teacher** | Dr. Resham Raj Shivwanshi |

---

## Repository layout

```
aisr-lab-500125279/
  README.md
  20-08-2026/        robot_transformation.ipynb      2D rigid-body frame transformations
  27-08-2026/        automatic_file_organizer.ipynb  file organiser exercise (+ sample files)
  exp01-signals/     exp01.ipynb   figs/
  exp02-queens/      exp02.ipynb   figs/
  exp03-search/      exp03.ipynb   figs/
  exp04-hillclimb/   exp04.ipynb   figs/
  exp05-rl/          exp05.ipynb   figs/
  exp06-neural/      exp06.ipynb   figs/
  exp07-webots/      controllers/  worlds/  tools/  analysis/runs/*.csv
  exp08-xembody/     xembody/  experiments/  results/*.csv
```

## Experiments

| # | Folder | Topic | Key result from this run |
|---|---|---|---|
| 1 | `exp01-signals` | Time and frequency domain, aliasing, simple pendulum | Peaks at 5, 20, 50 Hz with amplitudes 1.00 / 0.50 / 0.25; 5 Hz sampled at 8 Hz aliases to 3 Hz; period grows from 2.01 s (5°) to ≈5.8 s (175°) |
| 2 | `exp02-queens` | Eight queens: generate-and-test vs backtracking | 92 solutions (12 fundamental), 15 720 nodes; both methods agree for n = 4…10 |
| 3 | `exp03-search` | Breadth-first vs depth-first search on a maze | 23 × 35 maze: BFS 267 expanded / path 69 (shortest); DFS 121 expanded / path 107 |
| 4 | `exp04-hillclimb` | Hill climbing and random restarts | Single run 12.5–14.5 % success; 20 restarts 97.5 %, matching 1 − (1 − p)^k |
| 5 | `exp05-rl` | Tabular Q-learning on a grid world | Final return 8.86 (ε = 0.05, 0.20) vs 7.44 (ε = 0.50); all three greedy policies reach the goal in 10 steps |
| 6 | `exp06-neural` | Two-layer neural network on XOR (NumPy only) | Final MSE 2.31e-3 / 1.11e-4 / 2.46e-5 for lr = 0.05 / 0.5 / 2.0; predictions 0.004, 0.995, 0.996, 0.006 |
| 7 | `exp07-webots` | Webots: e-puck Braitenberg swarm and Pioneer 3-DX lidar navigation | Default swarm coverage 79 ± 3 % over 3 runs; cruise = 0.9 explores more (86–89 %) but can trap a robot |
| 8 | `exp08-xembody` | Cross-embodiment transfer of a pick-and-place skill (PyBullet) | Joint-space transfer 0 % on other robots; task-space 100 % on Panda and xArm6. E4: smallest reliable KUKA scale 0.80; E5: moving the base raises kuka_mini from 30 % to 80 % |

## Environment

| Item | Version |
|---|---|
| OS / CPU | Windows 11 Home (64-bit); Intel Core i5-1155G7 @ 2.50 GHz, 16 GB RAM |
| Experiments 1–6 | Python 3.12, NumPy 2.4.3, SciPy 1.15.1, Matplotlib 3.10.8, JupyterLab |
| Experiment 7 | Webots R2025a, Python 3.10 |
| Experiment 8 | Python 3.10.9 virtual environment, PyBullet 3.2.7, scikit-learn 1.7.2, NumPy 2.2.6, Matplotlib 3.10.9 |

## How to run

**Experiments 1–6:** open the notebook and run all cells, or run it headless:

```bash
pip install numpy scipy matplotlib jupyterlab
cd exp01-signals
jupyter nbconvert --to notebook --execute --inplace exp01.ipynb
```

Each notebook runs top to bottom on a fresh kernel and saves its figures to `figs/`.

**Experiment 7 (Webots):** install Webots R2025a, then run a world headless:

```bash
cd exp07-webots
python tools/run_experiment.py swarm --seconds 120
python tools/run_experiment.py swarm --seconds 120 --set cruise=0.9 --name swarm_cruise-0.9_run2
python analysis/metrics.py analysis/runs/swarm_default.csv swarm
```

On Windows, set `WEBOTS_HOME` if Webots is not installed in the default location.

**Experiment 8 (PyBullet):**

```bash
python -m venv ~/aisr-venv          # keep the venv on a short path on Windows
~/aisr-venv/Scripts/activate        # macOS/Linux: source ~/aisr-venv/bin/activate
pip install -r exp08-xembody/requirements.txt
cd exp08-xembody
python experiments/00_check_setup.py
python experiments/03_task_space_transfer.py --episodes 20
python experiments/08_exercises_E4_E5.py          # exercises E4 and E5
```

PyBullet has no prebuilt Windows wheel, so `pip` compiles it (needs the Microsoft C++ Build Tools).

## Sources

* CSAI4014 Laboratory Manual, Experiments 1 to 6, UPES, Autumn 2026–27.
* Webots robotics simulations (Experiment 7), prepared for the AISR lab: <https://github.com/reshamrajs/webots-robotics-sim>
* Cross-Embodiment Transfer Lab (Experiment 8), prepared by Dr. Resham Raj Shivwanshi for the AISR lab:
  <https://github.com/reshamrajs/AISR-Cross-Embodiment-PyBullet>
* Cyberbotics, *Webots R2025a*, <https://cyberbotics.com>.
* E. Coumans and Y. Bai, *PyBullet*, <http://pybullet.org>. Robot models from `pybullet_data`.
* S. Russell and P. Norvig, *Artificial Intelligence: A Modern Approach*, 3rd ed.
* NumPy, SciPy, Matplotlib and scikit-learn documentation.
* AI assistants used: ChatGPT and Claude
