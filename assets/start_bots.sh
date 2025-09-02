#!/bin/bash

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


BOTS_LIST=(50)
#BOTS_LIST=(1)
_idx=0
_i=1
_gus=1
for i in ${BOTS_LIST[*]}; do
	echo ">> run bots process" $_i "num: " $i "..."
	$KBE_BIN_PATH/bots $_idx $i --gus=$_gus &
	_idx=`expr $_idx + $i`
	_i=`expr $_i + 1`
	_gus=`expr $_gus + 1`
done

# $KBE_BIN_PATH/bots 0 100 --gus=1&
# $KBE_BIN_PATH/bots 0 29&
# $KBE_BIN_PATH/bots 10 10&
# $KBE_BIN_PATH/bots 20 10&
# $KBE_BIN_PATH/BOTS 149 50&

