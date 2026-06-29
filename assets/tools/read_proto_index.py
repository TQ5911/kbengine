#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
从 _pb2.py 文件中读取 service / method 的 index 和参数类型信息，支持导出为 lua 格式。

采用 ast 静态解析方式，不依赖 google.protobuf 运行库。

用法:
    python read_proto_index.py <pb2_file> [service] [method] [options]

选项:
    --lua                       以 lua 格式输出（默认含 method -> arg 映射）
    -o FILE / --output FILE     输出到指定文件（默认输出到 stdout）
    --dir DIR --out-dir DIR     批量处理目录下所有 *_pb2.py，输出到指定目录
    --prefix PREFIX             批量导出时 lua 表名前缀（默认 "ProtoIndex"）
    --no-args                   lua 模式下不输出 method -> arg 映射

示例:
    # 文本输出
    python read_proto_index.py scripts/common/proto/centralLogin_pb2.py
    python read_proto_index.py scripts/common/proto/centralLogin_pb2.py CentralServer
    python read_proto_index.py scripts/common/proto/centralLogin_pb2.py CentralServer loginByPassword

    # 导出单个 lua（带 method -> arg 映射）
    python read_proto_index.py scripts/common/proto/centralLogin_pb2.py --lua -o lua_proto/centralLogin.lua

    # 批量导出整个目录
    python read_proto_index.py --dir scripts/common/proto --out-dir lua_proto
"""

import argparse
import ast
import os
import sys


def _get_call_func_name(func_node):
    """提取函数调用的最终名字（兼容 Name 和 Attribute 两种形式）"""
    if isinstance(func_node, ast.Name):
        return func_node.id
    if isinstance(func_node, ast.Attribute):
        return func_node.attr
    return None


def _extract_const_str(kw_node):
    """从关键字参数中提取字符串常量值"""
    if kw_node is None:
        return None
    if isinstance(kw_node.value, ast.Constant) and isinstance(kw_node.value.value, str):
        return kw_node.value.value
    return None


def _extract_const_int(kw_node):
    """从关键字参数中提取整型常量值"""
    if kw_node is None:
        return None
    if isinstance(kw_node.value, ast.Constant) and isinstance(kw_node.value.value, int):
        return kw_node.value.value
    return None


def _extract_name_id(kw_node):
    """从关键字参数中提取 Name 节点的 id（用于 input_type=_XXX 这类引用）"""
    if kw_node is None:
        return None
    if isinstance(kw_node.value, ast.Name):
        return kw_node.value.id
    return None


def _build_type_name_map(tree):
    """扫描 _descriptor.Descriptor(...) 调用，建立 变量名 -> proto 类型名 的映射。
    例如: _LOGINKEYREQUEST -> "LoginKeyRequest"
    """
    type_map = {}
    for node in ast.walk(tree):
        if not isinstance(node, ast.Assign):
            continue
        if not isinstance(node.value, ast.Call):
            continue
        if _get_call_func_name(node.value.func) != "Descriptor":
            continue
        if not node.targets:
            continue
        target = node.targets[0]
        if not isinstance(target, ast.Name):
            continue
        for kw in node.value.keywords:
            if kw.arg == "name":
                proto_name = _extract_const_str(kw)
                if proto_name:
                    type_map[target.id] = proto_name
                break
    return type_map


def parse_pb2_file(pb2_path):
    """通过 ast 解析 _pb2.py 文件中的 service / method 信息。
    返回: { service_name: [ {name, index, input, output}, ... ] }
    """
    with open(pb2_path, "r", encoding="utf-8") as f:
        source = f.read()

    try:
        tree = ast.parse(source)
    except SyntaxError as e:
        print("错误: 解析 {0} 失败: {1}".format(pb2_path, e), file=sys.stderr)
        return None

    type_map = _build_type_name_map(tree)
    services = {}

    for node in ast.walk(tree):
        if not isinstance(node, ast.Assign):
            continue
        value = node.value
        if not isinstance(value, ast.Call):
            continue
        if _get_call_func_name(value.func) != "ServiceDescriptor":
            continue

        service_name = None
        methods = []

        for kw in value.keywords:
            if kw.arg == "name":
                service_name = _extract_const_str(kw)
            elif kw.arg == "methods" and isinstance(kw.value, ast.List):
                for elt in kw.value.elts:
                    if not isinstance(elt, ast.Call):
                        continue
                    if _get_call_func_name(elt.func) != "MethodDescriptor":
                        continue
                    method_name = None
                    method_index = None
                    input_var = None
                    output_var = None
                    for mkw in elt.keywords:
                        if mkw.arg == "name":
                            method_name = _extract_const_str(mkw)
                        elif mkw.arg == "index":
                            method_index = _extract_const_int(mkw)
                        elif mkw.arg == "input_type":
                            input_var = _extract_name_id(mkw)
                        elif mkw.arg == "output_type":
                            output_var = _extract_name_id(mkw)
                    if method_name is None or method_index is None:
                        continue
                    input_type = type_map.get(input_var, input_var)
                    output_type = type_map.get(output_var, output_var)
                    methods.append({
                        "name": method_name,
                        "index": method_index,
                        "input": input_type,
                        "output": output_type,
                    })

        if service_name:
            services[service_name] = methods

    return services


def format_text_all(services):
    lines = []
    for name, methods in services.items():
        lines.append("service {0}:".format(name))
        for m in methods:
            lines.append("  {0}: index={1}, input={2}, output={3}".format(
                m["name"], m["index"], m["input"], m["output"]))
        lines.append("")
    return "\n".join(lines)


def format_text_service(services, svc_name):
    if svc_name not in services:
        return None
    lines = ["service {0}:".format(svc_name)]
    for m in services[svc_name]:
        lines.append("  {0}: index={1}, input={2}, output={3}".format(
            m["name"], m["index"], m["input"], m["output"]))
    return "\n".join(lines)


def _lua_safe_name(name):
    """将 service / method 名字转成 lua 合法标识符"""
    safe = []
    for ch in name:
        if ch.isalnum() or ch == "_":
            safe.append(ch)
        else:
            safe.append("_")
    out = "".join(safe)
    if out and out[0].isdigit():
        out = "_" + out
    return out


def _lua_quote(s):
    """lua 字符串字面量转义"""
    if s is None:
        return "nil"
    escaped = s.replace("\\", "\\\\").replace('"', '\\"')
    return '"{0}"'.format(escaped)


def format_lua(services, prefix="ProtoIndex", with_args=True):
    """生成 lua 表文本"""
    lines = []
    lines.append("-- Auto generated from _pb2.py, do not edit.")
    lines.append("")
    lines.append("local M = {}")
    lines.append("")

    for svc_name, methods in services.items():
        svc_key = _lua_safe_name(svc_name)
        if not methods:
            continue
        lines.append("M.{0} = {{".format(svc_key))
        lines.append("    -- {0}".format(svc_name))
        for m in methods:
            m_key = _lua_safe_name(m["name"])
            lines.append("    {0} = {1},".format(m_key, m["index"]))
        lines.append("}")
        lines.append("")

        if with_args:
            lines.append("M.{0}Args = {{".format(svc_key))
            lines.append("    -- method -> input message name (one arg per method)")
            for m in methods:
                m_key = _lua_safe_name(m["name"])
                lines.append("    {0} = {1},".format(
                    m_key, _lua_quote(m["input"])))
            lines.append("}")
            lines.append("")

            lines.append("M.{0}Method = {{".format(svc_key))
            lines.append("    -- method -> { input, output }")
            for m in methods:
                m_key = _lua_safe_name(m["name"])
                lines.append("    {0} = {{ input = {1}, output = {2} }},".format(
                    m_key, _lua_quote(m["input"]), _lua_quote(m["output"])))
            lines.append("}")
            lines.append("")

    lines.append("M.byFullName = {")
    for svc_name, methods in services.items():
        for m in methods:
            full = "{0}.{1}".format(svc_name, m["name"])
            lines.append('    ["{0}"] = {1},'.format(full, m["index"]))
    lines.append("}")
    lines.append("")

    if with_args:
        lines.append("M.byFullNameArgs = {")
        for svc_name, methods in services.items():
            for m in methods:
                full = "{0}.{1}".format(svc_name, m["name"])
                lines.append('    ["{0}"] = {1},'.format(full, _lua_quote(m["input"])))
        lines.append("}")
        lines.append("")

    lines.append("return M")
    return "\n".join(lines) + "\n"


def write_output(path, content):
    """输出到文件或 stdout"""
    if path:
        out_dir = os.path.dirname(os.path.abspath(path))
        if out_dir and not os.path.exists(out_dir):
            os.makedirs(out_dir)
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        print("已写入: {0}".format(path), file=sys.stderr)
    else:
        sys.stdout.write(content)


def run_single(args):
    if not os.path.exists(args.pb2_file):
        print("错误: 文件不存在: {0}".format(args.pb2_file), file=sys.stderr)
        return 1

    services = parse_pb2_file(args.pb2_file)
    if not services:
        print("在 {0} 中未找到任何 service 信息".format(args.pb2_file), file=sys.stderr)
        return 1

    if args.lua:
        if args.service:
            print("警告: lua 模式会忽略 service / method 过滤，输出全部内容",
                  file=sys.stderr)
        content = format_lua(services, prefix=args.prefix, with_args=args.args)
        write_output(args.output, content)
        return 0

    if args.method:
        if args.service not in services:
            print("错误: 未找到 service '{0}'".format(args.service), file=sys.stderr)
            return 1
        for m in services[args.service]:
            if m["name"] == args.method:
                write_output(args.output, "{0}\n".format(m["index"]))
                return 0
        print("错误: 未找到 method '{0}' (in service '{1}')".format(
            args.method, args.service), file=sys.stderr)
        return 1
    if args.service:
        content = format_text_service(services, args.service)
        if content is None:
            print("错误: 未找到 service '{0}'".format(args.service), file=sys.stderr)
            print("可用的 service:", file=sys.stderr)
            for n in services:
                print("  {0}".format(n), file=sys.stderr)
            return 1
        write_output(args.output, content + "\n")
        return 0

    content = format_text_all(services)
    write_output(args.output, content)
    return 0


def run_batch(args):
    if not os.path.isdir(args.dir):
        print("错误: 目录不存在: {0}".format(args.dir), file=sys.stderr)
        return 1
    if not os.path.exists(args.out_dir):
        os.makedirs(args.out_dir)

    files = sorted(
        os.path.join(args.dir, f)
        for f in os.listdir(args.dir)
        if f.endswith("_pb2.py")
    )
    if not files:
        print("在 {0} 中未找到任何 *_pb2.py 文件".format(args.dir), file=sys.stderr)
        return 1

    rc_total = 0
    for pb2_path in files:
        services = parse_pb2_file(pb2_path)
        if not services:
            print("跳过(无service): {0}".format(pb2_path), file=sys.stderr)
            continue
        base = os.path.basename(pb2_path)[:-len("_pb2.py")]
        out_path = os.path.join(args.out_dir, base + ".lua")
        content = format_lua(services, prefix=args.prefix, with_args=args.args)
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(content)
        print("已写入: {0}".format(out_path), file=sys.stderr)
    return rc_total


def main():
    parser = argparse.ArgumentParser(
        description="从 _pb2.py 文件中读取 service / method 的 index 和参数类型，支持导出 lua。",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("pb2_file", nargs="?", help="_pb2.py 文件路径")
    parser.add_argument("service", nargs="?", help="service 名称（可选）")
    parser.add_argument("method", nargs="?", help="method 名称（可选）")
    parser.add_argument("--lua", action="store_true", help="以 lua 格式输出")
    parser.add_argument("-o", "--output", dest="output", default=None,
                        help="输出文件路径（默认 stdout）")
    parser.add_argument("--dir", dest="dir", default=None,
                        help="批量处理的 _pb2.py 所在目录")
    parser.add_argument("--out-dir", dest="out_dir", default=None,
                        help="批量导出时的输出目录")
    parser.add_argument("--prefix", dest="prefix", default="ProtoIndex",
                        help="lua 表名前缀（默认 ProtoIndex）")
    parser.add_argument("--no-args", dest="args", action="store_false",
                        help="lua 模式下不输出 method -> arg 映射")
    parser.set_defaults(args=True)
    args = parser.parse_args()

    if args.dir or args.out_dir:
        if not (args.dir and args.out_dir):
            print("错误: 批量模式需要同时指定 --dir 和 --out-dir", file=sys.stderr)
            return 1
        return run_batch(args)

    if not args.pb2_file:
        parser.print_help(sys.stderr)
        return 1

    return run_single(args)


if __name__ == "__main__":
    sys.exit(main())
