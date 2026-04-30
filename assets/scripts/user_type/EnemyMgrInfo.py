
# coding: utf-8

import userType
import RelationEnemyInfo
import gameconst
import utils
import relationConfig_relationConfig as RC_RCD
import heapq
from KBEDebug import *


class EnemyMgrVal(userType.UserSingleType):
    '''ENEMY_MGR_DATA_INFO'''
    def __init__(self, enemyList=(), recordList=(), killList=()):
        self.enemyDict = {}
        for enemy in enemyList:
            self.enemyDict[enemy.gbId] = enemy

        self.recordDict = {}
        for record in recordList:
            self.recordDict[record['gbId']] = RelationEnemyInfo.EnemyRecordListVal(**record)

        self.killDict = {}
        for record in killList:
            self.killDict[record['gbId']] = RelationEnemyInfo.KillRecordListVal(**record)

        # 构造恩怨簿
        self.constructRecordList()

    def constructRecordList(self):
        self.recordList = []
        recordHeap = []
        maxSize = RC_RCD.datas['enemyRecordNumLimit']['value']

        for gbId, _recordVal in self.killDict.items():
            for _record in _recordVal.recordList:
                _val = {'name': _recordVal.name, 'gbId': gbId, 'school': _recordVal.school, 'level': _recordVal.level, 'sex': _recordVal.sex}
                _val.update(_record.toEnemyRecordSavedDict())
                if len(recordHeap) < maxSize:
                    heapq.heappush(recordHeap, (_val['ts'], _val))
                else:
                    if _val['ts'] > recordHeap[0][0]:
                        heapq.heapreplace(recordHeap, (_val['ts'], _val))

        self.recordList = [item[1] for item in recordHeap]
        self.recordList.sort(key=lambda x: x['ts'])

    def addRecord(self, gbId, name, school, level, sex, recordType, spaceNo):
        self.recordList.append({
            'gbId': gbId,
            'name': name,
            'ts': utils.curTS(),
            'type': recordType,
            'spaceNo': spaceNo,
            'school': school,
            'level': level,
            'sex': sex,
        })
        while len(self.recordList) > RC_RCD.datas['enemyRecordNumLimit']['value']:
            _val = self.recordList.pop(0)
            _recordVal = self.killDict.get(_val['gbId'])
            if _recordVal:
                _recordVal.recordList = [record for record in _recordVal.recordList if record.ts != _val['ts']]
                if not _recordVal.recordList:
                    self.killDict.pop(_val['gbId'], None)

    def getAllRecordList(self):
        return self.recordList

    def isEnemy(self, gbId):
        return gbId in self.enemyDict
    
    def getRecordDatas(self):
        datas = []

        for _relationEnemyVal in self.recordDict.values():
            datas.append(_relationEnemyVal.toEnemyRecordListSavedDict())

        return datas

    def getRecordByGbId(self, gbId):
        return self.recordDict.get(gbId)

    def getAllEnemyies(self):
        return [enemy for enemy in self.enemyDict.values()]

    def toEnemyMgrSavedDict(self):
        return {
            'enemyList': [enemy for enemy in self.enemyDict.values()],
            'recordList': [record.toEnemyRecordListSavedDict() for record in self.recordDict.values()],
            'killList': [record.toEnemyRecordListSavedDict() for record in self.killDict.values()],
        }
    
    def onKillOtherAvatarRecord(self, avatar, gbId, spaceNo, name, school, level, sex):
        _recordListVal = self.killDict.get(gbId, None)
        if not _recordListVal:
            _recordListVal = RelationEnemyInfo.KillRecordListVal(gbId, name, school, level, sex, [])
            self.killDict[gbId] = _recordListVal

        _recordListVal.addEnemyRecord(gameconst.EnemyRecordType.KILL_ENEMY, spaceNo)
        self.addRecord(gbId, _recordListVal.name, school, level, sex, gameconst.EnemyRecordType.KILL_ENEMY, spaceNo)

        _recordListVal = self.recordDict.get(gbId)
        if not _recordListVal:
            return

        _recordVal = _recordListVal.addEnemyRecord(gameconst.EnemyRecordType.KILL_ENEMY, spaceNo)
        avatar.client.onNewEnemyRecord(gbId, _recordVal.toEnemyRecordSavedDict())

    def updateEnemyOfflineTime(self, gbId):
        _relationEnemyVal = self.enemyDict.get(gbId)
        if not _relationEnemyVal:
            return

        _relationEnemyVal.offlineTime = utils.curTS()

    def addEnemy(self, avatar, gbId, name, school, level, spaceNo, sex, score):
        _recordListVal = self.killDict.get(gbId, None)
        if not _recordListVal:
            _recordListVal = RelationEnemyInfo.KillRecordListVal(gbId, name, school, level, sex, [])
            self.killDict[gbId] = _recordListVal
        _recordListVal.addEnemyRecord(gameconst.EnemyRecordType.BE_KILL_BY_ENEMY, spaceNo)
        self.addRecord(gbId, name, school, level, sex, gameconst.EnemyRecordType.BE_KILL_BY_ENEMY, spaceNo)

        if gbId in self.enemyDict:
            _recordListVal = self.recordDict.get(gbId)
            _recordVal = _recordListVal.addEnemyRecord(gameconst.EnemyRecordType.BE_KILL_BY_ENEMY, spaceNo)
            avatar.client.onNewEnemyRecord(gbId, _recordVal.toEnemyRecordSavedDict())
            return

        _relationEnemyVal = RelationEnemyInfo.RelationEnemyVal(gbId, name, school, level, sex, addTime=utils.curTS(), lastFindSpaceNo=spaceNo, lastFindTime=0, score=score)
        self.enemyDict[gbId] = _relationEnemyVal
        avatar.client.onEnemyDatas([_relationEnemyVal])

        _recordListVal = RelationEnemyInfo.EnemyRecordListVal(gbId, name, [])
        self.recordDict[gbId] = _recordListVal
        _recordVal = _recordListVal.addEnemyRecord(gameconst.EnemyRecordType.BE_KILL_BY_ENEMY, spaceNo)
        avatar.client.onNewEnemyRecord(gbId, _recordVal.toEnemyRecordSavedDict())

        self._autoPopEnemy(avatar)

    def updateEnemyLastFindInfo(self, gbId, spaceNo):
        _relationEnemyVal = self.enemyDict.get(gbId)
        if not _relationEnemyVal:
            return

        _relationEnemyVal.lastFindSpaceNo = spaceNo
        _relationEnemyVal.lastFindTime = utils.curTS()
        _relationEnemyVal.lastScheduleTime = utils.curTS()

    def scheduleEnemyLastFindInfo(self, gbId, spaceNo):
        _relationEnemyVal = self.enemyDict.get(gbId)
        if not _relationEnemyVal:
            return

        _relationEnemyVal.lastFindSpaceNo = spaceNo
        _relationEnemyVal.lastScheduleTime = utils.curTS()

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
            if _enemyVal:
                _enemyVal.updateFromFcVal(_fcVal)

            _killVal = self.killDict.get(_fcVal.gbId)
            if _killVal and _killVal.updateFromFcVal(_fcVal):
                self.updateRecordListByFcVals(_fcVal)

    def updateRecordListByFcVals(self, fcVals):
        for _recordVal in self.recordList:
            if _recordVal['gbId'] == fcVals.gbId:
                _recordVal.update({
                    'name': fcVals.name,
                    'school': fcVals.school,
                    'level': fcVals.level,
                })
    
    def getEnemyFreshInfo(self):
        return [enemy.toEnemyFreshInfo() for enemy in self.enemyDict.values()]
    
    def getNeedUpdateEnemyIds(self, login):
        _now = utils.curTS()
        _activeList = []
        _updateList = []
        for _relationEnemyVal in self.enemyDict.values():
            if _relationEnemyVal.lastFindTime == 0 or _relationEnemyVal.lastFindTime + gameconst.ONE_MINUTE_COST_SECONDS * 10 < _now:
                continue
            _activeList.append(_relationEnemyVal.gbId)
            if login or _relationEnemyVal.lastScheduleTime + RC_RCD.datas['enemyPositionRefreshTime']['value'] <= _now:
                _updateList.append(_relationEnemyVal.gbId)

        return _activeList, _updateList
    
    def getEnemyLastSpaceNo(self, gbId):
        _relationEnemyVal = self.enemyDict.get(gbId)
        if not _relationEnemyVal:
            return 0

        return _relationEnemyVal.lastFindSpaceNo

class EnemyMgrInfo(object):
    def createObjFromDict(self, dataDict):
        obj = EnemyMgrVal(**dataDict)
        return obj

    def getDictFromObj(self, obj):
        return obj.toEnemyMgrSavedDict()

    def isSameType(self, obj):
        return type(obj) is EnemyMgrVal


EnemyMgrInstance = EnemyMgrInfo()

