#!/bin/bash

# 排除的目录
EXCLUDE_DIRS=" data proto "

# 收集实际处理的服务名，用于最后检查进程状态
SERVICE_NAMES=""

# 遍历当前目录下的一级子目录
for dir in */; do
    dir=${dir%/}
    # 排除 data 和 proto 目录
    case "$EXCLUDE_DIRS" in
        *" $dir "*) continue ;;
    esac

    echo "Processing service in $dir..."
    cd "$dir"
    if [ -f "./game.sh" ]; then
        ./game.sh stop
        ./game.sh start
        SERVICE_NAMES="$SERVICE_NAMES|$dir"
    else
        echo "Warning: game.sh not found in $dir"
    fi
    cd ..
done

# 最后检查进程状态
if [ -n "$SERVICE_NAMES" ]; then
    ps -ef | grep -v grep | grep -E "${SERVICE_NAMES#|}"
fi
