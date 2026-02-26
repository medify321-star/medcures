# 🚀 QUICK REFERENCE CARD

## Free Deployment: Google Cloud + Vercel

**Total Time: 30 minutes**
**Total Cost: $0**

---

## 📝 You'll Need

- [ ] Gmail/Google account
- [ ] GitHub account (will create)
- [ ] Credit card for Google Cloud (won't charge - free tier)

---

## 🎯 The 9 Steps

| Step | What | Time | ✅ |
|------|------|------|---|
| 1 | Create GitHub account | 2 min | |
| 2 | Push code to GitHub | 3 min | |
| 3 | Deploy frontend to Vercel | 5 min | |
| 4 | Create Google Cloud account | 3 min | |
| 5 | Enable Google Cloud services | 3 min | |
| 6 | Deploy backend to Google Cloud | 10 min | |
| 7 | Connect frontend to backend | 2 min | |
| 8 | Test everything | 5 min | |
| 9 | Optional: Add custom domain | - | |

---

## 🔐 Important Credentials

Save these in a safe file:

```
GitHub:
  Username: ________________
  Password: ________________
  Email: ________________

Google Cloud:
  Email: ________________
  Project ID: ________________

Vercel:
  Email: ________________ (will ask)

URLs After Deployment:
  Frontend: ________________
  Backend: ________________
```

---

## ⚡ Key Commands

### Push to GitHub
```powershell
git init
git add .
git commit -m "Initial deployment"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/medcures.git
git push -u origin main
```

### Deploy Backend
```powershell
cd backend

gcloud auth login
gcloud config set project YOUR_PROJECT_ID

gcloud run deploy medcures-backend `
  --source . `
  --platform managed `
  --region us-central1 `
  --allow-unauthenticated `
  --memory 512Mi `
  --cpu 1
```

---

## 🌐 Important URLs

| Service | URL |
|---------|-----|
| **GitHub New Repo** | https://github.com/new |
| **Vercel Sign Up** | https://vercel.com/signup |
| **Google Cloud Free** | https://cloud.google.com/free |
| **Google Cloud SDK** | https://cloud.google.com/sdk/docs/install |

---

## 📊 Free Tier Limits

| Service | Free Limit | Your Usage |
|---------|-----------|-----------|
| Vercel | Unlimited | ✅ |
| Google Cloud Run | 2M requests/month | ✅ (plenty) |
| MongoDB Atlas | 512MB | ✅ (enough for start) |

---

## 🔄 After Deployment

### Update Frontend
```powershell
git add .
git commit -m "Update frontend"
git push
# Vercel auto-deploys!
```

### Update Backend
```powershell
cd backend
git add .
git commit -m "Update backend"
git push

# Then redeploy:
gcloud run deploy medcures-backend --source . --platform managed --region us-central1 --allow-unauthenticated
```

---

## ❓ Quick Troubleshooting

| Problem | Solution |
|---------|----------|
| Frontend won't load | Clear cache (Ctrl+Shift+Del) |
| Backend 404 | Check URL in Vercel env vars |
| Database error | Verify MongoDB connection string |
| Permission denied | Run PowerShell as Administrator |

---

## 📞 Getting Help

Provide:
1. Step number you're stuck on
2. Exact error message (screenshot)
3. What you tried
4. Expected vs actual result

---

**Ready? Start with: SIMPLE_DEPLOYMENT_STEPS.md**

Questions? Ask before starting any step! 👍
