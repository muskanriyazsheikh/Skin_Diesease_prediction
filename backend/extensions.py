"""
Flask Extensions
=================
Initialize all Flask extensions here to avoid circular imports.
"""

from pymongo import MongoClient

# MongoDB instances
_mongo_client = None
_mongo_db = None


def init_mongo(app):
    """
    Initialize MongoDB connection.
    
    Args:
        app: Flask application instance
    
    Returns:
        MongoDB database instance
    """
    global _mongo_client, _mongo_db
    
    mongo_uri = app.config.get('MONGO_URI', 'mongodb://localhost:27017/')
    db_name = app.config.get('MONGO_DBNAME', 'skin_prediction_db')
    
    try:
        _mongo_client = MongoClient(mongo_uri, serverSelectionTimeoutMS=5000)
        # Test connection
        _mongo_client.admin.command('ping')
        _mongo_db = _mongo_client[db_name]
        
        print(f"✓ MongoDB connected to: {mongo_uri}{db_name}")
        return _mongo_db
    except Exception as e:
        print(f"❌ MongoDB connection failed: {e}")
        raise


def get_mongo_db():
    """
    Get MongoDB database instance.
    
    Returns:
        MongoDB database instance or None
    """
    return _mongo_db


def get_mongo_client():
    """
    Get MongoDB client instance.
    
    Returns:
        MongoDB client instance or None
    """
    return _mongo_client
