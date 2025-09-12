#!/bin/bash
# Telegram Keyword Monitor - Start Script

echo "🐳 Starting Telegram Keyword Monitor with Docker..."

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker first."
    exit 1
fi

# Check if docker-compose is available
if ! command -v docker-compose &> /dev/null; then
    echo "❌ docker-compose not found. Please install docker-compose."
    exit 1
fi

# Create directories if they don't exist
mkdir -p data logs

# Check if session file exists
if [ ! -f "data/telegram_monitor.session" ]; then
    echo "⚠️  No Telegram session found!"
    echo ""
    echo "For first-time setup, you need to create a session file:"
    echo "1. Run: python3 setup_session.py"
    echo "2. Enter your phone number and verification code"
    echo "3. Then run: ./start.sh again"
    echo ""
    echo "This is only needed once. After that, Docker will start automatically."
    exit 1
fi

# Build and start the container
echo "🔨 Building and starting container..."
docker-compose up -d --build

# Wait a moment for startup
sleep 3

# Show status
echo ""
echo "📊 Container Status:"
docker-compose ps

echo ""
echo "📋 Recent Logs:"
docker-compose logs --tail=10 telegram-monitor

echo ""
echo "✅ Telegram Keyword Monitor started!"
echo ""
echo "📝 Useful commands:"
echo "  View logs:     docker-compose logs -f telegram-monitor"
echo "  Stop:          docker-compose down"
echo "  Restart:       docker-compose restart telegram-monitor"
echo "  Status:        docker-compose ps"
echo ""
echo "💬 Send commands to your Telegram 'Saved Messages':"
echo "  /help - Show all commands"
echo "  /status - Show monitor status"
echo "  /keywords - List current keywords"