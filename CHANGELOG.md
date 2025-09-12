# Changelog

All notable changes to this project will be documented in this file.

## [1.0.0] - 2024-09-12

### Added
- 🎉 Initial release
- 🔍 Real-time keyword monitoring for all Telegram groups
- 💬 Telegram command interface for easy management
- 🚫 Intelligent duplicate detection to prevent spam notifications
- 🎛️ Flexible group filtering with whitelist/blacklist
- 🐳 Complete Docker support with docker-compose
- 🔒 Secure session management
- 📊 Comprehensive logging and monitoring
- 🛠️ Easy setup scripts (start.sh, stop.sh)

### Features
- Keyword management via Telegram commands (`/add`, `/remove`, `/keywords`)
- Group management (`/whitelist`, `/blacklist`)
- Duplicate detection settings (`/duplicates`)
- Status monitoring (`/status`, `/help`)
- Regex pattern support for advanced keyword matching
- Configurable message formatting and length limits
- Health checks and auto-restart capabilities
- Non-root Docker container for security

### Technical
- Python 3.11+ support
- Telethon library for Telegram API
- SQLite session storage
- MD5-based duplicate detection
- Bind mounts for persistent data
- MIT License