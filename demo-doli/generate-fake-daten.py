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

# Bausteine für die Zwingernamen
praefixe = [
    "vom", "von der", "von den"
]

# Fantasie-Ortsbestandteile
ort_teile1 = [
    "Eichen", "Grander", "Silber", "Wolf", "Hohen", "Jurameer",
    "Lehmbach", "Dunkel", "Lebergs", "Gold", "Mond", "Sonnen", "Burg"
]
ort_teile2 = [
    "Tal", "Hain", "Tannen", "Wiesen", "Burg", "See", "Fels", "Au", "Grund", "Moor"
]
def generate_zwingername():
    praefix = random.choice(praefixe)
    teil1 = random.choice(ort_teile1)
    teil2 = random.choice(ort_teile2)
    # Evtl. zusammensetzen ohne Leerzeichen, wenn es wie "Jurameer" klingen soll
    if random.random() < 0.3:
        ort = teil1 + teil2
    else:
        ort = f"{teil1} {teil2}"
    return f"{praefix} {ort}"

hundenamen = [
    "Bello", "Luna", "Sam", "Max", "Rocky", "Maya", "Lucky", "Bruno", "Nala", "Spike",
    "Amy", "Kira", "Charlie", "Balou", "Flocke", "Leo", "Milo", "Lilly", "Rex", "Oskar",
    "Simba", "Emma", "Chico", "Paula", "Ben", "Lucy", "Charly", "Sammy", "Molly", "Finn",
    "Sally", "Tobi", "Bella", "Snoopy", "Mia", "Balu", "Bonnie", "Keks", "Rocco", "Mika",
    "Cleo", "Holly", "Susi", "Fiete", "Bobby", "Anton", "Sandy", "Loki", "Momo", "Lisa",
    "Nero", "Ella", "Coco", "Sky", "Maja", "Carlo", "Momo", "Buddy", "Pepe", "Frodo",
    "Shadow", "Oscar", "Kuno", "Yara", "Tara", "Kalle", "Nemo", "Pina", "Wilma", "Nino",
    "Lenny", "Greta", "Theo", "Sunny", "Toni", "Stella", "Lou", "Pablo", "Amyra", "Aris",
    "Lando", "Mira", "Freddy", "Clara", "Marley", "Sparky", "Dusty", "Chilli", "Winnie", "Alma",
    "Bo", "Enzo", "Nelly", "Filou", "Jette", "Kimba", "Ronja", "Pixie", "Otis", "Lupo"
]

def hundename():
    name = random.choice(hundenamen)
    # Gelegentlich einen "Kosenamen" erzeugen
    if random.random() < 0.2:
        name += "chen"
    return name

def generiere_daten(mitgliedsnr):
    vorname = fake.first_name()
    nachname = fake.last_name()
    straße = fake.street_name()
    hausnummer = str(random.randint(1, 299))  # nur positive Hausnummern
    plz = fake.postcode()
    ort = fake.city()
    geburtsdatum = fake.date_of_birth(minimum_age=18, maximum_age=85).strftime("%Y-%m-%d")
    mitgliedsstatus = gewichteter_status()
    iban = fake.iban()


    hund = fake.first_name_nonbinary()
    wurfdatum = fake.date_of_birth(minimum_age=0, maximum_age=18).strftime("%Y-%m-%d")
    if mitgliedsstatus=="familienmitglied":
        if random.random() < 0.9:
            hund = ""
            wurfdatum = ""

    is_breeder = False
    zwingername = ""
    if mitgliedsstatus=="vollmitglied":
        if random.random() < 0.2:
            is_breeder = True
            zwingername = generate_zwingername()

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
        mitgliedsnr,
        vorname, nachname, straße, hausnummer, plz, ort,
        geburtsdatum, email, mitgliedsstatus,
        hund, wurfdatum,
        is_breeder,
        zwingername,
        iban,
        mitglied_seit, gekuendigt_zum
    ]

# Datei schreiben
with open("testdaten.csv", "w", newline="", encoding="utf-8") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow([
        "mitgliedsnr", "vorname", "nachname",
        "straße", "hausnummer", "plz", "ort",
        "geburtsdatum", "email", "mitgliedsstatus",
        "hund", "wurfdatum",
        "ist_zuechter", "zwingername",
        "iban", "mitglied_seit", "gekuendigt_zum"
    ])
    n = 2000
    mitgliedsnrs = random.sample(range(1, 20000), n)
    for i in range(n):
        writer.writerow(generiere_daten(mitgliedsnrs[i]))
