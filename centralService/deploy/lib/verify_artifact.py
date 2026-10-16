#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
交付二进制校验。

install.sh 装的是别人在构建机上编出来的 ELF，中间隔着一次文件传输。
这里在装之前替运维把三件事查清楚：

  1. 它真的是 Linux 可执行文件吗？
     bin/ 这个目录长期混着 .exe、.sh、vendored 的 protoc，
     拷错文件或者拷了 Windows 版本过去，靠肉眼很难发现。
  2. 架构对吗？
     构建机 GOARCH 设错时，go build 不会报错，文件只在目标机上才崩。
  3. 它比源码新吗？
     这一条最要命。bin/ 里的二进制可能停留在几周前，
     而源码早就改了。此时 --skip-build 会把过期代码装成生产版本，
     而且没有任何提示。

用法
----
    python3 verify_artifact.py \\
        --repo-root <repo> --dist-dir <dir> --instances <file> \\
        [--arch amd64|arm64] [--strict-fresh]

退出码 0 = 全部通过；1 = 有阻断项。
"""

import argparse
import os
import struct
import sys

# ELF e_machine 取值
EM_X86_64 = 0x3E
EM_AARCH64 = 0xB7
ARCH_BY_MACHINE = {EM_X86_64: "amd64", EM_AARCH64: "arm64"}

SOURCE_EXTS = (".go", ".proto", ".sh", ".mod", ".sum")


def fail(msg):
    sys.stderr.write("verify_artifact: %s\n" % msg)
    sys.exit(2)


def read_elf_header(path):
    """返回 (是否 ELF, 架构)。非 ELF 返回 (False, None)。"""
    try:
        with open(path, "rb") as fh:
            head = fh.read(20)
    except OSError as exc:
        fail("读取失败 %s: %s" % (path, exc))
    if len(head) < 20 or head[:4] != b"\x7fELF":
        return False, None
    # e_machine 是 ELF header 偏移 18 处的 2 字节小端值
    machine = struct.unpack_from("<H", head, 18)[0]
    return True, ARCH_BY_MACHINE.get(machine, "unknown(0x%x)" % machine)


def newest_source_mtime(repo_root):
    """整个模块的源码与依赖描述文件里最新的修改时间。"""
    newest = 0.0
    newest_path = ""
    for name in ("go.mod", "go.sum"):
        path = os.path.join(repo_root, name)
        if os.path.isfile(path):
            mtime = os.path.getmtime(path)
            if mtime > newest:
                newest, newest_path = mtime, name

    src_root = os.path.join(repo_root, "src")
    for dirpath, _dirnames, filenames in os.walk(src_root):
        for fname in filenames:
            if not fname.endswith(SOURCE_EXTS):
                continue
            path = os.path.join(dirpath, fname)
            try:
                mtime = os.path.getmtime(path)
            except OSError:
                continue
            if mtime > newest:
                newest, newest_path = mtime, os.path.relpath(path, repo_root)
    return newest, newest_path


def load_services(path):
    names = []
    with open(path, "r", encoding="utf-8-sig") as fh:
        for raw in fh:
            line = raw.strip()
            if not line or line.startswith("#"):
                continue
            name = line.split("|", 1)[0].strip()
            if name:
                names.append(name)
    return names


def main():
    parser = argparse.ArgumentParser(description="校验待交付的 Linux 二进制")
    parser.add_argument("--repo-root", required=True, help="仓库根目录（用于比对源码时间）")
    parser.add_argument("--dist-dir", required=True, help="二进制所在目录")
    parser.add_argument("--instances", required=True, help="服务清单")
    parser.add_argument("--arch", default="amd64", choices=["amd64", "arm64"],
                        help="期望的目标架构，默认 amd64")
    parser.add_argument("--strict-fresh", action="store_true",
                        help="发现过期二进制时以非零码退出（默认只警告）")
    args = parser.parse_args()

    if not os.path.isdir(args.dist_dir):
        fail("二进制目录不存在: %s\n       目标机不编译时，必须先在构建机上跑 ./deploy/build_linux.sh" % args.dist_dir)
    if not os.path.isdir(args.repo_root):
        fail("仓库根目录不存在: %s" % args.repo_root)

    services = load_services(args.instances)
    newest, newest_path = newest_source_mtime(args.repo_root)
    # 没找到任何源码时不能拿 0 去比，否则每个二进制都会被判成"早于 1970 年"
    can_check_freshness = newest > 0
    if not can_check_freshness:
        print("注意：%s 下没找到 src/ 源码，跳过新鲜度比对。" % args.repo_root)
        print("      （只拷贝了 bin/ 和 dist/ 时会这样，此时无法判断二进制是否过期）")

    print()
    print("%-18s %-9s %-8s %-11s %s" % ("SERVICE", "SIZE", "FORMAT", "FRESHNESS", "NOTE"))
    print("-" * 88)

    blocking = []

    for svc in services:
        path = os.path.join(args.dist_dir, svc, svc)
        size = 0
        note = ""
        blocking_here = False
        fresh = "跳过"
        fmt = "缺失"

        if not os.path.isfile(path):
            blocking_here = True
            note = "先在构建机执行 ./deploy/build_linux.sh"
        else:
            size = os.path.getsize(path)
            is_elf, arch = read_elf_header(path)
            if not is_elf:
                fmt, blocking_here = "非ELF", True
                note = "不是 Linux 可执行文件，别把 .exe 拷进来了"
            elif arch != args.arch:
                fmt, blocking_here = arch or "?", True
                note = "架构不符，期望 %s（构建机 GOARCH 是不是设错了）" % args.arch
            else:
                fmt = "ELF/" + (arch or "?")
                if not os.access(path, os.X_OK):
                    blocking_here = True
                    note = "没有可执行权限"

                # 新鲜度：二进制必须不早于整个模块最新的源码
                if can_check_freshness:
                    bin_mtime = os.path.getmtime(path)
                    if bin_mtime + 1 < newest:
                        stale_days = int((newest - bin_mtime) / 86400)
                        fresh = "旧%d天" % stale_days if stale_days >= 1 else "偏旧"
                        note = "早于 %s，源码有改动未重新编译" % newest_path
                        if args.strict_fresh:
                            blocking_here = True
                    else:
                        fresh = "OK"

        if blocking_here:
            blocking.append(svc)

        print("%-18s %-9s %-8s %-11s %s" % (
            svc,
            ("%.1fM" % (size / 1048576.0)) if size else "-",
            fmt,
            fresh,
            note,
        ))

    print("-" * 88)
    print("基准：最新源码 %s" % (newest_path if can_check_freshness else "（无，跳过新鲜度比对）"))
    print("")

    if blocking:
        print("以下 %d 个服务不可交付：%s" % (len(blocking), "、".join(blocking)))
        if not args.strict_fresh:
            print("加 --strict-fresh 可让过期二进制也阻断部署。")
        return 1

    print("全部 %d 个二进制校验通过（%s）。" % (len(services), args.arch))
    return 0


if __name__ == "__main__":
    sys.exit(main())