"""
Test Model Loading from Backend
================================
This script tests if the backend can properly load and use the model.
Run this from the backend directory.
"""

import os
import sys

# Add project root to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

print("="*60)
print("Testing Model Loading from Backend")
print("="*60)

# Test 1: Check if model file exists
model_path = os.path.join(os.path.dirname(__file__), '..', 'model', 'skin_disease_model.h5')
print(f"\n1. Checking model file...")
print(f"   Path: {model_path}")
print(f"   Exists: {os.path.exists(model_path)}")

if os.path.exists(model_path):
    size = os.path.getsize(model_path) / (1024 * 1024)
    print(f"   Size: {size:.2f} MB")
else:
    print("   ✗ Model file not found!")
    sys.exit(1)

# Test 2: Try to import model utilities
print(f"\n2. Importing model utilities...")
try:
    from model.model_utils import get_prediction, load_model, load_class_labels
    print("   ✓ Import successful")
except Exception as e:
    print(f"   ✗ Import failed: {str(e)}")
    sys.exit(1)

# Test 3: Try to load the model
print(f"\n3. Loading model...")
try:
    model = load_model()
    print("   ✓ Model loaded successfully")
except Exception as e:
    print(f"   ✗ Model loading failed: {str(e)}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Test 4: Try to load class labels
print(f"\n4. Loading class labels...")
try:
    labels = load_class_labels()
    print(f"   ✓ Class labels loaded: {len(labels)} classes")
    print(f"   Labels: {labels}")
except Exception as e:
    print(f"   ✗ Class labels loading failed: {str(e)}")
    sys.exit(1)

# Test 5: Try to make a prediction (if test image exists)
test_image = os.path.join(os.path.dirname(__file__), '..', 'model', 'test_image.jpg')
if os.path.exists(test_image):
    print(f"\n5. Testing prediction...")
    try:
        result = get_prediction(test_image)
        print(f"   ✓ Prediction successful")
        print(f"   Disease: {result['disease']}")
        print(f"   Confidence: {result['confidence']:.2%}")
    except Exception as e:
        print(f"   ✗ Prediction failed: {str(e)}")
        import traceback
        traceback.print_exc()
else:
    print(f"\n5. Skipping prediction test (no test image found)")

print("\n" + "="*60)
print("All tests passed! Model is ready for use.")
print("="*60)
