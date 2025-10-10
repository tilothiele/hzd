# E-Mail-Verifizierung für existierende Anmeldungen

## Übersicht

Wenn ein Benutzer versucht, sich mit einer E-Mail-Adresse anzumelden, die bereits im System existiert, wird automatisch:

1. Das Feld `verificationSentAt` in der Application-Tabelle wird aktualisiert (gültig für 30 Minuten)
2. Eine E-Mail mit einem Bestätigungslink an die E-Mail-Adresse gesendet
3. Der Benutzer erhält eine Meldung, dass eine Anmeldung bereits existiert

## Funktionsweise

### 1. Duplizierte Anmeldung erkannt
Wenn `submitApplication` aufgerufen wird und die E-Mail-Adresse bereits existiert:
- Die **bestehende UUID** der ursprünglichen Anmeldung wird verwendet (keine neue UUID!)
- Das Feld `verificationSentAt` wird auf den aktuellen Zeitstempel gesetzt
- Eine E-Mail mit dem Verifizierungslink wird an die Adresse gesendet

### 2. E-Mail-Versand
Die E-Mail enthält:
- Einen personalisierten Link zur Verifizierung (mit der ursprünglichen UUID)
- Hinweis auf 30-Minuten-Gültigkeit
- Kontaktinformationen

Format: `{BASE_URL}/verify-email?uuid={UUID}&email={EMAIL}`

### 3. Verifizierung
Wenn der Benutzer auf den Link klickt (Page `/verify-email`):
- UUID und E-Mail werden aus den Query-Parametern gelesen
- Application wird anhand der E-Mail gesucht
- UUID wird mit der gespeicherten UUID verglichen
- `verificationSentAt` wird geprüft (darf nicht älter als 30 Minuten sein)
- Bei Erfolg: Anmeldungsdaten werden angezeigt

## Umgebungsvariablen

Folgende Umgebungsvariablen müssen konfiguriert werden:

```bash
# Datenbank
DATABASE_URL="file:./data/applications.db"

# Server Base URL (für E-Mail-Links)
NEXT_PUBLIC_BASE_URL="http://localhost:3000"

# SMTP E-Mail-Konfiguration
SMTP_HOST="localhost"
SMTP_PORT="587"
SMTP_SECURE="false"  # "true" für Port 465
SMTP_USER=""         # Optional: SMTP-Benutzername
SMTP_PASS=""         # Optional: SMTP-Passwort
SMTP_FROM="noreply@hzd-og-hamburg.de"
```

## Datenbankschema

### Application Model (erweitert)

```prisma
model Application {
  id                   Int       @id @default(autoincrement())
  creationDate         DateTime  @default(now())
  email                String    @unique @map("email")
  uuid                 String?   @map("uuid")
  payload              String?   @map("payload")
  verificationSentAt   DateTime? @map("verification_sent_at")

  @@map("applications")
}
```

**Neues Feld:**
- `verificationSentAt`: Zeitstempel, wann die letzte Verifizierungs-E-Mail gesendet wurde
  - Wird verwendet, um die 30-Minuten-Gültigkeit zu prüfen
  - NULL wenn noch nie eine Verifizierungs-E-Mail gesendet wurde

## Endpunkte

### POST /api/submit-application
Wenn eine duplizierte E-Mail erkannt wird:

**Response (409 Conflict):**
```json
{
  "success": false,
  "message": "Eine Anmeldung mit dieser E-Mail-Adresse existiert bereits. Wir haben Ihnen eine E-Mail mit einem Bestätigungslink gesendet."
}
```

### GET /verify-email?uuid={UUID}&email={EMAIL}

**Typ:** Next.js Server Component Page (keine API-Route)

**Query-Parameter:**
- `uuid`: Der Verification Token (UUID der Application)
- `email`: Die E-Mail-Adresse

**Erfolgreiche Response:**
- Zeigt eine HTML-Seite mit den gespeicherten Anmeldungsdaten
- Verwendet Tailwind CSS für das Styling
- Responsive Design

**Fehler-Anzeige:**
Die Seite zeigt eine Fehlermeldung bei:
- Fehlenden Parametern (UUID oder E-Mail)
- Ungültigem Verifizierungslink
- Abgelaufenem Link (älter als 30 Minuten)
- Keiner gefundenen Anmeldung

## Services

### EmailService (`src/services/emailService.ts`)

**Hauptfunktionen:**
- `sendVerificationEmail(email, uuid, baseUrl)`: Sendet Verifizierungs-E-Mail
- `testConnection()`: Testet SMTP-Verbindung

**Verwendung:**
```typescript
import { getEmailService } from '../services/emailService';

const emailService = getEmailService();
await emailService.sendVerificationEmail(
  'user@example.com',
  'uuid-token',
  'https://example.com'
);
```

### DatabaseService - Neue Methoden

```typescript
// Zeitstempel für Verifizierungs-E-Mail setzen
await db.updateVerificationSentAt('user@example.com');

// Application mit UUID und Email suchen (für Verifizierung)
const application = await db.getApplicationByEmail(email);
if (application && application.uuid === uuid) {
  // UUID stimmt überein
  if (application.verificationSentAt) {
    const thirtyMinsAgo = new Date(Date.now() - 30 * 60 * 1000);
    const isExpired = new Date(application.verificationSentAt) < thirtyMinsAgo;
    // Prüfe ob abgelaufen
  }
}
```

## Installation

1. **Pakete installieren:**
```bash
npm install
```

2. **Prisma-Datenbank migrieren:**
```bash
npx prisma generate
npx prisma db push
```

3. **Umgebungsvariablen konfigurieren:**
Erstellen Sie eine `.env`-Datei mit den oben genannten Variablen.

4. **SMTP-Server konfigurieren:**
- Lokaler Test: Verwenden Sie `mailhog` oder `smtp4dev`
- Produktion: Konfigurieren Sie einen echten SMTP-Server

## Testen

### Lokaler SMTP-Test mit MailHog

```bash
# MailHog starten (Docker)
docker run -d -p 1025:1025 -p 8025:8025 mailhog/mailhog

# In .env konfigurieren:
SMTP_HOST="localhost"
SMTP_PORT="1025"
SMTP_SECURE="false"
```

Web-Interface: http://localhost:8025

### Test-Szenario

1. Füllen Sie das Formular aus und senden Sie es ab
2. Versuchen Sie, sich mit derselben E-Mail erneut anzumelden
3. Prüfen Sie den Posteingang (MailHog) auf die Verifizierungs-E-Mail
4. Klicken Sie auf den Link in der E-Mail
5. Bestätigen Sie, dass die Anmeldungsdaten angezeigt werden

## Sicherheitshinweise

- Tokens sind nur 30 Minuten gültig
- Tokens werden nach Verwendung gelöscht
- Abgelaufene Tokens werden automatisch bereinigt
- E-Mail-Adressen werden URL-kodiert
- HTTPS sollte in Produktion verwendet werden

## Vorteile dieser Implementierung

1. **Keine separate Token-Tabelle nötig**: Die bestehende UUID der Application wird wiederverwendet
2. **Einfachere Datenbankstruktur**: Nur ein zusätzliches Feld (`verificationSentAt`) statt ganzer Tabelle
3. **Keine Token-Bereinigung nötig**: Es müssen keine abgelaufenen Tokens gelöscht werden
4. **Bessere Performance**: Weniger Datenbankabfragen und keine JOIN-Operationen
5. **Konsistente Daten**: UUID ist direkt mit der Application verknüpft
6. **Native Next.js Page**: Verwendet Server Components statt API-Route
7. **SEO-freundlich**: Normale HTML-Seite statt JSON-Response
8. **Bessere UX**: Direktes Rendering mit Tailwind CSS

## Fehlerbehebung

### E-Mails werden nicht gesendet

1. Prüfen Sie die SMTP-Konfiguration in `.env`
2. Testen Sie die Verbindung:
```typescript
const emailService = getEmailService();
await emailService.testConnection();
```
3. Prüfen Sie Firewall/Port-Einstellungen
4. Überprüfen Sie die Server-Logs

### Verifizierung schlägt fehl

- Prüfen Sie, ob die Datenbank-Migration durchgeführt wurde (`npx prisma db push`)
- Stellen Sie sicher, dass `npx prisma generate` ausgeführt wurde
- Überprüfen Sie die `DATABASE_URL` in `.env`
- Stellen Sie sicher, dass `verificationSentAt` in der Datenbank existiert

### Links funktionieren nicht

- Stellen Sie sicher, dass `NEXT_PUBLIC_BASE_URL` korrekt gesetzt ist
- In Produktion: Verwenden Sie die vollständige Domain mit HTTPS
- Lokal: Verwenden Sie `http://localhost:3000`

