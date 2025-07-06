# models/DolibarrMember.py

from dataclasses import dataclass
from typing import Optional, Dict, Any, List
from dotenv import load_dotenv

# .env-Datei laden
load_dotenv(dotenv_path='../.env')

@dataclass
class DolibarrMember:
    id: str
    entity: str
    ref: str
    statut: str
    status: str
    country_code: str
    state_id: str
    note_public: Optional[str]
    note_private: Optional[str]
    lastname: Optional[str]
    firstname: Optional[str]
    date_creation: Optional[int]
    date_validation: Optional[int]
    date_modification: Optional[int]
    email: Optional[str]
    phone_mobile: Optional[str]
    gender: Optional[str]
    type: Optional[str]
    user_login: Optional[str]
    address: Optional[str]
    zip: Optional[str]
    town: Optional[str]
    photo: Optional[str]
    fk_soc: Optional[str]
    typeid: Optional[str]
    mitgliedsnr: Optional[str]

    @classmethod
    def from_json(cls, data: Dict[str, Any]) -> "DolibarrMember":
        return cls(
            id=data.get("id"),
            entity=data.get("entity"),
            ref=data.get("ref"),
            statut=data.get("statut"),
            status=data.get("status"),
            country_code=data.get("country_code"),
            state_id=data.get("state_id"),
            note_public=data.get("note_public"),
            note_private=data.get("note_private"),
            lastname=data.get("lastname"),
            firstname=data.get("firstname"),
            date_creation=data.get("date_creation"),
            date_validation=data.get("date_validation"),
            date_modification=data.get("date_modification"),
            email=data.get("email"),
            phone_mobile=data.get("phone_mobile"),
            gender=data.get("gender"),
            type=data.get("type"),
            user_login=data.get("user_login"),
            address=data.get("address"),
            zip=data.get("zip"),
            town=data.get("town"),
            photo=data.get("photo"),
            typeid=data.get("typeid"),
            fk_soc=data.get("fk_soc"),
            mitgliedsnr=optional_str(data.get("array_options"), "options_mitgliedsnummer")
        )

def optional_str(dict, name):
    if dict==None:
        return None
    return dict.get(name)

class BankAccount:
    def __init__(self, id, label, bank, bic, iban, socid, datec, default_rib, rum, frstrecur, datem):
        self.id = id
        self.label = label
        self.bank = bank
        self.bic = bic
        self.iban = iban
        self.socid = socid
        self.datec = datec
        self.default_rib = default_rib
        self.rum = rum
        self.frstrecur = frstrecur
        self.datem = datem

    @classmethod
    def from_json(cls, json_data):
        return cls(
            json_data["id"],
            json_data["label"],
            json_data["bank"],
            json_data["bic"],
            json_data["iban"],
            json_data["socid"],
            json_data["datec"],
            json_data["default_rib"],
            json_data["rum"],
            json_data["frstrecur"],
            json_data["datem"]
        )

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

def find_by_name(firstname, lastname):

    return None