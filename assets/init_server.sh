#!/bin/bash
echo "init begin $1 $2"

homeDir="/home/"`whoami`
workDir=`pwd -P`

#serverProcess=`ps axu|pgrep baseapp`
#if [ "$serverProcess" != "" ]; then
#    echo "PLS kill running server process first"
#    exit 0
#fi

echo "create links $workDir"
rm -f $homeDir/gameserver/kbengine/kbe
mkdir -p $homeDir/gameserver/kbengine/assets/
find  $homeDir/gameserver/kbengine/assets/ -maxdepth 1 -type l -not -name "*core*" -delete
ln -s `readlink -f ../kbe` $homeDir/gameserver/kbengine/kbe
for fn in *; do
    if [[ "$fn" = "scripts" || "$fn" = "scripts.dev" || "$fn" = "scripts.dist" ]]; then
        continue
    fi
    if [ "`echo $fn|grep ".*\.bat"`" != "" ]; then
        continue
    fi
    ln -s `readlink -f $fn` $homeDir/gameserver/kbengine/assets/$fn
done

if [ -d "scripts/base" ]; then
    ln -s $workDir/scripts $homeDir/gameserver/kbengine/assets/scripts
elif [ -d "scripts.dist" ]; then
    ln -s $workDir/scripts.dist $homeDir/gameserver/kbengine/assets/scripts
else
echo "cannot find script!!!"
fi


publishUrl=`svn info|grep "^URL.*release"`
dbName="game_trunk"
forceRecreate=$1
if [ "$publishUrl" != "" ]
then
    dbName="game_release"
fi

if [ "$2" != "" ]
then
    dbName=$2
fi

exists=`mysql -ufengyan -p123456 -e "show databases like \"$dbName\""`
sed -i "s|<databaseName>.*</databaseName>|<databaseName> $dbName </databaseName>|g" ../assets/res/server/kbengine.xml
sed -i '/<auth>/,/<\/auth>/ s|<username>.*</username>|<username> fengyan </username>|g' ../assets/res/server/kbengine.xml
sed -i '/<auth>/,/<\/auth>/ s|<password>.*</password>|<password> 123456 </password>|g' ../assets/res/server/kbengine.xml
sed -i '/<default>/,/<\/default>/ s|<host>.*</host>|<host> 127.0.0.1 </host>|g' ../assets/res/server/kbengine.xml

if [[ "$exists" = "" || "$forceRecreate" -eq 1 ]];
then
    echo "create&sync db $dbName"
    mysql -ufengyan -p123456 -e "drop database if exists "$dbName
    mysql -ufengyan -p123456 -e "create database "$dbName
    ./syncdb.sh
    echo "sync db done"
fi

echo "init done"

