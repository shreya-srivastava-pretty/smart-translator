# streamlit_app.py
import streamlit as st
import cv2
from PIL import Image
import pytesseract
from googletrans import Translator
import numpy as np

translator = Translator()

st.set_page_config(page_title="OCR + Translator", layout="wide")
st.title("📄 OCR + Multi-language Translator")

# ---------------------------
# 1. Upload Image
# ---------------------------
uploaded_file = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])
if uploaded_file:
    img = Image.open(uploaded_file).convert("RGB")
    img_np = np.array(img)
    st.subheader("Original Image")
    st.image(img_np, use_column_width=True)

    # ---------------------------
    # 2. Preprocess Image
    # ---------------------------
    gray = cv2.cvtColor(img_np, cv2.COLOR_RGB2GRAY)
    denoised = cv2.fastNlMeansDenoising(gray, h=10)
    thresh = cv2.adaptiveThreshold(
        denoised, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY, 31, 10
    )
    pil_img = Image.fromarray(thresh)
    pil_img = pil_img.resize((pil_img.width*2, pil_img.height*2), Image.LANCZOS)

    st.subheader("Processed Image for OCR")
    st.image(np.array(pil_img), use_column_width=True)

    # ---------------------------
    # 3. OCR
    # ---------------------------
    custom_configs = [r'--oem 3 --psm 3', r'--oem 3 --psm 6', r'--oem 3 --psm 11']
    extracted_text = ""
    for config in custom_configs:
        text = pytesseract.image_to_string(pil_img, config=config).strip()
        if text:
            extracted_text = text
            break

    st.subheader("Extracted Text")
    st.text(extracted_text if extracted_text else "No text detected")

    # ---------------------------
    # 4. Translation
    # ---------------------------
    if extracted_text:
        languages = {
            "Hindi": "hi",
            "Bengali": "bn",
            "Tamil": "ta",
            "Telugu": "te",
            "Marathi": "mr",
            "English": "en",
            "Gujarati": "gu",
            "Kannada": "kn"
        }

        st.subheader("Select languages to translate")
        selected_langs = st.multiselect(
            "Pick languages",
            options=list(languages.keys()),
            default=["Hindi"]
        )

        if selected_langs:
            st.subheader("Translations")
            for idx, lang_name in enumerate(selected_langs):
                lang_code = languages[lang_name]
                try:
                    translated = translator.translate(extracted_text, dest=lang_code)
                    text = translated.text
                    if any(word in text.lower() for word in ["danger", "stop", "warning"]):
                        text = "⚠️ " + text
                    st.markdown(f"**{lang_name} ({lang_code}):** {text}")
                except Exception as e:
                    st.markdown(f"**{lang_name} ({lang_code}):** Translation Error - {e}")
