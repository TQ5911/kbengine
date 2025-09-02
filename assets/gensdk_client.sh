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

if [ -z "$uid" ]; then
    uid=$(($RANDOM%32760+1))
fi
    
echo "UID=$uid"

echo KBE_ROOT = $KBE_ROOT
echo KBE_RES_PATH = $KBE_RES_PATH
echo KBE_BIN_PATH = $KBE_BIN_PATH

cd $currPath

$KBE_BIN_PATH/kbcmd --clientsdk=unitylua --outpath=../../../../Client/Assets/StreamingAssets/Lua/KBEngine/generated --cspath=$currPath/../../../../Client/Assets/Scripts/ScriptsKBE/kbengine/kbengine_unity3d_plugins
$KBE_BIN_PATH/kbcmd --clientsdk=unity --outpath=../../../../Client/Assets/Scripts/ScriptsKBE/kbengine/kbengine_unity3d_plugins
