
# coding: utf-8

import userType
import LogTrackingMgr

class LeaderBoardAvatarCacheVal(userType.UserSingleType):
    '''LEADER_BOARD_AVATAR_CACHE_DATA_INFO'''
    def __init__(self, gbId=0, name='', level=0, school=0, ts=0, guildName='', guildUUID=0):
        self.gbId = gbId
        self.name = name
        self.level = level
        self.school = school
        self.ts = ts
        self.guildName = guildName
        self.guildUUID = guildUUID

    @property
    def key(self):
        return self.gbId

    @staticmethod
    def sortKeyFunc():
        return lambda x: (-x.level, x.ts)

    @staticmethod
    def maxNum():
        return 5

    @staticmethod
    def funcName():
        return 'onLeaderBoardAvatarLevel'

    @staticmethod
    def calcSchool():
        return True

    def toLeaderBoardCacheSavedDict(self):
        # 通用名字不能变
        return {
            'gbId': self.gbId,
            'name': self.name,
            'level': self.level,
            'school': self.school,
            'ts': self.ts,
            'guildName': self.guildName,
            'guildUUID': self.guildUUID,
        }

    # 必须实现
    def leaderBoardLog(self, leaderType, rank):
        LogTrackingMgr.LogTrackingMgr.LeaderBoard_Level(
            self.gbId,
            '',
            leaderType,
            rank,
            self.gbId,
            self.name,
            self.level,
            self.school,
            self.guildUUID,
            self.guildName,
        )


class LeaderBoardAvatarCacheInfo(object):
    def createObjFromDict(self, dataDict):
        obj = LeaderBoardAvatarCacheVal(**dataDict)
        return obj

    def getDictFromObj(self, obj):
        return obj.toLeaderBoardCacheSavedDict()

    def isSameType(self, obj):
        return type(obj) is LeaderBoardAvatarCacheVal


LeaderBoardAvatarCacheInstance = LeaderBoardAvatarCacheInfo()

