#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
一键批量替换 bin/ 下各服务配置文件中的 mysql / redis 连接信息。

支持：mysql.host、mysql.port、mysql.user、mysql.passwd、redis.host、redis.port、redis.user、redis.passwd。
默认 dry-run，需加 --apply 才真正写盘；--backup 在写盘前生成 .bak 副本。

示例：
  python replace_db_config.py \
      --mysql-host 10.0.0.1 --mysql-port 3306 --mysql-user admin --mysql-passwd secret \
      --redis-host 10.0.0.2 --redis-port 6379 --redis-passwd rspass \
      --backup --apply
"""
import argparse
import glob
import json
import os
import shutil
import sys
from collections import OrderedDict

DEFAULT_MYSQL_PORT = 3306
DEFAULT_REDIS_PORT = 6379

# 不是 DB 连接配置的文件名（跳过）
SKIP_FILES = {"serverList.json"}

# mysql 配置的多种大小写形式（与其它脚本保持一致）
MYSQL_KEY_VARIANTS = ("mysql", "Mysql", "MYSQL")


def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f, object_pairs_hook=OrderedDict)


def save_json(path, config):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=4, ensure_ascii=False)
        f.write("\n")


def find_mysql_block(config):
    for k in MYSQL_KEY_VARIANTS:
        block = config.get(k)
        if isinstance(block, dict):
            return block
    return None


def update_addr(block, new_host, new_port, default_port):
    """根据 user 给的 host/port 与原值合并新 addr；若最终未变化则返回 None。"""
    old_addr = block.get("addr") or ""
    # 仅当存在 ":" 时按 last colon 切分，否则整体视为 host（兼容 "127.0.0.1" / "10.0.0.1:3306" 两种形式）
    if ":" in old_addr:
        host_part, port_part = old_addr.rsplit(":", 1)
    else:
        host_part, port_part = old_addr, ""
    final_host = new_host if new_host is not None else host_part
    final_port = (
        str(new_port) if new_port is not None else (port_part or str(default_port))
    )
    new_addr = f"{final_host}:{final_port}"
    if new_addr == old_addr:
        return None
    return ("addr", old_addr, new_addr)


def update_field(block, key, new_value):
    old = block.get(key)
    if old == new_value:
        return None
    return (key, old, new_value)


def merge_mysql(block, args):
    changes = []
    addr_change = update_addr(
        block, args.mysql_host, args.mysql_port, DEFAULT_MYSQL_PORT
    )
    if addr_change is not None:
        changes.append(addr_change)
        block["addr"] = addr_change[2]
    for key, new_value in (
        ("user", args.mysql_user),
        ("passwd", args.mysql_passwd),
    ):
        if new_value is None:
            continue
        ch = update_field(block, key, new_value)
        if ch is not None:
            changes.append(ch)
            block[key] = new_value
    return changes


def merge_redis(block, args):
    changes = []
    addr_change = update_addr(
        block, args.redis_host, args.redis_port, DEFAULT_REDIS_PORT
    )
    if addr_change is not None:
        changes.append(addr_change)
        block["addr"] = addr_change[2]
    for key, new_value in (
        ("username", args.redis_user),
        ("passwd", args.redis_passwd),
    ):
        if new_value is None:
            continue
        ch = update_field(block, key, new_value)
        if ch is not None:
            changes.append(ch)
            block[key] = new_value
    return changes


def main():
    parser = argparse.ArgumentParser(
        description="Replace mysql/redis connection info across all service JSON configs under bin/."
    )
    parser.add_argument("--mysql-host", help="MySQL host; combines with --mysql-port into addr")
    parser.add_argument("--mysql-port", type=int, help="MySQL port (default 3306 if absent from existing addr)")
    parser.add_argument("--mysql-user", help="MySQL user")
    parser.add_argument("--mysql-passwd", help="MySQL password (use \"\" to clear)")
    parser.add_argument("--redis-host", help="Redis host; combines with --redis-port into addr")
    parser.add_argument("--redis-port", type=int, help="Redis port (default 6379 if absent from existing addr)")
    parser.add_argument("--redis-user", help="Redis username (some configs leave it empty)")
    parser.add_argument("--redis-passwd", help="Redis password (use \"\" to clear)")
    parser.add_argument(
        "--apply",
        action="store_true",
        help="Actually write changes (default is dry-run, only prints diffs)",
    )
    parser.add_argument(
        "--backup",
        action="store_true",
        help="Create <file>.bak before writing (only effective with --apply)",
    )
    args = parser.parse_args()

    bin_dir = os.getcwd()
    print(f"Scanning JSON configs in: {bin_dir}")
    print(f"Mode: {'APPLY (writing files)' if args.apply else 'DRY-RUN (no files written)'}")
    if not args.apply:
        print("          pass --apply to commit changes")
    print("-" * 60)

    if all(
        v is None
        for v in (
            args.mysql_host,
            args.mysql_port,
            args.mysql_user,
            args.mysql_passwd,
            args.redis_host,
            args.redis_port,
            args.redis_user,
            args.redis_passwd,
        )
    ):
        print("Nothing to do: no --mysql-* / --redis-* value provided.")
        return

    changed_files = 0
    total_changes = 0

    for folder in sorted(os.listdir(bin_dir)):
        folder_path = os.path.join(bin_dir, folder)
        if not os.path.isdir(folder_path):
            continue

        for json_file in sorted(glob.glob(os.path.join(folder_path, "*.json"))):
            name = os.path.basename(json_file)
            if name in SKIP_FILES:
                continue

            try:
                config = load_json(json_file)
            except (IOError, ValueError) as e:
                print(f"[skip] {folder}/{name}: parse/load failed: {e}")
                continue

            file_changes = []

            mysql_block = find_mysql_block(config)
            if mysql_block is not None:
                for key, old, new in merge_mysql(mysql_block, args):
                    file_changes.append(("mysql", key, old, new))

            redis_block = config.get("redisServer")
            if isinstance(redis_block, dict):
                for key, old, new in merge_redis(redis_block, args):
                    file_changes.append(("redis", key, old, new))

            if not file_changes:
                continue

            print(f"\n{folder}/{name}:")
            for kind, key, old, new in file_changes:
                old_repr = "None" if old is None else repr(old)
                new_repr = "None" if new is None else repr(new)
                print(f"  {kind}.{key}: {old_repr} -> {new_repr}")

            if args.apply:
                if args.backup:
                    shutil.copy2(json_file, json_file + ".bak")
                save_json(json_file, config)

            changed_files += 1
            total_changes += len(file_changes)

    print("\n" + "=" * 60)
    print(f"Files affected: {changed_files}")
    print(f"Total field changes: {total_changes}")
    if not args.apply:
        print("(DRY-RUN: no files written. Re-run with --apply to commit.)")


if __name__ == "__main__":
    main()
