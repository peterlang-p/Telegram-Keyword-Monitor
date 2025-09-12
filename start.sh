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