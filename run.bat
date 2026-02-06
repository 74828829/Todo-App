@echo off
REM TodoHub - Flask Web Application Startup Script

echo.
echo ====================================================
echo     TODOHUB - MODERN TODO WEB APPLICATION
echo ====================================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Error: Python is not installed or not in PATH
    pause
    exit /b 1
)

REM Check if pip is available
pip --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Error: pip is not available
    pause
    exit /b 1
)

REM Install dependencies if not already installed
echo Checking dependencies...
pip install -q -r requirements.txt

if %errorlevel% neq 0 (
    echo Error: Failed to install dependencies
    pause
    exit /b 1
)

echo.
echo ✓ Dependencies installed successfully
echo.
echo Starting Flask development server...
echo.
echo ====================================================
echo Web app will be available at: http://localhost:5000
echo Press Ctrl+C to stop the server
echo ====================================================
echo.

REM Run the Flask app
python app.py

pause
