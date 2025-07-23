from lxml import etree

# Lade das XML-Dokument
with open('hzd-og-hh-mitgliedsbeitraege-2025.xml', 'rb') as xml_file:
    xml_doc = etree.parse(xml_file)

# Lade das XSD-Schema
with open('pain.008.001.08.xsd', 'rb') as xsd_file:
    xmlschema_doc = etree.parse(xsd_file)
    xmlschema = etree.XMLSchema(xmlschema_doc)

# Validierung
if xmlschema.validate(xml_doc):
    print("✅ Das XML-Dokument ist gültig.")
else:
    print("❌ Fehler bei der Validierung:")
    for error in xmlschema.error_log:
        print(error.message)
