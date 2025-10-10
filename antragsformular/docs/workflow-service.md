# Workflow Service - Dokumentation

## Übersicht

Der `WorkflowService` verwaltet automatisierte Workflows nach der Antragsstellung. Er wird nach erfolgreichem Speichern eines Antrags automatisch aufgerufen.

## Methode: neuesMitglied()

### Funktionalität

Die Methode `neuesMitglied(formData)` wird aufgerufen bei:
- ✅ Erfolgreicher Antragsstellung (`submitApplication`)
- ✅ E-Mail-Verifizierung durch bestehenden Benutzer

### Ablauf

1. **PDF-Generierung**
   - Erstellt automatisch ein PDF des Antragsformulars
   - Verwendet `pdfService.createPdf()`

2. **REST-Endpoint-Aufruf** (optional)
   - Sendet FormData und PDF an externen Endpoint
   - Nur wenn `WORKFLOW_ENDPOINT_URL` konfiguriert ist
   - Unterstützt BASIC Authentication

3. **Logging**
   - Detailliertes Logging aller Schritte
   - Fehler werden protokolliert, aber nicht weitergereicht

## Konfiguration

### Umgebungsvariablen

```env
# Workflow-Endpoint (optional)
WORKFLOW_ENDPOINT_URL="https://api.example.com/new-member"

# BASIC Auth (optional, nur wenn Endpoint geschützt ist)
WORKFLOW_ENDPOINT_USER="username"
WORKFLOW_ENDPOINT_PASSWORD="password"

# SSL-Validierung (optional)
WORKFLOW_IGNORE_SSL="false"  # "true" = Ignoriere SSL-Zertifikatsfehler (nur Dev/Test!)
```

**Ohne Konfiguration:**
- Der Workflow läuft trotzdem
- REST-Endpoint wird übersprungen
- Nur PDF-Generierung erfolgt

## REST-Endpoint Spezifikation

### Request

**Methode:** `POST`

**Content-Type:** `application/json`

**Headers:**
```
Content-Type: application/json
Authorization: Basic {BASE64(username:password)}  // Optional
```

**Body:**

```json
{
  "formData": {
    "email": "user@example.com",
    "vorname": "Max",
    "name": "Mustermann",
    ...
  },
  "pdf": "JVBERi0xLjMKJeLjz9MKM..." // Base64-kodiertes PDF
}
```

**Body-Struktur:**

| Feld | Typ | Beschreibung |
|------|-----|--------------|
| `formData` | Object | Alle Formulardaten als JSON-Objekt |
| `pdf` | String | PDF-Dokument als Base64-String |

### Beispiel Request

```bash
curl -X POST https://api.example.com/new-member \
  -u username:password \
  -H "Content-Type: application/json" \
  -d '{
    "formData": {
      "email": "user@example.com",
      "vorname": "Max",
      "name": "Mustermann"
    },
    "pdf": "JVBERi0xLjMK..."
  }'
```

### FormData Struktur

Das `formData` JSON-Objekt enthält:

```json
{
  "email": "user@example.com",
  "vorname": "Max",
  "name": "Mustermann",
  "geburtsdatum": "1990-01-01",
  "strasse": "Musterstraße 1",
  "plz": "12345",
  "ort": "Musterstadt",
  "telefon": "+49 123 456789",
  "mitgliedschaftVDH": "",
  "hundName": "Bello",
  "hundZwinger": "",
  "hundZuchtbuch": "",
  "hundChip": "123456789012345",
  "hundWurfdatum": "2020-05-15",
  "hundRasse": "Hovawart",
  "hundGeschlecht": "männlich",
  "hundVersicherung": "Versicherung AG",
  "hundVersNr": "12345",
  "mitgliedschaft": "hzd-vollmitglied",
  "kurzzeitVon": "",
  "kurzzeitBis": "",
  "kontoinhaber": "Max Mustermann",
  "sepaName": "Max Mustermann",
  "sepaIban": "DE89370400440532013000",
  "sepaBic": "COBADEFFXXX",
  "sepaKreditinstitut": "Commerzbank",
  "weitereMitteilungen": ""
}
```

### Expected Response

Der Endpoint sollte mit HTTP 200-299 antworten.

**Erfolg (200):**
```json
{
  "success": true,
  "message": "Mitglied erfolgreich verarbeitet"
}
```

**Bei Fehler werden diese geloggt, aber der Workflow läuft weiter.**

## Fehlerbehandlung

### Robustes Fehler-Handling

Der Workflow-Service ist so konzipiert, dass Fehler den Hauptprozess nicht unterbrechen:

1. **PDF-Generierung fehlgeschlagen**
   - Workflow wird abgebrochen
   - Return: `false`

2. **Endpoint-Aufruf fehlgeschlagen**
   - Fehler wird geloggt
   - Workflow läuft weiter
   - Return: `true` (Antrag wurde gespeichert)

3. **Endpoint nicht konfiguriert**
   - Wird übersprungen
   - Nur Logging
   - Return: `true`

### Logging

Alle wichtigen Schritte werden geloggt:

```
Workflow "Neues Mitglied" gestartet für: user@example.com
PDF-Generierung gestartet für: user@example.com
PDF-Generierung erfolgreich abgeschlossen für: user@example.com
Sende Daten an Workflow-Endpoint: https://api.example.com/new-member
BASIC Auth aktiviert für Workflow-Endpoint
Workflow-Endpoint erfolgreich aufgerufen. Response: {...}
Workflow "Neues Mitglied" abgeschlossen für: user@example.com
```

## Integration

### In ApplicationService

```typescript
const workflowService = getWorkflowService();
const workflowResult = await workflowService.neuesMitglied(formData);

if (!workflowResult) {
  return {
    success: false,
    message: 'Fehler beim Verarbeiten der Antragsanmeldung'
  };
}
```

### In VerifyEmailPage

```typescript
const workflowService = getWorkflowService();
await workflowService.neuesMitglied(formData);
```

## Beispiel-Implementierung eines Endpoints

### Express.js Endpoint

```javascript
const express = require('express');

app.post('/new-member', express.json({ limit: '10mb' }), (req, res) => {
  const { formData, pdf } = req.body;
  
  // PDF von Base64 dekodieren
  const pdfBuffer = Buffer.from(pdf, 'base64');
  
  console.log('Neues Mitglied:', formData.email);
  console.log('PDF erhalten:', pdfBuffer.length, 'bytes');
  
  // Optional: PDF in Datei speichern
  // fs.writeFileSync('antrag.pdf', pdfBuffer);
  
  // Verarbeitung...
  
  res.json({ success: true, message: 'Mitglied erfolgreich verarbeitet' });
});
```

### Python Flask Endpoint

```python
from flask import Flask, request, jsonify
import base64

@app.route('/new-member', methods=['POST'])
def new_member():
    data = request.get_json()
    
    # FormData extrahieren
    form_data = data['formData']
    
    # PDF von Base64 dekodieren
    pdf_bytes = base64.b64decode(data['pdf'])
    
    print(f"Neues Mitglied: {form_data['email']}")
    print(f"PDF erhalten: {len(pdf_bytes)} bytes")
    
    # Optional: PDF in Datei speichern
    # with open('antrag.pdf', 'wb') as f:
    #     f.write(pdf_bytes)
    
    # Verarbeitung...
    
    return jsonify(success=True, message='Mitglied erfolgreich verarbeitet')
```

## Erweiterungsmöglichkeiten

Die `neuesMitglied()`-Methode kann erweitert werden um:

- ✅ Datenbank-Einträge in externen Systemen erstellen
- ✅ Benachrichtigungen an Admins senden
- ✅ Dokumente in Cloud-Storage hochladen
- ✅ CRM-Systeme aktualisieren
- ✅ Zahlungssysteme initialisieren
- ✅ Weitere automatisierte Prozesse anstoßen

## Sicherheitshinweise

1. **HTTPS verwenden**: In Produktion immer HTTPS für den Endpoint
2. **BASIC Auth**: Verwenden Sie starke Passwörter
3. **IP-Whitelisting**: Beschränken Sie Zugriff auf bekannte IPs
4. **Rate Limiting**: Implementieren Sie Rate Limiting am Endpoint
5. **Validierung**: Validieren Sie alle Daten am Endpoint
6. **Secrets**: Speichern Sie Credentials sicher (nicht im Code)
7. **SSL-Validierung**: ⚠️ **NIEMALS** `WORKFLOW_IGNORE_SSL=true` in Produktion verwenden!
   - Nur für lokale Entwicklung mit selbstsignierten Zertifikaten
   - Macht Man-in-the-Middle-Angriffe möglich

## Testen

### Lokaler Test ohne Endpoint

Einfach keine `WORKFLOW_ENDPOINT_URL` setzen - der Workflow läuft trotzdem.

### Lokaler Test mit Mock-Endpoint

```bash
# Einfacher HTTP-Server zum Testen
npx http-echo-server --port 8080
```

In `.env`:
```env
WORKFLOW_ENDPOINT_URL="http://localhost:8080/new-member"
```

### Test mit RequestBin

Verwenden Sie [requestbin.com](https://requestbin.com) um Requests zu inspizieren:

```env
WORKFLOW_ENDPOINT_URL="https://your-bin.requestbin.com"
```

