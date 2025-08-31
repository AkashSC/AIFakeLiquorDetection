def record_and_transcribe():
    """
    Dummy transcript. Replace with real STT if needed.
    """
    return "Bottle looks intact and authorized"

def analyze_transcript(transcript):
    t = transcript.lower()
    SUSPICIOUS = ["tamper", "crooked", "peeling", "fake", "counterfeit", "unreadable", "missing", "refill", "street"]
    sus_hits = any(k in t for k in SUSPICIOUS)
    verdict = "SUSPICIOUS" if sus_hits else "OK"
    return {"verdict": verdict, "transcript": transcript}
