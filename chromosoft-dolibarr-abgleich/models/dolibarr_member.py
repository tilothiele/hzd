# models/DolibarrMember.py

from dataclasses import dataclass
from typing import Optional, Dict, Any, List
from dotenv import load_dotenv

# .env-Datei laden
load_dotenv(dotenv_path='../.env')

@dataclass
class Subscription:
    id: str
    datef: Optional[int]
    dateh: Optional[int]
    fk_type: Optional[str]
    fk_adherent: Optional[str]
    amount: float
    note_public: str

    @classmethod
    def from_json(cls, data: Dict[str, Any]) -> "Subscription":
        return cls(
            id=data.get("id"),
            datef=int(data["datef"]) if data.get("datef") else None,
            dateh=int(data["dateh"]) if data.get("dateh") else None,
            fk_type=data.get("fk_type"),
            fk_adherent=data.get("fk_adherent"),
            amount=float(data.get("amount", 0)),
            note_public=data.get("note_public", "")
        )

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

def mussZahlen(p: DolibarrMember) -> bool:
    if(p.typeid=='6'):
        return False
    if(not p.statut=='1'):
        return False
    return True

def optional_str(dict, name):
    if dict==None:
        return None
    return dict.get(name)

class Category:
    def __init__(
        self,
        id: str,
        fk_parent: int,
        label: str,
        description: str,
        color: str,
        position: str,
        socid: int,
        ref_ext: Optional[str],
        visible: int,
        type_: str,
        entity: int,
        array_options: List[Any],
    ):
        self.id = id
        self.fk_parent = fk_parent
        self.label = label
        self.description = description
        self.color = color
        self.position = position
        self.socid = socid
        self.ref_ext = ref_ext
        self.visible = visible
        self.type = type_
        self.entity = entity
        self.array_options = array_options

    def __repr__(self):
        return f"Category(id={self.id}, label='{self.label}', type={self.type})"

    @classmethod
    def from_json(cls, data: Dict[str, Any]) -> "Category":
        """
        Erzeugt eine Category-Instanz aus einem JSON-String oder einem dict.
        """
        if isinstance(data, str):
            data = json.loads(data)
        return cls(
            id=data.get("id"),
            fk_parent=data.get("fk_parent"),
            label=data.get("label"),
            description=data.get("description", ""),
            color=data.get("color", ""),
            position=data.get("position"),
            socid=data.get("socid"),
            ref_ext=data.get("ref_ext"),
            visible=data.get("visible"),
            type_=data.get("type"),
            entity=data.get("entity"),
            array_options=data.get("array_options", []),
        )

class BankAccount:
    def __init__(self, id, label, bank, bic, iban, socid, datec, default_rib, rum, frstrecur, datem, proprio, date_rum):
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
        self.proprio = proprio
        self.date_rum = date_rum

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
            json_data["datem"],
            json_data["proprio"],
            json_data["date_rum"]
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


