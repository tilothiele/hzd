import csv
import datetime
from models.faker_member import DoliMember
from models.dolibarr_actions import post_member

# CSV zeilenweise einlesen
with open("testdaten.csv", newline="", encoding="utf-8") as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        member = DoliMember.from_csv_row(row)
        typeid = 1 if member.mitgliedsstatus=="vollmitglied" else 2 if member.mitgliedsstatus=="familienmitglied" else 3
        dmember = {
                'lastname': member.nachname,
                'firstname': member.vorname,
                'email': member.email,
                'user_login': member.vorname+"."+member.nachname,
                'address' :member.straße+" "+member.hausnummer,
                'zip': member.plz,
                'town': member.ort,
                'type': member.mitgliedsstatus,
                #'phone_perso': member.
                'morphy': 'phy',
                'entity': '1',
                'statut': '1',
                'status': '1',
                'country_id': '5',
                'country_code': 'DE',
                'typeid': str(typeid),
                'birth': member.geburtsdatum.strftime("%Y-%m-%d"),
                'array_options': {
                    'options_mitgliedsnummer': str(member.mitgliedsnr),
                    'options_hundename': member.hund,
                    'options_wurfdatum': int(datetime.datetime.combine(member.wurfdatum, datetime.time()).timestamp()) if member.wurfdatum!=None else None,
                    'options_zuchter': '1' if member.ist_zuechter else '0',
                    'options_zwingername': member.zwingername,
                    'options_mitglied_seit': int(datetime.datetime.combine(member.mitglied_seit, datetime.time()).timestamp()) if member.mitglied_seit!=None else None,
                    'options_gekundigt_zum': int(datetime.datetime.combine(member.gekuendigt_zum, datetime.time()).timestamp()) if member.gekuendigt_zum!=None else None
                }
        }
        post_member(dmember)
        print(str(member.mitgliedsnr)+" - "+member.vorname+" "+member.nachname)
