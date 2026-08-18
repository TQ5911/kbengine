# -*- coding: utf-8 -*-
from KBEDebug import *

import utils

import userType

import math
import gametimer


class LinePlayerVal(userType.UserSingleType):
    NONE = 0
    ENTERING = 1
    INLINE = 2
    SWITCHING = 3

    def __init__(self, box, gbId, teamUUID, areaId, playerStatus, curSpaceNo, tEnter, guildUUID=0):
        self.playerBox = box
        self.gbId = gbId
        self.areaId = areaId
        self.teamUUID = teamUUID
        self.playerStatus = playerStatus
        self.curSpaceNo = curSpaceNo
        self.checkEnterTimer = 0
        self.statusArgs = None
        self.guildUUID = guildUUID
        self.tEnter = tEnter

    def setPlayerStatus(self, st, stArgs=None):
        self.playerStatus = st
        self.statusArgs = stArgs

    def onAreaChanged(self, areaId):
        self.areaId = areaId

    def onTeamChanged(self, teamUUID):
        self.teamUUID = teamUUID


class LinePlayers(userType.UserDictType):
    def __init__(self, lineNo):
        self.pendingSec = 0
        self.lineNo = lineNo
        self.pendingSecNum = 0
        self.teamPlayersDic = {}
        self.areaPlayersDic = {}
        self.pendingEnterPlayersDic = {}
        self.lastUpPlayerNum = 0

    def clearTimeOutInfo(self, timestamp):
        _clearList = []
        for gbId, sec in self.pendingEnterPlayersDic.items():
            if timestamp > sec:
                _clearList.append(gbId)

        for gbId in _clearList:
            self.pendingEnterPlayersDic.pop(gbId)

        _clearList = []

        for gbId, playerVal in self.items():
            if playerVal.playerStatus == LinePlayerVal.ENTERING:
                if timestamp > playerVal.tEnter:
                    _clearList.append(gbId)

        for gbId in _clearList:
            self.doRemoveLinePlayer(gbId)

        return _clearList

    def doAddLinePlayerVal(self, playerVal, isLeader):
        self[playerVal.gbId] = playerVal

        if playerVal.teamUUID:
            self.teamPlayersDic.setdefault(playerVal.teamUUID, {})
            self.teamPlayersDic[playerVal.teamUUID][playerVal.gbId] = isLeader

        if playerVal.areaId:
            self.areaPlayersDic.setdefault(playerVal.areaId, {})
            self.areaPlayersDic[playerVal.areaId][playerVal.gbId] = 1

        self.removePendingEnterPlayer(playerVal.gbId)

    def doAddLinePlayer(self, owner, box, gbId, teamUUID, areaId, status, curSpaceNo, extra):
        self[gbId] = LinePlayerVal(
            box, 
            gbId, 
            teamUUID,
            areaId,
            status,
            curSpaceNo, 
            utils.curTS(), 
            extra.get('selfGuildUUID', 0))

        if teamUUID:
            self.teamPlayersDic.setdefault(teamUUID, {})
            self.teamPlayersDic[teamUUID][gbId] = extra.get('isLeader', False)

        if areaId:
            self.areaPlayersDic.setdefault(areaId, {})
            self.areaPlayersDic[areaId][gbId] = 1

        self.removePendingEnterPlayer(gbId)

    def isTeamLeader(self, teamUUID, gbId):
        return self.teamPlayersDic.get(teamUUID, {}).get(gbId)

    def hasTeamMember(self, teamUUID):
        return self.teamPlayersDic.get(teamUUID)

    def getLeaderGbId(self, teamUUID):
        for gbId, isLeader in self.teamPlayersDic.get(teamUUID, {}).items():
            if isLeader:
                return gbId
        return 0

    def doRemoveLinePlayer(self, gbId):
        _pVal = self.pop(gbId, None)
        if not _pVal:
            return False

        self._removeFromTeamPlayers(_pVal)
        self._removeFromAreaPlayers(_pVal)
        return True

    def _removeFromTeamPlayers(self, pVal):
        if pVal.teamUUID in self.teamPlayersDic:
            self.teamPlayersDic[pVal.teamUUID].pop(pVal.gbId, 0)
            if not self.teamPlayersDic[pVal.teamUUID]:
                self.teamPlayersDic.pop(pVal.teamUUID)

    def _removeFromAreaPlayers(self, pVal):
        if pVal.areaId in self.areaPlayersDic:
            self.areaPlayersDic[pVal.areaId].pop(pVal.gbId, 0)
            if not self.areaPlayersDic[pVal.areaId]:
                self.areaPlayersDic.pop(pVal.areaId)

    def onPlayerTeamChanged(self, gbId, oldTeamUUID, newTeamUUID, isLeader):
        _pVal = self.get(gbId)
        if not _pVal:
            return

        if oldTeamUUID and oldTeamUUID != _pVal.teamUUID:
            LOG_WARN('teamUUID mismatch', _pVal, gbId, oldTeamUUID, newTeamUUID)

        self._removeFromTeamPlayers(_pVal)
        _pVal.onTeamChanged(newTeamUUID)

        if newTeamUUID:
            self.teamPlayersDic.setdefault(newTeamUUID, {})
            self.teamPlayersDic[newTeamUUID][gbId] = isLeader

    def onPlayerAreaChanged(self, gbId, newArea):
        _pVal = self.get(gbId)
        if not _pVal:
            return

        if newArea == _pVal.areaId:
            return

        self._removeFromAreaPlayers(_pVal)
        _pVal.onAreaChanged(newArea)

        if newArea:
            self.areaPlayersDic.setdefault(newArea, {})
            self.areaPlayersDic[newArea][gbId] = 1

    def playersInArea(self, areaId):
        return self.areaPlayersDic.get(areaId, {})

    def doAddPendingEnterPlayer(self, owner, gbId):
        if gbId in self.pendingEnterPlayersDic:
            self.removePendingEnterPlayer(gbId)

        _sec = utils.curTS()
        self.pendingEnterPlayersDic[gbId] = _sec
        if self.pendingSec == _sec:
            self.pendingSecNum += 1
        else:
            self.pendingSec = _sec
            self.pendingSecNum = 1

    def doEnterSpaceFailed(self, gbId):
        if gbId in self.pendingEnterPlayersDic:
            self.removePendingEnterPlayer(gbId)
            return False

        return self.doRemoveLinePlayer(gbId)

    def removePendingEnterPlayer(self, gbId):
        if gbId not in self.pendingEnterPlayersDic:
            return

        self.pendingEnterPlayersDic.pop(gbId)

    def getPendingEnterNum(self):
        return len(self.pendingEnterPlayersDic)

    def getPendingEnterNumNowSec(self):
        sec = utils.curTS()
        if self.pendingSec == sec:
            return self.pendingSecNum
        return 0


class AllLinePlayers(userType.UserDictType):
    def __init__(self, lineType):
        self.lineType = lineType

    def getPlayer(self, lineNo, gbId):
        if lineNo < 0:
            for _playersVal in self.values():
                if gbId in _playersVal:
                    return _playersVal[gbId]
        else:
            _linePlayers = self.getLinePlayers(lineNo)
            if not _linePlayers:
                return None
            return _linePlayers.get(gbId, None)

        return None

    def getLinePlayers(self, lineNo):
        return self.get(lineNo)

    def addLinePlayer(self, owner, lineNo, box, gbId, teamUUID, areaId, status, curSpaceNo, extra):
        _players = self.getLinePlayers(lineNo)
        _players.doAddLinePlayer(owner, box, gbId, teamUUID, areaId, status, curSpaceNo, extra)

    def removeLinePlayer(self, owner, lineNo, gbId):
        _players = self.getLinePlayers(lineNo)
        if not _players:
            return

        if not _players.doRemoveLinePlayer(gbId):
            LOG_ERR('zt: fail to remove player', lineNo, gbId)
            for ln, playersVal in self.items():
                if ln == lineNo:
                    continue
                if _players.doRemoveLinePlayer(gbId):
                    LOG_DBG('zt: remove player', ln, gbId)

