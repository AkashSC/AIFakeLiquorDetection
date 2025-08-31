import streamlit as st
from utils.cnn_image import predict_image
from utils.stt_vosk import record_and_transcribe, analyze_transcript

st.set_page_config(page_title="Fake Liquor CNN PoC", layout="centered")
st.title("🍾 Fake Liquor Detector — CNN PoC")

tab1, tab2 = st.tabs(["📷 Image Check", "🗣️ Simulate Voice"])

# Image Tab
with tab1:
    st.subheader("Upload bottle photo")
    img_file = st.file_uploader("Image (PNG/JPG)", type=["png","jpg","jpeg"])
    if img_file:
        result = predict_image(img_file)
        st.image(img_file, caption="Uploaded image", use_column_width=True)
        if result["label"]=="Genuine":
            st.success(f"✅ Genuine Bottle ({result['confidence']*100:.1f}%)")
        else:
            st.error(f"❌ Suspicious / Fake ({result['confidence']*100:.1f}%)")

# Voice Simulation Tab
with tab2:
    st.subheader("Simulate voice check")
    if st.button("Simulate Voice Check"):
        transcript = record_and_transcribe()
        result = analyze_transcript(transcript)
        st.text_area("Transcript", value=result["transcript"], height=100)
        if result["verdict"]=="OK":
            st.success("✅ Voice OK")
        else:
            st.error("❌ Voice SUSPICIOUS")
