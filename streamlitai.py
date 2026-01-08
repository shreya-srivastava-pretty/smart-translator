# ...existing code...
"""
Streamlit app for Signboard Interpreter: OCR, denoise, translate, and provide guidance.
Run with: streamlit run app.py
"""

import streamlit as st
import cv2
import numpy as np
from PIL import Image, ImageEnhance
import os
import tempfile
from ocr import extract_text
from translate import translate_text
from guidance import generate_guidance
from denoise import denoise_image

# Page configuration
st.set_page_config(
    page_title="Signboard Interpreter",
    page_icon="📋",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("📋 Signboard Interpreter")
st.markdown("Extract text from signboards, translate, and get guidance using OCR and AI")

# Sidebar configuration
with st.sidebar:
    st.header("⚙ Settings")
    
    target_language = st.selectbox(
        "Target Language for Translation",
        options=[
            ("English", "en"),
            ("Hindi", "hi"),
            ("Bengali", "bn"),
            ("Tamil", "ta"),
            ("Telugu", "te"),
            ("Marathi", "mr"),
            ("Gujarati", "gu"),
            ("Kannada", "kn"),
            ("Spanish", "es"),
            ("French", "fr"),
            ("German", "de"),
            ("Chinese", "zh-cn"),
        ],
        format_func=lambda x: x[0],
    )
    target_lang_code = target_language[1]
    
    st.markdown("---")
    enable_denoise = st.checkbox("Denoise image before OCR", value=False)
    
    if enable_denoise:
        denoise_method = st.radio(
            "Denoising Method",
            options=["gaussian", "nlmeans", "bilateral"],
            horizontal=True,
        )
    else:
        denoise_method = "gaussian"
    
    st.markdown("---")
    enable_preprocessing = st.checkbox("Advanced preprocessing for OCR", value=False)
    
    if enable_preprocessing:
        st.write("Advanced options:")
        upscale = st.slider("Upscale factor", 1, 4, 2)
        contrast = st.slider("Contrast enhancement", 0.5, 3.0, 1.0)
    else:
        upscale = 1
        contrast = 1.0


# Main content
col1, col2 = st.columns(2)

with col1:
    st.subheader("📸 Upload Image")
    uploaded_file = st.file_uploader(
        "Choose an image file (JPG, PNG, etc.)",
        type=["jpg", "jpeg", "png", "bmp", "tiff"]
    )

if uploaded_file is not None:
    # Save uploaded file to temporary location
    with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(uploaded_file.name)[1]) as tmp:
        tmp.write(uploaded_file.getbuffer())
        img_path = tmp.name
    
    try:
        # Read original image
        original_img = cv2.imread(img_path)
        if original_img is None:
            st.error("Failed to read image file")
        else:
            original_rgb = cv2.cvtColor(original_img, cv2.COLOR_BGR2RGB)
            
            # Process image
            processing_image = original_img.copy()
            
            # Step 1: Denoise if enabled
            if enable_denoise:
                with st.spinner(f"Denoising image ({denoise_method} method)..."):
                    try:
                        denoised_path = denoise_image(img_path, method=denoise_method)
                        processing_image = cv2.imread(denoised_path)
                        st.success(f"✓ Denoised using {denoise_method} method")
                    except Exception as e:
                        st.warning(f"Denoising failed: {e}. Proceeding with original image.")
            
            # Step 2: Preprocess for OCR if advanced mode enabled
            if enable_preprocessing:
                gray = cv2.cvtColor(processing_image, cv2.COLOR_BGR2GRAY)
                
                # Denoise if not already done
                if not enable_denoise:
                    denoised = cv2.fastNlMeansDenoising(gray, h=10)
                else:
                    denoised = gray
                
                # Sharpening kernel
                kernel = np.array([[0, -1, 0],
                                   [-1, 5, -1],
                                   [0, -1, 0]])
                sharpened = cv2.filter2D(denoised, -1, kernel)
                
                # Adaptive threshold
                thresh = cv2.adaptiveThreshold(
                    sharpened, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                    cv2.THRESH_BINARY, 31, 10
                )
                
                # Convert to PIL and enhance
                pil_img = Image.fromarray(thresh)
                
                # Upscale
                if upscale > 1:
                    pil_img = pil_img.resize(
                        (pil_img.width * upscale, pil_img.height * upscale),
                        Image.LANCZOS
                    )
                
                # Contrast enhancement
                if contrast != 1.0:
                    enhancer = ImageEnhance.Contrast(pil_img)
                    pil_img = enhancer.enhance(contrast)
                
                # Save processed image temporarily for OCR
                proc_tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".processed.png")
                proc_tmp.close()
                processed_path = proc_tmp.name
                pil_img.save(processed_path)
                ocr_input_path = processed_path
            else:
                ocr_input_path = img_path
            
            # Display original image
            with col1:
                st.markdown("### Original Image")
                st.image(original_rgb, use_column_width=True)
            
            # Display processed image if preprocessing enabled
            if enable_preprocessing:
                with col2:
                    st.markdown("### Processed Image for OCR")
                    processed_rgb = cv2.cvtColor(cv2.imread(ocr_input_path), cv2.COLOR_BGR2RGB)
                    st.image(processed_rgb, use_column_width=True)
            
            # Step 3: OCR
            st.markdown("---")
            with st.spinner("Extracting text using OCR..."):
                try:
                    extracted_text = extract_text(ocr_input_path)
                    st.success("✓ OCR completed")
                except Exception as e:
                    st.error(f"❌ OCR failed: {e}")
                    extracted_text = None
            
            if extracted_text:
                # Display extracted text
                st.subheader("📝 Extracted Text")
                st.text_area("Detected text:", value=extracted_text, height=100, disabled=True)
                
                # Step 4: Translate
                st.markdown("---")
                with st.spinner(f"Translating to {target_language[0]}..."):
                    try:
                        translated_text = translate_text(extracted_text, target_lang_code)
                        st.success("✓ Translation completed")
                    except Exception as e:
                        st.warning(f"Translation failed: {e}")
                        translated_text = extracted_text
                
                # Display translated text
                st.subheader(f"🌐 Translated Text ({target_language[0]})")
                st.text_area("Translated text:", value=translated_text, height=100, disabled=True)
                
                # Step 5: Guidance
                st.markdown("---")
                with st.spinner("Generating guidance..."):
                    try:
                        guidance = generate_guidance(extracted_text)
                        st.success("✓ Guidance generated")
                    except Exception as e:
                        st.warning(f"Guidance generation failed: {e}")
                        guidance = "Unable to generate guidance"
                
                # Display guidance
                st.subheader("💡 Guidance")
                st.info(guidance)
                
                # Download options
                st.markdown("---")
                st.subheader("📥 Download Results")
                
                # Create results text file
                results = f"""SIGNBOARD INTERPRETATION RESULTS
=================================

EXTRACTED TEXT:
{extracted_text}

TRANSLATED TEXT ({target_language[0]}):
{translated_text}

GUIDANCE:
{guidance}
"""
                st.download_button(
                    label="Download Results (TXT)",
                    data=results,
                    file_name="signboard_results.txt",
                    mime="text/plain"
                )
            else:
                st.warning("⚠ No text was detected in the image. Try:")
                st.markdown("""
                - Uploading a clearer/higher resolution image
                - Enabling advanced preprocessing
                - Enabling denoising
                - Ensuring the text in the image is clear and readable
                """)
        
        # Clean up temporary files
        try:
            # remove uploaded temp
            try:
                os.remove(img_path)
            except:
                pass

            # remove processed image if created
            if enable_preprocessing and 'processed_path' in locals():
                try:
                    os.remove(processed_path)
                except:
                    pass

            # remove denoised image if denoise_image returned a temp path
            if enable_denoise and 'denoised_path' in locals():
                try:
                    os.remove(denoised_path)
                except:
                    pass
        except:
            pass
    
    except Exception as e:
        st.error(f"Error processing image: {e}")
else:
    st.info("👆 Upload an image to get started")
    
    # Show example features
    st.markdown("---")
    st.subheader("Features")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("### 📸 OCR")
        st.write("Extract text from images using Tesseract")
    with col2:
        st.markdown("### 🌐 Translation")
        st.write("Translate to 12+ languages")
    with col3:
        st.markdown("### 💡 Guidance")
        st.write("Get contextual guidance based on signboard content")
# ...existing code...