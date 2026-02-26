# ⚡ Pre-Deployment Checklist

Before you deploy to Google Cloud + Vercel, verify everything works locally.

---

## ✅ Backend Ready?

```powershell
# 1. Health check works
curl http://localhost:8000/health

# Expected response:
# {"status":"ok","environment":"development"}

# 2. API docs accessible
# Open: http://localhost:8000/docs

# 3. MongoDB connected
# Check logs for: "✓ MongoDB connection configured"
pm2 logs medcures-backend
```

---

## ✅ Frontend Ready?

```powershell
# 1. Frontend loads
# Open: http://localhost:3001
# Should see website, no errors

# 2. Can send message
# Try typing a message in the chat
# Should get response from backend

# 3. Check console (F12 → Console)
# Should show NO red errors
```

---

## ✅ Files Ready?

Check these files exist:

```
backend/
  ├── Dockerfile ✅
  ├── .dockerignore ✅
  ├── requirements.txt ✅
  ├── server.py ✅
  └── .env (has all variables) ✅

frontend/
  ├── vercel.json ✅
  ├── package.json ✅
  └── src/ (code) ✅

.gitignore ✅
.env (don't push to git!) ✅
```

---

## ✅ Environment Variables Set?

### backend/.env (for local testing)
```
MONGO_URL=mongodb+srv://...
DB_NAME=test_database
JWT_SECRET_KEY=medcures_secret_key_2026_secure_random_string_change_in_production
FOUNDER_EMAIL=medcures15@gmail.com
CORS_ORIGINS=http://localhost:3000,http://localhost:3001
OPENROUTER_API_KEY=sk-or-v1-...
```

### backend/.env.production (for deployment)
```
MONGO_URL=mongodb+srv://...  (SAME as above)
JWT_SECRET_KEY=medcures_secret_key_2026_secure_random_string_change_in_production
FOUNDER_EMAIL=medcures15@gmail.com
CORS_ORIGINS=https://your-app.vercel.app  (UPDATE this)
OPENROUTER_API_KEY=sk-or-v1-...
ENVIRONMENT=production
```

---

## ✅ Git Ready?

```powershell
# Check git status
git status

# Should show:
# - No .env files (should be .gitignore'd)
# - Backend and frontend code present
# - Dockerfile and vercel.json included

# If NOT ready:
git init
git add .
git commit -m "Initial commit"
```

---

## ✅ Accounts Created?

| Service | Created? | Link |
|---------|----------|------|
| **GitHub** | ☐ | https://github.com/signup |
| **MongoDB Atlas** | ☐ | https://mongodb.com/cloud/atlas |
| **Google Cloud** | ☐ | https://cloud.google.com/free |
| **Vercel** | ☐ | https://vercel.com/signup |

---

## ✅ Ready to Deploy?

If ALL checks pass:

1. **Push to GitHub**
   ```powershell
   git push origin main
   ```

2. **Deploy Frontend (5 min)**
   - Go to Vercel → Import Project
   - Select from GitHub
   - Deploy!

3. **Deploy Backend (10 min)**
   - Use Google Cloud Run commands
   - Point frontend to backend URL

4. **Test Live**
   - Open deployed frontend
   - Try chat feature
   - Check console for errors

---

## 🐛 Something Not Working?

### Backend endpoint 404?
- Verify server.py has `/health` endpoint ✅

### Frontend won't load?
- Check REACT_APP_BACKEND_URL set correctly ✅

### Database connection fails?
- Verify MongoDB Atlas cluster created ✅
- Check whitelist includes Google Cloud IP ✅

### Can't deploy to Google Cloud?
- Verify gcloud CLI installed ✅
- Check project ID correct ✅
- Verify APIs enabled (Cloud Run, Container Registry) ✅

---

## 💾 Save This Info

Before deploying, write down:

```
BACKEND_URL = (you'll get after deploying)
FRONTEND_URL = (you'll get after deploying)
MONGODB_CONNECTION = mongodb+srv://...
GOOGLE_PROJECT_ID = ...
```

---

**When ready, follow: DEPLOYMENT_GUIDE_FREE.md**
