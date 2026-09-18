# coding: utf-8
from KBEDebug import *
import KBEngine

import math

import gameconst
import userType
import LogTrackingMgr

class AvatarScores(userType.UserSingleType):

    __attrs__ = gameconst.PlayerScoreKeyDatas.INIT

    def __repr__(self):
        return '{}({})'.format(
            self.__class__.__name__,
            ','.join(['{}={}'.format(_k, _v) for _k, _v in self.__dict__.items()])
        )

    def __setattr__(self, keyName, value):
        if keyName not in self.__dict__:
            return object.__setattr__(self, keyName, value)

        _crtValue = self.__dict__.get(keyName, 0)
        if _crtValue != value:
            object.__setattr__(self, keyName, value)
            LOG_DBG('\- AvatarScoreColl:: set "{}" from {} to {}'.format(keyName, _crtValue, value))
            LOG_DBG('  |- CurrentScore: ', self.__repr__())
            LOG_DBG('  |- TotalScore:   ', self.totalScore)
        else:
            LOG_DBG('\= AvatarScoreColl:: un-change "{}" {} == {}'.format(keyName, _crtValue, value))

    def __init__(self, equipments=0, level=0, rewardFightProp=0, mount=0, pet=0, skill=0, guildtrain=0, meridian=0, bless=0):
        self.equipments = equipments            # 装备评分
        self.level = level                      # 等级评分
        self.rewardFightProp = rewardFightProp  # reward奖励属性评分
        self.mount = mount                      # 坐骑评分
        self.pet = pet                          # 宠物评分
        self.skill = skill                      # 技能评分
        self.guildtrain = guildtrain            # 公会训练评分
        self.meridian = meridian                # 经脉评分
        self.bless = bless                      # 祝福评分

    @property
    def totalScore(self):
        scores = [self.equipments, self.level, self.rewardFightProp, self.mount, self.pet, self.skill, self.guildtrain, self.meridian, self.bless]
        totalScores = sum(scores)
        return totalScores

    def getAllScore(self):
        score = 0
        for scoreKey in gameconst.PlayerScoreKeyDatas.ALL:
            score += getattr(self, scoreKey)
        return score

    def updateScore(self, owner, isInited, opUUID, scoreKey, newScoreVal):
        oldScore = self.getAllScore()
        _crtScoreVal = getattr(self, scoreKey)
        _newScoreVal = math.floor(newScoreVal)
        setattr(self, scoreKey, _newScoreVal)
        newScore = self.getAllScore()
        if isInited:
            delta = newScore - oldScore
            if delta != 0:
                LogTrackingMgr.LogTrackingMgr.power_change(owner.gbID, owner.accountEntity.clientDistinctId, newScore, oldScore, newScore - oldScore, opUUID, scoreKey)
        return _crtScoreVal, _newScoreVal


class AvatarScoresInfo(userType.ABCInfo):
    def createObjFromDict(self, dict):
        return AvatarScores(**dict)

    def getDictFromObj(self, obj: AvatarScores):
        return {
            gameconst.PlayerScoreKeyDatas.Level:            math.floor(obj.level),
            gameconst.PlayerScoreKeyDatas.Equipments:       math.floor(obj.equipments),
            gameconst.PlayerScoreKeyDatas.RewardFightProp:  math.floor(obj.rewardFightProp),
            gameconst.PlayerScoreKeyDatas.Mount:            math.floor(obj.mount),
            gameconst.PlayerScoreKeyDatas.Pet:              math.floor(obj.pet),
            gameconst.PlayerScoreKeyDatas.Skill:            math.floor(obj.skill),
            gameconst.PlayerScoreKeyDatas.Guildtrain:       math.floor(obj.guildtrain),
            gameconst.PlayerScoreKeyDatas.Meridian:         math.floor(obj.meridian),
            gameconst.PlayerScoreKeyDatas.Bless:            math.floor(obj.bless),
        }

    def isSameType(self, obj):
        return type(obj) == AvatarScores


avatarScoresInstance = AvatarScoresInfo()
