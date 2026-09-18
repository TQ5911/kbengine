# coding: utf-8
import KBEngine
from KBEDebug import *

import gameconst
import userType

class enmityItem(userType.UserSingleType):
    def __init__(self, gbId=0, now=0):
        self.gbId = gbId
        self.name = ''
        self.school = 0
        self.level = 0
        self.sex = 0
        self.score = 0
        self.offlineTime = 0
        self.addTime = now

    @staticmethod
    def getModifyPropList():
        return (('name',), ('school',), ('level',), ('sex',), ('score', 'battleEffect'))

    def updateEnmityInfo(self, usersInfo):
        beUpdate = False
        modifyPropList = self.getModifyPropList()
        for modifyProp in modifyPropList:
            prop1 = modifyProp[0]
            if not hasattr(self, prop1):
                continue
            prop2 = modifyProp[1] if len(modifyProp) > 1 else prop1
            if not hasattr(usersInfo, prop2):
                continue
            oldVal = getattr(self, prop1)
            newVal = getattr(usersInfo, prop2)
            if oldVal == newVal:
                continue
            setattr(self, prop1, newVal)
            beUpdate = True

        offlineTime = self.offlineTime
        if usersInfo.isOnline:
            self.offlineTime = 0
        else:
            self.offlineTime = usersInfo.offlineTime
        if offlineTime != self.offlineTime:
            beUpdate = True

        return beUpdate

    def initFromDict(self, dataDict):
        self.gbId = dataDict['gbId']
        self.name = dataDict['name']
        self.school = dataDict['school']
        self.level = dataDict['level']
        self.sex = dataDict['sex']
        self.score = dataDict['score']
        self.offlineTime = dataDict['offlineTime']
        self.addTime = dataDict['addTime']

    def toStreamSavedDic(self):
        return {
            'gbId': self.gbId,
            'name': self.name,
            'school': self.school,
            'level': self.level,
            'sex': self.sex,
            'score': self.score,
            'offlineTime': self.offlineTime,
            'addTime': self.addTime,
        }

    def toStreamClientDic(self):
        return {
            'gbId': self.gbId,
            'name': self.name,
            'school': self.school,
            'level': self.level,
            'sex': self.sex,
            'score': self.score,
            'offlineTime': self.offlineTime,
            'addTime': self.addTime,
        }
    
class enmityInfo(userType.UserDictType):
    def __init__(self):
        LOG_DBG('enmityInfo::__init__')

    def initFromDict(self, dataDict):
        for item in dataDict['enmityList']:
            enmity = enmityItem()
            enmity.initFromDict(item)
            self[enmity.gbId] = enmity

    def toStreamSavedDic(self):
        enmityList = []
        for item in self.values():
            enmityList.append(item.toStreamSavedDic())

        dataDict = {
            'enmityList': enmityList,
        }
        return dataDict

    def getClientDatas(self, gbId=0):
        enmityList = []
        if gbId == 0:
            for item in self.values():
                enmityList.append(item.toStreamClientDic())
        elif gbId in self:
            enmityList.append(self[gbId].toStreamClientDic())
        return enmityList

    def hasAdded(self, gbId):
        return gbId in self

    def addOrUpdate(self, usersInfo, now):
        enmity = self.setdefault(usersInfo.gbId, enmityItem(usersInfo.gbId, now))
        beUpdate = enmity.updateEnmityInfo(usersInfo)
        return beUpdate, enmity.toStreamClientDic()

    def remove(self, gbId):
        enmity = self.pop(gbId, None)
        return enmity.toStreamClientDic() if enmity else None
    
    def getGbIds(self):
        return list(self.keys())
    
    def getSize(self):
        return len(self)

class enmityInstance(object):
    def createObjFromDict(self, dataDict):
        enmityInst = enmityInfo()
        enmityInst.initFromDict(dataDict)
        return enmityInst
    
    def getDictFromObj(self, obj):
        return obj.toStreamSavedDic()
    
    def isSameType(self, obj):
        return type(obj) is enmityInfo
    
enmityInfoInstance = enmityInstance()
