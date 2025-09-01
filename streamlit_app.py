import streamlit as st
import pandas as pd
from PIL import Image
import io

st.set_page_config(page_title="OCR Product Verification", layout="centered")
st.title("📷 OCR Product Verification")

# Load dataset
df = pd.read_csv("sample_dataset.csv")

# Initialize EasyOCR once
import easyocr
reader = easyocr.Reader(['en'], gpu=False)

def run_ocr(image_bytes):
    results = reader.readtext(image_bytes)
    text = " ".join([res[1] for res in results])
    return text.strip()

# Upload image
uploaded_file = st.file_uploader("Upload a product image", type=["jpg","jpeg","png"])
if uploaded_file:
    st.image(uploaded_file, caption="Uploaded Image", use_column_width=True)
    if st.button("🔍 Verify Product"):
        image_bytes = uploaded_file.read()
        extracted_text = run_ocr(image_bytes)

        st.subheader("📑 Extracted Text")
        st.text(extracted_text if extracted_text else "No text found.")

        # Compare with dataset
        match = False
        matched_item = None
        for product in df["product_name"]:
            if product.lower() in extracted_text.lower():
                match = True
                matched_item = product
                break

        if match:
            st.success(f"✅ Match found: {matched_item}")
        else:
            st.error("❌ No match found in dataset.")
