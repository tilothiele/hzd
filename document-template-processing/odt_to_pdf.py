import uno
import os
from com.sun.star.beans import PropertyValue
from pathlib import Path

uno_host = os.getenv("UNO_HOST", "localhost")
uno_port = os.getenv("UNO_PORT", "2002")

def replace_placeholders(doc, replacements):
    # Zugriff auf alle Textbereiche im Dokument
    text = doc.Text
    cursor = text.createTextCursor()

    for key, value in replacements.items():
        search = doc.createSearchDescriptor()
        search.SearchString = f"${{{key}}}"  # z. B. ${vorname}
        found = doc.findFirst(search)

        while found:
            found.String = value
            found = doc.findNext(found.End, search)

def convert_odt_to_pdf(input_path, output_path, replacements):
    local_context = uno.getComponentContext()
    resolver = local_context.ServiceManager.createInstanceWithContext(
        "com.sun.star.bridge.UnoUrlResolver", local_context
    )
    
    url = f"uno:socket,host={uno_host},port={uno_port};urp;StarOffice.ComponentContext"
    print(url)
    context = resolver.resolve(url)
    
    desktop = context.ServiceManager.createInstanceWithContext(
        "com.sun.star.frame.Desktop", context
    )

    # Datei öffnen
    input_url = Path(input_path).absolute().as_uri()
    output_url = Path(output_path).absolute().as_uri()

    props = (
        PropertyValue(Name="Hidden", Value=True),
    )

    doc = desktop.loadComponentFromURL(input_url, "_blank", 0, props)

    # Platzhalter ersetzen
    replace_placeholders(doc, replacements)

    # Als PDF exportieren
    export_props = (
        PropertyValue(Name="FilterName", Value="writer_pdf_Export"),
    )
    doc.storeToURL(output_url, export_props)

    # Schließen
    doc.close(True)

# Beispielnutzung
if __name__ == "__main__":
    convert_odt_to_pdf(
        "vorlage.odt",
        "output.pdf",
        {
            "vorname": "Max",
            "nachname": "Mustermann",
            "anrede": "Herr"
        }
    )
