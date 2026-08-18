#!/bin/bash
binName='dropServer'
dropServerPath=`pwd`'/'$binName

if [ -n "$2" ]; then
    INST_ID=$2
else
    INST_ID=0
fi

pidFileName="dropServer_${INST_ID}.pid"

function stop_gameapp(){
    if [ -f ${pidFileName} ]; then
        kill `cat ${pidFileName}`
    fi
}

function start_gameapp(){
    if [ -f $pidFileName ]; then
        pid=`cat ${pidFileName} 2>/dev/null`
        if ! [[ "$pid" =~ ^[0-9]+$ ]]; then
            echo "$binName - delete invalid pid file $pidFileName $pid"
            rm -f $pidFileName
        else
            pl=`ps -A | grep -w "$pid"`

            if [ "$pl" == "" ]; then
                pc=0
            else
                pc=`echo $pl | wc -l`
            fi

            pn=`echo $pl | awk -F ' ' '{print $4}'`

            if (("$pc" == "0")); then
                echo "$binName - delete untracked pid file $pidFileName $pid"
                rm -f $pidFileName
            elif [ "$pn" == "$binName" ]; then
                echo "$binName - start server failed, process running, pid=$pid"
                exit 255
            else
                echo "$binName - delete outdate pid file $pidFileName $pid $pn"
                rm -f $pidFileName
            fi
        fi
    fi

    nohup $dropServerPath --instid=$INST_ID 2>&1 > nohup.out &
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


