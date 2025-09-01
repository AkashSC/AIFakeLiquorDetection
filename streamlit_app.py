import streamlit as st
import pandas as pd
from PIL import Image
import pytesseract

# Load dataset
@st.cache_data
def load_dataset():
    return pd.read_csv("sample_dataset.csv")

dataset = load_dataset()

def run_ocr(image_file):
    img = Image.open(image_file)
    text = pytesseract.image_to_string(img)
    return text.strip()

# Streamlit UI
st.set_page_config(page_title="🧾 Product Verification OCR", layout="centered")
st.title("🧾 Product Verification via OCR")

uploaded_file = st.file_uploader("📤 Upload product image", type=["jpg", "jpeg", "png"])

if uploaded_file:
    st.image(uploaded_file, caption="Uploaded Image", use_column_width=True)

    if st.button("✅ Verify Product"):
        with st.spinner("Running OCR..."):
            extracted_text = run_ocr(uploaded_file)

            st.subheader("📜 Extracted Text")
            st.text(extracted_text if extracted_text else "No text found.")

            matched = dataset[dataset['product_name'].str.contains(extracted_text, case=False, na=False)]

            st.subheader("🔎 Match Result")
            if not matched.empty:
                st.success(f"✅ Match Found: {matched.iloc[0]['product_name']}")
            else:
                st.error("❌ No match found in dataset.")
