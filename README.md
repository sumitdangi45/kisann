# KisanSathi - Smart Farming Assistant

An AI-driven agricultural platform offering crop recommendations, fertilizer suggestions, and disease detection for optimal farming.

## 📁 Project Structure

```
kisansathi/
├── frontend/                 # React + TypeScript + Tailwind CSS
│   └── pixel-perfect-copy/   # Main React app
│       ├── src/
│       │   ├── components/   # React components (Crop, Fertilizer, Disease)
│       │   ├── pages/        # Page components
│       │   └── App.tsx       # Main app with routes
│       └── package.json
│
├── backend/                  # Flask Python API
│   ├── app.py               # Main Flask application
│   ├── config.py            # Configuration
│   ├── requirements.txt      # Python dependencies
│   ├── utils/               # Utility modules (disease, fertilizer, model)
│   ├── models/              # ML models (RandomForest, ResNet-99, etc.)
│   ├── Data/                # Processed data (fertilizer.csv, crop data)
│   ├── Data-raw/            # Raw datasets
│   ├── static/              # CSS, images, JavaScript
│   └── templates/           # HTML templates
│
├── docs/                     # Documentation
│   ├── README.md
│   ├── MODEL_TRAINING_SUMMARY.md
│   ├── QUICK_START.md
│   ├── SAMPLE_DATA.md
│   ├── START_HERE.md
│   ├── TEST_GUIDE.txt
│   ├── TESTING_SUMMARY.md
│   └── notebooks/           # Jupyter notebooks for model training
│
└── README.md               # This file
```

## 🚀 Quick Start

### Prerequisites
- Python 3.7+
- Node.js 14+
- npm or yarn

### Backend Setup

```bash
cd backend
pip install -r requirements.txt
python app.py
```

Backend runs on: `http://localhost:5000`

### Frontend Setup

```bash
cd frontend/pixel-perfect-copy
npm install
npm run dev
```

Frontend runs on: `http://localhost:8080`

## 🎯 Features

### 1. Crop Recommendation
- Analyzes soil nutrients (N, P, K), pH, rainfall, and weather
- Recommends best crop for maximum yield
- Uses Random Forest ML model

### 2. Fertilizer Recommendation
- Analyzes current soil nutrient levels
- Identifies deficiencies or excess
- Provides specific fertilizer recommendations

### 3. Disease Detection
- Identifies plant diseases from leaf images
- Uses ResNet-99 deep learning model (99.2% accuracy)
- Provides prevention and cure tips

## 🛠️ Tech Stack

**Frontend:**
- React 18
- TypeScript
- Tailwind CSS
- Vite
- React Router

**Backend:**
- Flask
- Python 3
- Scikit-learn (ML models)
- PyTorch (Deep learning)
- Pandas & NumPy (Data processing)

**APIs:**
- OpenWeatherMap (Weather data)

## 📊 API Endpoints

### Crop Prediction
```
POST /api/crop-predict
{
  "nitrogen": 40,
  "phosphorous": 40,
  "potassium": 40,
  "ph": 6.5,
  "rainfall": 200,
  "city": "Delhi"
}
```

### Fertilizer Prediction
```
POST /api/fertilizer-predict
{
  "cropname": "rice",
  "nitrogen": 20,
  "phosphorous": 40,
  "potassium": 40
}
```

### Disease Detection
```
POST /api/disease-predict
(multipart/form-data with image file)
```

## 📚 Documentation

- `docs/README.md` - Full documentation
- `docs/QUICK_START.md` - Quick reference
- `docs/SAMPLE_DATA.md` - Test data and examples
- `docs/MODEL_TRAINING_SUMMARY.md` - Model details
- `docs/notebooks/` - Jupyter notebooks for model training

## 🧪 Testing

Sample test data available in `docs/SAMPLE_DATA.md`

**Test Crop Recommendation:**
- N=40, P=40, K=40, pH=6.5, Rainfall=200, City=Delhi
- Expected: Rice

**Test Fertilizer:**
- Crop=Rice, N=20, P=40, K=40
- Expected: Low Nitrogen recommendation

**Test Disease Detection:**
- Upload any plant leaf image
- Expected: Disease information

## 🌍 Supported Cities

Delhi, Mumbai, Bangalore, Pune, Chennai, Hyderabad, Kolkata, Ahmedabad, Jaipur, Lucknow

## 📈 Supported Crops

Rice, Maize, Chickpea, Kidney Beans, Pigeon Peas, Moth Beans, Mung Bean, Black Gram, Lentil, Pomegranate, Banana, Mango, Grapes, Watermelon, Muskmelon, Apple, Orange, Papaya, Coconut

## 🔧 Configuration

Edit `backend/config.py` to configure:
- Weather API key
- Database settings
- Application settings

## 📝 License

Open source - MIT License

## 🤝 Contributing

Contributions welcome! Feel free to:
- Report bugs
- Suggest improvements
- Submit pull requests

## 📞 Contact

For questions or suggestions, reach out to the development team.

---

**Status:** ✅ Production Ready  
**Version:** 1.0.0  
**Last Updated:** April 2026
