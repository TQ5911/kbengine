# -*- coding: utf-8 -*-
import KBEngine
import random
import gameconst
from KBEDebug import *
import time

import userType


class AwardArgs(userType.UserSingleType):
    def __init__(self, lv=0, avatarLv=0, **kwargs):
        self.avatarLv = avatarLv
        self.lv = lv
        for _k, v in kwargs.items():
            setattr(self, _k, v)

    @property
    def expEx(self):
        return 0

    def addArg(self, name, val):
        setattr(self, name, val)


class AwardContext(userType.UserSingleType):
    def __init__(self):
        self.extra = None

    def addContextVar(self, name, val):
        self.extra[name] = val

    def __getattr__(self, item):
        return self.extra.get(item, '')

    def __str__(self):
        return '%s:%s' % (self.srcType, str(vars(self)))


class CommonContext(AwardContext):
    def __init__(self, mailId, argsDic=None, **kwargs):
        self.args = AwardArgs(**(argsDic or {}))
        self.mailId = mailId
        self.extra = kwargs
        self.itemArgs = {}

    def __getstate__(self):
        _st = {}
        if self.mailId:
            _st['mailId'] = self.mailId
        if vars(self.args):
            _st['args'] = vars(self.args)
        if self.extra:
            _st['extra'] = self.extra
        return _st

    def __setstate__(self, state):
        self.__init__(state.get('mailId', 0), state.get('args', None), **state.get('extra', {}),)


class DropAwardCtx(AwardContext):
    def __init__(self, srcEntId, srcEntLevel, argsDic=None, **keywordArgs):
        self.level = srcEntLevel
        self.srcEntId = srcEntId
        self.args = AwardArgs(**(argsDic or {}))
        self.extra = keywordArgs

        if srcEntLevel:
            self.args.lv = srcEntLevel

    def __getstate__(self):
        _st = {}
        if self.srcEntId:
            _st['srcEntId'] = self.srcEntId
        if self.level:
            _st['level'] = self.level
        if vars(self.args):
            _st['args'] = vars(self.args)
        if self.extra:
            _st['extra'] = self.extra
        return _st

    def __setstate__(self, state):
        _argsDic = state.get('args', {})
        srcEntId = state.get('srcEntId', 0)
        srcEntLevel = state.get('level', 0)
        self.__init__(srcEntId, srcEntLevel, _argsDic, **state.get('extra', {}))
