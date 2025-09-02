import streamlit as st
import requests

st.set_page_config(page_title="Fake Liquor Detector", layout="centered")
st.title("🍺 Fake Liquor Detection")

# Sample product dataset
dataset = ["Coca Cola", "Pepsi", "Fanta", "Sprite"]

uploaded_file = st.file_uploader("Upload product image (jpg/png)", type=["jpg", "png"])

if uploaded_file:
    st.image(uploaded_file, caption="Uploaded Image", use_column_width=True)

    if st.button("Verify Product"):
        st.info("Running OCR, please wait...")

        try:
            # OCR.space API request
            result = requests.post(
                "https://api.ocr.space/parse/image",
                files={"filename": uploaded_file.getvalue()},
                data={"apikey": "helloworld", "language": "eng"}
            ).json()

            parsed_text = result.get("ParsedResults")[0].get("ParsedText", "").strip()
            if parsed_text:
                st.success(f"Extracted Text: {parsed_text}")

                matches = [p for p in dataset if parsed_text.lower() in p.lower()]
                if matches:
                    st.success(f"✅ Product matches dataset: {matches}")
                else:
                    st.warning("❌ No match found in dataset.")
            else:
                st.error("OCR failed: Unable to extract text. Make sure the image is clear and not too large.")

        except Exception as e:
            st.error(f"OCR failed: {str(e)}")
