from models.dolibarr_member import DolibarrMember
from models.dolibarr_actions import find_by_soc, find_all, hasMitgliedsantrag
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

def mussZahlen(p: DolibarrMember) -> bool:
    if(p.typeid=='6'):
        return False
    if(not p.statut=='1'):
        return False
    return True

if __name__ == '__main__':
    lastschriften_map = {}

    dolibarr_liste = find_all()
    dolibarr_liste_sorted = sorted(dolibarr_liste, key=lambda p: (p.lastname.lower(), p.firstname.lower()))
    n = 0
    ohne_bankverbindung = 0
    ohne_mitgliedsantrag = 0
    for p in dolibarr_liste_sorted:
        if not mussZahlen(p):
            print("---> muss nicht zahlen: "+dolibarrKey(p))
            continue
        n = n+1
        ibans = ""
        kontoinhaber = ""
        if p.fk_soc:
            bank_accounts = find_by_soc(p.fk_soc)
            ibans = ",".join([account.iban for account in bank_accounts])
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
        if ibans == "":
            ibans = "*** Keine Bankverbindung *** "
            ohne_bankverbindung = ohne_bankverbindung + 1
        b = typeid2Beitrag(p.typeid)
        if not hasMitgliedsantrag(p.id):
            hm = "*** Mitgliedsantrag fehlt ***"
            ohne_mitgliedsantrag = ohne_mitgliedsantrag +1
        else:
            hm = ""
        print(str(n)+ ", "+ p.lastname+", "+p.firstname+", "+p.type+", "+p.email+", "+str(b)+", "+ibans+", "+hm)
    print(str(ohne_bankverbindung)+" Mitglieder ohne Bankverbindung.")
    print(str(ohne_mitgliedsantrag)+" Mitglieder ohne Mitgliedsantrag.")
