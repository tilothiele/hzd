Ein potentielles Mitglied stellt online einen Antrag auf Mitgliedschaft in der OG.

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