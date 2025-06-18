import uno
from dotenv import load_dotenv
import os

load_dotenv()

localContext = uno.getComponentContext()
resolver = localContext.ServiceManager.createInstanceWithContext(
    "com.sun.star.bridge.UnoUrlResolver", localContext)
context = resolver.resolve("uno:socket,host=localhost,port=2002;urp;StarOffice.ComponentContext")

desktop = context.ServiceManager.createInstanceWithContext("com.sun.star.frame.Desktop", context)
document = desktop.loadComponentFromURL("file:///pfad/zur/briefvorlage.odt", "_blank", 0, ())

# Zugriff auf den Text
text = document.Text
cursor = text.createTextCursor()

# Beispiel: Direkt schreiben
text.insertString(cursor, "Sehr geehrter Herr Mustermann", 0)

# Speichern
document.storeToURL("file:///pfad/zur/brief_fertig.odt", ())
document.close(True)
