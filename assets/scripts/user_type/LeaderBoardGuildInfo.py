
# coding: utf-8

import userType
import LogTrackingMgr

class LeaderBoardGuildVal(userType.UserSingleType):
    '''LEADER_BOARD_GUILD_DATA_INFO'''
    def __init__(self, guildUUID=0, guildName="", leaderName="", guildLevel=0, guildScore=0, ts=0):
        self.guildUUID = guildUUID
        self.guildName = guildName
        self.leaderName = leaderName
        self.guildLevel = guildLevel
        self.guildScore = guildScore
        self.ts = ts

    def __eq__(self, other):
        return self.guildUUID == other.guildUUID\
            and self.guildName == other.guildName\
            and self.leaderName == other.leaderName\
            and self.guildLevel == other.guildLevel\
            and self.guildScore == other.guildScore\
            and self.ts == other.ts

    @property
    def key(self):
        return self.guildUUID

    @staticmethod
    def maxNum():
        return 5

    @staticmethod
    def sortKeyFunc():
        return lambda x: (-x.guildLevel, -x.guildScore, x.ts)

    @staticmethod
    def funcName():
        return 'onLeaderBoardGuild'

    @staticmethod
    def calcSchool():
        return False

    # 必须实现
    def leaderBoardLog(self, leaderType, rank):
        LogTrackingMgr.LogTrackingMgr.LeaderBoard_Guild(
            leaderType,
            rank,
            self.guildUUID,
            self.guildName,
            self.guildLevel,
            self.guildScore,
        )

    def toLeaderBoardCacheSavedDict(self):
        # 通用名字不能变
        return {
            "guildUUID": self.guildUUID,
            "guildName": self.guildName,
            "leaderName": self.leaderName,
            "guildLevel": self.guildLevel,
            "guildScore": self.guildScore,
            "ts": self.ts
        }


class LeaderBoardGuildInfo(object):
    def createObjFromDict(self, dataDict):
        obj = LeaderBoardGuildVal(**dataDict)
        return obj

    def getDictFromObj(self, obj):
        return obj.toLeaderBoardCacheSavedDict()

    def isSameType(self, obj):
        return type(obj) is LeaderBoardGuildVal


LeaderBoardGuildInstance = LeaderBoardGuildInfo()

