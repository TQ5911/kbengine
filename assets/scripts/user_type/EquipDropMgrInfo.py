
# coding: utf-8
import utils
import userType
import gameconst
import gameengine
import EquipDropInfo
import EquipDropTakerInfo

import gearBase_gearConst as GB_GCD


class EquipDropMgrTimerData(userType.UserSoleType):
    def __init__(self, uniqueId=0, endTime=0):
        self.uniqueId = uniqueId
        self.endTime = endTime

    def toEquipDropMgrTimerDataSavedDict(self):
        return {
            "uniqueId": self.uniqueId,
            "endTime": self.endTime,
        }


class EquipDropMgrVal(userType.UserSoleType):
    '''EQUIP_DROP_MGR_DATA_INFO'''
    def __init__(self, dropList=(), takerList=(), takerWaitList=(), lockTime=0, timerData=None):
        self.dropDic = {}
        for _dropVal in dropList:
            self.dropDic[_dropVal.uniqueId] = _dropVal

        self.takerDict = {}
        for _takerVal in takerList:
            self.takerDict[_takerVal.uniqueId] = _takerVal

        self.takerWaitDict = {}
        for _takerWaitVal in takerWaitList:
            self.takerWaitDict[_takerWaitVal.uniqueId] = _takerWaitVal

        self.lockTime = lockTime

        self.timerList = []

        if timerData:
            for _data in timerData:
                self.timerList.append(EquipDropMgrTimerData(**_data))


    def addNotifyDropFixTimer(self, uniqueId, endTime):
        for i in range(len(self.timerList) - 1, -1, -1):
            if endTime < self.timerList[i].endTime:
                self.timerList.insert(i + 1, EquipDropMgrTimerData(uniqueId, endTime))
                return

        self.timerList.insert(0, EquipDropMgrTimerData(uniqueId, endTime))

    def firstTimerVal(self):
        if not self.timerList:
            return None

        return self.timerList[0]
    
    def popFirstTimerVal(self):
        if not self.timerList:
            return None

        return self.timerList.pop(0)

    def onDropTypeChange(self, uniqueId, dropType):
        _dropVal = self.dropDic.get(uniqueId, None)
        if not _dropVal:
            return

        _dropVal.state = dropType

    def fetchNeedRemoveDropEquip(self):
        _val = None
        for _dropVal in list(self.dropDic.values()):
            if _val is None or _val > _dropVal:
                _val = _dropVal

        return _val
    
    def dropNum(self):
        return len(self.dropDic)

    def addNewDrop(self, 
                   avatar, 
                   uniqueId, 
                   price, 
                   mapId, 
                   pos, 
                   equipInfo, 
                   collEndTime, 
                   killerName,
                   endTime,
                   dropType,
                   isNotify):
        _dropVal = EquipDropInfo.EquipDropVal(
            uniqueId, 
            price, 
            dropType,
            mapId,
            pos,
            equipInfo,
            collEndTime,
            killerName,
            endTime,
        )
        self.dropDic[uniqueId] = _dropVal
        if isNotify:
            avatar.client.onAddNewEquipDrop(_dropVal)

    def getDropList(self):
        return list(self.dropDic.keys())
    
    def clearEndTimeVals(self):
        _now = utils.getNow()
        for _dropVal in list(self.dropDic.values()):
            if _dropVal.state not in (gameconst.DropType.TYPE_DROP, gameconst.DropType.TYPE_TAKE):
                continue

            if _dropVal.endTime < _now:
                self.dropDic.pop(_dropVal.uniqueId, None)

        for _takerVal in list(self.takerDict.values()):
            if _takerVal.state not in (gameconst.DropType.TYPE_TAKE, gameconst.DropType.TYPE_GIVEUP):
                continue

            if _takerVal.endTime < _now:
                self.takerDict.pop(_takerVal.uniqueId, None)

    def getTakeList(self):
        return list(self.takerDict.keys())

    def getDropVal(self, uniqueId):
        return self.dropDic.get(uniqueId, None)

    def getTakerVal(self, uniqueId):
        return self.takerDict.get(uniqueId, None)

    def addTaker(self, avatar, uniqueId, equip, endTime, state, price, isNotify):
        _takerVal = EquipDropTakerInfo.EquipDropTakerVal(uniqueId, equip, endTime, state, price)
        self.takerDict[uniqueId] = _takerVal
        if isNotify:
            avatar.client.onPickNewEquipDrop(_takerVal)

    def addTakerWait(self, uniqueId, equip, endTime, price):
        _takerWaitVal = EquipDropTakerInfo.EquipDropTakerVal(uniqueId, equip, endTime, gameconst.DropType.TYPE_REDEEM, price)
        self.takerWaitDict[uniqueId] = _takerWaitVal

    def removeTaker(self, avatar, uniqueId, isNotify=True):
        _takerVal = self.takerDict.pop(uniqueId, None)
        if isNotify:
            avatar.client.onRemovePickEquipDrop(uniqueId)
        return _takerVal
    
    def removeTakerWait(self, avatar, uniqueId):
        _takerWaitVal = self.takerWaitDict.pop(uniqueId, None)
        avatar.client.onRemovePickEquipDrop(uniqueId)
        return _takerWaitVal
    
    def doDealDropEquipExpire(self, avatar):
        _endTime = utils.getNow() + 5
        for _dropVal in list(self.dropDic.values()):
            if _dropVal.endTime < _endTime:
                gameengine.getGlobalBase('DropStub').doCheckDropExpire(_dropVal.uniqueId, avatar.gbID, avatar)

        for _takerVal in list(self.takerDict.values()):
            if _takerVal.endTime < _endTime:
                gameengine.getGlobalBase('DropStub').doCheckDropExpire(_takerVal.uniqueId, avatar.gbID, avatar)

    def checkCouldTakeDrop(self, uniqueId):
        if uniqueId in self.dropDic:
            return True

        if len(self.takerDict) + len(self.takerWaitDict) >= GB_GCD.datas['pickListFullNum']['value']:
            return False

        return True

    def hasTakeDrop(self, uniqueId):
        return uniqueId in self.takerDict

    def hasDrop(self, uniqueId):
        return uniqueId in self.dropDic

    def removeDrop(self, avatar, uniqueId):
        _dropVal = self.dropDic.pop(uniqueId, None)
        avatar.client.onRemoveEquipDrop(uniqueId)
        return _dropVal

    def tryLock(self):
        _now = utils.getNow()
        if self.lockTime > _now:
            return False

        self.lockTime = _now + 60
        return True
    
    def unlock(self):
        self.lockTime = 0

    def toEquipDropMgrSavedDict(self):
        return {
            "dropList": [dropVal for dropVal in self.dropDic.values()],
            "takerList": [takerVal for takerVal in self.takerDict.values()],
            "takerWaitList": [takerWaitVal for takerWaitVal in self.takerWaitDict.values()],
            "lockTime": self.lockTime,
            "timerData": [timerData.toEquipDropMgrTimerDataSavedDict() for timerData in self.timerList],
        }


class EquipDropMgrInfo(object):
    def createObjFromDict(self, dataDict):
        obj = EquipDropMgrVal(**dataDict)
        return obj

    def getDictFromObj(self, obj):
        return obj.toEquipDropMgrSavedDict()

    def isSameType(self, obj):
        return type(obj) is EquipDropMgrVal


EquipDropMgrInstance = EquipDropMgrInfo()

