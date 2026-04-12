"""
File Handler Utilities
======================
Helper functions for secure file upload handling.
Includes validation, secure filename generation, and cleanup.
"""

import os
import uuid
import logging
from werkzeug.utils import secure_filename
from flask import current_app

# Configure logging
logger = logging.getLogger(__name__)


def allowed_file(filename):
    """
    Check if the uploaded file has an allowed extension.
    
    Args:
        filename: Name of the file to check
    
    Returns:
        bool: True if file extension is allowed, False otherwise
    """
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']


def generate_secure_filename(original_filename):
    """
    Generate a secure, unique filename while preserving the original extension.
    
    This prevents filename conflicts and potential security issues.
    
    Args:
        original_filename: Original filename from upload
    
    Returns:
        str: Secure unique filename
    """
    # Get the file extension
    ext = original_filename.rsplit('.', 1)[1].lower() if '.' in original_filename else 'jpg'
    
    # Generate unique filename using UUID
    unique_filename = f"{uuid.uuid4().hex}.{ext}"
    
    return unique_filename


def validate_image(file):
    """
    Validate uploaded image file.
    
    Checks:
    - File exists
    - File has allowed extension
    - File size is within limits
    
    Args:
        file: File object from request.files
    
    Returns:
        tuple: (is_valid: bool, error_message: str)
    """
    if not file or file.filename == '':
        return False, "No file selected"
    
    if not allowed_file(file.filename):
        allowed = ', '.join(current_app.config['ALLOWED_EXTENSIONS'])
        return False, f"File type not allowed. Allowed types: {allowed}"
    
    # Check file size (in bytes)
    file.seek(0, os.SEEK_END)
    file_size = file.tell()
    file.seek(0)  # Reset file pointer
    
    max_size = current_app.config['MAX_CONTENT_LENGTH']
    if file_size > max_size:
        max_mb = max_size / (1024 * 1024)
        return False, f"File too large. Maximum size: {max_mb}MB"
    
    return True, ""


def save_uploaded_file(file):
    """
    Save uploaded file to the upload folder.
    
    Args:
        file: File object from request.files
    
    Returns:
        tuple: (filename: str, error_message: str)
    """
    try:
        # Validate file
        is_valid, error_msg = validate_image(file)
        if not is_valid:
            return None, error_msg
        
        # Generate secure filename
        filename = generate_secure_filename(file.filename)
        
        # Get upload folder path
        upload_folder = current_app.config['UPLOAD_FOLDER']
        os.makedirs(upload_folder, exist_ok=True)
        
        # Save file
        filepath = os.path.join(upload_folder, filename)
        file.save(filepath)
        
        logger.info(f"File saved: {filename}")
        return filename, ""
    
    except Exception as e:
        logger.error(f"Error saving file: {str(e)}")
        return None, f"Error saving file: {str(e)}"


def delete_file(filename):
    """
    Delete a file from the upload folder.
    
    Args:
        filename: Name of file to delete
    
    Returns:
        bool: True if deleted successfully, False otherwise
    """
    try:
        filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        if os.path.exists(filepath):
            os.remove(filepath)
            logger.info(f"File deleted: {filename}")
            return True
        return False
    except Exception as e:
        logger.error(f"Error deleting file {filename}: {str(e)}")
        return False


def cleanup_old_files(max_age_hours=24):
    """
    Delete files older than specified age to save disk space.
    
    Args:
        max_age_hours: Maximum age in hours before deletion
    
    Returns:
        int: Number of files deleted
    """
    import time
    
    upload_folder = current_app.config['UPLOAD_FOLDER']
    if not os.path.exists(upload_folder):
        return 0
    
    current_time = time.time()
    max_age_seconds = max_age_hours * 3600
    deleted_count = 0
    
    try:
        for filename in os.listdir(upload_folder):
            filepath = os.path.join(upload_folder, filename)
            file_age = current_time - os.path.getctime(filepath)
            
            if file_age > max_age_seconds:
                os.remove(filepath)
                deleted_count += 1
                logger.info(f"Cleaned up old file: {filename}")
    
    except Exception as e:
        logger.error(f"Error during cleanup: {str(e)}")
    
    return deleted_count
