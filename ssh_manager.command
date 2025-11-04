#!/bin/bash
# SSH Connection Manager Launcher for macOS
# Double-click this file to run the SSH Manager

# Get the directory where this script is located
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Change to that directory
cd "$DIR"

# Clear screen for better appearance
clear

# Display header
echo "=================================="
echo "  SSH Connection Manager"
echo "=================================="
echo ""

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed!"
    echo ""
    echo "Please install Python 3 from:"
    echo "https://www.python.org/downloads/"
    echo ""
    echo "Or use Homebrew:"
    echo "brew install python3"
    echo ""
    read -p "Press Enter to exit..."
    exit 1
fi

# Check if dependencies are installed
if ! python3 -c "import cryptography" &> /dev/null; then
    echo "📦 Installing dependencies..."
    pip3 install -r requirements.txt
    echo ""
fi

# Run the SSH Manager
python3 ssh_manager.py

# Keep terminal open if there was an error
if [ $? -ne 0 ]; then
    echo ""
    read -p "Press Enter to exit..."
fi
