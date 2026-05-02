# 🚀 Railway.app पर KisanSathi Deploy करने का Guide

## ✅ Status
- ✅ Code GitHub पर है (models को छोड़कर)
- ✅ Backend तैयार है
- ✅ Frontend तैयार है
- ✅ Database configuration तैयार है

---

## 📋 Railway.app पर Deploy करने के Steps

### **Step 1: Railway.app Account बनाएं** (2 minutes)
1. जाएं: https://railway.app
2. "Sign Up" पर क्लिक करें
3. GitHub से login करें
4. Authorization दें

### **Step 2: New Project बनाएं** (3 minutes)
1. Railway Dashboard में जाएं
2. "New Project" पर क्लिक करें
3. "Deploy from GitHub repo" चुनें
4. अपना `kisansathi` repository select करें
5. "Deploy" पर क्लिक करें

### **Step 3: Environment Variables सेट करें** (5 minutes)

Railway Dashboard में जाएं और ये variables add करें:

```
# Backend Variables
FLASK_ENV=production
PORT=5000
MONGODB_URI=your_mongodb_connection_string
REDIS_URL=redis://default:password@redis-host:6379
SECRET_KEY=your_secret_key_here
GEMINI_API_KEY=your_gemini_api_key

# Frontend Variables (अगर अलग deploy करें)
VITE_API_URL=https://your-backend-url.railway.app
```

### **Step 4: MongoDB Atlas Setup** (5 minutes)

1. जाएं: https://www.mongodb.com/cloud/atlas
2. "Sign Up" करें (free account)
3. "Create a Cluster" (M0 - free tier)
4. "Create a Database User"
5. "Get Connection String"
6. Connection string को Railway के `MONGODB_URI` में paste करें

**Connection String Format:**
```
mongodb+srv://username:password@cluster.mongodb.net/kisansathi?retryWrites=true&w=majority
```

### **Step 5: Procfile Check करें** (1 minute)

Root directory में `Procfile` होनी चाहिए:

```
web: cd backend && python app_enhanced.py
```

### **Step 6: Deploy होने दें** (10 minutes)

Railway automatically:
- ✅ Code को pull करेगा
- ✅ Dependencies install करेगा
- ✅ Application start करेगा
- ✅ URL generate करेगा

---

## 🔗 After Deployment URLs

**Backend URL**: `https://kisansathi-backend.railway.app`  
**Frontend URL**: `https://kisansathi-frontend.railway.app` (अगर अलग deploy करें)

---

## ✅ Verification Checklist

Deploy होने के बाद verify करें:

```bash
# Backend health check
curl https://kisansathi-backend.railway.app/health

# API test
curl https://kisansathi-backend.railway.app/api/months

# Crop recommendation test
curl -X POST https://kisansathi-backend.railway.app/api/recommendations/crop \
  -H "Content-Type: application/json" \
  -d '{"N":90,"P":42,"K":43,"temperature":20,"humidity":82,"ph":6.5,"rainfall":200}'
```

---

## 🆘 Troubleshooting

| Problem | Solution |
|---------|----------|
| Build failed | Check Railway logs, verify Procfile |
| DB not connecting | Verify MongoDB URI, add IP 0.0.0.0 to whitelist |
| Models not loading | Models download automatically on first run |
| Frontend blank | Check browser console, verify VITE_API_URL |
| API 502 error | Check backend logs in Railway |

---

## 📊 Railway Free Tier Limits

- **Compute**: 500 hours/month (free)
- **Database**: MongoDB Atlas M0 (free)
- **Bandwidth**: Unlimited
- **Storage**: 512MB (MongoDB)

---

## 🎯 Next Steps

1. ✅ Deploy backend
2. ✅ Deploy frontend (या same project में)
3. ✅ Test all features
4. ✅ Monitor logs
5. ✅ Set up alerts

---

## 📞 Railway Support

- **Docs**: https://docs.railway.app
- **Status**: https://status.railway.app
- **Discord**: https://discord.gg/railway

---

**Ready to deploy?** Follow the steps above! 🚀

