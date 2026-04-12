"""
Main Flask Application
======================
Entry point for the Skin Disease Detection API.
Initializes the Flask app, database, and registers routes.
"""

import os
import logging
from logging.handlers import RotatingFileHandler
from flask import Flask, jsonify
from flask_cors import CORS

from config import config
from routes.api import api_bp
from extensions import init_mongo


def create_app(config_name=None):
    """
    Application factory function.
    Creates and configures the Flask application.
    
    Args:
        config_name: Configuration environment ('development', 'production', 'testing')
    
    Returns:
        Flask: Configured Flask application instance
    """
    if config_name is None:
        config_name = os.environ.get('FLASK_ENV', 'default')
    
    # Create Flask app
    app = Flask(__name__)
    
    # Load configuration
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    
    # Initialize MongoDB
    if app.config.get('MONGO_URI'):
        init_mongo(app)
        print(f"✓ MongoDB initialized successfully")
    else:
        print("⚠ MONGO_URI not found in configuration")
    
    # Configure CORS (Cross-Origin Resource Sharing)
    # Allows frontend to make requests to this backend
    CORS(app, resources={
        r"/api/*": {
            "origins": os.environ.get('FRONTEND_URL', '*').split(','),
            "methods": ["GET", "POST", "OPTIONS"],
            "allow_headers": ["Content-Type"]
        }
    })
    
    # Register blueprints (routes)
    app.register_blueprint(api_bp)
    
    # Configure logging
    setup_logging(app)
    
    # Create MongoDB indexes on startup
    with app.app_context():
        try:
            from extensions import get_mongo_db
            from models.prediction import Prediction
            
            db = get_mongo_db()
            if db is not None:
                db.command('ping')  # Test connection
                Prediction.create_indexes_direct(db)
                logging.info("✓ MongoDB indexes created")
        except Exception as e:
            logging.warning(f"Could not create indexes: {e}")
    
    # Root endpoint
    @app.route('/')
    def index():
        """Root endpoint with API information."""
        return jsonify({
            "name": "Skin Disease Detection API",
            "version": "1.0.0",
            "description": "AI-powered skin disease classification using CNN",
            "endpoints": {
                "health": "GET /api/health",
                "predict": "POST /api/predict",
                "history": "GET /api/history",
                "diseases": "GET /api/diseases"
            },
            "documentation": "See README.md for full documentation"
        })
    
    # Error handlers
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "error": "Not found",
            "message": "The requested endpoint does not exist"
        }), 404
    
    @app.errorhandler(405)
    def method_not_allowed(error):
        return jsonify({
            "error": "Method not allowed",
            "message": "The HTTP method is not allowed for this endpoint"
        }), 405
    
    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({
            "error": "Internal server error",
            "message": "An unexpected error occurred"
        }), 500
    
    return app


def setup_logging(app):
    """
    Configure application logging.
    
    Args:
        app: Flask application instance
    """
    if not app.debug and not app.testing:
        # Create log directory
        log_folder = app.config.get('LOG_FOLDER', 'logs')
        os.makedirs(log_folder, exist_ok=True)
        
        # File handler with rotation
        file_handler = RotatingFileHandler(
            os.path.join(log_folder, 'skin_detection.log'),
            maxBytes=10 * 1024 * 1024,  # 10MB
            backupCount=5
        )
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        ))
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)
        
        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(logging.Formatter(
            '%(asctime)s - %(levelname)s - %(message)s'
        ))
        app.logger.addHandler(console_handler)
        
        app.logger.setLevel(logging.INFO)
        app.logger.info('Skin Disease Detection API starting up')


# Create application instance
app = create_app()


if __name__ == '__main__':
    # Run development server
    # For production, use: gunicorn app:app
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True
    )
