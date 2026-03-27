import folium
from folium.plugins import HeatMap
import numpy as np


# Kerala district coordinates
districts = {
    "Kochi": [9.9312, 76.2673],
    "Thrissur": [10.5276, 76.2144],
    "Alappuzha": [9.4981, 76.3388],
    "Kottayam": [9.5916, 76.5222],
    "Palakkad": [10.7867, 76.6548],
    "Kozhikode": [11.2588, 75.7804],
    "Kannur": [11.8745, 75.3704]
}


def generate_flood_intensity():
    flood_data = []

    for district, coords in districts.items():

        rainfall = np.random.gamma(2, 6)
        river_flow = np.random.uniform(60, 150)

        intensity = (rainfall * 0.5) + (river_flow * 0.5)

        flood_data.append([coords[0], coords[1], intensity])

    return flood_data


def create_advanced_map():

    kerala_map = folium.Map(
        location=[10.2, 76.3],
        zoom_start=7,
        tiles="cartodbpositron"
    )

    flood_data = generate_flood_intensity()

    # Heatmap layer
    HeatMap(
        flood_data,
        radius=25,
        blur=20,
        max_zoom=10
    ).add_to(kerala_map)

    # Add district markers
    for district, coords in districts.items():

        folium.Marker(
            location=coords,
            popup=f"District: {district}",
            icon=folium.Icon(color="blue", icon="info-sign")
        ).add_to(kerala_map)

    kerala_map.save("kerain_advanced_flood_map.html")

    print("Advanced map saved as kerain_advanced_flood_map.html")


if __name__ == "__main__":
    create_advanced_map()