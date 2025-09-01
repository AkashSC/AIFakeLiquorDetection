import streamlit as st
import pandas as pd
from PIL import Image
import io

# -------------------------------
# Load dataset (sample CSV of products)
# -------------------------------
@st.cache_data
def load_dataset():
    # Dataset file: sample_dataset.csv
    return pd.read_csv("sample_dataset.csv")

dataset = load_dataset()

# -------------------------------
# OCR Setup
# -------------------------------
try:
    import easyocr
    reader = easyocr.Reader(['en'], gpu=False)
    OCR_ENGINE = "easyocr"
except Exception:
    import pytesseract
    OCR_ENGINE = "pytesseract"

def run_ocr(image_bytes):
    if OCR_ENGINE == "easyocr":
        results = reader.readtext(image_bytes)
        text = " ".join([res[1] for res in results])
    else:
        img = Image.open(io.BytesIO(image_bytes))
        text = pytesseract.image_to_string(img)
    return text.strip()

# -------------------------------
# Streamlit UI
# -------------------------------
st.set_page_config(page_title="🧾 Product Verification OCR", layout="centered")
st.title("🧾 Product Verification via OCR")

uploaded_file = st.file_uploader("📤 Upload product image", type=["jpg", "jpeg", "png"])

if uploaded_file:
    st.image(uploaded_file, caption="Uploaded Image", use_column_width=True)

    if st.button("✅ Verify Product"):
        with st.spinner("Running OCR..."):
            try:
                image_bytes = uploaded_file.read()
                extracted_text = run_ocr(image_bytes)

                st.subheader("📜 Extracted Text")
                st.text(extracted_text if extracted_text else "No text found.")

                # Compare with dataset
                matched = dataset[dataset['product_name'].str.contains(extracted_text, case=False, na=False)]

                st.subheader("🔎 Match Result")
                if not matched.empty:
                    st.success(f"✅ Match Found: {matched.iloc[0]['product_name']}")
                else:
                    st.error("❌ No match found in dataset.")

            except Exception as e:
                st.error(f"OCR failed: {str(e)}")
