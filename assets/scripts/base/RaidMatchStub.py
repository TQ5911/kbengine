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


class RaidMatchStub(iGlobal.IGlobal, iBaseNoCell.IBaseNoCell, iTimer.ITimer):

    MATCH_LIST_MAX_NUM = 15

    def __init__(self):
        super(RaidMatchStub, self).__init__()
        self.raidsDic = {}
        self.playersDic = {}

        self.matchRaidsPool = {}
        self.matchPlayersPool = {}
        return

    def doNext(self):
        gameglobal.localBaseApp.fullPrepare(self.classname())
        self.initMatchData()
        return

    def initMatchData(self):
        self.raidsDic = {}
        self.playersDic = {}

        self.matchRaidsPool = {}
        self.matchPlayersPool = {}

        for tgtId, d in TMACTD.datas.items():
            if tgtId == 0:
                continue
            actData = AC_ADD.datas.get(int(d['pareActivity']))
            if actData and gameconst.ActivityControlType.RAID == int(actData['needTeam']):
                self.matchRaidsPool[tgtId] = []
                self.matchPlayersPool[tgtId] = []

        self._callback(1, '_doMatch', (), gametimer.TIMER_TAG_DO_RAID_MATCH)
        self._callback(10, '_checkTimeOutMatch', (), gametimer.TIMER_TAG_DO_RAID_MATCH_TIMEOUT)
        return

    def postReloadScript(self):
        if hasattr(super(RaidMatchStub, self), 'postReloadScript'):
            super(RaidMatchStub, self).postReloadScript()
        for v in self.raidsDic.values():
            v.reloadScript()
        for v in self.playersDic.values():
            v.reloadScript()
        return

    def onTimer(self, tid, userArg):
        self._onTimer(tid, userArg)
        if utils.isBelongTimerTag(userArg):
            self._onTimerCallback(tid)

    def raidAutoMatch(self, raidInfoDic):
        INFO_MSG('in raidAutoMatch:', raidInfoDic)
        if 0 == raidInfoDic['raidTarget']:
            return
        tmVal = self.raidsDic.get(raidInfoDic['raidID'])
        if tmVal:
            self._rmRaidFromMatchPool(raidInfoDic['raidID'])

        tmVal = RaidTeamMatchVal(raidInfoDic, utils.getNow())
        if tmVal.isRaidFull():
            return
        self._addRaidToPool(tmVal)
        return

    def onRaidInfoUpdate(self, raidInfoDic):
        INFO_MSG('in onRaidInfoUpdate:', raidInfoDic)
        if 0 == raidInfoDic['raidTarget']:
            self._rmRaidFromMatchPool(raidInfoDic['raidID'])
            return
        tmVal = self.raidsDic.get(raidInfoDic['raidID'])
        if not tmVal:
            return
        tmVal.updateFromRaidInfoDic(raidInfoDic)
        if tmVal.isRaidFull():
            self._rmRaidFromMatchPool(raidInfoDic['raidID'])
        return

    def _addRaidToPool(self, tmVal):
        self.raidsDic[tmVal.raidID] = tmVal
        self.matchRaidsPool[tmVal.raidTarget].append(tmVal.raidID)
        return

    def raidStopAutoMatch(self, raidID):
        INFO_MSG('in raidStopAutoMatch:', raidID)
        self._rmRaidFromMatchPool(raidID)
        return

    def _rmRaidFromMatchPool(self, raidID):
        tmVal = self.raidsDic.pop(raidID, None)
        if not tmVal:
            return
        if raidID in self.matchRaidsPool[tmVal.raidTarget]:
            self.matchRaidsPool[tmVal.raidTarget].remove(raidID)
        return True

    def onRaidPlayerMatchInfoUpdate(self, playerInfoDic):
        INFO_MSG('in onRaidPlayerMatchInfoUpdate:', playerInfoDic)
        pmVal = self.playersDic.get(playerInfoDic['playerGbId'], None)
        if not pmVal:
            return
        pmVal.updateMatchProp(playerInfoDic)
        return

    def raidPlayerAutoMatch(self, playerMatchDic):
        INFO_MSG('in playerAutoMatch:', playerMatchDic)
        pmVal = self.playersDic.get(playerMatchDic['playerGbId'], None)
        if pmVal:
            self._rmPlayerFromMatchPool(playerMatchDic['playerGbId'])

        now = utils.getNow()
        pmVal = RaidPlayerMatchVal(playerMatchDic, utils.getNow())
        self._playerStartMatch(pmVal)
        playerMatchDic['playerBox'].cell.onCellRaidPlayerStartAutoMatch(now, playerMatchDic['target'])
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
            pmVal.playerBox.cell.onCellRaidPlayerMatchedSucc()
        return

    def raidPlayerStopAutoMatch(self, playerGbId):
        INFO_MSG('in raidPlayerStopAutoMatch:', playerGbId)
        pmVal = self.playersDic.get(playerGbId, None)
        if not pmVal:
            return
        if self._rmPlayerFromMatchPool(playerGbId):
            pmVal.playerBox.client.onRaidPlayerStopAutoMatch()
        return

    def playerAutoMatchTimeout(self, playerGbId):
        INFO_MSG('in playerAutoMatchTimeout:', playerGbId)
        pmVal = self.playersDic.get(playerGbId, None)
        if not pmVal:
            return
        if self._rmPlayerFromMatchPool(playerGbId):
            pmVal.playerBox.cell.onCellRaidPlayerAutoMatchTimeout()
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
        if len(self.raidsDic) > 0 or len(self.playersDic) > 0:
            # DEBUG_MSG('in _doMatch, matchPlayersPool:', self.matchPlayersPool)
            # DEBUG_MSG('in _doMatch, matchRaidsPool:', self.matchRaidsPool)
            try:
                matchedPlayers = []
                for playerGbid, pmVal in self.playersDic.items():
                    tgtId = pmVal.target
                    if 0 == tgtId:
                        continue
                    fullTeams = []
                    for raidUUID in self.matchRaidsPool[tgtId]:
                        tmVal = self.raidsDic.get(raidUUID, None)
                        if not tmVal:
                            continue
                        if not tmVal.canAddPlayer(pmVal):
                            continue
                        #matched
                        INFO_MSG('     in _doMatch, matched:', playerGbid, raidUUID)
                        if tmVal.addPlayerToTeam(pmVal):
                            matchedPlayers.append(playerGbid)
                            if tmVal.isRaidFull():
                                fullTeams.append(raidUUID)
                            break
                    for raidUUID in fullTeams:
                        self.raidStopAutoMatch(raidUUID)
                for playerGBID in matchedPlayers:
                    self.playerMatchedSucc(playerGBID)
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
                INFO_MSG('     in _checkTimeOutMatch, rmPlayers:', rmPlayers)
        for playerGBID in rmPlayers:
            self.playerAutoMatchTimeout(playerGBID)

        fullTeams = []
        for raidUUID, tmVal in self.raidsDic.items():
            if tmVal.isRaidFull():
                fullTeams.append(raidUUID)

        for raidUUID in fullTeams:
            self.raidStopAutoMatch(raidUUID)

class RaidTeamMatchVal(userType.UserSoleType):
    def __init__(self, raidInfoDic, startTime):
        self.raidID = raidInfoDic['raidID']
        self.raidCapacity = raidInfoDic['raidCapacity']
        self.raidLeaderGBID = raidInfoDic['raidLeaderGBID']
        self.raidTarget = raidInfoDic['raidTarget']
        self.raidMinLv = raidInfoDic['raidMinLv']
        self.raidMinScore = raidInfoDic['raidMinScore']
        self.raidFilterPlayers = raidInfoDic['raidFilterPlayers']
        self.raidPlayerDic = raidInfoDic['raidPlayerDic']
        self.startTime = startTime

    def updateFromRaidInfoDic(self, raidInfoDic):
        self.raidID = raidInfoDic['raidID']
        self.raidCapacity = raidInfoDic['raidCapacity']
        self.raidLeaderGBID = raidInfoDic['raidLeaderGBID']
        self.raidTarget = raidInfoDic['raidTarget']
        self.raidMinLv = raidInfoDic['raidMinLv']
        self.raidMinScore = raidInfoDic['raidMinScore']
        self.raidFilterPlayers = raidInfoDic['raidFilterPlayers']
        self.raidPlayerDic = raidInfoDic['raidPlayerDic']

    def addPlayerToTeam(self, pmVal):
        self.raidPlayerDic[pmVal.playerGbId] = (pmVal.level, pmVal.playerName, pmVal.school, pmVal.sex)
        pmVal.playerBox.cell.onPlayerMatchedRaid(self.raidID)
        return True


    def canAddPlayer(self,  pmVal):
        if self.raidTarget != pmVal.target:
            return False
        if self.isRaidFull():
            return False
        if pmVal.level < self.raidMinLv:
            return False
        if pmVal.score < self.raidMinScore:
            return False
        return True

    def isRaidFull(self):
        return len(self.raidPlayerDic) >= self.raidCapacity

    def isTimeOut(self):
        maxMatchTime = TMMCD.datas['maxMatchTime']['value']
        return self.startTime + maxMatchTime < utils.getNow()

class RaidPlayerMatchVal(userType.UserSoleType):
    def __init__(self, playerInfoDic, startTime):
        self.startTime = startTime
        self.target = playerInfoDic['target']
        self.playerGbId = playerInfoDic['playerGbId']
        self.playerBox = playerInfoDic['playerBox']
        self.playerName = playerInfoDic['playerName']
        self.level = playerInfoDic['level']
        self.school = playerInfoDic['school']
        self.sex = playerInfoDic['sex']
        self.picFrameId = playerInfoDic['picFrameId']
        self.bFollow = playerInfoDic['bFollow']
        self.bOnline = playerInfoDic['bOnline']
        self.spaceNo = playerInfoDic['spaceNo']
        self.position = playerInfoDic['position']
        self.hp = playerInfoDic['hp']
        self.fullHp = playerInfoDic['fullHp']
        self.score = playerInfoDic['score']
        self.hpkScore = playerInfoDic['hpkScore']
        self.mountState = playerInfoDic['mountState']
        self.raidUUID = playerInfoDic['raidUUID']
        self.enableMics = playerInfoDic['enableMics']
        self.isBlockMics = playerInfoDic['isBlockMics']
        self.isDead = playerInfoDic['isDead']
        self.openId = playerInfoDic['openId']

    def isTimeOut(self):
        maxMatchTime = TMMCD.datas['maxMatchTime']['value']
        return self.startTime + maxMatchTime < utils.getNow()

    def updateMatchProp(self, playerInfoDic):
        self.playerGbId = playerInfoDic['playerGbId']
        self.playerBox = playerInfoDic['playerBox']
        self.playerName = playerInfoDic['playerName']
        self.level = playerInfoDic['level']
        self.school = playerInfoDic['school']
        self.sex = playerInfoDic['sex']
        self.picFrameId = playerInfoDic['picFrameId']
        self.bFollow = playerInfoDic['bFollow']
        self.bOnline = playerInfoDic['bOnline']
        self.spaceNo = playerInfoDic['spaceNo']
        self.position = playerInfoDic['position']
        self.hp = playerInfoDic['hp']
        self.fullHp = playerInfoDic['fullHp']
        self.score = playerInfoDic['score']
        self.hpkScore = playerInfoDic['hpkScore']
        self.mountState = playerInfoDic['mountState']
        self.raidUUID = playerInfoDic['raidUUID']
        self.enableMics = playerInfoDic['enableMics']
        self.isBlockMics = playerInfoDic['isBlockMics']
        self.isDead = playerInfoDic['isDead']
        self.openId = playerInfoDic['openId']
