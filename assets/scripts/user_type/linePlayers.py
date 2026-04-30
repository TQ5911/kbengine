# -*- coding: utf-8 -*-
from KBEDebug import *

import utils

import userType

import math
import gametimer


class LinePlayerVal(userType.UserSingleType):
    NONE = 0
    ENTERING = 1
    IN_LINE = 2
    SWITCHING = 3

    def __init__(self, box, gbId, teamUUID, areaId, playerStatus, curSpaceNo, tEnter, guildUUID=0):
        self.playerBox = box
        self.gbId = gbId
        self.teamUUID = teamUUID
        self.areaId = areaId
        self.playerStatus = playerStatus
        self.curSpaceNo = curSpaceNo
        self.checkEnterTimer = 0
        self.statusArgs = None
        self.guildUUID = guildUUID
        self.tEnter = tEnter

    def onTeamChanged(self, teamUUID):
        self.teamUUID = teamUUID

    def onAreaChanged(self, areaId):
        self.areaId = areaId

    def setPlayerStatus(self, st, stArgs=None):
        self.playerStatus = st
        self.statusArgs = stArgs


class LinePlayers(userType.UserDictType):
    def __init__(self, lineNo):
        self.lineNo = lineNo
        self.pendingSec = 0
        self.pendingSecNum = 0
        self.areaPlayers = {}
        self.teamPlayers = {}
        self.pendingEnterPlayers = {}
        self.lastUpPlayerNum = 0

    def clearTimeOutInfo(self, timestamp):
        _clearList = []
        for gbId, sec in self.pendingEnterPlayers.items():
            if timestamp > sec:
                _clearList.append(gbId)

        for gbId in _clearList:
            self.pendingEnterPlayers.pop(gbId)

        _clearList = []

        for gbId, playerVal in self.items():
            if playerVal.playerStatus == LinePlayerVal.ENTERING:
                if timestamp > playerVal.tEnter:
                    _clearList.append(gbId)

        for gbId in _clearList:
            self.doRemoveLinePlayer(None, gbId)

        return _clearList

    def doAddLinePlayerVal(self, playerVal, isLeader):
        self[playerVal.gbId] = playerVal

        if playerVal.teamUUID:
            self.teamPlayers.setdefault(playerVal.teamUUID, {})
            self.teamPlayers[playerVal.teamUUID][playerVal.gbId] = isLeader

        if playerVal.areaId:
            self.areaPlayers.setdefault(playerVal.areaId, {})
            self.areaPlayers[playerVal.areaId][playerVal.gbId] = 1

        self.removePendingEnterPlayer(None, playerVal.gbId)

    def doAddLinePlayer(self, owner, box, gbId, teamUUID, areaId, status, curSpaceNo, extraInfo):
        self[gbId] = LinePlayerVal(box, gbId, teamUUID, areaId, status, curSpaceNo, utils.curTS(), extraInfo.get('selfGuildUUID', 0))

        if teamUUID:
            self.teamPlayers.setdefault(teamUUID, {})
            self.teamPlayers[teamUUID][gbId] = extraInfo.get('isLeader', False)

        if areaId:
            self.areaPlayers.setdefault(areaId, {})
            self.areaPlayers[areaId][gbId] = 1

        self.removePendingEnterPlayer(owner, gbId)

    def isTeamLeader(self, teamUUID, gbId):
        return self.teamPlayers.get(teamUUID, {}).get(gbId)

    def hasTeamMember(self, teamUUID):
        return self.teamPlayers.get(teamUUID)

    def getLeaderGbId(self, teamUUID):
        for gbId, isLeader in self.teamPlayers.get(teamUUID, {}).items():
            if isLeader:
                return gbId
        return 0

    def doRemoveLinePlayer(self, owner, gbId):
        pVal = self.pop(gbId, None)
        if not pVal:
            return False

        self._removeFromTeamPlayers(pVal)
        self._removeFromAreaPlayers(pVal)
        return True

    def _removeFromTeamPlayers(self, pVal):
        if pVal.teamUUID in self.teamPlayers:
            self.teamPlayers[pVal.teamUUID].pop(pVal.gbId, 0)
            if not self.teamPlayers[pVal.teamUUID]:
                self.teamPlayers.pop(pVal.teamUUID)

    def _removeFromAreaPlayers(self, pVal):
        if pVal.areaId in self.areaPlayers:
            self.areaPlayers[pVal.areaId].pop(pVal.gbId, 0)
            if not self.areaPlayers[pVal.areaId]:
                self.areaPlayers.pop(pVal.areaId)

    def onPlayerTeamChanged(self, gbId, oldTeamUUID, newTeamUUID, isLeader):
        pVal = self.get(gbId)
        if not pVal:
            return

        if oldTeamUUID and oldTeamUUID != pVal.teamUUID:
            LOG_WARN('teamUUID mismatch', pVal, gbId, oldTeamUUID, newTeamUUID)

        self._removeFromTeamPlayers(pVal)
        pVal.onTeamChanged(newTeamUUID)

        if newTeamUUID:
            self.teamPlayers.setdefault(newTeamUUID, {})
            self.teamPlayers[newTeamUUID][gbId] = isLeader

    def onPlayerAreaChanged(self, gbId, newArea):
        pVal = self.get(gbId)
        if not pVal:
            return

        if newArea == pVal.areaId:
            return

        self._removeFromAreaPlayers(pVal)
        pVal.onAreaChanged(newArea)

        if newArea:
            self.areaPlayers.setdefault(newArea, {})
            self.areaPlayers[newArea][gbId] = 1

    def playersInArea(self, areaId):
        return self.areaPlayers.get(areaId, {})

    def addPendingEnterPlayer(self, owner, gbId):
        if gbId in self.pendingEnterPlayers:
            self.removePendingEnterPlayer(owner, gbId)

        sec = utils.curTS()
        self.pendingEnterPlayers[gbId] = sec
        if self.pendingSec == sec:
            self.pendingSecNum += 1
        else:
            self.pendingSec = sec
            self.pendingSecNum = 1

    def removePendingEnterPlayer(self, owner, gbId):
        if gbId not in self.pendingEnterPlayers:
            return

        self.pendingEnterPlayers.pop(gbId)

    def getPendingEnterNum(self):
        return len(self.pendingEnterPlayers)

    def getPendingEnterNumNowSec(self):
        sec = utils.curTS()
        if self.pendingSec == sec:
            return self.pendingSecNum
        return 0


class AllLinePlayers(userType.UserDictType):
    def __init__(self, lineType):
        self.lineType = lineType

    def getLinePlayers(self, lineNo):
        return self.get(lineNo)

    def getPlayer(self, lineNo, gbId):
        if lineNo < 0:
            for playersVal in self.values():
                if gbId in playersVal:
                    return playersVal[gbId]
        else:
            linePlayers = self.getLinePlayers(lineNo)
            if not linePlayers:
                return None
            return linePlayers.get(gbId, None)

        return None

    def addLinePlayer(self, owner, lineNo, box, gbId, teamUUID, areaId, status, curSpaceNo, extraInfo):
        players = self.getLinePlayers(lineNo)
        players.doAddLinePlayer(owner, box, gbId, teamUUID, areaId, status, curSpaceNo, extraInfo)

    def removeLinePlayer(self, owner, lineNo, gbId):
        players = self.getLinePlayers(lineNo)
        if not players:
            return

        if not players.doRemoveLinePlayer(owner, gbId):
            LOG_ERR('zt: fail to remove player', lineNo, gbId)
            for ln, playersVal in self.items():
                if ln == lineNo:
                    continue
                if players.doRemoveLinePlayer(owner, gbId):
                    LOG_DBG('zt: remove player', ln, gbId)

