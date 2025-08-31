
import json, math
from pathlib import Path
from typing import Dict, Any
import numpy as np
from PIL import Image, ImageFilter, ImageStat

def _to_array(img):
    if not isinstance(img, Image.Image):
        img = Image.open(img).convert("RGB")
    else:
        img = img.convert("RGB")
    return np.array(img)

def _histogram_corr(a: np.ndarray, b: np.ndarray) -> float:
    # Simple RGB histogram correlation (normalized)
    ha, _ = np.histogram(a.ravel(), bins=64, range=(0,255), density=True)
    hb, _ = np.histogram(b.ravel(), bins=64, range=(0,255), density=True)
    num = np.sum((ha - ha.mean())*(hb - hb.mean()))
    den = math.sqrt(np.sum((ha - ha.mean())**2) * np.sum((hb - hb.mean())**2)) + 1e-8
    return float(max(0.0, min(1.0, num/den)))

def _edge_density(img_arr: np.ndarray) -> float:
    img = Image.fromarray(img_arr).filter(ImageFilter.FIND_EDGES)
    arr = np.array(img).astype(np.float32)
    mag = np.linalg.norm(arr, axis=2)
    return float((mag > 30).mean())  # fraction of "edge" pixels

def _blur_score(img_arr: np.ndarray) -> float:
    # Cheap blur score: edge magnitude variance
    img = Image.fromarray(img_arr).filter(ImageFilter.FIND_EDGES)
    arr = np.array(img).astype(np.float32)
    mag = np.linalg.norm(arr, axis=2)
    return float(np.var(mag))

def analyze_image(
    image_path: str,
    model_cfg_path: str,
    logo_template_path: str
) -> Dict[str, Any]:
    cfg = json.loads(Path(model_cfg_path).read_text())
    img = Image.open(image_path).convert("RGB")
    arr = _to_array(img)
    logo = Image.open(logo_template_path).convert("RGB")
    logo_arr = _to_array(logo)

    hist_corr = _histogram_corr(arr, logo_arr)
    edge_density_img = _edge_density(arr)
    edge_density_logo = _edge_density(logo_arr)
    edge_density_diff = abs(edge_density_img - edge_density_logo)
    blur = _blur_score(arr)

    # normalize blur to 0..1 via heuristic (0..50 -> 0..1)
    blur_norm = max(0.0, min(1.0, (blur / 50.0)))

    # Risk from features (lower hist corr -> higher risk, etc.)
    hist_risk = 1.0 - hist_corr
    edge_risk = min(1.0, edge_density_diff / cfg["image"]["edge_density_max_diff"]) if cfg["image"]["edge_density_max_diff"]>0 else 0.0
    blur_risk = 1.0 - min(1.0, blur_norm)  # blur too low -> higher risk

    weights = cfg["image"]["weights"]
    image_risk = (
        weights["hist"] * hist_risk +
        weights["edge"] * edge_risk +
        weights["blur"] * blur_risk
    )
    image_risk = max(0.0, min(1.0, image_risk))

    details = {
        "hist_corr": hist_corr,
        "edge_density_diff": edge_density_diff,
        "blur_score": blur,
        "hist_risk": hist_risk,
        "edge_risk": edge_risk,
        "blur_risk": blur_risk,
        "image_risk": image_risk
    }
    return details
