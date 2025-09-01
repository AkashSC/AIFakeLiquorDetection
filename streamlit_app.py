import streamlit as st
import pandas as pd
import numpy as np
import easyocr
import pytesseract
from PIL import Image

# Must be first command
st.set_page_config(page_title="Fake Liquor Detector", layout="centered")

# Load dataset (example)
DATA_FILE = "sample_data.csv"
data = pd.read_csv(DATA_FILE)

# EasyOCR reader
reader = easyocr.Reader(['en'], gpu=False)

st.title("🍾 Fake Liquor Detector (OCR)")

uploaded_file = st.file_uploader("Upload Product Image", type=["jpg", "jpeg", "png"])

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Product", use_container_width=True)

    if st.button("Verify Product"):
        ocr_text = ""

        # Try EasyOCR first
        try:
            results = reader.readtext(np.array(image))
            ocr_text = " ".join([res[1] for res in results])
            st.success("✅ OCR via EasyOCR successful")
        except Exception as e:
            st.warning(f"EasyOCR failed: {e}")
            # Fallback: pytesseract
            try:
                ocr_text = pytesseract.image_to_string(image)
                st.info("⚠️ Using fallback OCR: Tesseract")
            except Exception as e2:
                st.error(f"OCR failed completely: {e2}")

        st.text_area("Extracted Text", ocr_text, height=120)

        if ocr_text:
            matches = data[data.apply(lambda row: row.astype(str).str.contains(ocr_text, case=False).any(), axis=1)]
            if not matches.empty:
                st.success("✅ Match Found in Dataset")
                st.dataframe(matches)
            else:
                st.error("❌ No Match Found – Product may be fake")
