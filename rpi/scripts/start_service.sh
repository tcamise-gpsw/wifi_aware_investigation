#!/bin/bash
# Start WiFi Aware service script

echo "Starting WiFi Aware Control Service..."

# Navigate to project directory
cd "$(dirname "$0")/.." || exit 1

# Activate virtual environment
if [ -d "venv" ]; then
    source venv/bin/activate
else
    echo "Virtual environment not found. Please run: python3 -m venv venv"
    exit 1
fi

# Check if running as root
if [ "$EUID" -ne 0 ]; then
    echo "Please run as root (sudo)"
    exit 1
fi

# Start the service
python3 main.py
