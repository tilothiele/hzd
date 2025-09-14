import csv
import mysql.connector
import os
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

# CREATE TABLE members (
#     id INT PRIMARY KEY AUTO_INCREMENT,
#     person_id INT,
#     access TINYINT(1),
#     salutation VARCHAR(10),
#     title VARCHAR(50),
#     firstname VARCHAR(50),
#     lastname VARCHAR(50),
#     language VARCHAR(20),
#     street VARCHAR(100),
#     zipcode VARCHAR(20),
#     city VARCHAR(50),
#     oblast VARCHAR(50),
#     country VARCHAR(50),
#     organization VARCHAR(100),
#     mobile VARCHAR(50),
#     phone VARCHAR(50),
#     email VARCHAR(100),
#     internet VARCHAR(100),
#     type_of_person VARCHAR(50),
#     is_breeder TINYINT(1),
#     is_member TINYINT(1),
#     is_subscriber TINYINT(1),
#     type_of_subscription VARCHAR(200),
#     is_active_breeder TINYINT(1),
#     breeding_station VARCHAR(100),
#     given_name_first VARCHAR(50),
#     membership_number INT,
#     membership_status VARCHAR(50),
#     role_in_association VARCHAR(50),
#     other_roles VARCHAR(100),
#     date_of_birth DATE,
#     date_of_death DATE,
#     date_of_joining DATE,
#     date_of_leaving DATE,
#     iban VARCHAR(34),
#     bic VARCHAR(12)
# );

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

with open(csv_file, newline='', encoding='utf-8') as f:
    reader = csv.DictReader(f, delimiter=',')
    for row in reader:
        print(row)
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

cursor.close()
conn.close()

print("CSV-Daten erfolgreich in MySQL importiert!")