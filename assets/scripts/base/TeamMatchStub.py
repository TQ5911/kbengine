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
    def __init__(self):
        super(TeamMatchStub, self).__init__()
        self.playersDic = {}
        self.teamsDic = {}

        self.teamsMatchPool = {}
        self.playersMatchPool = {}

    def doNext(self):
        gameglobal.localBaseApp.fullPrepare(self.classname())
        self.initMatchData()

    def initMatchData(self):
        self.playersDic = {}
        self.teamsDic = {}

        self.teamsMatchPool = {}
        self.playersMatchPool = {}

        for tgtId, d in TMACTD.datas.items():
            if tgtId == 0:
                continue
            actData = AC_ADD.datas.get(int(d['pareActivity']))
            if actData and gameconst.ActivityControlType.TEAM == int(actData['needTeam']):
                self.teamsMatchPool[tgtId] = []
                self.playersMatchPool[tgtId] = []

        self.addTimerCB(1, '_doMatch', (), gametimer.TIMER_TAG_DO_MATCH)
        self.addTimerCB(10, '_checkTimeOutMatch', (), gametimer.TIMER_TAG_CHECK_TIME_OUT_MATCH)

    def postReloadScript(self):
        _super = super(TeamMatchStub, self)
        if hasattr(_super, 'postReloadScript'):
            _super.postReloadScript()
        for _v in self.teamsDic.values():
            _v.reloadScript()
        for _v in self.playersDic.values():
            _v.reloadScript()

    def onTimer(self, tid, userArg):
        self._onTimerTrigger(tid, userArg)
        if utils.isBelongTimerTag(userArg):
            self._onTimerCallback(tid)

    def teamAutoMatch(self, teamInfoDic):
        LOG_INFO('in teamAutoMatch:', teamInfoDic)
        if 0 == teamInfoDic['teamTarget']:
            return
        _tmVal = self.teamsDic.get(teamInfoDic['teamId'])
        if _tmVal:
            self._rmTeamFromMatchPool(teamInfoDic['teamId'])

        _tmVal = TeamMatchVal(teamInfoDic, utils.curTS())
        if _tmVal.isTeamFull():
            return
        self._addTeamToPool(_tmVal)

    def onTeamInfoUpdate(self, teamInfoDic):
        LOG_INFO('in onTeamInfoUpdate:', teamInfoDic)
        if 0 == teamInfoDic['teamTarget']:
            self._rmTeamFromMatchPool(teamInfoDic['teamId'])
            return
        _tmVal = self.teamsDic.get(teamInfoDic['teamId'])
        if not _tmVal:
            return
        _tmVal.updateFromTeamInfoDic(teamInfoDic)
        if _tmVal.isTeamFull():
            self._rmTeamFromMatchPool(teamInfoDic['teamId'])

    def _addTeamToPool(self, tmVal):
        self.teamsDic[tmVal.teamId] = tmVal
        self.teamsMatchPool[tmVal.teamTarget].append(tmVal.teamId)

    def doTeamStopAutoMatch(self, teamId):
        LOG_INFO('in doTeamStopAutoMatch:', teamId)
        self._rmTeamFromMatchPool(teamId)

    def _rmTeamFromMatchPool(self, teamId):
        _tmVal = self.teamsDic.pop(teamId, None)
        if not _tmVal:
            return False
        if teamId in self.teamsMatchPool[_tmVal.teamTarget]:
            self.teamsMatchPool[_tmVal.teamTarget].remove(teamId)
        return True

    def onPlayerMatchInfoUpdate(self, playerInfoDic):
        LOG_INFO('in onPlayerMatchInfoUpdate:', playerInfoDic)
        _pmVal = self.playersDic.get(playerInfoDic['playerGbId'], None)
        if not _pmVal:
            return
        _pmVal.updateMatchProp(playerInfoDic)

    def playerAutoMatch(self, playerMatchDic):
        LOG_INFO('in playerAutoMatch:', playerMatchDic)
        _pmVal = self.playersDic.get(playerMatchDic['playerGbId'], None)
        if _pmVal:
            self._rmPlayerFromMatchPool(playerMatchDic['playerGbId'])

        now = utils.curTS()
        _pmVal = PlayerMatchVal(playerMatchDic, utils.curTS())
        self._playerStartMatch(_pmVal)
        playerMatchDic['playerBox'].cell.cellPlayerStartAutoMatch(now, playerMatchDic['target'])

    def _playerStartMatch(self, pmVal):
        self.playersDic[pmVal.playerGbId] = pmVal
        self.playersMatchPool[pmVal.target].append(pmVal.playerGbId)

    def playerMatchedSucc(self, playerGbId):
        _pmVal = self.playersDic.get(playerGbId, None)
        if not _pmVal:
            return
        if self._rmPlayerFromMatchPool(playerGbId):
            _pmVal.playerBox.cell.onPlayerMatchedSuccess()

    def doPlayerStopAutoMatch(self, playerGbId):
        LOG_INFO('in doPlayerStopAutoMatch:', playerGbId)
        _pmVal = self.playersDic.get(playerGbId, None)
        if not _pmVal:
            return
        if self._rmPlayerFromMatchPool(playerGbId):
            pass

    def playerAutoMatchTimeout(self, playerGbId):
        LOG_INFO('in playerAutoMatchTimeout:', playerGbId)
        _pmVal = self.playersDic.get(playerGbId, None)
        if not _pmVal:
            return
        if self._rmPlayerFromMatchPool(playerGbId):
            _pmVal.playerBox.cell.onPlayerAutoMatchTimeout()

    def _rmPlayerFromMatchPool(self, playerGbId):
        LOG_INFO('in _rmPlayerFromMatchPool:', playerGbId)
        _pmVal = self.playersDic.pop(playerGbId, None)
        if not _pmVal:
            return False
        if playerGbId in self.playersMatchPool[_pmVal.target]:
            self.playersMatchPool[_pmVal.target].remove(playerGbId)
        return True

    def _doMatch(self):
        self.addTimerCB(3.0, '_doMatch', (), gametimer.TIMER_TAG_DO_MATCH)
        if len(self.teamsDic) > 0 or len(self.playersDic) > 0:
            try:
                matchedPlayers = []
                for playerGbid, _pmVal in self.playersDic.items():
                    tgtId = _pmVal.target
                    if 0 == tgtId:
                        continue
                    fullTeams = []
                    for teamId in self.teamsMatchPool[tgtId]:
                        tmVal = self.teamsDic.get(teamId, None)
                        if not tmVal:
                            continue
                        if not tmVal.canAddPlayer(_pmVal):
                            continue
                        #matched
                        LOG_INFO('     in _doMatch, matched:', playerGbid, teamId)
                        if tmVal.addPlayerToTeam(_pmVal):
                            matchedPlayers.append(playerGbid)
                            if tmVal.isTeamFull():
                                fullTeams.append(teamId)
                            break
                    for rmTeamId in fullTeams:
                        self.doTeamStopAutoMatch(rmTeamId)
                for rmPlayeId in matchedPlayers:
                    self.playerMatchedSucc(rmPlayeId)
            except Exception as e:
                LOG_ERR('in _doMatch, exception:', e)

    def _checkTimeOutMatch(self):
        self.addTimerCB(10, '_checkTimeOutMatch', (), gametimer.TIMER_TAG_CHECK_TIME_OUT_MATCH)
        rmPlayers = []
        for playerGbid, _pmVal in self.playersDic.items():
            if _pmVal.isTimeOut():
                rmPlayers.append(playerGbid)
                LOG_DBG('     in _checkTimeOutMatch, rmPlayers:', rmPlayers)
        for rmPlayeId in rmPlayers:
            self.playerAutoMatchTimeout(rmPlayeId)
        fullTeams = []
        for teamId, tmVal in self.teamsDic.items():
            if tmVal.isTeamFull():
                fullTeams.append(teamId)

        for rmTeamId in fullTeams:
            self.doTeamStopAutoMatch(rmTeamId)

class TeamMatchVal(userType.UserSingleType):
    def __init__(self, teamInfoDic, startTime):
        self.teamTarget = teamInfoDic['teamTarget']
        self.teamId = teamInfoDic['teamId']
        self.teamCaptainGbId = teamInfoDic['teamCaptainGbId']
        self.teamMinScore = teamInfoDic['teamMinScore']
        self.teamMinLv = teamInfoDic['teamMinLv']
        self.teamPlayerDict = teamInfoDic['teamPlayerDict']
        self.startTime = startTime
        self.guildUUID = teamInfoDic.get('guildUUID', 0)

    def updateFromTeamInfoDic(self, teamInfoDic):
        self.teamTarget = teamInfoDic['teamTarget']
        self.teamId = teamInfoDic['teamId']
        self.teamCaptainGbId = teamInfoDic['teamCaptainGbId']
        self.teamMinLv = teamInfoDic['teamMinLv']
        self.teamMinScore = teamInfoDic['teamMinScore']
        self.teamPlayerDict = teamInfoDic['teamPlayerDict']
        guildUUID = teamInfoDic.get('guildUUID')
        if guildUUID:
            self.guildUUID = guildUUID

    def addPlayerToTeam(self, pmVal):
        self.teamPlayerDict[pmVal.playerGbId] = (pmVal.level, pmVal.playerName, pmVal.school, pmVal.sex)
        extraNum = len(self.teamPlayerDict)-gameconst.TEAM_MEMBER_MAX_NUM
        if extraNum > 0:
            gameengine.panicStack('addPlayerToTeam, player exceed max num:', self.teamPlayerDict)
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
        return len(self.teamPlayerDict) >= gameconst.TEAM_MEMBER_MAX_NUM

    def isTimeOut(self):
        maxMatchTime = TMMCD.datas['maxMatchTime']['value']
        return self.startTime + maxMatchTime < utils.curTS()

class PlayerMatchVal(userType.UserSingleType):
    def __init__(self, playerInfoDic, startTime):
        self.playerGbId = playerInfoDic['playerGbId']
        self.target = playerInfoDic['target']
        self.playerBox = playerInfoDic['playerBox']
        self.playerName = playerInfoDic['playerName']
        self.level = playerInfoDic['level']
        self.sex = playerInfoDic['sex']
        self.school = playerInfoDic['school']
        self.spaceNo = playerInfoDic['spaceNo']
        self.startTime = startTime
        self.guildUUID = playerInfoDic.get('guildUUID', 0)
        self.score = playerInfoDic.get('score', 0)

    def isTimeOut(self):
        maxMatchTime = TMMCD.datas['maxMatchTime']['value']
        return self.startTime + maxMatchTime < utils.curTS()

    def updateMatchProp(self, playerInfoDic):
        self.playerGbId = playerInfoDic['playerGbId']
        self.playerBox = playerInfoDic['playerBox']
        self.spaceNo = playerInfoDic['spaceNo']
        self.level = playerInfoDic['level']
        guildUUID = playerInfoDic.get('guildUUID')
        if guildUUID:
            self.guildUUID = guildUUID
