import streamlit as st
import requests
from PIL import Image
import io

# -----------------------------
# Load dataset
# -----------------------------
with open("sample_data/dataset.txt", "r") as f:
    dataset = [line.strip() for line in f.readlines()]

# -----------------------------
# Streamlit UI
# -----------------------------
st.set_page_config(page_title="🍺 OCR Product Verifier", page_icon="🍺")

st.title("🍺 OCR Product Verifier")
st.write("Upload a product image, and we'll check if it matches our dataset.")

uploaded_file = st.file_uploader("Upload Image", type=["jpg","jpeg","png"])

if uploaded_file:
    st.image(uploaded_file, caption="Uploaded Image", use_column_width=True)

    if st.button("Verify Product"):
        st.info("Running OCR, please wait...")

        try:
            # Send the file with proper filename and content type
            files = {
                "filename": (uploaded_file.name, uploaded_file, uploaded_file.type)
            }
            data = {"apikey": "helloworld", "language": "eng"}

            response = requests.post(
                "https://api.ocr.space/parse/image",
                files=files,
                data=data
            )

            result = response.json()

            if "ParsedResults" in result and result["ParsedResults"]:
                parsed_text = result["ParsedResults"][0].get("ParsedText", "").strip()

                if parsed_text:
                    st.success(f"Extracted Text: {parsed_text}")

                    matches = [p for p in dataset if parsed_text.lower() in p.lower()]
                    if matches:
                        st.success(f"✅ Product matches dataset: {matches}")
                    else:
                        st.warning("❌ No match found in dataset.")
                else:
                    st.error("OCR failed: No text detected in image.")
            else:
                error_message = result.get("ErrorMessage", "Unknown error from OCR API")
                st.error(f"OCR failed: {error_message}")

        except Exception as e:
            st.error(f"OCR request failed: {str(e)}")
