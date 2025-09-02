import streamlit as st
from PIL import Image
import easyocr
import tempfile
import os

st.set_page_config(page_title="OCR Product Verifier", layout="wide")
st.title("🍾 Fake Liquor Detection - OCR Verifier")

uploaded_file = st.file_uploader("📤 Upload product label image", type=["png", "jpg", "jpeg"])

if uploaded_file:
    # Show image preview
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_column_width=True)

    st.write("🔍 Running OCR, please wait...")

    # Save uploaded file to a temporary location
    with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp_file:
        tmp_file.write(uploaded_file.getvalue())
        temp_path = tmp_file.name

    # Initialize EasyOCR (English only for speed)
    reader = easyocr.Reader(['en'], gpu=False)

    # Run OCR
    results = reader.readtext(temp_path)

    if results:
        extracted_text = " ".join([res[1] for res in results])
        st.subheader("✅ OCR Extracted Text:")
        st.code(extracted_text)

        # Simple brand verification
        valid_brands = ["Coca Cola", "Pepsi", "Kingfisher", "Bacardi"]
        found = [brand for brand in valid_brands if brand.lower() in extracted_text.lower()]

        if found:
            st.success(f"✔️ Product Verified! Matched brand(s): {', '.join(found)}")
        else:
            st.error("⚠️ No matching brand found. Product might be fake!")
    else:
        st.error("❌ No text detected in the image.")

    # Clean up temp file
    os.remove(temp_path)
