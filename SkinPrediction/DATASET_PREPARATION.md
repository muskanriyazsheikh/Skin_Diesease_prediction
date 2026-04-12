# Dataset Preparation Guide

This guide explains how to obtain and prepare the HAM10000 dataset for training the skin disease detection model.

---

## 📊 Dataset Overview

**HAM10000** ("Human Against Machine with 10000 training images") is a large collection of multi-source dermatoscopic images of common pigmented skin lesions.

### Dataset Statistics
- **Total Images**: 10,015
- **Classes**: 7 skin conditions
- **Image Size**: Variable (will be resized to 128x128)
- **Format**: JPEG

### Class Distribution

| Class Code | Disease Name | Images | Percentage |
|------------|--------------|--------|------------|
| nv | Melanocytic nevi | 6,705 | 67.0% |
| mel | Melanoma | 1,113 | 11.1% |
| bkl | Benign keratosis-like lesions | 1,099 | 11.0% |
| bcc | Basal cell carcinoma | 514 | 5.1% |
| akiec | Actinic keratoses | 327 | 3.3% |
| vas | Vascular lesions | 142 | 1.4% |
| df | Dermatofibroma | 115 | 1.1% |

**Note**: The dataset is imbalanced. The training script uses data augmentation to address this.

---

## 📥 Step 1: Download the Dataset

### Option 1: Kaggle (Recommended)

1. **Create Kaggle Account**
   - Go to [kaggle.com](https://www.kaggle.com)
   - Sign up (free)

2. **Download Dataset**
   - Visit: https://www.kaggle.com/datasets/kmader/skin-cancer-mnist-ham10000
   - Click "Download" button
   - Or use Kaggle API:
     ```bash
     pip install kaggle
     kaggle datasets download -d kmader/skin-cancer-mnist-ham10000
     ```

3. **Extract Files**
   ```bash
   unzip skin-cancer-mnist-ham10000.zip
   ```

### Option 2: Direct Download

If available from academic sources:
- Check the ISIC Archive: https://www.isic-archive.com
- Or other dermatology datasets

---

## 📁 Step 2: Organize Dataset Structure

The model expects images organized in class-specific folders:

```
dataset/
├── akiec/          # Actinic keratoses
│   ├── img1.jpg
│   ├── img2.jpg
│   └── ...
├── bcc/            # Basal cell carcinoma
│   ├── img1.jpg
│   └── ...
├── bkl/            # Benign keratosis-like lesions
│   ├── img1.jpg
│   └── ...
├── df/             # Dermatofibroma
│   ├── img1.jpg
│   └── ...
├── mel/            # Melanoma
│   ├── img1.jpg
│   └── ...
├── nv/             # Melanocytic nevi
│   ├── img1.jpg
│   └── ...
└── vas/            # Vascular lesions
    ├── img1.jpg
    └── ...
```

### Organize Using Python Script

Create `organize_dataset.py` in the `model/` directory:

```python
import os
import shutil
import pandas as pd
from pathlib import Path

# Configuration
CSV_FILE = '../HAM10000_metadata.csv'  # Path to metadata CSV
IMAGE_DIR = '../HAM10000_images'       # Path to downloaded images
OUTPUT_DIR = '../dataset'              # Output directory

# Create output directories
classes = ['akiec', 'bcc', 'bkl', 'df', 'mel', 'nv', 'vas']
for cls in classes:
    os.makedirs(os.path.join(OUTPUT_DIR, cls), exist_ok=True)

# Read metadata
metadata = pd.read_csv(CSV_FILE)

# Organize images
for _, row in metadata.iterrows():
    image_id = row['image_id']
    dx = row['dx']  # Diagnosis code
    
    # Find image file
    image_path = None
    for ext in ['.jpg', '.jpeg', '.png']:
        potential_path = os.path.join(IMAGE_DIR, image_id + ext)
        if os.path.exists(potential_path):
            image_path = potential_path
            break
    
    if image_path and dx in classes:
        # Copy to appropriate folder
        dest_path = os.path.join(OUTPUT_DIR, dx, f'{image_id}.jpg')
        shutil.copy(image_path, dest_path)

print(f"Dataset organized in {OUTPUT_DIR}")
```

Run the script:
```bash
python organize_dataset.py
```

---

## 🔍 Step 3: Verify Dataset

### Check Image Counts

```python
import os

dataset_dir = '../dataset'
classes = os.listdir(dataset_dir)

print("Dataset Summary:")
print("=" * 50)

total_images = 0
for cls in sorted(classes):
    cls_dir = os.path.join(dataset_dir, cls)
    if os.path.isdir(cls_dir):
        count = len(os.listdir(cls_dir))
        total_images += count
        print(f"{cls:10s}: {count:5d} images")

print("=" * 50)
print(f"Total: {total_images} images")
```

### Visualize Sample Images

```python
import matplotlib.pyplot as plt
import os
import random
from tensorflow.keras.preprocessing import image

dataset_dir = '../dataset'
classes = os.listdir(dataset_dir)

fig, axes = plt.subplots(2, 4, figsize=(15, 8))
axes = axes.flatten()

for idx, cls in enumerate(sorted(classes)[:7]):
    cls_dir = os.path.join(dataset_dir, cls)
    images = os.listdir(cls_dir)
    
    if images:
        random_image = random.choice(images)
        img_path = os.path.join(cls_dir, random_image)
        
        img = image.load_img(img_path, target_size=(128, 128))
        axes[idx].imshow(img)
        axes[idx].set_title(f'{cls}', fontsize=12, fontweight='bold')
        axes[idx].axis('off')

plt.tight_layout()
plt.savefig('dataset_samples.png', dpi=300)
plt.show()
```

---

## ⚖️ Step 4: Handle Class Imbalance (Optional)

The dataset is imbalanced. Options to address this:

### Option 1: Data Augmentation (Already Implemented)

The training script uses augmentation:
- Rotation
- Width/Height shift
- Shear
- Zoom
- Horizontal flip

### Option 2: Class Weights

Add to `train_model.py`:

```python
from sklearn.utils import class_weight
import numpy as np

# Calculate class weights
class_weights = class_weight.compute_class_weight(
    'balanced',
    classes=np.unique(train_generator.classes),
    y=train_generator.classes
)

class_weight_dict = dict(enumerate(class_weights))

# Use in model.fit()
model.fit(
    train_generator,
    class_weight=class_weight_dict,
    # ...
)
```

### Option 3: Oversampling/Undersampling

- Oversample minority classes
- Undersample majority classes
- Use SMOTE or similar techniques

---

## 🔄 Step 5: Train-Validation-Test Split

The training script automatically splits data:
- **Training**: 80%
- **Validation**: 20%

For a separate test set, modify the dataset structure:

```
dataset/
├── train/          # 70%
│   ├── akiec/
│   ├── bcc/
│   └── ...
├── val/            # 15%
│   ├── akiec/
│   └── ...
└── test/           # 15%
    ├── akiec/
    └── ...
```

Split script:

```python
import os
import shutil
import random
from pathlib import Path

dataset_dir = '../dataset'
output_dir = '../dataset_split'

# Create directories
for split in ['train', 'val', 'test']:
    for cls in os.listdir(dataset_dir):
        os.makedirs(os.path.join(output_dir, split, cls), exist_ok=True)

# Split ratios
train_ratio = 0.70
val_ratio = 0.15
test_ratio = 0.15

# Split each class
for cls in os.listdir(dataset_dir):
    cls_dir = os.path.join(dataset_dir, cls)
    images = os.listdir(cls_dir)
    random.shuffle(images)
    
    n_total = len(images)
    n_train = int(n_total * train_ratio)
    n_val = int(n_total * val_ratio)
    
    train_images = images[:n_train]
    val_images = images[n_train:n_train + n_val]
    test_images = images[n_train + n_val:]
    
    # Copy images
    for img in train_images:
        shutil.copy(os.path.join(cls_dir, img), 
                   os.path.join(output_dir, 'train', cls, img))
    
    for img in val_images:
        shutil.copy(os.path.join(cls_dir, img),
                   os.path.join(output_dir, 'val', cls, img))
    
    for img in test_images:
        shutil.copy(os.path.join(cls_dir, img),
                   os.path.join(output_dir, 'test', cls, img))

print("Dataset split complete!")
```

---

## 📊 Step 6: Dataset Statistics

Generate comprehensive statistics:

```python
import os
import matplotlib.pyplot as plt
import numpy as np

dataset_dir = '../dataset'
classes = sorted(os.listdir(dataset_dir))
counts = []

for cls in classes:
    cls_dir = os.path.join(dataset_dir, cls)
    if os.path.isdir(cls_dir):
        counts.append(len(os.listdir(cls_dir)))

# Plot distribution
plt.figure(figsize=(12, 6))

plt.subplot(1, 2, 1)
plt.bar(classes, counts, color='skyblue', edgecolor='black')
plt.xlabel('Class', fontsize=12)
plt.ylabel('Number of Images', fontsize=12)
plt.title('Class Distribution', fontsize=14, fontweight='bold')
plt.xticks(rotation=45)
plt.tight_layout()

plt.subplot(1, 2, 2)
plt.pie(counts, labels=classes, autopct='%1.1f%%', startangle=90)
plt.title('Class Percentage', fontsize=14, fontweight='bold')
plt.tight_layout()

plt.savefig('dataset_statistics.png', dpi=300)
plt.show()

# Print statistics
print("\nDataset Statistics:")
print("=" * 60)
for cls, count in zip(classes, counts):
    print(f"{cls:10s}: {count:5d} images ({count/sum(counts)*100:.1f}%)")
print("=" * 60)
print(f"Total: {sum(counts)} images")
```

---

## ✅ Dataset Checklist

Before training, verify:

- [ ] Dataset downloaded from reliable source
- [ ] Images organized in class-specific folders
- [ ] All 7 classes present
- [ ] Image files are valid (not corrupted)
- [ ] Dataset placed in `dataset/` directory
- [ ] Class distribution reviewed
- [ ] Train/val/test split completed (if using custom split)

---

## 🔧 Alternative Datasets

If HAM10000 is not available, consider:

1. **ISIC Archive**: https://www.isic-archive.com
   - Larger dataset
   - Multiple challenges
   - Requires registration

2. **DermNet**: https://dermnet.com
   - 23 skin disease classes
   - Good for multi-class classification

3. **Skin Cancer MNIST**: https://www.kaggle.com/datasets/kmader/skin-cancer-mnist-ham10000
   - Same as HAM10000 but preprocessed

4. **Custom Dataset**
   - Collect your own images
   - Ensure proper labeling
   - Get medical professional verification

---

## 📝 Notes

- **Image Quality**: Ensure images are clear and well-lit
- **Labeling Accuracy**: Verify labels with medical professionals
- **Data Privacy**: Respect patient privacy and data usage rights
- **Licensing**: Check dataset license for commercial use
- **Augmentation**: The training script includes augmentation to handle the imbalanced dataset

---

## 🆘 Troubleshooting

### Issue: Images not found
**Solution:** Verify image paths in metadata CSV match actual file names.

### Issue: Corrupted images
**Solution:** Remove or replace corrupted files:
```python
from PIL import Image
import os

for cls in os.listdir(dataset_dir):
    cls_dir = os.path.join(dataset_dir, cls)
    for img in os.listdir(cls_dir):
        try:
            img_path = os.path.join(cls_dir, img)
            Image.open(img_path).verify()
        except Exception as e:
            print(f"Corrupted: {img_path}")
            os.remove(img_path)
```

### Issue: Not enough images
**Solution:** 
- Use data augmentation
- Collect more data
- Use transfer learning with pre-trained models

---

**Dataset preparation complete! You're ready to train the model.** 🎉
