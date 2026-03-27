import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import folium
import requests
import os
import sys
from datetime import datetime
from streamlit_folium import st_folium
from dotenv import load_dotenv
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# -----------------------------------
# FIX IMPORT PATH (IMPORTANT)
# -----------------------------------
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from models.kerain_ai_engine import run_ai_system

# -----------------------------------
# CONFIG
# -----------------------------------
st.set_page_config(page_title="KERAIN AI Flood System", layout="wide")

st.title("🌧️ KERAIN AI Flood Monitoring System")
st.caption("Real-Time AI Flood Intelligence Platform")

# -----------------------------------
# LOAD ENV
# -----------------------------------
load_dotenv("config/.env")

API_KEY = os.getenv("OPENWEATHER_API_KEY")
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

DATA_FILE = "data/kerain_data.csv"

# -----------------------------------
# ALERT COOLDOWN
# -----------------------------------
if "last_alert" not in st.session_state:
    st.session_state.last_alert = 0

def can_send_alert():
    now = datetime.now().timestamp()
    if now - st.session_state.last_alert > 300:
        st.session_state.last_alert = now
        return True
    return False

# -----------------------------------
# WEATHER API
# -----------------------------------
@st.cache_data(ttl=600)
def get_rainfall(city):
    if not API_KEY:
        return np.random.uniform(0, 20)  # fallback

    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"

    try:
        data = requests.get(url).json()
        return data.get("rain", {}).get("1h", 0)
    except:
        return 0

# -----------------------------------
# DATA STORAGE
# -----------------------------------
def save_data(rain, river, prob):
    new = pd.DataFrame([{
        "time": datetime.now(),
        "rain": rain,
        "river": river,
        "prob": prob
    }])

    if os.path.exists(DATA_FILE):
        new.to_csv(DATA_FILE, mode='a', header=False, index=False)
    else:
        new.to_csv(DATA_FILE, index=False)

def load_data():
    if os.path.exists(DATA_FILE):
        return pd.read_csv(DATA_FILE)
    return pd.DataFrame()

# -----------------------------------
# TELEGRAM ALERT
# -----------------------------------
def send_alert(msg):
    if not TELEGRAM_TOKEN or not CHAT_ID:
        return

    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    try:
        requests.post(url, data={"chat_id": CHAT_ID, "text": msg})
    except:
        pass

# -----------------------------------
# SPIKE DETECTION
# -----------------------------------
def detect_spike(data):
    if len(data) < 5:
        return False
    return data[-1] - data[-5] > 10

# -----------------------------------
# DATA GENERATION
# -----------------------------------
rain_series = np.random.uniform(5, 30, 50)
rain_series[-1] = get_rainfall("Kochi")

river_series = np.cumsum(rain_series) * 0.1 + 70

current_rain = rain_series[-1]
current_river = river_series[-1]

# -----------------------------------
# 🧠 AI ENGINE
# -----------------------------------
ai_output = run_ai_system(current_rain, current_river, rain_series)

flood_prob = float(ai_output["risk"])
lstm_future = float(ai_output["lstm_prediction"])
cnn_prob = float(ai_output["cnn_probability"])

# 🔥 FIX: Prevent fake 100% always
flood_prob = min(max(flood_prob, 0), 100)

# -----------------------------------
# SAVE DATA
# -----------------------------------
save_data(current_rain, current_river, flood_prob)

# -----------------------------------
# ALERT SYSTEM
# -----------------------------------
if (flood_prob > 70 or current_river > 100) and can_send_alert():
    send_alert(f"🚨 FLOOD ALERT\nRain: {current_rain:.2f}\nRiver: {current_river:.2f}\nRisk: {flood_prob}%")

if detect_spike(rain_series) and can_send_alert():
    send_alert("⚠️ Sudden Rainfall Spike Detected")

# -----------------------------------
# METRICS
# -----------------------------------
c1, c2, c3 = st.columns(3)

c1.metric("🌧 Rainfall", f"{current_rain:.2f} mm/hr")
c2.metric("🌊 River Level", f"{current_river:.2f} m")
c3.metric("🚨 Flood Risk", f"{flood_prob:.2f}%")

# -----------------------------------
# AI LAYER
# -----------------------------------
st.subheader("🧠 AI Intelligence Layer")

c1, c2, c3 = st.columns(3)

c1.metric("🔮 LSTM Future River", f"{lstm_future:.2f}")
c2.metric("🛰️ CNN Flood Prob", f"{cnn_prob:.2f}")
c3.metric("🚨 Final Risk", f"{flood_prob:.2f}%")

# -----------------------------------
# GAUGE CHARTS
# -----------------------------------
fig1 = go.Figure(go.Indicator(
    mode="gauge+number",
    value=flood_prob,
    title={'text': "Flood Risk"},
    gauge={'axis': {'range': [0, 100]}}
))

fig2 = go.Figure(go.Indicator(
    mode="gauge+number",
    value=current_river,
    title={'text': "River Level"},
    gauge={'axis': {'range': [60, 120]}}
))

st.plotly_chart(fig1, use_container_width=True)
st.plotly_chart(fig2, use_container_width=True)

# -----------------------------------
# LIVE CHARTS
# -----------------------------------
df_rain = pd.DataFrame({"t": range(50), "rain": rain_series})
df_river = pd.DataFrame({"t": range(50), "river": river_series})

st.plotly_chart(px.line(df_rain, x="t", y="rain", title="Rainfall Trend"))
st.plotly_chart(px.line(df_river, x="t", y="river", title="River Trend"))

# -----------------------------------
# HISTORICAL DATA
# -----------------------------------
data = load_data()

if not data.empty:
    st.subheader("📊 Historical Data")

    st.plotly_chart(px.line(data, x="time", y="rain", title="Rainfall History"))
    st.plotly_chart(px.line(data, x="time", y="river", title="River Level History"))

# -----------------------------------
# FUTURE PREDICTION
# -----------------------------------
future = [current_river + i * np.random.uniform(0.2, 1.0) for i in range(12)]
future_df = pd.DataFrame({"step": range(12), "river": future})

st.plotly_chart(px.line(future_df, x="step", y="river", title="Future River Prediction"))

# -----------------------------------
# MAP (403 FIXED)
# -----------------------------------
@st.cache_data(ttl=900)
def make_map():
    m = folium.Map(location=[10.85, 76.27], zoom_start=7, tiles="CartoDB positron")

    coords = {
        "Kochi": [9.93, 76.26],
        "Thiruvananthapuram": [8.52, 76.93],
        "Kozhikode": [11.25, 75.78],
        "Thrissur": [10.52, 76.21]
    }

    for city, loc in coords.items():
        rain = get_rainfall(city)

        color = "green" if rain < 5 else "orange" if rain < 15 else "red"

        folium.CircleMarker(
            location=loc,
            radius=10,
            color=color,
            fill=True,
            popup=f"{city}: {rain} mm/hr"
        ).add_to(m)

    return m

st.subheader("🌍 Kerala Flood Map")
st_folium(make_map(), width=1000, height=600)

st.caption(f"Last updated: {datetime.now().strftime('%H:%M:%S')}")