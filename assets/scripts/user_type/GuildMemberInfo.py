# coding: utf-8

import userType
import utils
import gameconst


class GuildMemberVal(userType.UserSoleType):
    # GUILD_MEMBER_DATA_INFO
    def __init__(self, gbId=0, job=0, name='', level=0, school=0, sex=0, score=0, tmpFlag=0, offlineTime=0, fund=0):
        self.gbId = gbId
        self.box = None
        self.job = job
        self.sex = sex
        self.name = name
        self.level = level
        self.school = school
        self.score = score
        self.tmpFlag = tmpFlag
        self.offlineTime = offlineTime
        self.fund = fund # 公会资金

    def setProperty(self, propName, propValue):
        setattr(self, propName, propValue)
        if propName == 'box':
            if propValue is None:
                self.offlineTime = utils.getNow()
                self.tmpFlag = utils.bitReset(self.tmpFlag, gameconst.GuildTmpFlag.ONLINE)
            else:
                self.tmpFlag = utils.bitSet(self.tmpFlag, gameconst.GuildTmpFlag.ONLINE)

        self.tmpFlag = utils.bitSet(self.tmpFlag, gameconst.GuildTmpFlag.DIRTY)

    def updateFromFcVal(self, fcVal):
        self.name = fcVal.name
        self.level = fcVal.level
        self.school = fcVal.school
        self.sex = fcVal.sex
        self.score = fcVal.battleEffect
        self.offlineTime = fcVal.offlineTime

    def toGuildMemberSavedDict(self):
        return {
            'gbId': self.gbId,
            'job': self.job,
            'name': self.name,
            'sex': self.sex,
            'level': self.level,
            'school': self.school,
            'score': self.score,
            'tmpFlag': self.tmpFlag,
            'offlineTime': self.offlineTime,
            'fund': self.fund,
        }


class GuildMemberInfo(object):
    def createObjFromDict(self, dataDict):
        obj = GuildMemberVal(**dataDict)
        return obj

    def getDictFromObj(self, obj):
        return obj.toGuildMemberSavedDict()

    def isSameType(self, obj):
        return type(obj) is GuildMemberVal


GuildMemberInstance = GuildMemberInfo()

