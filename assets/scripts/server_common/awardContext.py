# -*- coding: utf-8 -*-
import KBEngine
import random
import gameconst
from KBEDebug import *
import time

import userType
import sMath
import utils


class AwardArgs(userType.UserSoleType):
    def __init__(self, lv=0, avatarLv=0, **kwargs):
        self.lv = lv
        self.avatarLv = avatarLv
        for k, v in kwargs.items():
            setattr(self, k, v)

    @property
    def expEx(self):
        return 0

    def addArg(self, name, val):
        setattr(self, name, val)


class AwardContext(userType.UserSoleType):
    def __init__(self):
        self.extra = None

    def __str__(self):
        return '%s:%s' % (self.srcType, str(vars(self)))

    def __getattr__(self, item):
        return self.extra.get(item, '')

    def addContextVar(self, name, val):
        self.extra[name] = val


class CommonContext(AwardContext):
    def __init__(self, mailId, argsDic=None, **kwargs):
        self.mailId = mailId
        self.args = AwardArgs(**(argsDic or {}))
        self.extra = kwargs
        self.itemArgs = {}

    def __getstate__(self):
        st = {}
        if self.mailId:
            st['mailId'] = self.mailId
        if vars(self.args):
            st['args'] = vars(self.args)
        if self.extra:
            st['extra'] = self.extra
        return st

    def __setstate__(self, state):
        self.__init__(state.get('mailId', 0), state.get('args'), **state.get('extra', {}))


class DropAwardCtx(AwardContext):
    def __init__(self, srcEntId, srcEntLevel, argsDic=None, **kwargs):
        self.srcEntId = srcEntId
        self.level = srcEntLevel
        self.args = AwardArgs(**(argsDic or {}))
        self.extra = kwargs

        if srcEntLevel:
            self.args.lv = srcEntLevel

    def __getstate__(self):
        st = {}
        if self.srcEntId:
            st['srcEntId'] = self.srcEntId
        if self.level:
            st['level'] = self.level
        if vars(self.args):
            st['args'] = vars(self.args)
        if self.extra:
            st['extra'] = self.extra
        return st

    def __setstate__(self, state):
        srcEntId = state.get('srcEntId', 0)
        argsDic = state.get('args', {})
        srcEntLevel = state.get('level', 0)
        self.__init__(srcEntId, srcEntLevel, argsDic, **state.get('extra', {}))
