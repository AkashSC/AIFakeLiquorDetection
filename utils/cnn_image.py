import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image as keras_image
import numpy as np
from pathlib import Path

BASE = Path(__file__).parent
MODEL_PATH = BASE.parent / "models" / "bottle_cnn.h5"

# Load lightweight model
model = load_model(MODEL_PATH)
CLASS_NAMES = ["Fake", "Genuine"]

def predict_image(uploaded_file):
    img = keras_image.load_img(uploaded_file, target_size=(224,224))
    x = keras_image.img_to_array(img)
    x = np.expand_dims(x, axis=0) / 255.0
    preds = model.predict(x)
    class_idx = np.argmax(preds, axis=1)[0]
    confidence = float(preds[0][class_idx])
    return {"label": CLASS_NAMES[class_idx], "confidence": confidence}
