import csv
import mysql.connector
import os
from datetime import datetime, timedelta
from dotenv import load_dotenv
import requests

load_dotenv()



# ----------------------------
# MySQL-Verbindung
# ----------------------------

conn = mysql.connector.connect(
    host=os.getenv('AUTOMATION_DB_HOST'),
    user=os.getenv('AUTOMATION_USERNAME'),
    password=os.getenv('AUTOMATION_PASSWORD'),
    database=os.getenv('AUTOMATION_DB_NAME')
)
cursor = conn.cursor()

# ----------------------------
# CSV-Datei einlesen
# ----------------------------
csv_file = 'selected_results.csv'

def parse_date(s):
    if(s==None):
        return None
    """Konvertiert DD/MM/YYYY in YYYY-MM-DD, None bei leerem Feld"""
    if s.strip() in ("", "-"):
        return None
    return datetime.strptime(s, "%d/%m/%Y").date()

def parse_int(s):
    try:
        return int(s)
    except:
        return None

def insert_member_data(cursor, conn, row):
    # ignoriere alle mitglieder ohne membership_number
    membership_number = row.get("membership number")
    if membership_number==None or membership_number=="-" or membership_number=="" or membership_number=="0":
        print(f"Datensatz mit membership_number {membership_number} ignorieren")
        return

    # wenn es bereits einen datensatz mit dieser membership_number gibt, ignoriere ihn
    sql = "SELECT firstname, lastname, email FROM members WHERE membership_number = %s"
    cursor.execute(sql, (parse_int(row.get("membership number")),))
    result = cursor.fetchone()
    if result:
        existing_firstname, existing_lastname, existing_email = result
        # wenn es abweichungen (firstname, lastname, email) gibt, melden und aktualisieren
        if existing_firstname != row.get("firstname") or existing_lastname != row.get("lastname") or existing_email != row.get("email"):
            print(f"Datensatz mit membership_number {row.get('membership number')} bereits vorhanden, aber mit abweichungen")
            print(f"  DB: {existing_firstname}, {existing_lastname}, {existing_email}")
            print(f"  CSV: {row.get('firstname')}, {row.get('lastname')}, {row.get('email')}")
            return
        print(f"Datensatz mit membership_number {row.get('membership number')} bereits vorhanden")
        return
    else:
        print(f"Datensatz mit membership_number {row.get('membership number')} nicht vorhanden")

    # wenn date_of_leaving gesetzt ist, meldung und abbruch
    if row.get("date of leaving")!=None:
        print(f"Datensatz mit membership_number {row.get('membership number')} hat date_of_leaving gesetzt, abbruch")
        return

    """Fügt einen Member-Datensatz in die Datenbank ein"""
    sql = """
    INSERT INTO members (
        person_id, access, salutation, title, firstname, lastname, language, street,
        zipcode, city,
        oblast, country, organization, mobile, phone, email, internet,
        type_of_person, is_breeder, is_member,
        is_subscriber, type_of_subscription,
        is_active_breeder, breeding_station, given_name_first, membership_number,
        membership_status, role_in_association, other_roles,
        date_of_birth,
        date_of_death, date_of_joining, date_of_leaving,
        iban, bic
    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
              %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
              %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
              %s, %s, %s, %s, %s)
    """

    values = (
        parse_int(row.get("ID Person")),
        parse_int(row.get("0/1 access")),
        row.get("salutation"),
        row.get("title"),
        row.get("firstname"),
        row.get("lastname"),
        row.get("language"),
        row.get("street"),
        row.get("zipcode"),
        row.get("city"),

        row.get("oblast"),
        row.get("country"),
        row.get("organization"),
        row.get("mobile"),
        row.get("phone"),
        row.get("email"),
        row.get("internet"),
        row.get("type of person"),
        parse_int(row.get("person is a breeder")),
        parse_int(row.get("person is a member")),

        parse_int(row.get("person is a subscriber")),
        row.get("type of subscription"),
        parse_int(row.get("person is an active breeder")),
        row.get("breeding station"),
        row.get("given name first"),
        parse_int(row.get("membership number")),
        row.get("membership status"),
        row.get("role in association"),
        row.get("other roles"),
        parse_date(row.get("date of birth")),

        parse_date(row.get("date of death")),
        parse_date(row.get("date of joining")),
        parse_date(row.get("date of leaving")),
        row.get("IBAN"),
        row.get("Bank Identifier Code (BIC)")
    )

    cursor.execute(sql, values)
    conn.commit()

def ntfy(channel, message, sign):
    # Ziel-URL
    url = f"https://ntfy.emsgmbh-tt-homeoffice.srv64.de/{channel}"

    # Nachricht (du kannst auch f-Strings nutzen, wenn du eine Variable wie count einsetzen willst)
#    count = 3
#    message = f"ems-gitlab Backup Abbruch: Es laufen bereits {count} rsync-Prozesse."

    # Header definieren (wie bei curl: -H "X-Tags: stop_sign")

    headers = {
        "X-Tags": sign
    }

    # POST-Request absenden
    response = requests.post(url, data=message.encode("utf-8"), headers=headers)

def check_for_new_members():
    # suche alle mitglieder, bei denen begruesst_am nicht gesetzt ist und date_of_joining gesetzt ist und mehr als 30 Tage in der Vergangenheit liegt
    sql = "SELECT * FROM members WHERE begruesst_am IS NULL AND date_of_leaving IS NULL AND date_of_joining < %s"
    cursor.execute(sql, (datetime.now() - timedelta(days=30),))
    result = cursor.fetchall()
    for row in result:
        # in einer zeile ausgeben: membership_number, salutation,firstname, lastname, email, street, zipcode, city, date_of_joining
        msg = f"Mitgl. bestätigen: {row[26]}, {row[27]}, {row[3]}, {row[5]}, {row[6]}, {row[7]}, {row[9]}, {row[10]}, {row[11]}, {row[16]}, {row[32]}"
        ntfy("hzd-nord", msg, "ok")

with open(csv_file, newline='', encoding='utf-8') as f:
    reader = csv.DictReader(f, delimiter=',')
    for row in reader:
#        print(row)
        insert_member_data(cursor, conn, row)

check_for_new_members()

cursor.close()

conn.close()

print("CSV-Daten erfolgreich in MySQL importiert!")