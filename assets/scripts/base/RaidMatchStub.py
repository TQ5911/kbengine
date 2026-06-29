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
    def __init__(self):
        super(RaidMatchStub, self).__init__()
        self.raidsDic = {}
        self.playersDic = {}

        self.matchRaidsPool = {}
        self.playersMatchPool = {}
        return

    def doNext(self):
        gameglobal.localBaseApp.fullPrepare(self.classname())
        self.initMatchData()
        return

    def initMatchData(self):
        self.raidsDic = {}
        self.playersDic = {}

        self.matchRaidsPool = {}
        self.playersMatchPool = {}

        for tgtId, d in TMACTD.datas.items():
            if tgtId == 0:
                continue
            actData = AC_ADD.datas.get(int(d['pareActivity']))
            if actData and gameconst.ActivityControlType.RAID == int(actData['needTeam']):
                self.matchRaidsPool[tgtId] = []
                self.playersMatchPool[tgtId] = []

        self.addTimerCB(1, '_doMatch', (), gametimer.TIMER_TAG_DO_RAID_MATCH)
        self.addTimerCB(10, '_checkTimeOutMatch', (), gametimer.TIMER_TAG_DO_RAID_MATCH_TIMEOUT)
        return

    def postReloadScript(self):
        if hasattr(super(RaidMatchStub, self), 'postReloadScript'):
            super(RaidMatchStub, self).postReloadScript()
        for _v in self.raidsDic.values():
            _v.reloadScript()
        for _v in self.playersDic.values():
            _v.reloadScript()

    def onTimer(self, tid, userArg):
        self._onTimerTrigger(tid, userArg)
        if utils.isBelongTimerTag(userArg):
            self._onTimerCallback(tid)

    def raidAutoMatch(self, raidInfoDic):
        LOG_INFO('in raidAutoMatch:', raidInfoDic)
        if 0 == raidInfoDic['raidTarget']:
            return
        tmVal = self.raidsDic.get(raidInfoDic['raidID'])
        if tmVal:
            self._rmRaidFromMatchPool(raidInfoDic['raidID'])

        tmVal = RaidTeamMatchVal(raidInfoDic, utils.curTS())
        if tmVal.isRaidFull():
            return
        self._addRaidToPool(tmVal)
        return

    def onRaidInfoUpdate(self, raidInfoDic):
        LOG_INFO('in onRaidInfoUpdate:', raidInfoDic)
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
        LOG_INFO('in raidStopAutoMatch:', raidID)
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
        LOG_INFO('in onRaidPlayerMatchInfoUpdate:', playerInfoDic)
        _pmVal = self.playersDic.get(playerInfoDic['playerGbId'], None)
        if not _pmVal:
            return
        _pmVal.updateMatchProp(playerInfoDic)

    def raidPlayerAutoMatch(self, playerMatchDic):
        LOG_INFO('in playerAutoMatch:', playerMatchDic)
        _pmVal = self.playersDic.get(playerMatchDic['playerGbId'], None)
        if _pmVal:
            self._rmPlayerFromMatchPool(playerMatchDic['playerGbId'])

        now = utils.curTS()
        _pmVal = RaidPlayerMatchVal(playerMatchDic, utils.curTS())
        self._playerStartMatch(_pmVal)
        playerMatchDic['playerBox'].cell.onCellRaidPlayerStartAutoMatch(now, playerMatchDic['target'])

    def _playerStartMatch(self, pmVal):
        self.playersDic[pmVal.playerGbId] = pmVal
        self.playersMatchPool[pmVal.target].append(pmVal.playerGbId)

    def playerMatchedSucc(self, playerGbId):
        _pmVal = self.playersDic.get(playerGbId, None)
        if not _pmVal:
            return
        if self._rmPlayerFromMatchPool(playerGbId):
            _pmVal.playerBox.cell.onCellRaidPlayerMatchedSucc()

    def raidPlayerStopAutoMatch(self, playerGbId):
        LOG_INFO('in raidPlayerStopAutoMatch:', playerGbId)
        _pmVal = self.playersDic.get(playerGbId, None)
        if not _pmVal:
            return
        if self._rmPlayerFromMatchPool(playerGbId):
            _pmVal.playerBox.client.onRaidPlayerStopAutoMatch()

    def playerAutoMatchTimeout(self, playerGbId):
        LOG_INFO('in playerAutoMatchTimeout:', playerGbId)
        _pmVal = self.playersDic.get(playerGbId, None)
        if not _pmVal:
            return
        if self._rmPlayerFromMatchPool(playerGbId):
            _pmVal.playerBox.cell.onCellRaidPlayerAutoMatchTimeout()
        return

    def _rmPlayerFromMatchPool(self, playerGbId):
        LOG_INFO('in _rmPlayerFromMatchPool:', playerGbId)
        _pmVal = self.playersDic.pop(playerGbId, None)
        if not _pmVal:
            return False
        if playerGbId in self.playersMatchPool[_pmVal.target]:
            self.playersMatchPool[_pmVal.target].remove(playerGbId)
        return True

    def _doMatch(self):
        self.addTimerCB(3, '_doMatch', (), gametimer.TIMER_TAG_DO_MATCH)
        if len(self.raidsDic) > 0 or len(self.playersDic) > 0:
            try:
                matchedPlayers = []
                for playerGbid, _pmVal in self.playersDic.items():
                    _tgtId = _pmVal.target
                    if 0 == _tgtId:
                        continue
                    fullTeams = []
                    for raidUUID in self.matchRaidsPool[_tgtId]:
                        tmVal = self.raidsDic.get(raidUUID, None)
                        if not tmVal:
                            continue
                        if not tmVal.canAddPlayer(_pmVal):
                            continue
                        #matched
                        LOG_INFO('     in _doMatch, matched:', playerGbid, raidUUID)
                        if tmVal.addPlayerToTeam(_pmVal):
                            matchedPlayers.append(playerGbid)
                            if tmVal.isRaidFull():
                                fullTeams.append(raidUUID)
                            break
                    for raidUUID in fullTeams:
                        self.raidStopAutoMatch(raidUUID)
                for playerGBID in matchedPlayers:
                    self.playerMatchedSucc(playerGBID)
            except Exception as e:
                LOG_ERR('in _doMatch, exception:', e)
        return

    def _checkTimeOutMatch(self):
        #LOG_DBG('in _checkTimeOutMatch')
        self.addTimerCB(10, '_checkTimeOutMatch', (), gametimer.TIMER_TAG_CHECK_TIME_OUT_MATCH)
        _rmPlayers = []
        for playerGbid, _pmVal in self.playersDic.items():
            if _pmVal.isTimeOut():
                _rmPlayers.append(playerGbid)
                LOG_INFO('     in _checkTimeOutMatch, _rmPlayers:', _rmPlayers)
        for playerGBID in _rmPlayers:
            self.playerAutoMatchTimeout(playerGBID)

        fullTeams = []
        for raidUUID, tmVal in self.raidsDic.items():
            if tmVal.isRaidFull():
                fullTeams.append(raidUUID)

        for raidUUID in fullTeams:
            self.raidStopAutoMatch(raidUUID)

class RaidTeamMatchVal(userType.UserSingleType):
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
        return self.startTime + maxMatchTime < utils.curTS()

class RaidPlayerMatchVal(userType.UserSingleType):
    def __init__(self, playerInfoDic, startTime):
        self.startTime = startTime
        self.target = playerInfoDic['target']
        self.playerBox = playerInfoDic['playerBox']
        self.playerGbId = playerInfoDic['playerGbId']
        self.level = playerInfoDic['level']
        self.playerName = playerInfoDic['playerName']
        self.sex = playerInfoDic['sex']
        self.school = playerInfoDic['school']
        self.picFrameId = playerInfoDic['picFrameId']
        self.bOnline = playerInfoDic['bOnline']
        self.spaceNo = playerInfoDic['spaceNo']
        self.position = playerInfoDic['position']
        self.hp = playerInfoDic['hp']
        self.fullHp = playerInfoDic['fullHp']
        self.score = playerInfoDic['score']
        self.mountState = playerInfoDic['mountState']
        self.raidUUID = playerInfoDic['raidUUID']
        self.enableMics = playerInfoDic['enableMics']
        self.isBlockMics = playerInfoDic['isBlockMics']
        self.isDead = playerInfoDic['isDead']
        self.openId = playerInfoDic['openId']

    def isTimeOut(self):
        maxMatchTime = TMMCD.datas['maxMatchTime']['value']
        return self.startTime + maxMatchTime < utils.curTS()

    def updateMatchProp(self, playerInfoDic):
        self.playerGbId = playerInfoDic['playerGbId']
        self.playerName = playerInfoDic['playerName']
        self.playerBox = playerInfoDic['playerBox']
        self.school = playerInfoDic['school']
        self.level = playerInfoDic['level']
        self.picFrameId = playerInfoDic['picFrameId']
        self.sex = playerInfoDic['sex']
        self.spaceNo = playerInfoDic['spaceNo']
        self.bOnline = playerInfoDic['bOnline']
        self.position = playerInfoDic['position']
        self.fullHp = playerInfoDic['fullHp']
        self.hp = playerInfoDic['hp']
        self.score = playerInfoDic['score']
        self.mountState = playerInfoDic['mountState']
        self.enableMics = playerInfoDic['enableMics']
        self.raidUUID = playerInfoDic['raidUUID']
        self.isBlockMics = playerInfoDic['isBlockMics']
        self.openId = playerInfoDic['openId']
        self.isDead = playerInfoDic['isDead']
