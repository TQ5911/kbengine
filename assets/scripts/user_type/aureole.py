# -*- coding: utf-8 -*-
import KBEngine
import gameconst
from KBEDebug import *
import aureola_aureola as A_AD
import time

import gametimer
import actionContext
import userType
import utils

class AureoleFromOtherVal(userType.UserSingleType):
    def __init__(self, aid, level, srcEntId, srcHostEntId=None):
        self.aureoleId = aid
        self.level = level
        self.srcEntId = srcEntId
        self.srcHostEntId = srcHostEntId


class AureolesFromOhters(userType.UserDictType):
    def applyAureole(self, aureoleId, level, srcEntId, srcHostEntId=None):
        aureole = AureoleFromOtherVal(aureoleId, level, srcEntId, srcHostEntId)
        self[aureoleId] = aureole

    def _lateReload(self):
        super(AureolesFromOhters, self)._lateReload()

        for _v in self.values():
            _v.reloadScript()

class ClientAureoleVal(userType.UserSingleType):
    def __init__(self, aid, level):
        self.level = int(level)
        self.aureoleId = aid

    def getClientData(self):
        return {'aureoleId':self.aureoleId, 'level': self.level,}


class ClientAureoles(userType.UserDictType):
    def _lateReload(self):
        super(ClientAureoles, self)._lateReload()

        for _v in self.values():
            _v.reloadScript()


class ServerAureoles(userType.UserDictType):
    def __init__(self, *args, **keywordArgs):
        super().__init__(*args, **keywordArgs)
        # k,v: aureolesId, aureolesCrtlId
        self._ctrlIdToIdMap = {}
        self._idToCtrlIdMap = {}
        self._wholeAreaAuraList = []
        self._pendingTrapAureoId = None

    def getClientData(self, aureoleIds=None):
        aureoleIds = aureoleIds or self.keys()
        clientAureoles = ClientAureoles()
        for _auraId in aureoleIds:
            if _auraId not in self:
                continue

            sVal = self[_auraId]
            clientAureoles[_auraId] = ClientAureoleVal(_auraId, sVal.level)
        return clientAureoles

    def addCtrlInPending(self, ctrlId):
        if self._pendingTrapAureoId is None:
            return

        self._idToCtrlIdMap[self._pendingTrapAureoId] = ctrlId
        self._ctrlIdToIdMap[ctrlId] = self._pendingTrapAureoId
        self._pendingTrapAureoId = None

    def addAureole(self, owner, aureoleId, level):
        if owner.IsAvatar:
            LOG_ERR('addAureole owner could not support Avatar')
            return

        _aura = Aureole(aureoleId, level)
        self[aureoleId] = _aura

        _aura.initAureole(owner)
        if owner.isWholeAreaAura(aureoleId):
            owner.spaceMgr.addWholeAuraEntId(owner.id)
            if aureoleId not in self._wholeAreaAuraList:
                self._wholeAreaAuraList.append(aureoleId)
        owner.allClients.onAddAureole(ClientAureoleVal(aureoleId, level).getClientData())

    def removeAureola(self, owner, aureoleId):
        #0 to remove all aureoles
        disabledAureoleIds = self.doDisableAura(owner, aureoleId)

        for aureoleId in disabledAureoleIds:
            if owner.isWholeAreaAura(aureoleId):
                owner.spaceMgr.removeWholeAureoleEntId(owner.id)
                if aureoleId in self._wholeAreaAuraList:
                    self._wholeAreaAuraList.remove(aureoleId)

            _aVal = self.pop(aureoleId)
            self._idToCtrlIdMap.pop(aureoleId, 0)
            self._ctrlIdToIdMap.pop(_aVal.aureoleTrapId, 0)
            owner.allClients.onRemoveAureole(aureoleId)

    def doDisableAura(self, owner, aureoleId):
        _aureoleIds = (aureoleId,) if aureoleId else self.keys()
        _disabledAureoleIds = []
        for aureoleId in _aureoleIds:
            _aura = self.get(aureoleId)
            if not _aura:
                continue

            _aura.doDisableAureole(owner)
            _disabledAureoleIds.append(aureoleId)

        return _disabledAureoleIds

    def _onLoop(self,owner, tid):
        for _auraId in list(self.keys()):
            _aura = self.get(_auraId)
            if not _aura:
                continue
            if not _aura.areaAction or _aura.loopTimeId!=tid:
                continue
            owner.doCombatActions(
                _aura.areaAction, 
                owner, 
                owner, 
                owner.id, 
                lambda r:actionContext.AureoleCtx(owner.id, _auraId, _aura.level, r))

    def _lateReload(self):
        super(ServerAureoles, self)._lateReload()

        for _v in self.values():
            _v.reloadScript()

    def getByCtrlId(self, ctrlId, default=None):
        _id = self._ctrlIdToIdMap.get(ctrlId, None)
        return self.get(_id, default)

class Aureole(userType.UserSingleType):
    def __init__(self, aureoleId, level, tStartTime=0):
        self.level = int(level)
        self.aureoleId = aureoleId
        self.tStartTime = int(tStartTime or time.time())
        self.aureoleTargetIds = set()
        self.loopTimeId = 0
        self.aureoleTrapId = 0

    @property
    def radius(self):
        return float(A_AD.datas[self.aureoleId].get('radium') or 0)

    @property
    def name(self):
        return A_AD.datas[self.aureoleId].get('name', '')

    @property
    def effectTarget(self):
        return A_AD.datas[self.aureoleId].get('effect', '')

    @property
    def maxTargetNum(self):
        return int(A_AD.datas[self.aureoleId].get('maxEffectObjectNum') or 0)

    @property
    def duration(self):
        return float(A_AD.datas[self.aureoleId].get('endByTime') or 0)

    @property
    def areaAction(self):
        return A_AD.datas[self.aureoleId].get('areaAction', '')

    @property
    def loopIntervalTime(self):
        return int(A_AD.datas[self.aureoleId].get('loopIntervalTime') or 0)

    def initAureole(self, owner):
        LOG_DBG('init aureole', self.aureoleId)
        if self.areaAction:
            _loopIntervalTime = self.loopIntervalTime if self.loopIntervalTime else 1
            self.loopTimeId = owner.pyAddTimer(0.1, _loopIntervalTime, gametimer.TIMER_AURA_LOOP)

        if owner.isWholeAreaAura(self.aureoleId):
            self.addWholeAreaAureole(owner)
        else :
            owner.addTimerCB(0.1, 'addTAureoleTrap', (self.aureoleId,), gametimer.TIMER_TAG_ADD_AUREOLE_TRAP)

        _remainTime = self.getRemainTime()
        if _remainTime > 0:
            owner.addTimerCB(_remainTime, 'removeAureolaById', (self.aureoleId,), gametimer.TIMER_TAG_REMOVE_AUREOLE)

    def addAureoleTrap(self, owner):
        owner.auraDic._pendingTrapAureoId = self.aureoleId
        # 在添加trap的一瞬间会触发身边所有人的trap，但是这时候trapId还没生成
        # 所以这里加个pending，类似于一个状态，表示处于加trap中
        self.aureoleTrapId = owner.addProximity(self.radius, self.radius, gameconst.AURA_TRAP)

        if owner.auraDic._pendingTrapAureoId is None:
            # 走到这里说明 trap 添加时候触发了
            return

        owner.auraDic._pendingTrapAureoId = None
        owner.auraDic._idToCtrlIdMap[self.aureoleId] = self.aureoleTrapId
        owner.auraDic._ctrlIdToIdMap[self.aureoleTrapId] = self.aureoleId

    def getRemainTime(self):
        return self.tStartTime+self.duration-time.time()

    def addWholeAreaAureole(self, owner):
        owner.auraDic._wholeAreaAuraList.append(self.aureoleId)

        for eid in list(owner.spaceMgr.spaceEntitiesDic.keys()):
            _e = KBEngine.entities.get(eid)
            if _e and not _e.isDestroyed and _e.IsCombatUnit and utils.checkTargetTypeValid(self.effectTarget, owner, _e):
                self.addAureoleTarget(owner,_e.id)
        for eid in list(owner.spaceMgr.players.keys()):
            _e = KBEngine.entities.get(eid)
            if _e and not _e.isDestroyed and _e.IsCombatUnit and utils.checkTargetTypeValid(self.effectTarget, owner, _e):
                self.addAureoleTarget(owner,_e.id)

    def onLeaveAureoleRnage(self, owner, targetId):
        if targetId not in self.aureoleTargetIds:
            return

        _reachMax = len(self.aureoleTargetIds)>=self.maxTargetNum
        _target = KBEngine.entities.get(targetId)
        if _target:
            if not _target.isDestroyed:
                _target.removeAureoleEffect(self.aureoleId, owner.id)

        self.aureoleTargetIds.remove(targetId)
        if _reachMax and owner.id not in self.aureoleTargetIds:
            owner.onEnterTrap(owner, 0, 0, self.aureoleTrapId, gameconst.AURA_TRAP)

    def addAureoleTarget(self, owner, targetId):
        if len(self.aureoleTargetIds)>=self.maxTargetNum:
            return

        _target = KBEngine.entities.get(targetId)
        if not _target or _target.isDestroyed:
            return
        if _target.addAureoleEffect(owner.id, self.aureoleId, self.level):
            self.aureoleTargetIds.add(targetId)

    def doDisableAureole(self, owner):
        if self.loopTimeId > 0:
            owner.pyDelTimer(self.loopTimeId, gametimer.TIMER_AURA_LOOP)
            self.loopTimeId = 0

        for targetId in self.aureoleTargetIds:
            _target = KBEngine.entities.get(targetId)
            if not _target or _target.isDestroyed:
                continue
            _target.removeAureoleEffect(self.aureoleId, owner.id)
        owner.cancelController(self.aureoleTrapId)

    def loadSavedDict(self, data):
        pass

    def getSavedDict(self):
        return {}

