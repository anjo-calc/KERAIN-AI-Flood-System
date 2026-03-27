import numpy as np
from sklearn.linear_model import LinearRegression


class ForecastEngine:

    def __init__(self):
        self.model = LinearRegression()

    def train(self, river_flow_series):

        X = []
        y = []

        # Use last 3 hours to predict next hour
        for i in range(len(river_flow_series) - 3):
            X.append(river_flow_series[i:i+3])
            y.append(river_flow_series[i+3])

        X = np.array(X)
        y = np.array(y)

        self.model.fit(X, y)

    def predict_future(self, last_values, hours):

        predictions = []
        current = list(last_values)

        for _ in range(hours):

            pred = self.model.predict([current[-3:]])[0]
            predictions.append(pred)

            current.append(pred)

        return predictions


def simulate_river_flow():

    base = np.random.normal(80, 10, 100)
    rainfall_effect = np.random.gamma(2, 3, 100)

    river_flow = base + rainfall_effect

    return river_flow


def run_forecast():

    river_flow = simulate_river_flow()

    engine = ForecastEngine()

    engine.train(river_flow)

    last_values = river_flow[-3:]

    pred_3 = engine.predict_future(last_values, 3)
    pred_6 = engine.predict_future(last_values, 6)
    pred_12 = engine.predict_future(last_values, 12)

    # Clean output
    pred_3 = [round(float(x), 2) for x in pred_3]
    pred_6 = [round(float(x), 2) for x in pred_6]
    pred_12 = [round(float(x), 2) for x in pred_12]

    print("\nCurrent River Flow:", [round(float(x), 2) for x in last_values])

    print("\n3 Hour Forecast:", pred_3)
    print("\n6 Hour Forecast:", pred_6)
    print("\n12 Hour Forecast:", pred_12)

    flood_threshold = 120

    if max(pred_6) > flood_threshold:
        print("\n⚠ Flood risk within next 6 hours")

    elif max(pred_12) > flood_threshold:
        print("\n⚠ Possible flood within 12 hours")

    else:
        print("\nNo immediate flood risk")


if __name__ == "__main__":
    run_forecast()