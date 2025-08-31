import os
import json
import streamlit as st
from PIL import Image
import pytesseract

# Load dataset
with open("sample_data/dataset.json", "r") as f:
    dataset = json.load(f)

st.title("📦 Product Verification using OCR")

# Upload image
uploaded_img = st.file_uploader("Upload product image", type=["jpg", "png", "jpeg"])

if uploaded_img:
    img = Image.open(uploaded_img).convert("RGB")
    st.image(img, caption="Uploaded Image", use_column_width=True)

    # --- OCR ---
    ocr_text = pytesseract.image_to_string(img).strip()
    st.write(f"🔎 OCR detected text: **{ocr_text}**")

    # --- Compare with dataset ---
    match_found = False
    for entry in dataset:
        if entry["label_text"].lower() in ocr_text.lower():
            st.success(f"✅ Product Verified: {entry['product']}")
            match_found = True
            break

    if not match_found:
        st.error("❌ Product text not recognized or mismatch")
