
# coding: utf-8

import userType


class GuildArchitectureVal(userType.UserSoleType):
    '''GUILD_ARCHITECTURE_DATA_INFO'''
    def __init__(self, level=0, exp=0):
        self.level = level
        self.exp = exp

    def __eq__(self, value: object) -> bool:
        if not isinstance(value, GuildArchitectureVal):
            return False

        return self.level == value.level and self.exp == value.exp

    def toGuildArchitectureSavedDict(self):
        return {
            'level': self.level,
            'exp': self.exp,
        }


class GuildArchitectureInfo(object):
    def createObjFromDict(self, dataDict):
        obj = GuildArchitectureVal(**dataDict)
        return obj

    def getDictFromObj(self, obj):
        return obj.toGuildArchitectureSavedDict()

    def isSameType(self, obj):
        return type(obj) is GuildArchitectureVal


GuildArchitectureInstance = GuildArchitectureInfo()

