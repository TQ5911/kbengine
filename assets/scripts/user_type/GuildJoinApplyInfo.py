
# coding: utf-8

import userType
import gameconst
import guild_guildConst as G_GCD


class GuildJoinApplyVal(userType.UserSoleType):
    '''GUILD_JOIN_APPLY_DATA_INFO'''
    def __init__(self, gbId=0, level=0, score=0, ts=0, sex=0, school=0, name=''):
        self.gbId = gbId
        self.level = level
        self.score = score
        self.ts = ts
        self.sex = sex
        self.school = school
        self.name = name

    def isTimeOut(self, now):
        return now - self.ts > gameconst.GUILD_APPLY_TIME_OUT_DUR

    def updateFromApplyData(self, applyData):
        for k, v in applyData.items():
            setattr(self, k, v)

    def toGuildJoinApplySavedDict(self):
        return {
            'gbId': self.gbId,
            'level': self.level,
            'score': self.score,
            'ts': self.ts,
            'sex': self.sex,
            'school': self.school,
            'name': self.name,
        }


class GuildJoinApplyInfo(object):
    def createObjFromDict(self, dataDict):
        obj = GuildJoinApplyVal(**dataDict)
        return obj

    def getDictFromObj(self, obj):
        return obj.toGuildJoinApplySavedDict()

    def isSameType(self, obj):
        return type(obj) is GuildJoinApplyVal


GuildJoinApplyInstance = GuildJoinApplyInfo()

