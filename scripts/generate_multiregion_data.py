import numpy as np
import pandas as pd

np.random.seed(42)

samples = 800

data = []

# Initial river flow
river_flow = 20

for t in range(samples):

    # Rainfall in two regions
    rain_A = max(0, np.random.normal(20, 15))
    rain_B = max(0, np.random.normal(15, 12))

    # Storm bursts
    if np.random.rand() < 0.12:
        rain_A += np.random.uniform(40, 80)

    if np.random.rand() < 0.10:
        rain_B += np.random.uniform(30, 70)

    # Upstream runoff
    runoff_A = rain_A * np.random.uniform(0.5, 0.9)

    # River flow propagation (delayed effect)
    river_flow = 0.7 * river_flow + runoff_A

    # Downstream storage
    storage_B = rain_B + river_flow * np.random.uniform(0.6, 1.1)

    # Flood probability
    flood_prob = (rain_B*0.02 + river_flow*0.03 + storage_B*0.02)
    flood_prob = min(1, flood_prob/5)

    flood = 1 if np.random.rand() < flood_prob else 0

    data.append([
        rain_A,
        rain_B,
        runoff_A,
        river_flow,
        storage_B,
        t % 24,
        flood
    ])

df = pd.DataFrame(data, columns=[
    "rain_A",
    "rain_B",
    "runoff_A",
    "river_flow",
    "storage_B",
    "hour",
    "flood"
])

df.to_csv("kerain_multiregion_data.csv", index=False)

print("Multi-region dataset created ✅")
print("Samples:", len(df))
print("Flood events:", df["flood"].sum())