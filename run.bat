@echo off
REM HR Copilot Run Script for Windows

echo ========================================
echo HR Copilot AI Agent - Starting...
echo ========================================
echo.

REM Check if virtual environment exists
if not exist venv (
    echo ERROR: Virtual environment not found
    echo Please run setup.bat first
    pause
    exit /b 1
)

REM Check if .env file exists
if not exist .env (
    echo ERROR: .env file not found
    echo Please run setup.bat first and configure your API key
    pause
    exit /b 1
)

REM Activate virtual environment and run Streamlit
call venv\Scripts\activate.bat
echo Starting Streamlit application...
echo.
echo The app will open in your default browser at http://localhost:8501
echo Press Ctrl+C to stop the server
echo.
streamlit run app.py
