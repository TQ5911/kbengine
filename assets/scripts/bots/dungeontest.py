import os
import sys
import threading
import time
import BotClient
import botBase
import re
import math

# BOT_CONFIG = botBase.initBotConfig(__file__)
gbidlist = []
botinfo = {}
count = 0

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


 
    def onBecomePlayer(self):
        print('check_login:%s' % self.botClient.avatarName)


    def onTeleportDone(self, *args):
        self.debug(f'onTeleportDone{args}')

    def sendmsg(self):
        global count
        count+=1
        mgs = f'第{count}条消息'
        self.base.sendFriendMsg(self.gbid, mgs)

    
    def enter_dungeon(self,dungeon_id):
        if self.isCaptain() or self.isRaidLeader():
            self.debug('我是队长')
            self.base.enterDungeon(dungeon_id)

    # 这里通过服务器给客户端发送聊天消息，指示机器人干什么
    def onRecvAvatarChannelMsg(self, channelID, avatarInfo, msgId):

        if msgId == '获取所有机器人gbid':
            gbidlist.append(self.player.gbId)


        if msgId == '输出所有机器人gbid':
            self.sendbotlistgbid()

        if msgId == '机器人信息':
            self.sendbotinfo()


        if msgId == '执行指令':
            self.base.runGmCommand(f'$finishNewbie 0 0')
            self.base.runGmCommand(f'$setlv 0 28')
            self.base.runGmCommand(f'$adjfullHp 0 99999')
            self.base.runGmCommand(f'$modifyscore 0 5000')

        
        #匹配队伍-101/102/103
        match=re.match(r'^匹配队伍(?:-(\d+))?$', msgId)
        if match:
                dungeon_id_str = match.group(1)
                if dungeon_id_str:
                    dungeon_id = int(dungeon_id_str)
                    self.cell.reqPlayerAutoMatch(dungeon_id)
        
        # 匹配团队-151/152/153
        match_raid=re.match(r'^匹配团队(?:-(\d+))?$', msgId)
        if match_raid:
                dungeon_id_str = match_raid.group(1)
                if dungeon_id_str:
                    dungeon_id = int(dungeon_id_str)
                    self.cell.reqRaidPlayerAutoMatch(dungeon_id)


        if msgId == '退出副本':
            self.exit_dungeon()

        if msgId == '自动战斗':
            self.debug('开始自动战斗')
            self.cell.startAutoCombat(160)
            
        if msgId == '停止自动战斗':
            self.debug('停止自动战斗')
            self.cell.stopAutoCombat(160)

        if msgId == "进入副本":
            self.debug('进入副本')
            self.base.runGmCommand(f'$gmenterDungeon 0 2101')

        
        if msgId == "机器人离线":
            self.player.offlineBot()






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
