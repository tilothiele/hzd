import csv
from datetime import datetime
import hashlib

import_file = "20250803-1139214280-umsatz-camt52v8.CSV"

class KontoauszugEintrag:
    def __init__(self, daten: dict):
        self.daten = daten  # Originaldaten zur Referenz
        self.auftragskonto = daten["Auftragskonto"]
        self.buchungstag = self._parse_datum(daten["Buchungstag"])
        self.valutadatum = self._parse_datum(daten["Valutadatum"])
        self.buchungstext = daten["Buchungstext"]
        self.verwendungszweck = daten["Verwendungszweck"]
        self.glaeubiger_id = daten["Glaeubiger ID"]
        self.mandatsreferenz = daten["Mandatsreferenz"]
        self.kundenreferenz = daten["Kundenreferenz (End-to-End)"]
        self.sammlerreferenz = daten["Sammlerreferenz"]
        self.lastschrift_ursprungsbetrag = daten["Lastschrift Ursprungsbetrag"]
        self.auslagenersatz_ruecklastschrift = daten["Auslagenersatz Ruecklastschrift"]
        self.beguenstigter = daten["Beguenstigter/Zahlungspflichtiger"]
        self.iban = daten["Kontonummer/IBAN"]
        self.bic = daten["BIC (SWIFT-Code)"]
        self.betrag = self._parse_betrag(daten["Betrag"])
        self.waehrung = daten["Waehrung"]
        self.info = daten["Info"]
        self.import_id = self._generiere_import_id()

    def _parse_datum(self, datum_str: str):
        return datetime.strptime(datum_str, "%d.%m.%y").date()

    def _parse_betrag(self, betrag_str: str):
        return float(betrag_str.replace(".", "").replace(",", "."))

    def _generiere_import_id(self):
        # Wichtige Felder für eindeutige ID
        basis = f"{self.buchungstag}{self.betrag:.2f}{self.iban}{self.beguenstigter}{self.verwendungszweck}"
        hash_id = hashlib.sha256(basis.encode("utf-8")).hexdigest()
        return hash_id

    def __repr__(self):
        return f"<Eintrag {self.buchungstag} {self.betrag:.2f} EUR ID={self.import_id[:8]}>"

def lade_kontoauszug(pfad: str):
    eintraege = []
    with open(pfad, newline='', encoding='iso-8859-1') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=';', quotechar='"')
        for zeile in reader:
            eintrag = KontoauszugEintrag(zeile)
            eintraege.append(eintrag)
    return eintraege

# Name der zu erzeugenden Datei
filename = "test_bankimport.csv"

# Header (Spaltennamen)
header = [
    "date",
    "label",
    "amount",
    "oper",
    "ref",
    "categorie",
    "transaction_id",
    "bank_other",
    "iban_other",
    "owner_other",
]


# Beispielnutzung:
if __name__ == "__main__":
    kontoauszug = lade_kontoauszug(import_file)
    rows = []
    for eintrag in kontoauszug:
        print(eintrag)
        rows.append([eintrag.buchungstag,
                     eintrag.valutadatum,
                     eintrag.verwendungszweck,
                     eintrag.betrag,
                     'VIR',
                     eintrag.mandatsreferenz,
                     eintrag.buchungstext,
                     '',
                     eintrag.bic,
                     eintrag.iban,
                     eintrag.beguenstigter
                     ]);

        # CSV-Datei schreiben (UTF-8, Semikolon als Trenner)
    with open(filename, mode="w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f, delimiter=";")
        writer.writerow(header)
        writer.writerows(rows)