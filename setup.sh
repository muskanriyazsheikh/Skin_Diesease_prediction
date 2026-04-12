#!/bin/bash

echo "============================================"
echo "SkinAI - Quick Setup Script"
echo "============================================"
echo ""

# Check Python
echo "[1/4] Checking Python installation..."
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python3 is not installed or not in PATH"
    echo "Please install Python 3.8+ from https://www.python.org/"
    exit 1
fi
echo "Python found!"
echo ""

# Check Node.js
echo "[2/4] Checking Node.js installation..."
if ! command -v node &> /dev/null; then
    echo "ERROR: Node.js is not installed or not in PATH"
    echo "Please install Node.js 16+ from https://nodejs.org/"
    exit 1
fi
echo "Node.js found!"
echo ""

# Setup Backend
echo "[3/4] Setting up Backend..."
cd backend || exit
echo "Creating virtual environment..."
python3 -m venv venv
source venv/bin/activate
echo "Installing Python dependencies..."
pip install -r requirements.txt
cd ..
echo "Backend setup complete!"
echo ""

# Setup Frontend
echo "[4/4] Setting up Frontend..."
cd frontend || exit
echo "Installing Node dependencies..."
npm install
cd ..
echo "Frontend setup complete!"
echo ""

echo "============================================"
echo "Setup Complete!"
echo "============================================"
echo ""
echo "Next steps:"
echo "1. Train the model (if not already done):"
echo "   cd model"
echo "   python train_model.py"
echo ""
echo "2. Start the backend server:"
echo "   cd backend"
echo "   source venv/bin/activate"
echo "   python app.py"
echo ""
echo "3. Start the frontend (in a new terminal):"
echo "   cd frontend"
echo "   npm run dev"
echo ""
echo "4. Open your browser to: http://localhost:3000"
echo ""
