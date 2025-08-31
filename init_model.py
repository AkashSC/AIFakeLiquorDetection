from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Flatten, Conv2D, MaxPooling2D
import os

os.makedirs("models", exist_ok=True)

model = Sequential([
    Conv2D(8, (3,3), activation="relu", input_shape=(224,224,3)),
    MaxPooling2D(2,2),
    Flatten(),
    Dense(2, activation="softmax")
])

model.compile(optimizer="adam", loss="sparse_categorical_crossentropy", metrics=["accuracy"])

model.save("models/bottle_cnn.h5")
print("✅ Dummy bottle_cnn.h5 created in /models/")
