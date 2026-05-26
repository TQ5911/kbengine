# -*- encoding:utf-8 -*-

from KBEDebug import *
import team


# ==================================
# TEAM DUNGEON INFO

class TeamDungeonInfo(object):
    def createObjFromDict(self, dataDict):
        teamObj = self._Type()()
        teamObj.initFromDict(dataDict)
        return teamObj

    def getDictFromObj(self, obj):
        return obj.toSavedDict()

    def isSameType(self, obj):
        return type(obj) is self._Type()

    def _Type(self):
        return team.TeamDungeonCache


teamDungeonCacheInstance = TeamDungeonInfo()


class TeamDungeonSpaceInfo(TeamDungeonInfo):

    def createObjFromDict(self, dataDict):
        teamObj = self._Type()(0, 0, 0)
        teamObj.initFromDict(dataDict)
        return teamObj

    def _Type(self):
        return team.TeamDungeonSpaceCacheVal


teamDungeonSpaceCacheInstance = TeamDungeonSpaceInfo()

# ==================================


class TeamInfo(object):
    def createObjFromDict(self, dataDict):
        teamObj = team.TeamVal()
        teamObj.initFromDict(dataDict)
        return teamObj

    def getDictFromObj(self, obj):
        return obj.toSavedDict()

    def isSameType(self, obj):
        return type(obj) is team.TeamVal

teamInstance = TeamInfo()

class ApplyJoinInfo(object):
    def createObjFromDict(self, dataDict):
        teamObj = team.ApplyJoinPlayerVal(dataDict['gbId'],
                                          dataDict['playerName'],
                                          dataDict['level'],
                                          dataDict['school'],
                                          dataDict['sex'],
                                          dataDict['score'],
                                          dataDict['applySource'])
        return teamObj

    def getDictFromObj(self, obj):
        return obj.toSavedDict()

    def isSameType(self, obj):
        return type(obj) is team.ApplyJoinPlayerVal

applyJoinInfoInstance = ApplyJoinInfo()

class TeamInfoCache(object):
    def createObjFromDict(self, dataDict):
        teamObj = team.PlayerTeamCacheVal()
        teamObj.initFromDict(dataDict)
        return teamObj

    def getDictFromObj(self, obj):
        return obj.toSavedDict()

    def isSameType(self, obj):
        return type(obj) is team.PlayerTeamCacheVal

teamCacheInstance = TeamInfoCache()
