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
    GET_GUILD_LIST = 2
    CREATE_GUILD = 3
    JOIN_GUILD = 4
    EXIT = 5
    APPLY_JOIN = 6
    UP_LEVEL = 7


WEIGHTS_NO_GUILD = {
    State.GET_GUILD_LIST: 20,
    State.CREATE_GUILD: 1,
    State.APPLY_JOIN: 1,
}

WEIGHTS_HAS_GUILD = {
    State.EXIT: 50,
    State.IDLE: 50,
}



class PlayerDelegate(botBase.BotBase):
    def __init__(self, robot, botClient):
        super(PlayerDelegate, self).__init__(robot, botClient)
        self._state = State.IDLE

    def runAction(self):
        while True:
            print('current state:', self._state)
            if self._state == State.IDLE:
                if self.player.level < 20:
                    self._state = State.UP_LEVEL

                elif self.player.guildUUID:
                    _act = self.randomByWeight(WEIGHTS_HAS_GUILD)
                    self._state = _act

                else:
                    _act = self.randomByWeight(WEIGHTS_NO_GUILD)
                    self._state = _act

            elif self._state == State.GET_GUILD_LIST:
                print('will get')
                ret = self.wbase.getGuildList()
                print('getGuildList:', ret)
                self._state = State.IDLE

            elif self._state == State.CREATE_GUILD:
                self.wbase.runGmCommand('$getitems 0 0 1000 0 30000001')
                self.wbase.runGmCommand('$getitems 0 0 2 0 30990000')
                ret = self.wbase.createGuild({
                    'guildName': self.botName,
                    'desc': 'test',
                    'dspFlag': 0,
                    'joinCond': {
                        'level': 1,
                        'score': 1,
                        'auto': True,
                    },
                })
                print('after create guild', ret)

                self.base.modifyJoinCond({
                    'level': 1,
                    'score': 1,
                    'auto': True,
                })

                self._state = State.IDLE

            elif self._state == State.EXIT:
                ret = self.wbase.exitGuild()
                print('exitGuild:', ret)
                self._state = State.IDLE

            elif self._state == State.APPLY_JOIN:
                self.base.oneKeyGuildApply([])
                self._state = State.IDLE

            elif self._state == State.UP_LEVEL:
                self.base.runGmCommand('$setlv 0 21')
                self._state = State.IDLE

            print('after state:', self._state)
            time.sleep(1)

    def set_guildUUID(self, newGuildUUID):
        print('onGuildUUIDChanged', newGuildUUID, self.player.guildUUID)
        self.setResult(newGuildUUID)

    def onMessage(self, msgId, args):
        print('onMessage', args)
        if msgId == 54000002:
            if args[0] == '1000' and args[1] == '30000001':
                self.setResult(args[1])

            elif args[0] == '2' and args[1] == '30990000':
                self.setResult(args[1])

    def set_level(self, newLevel):
        print('onLevelChanged', newLevel, self.player.level)
        self.setResult(newLevel)

    def onGetGuildListData(self, guildList):
        print('onGetGuildListData', guildList)
        self.setResult(guildList)

    def onGetGuildData(self, guildData):
        print('onGetGuildData', guildData)


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
