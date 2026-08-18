# -*- coding: utf-8 -*-
import KBEngine

import dataUtils
from KBEDebug import *
import utils
import gameconst
import formula
import gametimer

import message_Message_def as MMD
import mounts_mounts as MOUNTS
import conflict_conflict_def as C_C_DD
import gamePlay_gamePlay as GPGPD
import mounts_set as MSD
import gamedecorator


class IMount(object):
    def __init__(self):
        pass

    def _initMountCell(self):
        if not self.curMountId:
            self._exitRiding()
        elif self.hasState(gameconst.StateEnum.riding):
            self.setCurMountSpeedBuff(False)

    @property
    def curMountId(self):
        return self.appearance.outfitData.mountId

    def doAddMountAction(self, opUUID, ctx, itemId, durationDays):
        LOG_INFO('do get mount action:', itemId, durationDays)
        itemData = dataUtils.getCommItemData(itemId)
        if not itemData:
            LOG_ERR('itemData invalid:', itemId)
            return gameconst.UseItemEnum.FALSE

        mountId = itemData['indexID']
        if mountId not in MOUNTS.datas:
            LOG_ERR('mountId invalid:', mountId)
            return gameconst.UseItemEnum.FALSE

        pid = self.setPendingUseId(opUUID, ctx)
        self.base.doAddMount(pid, mountId, durationDays)
        return gameconst.UseItemEnum.PENDING

    def setCurMountCell(self, mountId):
        self.enableOutfit(gameconst.OutfitEnum.mount, mountId)

    # 由于跟随情况下上坐骑的玩家更多，所以这里用反状态，当玩家跟随不上坐骑，记下标志位
    @utils.isMyself
    def setFollowRideFlag(self, exposed, isRide):
        pass

    def enterRidingByAction(self):
        self._enterRidingWithCast(False, False)

    @utils.isMyself
    @gamedecorator.crossServer
    def enterRiding(self, exposed, isCast):
        LOG_DBG('enter riding')
        if not self._checkCanRide(True):
            return

        self._enterRidingWithCast(True, isCast)

    def _checkCanRide(self, bMsg):
        if not self.curMountId:
            if bMsg:
                self.showMsg(MMD.datas.pressRideButtonNotEquipMount, [])
            return False

        if not GPGPD.datas[formula.fetchMapId(self.spaceNo)]['ifRide']:
            return False

        return True

    def _enterRidingWithCast(self, bMsg, isCast):
        if isCast:
            self._commonNeedCast(
                C_C_DD.datas.summonMount, 
                gameconst.StateEnum.summonMount, 
                gameconst.CastEnum.ride,
                '_enterRiding', 
                (bMsg, '', None), 
                failedFunc='', 
                failedArgs=None)
        else:
            self._enterRiding(bMsg, '', None)

    def _enterRiding(self, bMsg, finishFunc, finishArgs):
        if not self._checkCanRide(bMsg) or\
                (not self.checkConflictState(C_C_DD.datas.ride, bMsg=bMsg)) or\
                (not self._setMountState(gameconst.StateEnum.riding)):
            if finishFunc:
                getattr(self, finishFunc)(*finishArgs)
            return

        self.setCurMountSpeedBuff(False)
        if finishFunc:
            getattr(self, finishFunc)(*finishArgs)

    @utils.isMyself
    @gamedecorator.crossServer
    def exitRiding(self, exposed):
        LOG_DBG('exit riding')
        self._exitRiding()

    def _exitRiding(self, exitType=gameconst.MountExitType.all):
        if self.hasState(gameconst.StateEnum.riding):
            if exitType == gameconst.MountExitType.fly:
                return

            self.removeState(gameconst.StateEnum.riding)

    def _setMountState(self, state):
        _ret = self.setState(state)
        if _ret:
            opUUID = KBEngine.genUUID64()
            self.base.setAvatarVariableByTag(
                'curMountID', 
                self.curMountId, 
                opUUID,
                gameconst.VarChangeSrcEnum.VAR_SRC_ENTER_MOUNT, 
                'enter mount state:{}'.format(state))

        return _ret

    def _onExitRiding(self, byConflictState):
        LOG_DBG('exit riding:', byConflictState)
        self._removeCurMountSpeedBuff(False)
        opUUID = KBEngine.genUUID64()
        self.base.setAvatarVariableByTag('curMountID', 0, opUUID,
                                         gameconst.VarChangeSrcEnum.VAR_SRC_EXIT_MOUNT, 'exit mount state')

    def getMountState(self):
        if self.hasState(gameconst.StateEnum.riding):
            return gameconst.TeamMountState.ride
        else:
            return gameconst.TeamMountState.none

    def setCurMountSpeedBuff(self, isFly):
        if self.delayAddMountSpeedBuffTimer:
            self.cancelTimerCB(self.delayAddMountSpeedBuffTimer, gametimer.TIMER_TAG_DELAY_ADD_MOUNT_SPEED_BUFF)
            self.delayAddMountSpeedBuffTimer = 0

        _mountSpeed = MSD.datas["mountspeed"]["value"]
        self.delayAddMountSpeedBuffTimer = self.addTimerCB(_mountSpeed, '_setCurMountSpeedBuff', (isFly, ), gametimer.TIMER_TAG_DELAY_ADD_MOUNT_SPEED_BUFF)

    def _setCurMountSpeedBuff(self, isFly):
        if self.delayAddMountSpeedBuffTimer:
            self.cancelTimerCB(self.delayAddMountSpeedBuffTimer, gametimer.TIMER_TAG_DELAY_ADD_MOUNT_SPEED_BUFF)
            self.delayAddMountSpeedBuffTimer = 0

        LOG_DBG('set curMount buff')
        if not self.curMountId:
            LOG_ERR('set cur mount buff but not has mount ID')
            return

        buffId = MOUNTS.datas[self.curMountId]['speedEnhance']
        if self.hasBuff(buffId):
            return

        self.addBuff(buffId, 1, self.id)

    def _removeCurMountSpeedBuff(self, isFly):
        if self.delayAddMountSpeedBuffTimer:
            self.cancelTimerCB(self.delayAddMountSpeedBuffTimer, gametimer.TIMER_TAG_DELAY_ADD_MOUNT_SPEED_BUFF)
            self.delayAddMountSpeedBuffTimer = 0

        if not self.curMountId:
            LOG_ERR('remove cur mount speed buff:', )
            return

        buffId = MOUNTS.datas[self.curMountId]['speedEnhance']
        self.removeBuff(buffId)

    def _changeSpacRecycleMount(self, isFromEdge):
        if not isFromEdge:
            gpData = GPGPD.datas[formula.fetchMapId(self.spaceNo)]
            if not gpData['ifRide'] and self.hasState(gameconst.StateEnum.riding):
                self._exitRiding(gameconst.MountExitType.ride)
            return

        if self._isMountLegal(self.spaceNo):
            return

        self.addTimerCB(2, '_notifyExitMount', (self.spaceNo, ), gametimer.TIMER_TAG_NOTIFY_EXIT_MOUNT)

    def _notifyExitMount(self, oldSpaceNo):
        if self.spaceNo != oldSpaceNo:
            return

        if self._isMountLegal(oldSpaceNo):
            return

        self.addTimerCB(2, '_notifyExitMount', (oldSpaceNo, ), gametimer.TIMER_TAG_NOTIFY_EXIT_MOUNT)

    def _exitIllegalMount(self, lastSpaceNo):
        self.popTempMiscProp(gameconst.EntityPropsEnum.mountIllegalTimer, None)
        if self.spaceNo != lastSpaceNo:
            return

        gpData = GPGPD.datas[formula.fetchMapId(lastSpaceNo)]
        if not gpData['ifRide'] and self.hasState(gameconst.StateEnum.riding):
            self._exitRiding(gameconst.MountExitType.ride)

    def _isMountLegal(self, spaceNo):
        gpData = GPGPD.datas[formula.fetchMapId(spaceNo)]
        if not gpData['ifRide'] and self.hasState(gameconst.StateEnum.riding):
            return False

        return True

