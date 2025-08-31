import streamlit as st
from utils.stt_vosk import analyze_transcript

st.title("🎙️ Voice Check (Dummy Vosk)")

audio_data = st.audio_recorder(key="audio", format="wav", max_length=5)  # 5 sec max
if audio_data is not None:
    st.audio(audio_data)  # playback
    transcript = "Bottle looks intact and authorized"  # dummy
    result = analyze_transcript(transcript)
    st.text_area("Transcript", value=result["transcript"], height=100)
    if result["verdict"]=="OK":
        st.success("✅ Voice OK")
    else:
        st.error("❌ Voice SUSPICIOUS")
