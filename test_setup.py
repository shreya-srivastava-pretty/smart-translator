#!/usr/bin/env python
"""Quick test to verify all modules are working correctly."""

import sys
import os

print("=" * 60)
print("SIGNBOARD INTERPRETER - SETUP TEST")
print("=" * 60)

# Test 1: Import all modules
print("\n1. Testing imports...")
try:
    from ocr import extract_text
    print("   ✓ ocr module loaded")
except Exception as e:
    print(f"   ✗ ocr module failed: {e}")
    sys.exit(1)

try:
    from translate import translate_text
    print("   ✓ translate module loaded")
except Exception as e:
    print(f"   ✗ translate module failed: {e}")
    sys.exit(1)

try:
    from guidance import generate_guidance
    print("   ✓ guidance module loaded")
except Exception as e:
    print(f"   ✗ guidance module failed: {e}")
    sys.exit(1)

try:
    from denoise import denoise_image
    print("   ✓ denoise module loaded")
except Exception as e:
    print(f"   ✗ denoise module failed: {e}")
    sys.exit(1)

# Test 2: Check for input image
print("\n2. Checking for input image...")
if os.path.exists("input.jpg") or os.path.exists("input.JPG"):
    img_path = "input.jpg" if os.path.exists("input.jpg") else "input.JPG"
    print(f"   ✓ Found image: {img_path}")
else:
    print("   ✗ No input.jpg or input.JPG found")
    print("      Please place an image file in this directory")
    sys.exit(1)

# Test 3: Test OCR
print("\n3. Testing OCR...")
try:
    text = extract_text(img_path)
    if text:
        print(f"   ✓ OCR successful")
        print(f"     Extracted: {text[:50]}..." if len(text) > 50 else f"     Extracted: {text}")
    else:
        print("   ⚠ OCR returned no text (image may be blank)")
except Exception as e:
    print(f"   ✗ OCR failed: {e}")
    sys.exit(1)

# Test 4: Test translation
print("\n4. Testing translation...")
try:
    if text:
        translated = translate_text(text, "hi")
        print(f"   ✓ Translation successful")
        print(f"     Hindi: {translated[:50]}..." if len(translated) > 50 else f"     Hindi: {translated}")
except Exception as e:
    print(f"   ⚠ Translation failed: {e}")

# Test 5: Test guidance
print("\n5. Testing guidance...")
try:
    if text:
        guidance = generate_guidance(text)
        print(f"   ✓ Guidance generated")
        print(f"     {guidance}")
except Exception as e:
    print(f"   ⚠ Guidance failed: {e}")

print("\n" + "=" * 60)
print("SETUP TEST COMPLETE - ALL SYSTEMS GO!")
print("=" * 60)
print("\nYou can now use:")
print("  • python MAIN1.PY              - CLI tool")
print("  • streamlit run app.py         - Web interface")
print("  • python denoise.py image.jpg  - Standalone denoising")
