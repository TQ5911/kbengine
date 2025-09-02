# -*- coding: utf-8 -*-
import KBEngine
import random
import gameconst
from KBEDebug import *
import aureola_aureola
import time

import gametimer
import actionContext
import userType
import sMath
import utils

class AureoleFromOtherVal(userType.UserSoleType):
    def __init__(self, aid, level, srcEntId):
        self.aureoleId = aid
        self.level = level
        self.srcEntId = srcEntId


class AureolesFromOhters(userType.UserDictType):
    def applyAureole(self, aureoleId, level, srcEntId):
        aureole = AureoleFromOtherVal(aureoleId, level, srcEntId)
        self[aureoleId] = aureole

    def _lateReload(self):
        super(AureolesFromOhters, self)._lateReload()

        for v in self.values():
            v.reloadScript()

        return

class ClientAureoleVal(userType.UserSoleType):
    def __init__(self, aid, level):
        self.aureoleId = aid
        self.level = int(level)

    def getClientData(self):
        return {'aureoleId':self.aureoleId, 'level': self.level}


class ClientAureoles(userType.UserDictType):
    def _lateReload(self):
        super(ClientAureoles, self)._lateReload()

        for v in self.values():
            v.reloadScript()

        return

class ServerAureoles(userType.UserDictType):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # k,v: aureolesId, aureolesCrtlId
        self._idToCtrlIdMap = {}
        self._ctrlIdToIdMap = {}
        self._wholeAreaAureoleList = []
        self._pendingTrapAureoId = None

    def getClientData(self, aureoleIds=None):
        aureoleIds = aureoleIds or self.keys()
        clientAureoles = ClientAureoles()
        for aureoleId in aureoleIds:
            if aureoleId not in self:
                continue

            sVal = self[aureoleId]
            clientAureoles[aureoleId] = ClientAureoleVal(aureoleId, sVal.level)
        return clientAureoles

    def addCtrlInPending(self, ctrlId):
        if self._pendingTrapAureoId is None:
            return

        self._idToCtrlIdMap[self._pendingTrapAureoId] = ctrlId
        self._ctrlIdToIdMap[ctrlId] = self._pendingTrapAureoId
        self._pendingTrapAureoId = None

    def addAureole(self, owner, aureoleId, level):
        if owner.IsAvatar:
            ERROR_MSG('addAureole owner could not support Avatar')
            return

        aureole = Aureole(aureoleId, level)
        self[aureoleId] = aureole

        aureole.initAureole(owner)
        if owner.isWholeAreaAureole(aureoleId):
            owner.spaceMgr.addWholeAureoleEntId(owner.id)
            if aureoleId not in self._wholeAreaAureoleList:
                self._wholeAreaAureoleList.append(aureoleId)
        owner.allClients.onAddAureole(ClientAureoleVal(aureoleId, level).getClientData())

    def removeAureole(self, owner, aureoleId):
        #0 to remove all aureoles
        disabledAureoleIds = self.disableAureole(owner, aureoleId)

        for aureoleId in disabledAureoleIds:
            if owner.isWholeAreaAureole(aureoleId):
                owner.spaceMgr.removeWholeAureoleEntId(owner.id)
                if aureoleId in self._wholeAreaAureoleList:
                    self._wholeAreaAureoleList.remove(aureoleId)

            aVal = self.pop(aureoleId)
            self._idToCtrlIdMap.pop(aureoleId, 0)
            self._ctrlIdToIdMap.pop(aVal.aureoleTrapId, 0)
            owner.allClients.onRemoveAureole(aureoleId)

    def disableAureole(self, owner, aureoleId):
        aureoleIds = (aureoleId,) if aureoleId else self.keys()
        disabledAureoleIds = []
        for aureoleId in aureoleIds:
            _aureole = self.get(aureoleId)
            if not _aureole:
                continue

            _aureole.doDisableAureole(owner)
            disabledAureoleIds.append(aureoleId)

        return disabledAureoleIds

    def _onLoop(self,owner, tid):
        for aureoleId in list(self.keys()):
            _aureole = self.get(aureoleId)
            if not _aureole:
                continue
            if not _aureole.areaAction or _aureole.loopTimeId!=tid:
                continue
            owner.doCombatActions(_aureole.areaAction, owner, owner, owner.id, lambda r:actionContext.AureoleCtx(owner.id, aureoleId, _aureole.level, r))

    def _lateReload(self):
        super(ServerAureoles, self)._lateReload()

        for v in self.values():
            v.reloadScript()

        return

    def getByCtrlId(self, ctrlId, default=None):
        id_ = self._ctrlIdToIdMap.get(ctrlId, None)
        return self.get(id_, default)

class Aureole(userType.UserSoleType):
    def __init__(self, aureoleId, level, tStartTime=0):
        self.aureoleId = aureoleId
        self.level = int(level)
        self.tStartTime = int(tStartTime or time.time())
        self.aureoleTargetIds = set()
        self.aureoleTrapId = 0
        self.loopTimeId = 0

    @property
    def name(self):
        return aureola_aureola.datas[self.aureoleId].get('name', '')

    @property
    def radius(self):
        return float(aureola_aureola.datas[self.aureoleId].get('radium') or 0)

    @property
    def effectTarget(self):
        return aureola_aureola.datas[self.aureoleId].get('effect', '')

    @property
    def maxTargetNum(self):
        return int(aureola_aureola.datas[self.aureoleId].get('maxEffectObjectNum') or 0)

    @property
    def duration(self):
        return float(aureola_aureola.datas[self.aureoleId].get('endByTime') or 0)

    @property
    def areaAction(self):
        return aureola_aureola.datas[self.aureoleId].get('areaAction', '')

    @property
    def loopIntervalTime(self):
        return int(aureola_aureola.datas[self.aureoleId].get('loopIntervalTime') or 0)

    def initAureole(self, owner):
        DEBUG_MSG('init aureole', self.aureoleId)
        if self.areaAction:
            loopIntervalTime = self.loopIntervalTime if self.loopIntervalTime else 1
            self.loopTimeId = owner.pyAddTimer(0.1, loopIntervalTime, gametimer.AUREOLE_LOOP)

        if owner.isWholeAreaAureole(self.aureoleId):
            self.addWholeAreaAureole(owner)
        else :
            owner._callback(0.1, 'addTAureoleTrap', (self.aureoleId,), gametimer.TIMER_TAG_ADD_AUREOLE_TRAP)

        remainTime = self.getRemainTime()
        if remainTime > 0:
            owner._callback(remainTime, 'removeAureole', (self.aureoleId,), gametimer.TIMER_TAG_REMOVE_AUREOLE)

    def getRemainTime(self):
        return self.tStartTime+self.duration-time.time()

    def addAureoleTrap(self, owner):
        owner.aureoleDic._pendingTrapAureoId = self.aureoleId
        # 在添加trap的一瞬间会触发身边所有人的trap，但是这时候trapId还没生成
        # 所以这里加个pending，类似于一个状态，表示处于加trap中
        self.aureoleTrapId = owner.addProximity(self.radius, self.radius, gameconst.AUREOLE_TRAP)

        if owner.aureoleDic._pendingTrapAureoId is None:
            # 走到这里说明 trap 添加时候触发了
            return

        owner.aureoleDic._pendingTrapAureoId = None
        owner.aureoleDic._idToCtrlIdMap[self.aureoleId] = self.aureoleTrapId
        owner.aureoleDic._ctrlIdToIdMap[self.aureoleTrapId] = self.aureoleId

        # if self.radius != -1 :
        #     for e in owner.entitiesInRange(self.radius+0.1):
        #         if e.IsCombatUnit and sMath.distance2D(owner.position, e.position) <= self.radius and utils.checkTargetType(self.effectTarget, owner, e):
        #             owner.onEnterTrap(e, 0, 0, self.aureoleTrapId, gameconst.AUREOLE_TRAP)
        #
        #     DEBUG_MSG('add aureole trap done', self)

    def addWholeAreaAureole(self, owner):
        owner.aureoleDic._wholeAreaAureoleList.append(self.aureoleId)

        for eid in list(owner.spaceMgr.spaceEntities.keys()):
            e = KBEngine.entities.get(eid)
            if e and not e.isDestroyed and e.IsCombatUnit and utils.checkTargetType(self.effectTarget, owner, e):
                self.addAureoleTarget(owner,e.id)
        for eid in list(owner.spaceMgr.players.keys()):
            e = KBEngine.entities.get(eid)
            if e and not e.isDestroyed and e.IsCombatUnit and utils.checkTargetType(self.effectTarget, owner, e):
                self.addAureoleTarget(owner,e.id)

    def addAureoleTarget(self, owner, targetId):
        if len(self.aureoleTargetIds)>=self.maxTargetNum:
            return

        target = KBEngine.entities.get(targetId)
        if not target or target.isDestroyed:
            return
        if target.addAureoleEffect(owner.id, self.aureoleId, self.level):
            self.aureoleTargetIds.add(targetId)

    def onLeaveAureoleRnage(self, owner, targetId):
        if targetId not in self.aureoleTargetIds:
            return

        reachMax = len(self.aureoleTargetIds)>=self.maxTargetNum
        target = KBEngine.entities.get(targetId)
        if target:
            if not target.isDestroyed:
                target.removeAureoleEffect(self.aureoleId, owner.id)

        self.aureoleTargetIds.remove(targetId)
        if reachMax and owner.id not in self.aureoleTargetIds:
            owner.onEnterTrap(owner, 0, 0, self.aureoleTrapId, gameconst.AUREOLE_TRAP)

    def doDisableAureole(self, owner):
        if self.loopTimeId > 0:
            owner.pyDelTimer(self.loopTimeId, gametimer.AUREOLE_LOOP)
            self.loopTimeId = 0

        for targetId in self.aureoleTargetIds:
            target = KBEngine.entities.get(targetId)
            if not target or target.isDestroyed:
                continue
            target.removeAureoleEffect(self.aureoleId, owner.id)
        owner.cancelController(self.aureoleTrapId)

    def getSavedDict(self):
        return {}

    def loadSavedDict(self, data):
        pass
