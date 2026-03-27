import numpy as np
import pandas as pd

np.random.seed(42)

# PARAMETERS
samples = 500

data = []

# Simulation parameters
base_rain = 10
storm_chance = 0.15
max_storm = 120

for i in range(samples):
    # Seasonal component (slow variation)
    season = np.sin(i / 50) * 5

    # Random storm
    if np.random.rand() < storm_chance:
        rainfall = np.random.uniform(40, max_storm)
    else:
        rainfall = np.random.uniform(0, base_rain)

    # Add season and noise
    rainfall = max(0, rainfall + season + np.random.normal(0, 2))

    # Hydrology features
    lag_1_rain = rainfall * np.random.uniform(0.6, 1.0)
    lag_2_rain = lag_1_rain * np.random.uniform(0.4, 0.9)
    cumulative_3hr = rainfall + lag_1_rain + lag_2_rain

    storage = np.random.uniform(20, 120)
    storage_change = rainfall - np.random.uniform(0, 5)

    runoff = max(0, rainfall - np.random.uniform(0, 8))
    runoff_ratio = runoff / (rainfall + 1)

    hour = i % 24

    # Flood probability (not deterministic)
    flood_prob = 0.01 * rainfall + 0.02 * storage + 0.05 * cumulative_3hr
    flood_prob = min(1, flood_prob / 15)

    # Probabilistic flood event
    flood = 1 if np.random.rand() < flood_prob else 0

    data.append([
        rainfall,
        lag_1_rain,
        lag_2_rain,
        cumulative_3hr,
        storage,
        storage_change,
        runoff,
        runoff_ratio,
        hour,
        flood
    ])

# Create DataFrame
df = pd.DataFrame(data, columns=[
    "rainfall",
    "lag_1_rain",
    "lag_2_rain",
    "cumulative_3hr",
    "storage",
    "storage_change",
    "runoff",
    "runoff_ratio",
    "hour",
    "flood"
])

# Save dataset
df.to_csv("kerain_expanded_data.csv", index=False)

print("New realistic dataset generated ✅")
print("Samples:", len(df))
print("Floods:", df['flood'].sum())