# 🚀 Render.com पर KisanSathi Deploy करने का Guide

**Platform**: Render.com (Free)  
**Time**: 30 minutes  
**Cost**: FREE  
**Difficulty**: EASY  

---

## ✅ Render.com क्यों?

- ✅ Completely FREE
- ✅ No credit card required
- ✅ Auto-deploy from GitHub
- ✅ Free SSL certificate
- ✅ 750 hours/month free
- ✅ MongoDB integration easy
- ✅ Environment variables support
- ✅ Logs और monitoring

---

## 📋 Render.com पर Deploy करने के Steps

### **Step 1: Render Account बनाएं** (2 minutes)

```
1. जाएं: https://render.com
2. "Sign Up" पर क्लिक करें
3. GitHub से login करें
4. Authorization दें
5. Done! ✅
```

### **Step 2: Backend Deploy करें** (10 minutes)

#### 2a. New Web Service बनाएं
```
1. Dashboard में जाएं
2. "New +" पर क्लिक करें
3. "Web Service" चुनें
4. "Connect a repository" पर क्लिक करें
5. अपना "kisansathi" repository select करें
6. "Connect" पर क्लिक करें
```

#### 2b. Configuration करें
```
Name: kisansathi-backend
Environment: Python 3
Build Command: pip install -r backend/requirements.txt
Start Command: cd backend && python app_enhanced.py
```

#### 2c. Environment Variables add करें
```
FLASK_ENV=production
PORT=5000
SECRET_KEY=your_secret_key_here
GEMINI_API_KEY=your_gemini_api_key
MONGODB_URI=your_mongodb_connection_string
```

#### 2d. Deploy करें
```
1. "Create Web Service" पर क्लिक करें
2. Build शुरू होगा
3. Wait करें (5-10 minutes)
4. Done! ✅
```

### **Step 3: Frontend Deploy करें** (10 minutes)

#### 3a. New Static Site बनाएं
```
1. Dashboard में जाएं
2. "New +" पर क्लिक करें
3. "Static Site" चुनें
4. "Connect a repository" पर क्लिक करें
5. अपना "kisansathi" repository select करें
6. "Connect" पर क्लिक करें
```

#### 3b. Configuration करें
```
Name: kisansathi-frontend
Root Directory: frontend/pixel-perfect-copy
Build Command: npm install && npm run build
Publish Directory: dist
```

#### 3c. Environment Variables add करें
```
VITE_API_URL=https://kisansathi-backend.onrender.com
```

#### 3d. Deploy करें
```
1. "Create Static Site" पर क्लिक करें
2. Build शुरू होगा
3. Wait करें (3-5 minutes)
4. Done! ✅
```

### **Step 4: MongoDB Setup** (5 minutes)

#### 4a. MongoDB Atlas Account बनाएं
```
1. जाएं: https://www.mongodb.com/cloud/atlas
2. "Sign Up" करें
3. "Create a Cluster" (M0 - free)
4. "Create a Database User"
5. "Get Connection String"
```

#### 4b. Connection String Format
```
mongodb+srv://username:password@cluster.mongodb.net/kisansathi?retryWrites=true&w=majority
```

#### 4c. Render में Add करें
```
1. Backend service में जाएं
2. "Environment" tab खोलें
3. MONGODB_URI add करें
4. "Save" पर क्लिक करें
5. Service auto-restart होगी
```

### **Step 5: Verify करें** (3 minutes)

```bash
# Backend health check
curl https://kisansathi-backend.onrender.com/health

# API test
curl https://kisansathi-backend.onrender.com/api/months

# Frontend
https://kisansathi-frontend.onrender.com
```

---

## 🔗 After Deployment URLs

**Backend**: `https://kisansathi-backend.onrender.com`  
**Frontend**: `https://kisansathi-frontend.onrender.com`  
**API**: `https://kisansathi-backend.onrender.com/api/months`

---

## ✅ Verification Checklist

Deploy होने के बाद verify करें:

```
✅ Backend URL accessible
✅ /health endpoint returns 200
✅ /api/months returns data
✅ /api/crops returns data
✅ /api/fertilizers returns data
✅ MongoDB connected
✅ Frontend loads
✅ API calls working
✅ No errors in logs
```

---

## 🆘 Troubleshooting

| Problem | Solution |
|---------|----------|
| Build failed | Check Render logs |
| DB not connecting | Verify MongoDB URI |
| 502 error | Check backend logs |
| Frontend blank | Check browser console |
| Models not loading | Wait 5 minutes, check logs |

---

## 📊 Render Free Tier

- **Compute**: 750 hours/month (free)
- **Bandwidth**: Unlimited
- **SSL**: Free
- **Database**: MongoDB Atlas M0 (free)
- **Storage**: 512MB (MongoDB)

---

## 💡 Pro Tips

1. **Auto-Deploy**: Render automatically deploys on GitHub push
2. **Logs**: Check logs in Render dashboard
3. **Monitoring**: Monitor performance in dashboard
4. **Scaling**: Easy to upgrade if needed

---

## 🎯 Deployment Timeline

| Step | Time | Status |
|------|------|--------|
| Render Account | 2 min | ⏳ TODO |
| Backend Deploy | 10 min | ⏳ TODO |
| Frontend Deploy | 10 min | ⏳ TODO |
| MongoDB Setup | 5 min | ⏳ TODO |
| Verification | 3 min | ⏳ TODO |
| **TOTAL** | **30 min** | ⏳ TODO |

---

## 📞 Support

- **Render Docs**: https://render.com/docs
- **MongoDB Docs**: https://docs.mongodb.com
- **GitHub Docs**: https://docs.github.com

---

## 🚀 Ready to Deploy?

Follow the steps above and your app will be live in 30 minutes!

**Questions?** Check Render documentation or GitHub issues.

---

**Last Updated**: May 2, 2026  
**Status**: ✅ READY FOR DEPLOYMENT  
**Next Action**: Deploy to Render.com

