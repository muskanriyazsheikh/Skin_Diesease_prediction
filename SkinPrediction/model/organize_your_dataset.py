"""
Custom Dataset Organizer for Pre-Combined HAM10000 + ISIC Dataset
==================================================================
This script organizes your existing combined dataset into the format 
required for training the skin disease classification model.

Your current structure:
- HAM10000_metadata.csv (metadata file)
- labeldataset/ (contains label files)
- processimagedataset/ (contains all images)

This script will:
1. Read metadata and labels
2. Organize images into class-specific folders
3. Create a training-ready dataset structure
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

# Main dataset folder (containing all components)
MAIN_DATASET_FOLDER = 'C:/Users/ACER/Downloads/combineDataset'

# Metadata file
METADATA_CSV = 'HAM10000_metadata.csv'  # Will be joined with MAIN_DATASET_FOLDER

# Label dataset folder
LABEL_DATASET_FOLDER = 'labeldataset'

# Processed images folder (contains all images)
IMAGE_FOLDER = 'processimagedataset'

# Output directory (where organized dataset will be saved)
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

# Common diagnosis mappings (covers both HAM10000 and ISIC formats)
DIAGNOSIS_MAPPING = {
    # HAM10000 format
    'akiec': 'akiec',
    'bcc': 'bcc',
    'bkl': 'bkl',
    'df': 'df',
    'mel': 'mel',
    'nv': 'nv',
    'vas': 'vas',
    
    # ISIC full names
    'Actinic keratoses': 'akiec',
    'Basal cell carcinoma': 'bcc',
    'Benign keratosis': 'bkl',
    'Benign keratosis-like lesions': 'bkl',
    'Dermatofibroma': 'df',
    'Melanoma': 'mel',
    'Melanocytic nevi': 'nv',
    'Vascular lesions': 'vas',
    'Vascular lesion': 'vas',
    
    # ISIC abbreviations
    'AK': 'akiec',
    'BCC': 'bcc',
    'BKL': 'bkl',
    'DF': 'df',
    'MEL': 'mel',
    'NV': 'nv',
    'VASC': 'vas',
}


def create_directories():
    """Create output directories for each class."""
    print("\nCreating directories...")
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    for class_code in CLASS_MAPPING.keys():
        class_dir = os.path.join(OUTPUT_DIR, class_code)
        os.makedirs(class_dir, exist_ok=True)
        print(f"  ✓ Created: {class_dir}")


def explore_label_files():
    """Explore the labeldataset folder to find label files."""
    label_folder = os.path.join(MAIN_DATASET_FOLDER, LABEL_DATASET_FOLDER)
    
    if not os.path.exists(label_folder):
        print(f"\n⚠ Label dataset folder not found: {label_folder}")
        return []
    
    # List all files in labeldataset
    files = os.listdir(label_folder)
    print(f"\n📁 Files in labeldataset folder:")
    for file in files:
        file_path = os.path.join(label_folder, file)
        if os.path.isfile(file_path):
            size = os.path.getsize(file_path) / 1024  # KB
            print(f"  📄 {file} ({size:.1f} KB)")
    
    # Filter CSV files
    csv_files = [f for f in files if f.endswith('.csv')]
    print(f"\nFound {len(csv_files)} CSV file(s): {csv_files}")
    
    return csv_files


def explore_metadata():
    """Explore the main metadata CSV file."""
    metadata_path = os.path.join(MAIN_DATASET_FOLDER, METADATA_CSV)
    
    if not os.path.exists(metadata_path):
        print(f"\n⚠ Metadata file not found: {metadata_path}")
        return None
    
    print(f"\n📊 Reading metadata from: {METADATA_CSV}")
    metadata = pd.read_csv(metadata_path)
    
    print(f"✓ Found {len(metadata)} entries")
    print(f"✓ Columns: {list(metadata.columns)}")
    print(f"\nFirst few rows:")
    print(metadata.head())
    
    return metadata


def explore_images():
    """Explore the image folder to understand the structure."""
    image_path = os.path.join(MAIN_DATASET_FOLDER, IMAGE_FOLDER)
    
    if not os.path.exists(image_path):
        print(f"\n⚠ Image folder not found: {image_path}")
        return []
    
    # List some sample files
    files = os.listdir(image_path)
    image_files = [f for f in files if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
    
    print(f"\n🖼️  Image folder: {IMAGE_FOLDER}")
    print(f"✓ Found {len(image_files)} image files")
    
    if len(image_files) > 0:
        print(f"\nSample image filenames:")
        for f in image_files[:10]:
            print(f"  {f}")
    
    return image_files


def organize_using_metadata():
    """
    Organize dataset using the main metadata CSV file.
    This is the primary method if metadata contains diagnosis labels.
    """
    print("\n" + "="*60)
    print("Method 1: Organizing using HAM10000_metadata.csv")
    print("="*60)
    
    metadata_path = os.path.join(MAIN_DATASET_FOLDER, METADATA_CSV)
    image_folder = os.path.join(MAIN_DATASET_FOLDER, IMAGE_FOLDER)
    
    if not os.path.exists(metadata_path):
        print(f"⚠ Metadata file not found")
        return 0, 0
    
    if not os.path.exists(image_folder):
        print(f"⚠ Image folder not found")
        return 0, 0
    
    # Read metadata
    metadata = pd.read_csv(metadata_path)
    print(f"✓ Loaded metadata with {len(metadata)} entries")
    print(f"✓ Available columns: {list(metadata.columns)}")
    
    # Find image ID column
    image_id_col = None
    for col in ['image_id', 'ISIC_id', 'isic_id', 'id', 'image', 'filename']:
        if col in metadata.columns:
            image_id_col = col
            break
    
    if image_id_col is None:
        print(f"\n⚠ Could not find image ID column")
        print(f"Available columns: {list(metadata.columns)}")
        return 0, 0
    
    print(f"✓ Using image ID column: '{image_id_col}'")
    
    # Find diagnosis column
    diagnosis_col = None
    for col in ['dx', 'diagnosis', 'label', 'ISIC_diagnosis', 'class', 'target']:
        if col in metadata.columns:
            diagnosis_col = col
            break
    
    if diagnosis_col is None:
        print(f"\n⚠ Could not find diagnosis column")
        print(f"Available columns: {list(metadata.columns)}")
        return 0, 0
    
    print(f"✓ Using diagnosis column: '{diagnosis_col}'")
    
    # Organize images
    print("\n📂 Organizing images...")
    success_count = 0
    error_count = 0
    skipped_count = 0
    
    for idx, row in tqdm(metadata.iterrows(), total=len(metadata), desc="Processing"):
        image_id = str(row[image_id_col])
        diagnosis_raw = str(row[diagnosis_col])
        
        # Map diagnosis to standard class code
        diagnosis = DIAGNOSIS_MAPPING.get(diagnosis_raw)
        
        if diagnosis is None:
            skipped_count += 1
            continue
        
        # Find the image file
        image_path = None
        for ext in ['.jpg', '.jpeg', '.png']:
            potential_path = os.path.join(image_folder, image_id + ext)
            if os.path.exists(potential_path):
                image_path = potential_path
                break
        
        if image_path:
            try:
                dest_dir = os.path.join(OUTPUT_DIR, diagnosis)
                dest_path = os.path.join(dest_dir, f'{image_id}.jpg')
                
                if not os.path.exists(dest_path):
                    shutil.copy2(image_path, dest_path)
                    success_count += 1
                    
            except Exception as e:
                error_count += 1
    
    print(f"\n✅ Success: {success_count} images organized")
    print(f"❌ Errors: {error_count}")
    print(f"⏭️  Skipped: {skipped_count} (diagnosis not in mapping)")
    
    return success_count, error_count


def organize_using_label_files():
    """
    Organize dataset using separate label files from labeldataset folder.
    Use this if the main metadata doesn't have diagnosis information.
    """
    print("\n" + "="*60)
    print("Method 2: Organizing using label files from labeldataset/")
    print("="*60)
    
    label_folder = os.path.join(MAIN_DATASET_FOLDER, LABEL_DATASET_FOLDER)
    image_folder = os.path.join(MAIN_DATASET_FOLDER, IMAGE_FOLDER)
    
    if not os.path.exists(label_folder):
        print(f"⚠ Label folder not found")
        return 0, 0
    
    if not os.path.exists(image_folder):
        print(f"⚠ Image folder not found")
        return 0, 0
    
    # Find CSV files in labeldataset
    csv_files = [f for f in os.listdir(label_folder) if f.endswith('.csv')]
    
    if len(csv_files) == 0:
        print(f"⚠ No CSV files found in labeldataset/")
        return 0, 0
    
    total_success = 0
    total_errors = 0
    
    # Process each label file
    for csv_file in csv_files:
        print(f"\n📄 Processing: {csv_file}")
        label_path = os.path.join(label_folder, csv_file)
        
        try:
            labels_df = pd.read_csv(label_path)
            print(f"✓ Loaded {len(labels_df)} labels")
            print(f"✓ Columns: {list(labels_df.columns)}")
            
            # Find image ID and diagnosis columns
            image_id_col = None
            diagnosis_col = None
            
            for col in labels_df.columns:
                col_lower = col.lower()
                if any(x in col_lower for x in ['image_id', 'isic_id', 'id', 'image', 'filename']):
                    image_id_col = col
                if any(x in col_lower for x in ['dx', 'diagnosis', 'label', 'class', 'target']):
                    diagnosis_col = col
            
            if image_id_col is None or diagnosis_col is None:
                print(f"⚠ Could not identify columns. Please check the CSV format")
                continue
            
            print(f"✓ Image ID column: '{image_id_col}'")
            print(f"✓ Diagnosis column: '{diagnosis_col}'")
            
            # Organize images
            success_count = 0
            error_count = 0
            
            for idx, row in tqdm(labels_df.iterrows(), total=len(labels_df), desc=f"Processing {csv_file}"):
                image_id = str(row[image_id_col])
                diagnosis_raw = str(row[diagnosis_col])
                
                # Map diagnosis
                diagnosis = DIAGNOSIS_MAPPING.get(diagnosis_raw)
                
                if diagnosis is None:
                    continue
                
                # Find image
                image_path = None
                for ext in ['.jpg', '.jpeg', '.png']:
                    potential_path = os.path.join(image_folder, image_id + ext)
                    if os.path.exists(potential_path):
                        image_path = potential_path
                        break
                
                if image_path:
                    try:
                        dest_dir = os.path.join(OUTPUT_DIR, diagnosis)
                        dest_path = os.path.join(dest_dir, f'{image_id}.jpg')
                        
                        if not os.path.exists(dest_path):
                            shutil.copy2(image_path, dest_path)
                            success_count += 1
                    except:
                        error_count += 1
            
            print(f"✅ {csv_file}: {success_count} images, {error_count} errors")
            total_success += success_count
            total_errors += error_count
            
        except Exception as e:
            print(f"❌ Error processing {csv_file}: {str(e)}")
    
    return total_success, total_errors


def print_dataset_statistics():
    """Print detailed statistics about the organized dataset."""
    print("\n" + "="*60)
    print("📊 Combined Dataset Statistics")
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
            bar = '█' * int(count / max(stats.values(), key=lambda x: x['count'])['count'] * 30)
            print(f"{class_code:8s} ({class_name:35s}): {count:5d} images {bar}")
    
    print("="*60)
    print(f"📈 Total: {total_images} images")
    print("="*60)
    
    # Calculate class distribution
    if total_images > 0:
        print("\n📉 Class Distribution:")
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
    print("🔍 Verifying Dataset...")
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
    print("🚀 Custom Dataset Organizer for Combined HAM10000 + ISIC")
    print("="*60)
    
    print("\n📁 Current Configuration:")
    print(f"  Main dataset folder: {MAIN_DATASET_FOLDER}")
    print(f"  Metadata file: {METADATA_CSV}")
    print(f"  Label folder: {LABEL_DATASET_FOLDER}")
    print(f"  Image folder: {IMAGE_FOLDER}")
    print(f"  Output directory: {OUTPUT_DIR}")
    
    response = input("\n✅ Are these paths correct? (yes/no): ")
    
    if response.lower() != 'yes':
        print("\n❌ Please update the configuration at the top of this script:")
        print("  - MAIN_DATASET_FOLDER: Path to your main dataset folder")
        print("  - METADATA_CSV: Name of metadata CSV file")
        print("  - LABEL_DATASET_FOLDER: Name of label folder")
        print("  - IMAGE_FOLDER: Name of image folder")
        exit()
    
    # Step 1: Create output directories
    create_directories()
    
    # Step 2: Explore your dataset structure
    print("\n" + "="*60)
    print("🔍 Exploring Dataset Structure")
    print("="*60)
    
    csv_files = explore_label_files()
    metadata = explore_metadata()
    image_files = explore_images()
    
    # Step 3: Try organizing with metadata first
    if metadata is not None:
        meta_success, meta_errors = organize_using_metadata()
        
        if meta_success > 100:
            print(f"\n✅ Successfully organized {meta_success} images using metadata!")
        else:
            print(f"\n⚠ Only organized {meta_success} images using metadata. Trying label files...")
            label_success, label_errors = organize_using_label_files()
            print(f"✅ Organized {label_success} images using label files")
    else:
        # Use label files
        label_success, label_errors = organize_using_label_files()
    
    # Step 4: Print statistics
    stats = print_dataset_statistics()
    
    # Step 5: Verify dataset
    verify_ok = verify_dataset()
    
    if verify_ok:
        total = sum(info['count'] for info in stats.values())
        print(f"\n🎉 Dataset organization complete!")
        print(f"📊 Total images organized: {total}")
        print("\n📝 Next steps:")
        print("  1. Open model/train_model.py")
        print("  2. Change DATASET_DIR to '../dataset_combined'")
        print("  3. Run: python train_model.py")
    else:
        print("\n⚠️  Dataset verification found issues. Please check the output above.")
