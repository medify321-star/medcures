# 🏥 MedCures - AI-Powered Medical Information Platform

**Status**: Development Complete ✅ | Ready for Production Deployment 🚀

A full-stack medical information companion platform with AI-powered drug information, built with React, FastAPI, and MongoDB.

---

## 📋 Quick Start

### Development (Local Testing)

```bash
# 1. Backend
cd backend
python -m uvicorn server:app --reload

# 2. Frontend (new terminal)
cd frontend
npm start

# 3. Open http://localhost:3000
```

### Production Deployment

Follow the step-by-step guide: **[LAUNCH_CHECKLIST.md](LAUNCH_CHECKLIST.md)**

Expected time: 3-4 hours for first deployment

---

## 📁 Project Structure

```
medcures/
├── backend/                    # FastAPI Python server
│   ├── server.py              # Main application
│   ├── requirements.txt        # Python dependencies
│   ├── .env.example            # Template for development
│   ├── .env.production         # Template for production
│   ├── setup_mongodb.py        # MongoDB setup helper
│   ├── pharmacopoeia.json      # Drug database
│   └── __pycache__/
│
├── frontend/                   # React web application
│   ├── src/
│   │   ├── App.js              # Main React component
│   │   ├── pages/              # Page components
│   │   │   ├── Landing.js      # Home page
│   │   │   ├── Signup.js       # User registration
│   │   │   ├── Login.js        # User authentication
│   │   │   └── Chat.js         # AI chat interface
│   │   ├── context/
│   │   │   └── AuthContext.js  # Authentication state
│   │   └── components/         # UI components (Radix UI)
│   ├── public/
│   ├── package.json
│   ├── tailwind.config.js      # Tailwind CSS config
│   ├── .env.example            # Template
│   └── .env.production         # Production config
│
├── PRODUCTION_DEPLOYMENT.md    # Complete deployment guide
├── MONGODB_ATLAS_SETUP.md      # Database setup
├── LAUNCH_CHECKLIST.md         # Pre-launch verification
├── SECURITY_VALIDATIONS_EXPLAINED.md
└── README.md                   # This file
```

---

## 🔧 Technology Stack

### Backend
- **Framework**: FastAPI (Python async web framework)
- **Server**: Uvicorn (ASGI server)
- **Database**: MongoDB Atlas (cloud NoSQL)
- **Auth**: JWT tokens + bcrypt hashing
- **AI**: OpenRouter API (LLM integration)
- **Security**: CORS, security headers, input validation

### Frontend
- **Framework**: React 18 with Hooks
- **Routing**: React Router v6
- **Styling**: Tailwind CSS 3.4
- **UI Components**: Radix UI
- **Icons**: Lucide React
- **HTTP Client**: Axios
- **Build Tool**: Craco (Create React App Config Override)

### Deployment
- **Option 1**: Google Cloud Run (Recommended)
- **Option 2**: Docker + Kubernetes
- **CDN**: Google Cloud Storage + CDN
- **Domain**: Custom domain with SSL

---

## 🚀 Production Launch Path

### Quick Timeline

| Phase | Duration | Status |
|-------|----------|--------|
| 1. Database Setup (MongoDB) | 20 min | Next |
| 2. Environment Configuration | 15 min | Next |
| 3. Local Testing | 30 min | Next |
| 4. Google Cloud Setup | 30 min | Next |
| 5. Backend Deployment | 20 min | Next |
| 6. Frontend Deployment | 15 min | Next |
| 7. Domain + SSL | 15 min | Next |
| 8. Monitoring Setup | 20 min | Next |
| 9. Final Verification | 20 min | Next |

**Total: ~3-4 hours**

### Step-by-Step Guides

1. **[MONGODB_ATLAS_SETUP.md](MONGODB_ATLAS_SETUP.md)**
   - Create MongoDB account
   - Set up cluster
   - Configure database
   - Test connection

2. **[LAUNCH_CHECKLIST.md](LAUNCH_CHECKLIST.md)**
   - Complete production checklist
   - Deploy to Google Cloud Run
   - Set up domain
   - Verify everything works

3. **[PRODUCTION_DEPLOYMENT.md](PRODUCTION_DEPLOYMENT.md)**
   - Comprehensive deployment guide
   - Database options (MongoDB/PostgreSQL)
   - Cloud deployment options
   - HIPAA/GDPR compliance
   - Performance optimization

---

## 🔐 Security Features

✅ **Built-in Security**
- JWT token-based authentication
- Bcrypt password hashing (10-round salting)
- CORS protection (restricted origins in production)
- Security headers middleware (HSTS, CSP, X-Frame-Options)
- Input validation with Pydantic
- SQL injection protection (using ORM)
- XSS protection via React's default escaping

✅ **Environment Management**
- Secrets stored in `.env` files
- `.env` committed to `.gitignore`
- `.env.example` for team onboarding
- Production validation enforces requirements:
  - JWT secret minimum 32 characters
  - No wildcard CORS in production
  - Required environment variables

✅ **Healthcare Compliance**
- HIPAA readiness (encrypt, audit logs, access control)
- GDPR support (data deletion endpoints)
- Privacy policy and terms of service
- User data isolation

---

## 📚 API Documentation

### Available at: `http://localhost:8000/docs`

#### Authentication Endpoints

```
POST   /api/auth/signup           # Register new user
POST   /api/auth/login            # User login
GET    /api/auth/me               # Get current user
POST   /api/auth/logout           # Logout
```

#### Chat Endpoints

```
POST   /api/chat/send             # Send message to AI
GET    /api/chat/history          # Get chat history
DELETE /api/chat/{message_id}     # Delete message
```

#### Drug Information

```
GET    /api/drugs                 # List all drugs
GET    /api/drugs/search?q=query  # Search drugs
GET    /api/drugs/{id}            # Get drug details
```

---

## 🎯 Features Implemented

### ✅ Completed
- [x] User authentication (signup/login/logout)
- [x] JWT token management
- [x] MongoDB integration
- [x] AI chat interface
- [x] Tailwind CSS styling
- [x] Responsive design
- [x] Security headers
- [x] Error handling
- [x] Environment configuration
- [x] Production validation

### 🚧 Recommended for Production
- [ ] Email verification
- [ ] Password reset flow
- [ ] Payment integration (if monetizing)
- [ ] Rate limiting per user
- [ ] Chat history export
- [ ] Admin dashboard
- [ ] Analytics integration
- [ ] A/B testing framework

---

## 🔧 Configuration

### Development Environment

Create `backend/.env`:
```env
MONGO_URL="mongodb+srv://user:pass@cluster.mongodb.net/?retryWrites=true"
DB_NAME="medcures_dev"
JWT_SECRET_KEY="dev-secret-key-at-least-32-chars"
FOUNDER_EMAIL="your@email.com"
CORS_ORIGINS="http://localhost:3000"
ENVIRONMENT="development"
OPENROUTER_API_KEY="your-api-key-optional"
```

Create `frontend/.env.local`:
```env
REACT_APP_BACKEND_URL="http://localhost:8000"
REACT_APP_ENVIRONMENT="development"
```

### Production Environment

See: **[backend/.env.production](backend/.env.production)**

---

## 🧪 Testing

### Manual Testing Checklist

```bash
# 1. Test Sign Up
POST http://localhost:8000/api/auth/signup
Body: {"email": "test@test.com", "password": "Test123!", "name": "Test User"}

# 2. Test Login
POST http://localhost:8000/api/auth/login
Body: {"email": "test@test.com", "password": "Test123!"}

# 3. Test Chat
POST http://localhost:8000/api/chat/send
Header: Authorization: Bearer {token}
Body: {"query": "What is ibuprofen?"}

# 4. Test Protected Route
GET http://localhost:8000/api/auth/me
Header: Authorization: Bearer {token}
```

### Automated Testing

```bash
# Backend tests
cd backend
pytest tests/

# Frontend tests
cd frontend
npm test
```

---

## 🚨 Troubleshooting

### Backend Won't Start

**Error**: `MONGO_URL not found`
- **Fix**: Add MONGO_URL to backend/.env

**Error**: `JWT_SECRET_KEY missing`
- **Fix**: Add JWT_SECRET_KEY to backend/.env (minimum 32 chars in production)

**Error**: `Port 8000 already in use`
- **Fix**: 
  ```bash
  # On Windows:
  netstat -ano | findstr :8000
  
  # On Mac/Linux:
  lsof -i :8000
  ```

### Frontend Won't Start

**Error**: `Port 3000 already in use`
- **Fix**: Kill port: `npx kill-port 3000`

**Error**: `Tailwind styles not showing`
- **Fix**: 
  ```bash
  npm run build
  npm start  # Restart to recompile
  ```

### MongoDB Connection Issues

**Run diagnostic**:
```bash
cd backend
python setup_mongodb.py
```

---

## 📞 Support

### Documentation
- [Production Deployment](PRODUCTION_DEPLOYMENT.md) - Full deployment guide
- [MongoDB Setup](MONGODB_ATLAS_SETUP.md) - Database configuration
- [Launch Checklist](LAUNCH_CHECKLIST.md) - Pre-launch verification
- [Security Validations](SECURITY_VALIDATIONS_EXPLAINED.md) - Why certain validations exist

### Resources
- FastAPI Docs: https://fastapi.tiangolo.com
- React Docs: https://react.dev
- MongoDB Docs: https://docs.mongodb.com
- Google Cloud: https://cloud.google.com/docs

---

## 📄 License

Private project - All rights reserved

---

## 🎯 Next Steps

1. **Already Done**:
   - ✅ Development servers running locally
   - ✅ Authentication working
   - ✅ Chat interface functional
   - ✅ Tailwind CSS configured
   - ✅ Security hardened

2. **Next**:
   - ⏭️ Set up MongoDB Atlas (follow [MONGODB_ATLAS_SETUP.md](MONGODB_ATLAS_SETUP.md))
   - ⏭️ Generate production JWT secret
   - ⏭️ Follow [LAUNCH_CHECKLIST.md](LAUNCH_CHECKLIST.md)
   - ⏭️ Deploy to Google Cloud Run

---

**Ready to launch? 🚀 Start with [MONGODB_ATLAS_SETUP.md](MONGODB_ATLAS_SETUP.md)**
