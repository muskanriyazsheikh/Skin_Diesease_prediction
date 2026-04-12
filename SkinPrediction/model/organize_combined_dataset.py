"""
Combined HAM10000 + ISIC Dataset Organizer
===========================================
This script organizes both HAM10000 and ISIC datasets into a unified format
for training the skin disease classification model.

The ISIC dataset contains additional skin lesion images that can significantly
improve model performance when combined with HAM10000.

Dataset Sources:
1. HAM10000: https://www.kaggle.com/datasets/kmader/skin-cancer-mnist-ham10000
2. ISIC Archive: https://www.kaggle.com/datasets/tschandl/isic-archive

Usage:
    1. Download both datasets from Kaggle
    2. Extract them to separate folders
    3. Update the paths in CONFIGURATION section below
    4. Run: python organize_combined_dataset.py
"""

import os
import shutil
import pandas as pd
import numpy as np
from pathlib import Path
from tqdm import tqdm
import json

# ============================================================
# CONFIGURATION - Update these paths based on your setup
# ============================================================

# HAM10000 Dataset Paths
HAM10000_METADATA_CSV = 'C:/Users/ACER/Downloads/HAM10000_metadata.csv'
HAM10000_IMAGE_FOLDER = 'C:/Users/ACER/Downloads/HAM10000_images'

# ISIC Dataset Paths  
ISIC_METADATA_CSV = 'C:/Users/ACER/Downloads/ISIC_metadata.csv'
ISIC_IMAGE_FOLDER = 'C:/Users/ACER/Downloads/ISIC_images'

# Output directory (where combined dataset will be saved)
OUTPUT_DIR = '../dataset_combined'

# ============================================================
# Dataset class codes and their meanings
# ============================================================
CLASS_MAPPING = {
    'akiec': 'Actinic keratoses',
    'bcc': 'Basal cell carcinoma',
    'bkl': 'Benign keratosis-like lesions',
    'df': 'Dermatofibroma',
    'mel': 'Melanoma',
    'nv': 'Melanocytic nevi',
    'vas': 'Vascular lesions'
}

# ISIC diagnosis mapping (may vary based on dataset version)
# Update this mapping based on your ISIC dataset's dx column values
ISIC_DX_MAPPING = {
    'AK': 'akiec',
    'BCC': 'bcc',
    'BKL': 'bkl',
    'DF': 'df',
    'MEL': 'mel',
    'NV': 'nv',
    'VASC': 'vas',
    'Actinic keratoses': 'akiec',
    'Basal cell carcinoma': 'bcc',
    'Benign keratosis': 'bkl',
    'Dermatofibroma': 'df',
    'Melanoma': 'mel',
    'Melanocytic nevi': 'nv',
    'Vascular lesion': 'vas'
}


def create_directories():
    """Create output directories for each class."""
    print("\nCreating directories...")
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    for class_code in CLASS_MAPPING.keys():
        class_dir = os.path.join(OUTPUT_DIR, class_code)
        os.makedirs(class_dir, exist_ok=True)
        print(f"  ✓ Created: {class_dir}")


def organize_ham10000_dataset():
    """Organize HAM10000 dataset images into class-specific folders."""
    print("\n" + "="*60)
    print("Organizing HAM10000 Dataset")
    print("="*60)
    
    if not os.path.exists(HAM10000_METADATA_CSV):
        print(f"\n⚠ HAM10000 metadata not found at {HAM10000_METADATA_CSV}")
        print("  Skipping HAM10000 dataset...")
        return 0, 0
    
    if not os.path.exists(HAM10000_IMAGE_FOLDER):
        print(f"\n⚠ HAM10000 images not found at {HAM10000_IMAGE_FOLDER}")
        print("  Skipping HAM10000 dataset...")
        return 0, 0
    
    # Read metadata
    print(f"\nReading HAM10000 metadata...")
    metadata = pd.read_csv(HAM10000_METADATA_CSV)
    print(f"✓ Found {len(metadata)} images in HAM10000 metadata")
    
    # Organize images
    print("\nOrganizing HAM10000 images...")
    success_count = 0
    error_count = 0
    
    for idx, row in tqdm(metadata.iterrows(), total=len(metadata), desc="HAM10000"):
        image_id = row['image_id']
        diagnosis = row['dx']
        
        # Skip if diagnosis not in our classes
        if diagnosis not in CLASS_MAPPING:
            continue
        
        # Find the image file
        image_path = None
        for ext in ['.jpg', '.jpeg', '.png']:
            potential_path = os.path.join(HAM10000_IMAGE_FOLDER, image_id + ext)
            if os.path.exists(potential_path):
                image_path = potential_path
                break
        
        if image_path:
            try:
                dest_dir = os.path.join(OUTPUT_DIR, diagnosis)
                dest_path = os.path.join(dest_dir, f'ham_{image_id}.jpg')
                
                # Copy only if doesn't exist (avoid duplicates)
                if not os.path.exists(dest_path):
                    shutil.copy2(image_path, dest_path)
                    success_count += 1
                    
            except Exception as e:
                error_count += 1
    
    print(f"\n✓ HAM10000: {success_count} images organized, {error_count} errors")
    return success_count, error_count


def organize_isic_dataset():
    """Organize ISIC dataset images into class-specific folders."""
    print("\n" + "="*60)
    print("Organizing ISIC Dataset")
    print("="*60)
    
    if not os.path.exists(ISIC_METADATA_CSV):
        print(f"\n⚠ ISIC metadata not found at {ISIC_METADATA_CSV}")
        print("  Skipping ISIC dataset...")
        return 0, 0
    
    if not os.path.exists(ISIC_IMAGE_FOLDER):
        print(f"\n⚠ ISIC images not found at {ISIC_IMAGE_FOLDER}")
        print("  Skipping ISIC dataset...")
        return 0, 0
    
    # Read metadata
    print(f"\nReading ISIC metadata...")
    metadata = pd.read_csv(ISIC_METADATA_CSV)
    print(f"✓ Found {len(metadata)} images in ISIC metadata")
    
    # Display available columns to help user map diagnosis
    print(f"\nAvailable columns in ISIC metadata: {list(metadata.columns)}")
    
    # Try to find diagnosis column (common names: 'dx', 'diagnosis', 'label', 'ISIC_diagnosis')
    diagnosis_col = None
    for col in ['dx', 'diagnosis', 'label', 'ISIC_diagnosis', 'mel_mit_score']:
        if col in metadata.columns:
            diagnosis_col = col
            break
    
    if diagnosis_col is None:
        print(f"\n⚠ Could not find diagnosis column in ISIC metadata")
        print(f"  Available columns: {list(metadata.columns)}")
        print("  Please update ISIC_DX_MAPPING and diagnosis_col in this script")
        return 0, 0
    
    print(f"✓ Using diagnosis column: '{diagnosis_col}'")
    
    # Find image ID column
    image_id_col = None
    for col in ['image_id', 'ISIC_id', 'isic_id', 'id', 'image']:
        if col in metadata.columns:
            image_id_col = col
            break
    
    if image_id_col is None:
        print(f"\n⚠ Could not find image ID column in ISIC metadata")
        print("  Please update image_id_col in this script")
        return 0, 0
    
    print(f"✓ Using image ID column: '{image_id_col}'")
    
    # Organize images
    print("\nOrganizing ISIC images...")
    success_count = 0
    error_count = 0
    skipped_count = 0
    
    for idx, row in tqdm(metadata.iterrows(), total=len(metadata), desc="ISIC"):
        image_id = row[image_id_col]
        diagnosis_raw = row[diagnosis_col]
        
        # Map ISIC diagnosis to our class codes
        diagnosis = ISIC_DX_MAPPING.get(diagnosis_raw)
        
        if diagnosis is None:
            skipped_count += 1
            continue
        
        # Find the image file
        image_path = None
        for ext in ['.jpg', '.jpeg', '.png']:
            potential_path = os.path.join(ISIC_IMAGE_FOLDER, image_id + ext)
            if os.path.exists(potential_path):
                image_path = potential_path
                break
        
        if image_path:
            try:
                dest_dir = os.path.join(OUTPUT_DIR, diagnosis)
                dest_path = os.path.join(dest_dir, f'isic_{image_id}.jpg')
                
                # Copy only if doesn't exist
                if not os.path.exists(dest_path):
                    shutil.copy2(image_path, dest_path)
                    success_count += 1
                    
            except Exception as e:
                error_count += 1
    
    print(f"\n✓ ISIC: {success_count} images organized, {error_count} errors, {skipped_count} skipped")
    return success_count, error_count


def print_dataset_statistics():
    """Print detailed statistics about the combined dataset."""
    print("\n" + "="*60)
    print("Combined Dataset Statistics")
    print("="*60)
    
    total_images = 0
    stats = {}
    
    for class_code, class_name in sorted(CLASS_MAPPING.items()):
        class_dir = os.path.join(OUTPUT_DIR, class_code)
        if os.path.exists(class_dir):
            files = os.listdir(class_dir)
            count = len(files)
            total_images += count
            stats[class_code] = {
                'name': class_name,
                'count': count
            }
            print(f"{class_code:8s} ({class_name:35s}): {count:5d} images")
    
    print("="*60)
    print(f"Total: {total_images} images")
    print("="*60)
    
    # Calculate class distribution
    if total_images > 0:
        print("\nClass Distribution:")
        for class_code, info in stats.items():
            percentage = (info['count'] / total_images) * 100
            print(f"  {class_code:8s}: {percentage:5.2f}%")
    
    # Save statistics to JSON
    stats_path = os.path.join(OUTPUT_DIR, 'dataset_stats.json')
    with open(stats_path, 'w') as f:
        json.dump({
            'total_images': total_images,
            'class_distribution': stats,
            'classes': list(CLASS_MAPPING.keys())
        }, f, indent=2)
    
    print(f"\n✓ Statistics saved to {stats_path}")
    return stats


def verify_dataset():
    """Verify the organized dataset."""
    print("\n" + "="*60)
    print("Verifying Dataset...")
    print("="*60)
    
    if not os.path.exists(OUTPUT_DIR):
        print(f"\n✗ Dataset directory not found: {OUTPUT_DIR}")
        return False
    
    all_valid = True
    for class_code, class_name in sorted(CLASS_MAPPING.items()):
        class_dir = os.path.join(OUTPUT_DIR, class_code)
        if os.path.exists(class_dir):
            files = os.listdir(class_dir)
            if len(files) > 0:
                print(f"✓ {class_code}: {len(files)} images")
                
                # Check a sample image
                sample_file = files[0]
                file_path = os.path.join(class_dir, sample_file)
                file_size = os.path.getsize(file_path)
                print(f"  Sample: {sample_file} ({file_size/1024:.1f} KB)")
            else:
                print(f"⚠ {class_code}: Directory exists but is empty")
        else:
            print(f"✗ {class_code}: Directory not found")
            all_valid = False
    
    return all_valid


if __name__ == "__main__":
    print("\n" + "="*60)
    print("Combined HAM10000 + ISIC Dataset Organizer")
    print("="*60)
    print("\nThis script will combine HAM10000 and ISIC datasets into:")
    for class_code, class_name in CLASS_MAPPING.items():
        print(f"  - {class_code}/ ({class_name})")
    
    print("\nBefore running, make sure you have:")
    print("  1. Downloaded HAM10000 dataset from Kaggle")
    print("  2. Downloaded ISIC dataset from Kaggle")
    print("  3. Extracted both datasets")
    print("  4. Updated path configurations in this script")
    
    response = input("\nHave you updated the configuration paths? (yes/no): ")
    
    if response.lower() == 'yes':
        # Create directories
        create_directories()
        
        # Organize HAM10000
        ham_success, ham_errors = organize_ham10000_dataset()
        
        # Organize ISIC
        isic_success, isic_errors = organize_isic_dataset()
        
        # Print statistics
        stats = print_dataset_statistics()
        
        # Verify dataset
        if ham_success > 0 or isic_success > 0:
            verify_ok = verify_dataset()
            
            if verify_ok:
                print("\n✅ Combined dataset is ready for training!")
                print(f"\nTotal images: {ham_success + isic_success}")
                print("\nNext steps:")
                print("  1. Update train_model.py DATASET_DIR to '../dataset_combined'")
                print("  2. Run: python train_model.py")
            else:
                print("\n⚠️  Dataset verification failed. Please check the output above.")
        else:
            print("\n❌ No images were organized. Please check the paths and metadata.")
    else:
        print("\nPlease update the configuration paths and run this script again.")
        print("\nOpen organize_combined_dataset.py and update:")
        print("  - HAM10000_METADATA_CSV: Path to HAM10000_metadata.csv")
        print("  - HAM10000_IMAGE_FOLDER: Path to HAM10000 images")
        print("  - ISIC_METADATA_CSV: Path to ISIC metadata CSV")
        print("  - ISIC_IMAGE_FOLDER: Path to ISIC images")
        print("  - OUTPUT_DIR: Path to output dataset folder")
