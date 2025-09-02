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


python hotReload/_genRefreshData.py $@
$KBE_BIN_PATH/runscript -cell --script=._refreshData.py
$KBE_BIN_PATH/runscript -base --script=._refreshData.py
rm ._refreshData.py