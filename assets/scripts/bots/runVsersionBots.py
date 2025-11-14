import sys
import time
import os
import requests
import pypinyin
from pypinyin import lazy_pinyin
from datetime import datetime
import random
from simpleBotBase import FACE_DATA
import http_service
# 添加目标服务器参数：modName, school, loginHost, loginPort
modName, _school, _loginHost, _loginPort = sys.argv[1:5]
const_workspace_id_h1 = "59721401"
const_url_Alluser = f'https://api.tapd.cn/workspaces/users?workspace_id={const_workspace_id_h1}'
const_api_username = "GLdhcEyf"
const_api_password = "503E42F4-C403-B92C-A28C-2856A7178963"
name_dict = {}

if modName.endswith('.py'):
    modName = os.path.splitext(modName)[0]

mod = __import__(modName)
import BotClient

if not hasattr(mod, 'DELEGATE_CLS'):
    print('%s has no attribute DELEGATE_CLS' % modName)
    exit(-1)

def GetAllUsers():
    url = const_url_Alluser
    req = requests.get(url, auth=(const_api_username, const_api_password))
    if req.status_code != 200:
        print(f"请求用户列表失败: {req.text}")
    else:
        print("请求用户列表成功")
    data = req.json()
    Allusers = [item["UserWorkspace"]["user"] for item in data["data"]]
    for name in Allusers:
        pinyin_name = ''.join(lazy_pinyin(name))
        name_dict[name] = pinyin_name
    print(name_dict)
    return name_dict


    # return Allusers
characterdict = {
    1001:{'avatarname':'道士','accountname':'daoshi'},
    1002:{'avatarname':'法师','accountname':'fashi'},
    1003:{'avatarname':'战士','accountname':'zhanshi'},
}

def startBot(delegateCls, school, loginHost, loginPort):
    today = datetime.now()
    month_day = today.strftime("%m%d")
    ts = []
    
    print(f'版本日机器人目标服务器: {loginHost}:{loginPort}')
    
    # 启动 HTTP 服务
    httpd, http_thread = http_service.start_http_server('0.0.0.0', 49527)
    host, port = httpd.server_address
    print(f'http service started at http://{host}:{port}')
    
    Allusers = GetAllUsers()
    faceData = FACE_DATA()
    for avatarName, accountName in Allusers.items():
        if school == 'all':
            # 为每个用户创建3个职业的机器人
            for school_id, info in characterdict.items():
                final_avatar_name = f"{avatarName}{info['avatarname']}"
                final_account_name = f"{accountName}{info['accountname']}"
                
                print(f"创建机器人 - 账号: {final_account_name}, 角色: {final_avatar_name}, 职业: {school_id}")
                
                try:
                    client = BotClient.BotClient(final_account_name, final_avatar_name, school_id)
                    
                    # 如果提供了登录服务器地址和端口，则使用指定服务器登录
                    if loginHost and loginPort and loginHost.strip() and loginPort.strip():
                        print(f'版本日机器人 {final_account_name} 登录到服务器: {loginHost}:{loginPort}')
                        robot = client.login(accountType=0, loginAddr=loginHost.strip(), loginPort=int(loginPort))
                    else:
                        print(f'版本日机器人 {final_account_name} 登录到默认服务器')
                        robot = client.login()
                        
                    robot.setPlayerDelegate(delegateCls(robot, client))
                    
                    ts.append(client.tickThread)
                    time.sleep(1)  # 避免创建过快
                    
                except Exception as e:
                    print(f"创建机器人失败 - 账号: {final_account_name}, 错误: {e}")
                    continue
        else:
            # 只创建指定职业的机器人
            if school == 0:
                schoollist = list(characterdict.keys())
                botschool = random.choice(schoollist)
                faceData.random_set_face_data_by_id(botschool)
                face_dict = faceData.toSavedDict()
            else:
                botschool = school
                faceData.random_set_face_data_by_id(botschool)
                face_dict = faceData.toSavedDict()
            final_account_name = f"{accountName}{int(month_day)}"
            final_avatarName = f"{avatarName}{int(month_day)}"
            
            print(f"创建机器人 - 账号: {final_account_name}, 角色: {final_avatarName}, 职业: {botschool}")
            
            try:
                client = BotClient.BotClient(final_account_name, final_avatarName, int(botschool), face_dict)
                
                # 如果提供了登录服务器地址和端口，则使用指定服务器登录
                if loginHost and loginPort and loginHost.strip() and loginPort.strip():
                    print(f'版本日机器人 {final_account_name} 登录到服务器: {loginHost}:{loginPort}')
                    robot = client.login(accountType=0, loginAddr=loginHost.strip(), loginPort=int(loginPort))
                else:
                    print(f'版本日机器人 {final_account_name} 登录到默认服务器')
                    robot = client.login()
                    
                robot.setPlayerDelegate(delegateCls(robot, client))
                
                ts.append(client.tickThread)
                time.sleep(1)
                
            except Exception as e:
                print(f"创建机器人失败 - 账号: {final_account_name}, 错误: {e}")
                continue

    print(f"总共创建了 {len(ts)} 个版本日机器人，目标服务器: {loginHost}:{loginPort}")
    for t in ts:
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
    #GetAllUsers()
    time.sleep(10)
    if _school == 'all':
        startBot(getattr(mod, 'DELEGATE_CLS'), _school, str(_loginHost), str(_loginPort))
    else:
        startBot(getattr(mod, 'DELEGATE_CLS'), int(_school), str(_loginHost), str(_loginPort))
