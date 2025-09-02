#!/bin/bash
if [ -d "tsssdk_log" ]; then
    rm tsssdk_log/*
fi
./kill_server.sh

timestamp=$(date +"%Y-%m-%d_%H-%M-%S")

# 创建一个以时间戳命名的文件
#touch "$timestamp"
dir="/tmp/log_$timestamp"
echo $dir
mkdir $dir
mv logs/*.log* $dir

chmod +x ./tools/fetchXml
cp ./tools/fetchXml.json ./
./tools/fetchXml
rm ./fetchXml.json

./syncdb.sh
./import_db.sh startServerDb.sql

baseNum=`sed -rn 's/\s*<baseAppCount>\s*([0-9]*)\s*<\/baseAppCount>.*/\1/p' res/server/kbengine.xml`
cellNum=`sed -rn 's/\s*<cellAppCount>\s*([0-9]*)\s*<\/cellAppCount>.*/\1/p' res/server/kbengine.xml`

for i in `seq $baseNum`
do
    ./game_baseapp.sh start $i
done

for i in `seq $cellNum`
do	
    ./game_cellapp.sh start $i
done

./game_interfaces.sh start 1

./game_dbmgr.sh start 1

./game_baseappmgr.sh start 1

./game_cellappmgr.sh start 1

./game_loginapp.sh start 1

./game_machine.sh start 1

./game_logger.sh start 1
echo "start server finished!"
