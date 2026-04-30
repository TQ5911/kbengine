
# coding: utf-8

import userType


class GuildApplyUnionVal(userType.UserSingleType):
    '''GUILD_APPLY_UNION_DATA_INFO'''
    def __init__(self, guildUUID=0, endTime=0, guildName='', guildIcon=0, flag=0, guildScore=0, guildLevel=0):
        self.guildUUID = guildUUID
        self.endTime = endTime
        self.guildName = guildName
        self.guildIcon = guildIcon
        self.flag = flag
        self.guildScore = guildScore
        self.guildLevel = guildLevel

    def toGuildApplyUnionSavedDict(self):
        return {
            'guildUUID': self.guildUUID,
            'endTime': self.endTime,
            'guildName': self.guildName,
            'guildIcon': self.guildIcon,
            'flag': self.flag,
            'guildScore': self.guildScore,
            'guildLevel': self.guildLevel,
        }


class GuildApplyUnionInfo(object):
    def createObjFromDict(self, dataDict):
        obj = GuildApplyUnionVal(**dataDict)
        return obj

    def getDictFromObj(self, obj):
        return obj.toGuildApplyUnionSavedDict()

    def isSameType(self, obj):
        return type(obj) is GuildApplyUnionVal


GuildApplyUnionInstance = GuildApplyUnionInfo()

