# 🤖 Telegram Keyword Monitor

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://python.org)
[![Docker](https://img.shields.io/badge/Docker-Ready-blue.svg)](https://docker.com)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

Ein intelligentes Python-Tool, das alle Telegram-Gruppen überwacht, in denen Sie Mitglied sind, und Sie über "Saved Messages" benachrichtigt, wenn definierte Keywords gefunden werden.

## 🎯 Hauptfunktionen

- 🔍 **Echtzeit-Überwachung** aller Telegram-Gruppen
- 💬 **Telegram-Befehle** zur einfachen Verwaltung
- 🚫 **Duplikat-Erkennung** verhindert mehrfache Benachrichtigungen
- 🎛️ **Flexible Filterung** mit Whitelist/Blacklist
- 🐳 **Docker-Support** für einfaches Deployment
- 🔒 **Sicher** - Nur lesender Zugriff, keine automatischen Antworten

## Features

- ✅ Überwachung aller Gruppen/Kanäle, in denen der Account Mitglied ist
- ✅ Flexible Keyword-Definition (einfache Strings oder Regex)
- ✅ **Keyword-Verwaltung direkt über Telegram-Befehle**
- ✅ Benachrichtigung über Saved Messages mit Deep Links
- ✅ Whitelist/Blacklist für Gruppen (auch über Telegram steuerbar)
- ✅ Session-Speicherung (kein wiederholter Login nötig)
- ✅ Umfassendes Logging
- ✅ Konfigurierbare Nachrichtenlänge
- ✅ Echtzeit-Konfiguration ohne Neustart

## 🚀 Schnellstart

### Option 1: Docker (Empfohlen)

1. **Repository klonen:**
   ```bash
   git clone https://github.com/yourusername/telegram-keyword-monitor.git
   cd telegram-keyword-monitor
   ```

2. **Konfiguration erstellen:**
   ```bash
   cp config.example.json config.json
   # Bearbeiten Sie config.json mit Ihren API-Credentials
   ```

3. **Starten:**
   ```bash
   ./start.sh
   ```

### Option 2: Lokale Installation

1. **Repository klonen:**
   ```bash
   git clone https://github.com/yourusername/telegram-keyword-monitor.git
   cd telegram-keyword-monitor
   ```

2. **Virtual Environment erstellen:**
   ```bash
   python3 -m venv telegram_monitor_env
   source telegram_monitor_env/bin/activate
   pip install -r requirements.txt
   ```

3. **Konfiguration:**
   ```bash
   cp config.example.json config.json
   # Bearbeiten Sie config.json mit Ihren Credentials
   ```

4. **Starten:**
   ```bash
   python3 main.py
   ```

## 🔑 API Credentials besorgen

1. Gehen Sie zu https://my.telegram.org
2. Loggen Sie sich mit Ihrer Telefonnummer ein
3. Gehen Sie zu "API development tools"
4. Erstellen Sie eine neue App
5. Notieren Sie sich `api_id` und `api_hash`
6. Tragen Sie diese in `config.json` ein

## Konfiguration

### config.json Struktur:

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

### Konfigurationsoptionen:

#### Telegram
- `api_id`: Ihre Telegram API ID
- `api_hash`: Ihr Telegram API Hash  
- `session_name`: Name der Session-Datei (wird automatisch erstellt)

#### Keywords
Liste von Keywords als Strings. Unterstützt:
- **Einfache Strings:** `"python"`, `"telegram"`
- **Regex-Patterns:** `"(?i)AI|artificial intelligence"` (case-insensitive)
- **Komplexe Regex:** `"\\b(machine learning|ML)\\b"`

#### Einstellungen
- `case_sensitive`: Groß-/Kleinschreibung beachten (Standard: false)
- `send_full_message`: Vollständige Nachricht senden oder kürzen (Standard: true)
- `max_message_length`: Maximale Nachrichtenlänge bei Kürzung (Standard: 500)

#### Gruppen-Filter
- `whitelist`: Nur diese Gruppen überwachen (leer = alle Gruppen)
  - Kann Gruppennamen oder Chat-IDs enthalten
- `blacklist`: Diese Gruppen ausschließen
  - Kann Gruppennamen oder Chat-IDs enthalten

#### Logging
- `enabled`: Logging aktivieren (Standard: true)
- `log_file`: Pfad zur Log-Datei (Standard: "keyword_monitor.log")
- `log_level`: Log-Level (DEBUG, INFO, WARNING, ERROR)

## Verwendung

1. **Erstmalige Ausführung:**
   ```bash
   source telegram_monitor_env/bin/activate
   python main.py
   ```
   Beim ersten Start werden Sie aufgefordert, Ihre Telefonnummer und einen Bestätigungscode einzugeben.

2. **Reguläre Ausführung:**
   Nach dem ersten Login läuft das Tool automatisch, ohne erneute Anmeldung.

3. **Keywords über Telegram verwalten:**
   Öffnen Sie Ihre "Saved Messages" in Telegram und verwenden Sie folgende Befehle:
   
   ```
   /help              - Alle verfügbaren Befehle anzeigen
   /keywords          - Aktuelle Keywords auflisten
   /add python        - Keyword hinzufügen
   /remove 1          - Keyword entfernen (per Nummer)
   /status            - Monitor-Status anzeigen
   ```

4. **Stoppen:**
   Drücken Sie `Ctrl+C` um das Tool zu beenden.

## Benachrichtigungen

Wenn ein Keyword gefunden wird, erhalten Sie eine Nachricht in Ihren "Saved Messages" mit folgenden Informationen:

- Gefundene Keywords
- Gruppenname
- Absender
- Zeitstempel
- Nachrichtentext (vollständig oder gekürzt)
- Deep Link zur Original-Nachricht

**Beispiel-Benachrichtigung:**
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

## Telegram-Befehle

Sie können Keywords und Einstellungen direkt über Telegram verwalten, ohne die Konfigurationsdatei zu bearbeiten. Alle Befehle funktionieren in Ihren **"Saved Messages"**.

### 📝 Keyword-Verwaltung

| Befehl | Beschreibung | Beispiel |
|--------|-------------|----------|
| `/keywords` | Alle Keywords anzeigen | `/keywords` |
| `/add <keyword>` | Keyword hinzufügen | `/add python` |
| `/remove <nummer\|keyword>` | Keyword entfernen | `/remove 1` oder `/remove python` |
| `/clear` | Alle Keywords löschen | `/clear` |

### 🏢 Gruppen-Verwaltung

| Befehl | Beschreibung | Beispiel |
|--------|-------------|----------|
| `/groups` | Gruppen-Hilfe anzeigen | `/groups` |
| `/whitelist add <gruppe>` | Gruppe zur Whitelist | `/whitelist add Python Jobs` |
| `/whitelist list` | Whitelist anzeigen | `/whitelist list` |
| `/blacklist add <gruppe>` | Gruppe zur Blacklist | `/blacklist add Spam Group` |
| `/blacklist list` | Blacklist anzeigen | `/blacklist list` |

### ℹ️ Status & Hilfe

| Befehl | Beschreibung |
|--------|-------------|
| `/status` | Monitor-Status und Statistiken anzeigen |
| `/help` | Alle verfügbaren Befehle auflisten |

### 🎯 Beispiele für Keyword-Befehle

**Einfache Keywords:**
```
/add python
/add telegram
/add job
/add freelancer
```

**Regex-Patterns (erweitert):**
```
/add (?i)machine learning
/add (?i)AI|artificial intelligence
/add (?i)react|vue|angular
/add \bjava\b
```

**Gruppen-Management:**
```
/whitelist add Python Developers
/blacklist add Spam Group
/whitelist list
/status
```

### 💡 Vorteile der Telegram-Steuerung

- ✅ **Keine Datei-Bearbeitung** mehr nötig
- ✅ **Änderungen von überall** (Handy, Desktop, Web)
- ✅ **Sofortige Bestätigung** der Änderungen
- ✅ **Echtzeit-Updates** ohne Neustart des Monitors
- ✅ **Einfache Verwaltung** auch unterwegs

## Dauerhafte Ausführung

### Mit systemd (Linux):

1. **Service-Datei erstellen:**
   ```bash
   sudo nano /etc/systemd/system/telegram-monitor.service
   ```

2. **Service-Konfiguration:**
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

3. **Service aktivieren:**
   ```bash
   sudo systemctl enable telegram-monitor.service
   sudo systemctl start telegram-monitor.service
   ```

### Mit Docker:

1. **Dockerfile erstellen:**
   ```dockerfile
   FROM python:3.11-slim
   WORKDIR /app
   COPY requirements.txt .
   RUN pip install -r requirements.txt
   COPY . .
   CMD ["python", "main.py"]
   ```

2. **Image bauen und starten:**
   ```bash
   docker build -t telegram-monitor .
   docker run -d --name telegram-monitor -v $(pwd)/config.json:/app/config.json telegram-monitor
   ```

## Troubleshooting

### Häufige Probleme:

1. **"Invalid API_ID or API_HASH"**
   - Überprüfen Sie Ihre Credentials in config.json
   - Stellen Sie sicher, dass api_id eine Zahl (ohne Anführungszeichen) ist

2. **"Config file not found"**
   - Stellen Sie sicher, dass config.json im gleichen Verzeichnis wie main.py liegt

3. **"No keywords found"**
   - Verwenden Sie `/keywords` in Saved Messages um aktuelle Keywords zu sehen
   - Fügen Sie Keywords mit `/add <keyword>` hinzu
   - Testen Sie Regex-Patterns mit einem Online-Regex-Tester

4. **Session-Probleme**
   - Löschen Sie die .session-Datei und starten Sie neu
   - Bei wiederholten Problemen: Neuen session_name verwenden

5. **Befehle funktionieren nicht**
   - Stellen Sie sicher, dass Sie die Befehle in "Saved Messages" senden
   - Befehle müssen mit `/` beginnen (z.B. `/help`)
   - Prüfen Sie die Logs für Fehlermeldungen

### Logs überprüfen:
```bash
tail -f keyword_monitor.log
```

## 🐳 Docker Commands

```bash
# Starten
./start.sh

# Stoppen  
./stop.sh

# Logs anzeigen
docker-compose logs -f telegram-monitor

# Status prüfen
docker-compose ps

# Neustart
docker-compose restart telegram-monitor
```

## 📁 Projektstruktur

```
telegram-keyword-monitor/
├── main.py                 # Hauptanwendung
├── keyword_manager.py      # Telegram-Befehle
├── config.example.json     # Beispiel-Konfiguration
├── requirements.txt        # Python-Abhängigkeiten
├── Dockerfile             # Docker-Container
├── docker-compose.yml     # Docker-Service
├── start.sh               # Start-Script
├── stop.sh                # Stop-Script
├── README.md              # Diese Datei
└── data/                  # Session-Dateien (wird erstellt)
    └── logs/              # Log-Dateien (wird erstellt)
```

## 🤝 Contributing

1. Fork das Repository
2. Erstellen Sie einen Feature Branch (`git checkout -b feature/amazing-feature`)
3. Committen Sie Ihre Änderungen (`git commit -m 'Add amazing feature'`)
4. Pushen Sie den Branch (`git push origin feature/amazing-feature`)
5. Öffnen Sie einen Pull Request

## 🔒 Sicherheit

- **API-Credentials:** Teilen Sie niemals Ihre `api_id` und `api_hash`
- **Session-Dateien:** Sind verschlüsselt, aber halten Sie sie privat
- **Nur lesend:** Das Tool sendet keine Nachrichten in Gruppen, nur an sich selbst
- **Docker:** Läuft als Non-Root User für zusätzliche Sicherheit

## 📄 Lizenz

Dieses Projekt steht unter der MIT-Lizenz. Siehe [LICENSE](LICENSE) für Details.

## ⚠️ Disclaimer

Dieses Tool ist für den privaten Gebrauch bestimmt. Beachten Sie die Telegram-Nutzungsbedingungen und verwenden Sie es verantwortungsvoll.