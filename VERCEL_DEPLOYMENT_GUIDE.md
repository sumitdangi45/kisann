# 🚀 Vercel + Render पर KisanSathi Deploy करने का Guide

**Frontend**: Vercel (Free)  
**Backend**: Render (Free)  
**Database**: MongoDB Atlas (Free)  
**Time**: 30 minutes  
**Cost**: FREE  

---

## ✅ क्यों Vercel + Render?

### Vercel (Frontend के लिए)
- ✅ Completely FREE
- ✅ Best for React apps
- ✅ Auto-deploy from GitHub
- ✅ Instant deployments
- ✅ Free SSL
- ✅ CDN included
- ✅ Environment variables

### Render (Backend के लिए)
- ✅ Completely FREE
- ✅ Best for APIs
- ✅ Auto-deploy from GitHub
- ✅ Free SSL
- ✅ 750 hours/month
- ✅ Easy MongoDB integration

---

## 📋 DEPLOYMENT STEPS

### **STEP 1: Render पर Backend Deploy करें** (10 minutes)

#### 1a. Render Account बनाएं
```
1. जाएं: https://render.com
2. "Sign Up" करें (GitHub से)
3. Authorization दें
```

#### 1b. New Web Service बनाएं
```
1. Dashboard में जाएं
2. "New +" → "Web Service"
3. "Connect a repository"
4. "kisansathi" select करें
5. "Connect"
```

#### 1c. Configuration करें
```
Name: kisansathi-backend
Environment: Python 3
Region: Singapore (या nearest)
Build Command: pip install -r backend/requirements.txt
Start Command: cd backend && python app_enhanced.py
```

#### 1d. Environment Variables add करें
```
FLASK_ENV=production
PORT=5000
SECRET_KEY=your_secret_key_12345
GEMINI_API_KEY=your_gemini_api_key
MONGODB_URI=your_mongodb_uri
```

#### 1e. Deploy करें
```
1. "Create Web Service" पर क्लिक करें
2. Build शुरू होगा
3. Wait करें (5-10 minutes)
4. Backend URL मिलेगा: https://kisansathi-backend.onrender.com
```

---

### **STEP 2: Vercel पर Frontend Deploy करें** (10 minutes)

#### 2a. Vercel Account बनाएं
```
1. जाएं: https://vercel.com
2. "Sign Up" करें (GitHub से)
3. Authorization दें
```

#### 2b. New Project बनाएं
```
1. Dashboard में जाएं
2. "New Project"
3. "Import Git Repository"
4. "kisansathi" select करें
5. "Import"
```

#### 2c. Configuration करें
```
Framework: Vite
Root Directory: frontend/pixel-perfect-copy
Build Command: npm run build
Output Directory: dist
```

#### 2d. Environment Variables add करें
```
VITE_API_URL=https://kisansathi-backend.onrender.com
```

#### 2e. Deploy करें
```
1. "Deploy" पर क्लिक करें
2. Build शुरू होगा
3. Wait करें (3-5 minutes)
4. Frontend URL मिलेगा: https://kisansathi-frontend.vercel.app
```

---

### **STEP 3: MongoDB Setup** (5 minutes)

#### 3a. MongoDB Atlas Account बनाएं
```
1. जाएं: https://www.mongodb.com/cloud/atlas
2. "Sign Up" करें
3. "Create a Cluster" (M0 - free)
4. "Create a Database User"
5. "Get Connection String"
```

#### 3b. Connection String Format
```
mongodb+srv://username:password@cluster.mongodb.net/kisansathi?retryWrites=true&w=majority
```

#### 3c. Render में Add करें
```
1. Render Dashboard में जाएं
2. Backend service खोलें
3. "Environment" tab
4. MONGODB_URI add करें
5. "Save" पर क्लिक करें
```

---

### **STEP 4: Verify करें** (5 minutes)

```bash
# Backend health check
curl https://kisansathi-backend.onrender.com/health

# API test
curl https://kisansathi-backend.onrender.com/api/months

# Frontend
https://kisansathi-frontend.vercel.app
```

---

## 🔗 After Deployment URLs

**Backend**: `https://kisansathi-backend.onrender.com`  
**Frontend**: `https://kisansathi-frontend.vercel.app`  
**API**: `https://kisansathi-backend.onrender.com/api/months`

---

## ✅ Verification Checklist

```
[ ] Backend URL accessible
[ ] /health endpoint returns 200
[ ] /api/months returns data
[ ] MongoDB connected
[ ] Frontend loads
[ ] API calls working
[ ] Crop recommendation works
[ ] Fertilizer recommendation works
[ ] Disease detection works
[ ] Weather forecast works
[ ] Chatbot responds
[ ] No errors in logs
```

---

## 🆘 Troubleshooting

### Backend Issues
```
Problem: Build failed
Solution: Check Render logs, verify requirements.txt

Problem: DB not connecting
Solution: Verify MongoDB URI, add IP 0.0.0.0 to whitelist

Problem: 502 error
Solution: Check backend logs, verify environment variables
```

### Frontend Issues
```
Problem: Blank page
Solution: Check browser console, verify VITE_API_URL

Problem: API calls failing
Solution: Verify backend URL, check CORS settings

Problem: Build failed
Solution: Check Vercel logs, verify build command
```

---

## 📊 Free Tier Limits

### Render
- Compute: 750 hours/month
- Bandwidth: Unlimited
- SSL: Free
- Database: MongoDB Atlas M0

### Vercel
- Deployments: Unlimited
- Bandwidth: 100GB/month
- SSL: Free
- Functions: 1000 invocations/day

### MongoDB Atlas
- Storage: 512MB
- Connections: 500
- Backup: Automatic

---

## 💡 Pro Tips

1. **Auto-Deploy**: Both platforms auto-deploy on GitHub push
2. **Logs**: Check logs in both dashboards
3. **Monitoring**: Monitor performance
4. **Scaling**: Easy to upgrade if needed
5. **Custom Domain**: Add custom domain later

---

## 🎯 Deployment Timeline

| Step | Time | Platform |
|------|------|----------|
| Render Account | 2 min | Render |
| Backend Deploy | 10 min | Render |
| Vercel Account | 2 min | Vercel |
| Frontend Deploy | 10 min | Vercel |
| MongoDB Setup | 5 min | MongoDB |
| Verification | 3 min | Both |
| **TOTAL** | **32 min** | - |

---

## 📞 Support Resources

- **Render Docs**: https://render.com/docs
- **Vercel Docs**: https://vercel.com/docs
- **MongoDB Docs**: https://docs.mongodb.com
- **GitHub Docs**: https://docs.github.com

---

## 🚀 Ready to Deploy?

Follow the steps above and your app will be live in 30 minutes!

**Questions?** Check the documentation or GitHub issues.

---

**Last Updated**: May 2, 2026  
**Status**: ✅ READY FOR DEPLOYMENT  
**Next Action**: Deploy to Render + Vercel

