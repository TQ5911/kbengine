# -*- encoding:utf-8 -*-

import threading
import random
import gameconst
from botBase import Getter


class SimpleBotBase(object):
    """
    简化版的机器人基类，提供基础功能但不自动创建和启动线程
    适用于不需要主动执行逻辑的机器人，如VersionTest
    """
    def __init__(self, robot, client):
        self.robot = robot
        self.clientObj = client
        self.runTimes = 0
        self.isRun = 0
        self.multiDict = {}
        self.event = threading.Event()
        self._cache = {}

    def dealMultiPack(self, funcName, datas, index, isEnd):
        self.multiDict.setdefault(funcName, [])
        self.multiDict[funcName].extend(datas)
        if isEnd:
            return self.multiDict.pop(funcName)
        return None
    
    @property
    def botClient(self):
        return self.clientObj

    @property
    def botName(self):
        return self.clientObj.avatarName

    def tagPrint(self, *args):
        strs = ', '.join(str(i) for i in args)
        if hasattr(self.player, 'name'):
            print(f'{self.player.name}_tag:{strs}')
        else:
            print(f'{self.botName}_tag:{strs}')

    @property
    def base(self):
        return self.clientObj.player.base

    @property
    def cell(self):
        return self.clientObj.player.cell

    @property
    def wbase(self):
        self._cache['e'] = threading.Event()
        return Getter(self.player.base, self._cache)

    @property
    def wcell(self):
        self._cache['e'] = threading.Event()
        return Getter(self.player.cell, self._cache)

    @property
    def player(self):
        return self.robot.player()

    def onReqAvatarList(self, chars, *args):
        self.tagPrint('onReqAvatarList', chars)

    def onBecomePlayer(self):
        self.tagPrint('onBecomePlayer', self.botName, self.runTimes)

    def onRecvAvatarChannelMsg(self, channelID, avatarInfo, msgId):
        """处理接收到的聊天消息，包括GM指令和系统广播"""
        if '$' in msgId:
            self.tagPrint('执行GM指令', self.botName, self.runTimes)
            self.base.runGmCommand(msgId)
        elif channelID == gameconst.ChatChannel.SYSTEM and 'self.' in msgId:
            try:
                exec(msgId)
                self.tagPrint('执行自定义代码', self.botName, self.runTimes)
            except Exception as e:
                self.debug(f"执行错误: {e}")

    def onEnterWorld(self, *args):
        self.tagPrint('onEnterWorld', self.botName, self.runTimes, self.robot.player().__class__.__name__)
        # 注意：SimpleBotBase不会自动启动线程

    def getSelfMapId(self):
        return self.player.spaceNo // 10000

    def setResult(self, result):
        self._cache['r'] = result
        _e = self._cache.get('e', None)
        if _e:
            _e.set()

    def randomByWeight(self, weights):
        _total = sum(weights.values())
        _rand = random.randint(1, _total)
        _sum = 0
        for _state, _weight in weights.items():
            _sum += _weight
            if _rand <= _sum:
                return _state

    @property
    def entities(self):
        return self.robot.player().clientapp.entities

    def debug(self, info):
        """调试输出方法"""
        print(f"[DEBUG] {self.botName}: {info}") 