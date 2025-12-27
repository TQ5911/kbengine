#!/usr/bin/env python3
#
import os
import sys
import threading
import random
import time

import BotClient
import botBase


class State(object):
    IDLE = 1
    SEND_DUAL_REQ = 2
    WAIT_DUEL_START = 3
    RELIVE = 4



class PlayerDelegate(botBase.BotBase):
    def __init__(self, robot, botClient):
        super(PlayerDelegate, self).__init__(robot, botClient)
        self._state = State.IDLE

    def runAction(self):
        while True:
            if self._state == State.IDLE:
                if self._isDead():
                    self._state = State.RELIVE
                else:
                    self._state = State.SEND_DUAL_REQ

            elif self._state == State.SEND_DUAL_REQ:
                if self._findAvatarAndSendDuelReq():
                    self._state = State.WAIT_DUEL_START

            elif self._state == State.WAIT_DUEL_START:
                if self.player.duelAttr['duelFlags'] != 0:
                    # self.cell.startAutoCombat(True)
                    pass

            elif self._state == State.RELIVE:
                if not self._isDead():
                    self._state = State.IDLE
                else:
                    self.base.runGmCommand('$reliveToPos 0 None 100')

            time.sleep(1)

    def _findAvatarAndSendDuelReq(self):
        for k, v in self.player.clientapp.entities.items():
            name = v.__class__.__name__
            if name == 'Avatar':
                # if not v.name.startswith('bot'):
                #     continue

                self.cell.reqDuel(v.id)
                return True

        return False

    def _isDead(self):
        return bool(self.player.state & (1 << 4))

    def onRecvDuelReq(self, reqId, name):
        self.tagPrint('onRecvDuelReq', reqId, name)
        self.cell.dealDuelReq(True, False)

    def set_duelAttr(self, *args):
        self.tagPrint('set_duelAttr', args)
        self.tagPrint('duelAttr', self.player.duelAttr)


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
