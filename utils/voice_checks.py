
import json, re
from pathlib import Path
from typing import Dict, Any

def analyze_transcript(transcript: str, model_cfg_path: str) -> Dict[str, Any]:
    cfg = json.loads(Path(model_cfg_path).read_text())
    t = transcript.lower()

    sus = cfg["voice"]["keywords_suspicious"]
    ok = cfg["voice"]["keywords_ok"]

    sus_hits = sum(1 for k in sus if k in t)
    ok_hits = sum(1 for k in ok if k in t)

    # Risk: suspicious words push up, ok words pull down
    raw = sus_hits - 0.5 * ok_hits
    # Map raw to 0..1 with a simple squashing
    risk = 1.0 - (1.0 / (1.0 + 0.8*max(0, raw)))
    risk = max(0.0, min(1.0, risk))

    return {
        "sus_hits": sus_hits,
        "ok_hits": ok_hits,
        "voice_risk": risk
    }
