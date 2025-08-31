import streamlit as st
import easyocr
from PIL import Image
import os

# Load dataset
with open("dataset.txt", "r") as f:
    dataset = [line.strip().lower() for line in f.readlines()]

# Initialize EasyOCR reader
reader = easyocr.Reader(['en'], gpu=False)

st.title("📦 Product Verification (OCR)")

uploaded_file = st.file_uploader("Upload a product image", type=["jpg", "jpeg", "png"])

if uploaded_file:
    # Show image
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_container_width=True)

    # Button to trigger verification
    if st.button("🔍 Verify Product"):
        with st.spinner("Reading text..."):
            # Perform OCR
            result = reader.readtext(image, detail=0)
            extracted_text = " ".join(result).lower()

        st.subheader("📖 Extracted Text")
        st.write(extracted_text if extracted_text else "⚠️ No text detected")

        # Compare with dataset
        match = None
        for item in dataset:
            if item in extracted_text:
                match = item
                break

        st.subheader("✅ Verification Result")
        if match:
            st.success(f"Product matched: **{match.upper()}**")
        else:
            st.error("❌ No matching product found in dataset.")
