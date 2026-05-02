# ✅ Deployment Checklist

## Pre-Deployment

- [x] Code cleaned up
- [x] Unused files removed
- [x] Documentation created
- [x] Git repository ready
- [x] Code pushed to GitHub

## GitHub Setup

- [ ] GitHub account created
- [ ] Repository created
- [ ] Code pushed to GitHub
- [ ] Repository is public

## Railway.app Setup

- [ ] Railway account created
- [ ] GitHub connected to Railway
- [ ] Project created in Railway
- [ ] Repository selected

## Database Setup

- [ ] MongoDB Atlas account created
- [ ] Cluster created (M0 Free)
- [ ] Connection string generated
- [ ] IP whitelist configured (0.0.0.0)

## Environment Variables

### Backend
- [ ] `MONGODB_URI` set
- [ ] `FLASK_ENV` = production
- [ ] `PORT` = 5000

### Frontend
- [ ] `VITE_API_URL` set to backend URL
- [ ] `PORT` = 3000

## Deployment

- [ ] Backend deployed
- [ ] Frontend deployed
- [ ] Deployment successful

## Testing

- [ ] Backend API responding
- [ ] Frontend loading
- [ ] Database connected
- [ ] All features working

## Post-Deployment

- [ ] Monitor logs
- [ ] Set up alerts
- [ ] Configure backups
- [ ] Document URLs

---

## Deployment URLs

**Frontend**: https://kisansathi-frontend.railway.app  
**Backend**: https://kisansathi-backend.railway.app  
**API**: https://kisansathi-backend.railway.app/api/months

---

## Quick Commands

### Push to GitHub
```bash
cd kisansathi
git push origin main
```

### Check Deployment Status
```bash
# In Railway Dashboard
# View Logs → Check for errors
```

### Test Backend
```bash
curl https://kisansathi-backend.railway.app/api/months
```

### Test Frontend
```bash
# Open in browser
https://kisansathi-frontend.railway.app
```

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Build failed | Check logs, verify dependencies |
| DB connection error | Verify MongoDB URI, check IP whitelist |
| Frontend can't reach backend | Check VITE_API_URL, verify CORS |
| Deployment stuck | Check Railway logs, restart deployment |

---

## Support

- Railway Docs: https://docs.railway.app
- MongoDB Docs: https://docs.mongodb.com
- GitHub Docs: https://docs.github.com

---

**Status**: Ready for Deployment ✅  
**Date**: May 2, 2026
