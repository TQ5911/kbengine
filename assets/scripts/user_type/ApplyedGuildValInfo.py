
# coding: utf-8

import userType
import gameconst


class ApplyedGuildValVal(userType.UserSoleType):
    '''APPLYED_GUILD_VAL_DATA_INFO'''
    def __init__(self, guildUUID=0, ts=0, name='', score=0, dspFlag=0, icon=0):
        self.guildUUID = guildUUID
        self.ts = ts
        self.name = name
        self.score = score
        self.dspFlag = dspFlag
        self.icon = icon

    def isTimeOut(self, now):
        return now - self.ts > gameconst.GUILD_APPLY_EXPIRED_TIME

    def toApplyedGuildValSavedDict(self):
        return {
            'guildUUID': self.guildUUID,
            'ts': self.ts,
            'name': self.name,
            'score': self.score,
            'dspFlag': self.dspFlag,
            'icon': self.icon
        }


class ApplyedGuildValInfo(object):
    def createObjFromDict(self, dataDict):
        obj = ApplyedGuildValVal(**dataDict)
        return obj

    def getDictFromObj(self, obj):
        return obj.toApplyedGuildValSavedDict()

    def isSameType(self, obj):
        return type(obj) is ApplyedGuildValVal


ApplyedGuildValInstance = ApplyedGuildValInfo()

