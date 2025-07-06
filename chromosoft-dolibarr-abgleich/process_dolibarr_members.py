from models.chromosoft_member import parse_csv, ChromosoftMember
from models.dolibarr_member import DolibarrMember
from models.dolibarr_actions import find_by_soc, find_all, set_mitgliedsnummer, freigeben, setze_bankverbindung

def key1(m: ChromosoftMember):
    return m.firstname+"/"+m.lastname

def key2(m: DolibarrMember):
    return m.firstname+"/"+m.lastname

if __name__ == '__main__':
    path_to_csv = 'chromosoft-export-20250621.csv'  # Pfad zur Datei anpassen
    chromosoft_liste = parse_csv(path_to_csv)
    chromosoft_map = {}
    for p in chromosoft_liste:
        chromosoft_map[key1(p)] = p

    dolibarr_liste = find_all()
    dolibarr_liste_sorted = sorted(dolibarr_liste, key=lambda p: (p.lastname.lower(), p.firstname.lower()))
    n = 0
    for p in dolibarr_liste_sorted:
        n = n+1
        ibans = ""
        if p.fk_soc:
            bank_accounts = find_by_soc(p.fk_soc)
            ibans = ",".join([account.iban for account in bank_accounts])
        mnr = "" if p.mitgliedsnr==None else p.mitgliedsnr
        c: ChromosoftMember = chromosoft_map.get(key2(p))
        if c:
            cf = "RG-"+mnr
            if p.mitgliedsnr==None and c.membership_number!=None:
                set_mitgliedsnummer(p, c.membership_number)
            setze_bankverbindung(p, c.iban, c.bic)
        else:
            cf = "   "+mnr
        if p.statut=="-1":
            freigeben(p)
        print(str(n)+ ", "+ cf+", "+p.lastname+", "+p.firstname+", "+p.type+", "+ibans)
