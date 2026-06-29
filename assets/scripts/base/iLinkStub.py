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

    MAX_UNIQUE_ID_CACHE = 5000
    LINK_OVERDUE_TIME = 1800

    def __init__(self):
        self.pyAddTimer(self.LINK_OVERDUE_TIME, self.LINK_OVERDUE_TIME, gametimer.DEL_OLD_LINK_CACHE)

    def doNext(self):
        gameglobal.localBaseApp.fullPrepare(self.classname())

    def onTimer(self, tid, userArg):
        self._onTimerTrigger(tid, userArg)
        if utils.isBelongTimerTag(userArg):
            self._onTimerCallback(tid)
        elif gametimer.DEL_OLD_LINK_CACHE == userArg:
            self._delOldLinkCache()

    def addLinkInfo(self, uniqueId, recordData):
        if not uniqueId:
            return

        if uniqueId in self.linkCache:
            self.uniqueIdsCache.remove(uniqueId)

        self.linkCache[uniqueId] = recordData
        self.uniqueIdsCache.append(uniqueId)

    def getLinkInfo(self, uniqueId):
        _cache = self.linkCache.get(uniqueId, None)
        if _cache:
            return _cache

        return None

    def _delOldLinkCache(self):
        if len(self.linkCache) > ILinkStub.MAX_UNIQUE_ID_CACHE:
            extraLength = len(self.linkCache)-ILinkStub.MAX_UNIQUE_ID_CACHE
            delIdList = self.uniqueIdsCache[:extraLength]

            for uniqueId in delIdList:
                _cache = self.linkCache.get(uniqueId, None)
                if _cache is None:
                    continue

                self.linkCache.pop(uniqueId, None)
            self.uniqueIdsCache = self.uniqueIdsCache[extraLength:]

