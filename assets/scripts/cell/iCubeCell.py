# coding: utf-8
import KBEngine
from KBEDebug import *


import math
import dataUtils
import random
import formula
import complexTeleportOption
import gameconst
import gameengine
import gamedecorator
import dungeonSrc
import utils
import actionContext
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
    def __init__(self):
        if self.cubeQuota.cubeDurState == gameconst.CubeDurStatus.ENTER:
            ERROR_MSG('cube dur state invalid', self.cubeQuota)
            self.cubeQuota.resetOnLogin()

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

    @gamedecorator.checkGameconfigEnable('square')
    @utils.isMyself
    def setEnterCubeFloor(self, exposed, floor):
        INFO_MSG('ICubeCell::setEnterCubeFloor: {}'.format(floor))
        if floor not in cube_floor.datas:
            ERROR_MSG('ICubeCell::setEnterCubeFloor: floor not found: {}'.format(floor))
            return

        _mapId = formula.getMapId(self.spaceNo)
        _mapData = cube_room.datas.get(_mapId)
        if not _mapData:
            ERROR_MSG('ICubeCell::setEnterCubeFloor: map not found: {}'.format(_mapId))
            return

        if _mapData['type'] != gameconst.CubeRoomType.READY:
            ERROR_MSG('ICubeCell::setEnterCubeFloor: not ready room: {}'.format(_mapId))
            return

        self.cubeEnterFloor = floor

    def _needTimerOn(self, spaceNo):
        if not formula.isCubeSpace(spaceNo):
            return False

        return not formula.isCubeReady(spaceNo)

    def _dealWithCubeTimer(self, fromSpaceNo, toSpaceNo):
        _fromNeed = self._needTimerOn(fromSpaceNo)
        _toNeed = self._needTimerOn(toSpaceNo)

        if _fromNeed == _toNeed:
            return

        if _toNeed:
            self.cubeQuota.setCubeEnterTime(self, utils.getNow())
            self._startCubeTimeOutTimer()

        else:
            if self.cubeRoomTimerId:
                self._cancelDatetimeCallback(self.cubeRoomTimerId, gametimer.TIMER_TAG_CUBE_ROOM)
                self.cubeRoomTimerId = 0

            self.cubeQuota.checkout()

    def _onCubeOffline(self):
        if not self._needTimerOn(self.spaceNo):
            return

        if self.cubeRoomTimerId:
            self._cancelDatetimeCallback(self.cubeRoomTimerId, gametimer.TIMER_TAG_CUBE_ROOM)
            self.cubeRoomTimerId = 0

        self.cubeQuota.checkout()

    @gamedecorator.checkGameconfigEnable('square')
    @utils.isMyself
    @gamedecorator.limitcall(1)
    def enterCube(self, exposed, floor):
        INFO_MSG('ICubeCell::enterCube', floor)
        self.enterCubeInternal()

    def enterCubeInternal(self):
        _floor = 1
        if not utils.isActOpen(cube_config.datas['cubeActID']['value']):
            self.showMsg(AC_CD.datas['activity_notOpen']['value'], [])
            return

        if formula.isCubeSpace(self.spaceNo):
            WARNING_MSG('enterCube but already in cube:', self.spaceNo)
            return

        # 这里直接选取大厅作为check能否进入的参考层
        _mapId = cube_room.floorTypeMapDic[_floor][gameconst.CubeRoomType.READY][0]
        _targetSpaceNo = formula.getLineSpaceNo(_mapId, 0)
        if not utils.checkCanChangeSceneAndShowMsg(self, self.spaceNo, _targetSpaceNo):
            return

        if self.cubeQuota.cubeDurState == gameconst.CubeDurStatus.ENTER:
            ERROR_MSG('ICubeCell::enterCube: has entered')
            return

        if self.cubeQuota.leftTime <= 0:
            self.base.beforeEnterCubeDecrementCnt({})
            return

        extra = {'enterCubeType': gameconst.ENTER_CUBE_HAS_LEFT_TIME}
        gameengine.getCubeStub(_floor).doEnterCubeReady(
            self.base, self.gbId, extra)

    @gamedecorator.checkGameconfigEnable('square')
    @utils.isMyself
    def randomCubeRoom(self, exposed):
        self.doRandomCubeRoom()

    def doRandomCubeRoom(self):
        if not formula.isCubeSpace(self.spaceNo):
            ERROR_MSG('randomCubeRoom but not in cube', self.spaceNo)
            return

        if not self.cubeEnterFloor:
            self.cubeEnterFloor = 1

        gameengine.getCubeStub(self.cubeEnterFloor).enterRandomRoom(self.base, self.gbId, {}, self.spaceNo)

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

        _floor = cube_room.datas[_mapId]['floor']
        gameengine.getCubeStub(_floor).doEnterCube(
            self.base, _mapId, self.gbId, {})

    @gamedecorator.checkGameconfigEnable('square')
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
        gameengine.getCubeStubBySpaceNo(_spaceNo).doEnterCube(
            self.base, _mapId, self.gbId, {'followPos': _pos})

    def gmEnterCubeRoom(self, mapId):
        _targetFloor = dataUtils.getCubeFloor(mapId)
        gameengine.getCubeStub(_targetFloor).doEnterCube(self.base, mapId, self.gbId, {})
        return True

    @utils.isMyself
    def leaveCube(self, exposed):
        self.leaveCubeInternal(gameconst.DungeonSrcEnum.FROM_CLIENT)

    def leaveCubeInternal(self, srcId):
        if not formula.isCubeSpace(self.spaceNo):
            INFO_MSG('leaveCubeInternal but not cube space: {}'.format(self.spaceNo))
            return

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

    def _startCubeTimeOutTimer(self):
        if self.cubeRoomTimerId:
            self._cancelDatetimeCallback(self.cubeRoomTimerId, gametimer.TIMER_TAG_CUBE_ROOM)

        _fireTime = utils.getNow() + max(1, self.cubeQuota.calcLeftTime())
        self.cubeRoomTimerId = self._datetimeCallback(_fireTime, '_onCubeTimeOut', (), gametimer.TIMER_TAG_CUBE_ROOM, 'cubeRoomTimerId')

    def _onCubeTimeOut(self):
        INFO_MSG('ICubeCell::_onCubeTimeOut: {}'.format(self.spaceNo))
        if not formula.isCubeSpace(self.spaceNo):
            return

        _switchVal = self.getTempMiscProp(gameconst.AvatarProps.cubeAutoRenewSwitch)

        if _switchVal is None:
            self.leaveCubeInternal(gameconst.DungeonSrcEnum.FROM_TIME_OUT)
            return

        if not _switchVal.canAddTimes():
            self.leaveCubeInternal(gameconst.DungeonSrcEnum.FROM_TIME_OUT)
            return

        if not self._checkAddCubeRoomDurationCondition():
            self.leaveCubeInternal(gameconst.DungeonSrcEnum.FROM_TIME_OUT)
            return

        _switchVal.addTimes()
        _ctx = actionContext.CubeDurCtx(self.base, True)
        self.base.autoRenewCubeRoom(_switchVal.toClientData(), _ctx)
        self.client.onCubeAutoRenewSwitch(True, _switchVal.toClientData())

    def _checkAddCubeRoomDurationCondition(self):
        _curMapId = formula.getMapId(self.spaceNo)
        _curFloor = dataUtils.getCubeFloor(_curMapId)
        if not _curFloor:
            WARNING_MSG('ICubeCell::checkAddCubeRoomDurationCondition: floor not found: {}'.format(_curMapId))
            return False

        if self.cubeQuota.calcLeftTime() > cube_config.datas['cubeNumTime']['value'] * 60:
            WARNING_MSG('ICubeCell::checkAddCubeRoomDurationCondition: duration beyond max')
            return False

        return True

    def checkAddCubeRoomDurationCondition(self, itemId, num):
        if not self._checkAddCubeRoomDurationCondition():
            return

        self.base.useItemAddCubeTimes(itemId, num, True, True, gameconst.CubeAddTimesReason.CHECK_COND)

    def directlyAddCubeRoomDuration(self, func, args, cubeDurCtx):
        if not self._checkAddCubeRoomDurationCondition():
            getattr(self.base, func)(*args)
            cubeDurCtx.done(False)
            return

        _dur = cube_config.datas['cubeNumTime']['value'] * 60
        self.cubeQuota.addLeftTime(self, _dur)
        self.base.activityComplete(cube_config.datas['cubeActID']['value'])
        self._startCubeTimeOutTimer()

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

        _time = self.cubeQuota.calcLeftTime() + utils.getNow()
        self.client.onCubeLoginData(_time, _renewSwitch, _switchData, _rewardList)

    def onLogonEnterCubeCB(self, spaceMgrId):
        INFO_MSG('ICubeCell::onLogonEnterCubeCB: {}'.format(spaceMgrId))
        _dir = self._getEntranceDirByDungeonNo(formula.getMapId(self.spaceNo))
        self.position = self._getEntranceByDungeonNo(formula.getMapId(self.spaceNo))
        self.direction = (0, 0, _dir * math.pi / 180) if _dir is not None else self.direction
        self.spaceMgrId = spaceMgrId
        self.spaceMgr.onPlayerEnter(self.id)
        gameengine.getCubeStubBySpaceNo(self.spaceNo).onEnterCubeSuccess(self.gbId, self.spaceNo)

        if self._needTimerOn(self.spaceNo):
            self.cubeQuota.setCubeEnterTime(self, utils.getNow())
            self._startCubeTimeOutTimer()

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

    @property
    def cubeRandRoomCD(self):
        return self.getTempMiscProp(gameconst.AvatarProps.cubeRandRoomCD, 0)

    @cubeRandRoomCD.setter
    def cubeRandRoomCD(self, val):
        if not val:
            self.popTempMiscProp(gameconst.AvatarProps.cubeRandRoomCD)
        else:
            self.setTempMiscProp(gameconst.AvatarProps.cubeRandRoomCD, val)

    @utils.isMyself
    def getCubeRoomLeftTime(self, exposed):
        INFO_MSG('ICubeCell::getCubeRoomLeftTime')
        self.client.onCubeRoomLeftTime(self.cubeQuota.leftTime)

    # ------------------------ props end ------------------------

    # ----------------------- 祈福之间 start ---------------------

    # ----------------------- 祈福之间 end ---------------------
