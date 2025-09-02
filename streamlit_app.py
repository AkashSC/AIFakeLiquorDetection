import streamlit as st
from PIL import Image
import easyocr

# Streamlit page setup
st.set_page_config(page_title="OCR Product Verifier", layout="wide")

st.title("🍾 Fake Liquor Detection - OCR Verifier")

# File upload
uploaded_file = st.file_uploader("📤 Upload product label image", type=["png", "jpg", "jpeg"])

if uploaded_file:
    # Show uploaded image
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_column_width=True)

    st.write("🔍 Running OCR, please wait...")

    # Initialize EasyOCR (English only to keep it fast)
    reader = easyocr.Reader(['en'], gpu=False)

    # Run OCR on the uploaded image
    results = reader.readtext(uploaded_file.getvalue())

    if results:
        extracted_text = " ".join([res[1] for res in results])
        st.subheader("✅ OCR Extracted Text:")
        st.code(extracted_text)

        # --- Simple verification logic (sample dataset) ---
        # Imagine we have a list of valid brand names
        valid_brands = ["Coca Cola", "Pepsi", "Kingfisher", "Bacardi"]

        found = [brand for brand in valid_brands if brand.lower() in extracted_text.lower()]

        if found:
            st.success(f"✔️ Product Verified! Matched brand(s): {', '.join(found)}")
        else:
            st.error("⚠️ No matching brand found. Product might be fake!")
    else:
        st.error("❌ No text detected in the image.")
