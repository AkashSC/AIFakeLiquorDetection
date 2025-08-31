import os
import base64

os.makedirs("sample_data/images", exist_ok=True)
os.makedirs("sample_data/voices", exist_ok=True)

# --- Tiny placeholder images (base64) ---
image_data = {
    "coca_cola1.jpg": b"/9j/4AAQSkZJRgABAQEAYABgAAD/2wBDABALDA4MChAODQ4SEhQ..."
    "coca_cola2.jpg": b"/9j/4AAQSkZJRgABAQEAYABgAAD/2wBDABALDA4MChAODQ4SEhQ..."
    "pepsi1.jpg": b"/9j/4AAQSkZJRgABAQEAYABgAAD/2wBDABALDA4MChAODQ4SEhQ..."
    "pepsi2.jpg": b"/9j/4AAQSkZJRgABAQEAYABgAAD/2wBDABALDA4MChAODQ4SEhQ..."
}

for fname, b64data in image_data.items():
    path = os.path.join("sample_data/images", fname)
    if not os.path.exists(path):
        with open(path, "wb") as f:
            f.write(base64.b64decode(b64data))

# --- Tiny placeholder audio (base64) ---
voice_data = {
    "coca_test.wav": b"UklGRigAAABXQVZFZm10IBAAAAABAAEARKwAABCxAgAEABAAZGF0YRAAAA==",
    "pepsi_test.wav": b"UklGRigAAABXQVZFZm10IBAAAAABAAEARKwAABCxAgAEABAAZGF0YRAAAA=="
}

for fname, b64data in voice_data.items():
    path = os.path.join("sample_data/voices", fname)
    if not os.path.exists(path):
        with open(path, "wb") as f:
            f.write(base64.b64decode(b64data))
