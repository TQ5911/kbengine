#!/bin/bash

# 排除的目录
EXCLUDE_DIRS=" data proto "

# 遍历当前目录下的一级子目录
for dir in */; do
    dir=${dir%/}
    # 排除 data 和 proto 目录
    case "$EXCLUDE_DIRS" in
        *" $dir "*) continue ;;
    esac

    echo "Stopping service in $dir..."
    cd "$dir"
    if [ -f "./game.sh" ]; then
        ./game.sh stop
    else
        echo "Warning: game.sh not found in $dir"
    fi
    cd ..
done

# 最后检查进程状态
./check_all.sh
