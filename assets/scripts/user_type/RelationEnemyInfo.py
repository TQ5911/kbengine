
# coding: utf-8

import userType
import utils
import relationConfig_relationConfig as RC_RCD

class EnemyRecordVal(userType.UserSoleType):
    '''ENEMY_RECORD_DATA_INFO'''
    def __init__(self, ts=0, type=0, spaceNo=0):
        self.ts = ts
        self.type = type
        self.spaceNo = spaceNo

    def toEnemyRecordSavedDict(self):
        return {
            'ts': self.ts,
            'type': self.type,
            'spaceNo': self.spaceNo,
        }
    

class EnemyRecordListVal(userType.UserSoleType):
    def __init__(self, gbId=0, recordList=()):
        self.gbId = gbId
        self.recordList = []
        for record in recordList:
            self.recordList.append(EnemyRecordVal(**record))

    def addEnemyRecord(self, type, spaceNo):
        _recordVal = EnemyRecordVal(utils.getNow(), type, spaceNo)
        self.recordList.append(_recordVal)

        while len(self.recordList) > RC_RCD.datas['enemyRecordNumLimit']['value']:
            self.recordList.pop(0)

        return _recordVal

    def toEnemyRecordListSavedDict(self):
        return {
            'gbId': self.gbId,
            'recordList': [record.toEnemyRecordSavedDict() for record in self.recordList]
        }


class RelationEnemyVal(userType.UserSoleType):
    '''RELATION_ENEMY_DATA_INFO'''
    def __init__(self, gbId=0, name='', school=0, level=0, sex=0, offlineTime=0, addTime=0, lastFindSpaceNo=0, lastFindTime=0, score=0):
        self.gbId = gbId
        self.name = name
        self.school = school
        self.level = level
        self.sex = sex
        self.offlineTime = offlineTime
        self.addTime = addTime
        self.lastFindSpaceNo = lastFindSpaceNo
        self.lastFindTime = lastFindTime
        self.score = score

    def updateFromFcVal(self, fcVal):
        self.level = fcVal.level
        self.score = fcVal.battleEffect
        if fcVal.isOnline:
            self.offlineTime = 0
        else:
            self.offlineTime = fcVal.offlineTime

    def toEnemyFreshInfo(self):
        return {
            'gbId': self.gbId,
            'offlineTime': self.offlineTime,
            'level': self.level,
            'score': self.score
        }
    
    # 小的会优先被删除掉
    def __lt__(self, other):
        if self.offlineTime == 0 and other.offlineTime == 0:
            return self.addTime < other.addTime
        elif self.offlineTime == 0:
            return False
        elif other.offlineTime == 0:
            return True
        else:
            return self.offlineTime < other.offlineTime

    def toRelationEnemySavedDict(self):
        return {
            'gbId': self.gbId,
            'name': self.name,
            'school': self.school,
            'level': self.level,
            'score': self.score,
            'offlineTime': self.offlineTime,
            'addTime': self.addTime,
            'lastFindSpaceNo': self.lastFindSpaceNo,
            'lastFindTime': self.lastFindTime,
            'sex': self.sex
        }


class RelationEnemyInfo(object):
    def createObjFromDict(self, dataDict):
        obj = RelationEnemyVal(**dataDict)
        return obj

    def getDictFromObj(self, obj):
        return obj.toRelationEnemySavedDict()

    def isSameType(self, obj):
        return type(obj) is RelationEnemyVal


RelationEnemyInstance = RelationEnemyInfo()

