#!/bin/bash
# First-time setup script for Telegram Keyword Monitor

echo "🚀 Telegram Keyword Monitor - First Time Setup"
echo "=============================================="
echo ""

# Check if config.json exists
if [ ! -f "config.json" ]; then
    echo "📋 Creating config.json from template..."
    if [ -f "config.example.json" ]; then
        cp config.example.json config.json
        echo "✅ config.json created from config.example.json"
        echo ""
        echo "⚠️  IMPORTANT: Please edit config.json and add your Telegram API credentials!"
        echo "   1. Go to https://my.telegram.org"
        echo "   2. Get your api_id and api_hash"
        echo "   3. Edit config.json and replace YOUR_API_ID and YOUR_API_HASH"
        echo ""
        echo "After updating config.json, run this script again."
        exit 1
    else
        echo "❌ config.example.json not found!"
        exit 1
    fi
fi

# Check if credentials are set
if grep -q "YOUR_API_ID" config.json; then
    echo "⚠️  Please update your API credentials in config.json first!"
    echo "   1. Go to https://my.telegram.org"
    echo "   2. Get your api_id and api_hash"
    echo "   3. Edit config.json and replace YOUR_API_ID and YOUR_API_HASH"
    echo ""
    echo "After updating config.json, run this script again."
    exit 1
fi

echo "📦 Installing dependencies..."
echo "This may take a moment..."
echo ""

# Check for pip and try to install if missing
if command -v pip3 &> /dev/null; then
    echo "✅ Found pip3"
    pip3 install -r requirements.txt
elif command -v pip &> /dev/null; then
    echo "✅ Found pip"
    pip install -r requirements.txt
else
    echo "⚠️  pip not found! Attempting to install pip..."
    
    # Try different methods to install pip
    if command -v apt-get &> /dev/null; then
        echo "📦 Installing pip via apt-get..."
        sudo apt-get update && sudo apt-get install -y python3-pip
    elif command -v yum &> /dev/null; then
        echo "📦 Installing pip via yum..."
        sudo yum install -y python3-pip
    elif command -v dnf &> /dev/null; then
        echo "📦 Installing pip via dnf..."
        sudo dnf install -y python3-pip
    elif command -v brew &> /dev/null; then
        echo "📦 Installing pip via brew..."
        brew install python3
    elif command -v pacman &> /dev/null; then
        echo "📦 Installing pip via pacman..."
        sudo pacman -S python-pip
    else
        echo "❌ Could not install pip automatically!"
        echo ""
        echo "🔧 Manual installation required:"
        echo "   Ubuntu/Debian: sudo apt-get install python3-pip"
        echo "   CentOS/RHEL:   sudo yum install python3-pip"
        echo "   Fedora:        sudo dnf install python3-pip"
        echo "   macOS:         brew install python3"
        echo "   Arch Linux:    sudo pacman -S python-pip"
        echo ""
        echo "After installing pip, run this script again."
        exit 1
    fi
    
    # Check if pip installation was successful
    if command -v pip3 &> /dev/null; then
        echo "✅ pip3 installed successfully!"
        pip3 install -r requirements.txt
    elif command -v pip &> /dev/null; then
        echo "✅ pip installed successfully!"
        pip install -r requirements.txt
    else
        echo "❌ pip installation failed!"
        echo "Please install pip manually and run this script again."
        exit 1
    fi
fi

if [ $? -ne 0 ]; then
    echo "❌ Failed to install dependencies!"
    echo "Please run manually: pip3 install -r requirements.txt"
    exit 1
fi

echo "✅ Dependencies installed successfully!"
echo ""

echo "📱 Setting up Telegram session..."
echo "You will be prompted for your phone number and verification code."
echo ""

# Run session setup
python3 setup_session.py

if [ $? -eq 0 ]; then
    echo ""
    echo "🎉 Setup completed successfully!"
    echo ""
    echo "🐳 Starting Docker container..."
    ./start.sh
else
    echo ""
    echo "❌ Setup failed. Please check your configuration and try again."
    exit 1
fi