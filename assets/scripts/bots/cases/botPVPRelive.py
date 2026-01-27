import os
import sys
import threading
import random
import time
import BotClient
import botBase
import Math
import sMath



class State(object):
    IDLE = 1
    RELIVE = 2
    GO_TO_PVP_POS = 3
    BATTLE = 4
    SKIP_NEWBIE = 5


TARGET_POS = (398.4615, 4.7590, 216.2478)


class PlayerDelegate(botBase.BotBase):
    def __init__(self, robot, botClient):
        super(PlayerDelegate, self).__init__(robot, botClient)
        botClient.client.setSyncViewEntities(0)  # 关闭同步视野内实体数据，减少机器人客户端开销
        self._state = State.IDLE
        self.moveEvent = botBase.TestEvent()

    def runAction(self):
        while True:
            if self._state == State.IDLE:
                if self.player.spaceNo // 10000 == 4002:
                    self.base.runGmCommand('$setlv 0 90')
                    self.base.runGmCommand('$finishNewbie 0 0')

                elif self._isDead():
                    self._state = State.RELIVE
                else:
                    self.base.runGmCommand('$getitems 0 0 9999 0 30010005 30010006')
                    for idx, itemId in enumerate([30010006,30010005]):
                        slotInfo = {"slotId": idx, "itemId": itemId, "potionState": 1}
                        self.base.setInstantPotionSlots(slotInfo)
                    if self.player.totalScore < 150000:
                        self.base.runGmCommand("$enhanceRole 0 0")
                    self._state = State.GO_TO_PVP_POS

            elif self._state == State.RELIVE:
                if not self._isDead():
                    self._state = State.GO_TO_PVP_POS
                else:
                    #self.base.runGmCommand('$reliveToPos 0 None 100')
                    self.base.runGmCommand("$reliveToPos 0 393,7,154 10000")

            elif self._state == State.GO_TO_PVP_POS:
                if sMath.distance2D(self.player.position, TARGET_POS) < 1:
                    self._state = State.BATTLE
                else:
                    self.player.moveToPoint(TARGET_POS, 10, 0, 0, True, False)
                    self.moveEvent.wait()

            elif self._state == State.BATTLE:
                if self._isDead():
                    self._state = State.RELIVE

                elif not self.isAutoCombat():
                    self.cell.startAutoCombat(0)

                elif self.player.pkModel != 3:
                    self.cell.switchPKModel(3)

            self.tagPrint('state:', self._state, self.isAutoCombat())
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

    def onMoveOver(self, *args):
        print('onMoveOver', args)
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
