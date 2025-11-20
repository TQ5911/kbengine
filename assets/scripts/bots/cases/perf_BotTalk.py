import os
import sys
import threading
import random
import time
import BotClient
import botBase
import re
import simpleBotBase
# BOT_CONFIG = botBase.initBotConfig(__file__)


class PlayerDelegate(simpleBotBase.SimpleBotBase):
    @property
    def player(self): return self.robot.player()

    @property
    def base(self): return self.player.base

    @property
    def cell(self): return self.player.cell

    def __init__(self, robot, botCLient):
        super(PlayerDelegate, self).__init__(robot, botCLient)
        self.world = 0
        self.team = 0
        self.present = 0
        self.guild = 0
        #1002广场区域



    def debug(self, info):
        print("%s %s %s" % (self.botClient.accountName, self.player.id, info))


    def onBecomePlayer(self):
        print('check_login:%s'%self.botClient.accountName)

        # pos = random.choice(BOT_CONFIG['randomPos'])
        # INFO_MSG(self.botClient.accountName, self.player.id,'登录成功')


        #客户端等待两秒后执行 self.cell.switchPKModel(2)
        # self.player.clientapp.callback(2,self.cell.switchPKModel(2))


    def onTeleportDone(self, *args):
        self.debug(f'onTeleportDone{args}')



    #这里通过服务器给客户端发送聊天消息，指示机器人干什么
    def onRecvAvatarChannelMsg(self, channelID,avatarInfo,msgId):
        if msgId == '机器人混合喊话':
            while self.world < 1000 or self.team < 1000 or self.present < 1000 or self.guild < 1000:
                randomvalue = random.choice(['世界', '队伍', '当前','帮会'])
                if randomvalue == '世界' and self.world < 1000:
                    self.world += 1
                    self.base.sendWorldChatMsg(f'{self.botClient.accountName}{randomvalue}喊话第{self.world}次')
                    # self.base.sendWorldChatMsg(f'{self.botClient.accountName}{randomvalue}喊话第{self.world}次')

                if randomvalue == '队伍' and self.team < 1000:
                    self.team+=1
                    self.base.sendTeamChatMsg(0,f'{self.botClient.accountName}{randomvalue}喊话第{self.team}次')

                if randomvalue == '当前' and self.present < 1000:
                    self.present+=1
                    self.base.sendNearbyChatMsg(f'{self.botClient.accountName}{randomvalue}喊话第{self.present}次')

                if randomvalue == '帮会' and self.guild < 1000:
                    self.guild+=1
                    self.base.sendGuildChatMsg(f'{self.botClient.accountName}{randomvalue}喊话第{self.guild}次')
        else:
            super().onRecvAvatarChannelMsg(channelID, avatarInfo, msgId)



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
