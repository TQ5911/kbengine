
# coding: utf-8

import userType


class GuildJoinCondVal(userType.UserSingleType):
    '''GUILD_JOIN_COND_DATA_INFO'''
    def __init__(self, level=0, score=0, auto=False):
        self.level = level
        self.score = score
        self.auto = auto

    def __eq__(self, value: object) -> bool:
        if not isinstance(value, GuildJoinCondVal):
            return False

        return self.level == value.level and self.score == value.score and self.auto == value.auto

    def isEligible(self, applyData):
        if applyData['level'] < self.level:
            return False

        if applyData['score'] < self.score:
            return False

        return True

    def toGuildJoinCondSavedDict(self):
        return {
            'level': self.level,
            'score': self.score,
            'auto': self.auto,
        }


class GuildJoinCondInfo(object):
    def createObjFromDict(self, dataDict):
        obj = GuildJoinCondVal(**dataDict)
        return obj

    def getDictFromObj(self, obj):
        return obj.toGuildJoinCondSavedDict()

    def isSameType(self, obj):
        return type(obj) is GuildJoinCondVal


GuildJoinCondInstance = GuildJoinCondInfo()

