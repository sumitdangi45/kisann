# KisanSathi - Quick Reference Guide

## 🚀 QUICK START

### Local Development
```bash
# Terminal 1: Backend
cd kisansathi/backend
python app_enhanced.py

# Terminal 2: Frontend
cd kisansathi/frontend/pixel-perfect-copy
npm run dev

# Open browser
http://localhost:8080
```

### Production URLs
- **Frontend:** https://kisansathi-frontend-ozq2nazkc-sumitdangi84551-6059s-projects.vercel.app/
- **Backend:** https://kisansathi-backend.onrender.com
- **Health Check:** https://kisansathi-backend.onrender.com/api/health

---

## 🔴 CURRENT ISSUE

**Backend returning 503 Service Unavailable**

### Quick Fix Steps:
1. Go to Render Dashboard
2. Select "kisansathi-backend"
3. Check "Logs" tab for errors
4. Click "Manual Deploy" to restart
5. Wait 2-3 minutes
6. Test: https://kisansathi-backend.onrender.com/api/health

---

## 📋 KEY FILES

### Frontend
- **Config:** `kisansathi/frontend/pixel-perfect-copy/vite.config.ts`
- **API Utility:** `kisansathi/frontend/pixel-perfect-copy/src/utils/api.ts`
- **Environment:** `VITE_API_URL` (set in Vercel)

### Backend
- **Main App:** `kisansathi/backend/app_enhanced.py`
- **Config:** `kisansathi/backend/.env`
- **Deployment:** `kisansathi/backend/render.yaml`

### Deployment
- **Frontend:** Vercel (auto-deploy from GitHub)
- **Backend:** Render (auto-deploy from GitHub)
- **Monitoring:** UptimeRobot (pings every 5 minutes)

---

## 🔧 COMMON TASKS

### Deploy Frontend Changes
```bash
git add .
git commit -m "Your message"
git push origin main
# Vercel auto-deploys
```

### Deploy Backend Changes
```bash
git add .
git commit -m "Your message"
git push origin main
# Render auto-deploys
```

### Check Backend Status
```bash
curl https://kisansathi-backend.onrender.com/api/health
```

### View Render Logs
1. Go to https://render.com
2. Select "kisansathi-backend"
3. Click "Logs" tab

### View Vercel Logs
1. Go to https://vercel.com
2. Select "kisansathi-frontend"
3. Click "Deployments" tab

---

## 🌐 API ENDPOINTS

### Health & Status
- `GET /api/health` - Health check
- `GET /api/status` - Application status

### Chatbot
- `POST /api/chatbot/message` - Send message to chatbot

### Crop Recommendations
- `POST /api/recommendations/crop` - Get crop recommendation
- `POST /api/recommendations/seasonal-crop` - Seasonal recommendation
- `POST /api/recommendations/advanced-crop` - Advanced recommendation

### Disease Detection
- `POST /api/disease-predict` - Detect plant disease
- `POST /api/rice-disease-predict` - Detect rice disease
- `POST /api/livestock-disease-predict` - Detect livestock disease

### Weather
- `GET /api/weather/{city}` - Get weather for city
- `GET /api/location/detect` - Detect user location

### Text-to-Speech
- `POST /api/text-to-speech` - Convert text to speech

---

## 🔑 ENVIRONMENT VARIABLES

### Vercel (Frontend)
```
VITE_API_URL=https://kisansathi-backend.onrender.com
```

### Render (Backend)
```
GEMINI_API_KEY=AIzaSyCiJHIN-wmr10w_vLVxPuf4e69wohbQ4HI
WEATHERAPI_KEY=a1c6fe1ec6ac438ea3475600261804
MONGODB_URI=mongodb+srv://kisansathi_user:Kisan2024Secure@cluster0.zlujp6r.mongodb.net/kisansathi?retryWrites=true&w=majority
MONGODB_DATABASE=kisansathi
FLASK_ENV=production
FLASK_DEBUG=False
SECRET_KEY=kisansathi_secret_key_2024
```

---

## 📊 MONITORING

### UptimeRobot
- **Email:** sumitdangi84551@gmail.com
- **Monitor:** https://kisansathi-backend.onrender.com/api/health
- **Frequency:** Every 5 minutes
- **Purpose:** Keep backend alive on free tier

### Check Status
1. Go to https://uptimerobot.com
2. Login with sumitdangi84551@gmail.com
3. Check "kisansathi-backend" monitor status

---

## 🐛 DEBUGGING

### Frontend Issues
1. Open browser DevTools (F12)
2. Check Console tab for errors
3. Check Network tab for API calls
4. Look for 503 errors from backend

### Backend Issues
1. Check Render logs
2. Look for import errors
3. Check MongoDB connection
4. Verify API keys

### API Issues
```bash
# Test health endpoint
curl https://kisansathi-backend.onrender.com/api/health

# Test chatbot
curl -X POST https://kisansathi-backend.onrender.com/api/chatbot/message \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello", "conversation_history": []}'
```

---

## 📱 TESTING

### Test Chatbot
1. Open frontend
2. Click "Chatbot" or find chat icon
3. Type a message
4. Should get response

### Test Crop Recommendation
1. Go to "Crop Recommendations" page
2. Fill in soil parameters
3. Click "Get Recommendations"
4. Should see crop suggestions

### Test Disease Detection
1. Go to "Disease Detection" page
2. Upload an image
3. Click "Predict"
4. Should see disease prediction

---

## 🎯 NEXT STEPS

### Immediate (Today)
- [ ] Check Render logs for backend errors
- [ ] Verify backend health endpoint
- [ ] Restart backend if needed
- [ ] Test API endpoints

### Short-term (This Week)
- [ ] Test all features end-to-end
- [ ] Monitor performance
- [ ] Fix any bugs found
- [ ] Optimize if needed

### Long-term (Future)
- [ ] Add more features
- [ ] Improve UI/UX
- [ ] Scale infrastructure
- [ ] Add more languages

---

## 📞 SUPPORT

### Documentation
- **Troubleshooting:** See `TROUBLESHOOTING_GUIDE.md`
- **Deployment:** See `DEPLOYMENT_STATUS.md`
- **System Check:** See `FINAL_SYSTEM_CHECK.txt`

### External Resources
- **Render Docs:** https://render.com/docs
- **Vercel Docs:** https://vercel.com/docs
- **MongoDB Docs:** https://www.mongodb.com/docs
- **Gemini API:** https://ai.google.dev/docs

---

## ✨ FEATURES

✅ Crop Recommendations (Manual, Voice, Seasonal)
✅ Disease Detection (Plant, Rice, Livestock)
✅ Weather Integration
✅ Chatbot with AI
✅ Voice Assistant
✅ Text-to-Speech
✅ Smart Reminders
✅ Community Features
✅ Livestock Management
✅ Fertilizer Recommendations

---

**Last Updated:** May 9, 2026
**Status:** Production Ready (Pending Backend Verification)
