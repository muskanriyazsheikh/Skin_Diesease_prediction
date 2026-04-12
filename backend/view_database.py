"""
Database Viewer - View Prediction History (MongoDB)
====================================================
Quick script to view all predictions stored in MongoDB database.
"""

from pymongo import MongoClient
from datetime import datetime
import os

# MongoDB configuration
MONGO_URI = os.environ.get('MONGO_URI', 'mongodb://localhost:27017/')
DB_NAME = os.environ.get('MONGO_DBNAME', 'skin_prediction_db')


def get_mongo_client():
    """Create MongoDB connection."""
    try:
        client = MongoClient(MONGO_URI)
        # Test connection
        client.admin.command('ping')
        return client
    except Exception as e:
        print(f"❌ Failed to connect to MongoDB: {e}")
        print("\n💡 Make sure MongoDB is running:")
        print("   - Windows: net start MongoDB")
        print("   - Or check MongoDB Compass: mongodb://localhost:27017")
        return None


def view_all_predictions():
    """View all predictions in the MongoDB database."""
    client = get_mongo_client()
    if not client:
        return
    
    db = client[DB_NAME]
    collection = db.predictions
    
    print("="*80)
    print("📊 SKIN DISEASE PREDICTION HISTORY (MongoDB)")
    print("="*80)
    
    # Get total count
    total = collection.count_documents({})
    print(f"\n📈 Total predictions: {total}\n")
    
    if total == 0:
        print("⚠️  No predictions found in database.")
        print("   Upload an image through the app to create predictions.")
        client.close()
        return
    
    # Fetch all predictions sorted by timestamp
    predictions = collection.find().sort('timestamp', -1)
    
    # Display predictions
    print(f"{'ID':<25} {'Image':<45} {'Prediction':<35} {'Confidence':<12} {'Timestamp':<25}")
    print("-" * 142)
    
    for pred in predictions:
        pred_id = str(pred.get('_id', ''))[:24]
        filename = pred.get('image_filename', 'N/A')[:45]
        disease = pred.get('predicted_disease', 'N/A')[:35]
        confidence = pred.get('confidence', 0)
        timestamp = pred.get('timestamp', '')
        
        # Format timestamp
        if hasattr(timestamp, 'strftime'):
            formatted_ts = timestamp.strftime('%Y-%m-%d %H:%M:%S')
        else:
            formatted_ts = str(timestamp)[:24]
        
        print(f"{pred_id:<25} {filename:<45} {disease:<35} {confidence:<12.2%} {formatted_ts:<25}")
    
    print("-" * 142)
    
    # Statistics
    print("\n📊 STATISTICS:")
    print("="*80)
    
    # Predictions by disease using aggregation
    pipeline = [
        {
            '$group': {
                '_id': '$predicted_disease',
                'count': {'$sum': 1},
                'avg_conf': {'$avg': '$confidence'}
            }
        },
        {'$sort': {'count': -1}}
    ]
    
    disease_stats = list(collection.aggregate(pipeline))
    
    print("\n🔬 Predictions by Disease:")
    for stat in disease_stats:
        disease = stat['_id'] or 'Unknown'
        count = stat['count']
        avg_conf = stat['avg_conf']
        print(f"  {disease:<40} {count:>5} predictions  (Avg confidence: {avg_conf:.2%})")
    
    # Recent predictions (last 7 days)
    from datetime import timedelta
    seven_days_go = datetime.utcnow() - timedelta(days=7)
    recent_count = collection.count_documents({'timestamp': {'$gte': seven_days_ago}})
    print(f"\n📅 Predictions in last 7 days: {recent_count}")
    
    # Average confidence
    avg_result = collection.aggregate([{'$group': {'_id': None, 'avg_conf': {'$avg': '$confidence'}}}])
    avg_confidence = list(avg_result)[0]['avg_conf'] if avg_result else 0
    print(f"📈 Overall average confidence: {avg_confidence:.2%}")
    
    client.close()
    print("\n" + "="*80)


def view_recent_predictions(limit=10):
    """View only the most recent predictions."""
    client = get_mongo_client()
    if not client:
        return
    
    db = client[DB_NAME]
    collection = db.predictions
    
    print(f"\n🕐 RECENT {limit} PREDICTIONS:")
    print("="*80)
    
    predictions = collection.find().sort('timestamp', -1).limit(limit)
    
    prediction_list = list(predictions)
    if not prediction_list:
        print("⚠️  No predictions found.")
        client.close()
        return
    
    for pred in prediction_list:
        pred_id = str(pred.get('_id', ''))[:24]
        filename = pred.get('image_filename', 'N/A')
        disease = pred.get('predicted_disease', 'N/A')
        confidence = pred.get('confidence', 0)
        timestamp = pred.get('timestamp', '')
        
        # Format timestamp
        if hasattr(timestamp, 'strftime'):
            formatted_ts = timestamp.strftime('%Y-%m-%d %H:%M:%S')
        else:
            formatted_ts = str(timestamp)[:24]
        
        print(f"\n  ID: {pred_id}")
        print(f"  Image: {filename}")
        print(f"  Prediction: {disease}")
        print(f"  Confidence: {confidence:.2%}")
        print(f"  Time: {formatted_ts}")
        print("  " + "-"*76)
    
    client.close()


if __name__ == "__main__":
    print("\n1️⃣  View ALL predictions")
    print("2️⃣  View RECENT predictions")
    
    choice = input("\nChoose option (1 or 2): ").strip()
    
    if choice == '1':
        view_all_predictions()
    elif choice == '2':
        limit = input("How many recent predictions? (default 10): ").strip()
        limit = int(limit) if limit.isdigit() else 10
        view_recent_predictions(limit)
    else:
        print("❌ Invalid choice")
