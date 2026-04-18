"""
Weather alerts for farmers based on current conditions
"""

def get_weather_alerts(temperature, humidity, rainfall, wind_speed=0):
    """
    Generate weather alerts based on current conditions
    """
    alerts = []
    
    # Heat Alert
    if temperature > 35:
        alerts.append({
            'type': 'heat_alert',
            'severity': 'high' if temperature > 40 else 'medium',
            'title': '🔥 Heat Alert',
            'message': f'Temperature is {temperature}°C. High heat can damage crops.',
            'recommendations': [
                'Increase irrigation frequency',
                'Apply mulch to retain soil moisture',
                'Provide shade for sensitive crops',
                'Water early morning or late evening',
                'Monitor for heat stress symptoms'
            ],
            'affected_crops': ['tomato', 'pepper', 'cucumber', 'lettuce'],
            'action_required': True
        })
    
    # Cold Alert
    elif temperature < 5:
        alerts.append({
            'type': 'cold_alert',
            'severity': 'high' if temperature < 0 else 'medium',
            'title': '❄️ Cold Alert',
            'message': f'Temperature is {temperature}°C. Frost risk for sensitive crops.',
            'recommendations': [
                'Cover sensitive plants with cloth',
                'Avoid irrigation before frost',
                'Use frost protection methods',
                'Monitor weather forecast',
                'Prepare frost protection materials'
            ],
            'affected_crops': ['tomato', 'pepper', 'cucumber', 'beans'],
            'action_required': True
        })
    
    # Rain Alert
    if rainfall > 50:
        alerts.append({
            'type': 'rain_alert',
            'severity': 'high' if rainfall > 100 else 'medium',
            'title': '🌧️ Heavy Rain Alert',
            'message': f'Heavy rainfall expected: {rainfall}mm. Risk of waterlogging.',
            'recommendations': [
                'Ensure proper drainage in fields',
                'Avoid planting in low-lying areas',
                'Check irrigation systems',
                'Prepare for potential flooding',
                'Harvest ripe crops before heavy rain'
            ],
            'affected_crops': ['rice', 'wheat', 'maize', 'cotton'],
            'action_required': True
        })
    
    # Drought Alert
    elif rainfall < 10:
        alerts.append({
            'type': 'drought_alert',
            'severity': 'high' if rainfall < 5 else 'medium',
            'title': '🏜️ Drought Alert',
            'message': f'Low rainfall: {rainfall}mm. Risk of water scarcity.',
            'recommendations': [
                'Increase irrigation',
                'Use drip irrigation systems',
                'Apply mulch to conserve moisture',
                'Choose drought-resistant varieties',
                'Monitor soil moisture regularly'
            ],
            'affected_crops': ['wheat', 'maize', 'cotton', 'groundnut'],
            'action_required': True
        })
    
    # High Humidity Alert (Disease Risk)
    if humidity > 80:
        alerts.append({
            'type': 'humidity_alert',
            'severity': 'medium',
            'title': '💧 High Humidity Alert',
            'message': f'Humidity is {humidity}%. High risk of fungal diseases.',
            'recommendations': [
                'Improve air circulation',
                'Avoid overhead irrigation',
                'Apply fungicide if needed',
                'Remove infected leaves',
                'Monitor for disease symptoms'
            ],
            'affected_crops': ['tomato', 'potato', 'grape', 'rice'],
            'action_required': True
        })
    
    # Low Humidity Alert
    elif humidity < 30:
        alerts.append({
            'type': 'low_humidity_alert',
            'severity': 'low',
            'title': '🌡️ Low Humidity Alert',
            'message': f'Humidity is {humidity}%. Risk of pest infestation.',
            'recommendations': [
                'Increase irrigation',
                'Apply mulch',
                'Monitor for pests',
                'Maintain soil moisture',
                'Use pest management practices'
            ],
            'affected_crops': ['cotton', 'groundnut', 'maize'],
            'action_required': False
        })
    
    # Wind Alert
    if wind_speed > 40:
        alerts.append({
            'type': 'wind_alert',
            'severity': 'high',
            'title': '💨 Strong Wind Alert',
            'message': f'Strong winds expected: {wind_speed} km/h. Risk of crop damage.',
            'recommendations': [
                'Stake tall plants',
                'Provide windbreaks',
                'Harvest ripe crops',
                'Secure loose structures',
                'Monitor for physical damage'
            ],
            'affected_crops': ['tomato', 'cotton', 'maize', 'sunflower'],
            'action_required': True
        })
    
    return alerts


def get_weather_summary(temperature, humidity, rainfall, wind_speed=0):
    """
    Get a summary of current weather conditions
    """
    summary = {
        'temperature': temperature,
        'humidity': humidity,
        'rainfall': rainfall,
        'wind_speed': wind_speed,
        'conditions': get_weather_condition(temperature, humidity, rainfall),
        'alerts_count': len(get_weather_alerts(temperature, humidity, rainfall, wind_speed)),
        'recommendation': get_general_recommendation(temperature, humidity, rainfall)
    }
    return summary


def get_weather_condition(temperature, humidity, rainfall):
    """
    Determine weather condition based on parameters
    """
    if rainfall > 50:
        return 'Heavy Rain'
    elif rainfall > 20:
        return 'Rainy'
    elif rainfall > 5:
        return 'Light Rain'
    elif humidity > 80:
        return 'Cloudy & Humid'
    elif humidity > 60:
        return 'Partly Cloudy'
    elif temperature > 35:
        return 'Hot & Dry'
    elif temperature < 5:
        return 'Cold'
    else:
        return 'Clear'


def get_general_recommendation(temperature, humidity, rainfall):
    """
    Get general farming recommendation based on weather
    """
    if rainfall > 50:
        return 'Good day for indoor work. Avoid field operations due to heavy rain.'
    elif rainfall > 20:
        return 'Rainy conditions. Ensure proper drainage. Avoid pesticide application.'
    elif temperature > 35:
        return 'Hot weather. Increase irrigation. Water early morning or late evening.'
    elif temperature < 5:
        return 'Cold weather. Protect sensitive crops. Avoid frost-prone areas.'
    elif humidity > 80:
        return 'High humidity. Risk of diseases. Improve air circulation.'
    else:
        return 'Favorable weather conditions for farming operations.'


def get_crop_specific_alerts(crop, temperature, humidity, rainfall):
    """
    Get alerts specific to a particular crop
    """
    crop_lower = crop.lower()
    
    crop_requirements = {
        'rice': {
            'temp_range': (20, 30),
            'humidity_range': (70, 90),
            'rainfall_range': (100, 200),
            'sensitive_to': ['cold', 'drought', 'high_wind']
        },
        'wheat': {
            'temp_range': (15, 25),
            'humidity_range': (40, 60),
            'rainfall_range': (40, 100),
            'sensitive_to': ['heat', 'frost', 'drought']
        },
        'maize': {
            'temp_range': (20, 30),
            'humidity_range': (50, 70),
            'rainfall_range': (50, 100),
            'sensitive_to': ['cold', 'drought', 'high_wind']
        },
        'cotton': {
            'temp_range': (20, 35),
            'humidity_range': (40, 70),
            'rainfall_range': (50, 100),
            'sensitive_to': ['cold', 'high_humidity', 'high_wind']
        },
        'potato': {
            'temp_range': (15, 25),
            'humidity_range': (70, 90),
            'rainfall_range': (50, 100),
            'sensitive_to': ['heat', 'high_humidity', 'drought']
        },
        'tomato': {
            'temp_range': (20, 30),
            'humidity_range': (60, 80),
            'rainfall_range': (50, 100),
            'sensitive_to': ['heat', 'cold', 'high_humidity']
        }
    }
    
    if crop_lower not in crop_requirements:
        return []
    
    requirements = crop_requirements[crop_lower]
    crop_alerts = []
    
    # Check temperature
    temp_min, temp_max = requirements['temp_range']
    if temperature < temp_min:
        crop_alerts.append({
            'type': 'crop_specific',
            'crop': crop,
            'issue': f'Temperature {temperature}°C is below optimal range ({temp_min}-{temp_max}°C)',
            'severity': 'medium',
            'action': 'Provide protection or delay planting'
        })
    elif temperature > temp_max:
        crop_alerts.append({
            'type': 'crop_specific',
            'crop': crop,
            'issue': f'Temperature {temperature}°C is above optimal range ({temp_min}-{temp_max}°C)',
            'severity': 'medium',
            'action': 'Increase irrigation and provide shade'
        })
    
    # Check humidity
    humid_min, humid_max = requirements['humidity_range']
    if humidity < humid_min:
        crop_alerts.append({
            'type': 'crop_specific',
            'crop': crop,
            'issue': f'Humidity {humidity}% is below optimal range ({humid_min}-{humid_max}%)',
            'severity': 'low',
            'action': 'Increase irrigation frequency'
        })
    elif humidity > humid_max:
        crop_alerts.append({
            'type': 'crop_specific',
            'crop': crop,
            'issue': f'Humidity {humidity}% is above optimal range ({humid_min}-{humid_max}%)',
            'severity': 'medium',
            'action': 'Improve air circulation and apply fungicide'
        })
    
    # Check rainfall
    rain_min, rain_max = requirements['rainfall_range']
    if rainfall < rain_min:
        crop_alerts.append({
            'type': 'crop_specific',
            'crop': crop,
            'issue': f'Rainfall {rainfall}mm is below optimal range ({rain_min}-{rain_max}mm)',
            'severity': 'medium',
            'action': 'Increase irrigation'
        })
    elif rainfall > rain_max:
        crop_alerts.append({
            'type': 'crop_specific',
            'crop': crop,
            'issue': f'Rainfall {rainfall}mm is above optimal range ({rain_min}-{rain_max}mm)',
            'severity': 'medium',
            'action': 'Ensure proper drainage'
        })
    
    return crop_alerts
