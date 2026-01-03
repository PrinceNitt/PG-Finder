"""
Database connection and management module.
Handles MongoDB connection with proper error handling and retries.
"""
import logging
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError
from config import Config

logger = logging.getLogger(__name__)

# Global database connection
_client = None
_db = None


def get_db():
    """
    Get database instance.
    Creates connection if not already established.
    
    Returns:
        Database instance
        
    Raises:
        ConnectionFailure: If unable to connect to MongoDB
    """
    global _db
    if _db is None:
        _client = get_client()
        _db = _client[Config.DATABASE_NAME]
    return _db


def get_client():
    """
    Get MongoDB client instance.
    Creates connection if not already established.
    
    Returns:
        MongoClient instance
        
    Raises:
        ConnectionFailure: If unable to connect to MongoDB
    """
    global _client
    if _client is None:
        try:
            # Handle SSL certificate issues for MongoDB Atlas on macOS
            client_options = {
                'serverSelectionTimeoutMS': 10000,  # 10 second timeout
                'connectTimeoutMS': 20000,
                'socketTimeoutMS': 30000,
                'retryWrites': True
            }
            
            # For MongoDB Atlas connections, handle SSL certificate verification
            if 'mongodb+srv' in Config.MONGO_URI or 'mongodb.net' in Config.MONGO_URI:
                # Fix SSL certificate verification error on macOS
                # This allows connection even if certificate verification fails
                # WARNING: Only for development, use proper certificates in production
                client_options['tlsAllowInvalidCertificates'] = True
            
            _client = MongoClient(Config.MONGO_URI, **client_options)
            # Test the connection
            _client.admin.command('ping')
            logger.info("Successfully connected to MongoDB")
        except (ConnectionFailure, ServerSelectionTimeoutError) as e:
            logger.error(f"Failed to connect to MongoDB: {e}")
            raise ConnectionFailure(f"Unable to connect to MongoDB: {e}")
    return _client


def close_connection():
    """Close MongoDB connection"""
    global _client, _db
    if _client:
        _client.close()
        _client = None
        _db = None
        logger.info("MongoDB connection closed")


def get_collection(collection_name):
    """
    Get a collection from the database.
    
    Args:
        collection_name: Name of the collection
        
    Returns:
        Collection instance
    """
    db = get_db()
    return db[collection_name]

