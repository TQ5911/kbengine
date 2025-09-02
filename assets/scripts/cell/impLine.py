# -*- coding: utf-8 -*-
from KBEDebug import *

import KBEngine

from common.KBEDebug import INFO_MSG
import formula
import gameconst
import gameengine
import complexTeleportOption
import utils
import gamedecorator
import Math
import sMath
import random
import gameglobal
import dungeonSrc

import message_Message_def as MMD
import conflict_conflict_def as CCD
import const_const as CONST
import gamePlay_gamePlay as GGD

import gametimer


class ImpLine(object):
    def _buildEnterLineExtra(self, position, dataDic=None):
        pos = position or self.position
        extra = dataDic or {}

        extra['position'] = pos
        if self.teamId:
            extra['teamUUID'] = self.teamId

        return extra

    @utils.isMyself
    def applyEnterLine(self, exposed, lineType):
        if lineType == formula.getMapId(self.spaceNo):
            return

        lineNo = formula.getLineNo(self.spaceNo)
        enterPos = formula.whatSpaceBornPoint(lineType)
        self.applyEnterLineInternal(lineType, lineNo, enterPos, self.direction, False)

    def enterLineByNpc(self, lineType, *args, **kwargs):
        lineNo = formula.getLineNo(self.spaceNo)
        lineType = int(lineType)
        mapId = lineType

        if not formula.isLineSpace(self.spaceNo):
            return

        enterPos, direction = formula.whatSpaceBornPosAndDir(lineType)

        if formula.isDuelMapId(lineType):
            _options = complexTeleportOption.ComplexTeleportOptions(teleportType=gameconst.ComplexTeleportType.ENTER)
            self.tryRegiTeleportOutsideRecord(self.spaceNo, _options)

        self.applyEnterLineInternal(lineType, lineNo, enterPos, direction)

    def applyEnterLineInternal(self, lineType, lineNo, position, direction, extra=None):
        INFO_MSG('zt: applyEnterLineInternal', lineType, lineNo, position, direction, extra)
        if formula.isDungeonSpace(self.spaceNo):
            # 从副本进入大世界一定要走icomplexTeleport过来
            if not (isinstance(extra, dict) and extra.get('toLine')):
                WARNING_MSG('dungeon enter line without toLine')
                return

        position = position or self.position
        direction = direction or self.direction
        extra = self._buildEnterLineExtra(position, extra)

        gameengine.getLineStub(lineType).enterLine(lineNo, self.base, self.gbId, position, direction, extra)

    # 已经在LineStub占了人数坑位，如果进入失败需要释放坑位
    def beginEnterLine(self, lineType, lineNo, spaceBox, position, direction, extra):
        INFO_MSG('zt: beginEnterLine', lineType, lineNo, spaceBox.id)
        cmpLineType = gameconst.TeleportLock.ENTER_LINE

        if extra.get('isLogin'):
            self._onEnterLine(0, lineType, lineNo, extra)
        else:
            if self.teleportLock and self.teleportLock != cmpLineType:
                failReason = 'locked:%s'%self.teleportLock
                gameengine.getLineStub(lineType).enterLineFailed(lineNo, self.base, self.gbId, {'reason':failReason})
                return

            self.aquireTeleportLock(cmpLineType)

            spaceNo = formula.getLineSpaceNo(lineType, lineNo)

            if formula.spaceInWorldLine(self.spaceNo):
                extra['fromSpaceMgrBox'] = self.spaceMgr

            self.teleportToCell(spaceBox.cell, spaceNo, position, direction, '_onEnterLine',
                                (self.spaceNo, lineType, lineNo, extra))

    def _onEnterLine(self, fromSpaceNo, lineType, lineNo, extra):
        INFO_MSG('_onEnterLine', fromSpaceNo, lineType, lineNo, extra)

        succInfo = {}
        succInfo['teamUUID'] = self.teamId

        if extra.get('callback'):
            func = getattr(self, extra['callback'])
            func and func(*extra.get('callbackArgs', ()))

        self.spaceMgrId = self.getCurrentSpace().spaceMgrId
        self.spaceMgr.onPlayerEnter(self.id)

        fromSpaceMgrBox = extra.get('fromSpaceMgrBox')
        if fromSpaceMgrBox:
            fromSpaceMgrBox.onPlayerLeave(self.gbId, self.id, self.base)

        if self.teleportLock:
            self.releaseTeleportLock(gameconst.TeleportLock.ENTER_LINE)

        gameengine.getLineStub(lineType).enterLineSuccess(lineNo, self.base, self.gbId, succInfo)

        if formula.isLineSpace(fromSpaceNo):
            self._clearLineState(fromSpaceNo)

        if formula.isDuelGround(self.spaceNo):
            ret = self.setPKModel(gameconst.PKModel.PEACE)
            if ret:
                self.changePKModeResetTargetId()

    def _checkSwitchLine(self, toLineNo):
        if not formula.isLineSpace(self.spaceNo):
            return False

        if toLineNo < 0:
            return False
        if self.hasState(gameconst.State.Teleporting):
            return False

        lineType = formula.getMapId(self.spaceNo)
        if toLineNo >= utils.getLineMaxNumber(lineType):
            return False

        if toLineNo == formula.getLineNo(self.spaceNo):
            return False

        return True

    @utils.isMyself
    def applySwitchLine(self, exposed, toLineNo):
        src = dungeonSrc.DungeonFromClientSrc(self.base, self.gbId)
        self.switchLineAndPosition(toLineNo, None, src=src)

    def switchLineAndPosition(self, toLineNo, toPosition, src=None, extra=None):
        canSwitch = self._checkSwitchLine(toLineNo)
        INFO_MSG('applySwitchLine', self.spaceNo, toLineNo, canSwitch, src, extra)
        if not canSwitch:
            return

        self.checkEnterLine(formula.getMapId(self.spaceNo), toLineNo, toPosition,
                            'onCheckSwitchLine', (self.spaceNo, toLineNo, toPosition, src, extra))

    def _onCheckSwitchLineReCheckCond(self, checkCode, checksumSpaceNo, toLineNo):
        if checkCode != gameconst.EnterLineCode.CAN_ENTER:
            WARNING_MSG("_onCheckSwitchLineReCheckCond:: cant enter", checkCode, checksumSpaceNo, toLineNo)
            return False

        if not self._checkSwitchLine(toLineNo):
            WARNING_MSG("_onCheckSwitchLineReCheckCond:: checkswitchline failed", checkCode, checksumSpaceNo, toLineNo)
            return False

        if not formula.isLineSpace(checksumSpaceNo):
            WARNING_MSG("_onCheckSwitchLineReCheckCond:: checksumSpaceNo failed", checkCode, checksumSpaceNo, toLineNo)
            return False

        lineType = formula.getMapId(self.spaceNo)
        checklineType = formula.getMapId(checksumSpaceNo)
        if lineType != checklineType:
            WARNING_MSG("_onCheckSwitchLineReCheckCond:: checklinetype failed", checkCode, checksumSpaceNo,
                        self.spaceNo, toLineNo)
            return False

        return True

    def onCheckSwitchLine(self, checkCode, checksumSpaceNo, toLineNo, toPosition, src, extra):
        INFO_MSG("onCheckSwitchLine::", checkCode, checksumSpaceNo, toLineNo, toPosition, src, extra)
        if checkCode == gameconst.EnterLineCode.CAN_ENTER:
            _result = self._onCheckSwitchLineReCheckCond(checkCode, checksumSpaceNo, toLineNo)
            extra = extra if extra is not None else {}
            if not _result:
                failFunc = extra.get("failCallback", '')
                failArgs = extra.get("callbackArgs", ())
                gameengine.getLineStub(formula.getMapId(checksumSpaceNo)).checkCanEnterLineFinallyFailed(
                    toLineNo, self.base, self.gbId, extra, failFunc, (checkCode, *failArgs))
                return
            extra.update({'src': src})
            self._switchLineInternal(toLineNo, toPosition, extra=extra)

        else:
            extra = extra if extra is not None else {}
            failFunc = extra.get("failCallback", '')
            failArgs = extra.get("callbackArgs", ())
            _fn = getattr(self, failFunc, None)
            _fn and _fn(checkCode, *failArgs)

    def _switchLineInternal(self, toLineNo, toPosition=None, toDir=None, extra=None):
        INFO_MSG('_switchLineInternal', self.spaceNo, toLineNo)
        extra = extra or {}
        _cbfn = "_switchLineInternalAfterCast"
        _cbargs = (toLineNo, toPosition, toDir, extra if extra else {})

        if extra.get('hasCast'):
            getattr(self, _cbfn)(*_cbargs)
        else:
            self._commonNeedCast(CCD.datas.teleportCast, gameconst.State.Teleporting, gameconst.CastType.teleport,
                                _cbfn, _cbargs)

    def _switchLineInternalAfterCast(self, toLineNo, toPosition, toDir, extra):
        lineType = formula.getMapId(self.spaceNo)
        lineNo = formula.getLineNo(self.spaceNo)

        extra = self._buildEnterLineExtra(toPosition, extra)

        if toDir:
            extra['dir'] = toDir

        # 这时候可能被传到副本里，会报错
        if formula.isLineSpace(self.spaceNo):
            gameengine.getLineStub(lineType).switchLine(lineNo, toLineNo, self.base, self.gbId, extra)

    # 已经在目标分线占了人数坑位，如果进入失败需要释放坑位
    def beginSwitchLine(self, lineType, fromLineNo, toLineNo, toSpaceBox, extra):
        INFO_MSG('beginSwitchLine', lineType, self.spaceNo, fromLineNo, toLineNo, toSpaceBox.id)

        if self.teleportLock and self.teleportLock!=gameconst.TeleportLock.SWITCH_LINE:
            failReason = 'locked:%s'%self.teleportLock
            gameengine.getLineStub(lineType).switchLineFailed(fromLineNo, toLineNo, self.base, self.gbId, {'reason':failReason})
            return

        self.aquireTeleportLock(gameconst.TeleportLock.SWITCH_LINE)

        spaceNo = formula.getLineSpaceNo(lineType, toLineNo)
        enterPos = extra.pop('position', self.position)
        enterDir = extra.pop('dir', self.direction)

        self.teleportToCell(toSpaceBox.cell, spaceNo, enterPos, enterDir, '_onSwitchLine',
                            (lineType, fromLineNo, toLineNo, extra))

    def _onSwitchLine(self, lineType, fromLineNo, toLineNo, extra):
        INFO_MSG('_onSwitchLine', lineType, fromLineNo, toLineNo, extra)
        gameengine.getLineStub(lineType).switchLineSuccess(fromLineNo, toLineNo, self.base, self.gbId, extra)

        if self.teleportLock:
            self.releaseTeleportLock(gameconst.TeleportLock.SWITCH_LINE)

        if extra and extra.get('callback'):
            func = getattr(self, extra['callback'])
            func and func(*extra.get('callbackArgs', ()))

    @utils.isMyself
    def applyLeaveLine(self, exposed):
        INFO_MSG('applyLeaveLine', self.spaceNo)
        if formula.isDuelGround(self.spaceNo):
            mapId, outRecord = self.tryGetLastTeleportOutesideRecord(self.spaceNo)
            if outRecord:
                self.applyEnterLineInternal(
                    mapId,
                    formula.getLineNo(outRecord.spaceNo),
                    outRecord.position,
                    outRecord.direction)

    # 有的时候已经离开分线了，调用这个接口清除分线状态，需要传fromSpaceNo，因为self.spaceNo已经是离开后场景了
    # toSpaceNo==0时是传到了其他场景后清除源分线的状态
    def _applyLeaveLineInternal(self, fromSpaceNo, toSpaceNo, toPosition, toDirection):
        INFO_MSG('_applyLeaveLineInternal', self.spaceNo, fromSpaceNo, toSpaceNo)
        if toSpaceNo and not formula.isLineSpace(self.spaceNo):
            return

        if formula.spaceInWorldLine(self.spaceNo) and toSpaceNo:
            updateTimer = self.popTempMiscProp(gameconst.AvatarProps.updateWorldLineAreaTimer, 0)
            if updateTimer:
                self.pyDelTimer(updateTimer, gametimer.AVATAR_UPDATE_AREAID)

        lineType = formula.getMapId(fromSpaceNo)
        gameengine.getLineStub(lineType).leaveLine(self.base, self.gbId, fromSpaceNo, toSpaceNo, toPosition, toDirection)

    def _clearLineState(self, clearSpaceNo):
        lineType = formula.getMapId(clearSpaceNo)
        gameengine.getLineStub(lineType).leaveLine(self.base, self.gbId, clearSpaceNo, 0,
                                                                gameconst.POSITION_ZERO, gameconst.DIRECTION_ZERO)

    def beginLeaveLine(self, fromSpaceNo, toSpaceNo, toPosition, toDirection):
        INFO_MSG('beginLeaveLine', self.spaceNo, fromSpaceNo, toSpaceNo, toPosition, toDirection)

        # 可以不指定toSpaceNo，比如从分线内进入分线，已经离开老分线后才调用_applyLeaveLineInternal，这里只
        # 执行上老分线的离开函数
        if not toSpaceNo:
            pass
        elif formula.isLineSpace(toSpaceNo):
            toLineType = formula.getMapId(toSpaceNo)
            toLineNo = formula.getLineNo(toSpaceNo)
            extra = {'callback': '_onLeaveLine', 'callbackArgs': (fromSpaceNo, toSpaceNo)}
            self.applyEnterLineInternal(toLineType, toLineNo, toPosition, toDirection, extra)
        else:
            ERROR_MSG('teleport to %s is not supported' % toSpaceNo)

    def _onLeaveLine(self, fromSpaceNo, toSpaceNo):
        INFO_MSG('_onLeaveLine', self.spaceNo, fromSpaceNo, toSpaceNo)

    def beginGoBackLine(self, lineSpaceNo, spaceBox, dstPos, dstDir, callback, callbackArgs):
        INFO_MSG('beginGoBackLine', lineSpaceNo, callback, callbackArgs)
        fromSpaceNo = self.spaceNo
        self.teleportToCell(spaceBox.cell, lineSpaceNo, dstPos, dstDir, '_onGoBackLine',
                            (fromSpaceNo, callback, callbackArgs))

    def _onGoBackLine(self, fromSpaceNo, callback, callbackArgs):
        INFO_MSG('_onGoBackLine', fromSpaceNo, callback, callbackArgs)

        func = getattr(self, callback)
        func and func(*callbackArgs)

    def checkEnterLine(self, lineType, lineNo, dstPos, cbName, cbArgs):
        extra = self._buildEnterLineExtra(dstPos)

        gameengine.getLineStub(lineType).checkCanEnterLine(lineNo, self.base, self.gbId, extra, cbName, cbArgs)

    def checkAutoSwitchLine(self, dstPos, dstDir, cbName, cbArgs):
        extra = self._buildEnterLineExtra(dstPos)
        extra['dir'] = dstDir

        lineType = formula.getMapId(self.spaceNo)
        gameengine.getLineStub(lineType).autoSwitchLine(self, self.gbId, self.spaceNo, extra, cbName, cbArgs)

    def onCheckAutoSwitch(self, toLineNo, toSpaceBox, position, desTelId, fromTelId, teleporter, dstSpaceNo, dstPos,
                          dstDir, src):
        dstPos = position or dstPos
        if toLineNo >= 0 and toLineNo != formula.getLineNo(self.spaceNo):
            self._switchLineInternal(toLineNo, dstPos, dstDir, extra={'src': src})
        else:
            self.teleportToCellWithCast(
                teleporter, dstSpaceNo, dstPos, dstDir, src,
                'teleportCallBack',
                (desTelId, fromTelId, teleporter, dstSpaceNo, dstPos, dstDir, tuple(self.position))
            )

    @gamedecorator.crossServer
    @utils.isMyself
    def queryLineInfo(self, exposed, lineType):
        gameengine.getLineStub(lineType).doQueryLineInfo(self.spaceNo, self.base, self.gbId)

    def updateAreaIdInWorldLine(self):
        if formula.spaceInWorldLine(self.spaceNo):
            lineType = formula.getMapId(self.spaceNo)
            lastPos = self.getTempMiscProp(gameconst.AvatarProps.lastUpdateAreaPos)
            if lastPos and sMath.offset2DSum(lastPos, self.position) < 5:
                return
            lineNo = formula.getLineNo(self.spaceNo)
            upData = {'areaId': utils.getAreaId(formula.getMapId(self.spaceNo), self.position)}
            gameengine.getLineStub(formula.getMapId(self.spaceNo)).updateLinePlayerInfo(lineNo, self.base, self.gbId, upData)
            self.setTempMiscProp(gameconst.AvatarProps.lastUpdateAreaPos, tuple(self.position))
        else:
            self.popTempMiscProp(gameconst.AvatarProps.lastUpdateAreaPos)
