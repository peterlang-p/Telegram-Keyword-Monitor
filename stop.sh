#!/bin/bash
# Telegram Keyword Monitor - Stop Script

echo "🛑 Stopping Telegram Keyword Monitor..."

# Stop the container
docker-compose down

echo "✅ Telegram Keyword Monitor stopped!"
echo ""
echo "📝 To start again, run: ./start.sh"
echo "📝 To view logs: docker-compose logs telegram-monitor"