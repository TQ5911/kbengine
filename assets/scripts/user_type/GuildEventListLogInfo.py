
# coding: utf-8

import userType
import gameconst
import utils
import GuildEventLogInfo


class GuildEventListLogVal(userType.UserSingleType):
    '''GUILD_EVENT_LIST_LOG_DATA_INFO'''
    def __init__(self, eventList=(), lastEventTS=0):
        self.eventList = eventList
        self.lastEventTS = lastEventTS

    def getTS(self):
        _ts = utils.getTimestamp64()
        if _ts <= self.lastEventTS:
            _ts = self.lastEventTS + 1

        self.lastEventTS = _ts
        return _ts

    def doAddGuildEvent(self, eventId, args):
        _e = GuildEventLogInfo.GuildEventLogVal(eventId, args, self.getTS())
        self.eventList.append(_e)

        while len(self.eventList) > gameconst.GUILD_EVENT_LOG_MAX_NUM:
            self.eventList.pop(0)

        return _e

    def toGuildEventListLogSavedDict(self):
        return {
            'eventList': self.eventList,
            'lastEventTS': self.lastEventTS,
        }


class GuildEventListLogInfo(object):
    def createObjFromDict(self, dataDict):
        obj = GuildEventListLogVal(**dataDict)
        return obj

    def getDictFromObj(self, obj):
        return obj.toGuildEventListLogSavedDict()

    def isSameType(self, obj):
        return type(obj) is GuildEventListLogVal


GuildEventListLogInstance = GuildEventListLogInfo()

