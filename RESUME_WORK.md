# Medcures - Quick Start Guide for Future Work

## Project Location
```
c:\Users\ASUS\OneDrive\Documents\my website\.emergent\.emergent
```

## To Resume Work

### Step 1: Start Backend (Port 8000)
```powershell
cd "c:\Users\ASUS\OneDrive\Documents\my website\.emergent\.emergent\backend"
C:/Python314/python.exe -m uvicorn server:app --reload --host 127.0.0.1 --port 8000
```

### Step 2: Start Frontend (Port 3002)
```powershell
cd "c:\Users\ASUS\OneDrive\Documents\my website\.emergent\.emergent\frontend"
npm start
```

### Step 3: Access Application
- **Frontend:** http://localhost:3002
- **Backend API:** http://localhost:8000
- **API Docs:** http://localhost:8000/docs

## Project Structure

### Frontend
- Location: `frontend/src/`
- Framework: React with React Router
- Styling: Tailwind CSS
- Pages: Chat, Landing, Login, Signup, Privacy, Terms
- Built with: npm run build

### Backend
- Location: `backend/`
- Framework: FastAPI with Uvicorn
- Database: In-memory for testing (pharmacopoeia.json)
- Auth: JWT tokens
- Drug Data: `backend/pharmacopoeia.json` (5 drugs)

## Key Features (Currently Working)

✅ User Authentication
- Signup/Login with in-memory storage
- JWT token generation

✅ Chat Interface
- Drug information search
- Mock AI responses from pharmacopoeia data
- Proper formatting and citations

✅ Pharmacopoeia Database
- Aspirin
- Paracetamol
- Amoxicillin
- Ibuprofen
- Metformin

## Git History (4 Commits)

1. Initial commit: Full stack platform setup
2. Fix: Clean pharmacopoeia.json with encoding (5 drugs)
3. Restore: Original comprehensive pharmacopoeia
4. Restore: Full pharmacopoeia with all drug info

## For Future MongoDB Setup

When ready to add persistent database:
1. Install MongoDB locally or use MongoDB Atlas
2. Update `.env` MONGO_URL setting
3. Uncomment database storage in `backend/server.py` send_chat()
4. Restart backend

## Environment Variables

- **Backend** (.env): MONGO_URL, OPENROUTER_API_KEY, JWT_SECRET_KEY
- **Frontend** (.env): REACT_APP_BACKEND_URL=http://localhost:8000

## Build Commands

```powershell
# Frontend build
cd frontend
npm run build

# Run tests (if added)
npm test
```

## All Code Is Saved in Git

Pull any changes or restore previous versions using:
```powershell
git log          # View history
git checkout <commit-hash>  # Go to previous version
git status       # Check current state
```

## Next Steps for Future Work

1. Add more drugs to pharmacopoeia.json
2. Set up MongoDB for persistence
3. Deploy to Google Cloud/Firebase
4. Add real AI integration (OpenRouter API key ready)
5. Add user chat history storage
6. Implement feedback system

---
Last Updated: February 22, 2026
Project Status: Fully Working - Ready for Future Edits
