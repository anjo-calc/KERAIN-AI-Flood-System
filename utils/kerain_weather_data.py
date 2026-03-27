import requests
import pandas as pd


def get_rainfall_data():

    # Coordinates for Kochi, Kerala
    latitude = 9.9312
    longitude = 76.2673

    url = f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&hourly=precipitation&forecast_days=2"

    response = requests.get(url)

    data = response.json()

    rainfall = data["hourly"]["precipitation"]
    time = data["hourly"]["time"]

    df = pd.DataFrame({
        "time": time,
        "rainfall_mm": rainfall
    })

    return df


def analyze_rainfall(df):

    total_rain = df["rainfall_mm"].sum()

    print("\nTotal Rainfall (next hours):", round(total_rain, 2), "mm")

    if total_rain > 100:
        print("⚠ Extreme rainfall expected")
    elif total_rain > 50:
        print("⚠ Heavy rainfall expected")
    else:
        print("Normal rainfall levels")


def run_weather_engine():

    print("\nFetching real rainfall data...\n")

    rainfall_data = get_rainfall_data()

    print(rainfall_data.head())

    analyze_rainfall(rainfall_data)

    rainfall_data.to_csv("kerain_real_rainfall.csv", index=False)

    print("\nRainfall data saved as kerain_real_rainfall.csv")


if __name__ == "__main__":
    run_weather_engine()