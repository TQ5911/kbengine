#!/bin/bash

# 定义所有服务目录
SERVICES="login admin router maple dropServer leaseServer auction crossDataServer queueServer orderService allianceService"

# 遍历每个目录
for dir in $SERVICES; do
    echo "Processing service in $dir..."
    if [ -d "$dir" ]; then
        cd "$dir"
        if [ -x "./game.sh" ] || [ -f "./game.sh" ]; then
            ./game.sh stop
            ./game.sh start
        else
            echo "Warning: game.sh not found in $dir"
        fi
        cd ..
    else
        echo "Error: Directory $dir not found"
    fi
done

# 最后检查进程状态
ps -ef | grep -v grep | grep -E 'centralLogin|admin|auction|router|maple|dropServer|leaseServer|crossDataServer|queueServer|orderService|allianceService'
