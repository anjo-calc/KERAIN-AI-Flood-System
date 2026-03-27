import folium

# -----------------------------
# LOCATION (Kerala)
# -----------------------------
latitude = 10.8505
longitude = 76.2711

# -----------------------------
# CREATE MAP (SAFE TILE)
# -----------------------------
m = folium.Map(
    location=[latitude, longitude],
    zoom_start=7,
    tiles="CartoDB positron"   # FIXED (no 403)
)

# -----------------------------
# ADD MARKER
# -----------------------------
folium.Marker(
    [latitude, longitude],
    popup="KERAIN Monitoring Point",
    tooltip="Flood Monitoring Active",
    icon=folium.Icon(color="blue", icon="info-sign")
).add_to(m)

# -----------------------------
# ADD MULTIPLE LOCATIONS (OPTIONAL)
# -----------------------------
locations = [
    (10.8505, 76.2711),  # Kerala
    (9.9312, 76.2673),   # Kochi
    (11.2588, 75.7804)   # Kozhikode
]

for loc in locations:
    folium.CircleMarker(
        location=loc,
        radius=6,
        color="red",
        fill=True,
        fill_color="red"
    ).add_to(m)

# -----------------------------
# SAVE MAP
# -----------------------------
m.save("kerain_map.html")

print("✅ Map created successfully → open kerain_map.html")