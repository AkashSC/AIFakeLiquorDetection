import numpy as np
from PIL import Image, ImageFilter

def analyze_image(image_path, logo_template_path):
    # Open images
    img = Image.open(image_path).convert("RGB")
    logo = Image.open(logo_template_path).convert("RGB")
    
    # Histogram correlation
    arr_img = np.array(img).ravel()
    arr_logo = np.array(logo).ravel()
    hist_img, _ = np.histogram(arr_img, bins=64, range=(0,255), density=True)
    hist_logo, _ = np.histogram(arr_logo, bins=64, range=(0,255), density=True)
    corr = np.corrcoef(hist_img, hist_logo)[0,1]
    
    # Threshold for matching
    match = corr > 0.7  # tweak if needed
    return {"match": match, "hist_corr": float(corr)}
