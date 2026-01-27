# coding: utf-8
import gameglobal
from KBEDebug import *
import KBEngine

import random
import json

import gameengine
import gameconst
import gameconfig
import gametimer
import formula
import dataUtils
import utils

import iBaseNoCell
import iGlobal
import iTimer

import message_Message_def as MMD
import userType
import raid
import raid_raidConst as RAID_CONST
import teamMatch_matchConfig as TMMCD
import teamMatch_activity as TMACTD
import raidBossChallenge_basicInfo as RBC_BI
import copy

class _RaidTeamMemberJoinRecordVal(userType.UserSoleType):
    def __init__(self, playerJoinVal, memberCheckDic):
        self.playerJoinVal = playerJoinVal
        self.memberCheckDic = memberCheckDic
        self.timerId = 0

    def _lateReload(self):
        self.playerJoinVal.reloadScript()


class _RaidStubJoinRecordCheckMixin(object):

    def _initTeamMemberJoinRecord(self, raidUUID, teamUUID, playerJoinVal, memberDic, timeout=5):
        v = _RaidTeamMemberJoinRecordVal(playerJoinVal, memberDic)
        self.raidTeamMembersJoinRecordDic.setdefault(raidUUID, {})
        self.raidTeamMembersJoinRecordDic[raidUUID][teamUUID] = v
        if timeout > 0:
            tid = self.toCallbackAfter(timeout, gametimer.TIMER_TAG_POP_TEAM_MEMBER_JOIN_RECORD)._popTeamMemberJoinRecord(raidUUID, teamUUID)
            v.timerId = tid
        return v

    def _getTeamMemberJoinRecord(self, raidUUID, teamUUID, default=None):
        return self.raidTeamMembersJoinRecordDic.get(raidUUID, {}).get(teamUUID, default)

    def _popTeamMemberJoinRecord(self, raidUUID, teamUUID, default=None):
        v = self.raidTeamMembersJoinRecordDic.get(raidUUID, {}).pop(teamUUID, default)
        v and v.timerId and self._cancelCallback(v.timerId, gametimer.TIMER_TAG_POP_TEAM_MEMBER_JOIN_RECORD)
        return v


class _RaidTeamMemberInviteRecordVal(userType.UserSoleType):
    def __init__(self, memberNum, memberCheckDic):
        self.memberCheckDic = memberCheckDic
        self.memberNum = memberNum
        self.captainGBID = 0
        self.timerId = 0

    def isAllChecked(self):
        return len(self.memberCheckDic) >= self.memberNum


class _RaidStubInviteRecordCheckMixin(object):

    def _initTeamMemberInviteRecord(self, raidUUID, teamUUID, recordID, memberNum, memberDic, timeout=3, force=False):
        _ov = self._getTeamMemberInviteRecord(raidUUID, teamUUID, recordID)
        if _ov is not None and not force:
            return _ov

        v = _RaidTeamMemberInviteRecordVal(memberNum, memberDic)
        self.raidTeamMembersInviteRecordDic.setdefault(raidUUID, {}).setdefault(teamUUID, {})

        self.raidTeamMembersInviteRecordDic[raidUUID][teamUUID][recordID] = v
        if timeout > 0:
            tid = self.toCallbackAfter(timeout, gametimer.TIMER_TAG_POP_TEAM_MEMBER_INVITE_RECORD)._popTeamMemberInviteRecord(raidUUID, teamUUID, recordID)
            v.timerId = tid
        return v

    def _getTeamMemberInviteRecord(self, raidUUID, teamUUID, recordID, default=None):
        return self.raidTeamMembersInviteRecordDic.get(raidUUID, {}).get(teamUUID, {}).get(recordID, default)

    def _popTeamMemberInviteRecord(self, raidUUID, teamUUID, recordID, default=None):
        v = self.raidTeamMembersInviteRecordDic.get(raidUUID, {}).get(teamUUID, {}).pop(recordID, default)
        v and v.timerId and self._cancelCallback(v.timerId, gametimer.TIMER_TAG_POP_TEAM_MEMBER_INVITE_RECORD)
        return v


class _RaidStandbyCheckerVal(userType.UserSoleType):
    def __init__(self, checkBoxes, trueCount=0, falseCount=0, unknownCount=0,
                 enterSrc=gameconst.RaidDungeonStandbyCheckSrcEnum.DEFAULT, extraProps=None):
        self.checkBoxes = checkBoxes
        self.timerId = 0
        # count
        self.trueCount = trueCount
        self.falseCount = falseCount
        self.unknownCount = unknownCount
        # source
        self.enterSrc = enterSrc
        self.extraProps = extraProps or {}

    @property
    def checkNum(self):
        return len(self.checkBoxes)

    def isChecked(self, gbId):
        return self.checkBoxes[gbId] is not None

    def isAllChecked(self):
        return self.unknownCount <= 0

    def isAllCheckSucceed(self):
        return self.trueCount >= self.checkNum and \
               not self.falseCount and \
               not self.unknownCount

    def checkIt(self, playerGBID, checkResult):
        if self.checkBoxes.get(playerGBID, None) is not None:
            ERROR_MSG('_RaidStandbyCheckerVal::checkIt:: already checked')
            return
        checkResult = bool(checkResult)
        self.checkBoxes[playerGBID] = checkResult
        if checkResult:
            self.trueCount += 1
        else:
            self.falseCount += 1
        self.unknownCount -= 1
        return checkResult

    def getCheckResult(self):
        _t, _f, _n = [], [], []
        for gbId, checkResult in self.checkBoxes.items():
            if checkResult is None:
                _x = _n
            elif not checkResult:
                _x = _f
            else:
                _x = _t
            _x.append(gbId)
        return _t, _f, _n


class _RaidStubStandbyCheckerMixin(object):

    def _initStanbyCheckerRecord(self, raidUUID, checkBoxes, trueCount,
                                 falseCount, unknownCount, checkSrc,
                                 cbFn='', cbArgs=(), timeout=30, force=False):
        _ov = self._getStandbyCheckerRecord(raidUUID)
        if _ov is not None and not force:
            return _ov

        v = _RaidStandbyCheckerVal(checkBoxes, trueCount, falseCount, unknownCount, checkSrc)
        self.raidStandbyCheckerDic[raidUUID] = v
        if timeout > 0 and cbFn:
            tid = self._callback(timeout, cbFn, cbArgs, gametimer.TIMER_TAG_INIT_STANBY_CHECKER_RECORD)
            v.timerId = tid
        return v

    def _getStandbyCheckerRecord(self, raidUUID, default=None):
        return self.raidStandbyCheckerDic.get(raidUUID, default)

    def _popStandbyCheckerRecord(self, raidUUID, default=None):
        v = self.raidStandbyCheckerDic.pop(raidUUID, default)
        v and v.timerId and self._cancelCallback(v.timerId, gametimer.TIMER_TAG_INIT_STANBY_CHECKER_RECORD)
        return v


class RaidStub(iGlobal.IGlobal, iBaseNoCell.IBaseNoCell, iTimer.ITimer,
               _RaidStubJoinRecordCheckMixin, _RaidStubInviteRecordCheckMixin,
               _RaidStubStandbyCheckerMixin):
    """  team raid stub """

    @property
    def raidJoinRecordTimeout(self):
        return RAID_CONST.datas['raidApplyDuration']['value'] * 60

    def __init__(self):
        super(RaidStub, self).__init__()
        self.raidDic = {}       # type: dict[int, raid.RaidVal]
        self.raidTeamMembersJoinRecordDic = {}
        self.raidTeamMembersInviteRecordDic = {}
        self.raidStandbyCheckerDic = {}
        self.teamMarkMonsterRec = {}

    def doNext(self):
        gameglobal.localBaseApp.fullPrepare(self.classname())

    def refreshRaidCache(self, raidUUID, playerGBIDs, extraProps):
        DEBUG_MSG('refreshRaidCache', raidUUID, playerGBIDs, extraProps)

        if raidUUID not in self.raidDic:
            ERROR_MSG('refreshRaidCache:: check failed, {}'.format(gameconst.RaidErrno.RAID_RAID_ID_NOT_FOUND))
            return

        # 没人需要处理的，直接结束
        if not playerGBIDs:
            return

        raidVal = self.raidDic[raidUUID]
        _checkBox = set(playerGBIDs)

        # 统一处理刷新逻辑
        def _refreshRaidCacheValue(raidPlayerVal, playerRaidCacheVal, _checkBox):
            if raidPlayerVal.bOnline and raidPlayerVal.playerBox and raidPlayerVal.playerBox.cell:
                DEBUG_MSG('_refreshRaidCacheValue :: force fresh avatar raidCache: ', raidPlayerVal.playerGbId)
                raidPlayerVal.playerBox.cell.onRefreshPlayerRaidCacheVal(playerRaidCacheVal)
            _checkBox.remove(raidPlayerVal.playerGbId)

        DEBUG_MSG('refreshRaidCache 0::', raidUUID, playerGBIDs, extraProps, len(_checkBox), raidVal.memberNum)
        playerRaidCacheVal = None
        # 1.处理检测数量大于等于团队数量的情况
        if len(_checkBox) >= raidVal.memberNum:
            for raidTeamVal in raidVal.raidTeamDic.values():
                for raidPlayerVal in raidTeamVal.teamPlayerDic.values():
                    if not _checkBox:
                        # checkBox已经没有玩家, 直接结束
                        return

                    if raidPlayerVal.playerGbId not in _checkBox:
                        continue

                    DEBUG_MSG('refreshRaidCache 1:: force fresh avatar raidCache: ', raidPlayerVal.playerGbId)
                    # 延迟处理
                    if not playerRaidCacheVal:
                        playerRaidCacheVal = raidVal._buildPlayerRaidCacheVal()
                    _refreshRaidCacheValue(raidPlayerVal, playerRaidCacheVal, _checkBox)
        else:
            # 2.处理检测数量小于团队数量的情况
            playerGBIDs = list(_checkBox)
            for playerGBID in playerGBIDs:
                for raidTeamVal in raidVal.raidTeamDic.values():
                    raidPlayerVal = raidTeamVal.teamPlayerDic.get(playerGBID, None)
                    if not raidPlayerVal:
                        continue
                    DEBUG_MSG('refreshRaidCache 2:: force fresh avatar raidCache: ', raidPlayerVal.playerGbId)
                    # 延迟处理
                    if not playerRaidCacheVal:
                        playerRaidCacheVal = raidVal._buildPlayerRaidCacheVal()
                    _refreshRaidCacheValue(raidPlayerVal, playerRaidCacheVal, _checkBox)

        # 处理不在队伍里的玩家，刷新缓存
        if _checkBox:
            playerRaidEmptyCacheVal = raid.PlayerRaidCacheVal()
            WARNING_MSG('refreshRaidCache 3:: force clear last avatars raidCache: ', _checkBox)
            gameengine.getGlobalBase('PlayerStub').doOnOthersCell(list(_checkBox), 'onRefreshPlayerRaidCacheVal',
                                                                  (playerRaidEmptyCacheVal, ), None, '', ())

    def onTimer(self, timerHandle, userData):
        self._onTimer(timerHandle, userData)
        if utils.isBelongTimerTag(userData):
            self._onTimerCallback(timerHandle)

    def onPlayerIsOffline(self, offlineGbId, gbId, name):
        """异步调用方法时玩家下线后回调"""
        INFO_MSG('onPlayerIsOffline::', offlineGbId, gbId, name)
        gameengine.getGlobalBase('PlayerStub').doOnOthersBase(
            [gbId], 'onMessagePre', (MMD.datas.raid_applicantOffline, [name]), None, '', ())

    def onTransfer(self, playerGbId, teamIDX, raidVal, broadcast):
        if raidVal.isEmpty():
            return
        teamVal = raidVal.raidTeamDic[teamIDX]
        playerVal = teamVal.teamPlayerDic[playerGbId]

        if playerVal.playerGbId == raidVal.raidLeaderGBID:
            deputyVal = raidVal.getRaidDeputy()
            if deputyVal and deputyVal.bOnline:
                self.transferRaidLeader(
                    playerVal.playerBox, playerVal.playerGbId, raidVal.raidUUID,
                    deputyVal.playerGbId, {}, broadcast)
            else:
                transedPlayerVal = raidVal.getNextActivePlayer(excepted=(playerVal.playerGbId,))
                if transedPlayerVal:
                    self.transferRaidLeader(
                        playerVal.playerBox, playerVal.playerGbId, raidVal.raidUUID,
                        transedPlayerVal.playerGbId, {}, broadcast)
        elif raidVal.isRaidDeputy(playerVal.playerGbId):
            self.transferRaidDeputy(
                playerVal.playerBox, playerVal.playerGbId, raidVal.raidUUID,
                0, {}, True, broadcast)

    def _onLeaderClientDeath(self, raidUUID, playerGBID):
        INFO_MSG('_onLeaderClientDeath::', raidUUID, playerGBID)
        if raidUUID not in self.raidDic:
            ERROR_MSG('_onLeaderClientDeath:: failed', raidUUID, playerGBID)
            return

        raidVal = self.raidDic[raidUUID]
        if raidVal.leaderClientDeathTimer > 0:
            self._cancelCallback(raidVal.leaderClientDeathTimer, gametimer.TIMER_TAG_LEADER_CLIENT_DEATH)
            raidVal.leaderClientDeathTimer = 0

        if playerGBID != raidVal.raidLeaderGBID:
            WARNING_MSG('_onLeaderClientDeath:: failed', raidUUID, playerGBID, raidVal.raidLeaderGBID)
            return

        leaderVal = raidVal.getRaidLeader()
        if leaderVal.bOnline:
            return

        self.onTransfer(raidVal.raidLeaderGBID, raidVal.raidLeaderTeamIDX, raidVal, False)
        if not raidVal.getNextActivePlayer(excepted=(playerGBID,)):
            self.doDisbandRaid(raidVal.raidUUID, {})
            raidVal.clearRaidCacheValToAllPlayers()
        else:
            raidVal.refreshRaidCacheValToAllPlayers()

    def onAvatarClientDeath(self, raidUUID, teamIDX, playerGBID):
        """团队玩家掉线后回调"""
        INFO_MSG('onAvatarClientDeath::', raidUUID, teamIDX, playerGBID)
        errno = gameconst.RaidErrno
        raidVal = None

        def _onAvatarClientOffline():
            nonlocal raidVal, teamIDX

            if raidUUID not in self.raidDic:
                return None, errno.RAID_RAID_ID_NOT_FOUND.initkvbody(source='onAvatarOffline',
                                                                     raidUUID=raidUUID)

            raidVal = self.raidDic[raidUUID]
            if not teamIDX:
                teamIDX = raidVal.getRaidTeamIDX(playerGBID)

            if teamIDX not in raidVal.raidTeamDic:
                return None, errno.RAID_TEAM_IDX_NOT_FOUND.initkvbody(source='onAvatarOffline',
                                                                      raidUUID=raidUUID,
                                                                      teamIDX=teamIDX)

            memberVal = raidVal.raidTeamDic[teamIDX]
            if playerGBID not in memberVal.teamPlayerDic:
                return None, errno.RAID_PLAYER_GBID_NOT_FOUND.initkvbody(source='onAvatarOffline',
                                                                         raidUUID=raidUUID,
                                                                         teamIDX=teamIDX,
                                                                         playerGBID=playerGBID)
            playerVal = memberVal.teamPlayerDic[playerGBID]
            playerVal.bOnline = False

            return playerVal, errno.RAID_OK

        clientOfflinePlayerVal, err = _onAvatarClientOffline()
        if err != errno.RAID_OK:
            WARNING_MSG('onAvatarClientDeath:: failed, {}'.format(err))
            return

        if raidVal.raidLeaderGBID == playerGBID:
            if raidVal.leaderClientDeathTimer > 0:
                self._cancelCallback(raidVal.leaderClientDeathTimer, gametimer.TIMER_TAG_LEADER_CLIENT_DEATH)

            raidVal.leaderClientDeathTimer = self._callback(RAID_CONST.datas["raid_RLDownGradeOfflineTime"]["value"], '_onLeaderClientDeath', (raidUUID, playerGBID, ), gametimer.TIMER_TAG_LEADER_CLIENT_DEATH)

        raidVal.refreshPlayerPropsValToAllPlayers(teamIDX, playerGBID, clientOfflinePlayerVal, needDel=False)
        raidVal.broadcastAllRaidMembersClient('onRaidAvatarOffline', (raidUUID, teamIDX, playerGBID))

        self.leaveRaid(clientOfflinePlayerVal.playerBox, playerGBID, raidUUID, {})

    def onAvatarOffline(self, raidUUID, teamIDX, playerGBID):
        self.onAvatarClientDeath(raidUUID, teamIDX, playerGBID)
        return

    def onAvatarLogin(self, playerBox, playerGBID, raidUUID):
        """团队玩家(客户端)重新登录后回调"""
        INFO_MSG('onAvatarLogin::', playerBox, playerGBID, raidUUID)
        errno = gameconst.RaidErrno

        raidVal = None
        teamIDX = 0

        def _onAvatarLogin():
            nonlocal teamIDX, raidVal
            if raidUUID not in self.raidDic:
                return None, errno.RAID_RAID_ID_NOT_FOUND.initkvbody(source='onAvatarLogin',
                                                                     raidUUID=raidUUID)

            raidVal = self.raidDic[raidUUID]
            teamIDX = raidVal.getRaidTeamIDX(playerGBID)
            if not teamIDX or teamIDX not in raidVal.raidTeamDic:
                return None, errno.RAID_TEAM_IDX_NOT_FOUND.initkvbody(source='onAvatarLogin',
                                                                      raidUUID=raidUUID,
                                                                  teamIDX=teamIDX)

            memberVal = raidVal.raidTeamDic[teamIDX]
            playerVal = memberVal.teamPlayerDic[playerGBID]
            playerVal.bOnline = True
            playerVal.playerBox = playerBox
            return playerVal, errno.RAID_OK

        onlinePlayerVal, err = _onAvatarLogin()
        if err != errno.RAID_OK:
            playerBox.cell.onRefreshPlayerRaidCacheVal(raid.PlayerRaidCacheVal())
            WARNING_MSG('onAvatarLogin:: cache outdate, clear avatar cache. {}'.format(err))
            return

        if raidVal.raidLeaderGBID == playerGBID and raidVal.leaderClientDeathTimer > 0:
            self._cancelCallback(raidVal.leaderClientDeathTimer, gametimer.TIMER_TAG_LEADER_CLIENT_DEATH)
            raidVal.leaderClientDeathTimer = 0

        playerBox.cell.onRefreshPlayerRaidCacheVal(raidVal._buildPlayerRaidCacheVal())
        raidVal.refreshPlayerPropsValToAllPlayers(teamIDX, playerGBID, onlinePlayerVal,
                                                  needDel=False, exclude=(playerGBID, ))

        playerBox.client.onGetRaidData(raidVal.toClientData())
        record = self._getStandbyCheckerRecord(raidUUID)

        raidVal.broadcastAllRaidMembersClient(
            'onRaidAvatarLogin', (raidUUID, teamIDX, playerGBID), exclude=(playerGBID, ))

    def updateRaidMemberCacheVal(self, raidUUID, playerGBID, playerUpdateProps):
        #DEBUG_MSG('updateRaidMemberCacheVal::', raidUUID, playerGBID, playerUpdateProps)

        def _updateRaidMemberCacheVal():
            if raidUUID not in self.raidDic:
                return None, gameconst.RaidErrno.RAID_RAID_ID_NOT_FOUND.initkvbody(source='updateRaidMemberCacheVal',
                                                                                    raidUUID=raidUUID, 
                                                                                    teamIDX=teamIDX,
                                                                                    playerGBID=playerGBID)
            raidVal = self.raidDic[raidUUID]
            teamIDX = raidVal.getRaidTeamIDX(playerGBID)
            if not teamIDX:
                return None, gameconst.RaidErrno.RAID_PLAYER_GBID_NOT_FOUND.initkvbody(source='updateRaidMemberCacheVal',
                                                                                        raidUUID=raidUUID,
                                                                                        teamIDX=teamIDX,
                                                                                        playerGBID=playerGBID)

            memberVal = raidVal.raidTeamDic[teamIDX].teamPlayerDic[playerGBID]
            memberVal.updateAttr(playerUpdateProps)
            return raidVal, gameconst.RaidErrno.RAID_OK

        updateRaidVal, err = _updateRaidMemberCacheVal()
        if err != gameconst.RaidErrno.RAID_OK:
            ERROR_MSG('updateRaidMemberCacheVal:: failed, {}'.format(err))
            return

        DEBUG_MSG('updateRaidMemberCacheVal:: broadcast ~ ', playerGBID, playerUpdateProps)
        updateRaidVal.updateMemberVolatileAttr(playerGBID, playerUpdateProps)

    def getRaidApplyJoinDic(self, srcPlayerBox, srcPlayerGBID, raidUUID):
        INFO_MSG('getRaidApplyJoinDic::', srcPlayerBox, srcPlayerGBID, raidUUID)
        _, err = self._getRaidApplyJoinDicCheck(srcPlayerBox, srcPlayerGBID, raidUUID)
        if err != gameconst.RaidErrno.RAID_OK:
            ERROR_MSG('getRaidApplyJoinDic:: failed, {}'.format(err))
            return

        raidVal = self.raidDic[raidUUID]
        _data = [i.toClientDict() for i in raidVal.raidApplyJoinDic.values()]
        # ERROR_MSG('  getRaidApplyJoinDic::', srcPlayerBox, srcPlayerGBID, raidUUID, _data)
        raidVal = self.raidDic[raidUUID]
        srcPlayerBox.client.onGetRaidApplyJoinList(raidUUID, _data)

    def _getRaidApplyJoinDicCheck(self, srcPlayerBox, srcPlayerGBID, raidUUID):
        if raidUUID not in self.raidDic:
            return None, gameconst.RaidErrno.RAID_RAID_ID_NOT_FOUND

        raidVal = self.raidDic[raidUUID]
        if raidVal.raidLeaderGBID != srcPlayerGBID and not raidVal.isRaidDeputy(srcPlayerGBID):
            return None, gameconst.RaidErrno.RAID_NOT_RAID_LEADER_OR_DEPUTY

        return None, gameconst.RaidErrno.RAID_OK

    def clearRaidApplyJoinDic(self, srcPlayerBox, srcPlayerGBID, raidUUID):
        INFO_MSG('clearRaidApplyJoinDic::', srcPlayerBox, srcPlayerGBID, raidUUID)
        _, err = self._clearRaidApplyJoinDicCheck(srcPlayerBox, srcPlayerGBID, raidUUID)
        if err != gameconst.RaidErrno.RAID_OK:
            ERROR_MSG('clearRaidApplyJoinDic:: failed, {}'.format(err))
            return
        self.doClearRaidApplyJoinDic(raidUUID)

    def _clearRaidApplyJoinDicCheck(self, srcPlayerBox, srcPlayerGBID, raidUUID):
        if raidUUID not in self.raidDic:
            return None, gameconst.RaidErrno.RAID_RAID_ID_NOT_FOUND
        raidVal = self.raidDic[raidUUID]

        if raidVal.raidLeaderGBID != srcPlayerGBID and not raidVal.isRaidDeputy(srcPlayerGBID):
            return None, gameconst.RaidErrno.RAID_NOT_RAID_LEADER_OR_DEPUTY

        return None, gameconst.RaidErrno.RAID_OK

    def doClearRaidApplyJoinDic(self, raidUUID):
        INFO_MSG('doClearRaidApplyJoinDic::', raidUUID)
        raidVal = self.raidDic[raidUUID]

        singleJoinPlayerGBIDList = []
        teamJoinPlayerGBIDList = []
        for joinVal in raidVal.raidApplyJoinDic.values():
            if joinVal.raidJoinType == gameconst.RaidJoinType.SINGLE:
                singleJoinPlayerGBIDList.append(joinVal.joinPlayerGBID)
            elif joinVal.raidJoinType == gameconst.RaidJoinType.TEAM:
                teamJoinPlayerGBIDList.append((joinVal.joinPlayerGBID, joinVal.joinTeamUUID))

        playerStub = gameengine.getGlobalBase('PlayerStub')
        playerStub.doOnOthersCell(singleJoinPlayerGBIDList, 'onJoinListPlayerClearRaidApplyJoinDic',
                                  (raidUUID, gameconst.RaidJoinType.SINGLE, 0), None, '', ())

        for gbId, teamUUID in teamJoinPlayerGBIDList:
            playerStub.doOnOthersCell([gbId, ], 'onJoinListPlayerClearRaidApplyJoinDic',
                                      (raidUUID, gameconst.RaidJoinType.TEAM, teamUUID), None, '', ())

        raidVal.clearRaidJoin()

        leaderAndDeputyVal = {raidVal.getRaidLeader(), raidVal.getRaidDeputy()}
        for val in leaderAndDeputyVal:
            if val and val.playerBox and val.playerBox.client:
                val.playerBox.client.onClearRaidApplyJoinDic(raidUUID)

    def clearRaidJoinRecords(self, srcPlayerBox, srcPlayerGBID, clearRaidIdList):
        INFO_MSG('clearRaidJoinRecords::', srcPlayerBox, srcPlayerGBID, clearRaidIdList)

        for raidUUID, joinType in clearRaidIdList:
            if raidUUID not in self.raidDic:
                WARNING_MSG('clearRaidJoinRecords:: raidUUID not found', raidUUID)
                continue
            raidVal = self.raidDic[raidUUID]
            joinVal, err = raidVal.getRaidJoin(srcPlayerGBID)
            if err != gameconst.RaidErrno.RAID_OK:
                WARNING_MSG('clearRaidJoinRecords:: get failed, {}'.format(err))
                continue

            if joinVal.raidJoinType != joinType:
                WARNING_MSG('clearRaidJoinRecords:: joinType not match', joinVal.raidJoinType, joinType)
                continue

            playerJoinVal, err = raidVal.popRaidJoin(srcPlayerGBID)
            if err != gameconst.RaidErrno.RAID_OK:
                WARNING_MSG('clearRaidJoinRecords:: pop failed, {}'.format(err))
            elif playerJoinVal.applyTimeoutTimerId:
                self._cancelCallback(playerJoinVal.applyTimeoutTimerId,
                                    gametimer.TIMER_TAG_RAID_APPLY_JOIN_TIMEOUT)
                playerJoinVal.applyTimeoutTimerId = 0

            # 刷新对应团队团/副团长客户端的申请列表
            leaderAndDeputyVal = {raidVal.getRaidLeader(), raidVal.getRaidDeputy()}
            for val in leaderAndDeputyVal:
                if val:
                    self.getRaidApplyJoinDic(val.playerBox, val.playerGbId, raidUUID)

        srcPlayerBox and srcPlayerBox.cell and srcPlayerBox.cell.onClearRaidJoinRecords(clearRaidIdList)

    def getRaidAllMembersAttrs(self, srcPlayerBox, srcPlayerGBID, raidUUID, memberGBIDList, extraProps):
        # INFO_MSG('getRaidAllMembersAttrs::', srcPlayerBox, srcPlayerGBID, raidUUID, memberGBIDList, extraProps)
        raidMemberAttrsList, err = self._getRaidAllMembersAttrs(srcPlayerBox, srcPlayerGBID, raidUUID, set(memberGBIDList))
        if err != gameconst.RaidErrno.RAID_OK:
            WARNING_MSG('getRaidAllMembersAttrs:: client get attrs failed, {}'.format(err),
                        srcPlayerGBID, raidUUID, memberGBIDList)
            return

        while raidMemberAttrsList:
            _raidMemberAttrsList = raidMemberAttrsList[:gameconst.RAID_TEAM_MEMBER_MAX_NUM]
            raidMemberAttrsList = raidMemberAttrsList[gameconst.RAID_TEAM_MEMBER_MAX_NUM:]
            srcPlayerBox.client.onGetRaidAllMembersAttrs(raidUUID, _raidMemberAttrsList)

    def _getRaidAllMembersAttrs(self, srcPlayerBox, srcPlayerGBID, raidUUID, memberGBIDList):
        if raidUUID not in self.raidDic:
            return None, gameconst.RaidErrno.RAID_RAID_ID_NOT_FOUND

        raidVal = self.raidDic[raidUUID]
        raidMemberAttrsList = []
        for raidTeamVal in raidVal.raidTeamDic.values():
            for raidMemberGBID, raidMemberVal in raidTeamVal.teamPlayerDic.items():
                if raidMemberGBID in memberGBIDList:
                    raidMemberAttrsList.append(raidMemberVal.toClientData())

        return raidMemberAttrsList, gameconst.RaidErrno.RAID_OK

    def createRaidLonely(self, srcPlayerBox, srcPlayerGBID, raidUUID, capacity, memberPropsList, extraProps, raidTarget, minLevel, minScore, recruitInfo, password, isAutoExpedition):
        INFO_MSG('createRaidLonely::', srcPlayerBox, srcPlayerGBID, raidUUID, capacity, memberPropsList, extraProps, raidTarget, minLevel, minScore, recruitInfo, password, isAutoExpedition)
        _, err = self._createRaid(srcPlayerBox, srcPlayerGBID, raidUUID, capacity, memberPropsList, raidTarget, minLevel, minScore, recruitInfo, password, isAutoExpedition)
        if err != gameconst.RaidErrno.RAID_OK:
            ERROR_MSG('createRaid:: failed, {}'.format(err))
            return

    def createRaid(self, srcPlayerBox, srcPlayerGBID, raidUUID, capacity, memberPropsList, extraProps):
        INFO_MSG('createRaid::', srcPlayerBox, srcPlayerGBID, raidUUID, capacity, memberPropsList, extraProps)
        _, err = self._createRaid(srcPlayerBox, srcPlayerGBID, raidUUID, capacity, memberPropsList, 1, 0, 0, TMMCD.datas["raidTeamTitleDes"]["value"], '', False)
        if err != gameconst.RaidErrno.RAID_OK:
            ERROR_MSG('createRaid:: failed, {}'.format(err))
            return

    def checkAutoStart(self, raidUUID):
        raidVal = self.raidDic.get(raidUUID)
        if not raidVal:
            return

        if raidVal.autoStartTimer > 0:
            self._cancelCallback(raidVal.autoStartTimer, gametimer.TIMER_TAG_RAID_AUTO_START)
            raidVal.autoStartTimer = 0

        if raidVal.isAutoExpedition and raidVal.raidTarget > gameconst.PARE_ACTIVITY_ID:
            if raidVal.isRaidFull():
                captainBox = raidVal.getRaidLeaderBox()
                if captainBox and captainBox.cell:
                    captainBox.cell.autoStartChiefDungeon()
                    return
            raidVal.autoStartTimer = self._callback(5, 'checkAutoStart', (raidUUID,), gametimer.TIMER_TAG_RAID_AUTO_START)

    def _createRaid(self, srcPlayerBox, srcPlayerGBID, raidUUID, capacity, memberPropsList, raidTarget, minLevel, minScore, recruitInfo, password, isAutoExpedition):
        raidLeaderBox, raidLeaderGBID = srcPlayerBox, srcPlayerGBID

        if not dataUtils.isRaidCapacityValidate(capacity):
            return None, gameconst.RaidErrno.RAID_UNKNOWN_CAPACITY.initkvbody(source='_createRaid',
                                                                              raidUUID=raidUUID,
                                                                              capacity=capacity)

        if raidUUID in self.raidDic:
            return None, gameconst.RaidErrno.RAID_RAID_ID_REPEAT.initkvbody(source='_createRaid',
                                                                            raidUUID=raidUUID)
        siegeWarCamp = 0
        if memberPropsList:
            siegeWarCamp = memberPropsList[0]['siegeWarCamp']
        if gameconfig.isCrossServer() and siegeWarCamp != 0:
            raidTarget = gameconst.SIEGEWAR_PARE_ACTIVITY_ID
        raidVal = raid.RaidVal(raidUUID=raidUUID, raidCapacity=capacity, siegeWarCamp=siegeWarCamp, raidTarget=raidTarget)
        teamIDX = 1
        raidTeamVal, err = raidVal.addNewTeam(teamIDX)
        if err != gameconst.RaidErrno.RAID_OK:
            ERROR_MSG('_createRaid:: create Team failed, {}'.format(err))
            return None, err

        for memberProps in memberPropsList:
            memberVal, err = raidTeamVal.addTeamMember(memberProps['playerGbId'], memberProps)
            if err != gameconst.RaidErrno.RAID_OK:
                ERROR_MSG('_createRaid:: add team member failed, {}'.format(err))
                return None, err
            raidVal.broadcastAllRaidMembersCell('onRaidAddNewMember', (memberProps['playerBox'].id,), (memberProps['playerGbId'],))
            
        _, err = raidVal.setRaidLeader(raidLeaderGBID, teamIDX)
        if err != gameconst.RaidErrno.RAID_OK:
            ERROR_MSG('_createRaid:: set raid leader failed, {}'.format(err))
            return None, err

        self.raidDic[raidUUID] = raidVal
        
        raidVal.isPublish = False

        if raidVal.raidTarget > 0 and len(raidVal.password) == 0:
            raidVal.isPublish = True
        
        raidVal.raidMinLevel = minLevel
        raidVal.raidMinScore = minScore
        raidVal.recruitInfo = recruitInfo
        raidVal.password = password
        raidVal.isAutoExpedition = isAutoExpedition

        raidVal.refreshRaidCacheValToAllPlayers()
        raidVal.broadcastAllRaidMembersClient('onCreateRaid', (raidVal.toClientData(), ))
        raidVal.broadcastAllRaidMembersBase('onMessagePre', (RAID_CONST.datas["raidCreated_chatMsg"]["value"], []))

        if len(raidVal.password) == 0:
            if raidVal.raidTarget > gameconst.PARE_ACTIVITY_ID:
                self.raidPrepareAutoMatch(raidUUID)
        self.checkAutoStart(raidUUID)

        return raidVal, gameconst.RaidErrno.RAID_OK

    def disbandRaid(self, srcPlayerBox, srcPlayerGBID, raidUUID, extra):
        INFO_MSG('disbandRaid::', srcPlayerBox, srcPlayerGBID, raidUUID, extra)
        delRaidVal, err = self._disbandRaidCheck(srcPlayerBox, srcPlayerGBID, raidUUID)
        if err != gameconst.RaidErrno.RAID_OK:
            ERROR_MSG('disbandRaid:: failed, {}'.format(err))
            return

        self.doDisbandRaid(raidUUID, extra)

        delRaidVal.clearRaidCacheValToAllPlayers()
        delRaidVal.broadcastAllRaidMembersClient('onDisbandRaid', (raidUUID, ))
        '''
        gameengine.getGlobalBase('EliteInvasionStub').onEliteInvRaidDisband(raidUUID)
        '''

    def _disbandRaidCheck(self, srcPlayerBox, srcPlayerGBID, raidUUID):
        leaderBox, leaderGBID = srcPlayerBox, srcPlayerGBID

        if raidUUID not in self.raidDic:
            return None, gameconst.RaidErrno.RAID_RAID_ID_NOT_FOUND.initkvbody(
                source='_disbandRaid', raidUUID=raidUUID)

        raidVal = self.raidDic[raidUUID]
        if raidVal.raidLeaderGBID != leaderGBID:
            return None, gameconst.RaidErrno.RAID_NOT_RAID_LEADER.initkvbody(
                source='_disbandRaid', orgLeaderGBID=leaderGBID, crtLeaderGBID=raidVal.raidLeaderGBID)

        return raidVal, gameconst.RaidErrno.RAID_OK

    def doDisbandRaid(self, raidUUID, extra):
        INFO_MSG('doDisbandRaid::', raidUUID, extra)
        # when disband raid, try clear all join val first
        self.doClearRaidApplyJoinDic(raidUUID)
        raidVal = self.raidDic.pop(raidUUID)

        try:
            raidVal.clearMarkRecord(self)
        except Exception as e:
            ERROR_MSG('doDisbandRaid:: clearMarkRecord exception: {}'.format(e))

        # 团队解散了，从匹配队列里停止
        if raidVal.raidAutoMatchTime > 0:
            raidVal.raidAutoMatchTime = 0
            gameengine.getGlobalBase('RaidMatchStub').raidStopAutoMatch(raidUUID)

        if raidVal.leaderClientDeathTimer > 0:
                self._cancelCallback(raidVal.leaderClientDeathTimer, gametimer.TIMER_TAG_LEADER_CLIENT_DEATH)
                raidVal.leaderClientDeathTimer = 0
        for dungeonNo, dunVal in raidVal.raidDungeonRecords.items():
            stub = gameengine.getDungeonStubBySpaceNo(dunVal.spaceNo)
            WARNING_MSG('doDisbandRaid:: disbandRaid and complete dungeon in force ', dungeonNo, dunVal)
            stub.completeRaidDungeon(dunVal.spaceNo, raidUUID, False, 0, gameconst.DunegonCompleteReasonType.LEAVE)

    def applyJoinRaidLonely(self, joinedPlayerBox, joinedPlayerGBID, joinedPlayerProps, raidUUID, extraProps, password, ignorePassword, applySource):
        INFO_MSG('applyJoinRaidLonely::', joinedPlayerBox, joinedPlayerGBID, joinedPlayerProps, raidUUID, extraProps, password, ignorePassword, applySource)
        playerJoinVal, err = self._applyJoinRaidLonely(joinedPlayerBox, joinedPlayerGBID, joinedPlayerProps, raidUUID, password, ignorePassword, applySource)
        if err != gameconst.RaidErrno.RAID_OK:
            return

        if joinedPlayerBox and joinedPlayerBox.cell:
            joinedPlayerBox.cell.onApplyJoinRaidLonelySucc(joinedPlayerGBID, raidUUID, extraProps)

        leaderAndDeputyVal = {self.raidDic[raidUUID].getRaidLeader(), self.raidDic[raidUUID].getRaidDeputy()}
        for val in leaderAndDeputyVal:
            if val and val.playerBox and val.playerBox.cell:
                val.playerBox.cell.onLeaderProcessApplyJoinRaidLonely(
                    joinedPlayerBox, joinedPlayerGBID, playerJoinVal.toClientDict(), raidUUID, extraProps)

        playerJoinVal.applyTimeoutTimerId = self.toCallbackAfter(
            self.raidJoinRecordTimeout, tag=gametimer.TIMER_TAG_RAID_APPLY_JOIN_TIMEOUT
        )._onRaidApplyJoinRecordTimeout(raidUUID, joinedPlayerGBID)

    def _applyJoinRaidLonely(self, joinedPlayerBox, joinedPlayerGBID, joinPlayerProps, raidUUID, password, ignorePassword, applySource):
        box = joinPlayerProps['playerBox']
        if raidUUID not in self.raidDic:
            box.client and box.client.onApplyJoinRaidLonelyFailed(gameconst.TeamApplyResult.RAID_IS_NOT_EXIST, 0, 0, 0, '', applySource)
            return None, gameconst.RaidErrno.RAID_RAID_ID_NOT_FOUND.initkvbody(
                source='_applyJoinRaidLonely', raidUUID=raidUUID)

        raidVal = self.raidDic[raidUUID]

        level = joinPlayerProps['level']
        score = joinPlayerProps['score']

        if self.checkInDungeon(raidVal.raidUUID):
            box.client and box.client.onApplyJoinRaidLonelyFailed(gameconst.TeamApplyResult.TEAM_APPLY_IS_IN_DUNGEON, raidVal.raidUUID, raidVal.raidMinLevel, raidVal.raidMinScore, raidVal.password, applySource)
            return None, gameconst.RaidErrno.RAID_IS_IN_DUNGEON.initkvbody(
                source='_applyJoinRaidLonely', raidUUID=raidUUID)

        if raidVal.isRaidFull():
            box.client and box.client.onApplyJoinRaidLonelyFailed(gameconst.TeamApplyResult.RAID_IS_FULL, raidVal.raidUUID, raidVal.raidMinLevel, raidVal.raidMinScore, raidVal.password, applySource)
            return None, gameconst.RaidErrno.RAID_RAID_TEAM_IS_FULL.initkvbody(
                source='_applyJoinRaidLonely', raidUUID=raidUUID)

        if raidVal.isRaidApplyListFull():
            box.client and box.client.onApplyJoinRaidLonelyFailed(gameconst.TeamApplyResult.RAID_APPLY_LIST_IS_FULL, raidVal.raidUUID, raidVal.raidMinLevel, raidVal.raidMinScore, raidVal.password, applySource)
            return None, gameconst.RaidErrno.RAID_APPLY_LIST_IS_FULL.initkvbody(
                source='_applyJoinRaidLonely', raidUUID=raidUUID)

        if level < raidVal.raidMinLevel:
            box.client and box.client.onApplyJoinRaidLonelyFailed(gameconst.TeamApplyResult.TEAM_APPLY_LEVEL_IS_NOT_ENOUGH, raidVal.raidUUID, raidVal.raidMinLevel, raidVal.raidMinScore, raidVal.password, applySource)
            return None, gameconst.RaidErrno.RAID_LEVEL_IS_ILLEGAL.initkvbody(
                source='_applyJoinRaidLonely', raidUUID=raidUUID)

        if score < raidVal.raidMinScore:
            box.client and box.client.onApplyJoinRaidLonelyFailed(gameconst.TeamApplyResult.TEAM_APPLY_SCORE_IS_NOT_ENOUGH, raidVal.raidUUID, raidVal.raidMinLevel, raidVal.raidMinScore, raidVal.password, applySource)
            return None, gameconst.RaidErrno.RAID_SOCRE_IS_ILLEGAL.initkvbody(
                source='_applyJoinRaidLonely', raidUUID=raidUUID)

        if not ignorePassword:
            if len(raidVal.password) > 0:
                if len(password) == 0:
                    box.client and box.client.onApplyJoinRaidLonelyFailed(gameconst.TeamApplyResult.TEAM_APPLY_NEED_PASSWORD, raidVal.raidUUID, raidVal.raidMinLevel, raidVal.raidMinScore, raidVal.password, applySource)
                    return None, gameconst.RaidErrno.RAID_PASSWORD_IS_EMPTY.initkvbody(
                        source='_applyJoinRaidLonely', raidUUID=raidUUID)
                if password != raidVal.password:
                    box.client and box.client.onApplyJoinRaidLonelyFailed(gameconst.TeamApplyResult.TEAM_APPLY_WRONG_PASSWORD, raidVal.raidUUID, raidVal.raidMinLevel, raidVal.raidMinScore, raidVal.password, applySource)
                    return None, gameconst.RaidErrno.RAID_PASSWORD_IS_ILLEGAL.initkvbody(
                        source='_applyJoinRaidLonely', raidUUID=raidUUID)


        if gameconfig.isCrossServer() and raidVal.siegeWarCamp != 0 and joinPlayerProps['siegeWarCamp'] != 0 \
            and raidVal.siegeWarCamp != joinPlayerProps['siegeWarCamp']:
            box.client and box.client.onApplyJoinRaidLonelyFailed(gameconst.TeamApplyResult.TEAM_APPLY_FAIL, raidVal.raidUUID, raidVal.raidMinLevel, raidVal.raidMinScore, raidVal.password, applySource)
            return None, gameconst.RaidErrno.RAID_NOT_SAME_SIEGEWAR_CAMP

        playerJoinVal, err = raidVal.addSingleRaidJoin(playerGBID=joinedPlayerGBID,
                                                       playerName=joinPlayerProps['playerName'],
                                                       level=joinPlayerProps['level'],
                                                       school=joinPlayerProps['school'],
                                                       sex=joinPlayerProps['sex'],
                                                       score=joinPlayerProps['score'], 
                                                       applySource=applySource)
        if err != gameconst.RaidErrno.RAID_OK:
            box.client and box.client.onApplyJoinRaidLonelyFailed(gameconst.TeamApplyResult.TEAM_APPLY_FAIL, raidVal.raidUUID, raidVal.raidMinLevel, raidVal.raidMinScore, raidVal.password, applySource)
            return None, err
        box.client and box.client.onApplyJoinRaidLonelyFailed(gameconst.TeamApplyResult.TEAM_APPLY_OK, raidVal.raidUUID, raidVal.raidMinLevel, raidVal.raidMinScore, raidVal.password, applySource)
        return playerJoinVal, gameconst.RaidErrno.RAID_OK

    def applyJoinRaidWithTeam(self, joinedCaptainBox, joinedCaptainGBID, teamUUID, raidUUID, memberDataList, extraProps):
        INFO_MSG('applyJoinRaidWithTeam::', joinedCaptainBox, joinedCaptainGBID, teamUUID, raidUUID, memberDataList, extraProps)
        raidPlayerJoinVal, _err = self._applyJoinRaidWithTeam(joinedCaptainBox, joinedCaptainGBID, teamUUID, raidUUID, memberDataList, extraProps)
        if _err != gameconst.RaidErrno.RAID_OK:
            if _err == gameconst.RaidErrno.RAID_APPLY_JOIN_NUMBER_OFR:
                WARNING_MSG('applyJoinRaidWithTeam::apply join number out of range', _err)
                joinedCaptainBox and joinedCaptainBox.onMessagePre(RAID_CONST.datas["raid_applyFull_msg"]["value"], [])
            elif _err == gameconst.RaidErrno.RAID_ALREADY_APPLY_JOIN:
                WARNING_MSG('applyJoinRaidWithTeam::already apply join', _err)
            else:
                ERROR_MSG('applyJoinRaidWithTeam:: failed, {}'.format(_err))
            return

        if joinedCaptainBox and joinedCaptainBox.cell:
            joinedCaptainBox.cell.onApplyJoinRaidWithTeamSucc(joinedCaptainGBID, teamUUID, raidUUID, extraProps)

        leaderAndDeputyVal = {self.raidDic[raidUUID].getRaidLeader(), self.raidDic[raidUUID].getRaidDeputy()}
        for val in leaderAndDeputyVal:
            if val and val.playerBox and val.playerBox.cell:
                val.playerBox.cell.onLeaderProcessApplyJoinRaidWithTeam(
                    joinedCaptainBox, joinedCaptainGBID, raidPlayerJoinVal.toClientDict(), teamUUID, raidUUID, extraProps)

        raidPlayerJoinVal.applyTimeoutTimerId = self.toCallbackAfter(
            self.raidJoinRecordTimeout, tag=gametimer.TIMER_TAG_RAID_APPLY_JOIN_TIMEOUT
        )._onRaidApplyJoinRecordTimeout(raidUUID, joinedCaptainGBID)

    def _applyJoinRaidWithTeam(self, joinedCaptainBox, joinedCaptainGBID, teamUUID, raidUUID, memberDataList, extraProps):
        if raidUUID not in self.raidDic:
            return None, gameconst.RaidErrno.RAID_RAID_ID_NOT_FOUND

        raidVal = self.raidDic[raidUUID]
        if gameconfig.isCrossServer() and raidVal.siegeWarCamp != 0 and extraProps['siegeWarCamp'] != 0 \
            and raidVal.siegeWarCamp != extraProps['siegeWarCamp']:
            return None, gameconst.RaidErrno.RAID_NOT_SAME_SIEGEWAR_CAMP
        raidPlayerJoinVal, err = raidVal.addTeamRaidJoin(captainGBID=joinedCaptainGBID,
                                                         teamUUID=teamUUID,
                                                         memberDataList=memberDataList)
        if err != gameconst.RaidErrno.RAID_OK:
            err = err.initkvbody(raidUUID=raidUUID, teamId=teamUUID)
            return None, err

        return raidPlayerJoinVal, gameconst.RaidErrno.RAID_OK

    def _onRaidApplyJoinRecordTimeout(self, raidUUID, primaryGBID):
        """入团申请超时, 取出该入团记录"""

        def _check():
            if raidUUID not in self.raidDic:
                return None, gameconst.RaidErrno.RAID_RAID_ID_NOT_FOUND
            raidVal = self.raidDic[raidUUID]
            if primaryGBID not in raidVal.raidApplyJoinDic:
                return None, gameconst.RaidErrno.RAID_APPLY_JOIN_STUB_VAL_NOT_FOUND
            return None, gameconst.RaidErrno.RAID_OK

        _, err = _check()
        if err != gameconst.RaidErrno.RAID_OK:
            WARNING_MSG('_onRaidApplyJoinRecordTimeout:: record lost', raidUUID, primaryGBID)
            return

        raidVal = self.raidDic[raidUUID]
        joinVal, _ = raidVal.popRaidJoin(primaryGBID)
        joinVal.applyTimeoutTimerId = 0
        gameengine.getGlobalBase('PlayerStub').doOnOthersCell(
            list(joinVal.raidJoinPlayerDic), 'onJoinPlayerHandleReplyJoinRaidReject',
            (raidUUID, ), None, '', ())

    def replyJoinRaid(self, srcPlayerBox, srcPlayerGBID, joinedPlayerGBID, raidUUID, beAgreed, extraProps):
        INFO_MSG('replyJoinRaid::', srcPlayerBox, srcPlayerGBID, joinedPlayerGBID, raidUUID, beAgreed, extraProps)

        def _reject():
            _playerJoinVal, _err = self._replyJoinRaidRemove(srcPlayerBox, srcPlayerGBID, joinedPlayerGBID, raidUUID)
            if _err != gameconst.RaidErrno.RAID_OK:
                WARNING_MSG('replyJoinRaid:: reject failed, {}'.format(_err))
                return

            gameengine.getGlobalBase('PlayerStub').doOnOthersCell(
                [joinedPlayerGBID, ], 'onJoinPlayerHandleReplyJoinRaidReject',
                (raidUUID, ), None, '', ())
            gameengine.getGlobalBase('PlayerStub').doOnOthersClient(
                [joinedPlayerGBID, ], 'onMessage',
                (RAID_CONST.datas["raid_applyRefused_msg"]["value"], []),
                    None, '', ())
            if _playerJoinVal.applyTimeoutTimerId:
                self._cancelCallback(_playerJoinVal.applyTimeoutTimerId,
                                    gametimer.TIMER_TAG_RAID_APPLY_JOIN_TIMEOUT)
                _playerJoinVal.applyTimeoutTimerId = 0

        if not beAgreed:
            _reject()
            return

        playerJoinVal, err = self._replyJoinRaidCheck(srcPlayerBox, srcPlayerGBID, joinedPlayerGBID, raidUUID)
        if err != gameconst.RaidErrno.RAID_OK:
            err = err.initkvbody(source=self._replyJoinRaidCheck.__name__,
                                 raidUUID=raidUUID,
                                 playerGBID=joinedPlayerGBID)

            if err == gameconst.RaidErrno.RAID_RAID_IS_FULL:
                WARNING_MSG('replayJoinRaid:: failed, raid is full')
                srcPlayerBox.onMessagePre(RAID_CONST.datas["raid_applyAcceptFail_raidFull_msg"]["value"], [])
                # DO NOT remove join info here
                return

            else:
                WARNING_MSG('replayJoinRaid:: failed, {}'.format(err))

            _reject()
            return

        if playerJoinVal.isSingle():
            # 单人申请直接通过
            self.doReplyJoinRaidLonely(srcPlayerBox, srcPlayerGBID, raidUUID, joinedPlayerGBID, extraProps)
        else:
            # 多人申请通过需要到teamStub上再确认以下
            self.doReplyJoinRaidWithTeam(srcPlayerBox, srcPlayerGBID, raidUUID,
                                         joinedPlayerGBID, extraProps)

    def _replyJoinRaidRemove(self, srcPlayerBox, srcPlayerGBID, joinedPlayerGBID, raidUUID):
        if raidUUID not in self.raidDic:
            return None, gameconst.RaidErrno.RAID_RAID_ID_NOT_FOUND

        raidVal = self.raidDic[raidUUID]
        if srcPlayerGBID != raidVal.raidLeaderGBID and not raidVal.isRaidDeputy(srcPlayerGBID):
            return None, gameconst.RaidErrno.RAID_NOT_RAID_LEADER_OR_DEPUTY

        playerJoinVal, err = raidVal.popRaidJoin(joinedPlayerGBID)
        if err != gameconst.RaidErrno.RAID_OK:
            return None, err

        return playerJoinVal, gameconst.RaidErrno.RAID_OK

    def _replyJoinRaidCheck(self, srcPlayerBox, srcPlayerGBID, joinedPlayerGBID, raidUUID):
        if raidUUID not in self.raidDic:
            return None, gameconst.RaidErrno.RAID_RAID_ID_NOT_FOUND

        raidVal = self.raidDic[raidUUID]
        if srcPlayerGBID != raidVal.raidLeaderGBID and not raidVal.isRaidDeputy(srcPlayerGBID):
            return None, gameconst.RaidErrno.RAID_NOT_RAID_LEADER_OR_DEPUTY

        if raidVal.isRaidFull():
            return None, gameconst.RaidErrno.RAID_RAID_IS_FULL

        playerJoinVal, err = raidVal.getRaidJoin(joinedPlayerGBID)
        if err != gameconst.RaidErrno.RAID_OK:
            return None, err

        return playerJoinVal, gameconst.RaidErrno.RAID_OK

    def doReplyJoinRaidLonely(self, srcPlayerBox, srcPlayerGBID, raidUUID, joinedPlayerGBID, extraProps):
        """ NOTE: Check raidUUID and joinPlayerGBID outside this method,
                  PLS DO NOT IMPL CHECK LOGIC INSIDE.
        """
        INFO_MSG('doReplyJoinRaidLonely::', raidUUID, joinedPlayerGBID, extraProps)
        raidVal = self.raidDic[raidUUID]
        playerJoinVal, _ = raidVal.popRaidJoin(joinedPlayerGBID)

        gameengine.getGlobalBase('PlayerStub').doOnOthersCell(
            [joinedPlayerGBID, ], 'onJoinPlayerReplyJoinRaidLonely',
            (srcPlayerGBID, raidUUID, joinedPlayerGBID, playerJoinVal.toSavedDict(), extraProps, playerJoinVal.raidJoinPlayerDic[joinedPlayerGBID].applySource),
             self, 'onPlayerIsOffline',
            (srcPlayerGBID, playerJoinVal.raidJoinPlayerDic[joinedPlayerGBID].playerName))

        if playerJoinVal.applyTimeoutTimerId:
            self._cancelCallback(playerJoinVal.applyTimeoutTimerId,
                                 gametimer.TIMER_TAG_RAID_APPLY_JOIN_TIMEOUT)
            playerJoinVal.applyTimeoutTimerId = 0

    def doReplyJoinRaidWithTeam(self, srcPlayerBox, srcPlayerGBID, raidUUID, joinedPlayerGBID, extraProps):
        """ NOTE: check conditions outisde this method,
                  PLS DO NOT IMPL CHECK LOGIC INSIDE.
        """
        INFO_MSG('doReplyJoinRaidWithTeam::', srcPlayerBox, srcPlayerGBID, raidUUID, joinedPlayerGBID, extraProps)
        raidVal = self.raidDic[raidUUID]
        playerJoinVal, _ = raidVal.getRaidJoin(joinedPlayerGBID)
        gameengine.getTeamStub(playerJoinVal.joinTeamUUID).replyJoinRaidWithTeam(
            srcPlayerBox, srcPlayerGBID, raidUUID, joinedPlayerGBID, playerJoinVal.joinTeamUUID,
            [i.toSavedDict() for i in playerJoinVal.raidJoinPlayerDic.values()], extraProps)

    def onReplyJoinRaidLonely(self, srcPlayerGBID, raidUUID, playerGBID, playerProps, extraProps):
        INFO_MSG('onReplyJoinRaidLonely::', srcPlayerGBID, raidUUID, playerGBID, playerProps, extraProps)
        playerVal, err = self._onReplyJoinRaidLonely(srcPlayerGBID, raidUUID, playerGBID, playerProps)
        if err != gameconst.RaidErrno.RAID_OK:
            if err == gameconst.RaidErrno.RAID_RAID_IS_FULL:
                gameengine.getGlobalBase('PlayerStub').doOnOthersClient(
                        [playerGBID, ], 'onMessage',
                        (RAID_CONST.datas["raid_applyAcceptFail_raidFull_msg"]["value"], []),
                        None, '', ())
            ERROR_MSG('onReplyJoinRaidLonely:: failed, {}'.format(err))
            return

        raidVal = self.raidDic[raidUUID]
        raidVal.refreshRaidCacheValToAllPlayers()

    def _onReplyJoinRaidLonely(self, srcPlayerGBID, raidUUID, playerGBID, playerProps):
        if raidUUID not in self.raidDic:
            return None, gameconst.RaidErrno.RAID_RAID_ID_NOT_FOUND

        raidVal = self.raidDic[raidUUID]
        if raidVal.raidLeaderGBID != srcPlayerGBID and not raidVal.isRaidDeputy(srcPlayerGBID):
            # NOTE: srcPlayerGBID 代表同意玩家申请时的 leaderGBID or deputyGBID, 不一定是raidVal中存放的GBID
            WARNING_MSG('_onReplyJoinRaidLonely:: leader changed when reply join raid')

        playerVal, err = raidVal.addNewMember(playerGBID, playerProps, toClient=True)
        if err != gameconst.RaidErrno.RAID_OK:
            WARNING_MSG('_onReplyJoinRaidLonely:: add member failed, {}'.format(err))
            return None, err

        return playerVal, gameconst.RaidErrno.RAID_OK

    def onTeamReplyJoinRaidWithTeam(self, srcPlayerBox, srcPlayerGBID, raidUUID, joinedPlayerGBID,
                                    error, extraProps):
        INFO_MSG('onTeamReplyJoinRaidWithTeam::', srcPlayerBox, srcPlayerGBID, raidUUID,
                  joinedPlayerGBID, error, extraProps)

        def _reject():
            _playerJoinVal, _err = self._replyJoinRaidRemove(srcPlayerBox, srcPlayerGBID, joinedPlayerGBID, raidUUID)
            if _err != gameconst.RaidErrno.RAID_OK:
                ERROR_MSG('onTeamReplyJoinRaidWithTeam:: reject failed, {}'.format(_err))
                return

            if _playerJoinVal.applyTimeoutTimerId:
                self._cancelCallback(_playerJoinVal.applyTimeoutTimerId,
                                    gametimer.TIMER_TAG_RAID_APPLY_JOIN_TIMEOUT)
                _playerJoinVal.applyTimeoutTimerId = 0

            gameengine.getGlobalBase('PlayerStub').doOnOthersCell(
                [joinedPlayerGBID, ], 'onJoinPlayerHandleReplyJoinRaidReject',
                (raidUUID, ), None, '', ())

        if error != gameconst.RaidErrno.RAID_OK:
            ERROR_MSG('onTeamReplyJoinRaidWithTeam:: failed from teamStub process, {}'.format(error))
            _reject()
            return

        playerJoinVal, err = self._replyJoinRaidCheck(srcPlayerBox, srcPlayerGBID, joinedPlayerGBID, raidUUID)
        if err != gameconst.RaidErrno.RAID_OK:
            err = err.initkvbody(source=self._replyJoinRaidCheck.__name__,
                                 raidUUID=raidUUID,
                                 playerGBID=joinedPlayerGBID)
            ERROR_MSG('onTeamReplyJoinRaidWithTeam:: failed, {}'.format(err))
            _reject()

        if playerJoinVal.isSingle():
            WARNING_MSG('onTeamReplyJoinRaidWithTeam:: change join type in call process, abort handle.', raidUUID, joinedPlayerGBID)
            return

        self._initTeamMemberJoinRecord(raidUUID, playerJoinVal.joinTeamUUID, playerJoinVal,
                                       {i: False for i in playerJoinVal.raidJoinPlayerDic})

        gbIdListIter = ((i.gbId, i.playerName) for i in playerJoinVal.raidJoinPlayerDic.values())
        for gbId, name in gbIdListIter:
            gameengine.getGlobalBase('PlayerStub').doOnOthersCell(
                [gbId, ], 'onJoinPlayerReplyJoinRaidWithTeam',
                (srcPlayerGBID, raidUUID, playerJoinVal.toSavedDict(), extraProps),
                self, 'onPlayerIsOffline', (srcPlayerGBID, name))

    def onReplyJoinRaidWithTeam(self, srcPlayerGBID, raidUUID, teamUUID, playerGBID, playerProps, extraProps):
        INFO_MSG('onReplyJoinRaidWithTeam::', srcPlayerGBID, raidUUID, teamUUID, playerGBID, playerProps, extraProps)
        memberErrno = extraProps.get('memberCheckErrno')
        memberValDic, err = self._onReplyJoinRaidWithTeam(srcPlayerGBID, raidUUID, teamUUID,
                                                          playerGBID, playerProps, memberErrno)
        if err != gameconst.RaidErrno.RAID_OK:
            if err == gameconst.RaidErrno.RAID_CHECKING_TEAM_JOIN:
                INFO_MSG('onReplyJoinRaidWithTeam:: skill checking ...')
            else:
                _i_errLog = False
                if err == gameconst.RaidErrno.RAID_ALREADY_IN_RAID:
                    gameengine.getGlobalBase('PlayerStub').doOnOthersBase(
                        [srcPlayerGBID, ], 'onMessagePre', (MMD.datas.raid_teamInvitationCheck_sectionTeam, []),
                        None, '', ())
                elif err in (gameconst.RaidErrno.RAID_RAID_IS_FULL, gameconst.RaidErrno.RAID_RAID_NOT_ENOUGH_SIT):
                    gameengine.getGlobalBase('PlayerStub').doOnOthersClient(
                        [srcPlayerGBID, ], 'onMessage',
                        (RAID_CONST.datas["raid_applyAcceptFail_raidFull_msg"]["value"], []),
                        None, '', ())
                else:
                    _i_errLog = True
                (ERROR_MSG if _i_errLog else WARNING_MSG)('onReplyJoinRaidWithTeam:: failed, {}'.format(err))
            return

        raidVal = self.raidDic[raidUUID]
        raidVal.refreshRaidCacheValToAllPlayers()

    def _onReplyJoinRaidWithTeam(self, srcPlayerGBID, raidUUID, teamUUID, playerGBID, playerProps, memberErrno):
        if memberErrno and memberErrno != gameconst.RaidErrno.RAID_OK:
            return None, memberErrno

        if not playerProps:
            self._popTeamMemberJoinRecord(raidUUID, teamUUID)
            return None, gameconst.RaidErrno.RAID_CHECKING_TEAM_JOIN_FAILED.initkvbody(source='_onReplyJoinRaidWithTeam')

        record = self._getTeamMemberJoinRecord(raidUUID, teamUUID)    # type: _RaidTeamMemberJoinRecordVal
        if not record:
            return None, gameconst.RaidErrno.UNKNOWN.initkvbody(source='_onReplyJoinRaidWithTeam',
                                                                reason='record-lost')

        if playerGBID not in record.memberCheckDic:
            return None, gameconst.RaidErrno.UNKNOWN.initkvbody(source='_onPeplyJoinRaidWithTeam',
                                                                reason='record-not-match')

        record.memberCheckDic[playerGBID] = playerProps

        if not all(record.memberCheckDic.values()):
            return None, gameconst.RaidErrno.RAID_CHECKING_TEAM_JOIN.initkvbody(source='_onReplyJoinRaidWithTeam')

        self._popTeamMemberJoinRecord(raidUUID, teamUUID)
        if raidUUID not in self.raidDic:
            return None, gameconst.RaidErrno.RAID_RAID_ID_NOT_FOUND

        # 可能超时了,所以需要在这里判断记录还在不在,在的话才允许加入
        raidVal = self.raidDic[raidUUID]
        playerJoinVal, err = raidVal.getRaidJoin(record.playerJoinVal.joinPlayerGBID)
        if err != gameconst.RaidErrno.RAID_OK:
            ERROR_MSG('_onReplyJoinRaidWithTeam:: get failed, {}'.format(err))
            return None, err

        memberValDic, err = raidVal.addNewTeamMembers(list(record.memberCheckDic.values()),
                                                      record.playerJoinVal.joinPlayerGBID, toClient=True)
        if err == gameconst.RaidErrno.RAID_OK or \
                err not in (gameconst.RaidErrno.RAID_RAID_IS_FULL, gameconst.RaidErrno.RAID_RAID_NOT_ENOUGH_SIT):
            callBackFunc = 'onJoinPlayerHandleReplyJoinRaidReject'
            if err == gameconst.RaidErrno.RAID_OK:
                callBackFunc = 'onJoinPlayerHandleReplyJoinRaidAccept'
            playerJoinVal, _ = raidVal.popRaidJoin(record.playerJoinVal.joinPlayerGBID)
            gameengine.getGlobalBase('PlayerStub').doOnOthersCell(
                [playerJoinVal.joinPlayerGBID,], callBackFunc,
                (raidUUID, ), None, '', ())
            if playerJoinVal.applyTimeoutTimerId:
                self._cancelCallback(playerJoinVal.applyTimeoutTimerId,
                                    gametimer.TIMER_TAG_RAID_APPLY_JOIN_TIMEOUT)
                playerJoinVal.applyTimeoutTimerId = 0

        return memberValDic, err

    def cancelRaidJoinRequest(self, playerBox, playerGBID, raidUUID, raidJoinType, extraProps):
        INFO_MSG("cancelRaidJoinRequest::", playerBox, playerGBID, raidUUID, raidJoinType, extraProps)
        playerJoinVal, err = self._cancelRaidJoinRequest(playerBox, playerGBID, raidUUID, raidJoinType)
        if err != gameconst.RaidErrno.RAID_OK:
            WARNING_MSG("cancelRaidJoinRequest::failed, errno={}".format(err), playerGBID, raidUUID, raidJoinType)
            return

        if playerJoinVal.applyTimeoutTimerId:
            self._cancelCallback(playerJoinVal.applyTimeoutTimerId,
                                 gametimer.TIMER_TAG_RAID_APPLY_JOIN_TIMEOUT)
            playerJoinVal.applyTimeoutTimerId = 0

        playerBox.cell.onCancelRaidJoinRequestSucc(raidUUID, raidJoinType, extraProps)

    def _cancelRaidJoinRequest(self, playerBox, playerGBID, raidUUID, raidJoinType):
        if raidUUID not in self.raidDic:
            return None, gameconst.RaidErrno.RAID_RAID_ID_NOT_FOUND

        raidVal = self.raidDic[raidUUID]
        playerJoinVal, err = raidVal.popRaidJoin(playerGBID)
        if err != gameconst.RaidErrno.RAID_OK:
            return None, err

        return playerJoinVal, gameconst.RaidErrno.RAID_OK

    def raidLeaderApplyInvitedRaid(self, srcPlayerBox, srcPlayerGBID, raidUUID,
                                   invitePlayerGBID, invitePlayerName, extraProps):
        INFO_MSG('raidLeaderApplyInvitedRaid::', srcPlayerBox, srcPlayerGBID,
                  raidUUID, invitePlayerGBID, invitePlayerName, extraProps)

        def _check():
            if raidUUID not in self.raidDic:
                return None, gameconst.RaidErrno.RAID_RAID_ID_NOT_FOUND

            raidVal = self.raidDic[raidUUID]
            if raidVal.raidLeaderGBID != srcPlayerGBID:
                return None, gameconst.RaidErrno.RAID_NOT_RAID_LEADER

            if raidVal.isRaidFull():
                return None, gameconst.RaidErrno.RAID_RAID_IS_FULL

            return raidVal, gameconst.RaidErrno.RAID_OK

        raidVal, err = _check()
        if err != gameconst.RaidErrno.RAID_OK:
            ERROR_MSG('raidLeaderApplyInvitedRaid:: check failed, {}'.format(err))
            if err == gameconst.RaidErrno.RAID_RAID_IS_FULL:
                srcPlayerBox.onMessagePre(RAID_CONST.datas["raid_inviteFail_raidFull_msg"]["value"], [])
            return

        joinVal, _ = raidVal.getRaidJoin(playerGBID=invitePlayerGBID)
        if joinVal:
            # 对于已经在申请列表中的玩家直接入团
            if joinVal.isSingle():
                INFO_MSG('raidLeaderInvitedRaidLonely:: auto apply invite if in joinDic: single')
                self.doReplyJoinRaidLonely(srcPlayerBox, srcPlayerGBID, raidUUID, invitePlayerGBID, extraProps)
            elif joinVal.isTeam():
                INFO_MSG('raidLeaderApplyInvitedRaid:: auto apply invite if in joinDic: team')
                self.doReplyJoinRaidWithTeam(srcPlayerBox, srcPlayerGBID, raidUUID,
                                             invitePlayerGBID, extraProps)
            else:
                ERROR_MSG('raidLeaderApplyInvitedRaid:: unknown joinValType', joinVal.raidJoinType)
            return
        raidVal = self.raidDic[raidUUID]
        leaderVal = raidVal.getRaidLeader()
        raidTarget = raidVal.raidTarget
        _teamUUID = extraProps.get('teamUUID')
        if _teamUUID:
            gameengine.getTeamStub(_teamUUID).raidApplyInvitedRaid(raidTarget,
                srcPlayerBox, srcPlayerGBID, raidUUID, leaderVal.playerName,
                leaderVal.playerGbId, leaderVal.playerName,
                invitePlayerGBID, invitePlayerName, _teamUUID, extraProps)
            return

        gameengine.getGlobalBase('PlayerStub').doOnOthersCell(
            [invitePlayerGBID], 'invitedPlayerOnApplyInvitedRaid',
            (raidUUID, raidTarget, leaderVal.playerGbId, leaderVal.playerName,
             leaderVal.playerName, extraProps), self, 'onPlayerIsOffline', (srcPlayerGBID, invitePlayerName))

    def raidDeputyApplyInvitedRaid(self, srcPlayerBox, srcPlayerGBID, raidUUID,
                                   invitePlayerGBID, invitePlayerName, extraProps):
        INFO_MSG('raidDeputyApplyInvitedRaid::', srcPlayerBox, srcPlayerGBID,
                  raidUUID, invitePlayerGBID, invitePlayerName, extraProps)

        def _check():
            if raidUUID not in self.raidDic:
                return None, gameconst.RaidErrno.RAID_RAID_ID_NOT_FOUND

            raidVal = self.raidDic[raidUUID]
            if not raidVal.isRaidDeputy(srcPlayerGBID):
                return None, gameconst.RaidErrno.RAID_NOT_RAID_DEPUTY

            if raidVal.isRaidFull():
                return None, gameconst.RaidErrno.RAID_RAID_IS_FULL

            return raidVal, gameconst.RaidErrno.RAID_OK

        raidVal, err = _check()
        if err != gameconst.RaidErrno.RAID_OK:
            ERROR_MSG('raidDeputyApplyInvitedRaid:: check failed, {}'.format(err))
            if err == gameconst.RaidErrno.RAID_RAID_IS_FULL:
                srcPlayerBox.onMessagePre(RAID_CONST.datas["raid_inviteFail_raidFull_msg"]["value"], [])
            return

        joinVal, _ = raidVal.getRaidJoin(playerGBID=invitePlayerGBID)
        if joinVal:
            # 对于已经在申请列表中的玩家直接入团
            if joinVal.isSingle():
                INFO_MSG('raidDeputyInvitedRaidLonely:: auto apply invite if in joinDic: single')
                self.doReplyJoinRaidLonely(srcPlayerBox, srcPlayerGBID, raidUUID, invitePlayerGBID, extraProps)
            elif joinVal.isTeam():
                INFO_MSG('raidDeputyApplyInvitedRaid:: auto apply invite if in joinDic: team')
                self.doReplyJoinRaidWithTeam(srcPlayerBox, srcPlayerGBID, raidUUID,
                                             invitePlayerGBID, extraProps)
            else:
                ERROR_MSG('raidDeputyApplyInvitedRaid:: unknown joinValType', joinVal.raidJoinType)
            return

        raidDeputyVal = raidVal.getRaidDeputy()
        raidLeaderVal = raidVal.getRaidLeader()
        raidTarget = raidVal.raidTarget
        _teamUUID = extraProps.get('teamUUID')
        if _teamUUID:
            gameengine.getTeamStub(_teamUUID).raidApplyInvitedRaid(raidTarget,
                srcPlayerBox, srcPlayerGBID, raidUUID, raidDeputyVal.playerName,
                raidLeaderVal.playerGbId, raidLeaderVal.playerName,
                invitePlayerGBID, invitePlayerName, _teamUUID, extraProps)
            return

        gameengine.getGlobalBase('PlayerStub').doOnOthersCell(
            [invitePlayerGBID], 'invitedPlayerOnApplyInvitedRaid',
            (raidUUID, raidTarget, raidDeputyVal.playerGbId, raidDeputyVal.playerName,
             raidLeaderVal.playerName, extraProps), self, 'onPlayerIsOffline', (srcPlayerGBID, invitePlayerName))
    #
    def raidCaptainApplyInvitedRaid(self, srcPlayerBox, srcPlayerGBID, raidUUID, raidTeamIDX,
                                    invitePlayerGBID, invitePlayerName, extraProps):
        INFO_MSG('raidCaptainApplyInvitedRaid::', srcPlayerBox, srcPlayerGBID,
                  raidUUID, invitePlayerGBID, invitePlayerName, extraProps)

        raidVal = teamVal = None

        def _check():
            nonlocal raidVal, teamVal

            if raidUUID not in self.raidDic:
                return None, gameconst.RaidErrno.RAID_RAID_ID_NOT_FOUND

            raidVal = self.raidDic[raidUUID]
            if raidTeamIDX not in raidVal.raidTeamDic:
                return None, gameconst.RaidErrno.RAID_TEAM_NOT_FOUND

            teamVal = raidVal.raidTeamDic[raidTeamIDX]
            if srcPlayerGBID != teamVal.teamCaptainGBID:
                return None, gameconst.RaidErrno.RAID_NOT_TEAM_CAPTAIN

            return None, gameconst.RaidErrno.RAID_OK

        _, err = _check()
        if err != gameconst.RaidErrno.RAID_OK:
            ERROR_MSG('raidCaptainApplyInvitedRaid:: check failed, {}'.format(err))
            return

        captainVal = teamVal.teamPlayerDic[srcPlayerGBID]
        raidVal = self.raidDic[raidUUID]
        leaderVal = raidVal.getRaidLeader()
        raidTarget = raidVal.raidTarget
        _teamUUID = extraProps.get('teamUUID')
        if _teamUUID:
            gameengine.getTeamStub(_teamUUID).raidApplyInvitedRaid(raidTarget,
                srcPlayerBox, srcPlayerGBID, raidUUID, captainVal.playerName,
                leaderVal.playerGbId, leaderVal.playerName,
                invitePlayerGBID, invitePlayerName, _teamUUID, extraProps)
            return

        gameengine.getGlobalBase('PlayerStub').doOnOthersCell(
            [invitePlayerGBID], 'invitedPlayerOnApplyInvitedRaid',
            (raidUUID, raidTarget, captainVal.playerGbId, captainVal.playerName,
             leaderVal.playerName, extraProps), self, 'onPlayerIsOffline', (srcPlayerGBID, invitePlayerName))

    def raidMemberApplyInvitedRaid(self, srcPlayerBox, srcPlayerGBID, raidUUID,
                                   invitePlayerGBID, invitePlayerName, extraProps):
        INFO_MSG('raidMemberApplyInvitedRaid::', srcPlayerBox, srcPlayerGBID,
                  raidUUID, invitePlayerGBID, invitePlayerName, extraProps)

        playerVal = None

        def _check():
            nonlocal playerVal

            if raidUUID not in self.raidDic:
                return None, gameconst.RaidErrno.RAID_RAID_ID_NOT_FOUND

            raidVal = self.raidDic[raidUUID]
            raidTeamIDX = raidVal.getRaidTeamIDX(srcPlayerGBID)
            if not raidTeamIDX:
                return None, gameconst.RaidErrno.RAID_TEAM_NOT_FOUND

            teamVal = raidVal.raidTeamDic[raidTeamIDX]
            playerVal = teamVal.teamPlayerDic[srcPlayerGBID]

            return playerVal, gameconst.RaidErrno.RAID_OK

        raidPlayerVal, err = _check()
        if err != gameconst.RaidErrno.RAID_OK:
            ERROR_MSG('raidMemberApplyInvitedRaid:: failed, {}'.format(err))
            return
        raidVal = self.raidDic[raidUUID]
        leaderVal = raidVal.getRaidLeader()
        raidTarget = raidVal.raidTarget
        _teamUUID = extraProps.get('teamUUID')
        if _teamUUID:
            gameengine.getTeamStub(_teamUUID).raidApplyInvitedRaid(raidTarget,
                srcPlayerBox, srcPlayerGBID, raidUUID, playerVal.playerName,
                leaderVal.playerGbId, leaderVal.playerName,
                invitePlayerGBID, invitePlayerName, _teamUUID, extraProps)
            return

        gameengine.getGlobalBase('PlayerStub').doOnOthersCell(
            [invitePlayerGBID], 'invitedPlayerOnApplyInvitedRaid',
            (raidUUID, raidTarget, playerVal.playerGbId, playerVal.playerName,
             leaderVal.playerName, extraProps), self, 'onPlayerIsOffline', (srcPlayerGBID, invitePlayerName))

    def replyInviteRaidLonely(self, invitedPlayerBox, invitedPlayerGBID, invitedPlayerProps,
                              srcPlayerGBID, srcPlayerTeamIDX, raidUUID, extraProps):
        INFO_MSG('replyInviteRaidLonely::', invitedPlayerBox, invitedPlayerGBID,
                  srcPlayerGBID, srcPlayerTeamIDX, raidUUID, invitedPlayerProps, extraProps)
        _, err = self._replyInviteRaidLonely(invitedPlayerBox, invitedPlayerGBID, invitedPlayerProps,
                                             srcPlayerGBID, srcPlayerTeamIDX, raidUUID)
        if err != gameconst.RaidErrno.RAID_OK:
            if err == gameconst.RaidErrno.RAID_INVITE_TO_JOIN:
                INFO_MSG('replyInviteRaidLonely:: invite to join, {}'.format(err))
            elif err == gameconst.RaidErrno.RAID_RAID_TEAM_IS_FULL:
                WARNING_MSG('replyInviteRaidLonely:: target raid team is full, {}'.format(err))
                invitedPlayerBox and invitedPlayerBox.onMessagePre(RAID_CONST.datas["raidInviteFail_partyFull"]["value"], [])
            elif err == gameconst.RaidErrno.RAID_RAID_IS_FULL:
                WARNING_MSG('replyInviteRaidLonely:: target raid is full, {}'.format(err))
                invitedPlayerBox and invitedPlayerBox.onMessagePre(RAID_CONST.datas["raid_joinFail_spaceless_msg"]["value"], [])
            else:
                ERROR_MSG('replyInviteRaidLonely:: failed, {}'.format(err))
            return

        raidVal = self.raidDic[raidUUID]
        raidVal.refreshRaidCacheValToAllPlayers()

    def _replyInviteRaidLonely(self, invitedPlayerBox, invitedPlayerGBID, invitedPlayerProps,
                               srcPlayerGBID, srcPlayerTeamIDX, raidUUID):
        def _precheck():
            if raidUUID not in self.raidDic:
                return None, gameconst.RaidErrno.RAID_RAID_ID_NOT_FOUND

            _raidVal = self.raidDic[raidUUID]
            if _raidVal.isRaidFull():
                return None, gameconst.RaidErrno.RAID_RAID_IS_FULL

            return _raidVal, gameconst.RaidErrno.RAID_OK

        raidVal, err = _precheck()
        if err != gameconst.RaidErrno.RAID_OK:
            return None, err.initkvbody(source='_replyInviteRaidLonely._precheck')

        # CASE1: 邀请者为小队队长, 存在特定邀请teamIDX, 其他team不能加入,
        #        如果在接受邀请期间小队队长变更(不是队长/队长变更为其他小队队长等),
        #        该邀请确认请求亦会失败.
        '''
        # 没有小队长了,这个暂时不考虑了
        if srcPlayerTeamIDX:
            raidTeamIDX = raidVal.getRaidTeamIDX(srcPlayerGBID)
            if not raidTeamIDX:
                return None, gameconst.RaidErrno.RAID_TEAM_IDX_NOT_FOUND
            elif raidTeamIDX != srcPlayerTeamIDX:
                return None, gameconst.RaidErrno.RAID_TEAM_IDX_CHANGED.initkvbody(
                    srcRaidTeamIDX=srcPlayerTeamIDX, crtRaidTeamIDX=raidTeamIDX,
                    source='_replyInviteRaidLonely')

            raidTeamVal = raidVal.raidTeamDic[raidTeamIDX]
            if srcPlayerGBID != raidTeamVal.teamCaptainGBID:
                return None, gameconst.RaidErrno.RAID_NOT_TEAM_CAPTAIN

            if raidTeamVal.isRaidFull():
                return None, gameconst.RaidErrno.RAID_RAID_TEAM_IS_FULL.initkvbody(
                    raidUUID=raidUUID, raidTeamIDX=raidTeamIDX, source='_replyInviteRaidLonely')

            playerVal, err = raidTeamVal.addTeamMember(invitedPlayerGBID, invitedPlayerProps)
            playerVal.playerBox and playerVal.playerBox.client.onGetRaidData(raidVal.toClientData())
            raidVal.broadcastAllRaidMembersClient(
                'onAddNewRaidMember', (raidUUID, raidTeamIDX, invitedPlayerGBID,
                                       playerVal.toClientData()),
                exclude=(invitedPlayerGBID, ))

            if err != gameconst.RaidErrno.RAID_OK:
                return None, err.initkvbody(source='_replyInviteRaidLonely')

            return None, gameconst.RaidErrno.RAID_OK
        '''

        # CASE2: 其他情况, 可能是团长或者副团长邀请
        if srcPlayerGBID == raidVal.raidLeaderGBID or raidVal.isRaidDeputy(srcPlayerGBID):
            # CASE2.1: 如果邀请发起方是团、副团长, 则直接加入
            playerVal, err = raidVal.addNewMember(invitedPlayerGBID, invitedPlayerProps, toClient=True)
            if err != gameconst.RaidErrno.RAID_OK:
                return None, err.initkvbody(source='_replyInviteRaidLonely')

            return None, gameconst.RaidErrno.RAID_OK

        # CASE2.2(DEFAULT): 其他情况, 发起方是普通小队成员, 则向团长发起申请
        joinExtraProps = {}
        self.applyJoinRaidLonely(invitedPlayerBox, invitedPlayerGBID, invitedPlayerProps, raidUUID, joinExtraProps, '', True, gameconst.ApplySource.RECRUIT)
        return None, gameconst.RaidErrno.RAID_INVITE_TO_JOIN

    def replyInviteRaidWithTeam(self, invitedPlayerBox, invitedPlayerGBID, raidUUID, recordID,
                                teamUUID, teamMemberNum, playerProps, isCaptain, srcPlayerGBID, extraProps):
        INFO_MSG('replyInviteRaidWithTeam::', invitedPlayerBox, invitedPlayerGBID, raidUUID, recordID,
                  teamUUID, isCaptain, teamMemberNum, playerProps, srcPlayerGBID, extraProps)
        memberValDic, err = self._replyInviteRaidWithTeamDirectly(invitedPlayerBox, invitedPlayerGBID, raidUUID,
                                                                  recordID, teamUUID, teamMemberNum, playerProps,
                                                                  srcPlayerGBID, isCaptain)
        if err != gameconst.RaidErrno.RAID_OK:
            if err == gameconst.RaidErrno.RAID_CHECKING_TEAM_INVITE:
                INFO_MSG('replyInviteRaidWithTeam:: skill checking...')
            elif err == gameconst.RaidErrno.RAID_INVITE_TO_JOIN:
                INFO_MSG('replyInviteRaidWithTeam:: invite to join, {}'.format(err))
            elif err == gameconst.RaidErrno.RAID_ERR_IGNORE:
                INFO_MSG('replyInviteRaidWithTeam:: ignored, {}'.format(err))
            else:
                if err in (gameconst.RaidErrno.RAID_RAID_IS_FULL, gameconst.RaidErrno.RAID_RAID_NOT_ENOUGH_SIT):
                    # TODO()(RAID_INFO): mock message
                    # 邀请者弹窗
                    # gameengine.getGlobalBase('PlayerStub').doOnOthersClient(
                    #     [srcPlayerGBID, ], 'onMessage',
                    #     (MMD.datas.CUSTOM_STRING6, ['团队中没有足够空间容纳该队伍']),
                    #     None, '', ())
                    # 被邀请者弹窗
                    invitedPlayerBox.onMessagePre(RAID_CONST.datas["raid_joinFail_spaceless_msg"]["value"], [])
                    pass
                ERROR_MSG('replyInviteRaidWithTeam::  failed, {}'.format(err))
            return

        raidVal = self.raidDic[raidUUID]
        raidVal.refreshRaidCacheValToAllPlayers()

    def _replyInviteRaidWithTeamDirectly(self, invitedPlayerBox, invitedPlayerGBID, raidUUID, recordID,
                                         teamUUID, teamMemberNum, playerProps, srcPlayerGBID, isCaptain):
        if raidUUID not in self.raidDic:
            return None, gameconst.RaidErrno.RAID_RAID_ID_NOT_FOUND

        raidVal = self.raidDic[raidUUID]
        if raidVal.isRaidFull():
            return None, gameconst.RaidErrno.RAID_RAID_IS_FULL

        # CASE1: 邀请者不是团队Leader; 如果调用来源是队长, 则将该队伍转到申请列表(绕过队员check)
        if srcPlayerGBID != raidVal.raidLeaderGBID:
            if isCaptain:
                gameengine.getTeamStub(teamUUID).applyJoinRaidWithTeam(
                    invitedPlayerBox, invitedPlayerGBID, teamUUID, raidUUID, {})
                return None, gameconst.RaidErrno.RAID_INVITE_TO_JOIN
            return None, gameconst.RaidErrno.RAID_ERR_IGNORE.initkvbody(reason='invited-src-is-member')

        # CASE2: 邀请者是团长, check所有团员, 然后将团员入队
        invitedCheckCache = self._initTeamMemberInviteRecord(raidUUID, teamUUID, recordID, teamMemberNum, {})
        if isCaptain:
            invitedCheckCache.captainGBID = invitedPlayerGBID
        invitedCheckCache.memberCheckDic[invitedPlayerGBID] = playerProps
        if not invitedCheckCache.isAllChecked():
            # CASE2.1: 没有全部check, 等待
            return None, gameconst.RaidErrno.RAID_CHECKING_TEAM_INVITE

        # CASE2.2: 全部check, 尝试加入团队
        if not all(invitedCheckCache.memberCheckDic.values()):
            return None, gameconst.RaidErrno.RAID_CHECKING_TEAM_INVITE_FAILED

        self._popTeamMemberInviteRecord(raidUUID, teamUUID, recordID)
        memberValDic, err = raidVal.addNewTeamMembers(list(invitedCheckCache.memberCheckDic.values()),
                                                      invitedCheckCache.captainGBID, toClient=True)
        if err != gameconst.RaidErrno.RAID_OK:
            return memberValDic, err.initkvbody(source='_replyInviteRaidWithTeamDirectly.addNewTeamMembers')

        return memberValDic, err

    def leaveRaid(self, leavePlayerBox, leavePlayerGBID, raidUUID, extraProps):
        INFO_MSG('leaveRaid::', leavePlayerBox, leavePlayerGBID, raidUUID, extraProps)
        if raidUUID not in self.raidDic:
            return
        
        raidVal = self.raidDic[raidUUID]
        raidMemberVal, err = self._raidMemberLeaveRaid(raidUUID, leavePlayerGBID)
        if err != gameconst.RaidErrno.RAID_OK:
            ERROR_MSG('leaveRaid:: failed, {}'.format(err))
            return
        # 通知客户端，谁走了
        raidVal.broadcastAllRaidMembersBase('onMessagePre', (MMD.datas.raid_playerLeft, [raidMemberVal.playerName]))

        # 最后一个人离开
        if raidVal.isEmpty():
            self.doDisbandRaid(raidUUID, extraProps)
            leavePlayerBox and leavePlayerBox.onMessagePre(RAID_CONST.datas["raidDismissedMsg"]["value"], [])
            raidVal.clearRaidCacheValToAllPlayers()
        # 剩余都下线了
        elif raidVal.isAllMembersOffline():
            self.doDisbandRaid(raidUUID, extraProps)
            raidVal.clearRaidCacheValToAllPlayers()
        # 离开之后，还有人
        else:
            raidVal.refreshRaidCacheValToAllPlayers(exclude=(leavePlayerGBID,))
        # 自己走离开逻辑
        ret = extraProps.get('leaveDungen', False)
        if not ret and self.checkInDungeon(raidVal.raidUUID):
            leavePlayerBox.cell.leaveRaidDungeon()
        else:
            leavePlayerBox.cell.onLeaveRaid(raidUUID, extraProps)

    def _raidMemberLeaveRaid(self, raidUUID, memberGBID, teamIDX=0):
        """通过离队方法"""
        INFO_MSG('_raidMemberLeaveRaid::', raidUUID, memberGBID)
        if raidUUID not in self.raidDic:
            return None, gameconst.RaidErrno.RAID_RAID_ID_NOT_FOUND

        raidVal = self.raidDic[raidUUID]
        teamIDX = teamIDX or raidVal.getRaidTeamIDX(memberGBID)
        if not teamIDX:
            return None, gameconst.RaidErrno.RAID_TEAM_IDX_NOT_FOUND

        self.onTransfer(memberGBID, teamIDX, raidVal, False)

        teamIDX = raidVal.getRaidTeamIDX(memberGBID)
        raidMemberVal, err = raidVal.popMember(teamIDX, memberGBID, toClient=True)
        if err != gameconst.RaidErrno.RAID_OK:
            return None, err.initkvbody(source='_raidMemberLeaveRaid::raidVal.popMember',
                                        raidUUID=raidUUID)()

        return raidMemberVal, gameconst.RaidErrno.RAID_OK

    def raidLeaderKickOutRaidMember(self, srcPlayerBox, srcPlayerGBID, raidUUID,
                                    rmPlayerRaidTeamIDX, rmPlayerGBID, extraProps):
        INFO_MSG('raidLeaderKickOutRaidMember::', srcPlayerBox, srcPlayerGBID,
                  raidUUID, rmPlayerRaidTeamIDX, rmPlayerGBID, extraProps)

        raidVal = None  # type: raid.RaidVal

        def _check():
            nonlocal raidVal
            if srcPlayerGBID == rmPlayerGBID:
                return None, gameconst.RaidErrno.RAID_KICKOUT_SELF.initkvbody(
                    source='raidLeaderKickOutRaidMember._check',
                    raidUUID=raidUUID,
                    srcPlayerGBID=srcPlayerGBID,
                    rmPlayerGBID=rmPlayerGBID)
            if raidUUID not in self.raidDic:
                return None, gameconst.RaidErrno.RAID_RAID_ID_NOT_FOUND.initkvbody(
                    source='raidLeaderKickOutRaidMember._check',
                    raidUUID=raidUUID)
            raidVal = self.raidDic[raidUUID]
            if raidVal.raidLeaderGBID != srcPlayerGBID:
                return None, gameconst.RaidErrno.RAID_NOT_RAID_LEADER.initkvbody(
                    source='raidLeaderKickOutRaidMember._check',
                    raidUUID=raidUUID,
                    srcPlayerGBID=srcPlayerGBID,
                    raidLeaderGBID=raidVal.raidLeaderGBID)
            _rmTeamIDX = raidVal.getRaidTeamIDX(rmPlayerGBID)
            if not _rmTeamIDX or _rmTeamIDX != rmPlayerRaidTeamIDX:
                return None, gameconst.RaidErrno.RAID_TEAM_IDX_CHANGED.initkvbody(
                    source='raidLeaderKickOutRaidMember._check',
                    raidUUID=raidUUID,
                    rmPlayerRaidTeamIDX=rmPlayerRaidTeamIDX,
                    crtPlayerRaidTeamIDX=_rmTeamIDX)
            return None, gameconst.RaidErrno.RAID_OK

        _, err = _check()
        if err != gameconst.RaidErrno.RAID_OK:
            ERROR_MSG('raidLeaderKickOutRaidMember:: _check failed, {}'.format(err))
            return

        memberVal, err = self._raidMemberLeaveRaid(raidUUID, rmPlayerGBID, rmPlayerRaidTeamIDX)
        if err != gameconst.RaidErrno.RAID_OK:
            ERROR_MSG('raidLeaderKickOutRaidMember:: popMember failed, {}'.format(err))
            return

        leaderVal = raidVal.getRaidLeader()
        memberVal.playerBox and memberVal.playerBox.onMessagePre(RAID_CONST.datas["raid_kicked_msg"]["value"], [leaderVal.playerName or ''])
        raidVal.broadcastAllRaidMembersBase('onMessagePre', (RAID_CONST.datas["raid_kickDone_msg"]["value"], [memberVal.playerName]))
        raidVal.broadcastAllRaidMembersBase('onMessagePre', (MMD.datas.raid_playerKicked, [memberVal.playerName]))

        raidVal.refreshRaidCacheValToAllPlayers()
        memberVal.playerBox and memberVal.playerBox.cell.onBeKickedOutRaidByRaidLeader(raidUUID, extraProps)
        srcPlayerBox.cell.onRaidLeaderKickOutRaidMember(raidUUID, rmPlayerRaidTeamIDX,
                                                        rmPlayerGBID, extraProps)

    def raidDeputyKickOutRaidMember(self, srcPlayerBox, srcPlayerGBID, raidUUID,
                                    rmPlayerRaidTeamIDX, rmPlayerGBID, extraProps):
        INFO_MSG('raidDeputyKickOutRaidMember::', srcPlayerBox, srcPlayerGBID,
                  raidUUID, rmPlayerRaidTeamIDX, rmPlayerGBID, extraProps)

        raidVal = None  # type: raid.RaidVal

        def _check():
            nonlocal raidVal
            if srcPlayerGBID == rmPlayerGBID:
                return None, gameconst.RaidErrno.RAID_KICKOUT_SELF.initkvbody(
                    source='raidDeputyKickOutRaidMember._check',
                    raidUUID=raidUUID,
                    srcPlayerGBID=srcPlayerGBID,
                    rmPlayerGBID=rmPlayerGBID)
            if raidUUID not in self.raidDic:
                return None, gameconst.RaidErrno.RAID_RAID_ID_NOT_FOUND.initkvbody(
                    source='raidDeputyKickOutRaidMember._check',
                    raidUUID=raidUUID)
            raidVal = self.raidDic[raidUUID]
            if not raidVal.isRaidDeputy(srcPlayerGBID):
                return None, gameconst.RaidErrno.RAID_NOT_RAID_DEPUTY.initkvbody(
                    source='raidDeputyKickOutRaidMember._check',
                    raidUUID=raidUUID,
                    srcPlayerGBID=srcPlayerGBID,
                    raidLeaderGBID=raidVal.raidLeaderGBID)
            if raidVal.raidLeaderGBID == rmPlayerGBID:
                return None, gameconst.RaidErrno.RAID_NOT_RAID_CANNOT_KICK_LEADER.initkvbody(
                    source='raidDeputyKickOutRaidMember._check',
                    raidUUID=raidUUID,
                    srcPlayerGBID=srcPlayerGBID,
                    raidLeaderGBID=raidVal.raidLeaderGBID)
            _rmTeamIDX = raidVal.getRaidTeamIDX(rmPlayerGBID)
            if not _rmTeamIDX or _rmTeamIDX != rmPlayerRaidTeamIDX:
                return None, gameconst.RaidErrno.RAID_TEAM_IDX_NOT_FOUND.initkvbody(
                    source='raidDeputyKickOutRaidMember._check',
                    raidUUID=raidUUID,
                    rmPlayerRaidTeamIDX=rmPlayerRaidTeamIDX,
                    crtPlayerRaidTeamIDX=_rmTeamIDX)
            return None, gameconst.RaidErrno.RAID_OK

        _, err = _check()
        if err != gameconst.RaidErrno.RAID_OK:
            ERROR_MSG('raidDeputyKickOutRaidMember:: _check failed, {}'.format(err))
            return

        memberVal, err = self._raidMemberLeaveRaid(raidUUID, rmPlayerGBID, rmPlayerRaidTeamIDX)
        if err != gameconst.RaidErrno.RAID_OK:
            ERROR_MSG('raidDeputyKickOutRaidMember:: popMember failed, {}'.format(err))
            return

        deputyVal = raidVal.getRaidDeputy()
        memberVal.playerBox and memberVal.playerBox.onMessagePre(RAID_CONST.datas["raid_kicked_msg"]["value"], [deputyVal.playerName or ''])
        raidVal.broadcastAllRaidMembersBase('onMessagePre', (RAID_CONST.datas["raid_kickDone_msg"]["value"], [memberVal.playerName]))
        raidVal.broadcastAllRaidMembersBase('onMessagePre', (MMD.datas.raid_playerKicked, [memberVal.playerName]))

        raidVal.refreshRaidCacheValToAllPlayers()
        memberVal.playerBox and memberVal.playerBox.cell.onBeKickedOutRaidByRaidDeputy(raidUUID, extraProps)
        srcPlayerBox.cell.onRaidDeputyKickOutRaidMember(raidUUID, rmPlayerRaidTeamIDX,
                                                        rmPlayerGBID, extraProps)
    #
    def raidTeamCaptainKickOutRaidMember(self, srcPlayerBox, srcPlayerGBID, raidUUID,
                                         rmPlayerRaidTeamIDX, rmPlayerGBID, extraProps):
        INFO_MSG('raidTeamCaptainKickOutRaidMember::', srcPlayerBox, srcPlayerGBID,
                  raidUUID, rmPlayerRaidTeamIDX, rmPlayerGBID, extraProps)

        raidVal = None
        raidCaptainVal = None   # type: raid.RaidTeamMemberVal

        def _check():
            nonlocal raidVal, raidCaptainVal
            if srcPlayerGBID == rmPlayerGBID:
                return None, gameconst.RaidErrno.RAID_KICKOUT_SELF.initkvbody(
                    source='raidTeamCaptainKickOutRaidMember._check',
                    raidUUID=raidUUID,
                    srcPlayerGBID=srcPlayerGBID,
                    rmPlayerGBID=rmPlayerGBID)
            if raidUUID not in self.raidDic:
                return None, gameconst.RaidErrno.RAID_RAID_ID_NOT_FOUND.initkvbody(
                    source='raidTeamCaptainKickOutRaidMember._check',
                    raidUUID=raidUUID)
            raidVal = self.raidDic[raidUUID]
            if rmPlayerRaidTeamIDX not in raidVal.raidTeamDic:
                return None, gameconst.RaidErrno.RAID_TEAM_IDX_NOT_FOUND.initkvbody(
                    source='raidTeamCaptainKickOutRaidMember._check',
                    raidUUID=raidUUID,
                    teamIDX=rmPlayerRaidTeamIDX,
                    rmPlayerGBID=rmPlayerGBID)
            _raidTeamVal = raidVal.raidTeamDic[rmPlayerRaidTeamIDX]
            if srcPlayerGBID != _raidTeamVal.teamCaptainGBID:
                return None, gameconst.RaidErrno.RAID_NOT_TEAM_CAPTAIN.initkvbody(
                    source='raidTeamCaptainKickOutRaidMember._check',
                    raidUUID=raidUUID,
                    teamCaptainGBID=_raidTeamVal.teamCaptainGBID,
                    srcPlayerGBID=srcPlayerGBID)
            if rmPlayerGBID not in _raidTeamVal.teamPlayerDic:
                return None, gameconst.RaidErrno.RAID_NOT_IN_TEAM.initkvbody(
                    source='raidTeamCaptainKickOutRaidMember._check',
                    raidUUID=raidUUID,
                    teamIDX=rmPlayerRaidTeamIDX,
                    rmPlayerGBID=rmPlayerGBID)

            raidCaptainVal = _raidTeamVal.teamPlayerDic[srcPlayerGBID]
            return None, gameconst.RaidErrno.RAID_OK

        _, err = _check()
        if err != gameconst.RaidErrno.RAID_OK:
            ERROR_MSG('raidTeamCaptainKickOutRaidMember:: _check failed, {}'.format(err))
            return

        memberVal, err = self._raidMemberLeaveRaid(raidUUID, rmPlayerGBID, rmPlayerRaidTeamIDX)
        if err != gameconst.RaidErrno.RAID_OK:
            ERROR_MSG('raidTeamCaptainKickOutRaidMember:: popMember failed, {}'.format(err))
            return

        memberVal.playerBox and memberVal.playerBox.onMessagePre(RAID_CONST.datas["raid_kicked_msg"]["value"], [raidCaptainVal.playerName])
        raidVal.broadcastAllRaidMembersBase('onMessagePre', (RAID_CONST.datas["raid_kickDone_msg"]["value"], [memberVal.playerName]))
        raidVal.broadcastAllRaidMembersBase('onMessagePre', (MMD.datas.raid_playerKicked, [memberVal.playerName]))

        raidVal.refreshRaidCacheValToAllPlayers()
        memberVal.playerBox and memberVal.playerBox.cell.onBeKickedOutRaidByRaidTeamCaptain(raidUUID, extraProps)
        srcPlayerBox.cell.onRaidTeamCaptainKickOutRaidMember(raidUUID, rmPlayerRaidTeamIDX,
                                                             rmPlayerGBID, extraProps)

    def transferRaidLeader(self, srcPlayerBox, srcPlayerGBID, raidUUID, toPlayerGBID, extraProps, broadcast):
        INFO_MSG('transferRaidLeader::', srcPlayerBox, srcPlayerGBID, raidUUID, toPlayerGBID, extraProps)
        _err = self._transferRaidDeputyCheck(srcPlayerGBID, toPlayerGBID, raidUUID)
        if _err == gameconst.RaidErrno.RAID_OK:
            self.transferRaidDeputy(srcPlayerBox, srcPlayerGBID, raidUUID, 0, extraProps, True, False)
        raidVal, orgRaidLeaderGBID, err = self._transferRaidLeader(srcPlayerBox, srcPlayerGBID, raidUUID, toPlayerGBID)
        if err != gameconst.RaidErrno.RAID_OK:
            ERROR_MSG('transferRaidLeader:: failed, {}'.format(err))
            return

        orgRaidLeaderTeamIDX = raidVal.getRaidTeamIDX(orgRaidLeaderGBID)
        orgRaidLeaderVal = raidVal.raidTeamDic[orgRaidLeaderTeamIDX].teamPlayerDic[orgRaidLeaderGBID]
        raidLeaderVal = raidVal.getRaidLeader()

        fn = 'onTransferRaidLeaderAllMemberNotify'
        args = (raidUUID, orgRaidLeaderGBID, raidVal.raidLeaderGBID, raidVal.raidLeaderTeamIDX, extraProps)

        raidVal.broadcastAllRaidMembersCell(fn, args)

        self.moveRaidTeamMember(raidLeaderVal.playerBox, raidLeaderVal.playerGbId, raidUUID,
                                raidVal.getRaidTeamIDX(raidLeaderVal.playerGbId), raidLeaderVal.playerGbId,
                                orgRaidLeaderTeamIDX, orgRaidLeaderGBID, extraProps)

        if raidVal.leaderClientDeathTimer > 0:
            self._cancelCallback(raidVal.leaderClientDeathTimer, gametimer.TIMER_TAG_LEADER_CLIENT_DEATH)
            raidVal.leaderClientDeathTimer = 0
        if not raidLeaderVal.bOnline:
            raidVal.leaderClientDeathTimer = self._callback(RAID_CONST.datas["raid_RLDownGradeOfflineTime"]["value"], '_onLeaderClientDeath', (raidUUID, raidLeaderVal.playerGbId, ), gametimer.TIMER_TAG_LEADER_CLIENT_DEATH)

        # client message
        if raidLeaderVal.playerBox:
            raidLeaderVal.playerBox.onMessagePre(RAID_CONST.datas["raid_appointedRL_msg"]["value"], [orgRaidLeaderVal.playerName, ])
            self.getRaidApplyJoinDic(raidLeaderVal.playerBox, raidLeaderVal.playerGbId, raidUUID)

        if broadcast:
            exclude = (toPlayerGBID, )
        else:
            exclude = (toPlayerGBID, srcPlayerGBID)
        raidVal.broadcastAllRaidMembersBase('onMessagePre', (RAID_CONST.datas["raid_appointRLDone_msg"]["value"], [raidLeaderVal.playerName]),
                                            exclude=exclude)

    def _transferRaidDeputyCheck(self, srcPlayerGBID, toPlayerGBID, raidUUID):
        if raidUUID not in self.raidDic:
            return gameconst.RaidErrno.RAID_RAID_ID_NOT_FOUND

        raidVal = self.raidDic[raidUUID]
        if srcPlayerGBID != raidVal.raidLeaderGBID:
            return gameconst.RaidErrno.RAID_RAID_LEADER_CHANGED

        if not raidVal.isRaidDeputy(toPlayerGBID):
            return gameconst.RaidErrno.RAID_NOT_RAID_DEPUTY

        return gameconst.RaidErrno.RAID_OK

    def _transferRaidLeader(self, srcPlayerBox, srcPlayerGBID, raidUUID, toPlayerGBID):
        if raidUUID not in self.raidDic:
            return None, 0, gameconst.RaidErrno.RAID_RAID_ID_NOT_FOUND

        raidVal = self.raidDic[raidUUID]
        if srcPlayerGBID != raidVal.raidLeaderGBID:
            return None, 0, gameconst.RaidErrno.RAID_RAID_LEADER_CHANGED

        if toPlayerGBID == raidVal.raidLeaderGBID:
            return None, 0, gameconst.RaidErrno.RAID_IS_SAME_PLAYER

        toPlayerTeamIDX = raidVal.getRaidTeamIDX(toPlayerGBID)
        if not toPlayerTeamIDX:
            return None, 0, gameconst.RaidErrno.RAID_TEAM_IDX_NOT_FOUND

        orgRaidLeaderGBID = raidVal.raidLeaderGBID

        _, err = raidVal.setRaidLeader(toPlayerGBID, toPlayerTeamIDX, toClient=True)
        if err != gameconst.RaidErrno.RAID_OK:
            err.initkvbody(source='_transferRaidLeader::raidVal.setRaidLeader')
            return None, 0, err

        return raidVal, orgRaidLeaderGBID, gameconst.RaidErrno.RAID_OK

    def transferRaidDeputy(self, srcPlayerBox, srcPlayerGBID, raidUUID, toPlayerGBID, extraProps, toClient=True, broadcast=True):
        INFO_MSG('transferRaidDeputy::', srcPlayerBox, srcPlayerGBID, raidUUID, toPlayerGBID, extraProps, toClient, broadcast)
        if not toPlayerGBID:
            raidVal, orgRaidDeputyGBID, err = self._cancelRaidDeputy(srcPlayerBox, srcPlayerGBID, raidUUID, 0, toClient)
        else:
            raidVal, orgRaidDeputyGBID, err = self._transferRaidDeputy(srcPlayerBox, srcPlayerGBID, raidUUID, toPlayerGBID, toClient)
        if err != gameconst.RaidErrno.RAID_OK:
            ERROR_MSG('transferRaidDeputy:: failed, {}'.format(err))
            return

        orgRaidDeputyTeamIDX = 0
        orgRaidDeputyVal = None
        if orgRaidDeputyGBID:
            orgRaidDeputyTeamIDX = raidVal.getRaidTeamIDX(orgRaidDeputyGBID)
            orgRaidDeputyVal = raidVal.raidTeamDic[orgRaidDeputyTeamIDX].teamPlayerDic[orgRaidDeputyGBID]

        raidLeaderVal = raidVal.getRaidLeader()
        raidDeputyVal = raidVal.getRaidDeputy()
        # client message
        if toClient:
            if raidDeputyVal and raidDeputyVal.playerBox:
                raidDeputyVal.playerBox.onMessagePre(RAID_CONST.datas["raid_appointedRDL_msg"]["value"], [raidLeaderVal.playerName, ])
                self.getRaidApplyJoinDic(raidDeputyVal.playerBox, raidDeputyVal.playerGbId, raidUUID)
            #if orgRaidDeputyVal and orgRaidDeputyVal.playerBox:
            #    orgRaidDeputyVal.playerBox.onMessagePre(RAID_CONST.datas[""]["value"], [raidLeaderVal.playerName, ])

            if raidDeputyVal:
                raidVal.broadcastAllRaidMembersBase('onMessagePre', (RAID_CONST.datas["raid_appointRDLDone_msg"]["value"], [raidDeputyVal.playerName]),
                                                exclude=(raidDeputyVal.playerGbId,))
            elif orgRaidDeputyVal and broadcast:
                raidVal.broadcastAllRaidMembersBase('onMessagePre', (RAID_CONST.datas["raid_RDLDownGrade_msg"]["value"], [orgRaidDeputyVal.playerName]))

        fn = 'onTransferRaidDeputyAllMemberNotify'
        args = (raidUUID, orgRaidDeputyGBID, raidVal.raidDeputyGBID, raidVal.raidDeputyTeamIDX, extraProps)

        raidVal.broadcastAllRaidMembersCell(fn, args)

    def _cancelRaidDeputy(self, srcPlayerBox, srcPlayerGBID, raidUUID, toPlayerGBID, toClient):
        if raidUUID not in self.raidDic:
            return None, 0, gameconst.RaidErrno.RAID_RAID_ID_NOT_FOUND

        raidVal = self.raidDic[raidUUID]

        if raidVal.raidDeputyGBID == 0:
            return None, 0, gameconst.RaidErrno.RAID_NOT_RAID_DEPUTY

        orgRaidDeputyGBID = raidVal.raidDeputyGBID

        _, err = raidVal.setRaidDeputy(0, 0, toClient)
        if err != gameconst.RaidErrno.RAID_OK:
            err.initkvbody(source='_transferRaidDeputy::raidVal.setRaidDeputy')
            return None, 0, err

        return raidVal, orgRaidDeputyGBID, gameconst.RaidErrno.RAID_OK

    def _transferRaidDeputy(self, srcPlayerBox, srcPlayerGBID, raidUUID, toPlayerGBID, toClient):
        if raidUUID not in self.raidDic:
            return None, 0, gameconst.RaidErrno.RAID_RAID_ID_NOT_FOUND

        raidVal = self.raidDic[raidUUID]
        if srcPlayerGBID != raidVal.raidLeaderGBID:
            return None, 0, gameconst.RaidErrno.RAID_RAID_LEADER_CHANGED

        if raidVal.isRaidDeputy(toPlayerGBID):
            return None, 0, gameconst.RaidErrno.RAID_IS_SAME_PLAYER

        toPlayerTeamIDX = raidVal.getRaidTeamIDX(toPlayerGBID)
        if not toPlayerTeamIDX:
            return None, 0, gameconst.RaidErrno.RAID_TEAM_IDX_NOT_FOUND

        orgRaidDeputyGBID = raidVal.raidDeputyGBID

        _, err = raidVal.setRaidDeputy(toPlayerGBID, toPlayerTeamIDX, toClient)
        if err != gameconst.RaidErrno.RAID_OK:
            err.initkvbody(source='_transferRaidDeputy::raidVal.setRaidDeputy')
            return None, 0, err

        return raidVal, orgRaidDeputyGBID, gameconst.RaidErrno.RAID_OK
    #
    def transferRaidTeamCaptain(self, srcPlayerBox, srcPlayerGBID, raidUUID, toPlayerGBID, extraProps):
        INFO_MSG('transferRaidTeamCaptain::', srcPlayerBox, srcPlayerGBID,
                  raidUUID, toPlayerGBID, extraProps)
        raidTeamVal, err = self._transferRaidTeamCaptain(srcPlayerBox, srcPlayerGBID, raidUUID, toPlayerGBID, toClient=True)
        if err != gameconst.RaidErrno.RAID_OK:
            ERROR_MSG('transferRaidTeamCaptain:: failed, {}'.format(err))
            return

        orgRaidTeamCaptainVal = raidTeamVal.teamPlayerDic[srcPlayerGBID]
        raidTeamCaptainVal = raidTeamVal.teamPlayerDic[raidTeamVal.teamCaptainGBID]
        # client message
        raidTeamCaptainVal.playerBox and raidTeamCaptainVal.playerBox.onMessagePre(
            RAID_CONST.datas["raid_appointedPL_msg"]["value"], [orgRaidTeamCaptainVal.playerName, ])
        for playerVal in raidTeamVal.teamPlayerDic.values():
            if playerVal.playerGbId == raidTeamVal.teamCaptainGBID:
                continue
            playerVal.playerBox and playerVal.playerBox.onMessagePre(
                RAID_CONST.datas["raid_appointPLDone_msg"]["value"], [raidTeamCaptainVal.playerName, ])

        fn = 'onTransferRaidTeamCaptainAllMemberNotify'
        args = (raidUUID, raidTeamVal.teamIDX, srcPlayerGBID, toPlayerGBID, extraProps)

        raidVal = self.raidDic[raidUUID]
        raidVal.broadcastAllRaidMembersCell(fn, args)
    #
    def _transferRaidTeamCaptain(self, srcPlayerBox, srcPlayerGBID, raidUUID, toPlayerGBID, toClient=False):
        if raidUUID not in self.raidDic:
            return None, gameconst.RaidErrno.RAID_RAID_ID_NOT_FOUND

        raidVal = self.raidDic[raidUUID]
        if srcPlayerGBID == raidVal.raidLeaderGBID:
            return None, gameconst.RaidErrno.RAID_LEADER_TEAM_CANT_TRANS_CAPTAIN

        srcPlayerTeamIDX = raidVal.getRaidTeamIDX(srcPlayerGBID)
        if not srcPlayerTeamIDX:
            return None, gameconst.RaidErrno.RAID_TEAM_IDX_NOT_FOUND

        raidTeamVal = raidVal.raidTeamDic[srcPlayerTeamIDX]
        if srcPlayerGBID != raidTeamVal.teamCaptainGBID:
            return None, gameconst.RaidErrno.RAID_NOT_TEAM_CAPTAIN

        _, err = raidTeamVal.setTeamCaptain(toPlayerGBID)
        if err != gameconst.RaidErrno.RAID_OK:
            return None, err

        if toClient:
            raidVal.broadcastAllRaidMembersClient('onSetRaidTeamCaptain', (raidUUID, srcPlayerTeamIDX, toPlayerGBID))

        return raidTeamVal, gameconst.RaidErrno.RAID_OK
    #
    def awardRaidTeamCaptain(self, srcPlayerBox, srcPlayerGBID, raidUUID, toRaidTeamIDX, toPlayerGBID, extraProps):
        INFO_MSG('awardRaidTeamCaptain::', srcPlayerBox, srcPlayerGBID, raidUUID, toRaidTeamIDX, toPlayerGBID, extraProps)
        orgCaptainVal, err = self._awardRaidTeamCaptain(srcPlayerBox, srcPlayerGBID, raidUUID,
                                                        toRaidTeamIDX, toPlayerGBID, toClient=True)
        if err != gameconst.RaidErrno.RAID_OK:
            err = err.initkvbody(source='awardRaidTeamCaptain', raidUUID=raidUUID,
                                 raidTeamIDX=toRaidTeamIDX, playerGBID=toPlayerGBID)()
            ERROR_MSG('awardRaidTeamCaptain:: failed, {}'.format(err))
            return

        fn = 'onAwardRaidTeamCaptainAllMemberNotify'
        args = (raidUUID, srcPlayerGBID, orgCaptainVal.playerGbId, toRaidTeamIDX, toPlayerGBID, extraProps)

        raidVal = self.raidDic[raidUUID]
        raidVal.broadcastAllRaidMembersCell(fn, args)
    #
    def _awardRaidTeamCaptain(self, srcPlayerBox, srcPlayerGBID, raidUUID, toRaidTeamIDX, toPlayerGBID, toClient=False):
        if raidUUID not in self.raidDic:
            return None, gameconst.RaidErrno.RAID_RAID_ID_NOT_FOUND

        raidVal = self.raidDic[raidUUID]
        if srcPlayerGBID != raidVal.raidLeaderGBID:
            return None, gameconst.RaidErrno.RAID_NOT_RAID_LEADER

        if toRaidTeamIDX not in raidVal.raidTeamDic:
            return None, gameconst.RaidErrno.RAID_TEAM_IDX_NOT_FOUND
        elif toRaidTeamIDX == raidVal.raidLeaderGBID:
            return None, gameconst.RaidErrno.RAID_AWARD_SELF_TEAM

        raidTeamVal = raidVal.raidTeamDic[toRaidTeamIDX]
        if toPlayerGBID not in raidTeamVal.teamPlayerDic:
            return None, gameconst.RaidErrno.RAID_PLAYER_GBID_NOT_FOUND
        elif toPlayerGBID == raidTeamVal.teamCaptainGBID:
            return None, gameconst.RaidErrno.RAID_ALREADY_BE_TEAM_CAPTAIN

        orgCaptainVal = raidTeamVal.teamPlayerDic[raidTeamVal.teamCaptainGBID]
        _, err = raidTeamVal.setTeamCaptain(toPlayerGBID)
        if err != gameconst.RaidErrno.RAID_OK:
            return None, err

        if toClient:
            raidVal.broadcastAllRaidMembersClient('onSetRaidTeamCaptain', (raidUUID, toRaidTeamIDX, toPlayerGBID))

        return orgCaptainVal, gameconst.RaidErrno.RAID_OK

    def moveRaidTeamMember(self, srcPlayerBox, srcPlayerGBID, raidUUID,
                           fromPlayerTeamIDX, fromPlayerGBID,
                           toPlayerTeamIDX, toPlayerGBID, extraProps):
        INFO_MSG('moveRaidTeamMember::', srcPlayerBox, srcPlayerGBID, raidUUID,
                  fromPlayerTeamIDX, fromPlayerGBID, toPlayerTeamIDX, toPlayerGBID,
                  extraProps)

        if toPlayerGBID:
            # 如果存在被交换的玩家ID, 则被交换两个玩家所在队伍
            self.moveRaidTeamMemberExchangeTargetPlayer(srcPlayerBox, srcPlayerGBID, raidUUID,
                                                        fromPlayerTeamIDX, fromPlayerGBID,
                                                        toPlayerTeamIDX, toPlayerGBID, extraProps)
        else:
            # 不存在被交换玩家ID, 将玩家交换至其他队伍(或空队伍)的空位
            self.moveRaidTeamMemberNoTargetPlayer(srcPlayerBox, srcPlayerGBID, raidUUID,
                                                  fromPlayerTeamIDX, fromPlayerGBID, toPlayerTeamIDX,
                                                  extraProps)

    def moveRaidTeamMemberNoTargetPlayer(self, srcPlayerBox, srcPlayerGBID, raidUUID,
                                         fromPlayerTeamIDX, fromPlayerGBID,
                                         toPlayerTeamIDX, extraProps):
        INFO_MSG('moveRaidTeamMemberNoTargetPlayer::', srcPlayerBox, srcPlayerGBID,
                  raidUUID, fromPlayerTeamIDX, fromPlayerGBID, toPlayerTeamIDX, extraProps)
        toRaidTeamVal, err = self._moveRaidTeamMemberNoTargetPlayer(srcPlayerBox, srcPlayerGBID, raidUUID,
                                                                    fromPlayerTeamIDX, fromPlayerGBID, toPlayerTeamIDX)
        if err != gameconst.RaidErrno.RAID_OK:
            ERROR_MSG('moveRaidTeamMemberNoTargetPlayer:: failed, {}'.format(err))
            return

        raidVal = self.raidDic[raidUUID]
        raidVal.refreshRaidCacheValToAllPlayers()

        toPlayerVal = toRaidTeamVal.teamPlayerDic[fromPlayerGBID]

        fn = 'onMoveRaidTeamMemberSucc'
        args = (srcPlayerGBID, raidUUID, fromPlayerTeamIDX, fromPlayerGBID, toPlayerTeamIDX, 0, extraProps)

        if toPlayerVal.bOnline and toPlayerVal.playerBox and toPlayerVal.playerBox.cell:
            getattr(toPlayerVal.playerBox.cell, fn)(*args)
        if srcPlayerGBID != fromPlayerGBID:
            srcPlayerBox.cell and getattr(srcPlayerBox.cell, fn)(*args)

    def _moveRaidTeamMemberNoTargetPlayer(self, srcPlayerBox, srcPlayerGBID, raidUUID,
                                          fromPlayerTeamIDX, fromPlayerGBID, toPlayerTeamIDX):
        if raidUUID not in self.raidDic:
            return None, gameconst.RaidErrno.RAID_RAID_ID_NOT_FOUND.initkvbody(raidUUID=raidUUID)

        raidVal = self.raidDic[raidUUID]
        if srcPlayerGBID != raidVal.raidLeaderGBID and not raidVal.isRaidDeputy(srcPlayerGBID):
            return None, gameconst.RaidErrno.RAID_NOT_RAID_LEADER_OR_DEPUTY

        if fromPlayerTeamIDX not in raidVal.raidTeamDic:
            return None, gameconst.RaidErrno.RAID_TEAM_IDX_NOT_FOUND.initkvbody(raidUUID=raidUUID,
                                                                                teamIDX=fromPlayerTeamIDX)

        fromRaidTeamVal = raidVal.raidTeamDic[fromPlayerTeamIDX]
        if fromPlayerGBID not in fromRaidTeamVal.teamPlayerDic:
            return None, gameconst.RaidErrno.RAID_PLAYER_GBID_NOT_FOUND.initkvbody(raidUUID=raidUUID,
                                                                                   teamIDX=fromPlayerTeamIDX,
                                                                                   playerGBID=fromPlayerGBID)

        # orgFromRaidTeamCaptainGBID = fromRaidTeamVal.teamCaptainGBID
        orgRaidLeaderGBID = raidVal.raidLeaderGBID
        orgRaidDeputyGBID = raidVal.raidDeputyGBID

        if toPlayerTeamIDX in raidVal.raidTeamDic:
            INFO_MSG('_moveRaidTeamMemberNoTargetPlayer:: transfer')
            # CASE1: 玩家转移至一个已经有小队的Team
            toRaidTeamVal = raidVal.raidTeamDic[toPlayerTeamIDX]
            if toRaidTeamVal.isRaidFull():
                return None, gameconst.RaidErrno.RAID_RAID_TEAM_IS_FULL
            fromPlayerVal, err = raidVal.popMember(fromPlayerTeamIDX, fromPlayerGBID)
            if err != gameconst.RaidErrno.RAID_OK:
                return None, err.initkvbody(source='_moveRaidTeamMemberNoTargetPlayer::raidVal.popMember',
                                            source2='CASE1')
            toPlayerVal, err = toRaidTeamVal.addTeamMember(fromPlayerGBID, fromPlayerVal.toSavedDict())
            if err != gameconst.RaidErrno.RAID_OK:
                return None, err.initkvbody(source='_moveRaidTeamMemberNoTargetPlayer::toRaidTeamVal.addTeamMember',
                                            srouce2='CASE1')

            if orgRaidLeaderGBID == fromPlayerGBID:
                # fix raid leader
                WARNING_MSG('_moveRaidTeamMemberNoTargetPlayer::CASE1 re-locate raid leader~', orgRaidLeaderGBID)
                raidVal.setRaidLeader(fromPlayerGBID, toRaidTeamVal.teamIDX)
            if orgRaidDeputyGBID == fromPlayerGBID:
                WARNING_MSG('_moveRaidTeamMemberNoTargetPlayer::CASE1 re-locate raid deputy~', orgRaidDeputyGBID)
                raidVal.setRaidDeputy(fromPlayerGBID, toRaidTeamVal.teamIDX)
            '''
            #
            # re-get fromRaidTeamVal, obj may change when popMember method called
            fromRaidTeamVal = raidVal.raidTeamDic.get(fromPlayerTeamIDX)
            if fromRaidTeamVal and orgFromRaidTeamCaptainGBID != fromRaidTeamVal.teamCaptainGBID:
                raidVal.broadcastAllRaidMembersClient('onSetRaidTeamCaptain',
                                                      (raidUUID, fromPlayerTeamIDX, fromRaidTeamVal.teamCaptainGBID))
            '''
            raidVal.broadcastAllRaidMembersClient('onExchangeRaidTeamMember',
                                                  (raidUUID, fromPlayerTeamIDX, fromPlayerGBID, toPlayerTeamIDX, 0))

            return toRaidTeamVal, gameconst.RaidErrno.RAID_OK

        elif toPlayerTeamIDX > raidVal.maxTeamNum:
            return None, gameconst.RaidErrno.RAID_RAID_TEAM_IDX_OFR.initkvbody(raidUUID=raidUUID,
                                                                               teamIDX=toPlayerTeamIDX)
        else:
            # CASE2: 玩家转移至一个新的小队
            INFO_MSG('_moveRaidTeamMemberNoTargetPlayer:: create && transfer')
            fromPlayerVal, err = raidVal.popMember(fromPlayerTeamIDX, fromPlayerGBID)
            if err != gameconst.RaidErrno.RAID_OK:
                return None, err.initkvbody(source='_moveRaidTeamMemberNoTargetPlayer::raidVal.popMember',
                                            source2='CASE2')
            toRaidTeamVal, err = raidVal.addNewTeam(toPlayerTeamIDX)
            if err != gameconst.RaidErrno.RAID_OK:
                return None, err.initkvbody(source='_moveRaidTeamMemberNoTargetPlayer::raidVal.addNewTeam')
            toPlayerVal, err = toRaidTeamVal.addTeamMember(fromPlayerGBID, fromPlayerVal.toSavedDict())
            if err != gameconst.RaidErrno.RAID_OK:
                return None, err.initkvbody(source='_moveRaidTeamMemberNoTargetPlayer::toRaidTeamVal.addTeamMember',
                                            srouce2='CASE2')
            #
            # toRaidTeamVal.setTeamCaptain(fromPlayerGBID)
            if orgRaidLeaderGBID == fromPlayerGBID:
                # fix raid leader
                WARNING_MSG('_moveRaidTeamMemberNoTargetPlayer::CASE2 re-locate raid leader~', orgRaidLeaderGBID)
                raidVal.setRaidLeader(fromPlayerGBID, toRaidTeamVal.teamIDX)
            if orgRaidDeputyGBID == fromPlayerGBID:
                WARNING_MSG('_moveRaidTeamMemberNoTargetPlayer::CASE1 re-locate raid deputy~', orgRaidDeputyGBID)
                raidVal.setRaidDeputy(fromPlayerGBID, toRaidTeamVal.teamIDX)
            '''
            #
            # re-get fromRaidTeamVal, obj may change when popMember method called
            fromRaidTeamVal = raidVal.raidTeamDic.get(fromPlayerTeamIDX)
            if fromRaidTeamVal and orgFromRaidTeamCaptainGBID != fromRaidTeamVal.teamCaptainGBID:
                raidVal.broadcastAllRaidMembersClient('onSetRaidTeamCaptain',
                                                      (raidUUID, fromPlayerTeamIDX, fromRaidTeamVal.teamCaptainGBID))
            raidVal.broadcastAllRaidMembersClient('onSetRaidTeamCaptain',
                                                  (raidUUID, toPlayerTeamIDX, fromPlayerGBID))
            '''
            raidVal.broadcastAllRaidMembersClient('onExchangeRaidTeamMember',
                                                  (raidUUID, fromPlayerTeamIDX, fromPlayerGBID, toPlayerTeamIDX, 0))
            return toRaidTeamVal, gameconst.RaidErrno.RAID_OK

    def moveRaidTeamMemberExchangeTargetPlayer(self, srcPlayerBox, srcPlayerGBID, raidUUID,
                                               fromPlayerTeamIDX, fromPlayerGBID,
                                               toPlayerTeamIDX, toPlayerGBID, extraProps):
        INFO_MSG('moveRaidTeamMemberExchangeTargetPlayer::', srcPlayerBox, srcPlayerGBID, raidUUID,
                  fromPlayerTeamIDX, fromPlayerGBID, toPlayerTeamIDX, toPlayerGBID, extraProps)

        teamPlayerValDic, err = self._moveRaidTeamMemberExchangeTargetPlayer(
            srcPlayerBox, srcPlayerGBID, raidUUID,
            fromPlayerTeamIDX, fromPlayerGBID,
            toPlayerTeamIDX, toPlayerGBID)
        if err != gameconst.RaidErrno.RAID_OK:
            ERROR_MSG('moveRaidTeamMemberExchangeTargetPlayer:: failed, {}'.format(err))
            return

        raidVal = self.raidDic[raidUUID]
        raidVal.refreshRaidCacheValToAllPlayers()

        newFromPlayerVal = teamPlayerValDic[fromPlayerGBID]
        newToPlayerVal = teamPlayerValDic[toPlayerGBID]

        fn = 'onMoveRaidTeamMemberSucc'
        args = (srcPlayerGBID, raidUUID, fromPlayerTeamIDX, fromPlayerGBID, toPlayerTeamIDX, toPlayerGBID, extraProps)

        for playerVal in (newFromPlayerVal, newToPlayerVal):
            if playerVal.bOnline and playerVal.playerBox and playerVal.playerBox.cell:
                getattr(playerVal.playerBox.cell, fn)(*args)
        if srcPlayerGBID != fromPlayerGBID and srcPlayerGBID != toPlayerGBID:
            srcPlayerBox.cell and getattr(srcPlayerBox.cell, fn)(*args)

    def _moveRaidTeamMemberExchangeTargetPlayer(self, srcPlayerBox, srcPlayerGBID, raidUUID,
                                               fromPlayerTeamIDX, fromPlayerGBID,
                                               toPlayerTeamIDX, toPlayerGBID):
        if raidUUID not in self.raidDic:
            return None, gameconst.RaidErrno.RAID_RAID_ID_NOT_FOUND.initkvbody(raidUUID=raidUUID)

        raidVal = self.raidDic[raidUUID]
        if srcPlayerGBID != raidVal.raidLeaderGBID and not raidVal.isRaidDeputy(srcPlayerGBID):
            return None, gameconst.RaidErrno.RAID_NOT_RAID_LEADER_OR_DEPUTY

        if fromPlayerTeamIDX not in raidVal.raidTeamDic:
            return None, gameconst.RaidErrno.RAID_TEAM_IDX_NOT_FOUND.initkvbody(raidUUID=raidUUID,
                                                                                teamIDX=fromPlayerTeamIDX)
        elif toPlayerTeamIDX not in raidVal.raidTeamDic:
            return None, gameconst.RaidErrno.RAID_TEAM_IDX_NOT_FOUND.initkvbody(raidUUID=raidUUID,
                                                                                teamIDX=fromPlayerTeamIDX)

        fromRaidTeamVal = raidVal.raidTeamDic[fromPlayerTeamIDX]
        toRaidTeamVal = raidVal.raidTeamDic[toPlayerTeamIDX]
        if fromPlayerGBID not in fromRaidTeamVal.teamPlayerDic:
            return None, gameconst.RaidErrno.RAID_PLAYER_GBID_NOT_FOUND.initkvbody(raidUUID=raidUUID,
                                                                                   teamIDX=fromPlayerTeamIDX,
                                                                                   playerGBID=fromPlayerGBID)
        elif toPlayerGBID not in toRaidTeamVal.teamPlayerDic:
            return None, gameconst.RaidErrno.RAID_PLAYER_GBID_NOT_FOUND.initkvbody(raidUUID=raidUUID,
                                                                                   teamIDX=toPlayerTeamIDX,
                                                                                   playerGBID=toPlayerGBID)

        orgRaidLeaderGBID = raidVal.raidLeaderGBID
        orgRaidDeputyGBID = raidVal.raidDeputyGBID
        #
        # orgFromRaidTeamCaptainGBID = fromRaidTeamVal.teamCaptainGBID
        # orgToRaidTeamCaptainGBID = toRaidTeamVal.teamCaptainGBID
        fromPlayerPos, err = raidVal.getMemberPos(fromPlayerTeamIDX, fromPlayerGBID)
        if err != gameconst.RaidErrno.RAID_OK:
            return None, err
        toPlayerPos, err = raidVal.getMemberPos(toPlayerTeamIDX, toPlayerGBID)
        if err != gameconst.RaidErrno.RAID_OK:
            return None, err

        minPos = min(toPlayerPos, fromPlayerPos)

        fromPlayerVal, err = raidVal.popMember(fromPlayerTeamIDX, fromPlayerGBID)
        if err != gameconst.RaidErrno.RAID_OK:
            return None, err

        def _revertFromPlayerPopMember():
            WARNING_MSG('_revertFromPlayerPopMember::~')
            raidVal._addNewMemberSpecially(fromPlayerGBID, fromPlayerVal.toSavedDict(), fromPlayerTeamIDX, pos=fromPlayerPos)
            _fromRaidTeamVal = raidVal.raidTeamDic[fromPlayerTeamIDX]
            '''
            #
            if orgFromRaidTeamCaptainGBID == fromPlayerGBID:
                WARNING_MSG('    \- revert: raid team captain', raidUUID, _fromRaidTeamVal.teamIDX, fromPlayerGBID)
                _fromRaidTeamVal.setTeamCaptain(fromPlayerGBID)
            '''
            if orgRaidLeaderGBID == fromPlayerGBID:
                WARNING_MSG('    \- revert: raid leader', raidUUID, fromPlayerGBID)
                raidVal.setRaidLeader(fromPlayerGBID, _fromRaidTeamVal.teamIDX)
            if orgRaidDeputyGBID == fromPlayerGBID:
                WARNING_MSG('    \- revert: raid deputy', raidUUID, fromPlayerGBID)
                raidVal.setRaidDeputy(fromPlayerGBID, _fromRaidTeamVal.teamIDX)

        toPlayerVal, err = raidVal.popMember(toPlayerTeamIDX, toPlayerGBID)
        if err != gameconst.RaidErrno.RAID_OK:
            _revertFromPlayerPopMember()
            return None, err

        def _revertToPlayerPopMember():
            WARNING_MSG('_revertToPlayerPopMember::~')
            raidVal._addNewMemberSpecially(toPlayerGBID, toPlayerVal.toSavedDict(), toPlayerTeamIDX, pos=toPlayerPos)
            _toRaidTeamVal = raidVal.raidTeamDic[toPlayerTeamIDX]
            '''
            #
            if orgToRaidTeamCaptainGBID == toPlayerGBID:
                WARNING_MSG('    \- revert: raid team captain', raidUUID, _toRaidTeamVal.teamIDX, toPlayerGBID)
                _toRaidTeamVal.setTeamCaptain(toPlayerGBID)
            '''
            if orgRaidLeaderGBID == toPlayerGBID:
                WARNING_MSG('    \- revert: raid leader', raidUUID, toPlayerGBID)
                raidVal.setRaidLeader(toPlayerGBID, _toRaidTeamVal.teamIDX)
            if orgRaidDeputyGBID == toPlayerGBID:
                WARNING_MSG('    \- revert: raid deputy', raidUUID, toPlayerGBID)
                raidVal.setRaidDeputy(toPlayerGBID, _toRaidTeamVal.teamIDX)

        if fromPlayerTeamIDX != toPlayerTeamIDX or minPos == toPlayerPos:
            newFromPlayerVal, err = raidVal._addNewMemberSpecially(
                fromPlayerGBID, fromPlayerVal.toSavedDict(), toPlayerTeamIDX, pos=toPlayerPos)
            if err != gameconst.RaidErrno.RAID_OK:
                _revertToPlayerPopMember()
                _revertFromPlayerPopMember()
                return None, err

            def _revertFromPlayerAddMember():
                WARNING_MSG('_revertFromPlayerAddMember::~')
                raidVal.popMember(toPlayerTeamIDX, fromPlayerGBID)

            newToPlayerVal, err = raidVal._addNewMemberSpecially(
                toPlayerGBID, toPlayerVal.toSavedDict(), fromPlayerTeamIDX, pos=fromPlayerPos)
            if err != gameconst.RaidErrno.RAID_OK:
                _revertFromPlayerAddMember()
                _revertToPlayerPopMember()
                _revertFromPlayerPopMember()
                return None, err
        else:
            newToPlayerVal, err = raidVal._addNewMemberSpecially(
                toPlayerGBID, toPlayerVal.toSavedDict(), fromPlayerTeamIDX, pos=fromPlayerPos)
            if err != gameconst.RaidErrno.RAID_OK:
                _revertFromPlayerPopMember()
                _revertToPlayerPopMember()
                return None, err

            def _revertToPlayerAddMember():
                WARNING_MSG('_revertToPlayerAddMember::~')
                raidVal.popMember(fromPlayerTeamIDX, toPlayerGBID)

            newFromPlayerVal, err = raidVal._addNewMemberSpecially(
                fromPlayerGBID, fromPlayerVal.toSavedDict(), toPlayerTeamIDX, pos=toPlayerPos)
            if err != gameconst.RaidErrno.RAID_OK:
                _revertToPlayerAddMember()
                _revertFromPlayerPopMember()
                _revertToPlayerPopMember()
                return None, err

        # fix raid leader
        if orgRaidLeaderGBID == fromPlayerGBID:
            WARNING_MSG('_moveRaidTeamMemberExchangeTargetPlayer:: re-locate raid leader A->B(nA)*', orgRaidLeaderGBID)
            raidVal.setRaidLeader(fromPlayerGBID, toPlayerTeamIDX)
        elif orgRaidLeaderGBID == toPlayerGBID:
            WARNING_MSG('_moveRaidTeamMemberExchangeTargetPlayer:: re-locate raid leader A(nB)*<-B', orgRaidLeaderGBID)
            raidVal.setRaidLeader(toPlayerGBID, fromPlayerTeamIDX)
        # fix raid deputy
        if orgRaidDeputyGBID == fromPlayerGBID:
            WARNING_MSG('_moveRaidTeamMemberExchangeTargetPlayer:: re-locate raid deputy A->B(nA)*', orgRaidDeputyGBID)
            raidVal.setRaidDeputy(fromPlayerGBID, toPlayerTeamIDX)
        elif orgRaidDeputyGBID == toPlayerGBID:
            WARNING_MSG('_moveRaidTeamMemberExchangeTargetPlayer:: re-locate raid deputy A(nB)*<-B', orgRaidDeputyGBID)
            raidVal.setRaidDeputy(toPlayerGBID, fromPlayerTeamIDX)
        '''
        #
        # re-get fromRaidTeamVal and toRaidTeamVal, obj may change when popMember method called
        fromRaidTeamVal = raidVal.raidTeamDic.get(fromPlayerTeamIDX)
        toRaidTeamVal = raidVal.raidTeamDic.get(toPlayerTeamIDX)
        if fromRaidTeamVal and orgFromRaidTeamCaptainGBID != fromRaidTeamVal.teamCaptainGBID:
            raidVal.broadcastAllRaidMembersClient('onSetRaidTeamCaptain',
                                                  (raidUUID, fromPlayerTeamIDX, fromRaidTeamVal.teamCaptainGBID))
        if toRaidTeamVal and orgToRaidTeamCaptainGBID != toRaidTeamVal.teamCaptainGBID:
            raidVal.broadcastAllRaidMembersClient('onSetRaidTeamCaptain',
                                                  (raidUUID, toPlayerTeamIDX, toRaidTeamVal.teamCaptainGBID))
        '''
        raidVal.broadcastAllRaidMembersClient('onExchangeRaidTeamMember',
                                              (raidUUID, fromPlayerTeamIDX, fromPlayerGBID, toPlayerTeamIDX, toPlayerGBID))

        return {fromPlayerGBID: newFromPlayerVal, toPlayerGBID: newToPlayerVal}, gameconst.RaidErrno.RAID_OK

    def setRaidTarget(self, srcPlayerBox, srcPlayerGBID, raidUUID, raidTarget, minLevel, minScore, recruitInfo, password, isAutoExpedition):
        INFO_MSG('setRaidTarget::', srcPlayerBox, srcPlayerGBID, raidUUID, raidTarget, minLevel, minScore, recruitInfo, password, isAutoExpedition)
        _, err = self._setRaidTarget(srcPlayerBox, srcPlayerGBID, raidUUID, raidTarget, minLevel, minScore, recruitInfo, password, isAutoExpedition, toClient=True)
        if err != gameconst.RaidErrno.RAID_OK:
            ERROR_MSG('setRaidTarget:: failed, {}'.format(err))
            return

        raidVal = self.raidDic[raidUUID]
        isPublic = len(raidVal.password) == 0
        raidVal.broadcastAllRaidMembersCell('onSetRaidTargetAllMemberNotify', (srcPlayerGBID, raidUUID, raidTarget, minLevel, minScore, recruitInfo, password, isAutoExpedition))
        self.checkAutoStart(raidUUID)

    def _setRaidTarget(self, srcPlayerBox, srcPlayerGBID, raidUUID, newRaidTargetId, minLevel, minScore, recruitInfo, password, isAutoExpedition, toClient=False):
        if raidUUID not in self.raidDic:
            return None, gameconst.RaidErrno.RAID_RAID_ID_NOT_FOUND

        raidVal = self.raidDic[raidUUID]
        if raidVal.raidLeaderGBID != srcPlayerGBID:
            return None, gameconst.RaidErrno.RAID_NOT_RAID_LEADER
        if raidVal.raidTarget != newRaidTargetId:
            return None, gameconst.RaidErrno.RAID_TARGET_IS_ILLEGAL
        if raidVal.raidMinLevel != minLevel:
            return None, gameconst.RaidErrno.RAID_LEVEL_IS_ILLEGAL
        if raidVal.raidMinScore != minScore:
            return None, gameconst.RaidErrno.RAID_SOCRE_IS_ILLEGAL
        if raidVal.password != password:
            return None, gameconst.RaidErrno.RAID_PASSWORD_IS_ILLEGAL
        if raidVal.recruitInfo == recruitInfo and raidVal.isAutoExpedition == isAutoExpedition:
            return None, gameconst.RaidErrno.RAID_SET_TARGET_ILLEGAL
        # check team member's score and level
        if not raidVal.setTarget(newRaidTargetId, minLevel, minScore, recruitInfo, password, isAutoExpedition):
            return None, gameconst.RaidErrno.RAID_TARGET_IS_ILLEGAL

        if toClient:
            raidVal.broadcastAllRaidMembersClient('onSetRaidTarget', (raidUUID, newRaidTargetId, minLevel, minScore, recruitInfo, raidVal.password, raidVal.isAutoExpedition))

        self.raidPrepareStopAutoMatch(raidUUID)
        if raidVal.isPublish and raidVal.raidTarget > gameconst.PARE_ACTIVITY_ID:
            self.raidPrepareAutoMatch(raidUUID)

        return raidVal, gameconst.RaidErrno.RAID_OK

    def startRaidStandbyChecker(self, srcPlayerBox, srcPlayerGBID, raidUUID, extraProps):
        INFO_MSG('startRaidStandbyChecker::', srcPlayerBox, srcPlayerGBID, raidUUID, extraProps)
        checkSrc = extraProps.pop('_checkSrc', gameconst.RaidDungeonStandbyCheckSrcEnum.DEFAULT)
        record, err = self._startRaidStandbyChecker(srcPlayerBox, srcPlayerGBID, raidUUID, checkSrc, extraProps)
        if err != gameconst.RaidErrno.RAID_OK:
            _i_errLog = False
            if err == gameconst.RaidErrno.RAID_DURING_STANDBY_CHECK:
                srcPlayerBox.onMessagePre(RAID_CONST.datas["raid_readyCheckUndergoing_msg"]["value"], [])
            else:
                _i_errLog = True

            (ERROR_MSG if _i_errLog else WARNING_MSG)('startRaidStandbyChecker:: failed, {}'.format(err))
            return

    def _startRaidStandbyChecker(self, srcPlayerBox, srcPlayerGBID, raidUUID,
                                 checkSrc, extraProps):
        if raidUUID not in self.raidDic:
            return None, gameconst.RaidErrno.RAID_RAID_ID_NOT_FOUND

        raidVal = self.raidDic[raidUUID]
        if srcPlayerGBID != raidVal.raidLeaderGBID and not raidVal.isRaidDeputy(srcPlayerGBID):
            return None, gameconst.RaidErrno.RAID_NOT_RAID_LEADER_OR_DEPUTY

        if self._getStandbyCheckerRecord(raidUUID):
            return None, gameconst.RaidErrno.RAID_DURING_STANDBY_CHECK

        checkBoxes = {}
        broadcastExcludeGBIDs = []
        trueCount = falseCount = unknownCount = 0
        for _, memberGBID, memberVal in raidVal.iterGetRaidMember():
            if srcPlayerGBID == memberGBID:
                checkBoxes[memberGBID] = True
                trueCount += 1
                # 【【团队】团确时候，团员准备好没有打钩】
                # NOTE()(RAID): 客户端手动处理团长消息
                # broadcastExcludeGBIDs.append(memberGBID)
                continue

            if not memberVal.bOnline:
                checkBoxes[memberGBID] = False
                falseCount += 1
                broadcastExcludeGBIDs.append(memberGBID)
                continue

            checkBoxes[memberGBID] = None
            unknownCount += 1

        _timeout = utils.getConfirmMessageCooldown(RAID_CONST.datas["raid_readyCheck_check"]["value"], 30) + 2
        record = self._initStanbyCheckerRecord(
            raidUUID, checkBoxes, trueCount, falseCount, unknownCount, checkSrc,
            cbFn='onReplyRaidStandbyChecker', cbArgs=(raidUUID, False, {}),
            timeout=_timeout)
        # FIXME(): 后面可以通过传给客户端时间戳的方式弹窗, 防止弹窗(由于网络延迟)的原因服务端先于客户端结束
        if checkSrc == gameconst.RaidDungeonStandbyCheckSrcEnum.ENTER_DUNGEON:
            INFO_MSG('_startRaidStandbyChecker::raidEnterDungeonStandbyCheckNotify,', broadcastExcludeGBIDs, extraProps)
            record.extraProps.update(extraProps)
            _dungeonNo = extraProps.get('enterDungeonNo', 0)
            dungeonPlayMode = extraProps.get('dungeonPlayMode')
            dunLevel = dungeonPlayMode.dunLevel
        else:
            INFO_MSG('_startRaidStandbyChecker::raidStandbyCheckNotify,', broadcastExcludeGBIDs, extraProps)

        return record, gameconst.RaidErrno.RAID_OK

    def replyRaidStandbyChecker(self, srcPlayerBox, srcPlayerGBID, raidUUID, beArgreed, extraProps):
        INFO_MSG('replyRaidStandbyChecker::', srcPlayerBox, srcPlayerGBID, raidUUID, beArgreed, extraProps)
        record, err = self._replyRaidStandbyChecker(srcPlayerBox, srcPlayerGBID, raidUUID, beArgreed, toClient=True)
        if err != gameconst.RaidErrno.RAID_OK:
            if err == gameconst.RaidErrno.RAID_CHECKING_STANDBY_CHECK:
                INFO_MSG('  replyRaidStandbyChecker:: skill checking...',
                         record.trueCount, record.falseCount, record.unknownCount)
            else:
                ERROR_MSG('replyRaidStandbyChecker:: failed, {}'.format(err))
            return

        self.onReplyRaidStandbyChecker(raidUUID, record.isAllCheckSucceed(), extraProps)

    def _replyRaidStandbyChecker(self, srcPlayerBox, srcPlayerGBID, raidUUID, beAgreed, toClient=False):
        if raidUUID not in self.raidDic:
            return None, gameconst.RaidErrno.RAID_RAID_ID_NOT_FOUND

        record = self._getStandbyCheckerRecord(raidUUID)    # type: _RaidStandbyCheckerVal
        if not record:
            return None, gameconst.RaidErrno.RAID_STANDBY_RECORD_NOT_FOUND
        if srcPlayerGBID not in record.checkBoxes:
            return None, gameconst.RaidErrno.RAID_PLAYER_GBID_NOT_FOUND
        if record.isChecked(srcPlayerGBID):
            return None, gameconst.RaidErrno.RAID_STANDBY_ALREADY_CHECKED

        checkResult = record.checkIt(srcPlayerGBID, beAgreed)

        if not record.isAllChecked():
            return record, gameconst.RaidErrno.RAID_CHECKING_STANDBY_CHECK

        return record, gameconst.RaidErrno.RAID_OK

    def onReplyRaidStandbyChecker(self, raidUUID, result, extraProps):
        INFO_MSG('onReplyRaidStandbyChecker::', raidUUID, result, extraProps)

        def _check():
            if raidUUID not in self.raidDic:
                return None, gameconst.RaidErrno.RAID_RAID_ID_NOT_FOUND
            return None, gameconst.RaidErrno.RAID_OK

        _, err = _check()
        if err != gameconst.RaidErrno.RAID_OK:
            WARNING_MSG('onReplyRaidStandbyChecker:: check failed, {}'.format(err))
            self._popStandbyCheckerRecord(raidUUID)
            return

        record = self._popStandbyCheckerRecord(raidUUID)    # Type: _RaidStandbyCheckerVal
        raidVal = self.raidDic[raidUUID]
        if record.enterSrc == gameconst.RaidDungeonStandbyCheckSrcEnum.ENTER_DUNGEON:
            pass
        else:
            raidVal.broadcastAllRaidMembersClient('onReplyRaidStandbyChecker', (raidUUID, result))

        # 【【任务】团队就位确认结果发送到团队频道】
        if result:
            raidVal.broadcastAllRaidMembersBase('onMessagePre', (MMD.datas.raid_ready, []))
        else:
            for i_gbId, i_result in record.checkBoxes.items():
                if i_result:
                    continue
                teamIdx = raidVal.getRaidTeamIDX(i_gbId)
                if teamIdx <= 0:
                    WARNING_MSG('onReplyRaidStandbyChecker:: teamIdx not found', i_gbId, teamIdx, raidUUID)
                    continue
                pVal = raidVal.raidTeamDic[teamIdx].teamPlayerDic.get(i_gbId)
                pVal and raidVal.broadcastAllRaidMembersBase('onMessagePre', (RAID_CONST.datas["raid_unready_msg"]["value"], [pVal.playerName]))

        if not result:
            return

        if record.enterSrc == gameconst.RaidDungeonStandbyCheckSrcEnum.ENTER_DUNGEON:
            dungeonNo, src = record.extraProps.pop('enterDungeonNo'), record.extraProps.pop('src')
            extraProps.update(record.extraProps)
            INFO_MSG('onReplyRaidStandbyChecker:: enter dungeon', raidUUID, dungeonNo)
            raidLeaderVal = raidVal.getRaidLeader()
            if raidLeaderVal.playerBox and raidLeaderVal.playerBox.cell:
                raidLeaderVal.playerBox.cell.doCreateAndEnterRaidDungeon(raidUUID, dungeonNo, src, extraProps)

    def broadRaidChatMsg(self, srcPlayerBox, srcPlayerGBID, raidUUID, avatarInfo, broadMsg, extraProps):
        DEBUG_MSG('broadRaidChatMsg::', srcPlayerBox, srcPlayerGBID, raidUUID, broadMsg, extraProps, avatarInfo)
        _, err = self._broadRaidChatMsg(srcPlayerBox, srcPlayerGBID, raidUUID, avatarInfo, broadMsg)
        if err != gameconst.RaidErrno.RAID_OK:
            WARNING_MSG('broadRaidChatMsg:: failed, {}'.format(err))

    def _broadRaidChatMsg(self, srcPlayerBox, srcPlayerGBID, raidUUID, avatarInfo, broadMsg):
        if raidUUID not in self.raidDic:
            return None, gameconst.RaidErrno.RAID_RAID_ID_NOT_FOUND
        raidVal = self.raidDic[raidUUID]
        raidVal.broadcastAllRaidMembersBase(
            'onRecvChannelMsg',
            (gameconst.ChatChannel.RAID, avatarInfo, broadMsg), exclude=(srcPlayerGBID, ))
        return None, gameconst.RaidErrno.RAID_OK

    # --------------------------------------------------------------------
    # RAID MICS
    def switchRaidMicsMode(self, srcPlayerBox, srcPlayerGBID, raidUUID, mode, extraProps):
        INFO_MSG("switchRaidMicsMode::", srcPlayerBox, srcPlayerGBID, raidUUID, mode, extraProps)
        raidVal, err = self._switchRaidMicsMode(srcPlayerBox, srcPlayerGBID, raidUUID, mode, extraProps)
        if err != gameconst.RaidErrno.RAID_OK:
            WARNING_MSG('switchRaidMicsMode:: failed, {}'.format(err))
            return

        raidVal.getAllRaidMemberMiscStatus(toClient=True)

    def _switchRaidMicsMode(self, srcPlayerBox, srcPlayerGBID, raidUUID, mode, extraProps):
        if raidUUID not in self.raidDic:
            return None, gameconst.RaidErrno.RAID_RAID_ID_NOT_FOUND
        raidVal = self.raidDic[raidUUID]
        return raidVal.switchRaidMiscMode(srcPlayerGBID, mode, extraProps, toClient=True)

    def turnOnRaidMics(self, srcPlayerBox, srcPlayerGBID, raidUUID, playerGBID, extraProps):
        INFO_MSG("turnOnRaidMics::", srcPlayerBox, srcPlayerGBID, raidUUID, playerGBID, extraProps)
        _, err = self._turnOnRaidMics(srcPlayerBox, srcPlayerGBID, raidUUID, playerGBID)
        if err != gameconst.RaidErrno.RAID_OK:
            WARNING_MSG('turnOnRaidMics:: failed, {}'.format(err))

    def _turnOnRaidMics(self, srcPlayerBox, srcPlayerGBID, raidUUID, playerGBID):
        if raidUUID not in self.raidDic:
            return None, gameconst.RaidErrno.RAID_RAID_ID_NOT_FOUND
        raidVal = self.raidDic[raidUUID]
        teamIDX = raidVal.getRaidTeamIDX(playerGBID)
        return raidVal.turnOnRaidMemberMics(srcPlayerGBID, teamIDX, playerGBID, toClient=True)

    def turnOffRaidMics(self, srcPlayerBox, srcPlayerGBID, raidUUID, playerGBID, extraProps):
        INFO_MSG("turnOffRaidMics::", srcPlayerBox, srcPlayerGBID, raidUUID, playerGBID, extraProps)
        _, err = self._turnOffRaidMics(srcPlayerBox, srcPlayerGBID, raidUUID, playerGBID)
        if err != gameconst.RaidErrno.RAID_OK:
            WARNING_MSG('turnOffRaidMics:: failed, {}'.format(err))

    def _turnOffRaidMics(self, srcPlayerBox, srcPlayerGBID, raidUUID, playerGBID):
        if raidUUID not in self.raidDic:
            return None, gameconst.RaidErrno.RAID_RAID_ID_NOT_FOUND
        raidVal = self.raidDic[raidUUID]
        teamIDX = raidVal.getRaidTeamIDX(playerGBID)
        return raidVal.turnOffRaidMemberMics(srcPlayerGBID, teamIDX, playerGBID, blockMics=False, toClient=True)

    def blockRaidMemberMics(self, srcPlayerBox, srcPlayerGBID, raidUUID, teamIDX, playerGBID, extraProps):
        INFO_MSG("blockRaidMemberMics::", srcPlayerBox, srcPlayerGBID, raidUUID, teamIDX, playerGBID, extraProps)
        _, err = self._blockRaidMemberMics(srcPlayerBox, srcPlayerGBID, raidUUID, teamIDX, playerGBID)
        if err != gameconst.RaidErrno.RAID_OK:
            WARNING_MSG('blockRaidMemberMics:: failed, {}'.format(err))

    def _blockRaidMemberMics(self, srcPlayerBox, srcPlayerGBID, raidUUID, teamIDX, playerGBID):
        if raidUUID not in self.raidDic:
            return None, gameconst.RaidErrno.RAID_RAID_ID_NOT_FOUND
        raidVal = self.raidDic[raidUUID]
        return raidVal.turnOffRaidMemberMics(srcPlayerGBID, teamIDX, playerGBID, blockMics=True, toClient=True)

    def unblockRaidMemberMics(self, srcPlayerBox, srcPlayerGBID, raidUUID, teamIDX, playerGBID, extraProps):
        INFO_MSG("unblockRaidMemberMics::", srcPlayerBox, srcPlayerGBID, raidUUID, teamIDX, playerGBID, extraProps)
        _, err = self._unblockRaidMemberMics(srcPlayerBox, srcPlayerGBID, raidUUID, teamIDX, playerGBID)
        if err != gameconst.RaidErrno.RAID_OK:
            WARNING_MSG('unblockRaidMemberMics:: failed, {}'.format(err))
            if err == gameconst.RaidErrno.RAID_ALL_MICS_BLOCKED:
                srcPlayerBox.onMessagePre(MMD.datas.voiceChat_allMicBanned, [])

    def _unblockRaidMemberMics(self, srcPlayerBox, srcPlayerGBID, raidUUID, teamIDX, playerGBID):
        if raidUUID not in self.raidDic:
            return None, gameconst.RaidErrno.RAID_RAID_ID_NOT_FOUND
        raidVal = self.raidDic[raidUUID]
        return raidVal.unblockRaidMemberMisc(srcPlayerGBID, teamIDX, playerGBID, toClient=True)

    def blockAllRaidMemberMics(self, srcPlayerBox, srcPlayerGBID, raidUUID, extraProps):
        INFO_MSG("blockAllRaidMemberMics::", srcPlayerBox, srcPlayerGBID, raidUUID, extraProps)
        raidVal, err = self._blockAllRaidMemberMics(srcPlayerBox, srcPlayerGBID, raidUUID)
        if err != gameconst.RaidErrno.RAID_OK:
            WARNING_MSG('blockAllRaidMemberMics:: failed, {}'.format(err))
            return

    def _blockAllRaidMemberMics(self, srcPlayerBox, srcPlayerGBID, raidUUID):
        if raidUUID not in self.raidDic:
            return None, gameconst.RaidErrno.RAID_RAID_ID_NOT_FOUND

        raidVal = self.raidDic[raidUUID]
        if not raidVal.raidMicsSwitch:
            return None, gameconst.RaidErrno.RAID_MICS_SWITCH_OFF

        if raidVal.raidMicsBlocked:
            return None, gameconst.RaidErrno.RAID_ALL_MICS_BLOCKED

        for teamIDX, memberGBID, memberVal in raidVal.iterGetRaidMember():
            if srcPlayerGBID == memberGBID:
                continue
            _, err = raidVal.turnOffRaidMemberMics(srcPlayerGBID, teamIDX, memberGBID, blockMics=True, toClient=False)
            if err != gameconst.RaidErrno.RAID_OK:
                WARNING_MSG("_blockAllRaidMemberMics::failed, errno={}".format(err),
                            raidUUID, srcPlayerGBID, teamIDX, memberGBID, memberVal)

        raidVal.raidMicsBlocked = True
        return raidVal, gameconst.RaidErrno.RAID_OK

    def unblockAllRaidMemberMics(self, srcPlayerBox, srcPlayerGBID, raidUUID, extraProps):
        INFO_MSG("unblockAllRaidMemberMics::", srcPlayerBox, srcPlayerGBID, raidUUID, extraProps)
        raidVal, err = self._unblockAllRaidMemberMics(srcPlayerBox, srcPlayerGBID, raidUUID)
        if err != gameconst.RaidErrno.RAID_OK:
            WARNING_MSG('unblockAllRaidMemberMics:: failed, {}'.format(err))
            return

    def _unblockAllRaidMemberMics(self, srcPlayerBox, srcPlayerGBID, raidUUID):
        if raidUUID not in self.raidDic:
            return None, gameconst.RaidErrno.RAID_RAID_ID_NOT_FOUND
        raidVal = self.raidDic[raidUUID]
        if not raidVal.raidMicsSwitch:
            return None, gameconst.RaidErrno.RAID_MICS_SWITCH_OFF

        raidVal.raidMicsBlocked = False
        for teamIDX, memberGBID, memberVal in raidVal.iterGetRaidMember():
            _, err = raidVal.unblockRaidMemberMisc(srcPlayerGBID, teamIDX, memberGBID, toClient=False)
            if err != gameconst.RaidErrno.RAID_OK:
                WARNING_MSG("_unblockAllRaidMemberMics::failed, errno={}".format(err),
                            raidUUID, srcPlayerGBID, teamIDX, memberGBID, memberVal)

        return raidVal, gameconst.RaidErrno.RAID_OK

    # --------------------------------------------------------------------

    # ----------------------------------------------------------------------
    # RAID DUNGEON METHODS
    # 团队副本相关
    # ----------------------------------------------------------------------

    def createAndEnterRaidDungeonPreCheck(self, srcPlayerBox, srcPlayerGBID,
                                          raidUUID, dungeonNo, src, extraProps):
        INFO_MSG('createAndEnterRaidDungeonPreCheck', srcPlayerBox, srcPlayerGBID,
                  raidUUID, dungeonNo, src, extraProps)
        _, err = self._createAndEnterRaidDungeonPreCheck(srcPlayerBox, srcPlayerGBID, raidUUID, dungeonNo, src)
        if err != gameconst.RaidDungeonErrno.RAIDDUN_OK:
            ERROR_MSG('createAndEnterRaidDungeonPreCheck:: failed, {}'.format(err))
            return

        srcPlayerBox.cell.onCreateAndEnterRaidDungeonCheckComplete(raidUUID, dungeonNo, src, extraProps)

    def _createAndEnterRaidDungeonPreCheck(self, srcPlayerBox, srcPlayerGBID,
                                           raidUUID, dungeonNo, src):
        if raidUUID not in self.raidDic:
            return None, gameconst.RaidDungeonErrno.RAIDDUN_RAID_ID_NOT_FOUND
        raidVal = self.raidDic[raidUUID]
        if srcPlayerGBID != raidVal.raidLeaderGBID:
            return None, gameconst.RaidDungeonErrno.RAIDDUN_NOT_RAID_LEADER
        if dungeonNo in raidVal.raidDungeonRecords:
            return None, gameconst.RaidDungeonErrno.RAIDDUN_RAID_ALREADY_EXIST_DUNGEON
        return None, gameconst.RaidDungeonErrno.RAIDDUN_OK

    def createAndEnterRaidDungeonPostCheck(self, srcPlayerBox, srcPlayerGBID,
                                           raidUUID, dungeonNo, spaceNo, spaceUUID,
                                           spaceBox, spaceMgrBox, src, extraProps):
        INFO_MSG('createAndEnterRaidDungeonPostCheck::', srcPlayerBox, srcPlayerGBID,
                  raidUUID, dungeonNo, spaceNo, spaceUUID, spaceBox, spaceMgrBox, src, extraProps)
        _, err = self._createAndEnterRaidDungeonPostCheck(srcPlayerBox, srcPlayerGBID,
                                                          raidUUID, dungeonNo, spaceNo,
                                                          spaceUUID, src)
        dungeonStub = gameengine.getDungeonStubByDungeonNo(dungeonNo, gameconst.DungeonEnterType.RAID)
        if err != gameconst.RaidDungeonErrno.RAIDDUN_OK:
            ERROR_MSG('createAndEnterRaidDungeonPostCheck:: failed, {}'.format(err))
            # 重复创建副本, 删除刚刚创建的副本
            dungeonStub.destoryDungeonSpace(spaceNo, spaceUUID, 'duplicated-create')
        else:
            raidVal = self.raidDic[raidUUID]
            raidVal.setRaidDungeonInfo(dungeonNo, spaceNo, spaceUUID,
                                       spaceBox, spaceMgrBox, toClient=True, toCell=True)

            raidVal.broadcastAllRaidMembersBase(
                'doEnterRaidDungeonSelfCheck',
                (dungeonNo, spaceNo, spaceUUID, spaceBox, spaceMgrBox, src, extraProps))

        # 无论如何, 都需要到raidDungeonStub上释放锁
        dungeonStub.releaseRaidDungeonCreatingLock(raidUUID)

    def _createAndEnterRaidDungeonPostCheck(self, srcPlayerBox, srcPlayerGBID,
                                            raidUUID, dungeonNo, spaceNo, spaceUUID,
                                            src):
        if raidUUID not in self.raidDic:
            return None, gameconst.RaidDungeonErrno.RAIDDUN_RAID_ID_NOT_FOUND

        raidVal = self.raidDic[raidUUID]
        if dungeonNo in raidVal.raidDungeonRecords:
            return None, gameconst.RaidDungeonErrno.RAIDDUN_RAID_ALREADY_EXIST_DUNGEON

        return None, gameconst.RaidDungeonErrno.RAIDDUN_OK

    def onLoadRaidDungeonSpaceReady(self, srcPlayerBox, srcPlayerGBID, raidUUID,
                                    dungeonNo, spaceNo, spaceUUID, spaceBox,
                                    spaceMgrBox, extraProps):
        """团队副本创建完成后回调"""
        INFO_MSG('onLoadRaidDungeonSpaceReady::', srcPlayerBox, srcPlayerGBID,
                  dungeonNo, spaceNo, spaceMgrBox, extraProps)
        src = extraProps.pop('src')     # 这里一定要有src
        self.createAndEnterRaidDungeonPostCheck(srcPlayerBox, srcPlayerGBID, raidUUID,
                                                dungeonNo, spaceNo, spaceUUID, spaceBox,
                                                spaceMgrBox, src, extraProps)

    def onRaidDungeonCompletedCallback(self, raidUUID, dungeonNo, spaceNo, spaceUUID):
        self.clearRaidDungeonInfo(raidUUID, dungeonNo, spaceNo, spaceUUID)
        # 解散团队
        delRaidVal = self.raidDic.get(raidUUID, None)
        if not delRaidVal:
            WARNING_MSG('onRaidDungeonCompletedCallback:: failed, missing raid')
            return

        self.doDisbandRaid(raidUUID, {})

        delRaidVal.clearRaidCacheValToAllPlayers()
        delRaidVal.broadcastAllRaidMembersClient('onDisbandRaid', (raidUUID, ))

    def clearRaidDungeonInfo(self, raidUUID, dungeonNo, spaceNo, spaceUUID):
        _, err = self._clearRaidDungeonInfo(raidUUID, dungeonNo, spaceNo, spaceUUID)
        if err != gameconst.RaidDungeonErrno.RAIDDUN_OK:
            WARNING_MSG('clearRaidDungeonInfo:: missing with err, {}'.format(err))

    def _clearRaidDungeonInfo(self, raidUUID, dungeonNo, spaceNo, spaceUUID):
        if raidUUID not in self.raidDic:
            return None, gameconst.RaidDungeonErrno.RAIDDUN_RAID_ID_NOT_FOUND

        raidVal = self.raidDic[raidUUID]
        raidVal.clearRaidDungeonInfo(dungeonNo, spaceNo, spaceUUID, toCell=True, toClient=True)
        return None, gameconst.RaidDungeonErrno.RAIDDUN_OK

    # ----------------------------------------------------------------------
    def queryEliteMonsteBelongName(self, monsterBox, raidUUID):
        raidVal = self.raidDic.get(raidUUID)
        if not raidVal:
            return
        INFO_MSG('queryEliteMonsteBelongName:', raidUUID)
        monsterBox.setMonsterBelongRaidName(raidUUID, raidVal.getRaidLeader().playerName)
        return

    def broadRaidMemMessage(self, raidUUID, msgId, msgArgs):
        DEBUG_MSG('broadRaidMemMessage:', raidUUID, msgId, msgArgs)
        raidVal = self.raidDic.get(raidUUID)
        if not raidVal:
            return
        raidVal.broadcastAllRaidMembersBase('onMessagePre', (msgId, msgArgs))
        return

    def broadRaidMemMessage_localCross(self, raidUUID, msgId, msgArgs):
        DEBUG_MSG('broadRaidMemMessage_localCross:', raidUUID, msgId, msgArgs)
        raidVal = self.raidDic.get(raidUUID)
        if not raidVal:
            return
        raidVal.broadcastAllRaidMembersBase('onMessagePre_localCross', (msgId, msgArgs))
        return

    # ----------------------------------------------------------------------
    # Raid Follow
    def followRaidLeader(self, srcPlayerBox, raidUUID, srcPlayerGBID):
        _, err = self._followRaidLeader(srcPlayerBox, raidUUID, srcPlayerGBID)
        if err != gameconst.RaidErrno.RAID_OK:
            WARNING_MSG('followRaidLeader:: failed, {}'.format(err))

    def _followRaidLeader(self, srcPlayerBox, raidUUID, srcPlayerGBID):
        if raidUUID not in self.raidDic:
            return None, gameconst.RaidErrno.RAID_RAID_ID_NOT_FOUND

        raidVal = self.raidDic[raidUUID]
        if srcPlayerGBID == raidVal.raidLeaderGBID:
            return None, gameconst.RaidErrno.RAID_IS_RAID_LEADER

        srcPlayerTeamIDX = raidVal.getRaidTeamIDX(srcPlayerGBID)
        if not srcPlayerTeamIDX:
            return None, gameconst.RaidErrno.RAID_TEAM_IDX_NOT_FOUND

        raidVal.onMemberFollowChanged(srcPlayerGBID, True)
        return None, gameconst.RaidErrno.RAID_OK

    def cancelFollowRaidLeader(self, srcPlayerBox, raidUUID, srcPlayerGBID):
        _, err = self._cancelFollowRaidLeader(srcPlayerBox, raidUUID, srcPlayerGBID)
        if err != gameconst.RaidErrno.RAID_OK:
            WARNING_MSG('cancelFollowRaidLeader:: failed, {}'.format(err))

    def _cancelFollowRaidLeader(self, srcPlayerBox, raidUUID, srcPlayerGBID):
        if raidUUID not in self.raidDic:
            return None, gameconst.RaidErrno.RAID_RAID_ID_NOT_FOUND

        raidVal = self.raidDic[raidUUID]
        # 这里拦截需要判断玩家是否在队伍里的原因是，不在队伍里，就不用通知了
        srcPlayerTeamIDX = raidVal.getRaidTeamIDX(srcPlayerGBID)
        if not srcPlayerTeamIDX:
            return None, gameconst.RaidErrno.RAID_TEAM_IDX_NOT_FOUND

        raidVal.onMemberFollowChanged(srcPlayerGBID, False)
        return None, gameconst.RaidErrno.RAID_OK

    def askAllMemberFollow(self, srcPlayerBox, raidUUID, srcPlayerGBID, spaceNo, pos):
        _, err = self._askAllMemberFollow(srcPlayerBox, raidUUID, srcPlayerGBID, spaceNo, pos)
        if err != gameconst.RaidErrno.RAID_OK:
            WARNING_MSG('askAllMemberFollow:: failed, {}'.format(err))

    def _askAllMemberFollow(self, srcPlayerBox, raidUUID, srcPlayerGBID, spaceNo, pos):
        if raidUUID not in self.raidDic:
            return None, gameconst.RaidErrno.RAID_RAID_ID_NOT_FOUND

        raidVal = self.raidDic[raidUUID]
        for teamIDX, memberGBID, memberVal in raidVal.iterGetRaidMember():
            if not memberVal.bOnline:
                continue

            if memberGBID == raidVal.raidLeaderGBID:
                continue

            #if formula.spaceForbidTeamFollow(memberVal.spaceNo):
            #    continue

            if not (memberVal.playerBox and memberVal.playerBox.client):
                WARNING_MSG('_askAllMemberFollow::raidMember has no client', teamIDX, memberGBID, memberVal.playerBox)
                continue

            memberVal.playerBox.client.onFollowTeamCaptainAsk(spaceNo, pos)

        srcPlayerBox.onMessagePre(RAID_CONST.datas["raid_captainSummonDone_msg"]["value"], [])
        return None, gameconst.RaidErrno.RAID_OK

    def askOneMemberFollow(self, srcPlayerBox, raidUUID, srcPlayerGBID, askPlayerGBID):
        _, err = self._askOneMemberFollow(srcPlayerBox, raidUUID, srcPlayerGBID, askPlayerGBID)
        if err != gameconst.RaidErrno.RAID_OK:
            WARNING_MSG('askOneMemberFollow:: failed, {}'.format(err))

    def _askOneMemberFollow(self, srcPlayerBox, raidUUID, srcPlayerGBID, askPlayerGBID):
        if raidUUID not in self.raidDic:
            return None, gameconst.RaidErrno.RAID_RAID_ID_NOT_FOUND

        raidVal = self.raidDic[raidUUID]
        if srcPlayerGBID != raidVal.raidLeaderGBID:
            return None, gameconst.RaidErrno.RAID_NOT_RAID_LEADER

        askPlayerTeamIDX = raidVal.getRaidTeamIDX(askPlayerGBID)
        if not askPlayerTeamIDX:
            return None, gameconst.RaidErrno.RAID_TEAM_IDX_NOT_FOUND

        raidTeamVal = raidVal.raidTeamDic[askPlayerTeamIDX]
        if not raidTeamVal.isInTeam(askPlayerGBID):
            return None, gameconst.RaidErrno.RAID_PLAYER_GBID_NOT_FOUND

        raidMemberVal = raidTeamVal.teamPlayerDic[askPlayerGBID]

        if not raidMemberVal.bOnline:
            return None, gameconst.RaidErrno.RAID_TEAM_MEMBER_OFFLINE

        if not (raidMemberVal.playerBox and raidMemberVal.playerBox.client):
            return None, gameconst.RaidErrno.RAID_TEAM_MEMBER_OFFLINE

        raidMemberVal.playerBox.cell.onAskedFollowCaptain()
        return None, gameconst.RaidErrno.RAID_OK

    def cancelAllMemberFollow(self, srcPlayerBox, raidUUID, srcPlayerGBID):
        _, err = self._cancelAllMemberFollow(srcPlayerBox, raidUUID, srcPlayerGBID)
        if err != gameconst.RaidErrno.RAID_OK:
            WARNING_MSG('cancelAllMemberFollow:: failed, {}'.format(err))

    def _cancelAllMemberFollow(self, srcPlayerBox, raidUUID, srcPlayerGBID):
        if raidUUID not in self.raidDic:
            return None, gameconst.RaidErrno.RAID_RAID_ID_NOT_FOUND

        raidVal = self.raidDic[raidUUID]
        for teamIDX, memberGBID, memberVal in raidVal.iterGetRaidMember():
            if memberGBID == raidVal.raidLeaderGBID:
                continue

            raidVal.onMemberFollowChanged(memberGBID, False)

            if not (memberVal.playerBox and memberVal.playerBox.client):
                WARNING_MSG('_askAllMemberFollow::teamMember has no client', teamIDX, memberGBID, memberVal.playerBox)
                continue

            memberVal.playerBox.cell.onCaptainCancleFollowTeam()

        return None, gameconst.RaidErrno.RAID_OK

    def checkDuoHunItemRaidMemberIds(self,playerBox,raidUUID,targetGbId,targetName,isSendMes,resistType,targetBox):
        if raidUUID not in self.raidDic:
            return
        raidVal = self.raidDic[raidUUID]
        raidMemberIds = []
        for raidTeamVal in raidVal.raidTeamDic.values():
            for raidPlayerVal in raidTeamVal.teamPlayerDic.values():
                if utils.isBoxOffline(raidPlayerVal.playerBox):
                    continue
                if playerBox.id == raidPlayerVal.playerBox.id:
                    continue
                raidMemberIds.append(raidPlayerVal.playerBox.id)

        playerBox.cell.checkDuoHunItemUseful(raidMemberIds,targetGbId,targetName,isSendMes,resistType,targetBox)
    # ----------------------------------------------------------------------

    def getRaidLeaderName(self, raidUUID, box, callBackFuncName, bossId):
        if raidUUID not in self.raidDic:
            return

        raidVal = self.raidDic[raidUUID]

        fn = getattr(box.cell, callBackFuncName, None)
        fn and fn(raidUUID, raidVal.getRaidLeader().playerName, bossId)

    def getRaidByRaidUUID(self, raidUUID):
        if raidUUID not in self.raidDic:
            WARNING_MSG('getRaidByRaidUUID raidUUID error', raidUUID)
            return
        return self.raidDic[raidUUID]

    def raidPrepareAutoMatch(self, raidUUID):
        INFO_MSG('in raidPrepareAutoMatch:', raidUUID)
        raidVal = self.getRaidByRaidUUID(raidUUID)
        if not raidVal:
            return
        if not raidVal.checkRaidTarget(raidVal.raidMinLevel, raidVal.raidMinScore):
            return
        if raidVal.isRaidFull():
            WARNING_MSG('in raidPrepareAutoMatch, raid full:', raidVal)
            raidVal.getRaidLeaderBox().onMessagePre(TMMCD.datas['teamMatch_raidFullMsg']['value'], [])
            return
        raidVal.startAutoMatch()

    def raidPrepareStopAutoMatch(self, raidUUID):
        INFO_MSG('in raidPrepareStopAutoMatch:', raidUUID)
        raidVal = self.getRaidByRaidUUID(raidUUID)
        if not raidVal:
            return
        raidVal.stopAutoMatch()

    def onRaidAutoMatchTimeout(self, randUUID):
        INFO_MSG('in onRaidAutoMatchTimeout:', randUUID)
        teamVal = self.getRaidByRaidUUID(randUUID)
        if not teamVal:
            return
        teamVal.stopAutoMatch(timeout=True)
        return

    def newRaidPlayerMatched(self, raidUUID, playerProps):
        teamVal = self.getRaidByRaidUUID(raidUUID)
        INFO_MSG('in newRaidPlayerMatched:', raidUUID, playerProps, teamVal)
        if not teamVal:
            return
        playerProps['joinType'] = gameconst.TeamJoinType.MATCH
        if teamVal.addNewMember(playerProps['playerGbId'], playerProps, toClient=True):
            teamVal.getRaidLeader().playerBox.cell.onMemJoinRaidByAutoMatch(playerProps['playerGbId'])
            if teamVal.isRaidFull():
                INFO_MSG('in newRaidPlayerMatched, raid is full, stop match ~:', raidUUID, playerProps, teamVal)
                teamVal.stopAutoMatch()
        return

    def getRaidList(self, box, raidTarget, checkTime, checkTeamstubNum, sendTeamNum, startTeamStubIndex):
        DEBUG_MSG('in getRaidList:', raidTarget, checkTime, checkTeamstubNum, sendTeamNum, startTeamStubIndex)
        raidList = []
        # 根据队伍的创建时间排序，最晚创建的队伍在最前面
        releaseNum = gameconst.RAID_LSIT_MAX_NUM - sendTeamNum
        sortedDic = sorted(self.raidDic.items(), key=lambda x: x[1].raidCreateTime, reverse=True)
        for _, raidVal in sortedDic:
            if len(raidList) >= releaseNum:
                break
            if raidVal.raidTarget != raidTarget:
                continue
            if raidVal.isRaidFull():
                continue
            if raidVal.isAllMembersOffline():
                continue
            if self.checkInDungeon(raidVal.raidUUID):
                continue
            raidList.append(raidVal.toClientData())
        box.client.onGetRaidList(checkTime, raidTarget, raidList)
        checkTeamstubNum += 1
        sendTeamNum += len(raidList)
        if checkTeamstubNum >= gameconst.RAIDSTUB_CONFIG_NUM:
            box.cell.onGetRaidListFinished(checkTeamstubNum-1, raidTarget)
            return
        if sendTeamNum >= gameconst.RAID_LSIT_MAX_NUM:
            box.cell.onGetRaidListFinished(checkTeamstubNum-1, raidTarget)
            return
        gameengine.getRaidStub(startTeamStubIndex+checkTeamstubNum).getRaidList(box, raidTarget, checkTime,
                                                                       checkTeamstubNum, sendTeamNum, startTeamStubIndex)
        return

    def enterRaidChiefDungeon(self, box, gbId, raidUUID, dungeonNo, extra):
        INFO_MSG('raidStub:enterRaidChiefDungeon::', gbId, dungeonNo, extra)
        dunPlayMode = extra['dungeonPlayMode']
        src = extra['src']

        box.enterRaidDungeon(dungeonNo, src, {
            'dungeonPlayMode': dunPlayMode
        })

    # ------------------------ 标记相关 --------------------------
    def addTeamMarkDataFromTeam(self, raidUUID, markDataInfo):
        INFO_MSG('addTeamMarkDataFromTeam: ', raidUUID, markDataInfo)
        if raidUUID not in self.raidDic:
            return

        raidVal = self.raidDic[raidUUID]
        raidVal.addRaidMarkMemberFromData(markDataInfo)

    def reqAddRaidMarkMember(self, raidUUID, playerBox, type, index, name, gbId, entId, pos, box):
        INFO_MSG('reqAddRaidMarkMember: ', raidUUID, playerBox, type, index, name, gbId, entId, pos, box)
        if raidUUID not in self.raidDic:
            return

        # 要先执行删除
        self.reqDelRaidMarkMember(raidUUID, playerBox, type, index)

        raidVal = self.raidDic[raidUUID]
        raidVal.addRaidMarkMember(playerBox, type, index, name, gbId, entId, pos)
        # 记录
        if type == gameconst.TeamMarkType.MARK_ENEMY and entId > 0:
            self.addRaidMarkMonsterRec(raidUUID, entId, index, box)

    def addRaidMarkMonsterRec(self, teamId, entId, index, box):
        # 满了说明处理逻辑有问题，功能暂停
        if len(self.teamMarkMonsterRec) >= 20000:
            INFO_MSG('addRaidMarkMonsterRec, mark monster rec full ', len(self.teamMarkMonsterRec))
            return
        if not self.teamMarkMonsterRec.get(entId, None):
            self.teamMarkMonsterRec[entId] = {0: box}

        if len(self.teamMarkMonsterRec[entId]) >= 10000:
            INFO_MSG('addRaidMarkMonsterRec, mark monster rec full for entId: ', entId, len(self.teamMarkMonsterRec[entId]))
            return
        self.teamMarkMonsterRec[entId][teamId] = index
        INFO_MSG('addRaidMarkMonsterRec, mark monster rec:', entId, teamId, index)

        box.onBeMarkedAsEnemy(teamId, gameconst.TeamType.RAID, index)

    def delMarkMonsterRec(self, teamId, entId):
        if entId not in self.teamMarkMonsterRec:
            return
        if teamId in self.teamMarkMonsterRec[entId]:
            self.teamMarkMonsterRec[entId].pop(teamId)
            INFO_MSG('delMonsterRec, del mark monster rec:', entId, teamId)
            box = self.teamMarkMonsterRec[entId].get(0, None)
            if box:
                box.delBeMarkedAsEnemy(teamId, gameconst.TeamType.TEAM)

        if len(self.teamMarkMonsterRec[entId]) <= 1:
            self.teamMarkMonsterRec.pop(entId)
            INFO_MSG('delMarkMonsterRec, remove mark monster rec box:', entId)

    def reqDelRaidMarkMember(self, raidUUID, playerBox, type, index):
        INFO_MSG('reqDelRaidMarkMember: ', raidUUID, playerBox, type, index)
        if raidUUID not in self.raidDic:
            return

        raidVal = self.raidDic[raidUUID]
        entId = raidVal.delRaidMarkMember(playerBox, type, index)

        self.delMarkMonsterRec(raidUUID, entId)

    def onMarkMonsterDead(self, entId):
        if entId not in self.teamMarkMonsterRec:
            return
        teamInfo = self.teamMarkMonsterRec.get(entId, {})
        INFO_MSG('onMarkMonsterDead, remove mark monster:', entId, teamInfo)
        teamInfo = copy.deepcopy(teamInfo)
        for teamId, index in teamInfo.items():
            self.reqDelRaidMarkMember(teamId, None, gameconst.TeamMarkType.MARK_ENEMY, index)

    def reqChangeRaidOnlyLeader(self, raidUUID, playerBox, bOnlyCapatain):
        INFO_MSG('reqChangeRaidOnlyLeader: ', raidUUID, playerBox, bOnlyCapatain)
        if raidUUID not in self.raidDic:
            return

        raidVal = self.raidDic[raidUUID]
        raidVal.changeRaidOnlyLeader(playerBox, bOnlyCapatain)

    def reqJoinRaid(self, playerBox, raidUUID, password, playerProps):
        raidVal, err = self._reqJoinRaidCheck(raidUUID, password, playerProps)
        # 加入成功，刷新一下成员的cache
        if err != gameconst.RaidErrno.RAID_OK:
            ERROR_MSG("reqJoinRaid, err:", err, playerProps)
            return
        raidVal.refreshRaidCacheValToAllPlayers()

    def _reqJoinRaidCheck(self, raidUUID, password, playerProps):
        raidVal = self.getRaidByRaidUUID(raidUUID)
        INFO_MSG('in _reqJoinRaidCheck:', raidUUID, playerProps, raidVal)
        if not raidVal:
            return None, gameconst.RaidErrno.RAID_RAID_ID_NOT_FOUND

        # 非公开的需要检查一下密码
        if not raidVal.isPublish:
            if raidVal.password != password:
                return None, gameconst.RaidErrno.RAID_PASSWORD_IS_WRONG

        raidTargetInfo = TMACTD.datas.get(raidVal.raidTarget)
        if raidTargetInfo is None:
            ERROR_MSG("_reqJoinRaidCheck, misssing raidTarget", raidVal.raidTarget)
            return None, gameconst.RaidErrno.UNKNOWN
        score = playerProps['score']
        level = playerProps['level']
        cfgMinLv = raidTargetInfo['minLevel']
        cfgMinScore = raidTargetInfo['minScore']
        if level < cfgMinLv:
            return None, gameconst.RaidErrno.RAID_LEVEL_IS_LIMITED
        if score < cfgMinScore:
            return None, gameconst.RaidErrno.RAID_SCORE_LIMITED

        _, err = raidVal.addNewMember(playerProps['playerGbId'], playerProps, toClient=True)

        return raidVal, err

    def setInDungeon(self, raidId):
        raidVal = self.raidDic.get(raidId, None)
        if not raidVal:
            WARNING_MSG('setInDungeon, not found raid:', raidId)
            return
        raidVal.isInDungeon = True

    def checkInDungeon(self, raidId):
        raidVal = self.raidDic.get(raidId, None)
        if not raidVal:
            WARNING_MSG('setInDungeon, not found raid:', raidId)
            return False
        return raidVal.isInDungeon
