# coding: utf-8

import KBEngine
from KBEDebug import *

import math
import random
import uuid
import json
from datetime import datetime

import Math
import gameconfig
import gameconst
import gametimer
import LogTrackingMgr
import utils
import redisUtils
import gamedecorator
import functools

import const_const as CONST
import PKData_PKData as PKD_PKDD

class IEnmity(object):
    def __init__(self):
        LOG_DBG("IEnmity::__init__")
        self.enmityList = []

    def onUpdateEnmityList(self, reason, enmityList):
        LOG_INFO('IEnmity::onUpdateEnmityList', reason, enmityList)
        self.enmityList = enmityList
        if reason not in (gameconst.EnmityDatasType.ADD, gameconst.EnmityDatasType.REMOVE):
            return
        self.resetAllTargetTypeCache()

    def inEnmityList(self, gbId):
        if gbId in self.enmityList:
            return True
        return self.tempEnmityDict.get(gbId, 0) > utils.curTS()

    def onTempEnmityAttackedBy(self, attacker):
        if attacker.gbId == self.gbId:
            return
        self._touchTempEnmity(attacker.gbId, True)

    def onTempEnmityCombatWith(self, gbId):
        self._touchTempEnmity(gbId, False)

    def _touchTempEnmity(self, gbId, forceAdd):
        if not gbId:
            return
        if not forceAdd and gbId not in self.tempEnmityDict:
            return
        isNew = not self.inEnmityList(gbId)
        duration = PKD_PKDD.datas['enemyListAutoRemove']['value']
        self.tempEnmityDict[gbId] = utils.curTS() + duration
        LOG_DBG('IEnmity::_touchTempEnmity', gbId, self.tempEnmityDict[gbId], forceAdd)
        self._ensureTempEnmityTimer()
        if isNew:
            self._refreshTempEnmityTargets((gbId,))

    def _refreshTempEnmityTargets(self, gbIds):
        targets = []
        for gbId in gbIds:
            target = utils.getAvatarByGbId(gbId)
            if target and not target.isDestroyed and target.spaceNo == self.spaceNo:
                targets.append(target)
        if targets:
            self.resetTargetTypeCache(targets)

    def _purgeExpiredTempEnmity(self):
        now = utils.curTS()
        expired = [gbId for gbId, expireTime in self.tempEnmityDict.items() if expireTime <= now]
        for gbId in expired:
            self.tempEnmityDict.pop(gbId, None)
        if expired:
            self._refreshTempEnmityTargets([gbId for gbId in expired if not self.inEnmityList(gbId)])

    def _ensureTempEnmityTimer(self):
        if self.tempEnmityTimerId or not self.tempEnmityDict:
            return
        self.tempEnmityTimerId = self.addTimerCB(
            1, '_onTempEnmityExpire', (), gametimer.TIMER_TAG_TEMP_ENMITY)

    def _onTempEnmityExpire(self):
        self.tempEnmityTimerId = 0
        self._purgeExpiredTempEnmity()
        self._ensureTempEnmityTimer()

    @gamedecorator.crossServer
    @utils.isMyself
    @gamedecorator.crossServer
    def getTempEnmityList(self, exposed):
        self._purgeExpiredTempEnmity()
        datas = [
            {'gbId': gbId, 'expireTime': expireTime}
            for gbId, expireTime in self.tempEnmityDict.items()
        ]
        LOG_DBG('IEnmity::getTempEnmityList', datas)
        self.client.onTempEnmityList(datas)