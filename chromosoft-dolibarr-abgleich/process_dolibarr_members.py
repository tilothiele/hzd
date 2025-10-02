from models.chromosoft_member import parse_csv, ChromosoftMember
from models.dolibarr_member import DolibarrMember
from models.dolibarr_actions import find_by_soc, find_all, set_hzd_mitglied_seit
from models.chromosoft_members_table import get_member_by_membership_number

from datetime import date

def chromosoftKey(m: ChromosoftMember):
    return str(m.membership_number)

def dolibarrKey(m: DolibarrMember):
    return str(m.mitgliedsnr)

if __name__ == '__main__':
    dolibarr_liste = find_all()
    dolibarr_liste_sorted = sorted(dolibarr_liste, key=lambda p: (p.lastname.lower(), p.firstname.lower()))
    n = 0
    for p in dolibarr_liste_sorted:
        mn = p.mitgliedsnr
        if(mn):
            cm = get_member_by_membership_number(mn)
            if(cm==None):
                print(mn, "nicht in tabelle gefunden")
                continue
            doj: date = cm['date_of_joining']
            if(doj):
                print(p.mitgliedsnr, doj)
                set_hzd_mitglied_seit(p, doj)
            else:
                print(p.mitgliedsnr, 'hat kein date_of_joining')

