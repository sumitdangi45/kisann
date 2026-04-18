# Weather & Alerts - Quick Start Guide

## What's New?
Added a complete **Weather & Alerts** feature to KisanSathi that provides:
- 🌤️ Real-time weather data (temperature, humidity, rainfall, wind)
- 🚨 Automated weather alerts (heat, cold, rain, drought, humidity, wind)
- 🌾 Crop-specific alerts based on optimal growing conditions
- 🔊 Voice output for all alerts and recommendations

## How to Use

### 1. Access Weather Feature
- **URL**: `http://localhost:8080/weather`
- **From Home**: Click on "Weather & Alerts" service card

### 2. Get Weather Data
1. Enter your city name (e.g., Delhi, Mumbai, Bangalore)
2. Click "Get Weather" button
3. View current weather conditions:
   - Temperature (°C)
   - Humidity (%)
   - Rainfall (mm)
   - Wind Speed (km/h)

### 3. View General Alerts
After fetching weather, you'll see:
- **Alert Cards** with color-coded severity:
  - 🔴 **High** (Red) - Immediate action required
  - 🟡 **Medium** (Yellow) - Monitor and prepare
  - 🔵 **Low** (Blue) - Informational

Each alert includes:
- Alert title with emoji
- Detailed message
- Recommendations (bulleted list)
- Affected crops
- Action required indicator

### 4. Get Crop-Specific Alerts
1. Select a crop from dropdown (rice, wheat, maize, cotton, potato, tomato)
2. Click "Get Crop Alerts" button
3. View alerts specific to that crop:
   - Temperature suitability
   - Humidity suitability
   - Rainfall suitability

### 5. Listen to Alerts
- Click **"🔊 Speak"** button on any alert
- Browser will read the alert aloud
- Works in Chrome, Firefox, Safari, Edge

## Alert Types

### General Alerts
| Alert | Trigger | Severity |
|-------|---------|----------|
| 🔥 Heat Alert | Temp > 35°C | Medium/High |
| ❄️ Cold Alert | Temp < 5°C | Medium/High |
| 🌧️ Heavy Rain | Rainfall > 50mm | Medium/High |
| 🏜️ Drought | Rainfall < 10mm | Medium/High |
| 💧 High Humidity | Humidity > 80% | Medium |
| 🌡️ Low Humidity | Humidity < 30% | Low |
| 💨 Strong Wind | Wind > 40 km/h | High |

### Crop-Specific Alerts
Each crop has optimal ranges:
- **Rice**: 20-30°C, 70-90% humidity, 100-200mm rainfall
- **Wheat**: 15-25°C, 40-60% humidity, 40-100mm rainfall
- **Maize**: 20-30°C, 50-70% humidity, 50-100mm rainfall
- **Cotton**: 20-35°C, 40-70% humidity, 50-100mm rainfall
- **Potato**: 15-25°C, 70-90% humidity, 50-100mm rainfall
- **Tomato**: 20-30°C, 60-80% humidity, 50-100mm rainfall

## Example Scenarios

### Scenario 1: High Temperature Alert
```
Temperature: 42°C
Alert: 🔥 Heat Alert (HIGH)
Message: Temperature is 42°C. High heat can damage crops.
Recommendations:
- Increase irrigation frequency
- Apply mulch to retain soil moisture
- Provide shade for sensitive crops
- Water early morning or late evening
- Monitor for heat stress symptoms
```

### Scenario 2: Crop-Specific Alert
```
Crop: Rice
Temperature: 18°C (Below optimal 20-30°C)
Alert: Temperature 18°C is below optimal range (20-30°C)
Severity: Medium
Action: Provide protection or delay planting
```

## Integration with Other Features
- **Crop Recommendation**: Use weather data to refine crop suggestions
- **Fertilizer Recommendation**: Adjust fertilizer based on weather conditions
- **Disease Detection**: Monitor humidity for disease risk

## API Endpoints (For Developers)

### Get Weather & Alerts
```
POST /api/weather
Body: {
  "city": "Delhi",
  "rainfall": 50,
  "wind_speed": 20
}
```

### Get Crop-Specific Alerts
```
POST /api/weather-alerts/{crop}
Body: {
  "city": "Delhi",
  "rainfall": 50,
  "wind_speed": 20
}
```

## Tips & Tricks
1. **Check before planting**: Always check crop-specific alerts before planting
2. **Monitor humidity**: High humidity increases disease risk
3. **Plan irrigation**: Use rainfall data to plan irrigation schedule
4. **Protect crops**: Act on high-severity alerts immediately
5. **Use voice**: Enable voice alerts for hands-free monitoring

## Troubleshooting

### Weather data not loading?
- Check internet connection
- Verify city name spelling
- Try a different city

### No alerts showing?
- Weather conditions might be favorable
- Try different rainfall/wind values
- Check if crop is supported

### Voice not working?
- Enable microphone permissions in browser
- Try a different browser (Chrome works best)
- Check system volume

## Files & Components
- **Backend**: `kisansathi/backend/app.py` (2 new endpoints)
- **Backend Logic**: `kisansathi/backend/utils/weather_alerts.py`
- **Frontend**: `kisansathi/frontend/pixel-perfect-copy/src/components/Weather.tsx`
- **Page**: `kisansathi/frontend/pixel-perfect-copy/src/pages/WeatherPage.tsx`

## Status
✅ Feature is complete and ready to use!
