import pandas as pd
from dotenv import load_dotenv
import os

load_dotenv()

#
# gibt eine Liste der Mitglieder aus.
# die neuesten Mitglieder stehen oben.
#

input = os.getenv("MITGLIEDERLISTE_INPUT")
# CSV einlesen (achte auf Encoding & Header ab zweiter Zeile)
df = pd.read_csv(input, skipinitialspace=True)

# Datum korrekt interpretieren (z. B. '23/02/1964' als dd/mm/yyyy)
df["date of joining"] = pd.to_datetime(df["date of joining"], format="%d/%m/%Y", errors="coerce")

# Nur die gewünschten Spalten auswählen
spalten = [
    "salutation",
    "firstname",
    "lastname",
    "street",
    "zipcode",
    "city",
    "email",
    "membership number",
    "membership status",
    "date of joining"
]
df_filtered = df[spalten]

# Sortieren nach Beitrittsdatum, absteigend
df_sorted = df_filtered.sort_values(by="date of joining", ascending=False)

# Nur die 30 neuesten Einträge
df_top10 = df_sorted.head(30)

# Ergebnis in neue CSV-Datei schreiben
df_top10.to_csv("ausgabe.csv", index=False)

# Markdown-Tabelle generieren
markdown_output = df_top10.to_markdown(index=False)

# In Datei schreiben
with open("ausgabe.md", "w", encoding="utf-8") as f:
    f.write(markdown_output)
