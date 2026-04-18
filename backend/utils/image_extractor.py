import pytesseract
from PIL import Image
import re
from typing import Dict, Optional
import io

def extract_text_from_image(image_data) -> str:
    """
    Extract text from image using OCR (Tesseract)
    """
    try:
        # Convert bytes to PIL Image
        if isinstance(image_data, bytes):
            image = Image.open(io.BytesIO(image_data))
        else:
            image = image_data
        
        # Extract text using Tesseract
        text = pytesseract.image_to_string(image)
        return text
    except Exception as e:
        print(f"Error extracting text from image: {e}")
        return ""


def extract_soil_parameters_from_image(image_data) -> Dict[str, Optional[float]]:
    """
    Extract soil parameters from image
    """
    text = extract_text_from_image(image_data)
    if not text:
        return {}
    
    # Use the same extraction logic as PDF
    from utils.pdf_extractor import extract_soil_parameters
    return extract_soil_parameters(text)
