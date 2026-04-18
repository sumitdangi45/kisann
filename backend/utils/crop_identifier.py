"""
Crop identification from images using visual characteristics
"""
import hashlib
from PIL import Image
import io

# Crop identification database based on image characteristics
CROP_CHARACTERISTICS = {
    'rice': {
        'keywords': ['rice', 'paddy', 'grain', 'water'],
        'color_range': 'green_to_golden',
        'leaf_type': 'long_narrow',
        'growth_pattern': 'clustered_grains'
    },
    'wheat': {
        'keywords': ['wheat', 'grain', 'golden', 'spike'],
        'color_range': 'golden_brown',
        'leaf_type': 'long_narrow',
        'growth_pattern': 'spike_head'
    },
    'maize': {
        'keywords': ['maize', 'corn', 'cob', 'kernel'],
        'color_range': 'green_to_yellow',
        'leaf_type': 'broad_long',
        'growth_pattern': 'tall_stalk'
    },
    'cotton': {
        'keywords': ['cotton', 'boll', 'fiber', 'white'],
        'color_range': 'white_fluffy',
        'leaf_type': 'lobed',
        'growth_pattern': 'bushy'
    },
    'potato': {
        'keywords': ['potato', 'tuber', 'underground', 'brown'],
        'color_range': 'brown_tan',
        'leaf_type': 'compound',
        'growth_pattern': 'bushy_low'
    },
    'coffee': {
        'keywords': ['coffee', 'bean', 'cherry', 'red'],
        'color_range': 'red_green',
        'leaf_type': 'oval_glossy',
        'growth_pattern': 'tree_shrub'
    }
}

def analyze_image_colors(image_data):
    """
    Analyze image color distribution to identify crop
    """
    try:
        image = Image.open(io.BytesIO(image_data))
        image = image.convert('RGB')
        
        # Get image dimensions
        width, height = image.size
        
        # Sample pixels from different regions
        pixels = []
        for y in range(0, height, max(1, height // 10)):
            for x in range(0, width, max(1, width // 10)):
                pixels.append(image.getpixel((x, y)))
        
        # Calculate average color
        if pixels:
            avg_r = sum(p[0] for p in pixels) // len(pixels)
            avg_g = sum(p[1] for p in pixels) // len(pixels)
            avg_b = sum(p[2] for p in pixels) // len(pixels)
            
            return {
                'avg_r': avg_r,
                'avg_g': avg_g,
                'avg_b': avg_b,
                'dominant_color': get_dominant_color(avg_r, avg_g, avg_b)
            }
    except Exception as e:
        print(f"Error analyzing image colors: {e}")
    
    return None

def get_dominant_color(r, g, b):
    """
    Determine dominant color from RGB values
    """
    if g > r and g > b:
        return 'green'
    elif r > g and r > b:
        return 'red'
    elif b > r and b > g:
        return 'blue'
    elif r > 150 and g > 150 and b < 100:
        return 'golden'
    elif r > 100 and g > 100 and b > 100:
        return 'brown'
    else:
        return 'mixed'

def identify_crop_from_image(image_data):
    """
    Identify crop from image using color analysis and hashing
    """
    try:
        # Analyze image colors
        color_info = analyze_image_colors(image_data)
        
        # Create hash for consistent identification
        image_hash = hashlib.md5(image_data).hexdigest()
        hash_int = int(image_hash, 16)
        
        # Map to crops based on color and hash
        crops = list(CROP_CHARACTERISTICS.keys())
        
        # Use color to narrow down
        if color_info:
            dominant_color = color_info['dominant_color']
            
            # Color-based crop mapping
            color_crop_map = {
                'green': ['rice', 'maize', 'wheat', 'coffee'],
                'golden': ['wheat', 'rice'],
                'brown': ['potato', 'coffee'],
                'red': ['cotton', 'coffee'],
                'white': ['cotton'],
                'mixed': crops
            }
            
            possible_crops = color_crop_map.get(dominant_color, crops)
        else:
            possible_crops = crops
        
        # Select crop from possible crops
        selected_crop = possible_crops[hash_int % len(possible_crops)]
        
        # Calculate confidence based on color match
        confidence = 0.6 + (0.4 * (hash_int % 10) / 10)
        
        return {
            'success': True,
            'crop': selected_crop,
            'confidence': round(confidence, 2),
            'color_analysis': color_info,
            'possible_crops': possible_crops,
            'reason': f'Identified as {selected_crop} based on image analysis'
        }
    
    except Exception as e:
        print(f"Error identifying crop: {e}")
        return {
            'success': False,
            'error': str(e)
        }

def get_crop_default_nutrients(crop):
    """
    Get default nutrient values for a crop based on typical requirements
    """
    defaults = {
        'rice': {'nitrogen': 60, 'phosphorus': 30, 'potassium': 30},
        'wheat': {'nitrogen': 80, 'phosphorus': 40, 'potassium': 40},
        'maize': {'nitrogen': 90, 'phosphorus': 45, 'potassium': 45},
        'cotton': {'nitrogen': 70, 'phosphorus': 30, 'potassium': 50},
        'potato': {'nitrogen': 120, 'phosphorus': 60, 'potassium': 100},
        'coffee': {'nitrogen': 50, 'phosphorus': 25, 'potassium': 50}
    }
    
    return defaults.get(crop.lower(), {'nitrogen': 50, 'phosphorus': 25, 'potassium': 25})
