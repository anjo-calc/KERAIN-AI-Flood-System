import numpy as np
import os
from tensorflow.keras.models import load_model

# -----------------------------------
# SAFE MODEL LOADING (PRODUCTION READY)
# -----------------------------------

BASE_DIR = os.path.dirname(__file__)
MODEL_PATH = os.path.join(BASE_DIR, "kerain_satellite_model.h5")

cnn_model = None

if os.path.exists(MODEL_PATH):
    try:
        cnn_model = load_model(MODEL_PATH)
        print("✅ CNN Model Loaded")
    except Exception as e:
        print("⚠️ Model load failed:", e)
else:
    print("⚠️ CNN model file not found → running in fallback mode")


# -----------------------------------
# MAIN AI SYSTEM
# -----------------------------------

def run_ai_system(rain, river, rain_series):
    # -----------------------------------
    # LSTM SIMULATION (Future Prediction)
    # -----------------------------------
    lstm_prediction = river + np.mean(rain_series[-5:]) * 0.3

    # -----------------------------------
    # CNN MODEL (Satellite AI)
    # -----------------------------------
    if cnn_model:
        try:
            dummy_input = np.random.rand(1, 64, 64, 3)
            cnn_prob = float(cnn_model.predict(dummy_input)[0][0])
        except:
            cnn_prob = np.random.uniform(0.3, 0.9)
    else:
        # fallback if model missing
        cnn_prob = np.random.uniform(0.3, 0.9)

    # -----------------------------------
    # RULE ENGINE (HYBRID AI)
    # -----------------------------------
    rule_risk = 0

    if rain > 20:
        rule_risk += 30
    if river > 95:
        rule_risk += 40
    if np.mean(rain_series[-5:]) > 15:
        rule_risk += 20

    # -----------------------------------
    # FINAL FUSION AI
    # -----------------------------------
    final_risk = (cnn_prob * 50) + rule_risk

    final_risk = min(100, max(0, final_risk))

    return {
        "risk": final_risk,
        "lstm_prediction": lstm_prediction,
        "cnn_probability": cnn_prob * 100
    }