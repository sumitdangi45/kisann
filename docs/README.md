# 🌾 KisanSathi - Smart Farming Assistant
#### An AI-driven platform offering crop recommendations, fertilizer suggestions, and disease detection for optimal farming.

**Developed by:** Sumit

---

## 🎯 Features

### 1. 🌾 Crop Recommendation
- Analyzes soil nutrients (N, P, K), pH, rainfall, and weather conditions
- Recommends the best crop to grow for maximum yield
- Uses intelligent ML-based scoring system

### 2. 🧪 Fertilizer Recommendation
- Analyzes current soil nutrient levels
- Identifies nutrient deficiencies or excess
- Provides specific fertilizer recommendations

### 3. 🍃 Disease Detection
- Identifies plant diseases from leaf images
- Provides disease information and prevention tips
- Supports multiple crop types

---

## 💡 How It Works

### Crop Recommendation
1. Enter soil nutrient values (Nitrogen, Phosphorous, Potassium)
2. Enter soil pH and expected rainfall
3. Select your city (for weather data)
4. Get personalized crop recommendation

### Fertilizer Suggestion
1. Select your crop type
2. Enter current soil nutrient levels
3. Get recommendations for nutrient adjustments
4. Receive specific fertilizer suggestions

### Disease Detection
1. Upload a plant leaf image
2. System analyzes the image
3. Get disease identification and prevention tips

---

## 🛠️ Built With

- **Backend:** Flask (Python)
- **Frontend:** HTML, CSS, Bootstrap, JavaScript
- **ML/Data:** NumPy, Pandas, Scikit-learn
- **API:** OpenWeatherMap (Weather data)
- **Database:** CSV files

---

## 📊 Tech Stack

<code><img height="30" src="https://raw.githubusercontent.com/github/explore/80688e429a7d4ef2fca1e82350fe8e3517d3494d/topics/python/python.png"></code>
<code><img height="30" src="https://raw.githubusercontent.com/github/explore/80688e429a7d4ef2fca1e82350fe8e3517d3494d/topics/html/html.png"></code>
<code><img height="30" src="https://raw.githubusercontent.com/github/explore/80688e429a7d4ef2fca1e82350fe8e3517d3494d/topics/css/css.png"></code>
<code><img height="30" src="https://raw.githubusercontent.com/github/explore/80688e429a7d4ef2fca1e82350fe8e3517d3494d/topics/javascript/javascript.png"></code>
<code><img height="30" src="https://github.com/tomchen/stack-icons/raw/master/logos/bootstrap.svg"></code>
<code><img height="30" src="https://raw.githubusercontent.com/github/explore/80688e429a7d4ef2fca1e82350fe8e3517d3494d/topics/git/git.png"></code>
<code><img height="30" src="https://symbols.getvecta.com/stencil_80/56_flask.3a79b5a056.jpg"></code>

---

## 🚀 Quick Start

### Prerequisites
- Python 3.7+
- pip (Python package manager)

### Installation

1. Clone the repository
```bash
git clone https://github.com/yourusername/kisansathi.git
cd kisansathi
```

2. Install dependencies
```bash
cd app
pip install -r requirements.txt
```

3. Run the application
```bash
python app.py
```

4. Open your browser and visit
```
http://localhost:5000
```

---

## 📖 Usage Guide

### Crop Recommendation
- Enter soil nutrient values (kg/hectare)
- Enter soil pH (0-14 scale)
- Enter expected rainfall (mm)
- Select your city
- Click "Predict" to get recommendation

### Fertilizer Recommendation
- Select crop name
- Enter current soil nutrient levels
- Click "Predict" to get recommendations

### Disease Detection
- Click "Disease Detection"
- Upload a plant leaf image
- Click "Predict" to identify disease
- View prevention and cure tips

---

## 🌍 Supported Cities

Delhi, Mumbai, Bangalore, Pune, Chennai, Hyderabad, Kolkata, Ahmedabad, Jaipur, Lucknow

---

## 📁 Project Structure

```
kisansathi/
├── app/
│   ├── app.py                 # Main Flask application
│   ├── config.py              # Configuration
│   ├── requirements.txt        # Dependencies
│   ├── templates/             # HTML templates
│   ├── static/                # CSS, images, JavaScript
│   ├── utils/                 # Utility functions
│   └── Data/                  # Data files
├── models/                    # ML models
├── README.md                  # This file
└── LICENSE                    # License
```

---

## 🧪 Testing

Sample test data is provided in the documentation:

**Test 1 - Crop Recommendation:**
```
N=40, P=40, K=40, pH=6.5, Rainfall=200, City=Delhi
Expected: Rice
```

**Test 2 - Fertilizer Recommendation:**
```
Crop=Rice, N=20, P=40, K=40
Expected: Low Nitrogen recommendation
```

**Test 3 - Disease Detection:**
```
Upload any leaf image
Expected: Disease information
```

---

## 📚 Documentation

- `SAMPLE_DATA.md` - Detailed test cases
- `QUICK_START.md` - Quick reference guide
- `TEST_GUIDE.txt` - Complete testing workflow
- `START_HERE.md` - Getting started guide

---

## 🔧 Configuration

Edit `app/config.py` to configure:
- Weather API key
- Database settings
- Application settings

---

## 🐛 Troubleshooting

**Issue:** App won't start
- Check if port 5000 is available
- Ensure all dependencies are installed

**Issue:** City not found
- Use common city names from the supported list
- Check internet connection for weather API

**Issue:** Disease detection not working
- Ensure image is a valid plant leaf
- Try different image formats (JPG, PNG)

---

## 📈 Future Improvements

- Real-time ML model for disease detection
- Mobile app version
- Multi-language support
- Advanced analytics dashboard
- Integration with IoT sensors
- Blockchain for supply chain tracking

---

## 📝 License

This project is open source and available under the MIT License.

---

## 🤝 Contributing

Contributions are welcome! Feel free to:
- Report bugs
- Suggest improvements
- Submit pull requests
- Share feedback

---

## 📞 Contact

For questions or suggestions, please reach out to the development team.

---

**Last Updated:** March 30, 2026
**Status:** ✅ Production Ready
**Version:** 1.0.0

---

**Happy Farming! 🌾**
