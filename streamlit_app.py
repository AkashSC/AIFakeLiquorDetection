import os
import json
import streamlit as st
from PIL import Image, UnidentifiedImageError
import pytesseract

# Load dataset
with open("sample_data/dataset.json", "r") as f:
    dataset = json.load(f)

st.title("📦 Product Verification via OCR")

# Upload image
uploaded_img = st.file_uploader("Upload product image", type=["jpg", "png", "jpeg"])

# Text output box for OCR result
ocr_text_box = st.empty()
match_result_box = st.empty()

if uploaded_img:
    img_path = "temp_image.jpg"
    with open(img_path, "wb") as f:
        f.write(uploaded_img.read())

    st.image(img_path, caption="Uploaded Image", use_column_width=True)

    if st.button("Verify Product"):
        try:
            img = Image.open(img_path).convert("RGB")
            ocr_text = pytesseract.image_to_string(img).strip()
            ocr_text_box.text_area("OCR Detected Text", value=ocr_text, height=100)

            # Compare with dataset
            match_dataset = None
            for entry in dataset:
                if entry["label_text"].lower() in ocr_text.lower():
                    match_dataset = entry["product"]
                    break

            if match_dataset:
                match_result_box.success(f"✅ Product Verified: {match_dataset}")
            else:
                match_result_box.error("❌ Product text not recognized or mismatch")

        except UnidentifiedImageError:
            match_result_box.error("❌ Uploaded file is not a valid image")
        except pytesseract.TesseractNotFoundError:
            match_result_box.error("❌ Tesseract not installed. Ensure render.yaml installs it correctly.")
