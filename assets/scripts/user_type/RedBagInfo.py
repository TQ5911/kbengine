# coding: utf-8
import KBEngine
from KBEDebug import *

import userType
import utils
import functools
import redisUtils
import gameglobal
import gameengine
import gameconst
import json
import random
import chatConfig_chatConfig as CC_CCD


class FetchPlayerVal(userType.UserSingleType):
    """RED_BAG_FETCH_PLAYER_VAL"""
    def __init__(self, playerGbId=0, name='', money=0, fetchTime=0):
        self.playerGbId = playerGbId
        self.name = name
        self.money = money
        self.fetchTime = fetchTime

    def initFromDict(self, dataDic):
        self.playerGbId = dataDic['playerGbId']
        self.name = dataDic['name']
        self.money = dataDic['money']
        self.fetchTime = dataDic['fetchTime']
        return self
    
    def toSaveDict(self):
        return {
            'playerGbId': self.playerGbId,
            'name': self.name,
            'money': self.money,
            'fetchTime': self.fetchTime,
        }
    
    def toClientDict(self):
        return {
            'playerGbId': self.playerGbId,
            'name': self.name,
            'money': self.money,
        }
    def toEncodeData(self):
        return json.dumps(self.toSaveDict())

class RedBagFetchVal(userType.UserSingleType):
    """RED_BAG_FETCH_VAL"""
    def __init__(self):
        self.fetchPlayerDict = {}
        self.maxGbId = 0
        self.maxMoney = 0

    def initFromDict(self, dataDic):
        for playerId, playerVal in dataDic.items():
            _PVal = FetchPlayerVal().initFromDict(playerVal)
            self.fetchPlayerDict[int(playerId)] = _PVal
            if self.maxMoney < _PVal.money:
                self.maxMoney = _PVal.money
                self.maxGbId = _PVal.playerGbId

        return self
    
    def toSaveDict(self):
        return {i.playerGbId: i.toSaveDict() for i in self.fetchPlayerDict.values()}
        
    
    def toClientDict(self):
        return {
            'maxGbId': self.maxGbId,
            'fetchPlayerList': [i.toClientDict() for i in self.fetchPlayerDict.values()],
        }
    
    def toEncodeData(self):
        return json.dumps(self.toSaveDict())
    
    def toDecodeData(self, data):
        dataDic = {}
        for k, v in data.items():
            dataDic[int(k)] = json.loads(v)
        return self.initFromDict(dataDic)

    def hasFetched(self, playerGbId):
        return playerGbId in self.fetchPlayerDict

    def doFetch(self, playerGbId, name, _money):
        LOG_IFO('doFetch: playerGbId=%d name=%s _money=%d' % (playerGbId, name, _money))

        if self.hasFetched(playerGbId):
            LOG_DBG('doFetch: playerGbId=%d already fetch' % playerGbId)
            return None
        if self.maxMoney < _money:
            self.maxMoney = _money
            self.maxGbId = playerGbId
        _FpVal = FetchPlayerVal(playerGbId, name, _money, utils.curTS())
        self.fetchPlayerDict[playerGbId] = _FpVal

        return _FpVal

class RedBagVal(userType.UserSingleType):
    """RED_BAG_VAL"""
    def __init__(self, redbagId=0, playerGbId=0, playerName='', guildUUID=0, redbagType=0, channel=0, money=0, leftMoney=0, num=0, leftNum=0, releaseTime=0, desc=u''):
        self.redbagId = redbagId
        self.playerGbId = playerGbId
        self.playerName = playerName
        self.guildUUID = guildUUID
        self.redbagType = redbagType
        self.channel = channel
        self.money = money
        self.leftMoney = leftMoney
        self.num = num
        self.leftNum = leftNum
        self.releaseTime = releaseTime
        self.desc = desc

    def toSaveDict(self):
        return {
            'redbagId': self.redbagId,
            'playerGbId': self.playerGbId,
            'playerName': self.playerName,
            'guildUUID': self.guildUUID,
            'redbagType': self.redbagType,
            'channel': self.channel,
            'money': self.money,
            'leftMoney': self.leftMoney,
            'num': self.num,
            'leftNum': self.leftNum,
            'releaseTime': self.releaseTime,
            'desc': self.desc,
        }
    
    def toClientDict(self):
        return {
            'redbagId': self.redbagId,
            'playerGbId': self.playerGbId,
            'playerName': self.playerName,
            'guildUUID': self.guildUUID,
            'redbagType': self.redbagType,
            'channel': self.channel,
            'money': self.money,
            'leftMoney': self.leftMoney,
            'num': self.num,
            'leftNum': self.leftNum,
            'desc': self.desc,
            'hasFetch': 0,
        }

    def getLeftNum(self):
        return self.leftNum
    
    def isExpire(self):
        return utils.curTS() >= self.releaseTime + CC_CCD.datas['returnPacketTime']['value'] * 3600
    
    # 检查条件 需前置判断
    def doFetchRedBag(self, playerGbId):
        _money = 0
        if self.redbagType == gameconst.RedBagType.NORMAL:
            _money = int(self.money // self.num)
            #_money = int(self.money / self.num + 0.5) # 四舍五入
        elif self.redbagType == gameconst.RedBagType.LUCKLY:
            _money = min(self.leftMoney // self.leftNum * 2, self.leftMoney)
            if _money > 1:
                _money = random.randint(1, _money)
            # 保证剩余的次数，每次至少可领一块钱
            _money = min(_money, self.leftMoney - self.leftNum + 1)

        if self.leftNum == 1:
            _money = self.leftMoney
        elif _money < 1:
            _money = 1

        if self.leftMoney < _money:
            LOG_DBG('RedBagVal::doFetchRedBag: leftMoney < _money', self.leftMoney, _money)
            return 0

        self.leftNum -= 1
        self.leftMoney -= _money

        return _money

class RedBagData(object):
    def createObjFromDict(self, dataDict):
        obj = RedBagVal(**dataDict)
        return obj
    
    def getDictFromObj(self, obj):
        return obj.toSaveDict()
    
    def isSameType(self, obj):
        return type(obj) is RedBagVal

RedBagDataInstance = RedBagData()

class RedBagDataVal(userType.UserDictType):
    """RED_BAG_DATA_INFO"""
    def __init__(self, redbags):
        for _gmVal in redbags:
            self[_gmVal.redbagId] = _gmVal

    def toSaveDict(self):
        return {
            'redbags': list(self.values()),
        }

class RedBagDataInfo(object):
    def createObjFromDict(self, dataDict):
        redbags = dataDict['redbags']
        obj = RedBagDataVal(redbags)
        return obj
    
    def getDictFromObj(self, obj):
        return obj.toSaveDict()
    
    def isSameType(self, obj):
        return type(obj) is RedBagDataVal
    
RedBagDataInfoInstance = RedBagDataInfo()
    
