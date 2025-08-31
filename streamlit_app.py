import os
import json
import streamlit as st
from PIL import Image, UnidentifiedImageError
import pytesseract

# Load dataset
with open("sample_data/dataset.json", "r") as f:
    dataset = json.load(f)

st.title("📦 Product Verification via OCR")

# Upload files
uploaded_img = st.file_uploader("Upload product image", type=["jpg", "png", "jpeg"])
uploaded_voice = st.file_uploader("Upload voice sample", type=["wav", "mp3"])

if uploaded_img and uploaded_voice:
    if st.button("Verify Product"):
        # Save uploaded files temporarily
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

        # --- Verification against dataset ---
        if ocr_text:
            match_dataset = None
            for entry in dataset:
                if entry["label_text"].lower() in ocr_text.lower():
                    match_dataset = entry["product"]
                    break

            if match_dataset:
                st.success(f"✅ Product Verified: {match_dataset}")
            else:
                st.error("❌ Product text not recognized or mismatch")
