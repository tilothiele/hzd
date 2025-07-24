import csv
import random
from faker import Faker
from datetime import datetime, timedelta

fake = Faker("de_DE")

def gewichteter_status():
    rnd = random.random()
    if rnd < 0.90:
        return "vollmitglied"
    elif rnd < 0.97:
        return "familienmitglied"
    else:
        return "kurzmitglied"

def generiere_daten():
    vorname = fake.first_name()
    nachname = fake.last_name()
    straße = fake.street_name()
    hausnummer = str(random.randint(1, 299))  # nur positive Hausnummern
    plz = fake.postcode()
    ort = fake.city()
    geburtsdatum = fake.date_of_birth(minimum_age=18, maximum_age=85).strftime("%Y-%m-%d")
    mitgliedsstatus = gewichteter_status()
    iban = fake.iban()

    # Mitglied seit: zwischen heute und vor 10 Jahren
    mitglied_seit_dt = fake.date_between(start_date='-10y', end_date='today')
    mitglied_seit = mitglied_seit_dt.strftime("%Y-%m-%d")

    # 20 % Wahrscheinlichkeit für gekündigt zum
    if random.random() < 0.2:
        # gekündigt irgendwann nach "mitglied_seit"
        max_kuendigung_dt = datetime.today()
        gekuendigt_zum_dt = fake.date_between(start_date=mitglied_seit_dt, end_date=max_kuendigung_dt)
        gekuendigt_zum = gekuendigt_zum_dt.strftime("%Y-%m-%d")
    else:
        gekuendigt_zum = ""

    # E-Mail auf Basis von Vor- und Nachnamen
    email = f"{vorname.lower()}.{nachname.lower()}@example.org".replace("ä", "ae").replace("ö", "oe").replace("ü", "ue").replace("ß", "ss")

    return [
        vorname, nachname, straße, hausnummer, plz, ort,
        geburtsdatum, email, mitgliedsstatus, iban, mitglied_seit, gekuendigt_zum
    ]

# Datei schreiben
with open("testdaten.csv", "w", newline="", encoding="utf-8") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow([
        "vorname", "nachname", "straße", "hausnummer", "plz", "ort",
        "geburtsdatum", "email", "mitgliedsstatus", "iban", "mitglied_seit", "gekündigt_zum"
    ])
    for _ in range(100):
        writer.writerow(generiere_daten())
