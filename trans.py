import cv2
import pytesseract
import shutil
from googletrans import Translator
import os
import numpy as np

# ====== Set Tesseract path (Windows) ======
tesseract_path = shutil.which('tesseract')
if tesseract_path:
    pytesseract.pytesseract.tesseract_cmd = tesseract_path
else:
    common_path = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
    if os.path.exists(common_path):
        pytesseract.pytesseract.tesseract_cmd = common_path
    else:
        raise Exception("Tesseract not found. Install it from https://github.com/tesseract-ocr/tesseract")

# ====== Initialize Translator =====
translator = Translator()

def translate_text(text: str, target_lang: str = "en") -> str:
    """Translate text into the selected language."""
    if not text.strip():
        return "No text to translate"
    try:
        translated = translator.translate(text, dest=target_lang)
        return translated.text
    except Exception as e:
        return f"Translation Error: {e}"

def preprocess_for_ocr(frame):
    """Preprocess the frame for better OCR accuracy"""
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.medianBlur(gray, 3)

    # Optional sharpening
    kernel = np.array([[0, -1, 0],
                       [-1, 5, -1],
                       [0, -1, 0]])
    gray = cv2.filter2D(gray, -1, kernel)

    # Adaptive thresholding
    gray = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                 cv2.THRESH_BINARY, 31, 10)
    return gray

# ====== Open Webcam ======
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    raise Exception("Cannot open camera")

# Ask user for target language
target_lang = input("Enter target language code (e.g., 'hi' for Hindi, 'fr' for French): ")

print("Press 's' to capture image, OCR + translate. Press 'q' to quit.")

while True:
    ret, frame = cap.read()
    if not ret:
        print("Failed to grab frame")
        break

    cv2.imshow("Camera", frame)
    key = cv2.waitKey(1) & 0xFF

    if key == ord('s'):  # Press 's' to capture
        processed = preprocess_for_ocr(frame)
        cv2.imshow("Captured Image", processed)

        # OCR using multiple PSM modes for better accuracy
        extracted_text = ""
        for psm in [6, 3, 11]:
            config = f"--oem 3 --psm {psm}"
            text = pytesseract.image_to_string(processed, config=config).strip()
            if text:
                extracted_text = text
                break

        print("\n===== DETECTED TEXT =====")
        print(extracted_text if extracted_text else "[No text detected]")

        # Translate
        translated_text = translate_text(extracted_text, target_lang)
        print(f"\n===== TRANSLATED TEXT ({target_lang}) =====")
        print(translated_text)

        print("\nPress any key on the captured image window to continue...")
        cv2.waitKey(0)
        cv2.destroyWindow("Captured Image")

    elif key == ord('q'):  # Press 'q' to quit
        break

cap.release()
cv2.destroyAllWindows()
