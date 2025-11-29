@echo off
REM HR Copilot Setup Script for Windows

echo ========================================
echo HR Copilot AI Agent - Setup Script
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8 or higher from https://www.python.org/
    pause
    exit /b 1
)

echo [1/5] Python detected
python --version
echo.

REM Check if .env file exists
if exist .env (
    echo [2/5] .env file found
) else (
    echo [2/5] Creating .env file from template...
    copy .env.example .env
    echo.
    echo IMPORTANT: Please edit .env file and add your GOOGLE_API_KEY
    echo Get your free API key at: https://aistudio.google.com/app/apikey
    echo.
    pause
)

REM Create virtual environment if it doesn't exist
if exist venv (
    echo [3/5] Virtual environment already exists
) else (
    echo [3/5] Creating virtual environment...
    python -m venv venv
    if errorlevel 1 (
        echo ERROR: Failed to create virtual environment
        pause
        exit /b 1
    )
    echo Virtual environment created successfully
)
echo.

REM Activate virtual environment and install dependencies
echo [4/5] Installing dependencies...
call venv\Scripts\activate.bat
pip install -r requirements.txt
if errorlevel 1 (
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)
echo Dependencies installed successfully
echo.

echo [5/5] Setup complete!
echo.
echo ========================================
echo Next Steps:
echo ========================================
echo 1. Edit .env file and add your GOOGLE_API_KEY
echo 2. Run: run.bat (or manually: streamlit run app.py)
echo ========================================
echo.
pause
