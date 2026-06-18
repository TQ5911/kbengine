#!/bin/bash

# 定义所有服务目录
SERVICES="login admin router maple dropServer leaseServer auction crossDataServer queueServer orderService"

# 遍历每个目录
for dir in $SERVICES; do
    echo "Processing service in $dir..."
    if [ -d "$dir" ]; then
        cd "$dir"
        # 查找该目录下唯一的 .sh 脚本
        script=$(ls *.sh 2>/dev/null | head -n 1)
        if [ -n "$script" ]; then
            ./"$script" stop
            ./"$script" start
        else
            echo "Warning: No .sh script found in $dir"
        fi
        cd ..
    else
        echo "Error: Directory $dir not found"
    fi
done

# 最后检查进程状态
ps -ef | grep -v grep | grep -E 'centralLogin|admin|auction|router|maple|dropServer|leaseServer|crossDataServer|queueServer|orderService'
