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


export tsssdk_env_type="EXPIRIENCE"
export KBE_RES_PATH="$KBE_ROOT/kbe/res/:$(pwd):$(pwd)/res:$(pwd)/scripts/"
export KBE_BIN_PATH="$KBE_ROOT/kbe/bin/server/"

if [ -n "$2" ]; then
    INST_ID=$2
else
    INST_ID=0
fi

function start_gameapp(){
    echo "loginapp start....."
    cid=`expr 900000 + $INST_ID`
    $KBE_BIN_PATH/loginapp --cid=$cid --instId=$INST_ID 2>&1 > /dev/null &
    echo "loginapp start done"
}

function stop_gameapp(){
    echo "loginapp stop...."
    pid=`cat $KBE_ROOT/assets/loginapp_${INST_ID}.pid`
    kill $pid
    ProcNumber=`ps -ef |grep -w $pid|grep -v grep|wc -l`
    until [ $ProcNumber -eq 0 ]
    do
        sleep 1
        ProcNumber=`ps -ef |grep -w $pid|grep -v grep|wc -l`
    done

    echo "loginapp stop done"
}

case $1 in
    start) start_gameapp
    ;;
    stop) stop_gameapp
    ;;
    restart)
    stop_gameapp
    start_gameapp
    ;;
    *) echo "(Arguments shuld be start|stop|restart,OK?!)" ;;
esac
