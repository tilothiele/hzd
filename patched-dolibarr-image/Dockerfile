# ARG vor dem FROM definieren
ARG BASE_TAG=21.0.1
FROM dolibarr/dolibarr:${BASE_TAG}

# Kopiere die gepatchten Dateien an die richtige Stelle im Container
COPY ./api_members.class.php /var/www/html/adherents/class/api_members.class.php
COPY ./api_thirdparties.class.php /var/www/html/societe/class/api_thirdparties.class.php

