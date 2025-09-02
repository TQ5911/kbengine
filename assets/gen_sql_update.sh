#!/bin/sh

currPath=$(pwd)
keyStr="/kbengine/"

bcontain=`echo $currPath|grep $keyStr|wc -l`


if [ $bcontain = 0 ]
then
	export KBE_ROOT=$(cd ../; pwd)
else
	export KBE_ROOT="$(pwd | awk -F "/kbengine/" '{print $1}')/kbengine"
fi



export KBE_RES_PATH="$KBE_ROOT/kbe/res/:$(pwd):$(pwd)/res:$(pwd)/scripts/"
export KBE_BIN_PATH="$KBE_ROOT/kbe/bin/server/"

echo KBE_ROOT = \"${KBE_ROOT}\"
echo KBE_RES_PATH = \"${KBE_RES_PATH}\"
echo KBE_BIN_PATH = \"${KBE_BIN_PATH}\"

sqlOpts="-ukbengine -pkbe123"
dbName="game_trunk_sql_diff"

mysql $sqlOpts -e "drop database $dbName;create database $dbName"
mysql $sqlOpts $dbName < $1
sed -i "s|<databaseName>.*</databaseName>|<databaseName> $dbName </databaseName>|g" ./res/server/kbengine.xml

$KBE_BIN_PATH/dbmgr -genupdatesql --cid=3129652375332859999 --instId=1
cat startServerDb.sql >> scripts/xzj.sql
