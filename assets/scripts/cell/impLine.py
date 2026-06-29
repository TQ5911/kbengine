# -*- coding: utf-8 -*-
from KBEDebug import *

import KBEngine

from common.KBEDebug import LOG_INFO
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
import conflict_conflict_def as C_C_DD
import const_const as CONST
import gamePlay_gamePlay as GGD
import branchData_set as BDS
import gametimer

import branchData_switchLines as BDSL
import branchData_branchData as BD_BDD

class ImpLine(object):
    def _buildEnterLineExtra(self, position, dataDic=None):
        _pos = position or self.position
        extra = dataDic or {}

        extra['position'] = _pos
        #teamId和raidId最多只会有一个存在
        if self.teamId:
            extra['teamUUID'] = self.teamId
        if self.raidId:
            extra['teamUUID'] = self.raidId

        return extra

    @utils.isMyself
    def applyEnterLine(self, exposed, lineType):
        if lineType == formula.fetchMapId(self.spaceNo):
            return

        lineNo = formula.parseLineNo(self.spaceNo)
        enterPos = formula.getSpaceBornPoint(lineType)
        if not self.onCheckMapUnlocked(lineType):
            return

        self.applyEnterLineInternal(lineType, lineNo, enterPos, self.direction, {"telToMainCityWhenFull": False})

    def enterLineByNpc(self, lineType, *args, **kwargs):
        lineNo = formula.parseLineNo(self.spaceNo)
        lineType = int(lineType)
        mapId = lineType

        if not formula.inLineScene(self.spaceNo):
            return

        enterPos, direction = formula.getSpaceBornPosAndDir(lineType)
        if not self.onCheckMapUnlocked(mapId):
            return

        if formula.checkDuelMapId(lineType):
            _options = complexTeleportOption.ComplexTeleportOpt(teleportType=gameconst.ComplexTeleportEnum.ENTER)
            self.tryRegiTeleportOutsideRecord(self.spaceNo, _options)

        self.applyEnterLineInternal(lineType, lineNo, enterPos, direction, {"telToMainCityWhenFull": False})

    def applyEnterLineInternal(self, lineType, lineNo, position, direction, extra=None):
        LOG_INFO('zt: applyEnterLineInternal', lineType, lineNo, position, direction, extra)
        if formula.inDungeonScene(self.spaceNo):
            # 从副本进入大世界一定要走icomplexTeleport过来
            if not (isinstance(extra, dict) and extra.get('toLine')):
                LOG_WARN('dungeon enter line without toLine')
                return

        position = position or self.position
        direction = direction or self.direction
        extra = self._buildEnterLineExtra(position, extra)

        gameengine.getLineStub(lineType).enterLine(lineNo, self.base, self.gbId, position, direction, extra)

    # 已经在LineStub占了人数坑位，如果进入失败需要释放坑位
    def beginEnterLine(self, lineType, lineNo, spaceBox, position, direction, extraData):
        LOG_INFO('zt: beginEnterLine', lineType, lineNo, spaceBox.id)
        _cmpLineType = gameconst.TeleportLockEnum.ENTER_LINE

        if extraData.get('isLogin'):
            self._onEnterLine(0, lineType, lineNo, extraData)
        else:
            if self.teleportLock and self.teleportLock != _cmpLineType:
                _failReason = 'locked:%s'%self.teleportLock
                gameengine.getLineStub(lineType).enterLineFailed(
                    lineNo, self.base, self.gbId, {'reason':_failReason})
                return

            self.aquireTeleportLock(_cmpLineType)

            spaceNo = formula.combineLineSpaceNo(lineType, lineNo)

            if formula.inWorldLineScene(self.spaceNo):
                extraData['fromSpaceMgrBox'] = self.spaceMgr

            self.teleportToCell(spaceBox.cell, spaceNo, position, direction, '_onEnterLine',
                                (self.spaceNo, lineType, lineNo, extraData))

    def _onEnterLine(self, fromSpaceNo, lineType, lineNo, extra):
        LOG_INFO('_onEnterLine', fromSpaceNo, lineType, lineNo, extra)

        succInfo = {}
        succInfo['teamUUID'] = self.teamId if self.teamId else self.raidId

        if extra.get('callback'):
            _func = getattr(self, extra['callback'])
            _func and _func(*extra.get('callbackArgs', ()))

        self.spaceMgrId = self.getCurrentSpace().spaceMgrId
        self.spaceMgr.onPlayerEnter(self.id)

        fromSpaceMgrBox = extra.get('fromSpaceMgrBox')
        self.afterEnterWorldLine(fromSpaceNo, fromSpaceMgrBox)

        if self.teleportLock:
            self.releaseTeleportLock(gameconst.TeleportLockEnum.ENTER_LINE)

        gameengine.getLineStub(lineType).enterLineSuccess(lineNo, self.base, self.gbId, succInfo)

        if formula.inLineScene(fromSpaceNo):
            self._clearLineState(fromSpaceNo)

        if formula.inDuelScene(self.spaceNo):
            ret = self.setPKModel(gameconst.PKModelEnum.PEACE)
            if ret:
                self.changePKModeResetTargetId()

    def afterEnterWorldLine(self, fromSpaceNo, fromSpaceMgrBox):
        if fromSpaceMgrBox:
            fromSpaceMgrBox.onPlayerLeave(self.gbId, self.id, self.base)

        if formula.inMineWarScene(fromSpaceNo):
            self.mineWarCamp = 0
            self.onLeaveMineWarSpace()

    def _checkSwitchLine(self, toLineNo):
        if not formula.inLineScene(self.spaceNo):
            return False

        if toLineNo < 0:
            return False
        if self.hasState(gameconst.StateEnum.Teleporting):
            return False

        lineType = formula.fetchMapId(self.spaceNo)
        if toLineNo >= utils.fetchLineMaxNumber(lineType):
            return False

        if toLineNo == formula.parseLineNo(self.spaceNo):
            return False

        return True

    @utils.isMyself
    @gamedecorator.crossServer
    def applySwitchLine(self, exposed, toLineNo):
        _src = dungeonSrc.DungeonFromClientSrc(self.base, self.gbId)

        if formula.inCubeScene(self.spaceNo):
            self.switchCubeLine(exposed, toLineNo)
            return
        
        if formula.inWonderLandScene(self.spaceNo):
            gameengine.getWonderLandStub(formula.fetchMapId(self.spaceNo)).doSwitchWonderLandLine(toLineNo, self.base, self.gbId, {})
            return

        self.switchLineAndPosition(toLineNo, None, src=_src, needPending=False)

    def switchLineAndPosition(self, toLineNo, toPosition, src=None, extra=None, needPending=True):
        canSwitch = self._checkSwitchLine(toLineNo)
        LOG_INFO('applySwitchLine', self.spaceNo, toLineNo, canSwitch, src, extra)
        if not canSwitch:
            return

        self.checkEnterLine(
            formula.fetchMapId(self.spaceNo), 
            toLineNo, 
            toPosition, 
            needPending,
            'onCheckSwitchLine', 
            (self.spaceNo, toLineNo, toPosition, src, extra))

    def onCheckSwitchLine(self, checkCode, checksumSpaceNo, toLineNo, toPosition, src, extraData):
        LOG_INFO("onCheckSwitchLine::", checkCode, checksumSpaceNo, toLineNo, toPosition, src, extraData)
        if checkCode == gameconst.EnterLineCodeEnum.ENTER_CHECK_SUCCESS:
            _result = self._onCheckSwitchLineReCheckCond(checkCode, checksumSpaceNo, toLineNo)
            extraData = extraData if extraData is not None else {}
            if not _result:
                failFunc = extraData.get("failCallback", '')
                failArgs = extraData.get("callbackArgs", ())
                gameengine.getLineStub(formula.fetchMapId(checksumSpaceNo)).checkCanEnterLineFinallyFailed(
                    toLineNo, self.base, self.gbId, extraData, failFunc, (checkCode, *failArgs))
                return
            extraData.update({'src': src})
            self._switchLineInternal(toLineNo, toPosition, extra=extraData)

        else:
            if checkCode == gameconst.EnterLineCodeEnum.ERR_MERGE_LINE:
                self.showMsg(BDS.datas["Branch_mergeChangeMsg"]["value"], [])
            else:
                self.showMsg(BDS.datas["Branch_fullCapacityMsg"]["value"], [])
            extraData = extraData if extraData is not None else {}
            failFunc = extraData.get("failCallback", '')
            failArgs = extraData.get("callbackArgs", ())
            _fn = getattr(self, failFunc, None)
            _fn and _fn(checkCode, *failArgs)

    def _onCheckSwitchLineReCheckCond(self, checkCode, checksumSpaceNo, toLineNo):
        if checkCode != gameconst.EnterLineCodeEnum.ENTER_CHECK_SUCCESS:
            LOG_WARN("_onCheckSwitchLineReCheckCond:: cant enter", checkCode, checksumSpaceNo, toLineNo)
            return False

        if not self._checkSwitchLine(toLineNo):
            LOG_WARN("_onCheckSwitchLineReCheckCond:: checkswitchline failed", checkCode, checksumSpaceNo, toLineNo)
            return False

        if not formula.inLineScene(checksumSpaceNo):
            LOG_WARN("_onCheckSwitchLineReCheckCond:: checksumSpaceNo failed", checkCode, checksumSpaceNo, toLineNo)
            return False

        lineType = formula.fetchMapId(self.spaceNo)
        checklineType = formula.fetchMapId(checksumSpaceNo)
        if lineType != checklineType:
            LOG_WARN("_onCheckSwitchLineReCheckCond:: checklinetype failed", checkCode, checksumSpaceNo,
                        self.spaceNo, toLineNo)
            return False

        return True

    def _switchLineInternal(self, toLineNo, toPosition=None, toDir=None, extra=None):
        LOG_INFO('_switchLineInternal', self.spaceNo, toLineNo)
        if not extra:
            extra = {}

        _cbfn = "_switchLineInternalAfterCast"
        _cbargs = (toLineNo, toPosition, toDir, extra)

        if extra.get('hasCast'):
            getattr(self, _cbfn)(*_cbargs)
        else:
            self._commonNeedCast(C_C_DD.datas.teleportCast, gameconst.StateEnum.Teleporting, gameconst.CastEnum.teleport,
                                _cbfn, _cbargs)

    def onMergeLine(self, toLineNo):
        LOG_DBG("onMergeLine", self.spaceNo, toLineNo)
        self.client.beginMergeLine()
        #合线要跳过读条
        if formula.inCubeScene(self.spaceNo):
            self._switchCubeLine(toLineNo)
            return
        
        if formula.inWonderLandScene(self.spaceNo):
            gameengine.getWonderLandStub(formula.fetchMapId(self.spaceNo)).doSwitchWonderLandLine(toLineNo, self.base, self.gbId, {'isMerge': True})
            return

        self._switchLineInternalAfterCast(toLineNo, None, None, {})

    def _switchLineInternalAfterCast(self, toLineNo, toPosition, toDir, extra):
        lineType = formula.fetchMapId(self.spaceNo)
        lineNo = formula.parseLineNo(self.spaceNo)

        extra = self._buildEnterLineExtra(toPosition, extra)

        if toDir:
            extra['dir'] = toDir

        # 这时候可能被传到副本里，会报错
        if formula.inLineScene(self.spaceNo):
            gameengine.getLineStub(lineType).doSwitchLine(lineNo, toLineNo, self.base, self.gbId, extra)

    # 已经在目标分线占了人数坑位，如果进入失败需要释放坑位
    def beginSwitchLine(self, lineType, fromLineNo, toLineNo, toSpaceBox, extra):
        LOG_INFO('beginSwitchLine', lineType, self.spaceNo, fromLineNo, toLineNo, toSpaceBox.id)

        if self.teleportLock and self.teleportLock!=gameconst.TeleportLockEnum.SWITCH_LINE:
            _failReason = 'locked:{}'.format(self.teleportLock)
            gameengine.getLineStub(lineType).switchLineFailed(
                fromLineNo, 
                toLineNo, 
                self.base, 
                self.gbId, 
                {'reason':_failReason,})
            return

        self.aquireTeleportLock(gameconst.TeleportLockEnum.SWITCH_LINE)

        spaceNo = formula.combineLineSpaceNo(lineType, toLineNo)
        enterPos = extra.pop('position', self.position)
        enterDir = extra.pop('dir', self.direction)
        if toLineNo == 0 and lineType in BDSL.datas:
            enterPos = BDSL.datas[lineType]['position']
        extra['fromSpaceMgrBox'] = self.spaceMgr

        self.teleportToCell(
            toSpaceBox.cell, 
            spaceNo, enterPos, 
            enterDir, 
            '_onSwitchLine',
            (lineType, self.spaceNo, toLineNo, extra)
        )

    def _onSwitchLine(self, lineType, fromSpaceNo, toLineNo, extra):
        LOG_INFO('_onSwitchLine', lineType, fromSpaceNo, toLineNo, extra)
        fromLineNo = formula.parseLineNo(fromSpaceNo)
        gameengine.getLineStub(lineType).switchLineSuccess(fromLineNo, toLineNo, self.base, self.gbId, extra)

        if self.teleportLock:
            self.releaseTeleportLock(gameconst.TeleportLockEnum.SWITCH_LINE)

        if extra and extra.get('callback'):
            _func = getattr(self, extra['callback'])
            _func and _func(*extra.get('callbackArgs', ()))

        self.spaceMgrId = self.getCurrentSpace().spaceMgrId
        self.spaceMgr.onPlayerEnter(self.id)

        fromSpaceMgrBox = extra.get('fromSpaceMgrBox')
        self.afterEnterWorldLine(fromSpaceNo, fromSpaceMgrBox)

    @utils.isMyself
    def applyLeaveLine(self, exposed):
        LOG_INFO('applyLeaveLine', self.spaceNo)
        if formula.inDuelScene(self.spaceNo):
            mapId, outRecord = self.tryGetLastTeleportOutesideRecord(self.spaceNo)
            if outRecord:
                self.applyEnterLineInternal(
                    mapId,
                    formula.parseLineNo(outRecord.spaceNo),
                    outRecord.position,
                    outRecord.direction,
                    {"telToMainCityWhenFull": True})

    # 有的时候已经离开分线了，调用这个接口清除分线状态，需要传fromSpaceNo，因为self.spaceNo已经是离开后场景了
    # toSpaceNo==0时是传到了其他场景后清除源分线的状态
    def _applyLeaveLineInternal(self, fromSpaceNo, toSpaceNo, toPosition, toDirection):
        LOG_INFO('_applyLeaveLineInternal', self.spaceNo, fromSpaceNo, toSpaceNo)
        if toSpaceNo and not formula.inLineScene(self.spaceNo):
            return

        if formula.inWorldLineScene(self.spaceNo) and toSpaceNo:
            updateTimer = self.popTempMiscProp(gameconst.EntityPropsEnum.updateWorldLineAreaTimer, 0)
            if updateTimer:
                self.pyDelTimer(updateTimer, gametimer.AVATAR_UPDATE_AREAID)

        lineType = formula.fetchMapId(fromSpaceNo)
        gameengine.getLineStub(lineType).leaveLine(self.base, self.gbId, fromSpaceNo, toSpaceNo, toPosition, toDirection)

    def _clearLineState(self, clearSpaceNo):
        lineType = formula.fetchMapId(clearSpaceNo)
        gameengine.getLineStub(lineType).leaveLine(self.base, self.gbId, clearSpaceNo, 0,
                                                                gameconst.POSITION_ZERO, gameconst.DIRECTION_ZERO)

    def beginLeaveLine(self, fromSpaceNo, toSpaceNo, toPosition, toDirection):
        LOG_INFO('beginLeaveLine', self.spaceNo, fromSpaceNo, toSpaceNo, toPosition, toDirection)

        # 可以不指定toSpaceNo，比如从分线内进入分线，已经离开老分线后才调用_applyLeaveLineInternal，这里只
        # 执行上老分线的离开函数
        if not toSpaceNo:
            pass
        elif formula.inLineScene(toSpaceNo):
            toLineType = formula.fetchMapId(toSpaceNo)
            toLineNo = formula.parseLineNo(toSpaceNo)
            extra = {'callback': '_onLeaveLine', 'callbackArgs': (fromSpaceNo, toSpaceNo), 'telToMainCityWhenFull': True}
            self.applyEnterLineInternal(toLineType, toLineNo, toPosition, toDirection, extra)
        else:
            LOG_ERR('teleport to %s is not supported' % toSpaceNo)

    def _onLeaveLine(self, fromSpaceNo, toSpaceNo):
        LOG_INFO('_onLeaveLine', self.spaceNo, fromSpaceNo, toSpaceNo)

    def beginGoBackLine(self, lineSpaceNo, spaceBox, dstPos, dstDir, callback, callbackArgs):
        LOG_INFO('beginGoBackLine', lineSpaceNo, callback, callbackArgs)
        _fromSpaceNo = self.spaceNo
        self.teleportToCell(spaceBox.cell, lineSpaceNo, dstPos, dstDir, '_onGoBackLine',
                            (_fromSpaceNo, callback, callbackArgs))

    def _onGoBackLine(self, fromSpaceNo, callback, callbackArgs):
        LOG_INFO('_onGoBackLine', fromSpaceNo, callback, callbackArgs)

        _func = getattr(self, callback)
        _func and _func(*callbackArgs)

    def checkEnterLine(self, lineType, lineNo, dstPos, needPending, cbName, cbArgs):
        _extra = self._buildEnterLineExtra(dstPos)
        _extra["needPending"] = needPending

        gameengine.getLineStub(lineType).checkCanEnterLine(
            lineNo, 
            self.base, 
            self.gbId, 
            _extra, 
            cbName, 
            cbArgs)

    def checkAutoSwitchLine(self, dstPos, dstDir, cbName, cbArgs):
        _extra = self._buildEnterLineExtra(dstPos)
        _extra['dir'] = dstDir

        lineType = formula.fetchMapId(self.spaceNo)
        gameengine.getLineStub(lineType).autoSwitchLine(self, self.gbId, self.spaceNo, _extra, cbName, cbArgs)

    def onCheckAutoSwitch(self, toLineNo, toSpaceBox, position, desTelId, _, teleporter, dstSpaceNo, dstPos,
                          dstDir, src):
        dstPos = position or dstPos
        if toLineNo >= 0 and toLineNo != formula.parseLineNo(self.spaceNo):
            self._switchLineInternal(toLineNo, dstPos, dstDir, extra={'src': src})
        else:
            self.showMsg(BDS.datas["Branch_fullCapacityMsg"]["value"], [])

    @gamedecorator.crossServer
    @utils.isMyself
    @gamedecorator.limitcall(0.1)
    def queryLineInfo(self, exposed, lineType):
        if formula.inCubeScene(self.spaceNo):
            LOG_INFO("queryLineInfo cube room", lineType)
            gameengine.getCubeStubBySpaceNo(self.spaceNo).doGetCubeReadyLineCnt(self.base, lineType)
            return

        if formula.inWonderLandScene(self.spaceNo):
            LOG_INFO("queryLineInfo wonder land", lineType)
            gameengine.getWonderLandStub(lineType).doGetWonderLandLineInfo(self.base)
            return

        if formula.inAbyssScene(self.spaceNo):
            LOG_INFO("queryLineInfo abyss", lineType)
            gameengine.getAbyssStub(lineType).doGetAbyssLineInfo(self.base)
            return

        if lineType not in gameconst.lineStubMap():
            LOG_ERR('queryLineInfo invalid lineType:', lineType)
            return

        gameengine.getLineStub(lineType).doQueryLineInfo(self.spaceNo, self.base, self.gbId)

    def onCheckMapUnlocked(self, mapId):
        mapData = GGD.datas.get(mapId)
        if not mapData:
            LOG_ERR('onCheckMapUnlocked but mapData invalid:', mapId)
            return False

        checkResult = True
        openTask = mapData['openTask']
        if openTask:
            checkResult = self._isUIVisibleStrCell(openTask)
            if not checkResult:
                self.client.onMapUnlockMessagePre(mapId)
        else:
            LOG_DBG("onCheckMapUnlocked map always locked")

        return checkResult
