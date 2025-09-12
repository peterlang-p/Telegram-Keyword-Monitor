# 🐳 Docker Setup für Telegram Keyword Monitor

## 📋 Voraussetzungen

- Docker installiert
- Docker Compose installiert
- Ihre Telegram API Credentials in `config.json`

## 🚀 Schnellstart

### 1. Container bauen und starten
```bash
docker-compose up -d --build
```

### 2. Logs anzeigen
```bash
docker-compose logs -f telegram-monitor
```

### 3. Container stoppen
```bash
docker-compose down
```

### 4. Container neu starten
```bash
docker-compose restart telegram-monitor
```

## 📁 Verzeichnisstruktur

```
telegram-keyword-monitor/
├── docker-compose.yml     # Docker Compose Konfiguration
├── Dockerfile            # Container-Definition
├── main.py              # Hauptanwendung
├── keyword_manager.py   # Keyword-Verwaltung
├── config.json          # Konfiguration
├── data/                # Session-Dateien (persistent)
└── logs/                # Log-Dateien (persistent)
```

## 🔧 Wichtige Docker-Befehle

### Container-Management
```bash
# Container starten (im Hintergrund)
docker-compose up -d

# Container stoppen
docker-compose down

# Container neu starten
docker-compose restart

# Container Status prüfen
docker-compose ps

# Container komplett neu bauen
docker-compose up -d --build --force-recreate
```

### Logs und Debugging
```bash
# Live-Logs anzeigen
docker-compose logs -f telegram-monitor

# Letzte 50 Log-Zeilen
docker-compose logs --tail=50 telegram-monitor

# In Container einsteigen (für Debugging)
docker-compose exec telegram-monitor /bin/bash

# Container-Informationen
docker-compose exec telegram-monitor python -c "import sys; print(sys.version)"
```

### Daten-Management
```bash
# Session-Dateien löschen (für Neuanmeldung)
rm -rf data/*.session*

# Log-Dateien anzeigen
tail -f logs/keyword_monitor.log

# Konfiguration bearbeiten
nano config.json
# Danach Container neu starten:
docker-compose restart telegram-monitor
```

## 🔄 Erstmalige Einrichtung

### 1. API Credentials eintragen
```bash
# config.json bearbeiten
nano config.json
```

Tragen Sie Ihre `api_id` und `api_hash` ein.

### 2. Container starten
```bash
docker-compose up -d --build
```

### 3. Erste Anmeldung (falls nötig)
```bash
# Logs verfolgen für Anmeldeprozess
docker-compose logs -f telegram-monitor
```

Falls eine Telefonnummer-Eingabe erforderlich ist:
```bash
# In Container einsteigen
docker-compose exec telegram-monitor /bin/bash

# Monitor manuell starten für interaktive Anmeldung
python main.py
```

Nach erfolgreicher Anmeldung wird die Session in `data/` gespeichert.

## 📊 Monitoring

### Health Check
```bash
# Container-Gesundheit prüfen
docker-compose ps
```

Gesunde Container zeigen `healthy` Status.

### Log-Monitoring
```bash
# Kontinuierliche Log-Überwachung
docker-compose logs -f telegram-monitor | grep -E "(ERROR|WARNING|Notification sent)"
```

### Ressourcen-Verbrauch
```bash
# Container-Statistiken
docker stats telegram-keyword-monitor
```

## 🛠️ Troubleshooting

### Container startet nicht
```bash
# Detaillierte Logs anzeigen
docker-compose logs telegram-monitor

# Container-Status prüfen
docker-compose ps

# Konfiguration validieren
docker-compose config
```

### Session-Probleme
```bash
# Session-Dateien löschen und neu starten
rm -rf data/*.session*
docker-compose restart telegram-monitor
```

### Berechtigungsprobleme
```bash
# Verzeichnis-Berechtigungen korrigieren
sudo chown -R $USER:$USER data/ logs/
chmod 755 data/ logs/
```

### Netzwerk-Probleme
```bash
# Container-Netzwerk prüfen
docker network ls
docker-compose exec telegram-monitor ping google.com
```

## 🔧 Erweiterte Konfiguration

### Umgebungsvariablen anpassen
Bearbeiten Sie `docker-compose.yml`:
```yaml
environment:
  - PYTHONUNBUFFERED=1
  - TZ=Europe/Berlin
  - LOG_LEVEL=DEBUG  # Für mehr Details
```

### Ressourcen-Limits setzen
```yaml
services:
  telegram-monitor:
    # ... andere Konfiguration
    deploy:
      resources:
        limits:
          memory: 256M
          cpus: '0.5'
```

### Backup-Strategie
```bash
# Session-Backup erstellen
tar -czf backup-$(date +%Y%m%d).tar.gz data/ logs/ config.json

# Backup wiederherstellen
tar -xzf backup-YYYYMMDD.tar.gz
```

## 🎯 Produktions-Deployment

### 1. Systemd Service (optional)
```bash
# Service-Datei erstellen
sudo nano /etc/systemd/system/telegram-monitor.service
```

```ini
[Unit]
Description=Telegram Keyword Monitor
Requires=docker.service
After=docker.service

[Service]
Type=oneshot
RemainAfterExit=yes
WorkingDirectory=/path/to/telegram-keyword-monitor
ExecStart=/usr/bin/docker-compose up -d
ExecStop=/usr/bin/docker-compose down
TimeoutStartSec=0

[Install]
WantedBy=multi-user.target
```

```bash
# Service aktivieren
sudo systemctl enable telegram-monitor.service
sudo systemctl start telegram-monitor.service
```

### 2. Automatische Updates
```bash
# Update-Script erstellen
cat > update.sh << 'EOF'
#!/bin/bash
cd /path/to/telegram-keyword-monitor
docker-compose pull
docker-compose up -d --build
docker image prune -f
EOF

chmod +x update.sh
```

## 📝 Tipps

- **Session-Dateien** werden in `data/` persistent gespeichert
- **Log-Dateien** finden Sie in `logs/`
- **Konfiguration** kann ohne Container-Neustart geändert werden (außer API-Credentials)
- **Telegram-Befehle** funktionieren normal über "Saved Messages"
- **Container** startet automatisch nach System-Reboot (wenn `restart: unless-stopped`)

## 🎉 Fertig!

Ihr Telegram Keyword Monitor läuft jetzt in Docker und kann einfach verwaltet werden!