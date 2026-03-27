# 🌧️ KERAIN — AI Flood Prediction & Monitoring System

KERAIN is an advanced AI-powered flood intelligence platform that combines:

* 🌦 Real-time weather data
* 🌊 Hydrological modeling
* 🧠 Deep Learning (LSTM + CNN)
* 🛰️ Satellite-inspired flood detection
* 📊 Interactive dashboards

---

## 🚀 Features

* 🔴 Real-time flood risk prediction
* 📈 Time-series forecasting using LSTM
* 🛰️ Satellite-based flood detection (CNN model)
* 🌍 Interactive Kerala flood map
* 📊 Historical + live data visualization
* ⚠️ Automated Telegram alerts
* 🧠 Multi-model AI decision engine

---

## 🧠 AI Architecture

KERAIN integrates multiple AI layers:

* **LSTM Model** → Predicts future river levels
* **CNN Model** → Detects flood patterns from satellite-like data
* **Ensemble AI Engine** → Combines signals into final flood risk

---

## 📂 Project Structure

```
KERAIN/
│
├── app/                # Streamlit dashboard
├── models/             # AI models (LSTM, CNN, ML)
├── data/               # Datasets
├── utils/              # APIs and processing logic
├── maps/               # Map visualizations
├── scripts/            # Data generation scripts
├── tests/              # Testing utilities
├── docs/               # Notes and documentation
├── config/             # Environment variables
│
└── README.md
```

---

## ⚙️ Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/your-username/kerain.git
cd kerain
```

### 2. Create virtual environment

```bash
python -m venv kerain_env
kerain_env\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure API keys

Create a file:

```
config/.env
```

Add:

```
OPENWEATHER_API_KEY=your_api_key
TELEGRAM_TOKEN=your_token
CHAT_ID=your_chat_id
```

---

## ▶️ Run the Application

```bash
python -m streamlit run app/kerain_web_dashboard.py
```

---

## 📊 Example Output

* Flood Risk Score (%)
* River Level Forecast
* Rainfall Trends
* Kerala Flood Map
* AI Decision Layer

---

## 🧭 Future Improvements

* 🌐 Live satellite data integration (NASA / ESA)
* 🤖 Reinforcement learning for flood control strategies
* ☁️ Cloud deployment (AWS / GCP)
* 📱 Mobile app interface

---

## 👨‍💻 Author

**Anjo Biju**
AI Developer | Climate Tech Enthusiast

---

## ⭐ Project Vision

To build a **real-time, AI-driven flood intelligence system** capable of saving lives and improving disaster response globally.

---

## 📜 License

This project is open-source under the MIT License.
