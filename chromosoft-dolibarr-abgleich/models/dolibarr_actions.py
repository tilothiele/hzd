import requests
from typing import List
from models.dolibarr_member import DolibarrMember, BankAccount
from dotenv import load_dotenv
import os
import json

def set_mitgliedsnummer(member: DolibarrMember, nr):
    data = {
        "array_options": {
            "options_mitgliedsnummer": nr
        }
    }
    put_member(member=member, data=data)
    return

def freigeben(member: DolibarrMember):
    data = {
        "statut": "1"
    }
    print("freigeben id="+member.id)
    put_member(member=member, data=data)
    return

def setze_bankverbindung(member: DolibarrMember, iban, bic):
    load_dotenv()
    host = os.getenv('DOLIBARR_HOST')
    api_key = os.getenv('DOLIBARR_API_KEY')
    headers = {
        'DOLAPIKEY': api_key,
        'Accept': 'application/json',
        'Content-Type': 'application/json'
    }
    if member.fk_soc==None:
        print("Kein Geschäftspartner vorhanden -> anlegen", iban, bic)
        data = {
            "status": "1",
            "country_id": "5",
            "country_code": "DE",
            "client": "1",
            "code_client": "-1",
            "name": member.firstname+" "+member.lastname,
            "email": member.email,
            "entity": "1"
        }
        url = f"{host}/api/index.php/thirdparties"
        response = requests.post(url, headers=headers, data=json.dumps(data))
        print(response.text)
        response.raise_for_status()
        soc_id = response.text
        data = {
            "fk_soc": soc_id,
            "socid": soc_id
        }
        put_member(member=member, data=data)

    url = f"{host}/api/index.php/members/{member.id}"
    return

def put_member(member: DolibarrMember, data):
    load_dotenv()
    host = os.getenv('DOLIBARR_HOST')
    api_key = os.getenv('DOLIBARR_API_KEY')
    url = f"{host}/api/index.php/members/{member.id}"
    headers = {
        'DOLAPIKEY': api_key,
        'Accept': 'application/json',
        'Content-Type': 'application/json'
    }

    #print(url, data)
    response = requests.put(url, headers=headers, data=json.dumps(data))
    response.raise_for_status()

def find_by_soc(soc_id) -> List[BankAccount]:
    load_dotenv()
    host = os.getenv('DOLIBARR_HOST')
    api_key = os.getenv('DOLIBARR_API_KEY')
    url = f"{host}/api/index.php/thirdparties/{soc_id}/bankaccounts"
    headers = {
        'DOLAPIKEY': api_key,
        'Accept': 'application/json'
    }

    # GET-Request an Dolibarr
    response = requests.get(url, headers=headers)

    # Antwort prüfen
    if response.status_code == 200:
        data = response.json()
        return [BankAccount.from_json(item) for item in data]
    if response.status_code == 404:
        return []

    raise


def find_all() -> List[DolibarrMember]:
    load_dotenv()
    host = os.getenv('DOLIBARR_HOST')
    api_key = os.getenv('DOLIBARR_API_KEY')
    url = f"{host}/api/index.php/members"
    headers = {
        'DOLAPIKEY': api_key,
        'Accept': 'application/json'
    }

    rv = []
    more_data = True
    limit = 100
    pageNo = 0
    while more_data:

        params = {
            "limit": limit,
            "page": pageNo,
            "sortfield": "t.rowid"

        }
        # GET-Request an Dolibarr
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()

        # Antwort prüfen
        data = response.json()
        liste = [DolibarrMember.from_json(item) for item in data]
        rv.extend(liste)
        pageNo = pageNo+1
        more_data = True if len(liste)==limit else False

    return rv


def find_by_name(vorname, nachname):
    # .env-Datei laden
    load_dotenv()
    host = os.getenv('DOLIBARR_HOST')
    api_key = os.getenv('DOLIBARR_API_KEY')
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
