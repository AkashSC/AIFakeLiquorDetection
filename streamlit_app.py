import os
import json
import streamlit as st
from PIL import Image, UnidentifiedImageError
import pytesseract
import requests

# ---------------------------
# Load dataset
# ---------------------------
with open("sample_data/dataset.json", "r") as f:
    dataset = json.load(f)

# ---------------------------
# HuggingFace Whisper API for voice
# ---------------------------
HF_API_URL = "https://api-inference.huggingface.co/models/openai/whisper-small"
HF_HEADERS = {
    "Authorization": "Bearer YOUR_HUGGINGFACE_API_KEY"  # Replace with your HuggingFace free API key
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

# ---------------------------
# Streamlit UI
# ---------------------------
st.title("📦 Product Verification with OCR + Voice")

tab1, tab2 = st.tabs(["🔼 Upload Files", "📂 Sample Data Test"])

# ---------------------------
# Tab 1: Upload Files
# ---------------------------
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

        # --- OCR ---
        try:
            img = Image.open(img_path).convert("RGB")
            st.image(img, caption="Uploaded Image", use_column_width=True)
            ocr_text = pytesseract.image_to_string(img).strip()
            st.write(f"🔎 OCR detected text: **{ocr_text}**")
        except UnidentifiedImageError:
            st.error("❌ Uploaded file is not a valid image")
            ocr_text = None

        # --- Voice recognition ---
        try:
            voice_text = recognize_speech(voice_path)
            st.write(f"🎤 Voice recognition result: **{voice_text}**")
        except Exception as e:
            st.error(f"❌ Failed to transcribe audio: {e}")
            voice_text = None

        # --- Verification ---
        if ocr_text and voice_text:
            match_dataset = None
            for entry in dataset:
                if entry["label_text"].lower() in ocr_text.lower():
                    match_dataset = entry["product"]
                    break

            if match_dataset:
                if match_dataset.lower() in voice_text.lower():
                    st.success(f"✅ Product Verified: {match_dataset}")
                else:
                    st.error(f"❌ Mismatch: OCR={match_dataset}, Voice={voice_text}")
            else:
                st.error("❌ Product not recognized in dataset")

# ---------------------------
# Tab 2: Sample Data Test
# ---------------------------
with tab2:
    sample_img = st.selectbox("Select sample image", os.listdir("sample_data/images"))
    sample_voice = st.selectbox("Select sample voice", os.listdir("sample_data/voices"))

    if st.button("Run Sample Test"):
        img_path = os.path.join("sample_data/images", sample_img)
        voice_path = os.path.join("sample_data/voices", sample_voice)

        img = Image.open(img_path).convert("RGB")
        st.image(img, caption=sample_img, use_column_width=True)

        ocr_text = pytesseract.image_to_string(img).strip()
        st.write(f"🔎 OCR detected text: **{ocr_text}**")

        voice_text = recognize_speech(voice_path)
        st.write(f"🎤 Voice recognition result: **{voice_text}**")

        match_dataset = None
        for entry in dataset:
            if entry["label_text"].lower() in ocr_text.lower():
                match_dataset = entry["product"]
                break

        if match_dataset:
            if match_dataset.lower() in voice_text.lower():
                st.success(f"✅ Product Verified: {match_dataset}")
            else:
                st.error(f"❌ Mismatch: OCR={match_dataset}, Voice={voice_text}")
        else:
            st.error("❌ Product not recognized in dataset")
