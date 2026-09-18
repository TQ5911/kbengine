#!/bin/bash
export GOTRACEBACK=crash
binName=$(basename "$PWD")
binPath=`pwd`'/'$binName

if [ -n "$2" ]; then
    INST_ID=$2
else
    INST_ID=0
fi

pidFileName="${binName}_${INST_ID}.pid"
function stop_fileserver(){
    if [ -f ${pidFileName} ]; then
        kill `cat ${pidFileName} 2>/dev/null`
    else
        echo "$binName - missing pid file, $pidFileName"
    fi
}

function start_fileserver(){
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

    nohup $binPath --instid=$INST_ID 2>&1 > nohup.out &
}

case $1 in
    start) start_fileserver
    ;;
    stop) stop_fileserver
    ;;
    restart)
    stop_fileserver
    start_fileserver
    ;;
    *) echo "(Arguments shuld be start|stop|restart,OK?!)" ;;
esac
