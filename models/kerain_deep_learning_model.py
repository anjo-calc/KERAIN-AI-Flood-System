import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, LSTM
from sklearn.preprocessing import MinMaxScaler

# -----------------------------
# GENERATE HISTORICAL DATA
# -----------------------------
np.random.seed(42)

time_steps = 200

rainfall = np.random.uniform(0, 50, time_steps)
river = np.cumsum(rainfall) * 0.05 + 70

data = pd.DataFrame({
    "Rainfall": rainfall,
    "River": river
})

# -----------------------------
# NORMALIZE DATA
# -----------------------------
scaler = MinMaxScaler()
scaled_data = scaler.fit_transform(data)

# -----------------------------
# CREATE SEQUENCES (LSTM INPUT)
# -----------------------------
X = []
y = []

window = 10

for i in range(len(scaled_data) - window):
    X.append(scaled_data[i:i+window])
    y.append(scaled_data[i+window][1])  # predict river

X = np.array(X)
y = np.array(y)

# -----------------------------
# BUILD LSTM MODEL
# -----------------------------
model = Sequential()
model.add(LSTM(50, return_sequences=True, input_shape=(window, 2)))
model.add(LSTM(50))
model.add(Dense(1))

model.compile(optimizer='adam', loss='mse')

# -----------------------------
# TRAIN MODEL
# -----------------------------
print("Training AI Model...")
model.fit(X, y, epochs=10, batch_size=8)

# -----------------------------
# PREDICT FUTURE
# -----------------------------
last_sequence = scaled_data[-window:]
last_sequence = np.reshape(last_sequence, (1, window, 2))

future_predictions = []

for i in range(10):
    pred = model.predict(last_sequence)[0][0]
    future_predictions.append(pred)

    new_row = np.array([[last_sequence[0][-1][0], pred]])
    last_sequence = np.append(last_sequence[:,1:,:], [new_row], axis=1)

# -----------------------------
# DENORMALIZE
# -----------------------------
dummy = np.zeros((len(future_predictions), 2))
dummy[:,1] = future_predictions

future_river = scaler.inverse_transform(dummy)[:,1]

# -----------------------------
# VISUALIZE
# -----------------------------
plt.figure(figsize=(10,5))
plt.plot(data["River"], label="Historical River")
plt.plot(range(len(data), len(data)+10), future_river, label="Predicted River", color='red')
plt.legend()
plt.title("KERAIN AI Flood Prediction (LSTM)")
plt.show()

print("Future River Levels:", future_river)