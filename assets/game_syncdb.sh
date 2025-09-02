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

export KBE_SH_PATH="$KBE_ROOT/assets/"

echo KBE_ROOT = \"${KBE_ROOT}\"
echo KBE_SH_PATH = \"${KBE_SH_PATH}\"

if [ -n "$1" ]; then
    EXE_ARG=$1
else
    EXE_ARG=0
fi
python $KBE_SH_PATH/game_syncdb.py $EXE_ARG