# coding:utf-8
from KBEDebug import *

import KBEngine
import redisUtils
import gamedecorator
import gameconst
import gameengine
import dropAward
import gameclass

import antiAddictCategory_antiAddictCategory_def as AAC_AACDD
import relationConfig_relationConfig as RC_RCD

class IEnemy(object):
    def onDeadAddEnemy(self, killerGbId, killerName, killerSchool, killerLevel, spaceNo, sex, score):
        self.enemyMgr.addEnemy(self, killerGbId, killerName, killerSchool, killerLevel, spaceNo, sex, score)

    def reqRemoveEnemy(self, gbId):
        self.enemyMgr.removeEnemy(gbId)
        self.client.onRemoveEnemy([gbId])

    @gamedecorator.limitcall(60)
    def getEnemyFreshInfo(self):
        WARNING_MSG('getEnemyFreshInfo')
        _gbIds = self.enemyMgr.getEnemyGbIds()

        redisUtils.RedisUtils.getUsersInfo(_gbIds, self._onGetEnemyFreshInfo)

    def _onGetEnemyFreshInfo(self, usersInfo):
        WARNING_MSG('usersInfo:', usersInfo)
        self.enemyMgr.updateByFcVals(usersInfo)
        self.client.onGetEnemyFreshInfo(self.enemyMgr.getEnemyFreshInfo())

    def getEnemyPosInfo(self, gbId):
        if not self.enemyMgr.isEnemy(gbId):
            self.client.sendEnemyPosInfoToClient(gbId, False, 0)
            return

        gameengine.getGlobalBase('PlayerStub').doOnOthersCell(
            [gbId], 
            'onGetEnemyPosInfo',
            (self, ), 
            self, 
            'onGetEnemyPosInfoResult', 
            (False, None))
        
    def onGetEnemyPosInfoResult(self, otherGbId, find, posInfo):
        if not find:
            INFO_MSG('onGetEnemyPosInfoResult not find', otherGbId, posInfo)
            self.client.sendEnemyPosInfoToClient(otherGbId, find, 0)
            self.enemyMgr.updateEnemyOfflineTime(otherGbId)
            return

        _deductVal = dropAward.DeductWealthVal()
        _deductVal.addWealthByItemId(
            RC_RCD.datas['enemySearchItem']['value'],
            RC_RCD.datas['enemySearchItemNum']['value'],
        )

        if not self.canDeductWealth(_deductVal, sendMsg=True):
            WARNING_MSG('in onGetEnemyPosInfoResult, items not enough:', _deductVal)
            self.client.sendEnemyPosInfoToClient(otherGbId, find, 0)
            return

        _opUUID = KBEngine.genUUID64()
        _src = AAC_AACDD.datas.BONUS_SRC_SCAN_ENEMY_POS
        _detail = gameclass.AwardDetail()
        self.deductWealth(_src, _deductVal, _opUUID, _detail)
        
        _spaceNo = posInfo[0]
        self.client.sendEnemyPosInfoToClient(otherGbId, find, _spaceNo)
        self.enemyMgr.updateEnemyLastFindInfo(otherGbId, _spaceNo)

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

