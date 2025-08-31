import os

# Dummy model path
VOSK_MODEL_PATH = os.path.join(os.path.dirname(__file__), "../models/vosk-tiny-dummy")

def record_and_transcribe(duration=5, samplerate=16000):
    # Instead of real Vosk STT, return a fixed transcript
    return "Bottle looks intact and authorized"

def analyze_transcript(transcript):
    t = transcript.lower()
    SUSPICIOUS = ["tamper", "crooked", "peeling", "fake", "counterfeit", "unreadable", "missing", "refill", "street"]
    sus_hits = any(k in t for k in SUSPICIOUS)
    verdict = "SUSPICIOUS" if sus_hits else "OK"
    return {"verdict": verdict, "transcript": transcript}
