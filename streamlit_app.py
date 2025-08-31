import os
os.environ["STREAMLIT_SERVER_HEADLESS"] = "true"
os.environ["STREAMLIT_BROWSER_GATHER_USAGE_STATS"] = "false"
os.environ["BROWSER"] = "none"

import streamlit as st
from transformers import CLIPProcessor, CLIPModel, WhisperProcessor, WhisperForConditionalGeneration
from PIL import Image
import torch

st.set_page_config(page_title="Product Match POC", layout="centered")

# Load models
clip_model = CLIPModel.from_pretrained("openai/clip-vit-base-patch16")
clip_processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch16")
whisper_model = WhisperForConditionalGeneration.from_pretrained("openai/whisper-tiny")
whisper_processor = WhisperProcessor.from_pretrained("openai/whisper-tiny")

st.title("🧪 Product Match Checker (POC)")

image_file = st.file_uploader("Upload Product Image", type=["jpg","jpeg","png"])
audio_file = st.file_uploader("Upload Voice File", type=["wav","mp3"])

if st.button("Check Product") and image_file and audio_file:
    with st.spinner("Processing..."):
        # Speech to text
        audio_bytes = audio_file.read()
        audio_input = whisper_processor(audio_bytes, return_tensors="pt", sampling_rate=16000).input_features
        generated_ids = whisper_model.generate(audio_input)
        voice_text = whisper_processor.batch_decode(generated_ids, skip_special_tokens=True)[0]

        # Image-text matching
        image = Image.open(image_file).convert("RGB")
        inputs = clip_processor(text=[voice_text], images=image, return_tensors="pt", padding=True)
        outputs = clip_model(**inputs)
        similarity = outputs.logits_per_image.item()
        match = "✅ Product matches" if similarity > 0.2 else "❌ Product does not match"

    st.success("✅ Analysis Complete!")
    st.write("**Voice Text:**", voice_text)
    st.write("**Similarity Score:**", similarity)
    st.write("**Match Result:**", match)
