"""
Dataset Organization Script
============================
This script organizes the HAM10000 dataset into class-specific folders.

Usage:
    1. Download HAM10000 dataset from Kaggle
    2. Extract files to a temporary location
    3. Update the paths below
    4. Run: python organize_dataset.py
"""

import os
import shutil
import pandas as pd
from pathlib import Path

# ============================================================
# CONFIGURATION - Update these paths based on your setup
# ============================================================

# Path to the downloaded HAM10000 metadata CSV file
# Example: ''
METADATA_CSV = 'C:/Users/ACER/Downloads/HAM10000_metadata.csv'

# Path to the folder containing the downloaded images
# Example: 'C:/Users/ACER/Downloads/HAM10000_images'
IMAGE_FOLDER = 'C:/Users/ACER/Downloads/HAM10000_images'

# Output directory (where organized dataset will be saved)
# This should be the dataset/ folder in your project
OUTPUT_DIR = '../dataset'

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


def create_directories():
    """Create output directories for each class."""
    print("\nCreating directories...")
    for class_code in CLASS_MAPPING.keys():
        class_dir = os.path.join(OUTPUT_DIR, class_code)
        os.makedirs(class_dir, exist_ok=True)
        print(f"  ✓ Created: {class_dir}")


def organize_dataset():
    """Organize images into class-specific folders."""
    print("\n" + "="*60)
    print("HAM10000 Dataset Organization")
    print("="*60)
    
    # Check if metadata file exists
    if not os.path.exists(METADATA_CSV):
        print(f"\n✗ Error: Metadata file not found at {METADATA_CSV}")
        print("\nPlease update METADATA_CSV path in this script.")
        return False
    
    # Check if image folder exists
    if not os.path.exists(IMAGE_FOLDER):
        print(f"\n✗ Error: Image folder not found at {IMAGE_FOLDER}")
        print("\nPlease update IMAGE_FOLDER path in this script.")
        return False
    
    # Create output directories
    create_directories()
    
    # Read metadata
    print(f"\nReading metadata from {METADATA_CSV}...")
    metadata = pd.read_csv(METADATA_CSV)
    print(f"✓ Found {len(metadata)} images in metadata")
    
    # Organize images
    print("\nOrganizing images...")
    success_count = 0
    error_count = 0
    missing_count = 0
    
    for idx, row in metadata.iterrows():
        image_id = row['image_id']
        diagnosis = row['dx']  # Diagnosis code
        
        # Skip if diagnosis not in our classes
        if diagnosis not in CLASS_MAPPING:
            continue
        
        # Find the image file (try different extensions)
        image_path = None
        for ext in ['.jpg', '.jpeg', '.png']:
            potential_path = os.path.join(IMAGE_FOLDER, image_id + ext)
            if os.path.exists(potential_path):
                image_path = potential_path
                break
        
        if image_path:
            try:
                # Destination path
                dest_dir = os.path.join(OUTPUT_DIR, diagnosis)
                dest_path = os.path.join(dest_dir, f'{image_id}.jpg')
                
                # Copy image
                shutil.copy2(image_path, dest_path)
                success_count += 1
                
                # Progress indicator
                if (idx + 1) % 1000 == 0:
                    print(f"  Processed {idx + 1}/{len(metadata)} images...")
                    
            except Exception as e:
                print(f"\n✗ Error copying {image_id}: {str(e)}")
                error_count += 1
        else:
            missing_count += 1
    
    # Print summary
    print("\n" + "="*60)
    print("Organization Complete!")
    print("="*60)
    print(f"✓ Successfully organized: {success_count} images")
    print(f"✗ Errors: {error_count}")
    print(f"⚠ Missing images: {missing_count}")
    print(f"\nDataset saved to: {OUTPUT_DIR}")
    
    # Show class distribution
    print("\n" + "="*60)
    print("Class Distribution:")
    print("="*60)
    total = 0
    for class_code, class_name in sorted(CLASS_MAPPING.items()):
        class_dir = os.path.join(OUTPUT_DIR, class_code)
        if os.path.exists(class_dir):
            count = len(os.listdir(class_dir))
            total += count
            print(f"{class_code:8s} ({class_name:35s}): {count:5d} images")
    
    print("="*60)
    print(f"Total: {total} images")
    print("="*60)
    
    return True


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
            print(f"✓ {class_code}: {len(files)} images")
            
            # Check a few images
            if len(files) > 0:
                sample_file = files[0]
                file_path = os.path.join(class_dir, sample_file)
                file_size = os.path.getsize(file_path)
                print(f"  Sample: {sample_file} ({file_size/1024:.1f} KB)")
        else:
            print(f"✗ {class_code}: Directory not found")
            all_valid = False
    
    return all_valid


if __name__ == "__main__":
    print("\n" + "="*60)
    print("HAM10000 Dataset Organization Tool")
    print("="*60)
    print("\nThis script will organize your HAM10000 dataset into:")
    print("  - akiec/ (Actinic keratoses)")
    print("  - bcc/   (Basal cell carcinoma)")
    print("  - bkl/   (Benign keratosis-like lesions)")
    print("  - df/    (Dermatofibroma)")
    print("  - mel/   (Melanoma)")
    print("  - nv/    (Melanocytic nevi)")
    print("  - vas/   (Vascular lesions)")
    
    # Ask for confirmation
    print("\nBefore running, make sure you have:")
    print("  1. Downloaded HAM10000 dataset from Kaggle")
    print("  2. Extracted the files")
    print("  3. Updated METADATA_CSV and IMAGE_FOLDER paths in this script")
    
    response = input("\nHave you updated the configuration paths? (yes/no): ")
    
    if response.lower() == 'yes':
        # Organize dataset
        success = organize_dataset()
        
        if success:
            # Verify dataset
            verify_ok = verify_dataset()
            
            if verify_ok:
                print("\n✅ Dataset is ready for training!")
                print("\nNext step: Run the training script")
                print("  cd model")
                print("  python train_model.py")
            else:
                print("\n⚠️  Dataset verification failed. Please check the output above.")
        else:
            print("\n❌ Dataset organization failed. Please check the errors above.")
    else:
        print("\nPlease update the configuration paths and run this script again.")
        print("\nOpen organize_dataset.py and update:")
        print("  - METADATA_CSV: Path to HAM10000_metadata.csv")
        print("  - IMAGE_FOLDER: Path to folder containing images")
        print("  - OUTPUT_DIR: Path to dataset/ folder (usually '../dataset')")
