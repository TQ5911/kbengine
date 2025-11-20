import os
import sys
import threading
import random
import time

import BotClient
import botBase

BOT_CONFIG = botBase.initBotConfig(__file__)


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
        self.base.runGmCommand('$setpos 0 {} {} {}'.format(pos[0], pos[1], pos[2]))

    def onTeleportDone(self, *args):
        print('onTeleportDone', args)


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
