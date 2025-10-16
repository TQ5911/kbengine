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
    def __init__(self, robot, botCLient):
        super(PlayerDelegate, self).__init__(robot, botCLient)

    def debug(self, info):
        print("%s %s %s" % (self.botClient.accountName, self.player.id, info))

    def randompos(self):
        randomspeed = random.randint(-5, 5)
        return randomspeed


    def onBecomePlayer(self):
        print('check_login:%s'%self.botClient.accountName)

    def onRecvAvatarChannelMsg(self, channelID,avatarInfo,msgId):

        """
        所有聊天消息都在这里处理，会根据消息内容，判断是否需要执行某些操作
        如：
        1. 如果消息内容包含“升级”，则执行升级操作
        2. 如果消息内容包含“传送”，则执行传送操作
        3. 如果消息内容包含“打怪”，则执行打怪操作
        4. 如果消息内容包含“聊天”，则执行聊天操作
        5. 如果消息内容包含“交易”，则执行交易操作
        """
        
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
