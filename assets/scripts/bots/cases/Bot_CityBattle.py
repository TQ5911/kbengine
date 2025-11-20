import os
import sys
import threading
import random
import time
import BotClient
import botBase
import re
import json
from datetime import datetime
# 移除命令行参数依赖，统一使用本服登录模式

# BOT_CONFIG = botBase.initBotConfig(__file__)
gbidlist = []
botinfo = {}
count = 0
jingongbotlist = []
fangshoubotlist = []
# 全局跨服token字典
GL_TOKEN_DICT = {}
# 跨服配置
CROSS_SERVER_CONFIG = {
    'main_server': {'ip': '192.168.10.221', 'port': 20013},  # 本服
    'cross_server': {'ip': '192.168.10.179', 'port': 20013}  # 跨服
}

class PlayerDelegate(object):
    @property
    def player(self):
        return self.robot.player()

    @property
    def base(self):
        return self.player.base

    @property
    def cell(self):
        return self.player.cell

    def __init__(self, robot, botCLient):

        self.robot = robot
        self.botClient = botCLient
        # 1002广场区域
   #     self.gbid = 5659099609889243137  #zxhhaoyouzuo
      #  self.gbid =  5659099747865067521  #haoyouzuozuo
      #  self.gbid = 5659099729812783105   #xisheng
      #  self.gbid  = 5659099764306739201  #haoyouzuozuo
        self.createguilditemid = 30000236
        self.guildUUid = 3265506825374007297    #zxh  帮会
        self.pos = [176.177567, 0.900842, 195.040192]
        self.Relive = False

    def debug(self, info):
        print(f'{self.botClient.avatarName},{self.player.gbId},{info}')



    def sendbotlistgbid(self):
        print(f'********************************\n{gbidlist}')

    def sendbotinfo(self):
        botinfo[self.botClient.avatarName] = self.player.gbId

    def _sendbotinfo(self):
        print(f'********************************\n{botinfo}')

    def randompos(self):
        randomspeed = random.randint(-10, 10)
        return randomspeed

    def randomlv(self):
        randomlv = random.randint(1, 20)
        randomzhanli = random.randint(1, 400)
        return randomlv, randomzhanli

    def reAvatarNameNumber(self):
        match = re.search(r'\d+', self.botClient.avatarName)
        if match:
            number = int(match.group())
            return number

    def onBecomePlayer(self):
        print('check_login:%s' % self.botClient.avatarName)
        self.debug("机器人已登录本服，等待指令...")
        
        # 可以在这里添加一些基础的初始化，但主要操作通过聊天消息触发
        # self.base.sendWorldChatMsg(f'{self.botClient.avatarName} 已就绪')

    def onTeleportDone(self, *args):
        self.debug(f'onTeleportDone{args}')

    def onCrossServerTokenResp(self, token, spaceNo, crossServerId):
        """接收到跨服token的回调"""
        GL_TOKEN_DICT[self.botClient.accountName] = {
            'token': token,
            'spaceNo': spaceNo,
            'crossServerId': crossServerId
        }
        self.debug(f'收到跨服token: {token}, spaceNo: {spaceNo}, crossServerId: {crossServerId}')
        print(f'[跨服TOKEN] {self.botClient.accountName} 收到token，等待跨服登录...')


    def sendmsg(self):
        global count
        count+=1
        mgs = f'第{count}条消息'
        self.base.sendFriendMsg(self.gbid, mgs)



    # 这里通过服务器给客户端发送聊天消息，指示机器人干什么
    def onRecvAvatarChannelMsg(self, channelID, avatarInfo, msgId):
    
        if msgId == '获取所有机器人gbid':
            gbidlist.append(self.player.gbId)

        elif msgId == '获取50个机器人gbid':
            number = self.reAvatarNameNumber()
            if number <= 50:
                gbidlist.append(self.player.gbId)

        elif msgId == '输出所有机器人gbid':
            self.sendbotlistgbid()

        elif msgId == '机器人信息':
            self.sendbotinfo()
        elif msgId == '输出机器人信息':
            self._sendbotinfo()

        elif msgId == '传送1001':
            self.debug(msgId)
            self.cell.applyEnterLine(1001)

        # (289.3742,4.7036,115.5110)
        # 传送到坐标(36.4585,39.0038,48.3531)
        if msgId.startswith('传送到坐标'):
            position = re.search(r"\((\d+\.\d+),(\d+\.\d+),(\d+\.\d+)\)", msgId)
            if position:
                x, y, z = position.groups()
                x = float(x) + self.randompos()
                y = float(y)
                z = float(z) + self.randompos()
                self.base.runGmCommand(f'$setpos 0 {x} {y} {z}')

        elif msgId == '升级':
            self.base.runGmCommand(f'$setlv 0 70')

        elif msgId == '获取金币':
            self.base.runGmCommand('$getitems 0 0 100000 0 30000001')

        elif msgId == '单人发送私聊消息':
            # number = self.reAvatarNameNumber()
            # if number == 1:
            for i in range(0,40):
                self.player.clientapp.callback(0.5, self.sendmsg)

        if msgId == '跳过新手':
            self.base.runGmCommand(f'$finishNewbie 0 0')

# --------------------------------------------------------------------------帮会逻辑--------------------------------------------------

        # 格式：            获取道具[{30000236:10},{30000001:20}]
        elif msgId.startswith('获取道具'):
            input_str = msgId
            inner_content = re.search(r"\[(.*?)\]", input_str).group(1)
            pattern = r"\{(\d+):(\d+)\}"
            matches = re.findall(pattern, inner_content)
            self.debug(f'道具列表：{matches}')
            result_list = [{int(key): int(value)} for key, value in matches]
            for i in result_list:
                for itemId, num in i.items():
                    self.base.runGmCommand(f'$getitems 0 0 {num} 0 {itemId}')

        elif msgId == "创建帮会":
            level = random.randint(1,20)
            score = random.randint(1,20)
            number = self.reAvatarNameNumber()

            joinCond = {
                "level":level,
                "score":score,
                "auto": random.randint(0,1)
            }
            createData = {
                'guildName':self.botClient.avatarName,
                'desc':f"我是帮会{number}",
                'dspFlag':random.randint(0,len(self.botClient.avatarName)-1),
                'joinCond':joinCond
            }
            self.base.createGuild(createData)


        elif msgId.startswith('结盟'):
            guildUUID = re.search(r"结盟(\d+)", msgId).group(1)
            self.base.applyGuildUnion(int(guildUUID))

        elif msgId.startswith('加入指定帮会'):
            guildUUID = re.search(r"加入指定帮会(\d+)", msgId).group(1)
            self.base.oneKeyGuildApply(int(guildUUID))
            self.debug(f'加入指定帮会{guildUUID}')


        elif msgId.startswith('加入进攻帮会'):
            guildUUID = re.search(r"加入进攻帮会(\d+)", msgId).group(1)
            if self.botClient.accountName in jingongbotlist:
                self.base.applyJoinGuild(int(guildUUID))

        elif msgId.startswith('加入防守帮会'):
            guildUUID = re.search(r"加入防守帮会(\d+)", msgId).group(1)
            self.debug(f'加入防守帮会{guildUUID}')
            if self.botClient.accountName in fangshoubotlist:
                self.base.applyJoinGuild(int(guildUUID))

        elif msgId == '退出帮会':
            self.base.exitGuild()
#-------------------------------------------------------------------------------------------------------------

        elif msgId == '机器人初始化':
            self.debug("开始机器人初始化...")
            self.base.runGmCommand('$finishNewbie 0 0')  # 跳过新手
            self.base.runGmCommand(f'$setlv 0 {random.randint(65,70 )}')  # 随机等级
            self.base.runGmCommand('$getitems 0 0 100000 0 30000001')  # 获取金币
            self.base.sendWorldChatMsg('机器人初始化完成')
            
        elif msgId == '自动加入帮会':
            if hasattr(self, 'guildUUid') and self.guildUUid:
                self.base.applyJoinGuild(self.guildUUid)
                self.debug(f"申请加入帮会: {self.guildUUid}")
            else:
                self.debug("未设置帮会ID")
                
        elif msgId == '开始跨服':
            self.debug("=== 开始跨服流程 ===")
            self.base.sendWorldChatMsg('准备进入跨服战场...')
            self.base.enterCrossServerSiegeWarSpace()
            
        elif msgId == '进入战场':
            self.base.enterCrossServerSiegeWarSpace()
            
        elif msgId == '查看跨服状态':
            if self.botClient.accountName in GL_TOKEN_DICT:
                token_info = GL_TOKEN_DICT[self.botClient.accountName]
                self.debug(f"已获取跨服token: {token_info}")
            else:
                self.debug("尚未获取跨服token")


        elif msgId == "机器人离线":
            self.player.offlineBot()



        # 队员加入队伍后，通知客户端

#创建帮会回调
    def onCreateGuildResult(self,result,ctx):
        if result == 0:
            self.debug('创建工会成功')


DELEGATE_CLS = PlayerDelegate

def crossServerBot():
    """跨服机器人监控线程"""
    print("[跨服监控] 启动跨服token监控线程...")
    
    while True:
        time.sleep(2)  # 每2秒检查一次
        
        if len(GL_TOKEN_DICT) > 0:
            print(f"[跨服监控] 发现 {len(GL_TOKEN_DICT)} 个待跨服token")
            
            # 处理所有待跨服的机器人
            for account_name in list(GL_TOKEN_DICT.keys()):
                token_info = GL_TOKEN_DICT.pop(account_name)
                
                print(f'[跨服登录] 开始跨服登录: {account_name}')
                
                try:
                    # 创建跨服客户端
                    client = BotClient.BotClient(account_name, account_name, 1)
                    
                    # 使用token登录跨服
                    cross_config = CROSS_SERVER_CONFIG['cross_server']
                    client_data = json.dumps({
                        'loginServerId': 1, 
                        'crossServerToken': str(token_info['token'])
                    })
                    
                    robot = client.login(3, cross_config['ip'], cross_config['port'], client_data)
                    robot.setPlayerDelegate(PlayerDelegate(robot, client))
                    
                    print(f'[跨服成功] {account_name} 成功登录跨服')
                    
                except Exception as e:
                    print(f'[跨服失败] {account_name} 跨服登录失败: {e}')

def startBot():
    """启动城战机器人 - 统一本服登录"""
    today = datetime.now()
    month_day = today.strftime("%m%d")
    ts = []
    fromIdx = 0
    botCount = 50
      # 机器人数量
    print(f'[机器人启动] 开始创建 {botCount} 个城战机器人')
    
    # 统一连接本服
    server_config = CROSS_SERVER_CONFIG['main_server']
    print(f'[服务器] 连接本服: {server_config["ip"]}:{server_config["port"]}')
    print('[流程] 机器人将在本服等待指令，通过聊天消息控制跨服')
    
    for i in range(botCount):
        idx = fromIdx + i
        # if i <=50:
        account_name = f'jingong{idx}'
        avatar_name = f'进攻{idx}-{month_day}'
        jingongbotlist.append(avatar_name)
        # else:
        #     account_name = f'fangshou{idx}'
        #     avatar_name = f'防守{idx}'
        #     fangshoubotlist.append(avatar_name)
        
        try:
            client = BotClient.BotClient(account_name, avatar_name, 1)
            # 统一使用本服登录 (accountType=0)
            robot = client.login(0, server_config['ip'], server_config['port'])
            robot.setPlayerDelegate(PlayerDelegate(robot, client))
            
            ts.append(client.tickThread)
            
            if i % 10 == 0:
                print(f'[进度] 已创建 {i+1}/{botCount} 个机器人')
                
        except Exception as e:
            print(f'[错误] 创建机器人 {account_name} 失败: {e}')
            continue
    
    print(f'[完成] 总共创建了 {len(ts)} 个机器人')
    print('[等待] 机器人已就绪，可以通过以下聊天消息控制:')
    print('  "机器人初始化" - 跳过新手、升级、获取金币')
    print('  "自动加入帮会" - 加入指定帮会') 
    print('  "开始跨服" - 请求跨服token并自动跨服登录')
    print('  "查看跨服状态" - 查看token获取状态')
    
    # 等待所有机器人线程
    for t in ts:
        t.join()

if __name__ == '__main__':
    print("=== 城战跨服机器人系统 ===")
    print("工作流程:")
    print("1. 机器人登录本服")
    print("2. 发送 '机器人初始化' - 完成基础设置")
    print("3. 发送 '自动加入帮会' - 加入帮会")
    print("4. 进行竞拍等其他操作...")  
    print("5. 发送 '开始跨服' - 自动跨服登录")
    print("========================")
    
    # 启动跨服监控线程（始终启动）
    cross_thread = threading.Thread(target=crossServerBot)
    cross_thread.daemon = True
    cross_thread.start()
    print("[跨服监控] 跨服监控线程已启动")
    
    # 启动机器人
    startBot()
