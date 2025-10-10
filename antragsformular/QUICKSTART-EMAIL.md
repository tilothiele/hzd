# Schnellstart: E-Mail-Versand einrichten

## Problem: Keine E-Mails werden versendet

Wenn beim Absenden des Antrags keine vorläufige Bestätigung versendet wird, fehlt wahrscheinlich die SMTP-Konfiguration.

## Lösung: SMTP konfigurieren

### 1. Pakete installieren

```bash
npm install
```

Dies installiert `nodemailer` und alle anderen Abhängigkeiten.

### 2. Umgebungsvariablen einrichten

Erstellen Sie eine `.env`-Datei im Projekt-Root:

```env
# Datenbank
DATABASE_URL="file:./data/applications.db"

# Server Base URL
NEXT_PUBLIC_BASE_URL="http://localhost:3000"

# SMTP E-Mail-Konfiguration
SMTP_HOST="localhost"
SMTP_PORT="1025"
SMTP_SECURE="false"
SMTP_FROM="noreply@hzd-og-hamburg.de"
```

### 3. Lokaler SMTP-Test-Server (MailHog)

Für lokale Entwicklung empfehlen wir MailHog:

```bash
# Mit Docker starten
docker run -d -p 1025:1025 -p 8025:8025 mailhog/mailhog
```

**Vorteile:**
- Fängt alle E-Mails ab (kein echter Versand)
- Web-Interface unter http://localhost:8025
- Keine Authentifizierung nötig

### 4. Server neu starten

```bash
npm run dev
```

### 5. Testen

1. Formular ausfüllen und absenden
2. Öffnen Sie http://localhost:8025
3. Sie sollten die Bestätigungs-E-Mail sehen

## Fehlersuche

### Logs überprüfen

In der Konsole/Terminal sollten Sie folgende Logs sehen:

```
Starte E-Mail-Versand für Bestätigung an: user@example.com
Template-Variablen: { EMAIL: '...', VORNAME: '...', ... }
Templates erfolgreich geladen
Mail-Optionen vorbereitet, sende E-Mail...
SMTP Konfiguration: { host: 'localhost', port: 1025, ... }
E-Mail erfolgreich gesendet, MessageID: <...>
Bestätigungs-E-Mail gesendet an user@example.com
```

### Häufige Fehler

**1. "SMTP_HOST nicht konfiguriert"**
- Lösung: `.env`-Datei erstellen mit SMTP-Konfiguration

**2. "ECONNREFUSED"**
- MailHog läuft nicht
- Lösung: `docker run -d -p 1025:1025 -p 8025:8025 mailhog/mailhog`

**3. "Cannot find module 'nodemailer'"**
- Lösung: `npm install`

**4. "Template ... konnte nicht geladen werden"**
- Templates fehlen im `src/templates/` Verzeichnis
- Lösung: Prüfen Sie, dass folgende Dateien existieren:
  - `src/templates/application-confirmation.html`
  - `src/templates/application-confirmation.txt`

## Produktion: Echter SMTP-Server

Für Produktion verwenden Sie einen echten SMTP-Server:

```env
# Beispiel: Gmail
SMTP_HOST="smtp.gmail.com"
SMTP_PORT="587"
SMTP_SECURE="false"
SMTP_USER="ihre-email@gmail.com"
SMTP_PASS="ihr-app-passwort"
SMTP_FROM="ihre-email@gmail.com"
```

**Hinweis:** Bei Gmail benötigen Sie ein App-Passwort (nicht Ihr normales Passwort).

## Alternative SMTP-Test-Server

### smtp4dev

```bash
docker run -d -p 3001:80 -p 25:25 rnwood/smtp4dev
```

Web-Interface: http://localhost:3001

### Mailtrap

Kostenloser Service für E-Mail-Testing: https://mailtrap.io

## Zusammenfassung

1. ✅ `npm install` ausführen
2. ✅ `.env`-Datei mit SMTP-Konfiguration erstellen
3. ✅ MailHog starten (für lokale Tests)
4. ✅ `npm run dev` ausführen
5. ✅ Formular testen
6. ✅ E-Mail in MailHog überprüfen

Bei weiteren Fragen schauen Sie in die ausführliche Dokumentation: `docs/setup.md`

