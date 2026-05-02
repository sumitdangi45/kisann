# 🌾 KisanSathi - Agricultural Advisory System

A comprehensive agricultural advisory platform providing crop recommendations, fertilizer suggestions, disease detection, and weather forecasting for Indian farmers.

## ✨ Features

### 🌱 Crop Recommendation
- **Manual Input**: Enter soil parameters for personalized recommendations
- **By Location & Season**: Get recommendations based on your region and month
- **Per Month**: Consistent month-based crop suggestions
- **Voice Input**: Speak your soil parameters

### 🧪 Fertilizer Recommendation
- **Manual Input**: Get fertilizer suggestions based on soil nutrients
- **Crop Image Analysis**: Upload crop images for health-based recommendations
  - Detects crop health status (Healthy/Stressed/Diseased)
  - Estimates crop size and growth stage
  - Provides customized fertilizer recommendations

### 🏥 Disease Detection
- Plant disease identification from images
- Pest management recommendations
- Treatment suggestions

### 🌤️ Weather Forecasting
- Current weather information
- 7-day forecast
- Location-based weather alerts

### 📚 Resources
- Agricultural guides and books
- PDF downloads
- Best practices

### 🤖 AI Chatbot
- Unified chatbot for all queries
- Hindi and English support
- Voice interaction

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Node.js 16+
- MongoDB
- Git

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/kisansathi.git
cd kisansathi
```

2. **Backend Setup**
```bash
cd backend
pip install -r requirements.txt
python app_enhanced.py
```

3. **Frontend Setup**
```bash
cd frontend/pixel-perfect-copy
npm install
npm run dev
```

4. **Access the application**
- Frontend: http://localhost:8080
- Backend API: http://localhost:5000

## 📁 Project Structure

```
kisansathi/
├── backend/
│   ├── app_enhanced.py          # Main Flask application
│   ├── requirements.txt          # Python dependencies
│   ├── models/                   # ML models
│   ├── utils/                    # Utility functions
│   └── Data/                     # Data files
├── frontend/
│   └── pixel-perfect-copy/       # React application
│       ├── src/
│       ├── public/
│       └── package.json
├── docker-compose.yml            # Docker configuration
└── README.md                      # This file
```

## 🔧 Configuration

### Environment Variables

Create `.env` file in backend directory:

```
MONGODB_URI=mongodb+srv://user:password@cluster.mongodb.net/kisansathi
FLASK_ENV=production
PORT=5000
GEMINI_API_KEY=your_gemini_api_key
```

## 🐳 Docker Deployment

```bash
docker-compose up -d
```

## 📦 Deployment

### Railway.app (Recommended)
1. Push code to GitHub
2. Connect GitHub to Railway
3. Set environment variables
4. Deploy

### AWS / Google Cloud / Heroku
See deployment guides in documentation

## 🧪 Testing

### Backend Tests
```bash
cd backend
python -m pytest
```

### Frontend Tests
```bash
cd frontend/pixel-perfect-copy
npm test
```

## 📖 API Documentation

### Crop Recommendation
- `POST /api/recommendations/crop` - Manual crop recommendation
- `POST /api/recommendations/advanced-crop` - Location & season based
- `GET /api/months` - Get available months

### Fertilizer Recommendation
- `POST /api/fertilizer/recommend` - Manual fertilizer recommendation
- `POST /api/fertilizer-from-image` - Image-based fertilizer recommendation

### Disease Detection
- `POST /api/disease/detect` - Detect plant diseases
- `POST /api/disease/livestock` - Detect livestock diseases

### Weather
- `GET /api/weather/current` - Current weather
- `GET /api/weather/forecast` - Weather forecast

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see LICENSE file for details.

## 👥 Team

- **Developer**: Kiro AI
- **Project**: KisanSathi Agricultural Advisory System

## 📞 Support

For issues and questions:
- GitHub Issues: [Create an issue](https://github.com/yourusername/kisansathi/issues)
- Email: support@kisansathi.com

## 🙏 Acknowledgments

- MongoDB for database
- Google Gemini for AI
- Flask for backend framework
- React for frontend framework
- Railway for deployment platform

---

**Status**: ✅ Production Ready  
**Last Updated**: May 2, 2026  
**Version**: 1.0.0
