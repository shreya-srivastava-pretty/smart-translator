# Signboard Interpreter (Winter Hackathon)

Extract text from signboard images, translate to multiple languages, and get contextual guidance.

## Features

- **📸 OCR**: Extract text from images using Tesseract
- **🌐 Translation**: Translate to 12+ languages (Hindi, Bengali, Tamil, etc.)
- **💡 Guidance**: Get contextual advice based on signboard content
- **🖼️ Image Denoising**: Gaussian, NLMeans, and bilateral filtering methods
- **🎨 Advanced Preprocessing**: Threshold, sharpening, upscaling, contrast enhancement
- **🌐 Web UI**: Interactive Streamlit interface

## Quick Setup

1. **Activate virtualenv** (if not already active):
   ```powershell
   c:\Users\DELL\Desktop\c language\env\Scripts\Activate.ps1
   ```

2. **Install dependencies**:
   ```powershell
   pip install -r requirements.txt
   ```

3. **Install Tesseract OCR** (required):
   - Download from: https://github.com/tesseract-ocr/tesseract/releases
   - Install and add to PATH (or use default Windows install path)
   - Verify: `tesseract --version`

## Usage

### Option 1: Web Interface (Recommended)
```powershell
streamlit run app.py
```
Then open http://localhost:8501 in your browser.

### Option 2: Command Line

**Basic OCR**:
```powershell
python MAIN1.PY input.jpg
```

**With language translation**:
```powershell
python MAIN1.PY input.jpg -l en  # English
python MAIN1.PY input.jpg -l hi  # Hindi
```

**With denoising**:
```powershell
python MAIN1.PY input.jpg -d -m nlmeans  # nlmeans, gaussian, or bilateral
```

**Denoise only**:
```powershell
python denoise.py input.jpg -m nlmeans -o denoised.png
```

## Project Structure

- `MAIN1.PY` - Main CLI script with OCR, translation, and guidance
- `app.py` - Streamlit web interface (interactive)
- `ocr.py` - Tesseract OCR wrapper with error handling
- `translate.py` - Google Translate integration
- `guidance.py` - Contextual guidance generator
- `denoise.py` - Image denoising with multiple methods
- `requirements.txt` - Python dependencies

## Dependencies

- `pillow` - Image processing
- `pytesseract` - OCR engine wrapper
- `opencv-python` - Image denoising and preprocessing
- `googletrans==4.0.0-rc1` - Translation
- `streamlit` - Web UI framework
- **Tesseract OCR** (binary, not pip package) - OCR engine

## Troubleshooting

**"tesseract is not installed"**
- Install Tesseract: https://github.com/tesseract-ocr/tesseract/releases
- Verify installation: `tesseract --version`

**"No text detected"**
- Try enabling denoising: `python MAIN1.PY input.jpg -d`
- Use advanced preprocessing in the web UI
- Ensure image is clear and readable

**Translation fails**
- Check internet connection (uses Google Translate)
- Try again; Google Translate API can be rate-limited

## Examples

Extract text and translate to Hindi:
```powershell
python MAIN1.PY input.jpg -l hi
```

Denoise and extract:
```powershell
python MAIN1.PY input.jpg -d -m bilateral
```

Run web interface with all features:
```powershell
streamlit run app.py
```
