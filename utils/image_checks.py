import numpy as np
from PIL import Image

def analyze_image(image_path, logo_template_path):
    img = Image.open(image_path).convert("RGB")
    logo = Image.open(logo_template_path).convert("RGB")
    
    arr_img = np.array(img).ravel()
    arr_logo = np.array(logo).ravel()
    hist_img, _ = np.histogram(arr_img, bins=64, range=(0,255), density=True)
    hist_logo, _ = np.histogram(arr_logo, bins=64, range=(0,255), density=True)
    corr = np.corrcoef(hist_img, hist_logo)[0,1]
    
    match = corr > 0.7
    return {"match": match, "hist_corr": float(corr)}
