@echo off
REM ============================================
REM  MedCures Startup Script (Simple & Easy)
REM ============================================
REM  This script starts both backend and frontend
REM  Just double-click this file to launch!
REM ============================================

echo.
echo ===================================
echo   🚀 Starting MedCures...
echo ===================================
echo.

REM Kill any existing processes on these ports
echo [1/3] Cleaning up old processes...
netstat -ano | findstr ":8000" | for /f "tokens=5" %%a in ('findstr "LISTENING"') do taskkill /PID %%a /F 2>nul
netstat -ano | findstr ":3000\|:3001" | for /f "tokens=5" %%a in ('findstr "LISTENING"') do taskkill /PID %%a /F 2>nul
timeout /t 1 /nobreak

REM Start backend with PM2
echo [2/3] Starting Backend (port 8000 with auto-restart)...
cd backend
pm2 start server.py --name medcures-backend --interpreter python --watch --max-memory-restart 500M --update-env
cd ..
timeout /t 2 /nobreak

REM Start frontend
echo [3/3] Starting Frontend (port 3001)...
cd frontend
start npm start
cd ..
timeout /t 3 /nobreak

REM Show status
echo.
echo ===================================
echo   ✅ MedCures Started!
echo ===================================
echo.
echo 📱 Frontend: http://localhost:3001
echo 📚 Backend API: http://localhost:8000
echo 📖 API Docs: http://localhost:8000/docs
echo 💚 Health Check: http://localhost:8000/health
echo.
echo ⚠️  NOTE: Keep this window open!
echo If you close it, services will stop.
echo.
echo 🔄 Auto-restart: 
echo   - Backend will restart if it crashes
echo   - Frontend will show errors in browser
echo.
pause
