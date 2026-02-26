# MedCures Production Deployment Guide

## Overview
This document covers everything needed to move your MedCures application from development to production on Google Cloud Platform (or any cloud provider).

## Phase 1: Pre-Deployment Security ✅

### 1.1 Environment Variables (CRITICAL)
**Status: Already configured**

Your `.env` files are now:
- Protected in `.gitignore` (never committed)
- Have `.env.example` templates for team members
- Production validation enforced in code

**DO NOT commit real .env files!**

```bash
# Verify .env is ignored
git status
# Should not show .env or .env.local files
```

### 1.2 JWT Secret Key Generation
Generate a strong random JWT secret for production:

```bash
# On Windows PowerShell:
python -c "import secrets; import base64; print(base64.urlsafe_b64encode(secrets.token_bytes(32)).decode())"

# On Linux/Mac:
python3 -c "import secrets; print(secrets.token_urlsafe(32))"
```

Copy the output and use as your `JWT_SECRET_KEY` in production `.env`

### 1.3 API Keys
- **OpenRouter API**: Sign up at https://openrouter.ai and get your API key
- **MongoDB**: Set up MongoDB Atlas cluster at https://www.mongodb.com/cloud/atlas

## Phase 2: Database Setup (PostgreSQL Recommended for Production)

### Option A: MongoDB Atlas (Simple)
1. Create free account at https://www.mongodb.com/cloud/atlas
2. Create a new cluster
3. Create database user with strong password
4. Get connection string
5. Add to `.env`:
```
MONGO_URL=mongodb+srv://username:password@cluster.mongodb.net/medcures_db?retryWrites=true&w=majority
DB_NAME=medcures_db
```

### Option B: PostgreSQL (Better for Healthcare Data)
Better for HIPAA compliance and regulatory requirements.

Install dependencies:
```bash
pip install psycopg2-binary sqlalchemy alembic
```

Create `backend/database.py`:
```python
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

DATABASE_URL = os.environ.get('DATABASE_URL', 'postgresql://user:password@localhost/medcures')

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
```

## Phase 3: Deployment Options

### Option A: Google Cloud Run (Recommended - Simple & Scalable)

#### Backend Deployment:

1. **Install Google Cloud CLI**
   ```bash
   # Download from: https://cloud.google.com/sdk/docs/install
   gcloud init
   gcloud auth login
   ```

2. **Create `backend/app.yaml`**
   ```yaml
   runtime: python39
   env: flex
   entrypoint: gunicorn -w 4 -b :$PORT server:app
   
   env_variables:
     ENVIRONMENT: "production"
     JWT_SECRET_KEY: "your-secret-key-here"
     MONGO_URL: "your-mongo-url"
     DB_NAME: "medcures_db"
     FOUNDER_EMAIL: "your@email.com"
     CORS_ORIGINS: "https://yourdomain.com"
     OPENROUTER_API_KEY: "your-api-key"
   
   automatic_scaling:
     min_instances: 1
     max_instances: 10
     target_cpu_utilization: 0.8
   
   resources:
     cpu: 1
     memory_gb: 0.5
   ```

3. **Create `backend/requirements-prod.txt`**
   ```
   fastapi==0.104.1
   uvicorn==0.24.0
   gunicorn==21.2.0
   python-dotenv==1.0.0
   pydantic[email]==2.5.0
   pydantic-settings==2.1.0
   bcrypt==4.1.1
   pyjwt==2.8.1
   motor==3.3.2
   openai==1.3.5
   sqlalchemy==2.0.23
   psycopg2-binary==2.9.9
   python-multipart==0.0.6
   ```

4. **Deploy Backend**
   ```bash
   cd backend
   gcloud app deploy app.yaml --project=your-project-id
   ```

#### Frontend Deployment:

1. **Build frontend**
   ```bash
   cd frontend
   npm run build
   ```

2. **Deploy to Cloud Storage + CDN**
   ```bash
   # Create bucket
   gsutil mb gs://medcures-frontend
   
   # Upload build
   gsutil -m cp -r build/* gs://medcures-frontend/
   
   # Make public
   gsutil iam ch serviceAccount:cloud-cdn@cloud.iam.gserviceaccount.com:objectViewer gs://medcures-frontend
   ```

3. **Create `frontend/.env.production`**
   ```
   REACT_APP_BACKEND_URL=https://your-backend-url.run.app
   REACT_APP_ENVIRONMENT=production
   REACT_APP_ENABLE_AI_CHAT=true
   ```

### Option B: Docker + Kubernetes (Enterprise)

#### Create `backend/Dockerfile`
```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements-prod.txt .
RUN pip install --no-cache-dir -r requirements-prod.txt

COPY . .

ENV PYTHONUNBUFFERED=1
ENV ENVIRONMENT=production

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:8000", "server:app"]
```

#### Create `frontend/Dockerfile`
```dockerfile
FROM node:18 AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

FROM nginx:alpine
COPY --from=builder /app/build /usr/share/nginx/html
COPY nginx.conf /etc/nginx/nginx.conf
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

#### Build and push
```bash
# Build images
docker build -t medcures-backend:latest ./backend
docker build -t medcures-frontend:latest ./frontend

# Push to Google Container Registry
docker push gcr.io/your-project-id/medcures-backend:latest
docker push gcr.io/your-project-id/medcures-frontend:latest
```

## Phase 4: Domain & SSL

### 1. Get a Domain
- Register at: Google Domains, Namecheap, or GoDaddy
- Recommended: `yourdomain.com`

### 2. SSL Certificate
Google Cloud automatically provides free SSL certificates

### 3. Configure DNS
Point your domain to:
- Frontend: Cloud Storage CDN IP
- Backend: Cloud Run service URL

## Phase 5: Healthcare Compliance (IMPORTANT!)

### Privacy & Data Protection
1. **HIPAA Compliance** (if US-based and handling protected health info)
   - Sign Business Associate Agreement (BAA)
   - Implement access controls
   - Enable audit logging
   - Encryption at rest and in transit ✅ (SSL enabled)

2. **GDPR Compliance** (if EU users)
   - Data processing agreement
   - Right to be forgotten implementation
   - Consent collection

3. **Add Privacy Policy**
   - Create `frontend/public/privacy.html`
   - Include in your Terms page

4. **Add Data Deletion API**
   ```python
   @api_router.delete("/api/users/delete")
   async def delete_user(current_user: User = Depends(get_current_user)):
       """Allow users to delete their data (GDPR right to be forgotten)"""
       # Delete user data from database
       # Delete all associated records
       return {"message": "Account and data deleted"}
   ```

## Phase 6: Monitoring & Logging

### Google Cloud Monitoring
```bash
gcloud logging read "resource.type=cloud_run_revision" --limit 50
```

### Add Application Monitoring
Update `backend/server.py` to send logs to Cloud Logging:

```python
import google.cloud.logging

if IS_PRODUCTION:
    client = google.cloud.logging.Client()
    client.setup_logging()
```

### Add Error Tracking
Sign up for Sentry: https://sentry.io

```bash
pip install sentry-sdk
```

Add to `backend/server.py`:
```python
import sentry_sdk
from sentry_sdk.integrations.fastapi import FastApiIntegration

if IS_PRODUCTION:
    sentry_sdk.init(
        dsn=os.environ.get('SENTRY_DSN'),
        integrations=[FastApiIntegration()],
        traces_sample_rate=0.1
    )
```

## Phase 7: Performance Optimization

### Backend
- Add caching: `pip install redis`
- Enable gzip: `pip install py-gzip`
- Database indexing on frequently queried fields

### Frontend
- Minification (done by `npm run build`)
- CDN distribution ✅ (Cloud Storage)
- Image optimization
- Code splitting

## Phase 8: Launch Checklist

- [ ] `.env.example` created and committed
- [ ] `.gitignore` properly configured
- [ ] JWT secret is 32+ characters in production
- [ ] CORS_ORIGINS configured to specific domains
- [ ] MongoDB or PostgreSQL cluster created
- [ ] Monitoring/logging configured
- [ ] SSL certificate issued
- [ ] Privacy policy published
- [ ] Terms of service published
- [ ] API rate limiting enabled
- [ ] Database backups configured
- [ ] Error tracking enabled
- [ ] Performance tested
- [ ] Security headers verified
- [ ] HIPAA/GDPR compliance reviewed

## Commands Reference

```bash
# Check environment
gcloud config list

# View logs
gcloud app logs read -n 50

# Scale backend
gcloud app services set-traffic default --splits=v1=100

# Rollback
gcloud app versions delete VERSION_ID

# Monitoring dashboard
gcloud monitoring dashboards list
```

## Emergency Procedures

### If Database Goes Down
1. Check Cloud Logging for errors
2. Verify network connectivity
3. Check authentication credentials
4. Restore from backup

### If API Keys Compromised
1. Invalidate old key immediately
2. Generate new key
3. Update `.env` in production
4. Restart service: `gcloud app deploy`

### If Performance Degrades
1. Check Cloud Monitoring
2. Review database query logs
3. Enable caching
4. Consider horizontal scaling

## Support & Resources

- Google Cloud Docs: https://cloud.google.com/docs
- FastAPI: https://fastapi.tiangolo.com
- React: https://react.dev
- MongoDB: https://docs.mongodb.com
- PostgreSQL: https://www.postgresql.org/docs

---

**Last Updated**: February 2026
**Status**: Production-Ready Template
