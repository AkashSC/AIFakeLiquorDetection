import streamlit as st
import pandas as pd
import requests

# Sample dataset
sample_data = pd.DataFrame({
    "Brand": ["Coca Cola", "Pepsi", "Fanta"],
    "Keyword": ["Coca Cola", "Pepsi", "Fanta"]
})

API_KEY = "helloworld"  # Replace with your own OCR.Space API key

st.title("🚨 Product OCR Verification")

uploaded_file = st.file_uploader("Upload Product Image", type=["jpg", "jpeg", "png"])

if uploaded_file:
    st.image(uploaded_file, caption="Uploaded Image", use_column_width=True)

    if st.button("Verify Product"):
        files = {"file": uploaded_file.getvalue()}
        response = requests.post(
            "https://api.ocr.space/parse/image",
            files=files,
            data={"apikey": API_KEY, "language": "eng"}
        )
        result = response.json()

        # Safe check for ParsedResults
        parsed_results = result.get("ParsedResults")
        if parsed_results and len(parsed_results) > 0:
            extracted_text = parsed_results[0].get("ParsedText", "")
            st.subheader("Extracted Text")
            st.write(extracted_text)

            # Compare with sample dataset
            match = sample_data[sample_data["Keyword"].apply(
                lambda x: x.upper() in extracted_text.upper()
            )]
            if not match.empty:
                st.success(f"✅ Verified! Matched with {match.iloc[0]['Brand']}")
            else:
                st.error("⚠️ No match found. Possible counterfeit.")
        else:
            error_msg = result.get("ErrorMessage", ["Unknown error"])[0]
            st.error(f"❌ OCR failed: {error_msg}")
