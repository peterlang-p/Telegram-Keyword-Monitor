#!/usr/bin/env python3
"""
Telegram Keyword Monitor
Monitors all Telegram groups for specified keywords and sends notifications to Saved Messages.
"""

import asyncio
import json
import logging
import re
import sys
import hashlib
from datetime import datetime, timedelta
from typing import List, Dict

from telethon import TelegramClient, events
from telethon.tl.types import MessageService, PeerUser

from keyword_manager import KeywordManager


class TelegramKeywordMonitor:
    def __init__(self, config_path: str = "config.json"):
        """Initialize the Telegram Keyword Monitor."""
        self.config_path = config_path
        self.config = self.load_config()
        self.client = None
        self.keyword_manager = KeywordManager(config_path)
        self.setup_logging()
        
        # Duplicate detection
        self.message_hashes: Dict[str, datetime] = {}
        self.cleanup_interval = 3600  # Clean up old hashes every hour
        
        # Load duplicate detection settings
        dup_config = self.config.get('duplicate_detection', {})
        self.duplicate_detection_enabled = dup_config.get('enabled', True)
        self.hash_expiry_hours = dup_config.get('expiry_hours', 24)
        self.include_sender_in_hash = dup_config.get('include_sender', True)
        
    def load_config(self) -> Dict:
        """Load configuration from JSON file."""
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
            
            # Validate required fields
            required_fields = ['telegram', 'keywords']
            for field in required_fields:
                if field not in config:
                    raise ValueError(f"Missing required field in config: {field}")
            
            return config
        except FileNotFoundError:
            logging.error(f"Config file {self.config_path} not found!")
            sys.exit(1)
        except json.JSONDecodeError as e:
            logging.error(f"Invalid JSON in config file: {e}")
            sys.exit(1)
        except Exception as e:
            logging.error(f"Error loading config: {e}")
            sys.exit(1)
    
    def setup_logging(self):
        """Setup logging configuration."""
        log_config = self.config.get('logging', {})
        if not log_config.get('enabled', True):
            return
        
        log_level = getattr(logging, log_config.get('log_level', 'INFO'))
        log_file = log_config.get('log_file', 'keyword_monitor.log')
        
        logging.basicConfig(
            level=log_level,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file, encoding='utf-8'),
                logging.StreamHandler(sys.stdout)
            ]
        )
        
        logging.info("Telegram Keyword Monitor started")
    
    async def initialize_client(self):
        """Initialize and connect the Telegram client."""
        telegram_config = self.config['telegram']
        
        try:
            api_id = int(telegram_config['api_id'])
            api_hash = telegram_config['api_hash']
            session_name = telegram_config['session_name']
            
            if api_id == "YOUR_API_ID" or api_hash == "YOUR_API_HASH":
                logging.error("Please update your API_ID and API_HASH in config.json")
                sys.exit(1)
            
        except (ValueError, KeyError) as e:
            logging.error(f"Invalid Telegram configuration: {e}")
            sys.exit(1)
        
        self.client = TelegramClient(session_name, api_id, api_hash)
        
        try:
            await self.client.start()
            me = await self.client.get_me()
            logging.info(f"Successfully logged in as {me.first_name} (@{me.username})")
            
        except Exception as e:
            logging.error(f"Failed to connect to Telegram: {e}")
            sys.exit(1)
    
    def check_group_filters(self, chat_id: int, chat_title: str) -> bool:
        """Check if the group should be monitored based on whitelist/blacklist."""
        groups_config = self.config.get('groups', {})
        whitelist = groups_config.get('whitelist', [])
        blacklist = groups_config.get('blacklist', [])
        
        # If whitelist is specified, only monitor whitelisted groups
        if whitelist:
            return any(
                str(chat_id) in whitelist or 
                chat_title.lower() in [w.lower() for w in whitelist]
                for w in whitelist
            )
        
        # If blacklist is specified, exclude blacklisted groups
        if blacklist:
            return not any(
                str(chat_id) in blacklist or 
                chat_title.lower() in [b.lower() for b in blacklist]
                for b in blacklist
            )
        
        # If no filters, monitor all groups
        return True
    
    def check_keywords(self, message_text: str) -> List[str]:
        """Check if message contains any keywords."""
        if not message_text:
            return []
        
        keywords = self.config.get('keywords', [])
        case_sensitive = self.config.get('settings', {}).get('case_sensitive', False)
        found_keywords = []
        
        for keyword in keywords:
            try:
                # Check if keyword is a regex pattern
                if keyword.startswith('(?i)') or '(' in keyword or '[' in keyword:
                    # Treat as regex
                    flags = 0 if case_sensitive else re.IGNORECASE
                    if re.search(keyword, message_text, flags):
                        found_keywords.append(keyword)
                else:
                    # Treat as simple string
                    text_to_search = message_text if case_sensitive else message_text.lower()
                    keyword_to_search = keyword if case_sensitive else keyword.lower()
                    
                    if keyword_to_search in text_to_search:
                        found_keywords.append(keyword)
                        
            except re.error as e:
                logging.warning(f"Invalid regex pattern '{keyword}': {e}")
                continue
        
        return found_keywords
    
    async def get_chat_info(self, event) -> tuple:
        """Get chat information from event."""
        try:
            chat = await event.get_chat()
            
            if hasattr(chat, 'title'):
                chat_title = chat.title
            elif hasattr(chat, 'first_name'):
                chat_title = f"{chat.first_name} {getattr(chat, 'last_name', '')}".strip()
            else:
                chat_title = "Unknown Chat"
            
            chat_id = event.chat_id
            return chat_id, chat_title
            
        except Exception as e:
            logging.error(f"Error getting chat info: {e}")
            return event.chat_id, "Unknown Chat"
    
    async def get_sender_info(self, event) -> str:
        """Get sender information from event."""
        try:
            sender = await event.get_sender()
            
            if hasattr(sender, 'first_name'):
                sender_name = f"{sender.first_name} {getattr(sender, 'last_name', '')}".strip()
                if hasattr(sender, 'username') and sender.username:
                    sender_name += f" (@{sender.username})"
            else:
                sender_name = "Unknown Sender"
            
            return sender_name
            
        except Exception as e:
            logging.error(f"Error getting sender info: {e}")
            return "Unknown Sender"
    
    def format_message(self, message_text: str) -> str:
        """Format message text according to settings."""
        settings = self.config.get('settings', {})
        send_full = settings.get('send_full_message', True)
        max_length = settings.get('max_message_length', 500)
        
        if not send_full and len(message_text) > max_length:
            return message_text[:max_length] + "..."
        
        return message_text
    
    async def send_notification(self, chat_title: str, sender_name: str, 
                              message_text: str, keywords: List[str], 
                              chat_id: int, message_id: int, original_message=None):
        """Send notification to Saved Messages with media support."""
        try:
            # Create message link
            if chat_id < 0:  # Group/Channel
                if str(chat_id).startswith('-100'):
                    chat_id_str = str(chat_id)[4:]  # Remove -100 prefix for supergroups
                else:
                    chat_id_str = str(abs(chat_id))  # Regular groups
                message_link = f"https://t.me/c/{chat_id_str}/{message_id}"
            else:  # Private chat
                message_link = f"https://t.me/c/{chat_id}/{message_id}"
            
            # Format notification
            formatted_message = self.format_message(message_text)
            keywords_str = ", ".join(keywords)
            
            # Check if message has media
            has_media = original_message and (
                original_message.photo or 
                original_message.video or 
                original_message.document or 
                original_message.sticker or
                original_message.voice or
                original_message.video_note or
                original_message.audio
            )
            
            media_info = ""
            if has_media:
                media_types = []
                if original_message.photo:
                    media_types.append("📷 Photo")
                if original_message.video:
                    media_types.append("🎥 Video")
                if original_message.document:
                    media_types.append("📄 Document")
                if original_message.sticker:
                    media_types.append("🎭 Sticker")
                if original_message.voice:
                    media_types.append("🎤 Voice")
                if original_message.video_note:
                    media_types.append("📹 Video Note")
                if original_message.audio:
                    media_types.append("🎵 Audio")
                
                media_info = f"**Media:** {', '.join(media_types)}\n"
            
            notification = (
                f"🔍 **Keyword Match Found!**\n\n"
                f"**Keywords:** {keywords_str}\n"
                f"**Group:** {chat_title}\n"
                f"**Sender:** {sender_name}\n"
                f"**Time:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
                f"{media_info}"
                f"\n**Message:**\n{formatted_message}\n\n"
                f"**Link:** {message_link}"
            )
            
            # Get own user ID for Saved Messages
            me = await self.client.get_me()
            
            # Send notification with media if available
            try:
                if has_media:
                    # Forward the original message first (with media)
                    await self.client.forward_messages('me', original_message)
                    
                    # Then send the notification text
                    await self.client.send_message('me', notification)
                    
                    logging.info(f"✅ Notification with media sent for keywords: {keywords_str} in {chat_title}")
                else:
                    # Send text-only notification
                    await self.client.send_message('me', notification)
                    logging.info(f"✅ Text notification sent for keywords: {keywords_str} in {chat_title}")
                    
            except Exception as e1:
                logging.warning(f"Failed to send via 'me': {e1}")
                try:
                    # Fallback: Send to own user ID
                    if has_media:
                        await self.client.forward_messages(me.id, original_message)
                        await self.client.send_message(me.id, notification)
                    else:
                        await self.client.send_message(me.id, notification)
                    logging.info(f"✅ Notification sent via user ID for keywords: {keywords_str} in {chat_title}")
                except Exception as e2:
                    logging.warning(f"Failed to send via user ID: {e2}")
                    try:
                        # Final fallback: Send text-only to PeerUser
                        await self.client.send_message(PeerUser(me.id), notification)
                        logging.info(f"✅ Text-only notification sent via PeerUser for keywords: {keywords_str} in {chat_title}")
                    except Exception as e3:
                        logging.error(f"❌ All notification methods failed: {e1}, {e2}, {e3}")
                        # Fallback: Log the notification
                        logging.info(f"NOTIFICATION: {notification}")
                        raise e3
            
        except Exception as e:
            logging.error(f"Error in send_notification: {e}")
            # Log the notification content for debugging
            logging.info(f"Failed notification content: Keywords: {keywords}, Group: {chat_title}, Sender: {sender_name}")
    
    def generate_message_hash(self, message_text: str, sender_id: int = None) -> str:
        """Generate a hash for message deduplication."""
        # Normalize message text for better duplicate detection
        normalized_text = re.sub(r'\s+', ' ', message_text.strip().lower())
        
        # Create hash from normalized text and optionally sender
        hash_input = normalized_text
        if self.include_sender_in_hash and sender_id:
            hash_input += f"_sender_{sender_id}"
        
        return hashlib.md5(hash_input.encode('utf-8')).hexdigest()
    
    def is_duplicate_message(self, message_hash: str) -> bool:
        """Check if message is a duplicate and update tracking."""
        current_time = datetime.now()
        
        # Clean up old hashes periodically
        if len(self.message_hashes) > 1000:  # Prevent memory buildup
            self.cleanup_old_hashes()
        
        # Check if hash exists and is still valid
        if message_hash in self.message_hashes:
            hash_time = self.message_hashes[message_hash]
            if current_time - hash_time < timedelta(hours=self.hash_expiry_hours):
                return True  # Duplicate found
            else:
                # Hash expired, remove it
                del self.message_hashes[message_hash]
        
        # Add new hash
        self.message_hashes[message_hash] = current_time
        return False  # Not a duplicate
    
    def cleanup_old_hashes(self):
        """Remove expired message hashes."""
        current_time = datetime.now()
        expired_hashes = []
        
        for message_hash, timestamp in self.message_hashes.items():
            if current_time - timestamp > timedelta(hours=self.hash_expiry_hours):
                expired_hashes.append(message_hash)
        
        for hash_to_remove in expired_hashes:
            del self.message_hashes[hash_to_remove]
        
        if expired_hashes:
            logging.info(f"Cleaned up {len(expired_hashes)} expired message hashes")
    
    async def message_handler(self, event):
        """Handle incoming messages."""
        try:
            # Skip service messages
            if isinstance(event.message, MessageService):
                return
            
            # Get message text
            message_text = event.message.message
            if not message_text:
                return
            
            # Get chat and sender info
            chat_id, chat_title = await self.get_chat_info(event)
            
            # Check if this is a command in Saved Messages (self-chat)
            me = await self.client.get_me()
            if chat_id == me.id:
                await self.handle_command(event, message_text)
                return
            
            # Check group filters
            if not self.check_group_filters(chat_id, chat_title):
                return
            
            # Check for keywords
            found_keywords = self.check_keywords(message_text)
            if not found_keywords:
                return
            
            # Check for duplicates (if enabled)
            if self.duplicate_detection_enabled:
                sender_id = event.sender_id if hasattr(event, 'sender_id') else None
                message_hash = self.generate_message_hash(message_text, sender_id)
                
                if self.is_duplicate_message(message_hash):
                    logging.info(f"Duplicate message detected in {chat_title}, skipping notification")
                    return
            
            # Get sender info
            sender_name = await self.get_sender_info(event)
            
            # Send notification with original message for media support
            await self.send_notification(
                chat_title=chat_title,
                sender_name=sender_name,
                message_text=message_text,
                keywords=found_keywords,
                chat_id=chat_id,
                message_id=event.message.id,
                original_message=event.message
            )
            
        except Exception as e:
            logging.error(f"Error in message handler: {e}")
    
    async def handle_command(self, event, message_text: str):
        """Handle commands sent to Saved Messages."""
        try:
            if not message_text.startswith('/'):
                return
            
            logging.info(f"Processing command: {message_text}")
            
            # Process command
            response = await self.keyword_manager.process_command(message_text)
            
            # Reload config after potential changes
            self.config = self.load_config()
            
            # Send response
            await self.client.send_message('me', response)
            
            logging.info(f"Command processed successfully")
            
        except Exception as e:
            logging.error(f"Error handling command: {e}")
            await self.client.send_message('me', f"❌ Fehler beim Verarbeiten des Befehls: {str(e)}")
    
    async def run(self):
        """Run the keyword monitor."""
        await self.initialize_client()
        
        # Register event handler for new messages
        @self.client.on(events.NewMessage)
        async def handle_new_message(event):
            await self.message_handler(event)
        
        logging.info("Keyword monitor is running... Press Ctrl+C to stop.")
        
        try:
            await self.client.run_until_disconnected()
        except KeyboardInterrupt:
            logging.info("Keyword monitor stopped by user")
        except Exception as e:
            logging.error(f"Unexpected error: {e}")
        finally:
            await self.client.disconnect()


async def main():
    """Main entry point."""
    monitor = TelegramKeywordMonitor()
    await monitor.run()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nStopped by user")
    except Exception as e:
        logging.error(f"Fatal error: {e}")
        sys.exit(1)