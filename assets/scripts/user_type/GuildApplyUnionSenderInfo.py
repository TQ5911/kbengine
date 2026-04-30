
# coding: utf-8

import userType


class GuildApplyUnionSenderVal(userType.UserSingleType):
    '''GUILD_APPLY_UNION_SENDER_DATA_INFO'''
    def __init__(self, guildUUID, guildName, guildIcon, flag, guildScore, endTime):
        self.guildUUID = guildUUID
        self.guildName = guildName
        self.guildIcon = guildIcon
        self.flag = flag
        self.guildScore = guildScore
        self.endTime = endTime

    def toGuildApplyUnionSenderSavedDict(self):
        return {
            'guildUUID': self.guildUUID,
            'guildName': self.guildName,
            'guildIcon': self.guildIcon,
            'flag': self.flag,
            'guildScore': self.guildScore,
            'endTime': self.endTime,
        }


class GuildApplyUnionSenderInfo(object):
    def createObjFromDict(self, dataDict):
        obj = GuildApplyUnionSenderVal(**dataDict)
        return obj

    def getDictFromObj(self, obj):
        return obj.toGuildApplyUnionSenderSavedDict()

    def isSameType(self, obj):
        return type(obj) is GuildApplyUnionSenderVal


GuildApplyUnionSenderInstance = GuildApplyUnionSenderInfo()

