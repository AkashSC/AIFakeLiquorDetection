from PIL import Image
from io import BytesIO
import numpy as np

def analyze_image(image_file, logo_template_path):
    """
    image_file: Streamlit UploadedFile
    logo_template_path: path to template image
    """
    # Read uploaded image as PIL
    img = Image.open(BytesIO(image_file.read())).convert("RGB")
    
    # Read template image
    logo = Image.open(logo_template_path).convert("RGB")
    
    # Flatten images and compute histogram
    arr_img = np.array(img).ravel()
    arr_logo = np.array(logo).ravel()
    hist_img, _ = np.histogram(arr_img, bins=64, range=(0,255), density=True)
    hist_logo, _ = np.histogram(arr_logo, bins=64, range=(0,255), density=True)
    corr = np.corrcoef(hist_img, hist_logo)[0,1]
    
    match = corr > 0.7
    return {"match": match, "hist_corr": float(corr)}
