"""
Skin Disease Detection Model Training Script
=============================================
This script trains a CNN model for skin disease classification
using the HAM10000 dataset or similar skin lesion datasets.

The model classifies 7 types of skin conditions:
1. Melanocytic nevi (nv)
2. Melanoma (mel)
3. Benign keratosis-like lesions (bkl)
4. Basal cell carcinoma (bcc)
5. Actinic keratoses (akiec)
6. Vascular lesions (vas)
7. Dermatofibroma (df)
"""

import os
import numpy as np
import matplotlib.pyplot as plt
import json
from pathlib import Path

import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers, models
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.callbacks import EarlyStopping, ReduceLROnPlateau, ModelCheckpoint

# Configuration
DATASET_DIR = "../dataset_combined"  # Change to "../dataset_combined" for HAM10000+ISIC
MODEL_SAVE_PATH = "skin_disease_model.h5"
CLASS_LABELS_PATH = "class_labels.json"
HISTORY_PLOT_PATH = "training_history.png"

# Model parameters
IMG_HEIGHT = 224  # MobileNetV2 requires 224x224
IMG_WIDTH = 224   # MobileNetV2 requires 224x224
BATCH_SIZE = 32
EPOCHS = 50
EPOCHS_FINE_TUNE = 30  # Additional epochs for fine-tuning
NUM_CLASSES = 7

# Advanced training options
USE_CLASS_WEIGHTS = True  # Handle class imbalance
USE_FINE_TUNING = True    # Enable fine-tuning phase
FINE_TUNE_FROM_LAYER = 100  # Unfreeze layers from this index

# Class labels (HAM10000 dataset)
CLASS_LABELS = {
    'akiec': 'Actinic keratoses',
    'bcc': 'Basal cell carcinoma',
    'bkl': 'Benign keratosis-like lesions',
    'df': 'Dermatofibroma',
    'mel': 'Melanoma',
    'nv': 'Melanocytic nevi',
    'vas': 'Vascular lesions'
}


def create_data_generators():
    """
    Create training and validation data generators with advanced augmentation.
    
    Returns:
        train_generator: Training data generator
        val_generator: Validation data generator
        train_steps: Number of training steps per epoch
        val_steps: Number of validation steps per epoch
        class_weights: Class weights for handling imbalance
    """
    print("\n" + "="*60)
    print("Setting up Data Generators with Advanced Augmentation")
    print("="*60)
    
    # Enhanced training data augmentation for better generalization
    train_datagen = ImageDataGenerator(
        rescale=1./255,              # Normalize pixel values to [0, 1]
        rotation_range=30,           # Increased rotation for more variation
        width_shift_range=0.25,      # Increased horizontal shift
        height_shift_range=0.25,     # Increased vertical shift
        shear_range=0.25,            # Increased shear transformation
        zoom_range=0.25,             # Increased zoom variation
        horizontal_flip=True,        # Random horizontal flip
        vertical_flip=False,         # Keep vertical flip off for medical images
        fill_mode='nearest',         # Fill mode for new pixels
        brightness_range=[0.8, 1.2], # Random brightness adjustment
        validation_split=0.2         # 20% for validation
    )
    
    # Validation data - only rescaling, no augmentation
    val_datagen = ImageDataGenerator(
        rescale=1./255,
        validation_split=0.2
    )
    
    # Create generators
    train_generator = train_datagen.flow_from_directory(
        DATASET_DIR,
        target_size=(IMG_HEIGHT, IMG_WIDTH),
        batch_size=BATCH_SIZE,
        class_mode='categorical',
        subset='training',
        shuffle=True
    )
    
    val_generator = val_datagen.flow_from_directory(
        DATASET_DIR,
        target_size=(IMG_HEIGHT, IMG_WIDTH),
        batch_size=BATCH_SIZE,
        class_mode='categorical',
        subset='validation',
        shuffle=False
    )
    
    # Save class labels
    class_indices = train_generator.class_indices
    reverse_labels = {v: k for k, v in CLASS_LABELS.items()}
    
    # Map folder names to display names
    formatted_labels = {}
    for folder_name, class_idx in class_indices.items():
        display_name = CLASS_LABELS.get(folder_name, folder_name)
        formatted_labels[display_name] = int(class_idx)
    
    with open(CLASS_LABELS_PATH, 'w') as f:
        json.dump(formatted_labels, f, indent=2)
    
    print(f"\n✓ Class labels saved to {CLASS_LABELS_PATH}")
    print(f"✓ Found {len(train_generator.classes)} training images")
    print(f"✓ Found {len(val_generator.classes)} validation images")
    print(f"✓ Number of classes: {NUM_CLASSES}")
    
    train_steps = len(train_generator)
    val_steps = len(val_generator)
    
    # Calculate class weights to handle imbalance
    class_weights = compute_class_weights(train_generator)
    
    return train_generator, val_generator, train_steps, val_steps, class_weights


def compute_class_weights(train_generator):
    """
    Compute class weights to handle imbalanced dataset.
    
    Args:
        train_generator: Training data generator
    
    Returns:
        dict: Class weights dictionary
    """
    if not USE_CLASS_WEIGHTS:
        print("\n⚠ Class weights disabled")
        return None
    
    print("\n" + "="*60)
    print("Computing Class Weights for Imbalanced Data")
    print("="*60)
    
    from sklearn.utils.class_weight import compute_class_weight
    
    # Get class distribution
    class_counts = np.bincount(train_generator.classes)
    total_samples = len(train_generator.classes)
    num_classes = len(class_counts)
    
    print(f"\nClass distribution:")
    class_names = list(train_generator.class_indices.keys())
    for i, count in enumerate(class_counts):
        percentage = (count / total_samples) * 100
        print(f"  {class_names[i]:10s}: {count:5d} images ({percentage:5.2f}%)")
    
    # Compute balanced class weights
    classes = np.arange(num_classes)
    weights = compute_class_weight('balanced', classes=classes, y=train_generator.classes)
    
    class_weights_dict = {i: weight for i, weight in enumerate(weights)}
    
    print(f"\nComputed class weights:")
    for class_idx, weight in class_weights_dict.items():
        print(f"  Class {class_idx} ({class_names[class_idx]:10s}): {weight:.3f}")
    
    return class_weights_dict


def build_cnn_model():
    """
    Build a MobileNetV2-based model for skin disease classification using transfer learning.
    
    Architecture:
    - MobileNetV2 (pre-trained on ImageNet) as base
    - Global Average Pooling
    - Batch Normalization
    - Dense layer (256 neurons)
    - Dropout (0.5)
    - Output layer (7 classes with softmax)
    
    Benefits:
    - Pre-trained features from 1.4M ImageNet images
    - Faster convergence
    - Higher accuracy
    - Better generalization
    
    Returns:
        model: Compiled Keras model
    """
    print("\n" + "="*60)
    print("Building MobileNetV2 Model (Transfer Learning)")
    print("="*60)
    
    # Load pre-trained MobileNetV2 base model
    # input_shape must be (224, 224, 3) for MobileNetV2
    base_model = tf.keras.applications.MobileNetV2(
        input_shape=(IMG_HEIGHT, IMG_WIDTH, 3),
        include_top=False,  # Remove the classification head
        weights='imagenet'  # Use pre-trained ImageNet weights
    )
    
    # Freeze the base model (don't train these layers initially)
    base_model.trainable = False
    
    print(f"\n✓ MobileNetV2 base model loaded")
    print(f"✓ Base model layers: {len(base_model.layers)}")
    print(f"✓ Base model trainable: False (frozen)")
    
    # Build the complete model
    model = models.Sequential([
        # Base model (feature extractor)
        base_model,
        
        # Global pooling layer
        layers.GlobalAveragePooling2D(),
        
        # Batch normalization
        layers.BatchNormalization(),
        
        # Dense classifier layer
        layers.Dense(256, activation='relu'),
        layers.Dropout(0.5),
        
        # Output layer (7 classes)
        layers.Dense(NUM_CLASSES, activation='softmax')
    ])
    
    # Compile the model
    model.compile(
        optimizer=tf.keras.optimizers.Adam(learning_rate=0.001),
        loss='categorical_crossentropy',
        metrics=['accuracy']
    )
    
    print("\n✓ Model Architecture:")
    model.summary()
    
    print(f"\n✓ Model compiled with:")
    print(f"  - Optimizer: Adam (lr=0.001)")
    print(f"  - Loss: categorical_crossentropy")
    print(f"  - Metrics: accuracy")
    
    return model


def train_model(model, train_generator, val_generator, train_steps, val_steps, class_weights=None):
    """
    Train the CNN model with callbacks and optional class weights.
    
    Callbacks:
    - EarlyStopping: Stop training if validation loss doesn't improve
    - ReduceLROnPlateau: Reduce learning rate when plateau detected
    - ModelCheckpoint: Save best model
    
    Args:
        model: Keras model to train
        train_generator: Training data generator
        val_generator: Validation data generator
        train_steps: Training steps per epoch
        val_steps: Validation steps per epoch
        class_weights: Optional class weights for imbalanced data
    
    Returns:
        history: Training history object
    """
    print("\n" + "="*60)
    print("Starting Model Training (Phase 1: Feature Extraction)")
    print("="*60)
    
    # Define callbacks
    callbacks = [
        # Save the best model based on validation accuracy
        ModelCheckpoint(
            MODEL_SAVE_PATH,
            monitor='val_accuracy',
            save_best_only=True,
            mode='max',
            verbose=1
        ),
        
        # Stop training if validation loss doesn't improve for 10 epochs
        EarlyStopping(
            monitor='val_loss',
            patience=10,
            restore_best_weights=True,
            verbose=1
        ),
        
        # Reduce learning rate if validation loss plateaus
        ReduceLROnPlateau(
            monitor='val_loss',
            factor=0.5,
            patience=5,
            min_lr=1e-6,
            verbose=1
        )
    ]
    
    # Train the model with optional class weights
    fit_kwargs = {
        'steps_per_epoch': train_steps,
        'epochs': EPOCHS,
        'validation_data': val_generator,
        'validation_steps': val_steps,
        'callbacks': callbacks,
        'verbose': 1
    }
    
    if class_weights is not None:
        fit_kwargs['class_weight'] = class_weights
        print(f"\n✓ Using class weights to handle imbalance")
    
    history = model.fit(
        train_generator,
        **fit_kwargs
    )
    
    print("\n✓ Phase 1 training completed!")
    print(f"✓ Best model saved to {MODEL_SAVE_PATH}")
    
    return history


def fine_tune_model(model, train_generator, val_generator, train_steps, val_steps, class_weights=None):
    """
    Fine-tune the model by unfreezing some base model layers and training with lower learning rate.
    
    This phase helps the model learn dataset-specific features and improves accuracy.
    
    Args:
        model: Trained Keras model
        train_generator: Training data generator
        val_generator: Validation data generator
        train_steps: Training steps per epoch
        val_steps: Validation steps per epoch
        class_weights: Optional class weights
    
    Returns:
        history: Fine-tuning history object
    """
    if not USE_FINE_TUNING:
        print("\n⚠ Fine-tuning disabled")
        return None
    
    print("\n" + "="*60)
    print("Starting Model Fine-Tuning (Phase 2)")
    print("="*60)
    
    # Load the best model from Phase 1
    if os.path.exists(MODEL_SAVE_PATH):
        print(f"\nLoading best model from {MODEL_SAVE_PATH}...")
        model = keras.models.load_model(MODEL_SAVE_PATH)
    else:
        print("\n⚠ No saved model found, using current model")
    
    # Unfreeze some layers of the base model for fine-tuning
    base_model = model.layers[0]  # First layer is the base model
    
    print(f"\nBase model has {len(base_model.layers)} layers")
    print(f"Unfreezing layers from index {FINE_TUNE_FROM_LAYER} onwards...")
    
    # Freeze earlier layers, unfreeze later layers
    for layer in base_model.layers[:FINE_TUNE_FROM_LAYER]:
        layer.trainable = False
    for layer in base_model.layers[FINE_TUNE_FROM_LAYER:]:
        layer.trainable = True
    
    trainable_count = sum([1 for layer in base_model.layers if layer.trainable])
    print(f"✓ Trainable layers in base model: {trainable_count}")
    
    # Recompile with lower learning rate for fine-tuning
    model.compile(
        optimizer=tf.keras.optimizers.Adam(learning_rate=1e-5),  # Much lower learning rate
        loss='categorical_crossentropy',
        metrics=['accuracy']
    )
    
    print(f"\n✓ Model recompiled with Adam optimizer (lr=1e-5)")
    
    # Define callbacks for fine-tuning
    callbacks = [
        ModelCheckpoint(
            MODEL_SAVE_PATH,
            monitor='val_accuracy',
            save_best_only=True,
            mode='max',
            verbose=1
        ),
        EarlyStopping(
            monitor='val_loss',
            patience=8,
            restore_best_weights=True,
            verbose=1
        ),
        ReduceLROnPlateau(
            monitor='val_loss',
            factor=0.5,
            patience=4,
            min_lr=1e-7,
            verbose=1
        )
    ]
    
    # Fine-tune the model
    fit_kwargs = {
        'steps_per_epoch': train_steps,
        'epochs': EPOCHS_FINE_TUNE,
        'validation_data': val_generator,
        'validation_steps': val_steps,
        'callbacks': callbacks,
        'verbose': 1
    }
    
    if class_weights is not None:
        fit_kwargs['class_weight'] = class_weights
    
    print(f"\nStarting fine-tuning for up to {EPOCHS_FINE_TUNE} epochs...")
    history = model.fit(
        train_generator,
        **fit_kwargs
    )
    
    print("\n✓ Phase 2 fine-tuning completed!")
    print(f"✓ Final model saved to {MODEL_SAVE_PATH}")
    
    return history


def plot_training_history(history, history_fine_tune=None):
    """
    Plot and save training history (accuracy and loss graphs).
    
    Args:
        history: Training history object from model.fit()
        history_fine_tune: Optional fine-tuning history object
    """
    print("\n" + "="*60)
    print("Generating Training History Plots")
    print("="*60)
    
    if history_fine_tune is not None:
        # Combine Phase 1 and Phase 2 histories
        combined_history = {
            'accuracy': history.history['accuracy'] + history_fine_tune.history['accuracy'],
            'val_accuracy': history.history['val_accuracy'] + history_fine_tune.history['val_accuracy'],
            'loss': history.history['loss'] + history_fine_tune.history['loss'],
            'val_loss': history.history['val_loss'] + history_fine_tune.history['val_loss']
        }
        
        phase1_epochs = len(history.history['accuracy'])
        total_epochs = len(combined_history['accuracy'])
        
        fig, axes = plt.subplots(1, 2, figsize=(15, 5))
        
        # Accuracy plot
        axes[0].plot(range(1, phase1_epochs + 1), combined_history['accuracy'][:phase1_epochs], 
                    label='Phase 1 - Training Accuracy', marker='o', linestyle='-')
        axes[0].plot(range(phase1_epochs + 1, total_epochs + 1), combined_history['accuracy'][phase1_epochs:], 
                    label='Phase 2 - Training Accuracy', marker='s', linestyle='--')
        axes[0].plot(range(1, phase1_epochs + 1), combined_history['val_accuracy'][:phase1_epochs], 
                    label='Phase 1 - Val Accuracy', marker='o', linestyle='-')
        axes[0].plot(range(phase1_epochs + 1, total_epochs + 1), combined_history['val_accuracy'][phase1_epochs:], 
                    label='Phase 2 - Val Accuracy', marker='s', linestyle='--')
        axes[0].axvline(x=phase1_epochs, color='red', linestyle=':', alpha=0.5, label='Fine-tuning starts')
        axes[0].set_title('Model Accuracy (2-Phase Training)', fontsize=14, fontweight='bold')
        axes[0].set_xlabel('Epoch', fontsize=12)
        axes[0].set_ylabel('Accuracy', fontsize=12)
        axes[0].legend(loc='lower right', fontsize=9)
        axes[0].grid(True, alpha=0.3)
        
        # Loss plot
        axes[1].plot(range(1, phase1_epochs + 1), combined_history['loss'][:phase1_epochs], 
                    label='Phase 1 - Training Loss', marker='o', linestyle='-')
        axes[1].plot(range(phase1_epochs + 1, total_epochs + 1), combined_history['loss'][phase1_epochs:], 
                    label='Phase 2 - Training Loss', marker='s', linestyle='--')
        axes[1].plot(range(1, phase1_epochs + 1), combined_history['val_loss'][:phase1_epochs], 
                    label='Phase 1 - Val Loss', marker='o', linestyle='-')
        axes[1].plot(range(phase1_epochs + 1, total_epochs + 1), combined_history['val_loss'][phase1_epochs:], 
                    label='Phase 2 - Val Loss', marker='s', linestyle='--')
        axes[1].axvline(x=phase1_epochs, color='red', linestyle=':', alpha=0.5, label='Fine-tuning starts')
        axes[1].set_title('Model Loss (2-Phase Training)', fontsize=14, fontweight='bold')
        axes[1].set_xlabel('Epoch', fontsize=12)
        axes[1].set_ylabel('Loss', fontsize=12)
        axes[1].legend(loc='upper right', fontsize=9)
        axes[1].grid(True, alpha=0.3)
    else:
        fig, axes = plt.subplots(1, 2, figsize=(15, 5))
        
        # Accuracy plot
        axes[0].plot(history.history['accuracy'], label='Training Accuracy', marker='o')
        axes[0].plot(history.history['val_accuracy'], label='Validation Accuracy', marker='s')
        axes[0].set_title('Model Accuracy', fontsize=14, fontweight='bold')
        axes[0].set_xlabel('Epoch', fontsize=12)
        axes[0].set_ylabel('Accuracy', fontsize=12)
        axes[0].legend(loc='lower right', fontsize=10)
        axes[0].grid(True, alpha=0.3)
        
        # Loss plot
        axes[1].plot(history.history['loss'], label='Training Loss', marker='o')
        axes[1].plot(history.history['val_loss'], label='Validation Loss', marker='s')
        axes[1].set_title('Model Loss', fontsize=14, fontweight='bold')
        axes[1].set_xlabel('Epoch', fontsize=12)
        axes[1].set_ylabel('Loss', fontsize=12)
        axes[1].legend(loc='upper right', fontsize=10)
        axes[1].grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(HISTORY_PLOT_PATH, dpi=300, bbox_inches='tight')
    print(f"✓ Training history plot saved to {HISTORY_PLOT_PATH}")
    plt.close()


def main():
    """Main function to orchestrate model training."""
    print("\n" + "="*60)
    print("SKIN DISEASE DETECTION - MODEL TRAINING")
    print("="*60)
    
    # Check if dataset exists
    if not os.path.exists(DATASET_DIR):
        print(f"\n✗ Error: Dataset directory '{DATASET_DIR}' not found!")
        print("\nPlease download the HAM10000 dataset and organize it as:")
        print("dataset/")
        print("  ├── akiec/")
        print("  ├── bcc/")
        print("  ├── bkl/")
        print("  ├── df/")
        print("  ├── mel/")
        print("  ├── nv/")
        print("  └── vas/")
        print("\nYou can download it from: https://www.kaggle.com/datasets/kmader/skin-cancer-mnist-ham10000")
        return
    
    # Step 1: Create data generators
    train_gen, val_gen, train_steps, val_steps, class_weights = create_data_generators()
    
    # Step 2: Build the model
    model = build_cnn_model()
    
    # Step 3: Train the model (Phase 1)
    history = train_model(model, train_gen, val_gen, train_steps, val_steps, class_weights)
    
    # Step 4: Fine-tune the model (Phase 2)
    history_fine_tune = fine_tune_model(model, train_gen, val_gen, train_steps, val_steps, class_weights)
    
    # Step 5: Plot training history
    plot_training_history(history, history_fine_tune)
    
    print("\n" + "="*60)
    print("TRAINING COMPLETE!")
    print("="*60)
    print(f"✓ Model saved: {MODEL_SAVE_PATH}")
    print(f"✓ Class labels saved: {CLASS_LABELS_PATH}")
    print(f"✓ Training history plot: {HISTORY_PLOT_PATH}")
    print("\nNext steps:")
    print("1. Run evaluate_model.py to test model performance")
    print("2. Start the Flask backend server")
    print("3. Launch the React frontend")


if __name__ == "__main__":
    main()
