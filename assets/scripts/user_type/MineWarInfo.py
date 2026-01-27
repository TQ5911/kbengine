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
import copy
import random
import GuildEventLogInfo
import mineBattle_config as MBC

class MineWarGuildVal():
    def __init__(self, guildGbId=0, guildName='', guildIcon=0, guildDspFlag=0):
        self.guildGbId = guildGbId
        self.guildName = guildName
        self.guildDspFlag = guildDspFlag
        self.guildIcon = guildIcon
        self.revenue = 0  # 帮派在矿战中的总收益
        self.ownerTime = 0
        self.ownerTimeStamp = 0
        self.leaderName = ''
        
    def toSaveDict(self):
        return {
            'guildGbId': self.guildGbId,
            'guildName': self.guildName,
            'guildIcon': self.guildIcon,
            'guildDspFlag': self.guildDspFlag,
            'leaderName': self.leaderName,
            'revenue': int(self.revenue),
            'ownerTime': self.ownerTime,
            'ownerTimeStamp': self.ownerTimeStamp,
        }
        
    def initFromDict(self, dataDic):
        self.guildGbId = dataDic.get('guildGbId', 0)
        self.guildName = dataDic.get('guildName', '')
        self.guildIcon = dataDic.get('guildIcon', 0)
        self.guildDspFlag = dataDic.get('guildDspFlag', 0)
        self.leaderName = dataDic.get('leaderName', '')
        self.revenue = dataDic.get('revenue', 0)
        self.ownerTime = dataDic.get('ownerTime', 0)
        self.ownerTimeStamp = dataDic.get('ownerTimeStamp', 0)

        return self
    
class MineWarScore:
    def __init__(self, gbId=0, name='', guildGbId=0, guildName='', guildIcon=0, guildDspFlag=0):
        self.gbId = gbId
        self.name = name
        self.guildGbId = guildGbId
        self.guildName = guildName
        self.guildIcon = guildIcon
        self.guildDspFlag = guildDspFlag
        self._killScore = 0
        self._destroyScore = 0
        self._hurtScore = 0

    @property
    def destroyScore(self):
        return self._destroyScore + self._hurtScore
    @property
    def killScore(self):
        return self._killScore
    @property
    def totalScore(self):
        return self._killScore + self.destroyScore

    def toSaveDict(self):
        return {
            'gbId': self.gbId,
            'name': self.name,
            'guildGbId': self.guildGbId,
            'guildName': self.guildName,
            'guildIcon': self.guildIcon,
            'guildDspFlag': self.guildDspFlag,
            'killScore': self._killScore,
            'destroyScore': self._destroyScore,
            'hurtScore': self._hurtScore,
        }
    
    def initFromDict(self, dataDic):
        self.gbId = dataDic.get('gbId', 0)
        self.name = dataDic.get('name', '')
        self.guildGbId = dataDic.get('guildGbId', 0)
        self.guildName = dataDic.get('guildName', '')
        self.guildIcon = dataDic.get('guildIcon', 0)
        self.guildDspFlag = dataDic.get('guildDspFlag', 0)
        self._killScore = dataDic.get('killScore', 0)
        self._destroyScore = dataDic.get('destroyScore', 0)
        self._hurtScore = dataDic.get('hurtScore', 0)
        return self
        
    def getData(self):
        return {
            'gbId': self.gbId,
            'playerName': self.name,
            'guildGbId': self.guildGbId,
            'guildName': self.guildName,
            'guildIcon': self.guildIcon,
            'guildDspFlag': self.guildDspFlag,
            'killScore': self._killScore,
            'destroyScore': self.destroyScore,
            'totalScore': self.totalScore
        }
    def getScoreData(self):
        return {
            'playerGbId': self.gbId,
            'score': self.totalScore
        }
        
    def addScore(self, v, tp, reset=False):
        if tp == 0:
            self._hurtScore = v
        elif tp == 1:
            self._destroyScore += v
        else:
            self._killScore += v

class MineWarMapVal():
    """MINE_WAR_MAP_VAL"""
    def __init__(self, mapId):
        self.mapId = mapId
        self.guildGbId = 0
        self.tempGuildGbId = 0
        self.flagDestroyedNum = 0  # 旗帜被毁次数
        self.flagDestroyedTime = 0  # 旗帜最后被毁时间
        self.spaceMgrbox = None  # MineWarSpaceMgr的basebox引用
        self.guildOwnerDict = {}  # 帮派占领统计
        self.coreDestroyedTime = 0  # 核心被摧毁时间
        self.playerScoreDict = {}  # 帮派玩家得分统计
        self.scoreRankList = []  # 最终保存的矿战排名列表
        self.scoreRankListTemp = []  # 临时排名列表
        self.mineWarEvents = []  # 矿战事件列表
        self.currGuildInfo = MineWarGuildVal().initFromDict({})

        self.currCollectNum = 0
        self.allCollectNum = 0
        
        # 暂存
        self.ownerRankList = []
        self.ownerRankListLast = []
        self.flagHp = 0

        self.lastScoreRankTime = 0
        # INFO_MSG('MineWarMapVal.__init__: mapId={}'.format(self.mapId))
        
    def initFromDict(self, dataDic):
        self.mapId = dataDic.get('mapId', 0)
        self.guildGbId = dataDic.get('guildGbId', 0)
        self.tempGuildGbId = dataDic.get('tempGuildGbId', 0)
        self.flagDestroyedNum = dataDic.get('flagDestroyedNum', 0)
        self.flagDestroyedTime = dataDic.get('flagDestroyedTime', 0)
        self.spaceMgrbox = None
        self.coreDestroyedTime = 0
        self.mineWarEvents = dataDic.get('mineWarEvents', [])

        self.currCollectNum = dataDic.get('currCollectNum', 0)
        self.allCollectNum = dataDic.get('allCollectNum', 0)
        
        self.guildOwnerDict = {}
        temp = dataDic.get('guildOwnerList', [])
        for guildInfo in temp:
            guildVal = MineWarGuildVal().initFromDict(guildInfo)
            self.guildOwnerDict[guildVal.guildGbId] = guildVal

        temp = dataDic.get('playerScoreList', [])
        for scoreInfo in temp:
            scoreVal = MineWarScore().initFromDict(scoreInfo)
            self.playerScoreDict[scoreVal.gbId] = scoreVal
            
        for scoreInfo in dataDic.get('scoreRankList', []):
            scoreVal = MineWarScore().initFromDict(scoreInfo)
            self.scoreRankList.append(scoreVal)
        self.scoreRankListTemp = []


        currGuildInfoList = dataDic.get('currGuildInfo', [])
        self.currGuildInfo = MineWarGuildVal().initFromDict(currGuildInfoList[0] if len(currGuildInfoList) > 0 else {})
        # INFO_MSG('MineWarMapVal.initFromDict:', self.mapId, self.currGuildInfo)

        return self
    
    def toSaveDict(self):
        return {
            'mapId': self.mapId,
            'guildGbId': self.guildGbId,
            'tempGuildGbId': self.tempGuildGbId,
            'flagDestroyedNum': self.flagDestroyedNum,
            'flagDestroyedTime': self.flagDestroyedTime,
            'mineWarEvents': self.mineWarEvents,
            'guildOwnerList': [val.toSaveDict() for val in self.guildOwnerDict.values()],
            'playerScoreList': [val.toSaveDict() for val in self.playerScoreDict.values()],
            'scoreRankList': [val.toSaveDict() for val in self.scoreRankList],
            'currGuildInfo': [self.currGuildInfo.toSaveDict()],
            'currCollectNum': self.currCollectNum,
            'allCollectNum': self.allCollectNum,
        }
    
    def toClientDict(self):
        return {
            'mapId': self.mapId,
            'guildGbId': self.guildGbId,
            'tempGuildGbId': self.tempGuildGbId,
            'flagDestroyedNum': self.flagDestroyedNum,
            'flagDestroyedTime': self.flagDestroyedTime,
        }
    
    def onStartReset(self):
        self.coreDestroyedTime = utils.getNow()
        self.tempGuildGbId = self.guildGbId

        # 上期占领时间排行 暂存
        ownerList = list(self.guildOwnerDict.values())
        ownerList.sort(key=lambda x: x.ownerTime, reverse=True)
        ownerList = ownerList[:MBC.datas['mineBatte_rankGuildNum']['value']]
        self.ownerRankListLast = ownerList    # 暂存        

        self.guildOwnerDict = {}
        self.playerScoreDict = {}
        self.playerScoreList = {}
        # self.scoreRankList = []

        # 初始化归属帮派
        if self.currGuildInfo and self.currGuildInfo.guildGbId > 0:
            self.currGuildInfo.ownerTime = 0
            self.guildOwnerDict[self.currGuildInfo.guildGbId] = copy.deepcopy(self.currGuildInfo)
    
    # 主要的帮派ID
    def setGuildGbId(self, guildGbId):
        self.guildGbId = guildGbId

    def getGuildGbId(self):
        return self.guildGbId

    def getTempGuildGbId(self):
        return self.tempGuildGbId
    
    def calcOwnerTime(self):
        lastTime = self.coreDestroyedTime
        if self.tempGuildGbId > 0 and lastTime > 0:
            guildVal = self.guildOwnerDict[self.tempGuildGbId]
            guildVal.ownerTime += (utils.getNow() - lastTime)
            self.guildOwnerDict[self.tempGuildGbId] = guildVal
            self.coreDestroyedTime = utils.getNow()
    
    def onMineWarEnd(self):
        #
        self.flagDestroyedNum = 0
        self.flagDestroyedTime = 0
        
        # 矿产清除
        self.allCollectNum = 0
        self.calcOwnerTime()    # 先结算，再置0

        # 暂存帮派排名清除
        self.ownerRankList = []
        #
        if self.tempGuildGbId > 0:
            # 重置归属帮派收益
            self.currGuildInfo.revenue = int((MBC.datas['mineBattle_incomeCoefficient']['value'] - 1.0) * 100)

            if self.guildGbId != self.tempGuildGbId:
                self.guildGbId = self.tempGuildGbId
                # 归属帮派不需要该记录了 == todo=
                # if self.guildGbId in self.guildOwnerDict:
                #     del self.guildOwnerDict[self.guildGbId]
                INFO_MSG('MineWarMapVal.onMineWarEnd: ', self.currGuildInfo.toSaveDict(), self.guildOwnerDict[self.tempGuildGbId].toSaveDict())
                # 更新占领帮派
                self.currGuildInfo = self.guildOwnerDict.get(self.tempGuildGbId, MineWarGuildVal().initFromDict({}))
                self.mineWarEvents = []

                # 重置归属帮派收益
                self.currGuildInfo.revenue = int((MBC.datas['mineBattle_incomeCoefficient']['value'] - 1.0) * 100)
                return True
        
        return False
    
    def onFlagAllDestroyed(self):
        destroyCfg = MBC.datas['mineBattle_flagDamageEffect']['value']
        self.currGuildInfo.revenue -= destroyCfg[1]

    def setSpaceMgrbox(self, box):
        self.spaceMgrbox = box

    def getSpaceMgrbox(self):
        return self.spaceMgrbox
    
    def getFlagDestroyedNum(self):
        return self.flagDestroyedNum
    
    def getflagDestroyedTime(self):
        return self.flagDestroyedTime
    
    def getEvents(self):
        return self.mineWarEvents
    
    def addMineWarEvent(self, eventType, args):
        e = GuildEventLogInfo.GuildEventLogVal(eventType, args, utils.getTimestamp64())
        self.mineWarEvents.append(e)
        # 限制最大事件数量
        maxEvent = 20
        if len(self.mineWarEvents) > maxEvent:
            self.mineWarEvents = self.mineWarEvents[-maxEvent:]

    def onFlagBeDestroyed(self):
        self.flagDestroyedNum += 1
        self.flagDestroyedTime = utils.getNow()

    def onCoreBeKilled(self, guildInfo):
        self.calcOwnerTime()
        
        killGuildId = guildInfo['guildGbId']
        self.coreDestroyedTime = utils.getNow() # 这里必须设置被摧毁时间
        self.tempGuildGbId = killGuildId
        if killGuildId not in self.guildOwnerDict:
            self.guildOwnerDict[killGuildId] = MineWarGuildVal().initFromDict(guildInfo)
        # 更新占领时间
        self.guildOwnerDict[killGuildId].ownerTimeStamp = utils.getNow()
        # 保存当前帮派信息
        # self.currGuildInfo = self.guildOwnerDict[killGuildId]

    def addMineWarScoreVal(self, playerGbId, playerName, guildGbId, guildName, guildIcon, guildDspFlag, score, scoreType):
        if playerGbId not in self.playerScoreDict:
            self.playerScoreDict[playerGbId] = MineWarScore(playerGbId, playerName, guildGbId, guildName, guildIcon, guildDspFlag)

        scoreVal = self.playerScoreDict[playerGbId]
        # 修正
        if scoreVal.name != playerName:
            scoreVal.name = playerName
        if scoreVal.guildName != guildName:
            scoreVal.guildName = guildName
        if scoreVal.guildIcon != guildIcon:
            scoreVal.guildIcon = guildIcon
        if scoreVal.guildDspFlag != guildDspFlag:
            scoreVal.guildDspFlag = guildDspFlag

        scoreVal.addScore(score, scoreType)
        self.playerScoreDict[playerGbId] = scoreVal

        INFO_MSG('MineWarMapVal.addMineWarScoreVal: mapId={}, playerGbId={}, score={}, scoreType={}, totalScore={}'.format(
            self.mapId, playerGbId, score, scoreType, scoreVal.totalScore))
        
    def addCollectNum(self, num):
        self.currCollectNum += num

    def onCollectEnd(self):
        revenue = MBC.datas['mineBattle_extraIncome']['value'] * 0.01
        self.allCollectNum += int(self.currCollectNum * revenue)
        self.currCollectNum = 0
        INFO_MSG('MineWarMapVal.onCollectEnd: ', self.mapId, revenue, self.allCollectNum)
        
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
