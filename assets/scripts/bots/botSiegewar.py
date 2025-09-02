import os
import sys
sysarg1 = sys.argv[1]
print("sysarg1", sysarg1, type(sysarg1))
import threading
import random
import time

import BotClient
import botBase
import json


BOT_CONFIG = botBase.initBotConfig(__file__)

GL_TOKEN_DICT = {}


class PlayerDelegate(object):
    @property
    def player(self): return self.robot.player()

    @property
    def base(self): return self.player.base

    @property
    def cell(self): return self.player.cell

    def __init__(self, robot, botCLient):
        self.robot = robot
        self.botClient = botCLient

    def onBecomePlayer(self):
        print('check_login:%s'%self.botClient.accountName)
        pos = random.choice(BOT_CONFIG['randomPos'])
        #参数1表示第一次，要升级、进帮会、退副本
        if sysarg1 == '1':
            self.base.runGmCommand('$finishNewbie 0 0')
            self.base.runGmCommand('$setlv 0 77')
            self.base.applyJoinGuild(4262671478430498817)
            self.base.sendWorldChatMsg('初始化机器人、升级、进帮会、退新手副本')
        else:
            self.base.sendWorldChatMsg('进跨服')
            self.base.enterCrossServerSiegeWarSpace()

    def onMessage(self, msgId, args):
        print('onMessage', msgId, args)

    def onTeleportDone(self, *args):
        print('onTeleportDone', args)

    #拿到token就开始重登进跨服
    def onCrossServerTokenResp(self, token, spaceNo, serverId):
        GL_TOKEN_DICT[self.botClient.accountName] = token
        print('onCrossServerTokenResp', token, spaceNo, serverId)

DELEGATE_CLS = PlayerDelegate

if __name__ == '__main__':
    fromIdx = 0
    print("enter")

    botCnt = 50
    def siegewarBot():
        while True:
            time.sleep(1)
            if len(GL_TOKEN_DICT) > 0:
                print("尝试登跨服", GL_TOKEN_DICT)
            for i in range(botCnt):
                idx = fromIdx + i
                name = 'siegewarBot%d' % idx
                if name in GL_TOKEN_DICT:
                    print('登跨服', name)
                    token = GL_TOKEN_DICT.pop(name)
                    client = BotClient.BotClient(name, name, 1)
                    robot = client.login(3, '192.168.10.222', 20013, json.dumps({'loginServerId': 1, 'crossServerToken': str(token)}))
                    robot.setPlayerDelegate(PlayerDelegate(robot, client))

    def startBot():
        ts = []
        print('start bot from', fromIdx)
        for i in range(botCnt):
            idx = fromIdx + i
            client = BotClient.BotClient('siegewarBot%d' % idx, 'siegewarBot%d' % idx, 1)
            robot = client.login(0, '192.168.10.219', 20013)
            robot.setPlayerDelegate(PlayerDelegate(robot, client))

            ts.append(client.tickThread)

        for t in ts:
            t.join()

    thread1 = threading.Thread(target=siegewarBot)
    thread1.start()
    startBot()
