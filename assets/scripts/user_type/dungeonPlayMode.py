# coding: utf-8
from KBEDebug import *
import KBEngine

import collections
import math

import utils
import gameconst
import userType
import dropAward
import awardContext
import gameengine

import gamePlay_gamePlay as GP_GPD
import teamDunChallenge_config as TDC_CFG
import raidBossChallenge_config as RBC_CFG
import activityControl_activityTicket as AC_AT


class _DungeonPlayMode(userType.UserSingleType):

    def __init__(self, playMode=0, **kwargs):
        self.playMode = playMode
        self.tCreate = kwargs.get('tCreate', 0)
        self.spaceUUID = kwargs.get('spaceUUID', 0)

    def getTEnd(self, dungeonNo):
        if not self.tCreate:
            LOG_WARN('_DungeonPlayMode:: tCreate not set', self.tCreate)
            return 0
        return int(self.tCreate + GP_GPD.datas[dungeonNo]['timeOut'] * 60 + 1)


class UnknownDungeonPlayMode(_DungeonPlayMode):
    def __init__(self, **kwargs):
        super(UnknownDungeonPlayMode, self).__init__(
            playMode=gameconst.DungeonPlayModeEnum.UNKNOWN)


class ChallengeDungeonPlayMode(_DungeonPlayMode):
    def __init__(self, dunLevel, easy):
        super(ChallengeDungeonPlayMode, self).__init__(gameconst.DungeonPlayModeEnum.CHALLENGE_DUNGEON)
        self.dunLevel = dunLevel
        self.easy = easy

class CrusadeDungeonPlayMode(_DungeonPlayMode):

    def __init__(self, dunLevel=0, mulFinalDmg=0, mulHurt=0, teamUUID = 0):
        super(CrusadeDungeonPlayMode, self).__init__(
            playMode=gameconst.DungeonPlayModeEnum.CRUSADE)
        self.spaceLevel = 0
        self.dunLevel = dunLevel
        self.mulFinalDmg = mulFinalDmg
        self.mulHurt = mulHurt
        self.teamUUID = teamUUID

class DungeonPlayModePlayerMiXin(userType.UserSingleType):
    def __init__(self, rewardNumber=0, rewardDailyCount=0, useCoinAddRewardNum=0, rewardCoinNumber=0, rewardItemNumber=0, ticketType=0, rewardCommonNumber=0):
        self.rewardNumber = rewardNumber
        self.rewardCoinNumber = rewardCoinNumber
        self.rewardItemNumber = rewardItemNumber
        self.rewardDailyCount = rewardDailyCount
        self.useCoinAddRewardNum = useCoinAddRewardNum
        self.ticketType = ticketType
        self.rewardCommonNumber = rewardCommonNumber
    
    def isCanTakeReward(self):
        return self.rewardNumber > 0

    def isCanAddRewardByCoin(self, useNum):
        return self.useCoinAddRewardNum >= useNum

    def resetUseCoinAddRewardDailyNum(self):
        self.useCoinAddRewardNum = self.rewardNumCoinDailyLimit

    @property
    def leftDailyRewardNum(self):
        return self.rewardNumber - self.rewardItemNumber - self.rewardCoinNumber - self.rewardCommonNumber

    def addRewardNumByDefault(self, num):
        self.addRewardNum(gameconst.DungeonAddRewardNumCountType.DEFAULT_COUNT, num, overLimit=False)

    def addRewardNumByUseCommonDefault(self, num):
        self.addRewardNum(gameconst.DungeonAddRewardNumCountType.COMMON_COUNT, num, overLimit=False)

    def addRewardNumByUseSpecialItem(self, num):
        self.addRewardNum(gameconst.DungeonAddRewardNumCountType.ITEM_COUNT, num, overLimit=True)

    def addRewardNumByUseCoin(self, addRewardNum):
        self.addRewardNum(gameconst.DungeonAddRewardNumCountType.COIN_COUNT, addRewardNum, overLimit=True)

    def deductUsedCoinAddRewardNum(self, useNum):
        nn = self.useCoinAddRewardNum - useNum
        self.useCoinAddRewardNum = nn if nn >= 0 else 0

    def addRewardNum(self, countType, num, overLimit=False):
        if countType not in gameconst.DungeonAddRewardNumCountType.VALID_TYPE:
            return
        newNum = self.rewardNumber + num
        if newNum < 0:
            LOG_WARN('Crusade _addRewardWithLimit 1:: newNum smaller than zero', newNum, countType)
            newNum = 0
        self.rewardNumber = newNum

        if countType == gameconst.DungeonAddRewardNumCountType.COMMON_COUNT:
            newNum = self.rewardCommonNumber + num
            if newNum < 0:
                LOG_WARN('Crusade _addRewardWithLimit 4:: newNum smaller than zero', newNum, countType)
                newNum = 0
            self.rewardCommonNumber = newNum

        if countType == gameconst.DungeonAddRewardNumCountType.ITEM_COUNT:
            newNum = self.rewardItemNumber + num
            if newNum < 0:
                LOG_WARN('Crusade _addRewardWithLimit 2:: newNum smaller than zero', newNum, countType)
                newNum = 0
            self.rewardItemNumber = newNum

        if countType == gameconst.DungeonAddRewardNumCountType.COIN_COUNT:
            newNum = self.rewardCoinNumber + num
            if newNum < 0:
                LOG_WARN('Crusade _addRewardWithLimit 3:: newNum smaller than zero', newNum, countType)
                newNum = 0
            self.rewardCoinNumber = newNum

    def deductRewardNum(self):
        LOG_INFO('deductRewardNum begin: ', self.rewardNumber, self.rewardCoinNumber, self.rewardItemNumber, self.rewardCommonNumber)
        if self.rewardNumber > 0:
            # 看看默认次数是否还有，优先使用默认次数，后面再使用道具购买的，最后使用金币购买的
            if self.rewardNumber - self.rewardItemNumber - self.rewardCoinNumber - self.rewardCommonNumber > 0:
                self.addRewardNum(gameconst.DungeonAddRewardNumCountType.DEFAULT_COUNT, -1)
                self.ticketType = gameconst.DungeonTicketType.NORMAL
            elif self.rewardCommonNumber > 0:
                self.addRewardNum(gameconst.DungeonAddRewardNumCountType.COMMON_COUNT, -1)
                self.ticketType = gameconst.DungeonTicketType.COMMON
            elif self.rewardItemNumber > 0:
                self.addRewardNum(gameconst.DungeonAddRewardNumCountType.ITEM_COUNT, -1)
                self.ticketType = gameconst.DungeonTicketType.ITEM
            elif self.rewardCoinNumber > 0:
                self.addRewardNum(gameconst.DungeonAddRewardNumCountType.COIN_COUNT, -1)
                self.ticketType = gameconst.DungeonTicketType.GOLD
        else:
            gameengine.panicStack(f"{self.__class__.__name__}::deductRewardNum:: remain count is zero !!!", self)
        LOG_INFO('deductRewardNum end: ', self.rewardNumber, self.rewardCoinNumber, self.rewardItemNumber, self.rewardCommonNumber)

    def hasCoinCount(self):
        return self.rewardCoinNumber > 0
    
    def getUsedTicketType(self):
        return self.ticketType
    
    def clear(self):
        self.rewardNumber = 0
        self.rewardCoinNumber = 0
        self.rewardItemNumber = 0
        self.rewardCommonNumber = 0

    def checkUsedTicketType(self, ticketType):
        return self.ticketType == ticketType

class CrusadeDungeonPlayModePlayerObj(DungeonPlayModePlayerMiXin):
    def __init__(self, rewardNumber=0, rewardDailyCount=0, useCoinAddRewardNum=0, rewardCoinNumber=0, rewardItemNumber=0, ticketType=0, rewardCommonNumber=0):
        DungeonPlayModePlayerMiXin.__init__(self, rewardNumber, rewardDailyCount, useCoinAddRewardNum, rewardCoinNumber, rewardItemNumber, ticketType, rewardCommonNumber)

    @property
    def dailyRewardNum(self):
        return 0

    @property
    def rewardNumCoinDailyLimit(self):
        return len(AC_AT.ticketIdDic[gameconst.RecoveryTicketSubType.CRUSADE])

class ChiefDungeonPlayMode(_DungeonPlayMode):

    def __init__(self, dunLevel=0, mulFinalDmg=0, mulHurt=0, raidUUID = 0):
        super(ChiefDungeonPlayMode, self).__init__(
            playMode=gameconst.DungeonPlayModeEnum.CHIEF)
        self.spaceLevel = 0
        self.dunLevel = dunLevel
        self.mulFinalDmg = mulFinalDmg
        self.mulHurt = mulHurt
        self.raidUUID = raidUUID

class ChiefDungeonPlayModePlayerObj(DungeonPlayModePlayerMiXin):
    def __init__(self, rewardNumber=0, rewardDailyCount=0, useCoinAddRewardNum=0, rewardCoinNumber=0, rewardItemNumber=0, ticketType=0, rewardCommonNumber=0):
        DungeonPlayModePlayerMiXin.__init__(self, rewardNumber, rewardDailyCount, useCoinAddRewardNum, rewardCoinNumber, rewardItemNumber, ticketType, rewardCommonNumber)

    @property
    def dailyRewardNum(self):
        return 0

    @property
    def rewardNumCoinDailyLimit(self):
        return len(AC_AT.ticketIdDic[gameconst.RecoveryTicketSubType.CHIEF])


class CrossCrusadeDungeonPlayMode(_DungeonPlayMode):
    # 跨服讨伐-魔物巢穴：teamUUID 语义为跨服队伍 ID（center 权威），
    # 本服队伍钩子不适用，结算经 syncMethodCallToLocalServerBase 透传玩家本服
    def __init__(self, dunLevel=0, mulFinalDmg=0, mulHurt=0, teamUUID=0):
        super(CrossCrusadeDungeonPlayMode, self).__init__(
            playMode=gameconst.DungeonPlayModeEnum.CROSS_CRUSADE)
        self.spaceLevel = 0
        self.dunLevel = dunLevel
        self.mulFinalDmg = mulFinalDmg
        self.mulHurt = mulHurt
        self.teamUUID = teamUUID


class CrossChiefDungeonPlayMode(_DungeonPlayMode):
    # 跨服讨伐-首领巢穴（15 人）：teamUUID 语义为跨服队伍 ID
    def __init__(self, dunLevel=0, mulFinalDmg=0, mulHurt=0, teamUUID=0):
        super(CrossChiefDungeonPlayMode, self).__init__(
            playMode=gameconst.DungeonPlayModeEnum.CROSS_CHIEF)
        self.spaceLevel = 0
        self.dunLevel = dunLevel
        self.mulFinalDmg = mulFinalDmg
        self.mulHurt = mulHurt
        self.teamUUID = teamUUID

class DungeonPassRecords(userType.UserSingleType):
    def __init__(self, entryIds=[], entryStatus=[]):
        self.passEntryRecords = {}
        for idx in range(0, len(entryIds)):
            self.passEntryRecords[entryIds[idx]] = entryStatus[idx]

    def finishEntryStatus(self, entryId):
        self.passEntryRecords[entryId] = True

    def checkEntryStatus(self, entryId):
        if entryId and entryId > 0:
            return entryId not in self.passEntryRecords
        return False

class ChallengeInnerDemonPlayMode(_DungeonPlayMode):
    def __init__(self, ownerGbId=0, challengeEndTime=0):
        super(ChallengeInnerDemonPlayMode, self).__init__(gameconst.DungeonPlayModeEnum.INNER_DEMON)
        self.ownerGbId = ownerGbId
        self.challengeEndTime = 0
