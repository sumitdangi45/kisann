# 🚀 DEPLOY NOW - 30 Minute Guide

**Time**: May 2, 2026  
**Status**: ✅ READY  
**Estimated Time**: 30 minutes

---

## 🎯 Your Mission

Deploy KisanSathi to Railway.app (free tier) in 30 minutes!

---

## ⏱️ Timeline

```
00:00 - 05:00  → Railway Account Setup
05:00 - 10:00  → Project Creation
10:00 - 15:00  → Environment Variables
15:00 - 20:00  → MongoDB Setup
20:00 - 30:00  → Deployment & Testing
```

---

## 📋 Step-by-Step Guide

### **STEP 1: Railway Account (5 minutes)**

```
1. Open: https://railway.app
2. Click "Sign Up"
3. Choose "GitHub"
4. Authorize Railway
5. Done! ✅
```

**Screenshot**: You'll see Railway Dashboard

---

### **STEP 2: Create Project (5 minutes)**

```
1. Click "New Project"
2. Select "Deploy from GitHub repo"
3. Search for "kisansathi"
4. Select your repository
5. Click "Deploy"
6. Wait for build to start
```

**What happens**: Railway starts building your app

---

### **STEP 3: Add Environment Variables (5 minutes)**

In Railway Dashboard, go to **Variables** tab and add:

```
FLASK_ENV=production
PORT=5000
SECRET_KEY=your_secret_key_12345
GEMINI_API_KEY=your_gemini_key
```

**Note**: MongoDB URI will be added in Step 4

---

### **STEP 4: MongoDB Setup (5 minutes)**

#### 4a. Create MongoDB Account
```
1. Open: https://www.mongodb.com/cloud/atlas
2. Click "Sign Up"
3. Create account
4. Create M0 cluster (free)
5. Create database user
```

#### 4b. Get Connection String
```
1. Go to "Connect"
2. Choose "Connect your application"
3. Copy connection string
4. Replace <password> with your password
```

#### 4c. Add to Railway
```
1. Go back to Railway
2. Add variable: MONGODB_URI=your_connection_string
3. Save
```

**Connection String Format**:
```
mongodb+srv://username:password@cluster.mongodb.net/kisansathi?retryWrites=true&w=majority
```

---

### **STEP 5: Deploy & Test (5 minutes)**

#### 5a. Check Deployment Status
```
1. Go to Railway Dashboard
2. Look for "Deployments" tab
3. Wait for "Success" status
4. Copy your backend URL
```

#### 5b. Test Backend
```
Open in browser:
https://your-backend-url.railway.app/health

You should see: {"status": "ok"}
```

#### 5c. Test API
```
Open in browser:
https://your-backend-url.railway.app/api/months

You should see: List of months
```

---

## ✅ Verification Checklist

After deployment, verify:

- [ ] Railway Dashboard shows "Success"
- [ ] Backend URL is accessible
- [ ] `/health` endpoint returns 200
- [ ] `/api/months` returns data
- [ ] MongoDB is connected
- [ ] No errors in logs

---

## 🎉 Success!

If all checks pass, your app is live! 🚀

**Your Backend URL**: `https://your-backend-url.railway.app`

---

## 🆘 Quick Troubleshooting

| Problem | Solution |
|---------|----------|
| Build failed | Check Railway logs |
| DB not connecting | Verify MongoDB URI |
| 502 error | Check backend logs |
| Blank page | Check browser console |

---

## 📊 What's Deployed

✅ Backend API (Flask)  
✅ ML Models (Auto-loaded)  
✅ Database (MongoDB)  
✅ All Features  
✅ Bilingual Support  

---

## 🔗 Important Links

- **Railway Dashboard**: https://railway.app/dashboard
- **MongoDB Atlas**: https://cloud.mongodb.com
- **Your Backend**: https://your-backend-url.railway.app
- **Logs**: Railway Dashboard → Logs tab

---

## 💡 Pro Tips

1. **Save your URLs**: Copy backend URL for later use
2. **Monitor logs**: Check Railway logs if something breaks
3. **Test features**: Try crop recommendation, disease detection, etc.
4. **Share URL**: Share your backend URL with frontend developers

---

## 🎓 What You've Done

✅ Deployed full-stack application  
✅ Set up cloud database  
✅ Configured environment variables  
✅ Learned Railway.app basics  
✅ Got production URL  

---

## 🚀 Next Steps

1. Deploy frontend (optional)
2. Test all features
3. Monitor performance
4. Gather user feedback
5. Plan updates

---

## 📞 Need Help?

- **Railway Docs**: https://docs.railway.app
- **MongoDB Docs**: https://docs.mongodb.com
- **GitHub Issues**: Create issue in your repo

---

**Ready?** Start with STEP 1! ⏱️

**Time**: 30 minutes  
**Difficulty**: Easy  
**Result**: Live application! 🎉

