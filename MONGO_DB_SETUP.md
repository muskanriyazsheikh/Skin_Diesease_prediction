# MongoDB Setup Guide for Skin Prediction Project

🚀 **Congratulations!** Your project has been migrated from SQLite to **MongoDB** - a modern, scalable NoSQL database!

---

## 📋 What Changed?

| Feature | Before (SQLite) | After (MongoDB) |
|---------|----------------|-----------------|
| **Database Type** | Relational (SQL) | Document-based (NoSQL) |
| **Scalability** | Limited | Horizontal scaling |
| **Schema** | Fixed schema | Flexible schema |
| **Performance** | Good for small data | Excellent for large data |
| **Modern Stack** | Traditional | Trending & Industry Standard |
| **Cloud Ready** | Difficult | Native cloud support |

---

## Step 1: Install MongoDB

### **Option A: Install MongoDB Community Edition (Windows)**

1. **Download MongoDB:**
   - Go to: https://www.mongodb.com/try/download/community
   - Select: Windows x64
   - Download the MSI installer

2. **Install MongoDB:**
   - Run the downloaded `.msi` file
   - Choose "Complete" installation
   - ✅ Check "Install MongoDB as a Service"
   - ✅ Check "Run service as Network Service user"
   - Complete the installation

3. **Verify Installation:**
   ```bash
   # Open Command Prompt or PowerShell
   mongod --version
   ```
   You should see version information like: `db version v7.0.x`

### **Option B: Use MongoDB Atlas (Cloud - FREE)**

If you want cloud database (accessible from anywhere):

1. Go to: https://www.mongodb.com/cloud/atlas/register
2. Create a free account
3. Create a free cluster (M0 - Free Forever)
4. Get your connection string (looks like: `mongodb+srv://username:password@cluster.mongodb.net/`)
5. Update `.env` file with your connection string (see Step 3)

---

## Step 2: Start MongoDB Service

### **Windows:**

MongoDB should start automatically as a service. Verify it's running:

```bash
# Check if MongoDB is running
net start MongoDB

# If not running, start it:
net start MongoDB
```

### **Alternative: Manual Start**

```bash
# Start MongoDB manually
mongod

# This will start MongoDB on default port 27017
```

---

## Step 3: Install Python Dependencies

Navigate to the backend folder and install the new MongoDB packages:

```bash
cd c:\Users\ACER\Downloads\SkinPrediction\backend

# Install dependencies (will install pymongo and flask-pymongo)
pip install -r requirements.txt
```

**What's installed:**
- `pymongo==4.6.1` - MongoDB Python driver
- `flask-pymongo==2.3.0` - Flask integration for MongoDB

---

## Step 4: Configure MongoDB Connection

### **For Local MongoDB (Development):**

Create or update the `.env` file in the `backend/` folder:

```env
# MongoDB Configuration
MONGO_URI=mongodb://localhost:27017/
MONGO_DBNAME=skin_prediction_db

# Other configurations
SECRET_KEY=your-secret-key-here
FLASK_ENV=development
```

### **For MongoDB Atlas (Cloud/Production):**

```env
# MongoDB Atlas Configuration
MONGO_URI=mongodb+srv://username:password@cluster.mongodb.net/
MONGO_DBNAME=skin_prediction_db

# Other configurations
SECRET_KEY=your-secret-key-here
FLASK_ENV=production
```

Replace `username`, `password`, and `cluster.mongodb.net` with your actual Atlas credentials.

---

## Step 5: Install MongoDB Compass (Optional but Recommended)

**MongoDB Compass** is a GUI tool to view and manage your database visually:

1. **Download:** https://www.mongodb.com/try/download/compass
2. **Install:** Run the installer
3. **Connect:**
   - Open MongoDB Compass
   - Connection string: `mongodb://localhost:27017`
   - Click "Connect"
4. **View Data:**
   - Navigate to `skin_prediction_db` database
   - Click on `predictions` collection
   - See all your predictions in a nice UI!

---

## Step 6: Test the Migration

### **Start the Backend:**

```bash
cd c:\Users\ACER\Downloads\SkinPrediction\backend
python app.py
```

You should see:
```
✓ MongoDB indexes created
Database indexes created
 * Running on http://0.0.0.0:5000
```

### **Test Health Endpoint:**

Open browser or use Postman:
```
http://localhost:5000/api/health
```

Expected response:
```json
{
  "status": "healthy",
  "timestamp": "2026-04-10T14:30:00",
  "model_loaded": true,
  "database": "connected",
  "database_type": "MongoDB",
  "version": "1.0.0"
}
```

---

## Step 7: View Your Database

### **Option 1: Using the Viewer Script**

```bash
cd backend
python view_database.py
```

This will show:
- ✅ All predictions in formatted table
- ✅ Statistics by disease type
- ✅ Average confidence scores
- ✅ Recent predictions count

### **Option 2: Using MongoDB Compass (GUI)**

1. Open MongoDB Compass
2. Connect to: `mongodb://localhost:27017`
3. Navigate to: `skin_prediction_db` → `predictions`
4. View all documents visually!

### **Option 3: Using MongoDB Shell**

```bash
# Open MongoDB shell
mongosh

# Use the database
use skin_prediction_db

# View all predictions
db.predictions.find().pretty()

# Count predictions
db.predictions.countDocuments()

# View statistics
db.predictions.aggregate([
  {
    $group: {
      _id: "$predicted_disease",
      count: { $sum: 1 },
      avgConfidence: { $avg: "$confidence" }
    }
  }
])

# Exit
exit
```

---

## 📊 MongoDB Document Structure

Your predictions are now stored as JSON-like documents:

```json
{
  "_id": ObjectId("65f1a2b3c4d5e6f7g8h9i0j1"),
  "image_filename": "abc123.jpg",
  "predicted_disease": "Melanocytic nevi",
  "confidence": 0.9234,
  "timestamp": ISODate("2026-04-10T14:30:00Z"),
  "ip_address": "192.168.1.100"
}
```

---

## 🔍 Useful MongoDB Queries

### **View Recent Predictions:**
```javascript
db.predictions.find().sort({timestamp: -1}).limit(10)
```

### **Filter by Disease:**
```javascript
db.predictions.find({predicted_disease: "Melanoma"})
```

### **High Confidence Predictions (>90%):**
```javascript
db.predictions.find({confidence: {$gt: 0.9}})
```

### **Statistics by Disease:**
```javascript
db.predictions.aggregate([
  {
    $group: {
      _id: "$predicted_disease",
      count: {$sum: 1},
      avgConfidence: {$avg: "$confidence"}
    }
  },
  {$sort: {count: -1}}
])
```

### **Delete All Predictions:**
```javascript
db.predictions.deleteMany({})
```

---

## 🚀 MongoDB Benefits You Now Have

### **1. Scalability**
- Handle millions of predictions
- Easy horizontal scaling with sharding
- Better performance as data grows

### **2. Flexibility**
- No schema migrations needed
- Add new fields anytime
- Store nested data easily

### **3. Performance**
- Faster read/write operations
- Better indexing options
- Aggregation pipeline for analytics

### **4. Modern Stack**
- Industry standard for 2024+
- Cloud-native (Atlas)
- Great for microservices

### **5. Developer Experience**
- JSON-like documents
- Easy to work with in Python/JavaScript
- Rich query language

---

## 🔧 Troubleshooting

### **Issue: "Failed to connect to MongoDB"**

**Solution:**
```bash
# Check if MongoDB is running
net start MongoDB

# Or start manually
mongod
```

### **Issue: "pymongo not found"**

**Solution:**
```bash
cd backend
pip install pymongo flask-pymongo
```

### **Issue: MongoDB Compass can't connect**

**Solution:**
- Make sure MongoDB service is running
- Connection string: `mongodb://localhost:27017`
- Check if port 27017 is not blocked by firewall

### **Issue: Port 27017 already in use**

**Solution:**
```bash
# Find what's using the port
netstat -ano | findstr :27017

# Kill the process (replace PID with actual process ID)
taskkill /PID <PID> /F
```

---

## 📈 Migration Complete Checklist

- ✅ Replaced `flask-sqlalchemy` with `pymongo` and `flask-pymongo`
- ✅ Updated `config.py` for MongoDB connection
- ✅ Converted SQLAlchemy models to MongoDB documents
- ✅ Updated all API routes to use MongoDB queries
- ✅ Created indexes for better performance
- ✅ Updated database viewer script
- ✅ Added MongoDB-specific error handling

---

## 🎯 Next Steps

1. **Install MongoDB** (if not already installed)
2. **Start MongoDB service**: `net start MongoDB`
3. **Install dependencies**: `pip install -r requirements.txt`
4. **Test the backend**: `python app.py`
5. **View in Compass** (optional): Download MongoDB Compass
6. **Make predictions** through your app - they'll be saved to MongoDB!

---

## 📚 Learn MongoDB

- **Official Docs:** https://www.mongodb.com/docs/
- **MongoDB University (Free):** https://university.mongodb.com/
- **PyMongo Docs:** https://pymongo.readthedocs.io/
- **MongoDB Compass:** https://www.mongodb.com/products/compass

---

**🎉 Congratulations! Your project is now using modern MongoDB technology!**

This migration makes your project:
- ✅ More scalable
- ✅ Industry-relevant
- ✅ Cloud-ready
- ✅ Performance-optimized
- ✅ Future-proof

You're now using the same database technology as companies like Uber, Spotify, and eBay! 🚀
