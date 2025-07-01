import requests
import csv
import os
import requests
import json
from dotenv import load_dotenv

# .env-Datei laden
load_dotenv()

host = os.getenv('DOLIBARR_HOST')
api_key = os.getenv('DOLIBARR_API_KEY')

#  ,ID Person,0/1 access,salutation,title,firstname,lastname,language,
# street,zipcode,city,oblast,country,organization,mobile,phone,email,
# internet,type of person,person is a breeder,person is a member,person is a subscriber,
# type of subscription,person is an active breeder,breeding station,given name first,
# membership number,membership status,role in association,other roles,date of birth,
# date of death,date of joining,date of leaving,
# IBAN,Bank Identifier Code (BIC),

# Pfad zur CSV-Datei
filename = 'chromosoft-export-20250621.csv'

def dolibarr_suche(vorname, nachname):
    # SQL-Filter für exakte Übereinstimmung
    sqlfilters = f"(firstname:=:'{vorname}') AND (lastname:=:'{nachname}')"

    # API-Endpunkt
    url = f"{host}/api/index.php/members"
    params = {'sqlfilters': sqlfilters}
    headers = {
        'DOLAPIKEY': api_key,
        'Accept': 'application/json'
    }

    # GET-Request an Dolibarr
    response = requests.get(url, headers=headers, params=params)

    # Antwort prüfen
    if response.status_code == 200:
        daten = response.json()
        if daten:
            #for mitglied in daten:
            #    print(f"- {mitglied.get('firstname')} {mitglied.get('lastname')} (ID: {mitglied.get('id')})")
            n = len(daten)
            if n<0 or n>1:
                print("Mehredutiges Mitglied")
                raise
            return daten[0]
    return None

by_mitgliedsnr = {}

def pruefe_row(row):
    id = row.get('ID Person')
    email = row.get('email')
    firstname = row.get('firstname')
    lastname = row.get('lastname')
    is_member = row.get('person is a member')

    status = row.get('membership status')
    mitgliedsnr = row.get('membership number')
    if is_member != "1":
        #print(f"Kein Mitglied (mehr) (id={id}/mitgliedsnr={mitgliedsnr}) - {firstname} {lastname} {email} {is_member}")
        raise
    if status == None or status.strip() == "-":
        #print(f"Kein Mitgliedsstatus (id={id}/mitgliedsnr={mitgliedsnr}) - {firstname} {lastname} {email}")
        raise
    if mitgliedsnr == None or status.strip() == "-":
        #print(f"Keine Mitgliedsnr (id={id})- {firstname} {lastname} – {email}")
        raise

    return id, email, firstname, lastname, status, mitgliedsnr

def check_member(dolibarr_user, row):
    dolibarr_membership = dolibarr_user["typeid"]
    chromosoft_membership = row.get('membership status')
    if dolibarr_membership=="3" and chromosoft_membership=="Mitglied":
        return
    if dolibarr_membership=="4" and chromosoft_membership=="Familienmitglied":
        return
    print(dolibarr_membership, chromosoft_membership)
    #raise

def typeid2type(typeid):
    if typeid=="1":
        return "OG-Mitglied"
    if typeid=="2":
        return "OG-Familienmitglied"
    if typeid=="3":
        return "HZD-Vollmitglied"
    if typeid=="4":
        return "HZD-Familienmitglied"
    if typeid=="5":
        return "Kurzmitglied"
    return

def dolibar_member(firstname, lastname, status, mitgliedsnr, email, typeid):
    url = f"{host}/api/index.php/members"
    headers = {
        'DOLAPIKEY': api_key,
        'Accept': 'application/json'
    }

    member = {
        "firstname": firstname,
        "lastname": lastname,
        "status": 0,
        "typeid": typeid,
        "email": email
    }
    print('Mitglied anlegen', member)
    response = requests.post(url, headers=headers, json=member)
    if response.status_code == 200:
        return
    print(response.status_code, response.text)
    return

# Öffne die Datei mit UTF-8 und newline=""
with open(filename, mode='r', encoding='utf-8', newline='') as csvfile:
    reader = csv.DictReader(csvfile)

    n = 0;
    n_oghh = 0;
    for row_num, row in enumerate(reader, start=1):

        # Optional: Zugriff auf z. B. Notizen oder Optionen
        notiz = row.get('note_public', '').strip()
        if notiz:
            print(f"   ➜ Öffentliche Notiz: {notiz}")

        try:
             id, email, firstname, lastname, status, mitgliedsnr = pruefe_row(row)
             by_mitgliedsnr[mitgliedsnr] = row
             joined = row.get('date of joining')
             n = n+1
             dolibarr_user = dolibarr_suche(firstname, lastname)
             if dolibarr_user:
                is_og = True
                og = "OG"
                check_member(dolibarr_user, row)
             else:
                is_og = False
                og = "  "
             print(f" verarbeite {n} {og} {id} {mitgliedsnr} {firstname} {lastname} - {joined}")
             if is_og != 0:
                n_oghh = n_oghh+1
             else:
                 dolibar_member(firstname, lastname, status, mitgliedsnr, email, 1)
        except:
            #print("fehler - nicht verarbeiten")
            continue

    print(f"{n_oghh}/{n} wurden in der oghh gefunden")

