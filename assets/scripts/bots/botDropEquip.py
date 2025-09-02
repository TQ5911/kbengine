#!/usr/bin/env python3
#
import os
import sys
import threading
import random
import json
import time
import deephyper

import BotClient
import botBase



class State(object):
    IDLE = 1
    GOTO_1020 = 2
    RELIVE = 3
    DROP_EQUIP = 4
    PICK_UP_EQUIP = 5

class PlayerDelegate(botBase.BotBase):
    def __init__(self, robot, botClient):
        super(PlayerDelegate, self).__init__(robot, botClient)
        self._state = State.IDLE

    def _isDead(self):
        return bool(self.player.state & (1 << 4))

    def runAction(self):
        while True:
            if self._state == State.IDLE:
                self.tagPrint('runAction', self.player.spaceNo)
                if self._isDead():
                    self._state = State.RELIVE

                elif int(self.player.spaceNo // 10000) != 1002:
                    self._state = State.GOTO_1020

                elif random.randint(0, 100) < 80:
                    self._state = State.PICK_UP_EQUIP

                else:
                    self._state = State.DROP_EQUIP
            
            elif self._state == State.GOTO_1020:
                self.base.runGmCommand('$enterMap 0 1002')
                self._state = State.IDLE

            elif self._state == State.RELIVE:
                self.base.runGmCommand('$relive 0')
                self._state = State.IDLE

            elif self._state == State.DROP_EQUIP:
                self.base.runGmCommand('$dropWithoutDress 0 1')
                self._state = State.IDLE

            elif self._state == State.PICK_UP_EQUIP:
                collection = self.getCollection()
                if collection:
                    self.cell.applyGather(collection.id)
                else:
                    self._state = State.IDLE

            time.sleep(1)

    def getCollection(self):
        for k, v in self.player.clientapp.entities.items():
            name = v.__class__.__name__
            if name == 'Collection':
                # self.tagPrint('v.dict', v.__dict__)
                if v.dropEquipId:
                    return v

        return None

    def onMoveOver(self, *args):
        self.tagPrint('onMoveOver', args)
        self.moveEvent.set()

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
