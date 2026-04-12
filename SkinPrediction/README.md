# SkinAI - AI-Powered Skin Disease Detection System

A complete production-ready web application that uses Convolutional Neural Networks (CNN) to detect and classify skin diseases from uploaded images. Built with TensorFlow, Flask, and React.

![SkinAI](https://img.shields.io/badge/version-1.0.0-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![React](https://img.shields.io/badge/react-18.2.0-blue.svg)

---

## 🎯 Features

- **AI-Powered Detection**: CNN deep learning model trained on HAM10000 dataset
- **7 Skin Conditions**: Detects melanoma, basal cell carcinoma, actinic keratoses, and more
- **Instant Results**: Get predictions with confidence scores in seconds
- **Treatment Recommendations**: Detailed treatment options and precautions
- **Modern UI**: Beautiful, responsive interface built with React and Tailwind CSS
- **Prediction History**: Store and view past predictions
- **Medical Disclaimer**: Clear disclaimers emphasizing professional consultation

---

## 🧠 Detectable Skin Diseases

1. **Melanocytic nevi (nv)** - Common moles
2. **Melanoma (mel)** - Serious skin cancer
3. **Benign keratosis-like lesions (bkl)** - Age spots
4. **Basal cell carcinoma (bcc)** - Common skin cancer
5. **Actinic keratoses (akiec)** - Precancerous lesions
6. **Vascular lesions (vas)** - Blood vessel abnormalities
7. **Dermatofibroma (df)** - Benign skin growth

---

## 🛠️ Tech Stack

### Backend
- **Framework**: Flask (Python)
- **Machine Learning**: TensorFlow 2.15.0, Keras
- **Database**: SQLite (with SQLAlchemy ORM)
- **Production Server**: Gunicorn
- **API**: RESTful architecture

### Frontend
- **Framework**: React 18.2
- **Build Tool**: Vite
- **Styling**: Tailwind CSS
- **Routing**: React Router v6
- **Animations**: Framer Motion
- **HTTP Client**: Axios
- **File Upload**: React Dropzone

---

## 📂 Project Structure

```
SkinPrediction/
├── backend/                    # Flask REST API
│   ├── app.py                 # Main Flask application
│   ├── config.py              # Configuration settings
│   ├── requirements.txt       # Python dependencies
│   ├── gunicorn.conf.py       # Production server config
│   ├── models/                # Database models
│   │   ├── __init__.py
│   │   └── prediction.py
│   ├── routes/                # API endpoints
│   │   ├── __init__.py
│   │   └── api.py
│   └── utils/                 # Helper functions
│       ├── disease_info.py    # Disease database
│       └── file_handler.py    # File upload utilities
├── model/                     # ML Model
│   ├── train_model.py         # Training script
│   ├── evaluate_model.py      # Evaluation script
│   ├── model_utils.py         # Preprocessing functions
│   ├── skin_disease_model.h5  # Trained model (after training)
│   └── class_labels.json      # Class labels (after training)
├── frontend/                  # React application
│   ├── src/
│   │   ├── components/        # Reusable UI components
│   │   │   ├── Navbar.jsx
│   │   │   ├── Footer.jsx
│   │   │   ├── ConfidenceBar.jsx
│   │   │   └── Disclaimer.jsx
│   │   ├── pages/             # Page components
│   │   │   ├── HomePage.jsx
│   │   │   ├── UploadPage.jsx
│   │   │   └── ResultPage.jsx
│   │   ├── services/          # API calls
│   │   │   └── api.js
│   │   ├── App.jsx
│   │   ├── main.jsx
│   │   └── index.css
│   ├── package.json
│   ├── vite.config.js
│   ├── tailwind.config.js
│   └── index.html
├── dataset/                   # Training data (HAM10000)
└── README.md                  # This file
```

---

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- Node.js 16 or higher
- npm or yarn
- 4GB RAM minimum (8GB recommended for model training)

### Step 1: Clone the Repository

```bash
git clone <repository-url>
cd SkinPrediction
```

### Step 2: Train the Model (or use pre-trained)

```bash
# Navigate to model directory
cd model

# Install Python dependencies
pip install tensorflow numpy matplotlib scikit-learn

# Prepare dataset
# Download HAM10000 dataset from: https://www.kaggle.com/datasets/kmader/skin-cancer-mnist-ham10000
# Organize into folders:
# dataset/
#   ├── akiec/
#   ├── bcc/
#   ├── bkl/
#   ├── df/
#   ├── mel/
#   ├── nv/
#   └── vas/

# Train the model
python train_model.py

# Evaluate the model
python evaluate_model.py

# Return to root directory
cd ..
```

**Note**: Model training takes 2-4 hours on CPU (faster with GPU). You can also download a pre-trained model.

### Step 3: Setup Backend

```bash
# Navigate to backend directory
cd backend

# Create virtual environment (recommended)
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Start the Flask server
python app.py
```

Backend will run on `http://localhost:5000`

### Step 4: Setup Frontend

```bash
# Open a new terminal and navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

Frontend will run on `http://localhost:3000`

### Step 5: Access the Application

Open your browser and navigate to: `http://localhost:3000`

---

## 📡 API Documentation

### Base URL
```
http://localhost:5000
```

### Endpoints

#### 1. Health Check
```http
GET /api/health
```

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2024-01-01T00:00:00.000Z",
  "model_loaded": true,
  "database": "connected",
  "version": "1.0.0"
}
```

#### 2. Predict Disease
```http
POST /api/predict
Content-Type: multipart/form-data

Form Data:
- image: <image_file>
```

**Response:**
```json
{
  "success": true,
  "prediction": {
    "disease": "Melanocytic nevi",
    "confidence": 0.92,
    "all_probabilities": {
      "Melanocytic nevi": 0.92,
      "Benign keratosis-like lesions": 0.05,
      ...
    }
  },
  "disease_info": {
    "description": "...",
    "symptoms": ["...", "..."],
    "treatment": "...",
    "precautions": ["...", "..."],
    "severity": "Low",
    "consultation": "..."
  },
  "disclaimer": "...",
  "timestamp": "2024-01-01T00:00:00.000Z"
}
```

#### 3. Get Prediction History
```http
GET /api/history?limit=10
```

#### 4. Get All Diseases Info
```http
GET /api/diseases
```

---

## 🗄️ Database

The application uses SQLite to store prediction history.

**Schema:**
- `predictions` table
  - `id`: Primary key
  - `image_filename`: Uploaded image name
  - `predicted_disease`: Prediction result
  - `confidence`: Confidence score (0-1)
  - `timestamp`: Prediction date/time
  - `ip_address`: User IP (optional)

Database file: `backend/predictions.db` (auto-created on first run)

---

## 🔒 Security Features

- File type validation (images only)
- File size limit (5MB max)
- Secure filename generation (UUID)
- CORS configuration
- Input sanitization
- Environment variables for sensitive data
- Automatic cleanup of old uploads

---

## 🌐 Deployment

### Deploy Backend to Render

1. **Create GitHub Repository**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git push origin main
   ```

2. **Setup on Render**
   - Go to [render.com](https://render.com)
   - Click "New +" → "Web Service"
   - Connect your GitHub repository
   - Configure:
     - **Name**: skin-detection-api
     - **Environment**: Python
     - **Build Command**: `cd backend && pip install -r requirements.txt`
     - **Start Command**: `cd backend && gunicorn -c gunicorn.conf.py app:app`
     - **Plan**: Free or Paid

3. **Set Environment Variables**
   ```
   SECRET_KEY=your-secret-key-here
   FLASK_ENV=production
   FRONTEND_URL=https://your-frontend-url.vercel.app
   ```

4. **Deploy**
   - Click "Create Web Service"
   - Wait for deployment to complete
   - Copy your backend URL

### Deploy Frontend to Vercel

1. **Update API URL**
   
   Create `.env` file in `frontend/` directory:
   ```
   VITE_API_URL=https://your-backend-url.onrender.com
   ```

2. **Build Frontend**
   ```bash
   cd frontend
   npm run build
   ```

3. **Deploy to Vercel**
   ```bash
   # Install Vercel CLI
   npm install -g vercel
   
   # Deploy
   vercel
   ```

   Or use Vercel Dashboard:
   - Go to [vercel.com](https://vercel.com)
   - Click "New Project"
   - Import your GitHub repository
   - Set root directory to `frontend`
   - Add environment variable: `VITE_API_URL`
   - Deploy

4. **Update Backend CORS**
   
   Update `FRONTEND_URL` environment variable on Render with your Vercel URL.

---

## 🧪 Testing

### Test Backend API

```bash
# Test health endpoint
curl http://localhost:5000/api/health

# Test prediction endpoint
curl -X POST http://localhost:5000/api/predict \
  -F "image=@path/to/test-image.jpg"
```

### Test Frontend

1. Open browser to `http://localhost:3000`
2. Navigate to Upload page
3. Upload a test image
4. Verify prediction results display correctly

---

## 📊 Model Performance

After training, check the following files:
- `model/model_metrics.json` - Accuracy, precision, recall, F1-score
- `model/confusion_matrix.png` - Confusion matrix visualization
- `model/training_history.png` - Training/validation curves

**Target Metrics:**
- Accuracy: ≥ 85%
- Precision: ≥ 85%
- Recall: ≥ 85%
- F1-Score: ≥ 85%

---

## 🔧 Configuration

### Backend Configuration (`backend/config.py`)

```python
SECRET_KEY = 'your-secret-key'
SQLALCHEMY_DATABASE_URI = 'sqlite:///predictions.db'
UPLOAD_FOLDER = 'uploads'
MAX_CONTENT_LENGTH = 5 * 1024 * 1024  # 5MB
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
```

### Frontend Configuration (`.env`)

```env
VITE_API_URL=http://localhost:5000
```

---

## 🐛 Troubleshooting

### Issue: Model not found
**Solution:** Run `python train_model.py` in the `model/` directory first.

### Issue: CORS errors
**Solution:** Ensure `FRONTEND_URL` is set correctly in backend environment variables.

### Issue: Port already in use
**Solution:** Change port in `backend/app.py` or `frontend/vite.config.js`

### Issue: Module not found
**Solution:** Run `pip install -r requirements.txt` in backend directory.

### Issue: npm install fails
**Solution:** Clear npm cache: `npm cache clean --force` and retry.

---

## 📝 Development Guidelines

### Adding New Disease Classes

1. Update `model/train_model.py` with new class
2. Retrain the model
3. Add disease info to `backend/utils/disease_info.py`
4. Update frontend if needed

### Modifying Model Architecture

Edit `build_cnn_model()` function in `model/train_model.py`

### Adding New API Endpoints

Create new route in `backend/routes/api.py`

---

## 📄 License

This project is licensed under the MIT License.

---

## ⚠️ Medical Disclaimer

**IMPORTANT**: This application is for **INFORMATIONAL PURPOSES ONLY** and should NOT be considered a medical diagnosis. Always consult with a qualified dermatologist or healthcare professional for proper medical advice, diagnosis, and treatment.

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📧 Contact

For questions or support:
- Email: support@skinai.com
- GitHub Issues: Create an issue in this repository

---

## 🙏 Acknowledgments

- HAM10000 Dataset: [Kaggle](https://www.kaggle.com/datasets/kmader/skin-cancer-mnist-ham10000)
- TensorFlow Documentation
- Flask Documentation
- React Documentation

---

**Made with ❤️ for better skin health awareness**
