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
            # Handle SSL certificate issues using certifi
            import certifi
            
            client_options = {
                'serverSelectionTimeoutMS': 10000,
                'connectTimeoutMS': 20000,
                'socketTimeoutMS': 30000,
                'retryWrites': True,
                'tls': True,
                'tlsCAFile': certifi.where(),  # Explicitly use certifi CA bundle
                'connect': False  # Lazy connection to handle Gunicorn forking safely
            }
            
            # Allow disabling SSL verification via environment variable (Escape hatch for Render)
            if os.getenv('MONGO_TLS_DISABLE', 'false').lower() == 'true':
                logger.warning("MongoDB TLS verification disabled by environment variable.")
                client_options['tlsAllowInvalidCertificates'] = True
                # When disabling verification, we might need to relax hostname check too
                client_options['tlsAllowInvalidHostnames'] = True
            
            logger.info(f"Connecting to MongoDB using certifi at: {certifi.where()}")
            
            _client = MongoClient(Config.MONGO_URI, **client_options)
            
            # Test the connection
            _client.admin.command('ping')
            logger.info("Successfully connected to MongoDB")
        except (ConnectionFailure, ServerSelectionTimeoutError) as e:
            logger.error(f"Failed to connect to MongoDB: {e}")
            raise ConnectionFailure(f"Unable to connect to MongoDB: {e}")
        except ImportError:
            logger.error("certifi module not found. Please add certifi to requirements.txt")
            raise
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

