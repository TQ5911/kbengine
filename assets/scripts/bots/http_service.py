import threading
from http.server import BaseHTTPRequestHandler, HTTPServer
from socketserver import ThreadingMixIn
import json
import time
from urllib.parse import urlparse, parse_qs
import global_data


# ----------------------- Routing helpers -----------------------
def _send_text(handler: BaseHTTPRequestHandler, text: str, status: int = 200):
    body = text.encode('utf-8')
    handler.send_response(status)
    handler.send_header('Content-Type', 'text/plain; charset=utf-8')
    handler.send_header('Content-Length', str(len(body)))
    handler.end_headers()
    handler.wfile.write(body)


def _send_json(handler: BaseHTTPRequestHandler, data, status: int = 200):
    body = json.dumps(data, ensure_ascii=False).encode('utf-8')
    handler.send_response(status)
    handler.send_header('Content-Type', 'application/json; charset=utf-8')
    handler.send_header('Content-Length', str(len(body)))
    handler.end_headers()
    handler.wfile.write(body)


def route_health(handler: BaseHTTPRequestHandler, parsed):
    _send_text(handler, 'OK', 200)


def route_account_count(handler: BaseHTTPRequestHandler, parsed):
    count = get_account_count() if hasattr(global_data, 'account_map') else 0
    _send_text(handler, str(count), 200)


def route_clients_count(handler: BaseHTTPRequestHandler, parsed):
    total = len(global_data.client_dic) if hasattr(global_data, 'client_dic') else 0
    _send_text(handler, str(total), 200)


def route_rpc_stats(handler: BaseHTTPRequestHandler, parsed):
    gd_stats = getattr(global_data, 'rpc_call_statistics', {})
    if isinstance(gd_stats, dict):
        stats = {str(k): int(v) for k, v in gd_stats.items()}
    else:
        stats = {}
    _send_json(handler, stats, 200)


def route_clients_slow(handler: BaseHTTPRequestHandler, parsed):
    q = parse_qs(parsed.query or '')
    try:
        age = float(q.get('age', ['20'])[0])
    except Exception:
        age = 20.0
    now = time.time()
    items = []
    for acc, rec in list(global_data.client_dic.items()):
        if (now - rec.tickTime) > age:
            items.append({
                'account': acc,
                'tickTime': rec.tickTime,
                'seconds_since_last_tick': round(now - rec.tickTime, 3)
            })
    _send_json(handler, {'age': age, 'count': len(items), 'clients': items}, 200)


def route_clients_noclient(handler: BaseHTTPRequestHandler, parsed):
    if not hasattr(global_data, 'client_dic'):
        raise AttributeError('global_data.client_dic is missing')
    result = []
    for acc, rec in list(global_data.client_dic.items()):
        if hasattr(rec, 'client'):
            client_obj = rec.client
        elif isinstance(rec, dict):
            client_obj = rec.get('client')
        else:
            raise TypeError(f'unexpected client_dic value for {acc}: {type(rec)}')
        if not client_obj:
            result.append({'account': str(acc), 'client': str(client_obj)})
    _send_json(handler, {'count': len(result), 'clients': result}, 200)


# ----------------------- Remote Call routes -----------------------
def route_execute(handler: BaseHTTPRequestHandler, parsed):
    """统一的远程执行接口
    
    参考 simpleBotBase.py 的 onRecvAvatarChannelMsg 方法
    
    参数:
        method: 要执行的命令/代码 (必需)
        accounts: 指定账号列表，JSON数组格式 (可选，不指定则对所有客户端执行)
    
    示例:
        # GM命令（包含$符号）- 所有机器人
        /execute?method=$setlv 0 20
        
        # Python代码（包含self.）
        /execute?method=self.base.someMethod()
        /execute?method=self.cell.teleport(100,200,300)
        
        # 对指定账号列表执行
        /execute?method=$setlv 0 20&accounts=["bot1","bot2","bot3"]
    """
    q = parse_qs(parsed.query or '')
    method = q.get('method', [None])[0]
    accounts_str = q.get('accounts', [None])[0]
    
    # 参数验证
    if not method:
        _send_json(handler, {'error': 'method required'}, 400)
        return
    
    # 解析账号列表
    accounts = None
    if accounts_str:
        try:
            accounts = json.loads(accounts_str)
            if not isinstance(accounts, list):
                _send_json(handler, {'error': 'accounts must be a JSON array'}, 400)
                return
        except Exception as e:
            _send_json(handler, {'error': f'invalid accounts format: {e}'}, 400)
            return
    
    # 执行命令
    results = _execute_command_on_clients(method, accounts)
    _send_json(handler, results, 200)


def _execute_command_on_clients(command, accounts=None):
    """在客户端上执行命令
    
    参考 simpleBotBase.py 的处理逻辑：
    1. 如果包含 $ 符号 → 执行GM命令
    2. 如果包含 self. → 执行Python代码
    
    Args:
        command: 要执行的命令/代码字符串
        accounts: 指定账号列表，None表示所有客户端
    
    Returns:
        {'success': bool, 'results': [...], 'errors': [...]}
    """
    print(f"[HTTP_EXECUTE] 开始执行命令: {command}")
    print(f"[HTTP_EXECUTE] 目标账号: {accounts if accounts else '所有客户端'}")
    
    if not hasattr(global_data, 'client_dic'):
        print(f"[HTTP_EXECUTE] 错误: client_dic 不可用")
        return {'success': False, 'error': 'client_dic not available'}
    
    client_dic = global_data.client_dic
    print(f"[HTTP_EXECUTE] client_dic 总数: {len(client_dic)}")
    
    # 确定要执行的客户端列表
    if accounts:
        # 指定了账号列表
        target_clients = {}
        not_found = []
        for acc in accounts:
            if acc in client_dic:
                target_clients[acc] = client_dic[acc]
            else:
                not_found.append(acc)
        
        if not_found:
            print(f"[HTTP_EXECUTE] 警告: {len(not_found)} 个账号未找到: {not_found[:3]}")
        print(f"[HTTP_EXECUTE] 指定模式: 找到 {len(target_clients)}/{len(accounts)} 个目标账号")
    else:
        # 所有客户端
        target_clients = dict(client_dic)
        print(f"[HTTP_EXECUTE] 广播模式: {len(target_clients)} 个客户端")
    
    results = []
    errors = []
    
    for acc, rec in target_clients.items():
        try:
            # rec 是 BotClient 实例
            # BotClient 有 player 属性（property），player 才有 base 和 cell
            rec_type = type(rec).__name__
            
            # 获取 player 对象
            player = rec.player if hasattr(rec, 'player') else None
            if not player:
                errors.append({
                    'account': acc,
                    'error': 'player not available (client not logged in?)'
                })
                continue
            
            # 判断执行类型并执行
            if '$' in command:
                # GM命令：通过 player.base.runGmCommand 调用
                try:
                    print(f"[HTTP_EXECUTE] {acc} ({rec_type}): 执行GM命令")
                    player.base.runGmCommand(command)
                    print(f"[HTTP_EXECUTE] {acc}: GM命令执行成功")
                    results.append({
                        'account': acc,
                            'success': True,
                        'type': 'gm',
                        'command': command
                    })
                except AttributeError as e:
                    error_msg = f'base not available: {str(e)}'
                    print(f"[HTTP_EXECUTE] {acc}: 失败 - {error_msg}")
                    errors.append({
                        'account': acc,
                        'error': error_msg
                        })
                except Exception as e:
                    error_msg = f'GM command error: {type(e).__name__}: {str(e)}'
                    print(f"[HTTP_EXECUTE] {acc}: 失败 - {error_msg}")
                    errors.append({
                        'account': acc,
                        'error': error_msg
                    })
                    
            elif 'self.' in command:
                # Python代码：使用exec执行，self 指向 player
                # 这样可以执行 self.base.xxx() 和 self.cell.xxx()
                try:
                    print(f"[HTTP_EXECUTE] {acc} ({rec_type}): 执行Python代码")
                    exec(command, {'self': player})
                    print(f"[HTTP_EXECUTE] {acc}: Python代码执行成功")
                    results.append({
                        'account': acc,
                            'success': True,
                        'type': 'code',
                        'command': command
                        })
                except Exception as e:
                    error_msg = f'exec error: {type(e).__name__}: {str(e)}'
                    print(f"[HTTP_EXECUTE] {acc}: 失败 - {error_msg}")
                    errors.append({
                        'account': acc,
                        'error': error_msg
                    })
            else:
                error_msg = 'invalid command format (must contain $ or self.)'
                print(f"[HTTP_EXECUTE] {acc}: 失败 - {error_msg}")
                errors.append({
                    'account': acc,
                    'error': error_msg
                })
            
        except Exception as e:
            error_msg = f'{type(e).__name__}: {str(e)}'
            print(f"[HTTP_EXECUTE] {acc}: 异常 - {error_msg}")
            errors.append({
                'account': acc,
                'error': error_msg
            })
    
    # 汇总日志
    print(f"[HTTP_EXECUTE] 执行完成: 成功={len(results)}, 失败={len(errors)}, 总计={len(target_clients)}")
    if errors:
        print(f"[HTTP_EXECUTE] 失败账号: {[e['account'] for e in errors[:5]]}")
    
    return {
        'success': len(errors) == 0,
        'executed': len(results),
        'failed': len(errors),
        'target_mode': 'targeted' if accounts else 'broadcast',
        'target_count': len(accounts) if accounts else len(client_dic),
        'results': results,
        'errors': errors
    }


# ----------------------- Switch routes -----------------------
def _parse_bool(s: str):
    if s is None:
        raise ValueError('value is required')
    v = s.strip().lower()
    if v in ('1', 'true', 't', 'on', 'yes', 'y'):  # truthy
        return True
    if v in ('0', 'false', 'f', 'off', 'no', 'n'):  # falsy
        return False
    if v == 'toggle':
        return 'toggle'
    raise ValueError(f'invalid boolean value: {s}')


def route_switch_list(handler: BaseHTTPRequestHandler, parsed):
    switches = getattr(global_data, 'feature_switches', {})
    if not isinstance(switches, dict):
        switches = {}
    # ensure JSON-serializable booleans
    out = {str(k): bool(v) for k, v in switches.items()}
    _send_json(handler, {'switches': out}, 200)


def route_switch_get(handler: BaseHTTPRequestHandler, parsed):
    q = parse_qs(parsed.query or '')
    name = q.get('name', [None])[0]
    if not name:
        _send_json(handler, {'error': 'name required'}, 400)
        return
    switches = getattr(global_data, 'feature_switches', {})
    exists = name in switches
    val = bool(switches.get(name, False))
    _send_json(handler, {'name': name, 'value': val, 'exists': exists}, 200)


def route_switch_set(handler: BaseHTTPRequestHandler, parsed):
    q = parse_qs(parsed.query or '')
    name = q.get('name', [None])[0]
    value = q.get('value', [None])[0]
    if not name:
        _send_json(handler, {'error': 'name required'}, 400)
        return
    try:
        val = _parse_bool(value)
    except ValueError as e:
        _send_json(handler, {'error': str(e)}, 400)
        return
    switches = getattr(global_data, 'feature_switches', None)
    if switches is None or not isinstance(switches, dict):
        # initialize if missing or invalid
        global_data.feature_switches = {}
        switches = global_data.feature_switches
    if val == 'toggle':
        new_val = not bool(switches.get(name, False))
    else:
        new_val = bool(val)
    switches[name] = new_val
    _send_json(handler, {'name': name, 'value': new_val}, 200)


ROUTES = [
    # exact matches
    (lambda p: p in ('/', '/health'), route_health),
    (lambda p: p in ('/account_count', '/accounts/count'), route_account_count),
    # prefix matches
    (lambda p: p.startswith('/clients/count') or p.startswith('/client_count'), route_clients_count),
    (lambda p: p.startswith('/rpc/stats') or p.startswith('/rpc_call_statistics'), route_rpc_stats),
    (lambda p: p.startswith('/clients/slow'), route_clients_slow),
    (lambda p: p.startswith('/clients/noclient'), route_clients_noclient),
    # remote execution
    (lambda p: p.startswith('/execute'), route_execute),
    # switches
    (lambda p: p == '/switch/list', route_switch_list),
    (lambda p: p == '/switch/get', route_switch_get),
    (lambda p: p == '/switch/set', route_switch_set),
]


class _BotHTTPHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path or '/'
        for matcher, func in ROUTES:
            try:
                if matcher(path):
                    func(self, parsed)
                    return
            except Exception:
                # Let handler raise to surface errors as requested for diagnostics
                raise
        _send_text(self, 'Not Found', 404)

    # Silence default logging to stderr to avoid noisy output
    def log_message(self, fmt, *args):  # noqa: D401
        return


class _ThreadingHTTPServer(ThreadingMixIn, HTTPServer):
    daemon_threads = True
    allow_reuse_address = True


def start_http_server(host='127.0.0.1', port=0):
    """
    Start a lightweight HTTP server in a new thread.

    If binding the desired port fails, increment the port by 1 and retry
    until success. When port=0 (ephemeral), try once; on failure, fall back
    to 8000 and then increment.

    Returns (server, thread). Call server.shutdown() then thread.join() to stop.
    """
    httpd = None
    attempt_port = port
    while True:
        try:
            httpd = _ThreadingHTTPServer((host, attempt_port), _BotHTTPHandler)
            break
        except OSError:
            # If ephemeral failed, fall back to 8000 then increment
            if attempt_port == 0:
                attempt_port = 8000
            else:
                attempt_port += 1
            # wrap around if exceeding max port
            if attempt_port > 65535:
                attempt_port = 1024
            continue

    t = threading.Thread(target=httpd.serve_forever, name='BotHTTPServer')
    t.start()
    return httpd, t


def get_account_count():
    """Return the current logged-in account count from global_data.account_map.

    This reads the shared map; it should be updated elsewhere when accounts log in/out.
    """
    if global_data is None or not hasattr(global_data, 'account_map'):
        return 0
    try:
        return len(global_data.account_map)
    except Exception:
        return 0
