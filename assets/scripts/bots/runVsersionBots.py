# -*- coding: utf-8 -*-
import sys
import time
import os
import requests
import pypinyin
from pypinyin import lazy_pinyin
from datetime import datetime
import random
from botUtils.faceData_CtoDict import FACE_DATA
import botUtils.http_service as http_service
import re
# 初始化环境变量
cur_path = os.path.realpath(__file__)
bot_dir = os.path.dirname(cur_path)
cases_dir = os.path.join(bot_dir, 'cases')
sys.path.append(cases_dir)
ROOT_PATH = os.path.dirname(bot_dir)
sys.path.append(os.path.join(ROOT_PATH, 'data'))
sys.path.append(os.path.join(ROOT_PATH, 'server_common'))
sys.path.append(os.path.join(ROOT_PATH, 'common'))

# 添加目标服务器参数：modName, school, loginHost, loginPort
modName, _school, _loginHost, _loginPort = sys.argv[1:5]
const_workspace_id_h1 = "59721401"
const_url_Alluser = f'https://api.tapd.cn/workspaces/users?workspace_id={const_workspace_id_h1}'
const_api_username = "GLdhcEyf"
const_api_password = "503E42F4-C403-B92C-A28C-2856A7178963"

#在企业微信 拿成员名单 re取一下，如果人员变更多，需要这里改一下
AllUserstr = "徐方磊;包航;曹逸凡(关卡);柴东月;陈成伟(特效);陈科争(服务端);陈拓;陈周平(场景原画);陈子琪(交互);车子豪(特效);崔国标(角色模型);戴诚磊(客户端);郭宁(交互);顾倩倩(GUI);黄晓洁(角色模型);胡阳;胡宇萌（角色原画）;纪萱;柯臣;廖作嘉;李崇(场景模型);李均(服务端);李蒙;凌乔亚(TA);林湉;李启迪(PM);李奇育;李胜楠(WEB-前端);李帅(地编);刘昊(战斗);刘建锋(TA);刘莫(GUI);刘晓龙(特效);李小秋;李子晗(WEB-后端);陆佳毅(场景原画);吕冬;马俊捷(数值);毛耀华;梅天杰;钱伟;邱伟(服务端);任凯(场景模型);沈翔(QA);沈锡生;司乾义(地编);斯羿涵;隋云峰;唐政(QA);田净雨(关卡);王萌辉(场景模型);王鹏(QA);王文涛(地编);王悦(QA);王云龙(客户端);温浩(地编);巫顶峰;吴焱斌(QA);肖建强(特效);肖明(场景模型);谢崇伦;郗浩钦(场景模型);许耿腾(系统);徐银燕(地编);杨乐;杨雅琼(场景模型);闫明(场景模型);颜敏捷(角色模型);严伟铭(QA);严毅;叶飞帆（地编）;游先毅;于森森(场景模型);张典;张浩杰(角色原画);张帅;张武建;张新辉(角色动作);张昕雅;张一晔(角色模型);张灼(地编);占星豪(QA);赵睿(战斗);赵文唯（QA）;郑炜（动作）;庄超(系统);祝天奇(服务端);朱子阳(角色模型);资萱梓(角色原画);"

name_dict = {}

if modName.endswith('.py'):
    modName = os.path.splitext(modName)[0]

mod = __import__(modName)
import BotClient

if not hasattr(mod, 'DELEGATE_CLS'):
    print('%s has no attribute DELEGATE_CLS' % modName)
    exit(-1)

def GetAllUsers():
    # url = const_url_Alluser
    # req = requests.get(url, auth=(const_api_username, const_api_password))
    # if req.status_code != 200:
    #     print(f"请求用户列表失败: {req.text}")
    # else:
    #     print("请求用户列表成功")
    # data = req.json()
    #Allusers = [item["UserWorkspace"]["user"] for item in data["data"]]
    Allusers = Username_RE()
    for name in Allusers:
        pinyin_name = ''.join(lazy_pinyin(name))
        name_dict[name] = pinyin_name
    print(name_dict)
    return name_dict

def Username_RE():
    Allusers = re.findall(r'[\u4e00-\u9fa5]+', AllUserstr)
    return Allusers


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
