import pandas as pd
import numpy as np
import folium


# Example Kerala district coordinates
districts = {
    "Kochi": [9.9312, 76.2673],
    "Thrissur": [10.5276, 76.2144],
    "Alappuzha": [9.4981, 76.3388],
    "Kottayam": [9.5916, 76.5222],
    "Palakkad": [10.7867, 76.6548],
    "Kozhikode": [11.2588, 75.7804],
    "Kannur": [11.8745, 75.3704]
}


def generate_risk():
    risks = {}

    for d in districts:
        rain = np.random.gamma(2, 6)
        river_flow = np.random.uniform(50, 150)

        if river_flow > 120:
            risk = "High Flood Risk"
        elif river_flow > 90:
            risk = "Medium Risk"
        else:
            risk = "Safe"

        risks[d] = risk

    return risks


def create_map():

    risks = generate_risk()

    kerala_map = folium.Map(location=[10.2, 76.3], zoom_start=7)

    for district, coords in districts.items():

        risk = risks[district]

        if risk == "High Flood Risk":
            color = "red"
        elif risk == "Medium Risk":
            color = "orange"
        else:
            color = "green"

        folium.CircleMarker(
            location=coords,
            radius=10,
            popup=f"{district}: {risk}",
            color=color,
            fill=True,
            fill_color=color
        ).add_to(kerala_map)

    kerala_map.save("kerain_flood_map.html")

    print("Map saved as kerain_flood_map.html")


if __name__ == "__main__":
    create_map()