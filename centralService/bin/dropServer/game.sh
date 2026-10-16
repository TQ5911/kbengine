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
            # ps -A + awk 按列取进程名的写法在 Linux 上取到的是 TIME 列而非
            # CMD 列，会把「服务正在运行」误判成「pid 已失效」。
            # ps -p <pid> -o comm= 在 Linux 与 macOS 上语义一致，
            # 且不受输出列位置影响。
            pn=$(ps -p "$pid" -o comm= 2>/dev/null | head -1)
            pn=${pn##*/}

            if [ -z "$pn" ]; then
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


