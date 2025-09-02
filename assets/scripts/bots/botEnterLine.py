#!/usr/bin/env python3
#
import os
import sys
import threading
import random
import time

import BotClient
import botBase


BOT_CONFIG = botBase.initBotConfig(__file__)

ENTITY_TYPE_2_ID_KEY = {
    "Npc": "npcId",
    "Collection": "collectionId",
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
        self.npcId = {
            "enter": 18110004,
            "leave": 18110010
        }
        self.dialogId = {
            "enter": 19800091002,
            "leave": 19800253001
        }
        self.pos = {
            "enter": (-98.38, 30.8, 85.03),
            "leave": (5.06, 1.09, -22.35)
        }
        self.robot = robot
        self.botClient = botCLient
        self.loopNum = 0

    def getEntityByClass(self, entityType, tgtId):
        key = ENTITY_TYPE_2_ID_KEY.get(entityType, "")
        for e in self.robot.entities.values():
            if e.className == entityType and getattr(e, key) == tgtId:
                return e.id, e
        return 0, None

    def talkToNpc(self, npcEntityId, taskId, dialogId, idx):
        self.cell.talkToNpc(npcEntityId, taskId, dialogId, idx)

    def handleSpace(self, param="enter"):
        if param == "enter":
            cmd = '$setops 0 %s %s %s' % (-98.38, 30.8, 85.03)
        else:
            cmd = '$setops 0 %s %s %s' % (5.06, 1.09, -22.35)
        self.base.runGmCommand(cmd)
        npcEntityId, err = self.getEntityByClass("Npc", self.npcId[param])
        print("handleSpace", param, self.player.gbId, npcEntityId)
        self.talkToNpc(npcEntityId, 0, self.dialogId[param], 0)

    def onBecomePlayer(self):
        print('check_login:%s,gbid:%s' % (self.botClient.accountName, self.player.gbId))
        self.handleSpace('enter')

    def onTeleportDone(self, *args):
        print('onTeleportDone', args)
        spaceNo = args[1]
        if int(spaceNo / 10000) == 2:
            # 成功进入了发布会场景
            print('enterSpace2', self.player.gbId)
            # 等1秒以后，再出去
            time.sleep(10)
            self.handleSpace('leave')
        if int(spaceNo / 10000) == 1:
            # 成功退出了发布会
            print('enterSpace1', self.player.gbId)
            time.sleep(10)
            self.handleSpace('enter')
            self.loopNum += 1


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
