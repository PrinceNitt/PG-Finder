"""
Script to check database connection and verify data
"""
from models.database import get_db, get_collection
from config import Config
from datetime import datetime

print("=" * 60)
print("Database Connection & Data Verification")
print("=" * 60)

# Show configuration
print(f"\n📊 Configuration:")
print(f"  Database Name: {Config.DATABASE_NAME}")
print(f"  MongoDB URI: {Config.MONGO_URI[:50]}...")  # Show first 50 chars only

# Test connection
try:
    db = get_db()
    print(f"\n✅ Connected to database: '{db.name}'")
    
    # List collections
    collections = db.list_collection_names()
    print(f"\n📁 Collections found: {len(collections)}")
    
    for col_name in collections:
        col = db[col_name]
        count = col.count_documents({})
        print(f"  - {col_name}: {count} documents")
        
        # Show sample data for main collections
        if col_name == 'users' and count > 0:
            sample = col.find_one({}, {'name': 1, 'email': 1, 'role': 1, 'created_at': 1})
            if sample:
                print(f"    Sample: {sample.get('name')} ({sample.get('email')}) - Role: {sample.get('role')}")
        
        elif col_name == 'pg_listings' and count > 0:
            sample = col.find_one({}, {'name': 1, 'city': 1, 'status': 1, 'created_at': 1})
            if sample:
                print(f"    Sample: {sample.get('name')} in {sample.get('city')} - Status: {sample.get('status')}")
        
        elif col_name == 'join_requests' and count > 0:
            sample = col.find_one({}, {'status': 1, 'created_at': 1})
            if sample:
                print(f"    Sample: Status - {sample.get('status')}")
    
    print("\n" + "=" * 60)
    print("✅ Database is working correctly!")
    print("=" * 60)
    print(f"\n💡 In MongoDB Atlas, look for database: '{Config.DATABASE_NAME}'")
    print("   NOT the 'local' database!")
    
except Exception as e:
    print(f"\n❌ Error connecting to database: {e}")
    print("\nTroubleshooting:")
    print("1. Check if MongoDB is running")
    print("2. Verify MONGO_URI in config.py or .env file")
    print("3. Check network connection (if using MongoDB Atlas)")

