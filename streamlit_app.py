import streamlit as st
from PIL import Image
import torch
import torchvision.transforms as transforms
from torchvision.models import resnet18
import speech_recognition as sr
import io

# ---------------- Streamlit config ----------------
st.set_page_config(page_title="Product Match POC", layout="centered")

st.title("🧪 Product Match Checker (Render Free Tier)")
st.write("Upload a product image and a voice description. The system will check if they match.")

# ---------------- Load ResNet18 ----------------
model = resnet18(pretrained=True)
model.eval()

# ---------------- Image preprocessing ----------------
preprocess = transforms.Compose([
    transforms.Resize(256),
    transforms.CenterCrop(224),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406],
                         std=[0.229, 0.224, 0.225])
])

# ---------------- File upload ----------------
image_file = st.file_uploader("Upload Product Image", type=["jpg","jpeg","png"])
audio_file = st.file_uploader("Upload Voice File", type=["wav","mp3"], help="Say the product name or description")

if st.button("Check Product") and image_file and audio_file:
    with st.spinner("Processing..."):
        # ---------------- Image recognition ----------------
        image = Image.open(image_file).convert("RGB")
        input_tensor = preprocess(image).unsqueeze(0)
        with torch.no_grad():
            outputs = model(input_tensor)
            _, predicted = torch.max(outputs, 1)
        
        # Load ImageNet class labels
        import json, requests
        labels_url = "https://raw.githubusercontent.com/pytorch/hub/master/imagenet_classes.txt"
        labels = requests.get(labels_url).text.splitlines()
        predicted_label = labels[predicted.item()]

        # ---------------- Speech-to-text ----------------
        recognizer = sr.Recognizer()
        audio_bytes = audio_file.read()
        audio_data = sr.AudioFile(io.BytesIO(audio_bytes))
        with audio_data as source:
            audio = recognizer.record(source)
        try:
            voice_text = recognizer.recognize_google(audio)
        except:
            voice_text = "Could not recognize speech"

        # ---------------- Compare ----------------
        match = "✅ Product matches" if predicted_label.lower() in voice_text.lower() else "❌ Product does not match"

    st.success("✅ Analysis Complete!")
    st.write("**Image Label:**", predicted_label)
    st.write("**Voice Text:**", voice_text)
    st.write("**Match Result:**", match)
