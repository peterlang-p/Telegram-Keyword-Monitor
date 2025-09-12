#!/usr/bin/env python3
"""
Interactive session setup for Telegram Keyword Monitor
Run this script locally to create the session file before using Docker
"""

import asyncio
import json
import sys
from telethon import TelegramClient

async def setup_session():
    """Setup Telegram session interactively."""
    print("🔧 Telegram Keyword Monitor - Session Setup")
    print("=" * 50)
    
    # Load config
    try:
        with open("config.json", 'r', encoding='utf-8') as f:
            config = json.load(f)
    except FileNotFoundError:
        print("❌ config.json not found!")
        print("Please copy config.example.json to config.json and add your credentials.")
        return False
    
    # Get credentials
    telegram_config = config['telegram']
    api_id = int(telegram_config['api_id'])
    api_hash = telegram_config['api_hash']
    session_name = telegram_config['session_name']
    
    # For local setup, use local session path
    local_session_name = session_name.replace('/app/data/', './data/')
    
    print(f"📱 API ID: {api_id}")
    print(f"🔑 API Hash: {api_hash[:10]}...")
    print(f"💾 Session: {local_session_name}")
    print()
    
    # Create data directory if it doesn't exist
    import os
    os.makedirs('./data', exist_ok=True)
    
    # Create client
    client = TelegramClient(local_session_name, api_id, api_hash)
    
    try:
        print("🔗 Connecting to Telegram...")
        await client.start()
        
        # Get user info
        me = await client.get_me()
        print(f"✅ Successfully logged in!")
        print(f"👤 Name: {me.first_name} {me.last_name or ''}")
        print(f"📱 Username: @{me.username or 'None'}")
        print(f"📞 Phone: {me.phone or 'Hidden'}")
        print()
        
        # Test sending a message to self
        test_message = (
            "🎉 **Telegram Keyword Monitor Setup Complete!**\n\n"
            "Your session has been created successfully. "
            "You can now start the Docker container.\n\n"
            f"Setup completed at: {asyncio.get_event_loop().time()}"
        )
        
        await client.send_message('me', test_message)
        print("✅ Test message sent to your Saved Messages!")
        print()
        
        print("🐳 Next steps:")
        print("1. Start Docker: ./start.sh")
        print("2. Check logs: docker-compose logs -f telegram-monitor")
        print("3. Send commands to your Saved Messages: /help")
        
        return True
        
    except Exception as e:
        print(f"❌ Error during setup: {e}")
        return False
        
    finally:
        await client.disconnect()

def main():
    """Main setup function."""
    print("This script will help you set up your Telegram session for Docker.")
    print("Make sure you have:")
    print("- Updated config.json with your API credentials")
    print("- Access to your phone for verification code")
    print()
    
    response = input("Continue with setup? (y/N): ").lower().strip()
    if response != 'y':
        print("Setup cancelled.")
        return
    
    success = asyncio.run(setup_session())
    
    if success:
        print("\n🎉 Setup completed successfully!")
        print("Your Telegram session is ready for Docker.")
    else:
        print("\n❌ Setup failed. Please check your configuration and try again.")

if __name__ == "__main__":
    main()