import numpy as np
import cv2
import os
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense

# -----------------------------
# CREATE SYNTHETIC SATELLITE DATA
# -----------------------------
def create_image(flood=False):
    img = np.zeros((64, 64, 3), dtype=np.uint8)

    if flood:
        # Blue-ish flood water
        img[:] = [255, 0, 0]  # OpenCV uses BGR
    else:
        # Green land
        img[:] = [0, 255, 0]

    noise = np.random.randint(0, 50, (64,64,3), dtype=np.uint8)
    img = cv2.add(img, noise)

    return img

# -----------------------------
# BUILD DATASET
# -----------------------------
X = []
y = []

for _ in range(200):
    X.append(create_image(flood=False))
    y.append(0)

for _ in range(200):
    X.append(create_image(flood=True))
    y.append(1)

X = np.array(X) / 255.0
y = np.array(y)

# -----------------------------
# BUILD CNN MODEL
# -----------------------------
model = Sequential()

model.add(Conv2D(32, (3,3), activation='relu', input_shape=(64,64,3)))
model.add(MaxPooling2D(2,2))

model.add(Conv2D(64, (3,3), activation='relu'))
model.add(MaxPooling2D(2,2))

model.add(Flatten())
model.add(Dense(64, activation='relu'))
model.add(Dense(1, activation='sigmoid'))

model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

# -----------------------------
# TRAIN MODEL
# -----------------------------
print("Training Satellite AI...")
model.fit(X, y, epochs=5, batch_size=16)

# -----------------------------
# TEST PREDICTION
# -----------------------------
test_img = create_image(flood=True)
test_img = test_img / 255.0
test_img = np.reshape(test_img, (1,64,64,3))

prediction = model.predict(test_img)[0][0]

print("Flood Probability:", prediction)

if prediction > 0.5:
    print("Flood Detected 🚨")
else:
    print("No Flood ✅")

# -----------------------------
# SAVE MODEL
# -----------------------------
model.save("kerain_satellite_model.h5")
print("Model Saved ✅")