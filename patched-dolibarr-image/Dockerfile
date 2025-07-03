# ARG vor dem FROM definieren
ARG BASE_TAG=21.0.1
FROM dolibarr/dolibarr:${BASE_TAG}

# Kopiere die gepatchte Datei an die richtige Stelle im Container
COPY ./api_members.class.php /var/www/html/adherents/class/api_members.class.php
