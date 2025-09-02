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

echo KBE_ROOT = \"${KBE_ROOT}\"

$KBE_BIN_PATH/runscript -cell --script=_refresh.py
$KBE_BIN_PATH/runscript -base --script=_refresh.py
