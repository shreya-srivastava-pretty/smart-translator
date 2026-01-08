import cv2
import os
import argparse


def denoise_image(input_path: str, output_path: str = None, method: str = "gaussian") -> str:
    """Denoise an image using OpenCV.
    
    Methods:
        gaussian: Convert to grayscale and apply Gaussian blur (simple, fast)
        nlmeans: Non-local means denoising (preserves color, slower, better quality)
        bilateral: Bilateral filter (preserves edges, medium speed)
    
    Args:
        input_path: Path to input image
        output_path: Path to save denoised image (default: next to input with .denoised suffix)
        method: Denoising method ('gaussian', 'nlmeans', 'bilateral')
    
    Returns:
        Path to saved denoised image
    
    Raises:
        FileNotFoundError: If input image does not exist
        RuntimeError: If image cannot be read or written
    """
    if not os.path.exists(input_path):
        raise FileNotFoundError(f"Input image not found: {input_path}")
    
    # Read the original image
    img = cv2.imread(input_path)
    if img is None:
        raise RuntimeError(f"Failed to read image: {input_path}")
    
    # Default output path: add .denoised before extension
    if output_path is None:
        base, ext = os.path.splitext(input_path)
        output_path = f"{base}.denoised{ext}"
    
    # Apply selected denoising method
    method = method.lower()
    if method == "gaussian":
        # Convert to grayscale and apply Gaussian blur
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        denoised = cv2.GaussianBlur(gray, (5, 5), 0)
    elif method == "nlmeans":
        # Non-local means denoising (color)
        denoised = cv2.fastNlMeansDenoisingColored(img, None, h=10, templateWindowSize=7, searchWindowSize=21)
    elif method == "bilateral":
        # Bilateral filter (preserves edges)
        denoised = cv2.bilateralFilter(img, d=9, sigmaColor=75, sigmaSpace=75)
    else:
        raise ValueError(f"Unknown denoising method: {method}. Use 'gaussian', 'nlmeans', or 'bilateral'.")
    
    # Ensure output directory exists
    outdir = os.path.dirname(output_path) or "."
    os.makedirs(outdir, exist_ok=True)
    
    # Save the denoised image
    success = cv2.imwrite(output_path, denoised)
    if not success:
        raise RuntimeError(f"Failed to write denoised image: {output_path}")
    
    return output_path


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Denoise an image using OpenCV")
    parser.add_argument("input", help="Input image path")
    parser.add_argument("-o", "--output", help="Output image path (default: input.denoised.ext)")
    parser.add_argument("-m", "--method", choices=["gaussian", "nlmeans", "bilateral"], 
                        default="gaussian", help="Denoising method (default: gaussian)")
    args = parser.parse_args()
    
    try:
        output = denoise_image(args.input, args.output, args.method)
        print(f"Denoised image saved: {output}")
    except Exception as e:
        print(f"Error: {e}")
        exit(1)