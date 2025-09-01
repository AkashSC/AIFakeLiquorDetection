import streamlit as st
import easyocr
import pandas as pd
import tempfile
import os

# Sample dataset (you can replace with DB or CSV later)
VALID_PRODUCTS = {
    "WHISKY123": "Original Brand Whisky",
    "VODKA456": "Premium Vodka",
    "RUM789": "Dark Rum"
}

st.title("🍾 Fake Liquor Detection (OCR Verification)")

uploaded_file = st.file_uploader("Upload product label image", type=["jpg", "jpeg", "png"])

if uploaded_file:
    # Save to temp file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmp_file:
        tmp_file.write(uploaded_file.read())
        tmp_path = tmp_file.name

    if st.button("Verify Product"):
        try:
            reader = easyocr.Reader(["en"], gpu=False)
            result = reader.readtext(tmp_path, detail=0)
            extracted_text = " ".join(result)

            st.subheader("🔍 OCR Extracted Text")
            st.write(extracted_text)

            # Check against dataset
            matched = [code for code in VALID_PRODUCTS if code in extracted_text.upper()]

            if matched:
                st.success(f"✅ Match Found: {VALID_PRODUCTS[matched[0]]}")
            else:
                st.error("❌ No match found in dataset.")

        except Exception as e:
            st.error(f"OCR failed: {e}")

    # Cleanup
    os.remove(tmp_path)
