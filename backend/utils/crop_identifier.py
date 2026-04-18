"""
Crop identification from images using Gemini Vision API
"""
import base64
import io
import os
import google.generativeai as genai
from PIL import Image
from dotenv import load_dotenv

load_dotenv()

_raw_key = os.getenv('GEMINI_API_KEY', '')
GEMINI_API_KEY = _raw_key if _raw_key and _raw_key != 'your_gemini_api_key_here' else None
SUPPORTED_CROPS = ['rice', 'wheat', 'maize', 'cotton', 'potato', 'coffee']

_vision_model = None

def _get_vision_model():
    global _vision_model
    if _vision_model is None and GEMINI_API_KEY:
        genai.configure(api_key=GEMINI_API_KEY)
        _vision_model = genai.GenerativeModel('gemini-1.5-flash')
    return _vision_model


def identify_crop_from_image(image_data):
    """
    Identify crop from image using Gemini Vision API.
    Falls back to color-based heuristic if API is unavailable.
    """
    model = _get_vision_model()

    if model:
        try:
            image = Image.open(io.BytesIO(image_data))
            prompt = (
                f"Look at this image and identify which crop plant is shown. "
                f"Choose ONLY from this list: {', '.join(SUPPORTED_CROPS)}. "
                f"Reply in this exact JSON format (no markdown, no extra text):\n"
                f'{{ "crop": "<crop_name>", "confidence": <0.0-1.0>, "reason": "<one sentence why>" }}'
            )
            response = model.generate_content([prompt, image])
            text = response.text.strip()
            # Strip markdown code fences if present
            if text.startswith("```"):
                text = text.split("```")[1]
                if text.startswith("json"):
                    text = text[4:]
            import json
            parsed = json.loads(text.strip())
            crop = parsed.get('crop', '').lower().strip()
            if crop not in SUPPORTED_CROPS:
                crop = SUPPORTED_CROPS[0]
            return {
                'success': True,
                'crop': crop,
                'confidence': float(parsed.get('confidence', 0.85)),
                'reason': parsed.get('reason', f'Identified as {crop} by Gemini Vision'),
                'method': 'gemini_vision'
            }
        except Exception as e:
            print(f"Gemini Vision error: {e}")
            # Fall through to heuristic

    # Heuristic fallback using color analysis
    return _heuristic_identify(image_data)


def _heuristic_identify(image_data):
    """Simple color-based heuristic fallback."""
    try:
        image = Image.open(io.BytesIO(image_data)).convert('RGB')
        w, h = image.size
        pixels = [image.getpixel((x, y))
                  for y in range(0, h, max(1, h // 10))
                  for x in range(0, w, max(1, w // 10))]
        avg_r = sum(p[0] for p in pixels) // len(pixels)
        avg_g = sum(p[1] for p in pixels) // len(pixels)
        avg_b = sum(p[2] for p in pixels) // len(pixels)

        if avg_g > avg_r and avg_g > avg_b:
            if avg_g > 120:
                crop = 'rice'
            else:
                crop = 'maize'
        elif avg_r > 150 and avg_g > 130 and avg_b < 80:
            crop = 'wheat'
        elif avg_r > avg_g and avg_r > avg_b:
            crop = 'cotton'
        else:
            crop = 'potato'

        return {
            'success': True,
            'crop': crop,
            'confidence': 0.45,
            'reason': f'Identified as {crop} based on color analysis (Gemini API key not configured)',
            'method': 'color_heuristic'
        }
    except Exception as e:
        return {'success': False, 'error': str(e)}

def get_crop_default_nutrients(crop):
    """
    Get typical soil nutrient values for a crop (used when no soil test is available).
    """
    defaults = {
        'rice':   {'nitrogen': 60,  'phosphorus': 30, 'potassium': 30},
        'wheat':  {'nitrogen': 80,  'phosphorus': 40, 'potassium': 40},
        'maize':  {'nitrogen': 90,  'phosphorus': 45, 'potassium': 45},
        'cotton': {'nitrogen': 70,  'phosphorus': 30, 'potassium': 50},
        'potato': {'nitrogen': 120, 'phosphorus': 60, 'potassium': 100},
        'coffee': {'nitrogen': 50,  'phosphorus': 25, 'potassium': 50},
    }
    return defaults.get(crop.lower(), {'nitrogen': 50, 'phosphorus': 25, 'potassium': 25})
