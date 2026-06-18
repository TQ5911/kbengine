#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
build_proto.py - 游戏服 Protobuf 中间代码生成工具

替代原有的 build_proto.bat，统一扫描 assets/scripts/common/proto/ 下的 .proto 文件，
自动生成 Python 服务端代码（_pb2.py），并可选择生成 C# 客户端 RPC 存根代码。

用法示例:
    python build_proto.py                     # 全量扫描，增量生成
    python build_proto.py --force             # 强制重新生成所有 proto
    python build_proto.py scripts/common/proto/interface.proto
                                              # 只生成指定的单个 proto 文件

参数说明:
    --force             强制重新生成，不比较 proto 与输出文件的修改时间
    --csharp-out DIR    指定 C# 输出目录（默认指向客户端工程 Proto 目录）
    --csharp-proto FILE 额外指定需要生成 C# RPC 代码的 proto 文件名
                        （可多次指定；默认包含 centralLogin.proto）
    --no-csharp         跳过 C# 代码生成，只生成 Python _pb2.py
    proto               位置参数，指定单个 proto 文件路径（绝对或相对路径均可）
                        不传则自动扫描 scripts/common/proto/ 目录下所有 .proto 文件

注意事项:
    - 本脚本仅用于游戏服（assets/ 目录），生成 Python _pb2.py 与可选的 C# 客户端代码
    - Go 中央服务代码由 Dev/tools/centralService/bin/proto/genproto.py 生成
    - C# RPC 代码通过 external/proto/protoc-3.6.1-win32/bin/csharpRpc.py 插件生成
"""

import os
import sys
import re
import glob
import stat
import shutil
import platform
import subprocess
import argparse
import tempfile

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
WORK_DIR = SCRIPT_DIR


def find_executable(name, search_dirs=None):
    """在指定目录和 PATH 中查找可执行文件（自动处理 .exe 后缀）"""
    if search_dirs is None:
        search_dirs = []
    for d in search_dirs:
        for ext in ['', '.exe']:
            p = os.path.join(d, name + ext)
            if os.path.isfile(p):
                return os.path.abspath(p)
    for path in os.environ.get('PATH', '').split(os.pathsep):
        for ext in ['', '.exe']:
            p = os.path.join(path, name + ext)
            if os.path.isfile(p):
                return os.path.abspath(p)
    return None


def get_protoc_python_path():
    """定位用于生成 Python 代码的 protoc 可执行文件"""
    proto_tool = os.path.join(SCRIPT_DIR, 'external', 'proto')
    candidates = [
        os.path.join(proto_tool, 'protoc-3.6.1-win32', 'bin', 'protoc.exe'),
    ]
    for c in candidates:
        if os.path.isfile(c):
            return c
    p = find_executable('protoc', [proto_tool])
    if p:
        return p
    raise RuntimeError(
        'protoc not found. Please place protoc in {} or install it in PATH.'.format(proto_tool)
    )


def get_protoc_csharp_path():
    """定位用于生成 C# 代码的 protoc 可执行文件"""
    proto_tool = os.path.join(SCRIPT_DIR, 'external', 'proto')
    candidates = [
        os.path.join(proto_tool, 'protoc-3.3.0-csharp', 'protoc.exe'),
    ]
    for c in candidates:
        if os.path.isfile(c):
            return c
    p = find_executable('protoc', [proto_tool])
    if p:
        return p
    raise RuntimeError(
        'protoc (csharp) not found. Please place protoc in {} or install it in PATH.'.format(proto_tool)
    )


def ensure_csharp_rpc_plugin():
    """
    protoc --plugin 要求一个可执行文件包装器。
    生成临时包装器调用 csharpRpc.py，并自动清理。
    """
    rpc_py = os.path.join(SCRIPT_DIR, 'external', 'proto', 'protoc-3.6.1-win32', 'bin', 'csharpRpc.py')
    if not os.path.isfile(rpc_py):
        raise RuntimeError('csharpRpc.py not found in {}'.format(os.path.dirname(rpc_py)))

    is_win = platform.system() == 'Windows'
    if is_win:
        wrapper = os.path.join(tempfile.gettempdir(), '_game_rpc_plugin_wrapper.bat')
        with open(wrapper, 'w', encoding='utf-8') as f:
            f.write('@"{}" "{}"\n'.format(sys.executable, rpc_py))
        return wrapper
    else:
        wrapper = os.path.join(tempfile.gettempdir(), '_game_rpc_plugin_wrapper.sh')
        with open(wrapper, 'w', encoding='utf-8') as f:
            f.write('#!/bin/sh\n')
            f.write('"{}" "{}"\n'.format(sys.executable, rpc_py))
        os.chmod(wrapper, stat.S_IRWXU)
        return wrapper


def parse_proto_package(proto_file):
    """简单解析 proto 文件中的 package 名称"""
    try:
        with open(proto_file, 'r', encoding='utf-8', errors='ignore') as f:
            for line in f:
                m = re.match(r'^\s*package\s+(\w+)', line)
                if m:
                    return m.group(1)
    except Exception:
        pass
    return None


def need_regenerate(proto_file, output_files, force=False):
    """基于 mtime 判断是否需要重新生成"""
    if force:
        return True
    proto_mtime = os.path.getmtime(proto_file)
    for out in output_files:
        if not os.path.exists(out) or os.path.getmtime(out) < proto_mtime:
            return True
    return False


def generate_python(proto_file, protoc, force=False):
    """生成 Python _pb2.py"""
    proto_dir = os.path.dirname(proto_file)
    filename = os.path.basename(proto_file)
    basename = os.path.splitext(filename)[0]
    out_py = os.path.join(proto_dir, basename + '_pb2.py')

    if not need_regenerate(proto_file, [out_py], force):
        print('  [skip py] {}'.format(filename))
        return True

    print('  [gen py] {}'.format(filename))

    cmd = [
        protoc,
        '-I', proto_dir,
        '--python_out', proto_dir,
        proto_file,
    ]
    try:
        subprocess.check_call(cmd, cwd=WORK_DIR)
        return True
    except subprocess.CalledProcessError as e:
        print('  [FAIL py] {} (exit={})'.format(filename, e.returncode))
        return False


def generate_csharp(proto_file, protoc, plugin, csharp_out, force=False):
    """生成 C# .cs 与自定义 RPC Service.cs"""
    proto_dir = os.path.dirname(proto_file)
    filename = os.path.basename(proto_file)
    basename = os.path.splitext(filename)[0]
    package = parse_proto_package(proto_file)

    output_files = [os.path.join(csharp_out, basename + '.cs')]
    if package:
        output_files.append(os.path.join(csharp_out, package + 'Service.cs'))

    if not need_regenerate(proto_file, output_files, force):
        print('  [skip cs] {}'.format(filename))
        return True

    print('  [gen cs] {}'.format(filename))

    if not os.path.isdir(csharp_out):
        os.makedirs(csharp_out, exist_ok=True)

    # 1) 生成标准 C# 消息类
    cmd_csharp = [
        protoc,
        '-I', proto_dir,
        '--csharp_out', csharp_out,
        proto_file,
    ]

    # 2) 生成自定义 RPC 存根
    cmd_rpc = [
        protoc,
        '-I', proto_dir,
        '--plugin=protoc-gen-custom=' + plugin,
        '--custom_out', csharp_out,
        proto_file,
    ]

    try:
        subprocess.check_call(cmd_csharp, cwd=WORK_DIR)
        subprocess.check_call(cmd_rpc, cwd=WORK_DIR)
        return True
    except subprocess.CalledProcessError as e:
        print('  [FAIL cs] {} (exit={})'.format(filename, e.returncode))
        return False


def collect_protos(root_dir):
    """递归收集所有 .proto 文件"""
    pattern = os.path.join(root_dir, '**', '*.proto')
    return sorted(glob.glob(pattern, recursive=True))


def default_csharp_out():
    """默认 C# 输出目录：assets/ 上四级 + Client/Assets/CSHotUpdate/Scripts/Proto"""
    return os.path.abspath(os.path.join(SCRIPT_DIR, '..', '..', '..', '..', 'Client', 'Assets', 'CSHotUpdate', 'Scripts', 'Proto'))


def main():
    parser = argparse.ArgumentParser(
        description='Generate protobuf Python code (and optional C# RPC code) for game server'
    )
    parser.add_argument(
        '--force', action='store_true',
        help='Force regeneration even if outputs are up-to-date'
    )
    parser.add_argument(
        '--csharp-out', default=None,
        help='C# output directory (default: {} relative to assets)'.format(default_csharp_out())
    )
    parser.add_argument(
        '--csharp-proto', action='append', default=[],
        help='Proto filename that also needs C# RPC generation (can be used multiple times)'
    )
    parser.add_argument(
        '--no-csharp', action='store_true',
        help='Skip C# code generation'
    )
    parser.add_argument(
        'proto', nargs='?',
        help='Generate only the specified proto file (absolute or relative path)'
    )
    args = parser.parse_args()

    protoc_python = get_protoc_python_path()
    protoc_csharp = get_protoc_csharp_path()
    csharp_plugin = ensure_csharp_rpc_plugin()

    csharp_out = args.csharp_out or default_csharp_out()
    csharp_proto_names = set(args.csharp_proto) if args.csharp_proto else set()
    csharp_proto_names.add('centralLogin.proto')  # 与旧 build_proto.bat 保持一致

    print('protoc (python) : {}'.format(protoc_python))
    print('protoc (csharp) : {}'.format(protoc_csharp))
    print('csharp plugin   : {}'.format(csharp_plugin))
    print('csharp out      : {}'.format(csharp_out))
    print('csharp protos   : {}'.format(sorted(csharp_proto_names)))
    print('work dir        : {}'.format(WORK_DIR))
    print('')

    if args.proto:
        proto_file = os.path.abspath(args.proto)
        if not os.path.isfile(proto_file):
            print('Error: proto file not found: {}'.format(proto_file))
            sys.exit(1)
        proto_files = [proto_file]
    else:
        src_root = os.path.abspath(os.path.join(SCRIPT_DIR, 'scripts', 'common', 'proto'))
        proto_files = collect_protos(src_root)
        print('Found {} proto files under {}'.format(len(proto_files), src_root))

    success = 0
    fail = 0

    for pf in proto_files:
        ok = True
        ok = generate_python(pf, protoc_python, force=args.force) and ok
        if not args.no_csharp and os.path.basename(pf) in csharp_proto_names:
            ok = generate_csharp(pf, protoc_csharp, csharp_plugin, csharp_out, force=args.force) and ok
        if ok:
            success += 1
        else:
            fail += 1

    # 清理临时包装器
    print('')
    if os.path.isfile(csharp_plugin):
        os.remove(csharp_plugin)
        print('Cleaned up temp wrapper: {}'.format(os.path.basename(csharp_plugin)))

    print('Done. Success: {}, Failed: {}'.format(success, fail))
    if fail > 0:
        sys.exit(1)


if __name__ == '__main__':
    main()
