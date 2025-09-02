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


class ICell(KBEngine.Entity):
    IsNpc = False
    IsAvatar = False
    IsMonster = False
    IsCombatUnit = False
    IsAICombatUnit = False
    IsPet = False
    IsSummon = False
    IsCreation = False
    IsTeleporter = False
    IsAvatarMirror = False
    IsCollection = False
    IsCrop = False
    IsPlunderPet = False
    IsSoulCardPillar = False
    IsDuelFlag = False
    IsBornPos = False


    def isDestroying(self):
        return self.delayDestroyTimerID > 0

    def isBot(self):
        return False

    def __init__(self):
        KBEngine.Entity.__init__(self)

        self.birthInMem = utils.getNow()

        return

    def onSpaceGone(self):
        DEBUG_MSG('onSpaceGone', self.base, self.isDestroyed)
        # 这里不再销毁base了，让base在onLoseCell里自己去销毁，否则base销毁时会先destroyCellEntity，这个时候cell已经被引擎自动销毁了
        # cellapp会出现EntityApp::destroyEntity: not found的报错
        self.safeDestroy()
        return

    def onDestroy(self):
        getattr(self, '_onDestroy')()

        return

    def _onDestroy(self):
        pass

    def safeDestroy(self, forceDestroy=False):
        # only call for entity no base component

        # only entity can call that have not base component

        if self.isDestroyed:
            return

        if self.isDestroying():
            if forceDestroy:
                self.cancelDelayDestroyTimer()
            else:
                return

        if getattr(self, '_no_destroy', False):
            gameengine.reportCritical("%s(%d) destroy mistakenly" % (self.__class__.__name__, self.id))

        self._preSafeDestory()
        self.destroy()
        self._postSafeDestory()

        return

    def _preSafeDestory(self):
        if self.base and hasattr(self.base, 'onCellSafeDestroy'):
            self.base.onCellSafeDestroy()

    def _postSafeDestory(self):
        pass

    def entireDestroy(self):
        if not hasattr(self, 'base') and self.base:
            self.safeDestroy()
        else:
            self.base.entireDestroy(False, False)

    def evadeTrigger(self):
        if not self.isReal():
            return True

        if self.isDestroyed:
            return True

        return False

    def renewalCell(self, attr):
        for k, v, in attr.items():
            setattr(self, k, v)

        return

    def callMethod(self, methodName, methodArgs):
        if not hasattr(self, methodName):
            ERROR_MSG('callMethod:: methodName {} not found'.format(methodName), methodArgs)
            return

        getattr(self, methodName)(*methodArgs)

        return

    def getMailBox(self):
        v = self.__reduce_ex__()
        return v[0](v[1][0])

    def preReloadScript(self):
        return

    def reloadScript(self):
        for pName, pVal in self.__dict__.items():
            if pName.startswith('__'):
                continue

            if hasattr(pVal, 'reloadScript'):
                pVal.reloadScript()

        self._reloadMiscProp(self.miscProps)
        self._reloadMiscProp(self.tempMiscProps)
        return

    def postReloadScript(self):
        if hasattr(super(ICell, self), 'postReloadScript'):
            super(ICell, self).postReloadScript()

    def safeTeleport(self, dstCell, pos, dir, spaceNo):
        try:
            self.beforeTeleport(spaceNo)
        except:
            gameengine.reportCritical('error occured during _beforeTeleport', self.id, self.gbId, spaceNo)
        self.teleport(dstCell, pos, dir)
        return

    def onTeleportNear(self, fromCell, pos, dir, spaceNo):
        fromCell.safeTeleport(self, pos, dir, spaceNo)
        return

    def beforeTeleport(self, spaceNo):
        pass

    @classmethod
    def classname(cls):
        return cls.__name__

    def isPersistent(self):
        return False

    def everyClients(self):
        return self.otherClients

    def myClientEntity(self, id):
        return utils.Faker()

    def myClient(self):
        return utils.Faker()

    def inRange2D(self, e2, dist):
        if not e2 or self.spaceID != e2.spaceID:
            return False

        return sMath.inRange2D(dist, self.position, e2.position)

    def inRange3D(self, e2, dist):
        if not e2 or self.spaceID != e2.spaceID:
            return False

        return sMath.inRange3D(dist, self.position, e2.position)

    def needWitnessed(self):
        return False

    def checkReloadScript(self, res, su=None):
        return

    def _ttlDestroy(self):
        pass

    def onTimer(self, timerID, userData):
        self._onTimer(timerID, userData)
        if userData == gametimer.TIMER_CELL_SAFE_DESTROY:
            self.onDelayTimerSafeDestroy()
        elif userData == gametimer.TIMER_CELL_TTL_DESTROY:
            if not self.isDestroyed:
                self._ttlDestroy()
        elif hasattr(super(ICell, self), 'onTimer'):
            super(ICell, self).onTimer(timerID, userData)

    def cancelDelayDestroyTimer(self):
        if self.delayDestroyTimerID:
            self.pyDelTimer(self.delayDestroyTimerID, gametimer.TIMER_CELL_SAFE_DESTROY)
            self.delayDestroyTimerID = 0

    def delaySafeDestroy(self, delay=0.3):
        if self.isDestroyed:
            return
        if getattr(self, '_no_destroy', False):
            gameengine.reportCritical("%s(%d) destroy mistakenly" % (self.__class__.__name__, self.id))

        self._preDelaySafeDestroy(delay)

        self.cancelDelayDestroyTimer()
        self.delayDestroyTimerID = self.pyAddTimer(delay, 0, gametimer.TIMER_CELL_SAFE_DESTROY)

    def _preDelaySafeDestroy(self, delay):
        """延迟销毁前置hook"""

    def onDelayTimerSafeDestroy(self):
        if self.isDestroyed:
            return
        self.delayDestroyTimerID = 0
        self.safeDestroy(forceDestroy=True)

    def setTempMiscProp(self, propId, value):
        if type(propId) is not int:
            ERROR_MSG('setPersistentMiscProp: propId must be int')
            return

        self.tempMiscProps[propId] = value

    def getTempMiscProp(self, propId, default=None):
        return self.tempMiscProps.get(propId, default)

    def popTempMiscProp(self, propId, default=None):
        return self.tempMiscProps.pop(propId, default)

    def hasTempMiscProp(self, propId):
        return propId in self.tempMiscProps

    def setPersistentMiscProp(self, propId, value):
        if type(propId) is not int:
            ERROR_MSG('setPersistentMiscProp: propId must be int')
            return

        self.miscProps[propId] = value

    def hasPersistentMiscProp(self, propId):
        return propId in self.miscProps

    def setDefaultPersistentMiscProp(self, propId, value):
        if self.hasPersistentMiscProp(propId):
            return self.miscProps[propId]

        self.miscProps[propId] = value
        return value

    def getPersistentMiscProp(self, propId, default=None):
        return self.miscProps.get(propId, default)

    def popPersistentMiscProp(self, propId, default=None):
        return self.miscProps.pop(propId, default)

    def _reloadMiscProp(self, propDic):
        for prop in propDic.values():
            if hasattr(prop, 'reloadScript'):
                prop.reloadScript()
            elif isinstance(prop, dict):
                for k, v in prop.items():
                    if hasattr(k, 'reloadScript'):
                        k.reloadScript()
                    if hasattr(v, 'reloadScript'):
                        v.reloadScript()
            elif hasattr(prop, '__iter__'):
                for v in prop:
                    if hasattr(v, 'reloadScript'):
                        v.reloadScript()

    def isVisible(self, target):
        return True

    def checkEventListened(self, eventId):
        """All Entity need check event listened method"""
        return False

    def telToPos(self, pos, toDir=None):
        self.position = pos
        if toDir:
            self.direction = toDir

    def scriptNavigate(self, dstPos, speed, dis=0, faceMovement=True, layer=gameconst.SpaceLayer.DEFAULT,
                       userData=None):
        maxDis = 128  # 引擎预留参数，暂时没有意义
        navController = self.navigate(dstPos, speed, dis, maxDis, maxDis, faceMovement, layer, True, userData)
        return navController

    def __repr__(self):
        return "%s id = %d" % (super(ICell, self).__repr__(), self.id,)

    def showMsg(self, msgId, args):
        pass

    def getCurrentSpace(self):
        return gameglobal.localSpaceIDMap.get(self.spaceID)

    def resetLimitcall(self):
        self.methodPool.clear()

    def setToBattle(self, **kwargs):
        WARNING_MSG(f"Class::{self.__class__.__name__} setToBattle not implement", kwargs)

    def setToNeutral(self, **kwargs):
        WARNING_MSG(f"Class::{self.__class__.__name__} setToNeutral not implement", kwargs)

    def setToFriendly(self, **kwargs):
        WARNING_MSG(f"Class::{self.__class__.__name__} setToFriendly not implement", kwargs)

    def setBaseGlobalIdx(self, idx):
        self.baseGlobalIdx = idx

    def dunData(self):
        _mapId = formula.getMapId(self.spaceNo)
        _dunData = utils.getDunModuleData(_mapId)
        if not _dunData:
            return None

        gid, gct = utils.splitGameEntityId(self.gameEntityId)
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
                ERROR_MSG('batchlyCall error', e)
                continue

        self._callback(interval, 'batchlyCall', (it, batchNum, interval, callback), gametimer.TIMER_TAG_BATCHLY_CALL)
