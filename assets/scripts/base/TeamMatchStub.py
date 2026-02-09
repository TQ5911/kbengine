# -*- coding: utf-8 -*-

from KBEDebug import *

import random
import gameengine
import gametimer
import gameglobal
import utils
import iBaseNoCell
import iGlobal
import iTimer
import userType
import gameconst
import teamMatch_activity as TMACTD
import teamMatch_matchConfig as TMMCD
import activityControl_activityData as AC_ADD


class TeamMatchStub(iGlobal.IGlobal, iBaseNoCell.IBaseNoCell, iTimer.ITimer):

    MATCH_LIST_MAX_NUM = 15

    def __init__(self):
        super(TeamMatchStub, self).__init__()
        self.teamsDic = {}
        self.playersDic = {}

        self.matchTeamsPool = {}
        self.matchPlayersPool = {}
        return

    def doNext(self):
        gameglobal.localBaseApp.fullPrepare(self.classname())
        self.initMatchData()
        return

    def initMatchData(self):
        self.teamsDic = {}
        self.playersDic = {}

        self.matchTeamsPool = {}
        self.matchPlayersPool = {}

        for tgtId, d in TMACTD.datas.items():
            if tgtId == 0:
                continue
            actData = AC_ADD.datas.get(int(d['pareActivity']))
            if actData and gameconst.ActivityControlType.TEAM == int(actData['needTeam']):
                self.matchTeamsPool[tgtId] = []
                self.matchPlayersPool[tgtId] = []

        self._callback(1, '_doMatch', (), gametimer.TIMER_TAG_DO_MATCH)
        self._callback(10, '_checkTimeOutMatch', (), gametimer.TIMER_TAG_CHECK_TIME_OUT_MATCH)
        return

    def postReloadScript(self):
        if hasattr(super(TeamMatchStub, self), 'postReloadScript'):
            super(TeamMatchStub, self).postReloadScript()
        for v in self.teamsDic.values():
            v.reloadScript()
        for v in self.playersDic.values():
            v.reloadScript()
        return

    def onTimer(self, tid, userArg):
        self._onTimer(tid, userArg)
        if utils.isBelongTimerTag(userArg):
            self._onTimerCallback(tid)

    def teamAutoMatch(self, teamInfoDic):
        INFO_MSG('in teamAutoMatch:', teamInfoDic)
        if 0 == teamInfoDic['teamTarget']:
            return
        tmVal = self.teamsDic.get(teamInfoDic['teamId'])
        if tmVal:
            self._rmTeamFromMatchPool(teamInfoDic['teamId'])

        tmVal = TeamMatchVal(teamInfoDic, utils.getNow())
        if tmVal.isTeamFull():
            return
        self._addTeamToPool(tmVal)
        return

    def onTeamInfoUpdate(self, teamInfoDic):
        INFO_MSG('in onTeamInfoUpdate:', teamInfoDic)
        if 0 == teamInfoDic['teamTarget']:
            self._rmTeamFromMatchPool(teamInfoDic['teamId'])
            return
        tmVal = self.teamsDic.get(teamInfoDic['teamId'])
        if not tmVal:
            return
        tmVal.updateFromTeamInfoDic(teamInfoDic)
        if tmVal.isTeamFull():
            self._rmTeamFromMatchPool(teamInfoDic['teamId'])
        return

    def _addTeamToPool(self, tmVal):
        self.teamsDic[tmVal.teamId] = tmVal
        self.matchTeamsPool[tmVal.teamTarget].append(tmVal.teamId)
        return

    def teamStopAutoMatch(self, teamId):
        INFO_MSG('in teamStopAutoMatch:', teamId)
        self._rmTeamFromMatchPool(teamId)
        return

    def _rmTeamFromMatchPool(self, teamId):
        tmVal = self.teamsDic.pop(teamId, None)
        if not tmVal:
            return
        if teamId in self.matchTeamsPool[tmVal.teamTarget]:
            self.matchTeamsPool[tmVal.teamTarget].remove(teamId)
        return True

    def onPlayerMatchInfoUpdate(self, playerInfoDic):
        INFO_MSG('in onPlayerMatchInfoUpdate:', playerInfoDic)
        pmVal = self.playersDic.get(playerInfoDic['playerGbId'], None)
        if not pmVal:
            return
        pmVal.updateMatchProp(playerInfoDic)
        return

    def playerAutoMatch(self, playerMatchDic):
        INFO_MSG('in playerAutoMatch:', playerMatchDic)
        pmVal = self.playersDic.get(playerMatchDic['playerGbId'], None)
        if pmVal:
            self._rmPlayerFromMatchPool(playerMatchDic['playerGbId'])

        now = utils.getNow()
        pmVal = PlayerMatchVal(playerMatchDic, utils.getNow())
        self._playerStartMatch(pmVal)
        playerMatchDic['playerBox'].cell.onCellPlayerStartAutoMatch(now, playerMatchDic['target'])
        return

    def _playerStartMatch(self, pmVal):
        self.playersDic[pmVal.playerGbId] = pmVal
        self.matchPlayersPool[pmVal.target].append(pmVal.playerGbId)
        return

    def playerMatchedSucc(self, playerGbId):
        pmVal = self.playersDic.get(playerGbId, None)
        if not pmVal:
            return
        if self._rmPlayerFromMatchPool(playerGbId):
            pmVal.playerBox.cell.onPlayerMatchedSucc()
        return

    def playerStopAutoMatch(self, playerGbId):
        INFO_MSG('in playerStopAutoMatch:', playerGbId)
        pmVal = self.playersDic.get(playerGbId, None)
        if not pmVal:
            return
        if self._rmPlayerFromMatchPool(playerGbId):
            pass
        return

    def playerAutoMatchTimeout(self, playerGbId):
        INFO_MSG('in playerAutoMatchTimeout:', playerGbId)
        pmVal = self.playersDic.get(playerGbId, None)
        if not pmVal:
            return
        if self._rmPlayerFromMatchPool(playerGbId):
            pmVal.playerBox.cell.onPlayerAutoMatchTimeout()
        return

    def _rmPlayerFromMatchPool(self, playerGbId):
        INFO_MSG('in _rmPlayerFromMatchPool:', playerGbId)
        pmVal = self.playersDic.pop(playerGbId, None)
        if not pmVal:
            return False
        if playerGbId in self.matchPlayersPool[pmVal.target]:
            self.matchPlayersPool[pmVal.target].remove(playerGbId)
        return True

    def _doMatch(self):
        self._callback(3, '_doMatch', (), gametimer.TIMER_TAG_DO_MATCH)
        if len(self.teamsDic) > 0 or len(self.playersDic) > 0:
            # DEBUG_MSG('in _doMatch, matchPlayersPool:', self.matchPlayersPool)
            # DEBUG_MSG('in _doMatch, matchTeamsPool:', self.matchTeamsPool)
            try:
                matchedPlayers = []
                for playerGbid, pmVal in self.playersDic.items():
                    tgtId = pmVal.target
                    if 0 == tgtId:
                        continue
                    fullTeams = []
                    for teamId in self.matchTeamsPool[tgtId]:
                        tmVal = self.teamsDic.get(teamId, None)
                        if not tmVal:
                            continue
                        if not tmVal.canAddPlayer(pmVal):
                            continue
                        #matched
                        INFO_MSG('     in _doMatch, matched:', playerGbid, teamId)
                        if tmVal.addPlayerToTeam(pmVal):
                            matchedPlayers.append(playerGbid)
                            if tmVal.isTeamFull():
                                fullTeams.append(teamId)
                            break
                    for rmTeamId in fullTeams:
                        self.teamStopAutoMatch(rmTeamId)
                for rmPlayeId in matchedPlayers:
                    self.playerMatchedSucc(rmPlayeId)
            except Exception as e:
                ERROR_MSG('in _doMatch, exception:', e)
        return

    def _checkTimeOutMatch(self):
        #DEBUG_MSG('in _checkTimeOutMatch')
        self._callback(10, '_checkTimeOutMatch', (), gametimer.TIMER_TAG_CHECK_TIME_OUT_MATCH)
        rmPlayers = []
        for playerGbid, pmVal in self.playersDic.items():
            if pmVal.isTimeOut():
                rmPlayers.append(playerGbid)
                DEBUG_MSG('     in _checkTimeOutMatch, rmPlayers:', rmPlayers)
        for rmPlayeId in rmPlayers:
            self.playerAutoMatchTimeout(rmPlayeId)
        fullTeams = []
        for teamId, tmVal in self.teamsDic.items():
            if tmVal.isTeamFull():
                fullTeams.append(teamId)

        for rmTeamId in fullTeams:
            self.teamStopAutoMatch(rmTeamId)

class TeamMatchVal(userType.UserSoleType):
    def __init__(self, teamInfoDic, startTime):
        self.teamId = teamInfoDic['teamId']
        self.teamTarget = teamInfoDic['teamTarget']
        self.teamCaptainGbId = teamInfoDic['teamCaptainGbId']
        self.teamMinLv = teamInfoDic['teamMinLv']
        self.teamMinScore = teamInfoDic['teamMinScore']
        self.teamPlayerDic = teamInfoDic['teamPlayerDic']
        self.startTime = startTime
        self.guildUUID = teamInfoDic.get('guildUUID', 0)

    def updateFromTeamInfoDic(self, teamInfoDic):
        self.teamId = teamInfoDic['teamId']
        self.teamTarget = teamInfoDic['teamTarget']
        self.teamCaptainGbId = teamInfoDic['teamCaptainGbId']
        self.teamMinLv = teamInfoDic['teamMinLv']
        self.teamMinScore = teamInfoDic['teamMinScore']
        self.teamPlayerDic = teamInfoDic['teamPlayerDic']
        guildUUID = teamInfoDic.get('guildUUID')
        if guildUUID:
            self.guildUUID = guildUUID

    def addPlayerToTeam(self, pmVal):
        self.teamPlayerDic[pmVal.playerGbId] = (pmVal.level, pmVal.playerName, pmVal.school, pmVal.sex)
        extraNum = len(self.teamPlayerDic)-gameconst.TEAM_MEMBER_MAX_NUM
        if extraNum > 0:
            gameengine.reportCritical('addPlayerToTeam, player exceed max num:', self.teamPlayerDic)
        pmVal.playerBox.cell.onPlayerMatchedTeam(self.teamId)
        return True

    def canAddPlayer(self,  pmVal):
        if self.teamTarget != pmVal.target:
            return False
        if self.isTeamFull():
            return False
        if pmVal.level < self.teamMinLv:
            return False
        if pmVal.score < self.teamMinScore:
            return False
        return True

    def isTeamFull(self):
        return len(self.teamPlayerDic) >= gameconst.TEAM_MEMBER_MAX_NUM

    def isTimeOut(self):
        maxMatchTime = TMMCD.datas['maxMatchTime']['value']
        return self.startTime + maxMatchTime < utils.getNow()

class PlayerMatchVal(userType.UserSoleType):
    def __init__(self, playerInfoDic, startTime):
        self.target = playerInfoDic['target']
        self.playerGbId = playerInfoDic['playerGbId']
        self.playerBox = playerInfoDic['playerBox']
        self.playerName = playerInfoDic['playerName']
        self.level = playerInfoDic['level']
        self.school = playerInfoDic['school']
        self.sex = playerInfoDic['sex']
        self.spaceNo = playerInfoDic['spaceNo']
        self.startTime = startTime
        self.guildUUID = playerInfoDic.get('guildUUID', 0)
        self.score = playerInfoDic.get('score', 0)

    def isTimeOut(self):
        maxMatchTime = TMMCD.datas['maxMatchTime']['value']
        return self.startTime + maxMatchTime < utils.getNow()

    def updateMatchProp(self, playerInfoDic):
        #self.__dict__.update(playInfoDic)
        self.playerGbId = playerInfoDic['playerGbId']
        self.playerBox = playerInfoDic['playerBox']
        self.level = playerInfoDic['level']
        self.spaceNo = playerInfoDic['spaceNo']
        guildUUID = playerInfoDic.get('guildUUID')
        if guildUUID:
            self.guildUUID = guildUUID
