import mysql.connector
import os
from mysql.connector import Error
from dotenv import load_dotenv

# .env-Datei laden
load_dotenv(dotenv_path='../.env')

def get_member_by_membership_number(membership_number: int):
    """
    Liefert den Member-Datensatz als Dict anhand der membership_number zurück.
    """
    try:
        conn = mysql.connector.connect(
            host=os.getenv('MYSQL_HOST'),       # anpassen
            port=os.getenv('MYSQL_PORT'),       # anpassen
            user=os.getenv('MYSQL_USER'),       # anpassen
            password=os.getenv('MYSQL_PASSWORD'), # anpassen
            database="automation"
        )

        cursor = conn.cursor(dictionary=True)
        query = """
            SELECT person_id, access, salutation, title, firstname, lastname,
                   language, street, zipcode, city, oblast, country, organization,
                   mobile, phone, email, internet, type_of_person, is_breeder,
                   is_member, is_subscriber, type_of_subscription, is_active_breeder,
                   breeding_station, given_name_first, membership_number, membership_status,
                   role_in_association, other_roles, date_of_birth, date_of_death,
                   date_of_joining, date_of_leaving, iban, bic, begruesst_am
            FROM members
            WHERE membership_number = %s
        """
        cursor.execute(query, (membership_number,))
        result = cursor.fetchone()
        return result

    except Error as e:
        print(f"Fehler: {e}")
        return None
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


