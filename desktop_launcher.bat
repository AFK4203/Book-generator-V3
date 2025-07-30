@echo off
title Story Generator Platform
echo ========================================
echo    Advanced Story Generation Platform
echo ========================================
echo.
echo Starting the platform...
echo.

:: Check if Node.js is installed
node --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Node.js is not installed or not in PATH
    echo Please install Node.js from https://nodejs.org/
    pause
    exit /b 1
)

:: Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python from https://python.org/
    pause
    exit /b 1
)

echo Node.js and Python are installed. ✓
echo.

:: Navigate to the project directory (assuming this file is in the root)
cd /d "%~dp0"

echo Starting backend server...
start /min cmd /c "cd backend && python -m pip install -r requirements.txt && python server.py"

timeout /t 3 /nobreak >nul

echo Starting frontend...
start /min cmd /c "cd frontend && yarn install && yarn start"

echo.
echo ========================================
echo Platform is starting up...
echo Backend: http://localhost:8001
echo Frontend: http://localhost:3000
echo ========================================
echo.
echo The Story Generator will open automatically in your browser.
echo You can close this window once the platform is loaded.
echo.

:: Wait a bit longer and then open the browser
timeout /t 10 /nobreak >nul
start http://localhost:3000

pause