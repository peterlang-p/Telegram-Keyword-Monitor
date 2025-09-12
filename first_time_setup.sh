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

# Install dependencies
if command -v pip3 &> /dev/null; then
    pip3 install -r requirements.txt
elif command -v pip &> /dev/null; then
    pip install -r requirements.txt
else
    echo "❌ pip not found! Please install Python pip first."
    exit 1
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