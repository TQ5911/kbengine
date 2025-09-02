
# coding: utf-8

import userType


class GuildMembersVal(userType.UserDictType):
    '''GUILD_MEMBERS_DATA_INFO'''
    def __init__(self, members=()):
        for _gmVal in members:
            self[_gmVal.gbId] = _gmVal


    def toGuildMembersSavedDict(self):
        return {
            'members': list(self.values()),
        }


class GuildMembersInfo(object):
    def createObjFromDict(self, dataDict):
        obj = GuildMembersVal(**dataDict)
        return obj

    def getDictFromObj(self, obj):
        return obj.toGuildMembersSavedDict()

    def isSameType(self, obj):
        return type(obj) is GuildMembersVal


GuildMembersInstance = GuildMembersInfo()

