# coding: utf-8

import KBEngine
from KBEDebug import *

import random

import utils
import json
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
import branchData_set as BDS
import cube_floor
import cube_room
import cube_config
import branchData_branchData as B_BD
import iLinePlayersStub
import branchData_set

class RandomRoomVal(object):
    def __init__(self, mapId):
        self.mapId = mapId


class CubeStub(iBaseNoCell.IBaseNoCell, iTimer.ITimer,
               iMultiStaticSpace.IMultiStaticSpace,
               iMultiStaticSpacePlayer.IMultiStaticSpacePlayer,
               iLinePlayersStub.IBranchLineStub):

    def __init__(self):
        iMultiStaticSpace.IMultiStaticSpace.__init__(self)
        iMultiStaticSpacePlayer.IMultiStaticSpacePlayer.__init__(self, gameconst.CUBE_MAX_ENTER_NUM)
        iLinePlayersStub.IBranchLineStub.__init__(self)
        self.addDatetimeTimerTick()
        self.cubeNo = self.cubeNo # type: int
        self.cubeRooms = {}
        self.randomRooms = []
        self.maxReadyLineNo = 0
        self.randomWeights = []
        interval = 60 * branchData_set.datas["Branch_mergeInterval"]["value"]
        waitTime = 60 * branchData_set.datas["Branch_mergeWaitingTime"]["value"]

        self.pyAddTimer(interval, interval, gametimer.CHECK_LINE_MERGE)
        self.pyAddTimer(interval + waitTime, interval, gametimer.DO_LINE_MERGE)
        self.pyAddTimer(5, 5, gametimer.CLEAR_MULTI_ENTER_TIME_OUT)

        self._startRefreshCowRefreshTimer()
        self.randomTeleporterPool = self._initRandomTeleporterPool()

    def _initRandomTeleporterPool(self):
        _list = []
        for _mapId in cube_room.floor2Rooms[self.cubeNo]:
            _dunData = utils.getDunStructModData(_mapId)
            if not _dunData:
                LOG_WARN('CubeStub::_initRandomTeleporterPool: dunData not found: {}'.format(_mapId))
                continue

            _cubeData = _dunData.get('Cube')
            if not _cubeData:
                LOG_WARN('CubeStub::_initRandomTeleporterPool: cubeData not found: {}'.format(_mapId))
                continue

            for _ in _cubeData.get('Teleporter', {}).keys():
                _list.append(_mapId)

        return _list

    def _startRefreshCowRefreshTimer(self):
        _delay = random.randint(*cube_config.datas['cube_cowRoomEntranceIntervalTime']['value'])
        _delay += cube_config.datas['cube_cowRoomEntranceTime']['value']
        _delay *= 60
        self.addTimerCB(_delay, '_doRandomTeleporter', (), gametimer.TIMER_TAG_CUBE_TELEPORTER_REFRESH)

    def _doRandomTeleporter(self):
        if not self.randomTeleporterPool:
            LOG_ERR('CubeStub::_doRandomTeleporter: randomTeleporterPool is empty')
            return

        _num = random.randint(*cube_config.datas['cube_cowRoomEntranceNum']['value'])
        _mapIds = random.sample(self.randomTeleporterPool, min(_num, len(self.randomTeleporterPool)))
        _dic = {}
        for _mapId in _mapIds:
            _dic[_mapId] = _dic.get(_mapId, 0) + 1

        LOG_INFO('_doRandomTeleporter:', _dic, [GP_GPD.datas[mapId]['name'] for mapId in _dic.keys()])
        for _mapId, num in _dic.items():
            lineCnt = gameconst.getBranchLineCnt(_mapId) if _mapId in B_BD.datas else 1
            for _lineNo in range(lineCnt):
                _spaceNo = formula.combineLineSpaceNo(_mapId, _lineNo)
                _spaceVal = self.staticSpaces[_spaceNo]
                _spaceVal.spaceMgrBoxCell.createTeleporterToCow(num)

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
        self._initAllRoom()
        self._initWeights()

    def _initWeights(self):
        for _cubeType, _mapIds in cube_room.floorTypeMapDic[self.cubeNo].items():
            if _cubeType not in (gameconst.CubeRoomType.NORMAL, gameconst.CubeRoomType.TIDE):
                continue

            for _mapId in _mapIds:
                self._addRandomInfos(_mapId)

    def onTimer(self, tid, userArg):
        if utils.isBelongTimerTag(userArg):
            self._onTimerCallback(tid)
        elif userArg == gametimer.TIMER_DATETIME_ITIMER_CALLBACK:
            self._onDatetimeTimerTick()
        elif userArg == gametimer.CLEAR_MULTI_ENTER_TIME_OUT:
            self.onClearEnterTimeOut(gameconst.CUBE_ENTER_TIME_OUT_DUR)
        elif userArg == gametimer.CHECK_LINE_MERGE:
            for _mapId in cube_room.floor2Rooms[self.cubeNo]:
                if _mapId in B_BD.datas:
                    self._checkLineMerge(_mapId)
        elif userArg == gametimer.DO_LINE_MERGE:
            for _mapId in cube_room.floor2Rooms[self.cubeNo]:
                if _mapId in B_BD.datas:
                    self._doLineMerge(_mapId)
        else:
            self._onTimer(tid, userArg)

    def _initAllRoom(self):
        for _floors in cube_room.floorTypeMapDic[self.cubeNo].values():
            for _mapId in _floors:
                if _mapId not in GP_GPD.datas:
                    LOG_ERR('CubeStub::_initAllRoom: mapId not found: {}'.format(_mapId))
                    continue
                
                if _mapId in B_BD.datas:
                    maxLineNum = gameconst.getBranchLineCnt(_mapId)
                    for _lineNo in range(maxLineNum):
                        self._createStaticSpace(_mapId, lineNo=_lineNo)
                else:
                    self._createStaticSpace(_mapId)

    def _getSpaceMgrEntityType(self):
        return 'CubeSpaceMgr'

    def _getRandomMapId(self, curSpaceNo, filterTypes):
        _mapId = formula.fetchMapId(curSpaceNo)
        _mapIds = []
        _weis = []
        for _idx, _room in enumerate(self.randomRooms):
            if _room.mapId == _mapId:
                continue

            _type = cube_room.datas[_room.mapId]['type']
            if _type in filterTypes:
                continue

            _wei = self.randomWeights[_idx]
            _mapIds.append(_room.mapId)
            _weis.append(_wei)

        _randomIdx = utils.randomByWeight(_weis)

        if _randomIdx is None:
            return None

        return _mapIds[_randomIdx]

    def doEnterCube(self, box, mapId, gbId, extra):
        _lineNo = 0
        if mapId in B_BD.datas:
            _lineNo = self._autoSelectLine(box, gbId, iLinePlayersStub.EnterLineExtra.new(extra, -1), lineType=mapId)
        LOG_INFO('CubeStub::doEnterCube: {} {} {}'.format(mapId, gbId, _lineNo))
        _spaceNo = formula.combineLineSpaceNo(mapId, _lineNo)
        self._doAvatarEnterCubeRoom(_spaceNo, box, gbId, extra)

    def gmEnterTargetRoom(self, box, gbId, spaceNo):
        _playerVal = self.allPlayers.get(gbId)
        self._doAvatarEnterCubeRoom(spaceNo, box, gbId, {})

    def _getAvailableReadyRoom(self):
        _mapId = cube_room.floorTypeMapDic[self.cubeNo][gameconst.CubeRoomType.READY][0]
        _enterSpaceNo = None
        # 100 是随便取的值，正常肯定达不到
        for _lineNo in range(100):
            _spaceNo = formula.combineLineSpaceNo(_mapId, _lineNo)
            if not self.isSpaceReady(_spaceNo):
                break

            if self.canSpaceEnter(_spaceNo):
                _enterSpaceNo = _spaceNo
                break

        if _enterSpaceNo is None:
            return formula.combineLineSpaceNo(_mapId, 0)
        else:
            return _enterSpaceNo

    def doEnterCubeReady(self, box, gbId, extra):
        _enterSpaceNo = self._getAvailableReadyRoom()
        self._doAvatarEnterCubeRoom(_enterSpaceNo, box, gbId, extra)

    def onAvatarOffline(self, gbId):
        LOG_INFO('CubeStub::onAvatarOffline: {}'.format(gbId))
        _playerVal = self.allPlayers.get(gbId)
        if not _playerVal:
            LOG_ERR('onAvatarOffline: player not found: {}'.format(gbId))
            return

        _oldCanEnter = self.canSpaceEnter(_playerVal.curSpaceNo)
        self.removePlayer(gbId)

        if _oldCanEnter != self.canSpaceEnter(_playerVal.curSpaceNo):
            self._addRandomInfos(formula.fetchMapId(_playerVal.curSpaceNo))

    def logonEnterCube(self, box, gbId, extra):
        _enterSpaceNo = self._getAvailableReadyRoom()
        self.addEnterPlayer(box, gbId, 0, 0, linePlayers.LinePlayerVal.ENTERING, _enterSpaceNo, extra)

        _spaceVal = self.staticSpaces[_enterSpaceNo]
        box.onLogonEnterCubeGetSpaceBox(_spaceVal.lineSpaceBox, _spaceVal.spaceMgrBoxCell.id, _enterSpaceNo)

    def enterRandomRoom(self, box, gbId, extra, curSpaceNo, filterTypes):
        mapId = self._getRandomMapId(curSpaceNo, filterTypes)
        if mapId is None:
            LOG_ERR('enterRandomRoom: no space available')
            return

        _lineNo = 0
        if mapId in B_BD.datas:
            _lineNo = self._autoSelectLine(box, gbId, iLinePlayersStub.EnterLineExtra.new(extra, -1), lineType=mapId)

        _spaceNo = formula.combineLineSpaceNo(mapId, _lineNo)

        self._doAvatarEnterCubeRoom(_spaceNo, box, gbId, extra)
        if not self.canSpaceEnter(_spaceNo):
            self._removeRandomInfos(formula.fetchMapId(_spaceNo))

    def _doAvatarEnterCubeRoom(self, spaceNo, box, gbId, extra):
        playerVal = self.allPlayers.get(gbId)
        if playerVal and playerVal.curSpaceNo == spaceNo:
            LOG_ERR('CubeStub::_doAvatarEnterCubeRoom: player already in space: {} {}'.format(gbId, spaceNo))
            return

        if playerVal:
            self.addPendingEnterPlayer(spaceNo, gbId)
        else:
            self.addEnterPlayer(box, gbId, 0, 0, linePlayers.LinePlayerVal.ENTERING, spaceNo, {})

        _spaceVal = self.staticSpaces[spaceNo]
        box.cell.beginEnterCubeRoom(_spaceVal.lineSpaceBox, _spaceVal.spaceMgrBoxCell.id, _spaceVal.getSpaceNo(), extra)

    def onEnterCubeSuccess(self, gbId, spaceNo):
        LOG_INFO('CubeStub::onEnterCubeSuccess: {} {}'.format(gbId, spaceNo))
        _playerVal = self.allPlayers.get(gbId)
        if not _playerVal:
            LOG_ERR('CubeStub::onEnterCubeSuccess: player not found: {}'.format(gbId))
            return

        _oldSpaceNo = _playerVal.curSpaceNo
        _oldCanEnter = self.canSpaceEnter(_oldSpaceNo)

        if _playerVal.playerStatus == linePlayers.LinePlayerVal.ENTERING:
            _playerVal.playerStatus = linePlayers.LinePlayerVal.IN_LINE

            if _playerVal.curSpaceNo != spaceNo:
                LOG_ERR('CubeStub::onEnterCubeSuccess: spaceNo not match: {} {}'.format(_playerVal.curSpaceNo, spaceNo))

        else:
            self.switchStaticSpace(gbId, spaceNo)

        if _oldCanEnter != self.canSpaceEnter(_oldSpaceNo):
            self._addRandomInfos(formula.fetchMapId(_oldSpaceNo))

    def onLeaveCube(self, gbId, fromSpaceNo, curSpaceNo):
        LOG_INFO('onLeaveCube: {} {}'.format(gbId, curSpaceNo))
        _playerVal = self.allPlayers.get(gbId)
        if not _playerVal:
            LOG_ERR('onLeaveCube: player not found: {}'.format(gbId))
            return

        if _playerVal.curSpaceNo != fromSpaceNo:
            LOG_ERR('onLeaveCube: spaceNo not match: {} {}'.format(_playerVal.curSpaceNo, fromSpaceNo))

        if curSpaceNo not in self.staticSpaces:
            self.removePlayer(gbId)

    def onLoadGroupEntities(self, info):
        LOG_DBG("CubeStub::onLoadGroupEntities", info)
        super(CubeStub, self).onLoadGroupEntities(info)

    def onRefreshGroupEntities(self, info):
        LOG_DBG("CubeStub::onRefreshGroupEntities", info)
        super(CubeStub, self).onRefreshGroupEntities(info)

    def onDestroyGroupEntities(self, info):
        LOG_DBG("CubeStub::onDestroyGroupEntities", info)
        super(CubeStub, self).onDestroyGroupEntities(info)

    # ------------------ 神秘商人 start -----------------------------------
    def onLoadEntitiesEnd(self, spaceNo):
        super(CubeStub, self).onLoadEntitiesEnd(spaceNo)
        if not self.loadWaitSet and not self.curChapManMapId:
            pass
            # self._createAndDestroyChapMan()
            # _delay = cube_config.datas['cube_chapmanRefreshInterval']['value'] * 60
            # self.addTimerCB(_delay, '_doCreateChapMan', (), gametimer.TIMER_TAG_CREATE_CHAP_MAN)

    def _doCreateChapMan(self):
        self._createAndDestroyChapMan()

        _delay = cube_config.datas['cube_chapmanRefreshInterval']['value'] * 60
        self.addTimerCB(_delay, '_doCreateChapMan', (), gametimer.TIMER_TAG_CREATE_CHAP_MAN)

    def _createAndDestroyChapMan(self):
        _newManInfo = self._getNewChapManMapInfo()

        if self.curChapManMapId:
            _spaceNo = formula.combineLineSpaceNo(self.curChapManMapId, 0) #TODO 分线（神秘商人目前被干掉了）
            _spaceVal = self.staticSpaces[_spaceNo]
            LOG_INFO('_createAndDestroyChapMan: destroy old chapman', _spaceNo)
            _spaceVal.spaceMgrBoxCell.destroyChanMap()

        _mapId, _pos, _dir = _newManInfo
        self.curChapManMapId = _mapId
        _spaceNo = formula.combineLineSpaceNo(_mapId, 0)
        _spaceVal = self.staticSpaces[_spaceNo]
        LOG_INFO('_createAndDestroyChapMan: create new chapman', _spaceNo)
        _spaceVal.spaceMgrBoxCell.createChapMan(_pos, _dir)

    def _getNewChapManMapInfo(self):
        _infos = []
        for _data in cube_floor.datas[self.cubeNo]['position']:
            _mapId, _x, _y, _z, _dir = _data
            if _mapId == self.curChapManMapId:
                continue

            _infos.append((_mapId, (_x, _y, _z), _dir))

        return random.choice(_infos)

    # ------------------ 神秘商人 end -----------------------------------

    def doGetCubeReadyLineCnt(self, box, mapId):
        res = self._calculateLineInfo(mapId)

        LOG_DBG('doQueryLineInfo', res)
        box.client.onGetLineInfo(json.dumps(res))

    def checkSwitchCubeLine(self, box, lineNo, _mapId):
        _spaceNo = formula.combineLineSpaceNo(_mapId, lineNo)

        _canEnter = self.canSpaceEnter(_spaceNo)
        box.cell.onCheckSwitchCubeLineResult(lineNo, _canEnter)

    def doSwitchCubeLine(self, box, gbId, lineNo, extra, _mapId):
        _spaceNo = formula.combineLineSpaceNo(_mapId, lineNo)

        if not self.canSpaceEnter(_spaceNo):
            self.onMessagePre(BDS.datas["Branch_fullCapacityMsg"]["value"], [])
            return

        self._doAvatarEnterCubeRoom(_spaceNo, box, gbId, extra)
    


