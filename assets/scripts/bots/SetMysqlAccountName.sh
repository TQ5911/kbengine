#!/bin/bash
# 数据库连接信息
DB_USER="fengyan"
DB_PASS="123456"
DB_NAME="game_trunk"
# 更新 SQL 语句
UPDATE_SQL="UPDATE kbe_accountinfos SET accountName = CASE
    WHEN accountName NOT LIKE '1:%' THEN CONCAT('1:', accountName)
    ELSE accountName
END,
password = 'd41d8cd98f00b204e9800998ecf8427e';"
# 连接到 MySQL 数据库并执行 SQL 更新命令
mysql -u"$DB_USER" -p"$DB_PASS" "$DB_NAME" -e "$UPDATE_SQL"
echo "更新完成"