from models.dolibarr_member import DolibarrMember,mussZahlen
from models.dolibarr_actions import find_by_soc, find_all
from dataclasses import dataclass
import csv

# -----------------------------------------------------------------
# Liest die Datei Lastschriften_IBAN_Datum.csv
# Hold alle aktiven Mitglieder von Dolibarr
# Schreibt auf stdout die Lastschriftdatensätze als csv
# -----------------------------------------------------------------

@dataclass
class LastschritDatensatz:
    name: str
    mandat: str
    betrag: float
    iban: str

def lastschriftenKey(m: LastschritDatensatz):
    return str(m.iban)

def dolibarrKey(m: DolibarrMember):
    return m.firstname + " " + m.lastname

def typeid2Beitrag(typeid) -> float:
    if typeid=="1":
        return 138
#        return "OG-Mitglied"
    if typeid=="2":
        return 16
#        return "OG-Familienmitglied"
    if typeid=="3":
        return 35
#        return "HZD-Vollmitglied"
    if typeid=="4":
        return 16
#        return "HZD-Familienmitglied"
    if typeid=="5":
        return 0
#        return "Kurzmitglied"
    raise

@dataclass
class AbgleichDatensatz:
    kontoinhaber: str
    datum: str
    iban: str
    mandatsreferenz: str

def lastschriftenKey(m: AbgleichDatensatz):
    return str(m.name)

def dolibarrKey(m: DolibarrMember):
    return m.firstname + " " + m.lastname

def parse_abgleich_csv() -> dict[str, AbgleichDatensatz]:
    rv = {}
    file_path = 'Lastschriften_IBAN_Datum.csv'  # Pfad zur Datei anpassen
    with open(file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        nr = 0
        for row in reader:
            nr = nr + 1
            ds = AbgleichDatensatz(
                kontoinhaber=row['Kontoinhaber'],
                datum=row['Datum des Mandates'],
                iban=row['IBAN'],
                mandatsreferenz=str(nr)
            )
            rv[ds.iban] = ds
    return rv;


if __name__ == '__main__':
    ad = parse_abgleich_csv()
    lastschriften_map = {}

    dolibarr_liste = find_all()
    dolibarr_liste_sorted = sorted(dolibarr_liste, key=lambda p: (p.lastname.lower(), p.firstname.lower()))
    for p in dolibarr_liste_sorted:
        if not mussZahlen(p):
            continue
        if not ("Bensemann" in p.lastname):
            continue
        ibans = ""
        kontoinhaber = ""
        if p.fk_soc:
            bank_accounts = find_by_soc(p.fk_soc)
            ibans = ",".join([account.iban for account in bank_accounts])
        if ibans == "":
            continue
        kontoinhaber = dolibarrKey(p)
        l = lastschriften_map.get(ibans)
        if l == None:
            l = LastschritDatensatz(
                iban = ibans,
                mandat = "",
                betrag= 0,
                name=kontoinhaber
            )
            lastschriften_map[ibans] = l
        b = typeid2Beitrag(p.typeid)
        l.betrag = l.betrag + b
        sep = ""  if len(l.mandat)==0 else "+"
        l.mandat = l.mandat + sep + str(b)+"("+dolibarrKey(p)+")"

    n = 0
    gesamt = 0
    print("iban,betrag,kontoinhaber,mandat_vom,buchungstext,Mandatsreferenz")
    for lastschrift in lastschriften_map.values():
        n = n+1
        gesamt = gesamt + lastschrift.betrag
        #print(lastschrift.mandat)
        a = ad[lastschrift.iban]
        buchungstext = "HZD OG-Hamburg Mitgliedsbeitrag 2025 "+lastschrift.mandat
        print(lastschrift.iban+","+str(lastschrift.betrag)+","+a.kontoinhaber+","+a.datum+","+buchungstext+","+a.mandatsreferenz)

    print(str(n)+" Datensätze erzeugt")
    print("Gesamtbetrag="+str(gesamt))
