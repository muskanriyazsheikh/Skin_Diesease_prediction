"""
Prediction Database Model
=========================
Stores prediction history in the database.
Each record contains information about a single prediction request.
"""

from datetime import datetime
from . import db


class Prediction(db.Model):
    """
    Prediction model for storing skin disease prediction results.
    
    Attributes:
        id: Unique identifier (primary key)
        image_filename: Name of the uploaded image file
        predicted_disease: Name of the predicted skin disease
        confidence: Confidence score of the prediction (0-1)
        timestamp: Date and time of the prediction
        ip_address: IP address of the user (for analytics)
    """
    
    __tablename__ = 'predictions'
    
    id = db.Column(db.Integer, primary_key=True)
    image_filename = db.Column(db.String(255), nullable=False)
    predicted_disease = db.Column(db.String(100), nullable=False)
    confidence = db.Column(db.Float, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    ip_address = db.Column(db.String(50), nullable=True)
    
    def to_dict(self):
        """
        Convert prediction object to dictionary.
        
        Returns:
            dict: Prediction data as dictionary
        """
        return {
            'id': self.id,
            'image_filename': self.image_filename,
            'predicted_disease': self.predicted_disease,
            'confidence': self.confidence,
            'timestamp': self.timestamp.isoformat(),
            'ip_address': self.ip_address
        }
    
    def __repr__(self):
        """String representation of the prediction."""
        return f'<Prediction {self.predicted_disease} ({self.confidence:.2%})>'
