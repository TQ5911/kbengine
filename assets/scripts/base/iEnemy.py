# coding:utf-8
from KBEDebug import *

import KBEngine
import redisUtils
import gamedecorator
import gameconst
import gameengine
import dropAward
import gameclass
import gametimer
import actionContext
import antiAddictCategory_antiAddictCategory_def as AAC_AACDD
import relationConfig_relationConfig as RC_RCD

class IEnemy(object):
    def __init__(self):
        #
        self.enemyScheduleTimerId = 0

    def onDeadAddEnemy(self, killerGbId, killerName, killerSchool, killerLevel, spaceNo, sex, score):
        self.enemyMgr.addEnemy(self, killerGbId, killerName, killerSchool, killerLevel, spaceNo, sex, score)
        self.triggerAchievementWithCtx(gameconst.AchieveType.ENEMY, actionContext.AchievementCtx(count=self.enemyMgr.getEnemyCount()))

    @gamedecorator.checkGameconfigEnable('enemy')
    def reqRemoveEnemy(self, exposed, gbId):
        self.enemyMgr.removeEnemy(gbId)
        self.client.onRemoveEnemy([gbId])

    @gamedecorator.limitcall(60)
    def getEnemyFreshInfo(self, exposed):
        LOG_INFO('getEnemyFreshInfo')
        _gbIds = self.enemyMgr.getEnemyGbIds()

        redisUtils.RedisUtils.getUsersInfo(_gbIds, self._onGetEnemyFreshInfo)

    def _onGetEnemyFreshInfo(self, usersInfo):
        LOG_DBG('usersInfo:', usersInfo)
        self.enemyMgr.updateByFcVals(usersInfo)
        # LOG_INFO('onGetEnemyFreshInfo, enemy fresh info:', self.enemyMgr.getEnemyFreshInfo())
        self.client.onGetEnemyFreshInfo(self.enemyMgr.getEnemyFreshInfo())

    @gamedecorator.checkGameconfigEnable('enemy')
    def getEnemyPosInfo(self, exposed, gbId):
        if not self.enemyMgr.isEnemy(gbId):
            self.client.sendEnemyPosInfoToClient(gbId, False, 0, True)
            return

        gameengine.getGlobalBase('PlayerStub').doOnOthersCell(
            [gbId],
            'onGetEnemyPosInfo',
            (self, False),
            self,
            'onGetEnemyPosInfoResult',
            (False, None))

    def onGetEnemyPosInfoResult(self, otherGbId, find, posInfo):
        if not find:
            LOG_INFO('onGetEnemyPosInfoResult not find', otherGbId, posInfo)
            self.client.sendEnemyPosInfoToClient(otherGbId, find, self.enemyMgr.getEnemyLastSpaceNo(otherGbId), True)
            self.enemyMgr.updateEnemyOfflineTime(otherGbId)
            return
        
        if self.enemyScheduleTimerId == 0:
            self.enemyScheduleTimerId = self.pyAddTimer(2, 2, gametimer.ENEMY_SCHEDULE)

        _deductVal = dropAward.DeductWealthVal()
        _deductVal.addWealthByItemId(
            RC_RCD.datas['enemySearchItem']['value'],
            RC_RCD.datas['enemySearchItemNum']['value'],
        )

        if not self.canDeductWealth(_deductVal, sendMsg=True):
            LOG_WARN('in onGetEnemyPosInfoResult, items not enough:', _deductVal)
            self.client.sendEnemyPosInfoToClient(otherGbId, find, 0, True)
            return

        _opUUID = KBEngine.genUUID64()
        _src = AAC_AACDD.datas.BONUS_SRC_SCAN_ENEMY_POS
        _detail = gameclass.AwardDetail()
        self.deductWealth(_src, _deductVal, _opUUID, _detail)

        _spaceNo = posInfo[0]
        self.client.sendEnemyPosInfoToClient(otherGbId, find, _spaceNo, True)
        self.enemyMgr.updateEnemyLastFindInfo(otherGbId, _spaceNo)
        self.client.showEnemyIcon(True)

    @gamedecorator.checkGameconfigEnable('enemy')
    @gamedecorator.limitcall(2)
    def switchEnemySchedule(self, exposed, flag):
        self.enemyScheduleTag = flag
        if flag:
            self.scheduleEnemyPosInfo()

    def scheduleEnemyPosInfo(self, login=False):
        activeList, updateList = self.enemyMgr.getNeedUpdateEnemyIds(login)
        # LOG_DBG('scheduleEnemyPosInfo, activeList:', activeList, 'updateList:', updateList)
        if not activeList:
            # 关闭图标
            self.client.showEnemyIcon(False)
            self.pyDelTimer(self.enemyScheduleTimerId, gametimer.ENEMY_SCHEDULE)
            self.enemyScheduleTimerId = 0
            self.enemyScheduleTag = False
            LOG_DBG('scheduleEnemyPosInfo: close')
            return

        # 重登之后定时器可能没了，重新开启
        if self.enemyScheduleTimerId == 0:
            self.enemyScheduleTimerId = self.pyAddTimer(2, 2, gametimer.ENEMY_SCHEDULE)

        # 未开启实时更新
        # if not self.enemyScheduleTag:
        #     return
        # 无需要更新的敌人
        if not updateList:
            return
        self.client.showEnemyIcon(True)
        
        gameengine.getGlobalBase('PlayerStub').doOnOthersCell(
            updateList,
            'onGetEnemyPosInfo',
            (self, True),
            self,
            'onScheduleEnemyPosInfoResult',
            (False, None))
            
    def onScheduleEnemyPosInfoResult(self, otherGbId, find, posInfo):
        lastSpaceNo = self.enemyMgr.getEnemyLastSpaceNo(otherGbId)
        if not find:
            LOG_INFO('onGetEnemyPosInfoResult not find', otherGbId, posInfo)
            self.client.sendEnemyPosInfoToClient(otherGbId, find, lastSpaceNo, False)
            self.enemyMgr.updateEnemyOfflineTime(otherGbId)
            return
        
        _spaceNo = posInfo[0]
        self.enemyMgr.scheduleEnemyLastFindInfo(otherGbId, _spaceNo)
        self.client.sendEnemyPosInfoToClient(otherGbId, find, _spaceNo, False)
        LOG_DBG('onScheduleEnemyPosInfoResult, find enemy pos info:', otherGbId, posInfo)

    def doSendEnemyRecordDatas(self):
        _datas = self.enemyMgr.getRecordDatas()
        while _datas:
            _sendDatas = _datas[:10]
            _datas = _datas[10:]

            if _datas:
                self.client.onInitEnemyRecord(False, _sendDatas)
            else:
                self.client.onInitEnemyRecord(True, _sendDatas)

            yield lambda : True

    def sendEnemyRecordDatas(self):
        _iter = self.doSendEnemyRecordDatas()
        self.batchlyCall(_iter, gameconst.SEND_ENEMY_RECORD_BATCH_NUM, 0.1)

    def sendAllEnemyDatas(self):
        LOG_DBG('sendAllEnemyDatas')
        self.client.onEnemyDatas(self.enemyMgr.getAllEnemyies())
        self.scheduleEnemyPosInfo(True)

    def getEnemyRecord(self, exposed, gbId):
        _recordData = self.enemyMgr.getRecordByGbId(gbId)
        if not _recordData:
            LOG_WARN('getEnemyRecord record not found', gbId)
            return

        LOG_DBG('on get record', gbId, _recordData)
        self.client.onEnemyRecord(_recordData.toEnemyRecordListSavedDict())

    def doSendRecordList(self, recordList):
        while recordList:
            _sendList = recordList[:10]
            recordList = recordList[10:]

            if recordList:
                self.client.onRecordList(False, _sendList)
            else:
                self.client.onRecordList(True, _sendList)
            # LOG_INFO('doSendRecordList, send record list:', _sendList)
            yield lambda : True

    @gamedecorator.checkGameconfigEnable('enemy')
    def getRecordList(self, exposed):
        recordList = self.enemyMgr.getAllRecordList()
        recordList = recordList[::-1]
        _iter = self.doSendRecordList(recordList)
        self.batchlyCall(_iter, gameconst.SEND_ENEMY_RECORD_BATCH_NUM, 0.1)

