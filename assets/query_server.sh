#!/bin/bash
homeDir="/home/"`whoami`
workDir=`pwd -P`
curUid=`id -u`

ps aux|grep kbengine
python "$homeDir/gameserver/kbengine/kbe/tools/server/pycluster/cluster_controller.py" $curUid|grep $curUid
