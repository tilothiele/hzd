from models.chromosoft_member import parse_csv
from models.dolibarr_actions import find_by_name

if __name__ == '__main__':
    path_to_csv = 'chromosoft-export-20250621.csv'  # Pfad zur Datei anpassen
    personen_liste = parse_csv(path_to_csv)
    for p in personen_liste:
        dolibarr_member = find_by_name(p.firstname, p.lastname)
        if dolibarr_member:
            print(dolibarr_member)
        else:
            print(p)
