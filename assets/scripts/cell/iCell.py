# -*- coding: utf-8 -*-

import KBEngine
from KBEDebug import *

import utils
import formula
import gameengine
import gametimer
import gameconst
import sMath
import gameglobal

import const_const as CONST


class ICell(KBEngine.Entity):
    IsNpc = False
    IsAvatar = False
    IsMonster = False
    IsCombatUnit = False
    IsAICombatUnit = False
    IsSummon = False
    IsCreation = False
    IsTeleporter = False
    IsCollection = False
    IsCrop = False
    IsPlunderPet = False
    IsSoulCardPillar = False
    IsDuelFlag = False
    IsBornPos = False
    IsAvatarReplica = False


    def isDestroying(self):
        return self.delayDestroyTimerID > 0

    def __init__(self):
        KBEngine.Entity.__init__(self)

        self.birthInMem = utils.curTS()

        return

    def onSpaceGone(self):
        LOG_DBG('onSpaceGone', self.base, self.isDestroyed)
        # 这里不再销毁base了，让base在onLoseCell里自己去销毁，否则base销毁时会先destroyCellEntity，这个时候cell已经被引擎自动销毁了
        # cellapp会出现EntityApp::destroyEntity: not found的报错
        self.safeDestroy()

    def onDestroy(self):
        getattr(self, '_onDestroy')()

    def _onDestroy(self):
        pass

    def safeDestroy(self, forceDestroy=False):
        # only call for entity no base component
        # only entity can call that have not base component
        if self.isDestroyed:
            return

        if self.isDestroying():
            if forceDestroy:
                self.stopDelayDestroyTimer()
            else:
                return

        if getattr(self, '_no_destroy', False):
            gameengine.panicStack("{}({}) destroy mistakenly".format(self.__class__.__name__, self.id))

        self._preSafeDestory()
        self.destroy()
        self._postSafeDestory()

    def destroyAttach(self):
        attachedIDList = self.popTempMiscProp(gameconst.EntityPropsEnum.attachedIDList, [])
        for attachedID in attachedIDList:
            attachedEntity = KBEngine.entities.get(attachedID)
            if attachedEntity:
                LOG_DBG("iCell.ICell _preSafeDestory", attachedEntity.id)
                attachedEntity.safeDestroy()

    def _preSafeDestory(self):
        if self.base and hasattr(self.base, 'onCellSafeDestroy'):
            self.base.onCellSafeDestroy()

        self.destroyAttach()

    def _postSafeDestory(self):
        pass

    def doEntireDestroy(self):
        if not hasattr(self, 'base') and self.base:
            self.safeDestroy()
        else:
            self.base.doEntireDestroy(False, False)

    def renewalCell(self, attr):
        for k, v, in attr.items():
            setattr(self, k, v)

    def evadeTrigger(self):
        if not self.isReal():
            return True

        if self.isDestroyed:
            return True

        return False

    def callMethod(self, methodName, methodArgs):
        if not hasattr(self, methodName):
            LOG_ERR('callMethod:: methodName {} not found'.format(methodName), methodArgs)
            return

        getattr(self, methodName)(*methodArgs)

    def getMailBox(self):
        _v = self.__reduce_ex__()
        return _v[0](_v[1][0])

    def preReloadScript(self):
        pass

    def reloadScript(self):
        for _pName, pVal in self.__dict__.items():
            if _pName.startswith('__'):
                continue

            if hasattr(pVal, 'reloadScript'):
                pVal.reloadScript()

        self._reloadMiscProp(self.tempMiscProps)
        self._reloadMiscProp(self.miscProps)

    def postReloadScript(self):
        if not hasattr(super(ICell, self), 'postReloadScript'):
            return

        super(ICell, self).postReloadScript()

    def safeTeleport(self, dstCell, pos, direction, spaceNo):
        try:
            self.beforeTeleport(spaceNo)
        except:
            gameengine.panicStack('error occured during _beforeTeleport', self.id, self.gbId, spaceNo)
        self.teleport(dstCell, pos, direction)

    def onTeleportNear(self, fromCell, pos, direction, spaceNo):
        gameglobal.cellAvatarCount += 1
        LOG_INFO("add avatar cnt when teleport", gameglobal.cellAvatarCount)
        fromCell.safeTeleport(self, pos, direction, spaceNo)

    def beforeTeleport(self, spaceNo):
        pass

    @classmethod
    def classname(cls):
        return cls.__name__

    def checkReloadScript(self, res, su=None):
        return

    def _onTtlDestroy(self):
        pass

    def onTimer(self, timerID, userData):
        self._onTimerTrigger(timerID, userData)
        if userData == gametimer.TIMER_CELL_DELAY_SAFE_DESTROY:
            self.onDelayTimerSafeDestroy()
        elif userData == gametimer.TIMER_ON_CELL_TTL_DESTROY:
            if not self.isDestroyed:
                self._onTtlDestroy()
        elif hasattr(super(ICell, self), 'onTimer'):
            super(ICell, self).onTimer(timerID, userData)

    def stopDelayDestroyTimer(self):
        if self.delayDestroyTimerID:
            self.pyDelTimer(self.delayDestroyTimerID, gametimer.TIMER_CELL_DELAY_SAFE_DESTROY)
            self.delayDestroyTimerID = 0

    def delaySafeDestroy(self, delay=0.3):
        if self.isDestroyed:
            return

        if getattr(self, '_no_destroy', None):
            gameengine.panicStack("%s(%d) destroy mistakenly" % (self.__class__.__name__, self.id))

        self._preDelaySafeDestroy(delay)

        self.stopDelayDestroyTimer()
        self.delayDestroyTimerID = self.pyAddTimer(delay, 0, gametimer.TIMER_CELL_DELAY_SAFE_DESTROY)

    def onDelayTimerSafeDestroy(self):
        if self.isDestroyed:
            return
        self.delayDestroyTimerID = 0
        self.safeDestroy(forceDestroy=True)

    def _preDelaySafeDestroy(self, delay):
        """延迟销毁前置hook"""

    def setTempMiscProp(self, propId, value):
        if type(propId) is not int:
            LOG_ERR('setPersistentMiscProp: propId must be int')
            return

        self.tempMiscProps[propId] = value

    def popTempMiscProp(self, propId, default=None):
        return self.tempMiscProps.pop(propId, default)

    def getTempMiscProp(self, propId, default=None):
        return self.tempMiscProps.get(propId, default)

    def setPersistentMiscProp(self, propId, value):
        if type(propId) is not int:
            LOG_ERR('setPersistentMiscProp: propId must be int')
            return

        self.miscProps[propId] = value

    def hasTempMiscProp(self, propId):
        return propId in self.tempMiscProps

    def hasPersistentMiscProp(self, propId):
        return propId in self.miscProps

    def setDefaultPersistentMiscProp(self, propId, value):
        if self.hasPersistentMiscProp(propId):
            return self.miscProps[propId]

        self.miscProps[propId] = value
        return value

    def popPersistentMiscProp(self, propId, default=None):
        return self.miscProps.pop(propId, default)

    def getPersistentMiscProp(self, propId, default=None):
        return self.miscProps.get(propId, default)

    def _reloadMiscProp(self, propDic):
        for _prop in propDic.values():
            if hasattr(_prop, 'reloadScript'):
                _prop.reloadScript()
            elif isinstance(_prop, dict):
                for _k, v in _prop.items():
                    if hasattr(_k, 'reloadScript'):
                        _k.reloadScript()
                    if hasattr(v, 'reloadScript'):
                        v.reloadScript()
            elif hasattr(_prop, '__iter__'):
                for v in _prop:
                    if hasattr(v, 'reloadScript'):
                        v.reloadScript()

    def isVisible(self, target):
        return True

    def telToPos(self, pos, toDir=None):
        self.position = pos
        if toDir:
            self.direction = toDir

    def checkAIEventListened(self, eventId):
        """All Entity need check event listened method"""
        return False

    def scriptNavigate(self, dstPos, speed, distance=0, faceMovement=True, 
                       layer=gameconst.SpaceLayer.DEFAULT, userData=None, 
                       extra=None):
        maxDis = 128  # 引擎预留参数，暂时没有意义
        _width = CONST.datas['navAgentWidth']['value']
        if extra is None:
            extra = {
                'sl': _width, # 搜索起始点的长
                'sw': _width, # 搜索起始点的宽
                'sh': 4.0, # 搜索起始点的高
            }
        else:
            extra['sl'] = _width
            extra['sw'] = _width
            extra['sh'] = 4.0
        
        navController = self.navigate(
            dstPos, 
            speed, 
            distance, 
            maxDis, 
            maxDis, 
            faceMovement, 
            layer, 
            True, 
            userData,
            extra
        )
        return navController

    def showMsg(self, msgId, args):
        pass

    def __repr__(self):
        return "%s id = %d" % (super(ICell, self).__repr__(), self.id,)

    def getCurrentSpace(self):
        return gameglobal.localSpaceIDMap.get(self.spaceID)

    def resetLimitcall(self):
        self.methodPool.clear()

    def setToBattle(self, **kwargs):
        LOG_WARN(f"Class::{self.__class__.__name__} setToBattle not implement", kwargs)

    def setToNeutral(self, **kwargs):
        LOG_WARN(f"Class::{self.__class__.__name__} setToNeutral not implement", kwargs)

    def setToFriendly(self, **kwargs):
        LOG_WARN(f"Class::{self.__class__.__name__} setToFriendly not implement", kwargs)

    def setBaseGlobalIdx(self, idx):
        self.baseGlobalIdx = idx

    def dunData(self):
        _mapId = formula.fetchMapId(self.spaceNo)
        _dunData = utils.getDunModuleData(_mapId)
        if not _dunData:
            return None

        gid, gct = utils.splitFromGameEntityId(self.gameEntityId)
        gid = str(gid)
        return _dunData.get(gid, None)

    def batchlyCall(self, iterableCall, batchNum, interval=0.5, callback=None):
        it = iter(iterableCall)
        for i in range(batchNum):
            callObj = next(it, None)
            if callObj is None:
                callback and callback()
                return
            try:
                callObj()
            except Exception as e:
                LOG_ERR('batchlyCall error', e)
                continue

        self.addTimerCB(interval, 'batchlyCall', (it, batchNum, interval, callback), gametimer.TIMER_TAG_BATCHLY_CALL)
