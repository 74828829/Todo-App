#!/bin/bash

# TodoHub - Flask Web Application Startup Script

echo ""
echo "===================================================="
echo "     TODOHUB - MODERN TODO WEB APPLICATION"
echo "===================================================="
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed"
    exit 1
fi

# Check Python version
python3_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "✓ Python $python3_version detected"
echo ""

# Install dependencies
echo "Installing dependencies..."
pip3 install -q -r requirements.txt

if [ $? -ne 0 ]; then
    echo "Error: Failed to install dependencies"
    exit 1
fi

echo "✓ Dependencies installed successfully"
echo ""
echo "Starting Flask development server..."
echo ""
echo "===================================================="
echo "Web app will be available at: http://localhost:5000"
echo "Press Ctrl+C to stop the server"
echo "===================================================="
echo ""

# Run the Flask app
python3 app.py
