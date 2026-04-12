"""
Model Evaluation Script
=======================
This script evaluates the trained CNN model on test data
and generates performance metrics and visualizations.

Metrics calculated:
- Accuracy, Precision, Recall, F1-Score
- Confusion Matrix
- Per-class performance
"""

import os
import numpy as np
import json
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import (
    classification_report, 
    confusion_matrix, 
    accuracy_score,
    precision_score,
    recall_score,
    f1_score
)
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import ImageDataGenerator

# Configuration
MODEL_PATH = "skin_disease_model.h5"
CLASS_LABELS_PATH = "class_labels.json"
DATASET_DIR = "../dataset"
IMG_HEIGHT = 224  # MobileNetV2 requires 224x224
IMG_WIDTH = 224   # MobileNetV2 requires 224x224
BATCH_SIZE = 32

# Output paths
CONFUSION_MATRIX_PATH = "confusion_matrix.png"
METRICS_PATH = "model_metrics.json"


def load_trained_model():
    """Load the trained model from .h5 file."""
    print("\n" + "="*60)
    print("Loading Trained Model")
    print("="*60)
    
    if not os.path.exists(MODEL_PATH):
        print(f"\n✗ Error: Model file '{MODEL_PATH}' not found!")
        print("Please run train_model.py first to train the model.")
        return None
    
    model = load_model(MODEL_PATH)
    print(f"✓ Model loaded from {MODEL_PATH}")
    return model


def create_test_generator():
    """Create test data generator (no augmentation)."""
    print("\n" + "="*60)
    print("Setting up Test Data Generator")
    print("="*60)
    
    test_datagen = ImageDataGenerator(rescale=1./255)
    
    test_generator = test_datagen.flow_from_directory(
        DATASET_DIR,
        target_size=(IMG_HEIGHT, IMG_WIDTH),
        batch_size=BATCH_SIZE,
        class_mode='categorical',
        shuffle=False
    )
    
    print(f"✓ Found {len(test_generator.classes)} test images")
    return test_generator


def evaluate_model(model, test_generator):
    """
    Evaluate model and calculate metrics.
    
    Args:
        model: Trained Keras model
        test_generator: Test data generator
    
    Returns:
        predictions: Model predictions
        true_labels: Ground truth labels
    """
    print("\n" + "="*60)
    print("Evaluating Model")
    print("="*60)
    
    # Get predictions
    predictions = model.predict(test_generator, verbose=1)
    predicted_classes = np.argmax(predictions, axis=1)
    true_classes = test_generator.classes
    
    # Calculate metrics
    accuracy = accuracy_score(true_classes, predicted_classes)
    precision = precision_score(true_classes, predicted_classes, average='weighted', zero_division=0)
    recall = recall_score(true_classes, predicted_classes, average='weighted', zero_division=0)
    f1 = f1_score(true_classes, predicted_classes, average='weighted', zero_division=0)
    
    print(f"\n{'='*60}")
    print(f"MODEL PERFORMANCE METRICS")
    print(f"{'='*60}")
    print(f"Accuracy:  {accuracy:.4f} ({accuracy*100:.2f}%)")
    print(f"Precision: {precision:.4f} ({precision*100:.2f}%)")
    print(f"Recall:    {recall:.4f} ({recall*100:.2f}%)")
    print(f"F1-Score:  {f1:.4f} ({f1*100:.2f}%)")
    
    # Classification report
    class_labels = list(test_generator.class_indices.keys())
    
    # Get unique labels present in true classes
    unique_labels = np.unique(true_classes)
    
    # Filter target names to only include classes present in test data
    target_names = [class_labels[i] for i in unique_labels]
    
    print(f"\n{'='*60}")
    print("CLASSIFICATION REPORT")
    print(f"{'='*60}")
    print(classification_report(
        true_classes, 
        predicted_classes, 
        labels=unique_labels,
        target_names=target_names,
        zero_division=0
    ))
    
    # Save metrics to JSON
    metrics = {
        "accuracy": float(accuracy),
        "precision": float(precision),
        "recall": float(recall),
        "f1_score": float(f1),
        "total_samples": len(true_classes),
        "class_names": class_labels
    }
    
    with open(METRICS_PATH, 'w') as f:
        json.dump(metrics, f, indent=2)
    
    print(f"✓ Metrics saved to {METRICS_PATH}")
    
    return predictions, true_classes


def plot_confusion_matrix(true_classes, predicted_classes, class_names):
    """
    Plot and save confusion matrix.
    
    Args:
        true_classes: Ground truth labels
        predicted_classes: Model predictions
        class_names: List of class names
    """
    print("\n" + "="*60)
    print("Generating Confusion Matrix")
    print("="*60)
    
    # Get unique labels present in the data
    unique_labels = np.unique(true_classes)
    
    # Filter class names to match unique labels
    filtered_class_names = [class_names[i] for i in unique_labels]
    
    # Calculate confusion matrix with only present labels
    cm = confusion_matrix(true_classes, predicted_classes, labels=unique_labels)
    
    # Plot
    plt.figure(figsize=(12, 10))
    sns.heatmap(
        cm, 
        annot=True, 
        fmt='d', 
        cmap='Blues',
        xticklabels=filtered_class_names,
        yticklabels=filtered_class_names,
        cbar_kws={'label': 'Count'}
    )
    
    plt.title('Confusion Matrix', fontsize=16, fontweight='bold', pad=20)
    plt.xlabel('Predicted Label', fontsize=12, fontweight='bold')
    plt.ylabel('True Label', fontsize=12, fontweight='bold')
    plt.xticks(rotation=45, ha='right')
    plt.yticks(rotation=0)
    plt.tight_layout()
    plt.savefig(CONFUSION_MATRIX_PATH, dpi=300, bbox_inches='tight')
    print(f"✓ Confusion matrix saved to {CONFUSION_MATRIX_PATH}")
    plt.close()


def main():
    """Main function to orchestrate model evaluation."""
    print("\n" + "="*60)
    print("SKIN DISEASE DETECTION - MODEL EVALUATION")
    print("="*60)
    
    # Step 1: Load model
    model = load_trained_model()
    if model is None:
        return
    
    # Step 2: Create test generator
    test_generator = create_test_generator()
    
    # Step 3: Evaluate model
    predictions, true_classes = evaluate_model(model, test_generator)
    
    # Step 4: Plot confusion matrix
    class_names = list(test_generator.class_indices.keys())
    plot_confusion_matrix(true_classes, predictions.argmax(axis=1), class_names)
    
    print("\n" + "="*60)
    print("EVALUATION COMPLETE!")
    print("="*60)
    print(f"✓ Confusion matrix: {CONFUSION_MATRIX_PATH}")
    print(f"✓ Model metrics: {METRICS_PATH}")
    print("\nThe model is ready for deployment!")


if __name__ == "__main__":
    main()
