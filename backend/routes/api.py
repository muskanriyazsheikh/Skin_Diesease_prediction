"""
API Routes
==========
REST API endpoints for skin disease prediction.

Endpoints:
- POST /api/predict - Upload image and get prediction
- GET /api/health - Check API status
- GET /api/history - Get prediction history
"""

import os
import sys
import logging
from datetime import datetime
from flask import Blueprint, request, jsonify, current_app

# Add parent directory to path for model imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

from extensions import get_mongo_db
from models.prediction import Prediction
from utils.file_handler import save_uploaded_file, delete_file
from utils.disease_info import DISEASE_INFO, MEDICAL_DISCLAIMER

# Import model utilities
try:
    from model.model_utils import get_prediction
    MODEL_AVAILABLE = True
except ImportError:
    MODEL_AVAILABLE = False
    print("Warning: Model not available. Running in demo mode.")

# Configure logging
logger = logging.getLogger(__name__)

# Create blueprint
api_bp = Blueprint('api', __name__, url_prefix='/api')


@api_bp.route('/health', methods=['GET'])
def health_check():
    """
    Health check endpoint.
    Returns API status, model availability, and database status.
    """
    try:
        # Check MongoDB connection
        db = get_mongo_db()
        if db is not None:
            db.command('ping')
            db_status = "connected"
        else:
            db_status = "not initialized"
    except Exception as e:
        db_status = f"error: {str(e)}"
    
    response = {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "model_loaded": MODEL_AVAILABLE,
        "database": db_status,
        "database_type": "MongoDB",
        "version": "1.0.0"
    }
    
    return jsonify(response), 200


@api_bp.route('/predict', methods=['POST'])
def predict():
    """
    Predict skin disease from uploaded image.
    
    Expects:
        - multipart/form-data with 'image' field
    
    Returns:
        JSON with prediction results including:
        - disease: Predicted disease name
        - confidence: Confidence score (0-1)
        - description: Disease description
        - treatment: Treatment recommendations
        - precautions: List of precautions
        - disclaimer: Medical disclaimer
    """
    # Check if image is provided
    if 'image' not in request.files:
        return jsonify({
            "error": "No image provided",
            "message": "Please upload an image file"
        }), 400
    
    image_file = request.files['image']
    
    # Validate and save image
    filename, error = save_uploaded_file(image_file)
    if error:
        return jsonify({
            "error": "Invalid file",
            "message": error
        }), 400
    
    try:
        # Get file path
        filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        
        # Make prediction
        if MODEL_AVAILABLE:
            # Use actual model
            prediction_result = get_prediction(filepath)
        else:
            # Demo mode - return mock prediction
            prediction_result = {
                "disease": "Melanocytic nevi",
                "confidence": 0.85,
                "all_probabilities": {
                    "Melanocytic nevi": 0.85,
                    "Benign keratosis-like lesions": 0.08,
                    "Dermatofibroma": 0.04,
                    "Vascular lesions": 0.02,
                    "Actinic keratoses": 0.005,
                    "Basal cell carcinoma": 0.003,
                    "Melanoma": 0.002
                }
            }
            logger.warning("Running in demo mode - using mock prediction")
        
        # Get disease information
        disease_name = prediction_result['disease']
        disease_data = DISEASE_INFO.get(disease_name, {})
        
        # Save prediction to MongoDB
        try:
            prediction_doc = Prediction(
                image_filename=filename,
                predicted_disease=disease_name,
                confidence=prediction_result['confidence'],
                ip_address=request.remote_addr
            )
            
            # Insert into MongoDB
            db = get_mongo_db()
            if db is not None:
                result = db.predictions.insert_one(prediction_doc.to_dict())
                logger.info(f"✓ Prediction saved to MongoDB with ID: {result.inserted_id}")
            else:
                logger.error("MongoDB connection is not initialized!")
        except Exception as db_error:
            logger.error(f"MongoDB error: {str(db_error)}")
        
        # Build response
        response = {
            "success": True,
            "prediction": {
                "disease": disease_name,
                "confidence": prediction_result['confidence'],
                "all_probabilities": prediction_result.get('all_probabilities', {})
            },
            "disease_info": {
                "description": disease_data.get('description', 'No information available'),
                "symptoms": disease_data.get('symptoms', []),
                "treatment": disease_data.get('treatment', 'Consult a dermatologist'),
                "precautions": disease_data.get('precautions', []),
                "severity": disease_data.get('severity', 'Unknown'),
                "consultation": disease_data.get('consultation', 'Consult a dermatologist')
            },
            "disclaimer": MEDICAL_DISCLAIMER,
            "timestamp": datetime.utcnow().isoformat()
        }
        
        return jsonify(response), 200
    
    except Exception as e:
        logger.error(f"Prediction error: {str(e)}")
        
        # Clean up uploaded file on error
        delete_file(filename)
        
        return jsonify({
            "error": "Prediction failed",
            "message": f"An error occurred during prediction: {str(e)}"
        }), 500


@api_bp.route('/history', methods=['GET'])
def get_history():
    """
    Get recent prediction history.
    
    Query parameters:
        - limit: Number of records to return (default: 10, max: 100)
    
    Returns:
        JSON list of recent predictions
    """
    try:
        # Get limit from query parameters
        limit = request.args.get('limit', 10, type=int)
        limit = min(limit, 100)  # Cap at 100
        
        # Query recent predictions from MongoDB
        db = get_mongo_db()
        if db is not None:
            predictions_cursor = db.predictions.find().sort('timestamp', -1).limit(limit)
            
            # Convert to list of dictionaries
            history = []
            for doc in predictions_cursor:
                doc['id'] = str(doc.pop('_id'))
                if 'timestamp' in doc and hasattr(doc['timestamp'], 'isoformat'):
                    doc['timestamp'] = doc['timestamp'].isoformat()
                history.append(doc)
        else:
            history = []
        
        return jsonify({
            "success": True,
            "count": len(history),
            "predictions": history
        }), 200
    
    except Exception as e:
        logger.error(f"Error fetching history: {str(e)}")
        return jsonify({
            "error": "Failed to fetch history",
            "message": str(e)
        }), 500


@api_bp.route('/diseases', methods=['GET'])
def get_diseases_info():
    """
    Get information about all detectable diseases.
    
    Returns:
        JSON with disease information for all classes
    """
    return jsonify({
        "success": True,
        "diseases": DISEASE_INFO,
        "disclaimer": MEDICAL_DISCLAIMER
    }), 200


# Error handlers
@api_bp.errorhandler(413)
def request_entity_too_large(error):
    """Handle file too large error."""
    return jsonify({
        "error": "File too large",
        "message": "Maximum file size is 5MB"
    }), 413


@api_bp.errorhandler(500)
def internal_server_error(error):
    """Handle internal server error."""
    logger.error(f"Internal server error: {str(error)}")
    return jsonify({
        "error": "Internal server error",
        "message": "An unexpected error occurred"
    }), 500
