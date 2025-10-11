// Test-Daten für das HZD-Antragsformular
// Diese Datei enthält verschiedene Test-Szenarien für die Entwicklung und das Testen

import { FormData } from './src/types/formData';

// Standard Test-Daten (Vollmitglied)
export const testFormData: FormData = {
  anrede: "Herr",
  name: "Mustermann",
  vorname: "Max",
  geburtsdatum: "1985-06-15",
  strasse: "Musterstraße 123",
  plz: "20095",
  ort: "Hamburg",
  email: "max.mustermann@example.com",
  telefon: "+49 40 12345678",
  mitgliedschaftVDH: "VDH Hamburg e.V., Mitglied seit 2020",
  hundName: "Bella",
  hundZwinger: "von der Elbe",
  hundZuchtbuch: "HZD-12345",
  hundChip: "123456789012345",
  hundWurfdatum: "2022-03-15",
  hundRasse: "Hovawart",
  hundGeschlecht: "Hündin",
  hundVersicherung: "Allianz",
  hundVersNr: "VERS-789456",
  kontoinhaber: "Max Mustermann",
  mitgliedschaft: "HZD Vollmitgliedschaft",
  kurzzeitVon: "",
  kurzzeitBis: "",
  sepaName: "Max Mustermann",
  sepaIban: "DE89370400440532013000",
  sepaBic: "COBADEFFXXX",
  sepaKreditinstitut: "Commerzbank AG",
  weitereMitteilungen: "Ich bin sehr interessiert an der Vereinsarbeit und möchte gerne bei Veranstaltungen mithelfen. Außerdem habe ich bereits Erfahrung in der Hundezucht."
};

// Test-Szenario: Kurzzeitmitgliedschaft
export const testKurzzeitMitglied: FormData = {
  anrede: "Frau",
  name: "Schmidt",
  vorname: "Anna",
  geburtsdatum: "1990-04-22",
  strasse: "Hauptstraße 45",
  plz: "21031",
  ort: "Hamburg",
  email: "anna.schmidt@email.de",
  telefon: "+49 40 98765432",
  mitgliedschaftVDH: "",
  hundName: "Luna",
  hundZwinger: "von der Alster",
  hundZuchtbuch: "HZD-67890",
  hundChip: "987654321098765",
  hundWurfdatum: "2021-08-10",
  hundRasse: "Hovawart",
  hundGeschlecht: "Hündin",
  hundVersicherung: "HUK-Coburg",
  hundVersNr: "HUK-456789",
  kontoinhaber: "Anna Schmidt",
  mitgliedschaft: "Kurzzeitmitglied",
  kurzzeitVon: "2024-01-01",
  kurzzeitBis: "2024-12-31",
  sepaName: "Anna Schmidt",
  sepaIban: "DE12500105170648489890",
  sepaBic: "INGDDEFF",
  sepaKreditinstitut: "ING-DiBa AG",
  weitereMitteilungen: "Ich möchte zunächst die Kurzzeitmitgliedschaft testen, bevor ich mich für eine Vollmitgliedschaft entscheide."
};

// Test-Szenario: Familienmitgliedschaft
export const testFamilienMitglied: FormData = {
  anrede: "Frau",
  name: "Weber",
  vorname: "Maria",
  geburtsdatum: "1982-09-14",
  strasse: "Familienweg 12",
  plz: "21035",
  ort: "Hamburg",
  email: "maria.weber@familie.de",
  telefon: "+49 40 11122233",
  mitgliedschaftVDH: "VDH Hamburg e.V., Mitglied seit 2015",
  hundName: "Bruno",
  hundZwinger: "von der Bille",
  hundZuchtbuch: "HZD-98765",
  hundChip: "555666777888999",
  hundWurfdatum: "2020-11-05",
  hundRasse: "Hovawart",
  hundGeschlecht: "Rüde",
  hundVersicherung: "Allianz",
  hundVersNr: "ALL-789012",
  kontoinhaber: "Maria Weber",
  mitgliedschaft: "OG Familienmitglied",
  kurzzeitVon: "",
  kurzzeitBis: "",
  sepaName: "Maria Weber",
  sepaIban: "DE12500105170648489890",
  sepaBic: "INGDDEFF",
  sepaKreditinstitut: "ING-DiBa AG",
  weitereMitteilungen: "Ich bin Mutter von zwei Kindern und möchte gerne an familienfreundlichen Veranstaltungen teilnehmen."
};

// Test-Szenario: Jugendmitgliedschaft mit Antragsteller als Kontoinhaber
export const testJugendMitglied: FormData = {
  anrede: "Herr",
  name: "Klein",
  vorname: "Peter",
  geburtsdatum: "1995-07-28",
  strasse: "Jugendweg 3",
  plz: "21037",
  ort: "Hamburg",
  email: "peter.klein@jugend.de",
  telefon: "+49 40 44455566",
  mitgliedschaftVDH: "",
  hundName: "Asta",
  hundZwinger: "von der Elbe",
  hundZuchtbuch: "HZD-13579",
  hundChip: "999888777666555",
  hundWurfdatum: "2022-05-12",
  hundRasse: "Hovawart",
  hundGeschlecht: "Hündin",
  hundVersicherung: "HUK-Coburg",
  hundVersNr: "HUK-246810",
  kontoinhaber: "Peter Klein",
  mitgliedschaft: "HZD Familienmitglied",
  kurzzeitVon: "",
  kurzzeitBis: "",
  sepaName: "",
  sepaIban: "DE89370400440532013000",
  sepaBic: "COBADEFFXXX",
  sepaKreditinstitut: "Commerzbank AG",
  weitereMitteilungen: "Als junger Hundebesitzer freue ich mich auf den Austausch mit erfahrenen Züchtern."
};

// Alle Test-Szenarien als Array
export const allTestScenarios: FormData[] = [
  testFormData,
  testKurzzeitMitglied,
  testFamilienMitglied,
  testJugendMitglied
];

// Hilfsfunktion zum Generieren von zufälligen Test-Daten
export function generateRandomTestData(): FormData {
  const names = ["Müller", "Schmidt", "Schneider", "Fischer", "Weber", "Meyer", "Wagner", "Becker"];
  const vornamen = ["Max", "Anna", "Thomas", "Maria", "Peter", "Lisa", "Michael", "Sarah"];
  const hundeNamen = ["Bella", "Luna", "Rex", "Bruno", "Asta", "Max", "Luna", "Rex"];
  const rassen = ["Hovawart", "Deutscher Schäferhund", "Labrador", "Golden Retriever"];
  const geschlechter = ["Rüde", "Hündin"];
  const mitgliedschaften = ["HZD Vollmitgliedschaft", "Kurzzeitmitglied", "OG Familienmitglied", "HZD Familienmitglied"];
  
  const randomName = names[Math.floor(Math.random() * names.length)];
  const randomVorname = vornamen[Math.floor(Math.random() * vornamen.length)];
  const randomHundName = hundeNamen[Math.floor(Math.random() * hundeNamen.length)];
  const randomRasse = rassen[Math.floor(Math.random() * rassen.length)];
  const randomGeschlecht = geschlechter[Math.floor(Math.random() * geschlechter.length)];
  const randomMitgliedschaft = mitgliedschaften[Math.floor(Math.random() * mitgliedschaften.length)];
  const randomAnrede = Math.random() > 0.5 ? "Herr" : "Frau";
  
  return {
    anrede: randomAnrede,
    name: randomName,
    vorname: randomVorname,
    geburtsdatum: "1985-06-15",
    strasse: "Teststraße 123",
    plz: "20095",
    ort: "Hamburg",
    email: `${randomVorname.toLowerCase()}.${randomName.toLowerCase()}@test.de`,
    telefon: "+49 40 12345678",
    mitgliedschaftVDH: "",
    hundName: randomHundName,
    hundZwinger: "von der Elbe",
    hundZuchtbuch: `HZD-${Math.floor(Math.random() * 99999)}`,
    hundChip: Math.floor(Math.random() * 1000000000000000).toString(),
    hundWurfdatum: "2022-03-15",
    hundRasse: randomRasse,
    hundGeschlecht: randomGeschlecht,
    hundVersicherung: "Allianz",
    hundVersNr: `VERS-${Math.floor(Math.random() * 999999)}`,
    kontoinhaber: `${randomVorname} ${randomName}`,
    mitgliedschaft: randomMitgliedschaft,
    kurzzeitVon: randomMitgliedschaft === "Kurzzeitmitglied" ? "2024-01-01" : "",
    kurzzeitBis: randomMitgliedschaft === "Kurzzeitmitglied" ? "2024-12-31" : "",
    sepaName: `${randomVorname} ${randomName}`,
    sepaIban: "DE89370400440532013000",
    sepaBic: "COBADEFFXXX",
    sepaKreditinstitut: "Commerzbank AG",
    weitereMitteilungen: "Test-Mitteilung für automatisch generierte Daten."
  };
}
