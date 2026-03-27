import pandas as pd

# Load current dataset
data = pd.read_csv("kerain_expanded_data.csv")

print("Dataset Loaded")
print("Samples:", len(data))

# Create future flood label (1 hour ahead)
data["flood_future"] = data["flood"].shift(-1)

# Remove last row (no future value)
data = data.dropna()

# Convert to integer
data["flood_future"] = data["flood_future"].astype(int)

# Save dataset
data.to_csv("kerain_future_data.csv", index=False)

print("Future prediction dataset created ✅")
print("Saved as kerain_future_data.csv")