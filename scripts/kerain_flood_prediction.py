import requests

# -----------------------------
# CONFIG
# -----------------------------
API_KEY = "0bf5056c944236e22817d1ab19667cb9"

cities = {
    "Kochi": (9.9312, 76.2673),
    "Thrissur": (10.5276, 76.2144),
    "Kozhikode": (11.2588, 75.7804),
    "Thiruvananthapuram": (8.5241, 76.9366)
}

# -----------------------------
# GET RAINFALL DATA
# -----------------------------
def get_rainfall(lat, lon):

    url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_KEY}&units=metric"

    response = requests.get(url)
    data = response.json()

    rain = 0
    if "rain" in data:
        rain = data["rain"].get("1h", 0)

    return rain

# -----------------------------
# FLOOD RISK MODEL
# -----------------------------
def flood_risk(rain):

    if rain < 2:
        return "LOW RISK"

    elif rain < 10:
        return "MEDIUM RISK"

    else:
        return "HIGH RISK"

# -----------------------------
# RUN SYSTEM
# -----------------------------
print("\nKERAIN – Flood Early Warning System")
print("-----------------------------------")

for city, coord in cities.items():

    lat, lon = coord
    rain = get_rainfall(lat, lon)

    risk = flood_risk(rain)

    print(f"{city}: Rainfall {rain} mm → {risk}")