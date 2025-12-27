import sys
import time
import os
import threading
import requests
from botUtils.faceData_CtoDict import FACE_DATA
import botUtils.http_service as http_service

# 初始化环境变量
cur_path = os.path.realpath(__file__)
bot_dir = os.path.dirname(cur_path)
cases_dir = os.path.join(bot_dir, 'cases')
sys.path.append(cases_dir)
ROOT_PATH = os.path.dirname(bot_dir)
sys.path.append(os.path.join(ROOT_PATH, 'data'))
sys.path.append(os.path.join(ROOT_PATH, 'server_common'))

# 添加loginserver参数：modName, botPrefix, numAll, numPerSec, fromIdx, avatarName, school, loginHost, loginPort
# 可选参数：serverId, queueServiceUrl（如果未提供则从环境变量或默认值获取）
modName, _botNamePrefix, _numAll, _numPerSec, _fromIdx, _avatarName, _school, _loginHost, _loginPort = sys.argv[1:10]

# 尝试获取 serverId 和 queueServiceUrl（从环境变量或命令行参数）
_serverId = os.getenv('QUEUE_SERVER_ID', '')
_queueServiceUrl = os.getenv('QUEUE_SERVICE_URL', 'http://192.168.10.214:4396')

# 如果命令行参数有 serverId 和 queueServiceUrl，则使用命令行参数
if len(sys.argv) >= 11:
    _serverId = sys.argv[10] if sys.argv[10] else _serverId
if len(sys.argv) >= 12:
    _queueServiceUrl = sys.argv[11] if sys.argv[11] else _queueServiceUrl

if modName.endswith('.py'):
    modName = os.path.splitext(modName)[0]

mod = __import__(modName)

import BotClient

if not hasattr(mod, 'DELEGATE_CLS'):
    print('%s has no attribute DELEGATE_CLS' % modName)
    exit(-1)


# ====================== 排队相关函数 ======================

def request_queue_login(queue_service_url, server_id, account_name, timeout=10):
    """
    请求登录排队
    
    Args:
        queue_service_url: 排队服务地址，如 'http://192.168.10.214:4396'
        server_id: 服务器ID
        account_name: 账号名称
        timeout: 请求超时时间（秒）
    
    Returns:
        int: 0 表示可以直接登录，1 表示需要排队，-1 表示请求失败
    """
    url = f"{queue_service_url}/startQueue"
    params = {
        "serverId": server_id,
        "accountName": account_name
    }
    
    try:
        response = requests.get(url, params=params, timeout=timeout)
        response.raise_for_status()
        result = response.json()
        # 返回格式: {"queueId":1,"state":0,"serverId":20105,"serverHost":"","waitTime":0}
        # state: 0=可以进入游戏, 1=需要排队
        if isinstance(result, dict):
            print(f"请求 {url} 登录 返回的json ({account_name}): {result}")
            state = result.get('state', -1)
            return int(state)
        else:
            return -1
    except requests.exceptions.RequestException as e:
        print(f"请求登录排队失败 ({account_name}): {e}")
        return -1
    except Exception as e:
        print(f"解析登录排队响应失败 ({account_name}): {e}")
        return -1


def get_queue_info(queue_service_url, server_id, account_name, timeout=10):
    """
    获取排队信息
    
    Args:
        queue_service_url: 排队服务地址
        server_id: 服务器ID
        account_name: 账号名称
        timeout: 请求超时时间（秒）
    
    Returns:
        dict: 排队信息，如果请求失败返回 None
    """
    url = f"{queue_service_url}/getQueueInfo"
    params = {
        "serverId": server_id,
        "accountName": account_name
    }
    
    try:
        response = requests.get(url, params=params, timeout=timeout)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"获取排队信息失败 ({account_name}): {e}")
        return None
    except Exception as e:
        print(f"解析排队信息失败 ({account_name}): {e}")
        return None


def wait_for_queue(queue_service_url, server_id, account_name, check_interval=5, max_wait_time=300):
    """
    等待排队，直到可以登录
    
    Args:
        queue_service_url: 排队服务地址
        server_id: 服务器ID
        account_name: 账号名称
        check_interval: 检查间隔（秒）
        max_wait_time: 最大等待时间（秒），0 表示不限制
    
    Returns:
        bool: True 表示可以登录，False 表示超时或失败
    """
    start_time = time.time()
    check_count = 0
    
    print(f"[排队] {account_name} 进入排队，开始检查排队状态...")
    
    while True:
        check_count += 1
        queue_info = get_queue_info(queue_service_url, server_id, account_name)
        
        if queue_info is None:
            print(f"[排队] {account_name} 获取排队信息失败，继续重试...")
        else:
            # 返回格式: {"queueId":1,"state":0,"serverId":20105,"serverHost":"","waitTime":0}
            # state: 0=可以进入游戏, 1=需要排队
            state = queue_info.get('state', 1)
            queue_id = queue_info.get('queueId', '?')
            wait_time = queue_info.get('waitTime', 0)
            

            if int(state) == 0:
                print(f"[排队] {account_name} 排队完成，可以登录！(queueId: {queue_id}, 等待时间: {wait_time}秒)")
                return True
            else:
                print(f"[排队] {account_name} 排队中... 当前在第: {queue_id}位, 预计等待: {wait_time}秒 (检查次数: {check_count})")
        
        # 检查是否超时
        if max_wait_time > 0 and (time.time() - start_time) >= max_wait_time:
            print(f"[排队] {account_name} 等待超时 ({max_wait_time}秒)，停止等待")
            return False
        
        time.sleep(check_interval)
    
    return False


def ensure_queue_login(queue_service_url, server_id, account_name):
    """
    确保账号可以登录（如果需要排队则等待）
    
    Args:
        queue_service_url: 排队服务地址
        server_id: 服务器ID
        account_name: 账号名称
    
    Returns:
        bool: True 表示可以登录，False 表示失败
    """
    if not queue_service_url or not server_id:
        print(f"[排队] {account_name} 排队服务未配置，跳过排队检查")
        return True
    
    # 请求登录排队
    result = request_queue_login(queue_service_url, server_id, account_name)
    
    if result == 0:
        print(f"[排队] {account_name} 可以直接登录")
        return True
    elif result == 1:
        print(f"[排队] {account_name} 需要排队，开始等待...")
        return wait_for_queue(queue_service_url, server_id, account_name)
    else:
        print(f"[排队] {account_name} 排队请求失败，尝试直接登录")
        return True  # 失败时允许尝试直接登录


# ====================== 主函数 ======================

def startBot(delegateCls, botPrefix, numAll, numPerSec, fromIdx, avatarName, school, loginHost, loginPort, serverId=None, queueServiceUrl=None):
    print(f'listen on {loginHost}:{loginPort}')
    httpd, http_thread = http_service.start_http_server('0.0.0.0', 49527)
    host, port = httpd.server_address
    print(f'http service started at http://{host}:{port}')
    tick_threads = []
    tick_threads_lock = threading.Lock()
    login_threads = []
    print('start bot from', fromIdx)
    print(f'target login server: {loginHost}:{loginPort}')
    import random
    school_list = [1001,1002,1003]

    def login_single_bot(idx):
        try:
            random_school = school
            # 随机
            if random_school == 0:
                random_school = random.choice(school_list)
            # 均匀分布
            elif random_school == 1:
                random_school = school_list[idx % len(school_list)]
            faceData = FACE_DATA()
            faceData.random_set_face_data_by_id(random_school)

            account_name = '%s%d' % (botPrefix, idx)
            client = BotClient.BotClient(account_name, '%s%d' % (avatarName, idx), random_school, faceData.toSavedDict())
            
            # 登录前先检查排队
            if serverId and queueServiceUrl:
                print(f'[排队] bot {idx} ({account_name}) 开始排队检查...')
                if not ensure_queue_login(queueServiceUrl, serverId, account_name):
                    print(f'[排队] bot {idx} ({account_name}) 排队失败，跳过登录')
                    return
            
            # 如果提供了登录服务器地址和端口，则使用指定服务器登录
            if loginHost and loginPort and loginHost.strip() and loginPort.strip():
                print(f'bot {idx} logging to server: {loginHost}:{loginPort}')
                robot = client.login(accountType=0, loginAddr=loginHost.strip(), loginPort=int(loginPort))
            else:
                print(f'bot {idx} logging to default server')
                robot = client.login()

            robot.setPlayerDelegate(delegateCls(robot, client))
            
            with tick_threads_lock:
                tick_threads.append(client.tickThread)
        except Exception as e:
            print(f"bot {idx} 启动失败: {e}")

    for i in range(numAll):
        idx = fromIdx + i
        t = threading.Thread(target=login_single_bot, args=(idx,))
        t.start()
        login_threads.append(t)
        if (i + 1) % numPerSec == 0:
            time.sleep(1)

    # 等待登录线程完成（排队与登录）
    for t in login_threads:
        t.join()

    print(f"总共创建了 {len(tick_threads)} 个机器人，目标服务器: {loginHost}:{loginPort}")
    for t in tick_threads:
        t.join()

    # 关闭并等待HTTP线程，确保在runBot流程内join
    try:
        httpd.shutdown()
    except Exception:
        pass
    try:
        httpd.server_close()
    except Exception:
        pass
    http_thread.join()


if __name__ == '__main__':
    time.sleep(10)
    # 转换 serverId 为整数（如果提供）
    _serverId_int = int(_serverId) if _serverId and _serverId.strip() else None
    startBot(getattr(mod, 'DELEGATE_CLS'), _botNamePrefix, int(_numAll), int(_numPerSec),
             int(_fromIdx), str(_avatarName), int(_school), str(_loginHost), str(_loginPort),
             serverId=_serverId_int, queueServiceUrl=_queueServiceUrl)
