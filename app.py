import streamlit as st
from streamlit_webrtc import webrtc_streamer, AudioProcessorBase, RTCConfiguration

from utils.stt_vosk import record_and_transcribe, analyze_transcript

st.title("🍾 Fake Liquor Detector — Voice Check")

RTC_CONFIGURATION = RTCConfiguration({"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]})

webrtc_ctx = webrtc_streamer(
    key="voice",
    mode="SENDONLY",
    rtc_configuration=RTC_CONFIGURATION,
    media_stream_constraints={"audio": True, "video": False},
)

if webrtc_ctx.audio_receiver:
    transcript = record_and_transcribe()  # dummy transcript
    result = analyze_transcript(transcript)
    st.text_area("Transcript", value=result["transcript"], height=100)
    if result["verdict"]=="OK":
        st.success("✅ Voice OK")
    else:
        st.error("❌ Voice SUSPICIOUS")
