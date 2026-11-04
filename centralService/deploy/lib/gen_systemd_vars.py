#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
生成 ansible/systemd-only.yml 所需的变量 JSON。

分成两路传参，是为了绕开 Git Bash(MSYS) 的路径转换，原因见 install-systemd.sh：

  · 远程路径（install_root 等）走 **key=value 文件**
    MSYS 会把「看起来像 POSIX 路径」的 argv / 环境变量悄悄转成 Windows 路径，
    /home/fengyan/Server/centralService/bin 会被拼成
    D:/.../PortableGit/home/fengyan/...。这是**远程机器上的路径**，本机并不存在，
    一转换就全错。写进文件再由本脚本读出来，内容不会被碰。

  · 本地文件路径（instances.conf）走 **argv**
    它是本机真实存在的文件，MSYS 的转换是等价映射（POSIX → Windows 同一文件），
    转换后 native python 反而才打得开。

用法：
    python3 gen_systemd_vars.py <params文件> <instances.conf>  > vars.json

params 文件格式（key=value，一行一个，value 不含换行）：
    only=maple,admin          # 留空表示全部
    prefix=<远程安装根目录>
    unit_prefix=centralsvc
    user=fengyan
    group=fengyan
    timezone=Asia/Shanghai
    gotraceback=crash
    start_timeout=90
    stop_timeout=30
    restart_sec=3
    log_mode=file
    protect_home=             # 留空=由 playbook 自动决定
    svc_state=restarted
    enable=true
    check_ports=false
    port_timeout=60
    ensure_user=true
    fix_owner=false
    backup=true
"""

import json
import sys


def parse_params(path):
    params = {}
    with open(path, encoding="utf-8") as fh:
        for raw in fh:
            line = raw.rstrip("\n")
            if not line or line.lstrip().startswith("#"):
                continue
            if "=" not in line:
                continue
            key, value = line.split("=", 1)
            params[key.strip()] = value.strip()
    return params


def parse_instances(path):
    """instances.conf: name | probe_ports | db_init | description"""
    names, ports, desc = [], {}, {}
    with open(path, encoding="utf-8") as fh:
        for raw in fh:
            line = raw.split("#", 1)[0].strip()
            if not line:
                continue
            parts = [p.strip() for p in line.split("|")]
            if len(parts) < 2 or not parts[0]:
                continue
            name = parts[0]
            names.append(name)
            ports[name] = [int(p) for p in parts[1].split(",") if p.strip().isdigit()]
            desc[name] = parts[3] if len(parts) > 3 and parts[3] else name
    return names, ports, desc


def as_bool(value):
    return str(value).strip().lower() in ("1", "y", "yes", "true", "on")


def main():
    if len(sys.argv) != 3:
        sys.exit("用法: gen_systemd_vars.py <params文件> <instances.conf>")
    params = parse_params(sys.argv[1])

    inst_file = sys.argv[2]
    all_names, all_ports, all_desc = parse_instances(inst_file)
    if not all_names:
        sys.exit("服务清单为空: %s" % inst_file)

    only = [s.strip() for s in params.get("only", "").split(",") if s.strip()]
    unknown = [s for s in only if s not in all_names]
    if unknown:
        sys.stderr.write("未知服务名: %s\n可用: %s\n"
                         % (", ".join(unknown), ", ".join(all_names)))
        return 1
    services = only or all_names

    def int_or(key, default):
        raw = params.get(key, "")
        try:
            return int(raw)
        except (TypeError, ValueError):
            return default

    vars_out = {
        "services": services,
        "service_desc": {s: all_desc.get(s, s) for s in services},
        "service_ports": {s: all_ports.get(s, []) for s in services},
        "install_root": params.get("prefix", ""),
        "unit_prefix": params.get("unit_prefix", "centralsvc"),
        "service_user": params.get("user", "fengyan"),
        "service_group": params.get("group", "") or params.get("user", "fengyan"),
        "timezone": params.get("timezone", "Asia/Shanghai"),
        "gotraceback": params.get("gotraceback", "crash"),
        "start_timeout": int_or("start_timeout", 90),
        "stop_timeout": int_or("stop_timeout", 30),
        "restart_sec": int_or("restart_sec", 3),
        "log_stdout_mode": params.get("log_mode", "file"),
        "systemd_protect_home": params.get("protect_home", ""),
        "svc_state": params.get("svc_state", "restarted"),
        "enable_service": as_bool(params.get("enable", "true")),
        "check_ports": as_bool(params.get("check_ports", "false")),
        "port_timeout": int_or("port_timeout", 60),
        "ensure_user": as_bool(params.get("ensure_user", "true")),
        "fix_owner": as_bool(params.get("fix_owner", "false")),
        "unit_backup": as_bool(params.get("backup", "true")),
    }

    if not vars_out["install_root"]:
        sys.stderr.write("params 里缺少 prefix=<远程安装根目录>\n")
        return 1
    if vars_out["svc_state"] not in ("started", "stopped", "restarted", "none"):
        sys.stderr.write("svc_state 只能是 started/stopped/restarted/none"
                         "（当前: %s）\n" % vars_out["svc_state"])
        return 1

    print(json.dumps(vars_out, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
