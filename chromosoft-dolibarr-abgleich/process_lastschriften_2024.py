from models.dolibarr_member import DolibarrMember
from models.dolibarr_actions import find_by_soc, find_all, set_mitgliedsnummer, freigeben, setze_bankverbindung
from dataclasses import dataclass
import csv
from typing import Optional, List

@dataclass
class LastschritDatensatz:
    name: str
    mandat: str
    betrag: float
    iban: str

def lastschriftenKey(m: LastschritDatensatz):
    return str(m.name)

def dolibarrKey(m: DolibarrMember):
    return m.firstname + " " + m.lastname

def parse_csv() -> List[LastschritDatensatz]:
    rv = []
    file_path = 'lastschriften-2024.csv'  # Pfad zur Datei anpassen
    with open(file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            ds = LastschritDatensatz(
                name=row['name'],
                mandat=row['mandat'],
                betrag=row['betrag'],
                iban=row['iban']
            )
            rv.append(ds)
    return rv;

if __name__ == '__main__':
    lastschriften_liste = parse_csv()
    lastschriften_map = {}
    for p in lastschriften_liste:
        k = lastschriftenKey(p)
        if(k==None or k==""):
            continue
        lastschriften_map[k] = p

    dolibarr_liste = find_all()
    dolibarr_liste_sorted = sorted(dolibarr_liste, key=lambda p: (p.lastname.lower(), p.firstname.lower()))
    n = 0
    for p in dolibarr_liste_sorted:
        n = n+1
        ibans = ""
        if p.fk_soc:
            bank_accounts = find_by_soc(p.fk_soc)
            ibans = ",".join([account.iban for account in bank_accounts])
        mnr = "" if p.mitgliedsnr==None or p.mitgliedsnr=="-" else p.mitgliedsnr
        c: LastschritDatensatz = lastschriften_map.get(dolibarrKey(p))
        if c:
            cf = "LS-"+mnr
            ls_iban = c.iban
            setze_bankverbindung(p, c.iban, '')
        else:
            cf = "   "+mnr
            ls_iban = ""
#        if p.statut=="-1":
#            freigeben(p)
        print(str(n)+ ", "+ cf+", "+p.lastname+", "+p.firstname+", "+p.type+", "+ibans+", "+ls_iban)
