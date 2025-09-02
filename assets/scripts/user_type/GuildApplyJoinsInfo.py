
# coding: utf-8

import userType


class GuildApplyJoinsVal(userType.UserDictType):
    '''GUILD_APPLY_JOINS_DATA_INFO'''
    def __init__(self, applyJoins=()):
        for _ajVal in applyJoins:
            self[_ajVal.gbId] = _ajVal

    def toGuildApplyJoinsSavedDict(self):
        return {
            'applyJoins': list(self.values()),
        }


class GuildApplyJoinsInfo(object):
    def createObjFromDict(self, dataDict):
        obj = GuildApplyJoinsVal(**dataDict)
        return obj

    def getDictFromObj(self, obj):
        return obj.toGuildApplyJoinsSavedDict()

    def isSameType(self, obj):
        return type(obj) is GuildApplyJoinsVal


GuildApplyJoinsInstance = GuildApplyJoinsInfo()

