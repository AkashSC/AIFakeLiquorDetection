import streamlit as st
import requests
import pandas as pd

# -----------------------------
# Config
# -----------------------------
st.set_page_config(page_title="Fake Liquor Detector", layout="centered")

OCR_API_KEY = "helloworld"  # Free test key from OCR.space

# -----------------------------
# Sample dataset
# -----------------------------
# Example CSV with product names
data = pd.DataFrame({
    "Product": ["Coca Cola", "Pepsi", "Fanta", "Sprite"]
})

st.title("🍺 Fake Liquor Detection (OCR)")

uploaded_file = st.file_uploader("Upload product image (jpg/png)", type=["jpg", "png"])

if uploaded_file:
    st.image(uploaded_file, caption="Uploaded Image", use_column_width=True)

    if st.button("Verify Product"):
        st.info("Running OCR, please wait...")

        # Send image to OCR.space
        result = requests.post(
            "https://api.ocr.space/parse/image",
            files={"filename": uploaded_file.getvalue()},
            data={"apikey": OCR_API_KEY, "language": "eng"}
        ).json()

        # Extract text safely
        parsed_text = ""
        try:
            parsed_text = result.get("ParsedResults")[0].get("ParsedText", "")
        except Exception:
            st.error("OCR failed. Make sure the image is clear and not too large.")

        if parsed_text:
            st.success(f"Extracted Text: {parsed_text}")

            # Check matching with dataset
            matches = data[data["Product"].str.contains(parsed_text.strip(), case=False)]
            if not matches.empty:
                st.success(f"✅ Product matches dataset: {matches['Product'].tolist()}")
            else:
                st.warning("❌ No match found in dataset.")
