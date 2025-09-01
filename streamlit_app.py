import streamlit as st
import pandas as pd
from PIL import Image
import pytesseract
import io

# ✅ must be the first Streamlit command
st.set_page_config(page_title="OCR Product Verification", layout="centered")

# Load dataset (sample product names)
DATA_FILE = "sample_dataset.csv"
df = pd.read_csv(DATA_FILE)

st.title("📷 OCR Product Verification")

uploaded_file = st.file_uploader("Upload a product image", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # Show image preview
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_column_width=True)

    if st.button("🔍 Verify Product"):
        try:
            # Run OCR
            extracted_text = pytesseract.image_to_string(image)
            st.subheader("📑 Extracted Text:")
            st.text(extracted_text.strip())

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
                st.error("❌ No matching product found in dataset.")

        except Exception as e:
            st.error(f"OCR failed: {e}")
