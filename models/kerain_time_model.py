# kerain_time_model.py

import pandas as pd


def calculate_runoff(C, rainfall_intensity, area):
    return C * rainfall_intensity * area


def simulate_flood(C, rainfall_series, area, drainage_capacity, storage_threshold):
    storage = 0
    data = []

    for hour in range(len(rainfall_series)):
        rainfall = rainfall_series[hour]
        runoff = calculate_runoff(C, rainfall, area)

        previous_storage = storage
        storage = storage + runoff - drainage_capacity

        if storage < 0:
            storage = 0

        flood = int(storage > storage_threshold)

        # Lag features
        lag_1 = rainfall_series[hour - 1] if hour >= 1 else 0
        lag_2 = rainfall_series[hour - 2] if hour >= 2 else 0
        cumulative_3hr = rainfall + lag_1 + lag_2

        storage_change = storage - previous_storage
        runoff_ratio = runoff / drainage_capacity

        data.append([
            hour + 1,
            rainfall,
            lag_1,
            lag_2,
            cumulative_3hr,
            runoff,
            runoff_ratio,
            storage,
            storage_change,
            flood
        ])

    columns = [
        "hour",
        "rainfall",
        "lag_1_rain",
        "lag_2_rain",
        "cumulative_3hr",
        "runoff",
        "runoff_ratio",
        "storage",
        "storage_change",
        "flood"
    ]

    df = pd.DataFrame(data, columns=columns)
    return df


if __name__ == "__main__":
    # Balanced rainfall pattern (SAFE → FLOOD → RECOVERY)
    rainfall_series = [
        5, 10, 15, 20, 25,     # Safe build-up
        60, 70, 80,            # Flood trigger
        40, 20, 10, 5          # Recovery
    ]

    C = 0.8
    area = 10
    drainage_capacity = 300
    storage_threshold = 400

    df = simulate_flood(C, rainfall_series, area, drainage_capacity, storage_threshold)

    print(df)

    # Save dataset
    df.to_csv("kerain_training_data.csv", index=False)

    print("\nDataset saved as kerain_training_data.csv")