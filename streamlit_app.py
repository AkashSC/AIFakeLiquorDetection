import streamlit as st
import torch
from transformers import CLIPProcessor, CLIPModel, WhisperProcessor, WhisperForConditionalGeneration
from PIL import Image
import os

# ---------------- Render-friendly config ----------------
st.set_page_config(page_title="Product Match POC", layout="centered")
os.environ["STREAMLIT_GATHER_USAGE_STATS"] = "false"
os.environ["BROWSER"] = "none"

# ---------------- CLIP for image-text matching ----------------
clip_model = CLIPModel.from_pretrained("openai/clip-vit-base-patch16")
clip_processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch16")

# ---------------- Whisper for speech-to-text ----------------
whisper_model_name = "openai/whisper-tiny"  # small & fast
whisper_model = WhisperForConditionalGeneration.from_pretrained(whisper_model_name)
whisper_processor = WhisperProcessor.from_pretrained(whisper_model_name)

st.title("🧪 Product Match Checker (POC)")
st.write("Upload a product image and a voice description. The system will check if they match.")

# ---------------- Upload Inputs ----------------
image_file = st.file_uploader("Upload Product Image", type=["jpg", "jpeg", "png"])
audio_file = st.file_uploader("Upload Voice File", type=["wav", "mp3"], help="Say the product name or description")

if st.button("Check Product") and image_file and audio_file:
    with st.spinner("Processing..."):
        # ---------------- Speech-to-text with Whisper ----------------
        audio_bytes = audio_file.read()
        audio_input = whisper_processor(audio_bytes, return_tensors="pt", sampling_rate=16000).input_features
        generated_ids = whisper_model.generate(audio_input)
        voice_text = whisper_processor.batch_decode(generated_ids, skip_special_tokens=True)[0]

        # ---------------- Image-text similarity with CLIP ----------------
        image = Image.open(image_file).convert("RGB")
        inputs = clip_processor(text=[voice_text], images=image, return_tensors="pt", padding=True)
        outputs = clip_model(**inputs)
        similarity = outputs.logits_per_image.item()
        match = "✅ Product matches" if similarity > 0.2 else "❌ Product does not match"

    st.success("✅ Analysis Complete!")
    st.write("**Voice Text:**", voice_text)
    st.write("**Similarity Score:**", similarity)
    st.write("**Match Result:**", match)

# ---------------- Streamlit Info ----------------
st.markdown("---")
st.markdown("**Note:** Running on Render Free Tier. Make sure to open the public URL provided by Render, not 0.0.0.0.")
