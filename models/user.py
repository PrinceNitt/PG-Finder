"""
User model for database operations.
"""
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from models.database import get_collection
import logging

logger = logging.getLogger(__name__)


class User:
    """User model class"""
    
    def __init__(self, name, email, password=None, user_id=None, role='student'):
        self.user_id = user_id
        self.name = name
        self.email = email
        self.password = password
        self.role = role
        self.created_at = datetime.utcnow()
    
    @staticmethod
    def create(name, email, password, role='student'):
        """
        Create a new user.
        
        Args:
            name: User's full name
            email: User's email address
            password: Plain text password (will be hashed)
            role: User role (student, pg_owner, admin)
            
        Returns:
            User object if created successfully, None otherwise
            
        Raises:
            ValueError: If user already exists or validation fails
        """
        users_collection = get_collection('users')
        
        # Check if user already exists
        if users_collection.find_one({'email': email}):
            raise ValueError("Email already registered")
        
        # Validate input
        if not name or not name.strip():
            raise ValueError("Name is required")
        if not email or not email.strip():
            raise ValueError("Email is required")
        if not password or len(password) < 8:
            raise ValueError("Password must be at least 8 characters long")
        
        # Validate role
        valid_roles = ['student', 'pg_owner', 'admin']
        if role not in valid_roles:
            raise ValueError(f"Invalid role. Must be one of: {', '.join(valid_roles)}")
        
        # Create user document
        user_data = {
            'name': name.strip(),
            'email': email.strip().lower(),
            'password': generate_password_hash(password),
            'role': role,
            'created_at': datetime.utcnow(),
            'updated_at': datetime.utcnow()
        }
        
        try:
            result = users_collection.insert_one(user_data)
            logger.info(f"User created: {email} with role: {role}")
            return User(name, email, user_id=str(result.inserted_id), role=role)
        except Exception as e:
            logger.error(f"Error creating user: {e}")
            raise
    
    @staticmethod
    def find_by_email(email):
        """
        Find user by email.
        
        Args:
            email: User's email address
            
        Returns:
            User document if found, None otherwise
        """
        users_collection = get_collection('users')
        return users_collection.find_one({'email': email.lower().strip()})
    
    @staticmethod
    def authenticate(email, password):
        """
        Authenticate user with email and password.
        
        Args:
            email: User's email address
            password: Plain text password
            
        Returns:
            User document if authenticated, None otherwise
        """
        user = User.find_by_email(email)
        if user and check_password_hash(user['password'], password):
            return user
        return None
    
    @staticmethod
    def find_by_id(user_id):
        """
        Find user by ID.
        
        Args:
            user_id: User's ID (string or ObjectId)
            
        Returns:
            User document if found, None otherwise
        """
        from bson import ObjectId
        users_collection = get_collection('users')
        try:
            return users_collection.find_one({'_id': ObjectId(user_id)})
        except Exception:
            return None

