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
export KBE_BIN_PATH="$KBE_ROOT/kbe/bin/server"


cmd_str=$1
enc_cmd=$(printf '%s' "$1" | base64 |  tr -d '\n') 
sed "s/TARGET/${enc_cmd}/g" hotReload/_genCommand.py > ._doCommand.py
cat ._doCommand.py
$KBE_BIN_PATH/runscript -base --script=._doCommand.py
rm ._doCommand.py
