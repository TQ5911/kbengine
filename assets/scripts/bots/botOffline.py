#!/usr/bin/env python3
#
import os
import sys
import threading
import random
import time
import re

import BotClient
import botBase


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
        self.dungeonId = 101

    def onBecomePlayer(self):
        # 这里申请进入副本
        print("offlineBot")
        self.player.offlineBot()


DELEGATE_CLS = PlayerDelegate

if __name__ == '__main__':
    fromIdx = 0


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
