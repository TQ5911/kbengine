#!/bin/bash
data="xzj.sql"
if [ -n "$1" ]; then
    data=$1
fi

dbHost=`sed -n '/<databaseInterfaces>/,/<\/databaseInterfaces>/p' res/server/kbengine.xml | sed -rn 's/\s*<host>\s*(\S*)\s*<\/host>.*/\1/p'`
dbPort=`sed -n '/<databaseInterfaces>/,/<\/databaseInterfaces>/p' res/server/kbengine.xml | sed -rn 's/\s*<port>\s*(\S*)\s*<\/port>.*/\1/p'`
dbUser=`sed -n '/<auth>/,/<\/auth>/p' res/server/kbengine.xml | sed -rn 's/\s*<username>\s*(\S*)\s*<\/username>.*/\1/p'`
dbPasswd=`sed -n '/<databaseInterfaces>/,/<\/databaseInterfaces>/p' res/server/kbengine.xml | sed -rn 's/\s*<password>\s*(\S*)\s*<\/password>.*/\1/p'`
dbName=`sed -rn 's/\s*<databaseName>\s*([0-9a-zA-Z_]*)\s*<\/databaseName>.*/\1/p' res/server/kbengine.xml`

if [ -z "$dbPort" ]; then
    echo "use default db port 3306"
    dbPort='3306'
fi

if [[ "$dbHost" = "" || "$dbUser" = "" || "$dbPasswd" = "" || "$dbName" = "" ]]; then
    echo "invalid db configs: host=$dbHost user=$dbUser pass=$dbPasswd database=$dbName"
    exit 0
fi

echo "import data: host=$dbHost:$dbPort user=$dbUser database=$dbName"
mysql -h$dbHost -u$dbUser -P$dbPort -p$dbPasswd $dbName < $data
