import streamlit as st
from pathlib import Path
from utils.image_checks import analyze_image
from utils.stt_vosk import record_and_transcribe, analyze_transcript
from streamlit_webrtc import webrtc_streamer, AudioProcessorBase, RTCConfiguration

st.set_page_config(page_title="Fake Liquor Detector PoC", layout="centered")
st.title("🍾 Fake Liquor Detector — Render Free PoC")

BASE = Path(__file__).parent
LOGO_TEMPLATE = BASE / "sample_data" / "logo_template.png"

tab1, tab2 = st.tabs(["📷 Image Check", "🎙️ Voice Check"])

# -------------------- Image Tab --------------------
with tab1:
    st.subheader("Upload bottle photo")
    img_file = st.file_uploader("Image (PNG/JPG)", type=["png","jpg","jpeg"])
    if img_file:
        details = analyze_image(img_file, LOGO_TEMPLATE)
        st.image(img_file, caption="Uploaded image", use_column_width=True)
        if details["match"]:
            st.success("✅ Genuine / Matches Template")
        else:
            st.error("❌ Suspicious / Does Not Match Template")
        st.json(details)

# -------------------- Voice Tab --------------------
with tab2:
    st.subheader("Record your voice")
    st.caption("Click 'Start' below and speak for a few seconds. Browser audio is captured.")
    
    RTC_CONFIGURATION = RTCConfiguration({
        "iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]
    })

    webrtc_ctx = webrtc_streamer(
        key="voice",
        mode="SENDONLY",
        rtc_configuration=RTC_CONFIGURATION,
        media_stream_constraints={"audio": True, "video": False},
        async_processing=False,
    )

    if webrtc_ctx.state.playing:
        # Dummy transcript for now
        transcript = record_and_transcribe()
        result = analyze_transcript(transcript)
        st.text_area("Transcript", value=result["transcript"], height=100)
        if result["verdict"] == "OK":
            st.success("✅ Voice OK")
        else:
            st.error("❌ Voice SUSPICIOUS")
