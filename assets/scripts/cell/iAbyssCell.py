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

import abyss_floor as AB_FD
import abyss_config as AB_CD
import creep_base as CBD
import activityControl_config as AC_CD
import const_const as CONST
import conflict_conflict_def as C_C_DD
import gameconfig

import LogTrackingMgr

class AbyssSwitch(object):
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
        LOG_DBG('AbyssSwitch::addTimes: {}'.format(self.curTimes))
        self.curTimes += 1

    def toClientData(self):
        return {
            'coinSwitch': self.coinSwitch,
            'itemSwitch': self.itemSwitch,
            'times': max(0, self.times - self.curTimes),
        }



class IAbyssCell(object):
    def __init__(self):
        if self.abyssQuota.quotaDurState == gameconst.QuotaDurStatus.ENTER:
            LOG_ERR('IAbyssCell::init: abyssQuota.quotaDurState == gameconst.QuotaDurStatus.ENTER')
            self.abyssQuota.resetOnLogin()
        
        if self.isCrossServer:
            self.pyAddTimer(60, 60, gametimer.CROSSSERVER_ABYSS_TIME_SYNC)

    def checkCanEnterAbyssCell(self, floor):
        if not utils.isActOpen(AB_CD.datas['abyssActID']['value']):
            self.showMsg(AC_CD.datas['activity_notOpen']['value'], [])
            return

        if self.level < AB_FD.datas[floor]['needLv']:
            LOG_ERR('IAbyssCell::enterAbyss: level < needLv: {} < {}'.format(self.level, AB_FD.datas[floor]['needLv']))
            return

        if self.totalScore < AB_FD.datas[floor]['needScore']:
            LOG_ERR('IAbyssCell::enterAbyss: totalScore < needScore: {} < {}'.format(self.totalScore, AB_FD.datas[floor]['needScore']))
            return

        mapId = AB_FD.datas[floor]['ID']
        _targetSpaceNo = formula.combineLineSpaceNo(mapId, 0)

        if not utils.checkCanChangeSceneAndShowMsg(self, self.spaceNo, _targetSpaceNo):
            return

        if self.abyssQuota.quotaDurState == gameconst.QuotaDurStatus.ENTER:
            LOG_ERR('IAbyssCell::enterAbyss: abyssQuota.quotaDurState == gameconst.QuotaDurStatus.ENTER')
            return
        
        return True
    
    def doSwitchAbyssLine(self, spaceBox, spaceMgrBoxCellId, spaceNo, extra):
        if extra.get('isMerge', False):
            self.beginEnterAbyss(spaceBox, spaceMgrBoxCellId, spaceNo, extra)
            return
        self._commonNeedCast(
            C_C_DD.datas.teleportCast,
            gameconst.StateEnum.Teleporting,
            gameconst.CastEnum.teleportAnchor,
            'beginEnterAbyss',
            (spaceBox, spaceMgrBoxCellId, spaceNo, extra),
            castTime=CONST.datas['teleportTime'].get("value", gameconst.ANCHOR_CAST_DUR)
        )

    def beginEnterAbyss(self, spaceBox, spaceMgrBoxCellId, spaceNo, extra):
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
            'enterType': extra.get('enterAbyssType', 0),
            'abyssExtra': extra.get('abyssExtra', {}),
        }

        _options = complexTeleportOption.ComplexTeleportOpt(teleportType=gameconst.ComplexTeleportEnum.ENTER)

        canLeave = self.packComplexTeleportLeaveData(_lContext)
        if not canLeave:
            LOG_WARN('IAbyssCell::beginEnterAbyss: can not leave')
            return

        self.telFromSpaceToSpace(self.spaceNo, spaceNo, options=_options, context=_context, failedFunc='enterAbyssFailed', failedArgs=(spaceNo,))

    def enterAbyssFailed(self, spaceNo):
        LOG_DBG("IAbyssCell::enterAbyssFailed", spaceNo)
        gameengine.getAbyssStubBySpaceNo(spaceNo).onLeaveAbyss(self.gbId)

    #gm是本服的
    def gmLeaveAbyss(self):
        srcId = gameconst.DunSrcEnum.FROM_CLIENT
        if not formula.inAbyssScene(self.spaceNo):
            LOG_WARN('IAbyssCell::leaveAbyss: spaceNo not line: {}'.format(self.spaceNo))
            return

        _src = dungeonSrc.BasicDungeonSrc(srcId=srcId)
        _l = {}
        _context = {
            'e': {},
            'l': _l,
            'src': _src,
            'hasCast': False,
        }

        _canLeave = self.packComplexTeleportLeaveData(_l)
        if not _canLeave:
            LOG_WARN('IAbyssCell::leaveAbyss: can not leave')
            return

        _, _m_outsideRecord = self.tryGetLastTeleportOutesideRecord(self.spaceNo, spaceType=formula.getSpaceType(self.spaceNo))
        _spaceNo = _m_outsideRecord.spaceNo if _m_outsideRecord else formula.combineLineSpaceNo(gameconst.MapIdDef.mapXinYuanCheng)

        _options = complexTeleportOption.ComplexTeleportOpt(teleportType=gameconst.ComplexTeleportEnum.LEAVE)
        self.doLeaveFromSapceToSpace(self.spaceNo, _spaceNo, _options, _context)

    def _onAbyssOffline(self):
        if not formula.inAbyssScene(self.spaceNo):
            return

        self._cancelAbyssTimer()
        self.abyssQuota.checkout()
        self._onLeftTimeSync()

    def _dealWithAbyssTimer(self, oldSpaceNo, newSpaceNo):
        _oldNeedTimer = formula.inAbyssScene(oldSpaceNo)
        _newNeedTimer = formula.inAbyssScene(newSpaceNo)

        self.abyssQuota.refreshEnterTime()
        if _oldNeedTimer == _newNeedTimer:
            return

        if _newNeedTimer:
            self.abyssQuota.setAbyssEnterTime(self, utils.curTS())
            self._startAbyssTimer(gameconst.ABYSS_DUR_RENEW)

        else:
            self._cancelAbyssTimer()
            self.abyssQuota.checkout()
            self._onLeftTimeSync()

    def _startAbyssTimer(self, durStatus):
        self._cancelAbyssTimer()

        _now = utils.curTS()
        _endTime = _now + self.abyssQuota.calcLeftTime()
        LOG_INFO("leftTime", self.abyssQuota.calcLeftTime(), self.abyssQuota)

        if durStatus == gameconst.ABYSS_DUR_RENEW:
            _fireTime = max(_now + 1, _endTime - 60)
        else:
            _fireTime = max(_now + 5, _endTime)

        self.abyssTimerId = self._datetimeCallback(
            _fireTime, 
            '_onAbyssTimeOut',
            (durStatus, ),
            gametimer.TIMER_TAG_ABYSS_TIME_OUT,
            'abyssTimerId'
        )

    def _onAbyssTimeOut(self, durStatus):
        if durStatus == gameconst.ABYSS_DUR_RENEW:
            self._onAbyssTimeOutRenew()
        else:
            self._onAbyssTimeOutEnd()

    def _onAbyssTimeOutEnd(self):
        if not formula.inAbyssScene(self.spaceNo):
            return

        LOG_INFO('IAbyssCell::_onAbyssTimeOutEnd: {}'.format(self.spaceNo))
        self.base.leaveCrossServerAbyss()

    def _onAbyssTimeOutRenew(self):
        LOG_INFO('IAbyssCell::abyssRenewCB: {}'.format(self.spaceNo))
        if not formula.inAbyssScene(self.spaceNo):
            return

        self._startAbyssTimer(gameconst.ABYSS_DUR_TIMEOUT)

        _switchVal = self.getTempMiscProp(gameconst.EntityPropsEnum.abyssSwitch)

        if _switchVal is None:
            return

        if not _switchVal.canAddTimes():
            return

        if not self._checkAddAbyssDurationCondition():
            return

        _switchVal.addTimes()
        self.base.autoRenewAbyss(_switchVal.toClientData())
        self.client.onAbyssSwitch(True, _switchVal.toClientData())
        self.client.onChangeAbyssRenewTimes(_switchVal.leftTimes())

    def _cancelAbyssTimer(self):
        if self.abyssTimerId:
            self._cancelDatetimeCallback(self.abyssTimerId, gametimer.TIMER_TAG_ABYSS_TIME_OUT)
            self.abyssTimerId = 0

    def afterLeaveAbyss(self):
        if self.getTempMiscProp(gameconst.EntityPropsEnum.abyssSwitch):
            self._changeAbyssSwitch(False, {})
        self.clearAbyssRewardRecord()

    def getMonsterIdFromGID(self, gid):
        _mapId = formula.fetchMapId(self.spaceNo)
        _dunData = utils.getDunModuleData(_mapId)
        if not _dunData:
            LOG_ERR('IAbyssCell::getMonsterIdFromGID: not found dunData', self.spaceNo)
            return

        _monData = _dunData.get(str(gid))
        if not _monData:
            LOG_ERR('IAbyssCell::getMonsterIdFromGID: not found monData', gid)
            return

        return _monData.get('EntityID')

    @utils.isMyself
    @gamedecorator.crossServer
    def reqChangeAbyssSwitch(self, exposed, masterSwitch, switchData):
        LOG_INFO('IAbyssCell::reqChangeAbyssSwitch: {} {}'.format(masterSwitch, switchData))
        if masterSwitch and not utils.isActOpen(AB_CD.datas['abyssActID']['value']):
            self.showMsg(AC_CD.datas['activity_notOpen']['value'], [])
            return

        self._changeAbyssSwitch(masterSwitch, switchData)

    def deadChangeAbyssSwitch(self):
        self.reqChangeAbyssSwitch(self.id, False, AbyssSwitch().toClientData())

    def _changeAbyssSwitch(self, masterSwitch, switchData):
        if not masterSwitch:
            self.popTempMiscProp(gameconst.EntityPropsEnum.abyssSwitch)
            self.client.onAbyssSwitch(False, AbyssSwitch().toClientData())
            return

        _switchVal = AbyssSwitch(**switchData)
        self.setTempMiscProp(gameconst.EntityPropsEnum.abyssSwitch, _switchVal)
        self.client.onAbyssSwitch(True, switchData)

        if _switchVal.canAddTimes():
            self._startAbyssTimer(gameconst.ABYSS_DUR_RENEW)

    def _checkAddAbyssDurationCondition(self):
        if not formula.inAbyssScene(self.spaceNo):
            LOG_WARN('IAbyssCell::checkAddAbyssDurationCondition: spaceNo not abyss: {}'.format(self.spaceNo))
            return False

        if self.abyssQuota.calcLeftTime() > AB_CD.datas['abyssNumTime']['value'] * 60:
            LOG_WARN('IAbyssCell::checkAddAbyssDurationCondition: abyssQuota.calcLeftTime() > AB_CD.datas[\'abyssNumTime\'][\'value\'] * 60: {}'.format(self.abyssQuota.calcLeftTime()))
            return False

        return True

    def directlyAddAbyssDuration(self, func, args):
        if not self._checkAddAbyssDurationCondition():
            getattr(self.base, func)(*args)
            return

        _dur = AB_CD.datas['abyssNumTime']['value'] * 60
        self.abyssQuota.addAbyssLeftTime(self, _dur)
        self.base.activityComplete(AB_CD.datas['abyssActID']['value'])
        self._startAbyssTimer(gameconst.ABYSS_DUR_RENEW)
        self.doSyncAbyssData()

    def checkAddAbyssDurationCondition(self, addType, itemId, itemNum, num, opUUID):
        if not self._checkAddAbyssDurationCondition():
            return

        self.base.doAddAbyssTicket(addType, itemId, itemNum, num, True, True, gameconst.AbyssAddTicketReason.CHECK_COND, opUUID)

    def addAbyssRewardRecord(self, rewardList):
        _dic = self.getTempMiscProp(gameconst.EntityPropsEnum.abyssRewardList, {})
        for _data in rewardList:
            _itemId = _data['itemId']
            _bindType = _data['bindType']
            _dic.setdefault(_itemId, {})
            _dic[_itemId][_bindType] = _dic[_itemId].get(_bindType, 0) + _data['itemNum']

        self.setTempMiscProp(gameconst.EntityPropsEnum.abyssRewardList, _dic)
        self.client.onAddAbyssRewardRecord(rewardList)

    def clearAbyssRewardRecord(self):
        self.popTempMiscProp(gameconst.EntityPropsEnum.abyssRewardList)

    def doSendAbyssLoginData(self):
        if not formula.inAbyssScene(self.spaceNo):
            return

        _rewardList = []
        for k, v in self.getTempMiscProp(gameconst.EntityPropsEnum.abyssRewardList, {}).items():
            for _bindType, _num in v.items():
                _rewardList.append({'itemId': k, 'itemNum': _num, 'bindType': _bindType})

        _switchVal = self.getTempMiscProp(gameconst.EntityPropsEnum.abyssSwitch)
        if _switchVal is None:
            _masterSwitch = False
            _switchData = AbyssSwitch().toClientData()
        else:
            _masterSwitch = True
            _switchData = _switchVal.toClientData()

        _endTime = utils.curTS() + self.abyssQuota.calcLeftTime()
        self.client.onAbyssLoginData(_endTime, _masterSwitch, _switchData, _rewardList)

    def onLogonEnterAbyssCB(self, spaceMgrBoxCellId):
        self.spaceMgrId = spaceMgrBoxCellId
        self.spaceMgr.onPlayerEnter(self.id)

        gameengine.getAbyssStubBySpaceNo(self.spaceNo).onEnterAbyssSuccess(self.gbId, self.spaceNo)
        self.abyssQuota.setAbyssEnterTime(self, utils.curTS())
        self._startAbyssTimer(gameconst.ABYSS_DUR_RENEW)

    @utils.isMyself
    @gamedecorator.crossServer
    def getAbyssLeftTime(self, exposed):
        LOG_INFO('IAbyssCell::getAbyssLeftTime: {}'.format(self.abyssQuota.calcLeftTime()))
        self.client.onAbyssLeftTimeDuration(self.abyssQuota.calcLeftTime())

    def checkAndEnterCrossServerAbyss(self, floor, noTicket):
        LOG_INFO('IAbyssCell::enterCrossServerAbyss: {} {} {}'.format(floor, noTicket, self.abyssQuota.leftTime))
        if not self.checkCanEnterAbyssCell(floor):
            return

        if self.abyssQuota.leftTime <= 0:
            if noTicket:
                return

        #用票买时间
        if self.abyssQuota.leftTime <= 0:
            self.abyssQuota.addAbyssLeftTime(self, AB_CD.datas['abyssNumTime']['value'] * 60)
            self.base.afterEnterAbyssDeductTimes({'floor': floor})

        #本服判断可以进了，开始读条
        self._commonNeedCast(
            C_C_DD.datas.teleportCast,
            gameconst.StateEnum.Teleporting,
            gameconst.CastEnum.teleportAnchor,
            '_doEnterCrossServerAbyss',
            (floor,),
            castTime=CONST.datas['teleportTime'].get("value", gameconst.ANCHOR_CAST_DUR)
        )

    def _doEnterCrossServerAbyss(self, floor):
        self.base.doEnterCrossServerAbyss(floor)
        
    def crossServerAbyssLeave(self):
        LOG_DBG("[lj]crossServerAbyssLeave")
        self.applyLeaveTeam(self.id)
        self.leaveRaid(self.id)
        gameengine.getAbyssStubBySpaceNo(self.spaceNo).onLeaveAbyssWithToSpaceNo(self.gbId, 0)
        self.spaceMgr.onPlayerLeave(self.gbId, self.id, self)

        LogTrackingMgr.LogTrackingMgr.abyss_leave(
            self.gbId,
            self.clientDistinctIdCell,
            utils.curTS()
        )

    def _onLeftTimeSync(self):
        self.abyssQuota.refreshEnterTime()
        leftTime = self.abyssQuota.calcLeftTime()
        LOG_INFO('IAbyssCell::_onLeftTimeSync: {}'.format(leftTime))
        self.client.onAbyssLeftTimeDuration(leftTime)
        self.doSyncAbyssData()

    #数据变化时同步回本服
    def doSyncAbyssData(self):
        LOG_INFO('IAbyssCell::doSyncAbyssData')
        if not gameconfig.isCrossServer():
            return

        leftTime = self.abyssQuota.calcLeftTime()
        enterTime = self.abyssQuota.enterTime
        self.syncMethodCallToLocalServerCell('onCrossServerSyncAbyssData', (leftTime, enterTime))
        self.base.syncAbyssDataContinue()

    def onCrossServerSyncAbyssData(self, leftTime, enterTime):
        LOG_INFO('IAbyssCell::onCrossServerSyncAbyssData: {} {}'.format(leftTime, enterTime))
        self.abyssQuota.onCrossServerSyncAbyssData(leftTime, enterTime)
