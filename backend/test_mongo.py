"""
Test MongoDB Connection and Save
=================================
Quick test to verify MongoDB is working properly.
"""

from flask import Flask
from extensions import init_mongo, get_mongo_db, get_mongo_client
from config import config
from datetime import datetime

# Create Flask app
app = Flask(__name__)
app.config.from_object(config['development'])

# Initialize MongoDB
print(f"MONGO_URI: {app.config.get('MONGO_URI')}")
init_mongo(app)
print(f"✓ MongoDB initialized")

# Test with app context
with app.app_context():
    mongo_db = get_mongo_db()
    mongo_client = get_mongo_client()
    
    print(f"\nMongo DB: {mongo_db}")
    print(f"Mongo DB name: {mongo_db.name if mongo_db is not None else 'N/A'}")
    
    # Test connection
    try:
        result = mongo_db.command('ping')
        print(f"✓ MongoDB ping successful: {result}")
    except Exception as e:
        print(f"❌ MongoDB ping failed: {e}")
    
    # Try to insert a test document
    try:
        test_doc = {
            'image_filename': 'test_image.jpg',
            'predicted_disease': 'Test Disease',
            'confidence': 0.95,
            'timestamp': datetime.utcnow(),
            'ip_address': '127.0.0.1'
        }
        
        result = mongo_db.predictions.insert_one(test_doc)
        print(f"✓ Test document inserted with ID: {result.inserted_id}")
        
        # Query it back
        doc = mongo_db.predictions.find_one({'_id': result.inserted_id})
        print(f"✓ Retrieved document: {doc}")
        
        # Clean up
        mongo_db.predictions.delete_one({'_id': result.inserted_id})
        print(f"✓ Test document deleted")
        
    except Exception as e:
        print(f"❌ Insert failed: {e}")
        import traceback
        traceback.print_exc()

print("\n✅ MongoDB test complete!")
