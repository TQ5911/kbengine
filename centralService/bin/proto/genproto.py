#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
genproto.py - 统一生成微服务 Go 协议代码

扫描 centralService/src/ 下所有 .proto，自动生成 .pb.go 和 .rpc.go。
兼容 Windows / Linux，替代原有的硬编码 genproto.bat。

用法示例:
    python genproto.py                    # 全量扫描，增量生成（只重新生成变更过的 proto）
    python genproto.py --force            # 强制重新生成所有 proto（忽略文件修改时间）
    python genproto.py ../../src/dropServer/dropApp/gameServerService/gameServerDrop.proto
                                          # 只生成指定的单个 proto 文件

参数说明:
    --force     强制重新生成，不比较 proto 与输出文件的修改时间
    proto       位置参数，指定单个 proto 文件路径（绝对或相对路径均可）
                不传则自动扫描 src/ 目录下所有 .proto 文件

注意事项:
    - 本脚本仅生成 Go 代码（.pb.go + .rpc.go），不涉及 Python / C# 客户端代码
    - Python / C# 客户端代码由游戏服目录下的 build_proto.bat 统一生成
    - adminWebService.proto 会额外带上 plugins=grpc 生成
    - adminWebService.rpc.go 不会被生成（该服务不需要 trpc 包装代码）
    - 执行完毕后自动清理临时插件包装器文件
"""

import os
import sys
import glob
import stat
import platform
import subprocess
import argparse

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
WORK_DIR = SCRIPT_DIR  # 保持和旧 genproto.bat 一致的相对路径基准


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


def get_protoc_path():
    """定位 protoc 可执行文件"""
    candidates = [
        os.path.join(SCRIPT_DIR, 'protoc.exe'),
        os.path.join(SCRIPT_DIR, 'protoc-3.6.1-win32', 'bin', 'protoc.exe'),
    ]
    for c in candidates:
        if os.path.isfile(c):
            return c
    p = find_executable('protoc', [SCRIPT_DIR])
    if p:
        return p
    raise RuntimeError(
        'protoc not found. Please place protoc in {} or install it in PATH.'.format(SCRIPT_DIR)
    )


def get_protoc_gen_go_path():
    """定位 protoc-gen-go 插件"""
    p = find_executable('protoc-gen-go', [SCRIPT_DIR])
    if p:
        return p
    raise RuntimeError(
        'protoc-gen-go not found. Please place it in {} or install it in PATH.'.format(SCRIPT_DIR)
    )


def ensure_custom_plugin():
    """
    protoc --plugin 要求一个可执行文件包装器。
    我们在 bin/proto/ 下生成临时包装器，调用 customRpc.py 并传入 trpc 包路径。
    """
    custom_rpc_py = os.path.join(SCRIPT_DIR, 'customRpc.py')
    if not os.path.isfile(custom_rpc_py):
        raise RuntimeError('customRpc.py not found in {}'.format(SCRIPT_DIR))

    rpc_package_path = 'centralService/src/trpc'
    is_win = platform.system() == 'Windows'

    if is_win:
        wrapper = os.path.join(SCRIPT_DIR, '_rpc_plugin_wrapper.bat')
        with open(wrapper, 'w', encoding='utf-8') as f:
            f.write('@python "{}" {}\n'.format(custom_rpc_py, rpc_package_path))
        return wrapper
    else:
        wrapper = os.path.join(SCRIPT_DIR, '_rpc_plugin_wrapper.sh')
        with open(wrapper, 'w', encoding='utf-8') as f:
            f.write('#!/bin/sh\n')
            f.write('cd "$(dirname "$0")"\n')
            f.write('python3 customRpc.py {}\n'.format(rpc_package_path))
        os.chmod(wrapper, stat.S_IRWXU)
        return wrapper


def need_regenerate(proto_file, pb_go, rpc_go, force=False):
    """基于 mtime 判断是否需要重新生成"""
    if force:
        return True
    proto_mtime = os.path.getmtime(proto_file)
    if not os.path.exists(pb_go) or os.path.getmtime(pb_go) < proto_mtime:
        return True
    if not os.path.exists(rpc_go) or os.path.getmtime(rpc_go) < proto_mtime:
        return True
    return False


def generate_proto(proto_file, protoc, protoc_gen_go, custom_plugin, force=False):
    """
    对单个 proto 文件生成 .pb.go 和 .rpc.go
    """
    proto_dir = os.path.dirname(proto_file)
    filename = os.path.basename(proto_file)
    basename = os.path.splitext(filename)[0]

    pb_go = os.path.join(proto_dir, basename + '.pb.go')
    rpc_go = os.path.join(proto_dir, basename + '.rpc.go')

    if not need_regenerate(proto_file, pb_go, rpc_go, force):
        print('  [skip] {}'.format(filename))
        return True

    print('  [gen ] {}'.format(filename))

    # 所有路径都转为相对于 WORK_DIR (bin/proto/)，保持和旧 bat 完全一致
    rel_proto = os.path.relpath(proto_file, WORK_DIR)
    rel_proto_dir = os.path.dirname(rel_proto)

    # 1) 生成 .pb.go
    # adminWebService.proto 特殊处理：需要 grpc 插件
    if filename == 'adminWebService.proto':
        go_out_arg = 'plugins=grpc:' + rel_proto_dir
    else:
        go_out_arg = rel_proto_dir

    cmd_pb = [
        protoc,
        '-I' + rel_proto_dir,
        '--plugin=protoc-gen-go=' + protoc_gen_go,
        '--go_out=' + go_out_arg,
        rel_proto,
    ]

    # 2) 生成 .rpc.go（adminWebService 不需要）
    if filename != 'adminWebService.proto':
        cmd_rpc = [
            protoc,
            '-I' + rel_proto_dir,
            '--plugin=protoc-gen-custom=' + custom_plugin,
            '--custom_out=' + rel_proto_dir,
            rel_proto,
        ]
    else:
        cmd_rpc = None

    try:
        subprocess.check_call(cmd_pb, cwd=WORK_DIR)
        if cmd_rpc:
            subprocess.check_call(cmd_rpc, cwd=WORK_DIR)
        return True
    except subprocess.CalledProcessError as e:
        print('  [FAIL] {} (exit={})'.format(filename, e.returncode))
        return False


def collect_protos(root_dir):
    """递归收集所有 .proto 文件"""
    pattern = os.path.join(root_dir, '**', '*.proto')
    return sorted(glob.glob(pattern, recursive=True))


def main():
    parser = argparse.ArgumentParser(
        description='Generate Go protobuf code (.pb.go + .rpc.go) for centralService'
    )
    parser.add_argument(
        '--force', action='store_true',
        help='Force regeneration even if outputs are up-to-date'
    )
    parser.add_argument(
        'proto', nargs='?',
        help='Generate only the specified proto file (absolute or relative path)'
    )
    args = parser.parse_args()

    protoc = get_protoc_path()
    protoc_gen_go = get_protoc_gen_go_path()
    custom_plugin = ensure_custom_plugin()

    print('protoc         : {}'.format(protoc))
    print('protoc-gen-go  : {}'.format(protoc_gen_go))
    print('custom plugin  : {}'.format(custom_plugin))
    print('work dir       : {}'.format(WORK_DIR))
    print('')

    if args.proto:
        proto_file = os.path.abspath(args.proto)
        if not os.path.isfile(proto_file):
            print('Error: proto file not found: {}'.format(proto_file))
            sys.exit(1)
        proto_files = [proto_file]
    else:
        src_root = os.path.abspath(os.path.join(SCRIPT_DIR, '../../src'))
        proto_files = collect_protos(src_root)
        print('Found {} proto files under {}'.format(len(proto_files), src_root))

    success = 0
    fail = 0

    for pf in proto_files:
        if generate_proto(pf, protoc, protoc_gen_go, custom_plugin, force=args.force):
            success += 1
        else:
            fail += 1

    # 清理临时文件
    print('')
    if os.path.isfile(custom_plugin):
        os.remove(custom_plugin)
        print('Cleaned up temp wrapper: {}'.format(os.path.basename(custom_plugin)))

    # adminWebService 不需要 .rpc.go，若存在则删除（避免误提交）
    admin_rpc_go = os.path.abspath(os.path.join(
        SCRIPT_DIR, '../../src/adminServer/adminProto/webservice/adminWebService.rpc.go'
    ))
    if os.path.isfile(admin_rpc_go):
        os.remove(admin_rpc_go)
        print('Cleaned up adminWebService.rpc.go (not needed)')

    print('Done. Success: {}, Failed: {}'.format(success, fail))
    if fail > 0:
        sys.exit(1)


if __name__ == '__main__':
    main()
