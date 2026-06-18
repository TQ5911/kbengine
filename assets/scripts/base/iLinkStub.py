# -*- coding: utf-8 -*-

import copy

import KBEngine
from KBEDebug import *

import gameglobal
import gametimer
import utils

import iGlobal
import iBaseNoCell
import iTimer

class ILinkStub(iGlobal.IGlobal, iBaseNoCell.IBaseNoCell, iTimer.ITimer):

    MAX_UNIQUEID_CACHE = 5000
    LINK_OVERDUE_TIME = 1800

    def __init__(self):
        self.pyAddTimer(self.LINK_OVERDUE_TIME, self.LINK_OVERDUE_TIME, gametimer.DEL_OLD_LINK_CACHE)

    def doNext(self):
        gameglobal.localBaseApp.fullPrepare(self.classname())

    def onTimer(self, tid, userArg):
        self._onTimerTrigger(tid, userArg)
        if utils.isBelongTimerTag(userArg):
            self._onTimerCallback(tid)
        elif userArg == gametimer.DEL_OLD_LINK_CACHE:
            self._delOldLinkCache()

    def addLinkInfo(self, uniqueId, record):
        if not uniqueId:
            return

        if uniqueId in self.linkCache:
            self.uniqueIdCache.remove(uniqueId)

        self.linkCache[uniqueId] = record
        self.uniqueIdCache.append(uniqueId)

    def getLinkInfo(self, uniqueId):
        cache = self.linkCache.get(uniqueId, None)
        if cache:
            return cache

        return None

    def _delOldLinkCache(self):
        if len(self.linkCache) > ILinkStub.MAX_UNIQUEID_CACHE:
            extraLength = len(self.linkCache)-ILinkStub.MAX_UNIQUEID_CACHE
            delIdList = self.uniqueIdCache[:extraLength]

            for uniqueId in delIdList:
                cache = self.linkCache.get(uniqueId, None)
                if cache is None:
                    continue

                self.linkCache.pop(uniqueId, None)
            self.uniqueIdCache = self.uniqueIdCache[extraLength:]

