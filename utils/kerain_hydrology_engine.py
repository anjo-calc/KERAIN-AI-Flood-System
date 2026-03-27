import numpy as np
import pandas as pd


class HydrologyEngine:

    def __init__(self):
        # runoff coefficients for regions
        self.runoff_coeff = {
            "A": 0.6,
            "B": 0.55,
            "C": 0.5
        }

    def calculate_runoff(self, rainfall, region):
        coeff = self.runoff_coeff.get(region, 0.5)
        runoff = rainfall * coeff
        return runoff

    def calculate_river_flow(self, runoff_values):
        flow = np.cumsum(runoff_values) * 0.1
        return flow

    def calculate_flood_risk(self, river_flow, threshold=100):
        risk = river_flow > threshold
        return risk.astype(int)


def simulate_hydrology(hours=200):

    engine = HydrologyEngine()

    rainfall_A = np.random.gamma(2, 6, hours)
    rainfall_B = np.random.gamma(2, 7, hours)
    rainfall_C = np.random.gamma(2, 5, hours)

    runoff_A = engine.calculate_runoff(rainfall_A, "A")
    runoff_B = engine.calculate_runoff(rainfall_B, "B")
    runoff_C = engine.calculate_runoff(rainfall_C, "C")

    total_runoff = runoff_A + runoff_B + runoff_C

    river_flow = engine.calculate_river_flow(total_runoff)

    flood_risk = engine.calculate_flood_risk(river_flow)

    df = pd.DataFrame({
        "rain_A": rainfall_A,
        "rain_B": rainfall_B,
        "rain_C": rainfall_C,
        "runoff_A": runoff_A,
        "runoff_B": runoff_B,
        "runoff_C": runoff_C,
        "river_flow": river_flow,
        "flood": flood_risk
    })

    return df


if __name__ == "__main__":

    data = simulate_hydrology(500)

    print(data.head())
    print("\nFlood events:", data["flood"].sum())

    data.to_csv("kerain_hydrology_dataset.csv", index=False)

    print("\nDataset saved as kerain_hydrology_dataset.csv")