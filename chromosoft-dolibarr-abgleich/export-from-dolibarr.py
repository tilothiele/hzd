import requests
import csv
import os
import json
from dotenv import load_dotenv

# .env-Datei laden
load_dotenv()

API_KEY = os.getenv('API_KEY')
DOLIBARR_HOST = os.getenv('DOLIBARR_HOST')
BASE_URL = f'{DOLIBARR_HOST}/api/index.php/members'
HEADERS = {
    'Accept': 'application/json',
    'DOLAPIKEY': API_KEY
}

def fetch_all_members():
    all_members = []
    limit = 100
    page = 0  # Start bei Seite 0 oder 1 – je nach API-Spezifikation (meistens 0-basiert)

    while True:
        params = {
            'sortfield': 't.rowid',
            'sortorder': 'ASC',
            'limit': limit,
            'page': page
        }
        response = requests.get(BASE_URL, headers=HEADERS, params=params)
        response.raise_for_status()

        data = response.json()

        if not data:
            break  # keine Daten mehr

        all_members.extend(data)

        if len(data) < limit:
            break  # letzte Seite erreicht

        page += 1  # nächste Seite

    return all_members

def write_to_csv(data, filename='dolibarr-export.csv'):
    if not data:
        print("Keine Daten zum Schreiben.")
        return

    # Alle Keys inklusive der inneren Keys aus array_options sammeln
    all_keys = set()

    normalized_data = []
    for entry in data:
        entry_copy = entry.copy()

        # array_options parsen, falls vorhanden
        array_opts_raw = entry_copy.get('array_options')
        if array_opts_raw:
            try:
                if isinstance(array_opts_raw, str):
                    array_opts = json.loads(array_opts_raw)
                elif isinstance(array_opts_raw, dict):
                    array_opts = array_opts_raw
                else:
                    array_opts = {}
                # Erweiterung des Haupt-Dicts
                entry_copy.update(array_opts)
                entry_copy.pop('array_options', None)
                all_keys.update(array_opts.keys())
            except json.JSONDecodeError:
                print("Fehler beim Parsen von array_options:", array_opts_raw)
        all_keys.update(entry_copy.keys())
        normalized_data.append(entry_copy)

    all_keys = sorted(all_keys)  # konsistente Spaltenreihenfolge

    with open(filename, mode='w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=all_keys)
        writer.writeheader()
        writer.writerows(normalized_data)

if __name__ == "__main__":
    members = fetch_all_members()
    write_to_csv(members)
    print(f"{len(members)} Mitglieder in members.csv gespeichert.")
