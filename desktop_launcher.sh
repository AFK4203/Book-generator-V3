#!/bin/bash

# Advanced Story Generation Platform Launcher
echo "========================================"
echo "   Advanced Story Generation Platform"
echo "========================================"
echo ""
echo "Starting the platform..."
echo ""

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "ERROR: Node.js is not installed"
    echo "Please install Node.js from https://nodejs.org/"
    exit 1
fi

# Check if Python is installed
if ! command -v python3 &> /dev/null && ! command -v python &> /dev/null; then
    echo "ERROR: Python is not installed"
    echo "Please install Python from https://python.org/"
    exit 1
fi

echo "Node.js and Python are installed. ✓"
echo ""

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
cd "$SCRIPT_DIR"

echo "Starting backend server..."
cd backend
python3 -m pip install -r requirements.txt > /dev/null 2>&1 || python -m pip install -r requirements.txt > /dev/null 2>&1
(python3 server.py || python server.py) &
BACKEND_PID=$!

cd ..
sleep 3

echo "Starting frontend..."
cd frontend
yarn install > /dev/null 2>&1
yarn start &
FRONTEND_PID=$!

cd ..

echo ""
echo "========================================"
echo "Platform is starting up..."
echo "Backend: http://localhost:8001"
echo "Frontend: http://localhost:3000"
echo "========================================"
echo ""
echo "The Story Generator will open automatically in your browser."
echo "Press Ctrl+C to stop the platform."
echo ""

# Wait a bit and then open the browser
sleep 10

# Try to open browser (works on most Linux distros and macOS)
if command -v xdg-open &> /dev/null; then
    xdg-open http://localhost:3000
elif command -v open &> /dev/null; then
    open http://localhost:3000
elif command -v gnome-open &> /dev/null; then
    gnome-open http://localhost:3000
else
    echo "Please open http://localhost:3000 in your browser"
fi

# Wait for user to stop the application
wait