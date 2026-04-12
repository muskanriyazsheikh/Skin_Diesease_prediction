@echo off
echo ============================================
echo SkinAI - Quick Setup Script
echo ============================================
echo.

echo [1/4] Checking Python installation...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://www.python.org/
    pause
    exit /b 1
)
echo Python found!
echo.

echo [2/4] Checking Node.js installation...
node --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Node.js is not installed or not in PATH
    echo Please install Node.js 16+ from https://nodejs.org/
    pause
    exit /b 1
)
echo Node.js found!
echo.

echo [3/4] Setting up Backend...
cd backend
echo Creating virtual environment...
python -m venv venv
call venv\Scripts\activate
echo Installing Python dependencies...
pip install -r requirements.txt
cd ..
echo Backend setup complete!
echo.

echo [4/4] Setting up Frontend...
cd frontend
echo Installing Node dependencies...
call npm install
cd ..
echo Frontend setup complete!
echo.

echo ============================================
echo Setup Complete!
echo ============================================
echo.
echo Next steps:
echo 1. Train the model (if not already done):
echo    cd model
echo    python train_model.py
echo.
echo 2. Start the backend server:
echo    cd backend
echo    venv\Scripts\activate
echo    python app.py
echo.
echo 3. Start the frontend (in a new terminal):
echo    cd frontend
echo    npm run dev
echo.
echo 4. Open your browser to: http://localhost:3000
echo.
pause
