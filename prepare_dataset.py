import os
import requests
from gtts import gTTS

os.makedirs("sample_data/images", exist_ok=True)
os.makedirs("sample_data/voices", exist_ok=True)

# --- Sample logos ---
images = {
    "coca_cola1.jpg": "https://upload.wikimedia.org/wikipedia/commons/1/15/Coca-Cola_logo.png",
    "coca_cola2.jpg": "https://upload.wikimedia.org/wikipedia/commons/0/09/Coca-Cola_bottle_cap.jpg",
    "pepsi1.jpg": "https://upload.wikimedia.org/wikipedia/commons/a/a6/Pepsi_logo_2014.svg",
    "pepsi2.jpg": "https://upload.wikimedia.org/wikipedia/commons/4/4f/Pepsi_bottle_cap.jpg",
}

for filename, url in images.items():
    path = os.path.join("sample_data/images", filename)
    if not os.path.exists(path):
        r = requests.get(url, stream=True)
        with open(path, "wb") as f:
            f.write(r.content)

# --- Sample voices ---
voices = {
    "coca_test.wav": "Coca Cola",
    "pepsi_test.wav": "Pepsi",
}

for filename, text in voices.items():
    path = os.path.join("sample_data/voices", filename)
    if not os.path.exists(path):
        tts = gTTS(text=text, lang="en")
        mp3_path = path.replace(".wav", ".mp3")
        tts.save(mp3_path)
        os.system(f"ffmpeg -y -i {mp3_path} -ar 16000 -ac 1 {path}")
        os.remove(mp3_path)
