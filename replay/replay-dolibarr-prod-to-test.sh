#!/bin/bash
set -e

source ../.env

#################################
# Konfiguration: Docker-Volumes
#################################
# Name des Docker-Volumes, in dem Dolibarr seine Dateien speichert
PROD_VOLUMES=("hzd-og-hh-documents" "hzd-og-hh-custom")
TEST_VOLUMES=("hzd-og-hh-documents-test" "hzd-og-hh-custom-test")

#################################
# Zeitstempel und Dump-Datei
#################################
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
DUMP_FILE="/tmp/dolibarr_prod_dump_$TIMESTAMP.sql"

#################################
# Funktion: Volume kopieren
#################################
copy_volume() {
  local src_volume="$1"
  local dst_volume="$2"

  echo "📁 Kopiere Volume: $src_volume → $dst_volume ..."
  docker run --rm \
    -v "$src_volume":/from \
    -v "$dst_volume":/to \
    alpine sh -c "cd /from && cp -a . /to"
  echo "✅ Volume $src_volume → $dst_volume kopiert."
}

# Funktion zum Setzen einer Konstante
set_conf_value() {
  local name="$1"
  local value="$2"
  echo "INSERT INTO llx_const (name, value) VALUES ('$name', '$value') ON DUPLICATE KEY UPDATE value = '$value';"| mysql -h $TEST_DB_HOST -u $DB_USER -p$DB_PASS -D $TEST_DB_NAME
}

#################################
# Start: Container stoppen
#################################
echo "=========================================================="
echo "🛑 Stoppe Container $PROD_CONTAINER und $TEST_CONTAINER ..."
docker stop "$PROD_CONTAINER" || echo "(nicht laufend)"
docker stop "$TEST_CONTAINER" || echo "(nicht laufend)"

echo "=========================================================="
echo "📦 1. Erstelle Datenbank-Dump von PROD (Remote: $PROD_DB_HOST) ..."
mysqldump -h "$PROD_DB_HOST" -u "$DB_USER" -p"$DB_PASS" "$PROD_DB_NAME" > "$DUMP_FILE"
echo "Dump erstellt: $DUMP_FILE"

echo "=========================================================="
echo "🧹 2. Lösche vorhandene TEST-Datenbank (Remote: $TEST_DB_HOST) und erstelle sie neu ..."
mysql -h "$TEST_DB_HOST" -u "$DB_USER" -p"$DB_PASS" -e "DROP DATABASE IF EXISTS \`$TEST_DB_NAME\`; CREATE DATABASE \`$TEST_DB_NAME\`;"
echo "TEST-Datenbank neu erstellt: $TEST_DB_NAME"

echo "=========================================================="
echo "🔄 3. Importiere Dump in TEST-Datenbank (Remote: $TEST_DB_HOST) ..."
mysql -h "$TEST_DB_HOST" -u "$DB_USER" -p"$DB_PASS" "$TEST_DB_NAME" < "$DUMP_FILE"
echo "Datenbankimport abgeschlossen."

echo "=========================================================="
echo "📁 4. Kopiere alle Volumes von PROD nach TEST ..."
for i in "${!PROD_VOLUMES[@]}"; do
  copy_volume "${PROD_VOLUMES[$i]}" "${TEST_VOLUMES[$i]}"
done
set_conf_value "MAIN_MAIL_SMTP_SERVER" "mailhog.tt-homeoffice.lan"
set_conf_value "MAIN_MAIL_SMTPS_AUTH_TYPE" "NONE"
set_conf_value "MAIN_MAIL_EMAIL_TLS" "0"
set_conf_value "THEME_ELDY_TOPMENU_BACK1" "191,95,0"

#################################
# Container wieder starten
#################################
echo "=========================================================="
echo "🚀 Starte Container $PROD_CONTAINER und $TEST_CONTAINER ..."
docker start "$PROD_CONTAINER"
docker start "$TEST_CONTAINER"
docker exec -it dolibarr_test rm -f /var/www/documents/install.lock
#docker exec -it dolibarr_test touch /var/www/documents/install.lock
echo "=========================================================="
echo "✅ Fertig: TEST-System wurde mit PROD-Daten überschrieben."
