import streamlit as st
import requests

st.set_page_config(page_title="OCR Product Verifier", layout="centered")

st.title("📝 OCR Product Verifier")

# Load sample dataset
with open("sample_data.txt", "r") as f:
    sample_texts = [line.strip().lower() for line in f.readlines()]

uploaded_file = st.file_uploader("Upload a product image", type=["jpg","png"])

if uploaded_file is not None:
    st.image(uploaded_file, caption="Uploaded Image", use_column_width=True)
    
    if st.button("Verify Product"):
        st.info("Performing OCR...")
        # Prepare file for OCR.Space
        files = {"filename": uploaded_file.getvalue()}
        payload = {"apikey": "helloworld", "language": "eng"}
        try:
            response = requests.post("https://api.ocr.space/parse/image",
                                     files=files, data=payload)
            result = response.json()
            if result.get("ParsedResults"):
                extracted_text = result["ParsedResults"][0]["ParsedText"].strip()
                st.success(f"Extracted Text: {extracted_text}")

                # Compare with dataset
                match_found = any(extracted_text.lower() in s for s in sample_texts)
                if match_found:
                    st.success("✅ Product matches the dataset")
                else:
                    st.error("❌ Product does NOT match the dataset")
            else:
                st.error("❌ OCR failed. Make sure the image is clear and not too large.")
        except Exception as e:
            st.error(f"❌ OCR failed: {e}")
