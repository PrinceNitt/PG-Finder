"""
Script to insert sample data for testing the PG Assistant System.
Run this script to populate the database with sample users, PG listings, and requests.
"""
from models.database import get_db, get_collection
from models.user import User
from models.pg_listing import PGListing
from models.join_request import JoinRequest
from bson import ObjectId
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def insert_sample_data():
    """Insert sample data into the database"""
    
    print("=" * 60)
    print("Inserting Sample Data for PG Assistant System")
    print("=" * 60)
    
    # Clear existing data (optional - comment out if you want to keep existing data)
    # print("\nClearing existing data...")
    # get_collection('users').delete_many({})
    # get_collection('pg_listings').delete_many({})
    # get_collection('join_requests').delete_many({})
    
    # 1. Create Sample Users
    print("\n1. Creating sample users...")
    
    users_data = [
        {
            'name': 'John Student',
            'email': 'student@example.com',
            'password': 'student123',
            'role': 'student'
        },
        {
            'name': 'Sarah Student',
            'email': 'sarah@example.com',
            'password': 'student123',
            'role': 'student'
        },
        {
            'name': 'Rajesh Kumar',
            'email': 'pgowner1@example.com',
            'password': 'owner123',
            'role': 'pg_owner'
        },
        {
            'name': 'Priya Sharma',
            'email': 'pgowner2@example.com',
            'password': 'owner123',
            'role': 'pg_owner'
        },
        {
            'name': 'Admin User',
            'email': 'admin@example.com',
            'password': 'admin123',
            'role': 'admin'
        }
    ]
    
    created_users = {}
    for user_data in users_data:
        try:
            # Check if user already exists
            existing = User.find_by_email(user_data['email'])
            if existing:
                print(f"  User {user_data['email']} already exists, skipping...")
                created_users[user_data['email']] = existing
            else:
                user = User.create(
                    user_data['name'],
                    user_data['email'],
                    user_data['password'],
                    user_data['role']
                )
                created_users[user_data['email']] = User.find_by_email(user_data['email'])
                print(f"  ✓ Created user: {user_data['name']} ({user_data['email']}) - Role: {user_data['role']}")
        except Exception as e:
            print(f"  ✗ Error creating user {user_data['email']}: {e}")
    
    # 2. Create Sample PG Listings
    print("\n2. Creating sample PG listings...")
    
    pg_owner1_id = str(created_users['pgowner1@example.com']['_id'])
    pg_owner2_id = str(created_users['pgowner2@example.com']['_id'])
    
    pg_listings_data = [
        {
            'owner_id': pg_owner1_id,
            'name': 'Green Valley PG',
            'address': '123 Main Street, Sector 5',
            'city': 'Delhi',
            'state': 'Delhi',
            'pincode': '110001',
            'rent': 8000,
            'deposit': 10000,
            'available_rooms': 3,
            'total_rooms': 10,
            'facilities': ['WiFi', 'AC', 'Food', 'Laundry', 'Power Backup', 'Security'],
            'description': 'A comfortable and secure PG accommodation near Delhi University. Well-maintained rooms with all modern facilities.',
            'contact_phone': '+91-9876543210',
            'contact_email': 'greenvalley@example.com',
            'nearby_colleges': ['Delhi University', 'Jawaharlal Nehru University', 'DU North Campus'],
            'nearby_workplaces': ['Connaught Place', 'CP Business District'],
            'status': 'approved',
            'is_verified': True
        },
        {
            'owner_id': pg_owner1_id,
            'name': 'Sunshine Hostel',
            'address': '456 Park Avenue, MG Road',
            'city': 'Bangalore',
            'state': 'Karnataka',
            'pincode': '560001',
            'rent': 12000,
            'deposit': 15000,
            'available_rooms': 2,
            'total_rooms': 8,
            'facilities': ['WiFi', 'AC', 'Food', 'Laundry', 'Gym', 'TV', 'Refrigerator'],
            'description': 'Premium PG accommodation in the heart of Bangalore. Close to IT parks and educational institutions.',
            'contact_phone': '+91-9876543211',
            'contact_email': 'sunshine@example.com',
            'nearby_colleges': ['Bangalore University', 'Christ University'],
            'nearby_workplaces': ['IT Park', 'Whitefield', 'Electronic City'],
            'status': 'approved',
            'is_verified': True
        },
        {
            'owner_id': pg_owner2_id,
            'name': 'Comfort Zone PG',
            'address': '789 College Road, Andheri',
            'city': 'Mumbai',
            'state': 'Maharashtra',
            'pincode': '400053',
            'rent': 15000,
            'deposit': 20000,
            'available_rooms': 1,
            'total_rooms': 6,
            'facilities': ['WiFi', 'AC', 'Food', 'Laundry', 'Security', 'Parking', 'Geyser'],
            'description': 'Affordable PG in Mumbai with excellent connectivity. Safe and secure environment for students and professionals.',
            'contact_phone': '+91-9876543212',
            'contact_email': 'comfortzone@example.com',
            'nearby_colleges': ['Mumbai University', 'IIT Bombay'],
            'nearby_workplaces': ['Bandra Kurla Complex', 'Andheri Business District'],
            'status': 'approved',
            'is_verified': True
        },
        {
            'owner_id': pg_owner2_id,
            'name': 'Student Hub PG',
            'address': '321 University Street',
            'city': 'Pune',
            'state': 'Maharashtra',
            'pincode': '411007',
            'rent': 7000,
            'deposit': 8000,
            'available_rooms': 4,
            'total_rooms': 12,
            'facilities': ['WiFi', 'Food', 'Laundry', 'Study Table', 'Cupboard', 'Housekeeping'],
            'description': 'Budget-friendly PG perfect for students. Clean rooms with essential facilities at affordable rates.',
            'contact_phone': '+91-9876543213',
            'contact_email': 'studenthub@example.com',
            'nearby_colleges': ['Pune University', 'Fergusson College', 'Symbiosis'],
            'nearby_workplaces': ['Hinjewadi IT Park', 'Kharadi'],
            'status': 'pending',
            'is_verified': False
        },
        {
            'owner_id': pg_owner1_id,
            'name': 'Elite Residency',
            'address': '555 Luxury Lane, Banjara Hills',
            'city': 'Hyderabad',
            'state': 'Telangana',
            'pincode': '500034',
            'rent': 18000,
            'deposit': 25000,
            'available_rooms': 2,
            'total_rooms': 5,
            'facilities': ['WiFi', 'AC', 'Food', 'Laundry', 'Gym', 'TV', 'Refrigerator', 'Washing Machine', 'Geyser', 'Housekeeping'],
            'description': 'Premium accommodation with all modern amenities. Perfect for working professionals seeking comfort and convenience.',
            'contact_phone': '+91-9876543214',
            'contact_email': 'elite@example.com',
            'nearby_colleges': ['Osmania University', 'Hyderabad University'],
            'nearby_workplaces': ['HITEC City', 'Gachibowli', 'Financial District'],
            'status': 'approved',
            'is_verified': True
        }
    ]
    
    created_pgs = []
    for pg_data in pg_listings_data:
        try:
            # Check if PG already exists
            existing = get_collection('pg_listings').find_one({
                'name': pg_data['name'],
                'owner_id': ObjectId(pg_data['owner_id'])
            })
            
            if existing:
                print(f"  PG '{pg_data['name']}' already exists, skipping...")
                created_pgs.append(existing)
            else:
                pg = PGListing.create(
                    owner_id=pg_data['owner_id'],
                    name=pg_data['name'],
                    address=pg_data['address'],
                    city=pg_data['city'],
                    state=pg_data['state'],
                    pincode=pg_data['pincode'],
                    rent=pg_data['rent'],
                    deposit=pg_data['deposit'],
                    available_rooms=pg_data['available_rooms'],
                    total_rooms=pg_data['total_rooms'],
                    facilities=pg_data['facilities'],
                    description=pg_data['description'],
                    contact_phone=pg_data['contact_phone'],
                    contact_email=pg_data['contact_email'],
                    nearby_colleges=pg_data['nearby_colleges'],
                    nearby_workplaces=pg_data['nearby_workplaces']
                )
                
                # Update status and verification
                PGListing.update(str(pg['_id']), status=pg_data['status'], is_verified=pg_data['is_verified'])
                
                created_pgs.append(pg)
                print(f"  ✓ Created PG: {pg_data['name']} in {pg_data['city']} - Status: {pg_data['status']}")
        except Exception as e:
            print(f"  ✗ Error creating PG {pg_data['name']}: {e}")
    
    # 3. Create Sample Join Requests
    print("\n3. Creating sample join requests...")
    
    student1_id = str(created_users['student@example.com']['_id'])
    student2_id = str(created_users['sarah@example.com']['_id'])
    
    # Get some approved PGs
    approved_pgs = [pg for pg in created_pgs if pg.get('status') == 'approved' and pg.get('available_rooms', 0) > 0]
    
    if approved_pgs:
        requests_data = [
            {
                'student_id': student1_id,
                'pg_id': str(approved_pgs[0]['_id']),
                'message': 'Hi, I am interested in your PG. I am a student at Delhi University. Please let me know if a room is available.',
                'status': 'pending'
            },
            {
                'student_id': student2_id,
                'pg_id': str(approved_pgs[0]['_id']),
                'message': 'Hello, I would like to join your PG. I am a working professional. Can you share more details?',
                'status': 'approved'
            },
            {
                'student_id': student1_id,
                'pg_id': str(approved_pgs[1]['_id']) if len(approved_pgs) > 1 else str(approved_pgs[0]['_id']),
                'message': 'Interested in accommodation near IT Park.',
                'status': 'pending'
            }
        ]
        
        for req_data in requests_data:
            try:
                # Check if request already exists
                existing = get_collection('join_requests').find_one({
                    'student_id': ObjectId(req_data['student_id']),
                    'pg_id': ObjectId(req_data['pg_id'])
                })
                
                if existing:
                    print(f"  Request already exists, skipping...")
                else:
                    req = JoinRequest.create(
                        req_data['student_id'],
                        req_data['pg_id'],
                        req_data['message']
                    )
                    
                    # Update status if needed
                    if req_data['status'] != 'pending':
                        JoinRequest.update_status(str(req['_id']), req_data['status'])
                    
                    print(f"  ✓ Created join request - Status: {req_data['status']}")
            except Exception as e:
                print(f"  ✗ Error creating join request: {e}")
    
    print("\n" + "=" * 60)
    print("Sample Data Insertion Complete!")
    print("=" * 60)
    print("\nTest Accounts Created:")
    print("\nStudents:")
    print("  - Email: student@example.com, Password: student123")
    print("  - Email: sarah@example.com, Password: student123")
    print("\nPG Owners:")
    print("  - Email: pgowner1@example.com, Password: owner123")
    print("  - Email: pgowner2@example.com, Password: owner123")
    print("\nAdmin:")
    print("  - Email: admin@example.com, Password: admin123")
    print("\nSample PGs Created:")
    for pg in created_pgs:
        print(f"  - {pg['name']} in {pg['city']} (Status: {pg.get('status', 'pending')})")
    print("\nYou can now login and test the system!")
    print("=" * 60)


if __name__ == '__main__':
    try:
        # Test database connection
        get_db()
        print("Database connection successful!\n")
        insert_sample_data()
    except Exception as e:
        print(f"\nError: {e}")
        print("\nMake sure MongoDB is running and the connection is configured correctly.")
        print("Check your MONGO_URI in config.py or .env file.")

