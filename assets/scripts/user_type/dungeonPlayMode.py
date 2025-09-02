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

import gamePlay_gamePlay as DDI
import teamDunChallenge_config as TDC_CFG
import raidBossChallenge_config as RBC_CFG


class _DungeonPlayMode(userType.UserSoleType):

    def __init__(self, playMode=0, **kwargs):
        self.playMode = playMode
        self.spaceUUID = kwargs.get('spaceUUID', 0)
        self.tCreate = kwargs.get('tCreate', 0)

    def getTEnd(self, dungeonNo):
        if not self.tCreate:
            WARNING_MSG('_DungeonPlayMode:: tCreate not set', self.tCreate)
            return 0
        return int(self.tCreate + DDI.datas[dungeonNo]['timeOut'] * 60 + 1)


class UnknownDungeonPlayMode(_DungeonPlayMode):
    def __init__(self):
        super(UnknownDungeonPlayMode, self).__init__(
            playMode=gameconst.DungeonPlayModeEnum.UNKNOWN)


class ChallengeDungeonPlayMode(_DungeonPlayMode):
    def __init__(self, dunLevel, easy):
        super(ChallengeDungeonPlayMode, self).__init__(gameconst.DungeonPlayModeEnum.CHALLENGE_DUNGEON)
        self.dunLevel = dunLevel
        self.easy = easy

class CrusadeDungeonPlayMode(_DungeonPlayMode):

    def __init__(self, dunLevel=0, mulFinalDmg=0, mulHurt=0):
        super(CrusadeDungeonPlayMode, self).__init__(
            playMode=gameconst.DungeonPlayModeEnum.CRUSADE)
        self.spaceLevel = 0
        self.dunLevel = dunLevel
        self.mulFinalDmg = mulFinalDmg
        self.mulHurt = mulHurt

class CrusadeDungeonPlayModePlayerObj(userType.UserSoleType):
    def __init__(self, rewardNumber=0, useItemAddRewardNumber=0, rewardDailyCount=0, useCoinAddRewardNum=0):
        self.rewardNumber = rewardNumber
        self.rewardDailyCount = rewardDailyCount
        self.useItemAddRewardNumber = useItemAddRewardNumber
        self.useCoinAddRewardNum = useCoinAddRewardNum

    @property
    def dailyRewardNum(self):
        return int(TDC_CFG.datas['dailyRewardNum']['value'])

    @property
    def rewardNumItemWeeklyLimit(self):
        return int(TDC_CFG.datas['rewardNumItemWeeklyLimit']['value'])

    @property
    def rewardNumCoinDailyLimit(self):
        return int(TDC_CFG.datas['rewardNumCoinDailyLimit']['value'])

    def isCanTakeReward(self):
        return self.rewardNumber > 0

    def isCanAddRewardByItem(self, useNum):
        return self.useItemAddRewardNumber >= useNum

    def isCanAddRewardByCoin(self, useNum):
        return self.useCoinAddRewardNum >= useNum

    def resetUseItemAddRewardNumber(self):
        self.useItemAddRewardNumber = self.rewardNumItemWeeklyLimit

    def resetUseCoinAddRewardNum(self):
        self.useCoinAddRewardNum = self.rewardNumCoinDailyLimit

    def addRewardNumByUseSpecialItem(self, num):
        self.addRewardNum(num, overLimit=True)
        nn = self.useItemAddRewardNumber - num
        self.useItemAddRewardNumber = nn if nn >= 0 else 0

    def addRewardNumByUseCoin(self, num):
        self.addRewardNum(num, overLimit=True)
        nn = self.useCoinAddRewardNum - num
        self.useCoinAddRewardNum = nn if nn >= 0 else 0

    def addRewardNum(self, num, overLimit=False):
        if overLimit or num < 0:
            self._addRewardNoLimit(num)
        else:
            self._addRewardWithLimit(num)

    def _addRewardWithLimit(self, num):
        newNum = self.rewardNumber + num
        if newNum < 0:
            WARNING_MSG('Crusade _addRewardWithLimit:: newNum smaller than zero', newNum)
            newNum = 0
        self.rewardNumber = newNum

    def _addRewardNoLimit(self, num):
        newNum = self.rewardNumber + num
        if newNum < 0:
            WARNING_MSG('Crusade _addRewardNoLimit:: newNum smaller than zero', newNum)
            newNum = 0
        self.rewardNumber = newNum

class ChiefDungeonPlayMode(_DungeonPlayMode):

    def __init__(self, dunLevel=0, mulFinalDmg=0, mulHurt=0):
        super(ChiefDungeonPlayMode, self).__init__(
            playMode=gameconst.DungeonPlayModeEnum.CHIEF)
        self.spaceLevel = 0
        self.dunLevel = dunLevel
        self.mulFinalDmg = mulFinalDmg
        self.mulHurt = mulHurt

class ChiefDungeonPlayModePlayerObj(userType.UserSoleType):
    def __init__(self, rewardNumber=0, useItemAddRewardNumber=0, rewardDailyCount=0, useCoinAddRewardNum=0):
        self.rewardNumber = rewardNumber
        self.rewardDailyCount = rewardDailyCount
        self.useItemAddRewardNumber = useItemAddRewardNumber
        self.useCoinAddRewardNum = useCoinAddRewardNum

    @property
    def dailyRewardNum(self):
        return int(RBC_CFG.datas['dailyRewardNum']['value'])

    @property
    def rewardNumItemWeeklyLimit(self):
        return int(RBC_CFG.datas['rewardNumItemWeeklyLimit']['value'])

    @property
    def rewardNumCoinDailyLimit(self):
        return int(RBC_CFG.datas['rewardNumCoinDailyLimit']['value'])

    def isCanTakeReward(self):
        return self.rewardNumber > 0

    def isCanAddRewardByItem(self, useNum):
        return self.useItemAddRewardNumber >= useNum

    def isCanAddRewardByCoin(self, useNum):
        return self.useCoinAddRewardNum >= useNum

    def resetUseItemAddRewardNumber(self):
        self.useItemAddRewardNumber = self.rewardNumItemWeeklyLimit

    def resetUseCoinAddRewardNum(self):
        self.useCoinAddRewardNum = self.rewardNumCoinDailyLimit

    def addRewardNumByUseSpecialItem(self, num):
        self.addRewardNum(num, overLimit=True)
        nn = self.useItemAddRewardNumber - num
        self.useItemAddRewardNumber = nn if nn >= 0 else 0

    def addRewardNumByUseCoin(self, num):
        self.addRewardNum(num, overLimit=True)
        nn = self.useCoinAddRewardNum - num
        self.useCoinAddRewardNum = nn if nn >= 0 else 0

    def addRewardNum(self, num, overLimit=False):
        if overLimit or num < 0:
            self._addRewardNoLimit(num)
        else:
            self._addRewardWithLimit(num)

    def _addRewardWithLimit(self, num):
        newNum = self.rewardNumber + num
        if newNum < 0:
            WARNING_MSG('Chief _addRewardWithLimit:: newNum smaller than zero', newNum)
            newNum = 0
        self.rewardNumber = newNum

    def _addRewardNoLimit(self, num):
        newNum = self.rewardNumber + num
        if newNum < 0:
            WARNING_MSG('Chief _addRewardNoLimit:: newNum smaller than zero', newNum)
            newNum = 0
        self.rewardNumber = newNum

