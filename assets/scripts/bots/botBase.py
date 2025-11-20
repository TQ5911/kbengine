import random
import time
import threading
import os
import sys
import json


def initBotConfig(filepath):
    basename = os.path.basename(filepath).split('.')[0]
    ROOT_PATH = os.path.realpath(filepath)
    max_depth = 0
    while os.path.basename(ROOT_PATH) != 'bots' and max_depth < 10:
        ROOT_PATH = os.path.dirname(ROOT_PATH)
        max_depth += 1
    # print(f'BOT ROOT_PATH: {ROOT_PATH}')
    config_path = os.path.join(ROOT_PATH, f'config/{basename}.json')
    if not os.path.exists(config_path):
        return {}
    BOT_CONFIG = json.load(open(config_path, 'r', encoding='utf-8'))
    return BOT_CONFIG

class Caller(object):
    def __init__(self, inst, func, cache):
        self.inst = inst
        self.func = func
        self.cache = cache

    def __call__(self, *args, **kwargs):
        getattr(self.inst, self.func)(*args, **kwargs)
        _e = self.cache['e']
        _e.wait()
        self.cache.pop('e')
        return self.cache['r']


class Getter(object):
    def __init__(self, inst, cache):
        self.inst = inst
        self.cache = cache

    def __getattr__(self, funcName):
        return Caller(self.inst, funcName, self.cache)


class TestEvent(threading.Event):
    def __init__(self):
        self.tStart = 0
        self.tEnd = 0
        super(TestEvent, self).__init__()

    def set(self):
        self.tEnd = time.time()
        super(TestEvent, self).set()

    def clear(self) -> None:
        self.tStart = time.time()
        super(TestEvent, self).clear()

    def costTime(self):
        return self.tEnd-self.tStart


class BotBase(object):
    def __init__(self, robot, client):
        self.robot = robot
        self.clientObj = client
        self.runTimes = 0
        self.isRun = 0
        self.runThread = threading.Thread(target=self.runAction, args=())
        self.multiDict = {}
        self.event = threading.Event()
        self._cache = {
        }

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
        # return self.player.base
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
        # chars = chars['characters']
        # if not chars:
        #     self.base.reqcreatebot(random.choice([1001, 1002, 1003, 1004]), self.botname, 2)
        #     return
        #
        # for char in chars:
        #     self.base.selectavatargame(char['gbid'])

    def onBecomePlayer(self):
        self.tagPrint('onBecomePlayer', self.botName, self.runTimes)
        # if self.robot.player().__class__.__name__=='PlayerAvatar':
        #     if not (self.runTimes or self.isRun):
        #         self.runThread.start()
        #         self.isRun = 1

    def onEnterWorld(self, *args):
        self.tagPrint('onEnterWorld', self.botName, self.runTimes, self.robot.player().__class__.__name__)
        if self.robot.player().__class__.__name__=='PlayerAvatar':
            if not (self.runTimes or self.isRun):
                self.runThread.start()
                self.isRun = 1

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

    def isAutoCombat(self):
        return self.player.autoCombat == 1

    @classmethod
    def recSearch(cls, obj, oriStr, deep):
        if not hasattr(obj, '__dict__'):
            return

        if deep > 10:
            return

        if hasattr(obj, 'entities'):
            cls.tagPrint(oriStr)
            return

        for k, v in obj.__dict__.items():
            newStr = f'{oriStr}->{k}'
            cls.recSearch(v, newStr, deep + 1)
