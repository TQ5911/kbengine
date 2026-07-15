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
import abyss_floor as AB_FD
import abyss_config as AB_CD
import branchData_branchData as B_BD
import branchData_set as BDS
import iLinePlayersStub
import formula
import json

class AbyssStub(iBaseNoCell.IBaseNoCell, iTimer.ITimer, \
                    iMultiStaticSpace.IMultiStaticSpace, \
                    iMultiStaticSpacePlayer.IMultiStaticSpacePlayer, \
                    iLinePlayersStub.IBranchLineStub):
    def __init__(self):
        iMultiStaticSpace.IMultiStaticSpace.__init__(self)
        iMultiStaticSpacePlayer.IMultiStaticSpacePlayer.__init__(self, gameconst.ABYSS_MAX_ENTER_NUM)
        iLinePlayersStub.IBranchLineStub.__init__(self)
        self.initDatetimeTimerTick()
        interval = 60 * BDS.datas["Branch_mergeInterval"]["value"]
        waitTime = 60 * BDS.datas["Branch_mergeWaitingTime"]["value"]

        self.pyAddTimer(interval, interval, gametimer.CHECK_LINE_MERGE)
        self.pyAddTimer(interval + waitTime, interval, gametimer.DO_LINE_MERGE)
        self.pyAddTimer(5, 5, gametimer.CLEAR_MULTI_ENTER_TIME_OUT)

    def doNext(self):
        LOG_DBG('AbyssStub doNext')
        _mapId = AB_FD.datas[self.floor]['ID']
        if _mapId in B_BD.datas:
            maxLineNum = gameconst.getBranchLineCnt(_mapId)
            for _lineNo in range(maxLineNum):
                self._createStaticSpace(_mapId, lineNo=_lineNo)
        else:
            self._createStaticSpace(_mapId)
        return

    def _getSpaceMgrEntityType(self):
        return 'AbyssSpaceMgr'

    def onTimer(self, tid, userArg):
        if utils.isBelongTimerTag(userArg):
            self._onTimerCallback(tid)
        elif userArg == gametimer.TIMER_DATETIME_ITIMER_CALLBACK:
            self._onDatetimeTimerTick()
        elif userArg == gametimer.CLEAR_MULTI_ENTER_TIME_OUT:
            self.onClearEnterTimeOut(gameconst.CUBE_ENTER_TIME_OUT_DUR)
        elif userArg == gametimer.CHECK_LINE_MERGE:
            mapId = AB_FD.datas[self.floor]['ID']
            if mapId in B_BD.datas:
                self._checkLineMerge(mapId)
        elif userArg == gametimer.DO_LINE_MERGE:
            mapId = AB_FD.datas[self.floor]['ID']
            if mapId in B_BD.datas:
                self._doLineMerge(mapId)
        else:
            self._onTimerTrigger(tid, userArg)

    def defaultSapceVal(self):
        spaceVals = list(self.staticSpaces.values())
        if not spaceVals:
            return None

        return spaceVals[0]

    def logonEnterAbyss(self, box, gbId, _):
        _mapId = AB_FD.datas[self.floor]['ID']
        _lineNo = 0
        if _mapId in B_BD.datas:
            _lineNo = self._autoSelectLine(box, gbId, iLinePlayersStub.EnterLineExtra.new({}, -1), lineType=_mapId)
        _spaceNo = formula.combineLineSpaceNo(_mapId, _lineNo)
        _spaceVal = self.staticSpaces.get(_spaceNo)
        if not _spaceVal:
            LOG_ERR('AbyssStub::logonEnterAbyss: spaceVal not found')
            return

        self.addEnterPlayer(box, gbId, 0, 0, linePlayers.LinePlayerVal.ENTERING, _spaceVal.getSpaceNo(), {})

        box.onLogonEnterAbyssGetSpaceBox(_spaceVal.lineSpaceBox, _spaceVal.spaceMgrBoxCell.id, _spaceNo)

    def doEnterAbyss(self, box, gbId, extra):
        _mapId = AB_FD.datas[self.floor]['ID']
        _lineNo = 0
        if _mapId in B_BD.datas:
            _lineNo = self._autoSelectLine(box, gbId, iLinePlayersStub.EnterLineExtra.new(extra, -1), lineType=_mapId)
        _spaceNo = formula.combineLineSpaceNo(_mapId, _lineNo)
        _spaceVal = self.staticSpaces.get(_spaceNo)
        if not _spaceVal:
            LOG_ERR('AbyssStub::doEnterAbyss: spaceVal not found')
            return

        if not self.canSpaceEnter(_spaceVal.getSpaceNo()):
            box.onMessagePre(AB_CD.datas['abyss_fullyBooked']['value'], [])
            return

        self.addEnterPlayer(box, gbId, 0, 0, linePlayers.LinePlayerVal.ENTERING, _spaceVal.getSpaceNo(), {})
        box.cell.beginEnterAbyss(_spaceVal.lineSpaceBox, _spaceVal.spaceMgrBoxCell.id, _spaceVal.getSpaceNo(), extra)

    def onEnterAbyssSuccess(self, gbId, spaceNo):
        _playerVal = self.allPlayers.get(gbId)
        if not _playerVal:
            LOG_ERR('AbyssStub::onEnterAbyssSuccess: playerVal not found', gbId)
            return

        if _playerVal.playerStatus == linePlayers.LinePlayerVal.ENTERING:
            _playerVal.playerStatus = linePlayers.LinePlayerVal.INLINE

            if _playerVal.curSpaceNo != spaceNo:
                LOG_ERR('AbyssStub::onEnterAbyssSuccess: spaceNo not match: {} {}'.format(_playerVal.curSpaceNo, spaceNo))
        else:
            self.switchStaticSpace(gbId, spaceNo)

    def onLeaveAbyss(self, gbId):
        _playerVal = self.allPlayers.get(gbId)
        if not _playerVal:
            LOG_ERR('AbyssStub::onLeaveAbyss: playerVal not found', gbId)
            return

        self.removePlayer(gbId)
    
    def onLeaveAbyssWithToSpaceNo(self, gbId, toSpaceNo):
        _playerVal = self.allPlayers.get(gbId)
        if not _playerVal:
            LOG_ERR('AbyssStub::onLeaveAbyssWithToSpaceNo: playerVal not found', gbId)
            return

        if toSpaceNo not in self.staticSpaces:
            self.removePlayer(gbId)

    def onLoadGroupEntities(self, info):
        LOG_DBG("AbyssStub::onLoadGroupEntities", info)
        super(AbyssStub, self).onLoadGroupEntities(info)

    def onRefreshGroupEntities(self, info):
        LOG_DBG("AbyssStub::onRefreshGroupEntities", info)
        super(AbyssStub, self).onRefreshGroupEntities(info)

    def onDestroyGroupEntities(self, info):
        LOG_DBG("AbyssStub::onDestroyGroupEntities", info)
        super(AbyssStub, self).onDestroyGroupEntities(info)

    def doGetAbyssLineInfo(self, box):
        _mapId = AB_FD.datas[self.floor]['ID']
        if _mapId in B_BD.datas:
            res = self._calculateLineInfo(_mapId)

            LOG_DBG('doGetAbyssLineInfo', res)
            box.client.onGetLineInfo(json.dumps(res))

    def doSwitchAbyssLine(self, toLineNo, box, gbId, extra):
        _mapId = AB_FD.datas[self.floor]['ID']
        playerVal = self.allPlayers.get(gbId)
        toSpaceNo = formula.combineLineSpaceNo(_mapId, toLineNo)
        if playerVal and playerVal.curSpaceNo == toSpaceNo:
            LOG_ERR('AbyssStub::doSwitchAbyssLine: player already in space: {} {}'.format(gbId, toSpaceNo))
            return

        _spaceVal = self.staticSpaces[toSpaceNo]
        if not self.canSpaceEnter(_spaceVal.getSpaceNo()):
            box.onMessagePre(BDS.datas["Branch_fullCapacityMsg"]["value"], [])
            return

        if playerVal:
            self.addPendingEnterPlayer(toSpaceNo, gbId)
        else:
            self.addEnterPlayer(box, gbId, 0, 0, linePlayers.LinePlayerVal.ENTERING, toSpaceNo, {})
            
        box.cell.doSwitchAbyssLine(_spaceVal.lineSpaceBox, _spaceVal.spaceMgrBoxCell.id, _spaceVal.getSpaceNo(), extra)

    def checkCanEnterCrossAbyss(self, box):
        for spaceNo, spaceVal in self.staticSpaces.items():
            if self.canSpaceEnter(spaceNo):
                box.onCrossServerCheckCanEnterAbyss(self.floor, True, 0)
                return

        box.onCrossServerCheckCanEnterAbyss(self.floor, False, 0)