#!/bin/bash
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CONFIG_FILE="${SCRIPT_DIR}/leaseServer.json"
SQL_FILE="${SCRIPT_DIR}/lease.sql"

if [ ! -f "$CONFIG_FILE" ]; then
    echo "Error: config file $CONFIG_FILE not found"
    exit 1
fi
if [ ! -f "$SQL_FILE" ]; then
    echo "Error: sql file $SQL_FILE not found"
    exit 1
fi

extract() {
    grep -oP "\"$1\"\\s*:\\s*\"\\K[^\"]+" "$CONFIG_FILE" | head -1
}

ADDR=$(extract "addr")
USER=$(extract "user")
PASSWD=$(extract "passwd")
[ -z "$PASSWD" ] && PASSWD=$(extract "password")
DB=$(extract "db")

if [ -z "$DB" ]; then
    echo "Error: db not found in $CONFIG_FILE"
    exit 1
fi
if [ -z "$ADDR" ]; then
    echo "Error: mysql addr not found in $CONFIG_FILE"
    exit 1
fi

HOST="${ADDR%:*}"
if [ "$HOST" = "$ADDR" ]; then
    PORT=3306
else
    PORT="${ADDR#*:}"
fi

echo "Service:    $(basename "$SCRIPT_DIR")"
echo "MySQL host: $HOST"
echo "MySQL port: $PORT"
echo "Database:   $DB"
echo "SQL file:   $SQL_FILE"

export MYSQL_PWD="$PASSWD"

echo "==> Creating database $DB (if not exists)"
mysql -h "$HOST" -P "$PORT" -u "$USER" \
    -e "CREATE DATABASE IF NOT EXISTS \`$DB\` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"

echo "==> Importing SQL file into $DB"
mysql -h "$HOST" -P "$PORT" -u "$USER" "$DB" < "$SQL_FILE"

unset MYSQL_PWD
echo "==> Done"