"""
Prediction Database Model
=========================
MongoDB schema for storing prediction history.
Each document contains information about a single prediction request.

MongoDB Schema (NoSQL - Schemaless but documented here for reference):
{
    "_id": ObjectId("..."),
    "image_filename": "abc123.jpg",
    "predicted_disease": "Melanocytic nevi",
    "confidence": 0.9234,
    "timestamp": ISODate("2026-04-10T14:30:00Z"),
    "ip_address": "192.168.1.100"
}
"""

from datetime import datetime, timezone
from bson import ObjectId


class Prediction:
    """
    Prediction model for MongoDB document operations.
    This is a helper class to work with MongoDB documents.
    """
    
    COLLECTION_NAME = 'predictions'
    
    def __init__(self, image_filename, predicted_disease, confidence, 
                 timestamp=None, ip_address=None, prediction_id=None):
        """
        Initialize a prediction document.
        
        Args:
            image_filename: Name of the uploaded image file
            predicted_disease: Name of the predicted skin disease
            confidence: Confidence score (0-1)
            timestamp: DateTime of prediction (default: now)
            ip_address: IP address of the user
            prediction_id: MongoDB ObjectId (for existing documents)
        """
        self.id = prediction_id
        self.image_filename = image_filename
        self.predicted_disease = predicted_disease
        self.confidence = confidence
        self.timestamp = timestamp or datetime.now(timezone.utc)
        self.ip_address = ip_address
    
    def to_dict(self):
        """
        Convert prediction object to dictionary for MongoDB insertion.
        
        Returns:
            dict: Prediction data as dictionary
        """
        return {
            'image_filename': self.image_filename,
            'predicted_disease': self.predicted_disease,
            'confidence': self.confidence,
            'timestamp': self.timestamp,
            'ip_address': self.ip_address
        }
    
    def to_json(self):
        """
        Convert prediction to JSON-serializable dictionary.
        
        Returns:
            dict: Prediction data with string ID and ISO timestamp
        """
        return {
            'id': str(self.id) if self.id else None,
            'image_filename': self.image_filename,
            'predicted_disease': self.predicted_disease,
            'confidence': self.confidence,
            'timestamp': self.timestamp.isoformat() if self.timestamp else None,
            'ip_address': self.ip_address
        }
    
    @staticmethod
    def from_mongo_doc(doc):
        """
        Create Prediction object from MongoDB document.
        
        Args:
            doc: MongoDB document dictionary
        
        Returns:
            Prediction: Prediction instance
        """
        return Prediction(
            image_filename=doc.get('image_filename'),
            predicted_disease=doc.get('predicted_disease'),
            confidence=doc.get('confidence'),
            timestamp=doc.get('timestamp'),
            ip_address=doc.get('ip_address'),
            prediction_id=doc.get('_id')
        )
    
    @staticmethod
    def create_indexes(mongo):
        """
        Create MongoDB indexes for better query performance.
        For backward compatibility - use create_indexes_direct instead.
        
        Args:
            mongo: Flask-PyMongo instance (deprecated)
        """
        try:
            collection = mongo.db.predictions
            
            # Create indexes
            collection.create_index([('timestamp', -1)])
            collection.create_index([('predicted_disease', 1)])
            collection.create_index([('confidence', 1)])
            
            print("✓ MongoDB indexes created")
        except Exception as e:
            print(f"⚠ Could not create indexes: {e}")
            raise
    
    @staticmethod
    def create_indexes_direct(db):
        """
        Create MongoDB indexes using direct database instance.
        
        Args:
            db: PyMongo database instance
        """
        try:
            collection = db.predictions
            
            # Create indexes
            collection.create_index([('timestamp', -1)])  # Descending timestamp for recent queries
            collection.create_index([('predicted_disease', 1)])  # Disease name for filtering
            collection.create_index([('confidence', 1)])  # Confidence for range queries
            
            print("✓ MongoDB indexes created")
        except Exception as e:
            print(f"⚠ Could not create indexes: {e}")
            raise
