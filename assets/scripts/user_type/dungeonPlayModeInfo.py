# coding: utf-8
from KBEDebug import *
import KBEngine

import userType
import dungeonPlayMode


class CrusadeDungeonPlayModePlayerObjInfo(userType.ABCInfo):

    def createObjFromDict(self, dic):
        return dungeonPlayMode.CrusadeDungeonPlayModePlayerObj(**dic)

    def getDictFromObj(self, obj):
        return {'rewardNumber': obj.rewardNumber,
                'rewardDailyCount': obj.rewardDailyCount,
                'useItemAddRewardNumber': obj.useItemAddRewardNumber,
                'useCoinAddRewardNum': obj.useCoinAddRewardNum}

    def isSameType(self, obj):
        return type(obj) is dungeonPlayMode.CrusadeDungeonPlayModePlayerObj


crusadeDungeonPlayModePlayerObjInstance = CrusadeDungeonPlayModePlayerObjInfo()

class ChiefDungeonPlayModePlayerObjInfo(userType.ABCInfo):

    def createObjFromDict(self, dic):
        return dungeonPlayMode.ChiefDungeonPlayModePlayerObj(**dic)

    def getDictFromObj(self, obj):
        return {'rewardNumber': obj.rewardNumber,
                'rewardDailyCount': obj.rewardDailyCount,
                'useItemAddRewardNumber': obj.useItemAddRewardNumber,
                'useCoinAddRewardNum': obj.useCoinAddRewardNum}

    def isSameType(self, obj):
        return type(obj) is dungeonPlayMode.ChiefDungeonPlayModePlayerObj


chiefDungeonPlayModePlayerObjInstance = ChiefDungeonPlayModePlayerObjInfo()
