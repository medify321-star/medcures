# MongoDB Atlas Setup Guide for MedCures

## Step 1: Create MongoDB Atlas Account

1. **Go to**: https://www.mongodb.com/cloud/atlas
2. **Sign up** with your email (use your Google/GitHub account for faster signup)
3. **Verify** your email address
4. **Select**: "Free forever" plan (good for MVP)

## Step 2: Create Your First Cluster

1. **Click** "Create a Deployment"
2. **Choose**: 
   - Deployment Type: "Shared" (Free tier)
   - Cloud Provider: "Google Cloud"
   - Region: Choose closest to your user base (e.g., "us-central1" for US)
3. **Click** "Create Deployment"
4. **Wait** 3-5 minutes for cluster to initialize

## Step 3: Create Database User

1. **In left sidebar**, click "Database Access"
2. **Click** "Add New Database User"
3. **Username**: `medcures_user` (or your choice)
4. **Password**: Click "Auto-generate password" → Copy it somewhere safe
5. **Database User Privileges**: "Atlas Admin" (for MVP)
6. **Click** "Add User"

**SAVE THIS PASSWORD - You'll need it in the connection string!**

## Step 4: Allow Network Access

1. **In left sidebar**, click "Network Access"
2. **Click** "Add IP Address"
3. **Choose one**:
   - **During Development**: 
     - Click "Allow Access from Anywhere"
     - IP: `0.0.0.0/0` (allows all IPs, fine for dev)
   - **Production**: 
     - Add your server's specific IP only
     - More secure but requires you to know your server IP in advance

4. **Click** "Confirm"

## Step 5: Get Connection String

1. **In left sidebar**, click "Clusters"
2. **Click** "Connect" on your cluster
3. **Choose Driver**: "Drivers"
4. **Language**: "Python"
5. **Version**: 4.2+
6. **Copy** the connection string, it looks like:
   ```
   mongodb+srv://<username>:<password>@cluster.mongodb.net/?retryWrites=true&w=majority
   ```

## Step 6: Fill in Your Credentials

Take the connection string and replace:
- `<username>` → `medcures_user` (or whatever you created)
- `<password>` → Your password from Step 3

**Example:**
```
mongodb+srv://medcures_user:MyP@ssw0rd123@cluster0.mongodb.net/?retryWrites=true&w=majority
```

## Step 7: Create Database Name

1. **In MongoDB Atlas**, click "Database"
2. **Under your cluster**, you should see "Collections"
3. If it says "No Collections yet", that's fine - the database will auto-create when you first write data

We'll name it: `medcures_db`

## Step 8: Update Your .env File

Edit `backend/.env` and add:

```env
MONGO_URL="mongodb+srv://medcures_user:MyP@ssw0rd123@cluster0.mongodb.net/?retryWrites=true&w=majority"
DB_NAME="medcures_db"
```

**⚠️ SECURITY**: Never commit `.env` to GitHub! It's already in `.gitignore` 👍

## Step 9: Test Connection

Run this to verify it works:

```bash
cd backend
python -c "
from motor.motor_asyncio import AsyncIOMotorClient
import asyncio
import os
from dotenv import load_dotenv

load_dotenv()

async def test():
    mongo_url = os.environ['MONGO_URL']
    client = AsyncIOMotorClient(mongo_url)
    try:
        await client.admin.command('ping')
        print('✅ MongoDB connection successful!')
    except Exception as e:
        print(f'❌ Connection failed: {e}')
    finally:
        client.close()

asyncio.run(test())
"
```

Expected output:
```
✅ MongoDB connection successful!
```

## Step 10: Create Collections (Tables)

MongoDB will auto-create collections, but here's what will be created when users sign up:

**Collection: `users`**
```json
{
  "email": "user@example.com",
  "password_hash": "bcrypt_hashed_password",
  "name": "User Name",
  "created_at": "2026-02-26T10:00:00Z"
}
```

**Collection: `chat_messages`**
```json
{
  "user_id": "unique_user_id",
  "query": "What is ibuprofen used for?",
  "response": "Ibuprofen is...",
  "created_at": "2026-02-26T10:00:00Z"
}
```

These will be created automatically by your FastAPI backend.

## Troubleshooting

### Connection String Error
**Error**: `authentication failed` or `invalid username/password`
- **Fix**: Double-check username/password matches what you set

### IP Address Error
**Error**: `connection refused` despite correct credentials
- **Fix**: Go to "Network Access" and verify your IP is whitelisted

### Cluster Not Ready
**Error**: `connection timed out`
- **Fix**: Wait for cluster initialization to complete (check status in "Clusters")

### Database Access Denied
**Error**: `unauthorized`
- **Fix**: Make sure database user has "Atlas Admin" role

## Next Steps After Connection Works

1. ✅ Test connection (you'll do this now)
2. ✅ Update backend `.env` with MongoDB credentials
3. ✅ Restart backend server: `python -m uvicorn server:app --reload`
4. ✅ Test sign-up/login to verify data persists in MongoDB
5. ✅ Check MongoDB Atlas dashboard to see data being written

## Free Tier Limits

MongoDB Atlas Free tier includes:
- ✅ 5GB storage
- ✅ Unlimited collections
- ✅ Shared cluster
- ✅ Free monitoring
- ✅ No credit card required

**Good enough for**: MVP, testing, <100,000 users

When you outgrow this, upgrade to paid tier (pay-as-you-go, ~$0.10/GB).

---

**Do these steps and let me know when you have the MongoDB connection string ready!**
