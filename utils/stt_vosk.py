import os
from vosk import Model, KaldiRecognizer
import sounddevice as sd
import queue
import json
import sys

# Path to the bundled Vosk model
VOSK_MODEL_PATH = os.path.join(os.path.dirname(__file__), "../models/vosk-model-small-en-us-0.15")

q = queue.Queue()
model = Model(VOSK_MODEL_PATH)

def record_and_transcribe(duration=5, samplerate=16000):
    rec = KaldiRecognizer(model, samplerate)
    
    def callback(indata, frames, time, status):
        if status:
            print(status, file=sys.stderr)
        q.put(bytes(indata))
    
    with sd.RawInputStream(samplerate=samplerate, blocksize = 8000, dtype='int16',
                           channels=1, callback=callback):
        print("Recording...")
        rec_text = ""
        for _ in range(int(duration*samplerate/8000)):
            data = q.get()
            if rec.AcceptWaveform(data):
                res = json.loads(rec.Result())
                rec_text += " " + res.get("text","")
        # final
        res = json.loads(rec.FinalResult())
        rec_text += " " + res.get("text","")
    return rec_text.strip()

# Simple keyword check
SUSPICIOUS = ["tamper", "crooked", "peeling", "fake", "counterfeit", "unreadable", "missing", "refill", "street"]
OK = ["intact", "clear", "authorized", "present", "scans"]

def analyze_transcript(transcript):
    t = transcript.lower()
    sus_hits = any(k in t for k in SUSPICIOUS)
    ok_hits = any(k in t for k in OK)
    verdict = "SUSPICIOUS" if sus_hits else "OK"
    return {"verdict": verdict, "transcript": transcript}
  
