# 🚀 CropCareAI - Quick Start Guide

## Running the Application

```bash
cd CropcareAI/app
python app.py
```

The app will start at: **http://localhost:5000**

---

## 📱 Features Overview

### 1. 🌾 Crop Recommendation
**Purpose:** Suggests the best crop to grow based on soil conditions and weather

**How to use:**
1. Click "Crop Recommendation"
2. Enter soil nutrients (N, P, K values)
3. Enter soil pH
4. Enter expected rainfall
5. Select your city (for weather data)
6. Click "Predict"

**Sample Input:**
```
Nitrogen: 40
Phosphorous: 40
Potassium: 40
pH: 6.5
Rainfall: 200 mm
City: Delhi
```

---

### 2. 🧪 Fertilizer Recommendation
**Purpose:** Analyzes soil nutrients and recommends fertilizer adjustments

**How to use:**
1. Click "Fertilizer Suggestion"
2. Select crop name
3. Enter current soil nutrients (N, P, K)
4. Click "Predict"

**Sample Input:**
```
Crop: Rice
Nitrogen: 20
Phosphorous: 40
Potassium: 40
```

**Output:** Will show which nutrient is deficient/excess and recommendations

---

### 3. 🍃 Disease Detection
**Purpose:** Identifies plant diseases from leaf images

**How to use:**
1. Click "Disease Detection"
2. Upload a plant leaf image
3. Click "Predict"
4. View disease information and prevention tips

**Supported Crops:**
- Tomato
- Potato
- Apple
- Corn
- Grape
- Pepper

---

## 🧪 Test Data

### Quick Test - Crop Recommendation
```
N: 40, P: 40, K: 40, pH: 6.5, Rainfall: 200, City: Delhi
→ Expected: Rice
```

### Quick Test - Fertilizer
```
Crop: Rice, N: 20, P: 40, K: 40
→ Expected: Low Nitrogen recommendation
```

### Quick Test - Disease Detection
```
Upload any leaf image
→ Expected: Disease information
```

---

## 🌍 Available Cities

Delhi, Mumbai, Bangalore, Pune, Chennai, Hyderabad, Kolkata, Ahmedabad, Jaipur, Lucknow

---

## 📊 Nutrient Reference

| Crop | N (kg/ha) | P (kg/ha) | K (kg/ha) | pH | Rainfall (mm) |
|------|-----------|-----------|-----------|-----|---------------|
| Rice | 40 | 40 | 40 | 6.5 | 200 |
| Wheat | 60 | 45 | 45 | 7.0 | 50 |
| Corn | 60 | 60 | 60 | 6.5 | 60 |
| Potato | 100 | 60 | 60 | 6.0 | 50 |
| Tomato | 100 | 60 | 60 | 6.5 | 50 |
| Cotton | 80 | 40 | 40 | 6.5 | 50 |

---

## 🔧 Troubleshooting

### Issue: "City not found" error
**Solution:** Use common city names like Delhi, Mumbai, Bangalore

### Issue: "Crop not found" in fertilizer
**Solution:** Make sure crop name matches exactly (case-sensitive)

### Issue: Disease detection shows generic result
**Solution:** This is normal - the mock classifier provides consistent results

---

## 📝 File Structure

```
CropcareAI/
├── app/
│   ├── app.py                 # Main Flask application
│   ├── config.py              # Configuration (API keys)
│   ├── requirements.txt        # Python dependencies
│   ├── Data/
│   │   └── fertilizer.csv      # Fertilizer data
│   ├── models/
│   │   └── RandomForest.pkl    # Crop recommendation model
│   ├── utils/
│   │   ├── disease.py          # Disease information
│   │   ├── fertilizer.py       # Fertilizer recommendations
│   │   └── model.py            # ML model definitions
│   ├── static/
│   │   ├── css/                # Stylesheets
│   │   ├── images/             # Images
│   │   └── scripts/            # JavaScript
│   └── templates/
│       ├── index.html          # Home page
│       ├── crop.html           # Crop recommendation form
│       ├── crop-result.html    # Crop results
│       ├── fertilizer.html     # Fertilizer form
│       ├── fertilizer-result.html # Fertilizer results
│       ├── disease.html        # Disease detection form
│       ├── disease-result.html # Disease results
│       └── test-data.html      # Test data reference
├── SAMPLE_DATA.md              # Sample test data
└── QUICK_START.md              # This file
```

---

## 🎯 Next Steps

1. **Test the app** with sample data
2. **Explore features** - try all three modules
3. **Check results** - verify recommendations make sense
4. **Customize** - modify mock models or add real ML models

---

## 📞 Support

For issues or questions:
1. Check the test data page: `http://localhost:5000/test-data`
2. Review SAMPLE_DATA.md for detailed test cases
3. Check app.py for implementation details

---

## ✨ Features Status

- ✅ Crop Recommendation (Mock ML Model)
- ✅ Fertilizer Suggestion (Rule-based)
- ✅ Disease Detection (Image-based classifier)
- ✅ Weather Integration (OpenWeatherMap API)
- ✅ Responsive UI (Bootstrap)

---

**Happy Farming! 🌾**
