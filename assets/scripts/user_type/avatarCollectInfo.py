
# -*- encoding:utf-8 -*-

from KBEDebug import *
import KBEngine
import userType

class collectItem(userType.UserSoleType):
    def __init__(self, collectibleID):
        self.collectibleID = collectibleID 
        # 这里的state用来记录客户端的收藏操作和服务端的任务进度
        # 收藏操作占用最高位，任务进度从低位开始记录
        self.state = 0

    def _lateReload(self):
        super(collectItem, self)._lateReload()

    # db -> obj
    def initFromDict(self, dataDict):
        self.collectibleID = dataDict['collectibleID']
        self.state = dataDict['state']

    # obj -> db
    def toSavedDict(self):
        return {
            'collectibleID': self.collectibleID,
            'state': self.state
        }

    def isCompleteAt(self, required):
        if not 0<=required<=14:
            WARNING_MSG('in isCompleteAt, required exceed :', required)
            return False
        mask = (1<<required)
        return (self.state & mask) == mask

    def isCompleteAll(self, required):
        if not 0<=required<=14:
            WARNING_MSG('in isCompleteAll, required exceed :', required)
            return False
        mask = (1<<required) - 1
        return (self.state & mask) == mask

    def onComplete(self, grid):
        self.state |= (1<<grid)

    def onMark(self, isMark):
        if isMark:
            self.state |= (1<<15)
        else:
            self.state &= ~(1<<15)
        

class collectInfo(userType.UserSoleType):
    def __init__(self, *args, **kwargs):
        super(collectInfo, self).__init__(*args, **kwargs)
        self.collectibleDict = {} 

    def _lateReload(self):
        super(collectInfo, self)._lateReload()
        for k,v in self.collectibleDict.items():
            v.reloadScript()

    # db -> obj
    def initFromDict(self, dataDict):
        for data in dataDict['collectibleList']:
            collectible = collectItem(data['collectibleID'])
            collectible.initFromDict(data)
            self.collectibleDict[data['collectibleID']] = collectible

    # obj -> db
    def toSavedDict(self):
        collectibleList = []
        for data in self.collectibleDict.values():
            collectibleList.append(data.toSavedDict())
        return {
            'collectibleList': collectibleList,
        }

class collectInstance(object):
    def createObjFromDict(self, dataDict):
        collectInstance = collectInfo()
        collectInstance.initFromDict(dataDict)
        return collectInstance

    def getDictFromObj(self, obj):
        return obj.toSavedDict()

    def isSameType(self, obj):
        return type(obj) is collectInfo

collectInfoInstance = collectInstance()