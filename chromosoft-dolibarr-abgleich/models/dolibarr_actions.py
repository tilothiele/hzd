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

def get_by_id(id: int) -> DolibarrMember:
    url = f"/api/index.php/members/{str(id)}"
    response = getDolibarApiResponse(url, None)
    response.raise_for_status()

    daten = response.json()
    return DolibarrMember.from_json(daten)

def setze_bankverbindung(member: DolibarrMember, iban, bic):
    load_dotenv()
    host = os.getenv('DOLIBARR_HOST')
    api_key = os.getenv('DOLIBARR_API_KEY')
    headers = {
        'DOLAPIKEY': api_key,
        'Accept': 'application/json',
        'Content-Type': 'application/json'
    }
    socid = member.fk_soc
    name = member.firstname+" "+member.lastname
    if socid==None:
        id = int(member.id)
        personenkonto = f"1000{id:04d}"
        print("Kein Geschäftspartner vorhanden -> anlegen", iban, bic)
        data = {
            "status": "1",
            "country_id": "5",
            "country_code": "DE",
            "client": "1",
            "code_client": "-1",
            "name": name,
            "email": member.email,
            "entity": "1",
            "mode_reglement_id": "3",
            "tva_assuj": "0",
            "code_compta": personenkonto
        }
        url = f"{host}/api/index.php/thirdparties"
        response = requests.post(url, headers=headers, data=json.dumps(data))
        response.raise_for_status()
        socid = response.text
        data = {
            "fk_soc": socid,
            "socid": socid
        }
        put_member(member=member, data=data)
    if iban==None or iban=='-':
        return
    if bic=='-':
        bic = None;
    bank_accounts = find_by_soc(socid)
    for ba in bank_accounts:
        if ba.iban==iban:
            print("IBAN "+iban+" gibt es schon für diesen Geschäftspartner")
            return
        else:
            print("*** ERROR *** " + name+" thirdparty hat ein anderes Konto: "+ba.iban+" nicht "+iban)
            return
    print("Bankkonto "+iban+" anlegen.")
    url = f"https://openiban.com/validate/{iban}?getBIC=true"
    response = requests.get(url)
    response.raise_for_status()
    iban_response = response.json()
    #print(iban_response)
    if iban_response["valid"]==False:
        print("*** WARN *** iban "+iban+" nicht gültig")
        return
    data = {
        "label": name,
        "iban": iban,
        "bic": iban_response["bankData"]["bic"],
        "bank": iban_response["bankData"]["name"],
        "default_rib": "1",
        "frstrecur": "RCUR"
    }
    url = f"{host}/api/index.php/thirdparties/{socid}/bankaccounts"
    response = requests.post(url, headers=headers, data=json.dumps(data))
    response.raise_for_status()
    return

def patch_bank_account(soc_id, bank_id, patch_data):
    load_dotenv()
    host = os.getenv('DOLIBARR_HOST')
    api_key = os.getenv('DOLIBARR_API_KEY')
    headers = {
        'DOLAPIKEY': api_key,
        'Accept': 'application/json',
        'Content-Type': 'application/json'
    }
    url = f"{host}/api/index.php/thirdparties/{soc_id}/bankaccounts/{bank_id}"
    response = requests.put(url, headers=headers, data=json.dumps(patch_data))
    response.raise_for_status()
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
    url = f"/api/index.php/thirdparties/{soc_id}/bankaccounts"

    # GET-Request an Dolibarr
    response = getDolibarApiResponse(url, None)

    # Antwort prüfen
    if response.status_code == 200:
        data = response.json()
        return [BankAccount.from_json(item) for item in data]
    if response.status_code == 404:
        return []

    raise


def find_all() -> List[DolibarrMember]:
    url = "/api/index.php/members"

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
        response = getDolibarApiResponse(url, params)
        response.raise_for_status()

        # Antwort prüfen
        data = response.json()
        liste = [DolibarrMember.from_json(item) for item in data]
        rv.extend(liste)
        pageNo = pageNo+1
        more_data = True if len(liste)==limit else False

    return rv


def find_by_name(vorname, nachname) -> DolibarrMember:
    # SQL-Filter für exakte Übereinstimmung
    sqlfilters = f"(firstname:=:'{vorname}') AND (lastname:=:'{nachname}')"

    # API-Endpunkt
    url = "/api/index.php/members"
    params = {'sqlfilters': sqlfilters}

    response = getDolibarApiResponse(url, params)

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

def getDolibarApiResponse(url: str, params):
    # .env-Datei laden
    load_dotenv()
    host = os.getenv('DOLIBARR_HOST')
    api_key = os.getenv('DOLIBARR_API_KEY')

    headers = {
        'DOLAPIKEY': api_key,
        'Accept': 'application/json'
    }

    # GET-Request an Dolibarr
    return requests.get(f"{host}{url}", headers=headers, params=params)

def hasMitgliedsantrag(member_id) -> bool:
    url = "/api/index.php/documents"
    params = {
        "modulepart": "member",
        "id": str(member_id)
    }
    response = getDolibarApiResponse(url, params);
    if response.status_code == 200:
        data = response.json()
        for item in data:
            if "Mitgliedsantrag" in item["fullname"]:
                return True
    return False
