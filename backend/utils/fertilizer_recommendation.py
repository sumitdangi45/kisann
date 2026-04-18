"""
Fertilizer recommendation based on crop and soil parameters
"""

# Fertilizer database with crop-specific requirements
FERTILIZER_DATABASE = {
    'rice': {
        'nitrogen': {'low': (0, 40), 'medium': (40, 80), 'high': (80, 150)},
        'phosphorus': {'low': (0, 20), 'medium': (20, 40), 'high': (40, 100)},
        'potassium': {'low': (0, 20), 'medium': (20, 40), 'high': (40, 100)},
        'recommendations': {
            'low_nitrogen': {
                'fertilizer': 'Urea (46% N)',
                'quantity': '50-60 kg/hectare',
                'timing': 'Split into 2-3 doses',
                'reason': 'Rice requires high nitrogen for vegetative growth',
                'benefits': 'Increases leaf area, tillering, and grain yield'
            },
            'low_phosphorus': {
                'fertilizer': 'Single Super Phosphate (16% P2O5)',
                'quantity': '40-50 kg/hectare',
                'timing': 'Apply at planting',
                'reason': 'Phosphorus promotes root development and grain formation',
                'benefits': 'Better root system, improved grain quality'
            },
            'low_potassium': {
                'fertilizer': 'Muriate of Potash (60% K2O)',
                'quantity': '30-40 kg/hectare',
                'timing': 'Apply at panicle initiation',
                'reason': 'Potassium improves disease resistance and grain quality',
                'benefits': 'Stronger stems, disease resistance, better grain filling'
            },
            'balanced': {
                'fertilizer': 'NPK 10:26:26 or 12:32:16',
                'quantity': '200-250 kg/hectare',
                'timing': 'Apply at planting and tillering',
                'reason': 'Balanced nutrition for optimal growth',
                'benefits': 'Complete nutrition for all growth stages'
            }
        }
    },
    'wheat': {
        'nitrogen': {'low': (0, 50), 'medium': (50, 100), 'high': (100, 180)},
        'phosphorus': {'low': (0, 25), 'medium': (25, 50), 'high': (50, 100)},
        'potassium': {'low': (0, 25), 'medium': (25, 50), 'high': (50, 100)},
        'recommendations': {
            'low_nitrogen': {
                'fertilizer': 'Urea (46% N)',
                'quantity': '60-80 kg/hectare',
                'timing': '3 splits: at sowing, tillering, and boot stage',
                'reason': 'Wheat needs high nitrogen for grain development',
                'benefits': 'Increases grain number and weight'
            },
            'low_phosphorus': {
                'fertilizer': 'Diammonium Phosphate (18% N, 46% P2O5)',
                'quantity': '50-60 kg/hectare',
                'timing': 'Apply at sowing',
                'reason': 'Phosphorus essential for root development',
                'benefits': 'Strong root system, better nutrient uptake'
            },
            'low_potassium': {
                'fertilizer': 'Muriate of Potash (60% K2O)',
                'quantity': '30-40 kg/hectare',
                'timing': 'Apply at tillering',
                'reason': 'Potassium strengthens stems and improves grain quality',
                'benefits': 'Reduced lodging, better grain quality'
            },
            'balanced': {
                'fertilizer': 'NPK 10:26:26',
                'quantity': '250-300 kg/hectare',
                'timing': 'Apply at sowing and tillering',
                'reason': 'Balanced nutrition for optimal yield',
                'benefits': 'Complete nutrition throughout growing season'
            }
        }
    },
    'maize': {
        'nitrogen': {'low': (0, 60), 'medium': (60, 120), 'high': (120, 200)},
        'phosphorus': {'low': (0, 30), 'medium': (30, 60), 'high': (60, 120)},
        'potassium': {'low': (0, 30), 'medium': (30, 60), 'high': (60, 120)},
        'recommendations': {
            'low_nitrogen': {
                'fertilizer': 'Urea (46% N)',
                'quantity': '80-100 kg/hectare',
                'timing': '2 splits: at planting and V6 stage',
                'reason': 'Maize is nitrogen-hungry crop',
                'benefits': 'Increases plant height, leaf area, and grain yield'
            },
            'low_phosphorus': {
                'fertilizer': 'Single Super Phosphate (16% P2O5)',
                'quantity': '60-80 kg/hectare',
                'timing': 'Apply at planting',
                'reason': 'Phosphorus critical for early root development',
                'benefits': 'Better root system, improved nutrient uptake'
            },
            'low_potassium': {
                'fertilizer': 'Muriate of Potash (60% K2O)',
                'quantity': '40-50 kg/hectare',
                'timing': 'Apply at V6-V8 stage',
                'reason': 'Potassium improves photosynthesis and grain filling',
                'benefits': 'Better grain filling, improved yield quality'
            },
            'balanced': {
                'fertilizer': 'NPK 12:32:16',
                'quantity': '300-350 kg/hectare',
                'timing': 'Apply at planting and V6 stage',
                'reason': 'Balanced nutrition for high-yielding maize',
                'benefits': 'Complete nutrition for maximum yield'
            }
        }
    },
    'cotton': {
        'nitrogen': {'low': (0, 50), 'medium': (50, 100), 'high': (100, 180)},
        'phosphorus': {'low': (0, 20), 'medium': (20, 40), 'high': (40, 80)},
        'potassium': {'low': (0, 30), 'medium': (30, 60), 'high': (60, 120)},
        'recommendations': {
            'low_nitrogen': {
                'fertilizer': 'Urea (46% N)',
                'quantity': '70-90 kg/hectare',
                'timing': '3 splits: at planting, flowering, and boll formation',
                'reason': 'Cotton needs sustained nitrogen supply',
                'benefits': 'Increased plant vigor, more bolls'
            },
            'low_phosphorus': {
                'fertilizer': 'Single Super Phosphate (16% P2O5)',
                'quantity': '40-50 kg/hectare',
                'timing': 'Apply at planting',
                'reason': 'Phosphorus promotes flowering and boll development',
                'benefits': 'More flowers, better boll set'
            },
            'low_potassium': {
                'fertilizer': 'Muriate of Potash (60% K2O)',
                'quantity': '50-60 kg/hectare',
                'timing': 'Apply at flowering stage',
                'reason': 'Potassium improves fiber quality and disease resistance',
                'benefits': 'Better fiber quality, disease resistance'
            },
            'balanced': {
                'fertilizer': 'NPK 10:26:26',
                'quantity': '250-300 kg/hectare',
                'timing': 'Apply at planting and flowering',
                'reason': 'Balanced nutrition for cotton growth',
                'benefits': 'Complete nutrition for optimal yield'
            }
        }
    },
    'potato': {
        'nitrogen': {'low': (0, 80), 'medium': (80, 150), 'high': (150, 250)},
        'phosphorus': {'low': (0, 40), 'medium': (40, 80), 'high': (80, 150)},
        'potassium': {'low': (0, 80), 'medium': (80, 150), 'high': (150, 250)},
        'recommendations': {
            'low_nitrogen': {
                'fertilizer': 'Urea (46% N)',
                'quantity': '100-120 kg/hectare',
                'timing': '2 splits: at planting and earthing up',
                'reason': 'Potato needs high nitrogen for tuber development',
                'benefits': 'Larger tubers, higher yield'
            },
            'low_phosphorus': {
                'fertilizer': 'Single Super Phosphate (16% P2O5)',
                'quantity': '80-100 kg/hectare',
                'timing': 'Apply at planting',
                'reason': 'Phosphorus essential for tuber formation',
                'benefits': 'Better tuber development, improved quality'
            },
            'low_potassium': {
                'fertilizer': 'Muriate of Potash (60% K2O)',
                'quantity': '100-120 kg/hectare',
                'timing': 'Apply at earthing up',
                'reason': 'Potassium critical for tuber quality and starch content',
                'benefits': 'Better tuber quality, higher starch content'
            },
            'balanced': {
                'fertilizer': 'NPK 10:26:26',
                'quantity': '400-500 kg/hectare',
                'timing': 'Apply at planting and earthing up',
                'reason': 'Balanced nutrition for potato growth',
                'benefits': 'Complete nutrition for maximum yield'
            }
        }
    },
    'coffee': {
        'nitrogen': {'low': (0, 30), 'medium': (30, 60), 'high': (60, 120)},
        'phosphorus': {'low': (0, 15), 'medium': (15, 30), 'high': (30, 60)},
        'potassium': {'low': (0, 30), 'medium': (30, 60), 'high': (60, 120)},
        'recommendations': {
            'low_nitrogen': {
                'fertilizer': 'Urea (46% N)',
                'quantity': '40-50 kg/hectare',
                'timing': '2 splits: pre-monsoon and post-monsoon',
                'reason': 'Coffee needs moderate nitrogen for leaf growth',
                'benefits': 'Healthy foliage, better flowering'
            },
            'low_phosphorus': {
                'fertilizer': 'Single Super Phosphate (16% P2O5)',
                'quantity': '30-40 kg/hectare',
                'timing': 'Apply before monsoon',
                'reason': 'Phosphorus promotes flowering and bean development',
                'benefits': 'Better flowering, improved bean quality'
            },
            'low_potassium': {
                'fertilizer': 'Muriate of Potash (60% K2O)',
                'quantity': '40-50 kg/hectare',
                'timing': 'Apply post-monsoon',
                'reason': 'Potassium improves bean quality and disease resistance',
                'benefits': 'Better bean quality, disease resistance'
            },
            'balanced': {
                'fertilizer': 'NPK 10:26:26',
                'quantity': '150-200 kg/hectare',
                'timing': 'Apply in 2 splits',
                'reason': 'Balanced nutrition for coffee growth',
                'benefits': 'Complete nutrition for optimal yield'
            }
        }
    }
}

def get_nutrient_level(value, crop, nutrient):
    """
    Determine if nutrient level is low, medium, or high
    """
    if crop not in FERTILIZER_DATABASE:
        return 'medium'
    
    ranges = FERTILIZER_DATABASE[crop][nutrient]
    if value <= ranges['low'][1]:
        return 'low'
    elif value <= ranges['medium'][1]:
        return 'medium'
    else:
        return 'high'

def recommend_fertilizer(crop, nitrogen, phosphorus, potassium):
    """
    Recommend fertilizer based on crop and soil parameters
    """
    crop_lower = crop.lower()
    
    if crop_lower not in FERTILIZER_DATABASE:
        return {
            'success': False,
            'error': f'Fertilizer data not available for {crop}',
            'available_crops': list(FERTILIZER_DATABASE.keys())
        }
    
    # Get nutrient levels
    n_level = get_nutrient_level(nitrogen, crop_lower, 'nitrogen')
    p_level = get_nutrient_level(phosphorus, crop_lower, 'phosphorus')
    k_level = get_nutrient_level(potassium, crop_lower, 'potassium')
    
    recommendations = FERTILIZER_DATABASE[crop_lower]['recommendations']
    
    # Determine primary deficiency
    deficiencies = []
    if n_level == 'low':
        deficiencies.append('low_nitrogen')
    if p_level == 'low':
        deficiencies.append('low_phosphorus')
    if k_level == 'low':
        deficiencies.append('low_potassium')
    
    # If no deficiency, recommend balanced fertilizer
    if not deficiencies:
        primary_recommendation = recommendations.get('balanced', {})
        deficiency_type = 'balanced'
    else:
        # Use first deficiency as primary
        deficiency_type = deficiencies[0]
        primary_recommendation = recommendations.get(deficiency_type, {})
    
    # Get secondary recommendations for other deficiencies
    secondary_recommendations = []
    for deficiency in deficiencies[1:]:
        if deficiency in recommendations:
            secondary_recommendations.append({
                'type': deficiency,
                'details': recommendations[deficiency]
            })
    
    return {
        'success': True,
        'crop': crop,
        'soil_status': {
            'nitrogen': {'value': nitrogen, 'level': n_level},
            'phosphorus': {'value': phosphorus, 'level': p_level},
            'potassium': {'value': potassium, 'level': k_level}
        },
        'primary_deficiency': deficiency_type,
        'primary_recommendation': primary_recommendation,
        'secondary_recommendations': secondary_recommendations,
        'all_deficiencies': deficiencies,
        'summary': f"Your {crop} soil has {n_level} nitrogen, {p_level} phosphorus, and {k_level} potassium. Primary recommendation: {primary_recommendation.get('fertilizer', 'N/A')}"
    }

def get_fertilizer_info(fertilizer_name):
    """
    Get detailed information about a specific fertilizer
    """
    fertilizer_info = {
        'Urea (46% N)': {
            'type': 'Nitrogen fertilizer',
            'composition': '46% Nitrogen',
            'solubility': 'Highly soluble',
            'application': 'Can be applied as granules or solution',
            'cost': 'Low to medium',
            'storage': 'Keep in dry place'
        },
        'Single Super Phosphate (16% P2O5)': {
            'type': 'Phosphorus fertilizer',
            'composition': '16% P2O5, 11% Sulfur',
            'solubility': 'Slightly soluble',
            'application': 'Apply as granules at planting',
            'cost': 'Low',
            'storage': 'Keep dry'
        },
        'Diammonium Phosphate (18% N, 46% P2O5)': {
            'type': 'Nitrogen + Phosphorus fertilizer',
            'composition': '18% N, 46% P2O5',
            'solubility': 'Soluble',
            'application': 'Apply at planting',
            'cost': 'Medium',
            'storage': 'Keep dry'
        },
        'Muriate of Potash (60% K2O)': {
            'type': 'Potassium fertilizer',
            'composition': '60% K2O',
            'solubility': 'Highly soluble',
            'application': 'Apply as granules or solution',
            'cost': 'Medium',
            'storage': 'Keep dry'
        },
        'NPK 10:26:26': {
            'type': 'Balanced NPK fertilizer',
            'composition': '10% N, 26% P2O5, 26% K2O',
            'solubility': 'Soluble',
            'application': 'Apply at planting and during growth',
            'cost': 'Medium to high',
            'storage': 'Keep dry'
        },
        'NPK 12:32:16': {
            'type': 'Balanced NPK fertilizer',
            'composition': '12% N, 32% P2O5, 16% K2O',
            'solubility': 'Soluble',
            'application': 'Apply at planting and during growth',
            'cost': 'Medium to high',
            'storage': 'Keep dry'
        }
    }
    
    return fertilizer_info.get(fertilizer_name, {})
