# 🚀 FREE Deployment Guide: Google Cloud + Vercel

## 📋 Final Checklist Before Deploying

- ✅ Backend running locally: http://localhost:8000
- ✅ Frontend running locally: http://localhost:3001
- ✅ Health check working: http://localhost:8000/health
- ✅ MongoDB Atlas account (free tier)
- ✅ GitHub account (to connect to Vercel)

---

## 💰 What's FREE

| Service | Free Tier | Cost |
|---------|-----------|------|
| **Google Cloud Run** | 2M requests/month | 🆓 FREE |
| **Vercel** | Unlimited deployments | 🆓 FREE |
| **MongoDB Atlas** | 512MB database | 🆓 FREE |
| **Custom Domain** | Optional | $$ (5-15/year) |

**Total Cost: $0 unless you add a custom domain**

---

## STEP 1: GitHub Setup (Required for Vercel)

### 1.1 Create GitHub Account
1. Go to https://github.com/signup
2. Create account with email
3. Verify email

### 1.2 Push Your Code to GitHub

```powershell
# In your project root directory
git init
git add .
git commit -m "Initial commit - ready for production"
git branch -M main

# Create new repo at https://github.com/new
# Then push (replace YOUR_USERNAME and YOUR_REPO):
git remote add origin https://github.com/YOUR_USERNAME/medcures.git
git push -u origin main
```

**Don't have Git?** Install from https://git-scm.com/

---

## STEP 2: Deploy Frontend to Vercel (5 minutes)

### 2.1 Create Vercel Account
1. Go to https://vercel.com
2. Click "Sign Up"
3. Choose "GitHub" option
4. Authorize Vercel to access GitHub
5. Confirm email

### 2.2 Deploy Frontend
1. In Vercel dashboard, click "Add New..." → "Project"
2. Select your GitHub repository
3. **Framework**: Select "Create React App"
4. **Build Command**: Leave as is (npm run build)
5. Click "Deploy"
6. Wait for deployment ✅

**Your frontend is now live at a Vercel URL!** (something like `medcures.vercel.app`)

### 2.3 Configure Environment Variable
After deployment:
1. Go to your Vercel project → Settings
2. Click "Environment Variables"
3. Add: 
   - **Name**: `REACT_APP_BACKEND_URL`
   - **Value**: (you'll get this after deploying backend)
4. Redeploy: Click "Deployments" → Latest → "Redeploy"

---

## STEP 3: Deploy Backend to Google Cloud (15 minutes)

### 3.1 Create Google Cloud Account
1. Go to https://cloud.google.com/free
2. Click "Get started for free"
3. Sign in with Gmail or create new account
4. Add billing info (required but won't charge for free tier)
5. Create a new project:
   - Project name: "medcures"
   - Click "Create"

### 3.2 Enable Required Services
1. Go to Google Cloud Console
2. Search for "Cloud Run" → Click it
3. Click "Enable" (this enables the API)
4. Go back and search for "Container Registry" → Enable it
5. Search for "Secret Manager" → Enable it

### 3.3 Deploy Backend Using Command Line

#### Install Google Cloud SDK
```powershell
# Download from: https://cloud.google.com/sdk/docs/install
# Run installer and follow steps
```

#### Login to Google Cloud
```powershell
gcloud auth login
gcloud config set project YOUR_PROJECT_ID
# (Find PROJECT_ID in Google Cloud Console top)
```

#### Create Secret for Environment Variables
```powershell
# Create secret file
$content = @"
MONGO_URL=mongodb+srv://USERNAME:PASSWORD@cluster.mongodb.net/DATABASE?retryWrites=true
FOUNDER_EMAIL=your_email@gmail.com
JWT_SECRET_KEY=GENERATE_A_RANDOM_STRING_32_CHARS_MINIMUM
OPENROUTER_API_KEY=your_api_key_if_you_have_one
CORS_ORIGINS=https://your-frontend.vercel.app
ENVIRONMENT=production
"@
$content | Out-File -FilePath backend/.env.production -Encoding UTF8
```

#### Deploy to Cloud Run
```powershell
cd backend

# Build and push
gcloud run deploy medcures-backend `
  --source . `
  --platform managed `
  --region us-central1 `
  --allow-unauthenticated `
  --memory 512Mi `
  --cpu 1 `
  --env-vars FROM-FILE=.env.production

# Wait for deployment to complete
```

**Your backend is now live at:** `https://medcures-backend-XXXXX.a.run.app`

---

## STEP 4: Connect Frontend to Backend

### 4.1 Update Vercel Environment Variable
1. Go to Vercel Dashboard
2. Select your project → Settings → Environment Variables
3. Update `REACT_APP_BACKEND_URL` with backend URL from Google Cloud
4. Click "Redeploy" on latest deployment

### 4.2 Test the Connection
1. Go to your Vercel frontend URL
2. Try sending a message in chat
3. Check if response comes back
4. Open browser console (F12) - should show no errors

---

## STEP 5: MongoDB Atlas (Already Done?)

If you haven't set up MongoDB yet:

### 5.1 Create Free Account
1. Go to https://www.mongodb.com/cloud/atlas
2. Click "Sign Up"
3. Create account
4. Verify email

### 5.2 Create Free Cluster
1. Click "Create a Deployment"
2. Select "Free" tier
3. Select region closest to you
4. Click "Create"
5. Wait 5-10 minutes

### 5.3 Get Connection String
1. Click "Connect" on your cluster
2. Select "Drivers"
3. Choose Python 3.9+
4. Copy connection string
5. Replace `USERNAME`, `PASSWORD`, `DATABASE`:
   ```
   mongodb+srv://USERNAME:PASSWORD@cluster.mongodb.net/DATABASE?retryWrites=true
   ```

### 5.4 Update Backend Secret
```powershell
# Update in Google Cloud Secret Manager
# Or redeploy with updated .env.production
```

---

## ✅ Verify Everything Works

### Test Checklist
- [ ] Frontend loads: Visit `https://your-app.vercel.app`
- [ ] API responds: Visit `https://backend-url.a.run.app/health`
- [ ] Chat works: Send message in frontend, see response
- [ ] No console errors: Open DevTools (F12) → Console tab
- [ ] Mobile friendly: Test on phone/tablet

---

## 📊 Monitor Your Deployment

### Google Cloud Console
- View logs: Cloud Run → medcures-backend → Logs
- Check usage: Billing → Overview
- Monitor errors: Cloud Run → Metrics

### Vercel Dashboard
- View logs: Deployments → Click deployment
- Check analytics: Analytics tab
- Monitor usage: Usage section

---

## 🔄 Update Your App After Deployment

### Update Frontend
```powershell
# Make changes in frontend folder
git add .
git commit -m "Update frontend"
git push

# Vercel auto-deploys on push!
# Check dashboard - it auto-redeploys
```

### Update Backend
```powershell
# Make changes in backend folder
cd backend
git add .
git commit -m "Update backend"
git push

# Redeploy manually:
gcloud run deploy medcures-backend --source . --platform managed --region us-central1 --allow-unauthenticated
```

---

## 💡 Cost Optimization

To keep everything FREE:

✅ Use free tiers only  
✅ Monitor API calls (stay under limits)  
✅ Set up budget alerts in Google Cloud  
✅ Archive old data in MongoDB  
✅ Don't use custom domain (saves $)

---

## 🆘 Troubleshooting

### Frontend shows error/won't load
- Check Vercel deployment logs
- Clear browser cache (Ctrl+Shift+Del)
- Check REACT_APP_BACKEND_URL is correct

### Backend returns 503 error
- Check Google Cloud logs
- Verify MongoDB connection string
- Check all environment variables set

### MongoDB connection fails
- Verify username/password correct
- Check IP whitelist in MongoDB Atlas → Network Access
- Add your Google Cloud IP to whitelist

### Health check fails
- Run locally first: `python backend/server.py`
- Check all dependencies in requirements.txt
- Verify .env.production has all variables

---

## 📞 Support Resources

- **Vercel Docs**: https://vercel.com/docs
- **Google Cloud Run**: https://cloud.google.com/run/docs
- **MongoDB**: https://docs.mongodb.com/atlas
- **FastAPI**: https://fastapi.tiangolo.com

---

## 🎉 You Did It!

Your app is now:
- ✅ Running 24/7 on Google Cloud
- ✅ Fast globally with Vercel CDN
- ✅ Completely FREE
- ✅ Production-ready
- ✅ Auto-scaling

**Congratulations!** 🚀
