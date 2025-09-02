
# coding: utf-8

import userType
import RelationEnemyInfo
import gameconst
import utils
import relationConfig_relationConfig as RC_RCD


class EnemyMgrVal(userType.UserSoleType):
    '''ENEMY_MGR_DATA_INFO'''
    def __init__(self, enemyList=(), recordList=()):
        self.enemyDict = {}
        for enemy in enemyList:
            self.enemyDict[enemy.gbId] = enemy

        self.recordDict = {}
        for record in recordList:
            self.recordDict[record['gbId']] = RelationEnemyInfo.EnemyRecordListVal(**record)

    def isEnemy(self, gbId):
        return gbId in self.enemyDict
    
    def getRecordDatas(self):
        datas = []

        for _relationEnemyVal in self.recordDict.values():
            datas.append(_relationEnemyVal.toEnemyRecordListSavedDict())

        return datas

    def toEnemyMgrSavedDict(self):
        return {
            'enemyList': [enemy for enemy in self.enemyDict.values()],
            'recordList': [record.toEnemyRecordListSavedDict() for record in self.recordDict.values()]
        }
    
    def onKillOtherAvatarRecord(self, avatar, gbId, spaceNo):
        _recordListVal = self.recordDict.get(gbId)
        if not _recordListVal:
            return

        _recordVal = _recordListVal.addEnemyRecord(gameconst.EnemyRecordType.KILL_ENEMY, spaceNo)
        avatar.client.onNewEnemyRecord(gbId, _recordVal.toEnemyRecordSavedDict())

    def updateEnemyOfflineTime(self, gbId):
        _relationEnemyVal = self.enemyDict.get(gbId)
        if not _relationEnemyVal:
            return

        _relationEnemyVal.offlineTime = utils.getNow()

    def addEnemy(self, avatar, gbId, name, school, level, spaceNo, sex, score):
        if gbId in self.enemyDict:
            _recordListVal = self.recordDict.get(gbId)
            _recordVal = _recordListVal.addEnemyRecord(gameconst.EnemyRecordType.BE_KILL_BY_ENEMY, spaceNo)
            avatar.client.onNewEnemyRecord(gbId, _recordVal.toEnemyRecordSavedDict())
            return

        _relationEnemyVal = RelationEnemyInfo.RelationEnemyVal(gbId, name, school, level, sex, addTime=utils.getNow(), lastFindSpaceNo=spaceNo, lastFindTime=0, score=score)
        self.enemyDict[gbId] = _relationEnemyVal
        avatar.client.onEnemyDatas([_relationEnemyVal])

        _recordListVal = RelationEnemyInfo.EnemyRecordListVal(gbId, [])
        self.recordDict[gbId] = _recordListVal
        _recordVal = _recordListVal.addEnemyRecord(gameconst.EnemyRecordType.BE_KILL_BY_ENEMY, spaceNo)
        avatar.client.onNewEnemyRecord(gbId, _recordVal.toEnemyRecordSavedDict())

        self._autoPopEnemy(avatar)

    def updateEnemyLastFindInfo(self, gbId, spaceNo):
        _relationEnemyVal = self.enemyDict.get(gbId)
        if not _relationEnemyVal:
            return

        _relationEnemyVal.lastFindSpaceNo = spaceNo
        _relationEnemyVal.lastFindTime = utils.getNow()

    def _autoPopEnemyOnce(self):
        _popOne = None
        for _relationEnemyVal in self.enemyDict.values():
            if _popOne is None:
                _popOne = _relationEnemyVal
            elif _relationEnemyVal < _popOne:
                _popOne = _relationEnemyVal

        if _popOne:
            self.removeEnemy(_popOne.gbId)
            return _popOne.gbId

        return 0

    def _autoPopEnemy(self, avatar):
        _gbIds = []
        while len(self.enemyDict) > RC_RCD.datas['enemyNumLimit']['value']:
            _gbId = self._autoPopEnemyOnce()
            if _gbId == 0:
                break

            _gbIds.append(_gbId)

        if not _gbIds:
            return

        avatar.client.onRemoveEnemy(_gbIds)

    def removeEnemy(self, gbId):
        self.enemyDict.pop(gbId, None)
        self.recordDict.pop(gbId, None)

    def getEnemyGbIds(self):
        return list(self.enemyDict.keys())
    
    def updateByFcVals(self, fcVals):
        for _fcVal in fcVals:
            _enemyVal = self.enemyDict.get(_fcVal.gbId)
            if not _enemyVal:
                continue

            _enemyVal.updateFromFcVal(_fcVal)
    
    def getEnemyFreshInfo(self):
        return [enemy.toEnemyFreshInfo() for enemy in self.enemyDict.values()]

class EnemyMgrInfo(object):
    def createObjFromDict(self, dataDict):
        obj = EnemyMgrVal(**dataDict)
        return obj

    def getDictFromObj(self, obj):
        return obj.toEnemyMgrSavedDict()

    def isSameType(self, obj):
        return type(obj) is EnemyMgrVal


EnemyMgrInstance = EnemyMgrInfo()

