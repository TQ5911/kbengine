# -*- encoding:utf-8 -*-

from KBEDebug import *
import team


# ==================================
# TEAM DUNGEON INFO

class TeamDungeonInfo(object):
    def createObjFromDict(self, dataDict):
        _teamObj = self._Type()()
        _teamObj.initFromDict(dataDict)
        return _teamObj

    def getDictFromObj(self, obj):
        return obj.toStreamSavedDic()

    def _Type(self):
        return team.TeamDungeonCache

    def isSameType(self, obj):
        return type(obj) is self._Type()


teamDungeonCacheInstance = TeamDungeonInfo()


class TeamDungeonSpaceInfo(TeamDungeonInfo):

    def _Type(self):
        return team.TeamDungeonSpaceCacheVal

    def createObjFromDict(self, dataDict):
        _teamObj = self._Type()(0, 0, 0)
        _teamObj.initFromDict(dataDict)
        return _teamObj


teamDungeonSpaceCacheInstance = TeamDungeonSpaceInfo()

# ==================================


class TeamInfo(object):
    def createObjFromDict(self, dataDict):
        _teamObj = team.TeamVal()
        _teamObj.initFromDict(dataDict)
        return _teamObj

    def getDictFromObj(self, obj):
        return obj.toStreamSavedDic()

    def isSameType(self, obj):
        return type(obj) is team.TeamVal

teamInstance = TeamInfo()

class ApplyJoinInfo(object):
    def createObjFromDict(self, dataDic):
        _teamObj = team.ApplyJoinPlayerVal(
            dataDic['gbId'],
            dataDic['playerName'],
            dataDic['level'],
            dataDic['school'],
            dataDic['sex'],
            dataDic['score'],
            dataDic['applySource'],
        )
        return _teamObj

    def getDictFromObj(self, obj):
        return obj.toStreamSavedDic()

    def isSameType(self, obj):
        return type(obj) is team.ApplyJoinPlayerVal

applyJoinInfoInstance = ApplyJoinInfo()

class TeamInfoCache(object):
    def createObjFromDict(self, dataDict):
        teamObj = team.TeamCacheValInPlayer()
        teamObj.initFromDict(dataDict)
        return teamObj

    def getDictFromObj(self, obj):
        return obj.toStreamSavedDic()

    def isSameType(self, obj):
        return type(obj) is team.TeamCacheValInPlayer

teamCacheInstance = TeamInfoCache()
