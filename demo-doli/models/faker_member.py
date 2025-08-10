from dataclasses import dataclass
from datetime import datetime, date
from typing import Optional

@dataclass
class DoliMember:
    mitgliedsnr: int
    vorname: str
    nachname: str
    straße: str
    hausnummer: str
    plz: str
    ort: str
    geburtsdatum: Optional[date]
    email: str
    mitgliedsstatus: str
    hund: str
    wurfdatum: Optional[date]
    ist_zuechter: bool
    zwingername: str
    iban: str
    mitglied_seit: Optional[date]
    gekuendigt_zum: Optional[date]

    @staticmethod
    def parse_date(date_str: str) -> Optional[date]:
        if not date_str:
            return None
        try:
            return datetime.strptime(date_str, "%Y-%m-%d").date()
        except ValueError:
            return None

    @classmethod
    def from_csv_row(cls, row: dict):
        return cls(
            mitgliedsnr=int(row["mitgliedsnr"]),
            vorname=row["vorname"],
            nachname=row["nachname"],
            straße=row["straße"],
            hausnummer=row["hausnummer"],
            plz=row["plz"],
            ort=row["ort"],
            geburtsdatum=cls.parse_date(row["geburtsdatum"]),
            email=row["email"],
            mitgliedsstatus=row["mitgliedsstatus"],
            hund=row["hund"],
            wurfdatum=cls.parse_date(row["wurfdatum"]),
            ist_zuechter=row["ist_zuechter"].lower() == "true",
            zwingername=row["zwingername"],
            iban=row["iban"],
            mitglied_seit=cls.parse_date(row["mitglied_seit"]),
            gekuendigt_zum=cls.parse_date(row["gekuendigt_zum"]),
        )
