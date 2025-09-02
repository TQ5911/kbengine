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



class WonderLandStub(iBaseNoCell.IBaseNoCell, iTimer.ITimer, \
                    iMultiStaticSpace.IMultiStaticSpace, \
                    iMultiStaticSpacePlayer.IMultiStaticSpacePlayer):
    def __init__(self):
        iMultiStaticSpace.IMultiStaticSpace.__init__(self)
        iMultiStaticSpacePlayer.IMultiStaticSpacePlayer.__init__(self, gameconst.WONDERLAND_MAX_ENTER_NUM)
        self.addDatetimeTimerTick()
        self.pyAddTimer(5, 5, gametimer.CLEAR_MULTI_ENTER_TIME_OUT)

    def doNext(self):
        DEBUG_MSG('WonderLandStub doNext')
        _mapId = WL_FD.datas[self.floor]['ID']
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
        else:
            self._onTimer(tid, userArg)

    def defaultSapceVal(self):
        spaceVals = list(self.staticSpaces.values())
        if not spaceVals:
            return None

        return spaceVals[0]

    def logonEnterWonderLand(self, box, gbId):
        _spaceVal = self.defaultSapceVal()
        self.addEnterPlayer(box, gbId, 0, 0, linePlayers.LinePlayerVal.ENTERING, _spaceVal.getSpaceNo(), {})

        box.onLogonEnterWonderLandGetSpaceBox(_spaceVal.lineSpaceBox, _spaceVal.spaceMgrBoxCell.id)

    def doEnterWonderLand(self, box, gbId):
        _spaceVal = self.defaultSapceVal()
        if not _spaceVal:
            ERROR_MSG('WonderLandStub::doEnterWonderLand: spaceVal not found')
            return

        if not self.canSpaceEnter(_spaceVal.getSpaceNo()):
            ERROR_MSG('WonderLandStub::doEnterWonderLand: can not enter: {}'.format(_spaceVal.getSpaceNo()))
            return

        self.addEnterPlayer(box, gbId, 0, 0, linePlayers.LinePlayerVal.ENTERING, _spaceVal.getSpaceNo(), {})
        box.cell.beginEnterWonderLand(_spaceVal.lineSpaceBox, _spaceVal.spaceMgrBoxCell.id, _spaceVal.getSpaceNo(), {})

    def onEnterWonderLandSuccess(self, gbId, spaceNo):
        _playerVal = self.allPlayers.get(gbId)
        if not _playerVal:
            ERROR_MSG('WonderLandStub::onEnterWonderLandSuccess: playerVal not found', gbId)
            return

        if _playerVal.playerStatus == linePlayers.LinePlayerVal.ENTERING:
            _playerVal.playerStatus = linePlayers.LinePlayerVal.IN_LINE

    def onLeaveWonderLand(self, gbId):
        _playerVal = self.allPlayers.get(gbId)
        if not _playerVal:
            ERROR_MSG('WonderLandStub::onLeaveWonderLand: playerVal not found', gbId)
            return

        self.removePlayer(gbId)

    def onLoadGroupEntities(self, info):
        DEBUG_MSG("WonderLandStub::onLoadGroupEntities", info)
        super(WonderLandStub, self).onLoadGroupEntities(info)

    def onRefreshGroupEntities(self, info):
        DEBUG_MSG("WonderLandStub::onRefreshGroupEntities", info)
        super(WonderLandStub, self).onRefreshGroupEntities(info)
