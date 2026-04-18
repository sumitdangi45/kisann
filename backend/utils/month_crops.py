"""
Month-based crop recommendations for India
Based on agricultural seasons and climate patterns
"""

MONTH_CROPS = {
    'January': {
        'season': 'Winter',
        'crops': ['wheat', 'chickpea', 'lentil', 'mustard', 'barley', 'peas'],
        'description': 'Winter crops - ideal for cool weather'
    },
    'February': {
        'season': 'Winter',
        'crops': ['wheat', 'chickpea', 'lentil', 'mustard', 'barley', 'peas'],
        'description': 'Winter crops - ideal for cool weather'
    },
    'March': {
        'season': 'Spring',
        'crops': ['wheat', 'chickpea', 'lentil', 'mustard', 'barley', 'peas', 'potato'],
        'description': 'Spring crops - transition season'
    },
    'April': {
        'season': 'Summer',
        'crops': ['maize', 'cotton', 'groundnut', 'sugarcane', 'watermelon', 'muskmelon'],
        'description': 'Summer crops - heat tolerant varieties'
    },
    'May': {
        'season': 'Summer',
        'crops': ['maize', 'cotton', 'groundnut', 'sugarcane', 'watermelon', 'muskmelon', 'rice'],
        'description': 'Summer crops - pre-monsoon planting'
    },
    'June': {
        'season': 'Monsoon',
        'crops': ['rice', 'maize', 'cotton', 'sugarcane', 'groundnut', 'soybean', 'pigeonpeas'],
        'description': 'Monsoon crops - high rainfall varieties'
    },
    'July': {
        'season': 'Monsoon',
        'crops': ['rice', 'maize', 'cotton', 'sugarcane', 'groundnut', 'soybean', 'pigeonpeas', 'jute'],
        'description': 'Monsoon crops - peak planting season'
    },
    'August': {
        'season': 'Monsoon',
        'crops': ['rice', 'maize', 'cotton', 'sugarcane', 'groundnut', 'soybean', 'pigeonpeas', 'jute'],
        'description': 'Monsoon crops - continued planting'
    },
    'September': {
        'season': 'Post-Monsoon',
        'crops': ['rice', 'maize', 'cotton', 'sugarcane', 'groundnut', 'soybean', 'pigeonpeas'],
        'description': 'Post-monsoon crops - harvest preparation'
    },
    'October': {
        'season': 'Autumn',
        'crops': ['rice', 'wheat', 'chickpea', 'lentil', 'mustard', 'barley', 'potato', 'sugarcane'],
        'description': 'Autumn crops - winter crop planting begins'
    },
    'November': {
        'season': 'Autumn',
        'crops': ['wheat', 'chickpea', 'lentil', 'mustard', 'barley', 'peas', 'potato'],
        'description': 'Autumn crops - winter crop season'
    },
    'December': {
        'season': 'Winter',
        'crops': ['wheat', 'chickpea', 'lentil', 'mustard', 'barley', 'peas', 'potato'],
        'description': 'Winter crops - ideal for cool weather'
    }
}

def get_crops_for_month(month):
    """Get recommended crops for a specific month"""
    if month in MONTH_CROPS:
        return MONTH_CROPS[month]
    return None

def filter_crops_by_month(predicted_crop, month):
    """
    Check if predicted crop is suitable for the given month
    If not, suggest alternative crops for that month
    """
    month_data = get_crops_for_month(month)
    if not month_data:
        return {
            'crop': predicted_crop,
            'suitable': True,
            'reason': 'Month not found'
        }
    
    suitable_crops = month_data['crops']
    predicted_crop_lower = predicted_crop.lower()
    
    if predicted_crop_lower in suitable_crops:
        return {
            'crop': predicted_crop,
            'suitable': True,
            'season': month_data['season'],
            'reason': f'{predicted_crop} is ideal for {month} ({month_data["season"]})',
            'alternatives': suitable_crops
        }
    else:
        return {
            'crop': predicted_crop,
            'suitable': False,
            'season': month_data['season'],
            'reason': f'{predicted_crop} is not ideal for {month}. Consider these alternatives:',
            'alternatives': suitable_crops,
            'recommended': suitable_crops[0] if suitable_crops else predicted_crop
        }

def get_all_months():
    """Get list of all months"""
    return list(MONTH_CROPS.keys())

def get_season_info(month):
    """Get season information for a month"""
    month_data = get_crops_for_month(month)
    if month_data:
        return {
            'month': month,
            'season': month_data['season'],
            'description': month_data['description'],
            'crops': month_data['crops']
        }
    return None
