# coding: utf-8
import KBEngine
from KBEDebug import *

import gameconst
import userType

class bountyItem(userType.UserSingleType):
    def __init__(self, uuid=0, gbid=0):
        self.uuid = uuid
        self.timestamp = 0
        self.leftTime = 0
        self.acceptedLeftTime = 0
        self.bountyType = 0
        self.publishMoney = 0
        self.depositMoney = 0
        self.totalMoney = 0
        self.flag = 0
        self.state = 0

        self.gbid = gbid
        self.name = ''
        self.school = 0

        self.preyGbId = 0
        self.preyName = ''
        self.preySchool = 0

        self.hunterGbId = 0
        self.hunterName = ''
        self.hunterSchool = 0

        self.preyOnline = False
        self.preyLevel = 0
        self.preyScore = 0
        self.preyPos = (0, 0, 0)
        self.preySpaceNo = 0

        # other
        self.checkNameList = []
        self.expiredTimestamp = 0
        self.lastCheckExpiredTimestamp = 0
        self.waitForCheckBits = [[False, False], [True, True], [False, False]]
        self.waitForCheckTimerId = 0
        self.needUpdate = False

    def __lt__(self, other):
        return self.expiredTimestamp < other.expiredTimestamp

    def updateAvatarInfo(self, prop, value):
        if not hasattr(self, prop):
            return []
        setattr(self, prop, value)
        return [self.gbid, self.preyGbId, self.hunterGbId]

    def refreshTime(self, now):
        if self.state == gameconst.BountyState.PUBLISHED:
            self.refreshLeftTime(now)
        elif self.state == gameconst.BountyState.ACCEPTED:
            self.refreshAcceptLeftTime(now)

    def refreshLeftTime(self, now):
        if self.leftTime <= 0:
            return
        elapsedTime = now - self.lastCheckExpiredTimestamp
        self.lastCheckExpiredTimestamp = now
        if self.leftTime <= elapsedTime:
            self.leftTime = 0
        else:
            self.leftTime -= elapsedTime

    def refreshAcceptLeftTime(self, now):
        if self.acceptedLeftTime <= 0:
            return
        elapsedTime = now - self.lastCheckExpiredTimestamp
        self.lastCheckExpiredTimestamp = now
        if self.acceptedLeftTime <= elapsedTime:
            self.acceptedLeftTime = 0
        else:
            self.acceptedLeftTime -= elapsedTime

    def isAllTypeBitsChecked(self):
        return len(self.getNotCheckedTypeBitIdxs(0)) == 0
    
    def isAllResBitsChecked(self):
        return len(self.getNotCheckedTypeBitIdxs(1)) == 0

    def getNotCheckedTypeBitIdxs(self, type):
        return [idx for idx, info in enumerate(self.waitForCheckBits) if not info[type]]

    def setBitCheckedByIdx(self, idx, res):
        if idx >= len(self.waitForCheckBits) or idx < 0:
            return [False, False]
        if idx == 1:
            return self.waitForCheckBits[1]

        res = False if not res else True
        self.waitForCheckBits[idx] = [True, res]
        return self.waitForCheckBits[idx]

    def initFromDict(self, dataDict):
        self.uuid = dataDict['uuid']
        self.timestamp = dataDict['timestamp']
        self.leftTime = dataDict['leftTime']
        self.acceptedLeftTime = dataDict['acceptedLeftTime']
        self.bountyType = dataDict['bountyType']
        self.publishMoney = dataDict['publishMoney']
        self.depositMoney = dataDict['depositMoney']
        self.totalMoney = dataDict['totalMoney']
        self.flag = dataDict['flag']
        self.state = dataDict['state']

        self.gbid = dataDict['gbid']
        self.name = dataDict['name']
        self.school = dataDict['school']
        
        self.preyGbId = dataDict['preyGbId']
        self.preyName = dataDict['preyName']
        self.preySchool = dataDict['preySchool']

        self.hunterGbId = dataDict['hunterGbId']
        self.hunterName = dataDict['hunterName']
        self.hunterSchool = dataDict['hunterSchool']
    
    def toSavedDict(self):
        return {
            'uuid': self.uuid,
            'timestamp': self.timestamp,
            'leftTime': self.leftTime,
            'acceptedLeftTime': self.acceptedLeftTime,
            'bountyType' : self.bountyType,
            'publishMoney' : self.publishMoney,
            'depositMoney' : self.depositMoney,
            'totalMoney' : self.totalMoney,
            'flag' : self.flag,
            'state' : self.state,

            'gbid': self.gbid,
            'name': self.name,
            'school': self.school,

            'preyGbId': self.preyGbId,
            'preyName': self.preyName,
            'preySchool': self.preySchool,

            'hunterGbId': self.hunterGbId,
            'hunterName': self.hunterName,
            'hunterSchool': self.hunterSchool,
        }

    def initFromSyncDict(self, syncDict):
        self.initFromDict(syncDict['baseInfo'])
        self.preyOnline = syncDict['preyOnline']

    def toSyncDict(self):
        syncDict = {}
        syncDict['baseInfo'] = self.toSavedDict()
        syncDict['preyOnline'] = self.preyOnline
        return syncDict

    def toClientDict(self):
        clientDict = {}
        clientDict['baseInfo'] = self.toSavedDict()
        clientDict['preyOnline'] = self.preyOnline
        clientDict['preyLevel'] = self.preyLevel
        clientDict['preyScore'] = self.preyScore
        clientDict['preyPos'] = self.preyPos
        clientDict['preySpaceNo'] = self.preySpaceNo
        return clientDict
    
class bountyInfo(userType.UserDictType):
    def __init__(self):
        DEBUG_MSG('bountyInfo::__init__')

    def initFromDict(self, dataDict):
        DEBUG_MSG('bountyInfo::initFromDict', dataDict['bountyList'])
        for item in dataDict['bountyList']:
            bounty = bountyItem()
            bounty.initFromDict(item)
            self[bounty.uuid] = bounty

    def toSavedDict(self):
        bountyList = []
        for item in self.values():
            bountyList.append(item.toSavedDict())

        dataDict = {
            'bountyList': bountyList,
        }
        DEBUG_MSG('bountyInfo::toSavedDict', dataDict)
        return dataDict

    def toSyncDict(self):
        bountyList = []
        for item in self.values():
            bountyList.append(item.toSyncDict())

        dataDict = {
            'bountyList': bountyList,
        }
        DEBUG_MSG('bountyInfo::toSyncDict', dataDict)
        return dataDict
    
class bountyInstance(object):
    def createObjFromDict(self, dataDict):
        bountyInstance = bountyInfo()
        bountyInstance.initFromDict(dataDict)
        return bountyInstance
    
    def getDictFromObj(self, obj):
        return obj.toSavedDict()
    
    def isSameType(self, obj):
        return type(obj) is bountyInfo
    
bountyInfoInstance = bountyInstance()

##############################################################
class hunterRankItem(userType.UserSingleType):
    def __init__(self, hunterGbId=0, hunterName='', online=False):
        self.hunterGbId = hunterGbId
        self.hunterName = hunterName
        self.successedCnt = 0
        self.failedCnt = 0
        self.lastUpdateTimestamp = 0

        self.online = online

        # other
        self.isInList = False

    def updateRankInfo(self, isSuccess, now, rankData):
        if isSuccess:
            self.successedCnt += 1
        else:
            self.failedCnt += 1
        self.lastUpdateTimestamp = now
        rankData.update(self)

    def updateAvatarInfo(self, prop, value, rankData):
        if not hasattr(self, prop):
            return []
        setattr(self, prop, value)
        rankData.update(self)
        return [self.hunterGbId]
    
    def initFromDict(self, dataDict):
        self.hunterGbId = dataDict['hunterGbId']
        self.hunterName = dataDict['hunterName']
        self.successedCnt = dataDict['successedCnt']
        self.failedCnt = dataDict['failedCnt']
        self.lastUpdateTimestamp = dataDict['lastUpdateTimestamp']
    
    def toSavedDict(self):
        return {
            'hunterGbId': self.hunterGbId,
            'hunterName': self.hunterName,
            'successedCnt': self.successedCnt,
            'failedCnt': self.failedCnt,
            'lastUpdateTimestamp': self.lastUpdateTimestamp,
        }

    def initFromSyncDict(self, syncDict):
        self.initFromDict(syncDict['baseInfo'])

    def toSyncDict(self):
        syncDict = {}
        syncDict['baseInfo'] = self.toSavedDict()
        return syncDict

    def toClientDict(self):
        '''
        data = {
            'id': self.hunterGbId,
            'name': self.hunterName,
            'scnt': self.successedCnt,
        }
        return data
        '''
        clientDict = {}
        clientDict['baseInfo'] = self.toSavedDict()
        clientDict["online"] = self.online
        return clientDict

class hunterRankInfo(userType.UserDictType):
    def __init__(self):
        DEBUG_MSG('hunterRankInfo::__init__')

    def initFromDict(self, dataDict):
        DEBUG_MSG('hunterRankInfo::initFromDict', dataDict['hunterRankList'])
        for rankItem in dataDict['hunterRankList']:
            hunterRank = hunterRankItem()
            hunterRank.initFromDict(rankItem)
            self[hunterRank.hunterGbId] = hunterRank

    def toSavedDict(self):
        hunterRankList = []
        for rankItem in self.values():
            hunterRankList.append(rankItem.toSavedDict())

        dataDict = {
            'hunterRankList': hunterRankList,
        }
        DEBUG_MSG('hunterRankInfo::toSavedDict', dataDict)
        return dataDict

    def toSyncDict(self):
        hunterRankList = []
        for rankItem in self.values():
            hunterRankList.append(rankItem.toSyncDict())

        dataDict = {
            'hunterRankList': hunterRankList,
        }
        DEBUG_MSG('hunterRankInfo::toSyncDict', dataDict)
        return dataDict
    
class hunterRankInstance(object):
    def createObjFromDict(self, dataDict):
        hunterRankInstance = hunterRankInfo()
        hunterRankInstance.initFromDict(dataDict)
        return hunterRankInstance
    
    def getDictFromObj(self, obj):
        return obj.toSavedDict()
    
    def isSameType(self, obj):
        return type(obj) is hunterRankInfo
    
hunterRankInfoInstance = hunterRankInstance()

##############################################################
class rankData(object):
    def __init__(self, brType):
        self.brType = brType
        self.beUpdate = True
        self.versionId = 1
        self.rankList = []
        self.clientData = {}
        DEBUG_MSG('rankData::__init__', self.brType)

    def __str__(self):
        return f'rankData(brType={self.brType}, beUpdate={self.beUpdate}, versionId={self.versionId}, rankList={self.rankList})'

    def update(self, rankItem):
        self.append(rankItem)

    def append(self, rankItem):
        self.beUpdate = True
        self.versionId += 1
        if rankItem.isInList:
            return

        rankItem.isInList = True
        self.rankList.append(rankItem)

    def sort(self):
        self.rankList.sort(key=self.sortKeyFunc())

    def sortKeyFunc(self):
        return None

    def toClientDict(self):
        if self.beUpdate:
            self.clientData["type"] = self.brType
            self.clientData["vId"] = self.versionId
            rankList = []
            for rankItem in self.rankList[0:100]:
                rankList.append(rankItem.toClientDict())
            self.clientData['list'] = rankList

        self.beUpdate = False
        return self.clientData

class hunterRankData(rankData):
    def __init__(self, brType=0):
        rankData.__init__(self, brType)
        DEBUG_MSG('hunterRankData::__init__')

    def sortKeyFunc(self):
        return lambda x: (-x.successedCnt, x.failedCnt, x.lastUpdateTimestamp)
