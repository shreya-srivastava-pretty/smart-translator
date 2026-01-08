# ocr.py
import os
import shutil
import cv2
from PIL import Image, ImageEnhance
import pytesseract
import numpy as np


def _ensure_tesseract_available() -> None:
    """Ensure pytesseract knows where the tesseract binary is.

    Search order:
    1. Environment variable `TESSERACT_CMD`
    2. shutil.which('tesseract')
    3. Common Windows install locations

    Raises RuntimeError with actionable instructions if not found.
    """
    # If user specified explicit path via env var, prefer it
    env_path = os.environ.get('TESSERACT_CMD')
    if env_path and os.path.isfile(env_path):
        pytesseract.pytesseract.tesseract_cmd = env_path
        return

    # Try system PATH
    path = shutil.which('tesseract')
    if path:
        pytesseract.pytesseract.tesseract_cmd = path
        return

    # Common Windows installation paths
    common_paths = [
        r'C:\\Program Files\\Tesseract-OCR\\tesseract.exe',
        r'C:\\Program Files (x86)\\Tesseract-OCR\\tesseract.exe',
    ]
    for p in common_paths:
        if os.path.isfile(p):
            pytesseract.pytesseract.tesseract_cmd = p
            return

    raise RuntimeError(
        "Tesseract not found. Install Tesseract OCR and add it to your PATH, "
        "or set the TESSERACT_CMD environment variable to the tesseract executable path. "
        "On Windows, installer typically places it in 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'."
    )


def extract_text(image_path: str) -> str:
    """
    Extract text from an image using Tesseract OCR with preprocessing.
    
    Args:
        image_path (str): Path to the image file.
    
    Returns:
        str: Extracted text from the image.
    """
    # Ensure tesseract binary is available
    _ensure_tesseract_available()

    # Read image
    img = cv2.imread(image_path)
    if img is None:
        raise ValueError("Image not found or unable to read.")

    # Convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Denoise
    denoised = cv2.fastNlMeansDenoising(gray, h=10)

    # Sharpen
    kernel = np.array([[0, -1, 0],
                       [-1, 5, -1],
                       [0, -1, 0]])
    sharpened = cv2.filter2D(denoised, -1, kernel)

    # Adaptive threshold
    thresh = cv2.adaptiveThreshold(
        sharpened, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY, 31, 10
    )

    # Convert to PIL image
    pil_img = Image.fromarray(thresh)

    # Optional: Enhance contrast
    enhancer = ImageEnhance.Contrast(pil_img)
    pil_img = enhancer.enhance(2.0)

    # OCR using multiple PSM modes for best accuracy
    psm_modes = [3, 6, 11]  # Fully automatic, single block, sparse text
    extracted_text = ""
    for psm in psm_modes:
        config = f"--oem 3 --psm {psm}"
        text = pytesseract.image_to_string(pil_img, config=config).strip()
        if text:
            extracted_text = text
            break

    return extracted_text
