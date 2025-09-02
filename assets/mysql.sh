#!/bin/bash
kbe_path=./res/server/kbengine.xml

dbHost=`sed -n '/<databaseInterfaces>/,/<\/databaseInterfaces>/p' $kbe_path | sed -rn 's/\s*<host>\s*(\S*)\s*<\/host>.*/\1/p'`
dbPort=`sed -n '/<databaseInterfaces>/,/<\/databaseInterfaces>/p' $kbe_path | sed -rn 's/\s*<port>\s*(\S*)\s*<\/port>.*/\1/p'`
dbUser=`sed -n '/<auth>/,/<\/auth>/p' $kbe_path | sed -rn 's/\s*<username>\s*(\S*)\s*<\/username>.*/\1/p'`
dbPasswd=`sed -n '/<databaseInterfaces>/,/<\/databaseInterfaces>/p' $kbe_path | sed -rn 's/\s*<password>\s*(\S*)\s*<\/password>.*/\1/p'`
echo $dbHost
echo $dbPort
echo $dbUser
echo $dbPasswd
echo "$@"
mysql -h$dbHost -P$dbPort -u$dbUser -p$dbPasswd "$@"
