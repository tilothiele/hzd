from models.dolibarr_member import DolibarrMember
from models.dolibarr_actions import find_by_soc,  get_by_id, setze_bankverbindung
from dataclasses import dataclass
import csv
from typing import Optional, List

# -----------------------------------------------------------------------
# Die IBANS werden vom Hauptmitglied zum Familienmitglied kopiert
# -----------------------------------------------------------------------

@dataclass
class TransferDatensatz:
    von: int
    nach: int

def name(m: DolibarrMember) -> str:
    return m.firstname+" "+m.lastname

def parse_csv() -> List[TransferDatensatz]:
    rv = []
    file_path = 'transfer-ibans.csv'  # Pfad zur Datei anpassen
    with open(file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            ds = TransferDatensatz(
                von=row['von'],
                nach=row['nach']
            )
            rv.append(ds)
    return rv;

if __name__ == '__main__':
    transfer_liste = parse_csv()
    lastschriften_map = {}
    for p in transfer_liste:
        von_member = get_by_id(p.von)
        bank_accounts = find_by_soc(von_member.fk_soc)
        iban = None
        bic = None
        for ba in bank_accounts:
            iban = ba.iban
            bic = ba.bic

        nach_member = get_by_id(p.nach)

        print(name(von_member)+"  ----->   "+name(nach_member))
        setze_bankverbindung(nach_member, iban, bic)
