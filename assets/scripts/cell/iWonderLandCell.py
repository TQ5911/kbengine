# coding: utf-8
from KBEDebug import *

import KBEngine

import utils
import math
import gameconst
import complexTeleportOption
import dungeonSrc
import formula
import gameengine
import gamedecorator
import gametimer
import CollectionCheckContext

import wonderLand_floor as WL_FD
import wonderLand_config as WL_CD
import creep_base as CBD
import activityControl_config as AC_CD

class WonderLandSwitch(object):
    def __init__(self, coinSwitch=False, itemSwitch=False, times=0):
        self.coinSwitch = coinSwitch
        self.itemSwitch = itemSwitch
        self.times = times
        self.curTimes = 0

    def leftTimes(self):
        return max(0, self.times - self.curTimes)

    def canAddTimes(self):
        return self.curTimes < self.times

    def addTimes(self):
        DEBUG_MSG('WonderLandSwitch::addTimes: {}'.format(self.curTimes))
        self.curTimes += 1

    def toClientData(self):
        return {
            'coinSwitch': self.coinSwitch,
            'itemSwitch': self.itemSwitch,
            'times': max(0, self.times - self.curTimes),
        }



class IWonderLandCell(object):
    def __init__(self):
        pass

    @utils.isMyself
    @gamedecorator.limitcall(1)
    def enterWonderLand(self, exposed, floor):
        if not utils.isActOpen(WL_CD.datas['wonderLandActID']['value']):
            self.showMsg(AC_CD.datas['activity_notOpen']['value'], [])
            return

        if self.totalScore < WL_FD.datas[floor]['needScore']:
            ERROR_MSG('IWonderLandCell::enterWonderLand: totalScore < needScore: {} < {}'.format(self.totalScore, WL_FD.datas[floor]['needScore']))
            return

        mapId = WL_FD.datas[floor]['ID']
        _targetSpaceNo = formula.getLineSpaceNo(mapId, 0)

        if not utils.checkCanChangeSceneAndShowMsg(self, self.spaceNo, _targetSpaceNo):
            return

        self.base.checkAndEnterWonderLand(floor)

    def beginEnterWonderLand(self, spaceBox, spaceMgrBoxCellId, spaceNo, extra):
        _lContext = {}
        _src = dungeonSrc.BasicDungeonSrc()
        _context = {
            'e': {
                'spaceBox': spaceBox,
                'spaceMgrId': spaceMgrBoxCellId,
            },
            'l': _lContext,
            'src': _src,
            'hasCast': True,
        }

        _options = complexTeleportOption.ComplexTeleportOptions(teleportType=gameconst.ComplexTeleportType.ENTER)

        canLeave = self.packageComplexTeleportLeaveData(_lContext)
        if not canLeave:
            WARNING_MSG('IWonderLandCell::beginEnterWonderLand: can not leave')
            return

        self.teleportFromSpaceToSpace(self.spaceNo, spaceNo, options=_options, context=_context)

    @utils.isMyself
    @gamedecorator.limitcall(1)
    def leaveWonderLand(self, exposed):
        if not formula.isWonderLandSpace(self.spaceNo):
            WARNING_MSG('IWonderLandCell::leaveWonderLand: spaceNo not line: {}'.format(self.spaceNo))
            return

        self._leaveWonderLand(gameconst.DungeonSrcEnum.FROM_CLIENT)

    def _leaveWonderLand(self, srcId):
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
            WARNING_MSG('IWonderLandCell::leaveWonderLand: can not leave')
            return

        _, _m_outsideRecord = self.tryGetLastTeleportOutesideRecord(self.spaceNo, spaceType=formula.whatSpaceType(self.spaceNo))
        _spaceNo = _m_outsideRecord.spaceNo if _m_outsideRecord else formula.getLineSpaceNo(gameconst.MapIdDef.mapXinYuanCheng)

        _options = complexTeleportOption.ComplexTeleportOptions(teleportType=gameconst.ComplexTeleportType.LEAVE)
        self.doLeaveFromSapceToSpace(self.spaceNo, _spaceNo, _options, _context)

    def _startWonderLandTimerOnEnter(self):
        _endTime = WL_CD.datas['wonderLandNumTime']['value'] * 60 + utils.getNow()
        self.setWonderLandLeftTime(_endTime)
        self._startWonderLandRenewTimer()

    def afterLeaveWonderLand(self):
        if self.getTempMiscProp(gameconst.AvatarProps.wonderLandSwitch):
            self._changeWonderLandSwitch(False, {})

        self.setWonderLandLeftTime(0)
        if self.wonderLandTimerId:
            self._cancelDatetimeCallback(self.wonderLandTimerId, gametimer.TIMER_TAG_WONDER_LAND)

        self.clearWonderLandRewardRecord()

    def summonWonderLandBoss(self, itemId, gid, collectionId):
        _bossId = self.getMonsterIdFromGID(gid)
        if self.spaceMgr.checkHasBoss(_bossId):
            self.showMsg(WL_CD.datas['wonderLand_bossAlive']['value'], [])
            return

        self.base.summonWonderLandBossBase(gid, itemId, collectionId)

    def summonWonderLandBossFromBase(self, gid, itemId, collectionId, opUUID):
        _mapId = formula.getMapId(self.spaceNo)
        _dunData = utils.getDunModuleData(_mapId)
        if not _dunData:
            ERROR_MSG('IWonderLandCell::summonWonderLandBossFromBase: not found dunData', self.spaceNo)
            return

        _monData = _dunData.get(str(gid))
        if not _monData:
            ERROR_MSG('IWonderLandCell::summonWonderLandBossFromBase: not found monData', gid)
            return

        if self.spaceMgr.checkHasBoss(_monData.get('EntityID')):
            self.showMsg(WL_CD.datas['wonderLand_bossAlive']['value'], [])
            self.base.summonWonderLandBossBaseFailed(opUUID, itemId)
            return

        _bossId = _monData.get('EntityID')
        _pos = (_monData['PosX'], _monData['PosY'], _monData['PosZ'])
        _dir = (0.0, 0.0, _monData['Dir'] * math.pi / 180)
        params = {
            'position': _pos,
            'direction': _dir,
            'spaceNo': self.spaceNo,
            'spaceno': self.spaceNo,
            'monsterId': _bossId,
            'level': int(_monData['Props']['Level']),
            'spaceMgrId': self.spaceMgrId,
            'instanceId': _monData['ID'],
        }

        self.spaceMgr.setCollToBoss(collectionId, _bossId)
        KBEngine.createEntity('Monster', self.spaceID, _pos, _dir, params)
        _bossName = CBD.datas[_bossId]['name']
        _msgId = utils.getNeedTranslateMsgId(WL_CD.datas['wonderLand_fixedBossAppear']['value'])
        _args = [utils.getNeedTranslateArg(_bossName)]
        self.spaceMgr.syncPlayer(lambda playerEnt: playerEnt.showMsg(_msgId, _args))

    def getMonsterIdFromGID(self, gid):
        _mapId = formula.getMapId(self.spaceNo)
        _dunData = utils.getDunModuleData(_mapId)
        if not _dunData:
            ERROR_MSG('IWonderLandCell::getMonsterIdFromGID: not found dunData', self.spaceNo)
            return

        _monData = _dunData.get(str(gid))
        if not _monData:
            ERROR_MSG('IWonderLandCell::getMonsterIdFromGID: not found monData', gid)
            return

        return _monData.get('EntityID')

    def checkSummonWonderLandBoss(self, itemId, gid, collectionId):
        _bossId = self.getMonsterIdFromGID(gid)
        return CollectionCheckContext.CollectionCheckWonderLand(itemId, _bossId, collectionId)

    def checkSummonWonderLandBossCell(self, bossId):
        _hasBoss = self.spaceMgr.checkHasBoss(bossId)
        if _hasBoss:
            self.showMsg(WL_CD.datas['wonderLand_bossAlive']['value'], [])

        return not _hasBoss

    @utils.isMyself
    def reqChangeWonderLandSwitch(self, exposed, masterSwitch, switchData):
        INFO_MSG('IWonderLandCell::reqChangeWonderLandSwitch: {} {}'.format(masterSwitch, switchData))
        if masterSwitch and not utils.isActOpen(WL_CD.datas['wonderLandActID']['value']):
            self.showMsg(AC_CD.datas['activity_notOpen']['value'], [])
            return

        self._changeWonderLandSwitch(masterSwitch, switchData)

    def _changeWonderLandSwitch(self, masterSwitch, switchData):
        if not masterSwitch:
            self.popTempMiscProp(gameconst.AvatarProps.wonderLandSwitch)
            self.client.onWonderLandSwitch(False, WonderLandSwitch().toClientData())
            return

        _switchVal = WonderLandSwitch(**switchData)
        self.setTempMiscProp(gameconst.AvatarProps.wonderLandSwitch, _switchVal)
        self.client.onWonderLandSwitch(True, switchData)

        if self.wonderLandDurStatus == gameconst.RenewDurStatus.WAIT_END:
            self._startWonderLandRenewTimer()

    def _startWonderLandRenewTimer(self):
        if self.wonderLandTimerId:
            self._cancelDatetimeCallback(self.wonderLandTimerId, gametimer.TIMER_TAG_WONDER_LAND)

        _fireTime = self.wonderLandLeftTime - 60
        _fireTime = max(utils.getNow() + 1, _fireTime)
        self.wonderLandTimerId = self._datetimeCallback(_fireTime, 'wonderLandRenewCB', (), gametimer.TIMER_TAG_WONDER_LAND, 'wonderLandTimerId')
        self.wonderLandDurStatus = gameconst.RenewDurStatus.WAIT_AUTO

    def wonderLandRenewCB(self):
        INFO_MSG('IWonderLandCell::wonderLandRenewCB: {}'.format(self.spaceNo))
        if not formula.isWonderLandSpace(self.spaceNo):
            return

        _fireTime = max(utils.getNow() + 5, self.wonderLandLeftTime)
        self.wonderLandTimerId = self._datetimeCallback(_fireTime, 'wonderLandEndTimeCB', (), gametimer.TIMER_TAG_WONDER_LAND, 'wonderLandTimerId')
        self.wonderLandDurStatus = gameconst.RenewDurStatus.WAIT_END
        _switchVal = self.getTempMiscProp(gameconst.AvatarProps.wonderLandSwitch)

        if _switchVal is None:
            return

        if not _switchVal.canAddTimes():
            return

        if not self._checkAddWonderLandDurationCondition():
            return

        _switchVal.addTimes()
        self.base.autoRenewWonderLand(_switchVal.toClientData())
        self.client.onWonderLandSwitch(True, _switchVal.toClientData())
        self.client.onChangeWonderLandRenewTimes(_switchVal.leftTimes())

    def wonderLandEndTimeCB(self):
        if not formula.isWonderLandSpace(self.spaceNo):
            return

        INFO_MSG('IWonderLandCell::wonderLandEndTimeCB: {}'.format(self.spaceNo))
        self._leaveWonderLand(gameconst.DungeonSrcEnum.FROM_TIME_OUT)
        self.wonderLandDurStatus = 0

    def _checkAddWonderLandDurationCondition(self):
        if not formula.isWonderLandSpace(self.spaceNo):
            WARNING_MSG('IWonderLandCell::checkAddWonderLandDurationCondition: spaceNo not wonderLand: {}'.format(self.spaceNo))
            return False

        if self.wonderLandLeftTime - utils.getNow() > WL_CD.datas['wonderLandNumTime']['value'] * 60:
            WARNING_MSG('IWonderLandCell::checkAddWonderLandDurationCondition: duration beyond max', self.wonderLandLeftTime)
            return False

        return True

    @property
    def wonderLandDurStatus(self):
        return self.getTempMiscProp(gameconst.AvatarProps.wonderLandDurStatus, 0)

    @wonderLandDurStatus.setter
    def wonderLandDurStatus(self, val):
        if not val:
            self.popTempMiscProp(gameconst.AvatarProps.wonderLandDurStatus)
        else:
            self.setTempMiscProp(gameconst.AvatarProps.wonderLandDurStatus, val)

    def directlyAddWonderLandDuration(self, func, args):
        if not self._checkAddWonderLandDurationCondition():
            getattr(self.base, func)(*args)
            return

        _dur = WL_CD.datas['wonderLandNumTime']['value'] * 60
        _now = utils.getNow()
        self.setWonderLandLeftTime(max(self.wonderLandLeftTime, _now) + _dur)
        self.base.activityComplete(WL_CD.datas['wonderLandActID']['value'])
        self._startWonderLandRenewTimer()


    def checkAddWonderLandDurationCondition(self, itemId, num):
        if not self._checkAddWonderLandDurationCondition():
            return

        self.base.doAddWonderLandTicket(itemId, num, True, True, gameconst.WonderAddTicketReason.CHECK_COND)

    def addWonderLandRewardRecord(self, rewardList):
        _dic = self.getTempMiscProp(gameconst.AvatarProps.wonderLandRewardList, {})
        for _data in rewardList:
            _itemId = _data['itemId']
            _bindType = _data['bindType']
            _dic.setdefault(_itemId, {})
            _dic[_itemId][_bindType] = _dic[_itemId].get(_bindType, 0) + _data['itemNum']

        self.setTempMiscProp(gameconst.AvatarProps.wonderLandRewardList, _dic)
        self.client.onAddWonderLandRewardRecord(rewardList)

    def clearWonderLandRewardRecord(self):
        self.popTempMiscProp(gameconst.AvatarProps.wonderLandRewardList)

    def doSendWonderLandLoginData(self):
        if not formula.isWonderLandSpace(self.spaceNo):
            return

        _rewardList = []
        for k, v in self.getTempMiscProp(gameconst.AvatarProps.wonderLandRewardList, {}).items():
            for _bindType, _num in v.items():
                _rewardList.append({'itemId': k, 'itemNum': _num, 'bindType': _bindType})

        _switchVal = self.getTempMiscProp(gameconst.AvatarProps.wonderLandSwitch)
        if _switchVal is None:
            _masterSwitch = False
            _switchData = WonderLandSwitch().toClientData()
        else:
            _masterSwitch = True
            _switchData = _switchVal.toClientData()

        self.client.onWonderLandLoginData(self.wonderLandLeftTime, _masterSwitch, _switchData, _rewardList)

    def onLogonEnterWonderLandCB(self, spaceMgrBoxCellId):
        self.spaceMgrId = spaceMgrBoxCellId
        self.spaceMgr.onPlayerEnter(self.id)

        gameengine.getWonderLandStubBySpaceNo(self.spaceNo).onEnterWonderLandSuccess(self.gbId, self.spaceNo)
        self._startWonderLandRenewTimer()

    def setWonderLandLeftTime(self, leftTime):
        self.wonderLandLeftTime = leftTime
        self.client.onWonderLandLeftTime(leftTime)
