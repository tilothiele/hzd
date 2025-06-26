
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