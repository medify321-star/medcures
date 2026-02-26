# 🚀 MedCures Production Launch Checklist

## Phase 1: Database Setup ⏱️ ~20 minutes

- **Step 1**: Follow [MONGODB_ATLAS_SETUP.md](MONGODB_ATLAS_SETUP.md)
  - [ ] Create MongoDB Atlas account
  - [ ] Create cluster
  - [ ] Create database user
  - [ ] Allow network access
  - [ ] Get connection string

- **Step 2**: Configure your app
  - [ ] Add `MONGO_URL` to `backend/.env`
  - [ ] Add `DB_NAME="medcures_db"` to `backend/.env`

- **Step 3**: Test connection
  ```bash
  cd backend
  python setup_mongodb.py
  ```
  Expected: ✅ MongoDB Connection Successful!

---

## Phase 2: Production Environment Setup ⏱️ ~15 minutes

- [ ] Review `backend/.env.production`
- [ ] Generate JWT Secret:
  ```bash
  python -c "import secrets; print(secrets.token_urlsafe(32))"
  ```
- [ ] Update these in `.env.production`:
  - `JWT_SECRET_KEY` = Your generated secret (32+ chars)
  - `FOUNDER_EMAIL` = Your email
  - `CORS_ORIGINS` = Your production domain(s)
  - `ENVIRONMENT` = "production"

- [ ] Review `frontend/.env.production`
- [ ] Update:
  - `REACT_APP_BACKEND_URL` = Your production API URL
  - `REACT_APP_ENVIRONMENT` = "production"

---

## Phase 3: Testing Before Production ⏱️ ~30 minutes

- **Local Testing**
  - [ ] Start backend: `python -m uvicorn server:app --reload`
  - [ ] Start frontend: `cd frontend && npm start`
  - [ ] Test Sign Up flow
  - [ ] Test Login flow
  - [ ] Test Chat with sign-in
  - [ ] Check MongoDB Atlas - see users/messages being saved
  - [ ] Verify data persists after server restart

- **Production Simulation**
  - [ ] Set `ENVIRONMENT=production` in backend `.env`
  - [ ] Set `CORS_ORIGINS="http://localhost:3000"` (not wildcard)
  - [ ] Restart backend - should start without errors
  - [ ] Test frontend still connects
  - [ ] Verify security headers: Open DevTools → Network → Response Headers
    - Check for: `X-Content-Type-Options`, `X-Frame-Options`, etc.

---

## Phase 4: Google Cloud Project Setup ⏱️ ~30 minutes

- [ ] Create Google Cloud account: https://cloud.google.com
- [ ] Create new project: "medcures-production"
- [ ] Enable APIs:
  - Cloud Run API
  - Cloud Build API
  - Container Registry API
- [ ] Create service account with permissions:
  - Cloud Run Admin
  - Service Account User

---

## Phase 5: Backend Deployment (Cloud Run) ⏱️ ~20 minutes

### Option A: Deploy via gcloud CLI (Recommended)

1. **Install Google Cloud CLI**: https://cloud.google.com/sdk/docs/install

2. **Authenticate**:
   ```bash
   gcloud auth login
   gcloud config set project medcures-production
   ```

3. **Create app.yaml** (Already configured in PRODUCTION_DEPLOYMENT.md)

4. **Deploy**:
   ```bash
   cd backend
   gcloud run deploy medcures-backend \
     --source . \
     --platform managed \
     --region us-central1 \
     --memory 512Mi \
     --timeout 300 \
     --allow-unauthenticated \
     --set-env-vars=ENVIRONMENT=production,JWT_SECRET_KEY="YOUR_SECRET",FOUNDER_EMAIL="your@email.com",MONGO_URL="your-mongo-url",DB_NAME=medcures_db,CORS_ORIGINS="https://yourdomain.com"
   ```

5. **Note the service URL** - looks like: `https://medcures-backend-xxxxx.run.app`

### Option B: Deploy via Docker

```bash
# Build image
docker build -t medcures-backend:latest ./backend

# Push to Google Container Registry
docker push gcr.io/medcures-production/medcures-backend:latest

# Deploy to Cloud Run
gcloud run deploy medcures-backend \
  --image gcr.io/medcures-production/medcures-backend:latest \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated
```

---

## Phase 6: Frontend Deployment (Cloud Storage + CDN) ⏱️ ~15 minutes

1. **Build frontend**:
   ```bash
   cd frontend
   npm run build
   ```

2. **Create Cloud Storage bucket**:
   ```bash
   gsutil mb gs://medcures-frontend-XYZ
   ```

3. **Upload build files**:
   ```bash
   gsutil -m cp -r build/* gs://medcures-frontend-XYZ/
   ```

4. **Make public**:
   ```bash
   gsutil iam ch allUsers:objectViewer gs://medcures-frontend-XYZ
   ```

5. **Enable CDN** (via Google Cloud Console):
   - Create Cloud CDN with backend as your bucket
   - Get CDN IP address

6. **Update frontend .env**:
   - Set `REACT_APP_BACKEND_URL` to your Cloud Run URL
   - Rebuild if needed

---

## Phase 7: Custom Domain & SSL ⏱️ ~15 minutes

1. **Register domain**: Google Domains / Namecheap / GoDaddy
   - Recommended: `medcures.com` or similar

2. **Point domain to backend**:
   - Create DNS record: `api.yourdomain.com` → Cloud Run URL
   - Add SSL certificate (Google Cloud auto-provides free cert)

3. **Point subdomain to frontend**:
   - Create DNS record: `yourdomain.com` → Cloud CDN IP
   - Or use Cloud Load Balancer for better control

4. **Update CORS_ORIGINS in production backend**:
   ```
   CORS_ORIGINS="https://yourdomain.com,https://www.yourdomain.com,https://api.yourdomain.com"
   ```

---

## Phase 8: Monitoring & Security ⏱️ ~20 minutes

- [ ] Set up error tracking:
  - [ ] Create Sentry account: https://sentry.io
  - [ ] Add `SENTRY_DSN` to backend `.env`

- [ ] Enable Google Cloud Monitoring:
  - [ ] View Cloud Run logs: `gcloud app logs read`
  - [ ] Set up alerts for high error rates

- [ ] Security Checklist:
  - [ ] Verify HTTPS working on all domains
  - [ ] Test CORS headers
  - [ ] Review `.gitignore` - no secrets committed
  - [ ] Set up database backups

- [ ] Performance Testing:
  - [ ] Test sign-up flow from production URL
  - [ ] Test chat from production URL
  - [ ] Check response times
  - [ ] Verify data saves to MongoDB

---

## Final Pre-Launch Verification ⏱️ ~20 minutes

- [ ] **Backend Tests**
  - [ ] API responds at `/docs` on production URL
  - [ ] Sign up works: POST `/api/auth/signup`
  - [ ] Login works: POST `/api/auth/login`
  - [ ] Chat responds: POST `/api/chat/send`
  - [ ] Error handling works (try invalid request)

- [ ] **Frontend Tests**
  - [ ] Landing page loads
  - [ ] Can click "Sign Up"
  - [ ] Can create account
  - [ ] Can login
  - [ ] Can access chat
  - [ ] Can send message and get response

- [ ] **Database Tests**
  - [ ] Check MongoDB Atlas dashboard
  - [ ] Verify users collection has data
  - [ ] Verify chat_messages collection has data
  - [ ] Backups are configured

- [ ] **Security Tests**
  - [ ] HTTPS working (green padlock)
  - [ ] No console errors about insecure resources
  - [ ] Security headers present (DevTools → Network)
  - [ ] CORS properly restricted

- [ ] **Documentation**
  - [ ] Privacy Policy published at `/privacy`
  - [ ] Terms of Service published at `/terms`
  - [ ] HIPAA/Health disclaimer visible in UI

---

## Launch! 🎉

Once all boxes are checked:

1. **Announce**: Tell users your app is live
2. **Monitor**: Watch error tracking and analytics
3. **Support**: Be ready for user feedback
4. **Iterate**: Fix bugs and add features based on feedback

---

## Rollback Plan (If Something Goes Wrong)

1. **Stop new deployments**: `gcloud run update medcures-backend --no-traffic-split`
2. **Revert backend**: Deploy previous version from artifact registry
3. **Revert frontend**: Restore previous build from Cloud Storage
4. **Notify users**: Post status update

---

## Total Time Estimate
- Phase 1: 20 min
- Phase 2: 15 min
- Phase 3: 30 min
- Phase 4: 30 min
- Phase 5: 20 min
- Phase 6: 15 min
- Phase 7: 15 min
- Phase 8: 20 min
- Verification: 20 min

**Total: ~3-4 hours for first-time production deployment**

---

**Start with Phase 1 and follow sequentially. Reach back out if you hit any blockers!** 🚀
