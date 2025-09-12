# 🤖 Telegram Keyword Monitor

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://python.org)
[![Docker](https://img.shields.io/badge/Docker-Ready-blue.svg)](https://docker.com)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![GitHub](https://img.shields.io/badge/GitHub-peterlang--p%2FTelegram--Keyword--Monitor-blue.svg)](https://github.com/peterlang-p/Telegram-Keyword-Monitor)

An intelligent Python tool that monitors all your Telegram groups in real-time and sends notifications to your "Saved Messages" when defined keywords are found.

## 🎯 Key Features

- 🔍 **Real-time monitoring** of all Telegram groups you're a member of
- 💬 **Telegram commands** for easy management via chat
- 🚫 **Duplicate detection** prevents multiple notifications for the same message
- 🎛️ **Flexible filtering** with whitelist/blacklist functionality
- 🐳 **Docker support** for easy deployment and management
- 🔒 **Secure** - Read-only access, no automatic replies in groups

## ✨ Features

- ✅ **Monitor all groups/channels** where your account is a member
- ✅ **Flexible keyword definition** (simple strings or regex patterns)
- ✅ **Keyword management via Telegram commands** - no file editing needed
- ✅ **Smart notifications** to Saved Messages with deep links to original messages
- ✅ **Group filtering** with whitelist/blacklist (manageable via Telegram)
- ✅ **Session persistence** - no repeated login required
- ✅ **Comprehensive logging** and error handling
- ✅ **Configurable message formatting** and length limits
- ✅ **Real-time configuration** updates without restart
- ✅ **Duplicate detection** prevents spam from cross-posted messages
- ✅ **Media forwarding** with photos, videos, documents, and other attachments
- ✅ **Custom notification targets** - use channels, groups, or Saved Messages
- ✅ **Debug tools** for troubleshooting and optimization

## 🚀 Quick Start

### Option 1: Docker (Recommended)

1. **Clone the repository:**
   ```bash
   git clone https://github.com/peterlang-p/Telegram-Keyword-Monitor.git
   cd Telegram-Keyword-Monitor
   ```

2. **First-time setup:**
   ```bash
   ./first_time_setup.sh
   ```
   This will:
   - Install Python dependencies automatically
   - Create config.json from template
   - Guide you through API credential setup
   - Create Telegram session interactively
   - Start the Docker container

   **If pip installation fails:**
   ```bash
   ./install_dependencies.sh              # Install pip and dependencies
   ./first_time_setup.sh                  # Then run setup
   ```

   **Manual setup (if needed):**
   ```bash
   pip3 install -r requirements.txt       # Install dependencies
   python3 setup_session.py              # Session setup only
   python3 fix_notification_target.py     # Fix notification issues
   ```

3. **Regular usage:**
   ```bash
   ./start.sh  # Start
   ./stop.sh   # Stop
   ```

### Option 2: Local Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/peterlang-p/Telegram-Keyword-Monitor.git
   cd Telegram-Keyword-Monitor
   ```

2. **Install dependencies:**
   ```bash
   pip3 install -r requirements.txt
   ```

3. **Setup configuration:**
   ```bash
   cp config.example.json config.json
   # Edit config.json with your API credentials from https://my.telegram.org
   ```

4. **Create session:**
   ```bash
   python3 setup_session.py
   ```

5. **Run the monitor:**
   ```bash
   python3 main.py
   ```

### Option 3: Virtual Environment (Advanced)

1. **Clone and setup:**
   ```bash
   git clone https://github.com/peterlang-p/Telegram-Keyword-Monitor.git
   cd Telegram-Keyword-Monitor
   python3 -m venv telegram_monitor_env
   source telegram_monitor_env/bin/activate
   pip install -r requirements.txt
   ```

2. **Configure and run:**
   ```bash
   cp config.example.json config.json
   # Edit config.json with your credentials
   python3 setup_session.py
   python3 main.py
   ```

## 🔑 Getting API Credentials

1. Go to https://my.telegram.org
2. Log in with your phone number
3. Go to "API development tools"
4. Create a new application
5. Note down your `api_id` and `api_hash`
6. Add them to your `config.json` file

## ⚙️ Configuration

### config.json Structure:

```json
{
  "telegram": {
    "api_id": "123456",
    "api_hash": "abcdef123456789",
    "session_name": "telegram_monitor"
  },
  "keywords": [
    "python",
    "telegram", 
    "(?i)machine learning",
    "(?i)AI|artificial intelligence"
  ],
  "settings": {
    "case_sensitive": false,
    "send_full_message": true,
    "max_message_length": 500
  },
  "groups": {
    "whitelist": [],
    "blacklist": ["Spam Group", "-1001234567890"]
  },
  "logging": {
    "enabled": true,
    "log_file": "keyword_monitor.log",
    "log_level": "INFO"
  }
}
```

### Configuration Options:

#### Telegram
- `api_id`: Your Telegram API ID
- `api_hash`: Your Telegram API Hash  
- `session_name`: Session file name (created automatically)

#### Keywords
List of keywords as strings. Supports:
- **Simple strings:** `"python"`, `"telegram"`
- **Regex patterns:** `"(?i)AI|artificial intelligence"` (case-insensitive)
- **Complex regex:** `"\\b(machine learning|ML)\\b"`

#### Settings
- `case_sensitive`: Whether to match case exactly (default: false)
- `send_full_message`: Send complete message or truncate (default: true)
- `max_message_length`: Maximum message length when truncating (default: 500)

#### Group Filters
- `whitelist`: Only monitor these groups (empty = monitor all groups)
  - Can contain group names or chat IDs
- `blacklist`: Exclude these groups from monitoring
  - Can contain group names or chat IDs

#### Logging
- `enabled`: Enable logging (default: true)
- `log_file`: Path to log file (default: "keyword_monitor.log")
- `log_level`: Logging level (DEBUG, INFO, WARNING, ERROR)

#### Duplicate Detection
- `enabled`: Enable duplicate message detection (default: true)
- `expiry_hours`: How long to remember message hashes (default: 24)
- `include_sender`: Include sender in hash calculation (default: true)

## 📱 Usage

### First Time Setup

**Docker users:** Use `./first_time_setup.sh` for guided setup.

**Local installation users:**
1. **Initial run:**
   ```bash
   source telegram_monitor_env/bin/activate
   python3 setup_session.py  # Interactive session setup
   python3 main.py           # Start monitoring
   ```

2. **Regular usage:**
   After initial login, the tool runs automatically without re-authentication.

### Managing Keywords via Telegram

Open your **"Saved Messages"** in Telegram and use these commands:

```
/help              - Show all available commands
/keywords          - List current keywords
/add python        - Add a keyword
/remove 1          - Remove keyword by number
/status            - Show monitor status
```

### Stopping the Monitor

- **Local:** Press `Ctrl+C`
- **Docker:** `./stop.sh` or `docker-compose down`

## 📬 Notifications

When a keyword is found, you'll receive a notification in your configured target with:

- **Media forwarding**: Photos, videos, documents are forwarded directly
- **Text notifications**: Include found keywords, group name, sender, timestamp
- **Deep links**: Direct links to original messages
- **Smart formatting**: Configurable message length and format

### Notification Targets

- **Saved Messages** (`me`): Default, always works
- **Public Channels** (`@channel_name`): Use channel username
- **Private Channels** (`https://t.me/+xxxxx`): Use invite link (auto-join)
- **Chat ID** (`-1001234567890`): Direct chat/channel ID

**Example notification:**
```
🔍 **Keyword Match Found!**

**Keywords:** python, telegram
**Group:** Python Developers
**Sender:** John Doe (@johndoe)
**Time:** 2024-01-15 14:30:25

**Message:**
Looking for help with python telegram bot development...

**Link:** https://t.me/c/1234567890/123
```

## 💬 Telegram Commands

You can manage keywords and settings directly via Telegram without editing configuration files. All commands work in your **"Saved Messages"**.

### 📝 Keyword Management

| Command | Description | Example |
|---------|-------------|---------|
| `/keywords` | List all keywords | `/keywords` |
| `/add <keyword>` | Add a keyword | `/add python` |
| `/remove <number\|keyword>` | Remove keyword | `/remove 1` or `/remove python` |
| `/clear` | Delete all keywords | `/clear` |

### 🏢 Group Management

| Command | Description | Example |
|---------|-------------|---------|
| `/groups` | Show group management help | `/groups` |
| `/whitelist add <group>` | Add group to whitelist | `/whitelist add Python Jobs` |
| `/whitelist list` | Show whitelist | `/whitelist list` |
| `/blacklist add <group>` | Add group to blacklist | `/blacklist add Spam Group` |
| `/blacklist list` | Show blacklist | `/blacklist list` |

### 🔄 Duplicate Detection

| Command | Description | Example |
|---------|-------------|---------|
| `/duplicates` | Show duplicate detection settings | `/duplicates` |
| `/duplicates on/off` | Enable/disable duplicate detection | `/duplicates off` |
| `/duplicates hours <number>` | Set hash expiry time | `/duplicates hours 12` |
| `/duplicates debug status` | Show debug information | `/duplicates debug status` |

### 📬 Notification Target

| Command | Description | Example |
|---------|-------------|---------|
| `/target` | Show current notification target | `/target` |
| `/target set me` | Use Saved Messages | `/target set me` |
| `/target set @channel` | Use public channel | `/target set @my_alerts` |
| `/target set -1001234567890` | Use chat ID | `/target set -1001234567890` |
| `/target set https://t.me/+xxxxx` | Use private channel (invite link) | `/target set https://t.me/+abc123` |
| `/target test` | Send test notification | `/target test` |
| `/target check <target>` | Check target permissions | `/target check @my_channel` |

### ℹ️ Status & Help

| Command | Description |
|---------|-------------|
| `/status` | Show monitor status and statistics |
| `/help` | List all available commands |

### 🎯 Command Examples

**Simple keywords:**
```
/add python
/add telegram
/add job
/add freelancer
```

**Regex patterns (advanced):**
```
/add (?i)machine learning
/add (?i)AI|artificial intelligence
/add (?i)react|vue|angular
/add \bjava\b
```

**Group management:**
```
/whitelist add Python Developers
/blacklist add Spam Group
/whitelist list
/status
```

**Notification targets:**
```
/target set me                           # Use Saved Messages
/target set @my_alerts                   # Use public channel
/target set -1001234567890               # Use chat ID
/target set https://t.me/+abc123         # Use private channel (invite link)
/target test                             # Test current target
```

**Debug and troubleshooting:**
```
/duplicates debug status         # Show duplicate detection info
/target check @my_channel       # Check channel permissions
/status                         # Overall system status
```

### 💡 Benefits of Telegram Control

- ✅ **No file editing** required
- ✅ **Manage from anywhere** (mobile, desktop, web)
- ✅ **Instant confirmation** of changes
- ✅ **Real-time updates** without restart
- ✅ **Easy management** on the go

## 🔄 Production Deployment

### Using systemd (Linux):

1. **Create service file:**
   ```bash
   sudo nano /etc/systemd/system/telegram-monitor.service
   ```

2. **Service configuration:**
   ```ini
   [Unit]
   Description=Telegram Keyword Monitor
   After=network.target

   [Service]
   Type=simple
   User=your-username
   WorkingDirectory=/path/to/telegram-monitor
   ExecStart=/usr/bin/python3 /path/to/telegram-monitor/main.py
   Restart=always
   RestartSec=10

   [Install]
   WantedBy=multi-user.target
   ```

3. **Activate service:**
   ```bash
   sudo systemctl enable telegram-monitor.service
   sudo systemctl start telegram-monitor.service
   ```

### Using Docker:

1. **Create Dockerfile:**
   ```dockerfile
   FROM python:3.11-slim
   WORKDIR /app
   COPY requirements.txt .
   RUN pip install -r requirements.txt
   COPY . .
   CMD ["python", "main.py"]
   ```

2. **Build image and run:**
   ```bash
   docker build -t telegram-monitor .
   docker run -d --name telegram-monitor -v $(pwd)/config.json:/app/config.json telegram-monitor
   ```

## 🔧 Troubleshooting

### Common Issues:

1. **"Invalid API_ID or API_HASH"**
   - Check your credentials in config.json
   - Ensure api_id is a number (without quotes)

2. **"Config file not found"**
   - Make sure config.json is in the same directory as main.py
   - Copy from config.example.json if missing

3. **"No keywords found"**
   - Use `/keywords` in Saved Messages to see current keywords
   - Add keywords with `/add <keyword>`
   - Test regex patterns with an online regex tester

4. **Session problems**
   - Delete .session files and restart
   - Use a new session_name if problems persist

5. **Commands not working**
   - Make sure you send commands in "Saved Messages"
   - Commands must start with `/` (e.g., `/help`)
   - Check logs for error messages

6. **Docker issues**
   - Check container status: `docker-compose ps`
   - View logs: `docker-compose logs telegram-monitor`
   - Restart: `docker-compose restart telegram-monitor`

7. **Notification target issues**
   - Channel not receiving messages: Use `/target check <target>`
   - Permission denied errors: Run `python3 fix_notification_target.py`
   - Private channel access: Use invite link with `/target set https://t.me/+xxxxx`
   - Fallback to Saved Messages: `/target set me`

### Checking Logs:
```bash
# Local installation
tail -f keyword_monitor.log

# Docker
docker-compose logs -f telegram-monitor
```

## 🐳 Docker Commands

```bash
# Start
./start.sh

# Stop  
./stop.sh

# Show logs
docker-compose logs -f telegram-monitor

# Check status
docker-compose ps

# Restart
docker-compose restart telegram-monitor
```

## 📁 Project Structure

```
Telegram-Keyword-Monitor/
├── main.py                 # Main application
├── keyword_manager.py      # Telegram command handlers
├── config.example.json     # Example configuration
├── requirements.txt        # Python dependencies
├── Dockerfile             # Docker container definition
├── docker-compose.yml     # Docker service configuration
├── start.sh               # Start script
├── stop.sh                # Stop script
├── setup_session.py       # Interactive session setup
├── fix_notification_target.py      # Fix notification issues
├── first_time_setup.sh    # Complete guided setup
├── README.md              # This file
├── LICENSE                # MIT license
├── CONTRIBUTING.md         # Contribution guidelines
├── CHANGELOG.md           # Version history
└── data/                  # Session files (created at runtime)
    └── logs/              # Log files (created at runtime)
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guidelines.

## 🔒 Security

- **API Credentials:** Never share your `api_id` and `api_hash`
- **Session Files:** Are encrypted but keep them private
- **Read-only:** The tool only reads messages, never sends to groups
- **Docker:** Runs as non-root user for additional security
- **Data Privacy:** All data stays local, nothing is sent to external services

## 📄 License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.

## ⚠️ Disclaimer

This tool is intended for personal use. Please comply with Telegram's Terms of Service and use responsibly. The authors are not responsible for any misuse of this software.