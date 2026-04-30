
# coding: utf-8

import userType


class GuildEventLogVal(userType.UserSingleType):
    '''GUILD_EVENT_LOG_DATA_INFO'''
    def __init__(self, eventId=0, args=0, ts=0):
        self.eventId = eventId
        self.args = args
        self.ts = ts

    def toGuildEventLogSavedDict(self):
        return {
            'eventId': self.eventId,
            'args': self.args,
            'ts': self.ts,
        }


class GuildEventLogInfo(object):
    def createObjFromDict(self, dataDict):
        obj = GuildEventLogVal(**dataDict)
        return obj

    def getDictFromObj(self, obj):
        return obj.toGuildEventLogSavedDict()

    def isSameType(self, obj):
        return type(obj) is GuildEventLogVal


GuildEventLogInstance = GuildEventLogInfo()

