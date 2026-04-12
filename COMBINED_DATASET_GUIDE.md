# Combined HAM10000 + ISIC Dataset Setup Guide

This guide will help you download, organize, and train your skin disease classification model using both HAM10000 and ISIC datasets for improved accuracy.

---

## 📋 Overview

**Benefits of combining datasets:**
- **More training data**: ISIC adds thousands of additional skin lesion images
- **Better generalization**: More diverse samples improve model performance
- **Improved accuracy**: Larger dataset helps the model learn better features
- **Reduced overfitting**: More data prevents the model from memorizing training examples

**Expected Results:**
- HAM10000 alone: ~10,015 images
- HAM10000 + ISIC: ~25,000+ images (depending on ISIC version)
- Expected accuracy improvement: 5-15%

---

## Step 1: Download the Datasets

### Option A: Download from Kaggle (Recommended)

#### 1.1 Download HAM10000 Dataset
1. Go to: https://www.kaggle.com/datasets/kmader/skin-cancer-mnist-ham10000
2. Click "Download" button
3. Extract the downloaded ZIP file

You should get:
- `HAM10000_metadata.csv` - Contains image IDs and diagnosis labels
- `HAM10000_images_part1.zip` and `HAM10000_images_part2.zip` - Image files
- Extract both image ZIPs into a single folder

#### 1.2 Download ISIC Dataset
1. Go to: https://www.kaggle.com/datasets/tschandl/isic-archive
2. Click "Download" button
3. Extract the downloaded ZIP file

You should get:
- Metadata CSV file (may be named `ISIC_metadata.csv` or similar)
- Image files in a folder

### Option B: Use Kaggle API

```bash
# Install Kaggle API
pip install kaggle

# Download HAM10000
kaggle datasets download -d kmader/skin-cancer-mnist-ham10000
unzip skin-cancer-mnist-ham10000.zip -d HAM10000_dataset

# Download ISIC
kaggle datasets download -d tschandl/isic-archive
unzip isic-archive.zip -d ISIC_dataset
```

---

## Step 2: Organize Your Files

After downloading, structure your files like this:

```
C:/Users/ACER/Downloads/
├── HAM10000_metadata.csv          # HAM10000 metadata
├── HAM10000_images/               # Folder with HAM10000 images
│   ├── ISIC_0000000.jpg
│   ├── ISIC_0000001.jpg
│   └── ...
├── ISIC_metadata.csv              # ISIC metadata (name may vary)
└── ISIC_images/                   # Folder with ISIC images
    ├── ISIC_0001234.jpg
    ├── ISIC_0001235.jpg
    └── ...
```

---

## Step 3: Configure the Organization Script

Open `model/organize_combined_dataset.py` and update the paths:

```python
# Update these paths to match your setup
HAM10000_METADATA_CSV = 'C:/Users/ACER/Downloads/HAM10000_metadata.csv'
HAM10000_IMAGE_FOLDER = 'C:/Users/ACER/Downloads/HAM10000_images'

ISIC_METADATA_CSV = 'C:/Users/ACER/Downloads/ISIC_metadata.csv'
ISIC_IMAGE_FOLDER = 'C:/Users/ACER/Downloads/ISIC_images'

OUTPUT_DIR = '../dataset_combined'
```

**Important:** The ISIC dataset may have different column names in the metadata. The script will display available columns when run, so you can verify the mapping.

---

## Step 4: Run the Organization Script

```bash
cd model
python organize_combined_dataset.py
```

The script will:
1. ✅ Create class folders (akiec, bcc, bkl, df, mel, nv, vas)
2. ✅ Copy HAM10000 images with `ham_` prefix
3. ✅ Copy ISIC images with `isic_` prefix
4. ✅ Display statistics about the combined dataset
5. ✅ Save dataset stats to `dataset_combined/dataset_stats.json`

**Expected Output:**
```
Combined Dataset Statistics
============================================================
akiec    (Actinic keratoses                ):  1500 images
bcc      (Basal cell carcinoma             ):  2000 images
bkl      (Benign keratosis-like lesions    ):  4000 images
df       (Dermatofibroma                   ):   500 images
mel      (Melanoma                         ):  4500 images
nv       (Melanocytic nevi                 ): 12000 images
vas      (Vascular lesions                 ):  1000 images
============================================================
Total: 25500 images
============================================================
```

---

## Step 5: Update Training Configuration

Open `model/train_model.py` and update the dataset path:

```python
# Change this line:
DATASET_DIR = "../dataset_combined"  # Use combined dataset
```

**Optional: Adjust training parameters**

```python
# For larger datasets, you can increase batch size and epochs
BATCH_SIZE = 32              # Increase to 64 if you have enough RAM/VRAM
EPOCHS = 50                  # Phase 1: Feature extraction
EPOCHS_FINE_TUNE = 30        # Phase 2: Fine-tuning

# Advanced options
USE_CLASS_WEIGHTS = True     # Handle class imbalance (recommended)
USE_FINE_TUNING = True       # Enable 2-phase training (recommended)
FINE_TUNE_FROM_LAYER = 100   # Unfreeze layers from this index
```

---

## Step 6: Train the Model

```bash
cd model
python train_model.py
```

**Training Process:**

### Phase 1: Feature Extraction (50 epochs)
- MobileNetV2 base is **frozen**
- Only trains the custom classifier layers
- Learning rate: 0.001
- Uses class weights to handle imbalance
- Saves best model based on validation accuracy

### Phase 2: Fine-Tuning (up to 30 epochs)
- Unfrees top layers of MobileNetV2 (from layer 100)
- Trains with **much lower learning rate** (1e-5)
- Helps model learn dataset-specific features
- Further improves accuracy by 3-8%

**Expected Training Time:**
- Phase 1: 30-60 minutes (depends on GPU)
- Phase 2: 20-40 minutes
- Total: ~1-1.5 hours with GPU

**Without GPU:** May take 3-5 hours total

---

## Step 7: Evaluate the Model

```bash
cd model
python evaluate_model.py
```

This will generate:
- ✅ Confusion matrix visualization
- ✅ Classification report (precision, recall, F1-score per class)
- ✅ Overall metrics saved to `model_metrics.json`

**Expected Performance with Combined Dataset:**

| Metric | HAM10000 Only | HAM10000 + ISIC |
|--------|---------------|-----------------|
| Accuracy | 80-85% | 87-93% |
| Precision | 79-84% | 86-92% |
| Recall | 78-83% | 85-91% |
| F1-Score | 78-83% | 85-91% |

---

## 🔧 Troubleshooting

### Issue: "Metadata file not found"
**Solution:** Double-check the file paths in `organize_combined_dataset.py`. Use absolute paths.

### Issue: "CUDA out of memory"
**Solution:** Reduce batch size:
```python
BATCH_SIZE = 16  # or even 8
```

### Issue: ISIC metadata has different column names
**Solution:** The script will display available columns. Update this mapping:
```python
ISIC_DX_MAPPING = {
    'your_column_value': 'akiec',  # Map ISIC diagnosis to our classes
    # ... add more mappings
}
```

### Issue: Training is very slow
**Solution:** 
- Use GPU if available
- Reduce image size (change `IMG_HEIGHT` and `IMG_WIDTH` to 128)
- Reduce batch size
- Use fewer epochs initially to test

### Issue: Class imbalance still affecting results
**Solution:** The script already uses class weights. If needed, you can:
1. Increase augmentation for minority classes
2. Use oversampling techniques
3. Collect more data for underrepresented classes

---

## 📊 Dataset Statistics

### HAM10000 Distribution:
| Class | Code | Images |
|-------|------|--------|
| Melanocytic nevi | nv | 6,705 |
| Melanoma | mel | 1,113 |
| Benign keratosis | bkl | 1,099 |
| Basal cell carcinoma | bcc | 514 |
| Actinic keratoses | akiec | 327 |
| Dermatofibroma | df | 115 |
| Vascular lesions | vas | 142 |
| **Total** | | **10,015** |

### After Adding ISIC:
Expected to increase each class by 1.5x-3x depending on ISIC version.

---

## 🚀 Next Steps After Training

1. **Test the model** with real images using the Flask backend
2. **Deploy to production** following DEPLOYMENT.md
3. **Monitor performance** and collect feedback
4. **Retrain periodically** with new data to improve accuracy

---

## 📝 Additional Tips

### For Best Results:
1. **Use GPU**: Training is 5-10x faster with GPU
2. **Don't skip fine-tuning**: Phase 2 typically adds 3-8% accuracy
3. **Monitor overfitting**: If validation accuracy decreases, reduce epochs
4. **Experiment with learning rates**: Try different values if results aren't optimal
5. **Save checkpoints**: The script automatically saves the best model

### Advanced Improvements:
- Try different base models (EfficientNet, ResNet50, Xception)
- Use ensemble methods (combine multiple models)
- Implement test-time augmentation (TTA)
- Add Grad-CAM visualization for explainability

---

## 🆘 Need Help?

If you encounter issues:
1. Check the error message carefully
2. Verify all file paths are correct
3. Ensure datasets are properly extracted
4. Check that you have enough disk space (combined dataset: 5-15 GB)
5. Review the troubleshooting section above

---

**Good luck with your training! 🎯**

With the combined HAM10000 + ISIC dataset and the improved 2-phase training approach, you should see significant improvements in model accuracy and robustness.
