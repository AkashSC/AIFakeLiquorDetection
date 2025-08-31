
import streamlit as st
from pathlib import Path
import json
from utils.image_checks import analyze_image
from utils.voice_checks import analyze_transcript

st.set_page_config(page_title="Fake Liquor Detector (PoC)", page_icon="🍾", layout="centered")
st.title("🍾 Fake Liquor Detection — Image + Voice (Tiny PoC)")

st.markdown("""
This PoC uses **tiny heuristic models**:
- Image: histogram/edge/blur features vs a template
- Voice: simple keyword risk from a transcript (or your own description)
- Fusion: weighted average → final risk
""")

BASE = Path(__file__).parent
MODEL_CFG = BASE / "models" / "tiny_rules.json"
LOGO_TEMPLATE = BASE / "sample_data" / "logo_template.png"

with st.sidebar:
    st.header("⚙️ Settings")
    cfg = json.loads(MODEL_CFG.read_text())
    w_image = st.slider("Fusion weight — Image", 0.0, 1.0, float(cfg["fusion"]["w_image"]), 0.05)
    w_voice = 1.0 - w_image
    st.caption(f"Fusion weight — Voice: **{w_voice:.2f}**")

tab1, tab2 = st.tabs(["📷 Image Check", "🎙️ Voice Claim"])

with tab1:
    st.subheader("Upload bottle photo")
    img_file = st.file_uploader("Image (PNG/JPG)", type=["png","jpg","jpeg"])
    if img_file:
        details = analyze_image(img_file, str(MODEL_CFG), str(LOGO_TEMPLATE))
        st.image(img_file, caption="Uploaded image", use_column_width=True)
        st.json(details)

with tab2:
    st.subheader("Describe your observation (voice/text)")
    st.caption("For PoC, paste the transcript of what you (or the customer) said about the bottle.")
    t = st.text_area("Transcript", placeholder="e.g., Seal looks tampered, label is crooked...")
    voice_risk = None
    if t.strip():
        vd = analyze_transcript(t, str(MODEL_CFG))
        st.json(vd)
        voice_risk = vd["voice_risk"]

st.divider()
st.subheader("🔗 Fusion & Verdict")

img_risk = None
if 'details' in locals():
    img_risk = details["image_risk"]

voice_risk = voice_risk if 'voice_risk' in locals() and voice_risk is not None else None

col1, col2 = st.columns(2)
with col1:
    st.metric("Image risk", f"{(img_risk if img_risk is not None else 0.0)*100:.1f}%")
with col2:
    st.metric("Voice risk", f"{(voice_risk if voice_risk is not None else 0.0)*100:.1f}%")

if img_risk is None and voice_risk is None:
    st.info("Provide at least an image or a transcript to compute a verdict.")
else:
    fr = ( (img_risk if img_risk is not None else 0.0)*w_image +
           (voice_risk if voice_risk is not None else 0.0)*(1-w_image) )
    st.metric("Final fused risk", f"{fr*100:.1f}%")

    cfg = json.loads(MODEL_CFG.read_text())
    if fr <= cfg["risk_thresholds"]["pass"]:
        st.success("✅ Likely Genuine — low risk. Proceed.")
    elif fr <= cfg["risk_thresholds"]["review"]:
        st.warning("🟨 Needs Manual Review — medium risk.")
    else:
        st.error("🟥 Likely Fake — high risk. Flag and escalate.")

st.divider()
st.caption("PoC only. For production, fine-tune a tiny CNN (e.g., MobileNetV2) on real bottle photos and use small-STT for voice (e.g., Vosk small).")
