# coding: utf-8

import userType
import utils
import gameconst
import LogTrackingMgr
import guildAuthorization_authorization as GA_AD


class GuildMemberVal(userType.UserSingleType):
    # GUILD_MEMBER_DATA_INFO
    def __init__(self, gbId=0, job=0, name='', level=0, school=0, sex=0, score=0, tmpFlag=0, offlineTime=0, fund=0, joinTime=0, histCond=0, commissionGold=0, commissionGoldDaily=0, commissionCumTenure=0, jobPositionTime=0):
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
        self.joinTime = joinTime
        self.histCond = histCond
        self.commissionGold = commissionGold
        self.commissionGoldDaily = commissionGoldDaily
        self.commissionCumTenure = commissionCumTenure
        self.jobPositionTime = jobPositionTime
        LogTrackingMgr.LogTrackingMgr.Guild_User_Set(
            self.gbId,
            '',
            GA_AD.datas[self.job]["name"] if self.job in GA_AD.datas else '',
        )

    def setProperty(self, propName, propValue):
        setattr(self, propName, propValue)
        if propName == 'box':
            if propValue is None:
                self.offlineTime = utils.curTS()
                self.tmpFlag = utils.breset(self.tmpFlag, gameconst.GuildTmpFlag.ONLINE)
            else:
                self.tmpFlag = utils.bset(self.tmpFlag, gameconst.GuildTmpFlag.ONLINE)

        self.tmpFlag = utils.bset(self.tmpFlag, gameconst.GuildTmpFlag.DIRTY)

        if propName == 'job':
            LogTrackingMgr.LogTrackingMgr.Guild_User_Set(
                self.gbId,
                '',
                GA_AD.datas[propValue]["name"] if propValue in GA_AD.datas else '',
            )

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
            'joinTime': self.joinTime,
            'histCond': self.histCond,
            'commissionGold': self.commissionGold,
            'commissionGoldDaily': self.commissionGoldDaily,
            'commissionCumTenure': self.commissionCumTenure,
            'jobPositionTime': self.jobPositionTime,
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

