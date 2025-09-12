#!/usr/bin/env python3
"""
Keyword Manager for Telegram Keyword Monitor
Allows managing keywords via Telegram commands in Saved Messages
"""

import json
import re
from typing import List, Dict, Tuple
from datetime import datetime


class KeywordManager:
    """Manages keywords through Telegram commands."""
    
    def __init__(self, config_path: str = "config.json"):
        self.config_path = config_path
        # Commands that need async (take args parameter)
        self.async_commands = {
            '/keywords': self.list_keywords,
            '/add': self.add_keyword,
            '/remove': self.remove_keyword,
            '/clear': self.clear_keywords,
            '/status': self.show_status,
            '/groups': self.manage_groups,
            '/whitelist': self.manage_whitelist,
            '/blacklist': self.manage_blacklist,
            '/duplicates': self.manage_duplicates,
            '/target': self.manage_notification_target
        }
        
        # Commands that are sync (no args parameter)
        self.sync_commands = {
            '/help': self.show_help
        }
    
    def load_config(self) -> Dict:
        """Load configuration from file."""
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            raise Exception(f"Error loading config: {e}")
    
    def save_config(self, config: Dict) -> None:
        """Save configuration to file."""
        try:
            with open(self.config_path, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=2, ensure_ascii=False)
        except Exception as e:
            raise Exception(f"Error saving config: {e}")
    
    async def process_command(self, message_text: str) -> str:
        """Process a command message and return response."""
        try:
            # Parse command and arguments
            parts = message_text.strip().split()
            if not parts or not parts[0].startswith('/'):
                return self.show_help()
            
            command = parts[0].lower()
            args = parts[1:] if len(parts) > 1 else []
            
            # Execute command
            if command in self.sync_commands:
                # Sync commands (like /help)
                return self.sync_commands[command]()
            elif command in self.async_commands:
                # Async commands (most commands)
                return await self.async_commands[command](args)
            else:
                return f"❌ Unbekannter Befehl: {command}\n\n{self.show_help()}"
                
        except Exception as e:
            return f"❌ Fehler beim Verarbeiten des Befehls: {str(e)}"
    
    async def list_keywords(self, args: List[str]) -> str:
        """List all current keywords."""
        config = self.load_config()
        keywords = config.get('keywords', [])
        
        if not keywords:
            return "📝 Keine Keywords konfiguriert.\n\nVerwenden Sie `/add <keyword>` um Keywords hinzuzufügen."
        
        response = f"📝 **Aktuelle Keywords ({len(keywords)}):**\n\n"
        for i, keyword in enumerate(keywords, 1):
            # Check if it's a regex pattern
            if keyword.startswith('(?i)') or '(' in keyword or '[' in keyword:
                response += f"{i}. `{keyword}` (Regex)\n"
            else:
                response += f"{i}. `{keyword}`\n"
        
        response += f"\n💡 Verwenden Sie `/remove <nummer>` zum Löschen"
        return response
    
    async def add_keyword(self, args: List[str]) -> str:
        """Add a new keyword."""
        if not args:
            return "❌ Bitte geben Sie ein Keyword an.\n\nBeispiel: `/add python`"
        
        keyword = ' '.join(args)
        
        # Validate regex if it looks like one
        if keyword.startswith('(?i)') or '(' in keyword or '[' in keyword:
            try:
                re.compile(keyword)
            except re.error as e:
                return f"❌ Ungültiger Regex-Ausdruck: {e}\n\nBeispiel: `/add (?i)machine learning`"
        
        config = self.load_config()
        keywords = config.get('keywords', [])
        
        if keyword in keywords:
            return f"⚠️ Keyword `{keyword}` existiert bereits."
        
        keywords.append(keyword)
        config['keywords'] = keywords
        self.save_config(config)
        
        return f"✅ Keyword `{keyword}` hinzugefügt.\n\n📝 Aktuelle Anzahl: {len(keywords)}"
    
    async def remove_keyword(self, args: List[str]) -> str:
        """Remove a keyword by number or text."""
        if not args:
            return "❌ Bitte geben Sie eine Nummer oder das Keyword an.\n\nBeispiel: `/remove 1` oder `/remove python`"
        
        config = self.load_config()
        keywords = config.get('keywords', [])
        
        if not keywords:
            return "❌ Keine Keywords zum Entfernen vorhanden."
        
        # Try to parse as number first
        try:
            index = int(args[0]) - 1
            if 0 <= index < len(keywords):
                removed_keyword = keywords.pop(index)
                config['keywords'] = keywords
                self.save_config(config)
                return f"✅ Keyword `{removed_keyword}` entfernt.\n\n📝 Verbleibende Keywords: {len(keywords)}"
            else:
                return f"❌ Ungültige Nummer. Verwenden Sie 1-{len(keywords)}."
        except ValueError:
            # Try to find by text
            keyword_to_remove = ' '.join(args)
            if keyword_to_remove in keywords:
                keywords.remove(keyword_to_remove)
                config['keywords'] = keywords
                self.save_config(config)
                return f"✅ Keyword `{keyword_to_remove}` entfernt.\n\n📝 Verbleibende Keywords: {len(keywords)}"
            else:
                return f"❌ Keyword `{keyword_to_remove}` nicht gefunden."
    
    async def clear_keywords(self, args: List[str]) -> str:
        """Clear all keywords."""
        config = self.load_config()
        keyword_count = len(config.get('keywords', []))
        
        if keyword_count == 0:
            return "❌ Keine Keywords zum Löschen vorhanden."
        
        config['keywords'] = []
        self.save_config(config)
        
        return f"✅ Alle {keyword_count} Keywords gelöscht."
    
    async def show_status(self, args: List[str]) -> str:
        """Show current monitor status."""
        config = self.load_config()
        
        keywords = config.get('keywords', [])
        settings = config.get('settings', {})
        groups = config.get('groups', {})
        
        response = "📊 **Monitor Status:**\n\n"
        response += f"🔍 Keywords: {len(keywords)}\n"
        response += f"📝 Case Sensitive: {'Ja' if settings.get('case_sensitive', False) else 'Nein'}\n"
        response += f"📄 Vollständige Nachrichten: {'Ja' if settings.get('send_full_message', True) else 'Nein'}\n"
        response += f"📏 Max. Nachrichtenlänge: {settings.get('max_message_length', 500)}\n"
        response += f"📷 Medien weiterleiten: {'Ja' if settings.get('forward_media', True) else 'Nein'}\n"
        response += f"📤 Nur Weiterleitung bei Medien: {'Ja' if settings.get('media_only_forward', True) else 'Nein'}\n"
        
        # Notification target
        telegram_config = config.get('telegram', {})
        notification_target = telegram_config.get('notification_target', 'me')
        response += f"📬 Benachrichtigungs-Ziel: {notification_target}\n\n"
        
        whitelist = groups.get('whitelist', [])
        blacklist = groups.get('blacklist', [])
        
        response += f"✅ Whitelist: {len(whitelist)} Gruppen\n"
        response += f"❌ Blacklist: {len(blacklist)} Gruppen\n\n"
        
        # Duplicate detection status
        dup_config = config.get('duplicate_detection', {})
        dup_enabled = dup_config.get('enabled', True)
        dup_hours = dup_config.get('expiry_hours', 24)
        dup_sender = dup_config.get('include_sender', True)
        
        response += f"🔄 Duplikat-Erkennung: {'Aktiviert' if dup_enabled else 'Deaktiviert'}\n"
        if dup_enabled:
            response += f"⏱️ Hash-Gültigkeit: {dup_hours} Stunden\n"
            response += f"👤 Absender berücksichtigen: {'Ja' if dup_sender else 'Nein'}\n"
        
        response += f"\n⏰ Letzte Aktualisierung: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        
        return response
    
    async def manage_groups(self, args: List[str]) -> str:
        """Show group management help."""
        return """📋 **Gruppen-Verwaltung:**

**Whitelist (nur diese Gruppen überwachen):**
• `/whitelist add <gruppenname>` - Gruppe zur Whitelist hinzufügen
• `/whitelist remove <gruppenname>` - Gruppe von Whitelist entfernen
• `/whitelist list` - Whitelist anzeigen
• `/whitelist clear` - Whitelist leeren

**Blacklist (diese Gruppen ausschließen):**
• `/blacklist add <gruppenname>` - Gruppe zur Blacklist hinzufügen
• `/blacklist remove <gruppenname>` - Gruppe von Blacklist entfernen
• `/blacklist list` - Blacklist anzeigen
• `/blacklist clear` - Blacklist leeren

💡 **Hinweis:** Wenn eine Whitelist existiert, werden nur diese Gruppen überwacht."""
    
    async def manage_whitelist(self, args: List[str]) -> str:
        """Manage whitelist."""
        return await self._manage_group_list('whitelist', args)
    
    async def manage_blacklist(self, args: List[str]) -> str:
        """Manage blacklist."""
        return await self._manage_group_list('blacklist', args)
    
    async def _manage_group_list(self, list_type: str, args: List[str]) -> str:
        """Helper method to manage group lists."""
        if not args:
            return f"❌ Bitte geben Sie eine Aktion an: add, remove, list, clear\n\nBeispiel: `/{list_type} list`"
        
        action = args[0].lower()
        config = self.load_config()
        groups = config.get('groups', {})
        group_list = groups.get(list_type, [])
        
        if action == 'list':
            if not group_list:
                return f"📝 {list_type.capitalize()} ist leer."
            
            response = f"📝 **{list_type.capitalize()} ({len(group_list)}):**\n\n"
            for i, group in enumerate(group_list, 1):
                response += f"{i}. `{group}`\n"
            return response
        
        elif action == 'add':
            if len(args) < 2:
                return f"❌ Bitte geben Sie einen Gruppennamen an.\n\nBeispiel: `/{list_type} add Python Developers`"
            
            group_name = ' '.join(args[1:])
            if group_name in group_list:
                return f"⚠️ Gruppe `{group_name}` ist bereits in der {list_type}."
            
            group_list.append(group_name)
            groups[list_type] = group_list
            config['groups'] = groups
            self.save_config(config)
            
            return f"✅ Gruppe `{group_name}` zur {list_type} hinzugefügt.\n\n📝 Anzahl: {len(group_list)}"
        
        elif action == 'remove':
            if len(args) < 2:
                return f"❌ Bitte geben Sie eine Nummer oder Gruppennamen an.\n\nBeispiel: `/{list_type} remove 1`"
            
            # Try number first
            try:
                index = int(args[1]) - 1
                if 0 <= index < len(group_list):
                    removed_group = group_list.pop(index)
                    groups[list_type] = group_list
                    config['groups'] = groups
                    self.save_config(config)
                    return f"✅ Gruppe `{removed_group}` von {list_type} entfernt."
                else:
                    return f"❌ Ungültige Nummer. Verwenden Sie 1-{len(group_list)}."
            except ValueError:
                # Try by name
                group_name = ' '.join(args[1:])
                if group_name in group_list:
                    group_list.remove(group_name)
                    groups[list_type] = group_list
                    config['groups'] = groups
                    self.save_config(config)
                    return f"✅ Gruppe `{group_name}` von {list_type} entfernt."
                else:
                    return f"❌ Gruppe `{group_name}` nicht in {list_type} gefunden."
        
        elif action == 'clear':
            count = len(group_list)
            if count == 0:
                return f"❌ {list_type.capitalize()} ist bereits leer."
            
            groups[list_type] = []
            config['groups'] = groups
            self.save_config(config)
            
            return f"✅ {list_type.capitalize()} geleert ({count} Gruppen entfernt)."
        
        else:
            return f"❌ Unbekannte Aktion: {action}\n\nVerfügbare Aktionen: add, remove, list, clear"
    
    async def manage_duplicates(self, args: List[str]) -> str:
        """Manage duplicate detection settings."""
        if not args:
            config = self.load_config()
            dup_config = config.get('duplicate_detection', {})
            
            enabled = dup_config.get('enabled', True)
            hours = dup_config.get('expiry_hours', 24)
            include_sender = dup_config.get('include_sender', True)
            
            response = "🔄 **Duplikat-Erkennung Einstellungen:**\n\n"
            response += f"Status: {'✅ Aktiviert' if enabled else '❌ Deaktiviert'}\n"
            response += f"Hash-Gültigkeit: {hours} Stunden\n"
            response += f"Absender berücksichtigen: {'Ja' if include_sender else 'Nein'}\n\n"
            response += "**Verfügbare Befehle:**\n"
            response += "• `/duplicates on` - Duplikat-Erkennung aktivieren\n"
            response += "• `/duplicates off` - Duplikat-Erkennung deaktivieren\n"
            response += "• `/duplicates hours <zahl>` - Hash-Gültigkeit setzen\n"
            response += "• `/duplicates sender on/off` - Absender-Berücksichtigung\n"
            
            return response
        
        action = args[0].lower()
        config = self.load_config()
        
        if 'duplicate_detection' not in config:
            config['duplicate_detection'] = {
                'enabled': True,
                'expiry_hours': 24,
                'include_sender': True
            }
        
        dup_config = config['duplicate_detection']
        
        if action == 'on':
            dup_config['enabled'] = True
            config['duplicate_detection'] = dup_config
            self.save_config(config)
            return "✅ Duplikat-Erkennung aktiviert."
        
        elif action == 'off':
            dup_config['enabled'] = False
            config['duplicate_detection'] = dup_config
            self.save_config(config)
            return "❌ Duplikat-Erkennung deaktiviert."
        
        elif action == 'hours':
            if len(args) < 2:
                return "❌ Bitte geben Sie die Anzahl Stunden an.\n\nBeispiel: `/duplicates hours 12`"
            
            try:
                hours = int(args[1])
                if hours < 1 or hours > 168:  # 1 hour to 1 week
                    return "❌ Stunden müssen zwischen 1 und 168 (1 Woche) liegen."
                
                dup_config['expiry_hours'] = hours
                config['duplicate_detection'] = dup_config
                self.save_config(config)
                return f"✅ Hash-Gültigkeit auf {hours} Stunden gesetzt."
                
            except ValueError:
                return "❌ Ungültige Zahl. Beispiel: `/duplicates hours 12`"
        
        elif action == 'sender':
            if len(args) < 2:
                return "❌ Bitte geben Sie on oder off an.\n\nBeispiel: `/duplicates sender off`"
            
            sender_action = args[1].lower()
            if sender_action == 'on':
                dup_config['include_sender'] = True
                config['duplicate_detection'] = dup_config
                self.save_config(config)
                return "✅ Absender wird bei Duplikat-Erkennung berücksichtigt."
            elif sender_action == 'off':
                dup_config['include_sender'] = False
                config['duplicate_detection'] = dup_config
                self.save_config(config)
                return "❌ Absender wird bei Duplikat-Erkennung ignoriert."
            else:
                return "❌ Verwenden Sie 'on' oder 'off'.\n\nBeispiel: `/duplicates sender off`"
        
        elif action == 'debug':
            return await self.debug_duplicates(args[1:])
        
        elif action == 'clear':
            response = "🗑️ **Hash-Speicher leeren:**\n\n"
            response += "Um alle gespeicherten Message-Hashes zu löschen,\n"
            response += "starten Sie den Container neu:\n\n"
            response += "`docker-compose restart telegram-monitor`\n\n"
            response += "⚠️ **Warnung:** Danach werden alle Nachrichten als 'neu' behandelt!"
            return response
        
        else:
            return f"❌ Unbekannte Aktion: {action}\n\nVerfügbare Aktionen: on, off, hours, sender, debug, clear"
    
    async def debug_duplicates(self, args: List[str]) -> str:
        """Debug duplicate detection system."""
        if not args:
            return """🔧 **Duplikat-Debug Befehle:**

• `/duplicates debug status` - Zeige Debug-Informationen
• `/duplicates debug clear` - Lösche alle gespeicherten Hashes
• `/duplicates debug test` - Teste Hash-Generierung

**Beispiel:** `/duplicates debug status`"""
        
        action = args[0].lower()
        
        if action == 'status':
            # Get current duplicate detection state
            from main import TelegramKeywordMonitor
            
            response = "🔧 **Duplikat-Debug Status:**\n\n"
            response += f"**Gespeicherte Hashes:** Wird zur Laufzeit angezeigt\n"
            response += f"**Einstellungen:**\n"
            
            config = self.load_config()
            dup_config = config.get('duplicate_detection', {})
            response += f"- Aktiviert: {'Ja' if dup_config.get('enabled', True) else 'Nein'}\n"
            response += f"- Gültigkeit: {dup_config.get('expiry_hours', 24)} Stunden\n"
            response += f"- Absender berücksichtigen: {'Ja' if dup_config.get('include_sender', True) else 'Nein'}\n\n"
            
            response += "💡 **Hinweis:** Detaillierte Hash-Informationen werden in den Logs angezeigt.\n"
            response += "Verwenden Sie `docker-compose logs -f telegram-monitor` um sie zu sehen."
            
            return response
            
        elif action == 'clear':
            response = "⚠️ **Hash-Speicher leeren:**\n\n"
            response += "Dies würde alle gespeicherten Message-Hashes löschen.\n"
            response += "Danach werden alle Nachrichten als 'neu' behandelt.\n\n"
            response += "💡 **Hinweis:** Diese Funktion ist nur zur Laufzeit verfügbar.\n"
            response += "Starten Sie den Container neu um den Hash-Speicher zu leeren:\n"
            response += "`docker-compose restart telegram-monitor`"
            
            return response
            
        elif action == 'test':
            import hashlib
            import re
            
            test_message = "Dies ist eine Test-Nachricht für Hash-Generierung"
            normalized = re.sub(r'\s+', ' ', test_message.strip().lower())
            hash_result = hashlib.md5(normalized.encode('utf-8')).hexdigest()
            
            response = "🧪 **Hash-Test:**\n\n"
            response += f"**Original:** `{test_message}`\n"
            response += f"**Normalisiert:** `{normalized}`\n"
            response += f"**Hash:** `{hash_result[:16]}...`\n\n"
            response += "💡 Gleiche Nachrichten erzeugen den gleichen Hash."
            
            return response
            
        else:
            return f"❌ Unbekannte Debug-Aktion: {action}\n\nVerfügbare Aktionen: status, clear, test"
    
    async def manage_notification_target(self, args: List[str]) -> str:
        """Manage notification target settings."""
        if not args:
            config = self.load_config()
            current_target = config.get('telegram', {}).get('notification_target', 'me')
            
            response = "📬 **Benachrichtigungs-Ziel Verwaltung:**\n\n"
            response += f"**Aktuelles Ziel:** `{current_target}`\n\n"
            response += "**Verfügbare Befehle:**\n"
            response += "• `/target set me` - Saved Messages verwenden\n"
            response += "• `/target set @channel_name` - Kanal verwenden\n"
            response += "• `/target set -1001234567890` - Chat-ID verwenden\n"
            response += "• `/target test` - Test-Nachricht senden\n"
            response += "• `/target check <ziel>` - Ziel-Berechtigung prüfen\n\n"
            response += "**Hinweise:**\n"
            response += "- Für Kanäle: Erstellen Sie einen Kanal und fügen Sie sich selbst als Admin hinzu\n"
            response += "- Für Gruppen: Verwenden Sie die Chat-ID (negative Zahl)\n"
            response += "- 'me' = Ihre Saved Messages (Standard)\n"
            response += "- Bei Chat-IDs: Stellen Sie sicher, dass Sie Schreibrechte haben\n\n"
            response += "**Troubleshooting:**\n"
            response += "- Kanal-ID funktioniert nicht? Versuchen Sie @username\n"
            response += "- Keine Berechtigung? Prüfen Sie Admin-Rechte im Kanal\n"
            response += "- Immer noch Probleme? Verwenden Sie 'me' als Fallback"
            
            return response
        
        action = args[0].lower()
        
        if action == 'set':
            if len(args) < 2:
                return "❌ Bitte geben Sie ein Ziel an.\n\nBeispiel: `/target set @my_channel`"
            
            new_target = args[1]
            
            # Validate target format
            if new_target not in ['me'] and not (new_target.startswith('@') or new_target.lstrip('-').isdigit()):
                return "❌ Ungültiges Ziel-Format.\n\nVerwenden Sie: 'me', '@channel_name' oder '-1001234567890'"
            
            config = self.load_config()
            if 'telegram' not in config:
                config['telegram'] = {}
            
            config['telegram']['notification_target'] = new_target
            self.save_config(config)
            
            return f"✅ Benachrichtigungs-Ziel auf `{new_target}` gesetzt.\n\nVerwenden Sie `/target test` um es zu testen."
        
        elif action == 'test':
            config = self.load_config()
            target = config.get('telegram', {}).get('notification_target', 'me')
            
            # Try to send a test message to verify the target works
            try:
                # This will be handled by the main app, we just return the test message
                response = f"🧪 **Test-Nachricht für Ziel: `{target}`**\n\n"
                response += "Wenn Sie diese Nachricht erhalten, funktioniert das Benachrichtigungs-Ziel korrekt!\n\n"
                response += f"**Ziel:** {target}\n"
                response += f"**Zeit:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
                response += "💡 **Hinweis:** Wenn Sie diese Nachricht nicht im konfigurierten Ziel sehen,\n"
                response += "überprüfen Sie die Berechtigungen oder verwenden Sie einen anderen Ziel-Typ."
                
                return response
            except Exception as e:
                return f"❌ Fehler beim Testen des Ziels `{target}`: {str(e)}"
        
        elif action == 'check':
            if len(args) < 2:
                return "❌ Bitte geben Sie ein Ziel zum Prüfen an.\n\nBeispiel: `/target check -1002153150590`"
            
            target_to_check = args[1]
            
            response = f"🔍 **Ziel-Prüfung für: `{target_to_check}`**\n\n"
            response += "**Wird geprüft...**\n"
            response += f"- Format: {'Chat-ID' if target_to_check.lstrip('-').isdigit() else 'Username/Text'}\n"
            response += f"- Typ: {'Kanal/Gruppe' if target_to_check.startswith('-') else 'Benutzer/Kanal'}\n\n"
            response += "💡 **Hinweis:** Detaillierte Prüfung wird in den Logs angezeigt.\n"
            response += "Verwenden Sie `docker-compose logs -f telegram-monitor` um Details zu sehen."
            
            return response
        
        else:
            return f"❌ Unbekannte Aktion: {action}\n\nVerfügbare Aktionen: set, test, check"
    
    def show_help(self) -> str:
        """Show help message."""
        return """🤖 **Telegram Keyword Monitor - Befehle:**

**Keywords verwalten:**
• `/keywords` - Alle Keywords anzeigen
• `/add <keyword>` - Keyword hinzufügen
• `/remove <nummer|keyword>` - Keyword entfernen
• `/clear` - Alle Keywords löschen

**Gruppen verwalten:**
• `/groups` - Gruppen-Verwaltung Hilfe
• `/whitelist <action>` - Whitelist verwalten
• `/blacklist <action>` - Blacklist verwalten

**Duplikat-Erkennung:**
• `/duplicates` - Duplikat-Einstellungen anzeigen
• `/duplicates on/off` - Duplikat-Erkennung ein/ausschalten
• `/duplicates hours <zahl>` - Hash-Gültigkeit setzen

**Benachrichtigungen:**
• `/target` - Benachrichtigungs-Ziel verwalten
• `/target set @channel` - Kanal für Benachrichtigungen setzen
• `/target test` - Test-Nachricht senden

**Status & Info:**
• `/status` - Monitor-Status anzeigen
• `/help` - Diese Hilfe anzeigen

**Beispiele:**
• `/add python` - Einfaches Keyword
• `/add (?i)machine learning` - Regex (case-insensitive)
• `/remove 1` - Erstes Keyword entfernen
• `/whitelist add Python Jobs` - Gruppe zur Whitelist

💡 **Hinweis:** Alle Befehle funktionieren nur in Ihren "Saved Messages"."""