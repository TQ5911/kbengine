# coding: utf-8
import KBEngine
from KBEDebug import *


import dataUtils
import random
import formula
import complexTeleportOption
import gameconst
import gameengine
import dungeonSrc
import utils
import cube_floor
import gametimer
import cube_config
import cube_room
import activityControl_config as AC_CD


class CubeSwitch(object):
    def __init__(self, coinSwitch=False, itemSwitch=False, times=0):
        self.coinSwitch = coinSwitch
        self.itemSwitch = itemSwitch
        self.times = times
        self.curTimes = 0

    def canAddTimes(self):
        return self.curTimes < self.times

    def addTimes(self):
        DEBUG_MSG('CubeSwitch::addTimes: {}'.format(self.curTimes))
        self.curTimes += 1

    def toClientData(self):
        return {
            'coinSwitch': self.coinSwitch,
            'itemSwitch': self.itemSwitch,
            'times': max(0, self.times - self.curTimes),
        }


class ICubeCell(object):
    def startCubeCowTimer(self):
        if self.cubeCowTimerId:
            return

        self.cubeCowTimerId = self.pyAddTimer(
            gameconst.CUBE_COW_DUR_INTERVAL,
            gameconst.CUBE_COW_DUR_INTERVAL,
            gametimer.CUBE_COW_TICK,
        )

    def resetCubeCowDur(self):
        self.todayCubeCowDur = 0

    def cubeCowTick(self):
        _mapId = formula.getMapId(self.spaceNo)
        if not dataUtils.isCubeCow(_mapId):
            if self.cubeCowTimerId:
                self.pyDelTimer(self.cubeCowTimerId, gametimer.CUBE_COW_TICK)
                self.cubeCowTimerId = 0
            return

        self.todayCubeCowDur += gameconst.CUBE_COW_DUR_INTERVAL
        if not self.isCubeCowDurFull():
            return

        if self.cubeCowTimerId:
            self.pyDelTimer(self.cubeCowTimerId, gametimer.CUBE_COW_TICK)
            self.cubeCowTimerId = 0

        self.backOriginRoomFromCow()

    def isCubeCowDurFull(self):
        return self.todayCubeCowDur >= cube_config.datas['cube_cowRoomEntrancePersonalTime']['value'] * 60

    @utils.isMyself
    def setEnterCubeFloor(self, exposed, floor):
        INFO_MSG('ICubeCell::setEnterCubeFloor: {}'.format(floor))
        if floor not in cube_floor.datas:
            ERROR_MSG('ICubeCell::setEnterCubeFloor: floor not found: {}'.format(floor))
            return

        self.cubeEnterFloor = floor

    @utils.isMyself
    def enterCube(self, exposed):
        INFO_MSG('ICubeCell::enterCube')
        if not utils.isActOpen(cube_config.datas['cubeActID']['value']):
            self.showMsg(AC_CD.datas['activity_notOpen']['value'], [])
            return

        # 这里直接选取大厅作为check能否进入的参考层
        _mapId = cube_config.datas['cube_hall']['value']
        _targetSpaceNo = formula.getLineSpaceNo(_mapId, 0)
        if not utils.checkCanChangeSceneAndShowMsg(self, self.spaceNo, _targetSpaceNo):
            return

        self.base.beforeEnterCubeDecrementCnt({})

    def enterCubeByFloorConfig(self):
        INFO_MSG('ICubeCell::enterCubeByFloorConfig: {}'.format(self.cubeEnterFloor))
        if not self.cubeEnterFloor:
            self.cubeEnterFloor = 1

        _mapIds = cube_room.floor2SignMapIds[self.cubeEnterFloor]
        self.enterCubeByMapIds(_mapIds)

    def backOriginRoomFromCow(self):
        INFO_MSG('ICubeCell::backOriginRoomFromCow: {}'.format(self.spaceNo))
        self.enterCubeByMapIds([self.fromCubeMapId])

    def enterCubeByMapIds(self, mapIds):
        INFO_MSG('ICubeCell::enterCubeByMapIds: {}'.format(mapIds))
        _mapIds = []
        _someScore = 0
        for _mapId in mapIds:
            if _mapId not in cube_room.datas:
                ERROR_MSG('ICubeCell::enterCubeByMapIds: map not found: {}'.format(_mapId))
                continue

            _floor = cube_room.datas[_mapId]['floor']
            _needScore = cube_floor.datas[_floor]['needScore']
            if self.getTotalScore() < _needScore:
                _someScore = _needScore
                continue

            _mapIds.append(_mapId)

        if not _mapIds:
            self.showMsg(cube_config.datas['cube_floorJudge']['value'], [str(_someScore)])
            return

        _mapId = random.choice(mapIds)

        if dataUtils.isCubeCow(_mapId) and self.isCubeCowDurFull():
            ERROR_MSG('cube cow full')
            return

        gameengine.getGlobalBase('CubeStub').doEnterCube(
            self.base, _mapId, self.gbId, {})

    @utils.isMyself
    def followCaptainInCube(self, exposed):
        INFO_MSG('ICubeCell::followCaptainInCube: {}'.format(self.spaceNo))
        if not formula.isCubeSpace(self.spaceNo):
            ERROR_MSG('ICubeCell::followCaptainInCube: not cube space: {}'.format(self.spaceNo))
            return

        _spaceNo = self.getCaptainSpaceNo()
        _pos = self.getCaptainPosition()
        if not (_spaceNo and _pos):
            WARNING_MSG('ICubeCell::followCaptainInCube: captain not found', _spaceNo, _pos)
            return

        if not formula.isCubeSpace(_spaceNo):
            WARNING_MSG('ICubeCell::followCaptainInCube: captain not in cube space', _spaceNo, _pos)
            return

        _mapId = formula.getMapId(_spaceNo)
        gameengine.getGlobalBase('CubeStub').doEnterCube(
            self.base, _mapId, self.gbId, {'followPos': _pos})

    def gmEnterCubeRoom(self, mapId):
        _curMapId = formula.getMapId(self.spaceNo)
        _curFloor = dataUtils.getCubeFloor(_curMapId)

        _targetFloor = dataUtils.getCubeFloor(mapId)
        if _curFloor != _targetFloor:
            ERROR_MSG('ICubeCell::gmEnterCubeRoom: floor not match: {} {}'.format(_curFloor, _targetFloor))
            return False

        spaceNo = formula.getLineSpaceNo(mapId, 0)
        gameengine.getCubeStub(_curFloor).gmEnterTargetRoom(self.base, self.gbId, spaceNo)
        return True

    @utils.isMyself
    def leaveCube(self, exposed):
        self._leaveCube(gameconst.DungeonSrcEnum.FROM_CLIENT)

    def _leaveCube(self, srcId):
        _src = dungeonSrc.BasicDungeonSrc(srcId=srcId)
        _l = {}
        _context = {
            'e': {},
            'l': _l,
            'src': _src,
            'hasCast': True,
        }

        _canLeave = self.packageComplexTeleportLeaveData(_l)
        if not _canLeave:
            WARNING_MSG('ICubeCell::leaveCube: can not leave')
            return

        _, _m_outsideRecord = self.tryGetLastTeleportOutesideRecord(self.spaceNo, spaceType=formula.whatSpaceType(self.spaceNo))
        _spaceNo = _m_outsideRecord.spaceNo if _m_outsideRecord else formula.getLineSpaceNo(gameconst.MapIdDef.mapXinYuanCheng)

        _options = complexTeleportOption.ComplexTeleportOptions(teleportType=gameconst.ComplexTeleportType.LEAVE)
        self.doLeaveFromSapceToSpace(self.spaceNo, _spaceNo, _options, _context)

    def beginEnterCubeRoom(self, spaceBox, spaceMgrCellId, spaceNo, extra):
        _lContext = {}
        _src = dungeonSrc.BasicDungeonSrc()
        _context = {
            'e': {
                'spaceBox': spaceBox,
                'spaceMgrId': spaceMgrCellId,
            },
            'l': _lContext,
            'src': _src,
            'hasCast': True,
            'cube': extra
        }
        _options = complexTeleportOption.ComplexTeleportOptions(teleportType=gameconst.ComplexTeleportType.ENTER)

        canLeave = self.packageComplexTeleportLeaveData(_lContext)
        if not canLeave:
            WARNING_MSG('ICubeCell::beginEnterCubeRoom: can not leave')
            return

        self.teleportFromSpaceToSpace(self.spaceNo, spaceNo, options=_options, context=_context)

    def onEnterCubeSetTime(self):
        _dur = cube_config.datas['cubeNumTime']['value'] * 60
        self.setCubeRoomLeftTime(utils.getNow() + _dur)
        self._startRenewTimer()
        self.base.afterEnterCubeDeductTimes()

    def _startRenewTimer(self):
        if self.cubeRoomTimerId:
            self._cancelDatetimeCallback(self.cubeRoomTimerId, gametimer.TIMER_TAG_CUBE_ROOM)

        _fireTime = self.cubeRoomLeftTime - 60
        _fireTime = max(utils.getNow() + 1, _fireTime)
        self.cubeRoomTimerId = self._datetimeCallback(_fireTime, 'autoRenewCB', (), gametimer.TIMER_TAG_CUBE_ROOM, 'cubeRoomTimerId')
        self.cubeDurStatus = gameconst.RenewDurStatus.WAIT_AUTO

    def autoRenewCB(self):
        INFO_MSG('ICubeCell::autoRenewCB: {}'.format(self.spaceNo))
        if not formula.isCubeSpace(self.spaceNo):
            return

        _fireTime = max(utils.getNow() + 5, self.cubeRoomLeftTime)
        self.cubeRoomTimerId = self._datetimeCallback(_fireTime, 'onCubeRoomEndTimeCB', (), gametimer.TIMER_TAG_CUBE_ROOM, 'cubeRoomTimerId')
        self.cubeDurStatus = gameconst.RenewDurStatus.WAIT_END
        _switchVal = self.getTempMiscProp(gameconst.AvatarProps.cubeAutoRenewSwitch)

        if _switchVal is None:
            return

        if not _switchVal.canAddTimes():
            return

        if not self._checkAddCubeRoomDurationCondition():
            return

        _switchVal.addTimes()
        self.base.autoRenewCubeRoom(_switchVal.toClientData())
        self.client.onCubeAutoRenewSwitch(True, _switchVal.toClientData())

    def onCubeRoomEndTimeCB(self):
        if not formula.isCubeSpace(self.spaceNo):
            return

        INFO_MSG('ICubeCell::onCubeRoomEndTime: {}'.format(self.spaceNo))
        self._leaveCube(gameconst.DungeonSrcEnum.FROM_TIME_OUT)
        self.cubeDurStatus = 0

    def _checkAddCubeRoomDurationCondition(self):
        _curMapId = formula.getMapId(self.spaceNo)
        _curFloor = dataUtils.getCubeFloor(_curMapId)
        if not _curFloor:
            WARNING_MSG('ICubeCell::checkAddCubeRoomDurationCondition: floor not found: {}'.format(_curMapId))
            return False

        if self.cubeRoomLeftTime - utils.getNow() > cube_config.datas['cubeNumTime']['value'] * 60:
            WARNING_MSG('ICubeCell::checkAddCubeRoomDurationCondition: duration beyond max', self.cubeRoomLeftTime)
            return False

        return True

    def setCubeRoomLeftTime(self, leftTime):
        self.cubeRoomLeftTime = leftTime
        self.client.onCubeRoomEndTime(leftTime)

    def checkAddCubeRoomDurationCondition(self, itemId, num):
        if not self._checkAddCubeRoomDurationCondition():
            return

        self.base.useItemAddCubeTimes(itemId, num, True, True, gameconst.CubeAddTimesReason.CHECK_COND)

    def directlyAddCubeRoomDuration(self, func, args):
        if not self._checkAddCubeRoomDurationCondition():
            getattr(self.base, func)(*args)
            return

        _dur = cube_config.datas['cubeNumTime']['value'] * 60
        _now = utils.getNow()
        self.setCubeRoomLeftTime(max(self.cubeRoomLeftTime, _now) + _dur)
        self.base.activityComplete(cube_config.datas['cubeActID']['value'])
        self._startRenewTimer()

    def addCubeRoomRewardRecord(self, rewardList):
        _dic = self.getTempMiscProp(gameconst.AvatarProps.cubeRoomRewardList, {})
        for _data in rewardList:
            _itemId = _data['itemId']
            _bindType = _data['bindType']
            _dic.setdefault(_itemId, {})
            _dic[_itemId][_bindType] = _dic[_itemId].get(_bindType, 0) + _data['itemNum']

        self.setTempMiscProp(gameconst.AvatarProps.cubeRoomRewardList, _dic)
        self.client.onAddCubeRoomRewardRecord(rewardList)

    def clearCubeRoomRewardRecord(self):
        self.popTempMiscProp(gameconst.AvatarProps.cubeRoomRewardList)

    def toClientCubeLoginData(self):
        if not formula.isCubeSpace(self.spaceNo):
            return

        _rewardList = []
        for k, v in self.getTempMiscProp(gameconst.AvatarProps.cubeRoomRewardList, {}).items():
            for _bindType, _num in v.items():
                _rewardList.append({'itemId': k, 'itemNum': _num, 'bindType': _bindType})

        _switchVal = self.getTempMiscProp(gameconst.AvatarProps.cubeAutoRenewSwitch)
        if _switchVal is None:
            _renewSwitch = False
            _switchData = CubeSwitch().toClientData()
        else:
            _renewSwitch = True
            _switchData = _switchVal.toClientData()

        self.client.onCubeLoginData(self.cubeRoomLeftTime, _renewSwitch, _switchData, _rewardList)

    def onLogonEnterCubeCB(self, spaceMgrId):
        INFO_MSG('ICubeCell::onLogonEnterCubeCB: {}'.format(spaceMgrId))
        self.spaceMgrId = spaceMgrId
        self.spaceMgr.onPlayerEnter(self.id)
        gameengine.getGlobalBase('CubeStub').onEnterCubeSuccess(self.gbId, self.spaceNo)
        self._startRenewTimer()

        _mapId = formula.getMapId(self.spaceNo)
        if dataUtils.isCubeCow(_mapId):
            self.startCubeCowTimer()

    # ------------------------ props start ------------------------
    @utils.isMyself
    def reqChangeCubeAutoRenewSwitch(self, exposed, masterSwitch, switchData):
        INFO_MSG('ICubeCell::reqChangeCubeAutoRenewSwitch: {} {}'.format(masterSwitch, switchData))
        if masterSwitch and not utils.isActOpen(cube_config.datas['cubeActID']['value']):
            INFO_MSG('ICubeCell::reqChangeCubeAutoRenewSwitch: cubeActID not open')
            return

        self._changeCubeAutoRenewSwitch(masterSwitch, switchData)

    def _changeCubeAutoRenewSwitch(self, masterSwitch, switchData):
        if not masterSwitch:
            self.popTempMiscProp(gameconst.AvatarProps.cubeAutoRenewSwitch)
            self.client.onCubeAutoRenewSwitch(False, CubeSwitch().toClientData())
            return

        _switchVal = CubeSwitch(**switchData)
        self.setTempMiscProp(gameconst.AvatarProps.cubeAutoRenewSwitch, _switchVal)
        self.client.onCubeAutoRenewSwitch(True, switchData)

        if self.cubeDurStatus == gameconst.RenewDurStatus.WAIT_END:
            self._startRenewTimer()

    @property
    def cubeRandRoomCD(self):
        return self.getTempMiscProp(gameconst.AvatarProps.cubeRandRoomCD, 0)

    @cubeRandRoomCD.setter
    def cubeRandRoomCD(self, val):
        if not val:
            self.popTempMiscProp(gameconst.AvatarProps.cubeRandRoomCD)
        else:
            self.setTempMiscProp(gameconst.AvatarProps.cubeRandRoomCD, val)

    @property
    def cubeDurStatus(self):
        return self.getTempMiscProp(gameconst.AvatarProps.cubeDurStatus, 0)

    @cubeDurStatus.setter
    def cubeDurStatus(self, val):
        if not val:
            self.popTempMiscProp(gameconst.AvatarProps.cubeDurStatus)
        else:
            self.setTempMiscProp(gameconst.AvatarProps.cubeDurStatus, val)
    # ------------------------ props end ------------------------
