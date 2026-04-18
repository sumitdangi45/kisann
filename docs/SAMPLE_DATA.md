# CropCareAI - Sample Test Data

Use this sample data to test all features of the application.

---

## 1. 🌾 CROP RECOMMENDATION

### Test Case 1: Rice Growing Conditions
- **Nitrogen (N):** 40
- **Phosphorous (P):** 40
- **Potassium (K):** 40
- **pH:** 6.5
- **Rainfall (mm):** 200
- **City:** Delhi
- **Expected Result:** Rice

### Test Case 2: Wheat Growing Conditions
- **Nitrogen (N):** 60
- **Phosphorous (P):** 45
- **Potassium (K):** 45
- **pH:** 7.0
- **Rainfall (mm):** 50
- **City:** Mumbai
- **Expected Result:** Wheat

### Test Case 3: Corn Growing Conditions
- **Nitrogen (N):** 60
- **Phosphorous (P):** 60
- **Potassium (K):** 60
- **pH:** 6.5
- **Rainfall (mm):** 60
- **City:** Bangalore
- **Expected Result:** Corn

### Test Case 4: Potato Growing Conditions
- **Nitrogen (N):** 100
- **Phosphorous (P):** 60
- **Potassium (K):** 60
- **pH:** 6.0
- **Rainfall (mm):** 50
- **City:** Pune
- **Expected Result:** Potato

### Test Case 5: Tomato Growing Conditions
- **Nitrogen (N):** 100
- **Phosphorous (P):** 60
- **Potassium (K):** 60
- **pH:** 6.5
- **Rainfall (mm):** 50
- **City:** Chennai
- **Expected Result:** Tomato

### Test Case 6: Cotton Growing Conditions
- **Nitrogen (N):** 80
- **Phosphorous (P):** 40
- **Potassium (K):** 40
- **pH:** 6.5
- **Rainfall (mm):** 50
- **City:** Hyderabad
- **Expected Result:** Cotton

---

## 2. 🧪 FERTILIZER RECOMMENDATION

### Test Case 1: Rice - Low Nitrogen
- **Crop Name:** Rice
- **Nitrogen (N):** 20
- **Phosphorous (P):** 40
- **Potassium (K):** 40
- **Expected Result:** Nitrogen is low - recommendation to add nitrogen fertilizer

### Test Case 2: Wheat - High Phosphorous
- **Crop Name:** Wheat
- **Nitrogen (N):** 60
- **Phosphorous (P):** 80
- **Potassium (K):** 45
- **Expected Result:** Phosphorous is high - recommendation to reduce phosphorous

### Test Case 3: Corn - Low Potassium
- **Crop Name:** Corn
- **Nitrogen (N):** 60
- **Phosphorous (P):** 60
- **Potassium (K):** 30
- **Expected Result:** Potassium is low - recommendation to add potassium fertilizer

### Test Case 4: Potato - Balanced Nutrients
- **Crop Name:** Potato
- **Nitrogen (N):** 100
- **Phosphorous (P):** 60
- **Potassium (K):** 60
- **Expected Result:** Nutrients are balanced - no major recommendations

### Test Case 5: Tomato - High Nitrogen
- **Crop Name:** Tomato
- **Nitrogen (N):** 150
- **Phosphorous (P):** 60
- **Potassium (K):** 60
- **Expected Result:** Nitrogen is high - recommendation to reduce nitrogen

---

## 3. 🍃 DISEASE DETECTION

### Test Case 1: Healthy Leaf
- **Upload any green leaf image**
- **Expected Result:** Disease information for a healthy plant

### Test Case 2: Diseased Leaf
- **Upload any leaf image with spots/discoloration**
- **Expected Result:** Disease information with prevention tips

### Sample Diseases Detected:
- Tomato___healthy
- Tomato___Early_blight
- Tomato___Late_blight
- Potato___healthy
- Potato___Early_blight
- Apple___healthy
- Apple___Apple_scab
- Corn_(maize)___healthy
- Grape___healthy
- Pepper,_bell___healthy

---

## 4. 🌍 WEATHER API TEST

### Cities with Weather Data Available:
- Delhi
- Mumbai
- Bangalore
- Pune
- Chennai
- Hyderabad
- Kolkata
- Ahmedabad
- Jaipur
- Lucknow

**Note:** The app uses OpenWeatherMap API. Make sure the city name is common and available in the API database.

---

## 5. 📊 QUICK TEST WORKFLOW

### Step 1: Test Crop Recommendation
1. Go to "Crop Recommendation"
2. Enter Test Case 1 data (Rice)
3. Click "Predict"
4. Verify result shows "Rice"

### Step 2: Test Fertilizer Recommendation
1. Go to "Fertilizer Suggestion"
2. Enter Test Case 1 data (Rice with low nitrogen)
3. Click "Predict"
4. Verify result shows nitrogen deficiency recommendation

### Step 3: Test Disease Detection
1. Go to "Disease Detection"
2. Upload any plant leaf image
3. Click "Predict"
4. Verify result shows disease information

---

## 6. 🔧 TROUBLESHOOTING

### If Crop Recommendation doesn't work:
- Check if city name is valid and available in OpenWeatherMap
- Try with common cities like Delhi, Mumbai, Bangalore

### If Fertilizer Recommendation shows error:
- Verify crop name matches exactly (case-sensitive)
- Check if crop exists in the fertilizer database

### If Disease Detection shows generic result:
- This is expected - the mock classifier provides consistent results
- For real ML predictions, install PyTorch

---

## 7. 📝 NOTES

- All sample data is based on typical Indian agricultural conditions
- Nutrient values are in kg/hectare
- pH values are on a scale of 0-14
- Rainfall is in millimeters
- Temperature and humidity are fetched from OpenWeatherMap API
