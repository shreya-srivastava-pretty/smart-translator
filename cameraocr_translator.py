# camera_translate.py
import cv2
import pytesseract
import shutil
import os
from googletrans import Translator

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

# ====== Initialize Translator ======
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

# ====== Open Webcam ======
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    raise Exception("Cannot open camera")

print("Press 's' to capture image and run OCR + Translate, 'q' to quit.")

while True:
    ret, frame = cap.read()
    if not ret:
        print("Failed to grab frame")
        break

    cv2.imshow("Camera", frame)
    key = cv2.waitKey(1) & 0xFF

    if key == ord('s'):  # Press 's' to capture
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.medianBlur(gray, 3)  # Optional denoise

        # OCR
        detected_text = pytesseract.image_to_string(gray)
        print("\nDetected Text:")
        print(detected_text)

        # Ask user for target language
        target_lang = input("Enter target language code (e.g., 'en', 'hi', 'fr'): ").strip()

        # Translate
        translated_text = translate_text(detected_text, target_lang)
        print("\nTranslated Text:")
        print(translated_text)

        cv2.imshow("Captured Image", gray)

    elif key == ord('q'):  # Press 'q' to quit
        break

cap.release()
cv2.destroyAllWindows()
