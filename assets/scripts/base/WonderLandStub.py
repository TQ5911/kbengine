# -*- coding: utf-8 -*-

from KBEDebug import *

import iGlobal
import iBaseNoCell
import iTimer
import iMultiStaticSpace
import iMultiStaticSpacePlayer
import linePlayers

import gameengine
import gametimer
import utils
import gameconst
import gameconfig
import wonderLand_floor as WL_FD
import wonderLand_config as WL_CD
import branchData_branchData as B_BD
import branchData_set as BDS
import iLinePlayersStub
import formula
import json

class WonderLandStub(iBaseNoCell.IBaseNoCell, iTimer.ITimer, \
                    iMultiStaticSpace.IMultiStaticSpace, \
                    iMultiStaticSpacePlayer.IMultiStaticSpacePlayer, \
                    iLinePlayersStub.IBranchLineStub):
    def __init__(self):
        iMultiStaticSpace.IMultiStaticSpace.__init__(self)
        iMultiStaticSpacePlayer.IMultiStaticSpacePlayer.__init__(self, gameconst.WONDERLAND_MAX_ENTER_NUM)
        iLinePlayersStub.IBranchLineStub.__init__(self)
        self.initDatetimeTimerTick()
        interval = 60 * BDS.datas["Branch_mergeInterval"]["value"]
        waitTime = 60 * BDS.datas["Branch_mergeWaitingTime"]["value"]

        self.pyAddTimer(interval, interval, gametimer.CHECK_LINE_MERGE)
        self.pyAddTimer(interval + waitTime, interval, gametimer.DO_LINE_MERGE)
        self.pyAddTimer(5, 5, gametimer.CLEAR_MULTI_ENTER_TIME_OUT)

    def doNext(self):
        LOG_DBG('WonderLandStub doNext')
        _mapId = WL_FD.datas[self.floor]['ID']
        if _mapId in B_BD.datas:
            maxLineNum = gameconst.getBranchLineCnt(_mapId)
            for _lineNo in range(maxLineNum):
                self._createStaticSpace(_mapId, lineNo=_lineNo)
        else:
            self._createStaticSpace(_mapId)
        return

    def _getSpaceMgrEntityType(self):
        return 'WonderLandSpaceMgr'

    def onTimer(self, tid, userArg):
        if utils.isBelongTimerTag(userArg):
            self._onTimerCallback(tid)
        elif userArg == gametimer.TIMER_DATETIME_ITIMER_CALLBACK:
            self._onDatetimeTimerTick()
        elif userArg == gametimer.CLEAR_MULTI_ENTER_TIME_OUT:
            self.onClearEnterTimeOut(gameconst.CUBE_ENTER_TIME_OUT_DUR)
        elif userArg == gametimer.CHECK_LINE_MERGE:
            mapId = WL_FD.datas[self.floor]['ID']
            if mapId in B_BD.datas:
                self._checkLineMerge(mapId)
        elif userArg == gametimer.DO_LINE_MERGE:
            mapId = WL_FD.datas[self.floor]['ID']
            if mapId in B_BD.datas:
                self._doLineMerge(mapId)
        else:
            self._onTimerTrigger(tid, userArg)

    def defaultSapceVal(self):
        spaceVals = list(self.staticSpaces.values())
        if not spaceVals:
            return None

        return spaceVals[0]

    def logonEnterWonderLand(self, box, gbId, spaceNo):
        _spaceVal = self.staticSpaces.get(spaceNo)
        if not _spaceVal:
            LOG_ERR('WonderLandStub::logonEnterWonderLand: spaceVal not found')
            return

        self.addEnterPlayer(box, gbId, 0, 0, linePlayers.LinePlayerVal.ENTERING, _spaceVal.getSpaceNo(), {})

        box.onLogonEnterWonderLandGetSpaceBox(_spaceVal.lineSpaceBox, _spaceVal.spaceMgrBoxCell.id)

    def doEnterWonderLand(self, box, gbId, extra):
        _mapId = WL_FD.datas[self.floor]['ID']
        _lineNo = 0
        if _mapId in B_BD.datas:
            _lineNo = self._autoSelectLine(box, gbId, iLinePlayersStub.EnterLineExtra.new(extra, -1), lineType=_mapId)
        if _lineNo == -1:
            LOG_ERR('WonderLandStub::doEnterWonderLand: lineNo is -1')
            return

        _spaceNo = formula.combineLineSpaceNo(_mapId, _lineNo)
        _spaceVal = self.staticSpaces.get(_spaceNo)
        if not _spaceVal:
            LOG_ERR('WonderLandStub::doEnterWonderLand: spaceVal not found')
            return

        if not self.canSpaceEnter(_spaceVal.getSpaceNo()):
            box.onMessagePre(WL_CD.datas['WonderLand_fullyBooked']['value'], [])
            return

        self.addEnterPlayer(box, gbId, 0, 0, linePlayers.LinePlayerVal.ENTERING, _spaceVal.getSpaceNo(), {})
        box.cell.beginEnterWonderLand(_spaceVal.lineSpaceBox, _spaceVal.spaceMgrBoxCell.id, _spaceVal.getSpaceNo(), extra)

    def onEnterWonderLandSuccess(self, gbId, spaceNo):
        _playerVal = self.allPlayers.get(gbId)
        if not _playerVal:
            LOG_ERR('WonderLandStub::onEnterWonderLandSuccess: playerVal not found', gbId)
            return

        if _playerVal.playerStatus == linePlayers.LinePlayerVal.ENTERING:
            _playerVal.playerStatus = linePlayers.LinePlayerVal.INLINE

            if _playerVal.curSpaceNo != spaceNo:
                LOG_ERR('WonderLandStub::onEnterWonderLandSuccess: spaceNo not match: {} {}'.format(_playerVal.curSpaceNo, spaceNo))
        else:
            self.switchStaticSpace(gbId, spaceNo)

    def onLeaveWonderLand(self, gbId):
        _playerVal = self.allPlayers.get(gbId)
        if not _playerVal:
            LOG_ERR('WonderLandStub::onLeaveWonderLand: playerVal not found', gbId)
            return

        self.removePlayer(gbId)
    
    def onLeaveWonderLandWithToSpaceNo(self, gbId, toSpaceNo):
        _playerVal = self.allPlayers.get(gbId)
        if not _playerVal:
            LOG_ERR('WonderLandStub::onLeaveWonderLandWithToSpaceNo: playerVal not found', gbId)
            return

        if toSpaceNo not in self.staticSpaces:
            self.removePlayer(gbId)

    def onLoadGroupEntities(self, info):
        LOG_DBG("WonderLandStub::onLoadGroupEntities", info)
        super(WonderLandStub, self).onLoadGroupEntities(info)

    def onRefreshGroupEntities(self, info):
        LOG_DBG("WonderLandStub::onRefreshGroupEntities", info)
        super(WonderLandStub, self).onRefreshGroupEntities(info)

    def onDestroyGroupEntities(self, info):
        LOG_DBG("WonderLandStub::onDestroyGroupEntities", info)
        super(WonderLandStub, self).onDestroyGroupEntities(info)

    def doGetWonderLandLineInfo(self, box):
        _mapId = WL_FD.datas[self.floor]['ID']
        if _mapId in B_BD.datas:
            res = self._calculateLineInfo(_mapId)

            LOG_DBG('doGetWonderLandLineInfo', res)
            box.client.onGetLineInfo(json.dumps(res))

    def doSwitchWonderLandLine(self, toLineNo, box, gbId, extra):
        _mapId = WL_FD.datas[self.floor]['ID']
        playerVal = self.allPlayers.get(gbId)
        toSpaceNo = formula.combineLineSpaceNo(_mapId, toLineNo)
        if playerVal and playerVal.curSpaceNo == toSpaceNo:
            LOG_ERR('WonderLandStub::doSwitchWonderLandLine: player already in space: {} {}'.format(gbId, toSpaceNo))
            return

        _spaceVal = self.staticSpaces[toSpaceNo]
        if not self.canSpaceEnter(_spaceVal.getSpaceNo()):
            box.onMessagePre(BDS.datas["Branch_fullCapacityMsg"]["value"], [])
            return

        if self._checkSelectLineActivity(toLineNo, box, gbId, extra, _mapId) != gameconst.EnterLineCodeEnum.ENTER_CHECK_SUCCESS:
            box.onMessagePre(BDS.datas["Branch_fullCapacityMsg"]["value"], [])
            return

        if playerVal:
            self.addPendingEnterPlayer(toSpaceNo, gbId)
        else:
            self.addEnterPlayer(box, gbId, 0, 0, linePlayers.LinePlayerVal.ENTERING, toSpaceNo, {})
            
        box.cell.doSwitchWonderLandLine(_spaceVal.lineSpaceBox, _spaceVal.spaceMgrBoxCell.id, _spaceVal.getSpaceNo(), extra)
