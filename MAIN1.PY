from ocr import extract_text
from translate import translate_text
from guidance import generate_guidance
from denoise import denoise_image
import os
import glob
import argparse

IMAGE_PATH = "input.jpg"  # default image to process
TARGET_LANG = "hi"        # hi = Hindi, en = English


def find_image(path: str) -> str:
    """Find an image file, trying common extensions and case variations."""
    if os.path.exists(path):
        return path
    
    base, _ = os.path.splitext(path)
    # Try common image extensions
    for ext in [".jpg", ".jpeg", ".png", ".bmp", ".JPG", ".JPEG", ".PNG", ".BMP"]:
        candidate = base + ext
        if os.path.exists(candidate):
            return candidate
    
    # Fallback: any file matching base*
    matches = glob.glob(base + "*")
    if matches:
        return matches[0]
    
    return path  # Return original if nothing found


def start(image_path=IMAGE_PATH, target_lang=TARGET_LANG, enable_denoise=False, denoise_method="gaussian"):
    """Process a signboard image through OCR, translation, and guidance.
    
    Args:
        image_path: Path to input image
        target_lang: Target language for translation (e.g., 'en', 'hi')
        enable_denoise: If True, denoise image before OCR
        denoise_method: Denoising method ('gaussian', 'nlmeans', 'bilateral')
    """
    print("\n===== SIGNBOARD INTERPRETER =====")
    
    # Find the image file
    image = find_image(image_path)
    if image != image_path:
        print(f"Using image: {image}")
    
    # Optional: Denoise image before OCR
    if enable_denoise:
        try:
            print(f"Denoising image ({denoise_method} method)...")
            denoised_path = denoise_image(image, method=denoise_method)
            image = denoised_path
            print(f"Using denoised image: {denoised_path}")
        except Exception as e:
            print(f"Warning: Denoising failed ({e}), proceeding with original image.")
    
    # 1. OCR
    extracted = None
    try:
        extracted = extract_text(image)
        print("\nExtracted Text:")
        print(extracted if extracted else "[no text found]")
    except FileNotFoundError as e:
        print(f"\nExtracted Text:")
        print(f"[ERROR] {e}")
        print("\nTranslated Text:")
        print("[SKIPPED] Image file not found.")
        print("\nGuidance:")
        print("[SKIPPED] Cannot process missing image.")
        print("\n=================================\n")
        return
    except RuntimeError as e:
        print(f"\nExtracted Text:")
        print(f"[ERROR] {e}")
        print("\nTranslated Text:")
        print("[SKIPPED] OCR failed. Ensure Tesseract is installed.")
        print("\nGuidance:")
        print("[SKIPPED] Cannot generate guidance without extracted text.")
        print("\n=================================\n")
        return
    
    # 2. Translation (skip if no text extracted)
    if not extracted or not extracted.strip():
        print("\nTranslated Text:")
        print("[SKIPPED] No text to translate.")
        print("\nGuidance:")
        print("[SKIPPED] No text to analyze.")
    else:
        try:
            translated = translate_text(extracted, target_lang)
            print("\nTranslated Text:")
            print(translated)
        except Exception as e:
            print(f"\nTranslated Text:")
            print(f"[ERROR] Translation failed: {e}")
            translated = None
        
        # 3. Guidance
        try:
            guide = generate_guidance(extracted)
            print("\nGuidance:")
            print(guide)
        except Exception as e:
            print(f"\nGuidance:")
            print(f"[ERROR] {e}")
    
    print("\n=================================\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Signboard Interpreter: OCR, translate, and provide guidance")
    parser.add_argument("image", nargs="?", default=IMAGE_PATH, help=f"Image path (default: {IMAGE_PATH})")
    parser.add_argument("-l", "--lang", default=TARGET_LANG, help=f"Target language code (default: {TARGET_LANG})")
    parser.add_argument("-d", "--denoise", action="store_true", help="Denoise image before OCR")
    parser.add_argument("-m", "--denoise-method", choices=["gaussian", "nlmeans", "bilateral"], 
                        default="gaussian", help="Denoising method (default: gaussian)")
    args = parser.parse_args()
    
    start(image_path=args.image, target_lang=args.lang, 
          enable_denoise=args.denoise, denoise_method=args.denoise_method)
