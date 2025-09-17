import os
import sys
import threading
import random
import time
import BotClient
import botBase
import simpleBotBase
import re
# BOT_CONFIG = botBase.initBotConfig(__file__)


class PlayerDelegate(simpleBotBase.SimpleBotBase):
    def __init__(self, robot, botCLient):
        super(PlayerDelegate, self).__init__(robot, botCLient)
        #1002广场区域
        self.pos = [404.0721, 0.8875, 187.3936]
        self.Relive = False


    def debug(self, info):
        print("%s %s %s" % (self.botClient.accountName, self.player.id, info))

    def randompos(self):
        randomspeed = random.randint(-5, 5)
        return randomspeed


    def onBecomePlayer(self):
        #print('check_login:%s'%self.botClient.accountName)
        self.debug(f"登录成功")



    def onTeleportDone(self, *args):
        self.debug(f'onTeleportDone{args}')


    #这里通过服务器给客户端发送聊天消息，指示机器人干什么
    # def onRecvAvatarChannelMsg(self, channelID,avatarInfo,msgId):

    #     #客户端GM里面。 执行自定义代码  替换下方的 GM 可直接执行对应的GM
    #      #  PlayerEntity.sendChatMsg(ChatChannel.World, @"$getitems 0 0 10000 0 30000001");
    #     if '$' in msgId:
    #         self.base.runGmCommand(msgId)
    #     elif channelID == gameconst.ChatChannel.SYSTEM and 'self.' in msgId:
    #         try:
    #             exec(msgId)
    #         except Exception as e:
    #             self.debug(f"执行错误: {e}")

    #     elif msgId == '升级':
    #         self.base.runGmCommand(f'$setlv 0 {random.randint(20,70)}')

    #     elif msgId == '添加血量':
    #         self.base.runGmCommand(f'$adjfullHp 0 99999')

    #     elif msgId == '跳过新手':
    #         self.base.runGmCommand(f'$finishNewbie 0 0')

    #     elif msgId == '执行指令':
    #         self.base.runGmCommand(f'$setlv 0 48')
    #         self.base.runGmCommand(f'$submittask 0 86050032')
    #         self.base.runGmCommand(f'$submittask 0 86010048')
    #         self.base.runGmCommand(f'$addEquipAnima 0 1000')
            
    #     # 传送到坐标(36.4585,39.0038,48.3531)
    #     elif msgId.startswith('传送到坐标'):
    #         position = re.search(r"\((\d+\.\d+),(\d+\.\d+),(\d+\.\d+)\)", msgId)
    #         if position:
    #             x, y, z = position.groups()
    #             x = float(x) + self.randompos()
    #             y = float(y)
    #             z = float(z) + self.randompos()
    #             self.base.runGmCommand(f'$setpos 0 {x} {y} {z}')


    #     elif '设置善恶值' in msgId:
    #         match = re.match(r'(.*?)(-?\d+)', msgId)
    #         if match:
    #             str = match.group(1)
    #             moralValue = int(match.group(2))  # 获取后面的整数并转换为整数类型
    #             self.base.runGmCommand(f'$moralValue 0 {moralValue}')
    #         else:
    #             self.debug('未设置成功善恶值')

    #     elif msgId == "PK模式":
    #         self.cell.switchPKModel(2)
    #         self.debug(f"开启PK模式")

    #     elif msgId == '随机切换一个模式':
    #         self.cell.switchPKModel(random.randint(0,2))

    #     elif msgId == "关闭帮派保护":
    #         self.cell.setPKProtect(2, 0)
        
    #     elif msgId == '开启帮派保护':
    #         self.cell.setPKProtect(2, 1)

    #     elif msgId == '开启自动战斗':
    #         self.cell.startAutoCombat(160)

    #     elif msgId == "机器人离线":
    #         self.player.offlineBot()
    #     elif msgId == "复活":
    #         self.cell.relive(2)
    #     elif msgId == "死亡立即复活":
    #         self.Relive = True
    #         self.cell.relive(2)

    #     elif msgId.startswith('加入队伍'):
    #         itemid = re.search(r"加入队伍(\d+)", msgId).group(1)
    #         self.cell.applyJoinTeam(int(itemid))
    #     else:
    #         self.debug(f'{msgId}输入无效')

    #死亡立即复活
    def onDead(self,*args):
        self.base.runGmCommand(f'$reliveToPos 0 None 10000')
        self.cell.startAutoCombat(160)

    #服务器给客户端发传送消息
    def startTeleport(self,*args):
        self.debug(f"已经传送到坐标,坐标位置{self.player.position}")

    def onStartAutoCombat(self):
        self.debug(f"开启自动战斗")



DELEGATE_CLS = PlayerDelegate

if __name__ == '__main__':
    fromIdx = 0
    print("enter")


    def startBot():
        ts = []
        print('start bot from', fromIdx)
        for i in range(80):
            idx = fromIdx + i
            client = BotClient.BotClient('testBot%d' % idx)
            robot = client.login()
            robot.setPlayerDelegate(PlayerDelegate(robot, client))

            ts.append(client.tickThread)

        for t in ts:
            t.join()


    startBot()
