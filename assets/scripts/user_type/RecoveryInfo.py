# coding: utf-8
import KBEngine
from KBEDebug import *

import gameconst
from collections import deque
import userType
import json
import utils
import gameconfig
import math
import welfare_resourceRecovery as W_RR


class freeTicketRecoveryItem(userType.UserSingleType):
    def __init__(self):
        LOG_DBG("freeTicketRecoveryItem::__init__")
        self.rType = gameconst.ResourceRecoveryType.FREE_TICKET
        self.dateNumDeques = [deque() for _ in range(gameconst.FreeTicketSubType.MAX_CNT)]

    def initFromDict(self, dataDict):
        LOG_DBG("freeTicketRecoveryItem::initFromDict", dataDict)
        self.rType = dataDict['rType']

        dateNumInfoStr = dataDict['dateNumInfo']
        if not dateNumInfoStr:
            dateNumInfoStr = '{}'
        dateNumInfo = json.loads(dateNumInfoStr)
        for subType, dateNumDictList in dateNumInfo.items():
            for dateNumDict in dateNumDictList:
                self.dateNumDeques[int(subType)].append([dateNumDict['date'], dateNumDict['num']])
        return self

    def toSavedDict(self):
        dataDict = {}
        dataDict['rType'] = self.rType
        dateNumInfo = {}
        
        for subType, dateNumQueue in enumerate(self.dateNumDeques):
            dateNumDictList = []
            for (date, num) in dateNumQueue:
                dateNumDictList.append({'date': date, 'num': num})
            dateNumInfo[subType] = dateNumDictList
        
        dateNumInfoStr = json.dumps(dateNumInfo)
        dataDict['dateNumInfo'] = dateNumInfoStr
        LOG_DBG("ResourceRecoveryStub::toSavedDict", dataDict)
        return dataDict

    def update(self, now, subType, nowDateTime, curNum):
        cfgData = W_RR.datas.get(subType + 1, {})
        if not cfgData:
            LOG_ERR("freeTicketRecoveryItem::update no cfg", subType + 1)
            return
        N = cfgData['time']
        LOG_INFO("freeTicketRecoveryItem::update", self.dateNumDeques[subType], now, subType, nowDateTime, curNum, N)
        if not self.dateNumDeques[subType]:
            LOG_DBG("freeTicketRecoveryItem::no data1")
            serverOpenTimestamp = gameconfig.serverOpenTime()
            serverOpenDateTime = utils.getIntDateTime(serverOpenTimestamp)
            diffDays = math.floor((now - serverOpenTimestamp) / 86400)
            LOG_INFO("freeTicketRecoveryItem::update no data2", utils.getSvrOpenDayFiveTS(), serverOpenTimestamp, serverOpenDateTime, nowDateTime, diffDays)
            if diffDays <= N:
                if serverOpenDateTime == nowDateTime:
                    self.dateNumDeques[subType].append([serverOpenDateTime, curNum])
                    LOG_DBG("freeTicketRecoveryItem::update no data3 1", (serverOpenDateTime, curNum))
                else:
                    self.dateNumDeques[subType].append([serverOpenDateTime, curNum])
                    self.dateNumDeques[subType].append([nowDateTime, curNum])
                    LOG_DBG("freeTicketRecoveryItem::update no data4 2", [serverOpenDateTime, curNum], [nowDateTime, curNum])
            else:
                offsetSeconds = 86400 * N
                firstDataTimestamp = now - offsetSeconds
                firstDateTime = utils.getIntDateTime(firstDataTimestamp)
                self.dateNumDeques[subType].append([firstDateTime, curNum])
                self.dateNumDeques[subType].append([nowDateTime, curNum])
                LOG_DBG("freeTicketRecoveryItem::update no data5 2", [firstDateTime, curNum], [nowDateTime, curNum])
            return True
        LOG_DBG("freeTicketRecoveryItem::update has data")

        lastData = self.dateNumDeques[subType][-1]
        LOG_INFO("freeTicketRecoveryItem::update has data1", lastData, nowDateTime, curNum)
        if nowDateTime < lastData[0]:
            LOG_ERR("freeTicketRecoveryItem::update has data2")
            return False

        if lastData[0] == nowDateTime:
            LOG_DBG("freeTicketRecoveryItem::update has data3")
            if lastData[1] == curNum:
                pass
            else:
                lastData[1] = curNum
            return False
        else:
            LOG_DBG("freeTicketRecoveryItem::_update has data4", self.dateNumDeques[subType], nowDateTime, curNum)
            if lastData[1] == curNum:
                LOG_DBG("freeTicketRecoveryItem::_update has data5")
                lastData[0] = nowDateTime
            else:
                LOG_DBG("freeTicketRecoveryItem::_update has data6")
                self.dateNumDeques[subType].append([nowDateTime, curNum])
            self._update(subType, nowDateTime, curNum, N)
            return True

    def _update(self, subType, nowDateTime, curNum, N):
        LOG_INFO("freeTicketRecoveryItem::_update", subType, self.dateNumDeques[subType], nowDateTime, curNum)
        if not self.dateNumDeques[subType]:
            LOG_ERR("freeTicketRecoveryItem::_update1")
            return

        lastData = self.dateNumDeques[subType][-1]
        lastDataTimestamp = utils.getIntTimestamp(str(lastData[0]) + gameconst.RESOURCE_RECOVER_TIME_POINT_STR)
        lastFirstData = None
        LOG_DBG("freeTicketRecoveryItem::_update2", lastData, lastDataTimestamp, lastFirstData, self.dateNumDeques[subType])
        while self.dateNumDeques[subType]:
            firstData = self.dateNumDeques[subType][0]
            firstDataTimestamp = utils.getIntTimestamp(str(firstData[0]) + gameconst.RESOURCE_RECOVER_TIME_POINT_STR)
            diffDays = math.floor((lastDataTimestamp - firstDataTimestamp) / 86400)
            LOG_DBG("freeTicketRecoveryItem::_update3 diffDays", firstData, diffDays)
            if diffDays <= N:
                LOG_DBG("freeTicketRecoveryItem::_update3 N")
                break
            lastFirstData = self.dateNumDeques[subType].popleft()

        LOG_DBG("freeTicketRecoveryItem::_update4", lastFirstData, self.dateNumDeques[subType])
        if not lastFirstData:
            return
        if not self.dateNumDeques[subType]:
            LOG_ERR("freeTicketRecoveryItem::_update5")
            return
        curFirstData = self.dateNumDeques[subType][0]
        curFirstDataTimestamp = utils.getIntTimestamp(str(curFirstData[0]) + gameconst.RESOURCE_RECOVER_TIME_POINT_STR)
        diffDays = math.floor((lastDataTimestamp - curFirstDataTimestamp) / 86400)
        LOG_DBG("freeTicketRecoveryItem::_update5", curFirstData, curFirstDataTimestamp, diffDays)
        if diffDays == N:
            LOG_DBG("freeTicketRecoveryItem::_update5 N")
            return
        offsetSecondsN = 86400 * N
        newFirstDataTimestamp = lastDataTimestamp - offsetSecondsN
        newFirstDateTime = utils.getIntDateTime(newFirstDataTimestamp)
        newFirstNum = lastFirstData[1]
        newFirstData = [newFirstDateTime, newFirstNum]
        LOG_DBG("freeTicketRecoveryItem::_update6", lastDataTimestamp, newFirstDataTimestamp, newFirstDateTime, newFirstNum, lastFirstData, newFirstData)
        self.dateNumDeques[subType].appendleft(newFirstData)
        LOG_DBG("freeTicketRecoveryItem::_update7", self.dateNumDeques[subType])


    def getData(self, subType):
        return list(self.dateNumDeques[subType])

class resourceRecoveryInfo(userType.UserSingleType):
    def __init__(self):
        LOG_DBG('resourceRecoveryInfo::__init__')
        self.ftRecoveryItem = freeTicketRecoveryItem()

    def initFromDict(self, dataDict):
        LOG_DBG('resourceRecoveryInfo::initFromDict', dataDict)
        self.ftRecoveryItem.initFromDict(dataDict['freeTicket'])
        return self

    def toSavedDict(self):
        dataDict = {}
        freeTicket = self.ftRecoveryItem.toSavedDict()
        dataDict['freeTicket'] = freeTicket
        LOG_DBG("toSavedDict", dataDict)
        return dataDict

class resourceRecoveryInstance(object):
    def createObjFromDict(self, dataDict):
        info = resourceRecoveryInfo()
        info.initFromDict(dataDict)
        return info
    
    def getDictFromObj(self, obj):
        return obj.toSavedDict()
    
    def isSameType(self, obj):
        return type(obj) is resourceRecoveryInfo
    
resourceRecoveryInfoInstance = resourceRecoveryInstance()
