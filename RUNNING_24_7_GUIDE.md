# 🎉 Your MedCures is Now Running 24/7!

## ✅ What's Running

- **Backend**: http://localhost:8000
  - Auto-restart enabled (crashes = auto-fix)
  - Health check: http://localhost:8000/health
  - API Docs: http://localhost:8000/docs

- **Frontend**: http://localhost:3001
  - Connected to backend automatically
  - Open this in browser: http://localhost:3001

## 🚀 How to Start Everything

### Option 1: Simple (Recommended)
1. Find `START_MEDCURES.bat` in your project folder
2. Double-click it
3. Wait 5 seconds
4. Open http://localhost:3001 in browser

### Option 2: Using Commands
```powershell
# In PowerShell or Command Prompt:
pm2 list              # See what's running
pm2 logs              # See error logs (if any)
pm2 restart all       # Restart everything
```

## 📊 Monitoring Commands

### Check if everything is running
```powershell
pm2 list
```
You should see:
- `medcures-backend` status: `online` ✅
- Terminal will show frontend running

### Check logs (if something breaks)
```powershell
pm2 logs medcures-backend --lines 50
```

### Restart if needed
```powershell
pm2 restart medcures-backend
pm2 restart all
```

## 🛡️ What Prevents Crashing Now

1. **PM2 Auto-Restart**
   - If backend crashes → automatically restarts
   - Restarts up to 4 times per minute
   
2. **Global Error Handler**
   - Catches all errors instead of crashing
   - Returns proper error response to user

3. **Health Check Endpoint**
   - http://localhost:8000/health
   - Use this to monitor if backend is alive

4. **Memory Limit**
   - Backend automatically restarts if using >500MB memory
   - Prevents memory leak issues

## ⚠️ Common Issues & Fixes

### "Port 8000 is already in use"
```powershell
# Kill the process using port 8000
netstat -ano | findstr ":8000"
taskkill /PID [number] /F
```

### "Port 3001/3000 already in use"
- Frontend will automatically use 3001 instead of 3000
- That's normal and fine!

### Backend keeps crashing (↺ keeps increasing)
1. Check logs: `pm2 logs medcures-backend`
2. Look for error messages
3. Common causes:
   - Missing .env variables → Add them to backend/.env
   - MongoDB connection problem → Check MONGO_URL
   - API key expired → Check OPENROUTER_API_KEY

### Frontend won't load
1. Try hard refresh: `Ctrl + Shift + R`
2. Check console for errors: `F12` → Console tab
3. Make sure backend is running: http://localhost:8000/health

## 📋 Checklist Before Going Live

- [ ] Backend running: http://localhost:8000/health returns `"status":"ok"`
- [ ] Frontend loads: http://localhost:3001 shows website
- [ ] Can type a message in chat
- [ ] Backend doesn't crash after 10 minutes
- [ ] Logs show no errors: `pm2 logs medcures-backend`

## 🔧 Maintenance

### Weekly
- [ ] Check PM2 logs for errors
- [ ] Verify both services running: `pm2 list`
- [ ] Test chat feature works end-to-end

### Monthly
- [ ] Rotate API keys if needed
- [ ] Check MongoDB usage
- [ ] Update dependencies: `npm update`

## 📞 Emergency Stop

If you need to stop everything:
```powershell
pm2 kill                # Stops everything
netstat -ano | findstr ":3001" | for /f "tokens=5" %%a in ('findstr "LISTENING"') do taskkill /PID %%a /F
```

## 🎯 Next Steps

1. **Test it working**: 
   - Open http://localhost:3001
   - Try sending a message
   - Verify response comes back

2. **Leave it running**:
   - Keep terminal open
   - Or set up Windows Service for true 24/7

3. **Monitor it**:
   - Run `pm2 logs` occasionally
   - Use health endpoint daily: http://localhost:8000/health

---

**You now have a system that's reliable and won't crash repeatedly!** 
The backend will auto-restart on any crashes.
