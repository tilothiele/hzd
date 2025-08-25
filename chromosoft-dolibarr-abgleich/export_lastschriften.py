from models.dolibarr_member import DolibarrMember,mussZahlen
from models.dolibarr_actions import find_by_soc, find_all, per_lastschrift, create_subscription, get_subscriptions
import datetime
import uuid
import os
import xml.etree.ElementTree as ET
from dotenv import load_dotenv

# -----------------------------------------------------------------
# Hold alle aktiven Mitglieder von Dolibarr
# Filtert alle raus, die nicht zahlen (müssen)
# Schreibt auf stdout die Lastschriftdatensätze als csv
# Erstellt eine Lastschrift-XML (SEPA)
# Verlängert die Mitgliedschaft -> Erstellt einen neuen Eintrag mit dem Betrag und vom 1.1. bis 31.12.
# -----------------------------------------------------------------

def dolibarrKey(m: DolibarrMember):
    return m.firstname + " " + m.lastname

# Ermittelt den Jahresbeitrag
def typeid2Beitrag(typeid) -> float:
    if typeid=="1":
        return 138
#        return "OG-Mitglied"
    if typeid=="2":
        return 16
#        return "OG-Familienmitglied"
    if typeid=="3":
        return 35
#        return "HZD-Vollmitglied"
    if typeid=="4":
        return 16
#        return "HZD-Familienmitglied"
    if typeid=="5":
        return 0
#        return "Kurzmitglied"
    raise

# Wird eine Verlängerung benötigt?
# Ja, falls es keine Subscription gibt, deren Endzeitpunkt in der Zukunft liegt
def need_subscription(m: DolibarrMember) -> bool:
    subscriptions = get_subscriptions(m)
    for s in subscriptions:
        bis = s.datef
        n = int(datetime.datetime.now().timestamp())
        if bis > n:
            return False
    return True

def dolibarrKey(m: DolibarrMember):
    return m.firstname + " " + m.lastname

if __name__ == '__main__':

    dolibarr_liste = find_all()
    dolibarr_liste_sorted = sorted(dolibarr_liste, key=lambda p: (p.lastname.lower(), p.firstname.lower()))

    xml_file = "sepa-lastschriften.xml"

    # .env-Datei laden
    load_dotenv()

    API_KEY = os.getenv('API_KEY')

    # Creditor-Informationen
    CREDITOR_NAME = os.getenv('CREDITOR_NAME')
    CREDITOR_IBAN = os.getenv('CREDITOR_IBAN')
    CREDITOR_BIC = os.getenv('CREDITOR_BIC')
    CREDITOR_ID = os.getenv('CREDITOR_ID')
    SEPA_SEQUENCE = "OOFF"  # Einmalig: OOFF, Wiederholung: RCUR

    # Register Namespaces
    ET.register_namespace('', 'urn:iso:std:iso:20022:tech:xsd:pain.008.001.08')
    ET.register_namespace('xsi', 'http://www.w3.org/2001/XMLSchema-instance')

    # Namespaces
    ns = {
        '': 'urn:iso:std:iso:20022:tech:xsd:pain.008.001.08',
        'xsi': 'http://www.w3.org/2001/XMLSchema-instance'
    }

    # Create root element with required attributes
    attrib = {
        '{http://www.w3.org/2001/XMLSchema-instance}schemaLocation':
            'urn:iso:std:iso:20022:tech:xsd:pain.008.001.08 pain.008.001.08.xsd'
    }
    document = ET.Element('{urn:iso:std:iso:20022:tech:xsd:pain.008.001.08}Document', attrib)

    cstmr_drct_db_initn = ET.SubElement(document, "CstmrDrctDbtInitn")

    # Gruppenübersicht
    grp_hdr = ET.SubElement(cstmr_drct_db_initn, "GrpHdr")
    ET.SubElement(grp_hdr, "MsgId").text = str(uuid.uuid4().hex)
    ET.SubElement(grp_hdr, "CreDtTm").text = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"
    ET.SubElement(grp_hdr, "NbOfTxs").text = "0"  # wird später ersetzt
    ET.SubElement(grp_hdr, "CtrlSum").text = "0.00"  # wird später ersetzt
    initg_pty = ET.SubElement(grp_hdr, "InitgPty")
    ET.SubElement(initg_pty, "Nm").text = CREDITOR_NAME

    # Payment-Informationen
    pmt_inf = ET.SubElement(cstmr_drct_db_initn, "PmtInf")


    # Namespaces
    ns = {
        '': 'urn:iso:std:iso:20022:tech:xsd:pain.008.001.08',
        'xsi': 'http://www.w3.org/2001/XMLSchema-instance'
    }

    # Create root element with required attributes
    attrib = {
        '{http://www.w3.org/2001/XMLSchema-instance}schemaLocation':
            'urn:iso:std:iso:20022:tech:xsd:pain.008.001.08 pain.008.001.08.xsd'
    }
    document = ET.Element('{urn:iso:std:iso:20022:tech:xsd:pain.008.001.08}Document', attrib)

    cstmr_drct_db_initn = ET.SubElement(document, "CstmrDrctDbtInitn")

    # Gruppenübersicht
    grp_hdr = ET.SubElement(cstmr_drct_db_initn, "GrpHdr")
    ET.SubElement(grp_hdr, "MsgId").text = str(uuid.uuid4().hex)
    ET.SubElement(grp_hdr, "CreDtTm").text = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"
    ET.SubElement(grp_hdr, "NbOfTxs").text = "0"  # wird später ersetzt
    ET.SubElement(grp_hdr, "CtrlSum").text = "0.00"  # wird später ersetzt
    initg_pty = ET.SubElement(grp_hdr, "InitgPty")
    ET.SubElement(initg_pty, "Nm").text = CREDITOR_NAME

    # Payment-Informationen
    pmt_inf = ET.SubElement(cstmr_drct_db_initn, "PmtInf")
    ET.SubElement(pmt_inf, "PmtInfId").text = str(uuid.uuid4().hex)
    ET.SubElement(pmt_inf, "PmtMtd").text = "DD"
    ET.SubElement(pmt_inf, "BtchBookg").text = "true"
    ET.SubElement(pmt_inf, "NbOfTxs").text = "0"  # später ersetzen
    ET.SubElement(pmt_inf, "CtrlSum").text = "0.00"  # später ersetzen

    pmt_tp_inf = ET.SubElement(pmt_inf, "PmtTpInf")
    svc_lvl = ET.SubElement(pmt_tp_inf, "SvcLvl")
    ET.SubElement(svc_lvl, "Cd").text = "SEPA"
    lcl_instrm = ET.SubElement(pmt_tp_inf, "LclInstrm")
    ET.SubElement(lcl_instrm, "Cd").text = "CORE"
    ET.SubElement(pmt_tp_inf, "SeqTp").text = SEPA_SEQUENCE

    ET.SubElement(pmt_inf, "ReqdColltnDt").text = (datetime.datetime.now() + datetime.timedelta(days=2)).date().isoformat()

    cdtr = ET.SubElement(pmt_inf, "Cdtr")
    ET.SubElement(cdtr, "Nm").text = CREDITOR_NAME
    cdtr_acct = ET.SubElement(pmt_inf, "CdtrAcct")
    id_acct = ET.SubElement(cdtr_acct, "Id")
    ET.SubElement(id_acct, "IBAN").text = CREDITOR_IBAN
    cdtr_agt = ET.SubElement(pmt_inf, "CdtrAgt")
    fin_instn_id = ET.SubElement(cdtr_agt, "FinInstnId")
    ET.SubElement(fin_instn_id, "BICFI").text = CREDITOR_BIC
    cdtr_schme_id = ET.SubElement(pmt_inf, "CdtrSchmeId")
    prt = ET.SubElement(cdtr_schme_id, "Id")
    org_id = ET.SubElement(prt, "PrvtId")
    othr = ET.SubElement(org_id, "Othr")
    ET.SubElement(othr, "Id").text = CREDITOR_ID
    schme_nm = ET.SubElement(othr, "SchmeNm")
    ET.SubElement(schme_nm, "Prtry").text = "SEPA"

    # CSV verarbeiten
    tx_count = 0
    tx_total = 0.00

    n = 0
    buchungstext = "HZD OG-Hamburg Mitgliedsbeitrag "+datetime.datetime.now().strftime("%Y")
    print("iban,betrag,kontoinhaber,mandat_vom,buchungstext,Mandatsreferenz")
    for p in dolibarr_liste_sorted:
        name = p.firstname+" "+p.lastname
        if not mussZahlen(p):
            print(f"{name} muss nicht zahlen")
            continue
        if not per_lastschrift(p):
            print(f"{name} zahlt nicht per Lastschrift")
            continue
        if not need_subscription(p):
            print(f"{name} hat offenbar (noch) eine gültige Mitgliedschaft")
            continue
        bank_account = None
        if p.fk_soc:
            bank_accounts = find_by_soc(p.fk_soc)
            if(bank_accounts and len(bank_accounts)>0):
                bank_account = bank_accounts[0]
        if bank_account == None:
            print(f"{name} hat kein Bankkonto")
            continue
        kontoinhaber = bank_account.proprio
        b = typeid2Beitrag(p.typeid)
        dr = datetime.datetime.fromtimestamp(bank_account.date_rum)
        bt = buchungstext+" "+p.type+" "+name

        print(f"Ziehe {b} Euro für {name} vom Konto {bank_account.iban} ({bank_account.proprio}) ein.")
        #print(bank_account.iban+","+str(b)+","+bank_account.proprio+","+dr.strftime("%d.%m.%Y")+","+bt+","+bank_account.rum)

        amount = float(b)
        tx_total += amount
        tx_count += 1

        drct_dbt_tx_inf = ET.SubElement(pmt_inf, "DrctDbtTxInf")

        pmt_id = ET.SubElement(drct_dbt_tx_inf, "PmtId")
        ET.SubElement(pmt_id, "EndToEndId").text = "NOTPROVIDED"

        instd_amt = ET.SubElement(drct_dbt_tx_inf, "InstdAmt", Ccy="EUR")
        instd_amt.text = f"{amount:.2f}"

        drct_dbt_tx = ET.SubElement(drct_dbt_tx_inf, "DrctDbtTx")
        mndt_rltd_inf = ET.SubElement(drct_dbt_tx, "MndtRltdInf")
        ET.SubElement(mndt_rltd_inf, "MndtId").text = bank_account.rum
        ET.SubElement(mndt_rltd_inf, "DtOfSgntr").text = dr.strftime("%Y-%m-%d")
        # ET.SubElement(mndt_rltd_inf, "AmdmntInd").text = "false"

        dbtr_agt = ET.SubElement(drct_dbt_tx_inf, "DbtrAgt")
        fin_instn_id = ET.SubElement(dbtr_agt, "FinInstnId")
        othr = ET.SubElement(fin_instn_id, "Othr")
        ET.SubElement(othr, "Id").text = "NOTPROVIDED"

        dbtr = ET.SubElement(drct_dbt_tx_inf, "Dbtr")
        ET.SubElement(dbtr, "Nm").text = bank_account.proprio

        dbtr_acct = ET.SubElement(drct_dbt_tx_inf, "DbtrAcct")
        id_acct = ET.SubElement(dbtr_acct, "Id")
        ET.SubElement(id_acct, "IBAN").text = bank_account.iban

        rmt_inf = ET.SubElement(drct_dbt_tx_inf, "RmtInf")
        bt1 = bt[:137] if len(bt) > 140 else bt
        if(len(bt)!=len(bt1)):
            print("gekürzt "+bt1)
        ET.SubElement(rmt_inf, "Ustrd").text = bt1

        create_subscription(p, b, datetime.datetime.now().year)

    # Gruppensummen nachtragen
    grp_hdr.find("NbOfTxs").text = str(tx_count)
    grp_hdr.find("CtrlSum").text = f"{tx_total:.2f}"
    pmt_inf.find("NbOfTxs").text = str(tx_count)
    pmt_inf.find("CtrlSum").text = f"{tx_total:.2f}"

    # XML speichern
    tree = ET.ElementTree(document)
    tree.write(xml_file, encoding="utf-8", xml_declaration=True)
    print(f"SEPA-XML-Datei erzeugt: {xml_file}")





