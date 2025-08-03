import csv
import uuid
import os
from datetime import datetime, timedelta
import xml.etree.ElementTree as ET
from dotenv import load_dotenv

# ----------------------------------------------------------
# Generiert die Datei hzd-og-hh-mitgliedsbeitraege-2025.xml mit Lastschriften
# aus der Datei hzd-og-hh-mitgliedsbeitraege-2025.csv
# ----------------------------------------------------------

# .env-Datei laden
load_dotenv()

API_KEY = os.getenv('API_KEY')

# Eingabedatei (CSV)
fname = "hzd-og-hh-mitgliedsbeitraege-2025-1"
csv_file = fname+".csv"

# Ausgabedatei (XML)
xml_file = fname+".xml"

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
ET.SubElement(grp_hdr, "CreDtTm").text = datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"
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

ET.SubElement(pmt_inf, "ReqdColltnDt").text = (datetime.now() + timedelta(days=2)).date().isoformat()

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
with open(csv_file, newline='', encoding="utf-8") as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:

#        iban,betrag,kontoinhaber,buchungstext
        n = n+1
        print("record "+str(n))

        b = row["betrag"]
        if(b==None):
            break
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
        ET.SubElement(mndt_rltd_inf, "MndtId").text = "HZD-OG-HH-"+row["Mandatsreferenz"]
        mv = datetime.strptime(row["mandat_vom"], "%d.%m.%Y")
        ET.SubElement(mndt_rltd_inf, "DtOfSgntr").text = mv.strftime("%Y-%m-%d")
        # ET.SubElement(mndt_rltd_inf, "AmdmntInd").text = "false"

        dbtr_agt = ET.SubElement(drct_dbt_tx_inf, "DbtrAgt")
        fin_instn_id = ET.SubElement(dbtr_agt, "FinInstnId")
        othr = ET.SubElement(fin_instn_id, "Othr")
        ET.SubElement(othr, "Id").text = "NOTPROVIDED"

        dbtr = ET.SubElement(drct_dbt_tx_inf, "Dbtr")
        ET.SubElement(dbtr, "Nm").text = row["kontoinhaber"]

        dbtr_acct = ET.SubElement(drct_dbt_tx_inf, "DbtrAcct")
        id_acct = ET.SubElement(dbtr_acct, "Id")
        ET.SubElement(id_acct, "IBAN").text = row["iban"]

        rmt_inf = ET.SubElement(drct_dbt_tx_inf, "RmtInf")
        bt = row["buchungstext"]
        bt1 = bt[:137] if len(bt) > 140 else bt
        if(len(bt)!=len(bt1)):
            print("gekürzt "+bt1)
        ET.SubElement(rmt_inf, "Ustrd").text = bt1

# Gruppensummen nachtragen
grp_hdr.find("NbOfTxs").text = str(tx_count)
grp_hdr.find("CtrlSum").text = f"{tx_total:.2f}"
pmt_inf.find("NbOfTxs").text = str(tx_count)
pmt_inf.find("CtrlSum").text = f"{tx_total:.2f}"

# XML speichern
tree = ET.ElementTree(document)
tree.write(xml_file, encoding="utf-8", xml_declaration=True)
print(f"SEPA-XML-Datei erzeugt: {xml_file}")
