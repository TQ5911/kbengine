
# coding: utf-8

import userType


class LeaderBoardAvatarScoreVal(userType.UserSoleType):
    '''LEADER_BOARD_AVATAR_SCORE_DATA_INFO'''
    def __init__(self, gbId=0, name='', score=0, ts=0, level=0, school=0, guildName='', guildUUID=0):
        self.gbId = gbId
        self.name = name
        self.score = score
        self.ts = ts
        self.level = level
        self.school = school
        self.guildName = guildName
        self.guildUUID = guildUUID

    @property
    def key(self):
        return self.gbId

    @staticmethod
    def sortKeyFunc():
        return lambda x: (-x.score, -x.level, x.ts)

    @staticmethod
    def maxNum():
        return 5

    @staticmethod
    def funcName():
        return 'onLeaderBoardAvatarScore'

    @staticmethod
    def calcSchool():
        return True

    def toLeaderBoardCacheSavedDict(self):
        # 通用名字不能变
        return {
            'gbId': self.gbId,
            'name': self.name,
            'score': self.score,
            'ts': self.ts,
            'level': self.level,
            'school': self.school,
            'guildName': self.guildName,
            'guildUUID': self.guildUUID,
        }


class LeaderBoardAvatarScoreInfo(object):
    def createObjFromDict(self, dataDict):
        obj = LeaderBoardAvatarScoreVal(**dataDict)
        return obj

    def getDictFromObj(self, obj):
        return obj.toLeaderBoardCacheSavedDict()

    def isSameType(self, obj):
        return type(obj) is LeaderBoardAvatarScoreVal


LeaderBoardAvatarScoreInstance = LeaderBoardAvatarScoreInfo()

