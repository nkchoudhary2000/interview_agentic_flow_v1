@echo off
REM Setup script for Django ADK Chatbot

echo ================================================
echo Django ADK Chatbot - Setup Script
echo ================================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8 or higher from https://www.python.org
    pause
    exit /b 1
)

echo [1/6] Creating virtual environment...
python -m venv venv
if errorlevel 1 (
    echo ERROR: Failed to create virtual environment
    pause
    exit /b 1
)

echo [2/6] Activating virtual environment...
call venv\Scripts\activate.bat

echo [3/6] Upgrading pip...
python -m pip install --upgrade pip

echo [4/6] Installing dependencies...
pip install -r requirements.txt
if errorlevel 1 (
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)

echo [5/6] Setting up environment variables...
if not exist .env (
    copy .env.example .env
    echo.
    echo IMPORTANT: Please edit .env file and add your Gemini API key!
    echo.
)

echo [6/6] Running database migrations...
python manage.py makemigrations
python manage.py migrate

echo.
echo ================================================
echo Setup Complete!
echo ================================================
echo.
echo Next steps:
echo 1. Edit .env file and add your GEMINI_API_KEY
echo 2. Run: venv\Scripts\activate
echo 3. Run: python manage.py createsuperuser (optional)
echo 4. Run: python manage.py runserver
echo 5. Open http://localhost:8000 in your browser
echo.
pause
