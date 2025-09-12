# PRD – Telegram Keyword-Monitor für User-Accounts
## 1. Ziel

Ein System, das alle Nachrichten in den Telegram-Gruppen, in denen mein Account Mitglied ist, überwacht und mich benachrichtigt, sobald definierte Keywords vorkommen.
Das Tool nutzt meinen eigenen Telegram-Account (kein Bot-Token nötig), da ich nicht in allen Gruppen Admin bin.

## 2. Hauptfunktionen

### Login als User

- Authentifizierung über Telegram API-ID und API-Hash (von my.telegram.org
).

- Einmalige Session-Speicherung, damit nicht jedes Mal ein Login-Code nötig ist.

### Keyword-Überwachung

- Überwachung von Nachrichten in allen Gruppen/Kanälen, in denen mein Account Mitglied ist.

- Möglichkeit, beliebig viele Keywords (Strings oder Regex) zu definieren.

- Treffer sollen unabhängig von Groß-/Kleinschreibung erkannt werden.

### Benachrichtigung

- Option 1: Selbstnachricht („Saved Messages“) mit Hinweis auf Gruppe, Absender und Nachrichtentext.

- Option 2: Push/E-Mail (optional, nice-to-have).

- Nachricht enthält Link zur Original-Nachricht in Telegram (Deep Link).

### Konfiguration

- Keywords sollen in einer einfachen Datei (z. B. keywords.txt oder JSON/YAML) verwaltet werden können.

- Einstellung, ob ganze Nachricht oder nur Auszug gesendet wird.

- Optional: Stummschalten bestimmter Gruppen (Whitelist/Blacklist).

## 3. Technische Anforderungen

- Framework: Python mit Telethon oder Pyrogram.

- Deployment:

  - Lokale Ausführung (Laptop, Raspberry Pi, Server).

  - Dauerhafter Prozess (z. B. via Docker oder Systemd).

- Datenhaltung:

  - Session-Datei für Telegram-Login.

  - Konfigurationsdatei für Keywords.

  - Logdatei für Treffer (optional).

## 4. Sicherheit

- Keine Weitergabe der Telegram-API-Credentials.

- Session-Datei lokal verschlüsselt speichern.

- Keine unerwünschten Aktionen in Gruppen (nur lesend, keine automatischen Antworten).

## 5. Nice-to-have Features

- Web-Dashboard für Verwaltung der Keywords.

- Mehrstufige Benachrichtigungen (z. B. „wichtige Keywords = sofort Push“, „normale Keywords = Tagesübersicht“).

- Export-Report mit allen Treffern (CSV/Excel).

## 6. Erfolgskriterien

- System erkennt zuverlässig Keywords in Echtzeit (<10s Verzögerung).

- System benachrichtigt mich verlässlich bei Treffern.

- Konfiguration ist einfach (Datei ändern, Neustart genügt).