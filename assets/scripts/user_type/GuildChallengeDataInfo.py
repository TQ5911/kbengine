
# coding: utf-8

import userType


class GuildChallengeDataInfoVal(userType.UserSoleType):
    '''GUILD_CHALLENGE_DATA_INFO'''
    def __init__(self, openedFundCount = 0, openedMoneyCount = 0, openedTime = 0, openedType = 0, consumedType = 0, openedDungeonId = 0, openedDungeonStatus = 0):
        self.openedFundCount = openedFundCount
        self.openedMoneyCount = openedMoneyCount
        self.openedTime = openedTime
        self.openedType = openedType
        self.consumedType = consumedType
        self.openedDungeonId = 0
        self.openedDungeonStatus = 0
        self.waitEnterDungeonData = {}
        self.spaceNo = 0

    def toSavedDict(self):
        return {
            'openedFundCount': self.openedFundCount,
            'openedMoneyCount': self.openedMoneyCount,
            'openedTime': self.openedTime,
            'openedType': self.openedType,
            'consumedType': self.consumedType,
        }

    def toClientInfo(self):
        return {
            'openedFundCount': self.openedFundCount,
            'openedMoneyCount': self.openedMoneyCount,
            'openedTime': self.openedTime,
            'openedType': self.openedType,
            'openedDungeonId': self.openedDungeonId,
            'consumedType': self.consumedType,
            'openedDungeonStatus': self.openedDungeonStatus,
        }
    
    def reset(self):
        self.openedFundCount = 0
        self.openedMoneyCount = 0
        self.openedTime = 0
        self.openedType = 0
        self.openedDungeonId = 0
        self.openedDungeonStatus = 0
        self.consumedType = 0
        self.waitEnterDungeonData = {}
        self.spaceNo = 0
    
    def __eq__(self, value: object) -> bool:
        if not isinstance(value, GuildChallengeDataInfoVal):
            return False

        return self.openedFundCount == value.openedFundCount and \
                self.openedMoneyCount == value.openedMoneyCount and \
                self.openedTime == value.openedTime and \
                self.openedType == value.openedType and \
                self.consumedType == value.consumedType

    def createObjFromDict(self, dataDict):
        obj = GuildChallengeDataInfoVal(**dataDict)
        return obj

    def getDictFromObj(self, obj):
        return obj.toSavedDict()

    def isSameType(self, obj):
        return type(obj) is GuildChallengeDataInfoVal
    
GuildChallengeDataInfoInstance = GuildChallengeDataInfoVal()

