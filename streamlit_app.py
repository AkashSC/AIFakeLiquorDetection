import easyocr
import streamlit as st
from PIL import Image
import numpy as np

st.set_page_config(page_title="Fake Liquor Detection", layout="centered")

st.title("🍾 Fake Liquor Detection with OCR")

# Initialize EasyOCR reader once
reader = easyocr.Reader(['en'])

uploaded_file = st.file_uploader("Upload product label", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Label", use_container_width=True)

    if st.button("Verify Product"):
        with st.spinner("Extracting text..."):
            result = reader.readtext(np.array(image))

        extracted_text = " ".join([res[1] for res in result])
        st.subheader("Extracted Text:")
        st.write(extracted_text)

        # Dummy verification step
        if "ORIGINAL" in extracted_text.upper():
            st.success("✅ Product verified as authentic!")
        else:
            st.error("⚠️ Warning: Product may be counterfeit.")
