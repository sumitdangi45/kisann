# KisanSathi Troubleshooting & Action Plan

## 🔴 Current Issue: Backend 503 Service Unavailable

### What We Know
- Frontend is deployed on Vercel ✅
- Backend is deployed on Render ⚠️
- UptimeRobot is monitoring the backend ✅
- All hardcoded URLs have been fixed ✅
- Environment variables are configured ✅

### Why Backend Might Be Returning 503

**Possible Causes:**
1. **Render Free Tier Sleep** - Backend goes to sleep after 15 minutes of inactivity
   - Solution: UptimeRobot should be pinging it every 5 minutes
   - Check: Verify UptimeRobot is actually working

2. **Import Errors** - Missing dependencies or failed imports
   - Solution: Check Render deployment logs
   - Check: Look for import errors in app_enhanced.py

3. **MongoDB Connection Failed** - Cannot connect to MongoDB Atlas
   - Solution: Verify MONGODB_URI is correct
   - Check: Test connection string in Render environment

4. **Gemini API Key Invalid** - API key is wrong or expired
   - Solution: Verify API key in .env
   - Check: Test API key directly

5. **Missing Dependencies** - requirements.txt not installed
   - Solution: Check Render build logs
   - Check: Verify all packages are listed in requirements.txt

6. **Port Configuration** - Backend not listening on correct port
   - Solution: Check render.yaml startCommand
   - Check: Verify PORT environment variable

---

## 🔧 STEP-BY-STEP TROUBLESHOOTING

### Step 1: Check Render Deployment Logs
**Action:** Go to Render Dashboard → Select kisansathi-backend → Logs

**What to Look For:**
- Build errors (missing packages)
- Runtime errors (import failures)
- Connection errors (MongoDB, Redis)
- Port binding errors

**Common Error Patterns:**
```
ModuleNotFoundError: No module named 'xxx'
→ Missing dependency in requirements.txt

ConnectionError: Cannot connect to MongoDB
→ MONGODB_URI is wrong or network issue

ImportError: cannot import name 'xxx'
→ Circular import or missing module
```

### Step 2: Test Backend Health Endpoint
**Action:** Open in browser or curl:
```
https://kisansathi-backend.onrender.com/api/health
```

**Expected Response:**
```json
{
  "status": "healthy",
  "timestamp": "2026-05-09T...",
  "database": "MongoDB",
  "version": "4.0.0"
}
```

**If 503 Error:**
- Backend is not running
- Go to Step 1 (check logs)

**If Timeout:**
- Backend is sleeping
- Trigger UptimeRobot ping manually
- Wait 30 seconds and try again

### Step 3: Verify Environment Variables on Render
**Action:** Render Dashboard → kisansathi-backend → Environment

**Required Variables:**
```
GEMINI_API_KEY=AIzaSyCiJHIN-wmr10w_vLVxPuf4e69wohbQ4HI
WEATHERAPI_KEY=a1c6fe1ec6ac438ea3475600261804
MONGODB_URI=mongodb+srv://kisansathi_user:Kisan2024Secure@cluster0.zlujp6r.mongodb.net/kisansathi?retryWrites=true&w=majority
MONGODB_DATABASE=kisansathi
FLASK_ENV=production
FLASK_DEBUG=False
SECRET_KEY=kisansathi_secret_key_2024
```

**If Missing:**
- Add the missing variables
- Click "Deploy" to restart with new variables

### Step 4: Check UptimeRobot Configuration
**Action:** Go to UptimeRobot Dashboard (sumitdangi84551@gmail.com)

**Verify:**
- Monitor is "Active"
- URL: `https://kisansathi-backend.onrender.com/api/health`
- Interval: 5 minutes
- Status: Should show "Up" (green)

**If Status is "Down":**
- Click "Check Now" to manually trigger
- Wait 30 seconds
- Refresh page

**If Still Down:**
- Backend is actually down
- Go to Step 1 (check Render logs)

### Step 5: Manual Backend Restart
**Action:** Render Dashboard → kisansathi-backend → Manual Deploy

**Steps:**
1. Click "Manual Deploy"
2. Select "Deploy latest commit"
3. Wait for deployment to complete (2-3 minutes)
4. Check logs for errors
5. Test health endpoint again

### Step 6: Test API Endpoints
**Action:** Once health endpoint works, test other endpoints

**Test Chatbot:**
```bash
curl -X POST https://kisansathi-backend.onrender.com/api/chatbot/message \
  -H "Content-Type: application/json" \
  -d '{"message": "नमस्ते", "conversation_history": []}'
```

**Test Crop Recommendation:**
```bash
curl -X POST https://kisansathi-backend.onrender.com/api/recommendations/crop \
  -H "Content-Type: application/json" \
  -d '{
    "N": 90,
    "P": 42,
    "K": 43,
    "temperature": 20,
    "humidity": 82,
    "ph": 6.5,
    "rainfall": 202
  }'
```

---

## 🚀 QUICK FIX CHECKLIST

- [ ] Check Render deployment logs for errors
- [ ] Verify all environment variables are set on Render
- [ ] Test health endpoint: `https://kisansathi-backend.onrender.com/api/health`
- [ ] Verify UptimeRobot is active and monitoring
- [ ] Manually restart backend on Render if needed
- [ ] Test chatbot endpoint
- [ ] Test crop recommendation endpoint
- [ ] Verify Vercel frontend can reach backend
- [ ] Test full app flow in browser

---

## 📱 TESTING THE FULL APP

### Local Testing (Before Production)
```bash
# Terminal 1: Start Backend
cd kisansathi/backend
python app_enhanced.py

# Terminal 2: Start Frontend
cd kisansathi/frontend/pixel-perfect-copy
npm run dev

# Open browser
http://localhost:8080
```

### Production Testing
1. Open: `https://kisansathi-frontend-ozq2nazkc-sumitdangi84551-6059s-projects.vercel.app/`
2. Test Chatbot:
   - Type a message
   - Should get response from backend
3. Test Crop Recommendation:
   - Fill in soil parameters
   - Should get crop recommendations
4. Test Disease Detection:
   - Upload an image
   - Should get disease prediction
5. Test Weather:
   - Should show weather for detected location

---

## 🔍 DEBUGGING TIPS

### Enable Verbose Logging
**File:** `kisansathi/backend/app_enhanced.py`
```python
logging.basicConfig(level=logging.DEBUG)  # Change from INFO to DEBUG
```

### Check MongoDB Connection
```python
# In Python shell
from pymongo import MongoClient
client = MongoClient('mongodb+srv://kisansathi_user:Kisan2024Secure@cluster0.zlujp6r.mongodb.net/kisansathi?retryWrites=true&w=majority')
db = client['kisansathi']
print(db.list_collection_names())  # Should list collections
```

### Test Gemini API Key
```python
import google.generativeai as genai
genai.configure(api_key='AIzaSyCiJHIN-wmr10w_vLVxPuf4e69wohbQ4HI')
model = genai.GenerativeModel('gemini-2.5-flash')
response = model.generate_content("Hello")
print(response.text)
```

### Check Frontend API Configuration
**File:** `kisansathi/frontend/pixel-perfect-copy/src/utils/api.ts`
```typescript
const API_BASE_URL = import.meta.env.VITE_API_URL 
  ? `${import.meta.env.VITE_API_URL}/api`
  : "/api";
console.log('API Base URL:', API_BASE_URL);  // Add this to debug
```

---

## 📞 SUPPORT RESOURCES

### Render Documentation
- Deployment Logs: https://render.com/docs/deploy-logs
- Environment Variables: https://render.com/docs/environment-variables
- Free Tier Limits: https://render.com/docs/free

### Vercel Documentation
- Environment Variables: https://vercel.com/docs/concepts/projects/environment-variables
- Deployment: https://vercel.com/docs/concepts/deployments/overview

### MongoDB Atlas
- Connection String: https://www.mongodb.com/docs/atlas/driver-connection
- Network Access: https://www.mongodb.com/docs/atlas/security/ip-access-list/

### Gemini API
- Documentation: https://ai.google.dev/docs
- API Keys: https://aistudio.google.com/app/apikey

---

## 🎯 SUCCESS CRITERIA

✅ Backend health endpoint returns 200 OK
✅ Chatbot responds to messages
✅ Crop recommendations work
✅ Disease detection works
✅ Frontend loads without errors
✅ All API calls complete in < 2 seconds
✅ UptimeRobot shows "Up" status

---

**Last Updated:** May 9, 2026
**Status:** Troubleshooting in Progress
