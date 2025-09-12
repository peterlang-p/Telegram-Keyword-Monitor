#!/bin/bash
# Dependency installation script for Telegram Keyword Monitor

echo "📦 Telegram Keyword Monitor - Dependency Installation"
echo "====================================================="
echo ""

# Function to install pip on different systems
install_pip() {
    echo "🔧 Installing pip for your system..."
    
    if command -v apt-get &> /dev/null; then
        echo "📦 Detected Ubuntu/Debian - Installing via apt-get..."
        sudo apt-get update
        sudo apt-get install -y python3-pip python3-venv
    elif command -v yum &> /dev/null; then
        echo "📦 Detected CentOS/RHEL - Installing via yum..."
        sudo yum install -y python3-pip
    elif command -v dnf &> /dev/null; then
        echo "📦 Detected Fedora - Installing via dnf..."
        sudo dnf install -y python3-pip
    elif command -v brew &> /dev/null; then
        echo "📦 Detected macOS - Installing via brew..."
        brew install python3
    elif command -v pacman &> /dev/null; then
        echo "📦 Detected Arch Linux - Installing via pacman..."
        sudo pacman -S python-pip
    elif command -v apk &> /dev/null; then
        echo "📦 Detected Alpine Linux - Installing via apk..."
        sudo apk add python3 py3-pip
    else
        echo "❌ Could not detect your package manager!"
        echo ""
        echo "🔧 Please install pip manually:"
        echo "   Ubuntu/Debian: sudo apt-get install python3-pip"
        echo "   CentOS/RHEL:   sudo yum install python3-pip"
        echo "   Fedora:        sudo dnf install python3-pip"
        echo "   macOS:         brew install python3"
        echo "   Arch Linux:    sudo pacman -S python-pip"
        echo "   Alpine:        sudo apk add python3 py3-pip"
        return 1
    fi
    
    return 0
}

# Check for Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 not found!"
    echo "Please install Python 3 first:"
    echo "   https://www.python.org/downloads/"
    exit 1
fi

echo "✅ Python 3 found: $(python3 --version)"

# Check for pip
if command -v pip3 &> /dev/null; then
    echo "✅ pip3 found: $(pip3 --version)"
    PIP_CMD="pip3"
elif command -v pip &> /dev/null; then
    echo "✅ pip found: $(pip --version)"
    PIP_CMD="pip"
else
    echo "⚠️  pip not found!"
    echo ""
    read -p "Install pip automatically? (y/N): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        if install_pip; then
            echo "✅ pip installed successfully!"
            if command -v pip3 &> /dev/null; then
                PIP_CMD="pip3"
            else
                PIP_CMD="pip"
            fi
        else
            echo "❌ Failed to install pip automatically."
            exit 1
        fi
    else
        echo "❌ pip installation cancelled."
        exit 1
    fi
fi

# Install requirements
echo ""
echo "📦 Installing Python dependencies..."
echo "This may take a moment..."

if $PIP_CMD install -r requirements.txt; then
    echo "✅ Dependencies installed successfully!"
    echo ""
    echo "🎉 Setup complete! You can now run:"
    echo "   python3 setup_session.py    # Setup Telegram session"
    echo "   python3 main.py             # Start the monitor"
    echo "   ./first_time_setup.sh       # Complete guided setup"
else
    echo "❌ Failed to install dependencies!"
    echo ""
    echo "🔧 Try manual installation:"
    echo "   $PIP_CMD install telethon aiofiles"
    exit 1
fi