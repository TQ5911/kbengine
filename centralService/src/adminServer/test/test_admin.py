#!/usr/bin/env python3
import requests
import json
import base64
import hashlib
import time
import datetime
import random
from concurrent.futures import ThreadPoolExecutor
from collections import Counter

def generate_sign(body: bytes, sign_key: str) -> str:
    """Generate MD5 signature for request body"""
    if not sign_key:
        return ""

    h = hashlib.md5()
    h.update(body)
    h.update(sign_key.encode('utf-8'))
    return h.hexdigest().lower()

def send_mail():
# title base 64 encode
    _cmd = '$sendglobalmail'

    _mail_id = 37001003
    _itemId_num = '30000236,1'
    _deps = ''
    _title = base64.b64encode('Test Title2'.encode('utf-8')).decode('utf-8')
    _content = base64.b64encode('Test Content'.encode('utf-8')).decode('utf-8')
    _start_time = '2022-01-01 00:00:00'
    # _start_time is int
    _start_time = int(datetime.datetime.strptime(_start_time, '%Y-%m-%d %H:%M:%S').timestamp())

    _end_time = '2026-01-01 01:00:00'
    # _end_time is int
    _end_time = int(datetime.datetime.strptime(_end_time, '%Y-%m-%d %H:%M:%S').timestamp())

    _min_level = 1
    _max_level = 99

    _channel = 1

    _args = f"{_mail_id} {_itemId_num} {_deps} {_title} {_content} {_start_time} {_end_time} {_min_level} {_max_level} {_channel}"                             # Command arguments

    return _cmd, _args

def official_msg():
    _cmd = '$gmPublishMarquee'
    _mid = 1
    _content = 'test'
    _startTime = int(time.time())
    _endTime = int(time.time()) + 3600
    _tick = 60
    _priority = 0
    _channels = 1
    _args = f"{_mid} {_content} {_startTime} {_endTime} {_tick} {_priority} {_channels}"                             # Command arguments
    return _cmd, _args

def ban_avatar():
    _cmd = '$banAvatar'
    #_gbId = '5692323899933458433'
    _gbId = '5692323864546954445'
    #_gbId = '5692323558839235377'
    _endTime = '1766284329'
    _args = f"{_gbId} {_endTime}"                             # Command arguments
    return _cmd, _args

def disban_avatar():
    _cmd = '$disbanAvatar'
    _gbId = '5692323864546954445'
    _args = f"{_gbId}"                             # Command arguments
    return _cmd, _args

def ban_chat():
    _cmd = '$setChatForbidden'
    _gbId = '5692323694627310797'
    _endTime = '180'
    _args = f"{_gbId} {_endTime}"                             # Command arguments
    return _cmd, _args

def add_buff():
    # $addbuff 0 64000002 1
    _cmd = '$addbuff'
    _id = 10058
    _buff_id = 64000002
    _num = 1
    _args = f"{_id} {_buff_id} {_num}"                             # Command arguments
    return _cmd, _args

def test_docmd():
    # -------------------------- CONFIGURATION --------------------------
    # Edit these parameters directly in the file:

    _cmd, _args = add_buff()
    print(f'{_cmd} {_args}')
    URL = "http://192.168.10.13:8080/docmd"           # Admin server docmd URL
    PARTITION = 20223                                  # Partition ID (0 for broadcast to all servers)
    COMMAND = _cmd
    ARGS = _args
    SEQID = int(time.time())                       # Sequence ID (current timestamp by default)
    SERIALNO = ""                                  # Serial number (optional)
    SIGN_KEY = "3Pi0ZsIoRha8h0MG6jfHdxG1WLcE7XplB0kzhFitVIZzUNIbKc871DMEZnHGygno"                                  # Signature key (if server requires signatures)
    TIMEOUT = 15                                   # Request timeout in seconds
    # -------------------------------------------------------------------

    # Use configured values
    url = URL
    partition = PARTITION
    command = COMMAND
    args = ARGS
    seqid = SEQID
    serialno = SERIALNO
    sign_key = SIGN_KEY
    timeout = TIMEOUT

    # Prepare request body - args need hex encoding as server uses bytes.fromhex(request.args).decode('utf-8')
    request_data = {
        "Partition": partition,
        "Command": command,
        "Args": args.encode('utf-8').hex(),
        "Seqid": seqid,
        "SerialNo": serialno
    }

    # Convert to JSON bytes
    body_str = json.dumps(request_data)
    body_bytes = body_str.encode('utf-8')

    # Generate signature if sign key provided
    sign = generate_sign(body_bytes, sign_key)
    params = {"sign": sign} if sign else {}

    print(f"Testing docmd interface:")
    print(f"URL: {url}")
    print(f"Request Body: {body_str}")
    if sign:
        print(f"Sign: {sign}")
    print("-" * 50)

    try:
        # Send POST request
        response = requests.post(
            url,
            params=params,
            data=body_bytes,
            headers={"Content-Type": "application/json"},
            timeout=timeout
        )

        print(f"Response Status: {response.status_code}")
        print(f"Response Headers: {dict(response.headers)}")
        print(f"Response Body: {response.text}")

        # Try to parse JSON response
        if response.headers.get("Content-Type", "").startswith("application/json"):
            try:
                response_json = response.json()
                print(f"Response JSON: {json.dumps(response_json, indent=2)}")
            except json.JSONDecodeError:
                print("Warning: Failed to parse response as JSON")

    except requests.exceptions.ConnectionError:
        print(f"Error: Cannot connect to {url}. Is the admin server running?")
    except requests.exceptions.Timeout:
        print(f"Error: Request timed out after {timeout} seconds")
    except Exception as e:
        print(f"Error: {str(e)}")

# ===================== 压测扩展（幂等专项） =====================
# 用法：python test_admin.py            # 默认跑压测
#       python test_admin.py single     # 跑原始单条测试
#
# 覆盖的幂等行为：
#   1. 同 SN 并发：pendingRequests 合并 + 缓存写入
#   2. 同 SN 顺序：idempotencyMap 读路径 + TTL 命中
#   3. 不同 SN 并发：互不干扰
#   4. 混合压测：高并发下幂等不失效

# 压测配置：直接修改下方参数即可
STRESS_CONFIG = {
    'url': 'http://192.168.10.13:8080/docmd',
    'partition': 20223,
    # 命令选择：
    #   只读命令（$getAllGMCmds / $getAllPlayers）：无副作用，推荐用于幂等测试
    #   写命令（$addbuff / $banAvatar）：有副作用，避免大量重放
    'command': '$getAllGMCmds',
    'args': '',
    'sign_key': '3Pi0ZsIoRha8h0MG6jfHdxG1WLcE7XplB0kzhFitVIZzUNIbKc871DMEZnHGygno',
    'timeout': 15,
    # 各场景规模
    'concurrent_same_sn': 50,    # 场景1：同 SN 并发线程数
    'sequential_same_sn': 10,    # 场景2：同 SN 顺序次数
    'different_sn_count': 30,    # 场景3：不同 SN 并发数
    'mixed_total': 200,          # 场景4：混合压测总请求数
    'mixed_concurrency': 50,     # 场景4：混合压测并发度
    'mixed_retry_groups': 5,     # 场景4：复用 SN 的分组数（模拟重试簇）
    'mixed_retry_ratio': 20,     # 场景4：复用请求占比（百分比）
}


def _build_body(command, args, partition, seqid, serialno):
    """构造请求体（bytes）"""
    data = {
        "Partition": partition,
        "Command": command,
        "Args": args.encode('utf-8').hex(),
        "Seqid": seqid,
        "SerialNo": serialno
    }
    return json.dumps(data).encode('utf-8')


def _send_request(session, url, body_bytes, sign_key, timeout):
    """发单个请求，返回 (status_code, body_bytes, latency_sec, err_str)"""
    sign = generate_sign(body_bytes, sign_key)
    params = {"sign": sign} if sign else {}
    start = time.time()
    try:
        resp = session.post(
            url, params=params, data=body_bytes,
            headers={"Content-Type": "application/json"},
            timeout=timeout
        )
        return (resp.status_code, resp.content, time.time() - start, None)
    except Exception as e:
        return (0, b"", time.time() - start, str(e))


def _make_session(pool_size):
    """构造带连接池的 Session，避免高并发下端口耗尽"""
    s = requests.Session()
    adapter = requests.adapters.HTTPAdapter(
        pool_connections=pool_size, pool_maxsize=pool_size
    )
    s.mount('http://', adapter)
    s.mount('https://', adapter)
    return s


def _pct(values, p):
    """百分位（线性插值的简化版）"""
    if not values:
        return 0.0
    s = sorted(values)
    k = max(0, min(len(s) - 1, int(len(s) * p / 100)))
    return s[k]


def _print_stats(latencies, errs):
    """打印单场景统计"""
    print(f"  成功: {len(latencies)}    失败: {len(errs)}")
    if errs:
        print(f"  错误样例:")
        for e in errs[:3]:
            print(f"    - {str(e)[:120]}")
    if latencies:
        ms = [l * 1000 for l in latencies]
        print(f"  延迟(ms): min={min(ms):.1f}  avg={sum(ms)/len(ms):.1f}  "
              f"p50={_pct(ms, 50):.1f}  p95={_pct(ms, 95):.1f}  "
              f"p99={_pct(ms, 99):.1f}  max={max(ms):.1f}")


def _check_server(cfg):
    """启动前检查 admin server 是否可达"""
    try:
        r = requests.get(cfg['url'].replace('/docmd', '/'), timeout=3)
        print(f"  [✓] admin server 可达 (status={r.status_code})")
        return True
    except Exception as e:
        print(f"  [✗] admin server 不可达: {e}")
        print(f"      请确认 {cfg['url']} 可访问")
        return False


# ----- 场景1：同 SN 并发 -----
# 目的：N 个线程同时打同一 SN，验证所有响应 body 完全一致
# 覆盖：pendingRequests 等待方合并 + finalResp 广播 + 缓存写入
def scenario_concurrent_same_sn(cfg):
    n = cfg['concurrent_same_sn']
    sn = f"stress-conc-{int(time.time()*1000)}"
    print()
    print("=" * 70)
    print(f"[场景1] 同 SN 并发：{n} 个线程打同一 SN")
    print(f"  SN   = {sn}")
    print(f"  期望 : 所有 {n} 个响应 body 完全一致（幂等核心）")

    body_bytes = _build_body(
        cfg['command'], cfg['args'], cfg['partition'],
        seqid=int(time.time()), serialno=sn
    )
    session = _make_session(n)

    def worker(_):
        return _send_request(session, cfg['url'], body_bytes,
                             cfg['sign_key'], cfg['timeout'])

    with ThreadPoolExecutor(max_workers=n) as ex:
        results = list(ex.map(worker, range(n)))
    session.close()

    statuses, bodies, latencies, errs = zip(*results)
    print(f"  状态码分布: {dict(Counter(statuses))}")

    # 校验：所有 200 响应的 body 必须完全一致
    ok_bodies = [b for s, b in zip(statuses, bodies) if s == 200]
    unique = set(ok_bodies)
    all_same = len(unique) == 1 and len(ok_bodies) > 0

    if all_same:
        print(f"  幂等校验: [✓] 通过 ({len(ok_bodies)} 个响应 body 完全一致)")
    else:
        print(f"  幂等校验: [✗] 失败 (出现 {len(unique)} 种不同 body)")
        # 打印差异样例辅助定位
        ref = ok_bodies[0] if ok_bodies else b""
        for i, b in enumerate(ok_bodies):
            if b != ref:
                print(f"    响应[0]: {ref[:200]}")
                print(f"    响应[{i}]: {b[:200]}")
                break

    _print_stats(list(latencies), list(errs))


# ----- 场景2：同 SN 顺序 -----
# 目的：连续发同一 SN，验证响应一致 + 后续请求走缓存（耗时降低）
# 覆盖：idempotencyMap 读路径 + 懒过期检查
def scenario_sequential_same_sn(cfg):
    n = cfg['sequential_same_sn']
    sn = f"stress-seq-{int(time.time()*1000)}"
    print()
    print("=" * 70)
    print(f"[场景2] 同 SN 顺序：连续 {n} 次同一 SN")
    print(f"  SN   = {sn}")
    print(f"  期望 : 所有响应 body 一致；首次耗时 > 后续（缓存命中）")

    session = _make_session(10)
    bodies = []
    latencies = []

    print(f"  {'序号':<6} {'状态':<8} {'耗时(ms)':<10}")
    print(f"  {'-' * 24}")
    for i in range(n):
        body_bytes = _build_body(
            cfg['command'], cfg['args'], cfg['partition'],
            seqid=int(time.time() * 1000) + i,  # seqid 递增以表示不同请求
            serialno=sn
        )
        status, body, lat, _ = _send_request(
            session, cfg['url'], body_bytes, cfg['sign_key'], cfg['timeout']
        )
        bodies.append(body)
        latencies.append(lat)
        print(f"  {i+1:<6} {status:<8} {lat * 1000:<10.1f}")

    session.close()

    unique = set(bodies)
    all_same = len(unique) == 1
    print(f"  幂等校验: {'[✓] 通过' if all_same else '[✗] 失败'} "
          f"({len(unique)} 种不同 body)")

    if n >= 2:
        first = latencies[0] * 1000
        rest_avg = sum(latencies[1:]) / (n - 1) * 1000
        print(f"  首次耗时  : {first:.1f}ms (实际执行)")
        print(f"  后续平均  : {rest_avg:.1f}ms (应明显低于首次)")

    _print_stats(latencies, [])


# ----- 场景3：不同 SN 并发 -----
# 目的：验证不同 SN 之间相互独立，不互相干扰
def scenario_different_sn_concurrent(cfg):
    n = cfg['different_sn_count']
    print()
    print("=" * 70)
    print(f"[场景3] 不同 SN 并发：{n} 个不同 SN 同时发送")
    print(f"  期望 : 每个 SN 独立处理；全部成功；状态码全 200")

    base_ts = int(time.time() * 1000)
    sns = [f"stress-diff-{base_ts}-{i}" for i in range(n)]
    body_map = {sn: _build_body(cfg['command'], cfg['args'], cfg['partition'],
                                seqid=base_ts, serialno=sn) for sn in sns}

    session = _make_session(n)

    def worker(sn):
        return sn, _send_request(session, cfg['url'], body_map[sn],
                                 cfg['sign_key'], cfg['timeout'])

    with ThreadPoolExecutor(max_workers=n) as ex:
        results = list(ex.map(worker, sns))
    session.close()

    sn_status = {sn: r[0] for sn, r in results}
    all_ok = all(s == 200 for s in sn_status.values())
    print(f"  状态码分布: {dict(Counter(sn_status.values()))}")
    print(f"  全部成功  : {'[✓]' if all_ok else '[✗]'}")

    latencies = [r[2] for _, r in results]
    errs = [r[3] for _, r in results if r[3]]
    _print_stats(latencies, errs)


# ----- 场景4：混合压测 -----
# 目的：模拟真实场景（独立请求 + 客户端重试复用 SN）
#       验证高并发下幂等不失效
def scenario_mixed(cfg):
    total = cfg['mixed_total']
    concurrency = cfg['mixed_concurrency']
    retry_groups = cfg['mixed_retry_groups']
    retry_ratio = cfg['mixed_retry_ratio']

    print()
    print("=" * 70)
    print(f"[场景4] 混合压测：总数 {total}，并发度 {concurrency}")
    print(f"  构造: {100 - retry_ratio}% 独立 SN + {retry_ratio}% 复用 "
          f"{retry_groups} 个 SN（模拟重试）")

    base_ts = int(time.time() * 1000)
    retry_count = total * retry_ratio // 100
    unique_count = total - retry_count

    # 复用 SN：模拟客户端对同一组命令的重试
    retry_sn_pool = [f"stress-mix-retry-{base_ts}-{i}" for i in range(retry_groups)]
    retry_sns = [random.choice(retry_sn_pool) for _ in range(retry_count)]
    # 独立 SN
    unique_sns = [f"stress-mix-uniq-{base_ts}-{i}" for i in range(unique_count)]
    all_sns = retry_sns + unique_sns
    random.shuffle(all_sns)

    body_map = {sn: _build_body(cfg['command'], cfg['args'], cfg['partition'],
                                seqid=base_ts, serialno=sn)
                for sn in set(all_sns)}

    session = _make_session(concurrency)

    def worker(sn):
        return sn, _send_request(session, cfg['url'], body_map[sn],
                                 cfg['sign_key'], cfg['timeout'])

    with ThreadPoolExecutor(max_workers=concurrency) as ex:
        results = list(ex.map(worker, all_sns))
    session.close()

    # 按 SN 分组收集响应
    sn_bodies = {}
    for sn, (status, body, lat, err) in results:
        sn_bodies.setdefault(sn, []).append(body)

    # 校验：每个复用 SN 收到的所有 body 必须一致
    violations = []
    for sn in retry_sn_pool:
        if sn in sn_bodies:
            bodies = sn_bodies[sn]
            unique = set(bodies)
            if len(unique) > 1:
                violations.append((sn, len(bodies), len(unique)))

    latencies = [r[2] for _, r in results]
    statuses = [r[0] for _, r in results]
    errs = [r[3] for _, r in results if r[3]]

    print(f"  状态码分布  : {dict(Counter(statuses))}")
    print(f"  复用 SN 数  : {len(retry_sn_pool)}")
    print(f"  复用请求总数: {retry_count}")
    print(f"  幂等违规    : {len(violations)} "
          f"{'[✓] 通过' if not violations else '[✗] 失败'}")
    if violations:
        for sn, cnt, uniq in violations[:3]:
            print(f"    - {sn}: {cnt} 次请求，{uniq} 种不同 body")

    _print_stats(latencies, errs)


def stress_test():
    cfg = STRESS_CONFIG
    print("=" * 70)
    print(" adminServer 幂等压测")
    print("=" * 70)
    print(f"  目标: {cfg['url']}")
    print(f"  命令: {cfg['command']} (args={cfg['args']!r})")
    print(f"  分区: {cfg['partition']}")

    if not _check_server(cfg):
        return

    scenario_concurrent_same_sn(cfg)
    scenario_sequential_same_sn(cfg)
    scenario_different_sn_concurrent(cfg)
    scenario_mixed(cfg)

    print()
    print("=" * 70)
    print(" 全部场景完成")
    print("=" * 70)


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == 'single':
        test_docmd()
    else:
        stress_test()
