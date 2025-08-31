import streamlit as st
from PIL import Image
import torch
import torchvision.transforms as transforms
from torchvision.models import resnet18, ResNet18_Weights
import speech_recognition as sr
import io

st.set_page_config(page_title="Product Match POC", layout="centered")
st.title("🧪 Product Match Checker (Render Free Tier)")

# ---------------- Load ResNet18 with DEFAULT weights ----------------
weights = ResNet18_Weights.DEFAULT
model = resnet18(weights=weights)
model.eval()
labels = weights.meta["categories"]

# ---------------- Image preprocessing ----------------
preprocess = transforms.Compose([
    transforms.Resize(256),
    transforms.CenterCrop(224),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406],
                         std=[0.229, 0.224, 0.225])
])

# ---------------- Upload Inputs ----------------
image_file = st.file_uploader("Upload Product Image", type=["jpg","jpeg","png"])
audio_file = st.file_uploader("Upload Voice File", type=["wav","mp3"], help="Say the product name or description")

if st.button("Check Product") and image_file and audio_file:
    with st.spinner("Processing..."):
        # Image recognition
        image = Image.open(image_file).convert("RGB")
        input_tensor = preprocess(image).unsqueeze(0)
        with torch.no_grad():
            outputs = model(input_tensor)
            _, predicted = torch.max(outputs, 1)
        predicted_label = labels[predicted.item()]

        # Speech-to-text
        recognizer = sr.Recognizer()
        audio_bytes = audio_file.read()
        audio_data = sr.AudioFile(io.BytesIO(audio_bytes))
        with audio_data as source:
            audio = recognizer.record(source)
        try:
            voice_text = recognizer.recognize_google(audio)
        except:
            voice_text = "Could not recognize speech"

        # Compare
        match = "✅ Product matches" if predicted_label.lower() in voice_text.lower() else "❌ Product does not match"

    st.success("✅ Analysis Complete!")
    st.write("**Image Label:**", predicted_label)
    st.write("**Voice Text:**", voice_text)
    st.write("**Match Result:**", match)
