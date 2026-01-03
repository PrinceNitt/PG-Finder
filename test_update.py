"""
Test script to verify database updates are working
"""
from models.database import get_collection
from models.user import User
from datetime import datetime
import time

print("=" * 60)
print("Testing Database Updates")
print("=" * 60)

# Test 1: Create a new user
print("\n1. Testing User Creation...")
try:
    test_email = f"test_{int(time.time())}@example.com"
    user = User.create(
        name="Test User",
        email=test_email,
        password="test123456",
        role="student"
    )
    print(f"   ✅ User created: {test_email}")
    
    # Verify it exists
    found = User.find_by_email(test_email)
    if found:
        print(f"   ✅ User found in database: {found.get('name')}")
    else:
        print("   ❌ User NOT found in database!")
        
except Exception as e:
    print(f"   ❌ Error: {e}")

# Test 2: Check current counts
print("\n2. Current Database Counts...")
try:
    users = get_collection('users')
    pgs = get_collection('pg_listings')
    requests = get_collection('join_requests')
    
    user_count = users.count_documents({})
    pg_count = pgs.count_documents({})
    req_count = requests.count_documents({})
    
    print(f"   Users: {user_count}")
    print(f"   PG Listings: {pg_count}")
    print(f"   Join Requests: {req_count}")
    
except Exception as e:
    print(f"   ❌ Error: {e}")

# Test 3: Check most recent documents
print("\n3. Most Recent Documents...")
try:
    users = get_collection('users')
    recent_users = list(users.find({}, {'name': 1, 'email': 1, 'created_at': 1})
                       .sort('created_at', -1).limit(3))
    
    print("   Recent Users:")
    for u in recent_users:
        created = u.get('created_at', 'N/A')
        if isinstance(created, datetime):
            created = created.strftime('%Y-%m-%d %H:%M:%S')
        print(f"     - {u.get('name')} ({u.get('email')}) - {created}")
        
except Exception as e:
    print(f"   ❌ Error: {e}")

print("\n" + "=" * 60)
print("✅ Database update test complete!")
print("=" * 60)
print("\n💡 If updates are not visible in MongoDB Atlas:")
print("   1. Check if you're using LOCAL MongoDB (not Atlas)")
print("   2. Refresh MongoDB Atlas page")
print("   3. Check the correct database: 'pgfinder_db'")
print("   4. Verify application is running when making changes")

