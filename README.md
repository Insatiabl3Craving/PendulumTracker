# PendulumTracker

A Python tool for estimating pendulum string lengths from tracked position data

## Method
1. Ingests per-frame (x, y) tracking CSVs for three pendulums.
2. Centers displacement and extracts zero crossings within a stable oscillation window (15–25s) to estimate period T.
3. Computes string length via the small-angle approximation: **L = T²g / 4π²**.
4. Reports period and length for each pendulum and identifies the longest.


The libararies used are NumPy, Pandas and Matplotlib

## Requirements
- Python 3.10+
- `numpy`, `pandas`, `matplotlib`

## Project structure
- `LengthEstimator.py` — main analysis script
- `TrackedData/` — input tracking CSV files
- `Results/` — generated result figures
- `RefVideos/` — reference videos (ignored in git)
