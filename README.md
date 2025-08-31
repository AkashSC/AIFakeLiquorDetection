
# Fake Liquor Detection — Image + Voice (Tiny PoC)

This is a **minimal** end-to-end PoC that detects potentially fake liquor products using **image heuristics** and **voice/text claims**, fused into a single risk score.

## What’s inside
- `app.py` — Streamlit app (single-page)
- `utils/image_checks.py` — tiny image feature checks (histogram correlation, edge density, blur)
- `utils/voice_checks.py` — keyword-based voice risk from transcript
- `models/tiny_rules.json` — threshold/weights config (acts as a **very small model**)
- `sample_data/` — generated images (4 real + 4 fake), logo template, transcripts, and placeholder WAVs

> No heavy ML frameworks are required for the basic PoC. Everything runs with **PIL + numpy**.

## Setup

```bash
python -m venv .venv && source .venv/bin/activate  # (Windows: .venv\Scripts\activate)
pip install -r requirements.txt
streamlit run app.py
```

Open the app in your browser. Upload a **bottle image** and paste a **transcript** (or your observation) to get a fused risk and verdict.

## Requirements

```
streamlit
pillow
numpy
```

> Optional (if you plan to add speech-to-text later): `vosk`, `soundfile`, `pydub`, `opencv-python-headless`

## How the tiny model works

**Image:**  
- Compute histogram correlation to a reference logo template (higher is better).  
- Compute edge density difference (label skew/printing noise increases it).  
- Compute a blur score (too low sharpness increases risk).  
Weighted combination → **image risk**.

**Voice:**  
- Count suspicious vs reassuring keywords in the transcript.  
Squash to 0–1 → **voice risk**.

**Fusion:**  
Weighted average of image and voice risk. Thresholds define **pass / review / fail**.

## Upgrading to a tiny learned model

When you want a **small learned model**:

### Image (MobileNetV2, ~14MB)

1. Collect 200–1000 labeled photos per class (genuine/fake).  
2. Fine-tune only the last layer for 5–10 epochs.  
3. Export to **ONNX** or **TFLite** for small size + speed.  
4. Replace `image_checks.py` with the classifier’s output.

### Voice (offline STT, Vosk small ~50MB)

1. Use `vosk-model-small-en-us-0.15` for on-device STT.  
2. Transcribe short claims and run the same keyword risk.  
3. Cache keywords per language/brand.

## Sample data

Look in `sample_data/images/real|fake` for 8 generated images, and `sample_data/transcripts` for two example transcripts.

## Notes

- This repo is a **PoC**—signals are simplistic but explainable and *very small*.  
- In production, add **QR/Excise stamp scan**, **OCR serial checks**, **logo template matching** (OpenCV), and **lighting normalization**.
