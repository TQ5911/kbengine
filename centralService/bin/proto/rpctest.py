#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
rpctest.py - trpc 通用 CLI 测试工具

通过动态反射读取 .proto，构造 JSON 请求并按 trpc 协议发送，
同时保持连接监听异步回调（GameServer / GameClient）。

用法示例：
    # 基本用法：发送请求并监听回调（Ctrl+C 退出）
    python rpctest.py \
        --proto src/dropServer/dropApp/gameServerService/gameServerDrop.proto \
        --service DropServer \
        --method drop \
        --addr 127.0.0.1:20001 \
        --json '{"serverId":1,"uniqueId":123}'

    # 只发送请求，不监听回调，发完即断开
    python rpctest.py ... --no-listen

    # 自定义回调监听 service + 10秒超时自动退出
    python rpctest.py ... --listen-service GameServer --listen-timeout 10

    # 从文件读取 JSON 请求体（替代 --json，适合复杂 JSON 或 Windows 命令行转义困难时）
    python rpctest.py ... --json-file req.json

参数说明：
    --proto              必填  .proto 文件路径
    --service            必填  要调用的目标 service（如 DropServer）
    --method             必填  要调用的目标 method（如 drop）
    --addr               必填  服务端地址，格式为 host:port（如 127.0.0.1:20001）
    --json               可选  请求 JSON 字符串，默认 '{}'
    --json-file          可选  从文件读取 JSON 请求体（与 --json 二选一）
    --listen-service     可选  指定回调 service 名称；默认自动检测 GameServer / GameClient
    --listen-timeout     可选  监听超时秒数，默认无限监听（按 Ctrl+C 手动退出）
    --no-listen          可选  只发送请求，不进入接收循环，发完后直接断开连接

注意事项：
    - trpc 是异步单向协议，服务端回包通过同一条 TCP 连接的反向 service 下发
    - 工具会自动在 proto 中查找 GameServer / GameClient 作为默认监听对象
    - JSON 解析失败时会打印实际收到的字符串，方便排查命令行引号转义问题
    - 内部依赖 protoc 生成临时二进制描述符，退出时自动清理
"""

import os
import struct
import socket
import argparse
import tempfile
import subprocess

from google.protobuf import descriptor_pb2
from google.protobuf import descriptor_pool
from google.protobuf import message_factory
from google.protobuf import json_format

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))


def find_executable(name, search_dirs=None):
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


def generate_descriptor(proto_file, protoc):
    """调用 protoc 生成临时的二进制 FileDescriptorSet"""
    proto_dir = os.path.dirname(os.path.abspath(proto_file))
    fd, tmp_pb = tempfile.mkstemp(suffix='.pb')
    os.close(fd)

    cmd = [
        protoc,
        '-I' + proto_dir,
        '--descriptor_set_out=' + tmp_pb,
        '--include_imports',
        os.path.abspath(proto_file),
    ]
    subprocess.check_call(cmd)
    return tmp_pb


def load_descriptor(tmp_pb):
    """加载 FileDescriptorSet，返回 (pool, message_factory, file_descriptor)"""
    with open(tmp_pb, 'rb') as f:
        fds = descriptor_pb2.FileDescriptorSet()
        fds.ParseFromString(f.read())

    pool = descriptor_pool.DescriptorPool()
    for fd in fds.file:
        pool.Add(fd)

    factory = message_factory.MessageFactory(pool)
    return pool, factory, fds.file[0]


def get_message_class(pool, factory, full_name):
    """根据 fully qualified name 获取 Message 类"""
    name = full_name.lstrip('.')
    desc = pool.FindMessageTypeByName(name)
    return factory.GetPrototype(desc)


def find_service(file_desc, service_name):
    for svc in file_desc.service:
        if svc.name == service_name:
            return svc
    return None


def find_method(svc, method_name):
    for idx, m in enumerate(svc.method):
        if m.name == method_name:
            return m, idx
    return None, -1


def send_request(sock, method_idx, msg):
    """按 trpc 协议发送请求：4字节 length + 2字节 index + protobuf payload"""
    msg_data = msg.SerializeToString()
    payload = struct.pack('<H', method_idx) + msg_data
    packet = struct.pack('<I', len(payload)) + payload
    sock.sendall(packet)


def recv_all(sock, n):
    buf = b''
    while len(buf) < n:
        chunk = sock.recv(n - len(buf))
        if not chunk:
            return None
        buf += chunk
    return buf


def recv_loop(sock, listen_svc, pool, factory, timeout=None):
    """保持连接，读取并打印回调消息"""
    sock.settimeout(timeout)
    try:
        while True:
            len_bytes = recv_all(sock, 4)
            if len_bytes is None:
                print('[disconnect] connection closed by remote')
                break

            length = struct.unpack('<I', len_bytes)[0]
            payload = recv_all(sock, length)
            if payload is None:
                print('[disconnect] connection closed by remote')
                break

            method_idx = struct.unpack('<H', payload[:2])[0]
            msg_data = payload[2:]

            if method_idx >= len(listen_svc.method):
                print('[warn] unknown method index: {}'.format(method_idx))
                continue

            method = listen_svc.method[method_idx]
            msg_class = get_message_class(pool, factory, method.input_type)
            msg = msg_class()
            msg.ParseFromString(msg_data)

            print('[recv] {}.{}: {}'.format(
                listen_svc.name,
                method.name,
                json_format.MessageToJson(msg, preserving_proto_field_name=True)
            ))
    except socket.timeout:
        print('[timeout] listen timeout')
    except KeyboardInterrupt:
        print('\n[exit] interrupted by user')


def list_services(file_desc):
    return [s.name for s in file_desc.service]


def list_methods(svc):
    return ['{}.{}'.format(svc.name, m.name) for m in svc.method]


def main():
    parser = argparse.ArgumentParser(description='trpc CLI test tool')
    parser.add_argument('--proto', required=True, help='Path to .proto file')
    parser.add_argument('--service', required=True, help='Target service to call (e.g. DropServer)')
    parser.add_argument('--method', required=True, help='Target method to call (e.g. Drop)')
    parser.add_argument('--addr', required=True, help='Server address, e.g. 127.0.0.1:20001')
    parser.add_argument('--json', default='{}', help='Request JSON payload (default: {})')
    parser.add_argument('--json-file', help='Path to file containing JSON payload (alternative to --json)')
    parser.add_argument('--listen-service', help='Callback service to listen (default: auto-detect GameServer/GameClient)')
    parser.add_argument('--listen-timeout', type=float, help='Listen timeout in seconds (default: infinite, Ctrl+C to stop)')
    parser.add_argument('--no-listen', action='store_true', help='Send request and exit immediately')
    args = parser.parse_args()

    protoc = get_protoc_path()
    tmp_pb = generate_descriptor(args.proto, protoc)

    try:
        pool, factory, file_desc = load_descriptor(tmp_pb)

        # 1. 查找发送 service / method
        send_svc = find_service(file_desc, args.service)
        if not send_svc:
            available = list_services(file_desc)
            raise RuntimeError(
                'service "{}" not found. available: {}'.format(args.service, available)
            )

        method, method_idx = find_method(send_svc, args.method)
        if not method:
            available = list_methods(send_svc)
            raise RuntimeError(
                'method "{}" not found in {}. available: {}'.format(
                    args.method, args.service, available)
            )

        # 2. 构造请求消息
        req_class = get_message_class(pool, factory, method.input_type)
        req_msg = req_class()

        if args.json_file:
            with open(args.json_file, 'r', encoding='utf-8') as f:
                json_str = f.read()
        else:
            json_str = args.json

        try:
            json_format.Parse(json_str, req_msg, ignore_unknown_fields=True)
        except Exception as e:
            print('[error] failed to parse JSON: {}'.format(e))
            print('[error] received JSON string: {}'.format(repr(json_str)))
            raise

        # 3. 确定监听 service
        listen_svc = None
        if not args.no_listen:
            listen_name = args.listen_service
            if not listen_name:
                for svc in file_desc.service:
                    if svc.name in ('GameServer', 'GameClient'):
                        listen_name = svc.name
                        break

            if listen_name:
                listen_svc = find_service(file_desc, listen_name)
                if not listen_svc:
                    available = list_services(file_desc)
                    raise RuntimeError(
                        'listen service "{}" not found. available: {}'.format(
                            listen_name, available)
                    )

        # 4. 连接并发送
        host, port = args.addr.rsplit(':', 1)
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((host, int(port)))

        send_request(sock, method_idx, req_msg)
        print('[send] {}.{} -> {}'.format(args.service, args.method, args.addr))

        # 5. 监听或退出
        if args.no_listen:
            print('[done] --no-listen set, closing connection')
            sock.close()
            return

        if listen_svc:
            print('[listen] waiting for {} callbacks (Ctrl+C to stop)...'.format(listen_svc.name))
            recv_loop(sock, listen_svc, pool, factory, timeout=args.listen_timeout)
        else:
            print('[warn] no listen service detected; use --listen-service to specify or --no-listen to skip')

        sock.close()

    finally:
        if os.path.isfile(tmp_pb):
            os.remove(tmp_pb)


if __name__ == '__main__':
    main()
