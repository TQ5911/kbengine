# coding: utf-8
from KBEDebug import *
import KBEngine

import math

import userType


class AvatarScores(userType.UserSoleType):

    __attrs__ = ("equipments", "level", "rewardFightProp", 'mount', 'pet', 'skill', 'guildtrain')

    def __repr__(self):
        return '{}({})'.format(
            self.__class__.__name__,
            ','.join(['{}={}'.format(k, v) for k, v in self.__dict__.items()])
        )

    def __setattr__(self, key, value):
        if key not in self.__dict__:
            return object.__setattr__(self, key, value)

        crtValue = self.__dict__.get(key, 0)
        if crtValue != value:
            object.__setattr__(self, key, value)
            DEBUG_MSG('\- AvatarScoreColl:: set "{}" from {} to {}'.format(key, crtValue, value))
            DEBUG_MSG('  |- CurrentScore: ', self.__repr__())
            DEBUG_MSG('  |- TotalScore:   ', self.totalScore)
        else:
            DEBUG_MSG('\= AvatarScoreColl:: un-change "{}" {} == {}'.format(key, crtValue, value))

    def __init__(self, equipments=0, level=0, rewardFightProp=0, mount=0, pet=0, skill=0, guildtrain=0):
        self.equipments = equipments            # 装备评分
        self.level = level                      # 等级评分
        self.rewardFightProp = rewardFightProp  # reward奖励属性评分
        self.mount = mount                      # 坐骑评分
        self.pet = pet                          # 宠物评分
        self.skill = skill                      # 技能评分
        self.guildtrain = guildtrain            # 公会训练评分

    @property
    def totalScore(self):
        return sum([self.equipments, self.level, self.rewardFightProp, self.mount, self.pet, self.skill, self.guildtrain])

    def updateScore(self, scoreKey, newScoreVal):
        crtScoreVal = getattr(self, scoreKey)
        newScoreVal = math.floor(newScoreVal)
        setattr(self, scoreKey, newScoreVal)
        return crtScoreVal, newScoreVal

    def getTlogStr(self):
        return ','.join(["{}:{}".format(scoreName, getattr(self, scoreName)) for scoreName in self.__attrs__])

class AvatarScoresInfo(userType.ABCInfo):
    def createObjFromDict(self, dic):
        return AvatarScores(**dic)

    def getDictFromObj(self, obj: AvatarScores):
        return {
            'equipments': math.floor(obj.equipments),
            'level': math.floor(obj.level),
            'rewardFightProp': math.floor(obj.rewardFightProp),
            'mount': math.floor(obj.mount),
            'pet': math.floor(obj.pet),
            'skill': math.floor(obj.skill),
            'guildtrain': math.floor(obj.guildtrain),
        }

    def isSameType(self, obj):
        return type(obj) == AvatarScores


avatarScoresInstance = AvatarScoresInfo()
