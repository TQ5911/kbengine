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

        for _floor in cube_room.floor2Cow.keys():
            self._startRefreshCowRefreshTimer(_floor)

    def _startRefreshCowRefreshTimer(self, floor):
        _delay = random.randint(*cube_config.datas['cube_cowRoomEntranceIntervalTime']['value'])
        _delay += cube_config.datas['cube_cowRoomEntranceTime']['value']
        _delay *= 60
        self._callback(_delay, '_doRandomTeleporter', (floor,), gametimer.TIMER_TAG_CUBE_TELEPORTER_REFRESH)

    def _doRandomTeleporter(self, floor):
        _num = random.randint(*cube_config.datas['cube_cowRoomEntranceNum']['value'])
        _mapIds = random.sample(cube_room.floor2Rooms[floor], _num)
        DEBUG_MSG('_doRandomTeleporter:', _mapIds)
        for _mapId in _mapIds:
            _spaceNo = formula.getLineSpaceNo(_mapId, 0)
            _spaceVal = self.staticSpaces[_spaceNo]
            _spaceVal.spaceMgrBoxCell.createTeleporterToCow()

        self._startRefreshCowRefreshTimer(floor)

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
        for _lineNo in range(gameconst.MAX_CUBE_LINE):
            self._createStaticSpace(
                cube_config.datas['cube_hall']['value'],
                lineNo=_lineNo)

        # 再创建其他房间，经验房等
        for _floor, _datas in cube_room.floor2Rooms.items():
            for _mapId in _datas:
                self._createStaticSpace(_mapId)

        for _mapId in cube_room.floor2Cow.values():
            self._createStaticSpace(_mapId)

        # _cubeDatas = dataUtils.getAllCubeRooms(self.cubeNo)
        # for _cubeData in _cubeDatas:
        #     _room = CubeRoom.CubeRoom(_cubeData['ID'], _cubeData['weight'], self.cubeNo)
        #     self.cubeRooms[_room.dunId] = _room
        #     self._createStaticSpace(_room.dunId)

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
        if mapId == cube_config.datas['cube_hall']['value']:
            _lineNo = self._getHallLineNo()
            _spaceNo = formula.getLineSpaceNo(mapId, _lineNo)
        else:
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
