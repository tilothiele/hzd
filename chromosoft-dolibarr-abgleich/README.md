
curl https://hzd-og-hh-test.swingdog.home64.de/api/index.php/members \
  -H 'DOLAPIKEY: b0i2xHD4eeSjdQ2nRf03N1QaLQX3He74' \
  -H 'Accept: application/json'

I. prüfen und ggf anlegen:

für alle chomosoft/rg-mitglieder:
  wenn es ein dolibarr mitglied gibt:
    wenn der Mitgliedschaftstyp nicht passt:
        Meldung ausgeben
  sonst:
    mitglied in dolibarr anlegen.
    - name, vorname, straße, hausnr, plz, ort, mobil, fn, email, date of birth,
      mitgliedsnr, mitgliedstyp, date of joining, date of leaving, IBAN, BIC
    geschäftspartner mit bankverbindung anlegen.

II. aktualisieren:

für alle chomosoft/rg-mitglieder:
  wenn es ein dolibarr mitglied gibt:
    stimmt der Mitgliedschaftstyp
    aktualisiere die Kontoverbindung
    setze de
  sonst:

dolibarr - typeid
1 - og mitglied
2 - og familienmitglied
3 - hzd vollmitglied
4 - hzd familienmitglied
5 - kurzmitglied

chromosoft - membership status:
Mitglied
Familienmitglied

## prompt

ich habe dolibar installiert. ich möchte unsere vereinsmitglieder und die Beitragszahlungen verwalten. ich habe die module mitglieder, banken/kasse, buchhaltung, geschäftspartner, rechnungen aktiviert. in der buchhaltung ist der skr49 eingerichtet. am 30.6.2025 sind die mitgliedsbeiträge fällig. wie gehe ich vor?

## Konfig

Testdaten:
Gläubiger-ID: DE98ZZZ09999999999
IBAN: GB33BUKB20201555555555

## Daten einspielen

* process_dolibarr_members.py
* process_lastschriften_2024.py

## scratch

{
    "module": null,
    "id": "106",
    "entity": "1",
    "import_key": null,
    "array_options": {
        "options_hundename": "Benji",
        "options_hunderufname": null,
        "options_zwingername": "von den Fröruper Bergen",
        "options_wurfdatum": 1544400000,
        "options_mitglied_seit": 1550966400,
        "options_mitgliedschaft_beginn": "",
        "options_gekundigt_zum": "",
        "options_mitgliedsnummer": null
    },
    "array_languages": null,
    "contacts_ids": null,
    "linkedObjectsIds": null,
    "canvas": null,
    "fk_project": null,
    "contact_id": null,
    "user": null,
    "origin_type": null,
    "origin_id": null,
    "ref": "106",
    "ref_ext": null,
    "statut": "1",
    "status": "1",
    "country_id": "5",
    "country_code": "DE",
    "state_id": null,
    "region_id": null,
    "barcode_type": null,
    "barcode_type_coder": null,
    "mode_reglement_id": null,
    "cond_reglement_id": null,
    "demand_reason_id": null,
    "transport_mode_id": null,
    "shipping_method": null,
    "fk_multicurrency": null,
    "multicurrency_code": null,
    "multicurrency_tx": null,
    "multicurrency_total_ht": null,
    "multicurrency_total_tva": null,
    "multicurrency_total_ttc": null,
    "multicurrency_total_localtax1": null,
    "multicurrency_total_localtax2": null,
    "last_main_doc": null,
    "fk_account": null,
    "note_public": null,
    "note_private": null,
    "lines": null,
    "actiontypecode": null,
    "name": null,
    "lastname": "Ochs",
    "firstname": "Sabine",
    "civility_id": null,
    "date_creation": 1740865015,
    "date_validation": 1742762507,
    "date_modification": 1742762618,
    "tms": null,
    "date_cloture": null,
    "user_author": null,
    "user_creation": null,
    "user_creation_id": null,
    "user_valid": null,
    "user_validation": null,
    "user_validation_id": null,
    "user_closing_id": null,
    "user_modification": null,
    "user_modification_id": null,
    "fk_user_creat": null,
    "fk_user_modif": null,
    "specimen": 0,
    "totalpaid": null,
    "extraparams": [],
    "product": null,
    "cond_reglement_supplier_id": null,
    "deposit_percent": null,
    "retained_warranty_fk_cond_reglement": null,
    "warehouse_id": null,
    "mesgs": null,
    "login": null,
    "pass_indatabase_crypted": null,
    "fullname": null,
    "civility_code": null,
    "civility": "",
    "societe": null,
    "company": null,
    "fk_soc": null,
    "socid": null,
    "socialnetworks": [],
    "phone": null,
    "phone_perso": null,
    "phone_pro": null,
    "phone_mobile": null,
    "fax": null,
    "poste": null,
    "morphy": "phy",
    "public": "0",
    "default_lang": null,
    "photo": null,
    "datec": 1740865015,
    "datem": 1742762618,
    "datevalid": 1742762507,
    "gender": null,
    "birth": "",
    "typeid": "3",
    "type": "HZD-Vollmitglied",
    "need_subscription": "1",
    "user_id": null,
    "user_login": null,
    "datefin": "",
    "first_subscription_date": null,
    "first_subscription_date_start": null,
    "first_subscription_date_end": null,
    "first_subscription_amount": null,
    "last_subscription_date": null,
    "last_subscription_date_start": null,
    "last_subscription_date_end": null,
    "last_subscription_amount": null,
    "ip": null,
    "partnerships": [],
    "invoice": null,
    "address": null,
    "zip": null,
    "town": null,
    "email": "amochs@web.de",
    "url": null
}