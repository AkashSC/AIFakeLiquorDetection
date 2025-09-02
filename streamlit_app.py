import streamlit as st
from PIL import Image
import pytesseract

st.title("📷 OCR Test")

# Upload image
uploaded_file = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])

if uploaded_file is not None:
    # Open as PIL image
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_column_width=True)

    try:
        # Extract text
        extracted_text = pytesseract.image_to_string(image)

        if extracted_text.strip():
            st.success("✅ OCR Success")
            st.write("Extracted Text:")
            st.code(extracted_text)
        else:
            st.error("⚠️ OCR failed. Image might be unclear or empty text.")

    except Exception as e:
        st.error(f"OCR Error: {e}")
