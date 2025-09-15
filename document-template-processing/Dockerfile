# Base Image: Debian oder Ubuntu, damit UNO / LibreOffice gut funktioniert
FROM ubuntu:24.04

# Grundlegende Pakete
RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y \
    libreoffice-core libreoffice-writer libreoffice-calc \
    python3 python3-pip python3-uno \
#    uno-libs3 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Arbeitsverzeichnis
WORKDIR /app

# Abhängigkeiten für dein Python‑Projekt
COPY requirements.txt .

# Hier unotools hinzufügen
# requirements.txt sollte mindestens enthalten: unotools
RUN pip3 install --no-cache-dir -r requirements.txt

# Dein Skript kopieren
COPY . .

# Option: puerto / Kommando
CMD ["python3", "odt_to_pdf.py"]
