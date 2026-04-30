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
        LOG_DBG('WonderLandSwitch::addTimes: {}'.format(self.curTimes))
        self.curTimes += 1

    def toClientData(self):
        return {
            'coinSwitch': self.coinSwitch,
            'itemSwitch': self.itemSwitch,
            'times': max(0, self.times - self.curTimes),
        }



class IWonderLandCell(object):
    def __init__(self):
        if self.wonderLandQuota.quotaDurState == gameconst.QuotaDurStatus.ENTER:
            LOG_ERR('IWonderLandCell::init: wonderLandQuota.quotaDurState == gameconst.QuotaDurStatus.ENTER')
            self.wonderLandQuota.resetOnLogin()

    @utils.isMyself
    @gamedecorator.limitcall(1)
    @gamedecorator.checkGameconfigEnable('wonderLand')
    def enterWonderLand(self, exposed, floor):
        if not utils.isActOpen(WL_CD.datas['wonderLandActID']['value']):
            self.showMsg(AC_CD.datas['activity_notOpen']['value'], [])
            return

        if self.level < WL_FD.datas[floor]['needLv']:
            LOG_ERR('IWonderLandCell::enterWonderLand: level < needLv: {} < {}'.format(self.level, WL_FD.datas[floor]['needLv']))
            return

        if self.totalScore < WL_FD.datas[floor]['needScore']:
            LOG_ERR('IWonderLandCell::enterWonderLand: totalScore < needScore: {} < {}'.format(self.totalScore, WL_FD.datas[floor]['needScore']))
            return

        mapId = WL_FD.datas[floor]['ID']
        _targetSpaceNo = formula.combineLineSpaceNo(mapId, 0)

        if not utils.checkCanChangeSceneAndShowMsg(self, self.spaceNo, _targetSpaceNo):
            return

        if self.wonderLandQuota.quotaDurState == gameconst.QuotaDurStatus.ENTER:
            LOG_ERR('IWonderLandCell::enterWonderLand: wonderLandQuota.quotaDurState == gameconst.QuotaDurStatus.ENTER')
            return

        if self.wonderLandQuota.leftTime <= 0:
            self.base.checkAndEnterWonderLand(floor)
            return

        extra = {'enterWonderLandType': gameconst.WONDER_LAND_ENTER_TYPE_LEFT_TIME}
        gameengine.getWonderLandStub(mapId).doEnterWonderLand(self.base, self.gbId, extra)

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
            'hasCast': False,
            'enterType': extra.get('enterWonderLandType', 0)
        }

        _options = complexTeleportOption.ComplexTeleportOptions(teleportType=gameconst.ComplexTeleportType.ENTER)

        canLeave = self.packageComplexTeleportLeaveData(_lContext)
        if not canLeave:
            LOG_WARN('IWonderLandCell::beginEnterWonderLand: can not leave')
            return

        self.teleportFromSpaceToSpace(self.spaceNo, spaceNo, options=_options, context=_context, failedFunc='enterWonderLandFailed', failedArgs=(spaceNo,))

    def enterWonderLandFailed(self, spaceNo):
        DEBUG_MSG("IWonderLandCell::enterWonderLandFailed", spaceNo)
        gameengine.getWonderLandStubBySpaceNo(spaceNo).onLeaveWonderLand(self.gbId)

    @utils.isMyself
    @gamedecorator.limitcall(1)
    def leaveWonderLand(self, exposed):
        self.leaveWonderLandInternal(gameconst.DungeonSrcEnum.FROM_CLIENT, False)

    def leaveWonderLandInternal(self, srcId, hasCast=True):
        if not formula.inWonderLandScene(self.spaceNo):
            LOG_WARN('IWonderLandCell::leaveWonderLand: spaceNo not line: {}'.format(self.spaceNo))
            return

        _src = dungeonSrc.BasicDungeonSrc(srcId=srcId)
        _l = {}
        _context = {
            'e': {},
            'l': _l,
            'src': _src,
            'hasCast': hasCast,
        }

        _canLeave = self.packageComplexTeleportLeaveData(_l)
        if not _canLeave:
            LOG_WARN('IWonderLandCell::leaveWonderLand: can not leave')
            return

        _, _m_outsideRecord = self.tryGetLastTeleportOutesideRecord(self.spaceNo, spaceType=formula.getSpaceType(self.spaceNo))
        _spaceNo = _m_outsideRecord.spaceNo if _m_outsideRecord else formula.combineLineSpaceNo(gameconst.MapIdDef.mapXinYuanCheng)

        _options = complexTeleportOption.ComplexTeleportOptions(teleportType=gameconst.ComplexTeleportType.LEAVE)
        self.doLeaveFromSapceToSpace(self.spaceNo, _spaceNo, _options, _context)

    def _onWonderLandOffline(self):
        if not formula.inWonderLandScene(self.spaceNo):
            return

        self._cancelWonderLandTimer()
        self.wonderLandQuota.checkout()

    def _dealWithWonderLandTimer(self, oldSpaceNo, newSpaceNo):
        _oldNeedTimer = formula.inWonderLandScene(oldSpaceNo)
        _newNeedTimer = formula.inWonderLandScene(newSpaceNo)

        self.wonderLandQuota.refreshEnterTime()
        if _oldNeedTimer == _newNeedTimer:
            return

        if _newNeedTimer:
            self.wonderLandQuota.setWonderLandEnterTime(self, utils.curTS())
            self._startWonderLandTimer(gameconst.WONDER_LAND_DUR_RENEW)

        else:
            self._cancelWonderLandTimer()
            #self.wonderLandQuota.checkout()
            self.wonderLandQuota.reset()

    def _startWonderLandTimer(self, durStatus):
        self._cancelWonderLandTimer()

        _now = utils.curTS()
        _endTime = _now + self.wonderLandQuota.calcLeftTime()

        if durStatus == gameconst.WONDER_LAND_DUR_RENEW:
            _fireTime = max(_now + 1, _endTime - 60)
        else:
            _fireTime = max(_now + 5, _endTime)

        self.wonderLandTimerId = self._datetimeCallback(
            _fireTime, 
            '_onWonderLandTimeOut',
            (durStatus, ),
            gametimer.TIMER_TAG_WONDER_LAND_TIME_OUT,
            'wonderLandTimerId'
        )

    def _onWonderLandTimeOut(self, durStatus):
        if durStatus == gameconst.WONDER_LAND_DUR_RENEW:
            self._onWonderLandTimeOutRenew()
        else:
            self._onWonderLandTimeOutEnd()

    def _onWonderLandTimeOutEnd(self):
        if not formula.inWonderLandScene(self.spaceNo):
            return

        LOG_IFO('IWonderLandCell::_onWonderLandTimeOutEnd: {}'.format(self.spaceNo))
        self.leaveWonderLandInternal(gameconst.DungeonSrcEnum.FROM_TIME_OUT, True)

    def _onWonderLandTimeOutRenew(self):
        LOG_IFO('IWonderLandCell::wonderLandRenewCB: {}'.format(self.spaceNo))
        if not formula.inWonderLandScene(self.spaceNo):
            return

        self._startWonderLandTimer(gameconst.WONDER_LAND_DUR_TIMEOUT)

        _switchVal = self.getTempMiscProp(gameconst.EntityPropsEnum.wonderLandSwitch)

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

    def _cancelWonderLandTimer(self):
        if self.wonderLandTimerId:
            self._cancelDatetimeCallback(self.wonderLandTimerId, gametimer.TIMER_TAG_WONDER_LAND_TIME_OUT)
            self.wonderLandTimerId = 0

    def afterLeaveWonderLand(self):
        if self.getTempMiscProp(gameconst.EntityPropsEnum.wonderLandSwitch):
            self._changeWonderLandSwitch(False, {})
        self.clearWonderLandRewardRecord()

    def summonWonderLandBoss(self, itemId, itemNum, gid, collectionId):
        _bossId = self.getMonsterIdFromGID(gid)
        if self.spaceMgr.checkHasBoss(_bossId):
            self.showMsg(WL_CD.datas['wonderLand_bossAlive']['value'], [])
            return

        self.base.summonWonderLandBossBase(gid, itemId, itemNum, collectionId)

    def summonWonderLandBossFromBase(self, gid, itemId, collectionId, opUUID):
        _mapId = formula.fetchMapId(self.spaceNo)
        _dunData = utils.getDunModuleData(_mapId)
        if not _dunData:
            LOG_ERR('IWonderLandCell::summonWonderLandBossFromBase: not found dunData', self.spaceNo)
            return

        _monData = _dunData.get(str(gid))
        if not _monData:
            LOG_ERR('IWonderLandCell::summonWonderLandBossFromBase: not found monData', gid)
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

    def getMonsterIdFromGID(self, gid):
        _mapId = formula.fetchMapId(self.spaceNo)
        _dunData = utils.getDunModuleData(_mapId)
        if not _dunData:
            LOG_ERR('IWonderLandCell::getMonsterIdFromGID: not found dunData', self.spaceNo)
            return

        _monData = _dunData.get(str(gid))
        if not _monData:
            LOG_ERR('IWonderLandCell::getMonsterIdFromGID: not found monData', gid)
            return

        return _monData.get('EntityID')

    def checkSummonWonderLandBoss(self, itemId, itemNum, gid, collectionId):
        _bossId = self.getMonsterIdFromGID(gid)
        return CollectionCheckContext.CollectionCheckWonderLand(itemId, itemNum, _bossId, collectionId)

    def checkSummonWonderLandBossCell(self, bossId):
        _hasBoss = self.spaceMgr.checkHasBoss(bossId)
        if _hasBoss:
            self.showMsg(WL_CD.datas['wonderLand_bossAlive']['value'], [])

        return not _hasBoss

    @utils.isMyself
    def reqChangeWonderLandSwitch(self, exposed, masterSwitch, switchData):
        LOG_IFO('IWonderLandCell::reqChangeWonderLandSwitch: {} {}'.format(masterSwitch, switchData))
        if masterSwitch and not utils.isActOpen(WL_CD.datas['wonderLandActID']['value']):
            self.showMsg(AC_CD.datas['activity_notOpen']['value'], [])
            return

        self._changeWonderLandSwitch(masterSwitch, switchData)

    def deadChangeWonderLandSwitch(self):
        self.reqChangeWonderLandSwitch(self.id, False, WonderLandSwitch().toClientData())

    def _changeWonderLandSwitch(self, masterSwitch, switchData):
        if not masterSwitch:
            self.popTempMiscProp(gameconst.EntityPropsEnum.wonderLandSwitch)
            self.client.onWonderLandSwitch(False, WonderLandSwitch().toClientData())
            return

        _switchVal = WonderLandSwitch(**switchData)
        self.setTempMiscProp(gameconst.EntityPropsEnum.wonderLandSwitch, _switchVal)
        self.client.onWonderLandSwitch(True, switchData)

        if _switchVal.canAddTimes():
            self._startWonderLandTimer(gameconst.WONDER_LAND_DUR_RENEW)

    def _checkAddWonderLandDurationCondition(self):
        if not formula.inWonderLandScene(self.spaceNo):
            LOG_WARN('IWonderLandCell::checkAddWonderLandDurationCondition: spaceNo not wonderLand: {}'.format(self.spaceNo))
            return False

        if self.wonderLandQuota.calcLeftTime() > WL_CD.datas['wonderLandNumTime']['value'] * 60:
            LOG_WARN('IWonderLandCell::checkAddWonderLandDurationCondition: wonderLandQuota.calcLeftTime() > WL_CD.datas[\'wonderLandNumTime\'][\'value\'] * 60: {}'.format(self.wonderLandQuota.calcLeftTime()))
            return False

        return True

    def directlyAddWonderLandDuration(self, func, args):
        if not self._checkAddWonderLandDurationCondition():
            getattr(self.base, func)(*args)
            return

        _dur = WL_CD.datas['wonderLandNumTime']['value'] * 60
        self.wonderLandQuota.addWonderLandLeftTime(self, _dur)
        self.base.activityComplete(WL_CD.datas['wonderLandActID']['value'])
        self._startWonderLandTimer(gameconst.WONDER_LAND_DUR_RENEW)

    def checkAddWonderLandDurationCondition(self, itemId, num, opUUID):
        if not self._checkAddWonderLandDurationCondition():
            return

        self.base.doAddWonderLandTicket(itemId, num, True, True, gameconst.WonderAddTicketReason.CHECK_COND, opUUID)

    def addWonderLandRewardRecord(self, rewardList):
        _dic = self.getTempMiscProp(gameconst.EntityPropsEnum.wonderLandRewardList, {})
        for _data in rewardList:
            _itemId = _data['itemId']
            _bindType = _data['bindType']
            _dic.setdefault(_itemId, {})
            _dic[_itemId][_bindType] = _dic[_itemId].get(_bindType, 0) + _data['itemNum']

        self.setTempMiscProp(gameconst.EntityPropsEnum.wonderLandRewardList, _dic)
        self.client.onAddWonderLandRewardRecord(rewardList)

    def clearWonderLandRewardRecord(self):
        self.popTempMiscProp(gameconst.EntityPropsEnum.wonderLandRewardList)

    def doSendWonderLandLoginData(self):
        if not formula.inWonderLandScene(self.spaceNo):
            return

        _rewardList = []
        for k, v in self.getTempMiscProp(gameconst.EntityPropsEnum.wonderLandRewardList, {}).items():
            for _bindType, _num in v.items():
                _rewardList.append({'itemId': k, 'itemNum': _num, 'bindType': _bindType})

        _switchVal = self.getTempMiscProp(gameconst.EntityPropsEnum.wonderLandSwitch)
        if _switchVal is None:
            _masterSwitch = False
            _switchData = WonderLandSwitch().toClientData()
        else:
            _masterSwitch = True
            _switchData = _switchVal.toClientData()

        _endTime = utils.curTS() + self.wonderLandQuota.calcLeftTime()
        self.client.onWonderLandLoginData(_endTime, _masterSwitch, _switchData, _rewardList)

    def onLogonEnterWonderLandCB(self, spaceMgrBoxCellId):
        self.spaceMgrId = spaceMgrBoxCellId
        self.spaceMgr.onPlayerEnter(self.id)

        gameengine.getWonderLandStubBySpaceNo(self.spaceNo).onEnterWonderLandSuccess(self.gbId, self.spaceNo)
        self.wonderLandQuota.setWonderLandEnterTime(self, utils.curTS())
        self._startWonderLandTimer(gameconst.WONDER_LAND_DUR_RENEW)

    @utils.isMyself
    def getWonderLandLeftTime(self, exposed):
        self.client.onWonderLandLeftTimeDuration(self.wonderLandQuota.calcLeftTime())


