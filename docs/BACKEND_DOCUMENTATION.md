# KisanSathi Backend Documentation

## Project Overview
KisanSathi is an AI-powered smart farming assistant that helps Indian farmers with:
- Crop recommendations based on soil and weather
- Disease detection from crop images
- Fertilizer recommendations
- Weather-based farming alerts
- Voice and text-based AI chatbot
- Crop lifecycle management
- Government scheme information

---

## Technology Stack

### Backend Framework
- **Flask** - Python web framework
- **Python 3.8+** - Programming language

### AI/ML Libraries
- **Google Gemini API** - AI chatbot and explanations
- **OpenAI API** (optional) - Alternative to Gemini
- **scikit-learn** - Machine learning models
- **TensorFlow/PyTorch** - Deep learning for disease detection
- **Tesseract OCR** - Text extraction from images
- **PyPDF2** - PDF text extraction

### APIs & Services
- **Open-Meteo API** - Free weather data (no API key required)
- **WeatherAPI** - Alternative weather service
- **Google Gemini API** - AI responses

### Database & Storage
- **JSON files** - Local data storage for reminders and crops
- **Pickle files** - ML model serialization

---

## Project Structure

```
kisansathi/backend/
├── app.py                          # Main Flask application
├── config.py                       # Configuration settings
├── requirements.txt                # Python dependencies
├── .env                           # Environment variables
├── models/                        # Pre-trained ML models
│   ├── crop_model_trained.pkl    # Crop recommendation model
│   ├── crop_encoder.pkl          # Crop label encoder
│   ├── crop_features.pkl         # Feature names
│   ├── plant_disease_model.pth   # Disease detection model
│   └── RandomForest.pkl          # Fertilizer model
├── Data/                          # Data files
│   ├── Data-processed/           # Processed datasets
│   │   ├── crop_recommendation.csv
│   │   └── fertilizer.csv
│   └── reminders/                # Reminder data
│       ├── crops.json
│       └── reminders.json
├── utils/                         # Utility modules
│   ├── unified_chatbot.py        # AI chatbot integration
│   ├── weather_integration.py    # Weather API integration
│   ├── crop_identifier.py        # Crop identification
│   ├── crop_lifecycle.py         # Crop stage tracking
│   ├── fertilizer_recommendation.py
│   ├── disease.py                # Disease detection
│   ├── image_extractor.py        # Image OCR
│   ├── pdf_extractor.py          # PDF text extraction
│   ├── reminders_db.py           # Reminder management
│   ├── smart_notifications.py    # Notification system
│   ├── voice_assistant.py        # Voice processing
│   ├── weather_alerts.py         # Weather alerts
│   ├── month_crops.py            # Seasonal crop info
│   └── gemini_helper.py          # Gemini API helper
└── static/                        # Static files (CSS, JS, images)
```

---

## API Endpoints

### 1. Crop Recommendation APIs

#### POST `/api/crop-prediction`
Predict best crops based on soil parameters
```json
{
  "N": 90,
  "P": 42,
  "K": 43,
  "temperature": 20.87,
  "humidity": 82.0,
  "ph": 6.5,
  "rainfall": 202.9
}
```
**Response:**
```json
{
  "crop": "rice",
  "confidence": 0.95,
  "reason": "Optimal conditions for rice cultivation"
}
```

#### POST `/api/crop-prediction-partial`
Predict crops with minimum 4 parameters (uses defaults for missing)
```json
{
  "N": 90,
  "P": 42,
  "K": 43,
  "temperature": 20.87
}
```

#### GET `/api/get-months`
Get crops suitable for each month
**Response:**
```json
{
  "January": ["Wheat", "Barley", "Gram"],
  "February": ["Wheat", "Mustard"],
  ...
}
```

---

### 2. Fertilizer Recommendation APIs

#### POST `/api/fert-recommend`
Get fertilizer recommendations
```json
{
  "crop": "rice",
  "N": 90,
  "P": 42,
  "K": 43
}
```
**Response:**
```json
{
  "fertilizer": "DAP",
  "dosage": "50 kg/hectare",
  "timing": "At planting time"
}
```

#### GET `/api/get-fertilizer-info/<fertilizer_name>`
Get detailed fertilizer information
**Response:**
```json
{
  "name": "DAP",
  "composition": "18:46:0",
  "uses": "Phosphorus and nitrogen source",
  "dosage": "50-100 kg/hectare"
}
```

#### POST `/api/fertilizer-from-image`
Identify fertilizer from image
- Upload image file
- Returns fertilizer type and recommendations

---

### 3. Disease Detection APIs

#### POST `/api/disease-prediction`
Detect crop disease from image
- Upload crop image
- Returns disease name and treatment options

**Response:**
```json
{
  "disease": "Leaf Blight",
  "confidence": 0.92,
  "treatment": "Spray fungicide",
  "organic_alternative": "Neem oil spray"
}
```

---

### 4. Soil Report APIs

#### POST `/api/soil-report-predict`
Analyze soil report PDF/image
- Upload soil report file
- Extracts text and provides recommendations

**Response:**
```json
{
  "soil_type": "Loamy",
  "pH": 6.5,
  "NPK": "90:42:43",
  "recommendations": ["Add organic matter", "Adjust pH"]
}
```

#### POST `/api/soil-image-prediction`
Analyze soil from image
- Upload soil image
- Returns soil type and properties

---

### 5. Weather APIs

#### GET `/api/get-weather?city=Delhi`
Get current weather and farming recommendations
**Response:**
```json
{
  "city": "Delhi",
  "temperature": 28.5,
  "humidity": 65,
  "wind_speed": 12,
  "rainfall": 0,
  "recommendations": [
    "Increase irrigation frequency",
    "Monitor for pest activity"
  ]
}
```

#### GET `/api/get-crop-alerts?crop=rice`
Get weather-based alerts for specific crop
**Response:**
```json
{
  "crop": "rice",
  "alerts": [
    "High temperature - increase irrigation",
    "Low humidity - mulch soil"
  ]
}
```

---

### 6. Crop Management APIs

#### POST `/api/add-crop`
Add a new crop to farmer's profile
```json
{
  "farmer_id": "farmer_123",
  "crop_name": "rice",
  "planting_date": "2024-06-15",
  "area": 2.5,
  "soil_type": "loamy"
}
```

#### GET `/api/get-crops/<farmer_id>`
Get all crops for a farmer

#### GET `/api/get-crop/<crop_id>`
Get specific crop details

#### GET `/api/get-crop-stage/<crop_id>`
Get current crop growth stage
**Response:**
```json
{
  "stage": "Vegetative",
  "days_elapsed": 45,
  "next_stage": "Flowering",
  "days_to_next": 15
}
```

---

### 7. Reminder & Notification APIs

#### GET `/api/get-today-reminders/<crop_id>`
Get today's farming reminders
**Response:**
```json
{
  "reminders": [
    {
      "id": "rem_001",
      "task": "Water the crop",
      "time": "06:00 AM",
      "completed": false
    }
  ]
}
```

#### GET `/api/get-upcoming-reminders/<crop_id>`
Get upcoming reminders (next 7 days)

#### GET `/api/get-all-reminders/<crop_id>`
Get all reminders for a crop

#### POST `/api/complete-reminder`
Mark reminder as completed
```json
{
  "reminder_id": "rem_001"
}
```

#### POST `/api/upload-photo/<crop_id>`
Upload crop photo for tracking
- Upload image file
- Stores for crop progress tracking

#### GET `/api/get-photos/<crop_id>`
Get all photos for a crop

#### GET `/api/get-stats/<crop_id>`
Get crop statistics
**Response:**
```json
{
  "total_photos": 15,
  "days_since_planting": 45,
  "growth_percentage": 65,
  "health_status": "Good"
}
```

---

### 8. AI Chatbot APIs

#### POST `/api/chatbot-message`
Send message to AI chatbot
```json
{
  "message": "मेरी गेहूं की फसल में क्या समस्या है?",
  "conversation_history": []
}
```
**Response:**
```json
{
  "response": "आपकी गेहूं की फसल के लिए...",
  "language": "hindi",
  "features_detected": ["crop_advice"],
  "timestamp": "2024-04-18T10:30:00"
}
```

#### POST `/api/voice-assistant-ask`
Process voice input
```json
{
  "audio_text": "What fertilizer should I use?",
  "language": "english"
}
```

#### GET `/api/get-quick-answer?question_type=crop_care`
Get quick farming answers

#### GET `/api/get-crop-advice?crop=rice&question_type=disease`
Get specific crop advice

---

### 9. Utility APIs

#### GET `/api/get-available-crops`
Get list of all available crops
**Response:**
```json
{
  "crops": ["rice", "wheat", "maize", "cotton", ...]
}
```

#### GET `/api/get-notification/<reminder_id>`
Get specific notification details

#### GET `/api/get-encouragement/<crop_id>`
Get motivational message for farmer

#### GET `/api/get-notifications-today/<crop_id>`
Get all notifications for today

---

## Environment Variables (.env)

```env
# Gemini API Configuration
GEMINI_API_KEY=your_gemini_api_key_here
USE_CHATGPT=False

# OpenAI API Configuration (Optional)
OPENAI_API_KEY=your_openai_api_key_here

# Weather API Configuration
WEATHERAPI_KEY=your_weatherapi_key_here

# Flask Configuration
FLASK_ENV=development
FLASK_DEBUG=True
SECRET_KEY=your_secret_key_here

# Database Configuration
DATABASE_URL=sqlite:///kisansathi.db

# File Upload Configuration
MAX_CONTENT_LENGTH=16777216  # 16MB
UPLOAD_FOLDER=uploads/
```

---

## Installation & Setup

### 1. Install Dependencies
```bash
cd kisansathi/backend
pip install -r requirements.txt
```

### 2. Set Environment Variables
```bash
# Create .env file
cp .env.example .env

# Edit .env with your API keys
```

### 3. Download ML Models
```bash
# Models are pre-trained and stored in models/ folder
# Ensure all .pkl and .pth files are present
```

### 4. Run Backend Server
```bash
python app.py
```

Server will start at `http://localhost:5000`

---

## Key Features

### 1. Crop Recommendation System
- Uses RandomForest ML model (99.55% accuracy)
- Analyzes: Nitrogen, Phosphorus, Potassium, Temperature, Humidity, pH, Rainfall
- Provides seasonal recommendations
- Supports 22 different crops

### 2. Disease Detection
- Deep learning model for plant disease classification
- Supports multiple crop types
- Provides organic and chemical treatment options
- Confidence scores for predictions

### 3. AI Chatbot
- Google Gemini API integration
- Auto-language detection (Hindi/English)
- Context-aware farming advice
- Weather-based recommendations
- Supports voice input/output

### 4. Weather Integration
- Real-time weather data from Open-Meteo API
- Weather-based farming alerts
- Seasonal farming recommendations
- Temperature, humidity, wind, rainfall monitoring

### 5. Crop Lifecycle Management
- Track crop growth stages
- Automated reminders for farming tasks
- Photo-based progress tracking
- Health status monitoring

### 6. Smart Notifications
- Timely farming reminders
- Weather alerts
- Disease warnings
- Seasonal recommendations

---

## Data Models

### Crop Model
```json
{
  "crop_id": "crop_001",
  "farmer_id": "farmer_123",
  "crop_name": "rice",
  "planting_date": "2024-06-15",
  "area": 2.5,
  "soil_type": "loamy",
  "stage": "Vegetative",
  "health_status": "Good",
  "photos": [],
  "reminders": []
}
```

### Reminder Model
```json
{
  "reminder_id": "rem_001",
  "crop_id": "crop_001",
  "task": "Water the crop",
  "date": "2024-07-15",
  "time": "06:00 AM",
  "completed": false,
  "notification_sent": true
}
```

### Weather Model
```json
{
  "location": "Delhi",
  "temperature": 28.5,
  "humidity": 65,
  "wind_speed": 12,
  "rainfall": 0,
  "timestamp": "2024-04-18T10:30:00"
}
```

---

## Error Handling

### Common Error Responses

#### 400 Bad Request
```json
{
  "error": "Missing required parameters",
  "details": "N, P, K parameters are required"
}
```

#### 404 Not Found
```json
{
  "error": "Resource not found",
  "details": "Crop with ID crop_001 not found"
}
```

#### 500 Internal Server Error
```json
{
  "error": "Internal server error",
  "details": "Error processing request"
}
```

---

## Performance Optimization

1. **Model Caching** - ML models loaded once at startup
2. **Image Compression** - Images compressed before processing
3. **API Rate Limiting** - Prevent abuse
4. **Database Indexing** - Fast data retrieval
5. **Async Processing** - Background task processing

---

## Security Considerations

1. **API Key Management** - Store in .env, never commit
2. **Input Validation** - All inputs validated
3. **CORS Enabled** - Cross-origin requests allowed
4. **File Upload Security** - File type validation
5. **Rate Limiting** - Prevent API abuse

---

## Testing

### Run Tests
```bash
pytest tests/
```

### Test Coverage
```bash
pytest --cov=app tests/
```

---

## Deployment

### Production Deployment
```bash
# Use Gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app

# Or use Heroku
git push heroku main
```

### Environment Setup
- Set `FLASK_ENV=production`
- Disable debug mode
- Use strong SECRET_KEY
- Configure CORS properly

---

## Troubleshooting

### Issue: Gemini API not responding
**Solution:** Check API key in .env, verify internet connection

### Issue: ML models not loading
**Solution:** Ensure all .pkl files exist in models/ folder

### Issue: Weather API errors
**Solution:** Open-Meteo is free and doesn't require key, check internet

### Issue: Image processing slow
**Solution:** Reduce image size, use compression

---

## Future Enhancements

1. Database integration (PostgreSQL/MongoDB)
2. User authentication system
3. Mobile app backend
4. Real-time notifications (WebSocket)
5. Advanced analytics dashboard
6. Multi-language support expansion
7. IoT sensor integration
8. Blockchain for supply chain tracking

---

## Support & Contact

For issues or questions:
- GitHub: https://github.com/sumitdangi45/kisann
- Email: support@kisansathi.com

---

**Last Updated:** April 18, 2026
**Version:** 1.0.0
