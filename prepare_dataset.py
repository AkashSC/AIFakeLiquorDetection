import os
import requests
from gtts import gTTS

os.makedirs("sample_data/images", exist_ok=True)
os.makedirs("sample_data/voices", exist_ok=True)

# --- Fixed sample logos (PNG/JPG) ---
images = {
    "coca_cola1.png": "https://upload.wikimedia.org/wikipedia/commons/thumb/1/15/Coca-Cola_logo.png/320px-Coca-Cola_logo.png",
    "coca_cola2.png": "https://upload.wikimedia.org/wikipedia/commons/thumb/0/09/Coca-Cola_bottle_cap.jpg/320px-Coca-Cola_bottle_cap.jpg",
    "pepsi1.png": "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a6/Pepsi_logo_2014.svg/320px-Pepsi_logo_2014.svg.png",
    "pepsi2.png": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4f/Pepsi_bottle_cap.jpg/320px-Pepsi_bottle_cap.jpg",
}

for filename, url in images.items():
    path = os.path.join("sample_data/images", filename)
    if not os.path.exists(path):
        r = requests.get(url, stream=True)
        if r.status_code == 200:
            with open(path, "wb") as f:
                f.write(r.content)
        else:
            print(f"Failed to download {filename} from {url}")

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
