import streamlit as st
import easyocr
from PIL import Image
import numpy as np
import cv2

st.title("📝 OCR Text Extractor & Verifier (EasyOCR)")

uploaded_file = st.file_uploader("Upload an image (JPG or PNG)", type=["jpg", "jpeg", "png"])

sample_dataset = ["Coca Cola", "Pepsi", "Budweiser", "Jack Daniels"]

reader = easyocr.Reader(['en'])  # English

if uploaded_file is not None:
    st.image(uploaded_file, caption="Uploaded Image", use_column_width=True)
    st.write("⏳ Running OCR, please wait...")

    try:
        image = Image.open(uploaded_file).convert("RGB")
        open_cv_image = np.array(image)
        open_cv_image = cv2.cvtColor(open_cv_image, cv2.COLOR_RGB2BGR)

        results = reader.readtext(open_cv_image)
        extracted_text = " ".join([res[1] for res in results])

        if extracted_text.strip():
            st.subheader("✅ Extracted Text:")
            st.text(extracted_text)

            matched = [word for word in sample_dataset if word.lower() in extracted_text.lower()]
            if matched:
                st.success(f"✔ Match found: {', '.join(matched)}")
            else:
                st.error("❌ No match found in dataset")
        else:
            st.warning("⚠ OCR failed: No text detected. Try a clearer image.")
    except Exception as e:
        st.error(f"OCR failed: {e}")
