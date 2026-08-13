#!/bin/bash

PROJECT_HOME=$(dirname $(dirname $(dirname $(readlink -f "$0"))))
APP_NAME="allianceService"
CONFIG_FILE="${PROJECT_HOME}/bin/${APP_NAME}/${APP_NAME}Config.json"
PID_FILE="${PROJECT_HOME}/bin/${APP_NAME}/${APP_NAME}.pid"
LOG_FILE="${PROJECT_HOME}/bin/${APP_NAME}/${APP_NAME}.log"

function start() {
    if [ -f "${PID_FILE}" ]; then
        pid=$(cat ${PID_FILE})
        if kill -0 ${pid} > /dev/null 2>&1; then
            echo "${APP_NAME} is already running, pid=${pid}"
            return
        fi
    fi

    cd ${PROJECT_HOME}/bin/${APP_NAME}
    nohup ${PROJECT_HOME}/bin/${APP_NAME}/${APP_NAME} > ${LOG_FILE} 2>&1 &
    echo $! > ${PID_FILE}
    echo "${APP_NAME} started, pid=$!"
}

function stop() {
    if [ -f "${PID_FILE}" ]; then
        pid=$(cat ${PID_FILE})
        kill ${pid}
        rm ${PID_FILE}
        echo "${APP_NAME} stopped"
    else
        echo "${APP_NAME} is not running"
    fi
}

function restart() {
    stop
    sleep 1
    start
}

case "$1" in
    start)
        start
        ;;
    stop)
        stop
        ;;
    restart)
        restart
        ;;
    *)
        echo "Usage: $0 {start|stop|restart}"
        exit 1
esac
