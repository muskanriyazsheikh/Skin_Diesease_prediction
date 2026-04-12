"""
Configuration File
==================
Central configuration for the Flask application.
Contains database settings, file upload settings, and security configurations.
"""

import os
from datetime import timedelta
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Base directory
BASE_DIR = os.path.abspath(os.path.dirname(__file__))


class Config:
    """Base configuration class."""
    
    # Secret key for session management and CSRF protection
    # In production, set this via environment variable
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
    
    # Database configuration
    # SQLite database for storing prediction history
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DATABASE_URL',
        f'sqlite:///{os.path.join(BASE_DIR, "predictions.db")}'
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # File upload configuration
    UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads')
    MAX_CONTENT_LENGTH = 5 * 1024 * 1024  # 5 MB max file size
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
    
    # Model configuration
    MODEL_PATH = os.path.join(BASE_DIR, '..', 'model', 'skin_disease_model.h5')
    
    # Session configuration
    PERMANENT_SESSION_LIFETIME = timedelta(hours=1)
    
    # Logging configuration
    LOG_FOLDER = os.path.join(BASE_DIR, 'logs')
    
    @staticmethod
    def init_app(app):
        """Initialize application with configuration."""
        # Create necessary directories
        os.makedirs(Config.UPLOAD_FOLDER, exist_ok=True)
        os.makedirs(Config.LOG_FOLDER, exist_ok=True)


class DevelopmentConfig(Config):
    """Development configuration."""
    DEBUG = True
    TESTING = False


class ProductionConfig(Config):
    """Production configuration."""
    DEBUG = False
    TESTING = False
    # In production, these should be set via environment variables
    SECRET_KEY = os.environ.get('SECRET_KEY')
    DATABASE_URL = os.environ.get('DATABASE_URL')


class TestingConfig(Config):
    """Testing configuration."""
    TESTING = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'  # In-memory database for tests


# Configuration dictionary
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}
