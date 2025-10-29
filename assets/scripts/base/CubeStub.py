# coding: utf-8

import KBEngine
from KBEDebug import *

import random

import utils
import iBaseNoCell
import iTimer
import formula
import gametimer
import linePlayers
import gameconst
import dataUtils
import CubeRoom
import iMultiStaticSpace
import iMultiStaticSpacePlayer

import gamePlay_gamePlay as GP_GPD
import cube_floor
import cube_room
import cube_config


class RandomRoomVal(object):
    def __init__(self, mapId):
        self.mapId = mapId


class CubeStub(iBaseNoCell.IBaseNoCell, iTimer.ITimer,
               iMultiStaticSpace.IMultiStaticSpace,
               iMultiStaticSpacePlayer.IMultiStaticSpacePlayer):

    def __init__(self):
        iMultiStaticSpace.IMultiStaticSpace.__init__(self)
        iMultiStaticSpacePlayer.IMultiStaticSpacePlayer.__init__(self, gameconst.CUBE_MAX_ENTER_NUM)
        self.addDatetimeTimerTick()
        self.cubeNo = self.cubeNo # type: int
        self.cubeRooms = {}
        self.randomRooms = []
        self.randomWeights = []
        self.pyAddTimer(5, 5, gametimer.CLEAR_MULTI_ENTER_TIME_OUT)

        self._startRefreshCowRefreshTimer()

    def _startRefreshCowRefreshTimer(self):
        _delay = random.randint(*cube_config.datas['cube_cowRoomEntranceIntervalTime']['value'])
        _delay += cube_config.datas['cube_cowRoomEntranceTime']['value']
        _delay *= 60
        self._callback(_delay, '_doRandomTeleporter', (), gametimer.TIMER_TAG_CUBE_TELEPORTER_REFRESH)

    def _doRandomTeleporter(self):
        _num = random.randint(*cube_config.datas['cube_cowRoomEntranceNum']['value'])
        _mapIds = random.sample(cube_room.floor2Rooms[self.cubeNo], _num)
        DEBUG_MSG('_doRandomTeleporter:', _mapIds)
        for _mapId in _mapIds:
            _spaceNo = formula.getLineSpaceNo(_mapId, 0)
            _spaceVal = self.staticSpaces[_spaceNo]
            _spaceVal.spaceMgrBoxCell.createTeleporterToCow()

        self._startRefreshCowRefreshTimer()

    def _removeRandomInfos(self, mapId):
        for _idx, _room in enumerate(self.randomRooms):
            if _room.mapId == mapId:
                self.randomRooms.pop(_idx)
                self.randomWeights.pop(_idx)
                break

    def _addRandomInfos(self, mapId):
        # if mapId == self.readyRoomMapId():
        #     return
        for _room in self.randomRooms:
            if _room.mapId == mapId:
                return

        _weight = cube_room.datas[mapId]['weight']
        self.randomRooms.append(RandomRoomVal(mapId))
        self.randomWeights.append(_weight)

    def readyRoomMapId(self):
        return cube_floor.datas[self.cubeNo]['ID']

    def doNext(self):
        super().doNext()
        self._initAllRoom()
        self._initWeights()

    def _initWeights(self):
        for _mapId in cube_room.floorTypeMapDic[self.cubeNo][gameconst.CubeRoomType.NORMAL]:
            self._addRandomInfos(_mapId)

    def onTimer(self, tid, userArg):
        if utils.isBelongTimerTag(userArg):
            self._onTimerCallback(tid)
        elif userArg == gametimer.TIMER_DATETIME_ITIMER_CALLBACK:
            self._onDatetimeTimerTick()
        elif userArg == gametimer.CLEAR_MULTI_ENTER_TIME_OUT:
            self.onClearEnterTimeOut(gameconst.CUBE_ENTER_TIME_OUT_DUR)
        else:
            self._onTimer(tid, userArg)

    def _initAllRoom(self):
        # 先创建大厅，只有大厅是多分线的
        for _floors in cube_room.floorTypeMapDic[self.cubeNo].values():
            for _mapId in _floors:
                if _mapId not in GP_GPD.datas:
                    ERROR_MSG('CubeStub::_initAllRoom: mapId not found: {}'.format(_mapId))
                    continue

                self._createStaticSpace(_mapId)

    def _getSpaceMgrEntityType(self):
        return 'CubeSpaceMgr'

    def _getRandomSpaceNo(self, curSpaceNo):
        # TODO: cube
        _mapId = formula.getMapId(curSpaceNo)
        _curIdx = -1
        _curWeight = 0
        for _idx, _room in enumerate(self.randomRooms):
            if _room.mapId == _mapId:
                _curIdx = _idx
                break

        if _curIdx != -1:
            _curWeight = self.randomWeights[_curIdx]
            self.randomWeights[_curIdx] = 0

        _randomIdx = utils.randomByWeight(self.randomWeights)

        if _curIdx != -1:
            self.randomWeights[_curIdx] = _curWeight

        if _randomIdx is None:
            return None

        return formula.getLineSpaceNo(self.randomRooms[_randomIdx].mapId, 0)

    def _getHallLineNo(self):
        for _lineNo in range(gameconst.MAX_CUBE_LINE):
            _spaceNo = formula.getLineSpaceNo(cube_config.datas['cube_hall']['value'], _lineNo)

            _linePlayers = self.allLines.get(_spaceNo)
            if not _linePlayers:
                return _lineNo

            if len(_linePlayers) + len(_linePlayers.pendingEnterPlayers) < gameconst.CUBE_HALL_MAX_NUM:
                return _lineNo

        return random.randint(0, gameconst.MAX_CUBE_LINE - 1)

    def doEnterCube(self, box, mapId, gbId, extra):
        INFO_MSG('CubeStub::doEnterCube: {} {}'.format(mapId, gbId))
        _spaceNo = formula.getLineSpaceNo(mapId, 0)
        self._doAvatarEnterCubeRoom(_spaceNo, box, gbId, extra)

    def gmEnterTargetRoom(self, box, gbId, spaceNo):
        _playerVal = self.allPlayers.get(gbId)
        self._doAvatarEnterCubeRoom(spaceNo, box, gbId, {})

    def reliveToCubeRoom(self, box, mapId, gbId, extra):
        _spaceNo = formula.getLineSpaceNo(mapId, 0)
        self._doAvatarEnterCubeRoom(_spaceNo, box, gbId, extra)

    def onAvatarOffline(self, gbId):
        INFO_MSG('CubeStub::onAvatarOffline: {}'.format(gbId))
        _playerVal = self.allPlayers.get(gbId)
        if not _playerVal:
            ERROR_MSG('onAvatarOffline: player not found: {}'.format(gbId))
            return

        _oldCanEnter = self.canSpaceEnter(_playerVal.curSpaceNo)
        self.removePlayer(gbId)

        if _oldCanEnter != self.canSpaceEnter(_playerVal.curSpaceNo):
            self._addRandomInfos(formula.getMapId(_playerVal.curSpaceNo))

    def logonEnterCube(self, box, gbId, spaceNo, extra):
        self.addEnterPlayer(box, gbId, 0, 0, linePlayers.LinePlayerVal.ENTERING, spaceNo, {})

        if not self.canSpaceEnter(spaceNo):
            self._removeRandomInfos(formula.getMapId(spaceNo))

        _spaceVal = self.staticSpaces[spaceNo]
        box.onLogonEnterCubeGetSpaceBox(_spaceVal.lineSpaceBox, _spaceVal.spaceMgrBoxCell.id)

    def enterRandomRoom(self, box, gbId, extra):
        _playerVal = self.allPlayers.get(gbId)
        if not _playerVal:
            ERROR_MSG('enterRandomRoom: player not found: {}'.format(gbId))
            return

        _spaceNo = self._getRandomSpaceNo(_playerVal.curSpaceNo)
        if _spaceNo is None:
            ERROR_MSG('enterRandomRoom: no space available')
            return

        self._doAvatarEnterCubeRoom(_spaceNo, box, gbId, extra)
        if not self.canSpaceEnter(_spaceNo):
            self._removeRandomInfos(formula.getMapId(_spaceNo))

    def _doAvatarEnterCubeRoom(self, spaceNo, box, gbId, extra):
        playerVal = self.allPlayers.get(gbId)
        if playerVal and playerVal.curSpaceNo == spaceNo:
            ERROR_MSG('CubeStub::_doAvatarEnterCubeRoom: player already in space: {} {}'.format(gbId, spaceNo))
            return

        if playerVal:
            self.addPendingEnterPlayer(spaceNo, gbId)
        else:
            self.addEnterPlayer(box, gbId, 0, 0, linePlayers.LinePlayerVal.ENTERING, spaceNo, {})

        _spaceVal = self.staticSpaces[spaceNo]
        box.cell.beginEnterCubeRoom(_spaceVal.lineSpaceBox, _spaceVal.spaceMgrBoxCell.id, _spaceVal.getSpaceNo(), extra)

    def onEnterCubeSuccess(self, gbId, spaceNo):
        INFO_MSG('CubeStub::onEnterCubeSuccess: {} {}'.format(gbId, spaceNo))
        _playerVal = self.allPlayers.get(gbId)
        if not _playerVal:
            ERROR_MSG('CubeStub::onEnterCubeSuccess: player not found: {}'.format(gbId))
            return

        _oldSpaceNo = _playerVal.curSpaceNo
        _oldCanEnter = self.canSpaceEnter(_oldSpaceNo)

        if _playerVal.playerStatus == linePlayers.LinePlayerVal.ENTERING:
            _playerVal.playerStatus = linePlayers.LinePlayerVal.IN_LINE

            if _playerVal.curSpaceNo != spaceNo:
                ERROR_MSG('CubeStub::onEnterCubeSuccess: spaceNo not match: {} {}'.format(_playerVal.curSpaceNo, spaceNo))

        else:
            self.switchStaticSpace(gbId, spaceNo)

        if _oldCanEnter != self.canSpaceEnter(_oldSpaceNo):
            self._addRandomInfos(formula.getMapId(_oldSpaceNo))

    def onLeaveCube(self, gbId, fromSpaceNo, curSpaceNo):
        INFO_MSG('onLeaveCube: {} {}'.format(gbId, curSpaceNo))
        _playerVal = self.allPlayers.get(gbId)
        if not _playerVal:
            ERROR_MSG('onLeaveCube: player not found: {}'.format(gbId))
            return

        if _playerVal.curSpaceNo != fromSpaceNo:
            ERROR_MSG('onLeaveCube: spaceNo not match: {} {}'.format(_playerVal.curSpaceNo, fromSpaceNo))

        if not formula.isCubeSpace(curSpaceNo):
            self.removePlayer(gbId)

    def onLoadGroupEntities(self, info):
        DEBUG_MSG("CubeStub::onLoadGroupEntities", info)
        super(CubeStub, self).onLoadGroupEntities(info)

    def onRefreshGroupEntities(self, info):
        DEBUG_MSG("CubeStub::onRefreshGroupEntities", info)
        super(CubeStub, self).onRefreshGroupEntities(info)
