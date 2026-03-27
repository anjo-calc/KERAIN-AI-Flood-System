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
# FUNCTION TO GET RAIN DATA
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
# TEST API
# -----------------------------
print("Real-time Rainfall Data")
print("----------------------")

for city, coord in cities.items():

    lat, lon = coord
    rain = get_rainfall(lat, lon)

    print(f"{city}: {rain} mm")