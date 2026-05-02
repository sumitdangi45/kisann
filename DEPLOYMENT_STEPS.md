# 🚀 Deployment Steps - Railway.app

## Step 1: GitHub Setup

### 1.1 Create GitHub Account (if not exists)
- Go to https://github.com/signup
- Create account with email

### 1.2 Create Repository
- Go to https://github.com/new
- Repository name: `kisansathi`
- Description: "KisanSathi - Agricultural Advisory System"
- Make it Public
- Click "Create repository"

### 1.3 Push Code to GitHub
```bash
cd kisansathi
git remote set-url origin https://github.com/YOUR_USERNAME/kisansathi.git
git push -u origin main
```

Replace `YOUR_USERNAME` with your GitHub username.

---

## Step 2: Railway.app Setup

### 2.1 Create Railway Account
- Go to https://railway.app
- Click "Sign up"
- Sign up with GitHub (easiest)
- Authorize Railway to access your GitHub

### 2.2 Create New Project
- Click "New Project"
- Select "Deploy from GitHub repo"
- Select your `kisansathi` repository
- Click "Deploy"

---

## Step 3: Configure Environment Variables

In Railway Dashboard:

### 3.1 Backend Service Variables
```
MONGODB_URI=mongodb+srv://user:password@cluster.mongodb.net/kisansathi
FLASK_ENV=production
PORT=5000
```

### 3.2 Frontend Service Variables
```
VITE_API_URL=https://your-backend-url.railway.app
PORT=3000
```

---

## Step 4: Database Setup (MongoDB Atlas)

### 4.1 Create MongoDB Account
- Go to https://www.mongodb.com/cloud/atlas
- Click "Sign up"
- Create account

### 4.2 Create Cluster
- Click "Create a Deployment"
- Choose "M0 Free" tier
- Select region (India recommended)
- Click "Create Deployment"

### 4.3 Get Connection String
- Click "Connect"
- Choose "Drivers"
- Copy connection string
- Replace `<password>` with your password
- Paste in Railway `MONGODB_URI`

---

## Step 5: Deploy

### 5.1 Automatic Deployment
- Railway automatically deploys when you push to GitHub
- Check deployment status in Railway Dashboard

### 5.2 Manual Deployment
- In Railway Dashboard
- Click "Deploy" button
- Wait for deployment to complete

---

## Step 6: Verify Deployment

### 6.1 Check Backend
```
https://your-backend-url.railway.app/api/months
```

Should return list of months.

### 6.2 Check Frontend
```
https://your-frontend-url.railway.app
```

Should load the application.

---

## Troubleshooting

### Build Failed
- Check Railway logs
- Ensure all dependencies are in requirements.txt
- Check for syntax errors

### Database Connection Error
- Verify MongoDB URI is correct
- Check IP whitelist in MongoDB Atlas (add 0.0.0.0)
- Verify password doesn't have special characters

### Frontend Can't Connect to Backend
- Check VITE_API_URL is correct
- Ensure backend is running
- Check CORS is enabled in backend

---

## URLs After Deployment

- **Frontend**: `https://kisansathi-frontend.railway.app`
- **Backend**: `https://kisansathi-backend.railway.app`
- **API Docs**: `https://kisansathi-backend.railway.app/api/months`

---

## Next Steps

1. Test all features
2. Set up custom domain (optional)
3. Configure monitoring
4. Set up backups

---

**Status**: Ready for Deployment ✅
