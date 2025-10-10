# Setup-Anleitung

## Lokale Entwicklung

### 1. Abhängigkeiten installieren

```bash
npm install
```

### 2. Umgebungsvariablen konfigurieren

Erstellen Sie eine `.env`-Datei im Projekt-Root:

```env
# Datenbank
DATABASE_URL="file:./data/applications.db"

# Server Base URL (für E-Mail-Links)
NEXT_PUBLIC_BASE_URL="http://localhost:3000"

# SMTP E-Mail-Konfiguration (optional für lokale Tests)
SMTP_HOST="localhost"
SMTP_PORT="1025"
SMTP_SECURE="false"
SMTP_FROM="noreply@hzd-og-hamburg.de"

# Workflow-Endpoint (optional)
WORKFLOW_ENDPOINT_URL=""                    # z.B. "https://api.example.com/new-member"
WORKFLOW_ENDPOINT_USER=""                   # Optional: BASIC Auth Username
WORKFLOW_ENDPOINT_PASSWORD=""               # Optional: BASIC Auth Password
WORKFLOW_IGNORE_SSL="false"                 # "true" = SSL-Fehler ignorieren (nur für Dev/Test!)
```

### 3. Datenbank initialisieren

```bash
# Prisma Client generieren
npx prisma generate

# Datenbank-Schema erstellen
npx prisma db push
```

Das `data`-Verzeichnis wird automatisch beim ersten Start erstellt, wenn es nicht existiert.

### 4. Entwicklungsserver starten

```bash
npm run dev
```

Die Anwendung ist nun unter `http://localhost:3000` erreichbar.

## Datenbank-Management

### Schema-Änderungen anwenden

Nach Änderungen am `prisma/schema.prisma`:

```bash
# Schema in die Datenbank pushen
npx prisma db push

# Prisma Client neu generieren
npx prisma generate
```

### Datenbank zurücksetzen

```bash
# Datenbank-Datei löschen
rm data/applications.db

# Schema neu erstellen
npx prisma db push
```

### Datenbank im Browser betrachten

```bash
npx prisma studio
```

Öffnet ein Web-Interface unter `http://localhost:5555`

## SMTP-Server für lokale Tests

### MailHog (empfohlen)

```bash
# Mit Docker starten
docker run -d -p 1025:1025 -p 8025:8025 mailhog/mailhog

# In .env konfigurieren:
SMTP_HOST="localhost"
SMTP_PORT="1025"
SMTP_SECURE="false"
```

Web-Interface: http://localhost:8025

### smtp4dev (Alternative)

```bash
docker run -d -p 3001:80 -p 25:25 rnwood/smtp4dev
```

Web-Interface: http://localhost:3001

## Docker-Deployment

### Lokal mit Docker bauen

```bash
docker build -t antragsformular .
docker run -p 3000:3000 antragsformular
```

### Mit Docker Compose

```bash
docker-compose up -d
```

## Produktion

### Umgebungsvariablen für Produktion

```env
DATABASE_URL="file:./data/applications.db"
NEXT_PUBLIC_BASE_URL="https://ihre-domain.de"

# SMTP mit echtem E-Mail-Server
SMTP_HOST="smtp.ihr-provider.de"
SMTP_PORT="587"
SMTP_SECURE="false"
SMTP_USER="ihr-benutzername"
SMTP_PASS="ihr-passwort"
SMTP_FROM="noreply@ihre-domain.de"
```

### Build für Produktion

```bash
npm run build
npm start
```

## Fehlerbehebung

### Fehler: "Unable to open the database file"

**Lösung 1:** Stellen Sie sicher, dass das `data`-Verzeichnis existiert:
```bash
mkdir -p data
```

**Lösung 2:** Prisma Client neu generieren und Schema pushen:
```bash
npx prisma generate
npx prisma db push
```

**Lösung 3:** Prüfen Sie Schreibrechte:
```bash
chmod 755 data
```

### Fehler: "PrismaClientInitializationError"

Prisma Client ist nicht generiert:
```bash
npx prisma generate
```

### E-Mails werden nicht gesendet

1. Prüfen Sie SMTP-Konfiguration in `.env`
2. Testen Sie mit MailHog für lokale Entwicklung
3. Prüfen Sie Firewall/Port-Einstellungen
4. Überprüfen Sie Server-Logs

### Port 3000 ist bereits belegt

Port ändern:
```bash
PORT=3001 npm run dev
```

## Verzeichnisstruktur

```
antragsformular/
├── data/                    # SQLite Datenbank (automatisch erstellt)
│   ├── .gitkeep            # Verzeichnis in Git behalten
│   └── applications.db     # SQLite Datenbank (nicht in Git)
├── prisma/
│   └── schema.prisma       # Datenbankschema
├── src/
│   ├── app/                # Next.js App Router
│   ├── lib/                # Hilfs-Funktionen
│   ├── services/           # Business-Logik
│   ├── templates/          # E-Mail-Templates
│   └── types/              # TypeScript-Typen
├── .env                    # Umgebungsvariablen (nicht in Git)
└── package.json
```

## Wichtige Dateien

- `prisma/schema.prisma` - Datenbankschema
- `src/lib/database-prisma.ts` - Datenbank-Service
- `src/services/applicationService.ts` - Antrags-Logik
- `src/services/emailService.ts` - E-Mail-Versand
- `src/templates/` - E-Mail-Templates


