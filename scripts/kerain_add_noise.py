import pandas as pd
import numpy as np

# Load original dataset
data = pd.read_csv("kerain_expanded_data.csv")

print("Original Dataset Loaded")
print("Samples:", len(data))

# Select feature columns (exclude target)
features = data.drop("flood", axis=1)

# Add Gaussian noise
noise_strength = 0.05   # 5% noise
noise = np.random.normal(0, noise_strength, features.shape)

noisy_features = features + noise

# Recombine with target
noisy_data = noisy_features.copy()
noisy_data["flood"] = data["flood"]

# Save new dataset
noisy_data.to_csv("kerain_noisy_data.csv", index=False)

print("Noisy dataset created ✅")
print("Saved as: kerain_noisy_data.csv")