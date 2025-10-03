Ein potentielles Mitglied stellt online einen Antrag auf Mitgliedschaft in der OG.

# Onboarding-Prozess

- Der Antragsteller füllt online das Antragsformular aus
- Vor dem Abschicken werden die Angaben validiert. Dies geschieht auf Feldebene im Browser.
- Im Backend geschieht die Validierung gegen die Dolibarr API
- Wenn die Angaben valide sind, gibt das System dem Antragsteller sofort ein PDF aus.
- Parallel wird ein PDF per Mail an die Geschäftsstelle und dem Antragsteller geschickt.
- Im Entwurfsordner des Emailkonto der Geschäftsstelle wird ein Bestätigungs- bzw. Begrüßungsmail gelegt.

## Validierung

### Auf Feldebene im Browser

- Feldvalidierung: PLZ, Email, IBAN, BIC, Telefon, Chipnummer, Von und Bis falls Kurzmitgliedschaft
- Weitere feldbasierte Regeln (min. Zeichen, ... s.u.)

### Businessregeln im Abgleich mit einer lokalen Datenbank und mit dem ERP System

- Eine Antragstellung wird in einer Datenbanktabelle abgespeichert
- Wenn zu einer gegebenen Emailadresse bereits ein Datensatz existiert, wird eine Email an diese Adresse gesendet.
  Gleichzeitig wird ein Datensatz mit den eingegebenen Daten und einer UUID gespeichert.
  Die Mail enthält einen Link, der die o.a. UUID enthält und auf die eingegeben Daten referenziert.
  Klickt der Benutzer diesen Link an, sind die Daten validiert und der Antragstellungsprozess wird gestartet.

## Antragsformular

1. Abschnitt: Antragsteller

- Vorname (mandatory, mindestens 2 Zeichen)
- Nachname (mandatory, mindestens 2 Zeichen)
- Geburtsdatum (mandatory, alter 5-100 Jahre)
- Straße (mandatory)
- plz (mandatory, 5-Stellig dezimal)
- Ort (mandatory)
- Telefon (mandatory, Telefonnummer)
- Emai (mandatory, nach iso validieren)
- VDH Mitgliedschaften

2. Abschnitt: Hund

- Name (mandatory)
- Zwinger
- Zuchtbuchnummer
- Chip-Nr. (Mandatory)
- Wurfdatum (mandatory, 0-20 Jahre)
- Rasse (mandatory)
- Geschlecht (Rüde/Hündin, mandatory)
- Haftpflichtversicherung (mandatory)
- Versicherungsnummer (mandatory)

2. Abschnitt: Mitgliedschaft

Eine der Optionen (mandatory)
- HZD Vollmitgliedschaft (35 euro pro Jahr)
- HZD Familienmitgliedschaft (16 euro pro Jahr - muss in häuslicher Gemeinschaft mit dem OG-Hauptmitglied leben)
- OG Mitglied (138 euro pro Jahr)
- OG Familienmitglied  (16 euro pro Jahr - muss in häuslicher Gemeinschaft mit dem OG-Hauptmitglied leben)
- Kurzzeitmitglied (11,50 euro pro Monat) mit angabe von Monat Bis Monat (mindestens 3 Monate)

3. Abschnitt: SEPA Lastschriftmandat

- Checkbox "Kontoinhaber identisch mit Antragsteller"
  - wenn checked -> feld Kontoinhaber ist disabled und nicht mehr mandatory. Wird mit Vorname Nachame ausgewiesen
  - wenn nicht checked -> Kontoinhaber ist mandatory
- Kontoinhaber (ggf. mandatory)
- Kreditinstitut (mandatory)
- IBAN (mandatory)
- BIC (mandatory)

4. Abschnitt: Abschluss

- Optional: Weitere Mitteilungen


Weiter Button ist deaktiviert, wenn das Formular nicht valide ist.

Wenn der Button geklickt wird, passiert folgendes im Backend:

1. Payload mit Antragsdaten wird gegen eine API gepostet - dort wird sie validiert. Wenn nicht valide, wird die Meldung angezeigt. Ansonsten...
2. Es wird ein Panel mit den Buttons 'PDF laden' und 'schließen' angezeigt