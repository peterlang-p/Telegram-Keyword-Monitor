#!/bin/bash
# Git setup script for Telegram Keyword Monitor

echo "🔧 Setting up Git repository..."

# Initialize git if not already done
if [ ! -d ".git" ]; then
    git init
    echo "✅ Git repository initialized"
else
    echo "✅ Git repository already exists"
fi

# Create initial commit if no commits exist
if [ -z "$(git log --oneline 2>/dev/null)" ]; then
    echo "📝 Creating initial commit..."
    
    # Add all files
    git add .
    
    # Create initial commit
    git commit -m "🎉 Initial commit: Telegram Keyword Monitor v1.0.0

Features:
- 🔍 Real-time keyword monitoring
- 💬 Telegram command interface  
- 🚫 Duplicate detection
- 🎛️ Group filtering
- 🐳 Docker support
- 🔒 Secure session management"
    
    echo "✅ Initial commit created"
else
    echo "✅ Repository already has commits"
fi

echo ""
echo "🚀 Next steps:"
echo "1. Create a repository on GitHub"
echo "2. Add remote: git remote add origin https://github.com/yourusername/telegram-keyword-monitor.git"
echo "3. Push to GitHub: git push -u origin main"
echo ""
echo "📋 Don't forget to:"
echo "- Update the GitHub URL in README.md"
echo "- Add your API credentials to config.json (copy from config.example.json)"
echo "- Test the application before pushing"