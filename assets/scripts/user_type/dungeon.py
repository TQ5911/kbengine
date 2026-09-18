# -*- coding: utf-8 -*-
from KBEDebug import *

import collections

import utils

import gameconst
import gameengine
import formula
import userType

import gamePlay_gamePlay as DDL


class DungeonSpaceVal(userType.UserSingleType):
    SPACE_STATUS_INIT = 1
    SPACE_STATUS_DURING = 2
    SPACE_STATUS_COMPLETE = 3
    SPACE_STATUS_TO_DESTORY = 4
    SPACE_STATUS_FAILED = 5

    def __init__(self, spaceNo, spaceUUID, spaceBox, spaceMgr, spaceLevel=1, extraPropsDic = {}, dungeonSpaceValType=gameconst.DungeonSpaceValType.NONE):
        self.spaceUUID = spaceUUID
        self.spaceNo = spaceNo
        self.spaceBox = spaceBox
        self.spaceMgr = spaceMgr
        self.spaceLevel = spaceLevel
        self.tCreate = utils.curTS()
        self.destroyTimer = 0
        self.nDestoryCnt = 0
        self.completeDungeonTimer = 0
        self.loadingDungeonEntitiesTimerDic = {}
        self.loadDungeonEntitiesCheckTimerDic = {}
        self.state = self.SPACE_STATUS_DURING
        self.src = 0
        self.extraProps = extraPropsDic
        self.dungeonSpaceValType = dungeonSpaceValType
        self.completedReasonType = gameconst.DunegonCompleteReasonType.DEFAULT
        self.challengeEndTime = 0
        # 跨服组队队伍 ID（中心权威）：0=非跨服组队副本空间；
        # 由副本 stub 建空间时按 extra['crossTeamId'] 记录（本服/跨服服两种模式均记录）。
        # 空间的玩法枚举只在 DungeonSpaceMgr 侧的 dungeonPlayMode 上（本服模式落
        # CRUSADE/CHIEF，跨服服落 CROSS_CRUSADE/CROSS_CHIEF），与队伍归属判定无关
        self.crossTeamId = 0

    def isActive(self):
        return self.state == self.SPACE_STATUS_DURING

    def isCrossDungeon(self):
        # 跨服组队副本空间判定：队伍全量落在组队中心（本服/跨服之分只是业务形态），
        # 归属唯一按 crossTeamId 识别（记录处见 CrossTeamDungeonStub._teamGetDungeonSpaceVal/
        # _raidGetDungeonSpaceVal）；与空间 playMode（本服副本/跨服副本行为分支用）无关。
        # 注：队伍中心化 + 旧链路客户端不可达后，CrossTeamDungeonStub 内本判定恒为 True——
        # 它只是双轨期标记旧 TeamStub/RaidStub 联动分支的删除锚点，随旧系统下线一并塌缩删除
        return self.crossTeamId > 0

    def completeDungeon(self, win=True):
        self.state = self.SPACE_STATUS_COMPLETE if win else self.SPACE_STATUS_FAILED

    def isCompleted(self):
        return self.state in (self.SPACE_STATUS_COMPLETE, self.SPACE_STATUS_FAILED)

    def isFailed(self):
        return self.state == self.SPACE_STATUS_FAILED

    def toDestoryDungeon(self):
        self.state = self.SPACE_STATUS_TO_DESTORY

    def isToDestory(self):
        return self.state == self.SPACE_STATUS_TO_DESTORY

    def getRemainTime(self, dungeonNo=None):
        dungeonNo = dungeonNo or formula.fetchMapId(self.spaceNo)

        if dungeonNo not in DDL.datas:
            LOG_ERR('Can\'t find dungeonNo in dungeonInfo: {}'.format(dungeonNo))
            return 0

        timeout = DDL.datas[dungeonNo]['timeOut'] * 60
        _lostT = utils.curTS() - self.tCreate

        remainT = int(timeout - _lostT)

        # remain time should not less than zero
        return remainT if remainT > 0 else 0

    def cancelCompleteTimer(self, owner, tag):
        if self.completeDungeonTimer:
            owner.cancelTimerCB(self.completeDungeonTimer, tag)
        self.clearCompleteTimer()

    def clearCompleteTimer(self):
        self.completeDungeonTimer = 0

    def getElapsedTime(self):
        return utils.curTS() - self.tCreate

# ======================================================
# Dungeon Monster Creator TimeLine Structure
# ======================================================

class DungeonSpaceTimeLineMixin(object):
    def __init__(self, dungeonTimeLineDic=None, killSum=0):
        if dungeonTimeLineDic is None:
            self.dungeonTimeLineDic = {}
        else:
            self.dungeonTimeLineDic = dungeonTimeLineDic

        self.killSum = killSum
        self.dungeonCreepBaseKillDic = {}

    def addTimeLine(self, flagId, *args, **kwargs):
        if 'flagId' in kwargs:
            kwargs.pop('flagId')

        self.dungeonTimeLineDic[flagId] = DungeonSpaceTimeLineVal(
            flagId, *args, **kwargs)

    def addKill(self, flagId, addKillSumFlag=True):
        if flagId not in self.dungeonTimeLineDic:
            return

        self.dungeonTimeLineDic[flagId].kills += 1
        if addKillSumFlag:
            self.killSum += 1

    def getTimeLine(self, flagId):
        if flagId in self.dungeonTimeLineDic:
            return self.dungeonTimeLineDic[flagId]

    def addKillByCreepBaseId(self, creepbaseId, addKillSumFlag=True):
        if creepbaseId not in self.dungeonCreepBaseKillDic:
            self.dungeonCreepBaseKillDic[creepbaseId] = 0
        self.dungeonCreepBaseKillDic[creepbaseId] += 1
        if addKillSumFlag:
            self.killSum += 1

    def getCreepBaseKilledNum(self, creepbaseId):
        return self.dungeonCreepBaseKillDic.get(creepbaseId, 0)

    def clearKills(self, flagId):
        if flagId not in self.dungeonTimeLineDic:
            return

        _sumKill = self.killSum - self.dungeonTimeLineDic[flagId].kills
        self.killSum = _sumKill if _sumKill > 0 else 0
        self.dungeonTimeLineDic[flagId].kills = 0


class DungeonSpaceTimeLineVal(userType.UserSingleType):
    def __init__(self, flagId=0, refreshCount=0, nextRefreshTime=0, 
                 stopRefresh=False, kills=0, **kwargs):
        self.refreshCount = refreshCount
        self.flagId = flagId
        self.nextRefreshTime = nextRefreshTime
        self.kills = kills
        self.stopRefresh = stopRefresh

    def stop(self):
        self.stopRefresh = True

    def updateRefreshTime(self, newTime):
        self.nextRefreshTime = newTime
        self.refreshCount += 1

# ======================================================


# ======================================================
# 副本刷怪队列
# ======================================================

class DungeonEntityDefine(object):
    def __init__(self, entType='', entProps=None, 
                 loadStatus=gameconst.DungeonEntityLoadEnum.UNLOAD):
        self.entProps = entProps or {}
        self.loadStatus = loadStatus
        self.entType = entType


class DungeonEntityGeneratorVal(object):
    def __init__(self, genUUID, entityList, withBase=False, extra=None):
        self.entityList = entityList    # type: list[DungeonEntityDefineStruct,]
        self.genUUID = genUUID
        self.extra = extra or {}
        self.withBase = withBase

    def isAllEntityLoaded(self):
        for entVal in self.entityList:
            if entVal.loadStatus != gameconst.DungeonEntityLoadEnum.LOADED:
                return False
        return True

    def getEntityNum(self):
        return len(self.entityList)

    def getEntityStatusVal(self, status):
        _num = 0
        for _entVal in self.entityList:
            if _entVal.loadStatus != status:
                _num += 1
        return _num



# ======================================================


#----------------------------单人副本----------------------------------------------
class SingleDungeonSpaceVal(DungeonSpaceVal, DungeonSpaceTimeLineMixin):
    def __init__(self, spaceNo, spaceUUID, spaceBox, spaceMgr, ownerGbId,\
                 spaceLevel=1, **kwargs):
        super(SingleDungeonSpaceVal, self).__init__(
            spaceNo, spaceUUID, 
            spaceBox, spaceMgr, 
            spaceLevel=spaceLevel,
            dungeonSpaceValType=gameconst.DungeonSpaceValType.SINGLE)

        super(DungeonSpaceVal, self).__init__()
        super(DungeonSpaceTimeLineMixin, self).__init__()

        self.homeEnts = []
        self.ownerGbId = ownerGbId

class SingleDungeonFounders(userType.UserDictType):
    def addFounder(self, spaceNo, spaceUUID, playerGbId, playerBox):
        _key = self.getFounderKey(playerGbId, spaceUUID)
        self[_key] = SingleDungeonFounderVal(spaceNo, spaceUUID, playerGbId, playerBox)

    def getFounderVal(self, playerGbId, spaceUUID):
        _key = self.getFounderKey(playerGbId, spaceUUID)
        if _key in self:
            return self[_key]
        return None

    def destoryFounder(self, playerGbId, spaceUUID):
        _key = self.getFounderKey(playerGbId, spaceUUID)
        self.pop(_key, None)

    def getFounderKey(self, playerGbId, spaceUUID):
        return playerGbId, spaceUUID

class SingleDungeonFounderVal(userType.UserSingleType):
    def __init__(self, spaceNo, spaceUUID, playerGbId, playerBox, tEnter=0, tLeave=0):
        self.spaceUUID = spaceUUID
        self.spaceNo = spaceNo
        self.playerGbId = playerGbId
        self.playerBox = playerBox
        self.tLeave= tLeave
        self.tEnter = tEnter

    def onAvatarEnter(self, gbId):
        if gbId != self.playerGbId:
            return

        self.tEnter = utils.curTS()
        self.tLeave = 0

    def hasAvatar(self):
        return self.tEnter and not self.tLeave

    def onAvatarLeave(self, gbId, isOffline=False):
        if gbId != self.playerGbId:
            return

        self.tEnter = 0
        self.tLeave = utils.curTS()
        if isOffline:
            self.playerBox = None

class SingleDungeonFoundersInfo(userType.UserDictType):
    def createObjFromDict(self, dict):
        _founders = SingleDungeonFounders()

        for _fVal in dict['founders']:
            _founders.addFounder(
                _fVal['spaceNo'], 
                _fVal['spaceUUID'], 
                _fVal['playerGbId'], 
                _fVal['playerBox'], 
                _fVal['tEnter'], 
                _fVal['tLeave'])

        return _founders

    def getDictFromObj(self, obj):
        _d = {'founders': []}
        founders = _d['founders']

        for fVal in obj.values():
            founders.append({
                'spaceUUID':fVal.spaceUUID,
                'spaceNo':fVal.spaceNo,
                'playerGbId':fVal.playerGbId,
                'playerBox': fVal.playerBox,
                'tLeave':fVal.tLeave,
                'tEnter':fVal.tEnter,
            })

        return _d

    def isSameType(self, obj):
        return type(obj) is SingleDungeonFounders


#----------------------------队伍副本--------------------------------------------------------
class TeamDungeonSpaceVal(DungeonSpaceVal, DungeonSpaceTimeLineMixin):
    def __init__(self, spaceNo, spaceUUID, spaceBox, spaceMgr, teamUUID,\
                 spaceLevel=1,extraDic={}, **kwargs):

        super(TeamDungeonSpaceVal, self).__init__(
            spaceNo, spaceUUID, spaceBox, spaceMgr, 
            spaceLevel,extraDic,
            dungeonSpaceValType=gameconst.DungeonSpaceValType.TEAM)

        super(DungeonSpaceVal, self).__init__()
        super(DungeonSpaceTimeLineMixin, self).__init__()
        self.markCreate = True
        self.teamUUID=teamUUID
        self.homeEnts = []
        self.markDestroy = 0


# ----------------------------------------------------------------------
# 团队副本
# ----------------------------------------------------------------------

class RaidDungeonSpaceVal(DungeonSpaceVal, DungeonSpaceTimeLineMixin):
    """RaidStub 团队副本Space结构体"""

    def __init__(self, spaceNo, spaceUUID, spaceBox, spaceMgr, raidUUID,\
                 spaceLevel=1, **kwargs):

        super(RaidDungeonSpaceVal, self).__init__(
            spaceNo, spaceUUID, spaceBox, spaceMgr, 
            spaceLevel,
            dungeonSpaceValType=gameconst.DungeonSpaceValType.RAID)

        super(DungeonSpaceVal, self).__init__()
        super(DungeonSpaceTimeLineMixin, self).__init__()
        self.raidUUID = raidUUID
        self.founders = RaidDungeonFounders()
        self.homeEnts = []
        self.tMarkDestroy = 0            # 标记删除时间, 在该时间内保证玩家可以安全离开副本space, 最后销毁副本
        self.extraProps = {}
        self.raidSrc = 0

    def getAllPlayerGbidAndNamePair(self):
        _result = []
        for i in self.founders.values():
            if i.playerName:
                _result.append((i.playerGBID, i.playerName))
        return _result

    def _lateReload(self):
        self.founders.reloadScript()


class RaidDungeonFounders(userType.UserDictType):
    """RaidStub 团队副本中存在成员集合字典"""

    def _lateReload(self):
        for _founderVal in self.values():
            _founderVal.reloadScript()

    def isNoFounders(self):
        for _founderVal in self.values():
            if _founderVal.hasAvatar():
                return False
        return True

    def getFounderVal(self, playerGBID):
        return self[playerGBID] if playerGBID in self else None

    def addFounder(self, spaceNo, spaceUUID, gbId, playerBox):
        self[gbId] = RaidDungeonFounderVal(spaceNo, spaceUUID, playerBox, gbId)

    def destoryFounder(self, playerGBID):
        self.pop(playerGBID, None)


class RaidDungeonFounderVal(userType.UserSingleType):
    """RaidStub 团队副本中存在成员结构体"""

    def __init__(self, spaceNo, spaceUUID, playerBox, playerGBID, tEnter=0, tLeave=0,
                 playerName="", **kwargs):
        self.spaceUUID = spaceUUID
        self.spaceNo = spaceNo
        self.playerBox = playerBox
        self.playerGBID = playerGBID
        self.tEnter = tEnter            # 进入时间
        self.playerName = playerName
        self.tLeave = tLeave            # 离开时间

    def onAvatarEnter(self, gbId):
        if gbId == self.playerGBID:
            self.tEnter = utils.curTS()
            self.tLeave = 0

    def onAvatarLeave(self, gbId, isOffline=False):
        if gbId != self.playerGBID:
            return

        self.tEnter = 0
        self.tLeave = utils.curTS()
        if isOffline:
            self.playerBox = None

    def hasAvatar(self):
        return self.tEnter and not self.tLeave

class BaseDungeonFoundersMixin(userType.UserSingleType):
    def __init__(self):
        self.founders = DungeonFounderVals()
    
    def _lateReload(self):
        self.founders.reloadScript()

class BaseDungeonStatisticFoundersMixin(userType.UserSingleType):
    def __init__(self):
        self.statisticFounders = DungeonStatisticFounderVals()
        self.statisticBatchCount = 0
        self.sortedStatisticFoundersRankCache = None
    
    def refreshFoundersSortRankCache(self):
        self.sortedStatisticFoundersRankCache = self.statisticFounders.getSortRankFounders()

    def _lateReload(self):
        self.statisticFounders.reloadScript()
    
class GuildBossDungeonSpaceVal(DungeonSpaceVal, DungeonSpaceTimeLineMixin, BaseDungeonFoundersMixin, BaseDungeonStatisticFoundersMixin):
    def __init__(self, spaceNo, spaceUUID, spaceBox, spaceMgr, guildUUID, guildBox=None, spaceLevel=1,extraDic={},
                school = 0, avatarLv = 0, avatarSex = 0, avatarGbId = 0, avatarId = 0):
        DungeonSpaceVal.__init__(self, spaceNo, spaceUUID, spaceBox, spaceMgr, spaceLevel, extraDic, dungeonSpaceValType=gameconst.DungeonSpaceValType.GUILD_BOSS)
        DungeonSpaceTimeLineMixin.__init__(self)
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

class DungeonStatisticMixin(userType.UserSingleType):
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

class DungeonFounderValMixin(userType.UserSingleType):
    def __init__(self, spaceNo, spaceUUID, playerBox, playerGBID, tEnter=0, 
                 tLeave=0, playerName="", **kwargs):
        self.spaceUUID = spaceUUID
        self.spaceNo = spaceNo
        self.playerBox = playerBox
        self.playerGBID = playerGBID
        self.tEnter = tEnter            # 进入时间
        self.playerName = playerName
        self.tLeave = tLeave            # 离开时间

    def onAvatarEnter(self, gbId):
        if gbId == self.playerGBID:
            self.tEnter = utils.curTS()
            self.tLeave = 0

    def onAvatarLeave(self, gbId, isOffline=False):
        if gbId != self.playerGBID:
            return

        self.tEnter = 0
        self.tLeave = utils.curTS()
        if isOffline:
            self.playerBox = None

    def hasAvatar(self):
        return self.tEnter and not self.tLeave

class DungeonStatisticFounderVal(DungeonStatisticMixin):
    def __init__(self, gbId = 0, name = "", rankId = 0, dmg = 0, hurt = 0, heal = 0, dead = 0):
        DungeonStatisticMixin.__init__(self, gbId, name, rankId, dmg, hurt, heal, dead)

class DungeonStatisticFounderVals(userType.UserDictType):
    def _lateReload(self):
        for _founderVal in self.values():
            _founderVal.reloadScript()

    def isNoFounders(self):
        for _founderVal in self.values():
            if _founderVal.hasAvatar():
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
        for _founderVal in self.values():
            _founderVal.reloadScript()

    def isNoFounders(self):
        for _founderVal in self.values():
            if _founderVal.hasAvatar():
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


SingleDungeonFoundersInstance = SingleDungeonFoundersInfo()
