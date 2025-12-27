# -*- coding: utf-8 -*-
from KBEDebug import *

import collections

import utils

import gameconst
import gameengine
import formula
import userType

import gamePlay_gamePlay as DDL


class DungeonSpaceVal(userType.UserSoleType):
    SPACE_STATE_INIT = 1
    SPACE_STATE_DURING = 2
    SPACE_STATE_COMPLETE = 3
    SPACE_STATE_TO_DESTORY = 4
    SPACE_STATE_FAILED = 5

    def __init__(self, spaceNo, spaceUUID, spaceBox, spaceMgr, spaceLevel=1, extraPropsDic = {}, dungeonSpaceValType=gameconst.DungeonSpaceValType.NONE):
        self.spaceNo = spaceNo
        self.spaceUUID = spaceUUID
        self.spaceBox = spaceBox
        self.spaceMgr = spaceMgr
        self.spaceLevel = spaceLevel
        self.tCreate = utils.getNow()
        self.nDestoryCnt = 0
        self.destroyTimer = 0
        self.completeDungeonTimer = 0
        self.loadingDungeonEntitiesTimerDic = {}
        self.loadDungeonEntitiesCheckTimerDic = {}
        self.state = self.SPACE_STATE_DURING
        self.src = 0
        self.extraProps = extraPropsDic
        self.dungeonSpaceValType = dungeonSpaceValType

    def isActive(self):
        return self.state == self.SPACE_STATE_DURING

    def completeDungeon(self, win=True):
        self.state = self.SPACE_STATE_COMPLETE if win else self.SPACE_STATE_FAILED

    def isCompleted(self):
        return self.state in (self.SPACE_STATE_COMPLETE, self.SPACE_STATE_FAILED)

    def isFailed(self):
        return self.state == self.SPACE_STATE_FAILED

    def toDestoryDungeon(self):
        self.state = self.SPACE_STATE_TO_DESTORY

    def isToDestory(self):
        return self.state == self.SPACE_STATE_TO_DESTORY

    def getRemainTime(self, dungeonNo=None):
        dungeonNo = dungeonNo or formula.getMapId(self.spaceNo)

        if dungeonNo not in DDL.datas:
            ERROR_MSG('Can\'t find dungeonNo in dungeonInfo: {}'.format(dungeonNo))
            return 0

        timeout = DDL.datas[dungeonNo]['timeOut'] * 60
        lostT = utils.getNow() - self.tCreate

        remainT = int(timeout - lostT)

        # remain time should not less than zero
        return remainT if remainT > 0 else 0

    def cancelCompleteTimer(self, owner, tag):
        if self.completeDungeonTimer:
            owner._cancelCallback(self.completeDungeonTimer, tag)
        self.clearCompleteTimer()

    def clearCompleteTimer(self):
        self.completeDungeonTimer = 0

    def getElapsedTime(self):
        return utils.getNow() - self.tCreate

# ======================================================
# Dungeon Monster Creator TimeLine Structure
# ======================================================

class DungeonSpaceTimeLineMixin(object):
    def __init__(self, dungeonTimeLineDic=None, killSum=0):
        self.dungeonTimeLineDic = dungeonTimeLineDic or {}
        self.dungeonCreepBaseKillDic = {}
        self.killSum = killSum

    def addTimeLine(self, flagId, *args, **kwargs):
        if 'flagId' in kwargs:
            del kwargs['flagId']
        self.dungeonTimeLineDic[flagId] = DungeonSpaceTimeLineVal(
            flagId, *args, **kwargs)

    def getTimeLine(self, flagId):
        if flagId in self.dungeonTimeLineDic:
            return self.dungeonTimeLineDic[flagId]

    def addKill(self, flagId, addKillSumFlag=True):
        if flagId in self.dungeonTimeLineDic:
            self.dungeonTimeLineDic[flagId].kills += 1
            if addKillSumFlag:
                self.killSum += 1

    def addKillByCreepBaseId(self, creepBaseId, addKillSumFlag=True):
        if creepBaseId not in self.dungeonCreepBaseKillDic:
            self.dungeonCreepBaseKillDic[creepBaseId] = 0
        self.dungeonCreepBaseKillDic[creepBaseId] += 1
        if addKillSumFlag:
            self.killSum += 1

    def getCreepBaseKilledNum(self, creepBaseId):
        return self.dungeonCreepBaseKillDic.get(creepBaseId, 0)

    def clearKills(self, flagId):
        if flagId in self.dungeonTimeLineDic:
            sumKill = self.killSum - self.dungeonTimeLineDic[flagId].kills
            self.killSum = sumKill if sumKill > 0 else 0
            self.dungeonTimeLineDic[flagId].kills = 0


class DungeonSpaceTimeLineVal(userType.UserSoleType):
    def __init__(self, flagId=0, refreshCount=0, nextRefreshTime=0, stopRefresh=False, kills=0):
        self.flagId = flagId
        self.refreshCount = refreshCount
        self.nextRefreshTime = nextRefreshTime
        self.stopRefresh = stopRefresh
        self.kills = kills

    def updateRefreshTime(self, newTime):
        self.nextRefreshTime = newTime
        self.refreshCount += 1

    def stop(self):
        self.stopRefresh = True

# ======================================================


# ======================================================
# 副本刷怪队列
# ======================================================

class DungeonEntityDefine(object):
    def __init__(self, entType='', entProps=None, loadStatus=gameconst.DungeonEntityLoadStatus.UNLOAD):
        self.entType = entType
        self.entProps = entProps or {}
        self.loadStatus = loadStatus


class DungeonEntityGeneratorVal(object):
    def __init__(self, genUUID, entityList, withBase=False, extra=None):
        self.genUUID = genUUID
        self.entityList = entityList    # type: list[DungeonEntityDefineStruct,]
        self.withBase = withBase
        self.extra = extra or {}

    def getEntityNum(self):
        return len(self.entityList)

    def isAllEntityLoaded(self):
        for entVal in self.entityList:
            if entVal.loadStatus != gameconst.DungeonEntityLoadStatus.LOADED:
                return False
        return True

    def getEntityStatusVal(self, status):
        _num = 0
        for entVal in self.entityList:
            if entVal.loadStatus != status:
                _num += 1
        return _num


class DungeonEntityGeneratorQueueMixin(object):
    def __init__(self, dungeonEntityGenerateQueue=None):
        self.dungeonEntityGenerateQueue = dungeonEntityGenerateQueue or collections.OrderedDict()
        self.dungeonEntityCreatingQueue = collections.OrderedDict()
        self._gameEntityIdentifyIDReversedDict = {}
        self._gameEntityIdReversedDict = {}

    def isNeedCreateEntity(self):
        if self.dungeonEntityGenerateQueue or self.dungeonEntityCreatingQueue:
            return True
        return False

    def isCreatingEntity(self):
        for genVal in self.dungeonEntityCreatingQueue.values():
            if genVal.getEntityStatusVal(gameconst.DungeonEntityLoadStatus.UNLOAD) > 0:
                return True
        return False

    def isFlagIdInEntityGenerator(self, flagId):
        if flagId not in self._gameEntityIdReversedDict:
            return False
        if not self._gameEntityIdReversedDict[flagId]:
            return False
        return True

    def clearEntityGeneratorQueue(self):
        self.dungeonEntityGenerateQueue.clear()
        self.dungeonEntityCreatingQueue.clear()
        self._gameEntityIdentifyIDReversedDict.clear()
        self._gameEntityIdReversedDict.clear()

    def addEntityGeneratorVal(self, val: DungeonEntityGeneratorVal):
        if val.genUUID in self.dungeonEntityGenerateQueue or val.genUUID in self.dungeonEntityCreatingQueue:
            return

        self.dungeonEntityGenerateQueue[val.genUUID] = val

        for entVal in val.entityList:
            self._gameEntityIdentifyIDReversedDict[entVal.entProps["gameEntityIdentifyID"]] = val.genUUID
            _gid = utils.getGidFromGameEntityId(entVal.entProps["gameEntityId"])
            self._gameEntityIdReversedDict.setdefault(_gid, set()).add(val.genUUID)

    def popEntityGeneratorVal(self, genUUID, default=None):
        _isCreating = genUUID in self.dungeonEntityCreatingQueue
        _isQueue = genUUID in self.dungeonEntityGenerateQueue
        if not (_isCreating or _isQueue):
            return default

        if _isCreating:
            val = self.dungeonEntityCreatingQueue.pop(genUUID)

        if _isQueue:
            val = self.dungeonEntityGenerateQueue.pop(genUUID)

        for entVal in val.entityList:
            self._gameEntityIdentifyIDReversedDict.pop(entVal.entProps["gameEntityIdentifyID"], None)
            _gid = utils.getGidFromGameEntityId(entVal.entProps["gameEntityId"])
            self._gameEntityIdReversedDict.get(_gid, set()).discard(genUUID)
        return val


    def makeNextEntityGeneratorValInCreatingQueue(self, default=None):
        if not self.dungeonEntityGenerateQueue:
            return default

        genUUID, val = self.dungeonEntityGenerateQueue.popitem(last=False)
        self.dungeonEntityCreatingQueue[genUUID] = val
        return val

    def onDungeonEntityCreated(self, gameEntityIdentifyID):
        if gameEntityIdentifyID not in self._gameEntityIdentifyIDReversedDict:
            ERROR_MSG("DungeonEntityGeneratorQueueMixin::onDungeonEntityCreated:: gameEntityIdentifyID not found",
                      gameEntityIdentifyID, self._gameEntityIdentifyIDReversedDict)
            return

        genUUID = self._gameEntityIdentifyIDReversedDict[gameEntityIdentifyID]
        if genUUID in self.dungeonEntityCreatingQueue:
            val = self.dungeonEntityCreatingQueue[genUUID]
        else:
            val = self.dungeonEntityGenerateQueue[genUUID]

        for entVal in val.entityList:
            if entVal.entProps["gameEntityIdentifyID"] == gameEntityIdentifyID:
                entVal.loadStatus = gameconst.DungeonEntityLoadStatus.LOADED

        if val.isAllEntityLoaded():
            self.popEntityGeneratorVal(genUUID)

        return val

# ======================================================


#----------------------------单人副本----------------------------------------------
class SingleDungeonSpaceVal(DungeonSpaceVal, DungeonSpaceTimeLineMixin, DungeonEntityGeneratorQueueMixin):
    def __init__(self, spaceNo, spaceUUID, spaceBox, spaceMgr, ownerGbId, spaceLevel=1):
        super(SingleDungeonSpaceVal, self).__init__(spaceNo, spaceUUID, spaceBox, spaceMgr, spaceLevel=spaceLevel,dungeonSpaceValType=gameconst.DungeonSpaceValType.SINGLE)
        super(DungeonSpaceVal, self).__init__()
        super(DungeonSpaceTimeLineMixin, self).__init__()

        self.ownerGbId = ownerGbId
        self.homeEnts = []

class SingleDungeonFounders(userType.UserDictType):
    def addFounder(self, spaceNo, spaceUUID, playerGbId, playerBox):
        key = self.getFounderKey(playerGbId, spaceUUID)
        self[key] = SingleDungeonFounderVal(spaceNo, spaceUUID, playerGbId, playerBox)

    def getFounderVal(self, playerGbId, spaceUUID):
        key = self.getFounderKey(playerGbId, spaceUUID)
        if key in self:
            return self[key]
        return None

    def destoryFounder(self, playerGbId, spaceUUID):
        key = self.getFounderKey(playerGbId, spaceUUID)
        self.pop(key, None)

    def getFounderKey(self, playerGbId, spaceUUID):
        return playerGbId, spaceUUID

class SingleDungeonFounderVal(userType.UserSoleType):
    def __init__(self, spaceNo, spaceUUID, playerGbId, playerBox, tEnter=0, tLeave=0):
        self.spaceNo = spaceNo
        self.spaceUUID = spaceUUID
        self.playerGbId = playerGbId
        self.playerBox = playerBox
        self.tEnter = tEnter
        self.tLeave= tLeave

    def onAvatarEnter(self, gbId):
        if gbId == self.playerGbId:
            self.tEnter = utils.getNow()
            self.tLeave = 0

    def onAvatarLeave(self, gbId, isOffline=False):
        if gbId == self.playerGbId:
            self.tEnter = 0
            self.tLeave = utils.getNow()
            if isOffline:
                self.playerBox = None

    def hasAvatar(self):
        return self.tEnter and not self.tLeave

class SingleDungeonFoundersInfo(userType.UserDictType):
    def createObjFromDict(self, dict):
        founders = SingleDungeonFounders()

        for fVal in dict['founders']:
            founders.addFounder(fVal['spaceNo'], fVal['spaceUUID'], fVal['playerGbId'], fVal['playerBox'], fVal['tEnter'], fVal['tLeave'])

        return founders

    def getDictFromObj(self, obj):
        d = {'founders': []}
        founders = d['founders']

        for fVal in obj.values():
            founders.append({
                'spaceNo':fVal.spaceNo,
                'spaceUUID':fVal.spaceUUID,
                'playerGbId':fVal.playerGbId,
                'playerBox': fVal.playerBox,
                'tEnter':fVal.tEnter,
                'tLeave':fVal.tLeave,
            })

        return d

    def isSameType(self, obj):
        return type(obj) is SingleDungeonFounders

SingleDungeonFoundersInstance = SingleDungeonFoundersInfo()

#----------------------------队伍副本--------------------------------------------------------
class TeamDungeonSpaceVal(DungeonSpaceVal, DungeonSpaceTimeLineMixin, DungeonEntityGeneratorQueueMixin):
    def __init__(self, spaceNo, spaceUUID, spaceBox, spaceMgr, teamUUID, spaceLevel=1,extraDic={}):
        super(TeamDungeonSpaceVal, self).__init__(spaceNo, spaceUUID, spaceBox, spaceMgr, spaceLevel,extraDic,dungeonSpaceValType=gameconst.DungeonSpaceValType.TEAM)
        super(DungeonSpaceVal, self).__init__()
        super(DungeonSpaceTimeLineMixin, self).__init__()
        self.teamUUID=teamUUID
        self.markCreate = True
        self.markDestroy = 0
        self.homeEnts = []


# ----------------------------------------------------------------------
# 团队副本
# ----------------------------------------------------------------------

class RaidDungeonSpaceVal(DungeonSpaceVal, DungeonSpaceTimeLineMixin, DungeonEntityGeneratorQueueMixin):
    """RaidStub 团队副本Space结构体"""

    def __init__(self, spaceNo, spaceUUID, spaceBox, spaceMgr, raidUUID, spaceLevel=1):
        super(RaidDungeonSpaceVal, self).__init__(spaceNo, spaceUUID, spaceBox, spaceMgr, spaceLevel,dungeonSpaceValType=gameconst.DungeonSpaceValType.RAID)
        super(DungeonSpaceVal, self).__init__()
        super(DungeonSpaceTimeLineMixin, self).__init__()
        self.founders = RaidDungeonFounders()
        self.raidUUID = raidUUID
        self.homeEnts = []
        self.tMarkDestroy = 0            # 标记删除时间, 在该时间内保证玩家可以安全离开副本space, 最后销毁副本
        self.raidSrc = 0
        self.extraProps = {}

    def _lateReload(self):
        self.founders.reloadScript()

    def getAllPlayerGbidAndNamePair(self):
        result = []
        for i in self.founders.values():
            if i.playerName:
                result.append((i.playerGBID, i.playerName))
        return result

class RaidDungeonFounders(userType.UserDictType):
    """RaidStub 团队副本中存在成员集合字典"""

    def _lateReload(self):
        for founderVal in self.values():
            founderVal.reloadScript()

    def isNoFounders(self):
        for founderVal in self.values():
            if founderVal.hasAvatar():
                return False
        return True

    def addFounder(self, spaceNo, spaceUUID, playerGBID, playerBox):
        self[playerGBID] = RaidDungeonFounderVal(spaceNo, spaceUUID, playerBox, playerGBID)

    def getFounderVal(self, playerGBID):
        return self[playerGBID] if playerGBID in self else None

    def destoryFounder(self, playerGBID):
        self.pop(playerGBID, None)


class RaidDungeonFounderVal(userType.UserSoleType):
    """RaidStub 团队副本中存在成员结构体"""

    def __init__(self, spaceNo, spaceUUID, playerBox, playerGBID, tEnter=0, tLeave=0,
                 playerName=""):
        self.spaceNo = spaceNo
        self.spaceUUID = spaceUUID
        self.playerBox = playerBox
        self.playerGBID = playerGBID
        self.tEnter = tEnter            # 进入时间
        self.tLeave = tLeave            # 离开时间
        self.playerName = playerName

    def onAvatarEnter(self, gbId):
        if gbId == self.playerGBID:
            self.tEnter = utils.getNow()
            self.tLeave = 0

    def onAvatarLeave(self, gbId, isOffline=False):
        if gbId == self.playerGBID:
            self.tEnter = 0
            self.tLeave = utils.getNow()
            if isOffline:
                self.playerBox = None

    def hasAvatar(self):
        return self.tEnter and not self.tLeave

class BaseDungeonFoundersMixin(userType.UserSoleType):
    def __init__(self):
        self.founders = DungeonFounderVals()
    
    def _lateReload(self):
        self.founders.reloadScript()

class BaseDungeonStatisticFoundersMixin(userType.UserSoleType):
    def __init__(self):
        self.statisticFounders = DungeonStatisticFounderVals()
        self.statisticBatchCount = 0
        self.sortedStatisticFoundersRankCache = None
    
    def refreshFoundersSortRankCache(self):
        self.sortedStatisticFoundersRankCache = self.statisticFounders.getSortRankFounders()

    def _lateReload(self):
        self.statisticFounders.reloadScript()
    
class GuildBossDungeonSpaceVal(DungeonSpaceVal, DungeonSpaceTimeLineMixin, DungeonEntityGeneratorQueueMixin, BaseDungeonFoundersMixin, BaseDungeonStatisticFoundersMixin):
    def __init__(self, spaceNo, spaceUUID, spaceBox, spaceMgr, guildUUID, guildBox=None, spaceLevel=1,extraDic={},
                school = 0, avatarLv = 0, avatarSex = 0, avatarGbId = 0, avatarId = 0):
        DungeonSpaceVal.__init__(self, spaceNo, spaceUUID, spaceBox, spaceMgr, spaceLevel, extraDic, dungeonSpaceValType=gameconst.DungeonSpaceValType.GUILD_BOSS)
        DungeonSpaceTimeLineMixin.__init__(self)
        DungeonEntityGeneratorQueueMixin.__init__(self)
        BaseDungeonFoundersMixin.__init__(self)
        BaseDungeonStatisticFoundersMixin.__init__(self)
        self.guildUUID = guildUUID
        self.markCreate = True
        self.markDestroy = 0
        self.homeEnts = []
        self.firstPass = False
        self.canReward = False
        self.guildBox = guildBox
        self.school = school
        self.avatarLv = avatarLv
        self.avatarSex = avatarSex
        self.avatarGbId = avatarGbId
        self.avatarId = avatarId

class DungeonStatisticMixin(userType.UserSoleType):
    def __init__(self, gbID = 0, name = "", rank = 0, dmg = 0, hurt = 0, heal = 0, dead = 0):
        self.gbID = gbID
        self.name = name
        self.dmg = dmg
        self.hurt = hurt
        self.heal = heal
        self.dead = dead
        self.rank = rank

    def getRank(self):
        return self.rank

class DungeonFounderValMixin(userType.UserSoleType):
    def __init__(self, spaceNo, spaceUUID, playerBox, playerGBID, tEnter=0, tLeave=0, playerName=""):
        self.spaceNo = spaceNo
        self.spaceUUID = spaceUUID
        self.playerBox = playerBox
        self.playerGBID = playerGBID
        self.tEnter = tEnter            # 进入时间
        self.tLeave = tLeave            # 离开时间
        self.playerName = playerName

    def onAvatarEnter(self, gbId):
        if gbId == self.playerGBID:
            self.tEnter = utils.getNow()
            self.tLeave = 0

    def onAvatarLeave(self, gbId, isOffline=False):
        if gbId == self.playerGBID:
            self.tEnter = 0
            self.tLeave = utils.getNow()
            if isOffline:
                self.playerBox = None

    def hasAvatar(self):
        return self.tEnter and not self.tLeave

class DungeonStatisticFounderVal(DungeonStatisticMixin):
    def __init__(self, gbId = 0, name = "", rankId = 0, dmg = 0, hurt = 0, heal = 0, dead = 0):
        DungeonStatisticMixin.__init__(self, gbId, name, rankId, dmg, hurt, heal, dead)

class DungeonStatisticFounderVals(userType.UserDictType):
    def _lateReload(self):
        for founderVal in self.values():
            founderVal.reloadScript()

    def isNoFounders(self):
        for founderVal in self.values():
            if founderVal.hasAvatar():
                return False
        return True

    def addFounder(self, gbId, name, rankId, dmg, hurt, heal, dead):
        self[gbId] = DungeonStatisticFounderVal(gbId, name, rankId, dmg, hurt, heal, dead)

    def getFounderVal(self, playerGBID):
        return self[playerGBID] if playerGBID in self else None
        
    def getSortRankFounders(self):
        return sorted(list(self.values()), key=lambda x:getattr(x, 'rank'))

class DungeonFounderVal(DungeonFounderValMixin):
    def __init__(self, spaceNo, spaceUUID, playerBox, playerGBID, tEnter=0, tLeave=0,
                 playerName=""):
        DungeonFounderValMixin.__init__(self, spaceNo, spaceUUID, playerBox, playerGBID, tEnter, tLeave, playerName)

class DungeonFounderVals(userType.UserDictType):
    def __init__(self):
        self.totalFounders = 0

    def _lateReload(self):
        for founderVal in self.values():
            founderVal.reloadScript()

    def isNoFounders(self):
        for founderVal in self.values():
            if founderVal.hasAvatar():
                return False
        return True

    def addFounder(self, spaceNo, spaceUUID, playerGBID, playerBox):
        # 这里只统计进来的founder个数
        self.totalFounders += 1
        self[playerGBID] = DungeonFounderVal(spaceNo, spaceUUID, playerBox, playerGBID)

    def getFounderVal(self, playerGBID):
        return self[playerGBID] if playerGBID in self else None
    
    def getTotalFounderCount(self):
        return self.totalFounders

    def destoryFounder(self, playerGBID):
        self.pop(playerGBID, None)

    def getFounderGBIDs(self):
        return list(self.keys())   

