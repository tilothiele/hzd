from datetime import datetime
import requests
from models.dolibarr_member import DolibarrMember,mussZahlen
from models.dolibarr_actions import find_by_soc, find_all, patch_bank_account
from dataclasses import dataclass
import csv
from typing import Optional, List

# -----------------------------------------------------------------------
# für jede Bankverbindung wird für jede IBANS der Kontoinhaber und das Unterzeichnerdatum kopiert.
# -----------------------------------------------------------------------


@dataclass
class LastschritDatensatz:
    kontoinhaber: str
    datum: str
    iban: str

def lastschriftenKey(m: LastschritDatensatz):
    return str(m.name)

def dolibarrKey(m: DolibarrMember):
    return m.firstname + " " + m.lastname

def parse_csv() -> dict[str, LastschritDatensatz]:
    rv = {}
    file_path = 'Lastschriften_IBAN_Datum.csv'  # Pfad zur Datei anpassen
    with open(file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            ds = LastschritDatensatz(
                kontoinhaber=row['Kontoinhaber'],
                datum=row['Datum des Mandates'],
                iban=row['IBAN']
            )
            rv[ds.iban] = ds
    return rv;


def ibanDetails(iban):
    url = f"https://openiban.com/validate/{iban}?getBIC=true"
    response = requests.get(url)
    response.raise_for_status()
    iban_response = response.json()
    #print(iban_response)
    if iban_response["valid"]==False:
        raise ValueError("*** WARN *** iban "+iban+" nicht gültig")
    if not iban.startswith("DE") or len(iban) != 22:
        raise ValueError("Nur deutsche IBANs mit 22 Zeichen werden unterstützt.")
    data = {
#        "label": name,
        "iban": iban,
        "bic": iban_response["bankData"]["bic"],
        "blz": iban_response["bankData"]["bankCode"],
        "bank": iban_response["bankData"]["name"],
        "kontonr": iban[12:]
#        "default_rib": "1",
#        "frstrecur": "RCUR"
    }
    return data

if __name__ == '__main__':
    lastschriften_liste = parse_csv()

    dolibarr_liste = find_all()
    dolibarr_liste_sorted = sorted(dolibarr_liste, key=lambda p: (p.lastname.lower(), p.firstname.lower()))
    for p in dolibarr_liste_sorted:
        if not mussZahlen(p):
            continue

        bas = find_by_soc(p.fk_soc)
        if(len(bas)==0):
            msg = f"*** keine Bankverbindung für {p.firstname} {p.lastname} ***"
            print(msg)
            continue
        ba = bas[0]
        ld = lastschriften_liste.get(ba.iban)
        if(ld==None):
            msg = f"*** Bankverbindung für {p.firstname} {p.lastname} (soc_id={p.fk_soc}) gefunden: {ba.label}, aber IBAN nicht in der csv-importdatei ***"
            print(msg)
            continue
        msg = f"Bankverbindung für {p.firstname} {p.lastname} (soc_id={p.fk_soc}) gefunden: {ba.label}"
        id = ibanDetails(ba.iban)
        #print(ba.iban, ld.datum)
        dt = datetime.strptime(ld.datum, "%d.%m.%Y")
        bank_accout_patch = {
            "label": ld.kontoinhaber,
            "owner_name": ld.kontoinhaber,
            "proprio": ld.kontoinhaber,
            "bank": id["bank"],
            "code_banque": id["blz"],
            "number": id["kontonr"],
            "bic": id["bic"],
            "date_rum": dt.strftime("%Y-%m-%d"),
            "frstrecur": "RCUR"
        }
        print(bank_accout_patch)
        patch_bank_account(p.fk_soc, ba.id, bank_accout_patch)

