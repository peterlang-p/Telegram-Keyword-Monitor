#!/usr/bin/env python3
"""
Helper script to create a private notification channel for Telegram Keyword Monitor
"""

import asyncio
import json
from telethon import TelegramClient
from telethon.tl.functions.channels import CreateChannelRequest

async def create_notification_channel():
    """Create a private channel for notifications."""
    print("📺 Creating Notification Channel for Telegram Keyword Monitor")
    print("=" * 60)
    
    # Load config
    try:
        with open("config.json", 'r', encoding='utf-8') as f:
            config = json.load(f)
    except FileNotFoundError:
        print("❌ config.json not found!")
        return False
    
    # Get credentials
    telegram_config = config['telegram']
    api_id = int(telegram_config['api_id'])
    api_hash = telegram_config['api_hash']
    session_name = telegram_config['session_name'].replace('/app/data/', './data/')
    
    # Create client
    client = TelegramClient(session_name, api_id, api_hash)
    
    try:
        await client.start()
        me = await client.get_me()
        
        print(f"✅ Connected as: {me.first_name} (@{me.username or 'None'})")
        print()
        
        # Create private channel
        channel_title = "Keyword Monitor Alerts"
        channel_about = "Private channel for Telegram Keyword Monitor notifications"
        
        print(f"📺 Creating private channel: '{channel_title}'...")
        
        result = await client(CreateChannelRequest(
            title=channel_title,
            about=channel_about,
            megagroup=False,  # Create a channel, not a supergroup
            broadcast=True    # Make it a broadcast channel
        ))
        
        channel = result.chats[0]
        channel_id = channel.id
        
        # Convert to the format used in Telegram
        full_channel_id = f"-100{channel_id}"
        
        print(f"✅ Channel created successfully!")
        print(f"📋 Channel Details:")
        print(f"   Title: {channel_title}")
        print(f"   ID: {full_channel_id}")
        print(f"   Type: Private Channel")
        print()
        
        # Send test message
        test_message = (
            f"🎉 **Keyword Monitor Channel Ready!**\n\n"
            f"This private channel will receive all your keyword notifications.\n\n"
            f"**Channel ID:** `{full_channel_id}`\n"
            f"**Created:** {asyncio.get_event_loop().time()}"
        )
        
        await client.send_message(channel, test_message)
        print("✅ Test message sent to channel!")
        print()
        
        # Update config
        config['telegram']['notification_target'] = full_channel_id
        
        with open("config.json", 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
        
        print("✅ Configuration updated!")
        print(f"   notification_target set to: {full_channel_id}")
        print()
        
        print("🚀 Next steps:")
        print("1. Restart the Docker container: docker-compose restart telegram-monitor")
        print("2. Test with: /target test")
        print("3. All keyword notifications will now go to your private channel!")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False
        
    finally:
        await client.disconnect()

def main():
    """Main function."""
    print("This script will create a private Telegram channel for your keyword notifications.")
    print("The channel will be automatically configured in your config.json.")
    print()
    
    response = input("Create notification channel? (y/N): ").lower().strip()
    if response != 'y':
        print("Cancelled.")
        return
    
    success = asyncio.run(create_notification_channel())
    
    if success:
        print("\n🎉 Notification channel created and configured successfully!")
    else:
        print("\n❌ Failed to create notification channel.")

if __name__ == "__main__":
    main()