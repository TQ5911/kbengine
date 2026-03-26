try:
    import GameInit
except:
    from core.demo.game.scripts.bots import GameInit

GameInit.init()

import os
import sys
import threading
import time
import logging
import KBEngine
import random
import json

from EntityCallAccountBase import AccountBaseEntityCall, AccountCellEntityCall
from EntityCallAvatarBase import AvatarBaseEntityCall, AvatarCellEntityCall
from Account import Account
from RemoteMethod import EntityMethodType
import global_data as GD

class RepeatTimer(threading.Thread):
    def __init__(self, delay, interval, onTimerCall, stopEvent):
        threading.Thread.__init__(self)
        self.delay = delay
        self.interval = interval
        self.onTimerCall = onTimerCall
        self.stopEvent = stopEvent

    def run(self):
        if not self.stopEvent.wait(self.delay):
            self.onTimerCall()

        while not self.stopEvent.wait(self.interval):
            self.onTimerCall()

class Player(object):
    def __init__(self, client, baseEtnityCall, cellEntityCall, playerType):
        self.client = client
        self.base = baseEtnityCall
        self.cell = cellEntityCall
        self.playerType = playerType

class BotClient(object):
    def __init__(self, accountName, avatarName, school, faceData = None):
        self.accountName = accountName
        self.avatarName = avatarName
        self.school = school
        self.faceData = faceData
        self.client = None
        self.playerAvatar = None
        self.playerAccount = None
        self.remoteCallBuffer = []
        self.stopEvent = threading.Event()
        self.tickThread = None
        GD.client_dic[accountName] = self
        self.tickTime = time.time()

    def clientTick(self):
        if GD.feature_switches.get('debugClient', False):
            self.client.debugClient(1)

        if not self.client:
            return

        if not self.client.scriptGameTick():
            print('client death:', self.accountName)
            self.close()
            return

        nCallPerFrame = 10
        cnt = 0

        while cnt<nCallPerFrame and self.remoteCallBuffer:
            rpc = self.remoteCallBuffer[0]
            self.remoteCallBuffer.pop(0)
            if rpc.callType==EntityMethodType.CELL:
                entityCall = self.client.player().cell
            else:
                entityCall = self.client.player().base

            try:
                GD.rpc_call_statistics[rpc.methodName] = GD.rpc_call_statistics.get(rpc.methodName, 0) + 1
                getattr(entityCall, rpc.methodName)(*rpc.args)
            except Exception as e:
                logging.error('call method error: %s %s'%(rpc, e))

    def login(self, accountType=0, loginAddr='', loginPort=0, clientData=''):
        accountName = '{}:{}'.format(accountType, self.accountName) if accountType else self.accountName
        print('login....', accountName, loginAddr, loginPort, clientData)

        if not clientData:
            clientData = json.dumps({
                'loginServerId': 1,
                'operatingSystem': "Windows 10  (10.0.19045) 64bit"
            })

        if loginAddr and loginPort:
            self.client = KBEngine.login(accountName, loginAddr, loginPort, clientData)
        else:

            self.client = KBEngine.login(accountName)
        self.playerAvatar = Player(self.client, AvatarBaseEntityCall(self.remoteCallBuffer), AvatarCellEntityCall(self.remoteCallBuffer), 'Avatar')
        self.playerAccount = Player(self.client, AccountBaseEntityCall(self.remoteCallBuffer), AccountCellEntityCall(self.remoteCallBuffer), 'Account')
        self.tickThread = RepeatTimer(random.random()*0.1, 0.1, self.clientTick, self.stopEvent)
        self.tickThread.setDaemon(True)
        self.tickThread.start()
        return self.client

    def updateTickTime(self):
        self.tickTime = time.time()

    @property
    def player(self):
        if not self.client:
            return None

        p = self.client.player()
        if not p:
            return None

        if isinstance(p, Account):
            return self.playerAccount

        return self.playerAvatar

    def close(self):
        self.client = None
        self.playerAvatar = None
        self.playerAccount = None
        self.remoteCallBuffer.clear()
        self.stopEvent.set()
        GD.client_dic.pop(self.accountName, None)

