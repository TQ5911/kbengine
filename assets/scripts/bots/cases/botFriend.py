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
    SEARCHING = 2
    ACCEPT = 3
    REMOVE_FRIEND = 4
    WAIT_SEARCH_RESULT = 5
    REMOVE_RECENT = 6
    REMOVE_BLOCK = 7
    REJECT_REQUESTS = 8


WEIGHTS = {
    State.SEARCHING: 1,
    State.ACCEPT: 1,
    State.REMOVE_FRIEND: 1,
    State.REMOVE_RECENT: 1,
    State.REMOVE_BLOCK: 1,
    State.REJECT_REQUESTS: 1,
}


class Options(object):
    SEARCH = 1,
    SEND_MSG = 2,
    BLOCK = 3,



WEIGHTS_AFTER_SEARCH = {
    Options.SEARCH: 1,
    Options.SEND_MSG: 1,
    Options.BLOCK: 1,
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
        self.itemId = 30030010
        self.uniqueId = None
        self.robot = robot
        self.botClient = botCLient
        self.attach = None
        self.mailUUID = None
        self.requests = {}
        self.friends = {}
        self.stranger = {}
        self.blocks = {}
        self._state = State.IDLE

    def onBecomePlayer(self):
        print('bot login success :%s' % self.botClient.accountName)
        threading.Thread(target=self.runAction).start()

    def onUpdateBlocks(self, blocks):
        print('onUpdateBlocks', blocks)
        for _data in blocks:
            self.blocks[_data['gbId']] = _data

    def onRemoveBlocks(self, gbIds):
        print('onRemoveBlocks', gbIds)
        for _gbId in gbIds:
            if _gbId in self.blocks:
                del self.blocks[_gbId]

    def randomByWeight(self, weights):
        _total = sum(weights.values())
        _rand = random.randint(1, _total)
        _sum = 0
        for _state, _weight in weights.items():
            _sum += _weight
            if _rand <= _sum:
                return _state

    def runAction(self):
        while True:
            if self._state == State.IDLE:
                self._state = self.randomByWeight(WEIGHTS)

            elif self._state == State.SEARCHING:
                self.base.searchFriend('')
                self._state = State.WAIT_SEARCH_RESULT

            elif self._state == State.REMOVE_FRIEND:
                _gbIds = list(self.friends.keys())
                if _gbIds:
                    _gbId = random.choice(_gbIds)
                    self.base.removeFriend(_gbId)

                self._state = State.IDLE

            elif self._state == State.REMOVE_BLOCK:
                _gbIds = list(self.blocks.keys())
                if _gbIds:
                    _gbId = random.choice(_gbIds)
                    self.base.removeFromBlock(_gbId)

                self._state = State.IDLE

            elif self._state == State.REJECT_REQUESTS:
                _gbIds = list(self.requests.keys())
                if _gbIds:
                    _gbId = random.choice(_gbIds)
                    self.base.rejectRequest(_gbId)

                self._state = State.IDLE

            elif self._state == State.REMOVE_RECENT:
                self._state = State.IDLE

            elif self._state == State.ACCEPT:
                self.acceptFriendRequest()
                self._state = State.IDLE

            time.sleep(1)

    def onRemoveFriendRequests(self, gbIds):
        print('onRemoveFriendRequests', gbIds)
        for _gbId in gbIds:
            if _gbId in self.requests:
                del self.requests[_gbId]

    def onUpdateStrangerData(self, strangers):
        print('onUpdateStrangerData', strangers)
        for _data in strangers:
            self.stranger[_data['gbId']] = _data

    def onUpdateFriendsFull(self, friends):
        print('onUpdateFriendsFull', friends)
        for _data in friends:
            self.friends[_data['gbId']] = _data

    def onRemoveFriends(self, gbIds):
        print('onRemoveFriends', gbIds)
        for _gbId in gbIds:
            if _gbId in self.friends:
                del self.friends[_gbId]

    def acceptFriendRequest(self):
        if not self.requests:
            return

        _gbIds = list(self.requests.keys())
        _gbId = random.choice(_gbIds)
        self.base.acceptRequest(_gbId)

    def onFriendRequests(self, requests):
        print('onFriendRequests', requests)
        for _data in requests:
            if _data['gbId'] == self.player.gbId:
                continue
    
            self.requests[_data['gbId']] = _data

    def onSearchFriends(self, friends):
        print('onSearchFriends', friends)
        _targets = []
        for _data in friends:
            if _data['gbId'] == self.player.gbId:
                continue

            _targets.append(_data['gbId'])

        _target = random.choice(_targets)

        _opr = self.randomByWeight(WEIGHTS_AFTER_SEARCH)
        if _opr == Options.SEARCH:
            self.base.sendFriendRequest(_target)

        elif _opr == Options.SEND_MSG:
            self.base.sendFriendMsg(_target, '你好，一开始是第一章，然后是第二章，然后是第三章，最后是第几张我就忘了')

        elif _opr == Options.BLOCK:
            self.base.blockPlayer(_target)

        if self._state == State.WAIT_SEARCH_RESULT:
            self._state = State.IDLE


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
