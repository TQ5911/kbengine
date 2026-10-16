#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
centralService 配置渲染器。

把 bin/<服务名>/*.json 渲染成部署目录下的生产配置。

设计取舍
--------
不采用「12 份配置模板 + 占位符」的做法。仓库里现有的 JSON 是业务配置的
真实来源，业务同学随时会新增配置键；复制成模板后两份文件必然漂移。
这里的做法是：

    仓库 JSON（基线）
      + deploy.env   —— 统一注入 MySQL / Redis 连接信息与上报地址
      + overrides.conf —— 逐键覆盖与机器环境相关的地址、端口
    = 部署目录下的配置

额外处理了仓库里长期存在的大小写/异名不一致：
    MySQL  块名: mysql / Mysql / MYSQL
    密码   键名: passwd / password        （orderService 用的是 password）
    Redis  块名: redisServer / redis / RedisServer / Redis
    Redis 用户键名: username / user

用法
----
    python3 render_config.py \\
        --src-dir  <repo>/bin \\
        --out-dir  <staging> \\
        --env      deploy.env \\
        --overrides overrides.conf \\
        --instances instances.conf

    --dry-run  只打印将要发生的变更，不写盘
    --only     只处理指定服务（逗号分隔）
"""

import argparse
import json
import os
import re
import sys
from collections import OrderedDict

# --- 仓库里出现过的键名变体 -------------------------------------------------
MYSQL_BLOCK_KEYS = ("mysql", "Mysql", "MYSQL")
REDIS_BLOCK_KEYS = ("redisServer", "redis", "RedisServer", "Redis")
PASSWORD_KEYS = ("passwd", "password")
USER_KEYS = ("username", "user")
# 日志路径键名在各服务里大小写不一（leaseServer 用的是 LogPath）
LOG_PATH_KEYS = ("logPath", "LogPath")

DEFAULT_MYSQL_PORT = "3306"
DEFAULT_REDIS_PORT = "6379"

# --- 内网地址扫描 ------------------------------------------------------------
# 仓库里的 JSON 是在开发机上写的，带着 192.168.x.x 这类地址。渲染只统一了
# MySQL / Redis 两处，其余跨服地址、对端地址全靠 overrides.conf。
# 如果忘了写 overrides，这些开发机地址会原样进到生产配置里，
# 表现为服务能起但连不上对端，且日志里看不出是配置问题。
# 所以渲染完成后统一扫一遍，把「没被 deploy.env 管到」的内网地址列出来。
_HOSTPORT_RE = re.compile(r"^(\d{1,3}(?:\.\d{1,3}){3}|localhost|\[[0-9a-fA-F:]+\])(:\d{1,5})$")


def _is_private_host(host):
    """返回 "rfc1918" / "loopback" / None。"""
    if host == "localhost":
        return "loopback"
    if host.startswith("["):
        return "loopback" if host == "[::1]" else None
    parts = host.split(".")
    if len(parts) != 4:
        return None
    try:
        octets = [int(p) for p in parts]
    except ValueError:
        return None
    if any(o > 255 for o in octets):
        return None
    if octets[0] == 10:
        return "rfc1918"
    if octets[0] == 192 and octets[1] == 168:
        return "rfc1918"
    if octets[0] == 172 and 16 <= octets[1] <= 31:
        return "rfc1918"
    if octets[0] == 127:
        return "loopback"
    return None


def scan_private_endpoints(where, node, path, managed, found):
    """递归找出配置里仍然是内网地址的 host:port 字符串。

    found 收到 (where, path, value, kind)，kind 为 rfc1918 或 loopback。
    """
    if isinstance(node, dict):
        for key, value in node.items():
            scan_private_endpoints(where, value, "%s.%s" % (path, key) if path else key,
                                   managed, found)
    elif isinstance(node, list):
        for idx, value in enumerate(node):
            scan_private_endpoints(where, value, "%s[%d]" % (path, idx), managed, found)
    elif isinstance(node, str):
        match = _HOSTPORT_RE.match(node.strip())
        if not match:
            return
        host = match.group(1)
        kind = _is_private_host(host)
        if not kind:
            return
        if node.strip() in managed:
            return          # 这就是 deploy.env 里声明的地址，符合预期
        found.append((where, path, node.strip(), kind))


def fail(msg):
    sys.stderr.write("render_config: %s\n" % msg)
    sys.exit(1)


def is_true(value):
    """deploy.env 里的开关。留空视为真（默认开启）。"""
    return str(value).strip().lower() not in ("0", "no", "false", "off", "n", "f")


# ============================================================================
#  文件解析
# ============================================================================
def load_env(path):
    """读取 KEY=VALUE 形式的 env 文件。不做变量展开，只去掉成对引号。"""
    env = {}
    if not path:
        return env
    if not os.path.isfile(path):
        fail("找不到环境文件: %s" % path)

    with open(path, "r", encoding="utf-8-sig") as fh:
        for lineno, raw in enumerate(fh, 1):
            line = raw.strip()
            if not line or line.startswith("#"):
                continue
            if line.startswith("export "):
                line = line[7:].strip()
            if "=" not in line:
                fail("%s:%d 不是 KEY=VALUE 形式: %s" % (path, lineno, raw.rstrip()))
            key, _, val = line.partition("=")
            key = key.strip()
            val = val.strip()
            if len(val) >= 2 and val[0] == val[-1] and val[0] in ("'", '"'):
                val = val[1:-1]
            env[key] = val
    return env


def load_overrides(path):
    """读取逐服务覆盖。

    返回 {服务名: [(目标文件名或 None, 点分键, 值, 行号), ...]}

    目标文件名的确定：
        服务名:键=值                  -> 作用于 <服务名>.json（主配置）
        服务名/serverList.json:键=值  -> 显式指定文件

    之所以要限定目标文件：服务目录下常有 serverList.json 这类副配置，
    如果把覆盖无差别地刷到该目录所有 JSON 上，会往不相干的文件里
    凭空造出 redisServer 之类的节点。
    """
    result = {}
    if not path or not os.path.isfile(path):
        return result

    with open(path, "r", encoding="utf-8-sig") as fh:
        for lineno, raw in enumerate(fh, 1):
            line = raw.strip()
            if not line or line.startswith("#"):
                continue
            scope, sep, rest = line.partition(":")
            if not sep or not scope.strip():
                fail("%s:%d 缺少「服务名:键=值」中的服务名: %s" % (path, lineno, raw.rstrip()))
            scope = scope.strip()
            svc = scope
            target = None
            if "/" in scope:
                svc, _, fname = scope.partition("/")
                svc = svc.strip()
                target = fname.strip()
                if not svc or not target:
                    fail("%s:%d 服务名或文件名为空: %s" % (path, lineno, raw.rstrip()))

            dotted, eq, raw_val = rest.partition("=")
            if not eq or not dotted.strip():
                fail("%s:%d 缺少「键=值」: %s" % (path, lineno, raw.rstrip()))
            dotted = dotted.strip()
            raw_val = raw_val.strip()
            try:
                value = json.loads(raw_val)
            except json.JSONDecodeError as exc:
                fail("%s:%d 的值不是合法 JSON (%s): %s" % (path, lineno, exc, raw_val))
            result.setdefault(svc, []).append((target, dotted, value, lineno))
    return result


def load_instances(path):
    """读取服务清单，返回 [服务名, ...]"""
    names = []
    with open(path, "r", encoding="utf-8") as fh:
        for raw in fh:
            line = raw.strip()
            if not line or line.startswith("#"):
                continue
            name = line.split("|", 1)[0].strip()
            if name:
                names.append(name)
    return names


def load_json(path):
    with open(path, "r", encoding="utf-8") as fh:
        return json.load(fh, object_pairs_hook=OrderedDict)


# ============================================================================
#  写入辅助
# ============================================================================
def find_block(cfg, candidates):
    for key in candidates:
        value = cfg.get(key)
        if isinstance(value, dict):
            return key, value
    return None, None


def ensure_port(addr, default_port):
    """配置里可能是 host 也可能是 host:port，统一补全端口。"""
    if ":" in addr:
        return addr
    return "%s:%s" % (addr, default_port)


def set_field(block, candidates, value, changes, where, label):
    """按 candidates 顺序写入；已存在的键名优先被复用，空值不覆盖。"""
    if value == "":
        return
    for key in candidates:
        if key in block:
            if block[key] != value:
                changes.append("%s  %s: %r -> %r" % (where, label, block[key], value))
                block[key] = value
            return
    # 仓库里没有该键，用首选名创建
    key = candidates[0]
    changes.append("%s  %s: <缺失> -> %r" % (where, label, value))
    block[key] = value


def set_dotted(cfg, dotted, value, changes, where):
    """按点分路径写值，中间层不存在时自动创建。"""
    parts = dotted.split(".")
    cursor = cfg
    for part in parts[:-1]:
        if part not in cursor:
            cursor[part] = OrderedDict()
            changes.append("%s  新建中间节点 %s: {}" % (where, part))
        elif not isinstance(cursor[part], dict):
            fail("%s: 覆盖路径 %s 的中间键 %r 不是对象，拒绝写入以免破坏原值" % (where, dotted, part))
        cursor = cursor[part]

    last = parts[-1]
    old = cursor.get(last, "<缺失>")
    if isinstance(old, (dict, list)) and not isinstance(value, (dict, list)):
        fail("%s: %s 现为 %s 类型，拒绝用标量覆盖" % (where, dotted, type(old).__name__))
    if old != value:
        changes.append("%s  %s: %r -> %r" % (where, dotted, old, value))
        cursor[last] = value


# ============================================================================
#  主渲染
# ============================================================================
def render_file(path, svc, env, svc_overrides, changes):
    fname = os.path.basename(path)
    try:
        cfg = load_json(path)
    except ValueError as exc:
        fail("%s 不是合法 JSON: %s" % (path, exc))
    if not isinstance(cfg, dict):
        fail("%s 顶层不是对象，跳过" % path)

    where = "%s/%s" % (svc, fname)

    # ---- MySQL ----
    _, mysql = find_block(cfg, MYSQL_BLOCK_KEYS)
    if mysql is not None:
        set_field(mysql, ("addr",), ensure_port(env.get("MYSQL_ADDR", ""), DEFAULT_MYSQL_PORT),
                  changes, where, "mysql.addr")
        set_field(mysql, ("user",), env.get("MYSQL_USER", ""), changes, where, "mysql.user")
        set_field(mysql, PASSWORD_KEYS, env.get("MYSQL_PASSWD", ""), changes, where, "mysql.passwd")

    # ---- Redis ----
    _, redis = find_block(cfg, REDIS_BLOCK_KEYS)
    if redis is not None:
        set_field(redis, ("addr",), ensure_port(env.get("REDIS_ADDR", ""), DEFAULT_REDIS_PORT),
                  changes, where, "redis.addr")
        set_field(redis, USER_KEYS, env.get("REDIS_USER", ""), changes, where, "redis.user")
        set_field(redis, PASSWORD_KEYS, env.get("REDIS_PASSWD", ""), changes, where, "redis.passwd")
        # db 键在各服务里类型不一（orderService 是数字，其余是字符串），
        # 统一不注入，需要改用 overrides.conf 显式指定。

    # ---- 日志路径 ----
    # logPath 是相对路径，配合 systemd 的 WorkingDirectory 就落在服务目录内。
    # 但仓库里的值不统一（drop.log / login.log / ./admin.log ...），
    # 统一成 <服务名>.log，这样「日志就在服务自己目录下、名字等于服务名」。
    # 只改主配置 <服务名>.json，serverList.json 这类副配置不带日志键。
    if is_true(env.get("LOG_IN_SERVICE_DIR", "1")) and fname == "%s.json" % svc:
        set_field(cfg, LOG_PATH_KEYS, "%s.log" % svc, changes, where, "logPath")

    # ---- 上报地址 ----
    report = env.get("REPORT_ADDR", "")
    if report != "" and "reportAddr" in cfg:
        if cfg["reportAddr"] != report:
            changes.append("%s  reportAddr: %r -> %r" % (where, cfg["reportAddr"], report))
            cfg["reportAddr"] = report

    # ---- 逐键覆盖（只作用于主配置 <服务名>.json，除非显式指定了文件名）----
    primary = "%s.json" % svc
    for target, dotted, value, lineno in svc_overrides:
        if target and target != fname:
            continue
        if not target and fname != primary:
            continue
        set_dotted(cfg, dotted, value, changes, where)

    return cfg


def main():
    parser = argparse.ArgumentParser(
        description="渲染 centralService 各服务的部署配置（基线=仓库 JSON，叠加 env 与 overrides）")
    parser.add_argument("--src-dir", required=True, help="源码产出目录，通常是 <repo>/bin")
    parser.add_argument("--out-dir", required=True, help="渲染输出根目录，通常是临时 staging")
    parser.add_argument("--env", default="", help="deploy.env 路径")
    parser.add_argument("--overrides", default="", help="overrides.conf 路径")
    parser.add_argument("--instances", required=True, help="instances.conf 路径")
    parser.add_argument("--only", default="", help="只渲染指定服务，逗号分隔")
    parser.add_argument("--dry-run", action="store_true", help="只打印变更，不写盘")
    parser.add_argument("--strict", action="store_true",
                        help="发现未声明的内网地址时以非零码退出（供 CI 卡关）")
    args = parser.parse_args()

    env = load_env(args.env)
    overrides = load_overrides(args.overrides)
    services = load_instances(args.instances)
    if args.only:
        wanted = {s.strip() for s in args.only.split(",") if s.strip()}
        services = [s for s in services if s in wanted]
    if not services:
        fail("没有要处理的服务")

    all_changes = []
    written = 0
    private_hits = []

    # deploy.env 与 overrides.conf 里声明过的地址属于「有意为之」，扫描时排除。
    # 注意：生产内网地址本身就是 10.x / 192.168.x，所以判断依据不是「是不是内网」，
    # 而是「有没有人显式配过」。没配过的才说明是从开发机仓库配置里带过来的。
    managed = set()
    for env_key, default_port in (("MYSQL_ADDR", DEFAULT_MYSQL_PORT),
                                  ("REDIS_ADDR", DEFAULT_REDIS_PORT)):
        value = env.get(env_key, "").strip()
        if value:
            managed.add(ensure_port(value, default_port))
    for svc_overrides in overrides.values():
        for _target, _dotted, value, _lineno in svc_overrides:
            if isinstance(value, str) and value.strip():
                managed.add(value.strip())

    for svc in services:
        src_dir = os.path.join(args.src_dir, svc)
        if not os.path.isdir(src_dir):
            fail("服务 %s 的源目录不存在: %s" % (svc, src_dir))

        json_files = sorted(f for f in os.listdir(src_dir) if f.endswith(".json"))
        if not json_files:
            fail("服务 %s 目录下没有任何 *.json，无法渲染配置" % svc)

        svc_overrides = overrides.get(svc, [])
        out_dir = os.path.join(args.out_dir, svc)

        for name in json_files:
            src = os.path.join(src_dir, name)
            changes = []
            cfg = render_file(src, svc, env, svc_overrides, changes)
            all_changes.extend(changes)
            scan_private_endpoints("%s/%s" % (svc, name), cfg, "", managed, private_hits)

            if not args.dry_run:
                if not os.path.isdir(out_dir):
                    os.makedirs(out_dir)
                dst = os.path.join(out_dir, name)
                with open(dst, "w", encoding="utf-8") as fh:
                    json.dump(cfg, fh, indent=4, ensure_ascii=False)
                    fh.write("\n")
                # 配置内含数据库口令，限制为属主可读写
                os.chmod(dst, 0o600)
            written += 1

    if all_changes:
        print("配置变更明细：")
        for line in all_changes:
            print("  " + line)
        print("")
    else:
        print("配置无需变更。")

    if args.dry_run:
        print("[dry-run] 校验了 %d 个配置文件，未写盘。" % written)
    else:
        print("已渲染 %d 个配置文件到 %s" % (written, args.out_dir))

    # ---- 遗留内网地址告警 ----
    if private_hits:
        # 分两档：192.168/10.x/172.16-31.x 几乎一定是开发机残留；
        # localhost / 127.0.0.1 在单机部署里通常本来就是对的。
        high = sorted(set(h for h in private_hits if h[3] == "rfc1918"))
        low = sorted(set(h for h in private_hits if h[3] == "loopback"))

        if high:
            print("")
            print("!! 高危：以下地址疑似开发机残留，必须确认后处理")
            for where, path, value, _kind in high:
                print("   %-38s %-32s %s" % (where, path, value))
            print("   在 overrides.conf 里覆盖，形如：<服务名>:<键路径>=\"<生产地址>:<端口>\"")
            print("   漏配的表现是服务能起但连不上对端，且日志里看不出是配置问题。")

        if low:
            print("")
            print(".. 提示：以下指向本机。单机部署通常正确，分机部署需改")
            for where, path, value, _kind in low:
                print("   %-38s %-32s %s" % (where, path, value))

    return 1 if (private_hits and any(h[3] == "rfc1918" for h in private_hits)
                 and args.strict) else 0


if __name__ == "__main__":
    sys.exit(main())