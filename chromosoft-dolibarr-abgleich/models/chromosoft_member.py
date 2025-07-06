from dataclasses import dataclass
import csv
from typing import Optional, List

@dataclass
class ChromosoftMember:
    id_person: int
    access: int
    salutation: str
    title: str
    firstname: str
    lastname: str
    language: str
    street: str
    zipcode: str
    city: str
    oblast: str
    country: str
    organization: str
    mobile: str
    phone: str
    email: str
    internet: str
    email_allowed: str
    is_breeder: int
    is_member: int
    is_subscriber: int
    subscription_type: str
    is_active_breeder: int
    breeding_station: str
    given_name_first: int
    membership_number: str
    membership_status: str
    role_in_association: str
    other_roles: str
    date_of_birth: str
    date_of_death: str
    date_of_joining: str
    date_of_leaving: str
    iban: str
    bic: str

def parse_csv(file_path: str) -> List[ChromosoftMember]:
    persons = []

    with open(file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            person = ChromosoftMember(
                id_person=int(row['ID Person']),
                access=int(row['0/1 access']),
                salutation=row['salutation'],
                title=row['title'],
                firstname=row['firstname'],
                lastname=row['lastname'],
                language=row['language'],
                street=row['street'],
                zipcode=row['zipcode'],
                city=row['city'],
                oblast=row['oblast'],
                country=row['country'],
                organization=row['organization'],
                mobile=row['mobile'],
                phone=row['phone'],
                email=row['email'],
                internet=row['internet'],
                email_allowed=row['type of person'],
                is_breeder=int(row['person is a breeder']),
                is_member=int(row['person is a member']),
                is_subscriber=int(row['person is a subscriber']),
                subscription_type=row['type of subscription'],
                is_active_breeder=int(row['person is an active breeder']),
                breeding_station=row['breeding station'],
                given_name_first=int(row['given name first']),
                membership_number=row['membership number'],
                membership_status=row['membership status'],
                role_in_association=row['role in association'],
                other_roles=row['other roles'],
                date_of_birth=row['date of birth'],
                date_of_death=row['date of death'],
                date_of_joining=row['date of joining'],
                date_of_leaving=row['date of leaving'],
                iban=row['IBAN'],
                bic=row['Bank Identifier Code (BIC)']
            )
            persons.append(person)

    return persons