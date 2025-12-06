#!/bin/bash

# MySQL配置文件导入脚本
# 功能：扫描当前目录下的所有文件夹，查找SQL文件并导入到对应的数据库中

# 默认MySQL配置
MYSQL_HOST="localhost"
MYSQL_PORT="3306"
MYSQL_USER="fengyan"
MYSQL_PASSWORD="123456"
MYSQL_CHARSET="utf8mb4"

# 显示帮助信息
show_help() {
    echo "用法: $0 [选项]"
    echo ""
    echo "选项:"
    echo "  -h, --host MySQL服务器地址 (默认: localhost)"
    echo "  -P, --port MySQL端口 (默认: 3306)"
    echo "  -u, --user MySQL用户名 (必填)"
    echo "  -p, --password MySQL密码 (必填)"
    echo "  -c, --charset 字符集 (默认: utf8mb4)"
    echo "  --help 显示此帮助信息"
    echo ""
    echo "示例:"
    echo "  $0 -u root -p your_password"
    echo "  $0 -u root -p your_password -h 127.0.0.1 -P 3306"
}

# 解析命令行参数
while [[ $# -gt 0 ]]; do
    case $1 in
        -h|--host)
            MYSQL_HOST="$2"
            shift 2
            ;;
        -P|--port)
            MYSQL_PORT="$2"
            shift 2
            ;;
        -u|--user)
            MYSQL_USER="$2"
            shift 2
            ;;
        -p|--password)
            MYSQL_PASSWORD="$2"
            shift 2
            ;;
        -c|--charset)
            MYSQL_CHARSET="$2"
            shift 2
            ;;
        --help)
            show_help
            exit 0
            ;;
        *)
            echo "未知选项: $1"
            show_help
            exit 1
            ;;
    esac
done

# 检查必填参数
if [[ -z "$MYSQL_USER" || -z "$MYSQL_PASSWORD" ]]; then
    echo "错误: MySQL用户名和密码为必填项"
    show_help
    exit 1
fi

# 测试MySQL连接
echo "正在测试MySQL连接..."
mysql -h "$MYSQL_HOST" -P "$MYSQL_PORT" -u "$MYSQL_USER" -p"$MYSQL_PASSWORD" -e "SELECT 1;" > /dev/null 2>&1
if [[ $? -ne 0 ]]; then
    echo "错误: 无法连接到MySQL服务器，请检查连接参数"
    exit 1
fi
echo "MySQL连接成功！"

# 获取当前目录
CURRENT_DIR=$(pwd)
echo "扫描目录: $CURRENT_DIR"

# 计数器
PROCESSED_COUNT=0
SKIPPED_COUNT=0
ERROR_COUNT=0

# 扫描当前目录下的所有文件夹
echo ""
echo "开始扫描文件夹..."
for folder in */; do
    # 移除尾部的斜杠
    folder=${folder%/}

    # 跳过非目录项
    if [[ ! -d "$folder" ]]; then
        continue
    fi

    echo ""
    echo "----------------------------------------"
    echo "处理文件夹: $folder"
    echo "----------------------------------------"

    # 进入文件夹
    cd "$folder"

    # 查找SQL文件
    sql_files=(*.sql)

    # 检查是否找到了SQL文件
    if [[ ! -e "${sql_files[0]}" ]]; then
        echo "  [跳过] 未找到SQL文件"
        SKIPPED_COUNT=$((SKIPPED_COUNT + 1))
        cd "$CURRENT_DIR"
        continue
    fi

    # 处理每个SQL文件
    for sql_file in "${sql_files[@]}"; do
        echo "  找到SQL文件: $sql_file"

        # 创建数据库（如果不存在）
        db_name="$folder"
        echo "  创建数据库: $db_name"

        mysql -h "$MYSQL_HOST" -P "$MYSQL_PORT" -u "$MYSQL_USER" -p"$MYSQL_PASSWORD" << EOF
CREATE DATABASE IF NOT EXISTS \`$db_name\` CHARACTER SET $MYSQL_CHARSET COLLATE ${MYSQL_CHARSET}_unicode_ci;
EOF

        if [[ $? -eq 0 ]]; then
            echo "  数据库 $db_name 创建成功（或已存在）"
        else
            echo "  错误: 数据库 $db_name 创建失败"
            ERROR_COUNT=$((ERROR_COUNT + 1))
            continue
        fi

        # 导入SQL文件
        echo "  正在导入SQL文件到数据库 $db_name..."

        mysql -h "$MYSQL_HOST" -P "$MYSQL_PORT" -u "$MYSQL_USER" -p"$MYSQL_PASSWORD" "$db_name" < "$sql_file"

        if [[ $? -eq 0 ]]; then
            echo "  ✓ SQL文件导入成功"
            PROCESSED_COUNT=$((PROCESSED_COUNT + 1))
        else
            echo "  ✗ SQL文件导入失败"
            ERROR_COUNT=$((ERROR_COUNT + 1))
        fi
    done

    # 返回上一级目录
    cd "$CURRENT_DIR"
done

# 显示总结
echo ""
echo "========================================"
echo "执行完成统计:"
echo "========================================"
echo "成功导入: $PROCESSED_COUNT 个数据库"
echo "跳过文件夹: $SKIPPED_COUNT 个"
echo "失败数量: $ERROR_COUNT 个"
echo "========================================"