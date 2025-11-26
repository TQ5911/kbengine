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


class MineWarMapVal():
    """MINE_WAR_MAP_VAL"""
    def __init__(self, mapId):
        self.mapId = mapId
        self.guildGbId = 0
        self.tempGuildGbId = 0
        self.flagDestroyedNum = 0  # 旗帜被毁次数
        self.flagDestroyedTime = 0  # 旗帜最后被毁时间
        self.spaceMgrbox = None  # MineWarSpaceMgr的basebox引用
        self.guildOwnerTime = {}
        self.coreDestroyedTime = 0  # 核心被摧毁时间

    def initFromDict(self, dataDic):
        self.mapId = dataDic.get('mapId', 0)
        self.guildGbId = dataDic.get('guildGbId', 0)
        self.tempGuildGbId = dataDic.get('tempGuildGbId', 0)
        self.flagDestroyedNum = dataDic.get('flagDestroyedNum', 0)
        self.flagDestroyedTime = dataDic.get('flagDestroyedTime', 0)
        self.spaceMgrbox = None
        self.guildOwnerTime = dataDic.get('guildOwnerTime', {})
        self.coreDestroyedTime = 0
        return self
    
    def toSaveDict(self):
        return {
            'mapId': self.mapId,
            'guildGbId': self.guildGbId,
            'tempGuildGbId': self.tempGuildGbId,
            'flagDestroyedNum': self.flagDestroyedNum,
            'flagDestroyedTime': self.flagDestroyedTime,
            'guildOwnerTime': self.guildOwnerTime,
        }
    
    def toClientDict(self):
        return {
            'mapId': self.mapId,
            'guildGbId': self.guildGbId,
            'tempGuildGbId': self.tempGuildGbId,
            'flagDestroyedNum': self.flagDestroyedNum,
            'flagDestroyedTime': self.flagDestroyedTime,
            'guildOwnerTime': self.guildOwnerTime,
        }
    
    def onStartReset(self):
        self.flagDestroyedNum = 0
        self.flagDestroyedTime = 0
        self.coreDestroyedTime = 0
        self.tempGuildGbId = 0
        self.guildOwnerTime = {}
    
    # 主要的帮派ID
    def setGuildGbId(self, guildGbId):
        self.guildGbId = guildGbId

    def getGuildGbId(self):
        return self.guildGbId
    
    # 当前战斗临时帮派ID
    def setTempGuildGbId(self, guildGbId):
        self.tempGuildGbId = guildGbId

    def getTempGuildGbId(self):
        return self.tempGuildGbId
    
    def onMineWarEnd(self):
        #
        self.flagDestroyedNum = 0
        self.flagDestroyedTime = 0
        self.coreDestroyedTime = 0
        #
        if self.tempGuildGbId > 0 and self.guildGbId != self.tempGuildGbId:
            self.guildGbId = self.tempGuildGbId
            # 归属帮派不需要该记录了
            self.guildOwnerTime.pop(self.guildGbId)
            return True
        return False

    
    def setSpaceMgrbox(self, box):
        self.spaceMgrbox = box

    def getSpaceMgrbox(self):
        return self.spaceMgrbox
    
    def getFlagDestroyedNum(self):
        return self.flagDestroyedNum
    
    def getflagDestroyedTime(self):
        return self.flagDestroyedTime
    
    def onFlagBeDestroyed(self):
        self.flagDestroyedNum += 1
        self.flagDestroyedTime = utils.getNow()

    def onCoreBeKilled(self, killerGuildGbId):
        lastTime = self.coreDestroyedTime
        if killerGuildGbId not in self.guildOwnerTime:
            self.guildOwnerTime[killerGuildGbId] = 0

        if lastTime > 0:
            self.guildOwnerTime[self.tempGuildGbId] += (utils.getNow() - lastTime)

        self.coreDestroyedTime = utils.getNow()
        self.tempGuildGbId = killerGuildGbId
    

class MineWarMapInfo(userType.UserSoleType):
    """MINE_WAR_MAP_INFO"""
    def createObjFromDict(self, dataDic):
        obj = MineWarMapVal(dataDic['mapId'])
        obj.initFromDict(dataDic)
        return obj
    
    def getDictFromObj(self, obj):
        return obj.toSaveDict()

    def isSameType(self, obj):
        return type(obj) is MineWarMapVal
    
MineWarMapInstance = MineWarMapInfo()

class MineWarDataVal(userType.UserDictType):
    def __init__(self, mineWarData):
        for _Val in mineWarData:
            self[_Val.mapId] = _Val

    def toSaveDict(self):
        return {
            'mineWarData': list(self.values()),
        }
    
class MineWarDataInfo(userType.UserSoleType):
    """MINE_WAR_DATA_INFO"""
    def createObjFromDict(self, dataDic):
        mineWarData = dataDic.get('mineWarData', [])
        obj = MineWarDataVal(mineWarData)
        return obj
    
    def getDictFromObj(self, obj):
        return obj.toSaveDict()
    
    def isSameType(self, obj):
        return type(obj) is MineWarDataVal
    
MineWarDataInstance = MineWarDataInfo()