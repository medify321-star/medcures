#!/usr/bin/env python3
"""
MongoDB Setup and Configuration Script
Helps you verify MongoDB connection and initialize the database
"""

import asyncio
import os
from pathlib import Path
from dotenv import load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient
import sys

# Load environment variables
ROOT_DIR = Path(__file__).parent / "backend"
load_dotenv(ROOT_DIR / '.env')

async def test_mongodb_connection():
    """Test if MongoDB connection works"""
    print("\n" + "="*60)
    print("🔍 Testing MongoDB Connection...")
    print("="*60)
    
    mongo_url = os.environ.get('MONGO_URL')
    db_name = os.environ.get('DB_NAME', 'medcures_db')
    
    if not mongo_url:
        print("❌ ERROR: MONGO_URL not found in .env")
        print("\n📋 Setup Instructions:")
        print("1. Create MongoDB Atlas account: https://www.mongodb.com/cloud/atlas")
        print("2. Create a cluster and database user")
        print("3. Get connection string and add to backend/.env:")
        print('   MONGO_URL="mongodb+srv://username:password@cluster.mongodb.net/?retryWrites=true"')
        print('   DB_NAME="medcures_db"')
        return False
    
    try:
        # Attempt connection
        client = AsyncIOMotorClient(mongo_url, serverSelectionTimeoutMS=5000)
        db = client[db_name]
        
        # Ping to verify
        result = await client.admin.command('ping')
        print(f"✅ MongoDB Connection Successful!")
        print(f"   Database: {db_name}")
        print(f"   Connected to: {mongo_url.split('@')[1] if '@' in mongo_url else 'Unknown'}")
        
        # Get stats
        stats = await db.command('dbstats')
        print(f"   Database Size: {stats['dataSize'] / 1024:.2f} KB")
        print(f"   Collections: {stats['collections']}")
        
        client.close()
        return True
        
    except Exception as e:
        print(f"❌ Connection Failed: {str(e)}")
        print("\n🔧 Troubleshooting:")
        print("   • Check MONGO_URL format: mongodb+srv://username:password@cluster...")
        print("   • Verify username and password are correct")
        print("   • Check if your IP is whitelisted in MongoDB Atlas")
        print("   • Ensure cluster is running (status shows 'Available')")
        return False

async def initialize_collections():
    """Create indexes and initial collections"""
    print("\n" + "="*60)
    print("📊 Initializing Collections and Indexes...")
    print("="*60)
    
    mongo_url = os.environ.get('MONGO_URL')
    db_name = os.environ.get('DB_NAME', 'medcures_db')
    
    if not mongo_url:
        print("❌ MongoDB not configured")
        return False
    
    try:
        client = AsyncIOMotorClient(mongo_url, serverSelectionTimeoutMS=5000)
        db = client[db_name]
        
        # Create users collection with indexes
        await db.users.create_index("email", unique=True)
        print("✅ Created 'users' collection with unique email index")
        
        # Create chat_messages collection
        await db.chat_messages.create_index("user_id")
        await db.chat_messages.create_index("created_at")
        print("✅ Created 'chat_messages' collection with indexes")
        
        # Create sessions collection
        await db.sessions.create_index("user_id")
        await db.sessions.create_index("created_at")
        print("✅ Created 'sessions' collection with indexes")
        
        # List all collections
        collections = await db.list_collection_names()
        print(f"\n📋 Collections in database '{db_name}':")
        for col in collections:
            count = await db[col].count_documents({})
            print(f"   • {col} ({count} documents)")
        
        client.close()
        return True
        
    except Exception as e:
        print(f"❌ Initialization failed: {str(e)}")
        return False

async def show_sample_data():
    """Show sample data from collections"""
    print("\n" + "="*60)
    print("👀 Sample Data Preview...")
    print("="*60)
    
    mongo_url = os.environ.get('MONGO_URL')
    db_name = os.environ.get('DB_NAME', 'medcures_db')
    
    if not mongo_url:
        return
    
    try:
        client = AsyncIOMotorClient(mongo_url, serverSelectionTimeoutMS=5000)
        db = client[db_name]
        
        # Show users
        users = await db.users.find().limit(3).to_list(3)
        if users:
            print(f"\n📝 Users ({len(users)} found):")
            for user in users:
                print(f"   • {user.get('email')} ({user.get('name')})")
        else:
            print("\n📝 Users: No users yet (expected on first setup)")
        
        # Show chat messages
        messages = await db.chat_messages.find().limit(3).to_list(3)
        if messages:
            print(f"\n💬 Chat Messages ({len(messages)} found):")
            for msg in messages:
                query = msg.get('query', '')[:50]
                print(f"   • {query}...")
        else:
            print("\n💬 Chat Messages: No messages yet")
        
        client.close()
        
    except Exception as e:
        pass  # Silently skip if collection doesn't exist yet

async def main():
    """Main execution"""
    print("\n" + "🚀 "*15)
    print("MEDCURES MONGODB SETUP")
    print("🚀 "*15)
    
    # Test connection
    connected = await test_mongodb_connection()
    
    if not connected:
        print("\n⛔ Cannot proceed without MongoDB connection")
        sys.exit(1)
    
    # Initialize collections
    print("\n" + "-"*60)
    initialized = await initialize_collections()
    
    if initialized:
        # Show sample data
        await show_sample_data()
        
        print("\n" + "="*60)
        print("✅ MongoDB Setup Complete!")
        print("="*60)
        print("\n🎉 You're ready to:")
        print("   1. Start the backend: python -m uvicorn server:app --reload")
        print("   2. Sign up a new user")
        print("   3. Check MongoDB Atlas dashboard to see your data")
        print("\n📊 Monitor your database at: https://cloud.mongodb.com")
        print("="*60 + "\n")
    else:
        print("\n⚠️  Setup incomplete - check errors above")
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())
