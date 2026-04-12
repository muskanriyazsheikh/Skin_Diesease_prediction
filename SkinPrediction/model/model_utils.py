"""
Model Utilities
===============
Helper functions for image preprocessing and model inference.
These functions are used by the Flask backend to make predictions.
"""

import os
import numpy as np
import json
from tensorflow.keras.models import load_model as keras_load_model
from tensorflow.keras.preprocessing import image as keras_image

# Configuration
MODEL_PATH = os.path.join(os.path.dirname(__file__), "skin_disease_model.h5")
CLASS_LABELS_PATH = os.path.join(os.path.dirname(__file__), "class_labels.json")
IMG_HEIGHT = 224  # MobileNetV2 requires 224x224
IMG_WIDTH = 224   # MobileNetV2 requires 224x224

# Global model variable (loaded once for efficiency)
_model = None
_class_labels = None


def load_model():
    """
    Load the trained CNN model from .h5 file.
    The model is cached to avoid reloading on every prediction.
    
    Returns:
        model: Loaded Keras model
    """
    global _model
    
    if _model is None:
        if not os.path.exists(MODEL_PATH):
            raise FileNotFoundError(
                f"Model file not found at {MODEL_PATH}. "
                "Please run train_model.py first."
            )
        
        print("Loading CNN model...")
        _model = keras_load_model(MODEL_PATH)
        print("✓ Model loaded successfully")
    
    return _model


def load_class_labels():
    """
    Load class labels from JSON file.
    
    Returns:
        dict: Dictionary mapping class names to indices
    """
    global _class_labels
    
    if _class_labels is None:
        if not os.path.exists(CLASS_LABELS_PATH):
            raise FileNotFoundError(
                f"Class labels file not found at {CLASS_LABELS_PATH}. "
                "Please run train_model.py first."
            )
        
        with open(CLASS_LABELS_PATH, 'r') as f:
            _class_labels = json.load(f)
        
        print(f"✓ Class labels loaded: {len(_class_labels)} classes")
    
    return _class_labels


def preprocess_image(image_path):
    """
    Preprocess an image for model prediction.
    
    Steps:
    1. Load image from file
    2. Resize to model input size (128x128)
    3. Convert to numpy array
    4. Add batch dimension
    5. Normalize pixel values to [0, 1]
    
    Args:
        image_path: Path to the image file
    
    Returns:
        numpy.ndarray: Preprocessed image array with shape (1, 128, 128, 3)
    """
    # Load and resize image
    img = keras_image.load_img(
        image_path, 
        target_size=(IMG_HEIGHT, IMG_WIDTH)
    )
    
    # Convert to numpy array
    img_array = keras_image.img_to_array(img)
    
    # Add batch dimension: (128, 128, 3) -> (1, 128, 128, 3)
    img_array = np.expand_dims(img_array, axis=0)
    
    # Normalize pixel values to [0, 1]
    img_array = img_array / 255.0
    
    return img_array


def get_prediction(image_path):
    """
    Make a prediction on a single image.
    
    Args:
        image_path: Path to the image file
    
    Returns:
        dict: Prediction results including:
            - disease: Predicted disease name
            - confidence: Confidence score (0-1)
            - all_probabilities: Probabilities for all classes
    """
    # Load model and class labels
    model = load_model()
    class_labels = load_class_labels()
    
    # Preprocess image
    img_array = preprocess_image(image_path)
    
    # Make prediction
    predictions = model.predict(img_array, verbose=0)
    
    # Get predicted class index and confidence
    predicted_idx = np.argmax(predictions[0])
    confidence = float(predictions[0][predicted_idx])
    
    # Map index to disease name
    reverse_labels = {idx: name for name, idx in class_labels.items()}
    predicted_disease = reverse_labels.get(predicted_idx, "Unknown")
    
    # Get all class probabilities
    all_probabilities = {}
    for class_name, class_idx in class_labels.items():
        all_probabilities[class_name] = float(predictions[0][class_idx])
    
    # Sort by probability (descending)
    all_probabilities = dict(
        sorted(all_probabilities.items(), key=lambda x: x[1], reverse=True)
    )
    
    return {
        "disease": predicted_disease,
        "confidence": confidence,
        "all_probabilities": all_probabilities
    }


# Example usage (for testing)
if __name__ == "__main__":
    print("Testing model utilities...")
    
    # Test loading model
    try:
        model = load_model()
        print("✓ Model loaded successfully")
    except Exception as e:
        print(f"✗ Error loading model: {e}")
    
    # Test loading class labels
    try:
        labels = load_class_labels()
        print(f"✓ Class labels: {labels}")
    except Exception as e:
        print(f"✗ Error loading class labels: {e}")
    
    print("\nUtilities ready for use!")
