# coding: utf-8
import gameglobal
from KBEDebug import *
import KBEngine


import gameengine
import gameconst
import gameconfig
import gametimer
import dataUtils
import utils

import iBaseNoCell
import iGlobal
import iTimer

import message_Message_def as M_M_DD
import userType
import raid
import raid_raidConst as RAID_CONST
import teamMatch_matchConfig as TMMCD
import teamMatch_activity as TMACTD
import teamDunChallenge_config as TDC_CFG
import teamMatch_matchConfig as TM_MCD
import copy

class _RaidTeamMemberJoinRecordVal(userType.UserSingleType):
    def __init__(self, playerJoinVal, memberCheckDic):
        self.memberCheckDic = memberCheckDic
        self.playerJoinVal = playerJoinVal
        self.timerId = 0

    def _lateReload(self):
        self.playerJoinVal.reloadScript()
        return


class _RaidStubJoinRecordCheckMixin(object):

    def _initTeamMemberJoinRecord(self, raidUUID, teamUUID, playerJoinVal, memberDic, timeout=5):
        _v = _RaidTeamMemberJoinRecordVal(playerJoinVal, memberDic)
        self.raidTeamMembersJoinRecordsDic.setdefault(raidUUID, {})
        self.raidTeamMembersJoinRecordsDic[raidUUID][teamUUID] = _v
        if timeout > 0:
            tid = self.asyncCallbackAfter(timeout, gametimer.TIMER_TAG_POP_TEAM_MEMBER_JOIN_RECORD)._doPopTeamMemberJoinRecord(raidUUID, teamUUID)
            _v.timerId = tid
        return _v

    def _getTeamMemberJoinRecord(self, raidUUID, teamUUID, default=None):
        return self.raidTeamMembersJoinRecordsDic.get(raidUUID, {}).get(teamUUID, default)

    def _doPopTeamMemberJoinRecord(self, raidUUID, teamUUID, default=None):
        _v = self.raidTeamMembersJoinRecordsDic.get(raidUUID, {}).pop(teamUUID, default)
        _v and _v.timerId and self.cancelTimerCB(_v.timerId, gametimer.TIMER_TAG_POP_TEAM_MEMBER_JOIN_RECORD)
        return _v


class _RaidTeamMemberInviteRecordVal(userType.UserSingleType):
    def __init__(self, memberNum, memberCheckDic):
        self.memberNum = memberNum
        self.memberCheckDic = memberCheckDic
        self.timerId = 0
        self.captainGBID = 0

    def isAllChecked(self):
        return len(self.memberCheckDic) >= self.memberNum


class _RaidStubInviteRecordsCheckMixin(object):

    def _initTeamMemberInviteRecord(self, raidUUID, teamUUID, recordID, memberNum, memberDic, timeout=3, force=False, **kwargs):
        _ov = self._getTeamMemberInviteRecord(raidUUID, teamUUID, recordID)
        if _ov is not None and not force:
            return _ov

        _v = _RaidTeamMemberInviteRecordVal(memberNum, memberDic)
        self.raidTeamMembersInviteRecordsDic.setdefault(raidUUID, {}).setdefault(teamUUID, {})

        self.raidTeamMembersInviteRecordsDic[raidUUID][teamUUID][recordID] = _v
        if timeout > 0:
            tid = self.asyncCallbackAfter(timeout, gametimer.TIMER_TAG_POP_TEAM_MEMBER_INVITE_RECORD)._popTeamMemberInviteRecord(raidUUID, teamUUID, recordID)
            _v.timerId = tid
        return _v

    def _getTeamMemberInviteRecord(self, raidUUID, teamUUID, recordID, default=None):
        return self.raidTeamMembersInviteRecordsDic\
            .get(raidUUID, {})\
            .get(teamUUID, {})\
            .get(recordID, default)

    def _popTeamMemberInviteRecord(self, raidUUID, teamUUID, recordID, default=None):
        _v = self.raidTeamMembersInviteRecordsDic.get(raidUUID, {}).get(teamUUID, {}).pop(recordID, default)
        _v and _v.timerId and self.cancelTimerCB(_v.timerId, gametimer.TIMER_TAG_POP_TEAM_MEMBER_INVITE_RECORD)
        return _v


class _RaidStandbyCheckerVal(userType.UserSingleType):
    def __init__(self, checkBoxesDic, trueCount=0, falseCount=0, unknownCount=0,\
                 enterSrc=gameconst.RaidDungeonStandbyCheckSrcEnum.DEFAULT,\
                 extraProps=None):

        self.timerId = 0
        self.checkBoxesDic = checkBoxesDic
        # count
        self.trueCount = trueCount
        self.unknownCount = unknownCount
        self.falseCount = falseCount
        # source
        self.extraProps = extraProps or {}
        self.enterSrc = enterSrc

    def isChecked(self, gbId):
        return self.checkBoxesDic[gbId] is not None

    @property
    def checkNum(self):
        return len(self.checkBoxesDic)

    def isAllChecked(self):
        return self.unknownCount <= 0

    def checkIt(self, playerGBID, checkResult):
        if self.checkBoxesDic.get(playerGBID, None) is not None:
            LOG_ERR('_RaidStandbyCheckerVal::checkIt:: already checked')
            return

        checkResult = bool(checkResult)
        self.checkBoxesDic[playerGBID] = checkResult

        if checkResult:
            self.trueCount += 1
        else:
            self.falseCount += 1

        self.unknownCount -= 1
        return checkResult

    def isAllCheckSuccess(self):
        return self.trueCount >= self.checkNum and \
               not self.falseCount and \
               not self.unknownCount

    def getCheckResult(self):
        _t, _f, _n = [], [], []
        for _gbId, _checkResult in self.checkBoxesDic.items():
            if _checkResult is None:
                _x = _n
            elif not _checkResult:
                _x = _f
            else:
                _x = _t
            _x.append(_gbId)
        return _t, _f, _n


class _RaidStubStandbyCheckerMixin(object):

    def _initStanbyCheckerRecord(self, raidUUID, checkBoxesDic, trueCount,\
                                 falseCount, unknownCount, checkSrc,\
                                 cbFn='', cbArgs=(), timeout=30, force=False):
        _ov = self._fetchStandbyCheckerRecord(raidUUID)
        if _ov is not None and not force:
            return _ov

        _v = _RaidStandbyCheckerVal(checkBoxesDic, trueCount, falseCount, unknownCount, checkSrc)
        self.raidStandbyCheckerDict[raidUUID] = _v
        if timeout > 0 and cbFn:
            tid = self.addTimerCB(timeout, cbFn, cbArgs, gametimer.TIMER_TAG_INIT_STANBY_CHECKER_RECORD)
            _v.timerId = tid
        return _v

    def _fetchStandbyCheckerRecord(self, raidUUID, default=None):
        return self.raidStandbyCheckerDict.get(raidUUID, default)

    def _popStandbyCheckerRecord(self, raidUUID, default=None):
        _v = self.raidStandbyCheckerDict.pop(raidUUID, default)
        if _v and _v.timerId:
            self.cancelTimerCB(_v.timerId, gametimer.TIMER_TAG_INIT_STANBY_CHECKER_RECORD)
        return _v


class RaidStub(iGlobal.IGlobal, iBaseNoCell.IBaseNoCell, iTimer.ITimer,
               _RaidStubJoinRecordCheckMixin, _RaidStubInviteRecordsCheckMixin,
               _RaidStubStandbyCheckerMixin):
    """  team raid stub """

    def __init__(self):
        super(RaidStub, self).__init__()
        self.raidDict = {}       # type: dict[int, raid.RaidVal]
        self.raidTeamMembersJoinRecordsDic = {}
        self.raidTeamMembersInviteRecordsDic = {}
        self.raidStandbyCheckerDict = {}
        self.teamMarkMonsterRec = {}

    @property
    def raidJoinRecordTimeout(self):
        return RAID_CONST.datas['raidApplyDuration']['value'] * 60

    def doNext(self):
        gameglobal.localBaseApp.fullPrepare(self.classname())

    def refreshRaidCache(self, raidUUID, playerGBIDs, extraProps):
        LOG_INFO('refreshRaidCache 0::', raidUUID, playerGBIDs, extraProps)

        # 没人需要处理的，直接结束
        if not playerGBIDs:
            LOG_INFO('refreshRaidCache 1:: no refresh player: ')
            return
        
        raidVal = self.raidDict.get(raidUUID, None)
        if not raidVal:
            LOG_ERR('refreshRaidCache 2:: check failed, {}'.format(gameconst.RaidErrno.ENUM_RAID_RAID_ID_NOT_FOUND))
            return

        _checkBox = set(playerGBIDs)
        playerRaidCacheVal = None
        playerGBIDs = list(_checkBox)
        for raidTeamVal in raidVal.raidTeamDic.values():
            for playerGBID in playerGBIDs:
                raidPlayerVal = raidTeamVal.teamPlayerDict.get(playerGBID, None)
                if not raidPlayerVal:
                    continue
                LOG_INFO('refreshRaidCache 3:: force fresh avatar raidCache: ', raidPlayerVal.playerGbId)
                # 延迟处理
                if not playerRaidCacheVal:
                    playerRaidCacheVal = raidVal._buildPlayerRaidCacheVal()

                if raidPlayerVal.bOnline and raidPlayerVal.playerBox and raidPlayerVal.playerBox.cell:
                    LOG_INFO('refreshRaidCache 4:: force fresh avatar raidCache: ', raidPlayerVal.playerGbId)
                    raidPlayerVal.playerBox.cell.onRefreshPlayerRaidCacheVal(playerRaidCacheVal)
                _checkBox.remove(playerGBID)
                
        # 处理不在队伍里的玩家，刷新空缓存
        if _checkBox:
            playerRaidEmptyCacheVal = raid.PlayerRaidCacheVal()
            LOG_INFO('refreshRaidCache 5:: force clear avatars raidCache: ', _checkBox)
            gameengine\
                .getGlobalBase('PlayerStub')\
                .doOnOthersCell(
                    list(_checkBox), 
                    'onRefreshPlayerRaidCacheVal', 
                    (playerRaidEmptyCacheVal, ), 
                    None, 
                    '', 
                    ())

    def onTimer(self, tid, userData):
        self._onTimerTrigger(tid, userData)
        if utils.isBelongTimerTag(userData):
            self._onTimerCallback(tid)

    def onPlayerIsOffline(self, offlineGbId, gbId, playerName):
        """异步调用方法时玩家下线后回调"""
        LOG_INFO('onPlayerIsOffline::', offlineGbId, gbId, playerName)
        gameengine.getGlobalBase('PlayerStub').doOnOthersBase(
            [gbId], 
            'onMessagePre', 
            (M_M_DD.datas.raid_applicantOffline, [playerName]), 
            None, 
            '', 
            ())

    def onTransfer(self, playerGbId, teamIDX, raidVal, broadcast):
        if raidVal.isEmpty():
            return
        teamVal = raidVal.raidTeamDic[teamIDX]
        playerVal = teamVal.teamPlayerDict[playerGbId]

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
        LOG_INFO('_onLeaderClientDeath::', raidUUID, playerGBID)
        if raidUUID not in self.raidDict:
            LOG_ERR('_onLeaderClientDeath:: failed', raidUUID, playerGBID)
            return

        raidVal = self.raidDict[raidUUID]
        if raidVal.leaderClientDeathTimer > 0:
            self.cancelTimerCB(raidVal.leaderClientDeathTimer, gametimer.TIMER_TAG_LEADER_CLIENT_DEATH)
            raidVal.leaderClientDeathTimer = 0

        if playerGBID != raidVal.raidLeaderGBID:
            LOG_WARN('_onLeaderClientDeath:: failed', raidUUID, playerGBID, raidVal.raidLeaderGBID)
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
        LOG_INFO('onAvatarClientDeath::', raidUUID, teamIDX, playerGBID)
        errno = gameconst.RaidErrno
        _raidVal = None

        def _onAvatarClientOffline():
            nonlocal _raidVal, teamIDX

            if raidUUID not in self.raidDict:
                return None, errno.ENUM_RAID_RAID_ID_NOT_FOUND.initkvbody(source='onAvatarOffline',
                                                                     raidUUID=raidUUID)

            _raidVal = self.raidDict[raidUUID]
            if not teamIDX:
                teamIDX = _raidVal.getRaidTeamIDX(playerGBID)

            if teamIDX not in _raidVal.raidTeamDic:
                return None, errno.ENUM_RAID_TEAM_IDX_NOT_FOUND.initkvbody(source='onAvatarOffline',
                                                                      raidUUID=raidUUID,
                                                                      teamIDX=teamIDX)

            memberVal = _raidVal.raidTeamDic[teamIDX]
            if playerGBID not in memberVal.teamPlayerDict:
                return None, errno.ENUM_RAID_PLAYER_GBID_NOT_FOUND.initkvbody(source='onAvatarOffline',
                                                                         raidUUID=raidUUID,
                                                                         teamIDX=teamIDX,
                                                                         playerGBID=playerGBID)
            playerVal = memberVal.teamPlayerDict[playerGBID]
            playerVal.bOnline = False

            return playerVal, errno.ENUM_RAID_OK

        clientOfflinePlayerVal, err = _onAvatarClientOffline()
        if err != errno.ENUM_RAID_OK:
            LOG_WARN('onAvatarClientDeath:: failed, {}'.format(err))
            return

        if _raidVal.raidLeaderGBID == playerGBID:
            if _raidVal.leaderClientDeathTimer > 0:
                self.cancelTimerCB(_raidVal.leaderClientDeathTimer, gametimer.TIMER_TAG_LEADER_CLIENT_DEATH)

            _raidVal.leaderClientDeathTimer = self.addTimerCB(RAID_CONST.datas["raid_RLDownGradeOfflineTime"]["value"], '_onLeaderClientDeath', (raidUUID, playerGBID, ), gametimer.TIMER_TAG_LEADER_CLIENT_DEATH)

        _raidVal.refreshPlayerPropsValToAllPlayers(teamIDX, playerGBID, clientOfflinePlayerVal, needDel=False)
        _raidVal.broadcastToAllRaidMembersClient('onRaidAvatarOffline', (raidUUID, teamIDX, playerGBID))

        self.leaveRaid(clientOfflinePlayerVal.playerBox, playerGBID, raidUUID, {})

    def onAvatarOffline(self, raidUUID, teamIDX, playerGBID):
        self.onAvatarClientDeath(raidUUID, teamIDX, playerGBID)
        return

    def onAvatarLogin(self, playerBox, playerGBID, raidUUID):
        """团队玩家(客户端)重新登录后回调"""
        LOG_INFO('onAvatarLogin::', playerBox, playerGBID, raidUUID)
        errno = gameconst.RaidErrno

        _raidVal = None
        teamIDX = 0

        def _onAvatarLogin():
            nonlocal teamIDX, _raidVal
            if raidUUID not in self.raidDict:
                return None, errno.ENUM_RAID_RAID_ID_NOT_FOUND.initkvbody(source='onAvatarLogin',
                                                                     raidUUID=raidUUID)

            _raidVal = self.raidDict[raidUUID]
            teamIDX = _raidVal.getRaidTeamIDX(playerGBID)
            if not teamIDX or teamIDX not in _raidVal.raidTeamDic:
                return None, errno.ENUM_RAID_TEAM_IDX_NOT_FOUND.initkvbody(source='onAvatarLogin',
                                                                      raidUUID=raidUUID,
                                                                  teamIDX=teamIDX)

            memberVal = _raidVal.raidTeamDic[teamIDX]
            playerVal = memberVal.teamPlayerDict[playerGBID]
            playerVal.bOnline = True
            playerVal.playerBox = playerBox
            return playerVal, errno.ENUM_RAID_OK

        onlinePlayerVal, err = _onAvatarLogin()
        if err != errno.ENUM_RAID_OK:
            playerBox.cell.onRefreshPlayerRaidCacheVal(raid.PlayerRaidCacheVal())
            LOG_WARN('onAvatarLogin:: cache outdate, clear avatar cache. {}'.format(err))
            return

        if _raidVal.raidLeaderGBID == playerGBID and _raidVal.leaderClientDeathTimer > 0:
            self.cancelTimerCB(_raidVal.leaderClientDeathTimer, gametimer.TIMER_TAG_LEADER_CLIENT_DEATH)
            _raidVal.leaderClientDeathTimer = 0

        playerBox.cell.onRefreshPlayerRaidCacheVal(_raidVal._buildPlayerRaidCacheVal())
        _raidVal.refreshPlayerPropsValToAllPlayers(teamIDX, playerGBID, onlinePlayerVal,
                                                  needDel=False, exclude=(playerGBID, ))

        playerBox.client.onGetRaidData(_raidVal.toClientData())

        _raidVal.broadcastToAllRaidMembersClient(
            'onRaidAvatarLogin', (raidUUID, teamIDX, playerGBID), exclude=(playerGBID, ))

    def updateRaidMemberCacheVal(self, raidUUID, playerBox, playerGBID, playerUpdateProps):
        #LOG_DBG('updateRaidMemberCacheVal::', raidUUID, playerGBID, playerUpdateProps)

        def _updateRaidMemberCacheVal():
            if raidUUID not in self.raidDict:
                return None, gameconst.RaidErrno.ENUM_RAID_RAID_ID_NOT_FOUND.initkvbody(source='updateRaidMemberCacheVal',
                                                                                    raidUUID=raidUUID,
                                                                                    playerGBID=playerGBID)
            _raidVal = self.raidDict[raidUUID]
            teamIDX = _raidVal.getRaidTeamIDX(playerGBID)
            if not teamIDX:
                return None, gameconst.RaidErrno.ENUM_RAID_PLAYER_GBID_NOT_FOUND.initkvbody(source='updateRaidMemberCacheVal',
                                                                                        raidUUID=raidUUID,
                                                                                        teamIDX=teamIDX,
                                                                                        playerGBID=playerGBID)

            memberVal = _raidVal.raidTeamDic[teamIDX].teamPlayerDict[playerGBID]
            memberVal.updateAttr(playerUpdateProps)
            return _raidVal, gameconst.RaidErrno.ENUM_RAID_OK

        updateRaidVal, err = _updateRaidMemberCacheVal()
        if err != gameconst.RaidErrno.ENUM_RAID_OK:
            if err == gameconst.RaidErrno.ENUM_RAID_PLAYER_GBID_NOT_FOUND or err == gameconst.RaidErrno.ENUM_RAID_RAID_ID_NOT_FOUND:
                playerRaidEmptyCacheVal = raid.PlayerRaidCacheVal()
                playerBox.cell.onRefreshPlayerRaidCacheVal(playerRaidEmptyCacheVal)
            LOG_WARN('updateRaidMemberCacheVal:: failed, {}'.format(err))
            return

        LOG_DBG('updateRaidMemberCacheVal:: broadcast ~ ', playerGBID, playerUpdateProps)
        updateRaidVal.updateMemberVolatileAttr(playerGBID, playerUpdateProps)

    def getRaidApplyJoinDic(self, srcPlayerBox, srcPlayerGbId, raidUUID):
        LOG_INFO('getRaidApplyJoinDic::', srcPlayerBox, srcPlayerGbId, raidUUID)
        _, _err = self._getRaidApplyJoinDicCheck(srcPlayerBox, srcPlayerGbId, raidUUID)
        if _err != gameconst.RaidErrno.ENUM_RAID_OK:
            LOG_ERR('getRaidApplyJoinDic:: failed, {}'.format(_err))
            return

        _raidVal = self.raidDict[raidUUID]
        _data = [i.toClientDict() for i in _raidVal.raidApplyJoinDic.values()]
        srcPlayerBox.client.onGetRaidApplyJoinList(raidUUID, _data)

    def _getRaidApplyJoinDicCheck(self, srcPlayerBox, srcPlayerGbId, raidUUID):
        _raidVal = self.raidDict.get(raidUUID, None)
        if not _raidVal:
            return None, gameconst.RaidErrno.ENUM_RAID_RAID_ID_NOT_FOUND

        if _raidVal.raidLeaderGBID != srcPlayerGbId and not _raidVal.isRaidDeputy(srcPlayerGbId):
            return None, gameconst.RaidErrno.ENUM_RAID_NOT_RAID_LEADER_OR_DEPUTY

        return None, gameconst.RaidErrno.ENUM_RAID_OK

    def clearRaidApplyJoinDic(self, srcPlayerBox, srcPlayerGbId, raidUUID):
        LOG_INFO('clearRaidApplyJoinDic::', srcPlayerBox, srcPlayerGbId, raidUUID)
        _, _err = self._clearRaidApplyJoinDicCheckInStub(srcPlayerGbId, raidUUID)
        if _err != gameconst.RaidErrno.ENUM_RAID_OK:
            LOG_ERR('clearRaidApplyJoinDic:: failed, {}'.format(_err))
            return
        self.doClearRaidApplyJoinDic(raidUUID)

    def _clearRaidApplyJoinDicCheckInStub(self, srcPlayerGbId, raidUUID):
        if raidUUID not in self.raidDict:
            return None, gameconst.RaidErrno.ENUM_RAID_RAID_ID_NOT_FOUND
        _raidVal = self.raidDict[raidUUID]

        if _raidVal.raidLeaderGBID != srcPlayerGbId and not _raidVal.isRaidDeputy(srcPlayerGbId):
            return None, gameconst.RaidErrno.ENUM_RAID_NOT_RAID_LEADER_OR_DEPUTY

        return None, gameconst.RaidErrno.ENUM_RAID_OK

    def doClearRaidApplyJoinDic(self, raidUUID):
        LOG_INFO('doClearRaidApplyJoinDic::', raidUUID)
        _raidVal = self.raidDict[raidUUID]

        _singleJoinPlayerGBIDList = []
        teamJoinPlayerGBIDList = []
        for _joinVal in _raidVal.raidApplyJoinDic.values():
            if _joinVal.raidJoinType == gameconst.RaidJoinTypeEnum.SINGLE:
                _singleJoinPlayerGBIDList.append(_joinVal.joinPlayerGBID)
            elif _joinVal.raidJoinType == gameconst.RaidJoinTypeEnum.TEAM:
                teamJoinPlayerGBIDList.append((_joinVal.joinPlayerGBID, _joinVal.joinTeamUUID))

        playerStub = gameengine.getGlobalBase('PlayerStub')
        playerStub.doOnOthersCell(
            _singleJoinPlayerGBIDList, 
            'onJoinListPlayerClearRaidApplyJoinDic',
            (raidUUID, gameconst.RaidJoinTypeEnum.SINGLE, 0), 
            None, 
            '', 
            ())

        for _gbId, teamUUID in teamJoinPlayerGBIDList:
            playerStub.doOnOthersCell([_gbId, ], 'onJoinListPlayerClearRaidApplyJoinDic',
                                      (raidUUID, gameconst.RaidJoinTypeEnum.TEAM, teamUUID), None, '', ())

        _raidVal.clearRaidJoin()

        leaderAndDeputyVal = {_raidVal.getRaidLeader(), _raidVal.getRaidDeputy()}
        for val in leaderAndDeputyVal:
            if val and val.playerBox and val.playerBox.client:
                val.playerBox.client.onClearRaidApplyJoinDic(raidUUID)

    def clearRaidJoinRecords(self, srcPlayerBox, srcPlayerGbId, clearRaidIdList):
        LOG_INFO('clearRaidJoinRecords::', srcPlayerBox, srcPlayerGbId, clearRaidIdList)

        for raidUUID, joinType in clearRaidIdList:
            if raidUUID not in self.raidDict:
                LOG_WARN('clearRaidJoinRecords:: raidUUID not found', raidUUID)
                continue
            _raidVal = self.raidDict[raidUUID]
            _joinVal, err = _raidVal.getRaidJoin(srcPlayerGbId)
            if err != gameconst.RaidErrno.ENUM_RAID_OK:
                LOG_WARN('clearRaidJoinRecords:: get failed, {}'.format(err))
                continue

            if _joinVal.raidJoinType != joinType:
                LOG_WARN('clearRaidJoinRecords:: joinType not match', _joinVal.raidJoinType, joinType)
                continue

            playerJoinVal, err = _raidVal.popRaidJoin(srcPlayerGbId)
            if err != gameconst.RaidErrno.ENUM_RAID_OK:
                LOG_WARN('clearRaidJoinRecords:: pop failed, {}'.format(err))
            elif playerJoinVal.applyTimeoutTimerId:
                self.cancelTimerCB(playerJoinVal.applyTimeoutTimerId,
                                    gametimer.TIMER_TAG_RAID_APPLY_JOIN_TIMEOUT)
                playerJoinVal.applyTimeoutTimerId = 0

            # 刷新对应团队团/副团长客户端的申请列表
            leaderAndDeputyVal = {_raidVal.getRaidLeader(), _raidVal.getRaidDeputy()}
            for val in leaderAndDeputyVal:
                if val:
                    self.getRaidApplyJoinDic(val.playerBox, val.playerGbId, raidUUID)

        if srcPlayerBox and srcPlayerBox.cell:
            srcPlayerBox.cell.onClearRaidJoinRecords(clearRaidIdList)

    def getRaidAllMembersAttrs(self, srcPlayerBox, srcPlayerGbId, raidUUID, memberGBIDList, extraProps):
        raidMemberAttrsList, err = self._getRaidAllMembersAttrs(raidUUID, set(memberGBIDList))
        if err != gameconst.RaidErrno.ENUM_RAID_OK:
            LOG_WARN('getRaidAllMembersAttrs:: client get attrs failed, {}'.format(err),
                        srcPlayerGbId, raidUUID, memberGBIDList)
            return

        while raidMemberAttrsList:
            _raidMemberAttrsList = raidMemberAttrsList[:dataUtils.raidMaxTeamMemberCount()]
            raidMemberAttrsList = raidMemberAttrsList[dataUtils.raidMaxTeamMemberCount():]
            srcPlayerBox.client.onGetRaidAllMembersAttrs(raidUUID, _raidMemberAttrsList)

    def _getRaidAllMembersAttrs(self, raidUUID, memberGBIDList):
        if raidUUID not in self.raidDict:
            return None, gameconst.RaidErrno.ENUM_RAID_RAID_ID_NOT_FOUND

        _raidVal = self.raidDict[raidUUID]
        raidMemberAttrsList = []
        for raidTeamVal in _raidVal.raidTeamDic.values():
            for raidMemberGBID, raidMemberVal in raidTeamVal.teamPlayerDict.items():
                if raidMemberGBID in memberGBIDList:
                    raidMemberAttrsList.append(raidMemberVal.toClientData())

        return raidMemberAttrsList, gameconst.RaidErrno.ENUM_RAID_OK

    def createRaidLonely(self, srcPlayerBox, srcPlayerGbId, raidUUID, capacity, memberPropsList, extraProps, raidTarget, minLevel, minScore, recruitInfo, password, isAutoExpedition):
        LOG_INFO('createRaidLonely::', srcPlayerBox, srcPlayerGbId, raidUUID, capacity, memberPropsList, extraProps, raidTarget, minLevel, minScore, recruitInfo, password, isAutoExpedition)
        _, err = self._createRaid(srcPlayerBox, srcPlayerGbId, raidUUID, capacity, memberPropsList, raidTarget, minLevel, minScore, recruitInfo, password, isAutoExpedition, extraProps)
        if err != gameconst.RaidErrno.ENUM_RAID_OK:
            LOG_ERR('createRaid:: failed, {}'.format(err))
            return

    def createRaid(self, srcPlayerBox, srcPlayerGbId, raidUUID, capacity, memberPropsList, extraProps):
        LOG_INFO('createRaid::', srcPlayerBox, srcPlayerGbId, raidUUID, capacity, memberPropsList, extraProps)
        _, err = self._createRaid(srcPlayerBox, srcPlayerGbId, raidUUID, capacity, memberPropsList, 1, 0, 0, TMMCD.datas["raidTeamTitleDes"]["value"], '', False, extraProps)
        if err != gameconst.RaidErrno.ENUM_RAID_OK:
            LOG_ERR('createRaid:: failed, {}'.format(err))
            return

    def checkAutoStart(self, raidUUID):
        _raidVal = self.raidDict.get(raidUUID)
        if not _raidVal:
            return

        if _raidVal.autoStartTimer > 0:
            self.cancelTimerCB(_raidVal.autoStartTimer, gametimer.TIMER_TAG_RAID_AUTO_START)
            _raidVal.autoStartTimer = 0

        if _raidVal.isAutoExpedition and _raidVal.raidTarget > gameconst.PARE_ACTIVITY_ID:
            if _raidVal.isRaidFull():
                captainBox = _raidVal.getRaidLeaderBox()
                if captainBox and captainBox.cell:
                    captainBox.cell.autoStartChiefDungeon()
                    return
            _raidVal.autoStartTimer = self.addTimerCB(5, 'checkAutoStart', (raidUUID,), gametimer.TIMER_TAG_RAID_AUTO_START)

    def _createRaid(self, srcPlayerBox, srcPlayerGbId, raidUUID, capacity, memberPropsList, raidTarget, minLevel, minScore, recruitInfo, password, isAutoExpedition, extraProps):
        raidLeaderGBID = srcPlayerGbId

        if not dataUtils.isRaidCapacityValidate(extraProps['raidTarget'], capacity):
            return None, gameconst.RaidErrno.ENUM_RAID_UNKNOWN_CAPACITY.initkvbody(source='_createRaid',
                                                                              raidUUID=raidUUID,
                                                                              capacity=capacity)

        if raidUUID in self.raidDict:
            return None, gameconst.RaidErrno.ENUM_RAID_RAID_ID_REPEAT.initkvbody(source='_createRaid',
                                                                            raidUUID=raidUUID)
        siegeWarCamp = 0
        if memberPropsList:
            siegeWarCamp = memberPropsList[0]['siegeWarCamp']
        if gameconfig.isCrossServer() and siegeWarCamp != 0:
            raidTarget = gameconst.SIEGEWAR_PARE_ACTIVITY_ID
        _raidVal = raid.RaidVal(raidUUID=raidUUID, raidCapacity=capacity, siegeWarCamp=siegeWarCamp, raidTarget=raidTarget)
        teamIDX = 1
        raidTeamVal, err = _raidVal.addNewTeam(teamIDX)
        if err != gameconst.RaidErrno.ENUM_RAID_OK:
            LOG_ERR('_createRaid:: create Team failed, {}'.format(err))
            return None, err

        for memberProps in memberPropsList:
            _, err = raidTeamVal.addTeamMember(memberProps['playerGbId'], memberProps)
            if err != gameconst.RaidErrno.ENUM_RAID_OK:
                LOG_ERR('_createRaid:: add team member failed, {}'.format(err))
                return None, err
            _raidVal.broadcastToAllRaidMembersCell('onRaidAddNewMember', (memberProps['playerBox'].id, extraProps.get('joinType', gameconst.TeamJoinType.DEFAULT)), ())
            
        _, err = _raidVal.setRaidLeader(raidLeaderGBID, teamIDX)
        if err != gameconst.RaidErrno.ENUM_RAID_OK:
            LOG_ERR('_createRaid:: set raid leader failed, {}'.format(err))
            return None, err

        self.raidDict[raidUUID] = _raidVal
        
        _raidVal.isPublish = False

        if _raidVal.raidTarget > 0 and len(_raidVal.password) == 0:
            _raidVal.isPublish = True
        
        _raidVal.raidMinLevel = minLevel
        _raidVal.raidMinScore = minScore
        _raidVal.recruitInfo = recruitInfo
        _raidVal.password = password
        _raidVal.isAutoExpedition = isAutoExpedition

        _raidVal.refreshRaidCacheValToAllPlayers()
        _raidVal.broadcastToAllRaidMembersClient('onCreateRaid', (_raidVal.toClientData(), ))
        _raidVal.broadcastAllRaidMembersBase('onMessagePre', (RAID_CONST.datas["raidCreated_chatMsg"]["value"], []))

        if len(_raidVal.password) == 0:
            if _raidVal.raidTarget > gameconst.PARE_ACTIVITY_ID:
                self.raidPrepareAutoMatch(raidUUID)
        self.checkAutoStart(raidUUID)

        return _raidVal, gameconst.RaidErrno.ENUM_RAID_OK

    def disbandRaid(self, srcPlayerBox, srcPlayerGbId, raidUUID, extra):
        LOG_INFO('disbandRaid::', srcPlayerBox, srcPlayerGbId, raidUUID, extra)
        _delRaidVal, err = self._disbandRaidCheck(srcPlayerBox, srcPlayerGbId, raidUUID)
        if err != gameconst.RaidErrno.ENUM_RAID_OK:
            LOG_ERR('disbandRaid:: failed, {}'.format(err))
            return

        self.doDisbandRaid(raidUUID, extra)

        _delRaidVal.clearRaidCacheValToAllPlayers()
        _delRaidVal.broadcastToAllRaidMembersClient('onDisbandRaid', (raidUUID, ))
        '''
        gameengine.getGlobalBase('EliteInvasionStub').onEliteInvRaidDisband(raidUUID)
        '''

    def _disbandRaidCheck(self, srcPlayerBox, srcPlayerGbId, raidUUID):
        leaderGBID = srcPlayerGbId

        if raidUUID not in self.raidDict:
            return None, gameconst.RaidErrno.ENUM_RAID_RAID_ID_NOT_FOUND.initkvbody(
                source='_disbandRaid', raidUUID=raidUUID)

        _raidVal = self.raidDict[raidUUID]
        if _raidVal.raidLeaderGBID != leaderGBID:
            return None, gameconst.RaidErrno.ENUM_RAID_NOT_RAID_LEADER.initkvbody(
                source='_disbandRaid', orgLeaderGBID=leaderGBID, crtLeaderGBID=_raidVal.raidLeaderGBID)

        return _raidVal, gameconst.RaidErrno.ENUM_RAID_OK

    def doDisbandRaid(self, raidUUID, extra):
        LOG_INFO('doDisbandRaid::', raidUUID, extra)
        # when disband raid, try clear all join val first
        self.doClearRaidApplyJoinDic(raidUUID)
        _raidVal = self.raidDict.pop(raidUUID)

        try:
            _raidVal.clearMarkRecord(self)
        except Exception as e:
            LOG_ERR('doDisbandRaid:: clearMarkRecord exception: {}'.format(e))

        # 团队解散了，从匹配队列里停止
        if _raidVal.raidAutoMatchTime > 0:
            _raidVal.raidAutoMatchTime = 0
            gameengine.getGlobalBase('RaidMatchStub').raidStopAutoMatch(raidUUID)

        if _raidVal.leaderClientDeathTimer > 0:
            self.cancelTimerCB(_raidVal.leaderClientDeathTimer, gametimer.TIMER_TAG_LEADER_CLIENT_DEATH)
            _raidVal.leaderClientDeathTimer = 0
        for dungeonNo, dunVal in _raidVal.raidDungeonRecords.items():
            stub = gameengine.getDungeonStubBySpaceNo(dunVal.spaceNo)
            LOG_WARN('doDisbandRaid:: disbandRaid and complete dungeon in force ', dungeonNo, dunVal)
            stub.completeRaidDungeon(dunVal.spaceNo, raidUUID, False, 0, gameconst.DunegonCompleteReasonType.LEAVE)

    def applyJoinRaidLonely(self, joinedPlayerBox, joinedPlayerGbId, joinedPlayerProps, raidUUID, extraProps, password, ignorePassword, applySource):
        LOG_INFO('applyJoinRaidLonely::', joinedPlayerBox, joinedPlayerGbId, joinedPlayerProps, raidUUID, extraProps, password, ignorePassword, applySource)
        _playerJoinVal, err = self._applyJoinRaidLonely(joinedPlayerGbId, joinedPlayerProps, raidUUID, extraProps, password, ignorePassword, applySource)
        if err != gameconst.RaidErrno.ENUM_RAID_OK:
            return

        if joinedPlayerBox and joinedPlayerBox.cell:
            joinedPlayerBox.cell.onApplyJoinRaidLonelySucc(joinedPlayerGbId, raidUUID, extraProps)

        leaderAndDeputyVal = {self.raidDict[raidUUID].getRaidLeader(), self.raidDict[raidUUID].getRaidDeputy()}
        for val in leaderAndDeputyVal:
            if val and val.playerBox and val.playerBox.cell:
                val.playerBox.cell.onLeaderProcessApplyJoinRaidLonely(
                    joinedPlayerBox, joinedPlayerGbId, _playerJoinVal.toClientDict(), raidUUID, extraProps)

        _playerJoinVal.applyTimeoutTimerId = self.asyncCallbackAfter(
            self.raidJoinRecordTimeout, tag=gametimer.TIMER_TAG_RAID_APPLY_JOIN_TIMEOUT
        )._onRaidApplyJoinRecordTimeout(raidUUID, joinedPlayerGbId)

    def _applyJoinRaidLonely(self, joinedPlayerGbId, joinedPlayerProps, raidUUID, extraProps, password, ignorePassword, applySource):
        box = joinedPlayerProps['playerBox']
        _raidVal = self.raidDict.get(raidUUID, None)
        if not _raidVal:
            box.client and box.client.onApplyJoinRaidLonelyFailed(gameconst.TeamApplyResult.RAID_IS_NOT_EXIST, 0, 0, 0, '', applySource)
            return None, gameconst.RaidErrno.ENUM_RAID_RAID_ID_NOT_FOUND.initkvbody(
                source='_applyJoinRaidLonely', raidUUID=raidUUID)

        isRaidUIVisibleId = extraProps.get('isRaidUIVisibleId', True)
        isRaidDungeonUIVisibleId = extraProps.get('isRaidDungeonUIVisibleId', True)

        if _raidVal.raidTarget > gameconst.PARE_ACTIVITY_ID:
            if not isRaidUIVisibleId:
                box.CheckFuncConditions(dataUtils.getRaidConstDataValue("raidUIVisibleId"))
                box.client and box.client.onApplyJoinRaidLonelyFailed(gameconst.TeamApplyResult.RAID_APPLY_RAID_UI_IS_NOT_VISIBLE, _raidVal.raidUUID, _raidVal.raidMinLevel, _raidVal.raidMinScore, _raidVal.password, applySource)
                return None, gameconst.RaidErrno.ENUM_RAID_LEVEL_IS_ILLEGAL.initkvbody(
                    source='_applyJoinRaidLonely', raidUUID=raidUUID)
            if not isRaidDungeonUIVisibleId:
                box.CheckFuncConditions(dataUtils.getRaidConstDataValue("raidDungeonUIVisibleId"))
                box.client and box.client.onApplyJoinRaidLonelyFailed(gameconst.TeamApplyResult.RAID_APPLY_RAID_UI_IS_NOT_VISIBLE, _raidVal.raidUUID, _raidVal.raidMinLevel, _raidVal.raidMinScore, _raidVal.password, applySource)
                return None, gameconst.RaidErrno.ENUM_RAID_LEVEL_IS_ILLEGAL.initkvbody(
                    source='_applyJoinRaidLonely', raidUUID=raidUUID)
            
        level = joinedPlayerProps['level']
        score = joinedPlayerProps['score']

        if self.checkInDungeon(_raidVal.raidUUID):
            box.client and box.client.onApplyJoinRaidLonelyFailed(gameconst.TeamApplyResult.TEAM_APPLY_IS_IN_DUNGEON, _raidVal.raidUUID, _raidVal.raidMinLevel, _raidVal.raidMinScore, _raidVal.password, applySource)
            return None, gameconst.RaidErrno.ENUM_RAID_IS_IN_DUNGEON.initkvbody(
                source='_applyJoinRaidLonely', raidUUID=raidUUID)

        if _raidVal.isRaidFull():
            box.client and box.client.onApplyJoinRaidLonelyFailed(gameconst.TeamApplyResult.RAID_IS_FULL, _raidVal.raidUUID, _raidVal.raidMinLevel, _raidVal.raidMinScore, _raidVal.password, applySource)
            return None, gameconst.RaidErrno.ENUM_RAID_RAID_TEAM_IS_FULL.initkvbody(
                source='_applyJoinRaidLonely', raidUUID=raidUUID)

        if _raidVal.isRaidApplyListFull():
            box.client and box.client.onApplyJoinRaidLonelyFailed(gameconst.TeamApplyResult.RAID_APPLY_LIST_IS_FULL, _raidVal.raidUUID, _raidVal.raidMinLevel, _raidVal.raidMinScore, _raidVal.password, applySource)
            return None, gameconst.RaidErrno.ENUM_RAID_APPLY_LIST_IS_FULL.initkvbody(
                source='_applyJoinRaidLonely', raidUUID=raidUUID)

        if level < _raidVal.raidMinLevel:
            box.client and box.client.onApplyJoinRaidLonelyFailed(gameconst.TeamApplyResult.TEAM_APPLY_LEVEL_IS_NOT_ENOUGH, _raidVal.raidUUID, _raidVal.raidMinLevel, _raidVal.raidMinScore, _raidVal.password, applySource)
            return None, gameconst.RaidErrno.ENUM_RAID_LEVEL_IS_ILLEGAL.initkvbody(
                source='_applyJoinRaidLonely', raidUUID=raidUUID)

        if score < _raidVal.raidMinScore:
            box.client and box.client.onApplyJoinRaidLonelyFailed(gameconst.TeamApplyResult.TEAM_APPLY_SCORE_IS_NOT_ENOUGH, _raidVal.raidUUID, _raidVal.raidMinLevel, _raidVal.raidMinScore, _raidVal.password, applySource)
            return None, gameconst.RaidErrno.ENUM_RAID_SOCRE_IS_ILLEGAL.initkvbody(
                source='_applyJoinRaidLonely', raidUUID=raidUUID)

        if not ignorePassword:
            if len(_raidVal.password) > 0:
                if len(password) == 0:
                    box.client and box.client.onApplyJoinRaidLonelyFailed(gameconst.TeamApplyResult.TEAM_APPLY_NEED_PASSWORD, _raidVal.raidUUID, _raidVal.raidMinLevel, _raidVal.raidMinScore, _raidVal.password, applySource)
                    return None, gameconst.RaidErrno.ENUM_RAID_PASSWORD_IS_EMPTY.initkvbody(
                        source='_applyJoinRaidLonely', raidUUID=raidUUID)
                if password != _raidVal.password:
                    box.client and box.client.onApplyJoinRaidLonelyFailed(gameconst.TeamApplyResult.TEAM_APPLY_WRONG_PASSWORD, _raidVal.raidUUID, _raidVal.raidMinLevel, _raidVal.raidMinScore, _raidVal.password, applySource)
                    return None, gameconst.RaidErrno.ENUM_RAID_PASSWORD_IS_ILLEGAL.initkvbody(
                        source='_applyJoinRaidLonely', raidUUID=raidUUID)


        if gameconfig.isCrossServer() and _raidVal.siegeWarCamp != 0 and joinedPlayerProps['siegeWarCamp'] != 0 \
            and _raidVal.siegeWarCamp != joinedPlayerProps['siegeWarCamp']:
            box.client and box.client.onApplyJoinRaidLonelyFailed(gameconst.TeamApplyResult.TEAM_APPLY_FAIL, _raidVal.raidUUID, _raidVal.raidMinLevel, _raidVal.raidMinScore, _raidVal.password, applySource)
            return None, gameconst.RaidErrno.ENUM_RAID_NOT_SAME_SIEGEWAR_CAMP

        playerJoinVal, err = _raidVal.addSingleRaidJoin(
            gbId=joinedPlayerGbId,
            playerName=joinedPlayerProps['playerName'],
            level=joinedPlayerProps['level'],
            school=joinedPlayerProps['school'],
            sex=joinedPlayerProps['sex'],
            score=joinedPlayerProps['score'], 
            applySource=applySource)

        if err != gameconst.RaidErrno.ENUM_RAID_OK:
            box.client and box.client.onApplyJoinRaidLonelyFailed(gameconst.TeamApplyResult.TEAM_APPLY_FAIL, _raidVal.raidUUID, _raidVal.raidMinLevel, _raidVal.raidMinScore, _raidVal.password, applySource)
            return None, err
        box.client and box.client.onApplyJoinRaidLonelyFailed(gameconst.TeamApplyResult.TEAM_APPLY_OK, _raidVal.raidUUID, _raidVal.raidMinLevel, _raidVal.raidMinScore, _raidVal.password, applySource)
        return playerJoinVal, gameconst.RaidErrno.ENUM_RAID_OK

    def applyJoinRaidWithTeam(self, joinCaptainBox, joinedCaptainGBID, teamUUID, raidUUID, memberDataList, extraProps):
        LOG_INFO('applyJoinRaidWithTeam::', joinCaptainBox, joinedCaptainGBID, teamUUID, raidUUID, memberDataList, extraProps)
        _raidPlayerJoinVal, _err = self._applyJoinRaidWithTeam(joinCaptainBox, joinedCaptainGBID, teamUUID, raidUUID, memberDataList, extraProps)
        if _err != gameconst.RaidErrno.ENUM_RAID_OK:
            if _err == gameconst.RaidErrno.ENUM_RAID_APPLY_JOIN_NUMBER_OFR:
                LOG_WARN('applyJoinRaidWithTeam::apply join number out of range', _err)
                if joinCaptainBox:
                    joinCaptainBox.onMessagePre(RAID_CONST.datas["raid_applyFull_msg"]["value"], [])

            elif _err == gameconst.RaidErrno.ENUM_RAID_ALREADY_APPLY_JOIN:
                LOG_WARN('applyJoinRaidWithTeam::already apply join', _err)

            else:
                LOG_ERR('applyJoinRaidWithTeam:: failed, {}'.format(_err))

            return

        if joinCaptainBox and joinCaptainBox.cell:
            joinCaptainBox.cell.onApplyJoinRaidWithTeamSucc(joinedCaptainGBID, teamUUID, raidUUID, extraProps)

        leaderAndDeputyVal = {self.raidDict[raidUUID].getRaidLeader(), self.raidDict[raidUUID].getRaidDeputy()}
        for val in leaderAndDeputyVal:
            if val and val.playerBox and val.playerBox.cell:
                val.playerBox.cell.onLeaderProcessApplyJoinRaidWithTeam(
                    joinCaptainBox, joinedCaptainGBID, _raidPlayerJoinVal.toClientDict(), teamUUID, raidUUID, extraProps)

        _raidPlayerJoinVal.applyTimeoutTimerId = self.asyncCallbackAfter(
            self.raidJoinRecordTimeout, tag=gametimer.TIMER_TAG_RAID_APPLY_JOIN_TIMEOUT
        )._onRaidApplyJoinRecordTimeout(raidUUID, joinedCaptainGBID)

    def _applyJoinRaidWithTeam(self, joinCaptainBox, joinedCaptainGBID, teamUUID, raidUUID, memberDataList, extraProps):
        if raidUUID not in self.raidDict:
            return None, gameconst.RaidErrno.ENUM_RAID_RAID_ID_NOT_FOUND

        _raidVal = self.raidDict[raidUUID]
        if gameconfig.isCrossServer() and _raidVal.siegeWarCamp != 0 and extraProps['siegeWarCamp'] != 0 \
            and _raidVal.siegeWarCamp != extraProps['siegeWarCamp']:
            return None, gameconst.RaidErrno.ENUM_RAID_NOT_SAME_SIEGEWAR_CAMP
        _raidPlayerJoinVal, err = _raidVal.addTeamRaidJoin(captainGBID=joinedCaptainGBID,
                                                         teamUUID=teamUUID,
                                                         memberDataList=memberDataList)
        if err != gameconst.RaidErrno.ENUM_RAID_OK:
            err = err.initkvbody(raidUUID=raidUUID, teamId=teamUUID)
            return None, err

        return _raidPlayerJoinVal, gameconst.RaidErrno.ENUM_RAID_OK

    def _checkOnRaidApplyJoinRecordTimeout(self, raidUUID, primaryGBID):
        if raidUUID not in self.raidDict:
            return None, gameconst.RaidErrno.ENUM_RAID_RAID_ID_NOT_FOUND
        _raidVal = self.raidDict[raidUUID]
        if primaryGBID not in _raidVal.raidApplyJoinDic:
            return None, gameconst.RaidErrno.ENUM_RAID_APPLY_JOIN_STUB_VAL_NOT_FOUND
        return None, gameconst.RaidErrno.ENUM_RAID_OK

    def _onRaidApplyJoinRecordTimeout(self, raidUUID, primaryGBID):
        """入团申请超时, 取出该入团记录"""
        _, err = self._checkOnRaidApplyJoinRecordTimeout(raidUUID, primaryGBID)
        if err != gameconst.RaidErrno.ENUM_RAID_OK:
            LOG_WARN('_onRaidApplyJoinRecordTimeout:: record lost', raidUUID, primaryGBID)
            return

        _raidVal = self.raidDict[raidUUID]
        _joinVal, _ = _raidVal.popRaidJoin(primaryGBID)
        _joinVal.applyTimeoutTimerId = 0
        gameengine.getGlobalBase('PlayerStub').doOnOthersCell(
            list(_joinVal.raidJoinPlayerDic), 'onJoinPlayerHandleReplyJoinRaidReject',
            (raidUUID, ), None, '', ())

    def _rejectReplyJoinRaid(self, srcPlayerBox, srcPlayerGbId, joinedPlayerGbId, raidUUID):
        _playerJoinVal, _err = self._replyJoinRaidRemove(srcPlayerBox, srcPlayerGbId, joinedPlayerGbId, raidUUID)
        if _err != gameconst.RaidErrno.ENUM_RAID_OK:
            LOG_WARN('replyJoinRaid:: reject failed, {}'.format(_err))
            return

        gameengine.getGlobalBase('PlayerStub').doOnOthersCell(
            [joinedPlayerGbId, ], 'onJoinPlayerHandleReplyJoinRaidReject',
            (raidUUID, ), None, '', ())
        gameengine.getGlobalBase('PlayerStub').doOnOthersClient(
            [joinedPlayerGbId, ], 'onMessage',
            (RAID_CONST.datas["raid_applyRefused_msg"]["value"], []),
                None, '', ())
        if _playerJoinVal.applyTimeoutTimerId:
            self.cancelTimerCB(_playerJoinVal.applyTimeoutTimerId,
                                gametimer.TIMER_TAG_RAID_APPLY_JOIN_TIMEOUT)
            _playerJoinVal.applyTimeoutTimerId = 0

    def replyJoinRaid(self, srcPlayerBox, srcPlayerGbId, joinedPlayerGbId, raidUUID, beAgreed, extraProps):
        LOG_INFO('replyJoinRaid::', srcPlayerBox, srcPlayerGbId, joinedPlayerGbId, raidUUID, beAgreed, extraProps)


        if not beAgreed:
            self._rejectReplyJoinRaid(srcPlayerBox, srcPlayerGbId, joinedPlayerGbId, raidUUID)
            return

        playerJoinVal, err = self._replyJoinRaidCheck(srcPlayerBox, srcPlayerGbId, joinedPlayerGbId, raidUUID)
        if err != gameconst.RaidErrno.ENUM_RAID_OK:
            err = err.initkvbody(source=self._replyJoinRaidCheck.__name__,
                                 raidUUID=raidUUID,
                                 playerGBID=joinedPlayerGbId)

            if err == gameconst.RaidErrno.ENUM_RAID_RAID_IS_FULL:
                LOG_WARN('replayJoinRaid:: failed, raid is full')
                srcPlayerBox.onMessagePre(RAID_CONST.datas["raid_applyAcceptFail_raidFull_msg"]["value"], [])
                # DO NOT remove join info here
                return

            else:
                LOG_WARN('replayJoinRaid:: failed, {}'.format(err))

            self._rejectReplyJoinRaid(srcPlayerBox, srcPlayerGbId, joinedPlayerGbId, raidUUID)
            return

        if playerJoinVal.isSingle():
            # 单人申请直接通过
            self.doReplyJoinRaidLonely(srcPlayerBox, srcPlayerGbId, raidUUID, joinedPlayerGbId, extraProps)
        else:
            # 多人申请通过需要到teamStub上再确认以下
            self.doReplyJoinRaidWithTeam(srcPlayerBox, srcPlayerGbId, raidUUID,
                                         joinedPlayerGbId, extraProps)

    def _replyJoinRaidRemove(self, srcPlayerBox, srcPlayerGbId, joinedPlayerGbId, raidUUID):
        if raidUUID not in self.raidDict:
            return None, gameconst.RaidErrno.ENUM_RAID_RAID_ID_NOT_FOUND

        _raidVal = self.raidDict[raidUUID]
        if srcPlayerGbId != _raidVal.raidLeaderGBID and not _raidVal.isRaidDeputy(srcPlayerGbId):
            return None, gameconst.RaidErrno.ENUM_RAID_NOT_RAID_LEADER_OR_DEPUTY

        playerJoinVal, err = _raidVal.popRaidJoin(joinedPlayerGbId)
        if err != gameconst.RaidErrno.ENUM_RAID_OK:
            return None, err

        return playerJoinVal, gameconst.RaidErrno.ENUM_RAID_OK

    def _replyJoinRaidCheck(self, srcPlayerBox, srcPlayerGbId, joinedPlayerGbId, raidUUID):
        if raidUUID not in self.raidDict:
            return None, gameconst.RaidErrno.ENUM_RAID_RAID_ID_NOT_FOUND

        _raidVal = self.raidDict[raidUUID]
        if srcPlayerGbId != _raidVal.raidLeaderGBID and not _raidVal.isRaidDeputy(srcPlayerGbId):
            return None, gameconst.RaidErrno.ENUM_RAID_NOT_RAID_LEADER_OR_DEPUTY

        if _raidVal.isRaidFull():
            return None, gameconst.RaidErrno.ENUM_RAID_RAID_IS_FULL

        playerJoinVal, err = _raidVal.getRaidJoin(joinedPlayerGbId)
        if err != gameconst.RaidErrno.ENUM_RAID_OK:
            return None, err

        return playerJoinVal, gameconst.RaidErrno.ENUM_RAID_OK

    def doReplyJoinRaidLonely(self, srcPlayerBox, srcPlayerGbId, raidUUID, joinedPlayerGbId, extraProps):
        """ NOTE: Check raidUUID and joinPlayerGBID outside this method,
                  PLS DO NOT IMPL CHECK LOGIC INSIDE.
        """
        LOG_INFO('doReplyJoinRaidLonely::', raidUUID, joinedPlayerGbId, extraProps)
        _raidVal = self.raidDict[raidUUID]
        playerJoinVal, _ = _raidVal.popRaidJoin(joinedPlayerGbId)

        extraProps['raidTarget'] = _raidVal.raidTarget
        inviteType = extraProps.get('inviteType', gameconst.InviteType.DEFAULT)
        needMsg = inviteType != gameconst.InviteType.GUILD
        if needMsg:
            gameengine.getGlobalBase('PlayerStub').doOnOthersCell(
                [joinedPlayerGbId, ], 'onJoinPlayerReplyJoinRaidLonely',
                (srcPlayerGbId, raidUUID, joinedPlayerGbId, playerJoinVal.toStreamSavedDic(), extraProps, playerJoinVal.raidJoinPlayerDic[joinedPlayerGbId].applySource),
                self, 'onPlayerIsOffline',
                (srcPlayerGbId, playerJoinVal.raidJoinPlayerDic[joinedPlayerGbId].playerName))
        else:
            gameengine.getGlobalBase('PlayerStub').doOnOthersCell(
                [joinedPlayerGbId, ], 'onJoinPlayerReplyJoinRaidLonely',
                (srcPlayerGbId, raidUUID, joinedPlayerGbId, playerJoinVal.toStreamSavedDic(), extraProps, playerJoinVal.raidJoinPlayerDic[joinedPlayerGbId].applySource),
                None, '',
                ())

        if playerJoinVal.applyTimeoutTimerId:
            self.cancelTimerCB(playerJoinVal.applyTimeoutTimerId,
                                 gametimer.TIMER_TAG_RAID_APPLY_JOIN_TIMEOUT)
            playerJoinVal.applyTimeoutTimerId = 0

    def doReplyJoinRaidWithTeam(self, srcPlayerBox, srcPlayerGbId, raidUUID, joinedPlayerGbId, extraProps):
        """ NOTE: check conditions outisde this method,
                  PLS DO NOT IMPL CHECK LOGIC INSIDE.
        """
        LOG_INFO('doReplyJoinRaidWithTeam::', srcPlayerBox, srcPlayerGbId, raidUUID, joinedPlayerGbId, extraProps)
        _raidVal = self.raidDict[raidUUID]
        playerJoinVal, _ = _raidVal.getRaidJoin(joinedPlayerGbId)
        gameengine.getTeamStub(playerJoinVal.joinTeamUUID).replyJoinRaidWithTeam(
            srcPlayerBox, srcPlayerGbId, raidUUID, joinedPlayerGbId, playerJoinVal.joinTeamUUID,
            [_i.toStreamSavedDic() for _i in playerJoinVal.raidJoinPlayerDic.values()], extraProps)

    def onReplyJoinRaidLonely(self, srcPlayerGbId, raidUUID, playerGBID, playerProps, extraProps):
        LOG_INFO('onReplyJoinRaidLonely::', srcPlayerGbId, raidUUID, playerGBID, playerProps, extraProps)
        playerVal, err = self._onReplyJoinRaidLonely(srcPlayerGbId, raidUUID, playerGBID, playerProps)
        needMsg = extraProps.get('inviteType', gameconst.InviteType.DEFAULT)
        if err != gameconst.RaidErrno.ENUM_RAID_OK:
            if err == gameconst.RaidErrno.ENUM_RAID_RAID_IS_FULL:
                if needMsg:
                    gameengine.getGlobalBase('PlayerStub').doOnOthersClient(
                            [playerGBID, ], 'onMessage',
                            (RAID_CONST.datas["raid_applyAcceptFail_raidFull_msg"]["value"], []),
                            None, '', ())
            return

        _raidVal = self.raidDict[raidUUID]
        _raidVal.refreshRaidCacheValToAllPlayers()

    def _onReplyJoinRaidLonely(self, srcPlayerGbId, raidUUID, playerGBID, playerProps):
        if raidUUID not in self.raidDict:
            return None, gameconst.RaidErrno.ENUM_RAID_RAID_ID_NOT_FOUND

        _raidVal = self.raidDict[raidUUID]
        if _raidVal.raidLeaderGBID != srcPlayerGbId and not _raidVal.isRaidDeputy(srcPlayerGbId):
            # NOTE: srcPlayerGbId 代表同意玩家申请时的 leaderGBID or deputyGBID, 不一定是_raidVal中存放的GBID
            LOG_WARN('_onReplyJoinRaidLonely:: leader changed when reply join raid')

        playerVal, err = _raidVal.addNewMember(playerGBID, playerProps, toClient=True)
        if err != gameconst.RaidErrno.ENUM_RAID_OK:
            LOG_WARN('_onReplyJoinRaidLonely:: add member failed, {}'.format(err))
            return None, err

        return playerVal, gameconst.RaidErrno.ENUM_RAID_OK

    def onTeamReplyJoinRaidWithTeam(self, srcPlayerBox, srcPlayerGbId, raidUUID, joinedPlayerGbId,
                                    error, extraProps):
        LOG_INFO('onTeamReplyJoinRaidWithTeam::', srcPlayerBox, srcPlayerGbId, raidUUID,
                  joinedPlayerGbId, error, extraProps)

        def _reject():
            _playerJoinVal, _err = self._replyJoinRaidRemove(srcPlayerBox, srcPlayerGbId, joinedPlayerGbId, raidUUID)
            if _err != gameconst.RaidErrno.ENUM_RAID_OK:
                LOG_ERR('onTeamReplyJoinRaidWithTeam:: reject failed, {}'.format(_err))
                return

            if _playerJoinVal.applyTimeoutTimerId:
                self.cancelTimerCB(_playerJoinVal.applyTimeoutTimerId,
                                    gametimer.TIMER_TAG_RAID_APPLY_JOIN_TIMEOUT)
                _playerJoinVal.applyTimeoutTimerId = 0

            gameengine.getGlobalBase('PlayerStub').doOnOthersCell(
                [joinedPlayerGbId, ], 'onJoinPlayerHandleReplyJoinRaidReject',
                (raidUUID, ), None, '', ())

        if error != gameconst.RaidErrno.ENUM_RAID_OK:
            LOG_ERR('onTeamReplyJoinRaidWithTeam:: failed from teamStub process, {}'.format(error))
            _reject()
            return

        playerJoinVal, err = self._replyJoinRaidCheck(srcPlayerBox, srcPlayerGbId, joinedPlayerGbId, raidUUID)
        if err != gameconst.RaidErrno.ENUM_RAID_OK:
            err = err.initkvbody(source=self._replyJoinRaidCheck.__name__,
                                 raidUUID=raidUUID,
                                 playerGBID=joinedPlayerGbId)
            LOG_ERR('onTeamReplyJoinRaidWithTeam:: failed, {}'.format(err))
            _reject()

        if playerJoinVal.isSingle():
            LOG_WARN('onTeamReplyJoinRaidWithTeam:: change join type in call process, abort handle.', raidUUID, joinedPlayerGbId)
            return

        self._initTeamMemberJoinRecord(raidUUID, playerJoinVal.joinTeamUUID, playerJoinVal,
                                       {_i: False for _i in playerJoinVal.raidJoinPlayerDic})

        gbIdListIter = ((_i.gbId, _i.playerName) for _i in playerJoinVal.raidJoinPlayerDic.values())
        inviteType = extraProps.get('inviteType', gameconst.InviteType.DEFAULT)
        needMsg = inviteType != gameconst.InviteType.GUILD
        for _gbId, _name in gbIdListIter:
            if needMsg:
                gameengine.getGlobalBase('PlayerStub').doOnOthersCell(
                    [_gbId, ], 'onJoinPlayerReplyJoinRaidWithTeam',
                    (srcPlayerGbId, raidUUID, playerJoinVal.toStreamSavedDic(), extraProps),
                    self, 'onPlayerIsOffline', (srcPlayerGbId, _name))
            else:
                gameengine.getGlobalBase('PlayerStub').doOnOthersCell(
                    [_gbId, ], 'onJoinPlayerReplyJoinRaidWithTeam',
                    (srcPlayerGbId, raidUUID, playerJoinVal.toStreamSavedDic(), extraProps),
                    None, '', ())

    def onReplyJoinRaidWithTeam(self, srcPlayerGbId, raidUUID, teamUUID, playerGBID, playerProps, extraProps):
        LOG_INFO('onReplyJoinRaidWithTeam::', srcPlayerGbId, raidUUID, teamUUID, playerGBID, playerProps, extraProps)
        memberErrno = extraProps.get('memberCheckErrno')
        inviteType = extraProps.get('inviteType', gameconst.InviteType.DEFAULT)
        needMsg = inviteType != gameconst.InviteType.GUILD
        memberValDic, err = self._onReplyJoinRaidWithTeam(srcPlayerGbId, raidUUID, teamUUID,
                                                          playerGBID, playerProps, memberErrno)
        if err != gameconst.RaidErrno.ENUM_RAID_OK:
            if err == gameconst.RaidErrno.ENUM_RAID_CHECKING_TEAM_JOIN:
                LOG_INFO('onReplyJoinRaidWithTeam:: skill checking ...')
            else:
                _iErrorLog = False
                if err == gameconst.RaidErrno.ENUM_RAID_ALREADY_IN_RAID:
                    if needMsg:
                        gameengine.getGlobalBase('PlayerStub').doOnOthersBase(
                            [srcPlayerGbId, ], 'onMessagePre', (M_M_DD.datas.raid_teamInvitationCheck_sectionTeam, []),
                            None, '', ())
                elif err in (gameconst.RaidErrno.ENUM_RAID_RAID_IS_FULL, gameconst.RaidErrno.ENUM_RAID_RAID_NOT_ENOUGH_SIT):
                    if needMsg:
                        gameengine.getGlobalBase('PlayerStub').doOnOthersClient(
                            [srcPlayerGbId, ], 'onMessage',
                            (RAID_CONST.datas["raid_applyAcceptFail_raidFull_msg"]["value"], []),
                            None, '', ())
                else:
                    _iErrorLog = True
                (LOG_ERR if _iErrorLog else LOG_WARN)('onReplyJoinRaidWithTeam:: failed, {}'.format(err))
            return

        _raidVal = self.raidDict[raidUUID]
        _raidVal.refreshRaidCacheValToAllPlayers()

    def _onReplyJoinRaidWithTeam(self, srcPlayerGbId, raidUUID, teamUUID, playerGBID, playerProps, memberErrno):
        if memberErrno and memberErrno != gameconst.RaidErrno.ENUM_RAID_OK:
            return None, memberErrno

        if not playerProps:
            self._doPopTeamMemberJoinRecord(raidUUID, teamUUID)
            return None, gameconst.RaidErrno.ENUM_RAID_CHECKING_TEAM_JOIN_FAILED.initkvbody(source='_onReplyJoinRaidWithTeam')

        _record = self._getTeamMemberJoinRecord(raidUUID, teamUUID)    # type: _RaidTeamMemberJoinRecordVal
        if not _record:
            return None, gameconst.RaidErrno.ENUM_UNKNOWN.initkvbody(source='_onReplyJoinRaidWithTeam',
                                                                reason='record-lost')

        if playerGBID not in _record.memberCheckDic:
            return None, gameconst.RaidErrno.ENUM_UNKNOWN.initkvbody(source='_onPeplyJoinRaidWithTeam',
                                                                reason='record-not-match')

        _record.memberCheckDic[playerGBID] = playerProps

        if not all(_record.memberCheckDic.values()):
            return None, gameconst.RaidErrno.ENUM_RAID_CHECKING_TEAM_JOIN.initkvbody(source='_onReplyJoinRaidWithTeam')

        self._doPopTeamMemberJoinRecord(raidUUID, teamUUID)
        if raidUUID not in self.raidDict:
            return None, gameconst.RaidErrno.ENUM_RAID_RAID_ID_NOT_FOUND

        # 可能超时了,所以需要在这里判断记录还在不在,在的话才允许加入
        _raidVal = self.raidDict[raidUUID]
        playerJoinVal, err = _raidVal.getRaidJoin(_record.playerJoinVal.joinPlayerGBID)
        if err != gameconst.RaidErrno.ENUM_RAID_OK:
            LOG_ERR('_onReplyJoinRaidWithTeam:: get failed, {}'.format(err))
            return None, err

        memberValDic, err = _raidVal.addNewTeamMembers(list(_record.memberCheckDic.values()),
                                                      _record.playerJoinVal.joinPlayerGBID, toClient=True)
        if err == gameconst.RaidErrno.ENUM_RAID_OK or \
                err not in (gameconst.RaidErrno.ENUM_RAID_RAID_IS_FULL, gameconst.RaidErrno.ENUM_RAID_RAID_NOT_ENOUGH_SIT):
            callBackFunc = 'onJoinPlayerHandleReplyJoinRaidReject'
            if err == gameconst.RaidErrno.ENUM_RAID_OK:
                callBackFunc = 'onJoinPlayerHandleReplyJoinRaidAccept'
            playerJoinVal, _ = _raidVal.popRaidJoin(_record.playerJoinVal.joinPlayerGBID)
            gameengine.getGlobalBase('PlayerStub').doOnOthersCell(
                [playerJoinVal.joinPlayerGBID,], callBackFunc,
                (raidUUID, ), None, '', ())
            if playerJoinVal.applyTimeoutTimerId:
                self.cancelTimerCB(playerJoinVal.applyTimeoutTimerId,
                                    gametimer.TIMER_TAG_RAID_APPLY_JOIN_TIMEOUT)
                playerJoinVal.applyTimeoutTimerId = 0

        return memberValDic, err

    def cancelRaidJoinRequest(self, playerBox, playerGBID, raidUUID, raidJoinType, extraProps):
        LOG_INFO("cancelRaidJoinRequest::", playerBox, playerGBID, raidUUID, raidJoinType, extraProps)
        _playerJoinVal, err = self._cancelRaidJoinRequest(playerGBID, raidUUID)
        if err != gameconst.RaidErrno.ENUM_RAID_OK:
            LOG_WARN("cancelRaidJoinRequest::failed, errno={}".format(err), playerGBID, raidUUID, raidJoinType)
            return

        if _playerJoinVal.applyTimeoutTimerId:
            self.cancelTimerCB(_playerJoinVal.applyTimeoutTimerId,
                                 gametimer.TIMER_TAG_RAID_APPLY_JOIN_TIMEOUT)
            _playerJoinVal.applyTimeoutTimerId = 0

        playerBox.cell.onCancelRaidJoinRequestSucc(raidUUID, raidJoinType, extraProps)

    def _cancelRaidJoinRequest(self, playerGBID, raidUUID):
        if raidUUID not in self.raidDict:
            return None, gameconst.RaidErrno.ENUM_RAID_RAID_ID_NOT_FOUND

        _raidVal = self.raidDict[raidUUID]
        playerJoinVal, err = _raidVal.popRaidJoin(playerGBID)
        if err != gameconst.RaidErrno.ENUM_RAID_OK:
            return None, err

        return playerJoinVal, gameconst.RaidErrno.ENUM_RAID_OK

    def raidLeaderApplyInvitedRaid(self, srcPlayerBox, srcPlayerGbId, raidUUID,
                                   invitePlayerGBID, invitePlayerName, extraProps):
        LOG_INFO('raidLeaderApplyInvitedRaid::', srcPlayerBox, srcPlayerGbId,
                  raidUUID, invitePlayerGBID, invitePlayerName, extraProps)
        inviteType = extraProps.get('inviteType', gameconst.InviteType.DEFAULT)
        needMsg = inviteType != gameconst.InviteType.GUILD
        def _check():
            if raidUUID not in self.raidDict:
                return None, gameconst.RaidErrno.ENUM_RAID_RAID_ID_NOT_FOUND

            _raidVal = self.raidDict[raidUUID]
            if _raidVal.raidLeaderGBID != srcPlayerGbId:
                return None, gameconst.RaidErrno.ENUM_RAID_NOT_RAID_LEADER

            if _raidVal.isRaidFull():
                return None, gameconst.RaidErrno.ENUM_RAID_RAID_IS_FULL

            return _raidVal, gameconst.RaidErrno.ENUM_RAID_OK

        _raidVal, err = _check()
        if err != gameconst.RaidErrno.ENUM_RAID_OK:
            LOG_ERR('raidLeaderApplyInvitedRaid:: check failed, {}'.format(err))
            if err == gameconst.RaidErrno.ENUM_RAID_RAID_IS_FULL:
                if needMsg:
                    srcPlayerBox.onMessagePre(RAID_CONST.datas["raid_inviteFail_raidFull_msg"]["value"], [])
            return

        _joinVal, _ = _raidVal.getRaidJoin(playerGBID=invitePlayerGBID)
        if _joinVal:
            # 对于已经在申请列表中的玩家直接入团
            if _joinVal.isSingle():
                LOG_INFO('raidLeaderInvitedRaidLonely:: auto apply invite if in joinDic: single')
                self.doReplyJoinRaidLonely(srcPlayerBox, srcPlayerGbId, raidUUID, invitePlayerGBID, extraProps)
            elif _joinVal.isTeam():
                LOG_INFO('raidLeaderApplyInvitedRaid:: auto apply invite if in joinDic: team')
                self.doReplyJoinRaidWithTeam(srcPlayerBox, srcPlayerGbId, raidUUID,
                                             invitePlayerGBID, extraProps)
            else:
                LOG_ERR('raidLeaderApplyInvitedRaid:: unknown joinValType', _joinVal.raidJoinType)
            return
        _raidVal = self.raidDict[raidUUID]
        leaderVal = _raidVal.getRaidLeader()
        raidTarget = _raidVal.raidTarget
        _teamUUID = extraProps.get('teamUUID')
        if _teamUUID:
            gameengine.getTeamStub(_teamUUID).raidApplyInvitedRaid(raidTarget,
                srcPlayerBox, srcPlayerGbId, raidUUID, leaderVal.playerName,
                leaderVal.playerGbId, leaderVal.playerName, invitePlayerGBID, 
                invitePlayerName, _teamUUID, _raidVal.raidMinScore, _raidVal.raidMinLevel, extraProps)
            return
        if needMsg:
            gameengine.getGlobalBase('PlayerStub').doOnOthersCell(
                [invitePlayerGBID], 'invitedPlayerOnApplyInvitedRaid',
                (raidUUID, raidTarget, leaderVal.playerGbId, leaderVal.playerName, leaderVal.playerName, 
                _raidVal.raidMinScore, _raidVal.raidMinLevel, extraProps), self, 'onPlayerIsOffline', (srcPlayerGbId, invitePlayerName))
        else:
            gameengine.getGlobalBase('PlayerStub').doOnOthersCell(
                [invitePlayerGBID], 'invitedPlayerOnApplyInvitedRaid',
                (raidUUID, raidTarget, leaderVal.playerGbId, leaderVal.playerName, leaderVal.playerName, 
                _raidVal.raidMinScore, _raidVal.raidMinLevel, extraProps), None, '', ())


    def raidDeputyApplyInvitedRaid(self, srcPlayerBox, srcPlayerGbId, raidUUID,
                                   invitePlayerGBID, invitePlayerName, extraProps):
        LOG_INFO('raidDeputyApplyInvitedRaid::', srcPlayerBox, srcPlayerGbId,
                  raidUUID, invitePlayerGBID, invitePlayerName, extraProps)

        def _check():
            if raidUUID not in self.raidDict:
                return None, gameconst.RaidErrno.ENUM_RAID_RAID_ID_NOT_FOUND

            _raidVal = self.raidDict[raidUUID]
            if not _raidVal.isRaidDeputy(srcPlayerGbId):
                return None, gameconst.RaidErrno.ENUM_RAID_NOT_RAID_DEPUTY

            if _raidVal.isRaidFull():
                return None, gameconst.RaidErrno.ENUM_RAID_RAID_IS_FULL

            return _raidVal, gameconst.RaidErrno.ENUM_RAID_OK

        _raidVal, err = _check()
        inviteType = extraProps.get('inviteType', gameconst.InviteType.DEFAULT)
        needMsg = inviteType != gameconst.InviteType.GUILD
        if err != gameconst.RaidErrno.ENUM_RAID_OK:
            LOG_ERR('raidDeputyApplyInvitedRaid:: check failed, {}'.format(err))
            if err == gameconst.RaidErrno.ENUM_RAID_RAID_IS_FULL:
                if needMsg:
                    srcPlayerBox.onMessagePre(RAID_CONST.datas["raid_inviteFail_raidFull_msg"]["value"], [])
            return

        _joinVal, _ = _raidVal.getRaidJoin(playerGBID=invitePlayerGBID)
        if _joinVal:
            # 对于已经在申请列表中的玩家直接入团
            if _joinVal.isSingle():
                LOG_INFO('raidDeputyInvitedRaidLonely:: auto apply invite if in joinDic: single')
                self.doReplyJoinRaidLonely(srcPlayerBox, srcPlayerGbId, raidUUID, invitePlayerGBID, extraProps)
            elif _joinVal.isTeam():
                LOG_INFO('raidDeputyApplyInvitedRaid:: auto apply invite if in joinDic: team')
                self.doReplyJoinRaidWithTeam(srcPlayerBox, srcPlayerGbId, raidUUID,
                                             invitePlayerGBID, extraProps)
            else:
                LOG_ERR('raidDeputyApplyInvitedRaid:: unknown joinValType', _joinVal.raidJoinType)
            return

        raidDeputyVal = _raidVal.getRaidDeputy()
        raidLeaderVal = _raidVal.getRaidLeader()
        raidTarget = _raidVal.raidTarget
        _teamUUID = extraProps.get('teamUUID')
        if _teamUUID:
            gameengine.getTeamStub(_teamUUID).raidApplyInvitedRaid(raidTarget,
                srcPlayerBox, srcPlayerGbId, raidUUID, raidDeputyVal.playerName,
                raidLeaderVal.playerGbId, raidLeaderVal.playerName, invitePlayerGBID, 
                invitePlayerName, _teamUUID, _raidVal.raidMinScore, _raidVal.raidMinLevel, extraProps)
            return
        if needMsg:
            gameengine.getGlobalBase('PlayerStub').doOnOthersCell(
                [invitePlayerGBID], 'invitedPlayerOnApplyInvitedRaid',
                (raidUUID, raidTarget, raidDeputyVal.playerGbId, raidDeputyVal.playerName, raidLeaderVal.playerName, 
                _raidVal.raidMinScore, _raidVal.raidMinLevel, extraProps), self, 'onPlayerIsOffline', (srcPlayerGbId, invitePlayerName))
        else:
            gameengine.getGlobalBase('PlayerStub').doOnOthersCell(
                [invitePlayerGBID], 'invitedPlayerOnApplyInvitedRaid',
                (raidUUID, raidTarget, raidDeputyVal.playerGbId, raidDeputyVal.playerName, raidLeaderVal.playerName, 
                _raidVal.raidMinScore, _raidVal.raidMinLevel, extraProps), None, '', ())
    #
    def raidCaptainApplyInvitedRaid(self, srcPlayerBox, srcPlayerGbId, raidUUID, raidTeamIDX,
                                    invitePlayerGBID, invitePlayerName, extraProps):
        LOG_INFO('raidCaptainApplyInvitedRaid::', srcPlayerBox, srcPlayerGbId,
                  raidUUID, invitePlayerGBID, invitePlayerName, extraProps)

        _raidVal = teamVal = None

        def _check():
            nonlocal _raidVal, teamVal

            if raidUUID not in self.raidDict:
                return None, gameconst.RaidErrno.ENUM_RAID_RAID_ID_NOT_FOUND

            _raidVal = self.raidDict[raidUUID]
            if raidTeamIDX not in _raidVal.raidTeamDic:
                return None, gameconst.RaidErrno.ENUM_RAID_TEAM_NOT_FOUND

            teamVal = _raidVal.raidTeamDic[raidTeamIDX]
            if srcPlayerGbId != teamVal.teamCaptainGBID:
                return None, gameconst.RaidErrno.ENUM_RAID_NOT_TEAM_CAPTAIN

            return None, gameconst.RaidErrno.ENUM_RAID_OK

        _, err = _check()
        if err != gameconst.RaidErrno.ENUM_RAID_OK:
            LOG_ERR('raidCaptainApplyInvitedRaid:: check failed, {}'.format(err))
            return

        captainVal = teamVal.teamPlayerDict[srcPlayerGbId]
        _raidVal = self.raidDict[raidUUID]
        leaderVal = _raidVal.getRaidLeader()
        raidTarget = _raidVal.raidTarget
        _teamUUID = extraProps.get('teamUUID')
        if _teamUUID:
            gameengine.getTeamStub(_teamUUID).raidApplyInvitedRaid(raidTarget,
                srcPlayerBox, srcPlayerGbId, raidUUID, captainVal.playerName,
                leaderVal.playerGbId, leaderVal.playerName, invitePlayerGBID, 
                invitePlayerName, _teamUUID, _raidVal.raidMinScore, _raidVal.raidMinLevel, extraProps)
            return

        gameengine.getGlobalBase('PlayerStub').doOnOthersCell(
            [invitePlayerGBID], 
            'invitedPlayerOnApplyInvitedRaid',
            (
                raidUUID, raidTarget, captainVal.playerGbId, captainVal.playerName, leaderVal.playerName, 
                _raidVal.raidMinScore, _raidVal.raidMinLevel, extraProps), 
            self, 
            'onPlayerIsOffline', 
            (srcPlayerGbId, invitePlayerName))

    def raidMemberApplyInvitedRaid(self, srcPlayerBox, srcPlayerGbId, raidUUID,
                                   invitePlayerGBID, invitePlayerName, extraProps):
        LOG_INFO('raidMemberApplyInvitedRaid::', srcPlayerBox, srcPlayerGbId,
                  raidUUID, invitePlayerGBID, invitePlayerName, extraProps)

        playerVal = None

        def _check():
            nonlocal playerVal

            if raidUUID not in self.raidDict:
                return None, gameconst.RaidErrno.ENUM_RAID_RAID_ID_NOT_FOUND

            _raidVal = self.raidDict[raidUUID]
            raidTeamIDX = _raidVal.getRaidTeamIDX(srcPlayerGbId)
            if not raidTeamIDX:
                return None, gameconst.RaidErrno.ENUM_RAID_TEAM_NOT_FOUND

            teamVal = _raidVal.raidTeamDic[raidTeamIDX]
            playerVal = teamVal.teamPlayerDict[srcPlayerGbId]

            return playerVal, gameconst.RaidErrno.ENUM_RAID_OK

        raidPlayerVal, err = _check()
        if err != gameconst.RaidErrno.ENUM_RAID_OK:
            LOG_ERR('raidMemberApplyInvitedRaid:: failed, {}'.format(err))
            return
        inviteType = extraProps.get('inviteType', gameconst.InviteType.DEFAULT)
        needMsg = inviteType != gameconst.InviteType.GUILD
        _raidVal = self.raidDict[raidUUID]
        leaderVal = _raidVal.getRaidLeader()
        raidTarget = _raidVal.raidTarget
        _teamUUID = extraProps.get('teamUUID')
        if _teamUUID:
            gameengine.getTeamStub(_teamUUID).raidApplyInvitedRaid(raidTarget,
                srcPlayerBox, srcPlayerGbId, raidUUID, playerVal.playerName,
                leaderVal.playerGbId, leaderVal.playerName, invitePlayerGBID, 
                invitePlayerName, _teamUUID, _raidVal.raidMinScore, _raidVal.raidMinLevel, extraProps)
            return
        if needMsg:
            gameengine.getGlobalBase('PlayerStub').doOnOthersCell(
                [invitePlayerGBID], 'invitedPlayerOnApplyInvitedRaid',
                (raidUUID, raidTarget, playerVal.playerGbId, playerVal.playerName, leaderVal.playerName, 
                _raidVal.raidMinScore, _raidVal.raidMinLevel, extraProps), self, 'onPlayerIsOffline', (srcPlayerGbId, invitePlayerName))
        else:
            gameengine.getGlobalBase('PlayerStub').doOnOthersCell(
                [invitePlayerGBID], 'invitedPlayerOnApplyInvitedRaid',
                (raidUUID, raidTarget, playerVal.playerGbId, playerVal.playerName, leaderVal.playerName, 
                _raidVal.raidMinScore, _raidVal.raidMinLevel, extraProps), None, '', ())

    def replyInviteRaidLonely(self, invitedPlayerBox, invitedPlayerGbId, invitedPlayerProps,
                              srcPlayerGbId, srcPlayerTeamIDX, raidUUID, extraProps):
        LOG_INFO('replyInviteRaidLonely::', invitedPlayerBox, invitedPlayerGbId,
                  srcPlayerGbId, srcPlayerTeamIDX, raidUUID, invitedPlayerProps, extraProps)
        _, err = self._replyInviteRaidLonely(invitedPlayerBox, invitedPlayerGbId, invitedPlayerProps,
                                             srcPlayerGbId, srcPlayerTeamIDX, raidUUID)
        inviteType = extraProps.get('inviteType', gameconst.InviteType.DEFAULT)
        needMsg = inviteType != gameconst.InviteType.GUILD
        if err != gameconst.RaidErrno.ENUM_RAID_OK:
            if err == gameconst.RaidErrno.ENUM_RAID_INVITE_TO_JOIN:
                LOG_INFO('replyInviteRaidLonely:: invite to join, {}'.format(err))
            elif err == gameconst.RaidErrno.ENUM_RAID_RAID_TEAM_IS_FULL:
                LOG_WARN('replyInviteRaidLonely:: target raid team is full, {}'.format(err))
                if needMsg:
                    invitedPlayerBox and invitedPlayerBox.onMessagePre(RAID_CONST.datas["raidInviteFail_partyFull"]["value"], [])
            elif err == gameconst.RaidErrno.ENUM_RAID_RAID_IS_FULL:
                LOG_WARN('replyInviteRaidLonely:: target raid is full, {}'.format(err))
                if needMsg:
                    invitedPlayerBox and invitedPlayerBox.onMessagePre(RAID_CONST.datas["raid_joinFail_spaceless_msg"]["value"], [])
            else:
                LOG_ERR('replyInviteRaidLonely:: failed, {}'.format(err))
            return

        raidVal = self.raidDict[raidUUID]
        raidVal.refreshRaidCacheValToAllPlayers()

    def _replyInviteRaidLonely(self, invitedPlayerBox, invitedPlayerGbId, invitedPlayerProps,
                               srcPlayerGbId, srcPlayerTeamIDX, raidUUID):
        def _precheck():
            if raidUUID not in self.raidDict:
                return None, gameconst.RaidErrno.ENUM_RAID_RAID_ID_NOT_FOUND

            _raidVal = self.raidDict[raidUUID]
            if _raidVal.isRaidFull():
                return None, gameconst.RaidErrno.ENUM_RAID_RAID_IS_FULL

            return _raidVal, gameconst.RaidErrno.ENUM_RAID_OK

        raidVal, err = _precheck()
        if err != gameconst.RaidErrno.ENUM_RAID_OK:
            return None, err.initkvbody(source='_replyInviteRaidLonely._precheck')

        # CASE1: 邀请者为小队队长, 存在特定邀请teamIDX, 其他team不能加入,
        #        如果在接受邀请期间小队队长变更(不是队长/队长变更为其他小队队长等),
        #        该邀请确认请求亦会失败.
        '''
        # 没有小队长了,这个暂时不考虑了
        if srcPlayerTeamIDX:
            raidTeamIDX = raidVal.getRaidTeamIDX(srcPlayerGbId)
            if not raidTeamIDX:
                return None, gameconst.RaidErrno.ENUM_RAID_TEAM_IDX_NOT_FOUND
            elif raidTeamIDX != srcPlayerTeamIDX:
                return None, gameconst.RaidErrno.ENUM_RAID_TEAM_IDX_CHANGED.initkvbody(
                    srcRaidTeamIDX=srcPlayerTeamIDX, crtRaidTeamIDX=raidTeamIDX,
                    source='_replyInviteRaidLonely')

            raidTeamVal = raidVal.raidTeamDic[raidTeamIDX]
            if srcPlayerGbId != raidTeamVal.teamCaptainGBID:
                return None, gameconst.RaidErrno.ENUM_RAID_NOT_TEAM_CAPTAIN

            if raidTeamVal.isRaidFull():
                return None, gameconst.RaidErrno.ENUM_RAID_RAID_TEAM_IS_FULL.initkvbody(
                    raidUUID=raidUUID, raidTeamIDX=raidTeamIDX, source='_replyInviteRaidLonely')

            playerVal, err = raidTeamVal.addTeamMember(invitedPlayerGbId, invitedPlayerProps)
            playerVal.playerBox and playerVal.playerBox.client.onGetRaidData(raidVal.toClientData())
            raidVal.broadcastToAllRaidMembersClient(
                'onAddNewRaidMember', (raidUUID, raidTeamIDX, invitedPlayerGbId,
                                       playerVal.toClientData()),
                exclude=(invitedPlayerGbId, ))

            if err != gameconst.RaidErrno.ENUM_RAID_OK:
                return None, err.initkvbody(source='_replyInviteRaidLonely')

            return None, gameconst.RaidErrno.ENUM_RAID_OK
        '''

        # CASE2: 其他情况, 可能是团长或者副团长邀请
        if srcPlayerGbId == raidVal.raidLeaderGBID or raidVal.isRaidDeputy(srcPlayerGbId):
            # CASE2.1: 如果邀请发起方是团、副团长, 则直接加入
            playerVal, err = raidVal.addNewMember(invitedPlayerGbId, invitedPlayerProps, toClient=True)
            if err != gameconst.RaidErrno.ENUM_RAID_OK:
                return None, err.initkvbody(source='_replyInviteRaidLonely')

            return None, gameconst.RaidErrno.ENUM_RAID_OK

        # CASE2.2(DEFAULT): 其他情况, 发起方是普通小队成员, 则向团长发起申请
        joinExtraProps = {}
        self.applyJoinRaidLonely(invitedPlayerBox, invitedPlayerGbId, invitedPlayerProps, raidUUID, joinExtraProps, '', True, gameconst.ApplySource.RECRUIT)
        return None, gameconst.RaidErrno.ENUM_RAID_INVITE_TO_JOIN

    def replyInviteRaidWithTeam(self, invitedPlayerBox, invitedPlayerGbId, raidUUID, recordID,
                                teamUUID, teamMemberNum, playerProps, isCaptain, srcPlayerGbId, extraProps):
        LOG_INFO('replyInviteRaidWithTeam::', invitedPlayerBox, invitedPlayerGbId, raidUUID, recordID,
                  teamUUID, isCaptain, teamMemberNum, playerProps, srcPlayerGbId, extraProps)
        memberValDic, err = self._replyInviteRaidWithTeamDirectly(invitedPlayerBox, invitedPlayerGbId, raidUUID,
                                                                  recordID, teamUUID, teamMemberNum, playerProps,
                                                                  srcPlayerGbId, isCaptain)
        if err != gameconst.RaidErrno.ENUM_RAID_OK:
            if err == gameconst.RaidErrno.ENUM_RAID_CHECKING_TEAM_INVITE:
                LOG_INFO('replyInviteRaidWithTeam:: skill checking...')
            elif err == gameconst.RaidErrno.ENUM_RAID_INVITE_TO_JOIN:
                LOG_INFO('replyInviteRaidWithTeam:: invite to join, {}'.format(err))
            elif err == gameconst.RaidErrno.ENUM_RAID_ERR_IGNORE:
                LOG_INFO('replyInviteRaidWithTeam:: ignored, {}'.format(err))
            else:
                if err in (gameconst.RaidErrno.ENUM_RAID_RAID_IS_FULL, gameconst.RaidErrno.ENUM_RAID_RAID_NOT_ENOUGH_SIT):
                    # TODO()(RAID_INFO): mock message
                    # 邀请者弹窗
                    # gameengine.getGlobalBase('PlayerStub').doOnOthersClient(
                    #     [srcPlayerGbId, ], 'onMessage',
                    #     (M_M_DD.datas.CUSTOM_STRING6, ['团队中没有足够空间容纳该队伍']),
                    #     None, '', ())
                    # 被邀请者弹窗
                    invitedPlayerBox.onMessagePre(RAID_CONST.datas["raid_joinFail_spaceless_msg"]["value"], [])
                    pass
                LOG_ERR('replyInviteRaidWithTeam::  failed, {}'.format(err))
            return

        raidVal = self.raidDict[raidUUID]
        raidVal.refreshRaidCacheValToAllPlayers()

    def _replyInviteRaidWithTeamDirectly(self, invitedPlayerBox, invitedPlayerGbId, raidUUID, recordID,
                                         teamUUID, teamMemberNum, playerProps, srcPlayerGbId, isCaptain):
        if raidUUID not in self.raidDict:
            return None, gameconst.RaidErrno.ENUM_RAID_RAID_ID_NOT_FOUND

        raidVal = self.raidDict[raidUUID]
        if raidVal.isRaidFull():
            return None, gameconst.RaidErrno.ENUM_RAID_RAID_IS_FULL

        # CASE1: 邀请者不是团队Leader; 如果调用来源是队长, 则将该队伍转到申请列表(绕过队员check)
        if srcPlayerGbId != raidVal.raidLeaderGBID:
            if isCaptain:
                gameengine.getTeamStub(teamUUID).applyJoinRaidWithTeam(
                    invitedPlayerBox, invitedPlayerGbId, teamUUID, raidUUID, {})
                return None, gameconst.RaidErrno.ENUM_RAID_INVITE_TO_JOIN
            return None, gameconst.RaidErrno.ENUM_RAID_ERR_IGNORE.initkvbody(reason='invited-src-is-member')

        # CASE2: 邀请者是团长, check所有团员, 然后将团员入队
        _invitedCheckCache = self._initTeamMemberInviteRecord(raidUUID, teamUUID, recordID, teamMemberNum, {})
        if isCaptain:
            _invitedCheckCache.captainGBID = invitedPlayerGbId
        _invitedCheckCache.memberCheckDic[invitedPlayerGbId] = playerProps
        if not _invitedCheckCache.isAllChecked():
            # CASE2.1: 没有全部check, 等待
            return None, gameconst.RaidErrno.ENUM_RAID_CHECKING_TEAM_INVITE

        # CASE2.2: 全部check, 尝试加入团队
        if not all(_invitedCheckCache.memberCheckDic.values()):
            return None, gameconst.RaidErrno.ENUM_RAID_CHECKING_TEAM_INVITE_FAILED

        self._popTeamMemberInviteRecord(raidUUID, teamUUID, recordID)
        _memberValDic, err = raidVal.addNewTeamMembers(list(_invitedCheckCache.memberCheckDic.values()),
                                                      _invitedCheckCache.captainGBID, toClient=True)
        if err != gameconst.RaidErrno.ENUM_RAID_OK:
            return _memberValDic, err.initkvbody(source='_replyInviteRaidWithTeamDirectly.addNewTeamMembers')

        return _memberValDic, err

    def leaveRaid(self, leavePlayerBox, leavePlayerGBID, raidUUID, extraProps):
        LOG_INFO('leaveRaid::', leavePlayerBox, leavePlayerGBID, raidUUID, extraProps)
        if raidUUID not in self.raidDict:
            return
        
        raidVal = self.raidDict[raidUUID]
        raidMemberVal, err = self._raidMemberLeaveRaid(raidUUID, leavePlayerGBID)
        if err != gameconst.RaidErrno.ENUM_RAID_OK:
            LOG_WARN('leaveRaid:: failed, {}'.format(err))
            return
        # 通知客户端，谁走了
        raidVal.broadcastAllRaidMembersBase('onMessagePre', (M_M_DD.datas.raid_playerLeft, [raidMemberVal.playerName, str(raidMemberVal.playerGbId)]))

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
        LOG_INFO('_raidMemberLeaveRaid::', raidUUID, memberGBID)
        if raidUUID not in self.raidDict:
            return None, gameconst.RaidErrno.ENUM_RAID_RAID_ID_NOT_FOUND

        raidVal = self.raidDict[raidUUID]
        teamIDX = teamIDX or raidVal.getRaidTeamIDX(memberGBID)
        if not teamIDX:
            return None, gameconst.RaidErrno.ENUM_RAID_TEAM_IDX_NOT_FOUND

        self.onTransfer(memberGBID, teamIDX, raidVal, False)

        teamIDX = raidVal.getRaidTeamIDX(memberGBID)
        raidMemberVal, err = raidVal.popMember(teamIDX, memberGBID, toClient=True)
        if err != gameconst.RaidErrno.ENUM_RAID_OK:
            return None, err.initkvbody(source='_raidMemberLeaveRaid::raidVal.popMember',
                                        raidUUID=raidUUID)()

        return raidMemberVal, gameconst.RaidErrno.ENUM_RAID_OK

    def raidLeaderKickOutRaidMember(self, srcPlayerBox, srcPlayerGbId, raidUUID,
                                    rmPlayerRaidTeamIDX, rmPlayerGBID, extraProps):
        LOG_INFO('raidLeaderKickOutRaidMember::', srcPlayerBox, srcPlayerGbId,
                  raidUUID, rmPlayerRaidTeamIDX, rmPlayerGBID, extraProps)

        _raidVal = None  # type: raid.RaidVal

        def _check():
            nonlocal _raidVal
            if srcPlayerGbId == rmPlayerGBID:
                return None, gameconst.RaidErrno.ENUM_RAID_KICKOUT_SELF.initkvbody(
                    source='raidLeaderKickOutRaidMember._check',
                    raidUUID=raidUUID,
                    srcPlayerGbId=srcPlayerGbId,
                    rmPlayerGBID=rmPlayerGBID)

            if raidUUID not in self.raidDict:
                return None, gameconst.RaidErrno.ENUM_RAID_RAID_ID_NOT_FOUND.initkvbody(
                    source='raidLeaderKickOutRaidMember._check',
                    raidUUID=raidUUID)

            _raidVal = self.raidDict[raidUUID]
            if _raidVal.raidLeaderGBID != srcPlayerGbId:
                return None, gameconst.RaidErrno.ENUM_RAID_NOT_RAID_LEADER.initkvbody(
                    source='raidLeaderKickOutRaidMember._check',
                    raidUUID=raidUUID,
                    srcPlayerGbId=srcPlayerGbId,
                    raidLeaderGBID=_raidVal.raidLeaderGBID)

            _rmTeamIDX = _raidVal.getRaidTeamIDX(rmPlayerGBID)
            if not _rmTeamIDX or _rmTeamIDX != rmPlayerRaidTeamIDX:
                return None, gameconst.RaidErrno.ENUM_RAID_TEAM_IDX_CHANGED.initkvbody(
                    source='raidLeaderKickOutRaidMember._check',
                    raidUUID=raidUUID,
                    rmPlayerRaidTeamIDX=rmPlayerRaidTeamIDX,
                    crtPlayerRaidTeamIDX=_rmTeamIDX)

            return None, gameconst.RaidErrno.ENUM_RAID_OK

        _, err = _check()
        if err != gameconst.RaidErrno.ENUM_RAID_OK:
            LOG_ERR('raidLeaderKickOutRaidMember:: _check failed, {}'.format(err))
            return

        _memberVal, err = self._raidMemberLeaveRaid(raidUUID, rmPlayerGBID, rmPlayerRaidTeamIDX)
        if err != gameconst.RaidErrno.ENUM_RAID_OK:
            LOG_ERR('raidLeaderKickOutRaidMember:: popMember failed, {}'.format(err))
            return

        leaderVal = _raidVal.getRaidLeader()
        _memberVal.playerBox and _memberVal.playerBox.onMessagePre(RAID_CONST.datas["raid_kicked_msg"]["value"], [leaderVal.playerName or ''])
        _raidVal.broadcastAllRaidMembersBase('onMessagePre', (RAID_CONST.datas["raid_kickDone_msg"]["value"], [_memberVal.playerName]))
        _raidVal.broadcastAllRaidMembersBase('onMessagePre', (M_M_DD.datas.raid_playerKicked, [_memberVal.playerName, str(_memberVal.playerGbId)]))

        _raidVal.refreshRaidCacheValToAllPlayers()
        _memberVal.playerBox and _memberVal.playerBox.cell.onBeKickedOutRaidByRaidLeader(raidUUID, extraProps)
        srcPlayerBox.cell.onRaidLeaderKickOutRaidMember(raidUUID, rmPlayerRaidTeamIDX,
                                                        rmPlayerGBID, extraProps)

    def raidDeputyKickOutRaidMember(self, srcPlayerBox, srcPlayerGbId, raidUUID,
                                    rmPlayerRaidTeamIDX, rmPlayerGBID, extraProps):
        LOG_INFO('raidDeputyKickOutRaidMember::', srcPlayerBox, srcPlayerGbId,
                  raidUUID, rmPlayerRaidTeamIDX, rmPlayerGBID, extraProps)

        _raidVal = None  # type: raid.RaidVal

        def _check():
            nonlocal _raidVal
            if srcPlayerGbId == rmPlayerGBID:
                return None, gameconst.RaidErrno.ENUM_RAID_KICKOUT_SELF.initkvbody(
                    source='raidDeputyKickOutRaidMember._check',
                    raidUUID=raidUUID,
                    srcPlayerGbId=srcPlayerGbId,
                    rmPlayerGBID=rmPlayerGBID)
            if raidUUID not in self.raidDict:
                return None, gameconst.RaidErrno.ENUM_RAID_RAID_ID_NOT_FOUND.initkvbody(
                    source='raidDeputyKickOutRaidMember._check',
                    raidUUID=raidUUID)
            _raidVal = self.raidDict[raidUUID]
            if not _raidVal.isRaidDeputy(srcPlayerGbId):
                return None, gameconst.RaidErrno.ENUM_RAID_NOT_RAID_DEPUTY.initkvbody(
                    source='raidDeputyKickOutRaidMember._check',
                    raidUUID=raidUUID,
                    srcPlayerGbId=srcPlayerGbId,
                    raidLeaderGBID=_raidVal.raidLeaderGBID)
            if _raidVal.raidLeaderGBID == rmPlayerGBID:
                return None, gameconst.RaidErrno.ENUM_RAID_NOT_RAID_CANNOT_KICK_LEADER.initkvbody(
                    source='raidDeputyKickOutRaidMember._check',
                    raidUUID=raidUUID,
                    srcPlayerGbId=srcPlayerGbId,
                    raidLeaderGBID=_raidVal.raidLeaderGBID)
            _rmTeamIDX = _raidVal.getRaidTeamIDX(rmPlayerGBID)
            if not _rmTeamIDX or _rmTeamIDX != rmPlayerRaidTeamIDX:
                return None, gameconst.RaidErrno.ENUM_RAID_TEAM_IDX_NOT_FOUND.initkvbody(
                    source='raidDeputyKickOutRaidMember._check',
                    raidUUID=raidUUID,
                    rmPlayerRaidTeamIDX=rmPlayerRaidTeamIDX,
                    crtPlayerRaidTeamIDX=_rmTeamIDX)
            return None, gameconst.RaidErrno.ENUM_RAID_OK

        _, err = _check()
        if err != gameconst.RaidErrno.ENUM_RAID_OK:
            LOG_ERR('raidDeputyKickOutRaidMember:: _check failed, {}'.format(err))
            return

        memberVal, err = self._raidMemberLeaveRaid(raidUUID, rmPlayerGBID, rmPlayerRaidTeamIDX)
        if err != gameconst.RaidErrno.ENUM_RAID_OK:
            LOG_ERR('raidDeputyKickOutRaidMember:: popMember failed, {}'.format(err))
            return

        deputyVal = _raidVal.getRaidDeputy()
        memberVal.playerBox and memberVal.playerBox.onMessagePre(RAID_CONST.datas["raid_kicked_msg"]["value"], [deputyVal.playerName or ''])
        _raidVal.broadcastAllRaidMembersBase('onMessagePre', (RAID_CONST.datas["raid_kickDone_msg"]["value"], [memberVal.playerName]))
        _raidVal.broadcastAllRaidMembersBase('onMessagePre', (M_M_DD.datas.raid_playerKicked, [memberVal.playerName, str(memberVal.playerGbId)]))

        _raidVal.refreshRaidCacheValToAllPlayers()
        memberVal.playerBox and memberVal.playerBox.cell.onBeKickedOutRaidByRaidDeputy(raidUUID, extraProps)
        srcPlayerBox.cell.onRaidDeputyKickOutRaidMember(raidUUID, rmPlayerRaidTeamIDX,
                                                        rmPlayerGBID, extraProps)
    #
    def raidTeamCaptainKickOutRaidMember(self, srcPlayerBox, srcPlayerGbId, raidUUID,
                                         rmPlayerRaidTeamIDX, rmPlayerGBID, extraProps):
        LOG_INFO('raidTeamCaptainKickOutRaidMember::', srcPlayerBox, srcPlayerGbId,
                  raidUUID, rmPlayerRaidTeamIDX, rmPlayerGBID, extraProps)

        _raidVal = None
        raidCaptainVal = None   # type: raid.RaidAndTeamMemberVal

        def _check():
            nonlocal _raidVal, raidCaptainVal
            if srcPlayerGbId == rmPlayerGBID:
                return None, gameconst.RaidErrno.ENUM_RAID_KICKOUT_SELF.initkvbody(
                    source='raidTeamCaptainKickOutRaidMember._check',
                    raidUUID=raidUUID,
                    srcPlayerGbId=srcPlayerGbId,
                    rmPlayerGBID=rmPlayerGBID)
            if raidUUID not in self.raidDict:
                return None, gameconst.RaidErrno.ENUM_RAID_RAID_ID_NOT_FOUND.initkvbody(
                    source='raidTeamCaptainKickOutRaidMember._check',
                    raidUUID=raidUUID)
            _raidVal = self.raidDict[raidUUID]
            if rmPlayerRaidTeamIDX not in _raidVal.raidTeamDic:
                return None, gameconst.RaidErrno.ENUM_RAID_TEAM_IDX_NOT_FOUND.initkvbody(
                    source='raidTeamCaptainKickOutRaidMember._check',
                    raidUUID=raidUUID,
                    teamIDX=rmPlayerRaidTeamIDX,
                    rmPlayerGBID=rmPlayerGBID)
            _raidTeamVal = _raidVal.raidTeamDic[rmPlayerRaidTeamIDX]
            if srcPlayerGbId != _raidTeamVal.teamCaptainGBID:
                return None, gameconst.RaidErrno.ENUM_RAID_NOT_TEAM_CAPTAIN.initkvbody(
                    source='raidTeamCaptainKickOutRaidMember._check',
                    raidUUID=raidUUID,
                    teamCaptainGBID=_raidTeamVal.teamCaptainGBID,
                    srcPlayerGbId=srcPlayerGbId)
            if rmPlayerGBID not in _raidTeamVal.teamPlayerDict:
                return None, gameconst.RaidErrno.ENUM_RAID_NOT_IN_TEAM.initkvbody(
                    source='raidTeamCaptainKickOutRaidMember._check',
                    raidUUID=raidUUID,
                    teamIDX=rmPlayerRaidTeamIDX,
                    rmPlayerGBID=rmPlayerGBID)

            raidCaptainVal = _raidTeamVal.teamPlayerDict[srcPlayerGbId]
            return None, gameconst.RaidErrno.ENUM_RAID_OK

        _, err = _check()
        if err != gameconst.RaidErrno.ENUM_RAID_OK:
            LOG_ERR('raidTeamCaptainKickOutRaidMember:: _check failed, {}'.format(err))
            return

        _memberVal, err = self._raidMemberLeaveRaid(raidUUID, rmPlayerGBID, rmPlayerRaidTeamIDX)
        if err != gameconst.RaidErrno.ENUM_RAID_OK:
            LOG_ERR('raidTeamCaptainKickOutRaidMember:: popMember failed, {}'.format(err))
            return

        _memberVal.playerBox and _memberVal.playerBox.onMessagePre(RAID_CONST.datas["raid_kicked_msg"]["value"], [raidCaptainVal.playerName])
        _raidVal.broadcastAllRaidMembersBase('onMessagePre', (RAID_CONST.datas["raid_kickDone_msg"]["value"], [_memberVal.playerName]))
        _raidVal.broadcastAllRaidMembersBase('onMessagePre', (M_M_DD.datas.raid_playerKicked, [_memberVal.playerName, str(_memberVal.playerGbId)]))

        _raidVal.refreshRaidCacheValToAllPlayers()
        _memberVal.playerBox and _memberVal.playerBox.cell.onBeKickedOutRaidByRaidTeamCaptain(raidUUID, extraProps)
        srcPlayerBox.cell.onRaidCaptainKickOutRaidMember(raidUUID, rmPlayerRaidTeamIDX,
                                                             rmPlayerGBID, extraProps)

    def transferRaidLeader(self, srcPlayerBox, srcPlayerGbId, raidUUID, toPlayerGBID, extraProps, broadcast):
        LOG_INFO('transferRaidLeader::', srcPlayerBox, srcPlayerGbId, raidUUID, toPlayerGBID, extraProps)
        _err = self._transferRaidDeputyCheck(srcPlayerGbId, toPlayerGBID, raidUUID)
        if _err == gameconst.RaidErrno.ENUM_RAID_OK:
            self.transferRaidDeputy(srcPlayerBox, srcPlayerGbId, raidUUID, 0, extraProps, True, False)
        _raidVal, orgRaidLeaderGBID, err = self._transferRaidLeader(srcPlayerBox, srcPlayerGbId, raidUUID, toPlayerGBID)
        if err != gameconst.RaidErrno.ENUM_RAID_OK:
            LOG_ERR('transferRaidLeader:: failed, {}'.format(err))
            return

        orgRaidLeaderTeamIDX = _raidVal.getRaidTeamIDX(orgRaidLeaderGBID)
        orgRaidLeaderVal = _raidVal.raidTeamDic[orgRaidLeaderTeamIDX].teamPlayerDict[orgRaidLeaderGBID]
        _raidLeaderVal = _raidVal.getRaidLeader()

        fn = 'onTransferRaidLeaderAllMemberNotify'
        args = (raidUUID, orgRaidLeaderGBID, _raidVal.raidLeaderGBID, _raidVal.raidLeaderTeamIDX, extraProps)

        _raidVal.broadcastToAllRaidMembersCell(fn, args)

        self.moveRaidTeamMember(_raidLeaderVal.playerBox, _raidLeaderVal.playerGbId, raidUUID,
                                _raidVal.getRaidTeamIDX(_raidLeaderVal.playerGbId), _raidLeaderVal.playerGbId,
                                orgRaidLeaderTeamIDX, orgRaidLeaderGBID, extraProps)

        if _raidVal.leaderClientDeathTimer > 0:
            self.cancelTimerCB(_raidVal.leaderClientDeathTimer, gametimer.TIMER_TAG_LEADER_CLIENT_DEATH)
            _raidVal.leaderClientDeathTimer = 0
        if not _raidLeaderVal.bOnline:
            _raidVal.leaderClientDeathTimer = self.addTimerCB(RAID_CONST.datas["raid_RLDownGradeOfflineTime"]["value"], '_onLeaderClientDeath', (raidUUID, _raidLeaderVal.playerGbId, ), gametimer.TIMER_TAG_LEADER_CLIENT_DEATH)

        # client message
        if _raidLeaderVal.playerBox:
            _raidLeaderVal.playerBox.onMessagePre(RAID_CONST.datas["raid_appointedRL_msg"]["value"], [orgRaidLeaderVal.playerName, ])
            self.getRaidApplyJoinDic(_raidLeaderVal.playerBox, _raidLeaderVal.playerGbId, raidUUID)

        if broadcast:
            exclude = (toPlayerGBID, )
        else:
            exclude = (toPlayerGBID, srcPlayerGbId)
        _raidVal.broadcastAllRaidMembersBase('onMessagePre', (RAID_CONST.datas["raid_appointRLDone_msg"]["value"], [_raidLeaderVal.playerName]),
                                            exclude=exclude)

    def _transferRaidDeputyCheck(self, srcPlayerGbId, toPlayerGBID, raidUUID):
        _raidVal = self.raidDict.get(raidUUID, None)
        if not _raidVal:
            return gameconst.RaidErrno.ENUM_RAID_RAID_ID_NOT_FOUND

        if srcPlayerGbId != _raidVal.raidLeaderGBID:
            return gameconst.RaidErrno.ENUM_RAID_RAID_LEADER_CHANGED

        if not _raidVal.isRaidDeputy(toPlayerGBID):
            return gameconst.RaidErrno.ENUM_RAID_NOT_RAID_DEPUTY

        return gameconst.RaidErrno.ENUM_RAID_OK

    def _transferRaidLeader(self, srcPlayerBox, srcPlayerGbId, raidUUID, toPlayerGBID):
        _raidVal = self.raidDict.get(raidUUID, None)
        if not _raidVal:
            return None, 0, gameconst.RaidErrno.ENUM_RAID_RAID_ID_NOT_FOUND
        
        if srcPlayerGbId != _raidVal.raidLeaderGBID:
            return None, 0, gameconst.RaidErrno.ENUM_RAID_RAID_LEADER_CHANGED

        if toPlayerGBID == _raidVal.raidLeaderGBID:
            return None, 0, gameconst.RaidErrno.ENUM_RAID_IS_SAME_PLAYER

        toPlayerTeamIdx = _raidVal.getRaidTeamIDX(toPlayerGBID)
        if not toPlayerTeamIdx:
            return None, 0, gameconst.RaidErrno.ENUM_RAID_TEAM_IDX_NOT_FOUND

        orgRaidLeaderGBID = _raidVal.raidLeaderGBID

        _, err = _raidVal.setRaidLeader(toPlayerGBID, toPlayerTeamIdx, toClient=True)
        if err != gameconst.RaidErrno.ENUM_RAID_OK:
            err.initkvbody(source='_transferRaidLeader::_raidVal.setRaidLeader')
            return None, 0, err

        return _raidVal, orgRaidLeaderGBID, gameconst.RaidErrno.ENUM_RAID_OK

    def transferRaidDeputy(self, srcPlayerBox, srcPlayerGbId, raidUUID, toPlayerGBID, extraProps, toClient=True, broadcast=True):
        LOG_INFO('transferRaidDeputy::', srcPlayerBox, srcPlayerGbId, raidUUID, toPlayerGBID, extraProps, toClient, broadcast)
        if not toPlayerGBID:
            _raidVal, orgRaidDeputyGBID, err = self._cancelRaidDeputy(srcPlayerBox, srcPlayerGbId, raidUUID, 0, toClient)
        else:
            _raidVal, orgRaidDeputyGBID, err = self._transferRaidDeputy(srcPlayerBox, srcPlayerGbId, raidUUID, toPlayerGBID, toClient)
        if err != gameconst.RaidErrno.ENUM_RAID_OK:
            LOG_ERR('transferRaidDeputy:: failed, {}'.format(err))
            return

        orgRaidDeputyTeamIDX = 0
        orgRaidDeputyVal = None
        if orgRaidDeputyGBID:
            orgRaidDeputyTeamIDX = _raidVal.getRaidTeamIDX(orgRaidDeputyGBID)
            orgRaidDeputyVal = _raidVal.raidTeamDic[orgRaidDeputyTeamIDX].teamPlayerDict[orgRaidDeputyGBID]

        raidLeaderVal = _raidVal.getRaidLeader()
        raidDeputyVal = _raidVal.getRaidDeputy()
        # client message
        if toClient:
            if raidDeputyVal:
                if raidDeputyVal.playerBox:
                    raidDeputyVal.playerBox.onMessagePre(RAID_CONST.datas["raid_appointedRDL_msg"]["value"], [raidLeaderVal.playerName, ])
                    self.getRaidApplyJoinDic(raidDeputyVal.playerBox, raidDeputyVal.playerGbId, raidUUID)
                _raidVal.broadcastAllRaidMembersBase('onMessagePre', (RAID_CONST.datas["raid_appointRDLDone_msg"]["value"], [raidDeputyVal.playerName]), exclude=(raidDeputyVal.playerGbId,))
            elif orgRaidDeputyVal and broadcast:
                _raidVal.broadcastAllRaidMembersBase('onMessagePre', (RAID_CONST.datas["raid_RDLDownGrade_msg"]["value"], [orgRaidDeputyVal.playerName]))

        fn = 'onTransferRaidDeputyAllMemberNotify'
        args = (raidUUID, orgRaidDeputyGBID, _raidVal.raidDeputyGBID, _raidVal.raidDeputyTeamIDX, extraProps)

        _raidVal.broadcastToAllRaidMembersCell(fn, args)

    def _cancelRaidDeputy(self, srcPlayerBox, srcPlayerGbId, raidUUID, toPlayerGBID, toClient):
        _raidVal = self.raidDict.get(raidUUID, None)

        if not _raidVal:
            return None, 0, gameconst.RaidErrno.ENUM_RAID_RAID_ID_NOT_FOUND

        if _raidVal.raidDeputyGBID == 0:
            return None, 0, gameconst.RaidErrno.ENUM_RAID_NOT_RAID_DEPUTY

        orgRaidDeputyGBID = _raidVal.raidDeputyGBID

        _, err = _raidVal.setRaidDeputy(0, 0, toClient)
        if err != gameconst.RaidErrno.ENUM_RAID_OK:
            err.initkvbody(source='_transferRaidDeputy::_raidVal.setRaidDeputy')
            return None, 0, err

        return _raidVal, orgRaidDeputyGBID, gameconst.RaidErrno.ENUM_RAID_OK

    def _transferRaidDeputy(self, srcPlayerBox, srcPlayerGbId, raidUUID, toPlayerGBID, toClient):
        _raidVal = self.raidDict.get(raidUUID, None)
        if not _raidVal:
            return None, 0, gameconst.RaidErrno.ENUM_RAID_RAID_ID_NOT_FOUND
        
        if srcPlayerGbId != _raidVal.raidLeaderGBID:
            return None, 0, gameconst.RaidErrno.ENUM_RAID_RAID_LEADER_CHANGED

        if _raidVal.isRaidDeputy(toPlayerGBID):
            return None, 0, gameconst.RaidErrno.ENUM_RAID_IS_SAME_PLAYER

        toPlayerTeamIdx = _raidVal.getRaidTeamIDX(toPlayerGBID)
        if not toPlayerTeamIdx:
            return None, 0, gameconst.RaidErrno.ENUM_RAID_TEAM_IDX_NOT_FOUND

        orgRaidDeputyGBID = _raidVal.raidDeputyGBID

        _, err = _raidVal.setRaidDeputy(toPlayerGBID, toPlayerTeamIdx, toClient)
        if err != gameconst.RaidErrno.ENUM_RAID_OK:
            err.initkvbody(source='_transferRaidDeputy::_raidVal.setRaidDeputy')
            return None, 0, err

        return _raidVal, orgRaidDeputyGBID, gameconst.RaidErrno.ENUM_RAID_OK
    #
    def transferRaidTeamCaptain(self, srcPlayerBox, srcPlayerGbId, raidUUID, toPlayerGBID, extraProps):
        LOG_INFO('transferRaidTeamCaptain::', srcPlayerBox, srcPlayerGbId,
                  raidUUID, toPlayerGBID, extraProps)
        raidTeamVal, err = self._transferRaidTeamCaptain(srcPlayerBox, srcPlayerGbId, raidUUID, toPlayerGBID, toClient=True)
        if err != gameconst.RaidErrno.ENUM_RAID_OK:
            LOG_ERR('transferRaidTeamCaptain:: failed, {}'.format(err))
            return

        orgRaidTeamCaptainVal = raidTeamVal.teamPlayerDict[srcPlayerGbId]
        raidTeamCaptainVal = raidTeamVal.teamPlayerDict[raidTeamVal.teamCaptainGBID]
        # client message
        if raidTeamCaptainVal.playerBox:
            raidTeamCaptainVal.playerBox.onMessagePre(
                RAID_CONST.datas["raid_appointedPL_msg"]["value"], 
                [orgRaidTeamCaptainVal.playerName, ])

        for _playerVal in raidTeamVal.teamPlayerDict.values():
            if _playerVal.playerGbId == raidTeamVal.teamCaptainGBID:
                continue

            if not _playerVal.playerBox:
                continue

            _playerVal.playerBox.onMessagePre(
                RAID_CONST.datas["raid_appointPLDone_msg"]["value"], 
                [raidTeamCaptainVal.playerName, ])

        _fn = 'onTransferRaidTeamCaptainAllMemberNotify'
        _args = (raidUUID, raidTeamVal.teamIDX, srcPlayerGbId, toPlayerGBID, extraProps)

        _raidVal = self.raidDict[raidUUID]
        _raidVal.broadcastToAllRaidMembersCell(_fn, _args)
    #
    def _transferRaidTeamCaptain(self, srcPlayerBox, srcPlayerGbId, raidUUID, toPlayerGBID, toClient=False):
        if raidUUID not in self.raidDict:
            return None, gameconst.RaidErrno.ENUM_RAID_RAID_ID_NOT_FOUND

        _raidVal = self.raidDict[raidUUID]
        if srcPlayerGbId == _raidVal.raidLeaderGBID:
            return None, gameconst.RaidErrno.ENUM_RAID_LEADER_TEAM_CANT_TRANS_CAPTAIN

        srcPlayerTeamIDX = _raidVal.getRaidTeamIDX(srcPlayerGbId)
        if not srcPlayerTeamIDX:
            return None, gameconst.RaidErrno.ENUM_RAID_TEAM_IDX_NOT_FOUND

        raidTeamVal = _raidVal.raidTeamDic[srcPlayerTeamIDX]
        if srcPlayerGbId != raidTeamVal.teamCaptainGBID:
            return None, gameconst.RaidErrno.ENUM_RAID_NOT_TEAM_CAPTAIN

        if toClient:
            _raidVal.broadcastToAllRaidMembersClient('onSetRaidTeamCaptain', (raidUUID, srcPlayerTeamIDX, toPlayerGBID))

        return raidTeamVal, gameconst.RaidErrno.ENUM_RAID_OK
    #
    def awardRaidTeamCaptain(self, srcPlayerBox, srcPlayerGbId, raidUUID, toRaidTeamIDX, toPlayerGBID, extraProps):
        LOG_INFO('awardRaidTeamCaptain::', srcPlayerBox, srcPlayerGbId, raidUUID, toRaidTeamIDX, toPlayerGBID, extraProps)
        orgCaptainVal, err = self._awardRaidTeamCaptain(srcPlayerBox, srcPlayerGbId, raidUUID,
                                                        toRaidTeamIDX, toPlayerGBID, toClient=True)
        if err != gameconst.RaidErrno.ENUM_RAID_OK:
            err = err.initkvbody(source='awardRaidTeamCaptain', raidUUID=raidUUID,
                                 raidTeamIDX=toRaidTeamIDX, playerGBID=toPlayerGBID)()
            LOG_ERR('awardRaidTeamCaptain:: failed, {}'.format(err))
            return

        fn = 'onAwardRaidTeamCaptainAllMemberNotify'
        args = (raidUUID, srcPlayerGbId, orgCaptainVal.playerGbId, toRaidTeamIDX, toPlayerGBID, extraProps)

        _raidVal = self.raidDict[raidUUID]
        _raidVal.broadcastToAllRaidMembersCell(fn, args)
    #
    def _awardRaidTeamCaptain(self, srcPlayerBox, srcPlayerGbId, raidUUID, toRaidTeamIDX, toPlayerGBID, toClient=False):
        if raidUUID not in self.raidDict:
            return None, gameconst.RaidErrno.ENUM_RAID_RAID_ID_NOT_FOUND

        _raidVal = self.raidDict[raidUUID]
        if srcPlayerGbId != _raidVal.raidLeaderGBID:
            return None, gameconst.RaidErrno.ENUM_RAID_NOT_RAID_LEADER

        if toRaidTeamIDX not in _raidVal.raidTeamDic:
            return None, gameconst.RaidErrno.ENUM_RAID_TEAM_IDX_NOT_FOUND
        elif toRaidTeamIDX == _raidVal.raidLeaderGBID:
            return None, gameconst.RaidErrno.ENUM_RAID_AWARD_SELF_TEAM

        raidTeamVal = _raidVal.raidTeamDic[toRaidTeamIDX]
        if toPlayerGBID not in raidTeamVal.teamPlayerDict:
            return None, gameconst.RaidErrno.ENUM_RAID_PLAYER_GBID_NOT_FOUND
        elif toPlayerGBID == raidTeamVal.teamCaptainGBID:
            return None, gameconst.RaidErrno.ENUM_RAID_ALREADY_BE_TEAM_CAPTAIN

        orgCaptainVal = raidTeamVal.teamPlayerDict[raidTeamVal.teamCaptainGBID]

        if toClient:
            _raidVal.broadcastToAllRaidMembersClient('onSetRaidTeamCaptain', (raidUUID, toRaidTeamIDX, toPlayerGBID))

        return orgCaptainVal, gameconst.RaidErrno.ENUM_RAID_OK

    def moveRaidTeamMember(self, srcPlayerBox, srcPlayerGbId, raidUUID,
                           fromPlayerTeamIdx, fromPlayerGBID,
                           toPlayerTeamIdx, toPlayerGBID, extraProps):
        LOG_INFO('moveRaidTeamMember::', srcPlayerBox, srcPlayerGbId, raidUUID,
                  fromPlayerTeamIdx, fromPlayerGBID, toPlayerTeamIdx, toPlayerGBID,
                  extraProps)

        if toPlayerGBID:
            # 如果存在被交换的玩家ID, 则被交换两个玩家所在队伍
            self.moveRaidTeamMemberExchangeTargetPlayer(srcPlayerBox, srcPlayerGbId, raidUUID,
                                                        fromPlayerTeamIdx, fromPlayerGBID,
                                                        toPlayerTeamIdx, toPlayerGBID, extraProps)
        else:
            # 不存在被交换玩家ID, 将玩家交换至其他队伍(或空队伍)的空位
            self.moveRaidTeamMemberNoTargetPlayer(srcPlayerBox, srcPlayerGbId, raidUUID,
                                                  fromPlayerTeamIdx, fromPlayerGBID, toPlayerTeamIdx,
                                                  extraProps)

    def moveRaidTeamMemberNoTargetPlayer(self, srcPlayerBox, srcPlayerGbId, raidUUID,
                                         fromPlayerTeamIdx, fromPlayerGBID,
                                         toPlayerTeamIdx, extraProps):
        LOG_INFO('moveRaidTeamMemberNoTargetPlayer::', srcPlayerBox, srcPlayerGbId,
                  raidUUID, fromPlayerTeamIdx, fromPlayerGBID, toPlayerTeamIdx, extraProps)
        toRaidTeamVal, err = self._moveRaidTeamMemberNoTargetPlayer(srcPlayerBox, srcPlayerGbId, raidUUID,
                                                                    fromPlayerTeamIdx, fromPlayerGBID, toPlayerTeamIdx)
        if err != gameconst.RaidErrno.ENUM_RAID_OK:
            LOG_ERR('moveRaidTeamMemberNoTargetPlayer:: failed, {}'.format(err))
            return

        _raidVal = self.raidDict[raidUUID]
        _raidVal.refreshRaidCacheValToAllPlayers()

        toPlayerVal = toRaidTeamVal.teamPlayerDict[fromPlayerGBID]

        _fn = 'onMoveRaidTeamMemberSucc'
        _args = (srcPlayerGbId, raidUUID, fromPlayerTeamIdx, fromPlayerGBID, toPlayerTeamIdx, 0, extraProps)

        if toPlayerVal.bOnline and toPlayerVal.playerBox and toPlayerVal.playerBox.cell:
            getattr(toPlayerVal.playerBox.cell, _fn)(*_args)

        if srcPlayerGbId != fromPlayerGBID:
            if srcPlayerBox.cell:
                getattr(srcPlayerBox.cell, _fn)(*_args)

    def _moveRaidTeamMemberNoTargetPlayer(self, srcPlayerBox, srcPlayerGbId, raidUUID,
                                          fromPlayerTeamIdx, fromPlayerGBID, toPlayerTeamIdx):
        if raidUUID not in self.raidDict:
            return None, gameconst.RaidErrno.ENUM_RAID_RAID_ID_NOT_FOUND.initkvbody(raidUUID=raidUUID)

        _raidVal = self.raidDict[raidUUID]
        if srcPlayerGbId != _raidVal.raidLeaderGBID and not _raidVal.isRaidDeputy(srcPlayerGbId):
            return None, gameconst.RaidErrno.ENUM_RAID_NOT_RAID_LEADER_OR_DEPUTY

        if fromPlayerTeamIdx not in _raidVal.raidTeamDic:
            return None, gameconst.RaidErrno.ENUM_RAID_TEAM_IDX_NOT_FOUND.initkvbody(raidUUID=raidUUID,
                                                                                teamIDX=fromPlayerTeamIdx)

        fromRaidTeamVal = _raidVal.raidTeamDic[fromPlayerTeamIdx]
        if fromPlayerGBID not in fromRaidTeamVal.teamPlayerDict:
            return None, gameconst.RaidErrno.ENUM_RAID_PLAYER_GBID_NOT_FOUND.initkvbody(raidUUID=raidUUID,
                                                                                   teamIDX=fromPlayerTeamIdx,
                                                                                   playerGBID=fromPlayerGBID)

        # orgFromRaidTeamCaptainGBID = fromRaidTeamVal.teamCaptainGBID
        orgRaidLeaderGBID = _raidVal.raidLeaderGBID
        orgRaidDeputyGBID = _raidVal.raidDeputyGBID

        if toPlayerTeamIdx in _raidVal.raidTeamDic:
            LOG_INFO('_moveRaidTeamMemberNoTargetPlayer:: transfer')
            # CASE1: 玩家转移至一个已经有小队的Team
            toRaidTeamVal = _raidVal.raidTeamDic[toPlayerTeamIdx]
            if toRaidTeamVal.isRaidFull():
                return None, gameconst.RaidErrno.ENUM_RAID_RAID_TEAM_IS_FULL
            fromPlayerVal, err = _raidVal.popMember(fromPlayerTeamIdx, fromPlayerGBID)
            if err != gameconst.RaidErrno.ENUM_RAID_OK:
                return None, err.initkvbody(source='_moveRaidTeamMemberNoTargetPlayer::_raidVal.popMember',
                                            source2='CASE1')
            toPlayerVal, err = toRaidTeamVal.addTeamMember(fromPlayerGBID, fromPlayerVal.toStreamSavedDic())
            if err != gameconst.RaidErrno.ENUM_RAID_OK:
                return None, err.initkvbody(source='_moveRaidTeamMemberNoTargetPlayer::toRaidTeamVal.addTeamMember',
                                            srouce2='CASE1')

            if orgRaidLeaderGBID == fromPlayerGBID:
                # fix raid leader
                LOG_WARN('_moveRaidTeamMemberNoTargetPlayer::CASE1 re-locate raid leader~', orgRaidLeaderGBID)
                _raidVal.setRaidLeader(fromPlayerGBID, toRaidTeamVal.teamIDX)
            if orgRaidDeputyGBID == fromPlayerGBID:
                LOG_WARN('_moveRaidTeamMemberNoTargetPlayer::CASE1 re-locate raid deputy~', orgRaidDeputyGBID)
                _raidVal.setRaidDeputy(fromPlayerGBID, toRaidTeamVal.teamIDX)
            '''
            #
            # re-get fromRaidTeamVal, obj may change when popMember method called
            fromRaidTeamVal = _raidVal.raidTeamDic.get(fromPlayerTeamIdx)
            if fromRaidTeamVal and orgFromRaidTeamCaptainGBID != fromRaidTeamVal.teamCaptainGBID:
                _raidVal.broadcastToAllRaidMembersClient('onSetRaidTeamCaptain',
                                                      (raidUUID, fromPlayerTeamIdx, fromRaidTeamVal.teamCaptainGBID))
            '''
            _raidVal.broadcastToAllRaidMembersClient('onExchangeRaidTeamMember',
                                                  (raidUUID, fromPlayerTeamIdx, fromPlayerGBID, toPlayerTeamIdx, 0))

            return toRaidTeamVal, gameconst.RaidErrno.ENUM_RAID_OK

        elif toPlayerTeamIdx > _raidVal.maxTeamNum:
            return None, gameconst.RaidErrno.ENUM_RAID_RAID_TEAM_IDX_OFR.initkvbody(raidUUID=raidUUID,
                                                                               teamIDX=toPlayerTeamIdx)
        else:
            # CASE2: 玩家转移至一个新的小队
            LOG_INFO('_moveRaidTeamMemberNoTargetPlayer:: create && transfer')
            fromPlayerVal, err = _raidVal.popMember(fromPlayerTeamIdx, fromPlayerGBID)
            if err != gameconst.RaidErrno.ENUM_RAID_OK:
                return None, err.initkvbody(source='_moveRaidTeamMemberNoTargetPlayer::_raidVal.popMember',
                                            source2='CASE2')
            toRaidTeamVal, err = _raidVal.addNewTeam(toPlayerTeamIdx)
            if err != gameconst.RaidErrno.ENUM_RAID_OK:
                return None, err.initkvbody(source='_moveRaidTeamMemberNoTargetPlayer::_raidVal.addNewTeam')
            toPlayerVal, err = toRaidTeamVal.addTeamMember(fromPlayerGBID, fromPlayerVal.toStreamSavedDic())
            if err != gameconst.RaidErrno.ENUM_RAID_OK:
                return None, err.initkvbody(source='_moveRaidTeamMemberNoTargetPlayer::toRaidTeamVal.addTeamMember',
                                            srouce2='CASE2')
            if orgRaidLeaderGBID == fromPlayerGBID:
                # fix raid leader
                LOG_WARN('_moveRaidTeamMemberNoTargetPlayer::CASE2 re-locate raid leader~', orgRaidLeaderGBID)
                _raidVal.setRaidLeader(fromPlayerGBID, toRaidTeamVal.teamIDX)
            if orgRaidDeputyGBID == fromPlayerGBID:
                LOG_WARN('_moveRaidTeamMemberNoTargetPlayer::CASE1 re-locate raid deputy~', orgRaidDeputyGBID)
                _raidVal.setRaidDeputy(fromPlayerGBID, toRaidTeamVal.teamIDX)

            _raidVal.broadcastToAllRaidMembersClient('onExchangeRaidTeamMember',
                                                  (raidUUID, fromPlayerTeamIdx, fromPlayerGBID, toPlayerTeamIdx, 0))
            return toRaidTeamVal, gameconst.RaidErrno.ENUM_RAID_OK

    def moveRaidTeamMemberExchangeTargetPlayer(self, srcPlayerBox, srcPlayerGbId, raidUUID,
                                               fromPlayerTeamIdx, fromPlayerGBID,
                                               toPlayerTeamIdx, toPlayerGBID, extraProps):
        LOG_INFO('moveRaidTeamMemberExchangeTargetPlayer::', srcPlayerBox, srcPlayerGbId, raidUUID,
                  fromPlayerTeamIdx, fromPlayerGBID, toPlayerTeamIdx, toPlayerGBID, extraProps)

        teamPlayerValDic, err = self._moveRaidTeamMemberExchangeTargetPlayer(
            srcPlayerBox, srcPlayerGbId, raidUUID,
            fromPlayerTeamIdx, fromPlayerGBID,
            toPlayerTeamIdx, toPlayerGBID)
        if err != gameconst.RaidErrno.ENUM_RAID_OK:
            LOG_ERR('moveRaidTeamMemberExchangeTargetPlayer:: failed, {}'.format(err))
            return

        raidVal = self.raidDict[raidUUID]
        raidVal.refreshRaidCacheValToAllPlayers()

        newFromPlayerVal = teamPlayerValDic[fromPlayerGBID]
        newToPlayerVal = teamPlayerValDic[toPlayerGBID]

        _fn = 'onMoveRaidTeamMemberSucc'
        _args = (srcPlayerGbId, raidUUID, fromPlayerTeamIdx, fromPlayerGBID, toPlayerTeamIdx, toPlayerGBID, extraProps)

        for playerVal in (newFromPlayerVal, newToPlayerVal):
            if not (playerVal.bOnline and playerVal.playerBox and playerVal.playerBox.cell):
                continue

            getattr(playerVal.playerBox.cell, _fn)(*_args)

        if srcPlayerGbId != fromPlayerGBID and srcPlayerGbId != toPlayerGBID:
            if srcPlayerBox.cell:
                getattr(srcPlayerBox.cell, _fn)(*_args)

    def _moveRaidTeamMemberExchangeTargetPlayer(self, srcPlayerBox, srcPlayerGbId, raidUUID,
                                               fromPlayerTeamIdx, fromPlayerGBID, toPlayerTeamIdx, toPlayerGBID):
        raidVal = self.raidDict.get(raidUUID, None)
        if not raidVal:
            return None, gameconst.RaidErrno.ENUM_RAID_RAID_ID_NOT_FOUND.initkvbody(raidUUID=raidUUID)

        if srcPlayerGbId != raidVal.raidLeaderGBID and not raidVal.isRaidDeputy(srcPlayerGbId):
            return None, gameconst.RaidErrno.ENUM_RAID_NOT_RAID_LEADER_OR_DEPUTY

        if fromPlayerTeamIdx not in raidVal.raidTeamDic:
            return None, gameconst.RaidErrno.ENUM_RAID_TEAM_IDX_NOT_FOUND.initkvbody(raidUUID=raidUUID,
                                                                                teamIDX=fromPlayerTeamIdx)
        elif toPlayerTeamIdx not in raidVal.raidTeamDic:
            return None, gameconst.RaidErrno.ENUM_RAID_TEAM_IDX_NOT_FOUND.initkvbody(raidUUID=raidUUID,
                                                                                teamIDX=fromPlayerTeamIdx)

        fromRaidTeamVal = raidVal.raidTeamDic[fromPlayerTeamIdx]
        toRaidTeamVal = raidVal.raidTeamDic[toPlayerTeamIdx]
        if fromPlayerGBID not in fromRaidTeamVal.teamPlayerDict:
            return None, gameconst.RaidErrno.ENUM_RAID_PLAYER_GBID_NOT_FOUND.initkvbody(raidUUID=raidUUID,
                                                                                   teamIDX=fromPlayerTeamIdx,
                                                                                   playerGBID=fromPlayerGBID)
        elif toPlayerGBID not in toRaidTeamVal.teamPlayerDict:
            return None, gameconst.RaidErrno.ENUM_RAID_PLAYER_GBID_NOT_FOUND.initkvbody(raidUUID=raidUUID,
                                                                                   teamIDX=toPlayerTeamIdx,
                                                                                   playerGBID=toPlayerGBID)

        orgRaidLeaderGBID = raidVal.raidLeaderGBID
        orgRaidDeputyGBID = raidVal.raidDeputyGBID
        #
        # orgFromRaidTeamCaptainGBID = fromRaidTeamVal.teamCaptainGBID
        # orgToRaidTeamCaptainGBID = toRaidTeamVal.teamCaptainGBID
        fromPlayerPos, err = raidVal.getMemberPos(fromPlayerTeamIdx, fromPlayerGBID)
        if err != gameconst.RaidErrno.ENUM_RAID_OK:
            return None, err
        toPlayerPos, err = raidVal.getMemberPos(toPlayerTeamIdx, toPlayerGBID)
        if err != gameconst.RaidErrno.ENUM_RAID_OK:
            return None, err

        minPos = min(toPlayerPos, fromPlayerPos)

        fromPlayerVal, err = raidVal.popMember(fromPlayerTeamIdx, fromPlayerGBID)
        if err != gameconst.RaidErrno.ENUM_RAID_OK:
            return None, err

        def _revertFromPlayerPopMember():
            LOG_WARN('_revertFromPlayerPopMember::~')
            raidVal._addNewMemberSpecially(fromPlayerGBID, fromPlayerVal.toStreamSavedDic(), fromPlayerTeamIdx, pos=fromPlayerPos)
            _fromRaidTeamVal = raidVal.raidTeamDic[fromPlayerTeamIdx]
            if orgRaidLeaderGBID == fromPlayerGBID:
                LOG_WARN('    \- revert: raid leader', raidUUID, fromPlayerGBID)
                raidVal.setRaidLeader(fromPlayerGBID, _fromRaidTeamVal.teamIDX)
            if orgRaidDeputyGBID == fromPlayerGBID:
                LOG_WARN('    \- revert: raid deputy', raidUUID, fromPlayerGBID)
                raidVal.setRaidDeputy(fromPlayerGBID, _fromRaidTeamVal.teamIDX)

        toPlayerVal, err = raidVal.popMember(toPlayerTeamIdx, toPlayerGBID)
        if err != gameconst.RaidErrno.ENUM_RAID_OK:
            _revertFromPlayerPopMember()
            return None, err

        def _revertToPlayerPopMember():
            LOG_WARN('_revertToPlayerPopMember::~')
            raidVal._addNewMemberSpecially(toPlayerGBID, toPlayerVal.toStreamSavedDic(), toPlayerTeamIdx, pos=toPlayerPos)
            _toRaidTeamVal = raidVal.raidTeamDic[toPlayerTeamIdx]
            if orgRaidLeaderGBID == toPlayerGBID:
                LOG_WARN('    \- revert: raid leader', raidUUID, toPlayerGBID)
                raidVal.setRaidLeader(toPlayerGBID, _toRaidTeamVal.teamIDX)
            if orgRaidDeputyGBID == toPlayerGBID:
                LOG_WARN('    \- revert: raid deputy', raidUUID, toPlayerGBID)
                raidVal.setRaidDeputy(toPlayerGBID, _toRaidTeamVal.teamIDX)

        if fromPlayerTeamIdx != toPlayerTeamIdx or minPos == toPlayerPos:
            newFromPlayerVal, err = raidVal._addNewMemberSpecially(
                fromPlayerGBID, fromPlayerVal.toStreamSavedDic(), toPlayerTeamIdx, pos=toPlayerPos)
            if err != gameconst.RaidErrno.ENUM_RAID_OK:
                _revertToPlayerPopMember()
                _revertFromPlayerPopMember()
                return None, err

            def _revertFromPlayerAddMember():
                LOG_WARN('_revertFromPlayerAddMember::~')
                raidVal.popMember(toPlayerTeamIdx, fromPlayerGBID)

            newToPlayerVal, err = raidVal._addNewMemberSpecially(
                toPlayerGBID, toPlayerVal.toStreamSavedDic(), fromPlayerTeamIdx, pos=fromPlayerPos)
            if err != gameconst.RaidErrno.ENUM_RAID_OK:
                _revertFromPlayerAddMember()
                _revertToPlayerPopMember()
                _revertFromPlayerPopMember()
                return None, err
        else:
            newToPlayerVal, err = raidVal._addNewMemberSpecially(
                toPlayerGBID, toPlayerVal.toStreamSavedDic(), fromPlayerTeamIdx, pos=fromPlayerPos)
            if err != gameconst.RaidErrno.ENUM_RAID_OK:
                _revertFromPlayerPopMember()
                _revertToPlayerPopMember()
                return None, err

            def _revertToPlayerAddMember():
                LOG_WARN('_revertToPlayerAddMember::~')
                raidVal.popMember(fromPlayerTeamIdx, toPlayerGBID)

            newFromPlayerVal, err = raidVal._addNewMemberSpecially(
                fromPlayerGBID, fromPlayerVal.toStreamSavedDic(), toPlayerTeamIdx, pos=toPlayerPos)
            if err != gameconst.RaidErrno.ENUM_RAID_OK:
                _revertToPlayerAddMember()
                _revertFromPlayerPopMember()
                _revertToPlayerPopMember()
                return None, err

        # fix raid leader
        if orgRaidLeaderGBID == fromPlayerGBID:
            LOG_WARN('_moveRaidTeamMemberExchangeTargetPlayer:: re-locate raid leader A->B(nA)*', orgRaidLeaderGBID)
            raidVal.setRaidLeader(fromPlayerGBID, toPlayerTeamIdx)
        elif orgRaidLeaderGBID == toPlayerGBID:
            LOG_WARN('_moveRaidTeamMemberExchangeTargetPlayer:: re-locate raid leader A(nB)*<-B', orgRaidLeaderGBID)
            raidVal.setRaidLeader(toPlayerGBID, fromPlayerTeamIdx)
        # fix raid deputy
        if orgRaidDeputyGBID == fromPlayerGBID:
            LOG_WARN('_moveRaidTeamMemberExchangeTargetPlayer:: re-locate raid deputy A->B(nA)*', orgRaidDeputyGBID)
            raidVal.setRaidDeputy(fromPlayerGBID, toPlayerTeamIdx)
        elif orgRaidDeputyGBID == toPlayerGBID:
            LOG_WARN('_moveRaidTeamMemberExchangeTargetPlayer:: re-locate raid deputy A(nB)*<-B', orgRaidDeputyGBID)
            raidVal.setRaidDeputy(toPlayerGBID, fromPlayerTeamIdx)

        raidVal.broadcastToAllRaidMembersClient('onExchangeRaidTeamMember',
                                              (raidUUID, fromPlayerTeamIdx, fromPlayerGBID, toPlayerTeamIdx, toPlayerGBID))

        return {fromPlayerGBID: newFromPlayerVal, toPlayerGBID: newToPlayerVal}, gameconst.RaidErrno.ENUM_RAID_OK

    def setRaidTarget(self, srcPlayerBox, srcPlayerGbId, raidUUID, raidTarget, minLevel, minScore, recruitInfo, password, isAutoExpedition):
        LOG_INFO('setRaidTarget::', srcPlayerBox, srcPlayerGbId, raidUUID, raidTarget, minLevel, minScore, recruitInfo, password, isAutoExpedition)
        _, err = self._setRaidTarget(srcPlayerBox, srcPlayerGbId, raidUUID, raidTarget, minLevel, minScore, recruitInfo, password, isAutoExpedition, toClient=True)
        if err != gameconst.RaidErrno.ENUM_RAID_OK:
            LOG_ERR('setRaidTarget:: failed, {}'.format(err))
            return

        raidVal = self.raidDict[raidUUID]
        isPublic = len(raidVal.password) == 0
        raidVal.broadcastToAllRaidMembersCell('onSetRaidTargetAllMemberNotify', (srcPlayerGbId, raidUUID, raidTarget, minLevel, minScore, recruitInfo, password, isAutoExpedition))
        self.checkAutoStart(raidUUID)

    def _setRaidTarget(self, srcPlayerBox, srcPlayerGbId, raidUUID, newRaidTargetId, minLevel, minScore, recruitInfo, password, isAutoExpedition, toClient=False):
        if raidUUID not in self.raidDict:
            return None, gameconst.RaidErrno.ENUM_RAID_RAID_ID_NOT_FOUND

        raidVal = self.raidDict[raidUUID]
        if raidVal.raidLeaderGBID != srcPlayerGbId:
            return None, gameconst.RaidErrno.ENUM_RAID_NOT_RAID_LEADER
        if raidVal.raidTarget != newRaidTargetId:
            return None, gameconst.RaidErrno.ENUM_RAID_TARGET_IS_ILLEGAL
        if raidVal.raidMinLevel != minLevel:
            return None, gameconst.RaidErrno.ENUM_RAID_LEVEL_IS_ILLEGAL
        if raidVal.raidMinScore != minScore:
            return None, gameconst.RaidErrno.ENUM_RAID_SOCRE_IS_ILLEGAL
        if raidVal.password != password:
            return None, gameconst.RaidErrno.ENUM_RAID_PASSWORD_IS_ILLEGAL
        if raidVal.recruitInfo == recruitInfo and raidVal.isAutoExpedition == isAutoExpedition:
            return None, gameconst.RaidErrno.ENUM_RAID_SET_TARGET_ILLEGAL
        # check team member's score and level
        if not raidVal.setTarget(newRaidTargetId, minLevel, minScore, recruitInfo, password, isAutoExpedition):
            return None, gameconst.RaidErrno.ENUM_RAID_TARGET_IS_ILLEGAL

        if toClient:
            raidVal.broadcastToAllRaidMembersClient('onSetRaidTarget', (raidUUID, newRaidTargetId, minLevel, minScore, recruitInfo, raidVal.password, raidVal.isAutoExpedition))

        self.raidPrepareStopAutoMatch(raidUUID)
        if raidVal.isPublish and raidVal.raidTarget > gameconst.PARE_ACTIVITY_ID:
            self.raidPrepareAutoMatch(raidUUID)

        return raidVal, gameconst.RaidErrno.ENUM_RAID_OK

    def startRaidStandbyChecker(self, srcPlayerBox, srcPlayerGbId, raidUUID, extraProps):
        LOG_INFO('startRaidStandbyChecker::', srcPlayerBox, srcPlayerGbId, raidUUID, extraProps)
        checkSrc = extraProps.pop('_checkSrc', gameconst.RaidDungeonStandbyCheckSrcEnum.DEFAULT)
        record, err = self._startRaidStandbyChecker(srcPlayerBox, srcPlayerGbId, raidUUID, checkSrc, extraProps)
        if err != gameconst.RaidErrno.ENUM_RAID_OK:
            _i_errLog = False
            if err == gameconst.RaidErrno.ENUM_RAID_DURING_STANDBY_CHECK:
                srcPlayerBox.onMessagePre(RAID_CONST.datas["raid_readyCheckUndergoing_msg"]["value"], [])
            else:
                _i_errLog = True

            (LOG_ERR if _i_errLog else LOG_WARN)('startRaidStandbyChecker:: failed, {}'.format(err))
            return

    def _startRaidStandbyChecker(self, srcPlayerBox, srcPlayerGbId, raidUUID,
                                 checkSrc, extraProps):
        if raidUUID not in self.raidDict:
            return None, gameconst.RaidErrno.ENUM_RAID_RAID_ID_NOT_FOUND

        raidVal = self.raidDict[raidUUID]
        if srcPlayerGbId != raidVal.raidLeaderGBID and not raidVal.isRaidDeputy(srcPlayerGbId):
            return None, gameconst.RaidErrno.ENUM_RAID_NOT_RAID_LEADER_OR_DEPUTY

        if self._fetchStandbyCheckerRecord(raidUUID):
            return None, gameconst.RaidErrno.ENUM_RAID_DURING_STANDBY_CHECK

        checkBoxesDic = {}
        broadcastExcludeGBIDs = []
        trueCount = falseCount = unknownCount = 0
        for _, memberGBID, memberVal in raidVal.iterGetRaidMember():
            if srcPlayerGbId == memberGBID:
                checkBoxesDic[memberGBID] = True
                trueCount += 1
                # 【【团队】团确时候，团员准备好没有打钩】
                # NOTE()(RAID): 客户端手动处理团长消息
                # broadcastExcludeGBIDs.append(memberGBID)
                continue

            if not memberVal.bOnline:
                checkBoxesDic[memberGBID] = False
                falseCount += 1
                broadcastExcludeGBIDs.append(memberGBID)
                continue

            checkBoxesDic[memberGBID] = None
            unknownCount += 1

        _timeout = utils.getConfirmMsgCooldown(RAID_CONST.datas["raid_readyCheck_check"]["value"], 30) + 2
        record = self._initStanbyCheckerRecord(
            raidUUID, checkBoxesDic, trueCount, falseCount, unknownCount, checkSrc,
            cbFn='onReplyRaidStandbyChecker', cbArgs=(raidUUID, False, {}),
            timeout=_timeout)
        # FIXME(): 后面可以通过传给客户端时间戳的方式弹窗, 防止弹窗(由于网络延迟)的原因服务端先于客户端结束
        if checkSrc == gameconst.RaidDungeonStandbyCheckSrcEnum.ENTER_DUNGEON:
            LOG_INFO('_startRaidStandbyChecker::raidEnterDungeonStandbyCheckNotify,', broadcastExcludeGBIDs, extraProps)
            record.extraProps.update(extraProps)
            _dungeonNo = extraProps.get('enterDungeonNo', 0)
            dungeonPlayMode = extraProps.get('dungeonPlayMode')
            dunLevel = dungeonPlayMode.dunLevel
        else:
            LOG_INFO('_startRaidStandbyChecker::raidStandbyCheckNotify,', broadcastExcludeGBIDs, extraProps)

        return record, gameconst.RaidErrno.ENUM_RAID_OK

    def replyRaidStandbyChecker(self, srcPlayerBox, srcPlayerGbId, raidUUID, beArgreed, extraProps):
        LOG_INFO('replyRaidStandbyChecker::', srcPlayerBox, srcPlayerGbId, raidUUID, beArgreed, extraProps)
        record, err = self._replyRaidStandbyChecker(srcPlayerBox, srcPlayerGbId, raidUUID, beArgreed, toClient=True)
        if err != gameconst.RaidErrno.ENUM_RAID_OK:
            if err == gameconst.RaidErrno.ENUM_RAID_CHECKING_STANDBY_CHECK:
                LOG_INFO('  replyRaidStandbyChecker:: skill checking...',
                         record.trueCount, record.falseCount, record.unknownCount)
            else:
                LOG_ERR('replyRaidStandbyChecker:: failed, {}'.format(err))
            return

        self.onReplyRaidStandbyChecker(raidUUID, record.isAllCheckSuccess(), extraProps)

    def _replyRaidStandbyChecker(self, srcPlayerBox, srcPlayerGbId, raidUUID, beAgreed, toClient=False):
        if raidUUID not in self.raidDict:
            return None, gameconst.RaidErrno.ENUM_RAID_RAID_ID_NOT_FOUND

        record = self._fetchStandbyCheckerRecord(raidUUID)    # type: _RaidStandbyCheckerVal
        if not record:
            return None, gameconst.RaidErrno.ENUM_RAID_STANDBY_RECORD_NOT_FOUND
        if srcPlayerGbId not in record.checkBoxesDic:
            return None, gameconst.RaidErrno.ENUM_RAID_PLAYER_GBID_NOT_FOUND
        if record.isChecked(srcPlayerGbId):
            return None, gameconst.RaidErrno.ENUM_RAID_STANDBY_ALREADY_CHECKED

        checkResult = record.checkIt(srcPlayerGbId, beAgreed)

        if not record.isAllChecked():
            return record, gameconst.RaidErrno.ENUM_RAID_CHECKING_STANDBY_CHECK

        return record, gameconst.RaidErrno.ENUM_RAID_OK

    def onReplyRaidStandbyChecker(self, raidUUID, result, extraProps):
        LOG_INFO('onReplyRaidStandbyChecker::', raidUUID, result, extraProps)

        def _check():
            if raidUUID not in self.raidDict:
                return None, gameconst.RaidErrno.ENUM_RAID_RAID_ID_NOT_FOUND
            return None, gameconst.RaidErrno.ENUM_RAID_OK

        _, err = _check()
        if err != gameconst.RaidErrno.ENUM_RAID_OK:
            LOG_WARN('onReplyRaidStandbyChecker:: check failed, {}'.format(err))
            self._popStandbyCheckerRecord(raidUUID)
            return

        _record = self._popStandbyCheckerRecord(raidUUID)    # Type: _RaidStandbyCheckerVal
        raidVal = self.raidDict[raidUUID]
        if _record.enterSrc == gameconst.RaidDungeonStandbyCheckSrcEnum.ENTER_DUNGEON:
            pass
        else:
            raidVal.broadcastToAllRaidMembersClient('onReplyRaidStandbyChecker', (raidUUID, result))

        # 【【任务】团队就位确认结果发送到团队频道】
        if result:
            raidVal.broadcastAllRaidMembersBase('onMessagePre', (M_M_DD.datas.raid_ready, []))
        else:
            for i_gbId, i_result in _record.checkBoxesDic.items():
                if i_result:
                    continue
                teamIdx = raidVal.getRaidTeamIDX(i_gbId)
                if teamIdx <= 0:
                    LOG_WARN('onReplyRaidStandbyChecker:: teamIdx not found', i_gbId, teamIdx, raidUUID)
                    continue
                pVal = raidVal.raidTeamDic[teamIdx].teamPlayerDict.get(i_gbId)
                if pVal:
                    raidVal.broadcastAllRaidMembersBase(
                        'onMessagePre', 
                        (RAID_CONST.datas["raid_unready_msg"]["value"], [pVal.playerName]))

        if not result:
            return

        if _record.enterSrc == gameconst.RaidDungeonStandbyCheckSrcEnum.ENTER_DUNGEON:
            dungeonNo, src = _record.extraProps.pop('enterDungeonNo'), _record.extraProps.pop('src')
            extraProps.update(_record.extraProps)
            LOG_INFO('onReplyRaidStandbyChecker:: enter dungeon', raidUUID, dungeonNo)
            _raidLeaderVal = raidVal.getRaidLeader()
            if _raidLeaderVal.playerBox and _raidLeaderVal.playerBox.cell:
                _raidLeaderVal.playerBox.cell.doCreateAndEnterRaidDungeon(raidUUID, dungeonNo, src, extraProps)

    def broadRaidChatMsg(self, srcPlayerBox, srcPlayerGbId, raidUUID, avatarInfo, broadMsg, extraProps):
        LOG_DBG('broadRaidChatMsg::', srcPlayerBox, srcPlayerGbId, raidUUID, broadMsg, extraProps, avatarInfo)
        _, err = self._broadRaidChatMsg(srcPlayerBox, srcPlayerGbId, raidUUID, avatarInfo, broadMsg)
        if err != gameconst.RaidErrno.ENUM_RAID_OK:
            LOG_WARN('broadRaidChatMsg:: failed, {}'.format(err))

    def _broadRaidChatMsg(self, srcPlayerBox, srcPlayerGbId, raidUUID, avatarInfo, broadMsg):
        if raidUUID not in self.raidDict:
            return None, gameconst.RaidErrno.ENUM_RAID_RAID_ID_NOT_FOUND
        raidVal = self.raidDict[raidUUID]
        raidVal.broadcastAllRaidMembersBase(
            'onRecvChannelMsg',
            (gameconst.ChatChannelEnum.RAID, avatarInfo, broadMsg), exclude=(srcPlayerGbId, ))
        return None, gameconst.RaidErrno.ENUM_RAID_OK

    # --------------------------------------------------------------------
    # RAID MICS
    def reqUpdateVoiceRoomState(self, srcPlayerGbId, raidUUID, voiceFlags):
        """客户端同步语音房间状态：inVoiceRoom/enableMics/enableSpeaker（轻量广播）
        voiceFlags: 0x01=inVoiceRoom, 0x02=enableMics, 0x04=enableSpeaker
        """
        if raidUUID not in self.raidDict:
            return
        raidVal = self.raidDict[raidUUID]
        for _teamVal in raidVal.raidTeamDic.values():
            member = _teamVal.teamPlayerDict.get(srcPlayerGbId)
            if member is not None:
                member.inVoiceRoom = (voiceFlags & 0x01) != 0
                member.enableMics = (voiceFlags & 0x02) != 0
                member.enableSpeaker = (voiceFlags & 0x04) != 0
                # 更新 cell 缓存
                raidVal.refreshPlayerPropsValToAllPlayers(_teamVal.teamIDX, srcPlayerGbId, member)
                # 轻量统一广播语音状态
                raidVal.broadcastMemberVoiceState(srcPlayerGbId)
                break

    def switchRaidMicsMode(self, srcPlayerBox, srcPlayerGbId, raidUUID, mode, extraProps):
        LOG_INFO("switchRaidMicsMode::", srcPlayerBox, srcPlayerGbId, raidUUID, mode, extraProps)
        raidVal, err = self._switchRaidMicsMode(srcPlayerBox, srcPlayerGbId, raidUUID, mode, extraProps)
        if err != gameconst.RaidErrno.ENUM_RAID_OK:
            LOG_WARN('switchRaidMicsMode:: failed, {}'.format(err))
            return

    def _switchRaidMicsMode(self, srcPlayerBox, srcPlayerGbId, raidUUID, mode, extraProps):
        if raidUUID not in self.raidDict:
            return None, gameconst.RaidErrno.ENUM_RAID_RAID_ID_NOT_FOUND
        raidVal = self.raidDict[raidUUID]
        return raidVal.switchRaidMiscMode(srcPlayerGbId, mode, extraProps, toClient=True)

    def turnOnRaidMics(self, srcPlayerBox, srcPlayerGbId, raidUUID, playerGBID, extraProps):
        LOG_INFO("turnOnRaidMics::", srcPlayerBox, srcPlayerGbId, raidUUID, playerGBID, extraProps)
        _, err = self._turnOnRaidMics(srcPlayerBox, srcPlayerGbId, raidUUID, playerGBID)
        if err != gameconst.RaidErrno.ENUM_RAID_OK:
            LOG_WARN('turnOnRaidMics:: failed, {}'.format(err))

    def _turnOnRaidMics(self, srcPlayerBox, srcPlayerGbId, raidUUID, playerGBID):
        if raidUUID not in self.raidDict:
            return None, gameconst.RaidErrno.ENUM_RAID_RAID_ID_NOT_FOUND
        raidVal = self.raidDict[raidUUID]
        teamIDX = raidVal.getRaidTeamIDX(playerGBID)
        return raidVal.turnOnRaidMemberMics(srcPlayerGbId, teamIDX, playerGBID, toClient=True)

    def turnOffRaidMics(self, srcPlayerBox, srcPlayerGbId, raidUUID, playerGBID, extraProps):
        LOG_INFO("turnOffRaidMics::", srcPlayerBox, srcPlayerGbId, raidUUID, playerGBID, extraProps)
        _, err = self._turnOffRaidMics(srcPlayerBox, srcPlayerGbId, raidUUID, playerGBID)
        if err != gameconst.RaidErrno.ENUM_RAID_OK:
            LOG_WARN('turnOffRaidMics:: failed, {}'.format(err))

    def _turnOffRaidMics(self, srcPlayerBox, srcPlayerGbId, raidUUID, playerGBID):
        if raidUUID not in self.raidDict:
            return None, gameconst.RaidErrno.ENUM_RAID_RAID_ID_NOT_FOUND
        raidVal = self.raidDict[raidUUID]
        teamIDX = raidVal.getRaidTeamIDX(playerGBID)
        return raidVal.turnOffRaidMemberMics(srcPlayerGbId, teamIDX, playerGBID, blockMics=False, toClient=True)

    def blockRaidMemberMics(self, srcPlayerBox, srcPlayerGbId, raidUUID, teamIDX, playerGBID, extraProps):
        LOG_INFO("blockRaidMemberMics::", srcPlayerBox, srcPlayerGbId, raidUUID, teamIDX, playerGBID, extraProps)
        _, err = self._blockRaidMemberMics(srcPlayerBox, srcPlayerGbId, raidUUID, teamIDX, playerGBID)
        if err != gameconst.RaidErrno.ENUM_RAID_OK:
            LOG_WARN('blockRaidMemberMics:: failed, {}'.format(err))

    def _blockRaidMemberMics(self, srcPlayerBox, srcPlayerGbId, raidUUID, teamIDX, playerGBID):
        if raidUUID not in self.raidDict:
            return None, gameconst.RaidErrno.ENUM_RAID_RAID_ID_NOT_FOUND
        raidVal = self.raidDict[raidUUID]
        return raidVal.turnOffRaidMemberMics(srcPlayerGbId, teamIDX, playerGBID, blockMics=True, toClient=True)

    def unblockRaidMemberMics(self, srcPlayerBox, srcPlayerGbId, raidUUID, teamIDX, playerGBID, extraProps):
        LOG_INFO("unblockRaidMemberMics::", srcPlayerBox, srcPlayerGbId, raidUUID, teamIDX, playerGBID, extraProps)
        _, err = self._unblockRaidMemberMics(srcPlayerBox, srcPlayerGbId, raidUUID, teamIDX, playerGBID)
        if err != gameconst.RaidErrno.ENUM_RAID_OK:
            LOG_WARN('unblockRaidMemberMics:: failed, {}'.format(err))
            if err == gameconst.RaidErrno.ENUM_RAID_ALL_MICS_BLOCKED:
                srcPlayerBox.onMessagePre(M_M_DD.datas.voiceChat_allMicBanned, [])

    def _unblockRaidMemberMics(self, srcPlayerBox, srcPlayerGbId, raidUUID, teamIDX, playerGBID):
        if raidUUID not in self.raidDict:
            return None, gameconst.RaidErrno.ENUM_RAID_RAID_ID_NOT_FOUND
        raidVal = self.raidDict[raidUUID]
        return raidVal.unblockRaidMemberMisc(srcPlayerGbId, teamIDX, playerGBID, toClient=True)

    # --------------------------------------------------------------------

    # ----------------------------------------------------------------------
    # RAID DUNGEON METHODS
    # 团队副本相关
    # ----------------------------------------------------------------------

    def createAndEnterRaidDungeonPreCheck(self, srcPlayerBox, srcPlayerGbId,
                                          raidUUID, dungeonNo, src, extraProps):
        LOG_INFO('createAndEnterRaidDungeonPreCheck', srcPlayerBox, srcPlayerGbId,
                  raidUUID, dungeonNo, src, extraProps)
        _, err = self._createAndEnterRaidDungeonPreCheck(srcPlayerBox, srcPlayerGbId, raidUUID, dungeonNo, src)
        if err != gameconst.RaidDunErrno.ENUM_RAIDDUN_OK:
            LOG_ERR('createAndEnterRaidDungeonPreCheck:: failed, {}'.format(err))
            return

        srcPlayerBox.cell.onCreateAndEnterRaidDungeonCheckOk(raidUUID, dungeonNo, src, extraProps)

    def _createAndEnterRaidDungeonPreCheck(self, srcPlayerBox, srcPlayerGbId,
                                           raidUUID, dungeonNo, src):
        if raidUUID not in self.raidDict:
            return None, gameconst.RaidDunErrno.ENUM_RAIDDUN_RAID_ID_NOT_FOUND
        raidVal = self.raidDict[raidUUID]
        if srcPlayerGbId != raidVal.raidLeaderGBID:
            return None, gameconst.RaidDunErrno.ENUM_RAIDDUN_NOT_RAID_LEADER
        if dungeonNo in raidVal.raidDungeonRecords:
            return None, gameconst.RaidDunErrno.ENUM_RAIDDUN_RAID_ALREADY_EXIST_DUNGEON
        return None, gameconst.RaidDunErrno.ENUM_RAIDDUN_OK

    def createAndEnterRaidDungeonPostCheck(self, srcPlayerBox, srcPlayerGbId,
                                           raidUUID, dungeonNo, spaceNo, spaceUUID,
                                           spaceBox, spaceMgrBox, src, extraProps):
        LOG_INFO('createAndEnterRaidDungeonPostCheck::', srcPlayerBox, srcPlayerGbId,
                  raidUUID, dungeonNo, spaceNo, spaceUUID, spaceBox, spaceMgrBox, src, extraProps)
        _, err = self._createAndEnterRaidDungeonPostCheck(srcPlayerBox, srcPlayerGbId,
                                                          raidUUID, dungeonNo, spaceNo,
                                                          spaceUUID, src)
        dungeonStub = gameengine.getDungeonStubByDungeonNo(dungeonNo, gameconst.DungeonEnterTypeEnum.RAID)
        if err != gameconst.RaidDunErrno.ENUM_RAIDDUN_OK:
            LOG_ERR('createAndEnterRaidDungeonPostCheck:: failed, {}'.format(err))
            # 重复创建副本, 删除刚刚创建的副本
            dungeonStub.destoryDungeonSpace(spaceNo, spaceUUID, 'duplicated-create')
        else:
            raidVal = self.raidDict[raidUUID]
            raidVal.setRaidDungeonInfo(dungeonNo, spaceNo, spaceUUID,
                                       spaceBox, spaceMgrBox, toClient=True, toCell=True)
            self.setInDungeon(raidUUID, True)
            raidVal.broadcastAllRaidMembersBase(
                'doEnterRaidDungeonSelfCheck',
                (dungeonNo, spaceNo, spaceUUID, spaceBox, spaceMgrBox, src, extraProps))

        # 无论如何, 都需要到raidDungeonStub上释放锁
        dungeonStub.releaseRaidDungeonCreatingLock(raidUUID)

    def _createAndEnterRaidDungeonPostCheck(self, srcPlayerBox, srcPlayerGbId,
                                            raidUUID, dungeonNo, spaceNo, spaceUUID,
                                            src):
        if raidUUID not in self.raidDict:
            return None, gameconst.RaidDunErrno.ENUM_RAIDDUN_RAID_ID_NOT_FOUND

        raidVal = self.raidDict[raidUUID]
        if dungeonNo in raidVal.raidDungeonRecords:
            return None, gameconst.RaidDunErrno.ENUM_RAIDDUN_RAID_ALREADY_EXIST_DUNGEON

        return None, gameconst.RaidDunErrno.ENUM_RAIDDUN_OK

    def onLoadRaidDungeonSpaceReady(self, srcPlayerBox, srcPlayerGbId, raidUUID,
                                    dungeonNo, spaceNo, spaceUUID, spaceBox,
                                    spaceMgrBox, extraProps):
        """团队副本创建完成后回调"""
        LOG_INFO('onLoadRaidDungeonSpaceReady::', srcPlayerBox, srcPlayerGbId,
                  dungeonNo, spaceNo, spaceMgrBox, extraProps)
        src = extraProps.pop('src')     # 这里一定要有src
        self.createAndEnterRaidDungeonPostCheck(srcPlayerBox, srcPlayerGbId, raidUUID,
                                                dungeonNo, spaceNo, spaceUUID, spaceBox,
                                                spaceMgrBox, src, extraProps)

    def onRaidDungeonCompletedCB(self, raidUUID, dungeonNo, spaceNo, spaceUUID):
        self.clearRaidDungeonInfo(raidUUID, dungeonNo, spaceNo, spaceUUID)
        self.raidPrepareAutoMatch(raidUUID)
        # # 解散团队
        # delRaidVal = self.raidDict.get(raidUUID, None)
        # if not delRaidVal:
        #     LOG_WARN('onRaidDungeonCompletedCB:: failed, missing raid')
        #     return

        # self.doDisbandRaid(raidUUID, {})

        # delRaidVal.clearRaidCacheValToAllPlayers()
        # delRaidVal.broadcastToAllRaidMembersClient('onDisbandRaid', (raidUUID, ))

    def clearRaidDungeonInfo(self, raidUUID, dungeonNo, spaceNo, spaceUUID):
        _, _err = self._clearRaidDungeonInfo(raidUUID, dungeonNo, spaceNo, spaceUUID)
        if _err != gameconst.RaidDunErrno.ENUM_RAIDDUN_OK:
            LOG_WARN('clearRaidDungeonInfo:: missing with err, {}'.format(_err))

    def _clearRaidDungeonInfo(self, raidUUID, dungeonNo, spaceNo, spaceUUID):
        if raidUUID not in self.raidDict:
            return None, gameconst.RaidDunErrno.ENUM_RAIDDUN_RAID_ID_NOT_FOUND

        raidVal = self.raidDict[raidUUID]
        raidVal.clearRaidDungeonInfo(dungeonNo, spaceNo, spaceUUID, toCell=True, toClient=True)
        return None, gameconst.RaidDunErrno.ENUM_RAIDDUN_OK

    # ----------------------------------------------------------------------
    def queryEliteMonsteBelongName(self, monsterBox, raidUUID):
        raidVal = self.raidDict.get(raidUUID)
        if not raidVal:
            return
        LOG_INFO('queryEliteMonsteBelongName:', raidUUID)
        monsterBox.setMonsterBelongRaidName(raidUUID, raidVal.getRaidLeader().playerName)
        return

    def broadRaidMemMessage(self, raidUUID, msgId, msgArgs):
        LOG_DBG('broadRaidMemMessage:', raidUUID, msgId, msgArgs)
        _raidVal = self.raidDict.get(raidUUID)
        if not _raidVal:
            return
        _raidVal.broadcastAllRaidMembersBase('onMessagePre', (msgId, msgArgs))

    def broadRaidMemMessage_localCross(self, raidUUID, msgId, msgArgs):
        LOG_DBG('broadRaidMemMessage_localCross:', raidUUID, msgId, msgArgs)
        raidVal = self.raidDict.get(raidUUID)
        if not raidVal:
            return
        raidVal.broadcastAllRaidMembersBase('onMessagePre_localCross', (msgId, msgArgs))

    # ----------------------------------------------------------------------
    def askAllMemberFollowRaidStub(self, srcPlayerBox, raidUUID, srcPlayerGbId, spaceNo, pos):
        _, err = self._askAllMemberFollow(srcPlayerBox, raidUUID, srcPlayerGbId, spaceNo, pos)
        if err != gameconst.RaidErrno.ENUM_RAID_OK:
            LOG_WARN('askAllMemberFollowRaidStub:: failed, {}'.format(err))

    def _askAllMemberFollow(self, srcPlayerBox, raidUUID, srcPlayerGbId, spaceNo, pos):
        if raidUUID not in self.raidDict:
            return None, gameconst.RaidErrno.ENUM_RAID_RAID_ID_NOT_FOUND

        raidVal = self.raidDict[raidUUID]
        for _teamIdx, memberGBID, memberVal in raidVal.iterGetRaidMember():
            if not memberVal.bOnline:
                continue

            if memberGBID == raidVal.raidLeaderGBID:
                continue

            if not (memberVal.playerBox and memberVal.playerBox.client):
                LOG_WARN('_askAllMemberFollow::raidMember has no client', _teamIdx, memberGBID, memberVal.playerBox)
                continue

            memberVal.playerBox.client.onFollowTeamCaptainAsk(spaceNo, pos)

        srcPlayerBox.onMessagePre(RAID_CONST.datas["raid_captainSummonDone_msg"]["value"], [])
        return None, gameconst.RaidErrno.ENUM_RAID_OK

    # ----------------------------------------------------------------------

    def getRaidByRaidUUID(self, raidUUID):
        if raidUUID not in self.raidDict:
            LOG_WARN('getRaidByRaidUUID raidUUID error', raidUUID)
            return
        return self.raidDict[raidUUID]

    def raidPrepareAutoMatch(self, raidUUID):
        LOG_INFO('in raidPrepareAutoMatch:', raidUUID)
        raidVal = self.getRaidByRaidUUID(raidUUID)
        if not raidVal:
            return
        
        if raidVal.isEmpty():
            self.doDisbandRaid(raidVal.raidUUID, {})
            return
        
        if raidVal.isRaidFull():
            return
        
        if not raidVal.checkRaidTarget(raidVal.raidMinLevel, raidVal.raidMinScore):
            return
        if raidVal.isRaidFull():
            LOG_WARN('in raidPrepareAutoMatch, raid full:', raidVal)
            raidVal.getRaidLeaderBox().onMessagePre(TMMCD.datas['teamMatch_raidFullMsg']['value'], [])
            return
        raidVal.startAutoMatch()

    def raidPrepareStopAutoMatch(self, raidUUID):
        LOG_INFO('in raidPrepareStopAutoMatch:', raidUUID)
        raidVal = self.getRaidByRaidUUID(raidUUID)
        if not raidVal:
            return
        raidVal.stopAutoMatch()

    def newRaidPlayerMatched(self, raidUUID, playerProps):
        teamVal = self.getRaidByRaidUUID(raidUUID)
        LOG_INFO('in newRaidPlayerMatched:', raidUUID, playerProps, teamVal)
        if not teamVal:
            return
        playerProps['joinType'] = gameconst.TeamJoinType.MATCH
        if teamVal.addNewMember(playerProps['playerGbId'], playerProps, toClient=True):
            if teamVal.isRaidFull():
                LOG_INFO('in newRaidPlayerMatched, raid is full, stop match ~:', raidUUID, playerProps, teamVal)
                teamVal.stopAutoMatch()
        return

    def getRaidList(self, box, raidTarget, checkTime, checkTeamstubNum, sendTeamNum, startTeamStubIndex):
        LOG_DBG('in getRaidList:', raidTarget, checkTime, checkTeamstubNum, sendTeamNum, startTeamStubIndex)
        raidList = []
        # 根据队伍的创建时间排序，最晚创建的队伍在最前面
        releaseNum = gameconst.RAID_LSIT_MAX_NUM - sendTeamNum
        sortedDic = sorted(self.raidDict.items(), key=lambda x: x[1].raidCreateTime, reverse=True)
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
        LOG_INFO('raidStub:enterRaidChiefDungeon::', gbId, dungeonNo, extra)
        if raidUUID not in self.raidDict:
            return

        raidVal = self.raidDict[raidUUID]

        remainTime = raidVal.lastDungeonFinishedTime - utils.curTS()
        if remainTime > 0:
            gameengine.getGlobalBase('PlayerStub').doOnOthersBase(
                                [gbId, ], 'onMessagePre', (TDC_CFG.datas['raid_rejoinCd']['value'], [str(remainTime)]),
                                None, '', ())
            return
        
        dunPlayMode = extra['dungeonPlayMode']
        src = extra['src']

        box.enterRaidDungeon(dungeonNo, src, {
            'dungeonPlayMode': dunPlayMode
        })

    # ------------------------ 标记相关 --------------------------
    def addTeamMarkDataFromTeam(self, raidUUID, markDataInfo):
        LOG_INFO('addTeamMarkDataFromTeam: ', raidUUID, markDataInfo)
        if raidUUID not in self.raidDict:
            return

        raidVal = self.raidDict[raidUUID]
        raidVal.addRaidMarkMemberFromData(markDataInfo)

    def reqAddRaidMarkMember(self, raidUUID, playerBox, type, index, name, gbId, entId, pos, box):
        LOG_INFO('reqAddRaidMarkMember: ', raidUUID, playerBox, type, index, name, gbId, entId, pos, box)
        if raidUUID not in self.raidDict:
            return

        # 要先执行删除
        self.reqDelRaidMarkMember(raidUUID, playerBox, type, index)

        raidVal = self.raidDict[raidUUID]
        raidVal.addRaidMarkMember(playerBox, type, index, name, gbId, entId, pos)
        # 记录
        if type == gameconst.TeamMarkType.MARK_ENEMY and entId > 0:
            self.addRaidMarkMonsterRec(raidUUID, entId, index, box)

    def addRaidMarkMonsterRec(self, teamId, entId, index, box):
        # 满了说明处理逻辑有问题，功能暂停
        if len(self.teamMarkMonsterRec) >= 20000:
            LOG_INFO('addRaidMarkMonsterRec, mark monster rec full ', len(self.teamMarkMonsterRec))
            return
        if not self.teamMarkMonsterRec.get(entId, None):
            self.teamMarkMonsterRec[entId] = {0: box}

        if len(self.teamMarkMonsterRec[entId]) >= 10000:
            LOG_INFO('addRaidMarkMonsterRec, mark monster rec full for entId: ', entId, len(self.teamMarkMonsterRec[entId]))
            return
        self.teamMarkMonsterRec[entId][teamId] = index
        LOG_INFO('addRaidMarkMonsterRec, mark monster rec:', entId, teamId, index)

        box.onBeMarkedAsEnemy(teamId, gameconst.TeamType.RAID, index)

    def delMarkMonsterRec(self, teamId, entId):
        if entId not in self.teamMarkMonsterRec:
            return
        if teamId in self.teamMarkMonsterRec[entId]:
            self.teamMarkMonsterRec[entId].pop(teamId)
            LOG_INFO('delMonsterRec, del mark monster rec:', entId, teamId)
            box = self.teamMarkMonsterRec[entId].get(0, None)
            if box:
                box.delBeMarkedAsEnemy(teamId, gameconst.TeamType.TEAM)

        if len(self.teamMarkMonsterRec[entId]) <= 1:
            self.teamMarkMonsterRec.pop(entId)
            LOG_INFO('delMarkMonsterRec, remove mark monster rec box:', entId)

    def reqDelRaidMarkMember(self, raidUUID, playerBox, type, index):
        LOG_INFO('reqDelRaidMarkMember: ', raidUUID, playerBox, type, index)
        if raidUUID not in self.raidDict:
            return

        raidVal = self.raidDict[raidUUID]
        entId = raidVal.delRaidMarkMember(playerBox, type, index)

        self.delMarkMonsterRec(raidUUID, entId)

    def onMarkMonsterDead(self, entId):
        if entId not in self.teamMarkMonsterRec:
            return
        teamInfo = self.teamMarkMonsterRec.get(entId, {})
        LOG_INFO('onMarkMonsterDead, remove mark monster:', entId, teamInfo)
        teamInfo = copy.deepcopy(teamInfo)
        for teamId, index in teamInfo.items():
            self.reqDelRaidMarkMember(teamId, None, gameconst.TeamMarkType.MARK_ENEMY, index)

    def reqChangeRaidOnlyLeader(self, raidUUID, playerBox, bOnlyCapatain):
        LOG_INFO('reqChangeRaidOnlyLeader: ', raidUUID, playerBox, bOnlyCapatain)
        if raidUUID not in self.raidDict:
            return

        raidVal = self.raidDict[raidUUID]
        raidVal.changeRaidOnlyLeader(playerBox, bOnlyCapatain)

    def reqJoinRaid(self, playerBox, raidUUID, password, playerProps):
        raidVal, err = self._reqJoinRaidCheck(raidUUID, password, playerProps)
        # 加入成功，刷新一下成员的cache
        if err != gameconst.RaidErrno.ENUM_RAID_OK:
            LOG_ERR("reqJoinRaid, err:", err, playerProps)
            return
        raidVal.refreshRaidCacheValToAllPlayers()

    def _reqJoinRaidCheck(self, raidUUID, password, playerProps):
        raidVal = self.getRaidByRaidUUID(raidUUID)
        LOG_INFO('in _reqJoinRaidCheck:', raidUUID, playerProps, raidVal)
        if not raidVal:
            return None, gameconst.RaidErrno.ENUM_RAID_RAID_ID_NOT_FOUND

        # 非公开的需要检查一下密码
        if not raidVal.isPublish:
            if raidVal.password != password:
                return None, gameconst.RaidErrno.ENUM_RAID_PASSWORD_IS_WRONG

        raidTargetInfo = TMACTD.datas.get(raidVal.raidTarget)
        if raidTargetInfo is None:
            LOG_ERR("_reqJoinRaidCheck, misssing raidTarget", raidVal.raidTarget)
            return None, gameconst.RaidErrno.ENUM_UNKNOWN
        score = playerProps['score']
        level = playerProps['level']
        cfgMinLv = raidTargetInfo['minLevel']
        cfgMinScore = raidTargetInfo['minScore']
        if level < cfgMinLv:
            return None, gameconst.RaidErrno.ENUM_RAID_LEVEL_IS_LIMITED
        if score < cfgMinScore:
            return None, gameconst.RaidErrno.ENUM_RAID_SCORE_LIMITED

        _, err = raidVal.addNewMember(playerProps['playerGbId'], playerProps, toClient=True)

        return raidVal, err

    def setInDungeon(self, raidId, status):
        LOG_INFO('raidStub::setInDungeon, ', raidId, status)
        raidVal = self.raidDict.get(raidId, None)
        if not raidVal:
            LOG_WARN('setInDungeon, not found raid:', raidId)
            return
        raidVal.isInDungeon = status

    def checkInDungeon(self, raidId):
        raidVal = self.raidDict.get(raidId, None)
        if not raidVal:
            LOG_WARN('setInDungeon, not found raid:', raidId)
            return False
        return raidVal.isInDungeon
    
    def refreshLastDungeonFinishedTime(self, raidId, lastDungeonFinishedTime):
        LOG_INFO("refreshLastDungeonFinishedTime", raidId, lastDungeonFinishedTime)
        raidVal = self.raidDict.get(raidId, None)
        if not raidVal:
            LOG_WARN('refreshLastDungeonFinishedTime, not found raid:', raidId)
            return
        raidVal.lastDungeonFinishedTime = lastDungeonFinishedTime + TDC_CFG.datas['raid_rejoinCdTime']['value']

        raidVal.broadcastToAllMembersClient('onRefreshLastDungeonFinishedTime', (gameconst.TeamType.RAID, raidVal.lastDungeonFinishedTime))

    def modifyPlayerName(self, box, raidUUID, gbId, newName, oldName):
        raidVal = self.raidDict.get(raidUUID, None)
        if not raidVal:
            LOG_WARN('modifyPlayerName, not found raid:', raidUUID)
            return
        self.updateRaidMemberCacheVal(raidUUID, box, gbId, {'playerName': newName})
        raidVal.broadcastToAllMembersBase('onMessagePre', (TM_MCD.datas['teammateChangeNameMsg']['value'], [oldName, newName]), exclude=(gbId,))

    def broadcastToAllMembers(self, box, gbId, raidUUID, exclude, comp, func, args):
        LOG_INFO("broadcastToAllMembers raid", gbId, raidUUID, exclude, comp, func, args)
        raidVal = self.raidDict.get(raidUUID, None)
        if not raidVal:
            LOG_WARN('broadcastToAllMembers, not found raid')
            return
        if gameconst.CELL == comp:
            raidVal.broadcastToAllMembersCell(func, args, exclude)
        else:
            raidVal.broadcastToAllMembersBase(func, args, exclude)
