#!/bin/sh
# 说明：
# 	1. 将协议文件重命名为idipdef.txt, 保存格式为utf-8, 放在 assets/res/server下
# 	2. 执行该脚本文件

currPath=$(pwd)
keyStr="/kbengine/"

bcontain=`echo $currPath|grep $keyStr|wc -l`


if [ $bcontain = 0 ]
then
	export KBE_ROOT=$(cd ../; pwd)
else
	export KBE_ROOT="$(pwd | awk -F "/kbengine/" '{print $1}')/kbengine"
fi


KBE_TOOL_PATH="$KBE_ROOT/kbe/tools/server/"
KBE_RES_PATH="$(pwd)/res/server/"
KBE_SCRIPT_PATH="$(pwd)/scripts/"

echo KBE_ROOT = \"${KBE_ROOT}\"
echo KBE_TOOL_PATH = \"${KBE_TOOL_PATH}\"
echo KBE_RES_PATH = \"${KBE_RES_PATH}\"
echo KBE_SCRIPT_PATH = \"${KBE_SCRIPT_PATH}\"

$KBE_TOOL_PATH/idiprpc/idiprpc -f external/tencent/xzj_IDIP.txt -o $KBE_SCRIPT_PATH/server_common/idipDef.py
