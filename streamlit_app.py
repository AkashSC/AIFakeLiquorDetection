import os
import numpy as np
import streamlit as st
from PIL import Image
import speech_recognition as sr
import prepare_dataset  # auto-create dataset

# --- Image comparison (histogram-based) ---
def classify_image(img_path):
    img = Image.open(img_path).resize((224, 224)).convert("RGB")
    hist = np.array(img.histogram())

    coca_ref = Image.open("sample_data/images/coca_cola1.jpg").resize((224, 224)).convert("RGB")
    pepsi_ref = Image.open("sample_data/images/pepsi1.jpg").resize((224, 224)).convert("RGB")

    coca_score = np.linalg.norm(hist - np.array(coca_ref.histogram()))
    pepsi_score = np.linalg.norm(hist - np.array(pepsi_ref.histogram()))

    if coca_score < pepsi_score:
        return "Coca Cola"
    else:
        return "Pepsi"

# --- Speech-to-text ---
def recognize_speech(file_path):
    r = sr.Recognizer()
    with sr.AudioFile(file_path) as source:
        audio = r.record(source)
    try:
        return r.recognize_google(audio)
    except Exception as e:
        return f"Error: {e}"

# --- UI ---
st.title("🍾 Product Verification POC (Python 3.10, Lightweight)")
st.write("Upload files OR test with sample Coca Cola / Pepsi dataset.")

tab1, tab2 = st.tabs(["🔼 Upload Files", "📂 Use Sample Data"])

with tab1:
    uploaded_img = st.file_uploader("Upload product image", type=["jpg", "png", "jpeg"])
    uploaded_voice = st.file_uploader("Upload voice sample", type=["wav", "mp3"])

    if uploaded_img and uploaded_voice:
        img_path = "temp_image.jpg"
        with open(img_path, "wb") as f:
            f.write(uploaded_img.read())

        voice_path = "temp_voice.wav"
        with open(voice_path, "wb") as f:
            f.write(uploaded_voice.read())

        st.image(img_path, caption="Uploaded Image", use_column_width=True)
        img_result = classify_image(img_path)
        st.write(f"🔎 Image recognition result: **{img_result}**")

        voice_result = recognize_speech(voice_path)
        st.write(f"🎤 Voice recognition result: **{voice_result}**")

        if img_result.lower() in voice_result.lower():
            st.success("✅ Product Verified")
        else:
            st.error("❌ Mismatch between image and voice")

with tab2:
    sample_img = st.selectbox("Select sample image", os.listdir("sample_data/images"))
    sample_voice = st.selectbox("Select sample voice", os.listdir("sample_data/voices"))

    if st.button("Run Sample Test"):
        img_path = os.path.join("sample_data/images", sample_img)
        voice_path = os.path.join("sample_data/voices", sample_voice)

        st.image(img_path, caption=sample_img, use_column_width=True)
        img_result = classify_image(img_path)
        st.write(f"🔎 Image recognition result: **{img_result}**")

        voice_result = recognize_speech(voice_path)
        st.write(f"🎤 Voice recognition result: **{voice_result}**")

        if img_result.lower() in voice_result.lower():
            st.success("✅ Product Verified")
        else:
            st.error("❌ Mismatch between image and voice")
