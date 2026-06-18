import json

import userType
import gameconst
from KBEDebug import *


class ResultBool(userType.UserSingleType):
    def __init__(self, boolVal, extra=-1):
        self.boolVal = boolVal
        self.extra = extra

    def __bool__(self):
        return self.boolVal

    def __str__(self):
        return '%s, %s' % (self.boolVal, self.extra)


class TaskCondResultCls(ResultBool):
    def __init__(self, boolVal, msgId=0, msgArgs=(), playerName=''):
        super(TaskCondResultCls, self).__init__(boolVal)
        self.msgId = msgId
        self.msgArgs = msgArgs
        self.playerName = playerName


class DummyObject(userType.UserSingleType):
    def __init__(_self, **kwargs):
        _self.__dict__.update(kwargs)


class AwardDetailCls(userType.UserSingleType):
    def __init__(self, **args):
        self.__dict__.update(args)

    def __str__(self):
        try:
            return '::'.join(['{}'] * len(self.__dict__)).format(*self.__dict__.values())
        except Exception as e:
            LOG_ERR('AwardDetailCls to json err:', e, vars(self))
            return ''

    def __getstate__(self):
        return self.__dict__

    def __setstate__(self, state):
        self.__init__(**state)

    def __getattr__(self, key, default=None):
        return self.__dict__.get(key, default)


class DuplicatedCallList(object):
    def __init__(self, objList):
        self.objList = objList

    def __getattr__(self, name):
        def func(*args, **kwargs):
            for obj in self.objList:
                getattr(obj, name)(*args, **kwargs)

        return func

class LockMinHpInfo(userType.UserSingleType):
    def __init__(self, srcType, srcId, hpPct, totalTimes, minHp):
        self.srcType = srcType
        self.srcId = srcId
        self.hpPct = hpPct
        self.totalTimes = totalTimes
        self.minHp = minHp
        self.effectTimes = 0

    def isValid(self):
        if self.totalTimes == -1:
            return True
        return self.effectTimes < self.totalTimes

