import streamlit as st
import requests
import pandas as pd

# Free demo API key from OCR.Space
API_KEY = "helloworld"  # replace with your own for production

sample_data = pd.DataFrame({
    "Brand": ["Kingfisher", "Corona", "Budweiser","Coca Cola"],
    "Keyword": ["ORIGINAL", "MEXICO", "USA", "USA"]
})

st.set_page_config(page_title="Fake Liquor Detection", page_icon="🍺")
st.title("🍺 Fake Liquor Detection (OCR via API)")

uploaded_file = st.file_uploader("Upload label image", type=["jpg", "jpeg", "png"])

if uploaded_file:
    st.image(uploaded_file, caption="Uploaded Label", use_column_width=True)

    if st.button("Verify Product"):
        files = {'file': uploaded_file.getvalue()}
        response = requests.post(
            "https://api.ocr.space/parse/image",
            files=files,
            data={"apikey": API_KEY, "language": "eng"}
        )

        result = response.json()
        extracted_text = result["ParsedResults"][0]["ParsedText"]
        st.subheader("Extracted Text")
        st.write(extracted_text)

        # Check for keyword match
        match = sample_data[sample_data["Keyword"].apply(
            lambda x: x.upper() in extracted_text.upper()
        )]

        if not match.empty:
            st.success(f"✅ Verified! Matched with {match.iloc[0]['Brand']}")
        else:
            st.error("⚠️ No match found. Possible counterfeit.")
