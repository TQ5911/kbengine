# coding: utf-8
import KBEngine
from KBEDebug import *


import math
import dataUtils
import random
import conflict_conflict_def as CCD
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
import branchData_set as BDS
import activityControl_config as AC_CD
import const_const as CONST
import dataUtils


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
        if self.cubeQuota.quotaDurState != gameconst.QuotaDurStatus.NORMAL:
            ERROR_MSG('cube dur state invalid', self.cubeQuota)
            self.cubeQuota.resetOnLogin()

    def _getCubeRoomType(self, spaceNo):
        _mapId = formula.getMapId(spaceNo)
        _cubeData = cube_room.datas.get(_mapId, None)
        if not _cubeData:
            return 0

        return _cubeData['type']

    def _getCubeRoomTypeByMapId(self, mapId):
        _cubeData = cube_room.datas.get(mapId, None)
        if not _cubeData:
            return 0

        return _cubeData['type']

    def _genCubeRoomFilterTypes(self):
        _filterTypes = []
        for _type, _data in self.cubeRoomLeftTimeDic.items():
            _useTime, _ = _data
            if _useTime >= dataUtils.getCubeTypeMaxTime(_type):
                _filterTypes.append(_type)

        return _filterTypes

    def _isCubeMapFullByMapId(self, mapId):
        _cubeData = cube_room.datas.get(mapId, None)
        if not _cubeData:
            return True

        _cubeType = _cubeData['type']
        _useTime, _enterTime = self.cubeRoomLeftTimeDic.get(_cubeType, (0, 0))
        _maxTime = dataUtils.getCubeTypeMaxTime(_cubeType)
        return _useTime >= _maxTime

    def _cubeRoomSetEnterTime(self, spaceNo, now):
        _cubeType = self._getCubeRoomType(spaceNo)
        _useTime, _enterTime = self.cubeRoomLeftTimeDic.get(_cubeType, (0, 0))
        self.cubeRoomLeftTimeDic[_cubeType] = (_useTime, now)
        DEBUG_MSG('[cube]_cubeRoomSetEnterTime', spaceNo, now, _useTime)

    def _cubeRoomKickCheckout(self, spaceNo):
        _cubeType = self._getCubeRoomType(spaceNo)
        _useTime, _enterTime = self.cubeRoomLeftTimeDic.get(_cubeType, (0, 0))
        _now = utils.getNow()
        if _now - _enterTime > gameconst.CUBE_ROOM_KICK_INTERVAL + 5:
            ERROR_MSG('_cubeRoomKickCheckout _now - _enterTime > gameconst.CUBE_ROOM_KICK_INTERVAL + 5', _now, _enterTime)

        _useTime += _now - _enterTime
        self.cubeRoomLeftTimeDic[_cubeType] = (_useTime, _now)
        DEBUG_MSG('[cube]_cubeRoomKickCheckout', spaceNo, _useTime, _now)

    def _dealWithCubeKickTimer(self, fromSpaceNo, toSpaceNo):
        _fromRoomType = self._getCubeRoomType(fromSpaceNo)
        _toRoomType = self._getCubeRoomType(toSpaceNo)
        if _fromRoomType == _toRoomType:
            return

        if self._isCubeRoomNeedKick(fromSpaceNo):
            self._cancelRoomKickTimer()
            self._cubeRoomKickCheckout(fromSpaceNo)

        if self._isCubeRoomNeedKick(toSpaceNo):
            self._cubeRoomSetEnterTime(toSpaceNo, utils.getNow())
            self._startRoomKickTimer(toSpaceNo)
            self._sendRoomKickLeftTime(toSpaceNo)

    def _sendRoomKickLeftTime(self, spaceNo):
        if not self._isCubeRoomNeedKick(spaceNo):
            return

        self._cubeRoomKickCheckout(spaceNo)

        _cubeType = self._getCubeRoomType(spaceNo)
        _useTime = self._getRoomUseTime(spaceNo)
        _maxTime = dataUtils.getCubeTypeMaxTime(_cubeType)
        _leftTime = max(0, _maxTime - _useTime)
        self.client.onCubeRoomKickLeftTime(utils.getNow() + _leftTime)

    def _isCubeRoomNeedKick(self, spaceNo):
        return self._getCubeRoomType(spaceNo) in gameconst.CubeRoomType.NeedKickTup

    def _getRoomUseTime(self, spaceNo):
        _cubeType = self._getCubeRoomType(spaceNo)
        _useTime, _enterTime = self.cubeRoomLeftTimeDic.get(_cubeType, (0, 0))
        return _useTime

    @utils.isMyself
    def getCubeKickLeftTime(self, exposed, cubeType, entityId, teleportId, lineNo):
        _useTime, _enterTime = self.cubeRoomLeftTimeDic.get(cubeType, (0, 0))
        _maxTime = dataUtils.getCubeTypeMaxTime(cubeType)
        self.client.onCubeKickLeftTime(max(0, _maxTime - _useTime), entityId, teleportId, lineNo)

    def _getRoomMaxTime(self, spaceNo):
        return dataUtils.getCubeTypeMaxTime(self._getCubeRoomType(spaceNo))

    def _startRoomKickTimer(self, spaceNo):
        if not self._isCubeRoomNeedKick(spaceNo):
            ERROR_MSG('cube room not need kick', spaceNo)
            return

        _useTime = self._getRoomUseTime(spaceNo)
        _maxTime = self._getRoomMaxTime(spaceNo)
        _leftTime = max(0, _maxTime - _useTime)
        _now = utils.getNow()

        _delay = min(10, _leftTime) # 最多10秒tick一次,保证使用次数一直在累积
        _fire = max(_now + 1, _now + _delay)
        self.cubeRoomKickTimerId = self._datetimeCallback(
            _fire,
            '_onRoomKickTimerFire',
            (spaceNo,),
            gametimer.TIMER_TAG_CUBE_ROOM_KICK,
            'cubeRoomKickTimerId'
        )

    def _onRoomKickTimerFire(self, spaceNo):
        if self.spaceNo != spaceNo:
            ERROR_MSG('_onRoomKickTimerFire ', self.spaceNo, spaceNo)
            return

        self._cubeRoomKickCheckout(spaceNo)

        _useTime = self._getRoomUseTime(spaceNo)
        _maxTime = self._getRoomMaxTime(spaceNo)
        _leftTime = max(0, _maxTime - _useTime)

        if _leftTime <= 0:
            self._doCubeRoomKick(spaceNo)

        else:
            self._startRoomKickTimer(spaceNo)

    def _doCubeRoomKick(self, spaceNo):
        _cubeType = self._getCubeRoomType(spaceNo)
        if _cubeType == gameconst.CubeRoomType.COW:
            self.backOriginRoomFromCow()

        elif _cubeType == gameconst.CubeRoomType.TIDE:
            self.showMsg(cube_config.datas['cube_crazyRoomTimeMsg']['value'], [])
            gameengine.getCubeStub(1).doEnterCubeReady(self.base, self.gbId, {})

    def _cancelRoomKickTimer(self):
        if self.cubeRoomKickTimerId:
            self._cancelDatetimeCallback(self.cubeRoomKickTimerId, gametimer.TIMER_TAG_CUBE_ROOM_KICK)
            self.cubeRoomKickTimerId = 0

    def resetCubeCowDur(self):
        self.cubeRoomLeftTimeDic = {}

        if self._isCubeRoomNeedKick(self.spaceNo):
            self._cubeRoomSetEnterTime(self.spaceNo, utils.getNow())
            self._sendRoomKickLeftTime(self.spaceNo)

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

        _needScore = cube_floor.datas[floor]['needScore']
        if self.getTotalScore() < _needScore:
            WARNING_MSG('ICubeCell::setEnterCubeFloor: need score: {}'.format(_needScore))
            return

        self.cubeEnterFloor = floor

    def _needTimerOn(self, spaceNo):
        if not formula.isCubeSpace(spaceNo):
            return False

        return not formula.isCubeReady(spaceNo)

    def _dealWithCubeTimer(self, fromSpaceNo, toSpaceNo):
        _fromNeed = self._needTimerOn(fromSpaceNo)
        _toNeed = self._needTimerOn(toSpaceNo)

        self.cubeQuota.refreshEnterTime()

        if not _toNeed:
            # 退出混沌回廊一定会走这里
            if self.cubeRoomTimerId:
                self._cancelDatetimeCallback(self.cubeRoomTimerId, gametimer.TIMER_TAG_CUBE_ROOM)
                self.cubeRoomTimerId = 0

            self.cubeQuota.checkout()

        else:
            self.cubeQuota.changeProtect()
            self._startCubeTimeOutTimer(gameconst.CUBE_CB_PROTECT)

    def _onCubeOffline(self):
        if self._needTimerOn(self.spaceNo):
            if self.cubeRoomTimerId:
                self._cancelDatetimeCallback(self.cubeRoomTimerId, gametimer.TIMER_TAG_CUBE_ROOM)
                self.cubeRoomTimerId = 0

            self.cubeQuota.checkout()

        if self._isCubeRoomNeedKick(self.spaceNo):
            self._cubeRoomKickCheckout(self.spaceNo)

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

        if self.cubeQuota.quotaDurState == gameconst.QuotaDurStatus.ENTER:
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
        #self.doRandomCubeRoom()
        pass

    def doRandomCubeRoom(self):
        if not formula.isCubeSpace(self.spaceNo):
            ERROR_MSG('randomCubeRoom but not in cube', self.spaceNo)
            return

        if not self.cubeEnterFloor:
            self.cubeEnterFloor = 1

        gameengine.getCubeStub(self.cubeEnterFloor).enterRandomRoom(
            self.base, 
            self.gbId, 
            {}, 
            self.spaceNo,
            self._genCubeRoomFilterTypes()
        )

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

        if dataUtils.isCubeCow(_mapId) and self._isCubeMapFullByMapId(_mapId):
            WARNING_MSG('map is full', _mapId)
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

    def _startCubeTimeOutTimer(self, cubeCBType):
        if self.cubeRoomTimerId:
            self._cancelDatetimeCallback(self.cubeRoomTimerId, gametimer.TIMER_TAG_CUBE_ROOM)

        _now = utils.getNow()
        _endTime = _now + self.cubeQuota.calcLeftTime()

        if cubeCBType == gameconst.CUBE_CB_PROTECT:
            _fireTime = _now + cube_config.datas['cube_transportProtection']['value']
        elif cubeCBType == gameconst.CUBE_CB_AUTO_RENEW:
            _fireTime = max(_now + 1, _endTime - 60)
        else:
            _fireTime = max(_now + 5, _endTime)

        DEBUG_MSG('next cube fire time', _fireTime)
        self.cubeRoomTimerId = self._datetimeCallback(
            _fireTime, 
            '_onCubeTimeOut', 
            (cubeCBType,), 
            gametimer.TIMER_TAG_CUBE_ROOM, 
            'cubeRoomTimerId')

    def _onCubeTimeOutRenew(self):
        if not formula.isCubeSpace(self.spaceNo):
            ERROR_MSG('_onCubeTimeOutRenew', self.spaceNo)
            return

        self._startCubeTimeOutTimer(gameconst.CUBE_CB_TIME_OUT)
        _switchVal = self.getTempMiscProp(gameconst.AvatarProps.cubeAutoRenewSwitch)
        if _switchVal is None:
            return

        if not _switchVal.canAddTimes():
            return

        if not self._checkAddCubeRoomDurationCondition():
            return

        _switchVal.addTimes()
        _ctx = actionContext.CubeDurCtx(self.base, True)
        self.base.autoRenewCubeRoom(_switchVal.toClientData(), _ctx)
        self.client.onCubeAutoRenewSwitch(True, _switchVal.toClientData())

    def _onCubeTimeOutProtect(self):
        if not formula.isCubeSpace(self.spaceNo):
            ERROR_MSG('_onCubeTimeOutProtect', self.spaceNo)
            return

        self.cubeQuota.setCubeEnterTime(self, utils.getNow())
        self._startCubeTimeOutTimer(gameconst.CUBE_CB_AUTO_RENEW)

    def _onCubeTimeOut(self, cubeCBType):
        INFO_MSG('ICubeCell::_onCubeTimeOut: {}, {}'.format(self.spaceNo, cubeCBType))
        if cubeCBType == gameconst.CUBE_CB_PROTECT:
            self._onCubeTimeOutProtect()

        elif cubeCBType == gameconst.CUBE_CB_AUTO_RENEW:
            self._onCubeTimeOutRenew()

        else:
            self.leaveCubeInternal(gameconst.DungeonSrcEnum.FROM_TIME_OUT)

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

    def checkAddCubeRoomDurationCondition(self, itemId, num, opUUID):
        if not self._checkAddCubeRoomDurationCondition():
            return

        self.base.useItemAddCubeTimes(itemId, num, True, True, gameconst.CubeAddTimesReason.CHECK_COND, opUUID)

    def directlyAddCubeRoomDuration(self, func, args, cubeDurCtx):
        if not self._checkAddCubeRoomDurationCondition():
            getattr(self.base, func)(*args)
            return

        _dur = cube_config.datas['cubeNumTime']['value'] * 60
        self.cubeQuota.addCubeLeftTime(self, _dur)
        self.base.activityComplete(cube_config.datas['cubeActID']['value'])
        self._startCubeTimeOutTimer(gameconst.CUBE_CB_AUTO_RENEW)

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
        self.client.onCubeLoginData(_time, _renewSwitch, _switchData, _rewardList, self.cubeQuota.quotaDurState)

    def onLogonEnterCubeCB(self, spaceMgrId):
        INFO_MSG('ICubeCell::onLogonEnterCubeCB: {}'.format(spaceMgrId))
        _dir = self._getEntranceDirByDungeonNo(formula.getMapId(self.spaceNo))
        self.position = self._getEntranceByDungeonNo(formula.getMapId(self.spaceNo))
        self.direction = (0, 0, _dir * math.pi / 180) if _dir is not None else self.direction
        self.spaceMgrId = spaceMgrId
        self.spaceMgr.onPlayerEnter(self.id)
        gameengine.getCubeStubBySpaceNo(self.spaceNo).onEnterCubeSuccess(self.gbId, self.spaceNo)

        if self._needTimerOn(self.spaceNo):
            ERROR_MSG('ICubeCell::onLogonEnterCubeCB: need timer on')

        if self._isCubeRoomNeedKick(self.spaceNo):
            self._startRoomKickTimer(self.spaceNo)
        

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

        if _switchVal.canAddTimes() and self._needTimerOn(self.spaceNo):
            self._startCubeTimeOutTimer(gameconst.CUBE_CB_AUTO_RENEW)

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
    # 擂主交互
    def _eventActionInteractArenaKing(self, *args, **kwargs):
        INFO_MSG('ICubeCell::_eventActionInteractArenaKing: {}'.format(args))
        if not formula.isCubeSpace(self.spaceNo):
            ERROR_MSG('ICubeCell::_eventActionInteractArenaKing: not cube space: {}'.format(self.spaceNo))
            return

        if self.spaceMgr.doInteractArenaKing(self):
            self.showMsg(cube_config.datas['cube_ringDefenderPresence2']['value'], [])
        else:
            self.showMsg(cube_config.datas['cube_ringDefenderPresence']['value'], [])

    @utils.isMyself
    @gamedecorator.limitcall(1)
    def switchCubeLine(self, exposed, lineNo):
        _cubeType = self._getCubeRoomType(self.spaceNo)
        if _cubeType != gameconst.CubeRoomType.READY:
            ERROR_MSG('ICubeCell::switchCubeLine: not ready room: {}'.format(self.spaceNo))
            return

        if formula.getLineNo(self.spaceNo) == lineNo:
            ERROR_MSG('ICubeCell::switchCubeLine: same line: {}'.format(self.spaceNo))
            return

        gameengine.getCubeStub(1).checkSwitchCubeLine(self.base, lineNo)

    def onCheckSwitchCubeLineResult(self, lineNo, canEnter):
        INFO_MSG('ICubeCell::onCheckSwitchCubeLineResult: {}'.format(canEnter))
        if not canEnter:
            self.showMsg(BDS.datas["Branch_fullCapacityMsg"]["value"], [])
            return

        self._commonNeedCast(
            CCD.datas.teleportCast,
            gameconst.State.Teleporting,
            gameconst.CastType.teleportAnchor,
            '_switchCubeLine',
            (lineNo,),
            castTime=CONST.datas['teleportTime'].get("value", gameconst.ANCHOR_CAST_DUR)
        )

    def _switchCubeLine(self, lineNo):
        INFO_MSG('ICubeCell::_switchCubeLine: {}'.format(lineNo))

        extra = {'enterCubeType': gameconst.ENTER_CUBE_SWITCH_LINE}
        gameengine.getCubeStub(1).doSwitchCubeLine(
            self.base, self.gbId, lineNo, extra)

    @utils.isMyself
    def getArenaKingPos(self, exposed):
        if not formula.isCubeSpace(self.spaceNo):
            WARNING_MSG('getArenaKingPos', self.spaceNo)
            return

        self.spaceMgr.doSendArenaKingPos(self)

