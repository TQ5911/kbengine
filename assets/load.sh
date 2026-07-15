#!/bin/bash
kbe_path=res/server/kbengine.xml

dbHost=`sed -n '/<databaseInterfaces>/,/<\/databaseInterfaces>/p' $kbe_path | sed -rn 's/\s*<host>\s*(\S*)\s*<\/host>.*/\1/p'`
dbPort=`sed -n '/<databaseInterfaces>/,/<\/databaseInterfaces>/p' $kbe_path | sed -rn 's/\s*<port>\s*(\S*)\s*<\/port>.*/\1/p'`
dbUser=`sed -n '/<auth>/,/<\/auth>/p' $kbe_path | sed -rn 's/\s*<username>\s*(\S*)\s*<\/username>.*/\1/p'`
dbPasswd=`sed -n '/<databaseInterfaces>/,/<\/databaseInterfaces>/p' $kbe_path | sed -rn 's/\s*<password>\s*(\S*)\s*<\/password>.*/\1/p'`
dbName=`sed -n '/<databaseInterfaces>/,/<\/databaseInterfaces>/p' $kbe_path | sed -rn 's/\s*<databaseName>\s*(\S*)\s*<\/databaseName>.*/\1/p'`


mysql -h$dbHost -u$dbUser -p$dbPasswd -e "drop database $dbName"
mysql -h$dbHost -u$dbUser -p$dbPasswd -e "create database $dbName"
mysql -h$dbHost -u$dbUser -p $dbName -p$dbPasswd < $1.sql
