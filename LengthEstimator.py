import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# Physical constants
G = 9.81  # Gravitational acceleration (m/s^2)
FPS = 59  # Video frame rate (frames per second)
DT = 1 / FPS  # Time step between frames (seconds)
CROP_START = 15  # Start time for cropped view (seconds)
CROP_END = 25  # End time for cropped view (seconds)
DATA_DIR = Path(__file__).resolve().parent / 'TrackedData'


def calculate_length(T, g):
    return (T**2 * g) / (4 * np.pi**2)


def find_zero_crossings(time, x_centered):
    crossings = []
    for i in range(len(x_centered) - 1):
        # Sign change between consecutive points indicates a zero crossing
        if x_centered[i] * x_centered[i + 1] < 0:
            crossings.append(time[i])
    return np.array(crossings)

# Calculate period by averaging time between crossings
def estimate_period(crossings):
    if len(crossings) < 2:
        return 0
    
    intervals = np.diff(crossings)
    period = 2 * np.mean(intervals)
    return period


# Main analysis
filenames = ['pendulum_1.csv', 'pendulum_2.csv', 'pendulum_3.csv']
results = []

for i, filename in enumerate(filenames, 1):
    data = pd.read_csv(DATA_DIR / filename)
    x = data.iloc[:, 0].values
    y = data.iloc[:, 1].values
    time = np.arange(len(x)) * DT
    x_centered = x - np.mean(x)
    y_centered = y - np.mean(y)
    
    # Crop data for period calculation
    crop_mask = (time >= CROP_START) & (time <= CROP_END)
    time_crop = time[crop_mask]
    x_crop = x_centered[crop_mask]
    
    crossings = find_zero_crossings(time_crop, x_crop)
    period = estimate_period(crossings)
    length = calculate_length(period, G)
    results.append((period, length))
    
    print(f"Pendulum {i} - Period: {period:.3f} s")
    
    # Full data plot: shows complete motion over entire recording
    plt.figure(figsize=(10, 6))
    plt.plot(time, x_centered, 'b-', linewidth=0.8, label='$X_{centered}$')
    plt.plot(time, y_centered, 'g-', linewidth=0.8, label='$Y_{centered}$')
    plt.axhline(0, color='gray', linestyle='--', alpha=0.5)
    plt.plot(crossings, np.zeros_like(crossings), 'ro', markersize=5)
    plt.xlabel('Time (s)')
    plt.ylabel('Position (pixels)')
    plt.title(f'Pendulum {i}: Full Data')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.show()
    
    # Cropped data plot: focuses on stable oscillation period for better analysis
    plt.figure(figsize=(10, 6))
    plt.plot(time, x_centered, 'b-', linewidth=0.8, label='$X_{centered}$')
    plt.axhline(0, color='gray', linestyle='--', alpha=0.5)
    plt.plot(crossings, np.zeros_like(crossings), 'ro', markersize=5, label='Zero crossings')
    plt.xlim(CROP_START, CROP_END)
    plt.xlabel('Time (s)')
    plt.ylabel('x-position (pixels)')
    plt.title(f'Pendulum {i}: Cropped ({CROP_START}-{CROP_END}s)')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    
    if i == 1:
        plt.savefig('pendulum_analysis.png', dpi=150, bbox_inches='tight')
    plt.show()

# Summary results
print("\nRESULTS:")
print(f"Pendulum 1: T = {results[0][0]:.3f} s, L = {results[0][1]:.3f} m")
print(f"Pendulum 2: T = {results[1][0]:.3f} s, L = {results[1][1]:.3f} m")
print(f"Pendulum 3: T = {results[2][0]:.3f} s, L = {results[2][1]:.3f} m")

# Find longest pendulum
longest = results[0][1]
if results[1][1] > longest:
    longest = results[1][1]
if results[2][1] > longest:
    longest = results[2][1]
    
print(f"\nLongest pendulum: {longest:.3f} m")
