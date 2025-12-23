#!/bin/bash
#
# Pool Stroke Trainer - Automated Setup Script
# 
# This script automates the setup process for the Pool Stroke Trainer application.
# It creates a virtual environment, installs dependencies, and prepares the application for running.
#
# Author: Scott Gordon
# Email: scott.aiengineer@outlook.com
# License: MIT

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Print colored message
print_msg() {
    echo -e "${2}${1}${NC}"
}

print_msg "🎱 Pool Stroke Trainer - Setup Script" "$BLUE"
print_msg "========================================" "$BLUE"
echo ""

# Check Python version
print_msg "📋 Checking Python version..." "$YELLOW"
if ! command -v python3 &> /dev/null; then
    print_msg "❌ Python 3 is not installed. Please install Python 3.10 or higher." "$RED"
    exit 1
fi

PYTHON_VERSION=$(python3 --version | cut -d ' ' -f 2 | cut -d '.' -f 1,2)
REQUIRED_VERSION="3.10"

if [ "$(printf '%s\n' "$REQUIRED_VERSION" "$PYTHON_VERSION" | sort -V | head -n1)" != "$REQUIRED_VERSION" ]; then
    print_msg "❌ Python $REQUIRED_VERSION or higher is required. Found: $PYTHON_VERSION" "$RED"
    exit 1
fi

print_msg "✅ Python $PYTHON_VERSION detected" "$GREEN"
echo ""

# Create virtual environment
print_msg "📦 Creating virtual environment..." "$YELLOW"
if [ -d "venv" ]; then
    print_msg "⚠️  Virtual environment already exists. Skipping creation." "$YELLOW"
else
    python3 -m venv venv
    print_msg "✅ Virtual environment created" "$GREEN"
fi
echo ""

# Activate virtual environment
print_msg "🔌 Activating virtual environment..." "$YELLOW"
source venv/bin/activate
print_msg "✅ Virtual environment activated" "$GREEN"
echo ""

# Upgrade pip
print_msg "⬆️  Upgrading pip..." "$YELLOW"
pip install --quiet --upgrade pip
print_msg "✅ Pip upgraded" "$GREEN"
echo ""

# Install dependencies
print_msg "📥 Installing dependencies..." "$YELLOW"
pip install --quiet -r requirements.txt
print_msg "✅ Dependencies installed" "$GREEN"
echo ""

# Verify installations
print_msg "🔍 Verifying installations..." "$YELLOW"
python3 -c "import flask; print(f'✅ Flask {flask.__version__}')"
python3 -c "import cv2; print(f'✅ OpenCV {cv2.__version__}')"
python3 -c "import numpy; print(f'✅ NumPy {numpy.__version__}')"
echo ""

# Create directories if needed
print_msg "📁 Creating directories..." "$YELLOW"
mkdir -p logs
mkdir -p static/css static/js
mkdir -p templates
print_msg "✅ Directories ready" "$GREEN"
echo ""

# Summary
print_msg "========================================" "$GREEN"
print_msg "✨ Setup Complete!" "$GREEN"
print_msg "========================================" "$GREEN"
echo ""
print_msg "📝 Next Steps:" "$BLUE"
echo "  1. Ensure your cue tip has a red marker"
echo "  2. Start the application:"
print_msg "     python app.py" "$YELLOW"
echo "  3. Open your browser to:"
print_msg "     http://localhost:7860" "$YELLOW"
echo ""
print_msg "📚 Documentation:" "$BLUE"
echo "  - Quick Start: QUICKSTART.md"
echo "  - Full Docs:   README.md"
echo "  - API Docs:    API.md"
echo "  - Help:        TROUBLESHOOTING.md"
echo ""
print_msg "🎱 Happy practicing! May your strokes be straight!" "$GREEN"
echo ""

# Optional: Ask if user wants to start the app
read -p "Do you want to start the application now? (y/n) " -n 1 -r
echo ""
if [[ $REPLY =~ ^[Yy]$ ]]; then
    print_msg "🚀 Starting Pool Stroke Trainer..." "$GREEN"
    python app.py
fi
