import os
import numpy as np
import streamlit as st
from PIL import Image, UnidentifiedImageError
import requests
import prepare_dataset  # auto-create sample files

# --- Image comparison (histogram-based) ---
def classify_image(img_path):
    img = Image.open(img_path).resize((224, 224)).convert("RGB")
    hist = np.array(img.histogram())

    coca_ref = Image.open("sample_data/images/coca_cola1.jpg").resize((224, 224)).convert("RGB")
    pepsi_ref = Image.open("sample_data/images/pepsi1.jpg").resize((224, 224)).convert("RGB")

    coca_score = np.linalg.norm(hist - np.array(coca_ref.histogram()))
    pepsi_score = np.linalg.norm(hist - np.array(pepsi_ref.histogram()))

    return "Coca Cola" if coca_score < pepsi_score else "Pepsi"

# --- Speech-to-text using HuggingFace Whisper API ---
HF_API_URL = "https://api-inference.huggingface.co/models/openai/whisper-small"
HF_HEADERS = {
    "Authorization": "Bearer YOUR_HUGGINGFACE_API_KEY"  # ← replace with free API key
}

def recognize_speech(file_path):
    with open(file_path, "rb") as f:
        audio_bytes = f.read()
    response = requests.post(HF_API_URL, headers=HF_HEADERS, files={"file": audio_bytes})
    if response.status_code == 200:
        res_json = response.json()
        return res_json.get("text", "Could not transcribe")
    else:
        return f"Error: {response.status_code}"

# --- UI ---
st.title("🍾 Product Verification POC (Manual Upload)")
st.write("Upload files OR test with sample dataset.")

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

        try:
            img = Image.open(img_path).convert("RGB")
            st.image(img, caption="Uploaded Image", use_column_width=True)
            img_result = classify_image(img_path)
            st.write(f"🔎 Image recognition result: **{img_result}**")
        except UnidentifiedImageError:
            st.error("❌ Uploaded file is not a valid image")
            img_result = None

        try:
            voice_result = recognize_speech(voice_path)
            st.write(f"🎤 Voice recognition result: **{voice_result}**")
        except Exception as e:
            st.error(f"❌ Failed to transcribe audio: {e}")
            voice_result = None

        if img_result and voice_result:
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
