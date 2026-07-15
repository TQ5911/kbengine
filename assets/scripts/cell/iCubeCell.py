# coding: utf-8
import KBEngine
from KBEDebug import *


import math
import dataUtils
import random
import conflict_conflict_def as C_C_DD
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
        LOG_DBG('CubeSwitch::addTimes: {}'.format(self.curTimes))
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
            LOG_ERR('cube dur state invalid', self.cubeQuota)
            self.cubeQuota.resetOnLogin()

    def _getCubeRoomType(self, spaceNo):
        _mapId = formula.fetchMapId(spaceNo)
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
        LOG_DBG('[cube]_cubeRoomSetEnterTime', spaceNo, now, _useTime)

    def _cubeRoomKickCheckout(self, spaceNo):
        _cubeType = self._getCubeRoomType(spaceNo)
        _useTime, _enterTime = self.cubeRoomLeftTimeDic.get(_cubeType, (0, 0))
        _now = utils.curTS()
        if _now - _enterTime > gameconst.CUBE_ROOM_KICK_INTERVAL + 5:
            LOG_ERR('_cubeRoomKickCheckout _now - _enterTime > gameconst.CUBE_ROOM_KICK_INTERVAL + 5', _now, _enterTime)

        _useTime += _now - _enterTime
        self.cubeRoomLeftTimeDic[_cubeType] = (_useTime, _now)
        LOG_DBG('[cube]_cubeRoomKickCheckout', spaceNo, _useTime, _now)

    def _dealWithCubeKickTimer(self, fromSpaceNo, toSpaceNo):
        _fromRoomType = self._getCubeRoomType(fromSpaceNo)
        _toRoomType = self._getCubeRoomType(toSpaceNo)
        if _fromRoomType == _toRoomType:
            return

        if self._isCubeRoomNeedKick(fromSpaceNo):
            self._cancelRoomKickTimer()
            self._cubeRoomKickCheckout(fromSpaceNo)

        if self._isCubeRoomNeedKick(toSpaceNo):
            self._cubeRoomSetEnterTime(toSpaceNo, utils.curTS())
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
        self.client.onCubeRoomKickLeftTime(utils.curTS() + _leftTime)

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
            LOG_ERR('cube room not need kick', spaceNo)
            return

        _useTime = self._getRoomUseTime(spaceNo)
        _maxTime = self._getRoomMaxTime(spaceNo)
        _leftTime = max(0, _maxTime - _useTime)
        _now = utils.curTS()

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
            LOG_ERR('_onRoomKickTimerFire ', self.spaceNo, spaceNo)
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
            self._cubeRoomSetEnterTime(self.spaceNo, utils.curTS())
            self._sendRoomKickLeftTime(self.spaceNo)

    def _cancelCubeRoomTimer(self):
        if self.cubeRoomTimerId:
            self.cancelTimerCB(self.cubeRoomTimerId, gametimer.TIMER_TAG_CUBE_ROOM)
            self.cubeRoomTimerId = 0

    @gamedecorator.checkGameconfigEnable('square')
    @utils.isMyself
    def setEnterCubeFloor(self, exposed, floor):
        LOG_INFO('ICubeCell::setEnterCubeFloor: {}'.format(floor))
        if floor not in cube_floor.datas:
            LOG_ERR('ICubeCell::setEnterCubeFloor: floor not found: {}'.format(floor))
            return

        _mapId = formula.fetchMapId(self.spaceNo)
        _mapData = cube_room.datas.get(_mapId)
        if not _mapData:
            LOG_ERR('ICubeCell::setEnterCubeFloor: map not found: {}'.format(_mapId))
            return

        if _mapData['type'] != gameconst.CubeRoomType.READY:
            LOG_ERR('ICubeCell::setEnterCubeFloor: not ready room: {}'.format(_mapId))
            return

        if self.level < cube_floor.datas[floor]['needLv']:
            LOG_WARN('ICubeCell::setEnterCubeFloor: level < needLv: {} < {}'.format(self.level, cube_floor.datas[floor]['needLv']))
            return

        _needScore = cube_floor.datas[floor]['needScore']
        if self.getTotalScore() < _needScore:
            LOG_WARN('ICubeCell::setEnterCubeFloor: need score: {}'.format(_needScore))
            return

        self.cubeEnterFloor = floor

    def _needTimerOn(self, spaceNo):
        if not formula.inCubeScene(spaceNo):
            return False

        return not formula.inCubeReadyScene(spaceNo)

    def _dealWithCubeTimer(self, fromSpaceNo, toSpaceNo):
        _fromNeed = self._needTimerOn(fromSpaceNo)
        _toNeed = self._needTimerOn(toSpaceNo)

        self.cubeQuota.refreshEnterTime()

        if not _toNeed:
            # 退出混沌回廊一定会走这里
            self._cancelCubeRoomTimer()

            self.cubeQuota.checkout()

        else:
            self.cubeQuota.changeProtect()
            self._startCubeTimeOutTimer(gameconst.CUBE_CB_PROTECT)

    def _onCubeOffline(self):
        if self._needTimerOn(self.spaceNo):
            self._cancelCubeRoomTimer()

            self.cubeQuota.checkout()

        if self._isCubeRoomNeedKick(self.spaceNo):
            self._cubeRoomKickCheckout(self.spaceNo)

    @gamedecorator.checkGameconfigEnable('square')
    @utils.isMyself
    @gamedecorator.limitcall(1)
    def enterCube(self, exposed, floor):
        LOG_INFO('ICubeCell::enterCube', floor)
        self.enterCubeInternal()

    def enterCubeInternal(self):
        _floor = 1
        if not utils.isActOpen(cube_config.datas['cubeActID']['value']):
            self.showMsg(AC_CD.datas['activity_notOpen']['value'], [])
            return

        if formula.inCubeScene(self.spaceNo):
            LOG_WARN('enterCube but already in cube:', self.spaceNo)
            return

        # 这里直接选取大厅作为check能否进入的参考层
        _mapId = cube_room.floorTypeMapDic[_floor][gameconst.CubeRoomType.READY][0]
        _targetSpaceNo = formula.combineLineSpaceNo(_mapId, 0)
        if not utils.checkCanChangeSceneAndShowMsg(self, self.spaceNo, _targetSpaceNo):
            return

        if self.cubeQuota.quotaDurState == gameconst.QuotaDurStatus.ENTER:
            LOG_ERR('ICubeCell::enterCube: has entered')
            return

        if self.cubeQuota.leftTime <= 0:
            self.base.beforeEnterCubeDecrementCnt({'floor': _floor})
            return

        extra = {'enterCubeType': gameconst.ENTER_CUBE_HAS_LEFT_TIME, 'hasCast': False, 'floor': _floor}
        gameengine.getCubeStub(_floor).doEnterCubeReady(
            self.base, self.gbId, extra)

    @gamedecorator.checkGameconfigEnable('square')
    @utils.isMyself
    def randomCubeRoom(self, exposed):
        #self.doRandomCubeRoom()
        pass

    def doRandomCubeRoom(self):
        if not formula.inCubeScene(self.spaceNo):
            LOG_ERR('randomCubeRoom but not in cube', self.spaceNo)
            return

        if self.cubeQuota.calcLeftTime() <= 0:
            LOG_WARN('randomCubeRoom but no left time', self.spaceNo)
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

    def enterCubeByFloorConfig(self, signType=gameconst.CUBE_SIGN_ARENA):
        LOG_INFO('ICubeCell::enterCubeByFloorConfig: {}, {}'.format(self.cubeEnterFloor, signType))
        if not self.cubeEnterFloor:
            self.cubeEnterFloor = 1

        _mapIds = cube_room.floor2SignMapIds[self.cubeEnterFloor][signType]
        extra = {'hasCast': False}
        self.enterCubeByMapIds(_mapIds, extra)

    def backOriginRoomFromCow(self):
        LOG_INFO('ICubeCell::backOriginRoomFromCow: {}'.format(self.spaceNo))
        self.enterCubeByMapIds([self.fromCubeMapId])

    def enterCubeByMapIds(self, mapIds, extra={}):
        LOG_INFO('ICubeCell::enterCubeByMapIds: {}, {}'.format(mapIds, extra))
        _mapIds = []
        _someScore = 0
        _someLv = 0
        for _mapId in mapIds:
            if _mapId not in cube_room.datas:
                LOG_ERR('ICubeCell::enterCubeByMapIds: map not found: {}'.format(_mapId))
                continue

            _floor = cube_room.datas[_mapId]['floor']
            _needScore = cube_floor.datas[_floor]['needScore']
            _needLv = cube_floor.datas[_floor]['needLv']
            if self.getTotalScore() < _needScore:
                _someScore = _needScore
                continue
            if self.level < _needLv:
                _someLv = _needLv
                continue

            _mapIds.append(_mapId)

        if not _mapIds:
            if _someScore:
                self.showMsg(cube_config.datas['cube_floorJudge']['value'], [str(_someScore)])
            elif _someLv:
                self.showMsg(cube_config.datas['cube_floorJudge2']['value'], [str(_someLv)])
            return

        _mapId = random.choice(mapIds)

        if dataUtils.isCubeCow(_mapId) and self._isCubeMapFullByMapId(_mapId):
            LOG_WARN('map is full', _mapId)
            return

        _floor = cube_room.datas[_mapId]['floor']
        gameengine.getCubeStub(_floor).doEnterCube(
            self.base, _mapId, self.gbId, extra)

    @gamedecorator.checkGameconfigEnable('square')
    @utils.isMyself
    def followCaptainInCube(self, exposed):
        LOG_INFO('ICubeCell::followCaptainInCube: {}'.format(self.spaceNo))
        return
        if not formula.inCubeScene(self.spaceNo):
            LOG_ERR('ICubeCell::followCaptainInCube: not cube space: {}'.format(self.spaceNo))
            return

        _spaceNo = self.getCaptainSpaceNo()
        _pos = self.getCaptainPosition()
        if not (_spaceNo and _pos):
            LOG_WARN('ICubeCell::followCaptainInCube: captain not found', _spaceNo, _pos)
            return

        if not formula.inCubeScene(_spaceNo):
            LOG_WARN('ICubeCell::followCaptainInCube: captain not in cube space', _spaceNo, _pos)
            return

        _mapId = formula.fetchMapId(_spaceNo)
        gameengine.getCubeStubBySpaceNo(_spaceNo).doEnterCube(
            self.base, _mapId, self.gbId, {'followPos': _pos, 'hasCast': False})

    def gmEnterCubeRoom(self, mapId):
        _targetFloor = dataUtils.getCubeFloor(mapId)
        gameengine.getCubeStub(_targetFloor).doEnterCube(self.base, mapId, self.gbId, {})
        return True

    @utils.isMyself
    def leaveCube(self, exposed):
        self.leaveCubeInternal(gameconst.DunSrcEnum.FROM_CLIENT, False)

    def leaveCubeInternal(self, srcId, hasCast=True):
        if not formula.inCubeScene(self.spaceNo):
            LOG_INFO('leaveCubeInternal but not cube space: {}'.format(self.spaceNo))
            return

        _src = dungeonSrc.BasicDungeonSrc(srcId=srcId)
        _l = {}
        _context = {
            'e': {},
            'l': _l,
            'src': _src,
            'hasCast': hasCast,
        }

        _canLeave = self.packComplexTeleportLeaveData(_l)
        if not _canLeave:
            LOG_WARN('ICubeCell::leaveCube: can not leave')
            return

        _, _mOutsideRecord = self.tryGetLastTeleportOutesideRecord(self.spaceNo, spaceType=formula.getSpaceType(self.spaceNo))
        _spaceNo = _mOutsideRecord.spaceNo if _mOutsideRecord else formula.combineLineSpaceNo(gameconst.MapIdDef.mapXinYuanCheng)

        _options = complexTeleportOption.ComplexTeleportOpt(teleportType=gameconst.ComplexTeleportEnum.LEAVE)
        self.doLeaveFromSapceToSpace(self.spaceNo, _spaceNo, _options, _context)

    def beginEnterCubeRoom(self, spaceBox, spaceMgrCellId, spaceNo, extra):
        _lContext = {}
        _src = dungeonSrc.BasicDungeonSrc()
        hasCast = extra.get('hasCast', True)
        _context = {
            'e': {
                'spaceBox': spaceBox,
                'spaceMgrId': spaceMgrCellId,
            },
            'l': _lContext,
            'src': _src,
            'hasCast': hasCast,
            'cube': extra,
            'hasCheck': extra.get('hasCheck', False)
        }
        _options = complexTeleportOption.ComplexTeleportOpt(teleportType=gameconst.ComplexTeleportEnum.ENTER)

        canLeave = self.packComplexTeleportLeaveData(_lContext)
        if not canLeave:
            LOG_WARN('ICubeCell::beginEnterCubeRoom: can not leave')
            return

        self.telFromSpaceToSpace(self.spaceNo, spaceNo, options=_options, context=_context, failedFunc='enterCubeRoomFailed', failedArgs=(self.spaceNo, spaceNo, ))

    def enterCubeRoomFailed(self, fromSpaceNo, toSpaceNo):
        LOG_DBG("ICubeCell::enterCubeRoomFailed", fromSpaceNo, toSpaceNo)
        gameengine.getCubeStubBySpaceNo(toSpaceNo).onLeaveCube(self.gbId, toSpaceNo, fromSpaceNo)

    def _startCubeTimeOutTimer(self, cubeCBType):
        self._cancelCubeRoomTimer()

        leftTime = self.cubeQuota.calcLeftTime()

        if cubeCBType == gameconst.CUBE_CB_PROTECT:
            _fireTime = cube_config.datas['cube_transportProtection']['value']
        elif cubeCBType == gameconst.CUBE_CB_AUTO_RENEW:
            cdpTime = cube_config.datas['cubeCountdownPrompt']['value']
            diffTime = leftTime - cdpTime if leftTime >= cdpTime else 0
            _fireTime = max(1, diffTime)
        else:
            _fireTime = max(1, leftTime)

        LOG_DBG('next cube fire time', _fireTime)
        self.cubeRoomTimerId = self.addTimerCB(
            _fireTime, 
            '_onCubeTimeOut', 
            (cubeCBType,), 
            gametimer.TIMER_TAG_CUBE_ROOM, 
            'cubeRoomTimerId')

    def _onCubeTimeOutRenew(self):
        if not formula.inCubeScene(self.spaceNo):
            LOG_ERR('_onCubeTimeOutRenew', self.spaceNo)
            return

        self._startCubeTimeOutTimer(gameconst.CUBE_CB_TIME_OUT)
        _switchVal = self.getTempMiscProp(gameconst.EntityPropsEnum.cubeAutoRenewSwitch)
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
        if not formula.inCubeScene(self.spaceNo):
            LOG_ERR('_onCubeTimeOutProtect', self.spaceNo)
            return

        self.cubeQuota.setCubeEnterTime(self, utils.curTS())
        self._startCubeTimeOutTimer(gameconst.CUBE_CB_AUTO_RENEW)

    def _onCubeTimeOut(self, cubeCBType):
        LOG_INFO('ICubeCell::_onCubeTimeOut: {}, {}'.format(self.spaceNo, cubeCBType))
        if cubeCBType == gameconst.CUBE_CB_PROTECT:
            self._onCubeTimeOutProtect()

        elif cubeCBType == gameconst.CUBE_CB_AUTO_RENEW:
            self._onCubeTimeOutRenew()

        else:
            self.leaveCubeInternal(gameconst.DunSrcEnum.FROM_TIME_OUT, True)

    def _checkAddCubeRoomDurationCondition(self):
        _curMapId = formula.fetchMapId(self.spaceNo)
        _curFloor = dataUtils.getCubeFloor(_curMapId)
        if not _curFloor:
            LOG_WARN('ICubeCell::checkAddCubeRoomDurationCondition: floor not found: {}'.format(_curMapId))
            return False

        if self.cubeQuota.calcLeftTime() > cube_config.datas['cubeNumTime']['value'] * 60:
            LOG_WARN('ICubeCell::checkAddCubeRoomDurationCondition: duration beyond max')
            return False

        return True

    def checkAddCubeRoomDurationCondition(self, addType, itemId, itemNum, num, opUUID):
        if not self._checkAddCubeRoomDurationCondition():
            return

        self.base.useItemAddCubeTimes(addType, itemId, itemNum, num, True, True, gameconst.CubeAddTimesReason.CHECK_COND, opUUID)

    def directlyAddCubeRoomDuration(self, func, args, cubeDurCtx):
        if not self._checkAddCubeRoomDurationCondition():
            getattr(self.base, func)(*args)
            return

        _dur = cube_config.datas['cubeNumTime']['value'] * 60
        self.cubeQuota.addCubeLeftTime(self, _dur)
        self.base.activityComplete(cube_config.datas['cubeActID']['value'])
        if self.cubeQuota.quotaDurState != gameconst.QuotaDurStatus.PROTECT:
            self._startCubeTimeOutTimer(gameconst.CUBE_CB_AUTO_RENEW)

    def addCubeRoomRewardRecord(self, rewardList):
        _dic = self.getTempMiscProp(gameconst.EntityPropsEnum.cubeRoomRewardList, {})
        for _data in rewardList:
            _itemId = _data['itemId']
            _bindType = _data['bindType']
            _dic.setdefault(_itemId, {})
            _dic[_itemId][_bindType] = _dic[_itemId].get(_bindType, 0) + _data['itemNum']

        self.setTempMiscProp(gameconst.EntityPropsEnum.cubeRoomRewardList, _dic)
        self.client.onAddCubeRoomRewardRecord(rewardList)

    def clearCubeRoomRewardRecord(self):
        self.popTempMiscProp(gameconst.EntityPropsEnum.cubeRoomRewardList)

    def toClientCubeLoginData(self):
        if not formula.inCubeScene(self.spaceNo):
            return

        _rewardList = []
        for k, v in self.getTempMiscProp(gameconst.EntityPropsEnum.cubeRoomRewardList, {}).items():
            for _bindType, _num in v.items():
                _rewardList.append({'itemId': k, 'itemNum': _num, 'bindType': _bindType})

        _switchVal = self.getTempMiscProp(gameconst.EntityPropsEnum.cubeAutoRenewSwitch)
        if _switchVal is None:
            _renewSwitch = False
            _switchData = CubeSwitch().toClientData()
        else:
            _renewSwitch = True
            _switchData = _switchVal.toClientData()

        _time = self.cubeQuota.calcLeftTime() + utils.curTS()
        self.client.onCubeLoginData(_time, _renewSwitch, _switchData, _rewardList, self.cubeQuota.quotaDurState)

    def onLogonEnterCubeCB(self, spaceMgrId):
        LOG_INFO('ICubeCell::onLogonEnterCubeCB: {}'.format(spaceMgrId))
        _dir = self._getEntranceDirByDungeonNo(formula.fetchMapId(self.spaceNo))
        self.position = self._getEntranceByDungeonNo(formula.fetchMapId(self.spaceNo))
        self.direction = (0, 0, _dir * math.pi / 180) if _dir is not None else self.direction
        self.spaceMgrId = spaceMgrId
        self.spaceMgr.onPlayerEnter(self.id)
        gameengine.getCubeStubBySpaceNo(self.spaceNo).onEnterCubeSuccess(self.gbId, self.spaceNo)

        if self._needTimerOn(self.spaceNo):
            LOG_ERR('ICubeCell::onLogonEnterCubeCB: need timer on')

        if self._isCubeRoomNeedKick(self.spaceNo):
            self._startRoomKickTimer(self.spaceNo)
        
    def directlyOutOfProtect(self):
        LOG_DBG("directlyOutOfProtect", self.cubeQuota.quotaDurState)
        if self.cubeQuota.quotaDurState != gameconst.QuotaDurStatus.PROTECT:
            return

        self._onCubeTimeOutProtect()

    # ------------------------ props start ------------------------
    @utils.isMyself
    def reqChangeCubeAutoRenewSwitch(self, exposed, masterSwitch, switchData):
        LOG_INFO('ICubeCell::reqChangeCubeAutoRenewSwitch: {} {}'.format(masterSwitch, switchData))
        if masterSwitch and not utils.isActOpen(cube_config.datas['cubeActID']['value']):
            LOG_INFO('ICubeCell::reqChangeCubeAutoRenewSwitch: cubeActID not open')
            return

        self._changeCubeAutoRenewSwitch(masterSwitch, switchData)

    def _changeCubeAutoRenewSwitch(self, masterSwitch, switchData):
        if not masterSwitch:
            self.popTempMiscProp(gameconst.EntityPropsEnum.cubeAutoRenewSwitch)
            self.client.onCubeAutoRenewSwitch(False, CubeSwitch().toClientData())
            return

        _switchVal = CubeSwitch(**switchData)
        self.setTempMiscProp(gameconst.EntityPropsEnum.cubeAutoRenewSwitch, _switchVal)
        self.client.onCubeAutoRenewSwitch(True, switchData)

        if _switchVal.canAddTimes() and self._needTimerOn(self.spaceNo):
            if self.cubeQuota.quotaDurState != gameconst.QuotaDurStatus.PROTECT:
                self._startCubeTimeOutTimer(gameconst.CUBE_CB_AUTO_RENEW)

    @property
    def cubeRandRoomCD(self):
        return self.getTempMiscProp(gameconst.EntityPropsEnum.cubeRandRoomCD, 0)

    @cubeRandRoomCD.setter
    def cubeRandRoomCD(self, val):
        if not val:
            self.popTempMiscProp(gameconst.EntityPropsEnum.cubeRandRoomCD)
        else:
            self.setTempMiscProp(gameconst.EntityPropsEnum.cubeRandRoomCD, val)

    @utils.isMyself
    def getCubeRoomLeftTime(self, exposed):
        leftTime = self.cubeQuota.calcLeftTime()
        LOG_INFO('ICubeCell::getCubeRoomLeftTime', self.cubeQuota.leftTime, leftTime)
        self.client.onCubeRoomLeftTime(leftTime)

    # ------------------------ props end ------------------------

    # ----------------------- 祈福之间 start ---------------------

    # ----------------------- 祈福之间 end ---------------------
    # 擂主交互
    def _eventActionInteractArenaKing(self, *args, **kwargs):
        LOG_INFO('ICubeCell::_eventActionInteractArenaKing: {}'.format(args))
        if not formula.inCubeScene(self.spaceNo):
            LOG_ERR('ICubeCell::_eventActionInteractArenaKing: not cube space: {}'.format(self.spaceNo))
            return

        if self.spaceMgr.doInteractArenaKing(self):
            self.showMsg(cube_config.datas['cube_ringDefenderPresence2']['value'], [])
        else:
            self.showMsg(cube_config.datas['cube_ringDefenderPresence']['value'], [])

    @utils.isMyself
    @gamedecorator.limitcall(1)
    def switchCubeLine(self, exposed, lineNo):
        LOG_INFO("switchCubeLine::", self.spaceNo, lineNo)
        if formula.parseLineNo(self.spaceNo) == lineNo:
            LOG_ERR('ICubeCell::switchCubeLine: same line: {}'.format(self.spaceNo))
            return

        #大厅支持选择分线，在房间中切换分线策划需求回到大厅
        _mapId = formula.fetchMapId(self.spaceNo)
        if _mapId == cube_config.datas['cube_hall']['value']:
            _floor = cube_room.datas[_mapId]['floor']
            gameengine.getCubeStub(_floor).checkSwitchCubeLine(self.base, lineNo, _mapId)
        else:
            self._commonNeedCast(
                C_C_DD.datas.teleportCast,
                gameconst.StateEnum.Teleporting,
                gameconst.CastEnum.teleportAnchor,
                '_switchCubeHall',
                (),
                castTime=CONST.datas['teleportTime'].get("value", gameconst.ANCHOR_CAST_DUR)
            )

    def _switchCubeHall(self):
        gameengine.getCubeStub(1).doEnterCubeReady(self.base, self.gbId, {})

    def onCheckSwitchCubeLineResult(self, lineNo, canEnter):
        LOG_INFO('ICubeCell::onCheckSwitchCubeLineResult: {}'.format(canEnter))
        if not canEnter:
            self.showMsg(BDS.datas["Branch_fullCapacityMsg"]["value"], [])
            return

        self._commonNeedCast(
            C_C_DD.datas.teleportCast,
            gameconst.StateEnum.Teleporting,
            gameconst.CastEnum.teleportAnchor,
            '_switchCubeLine',
            (lineNo,),
            castTime=CONST.datas['teleportTime'].get("value", gameconst.ANCHOR_CAST_DUR)
        )

    def _switchCubeLine(self, lineNo, extra={}):
        LOG_INFO('ICubeCell::_switchCubeLine: {}'.format(lineNo))

        extra['enterCubeType'] = gameconst.ENTER_CUBE_SWITCH_LINE
        _mapId = formula.fetchMapId(self.spaceNo)
        _floor = cube_room.datas[_mapId]['floor']
        gameengine.getCubeStub(_floor).doSwitchCubeLine(
            self.base, self.gbId, lineNo, extra, _mapId)

    @utils.isMyself
    def getArenaKingPos(self, exposed):
        if not formula.inCubeScene(self.spaceNo):
            LOG_WARN('getArenaKingPos', self.spaceNo)
            return

        self.spaceMgr.doSendArenaKingPos(self)

