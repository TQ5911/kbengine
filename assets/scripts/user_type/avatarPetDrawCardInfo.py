
# -*- encoding:utf-8 -*-

from KBEDebug import *
import KBEngine
import userType
import json
import utils
import gzip
from collections import deque

class cardPoolInfo(userType.UserSingleType):
    def __init__(self, pool=0, num=0, guaranteed=0, dailyNum=0, coinLeftTimes=0):
        self.pool = pool
        self.num = num
        self.guaranteed = guaranteed
        self.dailyNum = dailyNum
        self.coinLeftTimes = coinLeftTimes

    def initFromDict(self, dataDict):
        self.pool = dataDict['pool']
        self.num = dataDict['num']
        self.guaranteed = dataDict['guaranteed']
        self.dailyNum = dataDict['dailyNum']
        self.coinLeftTimes = dataDict['coinLeftTimes']

    def toStreamSavedDic(self):
        data = {
            'pool': self.pool,
            'num': self.num,
            'guaranteed': self.guaranteed,
            'dailyNum': self.dailyNum,
            'coinLeftTimes': self.coinLeftTimes,
        }
        return data

    def toClientDict(self):
        data = {
            'pool': self.pool,
            'num': self.num,
            'guaranteed': self.guaranteed,
            'dailyNum': self.dailyNum,
            'coinLeftTimes': self.coinLeftTimes,
        }
        return data

    def getLeftTimes(self, prop):
        return getattr(self, prop, -1)

    def hasLeftTimes(self, prop, value):
        if not hasattr(self, prop):
            return True
        return getattr(self, prop) >= value

    def updateLeftTimes(self, prop, value):
        if not hasattr(self, prop):
            return
        val = getattr(self, prop)
        setattr(self, prop, val + value)

class petDrawCardInfo(userType.UserSTSoleType):
    def __init__(self):
        self.cardPoolInfoDict = {}

    def initFromDict(self, dataDic):
        cardPoolInfoList = dataDic.get('cardPoolInfoList', [])
        for curInfo in cardPoolInfoList:
            info = cardPoolInfo()
            info.initFromDict(curInfo)
            self.cardPoolInfoDict[curInfo['pool']] = info
        return self

    def toStreamSavedDic(self):
        cardPoolInfoList = []
        for pool, info in self.cardPoolInfoDict.items():
            cardPoolInfoList.append(info.toStreamSavedDic())
        data = {
            'cardPoolInfoList': cardPoolInfoList,
        }
        return data

    def setdefault(self, pool, coinLeftTimes):
        return self.cardPoolInfoDict.setdefault(pool, cardPoolInfo(pool=pool, coinLeftTimes=coinLeftTimes))

class petDrawCardInfoInstance(userType.UserSTSoleInfo):
    @property
    def cls(self):
        return petDrawCardInfo

petDrawCardInfoInstance = petDrawCardInfoInstance()


class drawCardRecord(userType.UserSingleType):
    def __init__(self, id=0, ts=0, items=[]):
        self.id = id
        self.ts = ts
        self.items = items
        self.itemsBit = 0

    def initFromDict(self, dataDict):
        self.id = dataDict['id']
        self.ts = dataDict['ts']
        self.items = dataDict['items']

    def toStreamSavedDic(self):
        data = {
            'id': self.id,
            'ts': self.ts,
            'items': self.items,
        }
        return data

    def toClientDict(self):
        data = {
            'id': self.id,
            'ts': self.ts,
            'items': self.items,
        }
        return data

    def allBitSet(self):
        for idx in range(len(self.items)):
            self.itemsBit = utils.bset(self.itemsBit, idx + 1)

    def bhasSet(self, idx=0):
        if idx == 0:
            return self.itemsBit != 0
        return utils.bhas(self.itemsBit, idx)

    def resetBitSet(self, idx):
        self.itemsBit = utils.breset(self.itemsBit, idx)

    def getAllBitSet(self):
        idxList = []
        for idx in range(len(self.items)):
            if self.bhasSet(idx + 1):
                idxList.append(idx + 1)
        return idxList

    def checkBitSet(self, idx):
        return idx <= len(self.items)

class petDrawCardRecord(userType.UserSTSoleType):
    def __init__(self):
        self.drawCardRecordDic = {}
        self.clientDataDic = {}
        pass

    @classmethod
    def _checkIgnores_(cls):
        return 'clientDataDic',

    def initFromDict(self, dataDic):
        #LOG_DBG('init DrawCardRecord', dataDic)
        drawCardRecordList = dataDic.get('drawCardRecordList', [])
        for poolRecordData in drawCardRecordList:
            pool = poolRecordData['pool']
            recordDicList = poolRecordData['data']
            poolData, clientData = self.setdefault(pool)
            recordList = poolData["recordList"]
            for recordDict in recordDicList:
                record = drawCardRecord()
                record.initFromDict(recordDict)
                recordList.append(record)
            poolData["curCnt"] = len(recordList)
            poolData["totalCnt"] = poolRecordData['totalCnt']

        # 初始化前检测一次
        ts = utils.curTS()
        for pool in self.drawCardRecordDic.keys():
            self.checkCntLimit(pool)
            self.checkExpiredLimit(pool, ts)
        return self

    def toStreamSavedDic(self):
        # 落库前检测一次
        ts = utils.curTS()
        for pool in self.drawCardRecordDic.keys():
            self.checkCntLimit(pool)
            self.checkExpiredLimit(pool, ts)

        drawCardRecordList = []
        for pool, poolData in self.drawCardRecordDic.items():
            poolRecordData = {}
            recordDicList = []
            recordList = poolData["recordList"]
            for record in recordList:
                recordDicList.append(record.toStreamSavedDic())
            poolRecordData['pool'] = pool
            poolRecordData['curCnt'] = len(recordDicList)
            poolRecordData['totalCnt'] = poolData["totalCnt"]
            poolRecordData['data'] = recordDicList
            drawCardRecordList.append(poolRecordData)
        data = {
            'drawCardRecordList': drawCardRecordList,
        }
        #LOG_DBG('save DrawCardRecord', data)
        return data

    def toClientDict(self, pool):
        # 同步前检测一次
        poolData = self.drawCardRecordDic.get(pool, None)
        clientData = self.clientDataDic.get(pool, None)
        if not poolData or not clientData:
            poolData, clientData = self.setdefault(pool)

        ts = utils.curTS()
        self.checkCntLimit(pool)
        self.checkExpiredLimit(pool, ts)

        if not clientData["beUpdate"]:
            #LOG_DBG('update DrawCardRecord', clientData["clientData"])
            return clientData["clientData"]

        poolRecordData = {}
        recordDicList = []
        recordList = poolData["recordList"]
        for record in recordList:
            recordDicList.append(record.toClientDict())
        poolRecordData['pool'] = pool
        #poolRecordData['curCnt'] = len(recordDicList)
        #poolRecordData['totalCnt'] = poolData["totalCnt"]
        poolRecordData['data'] = recordDicList
        #LOG_DBG('client DrawCardRecord', poolRecordData)

        clientData["beUpdate"] = False
        clientData["clientData"] = poolRecordData

        #LOG_DBG('update DrawCardRecord', clientData["clientData"])
        return poolRecordData

    def setdefault(self, pool):
        poolData = dict()
        poolData["recordList"] = deque()
        poolData["curCnt"] = 0
        poolData["totalCnt"] = 0
        clientData = dict()
        clientData["beUpdate"] = True
        clientData["clientData"] = {}
        return self.drawCardRecordDic.setdefault(pool, poolData), self.clientDataDic.setdefault(pool, clientData)

    def appendRecord(self, pool, items):
        poolData = self.drawCardRecordDic.get(pool, None)
        clientData = self.clientDataDic.get(pool, None)
        if not poolData or not clientData:
            poolData, clientData = self.setdefault(pool)
        ts = utils.curTS()
        poolData["totalCnt"] += 1
        record = drawCardRecord(poolData["totalCnt"], ts, items)
        poolData['recordList'].appendleft(record)
        poolData["curCnt"] = len(poolData["recordList"])
        clientData["beUpdate"] = True
        self.checkCntLimit(pool)
        self.checkExpiredLimit(pool, ts)
        return record

    def checkCntLimit(self, pool):
        poolData = self.drawCardRecordDic.get(pool, None)
        clientData = self.clientDataDic.get(pool, None)
        if not poolData or not clientData:
            return
        recordList = poolData["recordList"]
        while len(recordList) > 500:
            recordList.pop()
            clientData["beUpdate"] = True
        poolData["curCnt"] = len(recordList)

    def checkExpiredLimit(self, pool, ts):
        expiredTime = 60 * 60 * 24 * 180
        poolData = self.drawCardRecordDic.get(pool, None)
        clientData = self.clientDataDic.get(pool, None)
        if not poolData or not clientData:
            return
        recordList = poolData["recordList"]
        while len(recordList) > 0:
            lastRecord = recordList[-1]
            if ts >= lastRecord.ts and ts - lastRecord.ts < expiredTime:
                break
            recordList.pop()
            clientData["beUpdate"] = True
        poolData["curCnt"] = len(recordList)

    def getStreamRecordData(self, pool):
        dic = self.toClientDict(pool)
        jsonStr = json.dumps(dic).encode('ascii')
        LOG_DBG('in getStreamRecordData, jsonStr:', len(jsonStr))
        zStr = gzip.compress(jsonStr)
        LOG_DBG('in getStreamRecordData, gzipStr:', len(zStr))
        return zStr

class petDrawCardRecordInstance(userType.UserSTSoleInfo):
    @property
    def cls(self):
        return petDrawCardRecord

petDrawCardRecordInstance = petDrawCardRecordInstance()

