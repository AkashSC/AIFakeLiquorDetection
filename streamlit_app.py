import os
import streamlit as st
from torchvision import models, transforms
from PIL import Image
import torch
import speech_recognition as sr
import prepare_dataset  # auto-create dataset

# --- Image classifier (ResNet18 pretrained) ---
model = models.resnet18(weights=models.ResNet18_Weights.DEFAULT)
model.eval()

transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
])

# --- Helper: predict image ---
def predict_image(img_path):
    img = Image.open(img_path).convert("RGB")
    img_t = transform(img).unsqueeze(0)
    with torch.no_grad():
        out = model(img_t)
        _, pred = torch.max(out, 1)
    return f"Predicted class index: {pred.item()}"

# --- Helper: speech-to-text ---
def recognize_speech(file_path):
    r = sr.Recognizer()
    with sr.AudioFile(file_path) as source:
        audio = r.record(source)
    try:
        return r.recognize_google(audio)
    except Exception as e:
        return f"Error: {e}"

# --- UI ---
st.title("🍾 Product Verification POC")
st.write("Upload an image & voice OR select from sample dataset to test.")

tab1, tab2 = st.tabs(["🔼 Upload Files", "📂 Use Sample Data"])

with tab1:
    uploaded_img = st.file_uploader("Upload product image", type=["jpg", "png", "jpeg"])
    uploaded_voice = st.file_uploader("Upload voice sample", type=["wav", "mp3"])

    if uploaded_img and uploaded_voice:
        # Save temp files
        img_path = f"temp_image.jpg"
        with open(img_path, "wb") as f:
            f.write(uploaded_img.read())

        voice_path = f"temp_voice.wav"
        with open(voice_path, "wb") as f:
            f.write(uploaded_voice.read())

        st.image(img_path, caption="Uploaded Image", use_column_width=True)
        img_result = predict_image(img_path)
        st.write(f"🔎 Image recognition result: {img_result}")

        voice_result = recognize_speech(voice_path)
        st.write(f"🎤 Voice recognition result: {voice_result}")

with tab2:
    sample_img = st.selectbox("Select sample image", os.listdir("sample_data/images"))
    sample_voice = st.selectbox("Select sample voice", os.listdir("sample_data/voices"))

    if st.button("Run Sample Test"):
        img_path = os.path.join("sample_data/images", sample_img)
        voice_path = os.path.join("sample_data/voices", sample_voice)

        st.image(img_path, caption=sample_img, use_column_width=True)
        img_result = predict_image(img_path)
        st.write(f"🔎 Image recognition result: {img_result}")

        voice_result = recognize_speech(voice_path)
        st.write(f"🎤 Voice recognition result: {voice_result}")

        if "coca" in sample_img.lower() and "coca" in voice_result.lower():
            st.success("✅ Product Verified (Coca Cola)")
        elif "pepsi" in sample_img.lower() and "pepsi" in voice_result.lower():
            st.success("✅ Product Verified (Pepsi)")
        else:
            st.error("❌ Mismatch between image and voice")
