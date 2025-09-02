import streamlit as st
import pytesseract
from PIL import Image
import cv2
import numpy as np
import os

# 🔑 explicitly set tesseract binary path
pytesseract.pytesseract.tesseract_cmd = "/usr/bin/tesseract"

st.title("📝 OCR Text Extractor & Verifier")

uploaded_file = st.file_uploader("Upload an image (JPG or PNG)", type=["jpg", "jpeg", "png"])

# Example dataset
sample_dataset = ["Coca Cola", "Pepsi", "Budweiser", "Jack Daniels"]

if uploaded_file is not None:
    st.image(uploaded_file, caption="Uploaded Image", use_column_width=True)

    st.write("⏳ Running OCR, please wait...")

    try:
        # Load image
        image = Image.open(uploaded_file).convert("RGB")
        open_cv_image = np.array(image)
        open_cv_image = cv2.cvtColor(open_cv_image, cv2.COLOR_RGB2BGR)

        # Extract text
        extracted_text = pytesseract.image_to_string(open_cv_image)

        if extracted_text.strip():
            st.subheader("✅ Extracted Text:")
            st.text(extracted_text)

            # Verify
            matched = [word for word in sample_dataset if word.lower() in extracted_text.lower()]
            if matched:
                st.success(f"✔ Match found: {', '.join(matched)}")
            else:
                st.error("❌ No match found in dataset")
        else:
            st.warning("⚠ OCR failed: No text detected. Try a clearer image.")

    except Exception as e:
        st.error(f"OCR failed: {e}")
