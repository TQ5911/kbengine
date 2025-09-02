import os
import sys
import threading
import random
import time

args = sys.argv

import BotClient


class RobotPlayer(object):
    def __init__(self, robot):
        self.robot = robot
        self.didTel = threading.Event()
        self.runThd = threading.Thread(target=self.runAction, args=())

    def onBecomePlayer(self):
        self.didTel.set()
        self.runThd.start()

    def teleport(self):
        import NPC_teleporter as tel
        tlist = []
        for telid, info in tel.datas.items():
            if info['isOpen'] == 1: tlist.append(telid)

        telid = random.choice(tlist)
        lineNo = -1
        print('!!!! teleport', telid, lineNo)
        self.robot.player().cell.telToTeleporter(telid, lineNo)

    def onTeleport(self, *arg):
        print('!!!! teleport suc. 1')
        self.didTel.set()

    def startTeleport(self, *args):
        print('!!!! teleport suc. 2')
        self.didTel.set()

    def runAction(self):
        while self.didTel.wait(20):
            time.sleep(2)
            self.didTel.clear()
            self.teleport()
        else:
            print('!!!! teleport fail.', self.robot.player().gbId)


def loginBot(st, ed):
    cnt = 20
    for i in range(cnt):
        if st + i >= ed: break

        client = BotClient.BotClient('testBot{}'.format(st + i))
        robot = client.login()
        robot.setPlayerDelegate(RobotPlayer(robot))

    if st + cnt >= ed:
        print('login finish')
        client.tickThread.join()
    else:
        threading.Timer(10, loginBot, (st + cnt, ed)).start()


def startBot():
    global args

    st = int(args[1])
    ed = int(args[2])
    threading.Timer(1, loginBot, (st, ed)).start()


startBot()
