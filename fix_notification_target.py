#!/usr/bin/env python3
"""
Fix notification target by creating a working solution
"""

import asyncio
import json
from telethon import TelegramClient
from telethon.tl.functions.channels import CreateChannelRequest

async def fix_notification_target():
    """Fix notification target by creating a new private channel or using 'me'."""
    print("🔧 Fixing Notification Target for Telegram Keyword Monitor")
    print("=" * 60)
    
    # Load config
    try:
        with open("config.json", 'r', encoding='utf-8') as f:
            config = json.load(f)
    except FileNotFoundError:
        print("❌ config.json not found!")
        return False
    
    # Get current target
    current_target = config.get('telegram', {}).get('notification_target', 'me')
    print(f"📋 Current target: {current_target}")
    
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
        
        # Test current target
        if current_target != 'me':
            print(f"🔍 Testing current target: {current_target}")
            try:
                entity = await client.get_entity(current_target)
                await client.send_message(current_target, "🧪 Test message")
                print("✅ Current target works! No changes needed.")
                return True
            except Exception as e:
                print(f"❌ Current target failed: {e}")
                print("   Creating a new solution...")
        
        print()
        print("🎯 Choose a solution:")
        print("1. Use 'me' (Saved Messages) - Always works")
        print("2. Create a new private channel - Full control")
        print("3. Use an existing channel/group you own")
        
        choice = input("\nEnter your choice (1-3): ").strip()
        
        if choice == "1":
            # Use 'me'
            config['telegram']['notification_target'] = 'me'
            
            with open("config.json", 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=2, ensure_ascii=False)
            
            # Test
            await client.send_message('me', "✅ Notification target set to Saved Messages!")
            
            print("✅ Target set to 'me' (Saved Messages)")
            
        elif choice == "2":
            # Create new channel
            channel_title = input("Enter channel name (or press Enter for 'Keyword Alerts'): ").strip()
            if not channel_title:
                channel_title = "Keyword Alerts"
            
            print(f"📺 Creating channel: {channel_title}")
            
            result = await client(CreateChannelRequest(
                title=channel_title,
                about="Private channel for keyword notifications",
                megagroup=False,
                broadcast=True
            ))
            
            channel = result.chats[0]
            channel_id = f"-100{channel.id}"
            
            # Update config
            config['telegram']['notification_target'] = channel_id
            
            with open("config.json", 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=2, ensure_ascii=False)
            
            # Test
            await client.send_message(channel_id, f"✅ Channel '{channel_title}' ready for notifications!")
            
            print(f"✅ Created channel: {channel_title}")
            print(f"   ID: {channel_id}")
            
        elif choice == "3":
            # Use existing channel
            print("\n📋 Your channels and groups:")
            
            dialogs = await client.get_dialogs()
            channels = []
            
            for i, dialog in enumerate(dialogs[:20]):  # Show first 20
                if hasattr(dialog.entity, 'broadcast') or hasattr(dialog.entity, 'megagroup'):
                    channels.append(dialog)
                    print(f"   {len(channels)}. {dialog.name} (ID: {dialog.id})")
            
            if not channels:
                print("   No channels/groups found. Using 'me' instead.")
                config['telegram']['notification_target'] = 'me'
            else:
                try:
                    selection = int(input(f"\nSelect channel (1-{len(channels)}): ")) - 1
                    if 0 <= selection < len(channels):
                        selected = channels[selection]
                        target_id = str(selected.id)
                        
                        # Test
                        await client.send_message(target_id, "🧪 Testing notification target...")
                        
                        config['telegram']['notification_target'] = target_id
                        print(f"✅ Target set to: {selected.name} ({target_id})")
                    else:
                        print("Invalid selection. Using 'me'.")
                        config['telegram']['notification_target'] = 'me'
                except:
                    print("Invalid input. Using 'me'.")
                    config['telegram']['notification_target'] = 'me'
            
            with open("config.json", 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=2, ensure_ascii=False)
        
        else:
            print("Invalid choice. Using 'me'.")
            config['telegram']['notification_target'] = 'me'
            
            with open("config.json", 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=2, ensure_ascii=False)
        
        print()
        print("✅ Configuration updated!")
        print("🚀 Restart Docker container: docker-compose restart telegram-monitor")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False
        
    finally:
        await client.disconnect()

def main():
    """Main function."""
    success = asyncio.run(fix_notification_target())
    
    if success:
        print("\n🎉 Notification target fixed!")
    else:
        print("\n❌ Failed to fix notification target.")

if __name__ == "__main__":
    main()