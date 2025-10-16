# coding: utf-8
from KBEDebug import *
import KBEngine

import functools

import gamedecorator
import gameengine
import gameconst
import gametimer
import gametlog
import dataUtils
import utils

import message_Message_def as MMD
import raid_raidConst as RAID_CONST
import visible_visible as UVVD
import teamMatch_matchConfig as TMMCD
import activityControl_activityData as AC_ADD
import teamMatch_activity as TMACTD

import raid
import dungeonSrc


def raidPermissionCheck(needPermission=gameconst.RaidPermission.UNKNOWN, onlyMode=False, exclude=()):
    def _raidPermission(fn):
        @functools.wraps(fn)
        def __wrapper(self, *args, **kwargs):
            selfPermission = self.raidPermission
            if not gameconst.RaidPermission.havePermission(selfPermission, needPermission,
                                                           onlyMode=onlyMode, exluce=exclude):
                WARNING_MSG('wrapper::raidPermission::{}, permission denied'.format(fn.__name__),
                            selfPermission, needPermission)
                return
            return fn(self, *args, **kwargs)
        return __wrapper
    return _raidPermission


def lockRaid(timeout=3):
    assert timeout > 0
    def _lockRaid(fn):
        @functools.wraps(fn)
        def __wrapper(self, *args, **kwargs):
            _m_lockedSucc = self._lockRaidProcess(timeout=timeout)
            if not _m_lockedSucc:
                ERROR_MSG("lockRaid::", fn.__name__, args, kwargs)
                return
            _r = fn(self, *args, **kwargs)
            if not _r:
                WARNING_MSG(f"lockRaid::{fn.__name__}:: auto fail unlocked")
                self._unlockRaidProcess()
        return __wrapper
    return _lockRaid


def unlockRaid(fn):
    @functools.wraps(fn)
    def __wrapper(self, *args, **kwargs):
        self._unlockRaidProcess()
        return fn(self, *args, **kwargs)
    return __wrapper


class ImpRaid(object):

    # ---------------------------------------------------------------
    # Cache Lock

    def _lockRaidProcess(self, timeout):
        if self.isRaidLocked():
            return False
        self.raidProcessLock = utils.getNow() + timeout
        return True

    def _unlockRaidProcess(self):
        self.raidProcessLock = 0

    def isRaidLocked(self):
        if utils.getNow() > self.raidProcessLock:
            return False
        return True

    # --------------------------------------------------------------

    @property
    def createRaidWithTeamCheckRecord(self) -> dict:
        if not self.hasTempMiscProp(gameconst.AvatarProps.raidCreateRaidTeamCheck):
            self.setTempMiscProp(gameconst.AvatarProps.raidCreateRaidTeamCheck, {})
        return self.getTempMiscProp(gameconst.AvatarProps.raidCreateRaidTeamCheck)

    @createRaidWithTeamCheckRecord.setter
    def createRaidWithTeamCheckRecord(self, newValue):
        self.setTempMiscProp(gameconst.AvatarProps.raidCreateRaidTeamCheck, newValue)

    def clearCreateRaidWithTeamCheckRecord(self):
        self.createRaidWithTeamCheckRecord.clear()

    def isInRaid(self):
        return bool(self.raidInfo.raidUUID)

    def isInRaidLeaderTeam(self):
        return self.raidInfo.raidTeamIDX == self.raidInfo.raidLeaderTeamIDX

    def isRaidLeader(self):
        return self.raidInfo.raidLeaderGBID and self.gbId == self.raidInfo.raidLeaderGBID

    def isRaidDeputy(self):
        return self.raidInfo.raidDeputyGBID and self.gbId == self.raidInfo.raidDeputyGBID
    
    def isRaidCaptain(self):
        return self.gbId == self.raidInfo.raidCaptainGBID

    def isInSameRaidTeam(self, target):
        return self.raidId and self.raidId == target.raidId and self.raidInfo.raidTeamIDX == target.raidInfo.raidTeamIDX

    def getRaidLeaderGBID(self):
        return self.raidInfo.raidLeaderGBID

    def forceRefreshRaidCache(self):
        WARNING_MSG('forceRefreshRaidCache:: ~')

        def _check():
            if not self.isInRaid():
                return None, gameconst.RaidErrno.RAID_NOT_IN_RAID
            return None, gameconst.RaidErrno.RAID_OK
        _, err = _check()
        if err != gameconst.RaidErrno.RAID_OK:
            ERROR_MSG('forceRefreshRaidCache::, failed, {}'.format(err))
            return

        raidUUID = self.raidUUID
        extraProps = {}
        gameengine.getRaidStub(raidUUID).refreshRaidCache(raidUUID, [self.gbId], extraProps)

    def onRefreshPlayerRaidCacheVal(self, newRaidCacheVal: raid.PlayerRaidCacheVal):
        DEBUG_MSG('onRefreshPlayerRaidCacheVal::', newRaidCacheVal.raidUUID)
        self.raidInfo = newRaidCacheVal
        for teamVal in self.raidInfo.raidTeamDic.values():
            if self.gbId in teamVal.teamPlayerDic:
                self.raidInfo.raidTeamIDX = teamVal.teamIDX
                # self.raidInfo.raidCaptainGBID = teamVal.teamCaptainGBID

        self.raidUUID = newRaidCacheVal.raidUUID
        # 【【程序自主】团队中团员职务暴露给所有客户端】
        self.raidAuth = self.raidPermission
        '''
        if oldRaidUUID != self.raidUUID:
            self.checkEliteInvRaidUUID(oldRaidUUID, self.raidUUID)
        '''

    def onRefreshPlayerRaidMemberCacheVal(self, raidUUID, teamIDX, playerGBID, propsDic, needDel):
        DEBUG_MSG('onRefreshPlayerRaidMemberCacheVal::', raidUUID, teamIDX, playerGBID, needDel)
        raidTeamMemberVal, err = self._onRefreshPlayerRaidMemberCacheVal(raidUUID, teamIDX, playerGBID, propsDic, needDel)
        if err != gameconst.RaidErrno.RAID_OK:
            WARNING_MSG('onRefreshPlayerRaidMemberCacheVal:: failed, {}'.format(err))
            return

    def _onRefreshPlayerRaidMemberCacheVal(self, raidUUID, teamIDX, playerGBID, newRaidTeamMemberCacheValDic, needDel):
        errno = gameconst.RaidErrno
        if raidUUID != self.raidInfo.raidUUID:
            return None, errno.RAID_RAID_ID_NOT_MATCH.initkvbody(source='_onRefreshPlayerRaidMemberCacheVal',
                                                                 orgRaidUUID=self.raidInfo.raidUUID,
                                                                 crtRaidUUID=raidUUID)

        raidTeamVal = self.raidInfo.raidTeamDic.get(teamIDX, None)
        if not raidTeamVal:
            return None, errno.RAID_TEAM_IDX_NOT_FOUND.initkvbody(source='_onRefreshPlayerRaidMemberCacheVal',
                                                                  raidUUID=raidUUID,
                                                                  teamIDX=teamIDX)

        raidTeamMemberVal = raidTeamVal.teamPlayerDic.get(playerGBID, None)
        if not raidTeamMemberVal:
            return None, errno.RAID_PLAYER_GBID_NOT_FOUND.initkvbody(source='_onRefreshPlayerRaidMemberCacheVal',
                                                                     raidUUID=raidUUID,
                                                                     teamIDX=teamIDX,
                                                                     playerGBID=playerGBID)

        if needDel:
            raidTeamVal.teamPlayerDic.pop(playerGBID)
        else:
            raidTeamMemberVal.updateAttr(newRaidTeamMemberCacheValDic)

        return raidTeamMemberVal, errno.RAID_OK

    def __init__(self):
        if not hasattr(self, 'raidInfo'):
            # 团队在Avatar身上的缓存, cell私有
            self.raidInfo = raid.PlayerRaidCacheVal()
        if not hasattr(self, 'raidId'):
            # 团队ID, 固化ID, ALL_CLIENTS
            # NOTE: DO NOT USE 'raidId' directly, try use property 'raidUUID'
            self.raidId = 0
        if not hasattr(self, 'raidAuth'):
            # 团队权限, ALL_CLIENTS
            self.raidAuth = self.raidPermission

    def isUIVisible(self, value):
        lvLimit = UVVD.datas.get(value, {}).get('level', utils.getPlayerMaxLevel()+1)
        return self.level >= lvLimit

    @property
    def raidBeInvitedRecord(self) -> dict:
        """受到团队(团长/队长)邀请记录"""
        if not self.hasTempMiscProp(gameconst.AvatarProps.raidBeInvitedRecord):
            self.setTempMiscProp(gameconst.AvatarProps.raidBeInvitedRecord, {})
        return self.getTempMiscProp(gameconst.AvatarProps.raidBeInvitedRecord)

    @property
    def raidJoinRecord(self) -> dict:
        """申请加入团队记录"""
        if not self.hasTempMiscProp(gameconst.AvatarProps.raidJoinRecord):
            self.setTempMiscProp(gameconst.AvatarProps.raidJoinRecord, {})
        return self.getTempMiscProp(gameconst.AvatarProps.raidJoinRecord)

    @property
    def raidAvatarPropsCache(self) -> dict:
        """玩家属性缓存, 用于raidTick刷新raidStub缓存"""
        if not self.hasTempMiscProp(gameconst.AvatarProps.raidAvatarPropsCache):
            self.setTempMiscProp(gameconst.AvatarProps.raidAvatarPropsCache, {})
        return self.getTempMiscProp(gameconst.AvatarProps.raidAvatarPropsCache)

    @property
    def raidUUID(self):
        return self.raidId

    @raidUUID.setter
    def raidUUID(self, newRaidUUID):
        self._autoCtrlRaidTimer(self.raidId, newRaidUUID)
        oldRaidId = self.raidId
        if oldRaidId != newRaidUUID:
            self.raidId = newRaidUUID
            self.resetAllTargetTypeCache()
        if not oldRaidId and newRaidUUID:
            self._unlockRaidProcess()
            self._onEnterNewRaid()
        self.base.onRaidChanged(self.raidId)

    def _onEnterNewRaid(self):
        if self.isCanLeaveTeam():
            gameengine.getTeamStub(self.teamId).leaveTeam(self.base, self.teamId, self.gbId, True)
        self._reqPlayerStopAutoMatch()

    @property
    def raidTickTimerId(self):
        return self.getTempMiscProp(gameconst.AvatarProps.raidTickTimerId, 0)

    @raidTickTimerId.setter
    def raidTickTimerId(self, newTimerId):
        self.setTempMiscProp(gameconst.AvatarProps.raidTickTimerId, newTimerId)

    @property
    def raidPermission(self):
        """获取团队权限"""
        if not self.isInRaid():
            return gameconst.RaidPermission.UNKNOWN

        if self.isRaidLeader():
            return gameconst.RaidPermission.LEADER

        elif self.isRaidDeputy():
            return gameconst.RaidPermission.DEPUTY
        '''
        #
        elif self.isRaidCaptain():
            return gameconst.RaidPermission.CAPTAIN
        '''
        return gameconst.RaidPermission.MEMBER

    def raidTick(self):
        """刷新团队成员在raidStub上的一些缓存"""
        if not self.isInRaid():
            ERROR_MSG('raidTick:: not in raid')
            self.stopRaidTimer()
            return

        modified = False
        lastRecord = self.raidAvatarPropsCache

        if 'level' not in lastRecord or lastRecord['level'] != self.level:
            lastRecord['level'] = self.level
            modified = True
        pos = tuple(self.position)
        if 'spaceNo' not in lastRecord or lastRecord['spaceNo'] != self.spaceNo or 'position' not in lastRecord or lastRecord['position'] != pos:
            lastRecord['spaceNo'] = self.spaceNo
            lastRecord['position'] = pos
            modified = True
        if 'hp' not in lastRecord or lastRecord['hp'] != self.hp or 'fullHp' not in lastRecord or lastRecord['fullHp'] != self.fullHp:
            lastRecord['hp'] = self.hp
            lastRecord['fullHp'] = self.fullHp
            modified = True
        if 'playerName' not in lastRecord or lastRecord['playerName'] != self.name:
            lastRecord['playerName'] = self.name
            modified = True

        oldScore = lastRecord.get('score', 0)
        newScore = self.getTotalScore()

        if 'score' not in lastRecord or oldScore != newScore:
            DEBUG_MSG("in raidTick, score updated:", oldScore, newScore)
            lastRecord['score'] = newScore
            modified = True

        if modified:
            excludedPlayerIDs = (self.gbId,)
            if 'spaceNo' in lastRecord and 'position' in lastRecord:
                for teamIDX, memberGBID, memberVal in self.raidInfo.iterGetRaidMember():
                    if memberGBID == self.gbId or not memberVal.playerBox:
                        continue
                    # 当只有spaceNo和position两个一起更新时，做一下筛选，视野范围内的就不需要通知了
                    if 'spaceNo' in lastRecord and 'position' in lastRecord and len(lastRecord) == 2:
                        if self.checkInView(memberVal.playerBox.id):
                            excludedPlayerIDs += (memberGBID,)
            lastRecord['excludedGbIDs'] = excludedPlayerIDs
            gameengine.getRaidStub(self.raidId).updateRaidMemberCacheVal(self.raidId, self.gbId, lastRecord)

        if self.followCaptain in (gameconst.TeamFollowState.Follow, gameconst.TeamFollowState.Suspending):
            self.followCaptainCheck()

    def clearRaidCacheBoxOnOffline(self):
        if self.raidUUID > 0:
            DEBUG_MSG('clearRaidCacheBoxOnOffline set all playerBox to None')
            for teamIDX, memberGBID, memberVal in self.raidInfo.iterGetRaidMember():
                memberVal.playerBox = None

    def startRaidTimer(self):
        DEBUG_MSG('startRaidTimer~')
        self.stopRaidTimer()
        self.raidTickTimerId = self.pyAddTimer(1, 1, gametimer.RAID_TICK)
        self._clearRaidJoinRecords()

    def stopRaidTimer(self):
        if self.raidTickTimerId:
            DEBUG_MSG('stopRaidTimer::~')
            self.pyDelTimer(self.raidTickTimerId, gametimer.RAID_TICK)
            self.raidTickTimerId = 0

    def _autoCtrlRaidTimer(self, crtRaidUUID, newRaidUUID):
        if newRaidUUID and not self.raidTickTimerId:
            # 有新的raidUUID, 且没有timerID, 需要开始timerTick
            self.startRaidTimer()
        elif not crtRaidUUID and newRaidUUID:
            # 有新的raidUUID, 且没有旧的raidUUID, 加入一个团队, 开始timerTick
            self.startRaidTimer()
        elif crtRaidUUID and not newRaidUUID:
            # 离开一个团队, 停止timerTick
            self.stopRaidTimer()

    def _getAvatarPropsForRaid(self):
        return raid.RaidTeamMemberVal(
            playerGbId=self.gbId, playerBox=self.base, playerName=self.name,
            level=self.level, school=self.school, sex=self.sex, picFrameId=self.appearance.outfitData.picFrameId,
            bFollow=False, bOnline=True, spaceNo=self.spaceNo, position=self.position,
            hp=self.hp, fullHp=self.fullHp, score=self.getTotalScore(), openId="openId")

    @gamedecorator.crossServer
    @utils.isMyself
    @raidPermissionCheck(needPermission=gameconst.RaidPermission.MEMBER)
    def getRaidAllMembersAttrs(self, exposed, memberList):
        # INFO_MSG('getRaidAllMembersAttrs~')

        def _check():
            if not self.isInRaid():
                return None, gameconst.RaidErrno.RAID_NOT_IN_RAID
            return None, gameconst.RaidErrno.RAID_OK

        _, err = _check()
        if err != gameconst.RaidErrno.RAID_OK:
            ERROR_MSG('getRaidAllMembersAttrs:: check failed, {}'.format(err))
            return

        raidUUID = self.raidUUID
        extraProps = {}
        gameengine.getRaidStub(raidUUID).getRaidAllMembersAttrs(
            self.base, self.gbId, raidUUID, memberList, extraProps)

    @utils.isMyself
    @raidPermissionCheck(needPermission=gameconst.RaidPermission.DEPUTY)
    def getRaidApplyJoinDic(self, exposed):
        INFO_MSG('getRaidApplyJoinDic::~')

        def _check():
            if not self.isInRaid():
                return None, gameconst.RaidErrno.RAID_NOT_IN_RAID
            if not self.isRaidLeader() and not self.isRaidDeputy():
                return None, gameconst.RaidErrno.RAID_NOT_RAID_LEADER_OR_DEPUTY
            return None, gameconst.RaidErrno.RAID_OK

        _, err = _check()
        if err != gameconst.RaidErrno.RAID_OK:
            ERROR_MSG('getRaidApplyJoinRaidDic:: failed, {}'.format(err))
            return

        raidUUID = self.raidUUID
        gameengine.getRaidStub(raidUUID).getRaidApplyJoinDic(self.base, self.gbId, raidUUID)

    @utils.isMyself
    @raidPermissionCheck(needPermission=gameconst.RaidPermission.DEPUTY)
    def clearRaidApplyJoinDic(self, exposed):
        INFO_MSG('clearRaidApplyJoinDic::~')
        _, err = self._clearRaidApplyJoinDicCheck()
        if err != gameconst.RaidErrno.RAID_OK:
            ERROR_MSG('clearRaidApplyJoinDic::, check failed, {}'.format(err))
            return
        raidUUID = self.raidUUID
        gameengine.getRaidStub(self.raidUUID).clearRaidApplyJoinDic(self.base, self.gbId, raidUUID)

    def _clearRaidApplyJoinDicCheck(self):
        if not self.isInRaid():
            return None, gameconst.RaidErrno.RAID_NOT_IN_RAID
        if not self.isRaidLeader() and not self.isRaidDeputy():
            return None, gameconst.RaidErrno.RAID_NOT_RAID_LEADER_OR_DEPUTY
        return None, gameconst.RaidErrno.RAID_OK

    def onJoinListPlayerClearRaidApplyJoinDic(self, raidUUID, joinType, teamUUID):
        INFO_MSG('onJoinListPlayerClearRaidApplyJoinDic::', raidUUID, joinType, teamUUID)
        raidJoinRecord = self.raidJoinRecord
        if raidUUID not in raidJoinRecord:
            WARNING_MSG('onJoinListPlayerClearRaidApplyJoinDic:: raid cache missing', raidUUID)
            return

        cacheJoinType = raidJoinRecord[raidUUID]
        if cacheJoinType != joinType:
            WARNING_MSG('onJoinListPlayerClearRaidApplyJoinDic:: cache joinType not match', raidUUID, cacheJoinType, joinType)
            return

        if cacheJoinType == gameconst.RaidJoinType.TEAM and teamUUID != self.teamInfo.teamId:
            WARNING_MSG('onJoinListPlayerClearRaidApplyJoinDic:: teamUUID not match', raidUUID, self.teamInfo.teamId, teamUUID)
            return

        raidJoinRecord.pop(raidUUID)

    def _clearRaidJoinRecords(self, withJoinTypes=()):
        raidStubDic = {}
        for raidId, joinType in self.raidJoinRecord.items():
            if withJoinTypes and joinType not in withJoinTypes:
                continue
            raidStubDic.setdefault(raidId, [])
            raidStubDic[raidId].append((raidId, joinType))

        for raidId, raidIdList in raidStubDic.items():
            raidStub = gameengine.getRaidStub(raidId)
            raidStub.clearRaidJoinRecords(self.base, self.gbId, raidIdList)

    def onClearRaidJoinRecords(self, clearRaidList):
        INFO_MSG('onClearRaidJoinRecords::', clearRaidList)
        raidJoinRecord = self.raidJoinRecord
        for raidUUID, joinType in clearRaidList:
            if joinType == raidJoinRecord.get(raidUUID):
                raidJoinRecord.pop(raidUUID, None)

    @utils.isMyself
    @lockRaid(timeout=3)
    def createRaidWithTeam(self, exposed, capacity):
        """API: 创建一个团队(小队)"""
        INFO_MSG('createRaidWithTeam::~', capacity)
        _, err = self._createRaidWithTeamCheck(capacity)
        if err != gameconst.RaidErrno.RAID_OK:
            if err == gameconst.RaidErrno.RAID_TEAM_MEMBER_OFFLINE:
                WARNING_MSG("createRaidWithTeam:: some player offline")
                gameengine.getTeamStub(self.teamId).onReplyInviteRaidWithTeamFail(
                    self.base, self.gbId, 0, self.gbId, self.teamId, err.errno, {})
            elif err == gameconst.RaidErrno.RAID_UI_DENIED:
                WARNING_MSG("createRaidWithTeam:: player check level failed", self.level)
                self.showMsg(RAID_CONST.datas["raidPartyInivte_underLevel_msg"]["value"], [])
            else:
                ERROR_MSG('createRaidWithTeam:: check failed, {}'.format(err))
            return

        extraProps = {}
        self.createRaidWithTeamCheckRecord = {i: (None, None) for i in self.teamInfo.teamPlayerDic}
        # timeout值要小于limitcall的值
        self.toCallbackAfter(1).clearCreateRaidWithTeamCheckRecord()
        self.checkTeamMembers(gameconst.CheckMemberReason.CHECK_MEMBER_FOR_RAID_DUNGEON_CREATE, False, gameconst.CELL, (capacity, extraProps))
        self._onCheckedMemberCreateRaidWithTeam(self.gbId, gameconst.RaidErrno.RAID_OK, capacity, extraProps)
        return True

    def _createRaidWithTeamCheck(self, capacity):
        errno = gameconst.RaidErrno

        if not self.isInTeam(self.gbId):
            return None, errno.RAID_NOT_IN_TEAM.initkvbody(source='_createRaidWithTeamCheck')

        if not self.isCaptain():
            return None, errno.RAID_NOT_TEAM_CAPTAIN.initkvbody(source='_createRaidWithTeamCheck')

        if self.isInRaid():
            return None, errno.RAID_ALREADY_IN_RAID.initkvbody(source='_createRaidWithTeamCheck')

        if not dataUtils.isRaidCapacityValidate(capacity):
            return None, errno.RAID_UNKNOWN_CAPACITY.initkvbody(source='_createRaidWithTeamCheck')

        if self.teamInfo.offlineMembers():
            return None, errno.RAID_TEAM_MEMBER_OFFLINE.initkvbody(source='_createRaidWithTeamCheck')

        if not self.isUIVisible(dataUtils.getRaidConstDataValue("raidUIVisibleId")):
            return None, errno.RAID_UI_DENIED.initkvbody(source='_createRaidWithTeamCheck', level=self.level)

        return None, errno.RAID_OK
 
    def _checkCreateRaidWithTeamMemberConditions(self, capacity, extra):
        """小队转化为团队: 小队成员检查条件"""
        INFO_MSG('_checkCreateRaidWithTeamMemberConditions::', capacity, extra)

        def _check():
            if self.isInRaid():
                return None, gameconst.RaidErrno.RAID_ALREADY_IN_RAID.initkvbody(
                    source='_checkCreateRaidWithTeamMemberConditions')
            if not self.isUIVisible(dataUtils.getRaidConstDataValue("raidUIVisibleId")):
                return None, gameconst.RaidErrno.RAID_UI_DENIED.initkvbody(
                    source='_checkCreateRaidWithTeamMemberConditions', level=self.level)
            return None, gameconst.RaidErrno.RAID_OK

        _, err = _check()
        if err != gameconst.RaidErrno.RAID_OK:
            WARNING_MSG('_createRaidWithTeamCheck:: member check failed, {}'.format(err))
            return True, (err, capacity, extra), ()

        return False, (err, capacity, extra), ()

    def _onCheckedMemberCreateRaidWithTeam(self, memberGBID, err, capacity, extra):
        INFO_MSG('_onCheckedMemberCreateRaidWithTeam::', memberGBID, capacity, extra, err)
        record = self.createRaidWithTeamCheckRecord
        if err != gameconst.RaidErrno.RAID_OK:
            err.initkvbody(memberGBID=memberGBID)
            WARNING_MSG('_onCheckedMemberCreateRaidWithTeam:: member check failed, {}'.format(err))
            record[memberGBID] = (False, err)
        else:
            record[memberGBID] = (True, err)

        checkResult = True
        if self.teamInfo.offlineMembers():
            checkResult = False

        if checkResult:
            for gbId, (result, _err) in record.items():
                if result is None:
                    DEBUG_MSG('_onCheckedMemberCreateRaidWithTeam:: skill checking')
                    return
                elif not result:
                    err = _err
                    checkResult = False
                    break

        # clear if all checked
        self.clearCreateRaidWithTeamCheckRecord()

        if not checkResult:
            WARNING_MSG('_onCheckedMemberCreateRaidWithTeam:: check failed', record)
            if err == gameconst.RaidErrno.RAID_ALREADY_IN_RAID:
                self.showMsg(MMD.datas.raid_teamInvitationCheck_sectionTeam, [])
            elif err == gameconst.RaidErrno.RAID_UI_DENIED:
                self.showMsg(RAID_CONST.datas["raidPartyInivte_underLevel_msg"]["value"], [])
            self._unlockRaidProcess()
            return

        self.doCreateRaidWithTeam(capacity, extra)

    def doCreateRaidWithTeam(self, capacity, extraProps):
        INFO_MSG('doCreateRaidWithTeam::', capacity, extraProps)
        needCreatedRaidUUID = KBEngine.genUUID64()
        gameengine.getTeamStub(self.teamId).createRaidWithTeam(
            self.base, self.gbId, self.teamId, needCreatedRaidUUID, capacity, extraProps)

    @utils.isMyself
    @raidPermissionCheck(needPermission=gameconst.RaidPermission.UNKNOWN, onlyMode=True)
    @lockRaid(timeout=3)
    @gamedecorator.limitcall(3)
    def createRaidLonely(self, exposed, capacity, raidTarget, minLevel, minScore, recruitInfo, password, isAutoExpedition):
        """API: 创建一个团队(单人)"""
        INFO_MSG('createRaidLonely::~', capacity, raidTarget, minLevel, minScore, recruitInfo, password, isAutoExpedition)
        _, err = self._createRaidLonelyCheck(capacity)
        if err != gameconst.RaidErrno.RAID_OK:
            ERROR_MSG('createRaidLonely:: check failed, {}'.format(
                err.initkvbody(source=self._createRaidLonelyCheck.__name__)))
            return

        if raidTarget <=0:
            ERROR_MSG("createRaidLonely, illegal teamTarget", raidTarget)
            return
        
        teamTargetInfo = TMACTD.datas.get(raidTarget)
        if teamTargetInfo is None:
            ERROR_MSG("createRaidLonely, misssing teamTarget", raidTarget)
            return
        
        if raidTarget > 1:
            actData = AC_ADD.datas.get(int(teamTargetInfo['pareActivity']))
            if not actData or gameconst.ActivityControlType.RAID != int(actData['needTeam']):
                ERROR_MSG("createRaidLonely, wrong activity control need team type", raidTarget)
                return

        cfgMinScore = teamTargetInfo['minScore']
        if minScore < cfgMinScore:
            WARNING_MSG("createRaidLonely, invalid minScore", minScore, cfgMinScore)
            minScore = cfgMinScore
        
        cfgMinLevel = teamTargetInfo['minLevel']
        if minLevel < cfgMinLevel:
            WARNING_MSG("createRaidLonely, invalid minLevel", minLevel, cfgMinLevel)
            minLevel = cfgMinLevel
        
        if not self.isCanCreateTeam(raidTarget, minLevel, minScore):
            return

        raidUUID = KBEngine.genUUID64()
        INFO_MSG('createRaidLonely::raidUUID: ', raidUUID)
        leaderProps = self._getAvatarPropsForRaid().toSavedDict()
        gameengine.getRaidStub(raidUUID).createRaidLonely(
            self.base, self.gbId, raidUUID, capacity, [leaderProps, ], {}, raidTarget, minLevel, minScore, recruitInfo, password, isAutoExpedition)
        return True

    def _createRaidLonelyCheck(self, capacity):
        errno = gameconst.RaidErrno
        if not dataUtils.isRaidCapacityValidate(capacity):
            return None, errno.RAID_UNKNOWN_CAPACITY

        if not self.isUIVisible(dataUtils.getRaidConstDataValue("raidUIVisibleId")):
            return None, errno.RAID_UI_DENIED.initkvbody(level=self.level)

        if self.isInRaid():
            return None, errno.RAID_ALREADY_IN_RAID

        if self.isInTeam(self.gbId):
            return None, errno.RAID_ALREADY_IN_TEAM

        return None, errno.RAID_OK

    @utils.isMyself
    @raidPermissionCheck(needPermission=gameconst.RaidPermission.LEADER, onlyMode=True)
    def disbandRaid(self, exposed):
        """API: 解散一个团队"""
        INFO_MSG('disbandRaid::~')
        _, err = self._disbandRaidCheck()
        if err != gameconst.RaidErrno.RAID_OK:
            ERROR_MSG('disbandRaid:: check failed, {}'.format(err))
            return

        extra = {}
        gameengine.getRaidStub(self.raidInfo.raidUUID).disbandRaid(
            self.base, self.gbId, self.raidInfo.raidUUID, extra)

    def _disbandRaidCheck(self):
        if not self.isInRaid():
            return None, gameconst.RaidErrno.RAID_NOT_IN_RAID.initkvbody(source='_disbandRaidCheck')

        if not self.isRaidLeader():
            return None, gameconst.RaidErrno.RAID_NOT_RAID_LEADER.initkvbody(source='_disbandRaidCheck')

        return None, gameconst.RaidErrno.RAID_OK

    @utils.isMyself
    def applyJoinRaidLonely(self, exposed, raidUUID):
        """API: 申请加入一个团队"""
        INFO_MSG('applyJoinRaidLonely::', raidUUID)
        _, err = self._applyJoinRaidLonelyCheck(raidUUID)
        if err != gameconst.RaidErrno.RAID_OK:
            err = err.initkvbody(source=self._applyJoinRaidLonelyCheck.__name__)
            WARNING_MSG('applyJoinRaidLonely:: check failed, {}'.format(err))
            if err == gameconst.RaidErrno.RAID_ALREADY_APPLY_JOIN:
                self.showMsg(RAID_CONST.datas["raid_applySent_msg"]["value"], [])
            return

        joinProps, extraProps = self._getAvatarPropsForRaid().toSavedDict(), {}
        gameengine.getRaidStub(raidUUID).applyJoinRaidLonely(self.base, self.gbId, joinProps, raidUUID, extraProps)

    def _applyJoinRaidLonelyCheck(self, raidUUID):
        _errno = gameconst.RaidErrno
        if not self.isUIVisible(dataUtils.getRaidConstDataValue("raidUIVisibleId")):
            return None, _errno.RAID_UI_DENIED.initkvbody(level=self.level)

        if not raidUUID:
            return None, _errno.RAID_PARAM_ERR.initkvbody(raidUUID=raidUUID)

        if self.isInRaid():
            return None, _errno.RAID_ALREADY_IN_RAID.initkvbody(raidUUID=raidUUID)

        if raidUUID in self.raidJoinRecord and self.raidJoinRecord[raidUUID] == gameconst.RaidJoinType.SINGLE:
            return None, _errno.RAID_ALREADY_APPLY_JOIN.initkvbody(raidUUID=raidUUID)

        return None, _errno.RAID_OK

    def onLeaderProcessApplyJoinRaidLonely(self, joinedPlayerBox, joinedPlayerGBID,
                                           joinedPlayerProps, raidUUID, extraProps):
        """成功申请团队后, 团长获得回调"""
        INFO_MSG('onLeaderProcessApplyJoinRaidLonely::', joinedPlayerBox,
                 joinedPlayerGBID, raidUUID, joinedPlayerProps, extraProps)
        self.client and self.client.beNotifiedApplyJoinRaid(raidUUID, joinedPlayerGBID, joinedPlayerProps)

    def onApplyJoinRaidLonelySucc(self, playerGBID, raidUUID, extraProps):
        """成功申请团队后, 申请者获得回调"""
        INFO_MSG('onApplyJoinRaidLonelySucc::', playerGBID, raidUUID, extraProps)
        self.raidJoinRecord[raidUUID] = gameconst.RaidJoinType.SINGLE
        self.showMsg(RAID_CONST.datas["raid_applySent_msg"]["value"], [])

    @utils.isMyself
    def applyJoinRaidWithTeam(self, exposed, raidUUID):
        """API: 申请加入一个团队(小队加入)"""
        INFO_MSG('applyJoinRaidWithTeam::', raidUUID)
        _, err = self._applyJoinRaidWithTeamCheck(raidUUID)
        if err != gameconst.RaidErrno.RAID_OK:
            WARNING_MSG('applyJoinRaidWithTeam:: check failed, {}'.format(
                err.initkvbody(source=self._applyJoinRaidWithTeamCheck.__name__)))
            if err == gameconst.RaidErrno.RAID_ALREADY_APPLY_JOIN:
                self.showMsg(RAID_CONST.datas["raid_applySent_msg"]["value"], [])
            return

        extraProps = {}
        gameengine.getTeamStub(self.teamId).applyJoinRaidWithTeam(
            self.base, self.gbId, self.teamId, raidUUID, extraProps)

    def _applyJoinRaidWithTeamCheck(self, raidUUID):
        _errno = gameconst.RaidErrno
        if not self.isUIVisible(dataUtils.getRaidConstDataValue("raidUIVisibleId")):
            return None, _errno.RAID_UI_DENIED.initkvbody(level=self.level)

        if not raidUUID:
            return None, _errno.RAID_PARAM_ERR.initkvbody(raidUUID=raidUUID)

        if self.isInRaid():
            return None, _errno.RAID_ALREADY_IN_RAID.initkvbody(raidUUID=raidUUID)

        if raidUUID in self.raidJoinRecord and self.raidJoinRecord[raidUUID] == gameconst.RaidJoinType.TEAM:
            return None, _errno.RAID_ALREADY_APPLY_JOIN.initkvbody(raidUUID=raidUUID)

        if not self.isInTeam(self.gbId):
            return None, _errno.RAID_NOT_IN_TEAM.initkvbody(raidUUID=raidUUID)

        if not self.isCaptain():
            return None, _errno.RAID_NOT_TEAM_CAPTAIN.initkvbody(raidUUID=raidUUID)

        return None, _errno.RAID_OK

    def onLeaderProcessApplyJoinRaidWithTeam(self, joinedCaptainBox, joinedCaptainGBID, joinedPlayersProps,
                                             teamUUID, raidUUID, extraProps):
        """组队成功申请团队后, 团长获得回调"""
        INFO_MSG('onLeaderProcessApplyJoinRaidWithTeam::',
                 joinedCaptainBox, joinedCaptainGBID, joinedPlayersProps, teamUUID, raidUUID, extraProps)
        self.client and self.client.beNotifiedApplyJoinRaid(raidUUID, joinedCaptainGBID, joinedPlayersProps)

    def onApplyJoinRaidWithTeamSucc(self, joinedCaptainGBID, teamUUID, raidUUID, extraProps):
        """组队成功申请团队后, 申请者获得回调"""
        INFO_MSG('onApplyJoinRaidWithTeamSucc::', joinedCaptainGBID, teamUUID, raidUUID, extraProps)
        self.raidJoinRecord[raidUUID] = gameconst.RaidJoinType.TEAM
        self.showMsg(RAID_CONST.datas["raid_applySent_msg"]["value"], [])
 
    @utils.isMyself
    @raidPermissionCheck(needPermission=gameconst.RaidPermission.DEPUTY)
    def replyJoinRaid(self, exposed, playerGBID, beAgreed):
        """API: 确认某个申请的玩家/小队加入团队"""
        INFO_MSG('replyJoinRaid::', playerGBID, beAgreed)
        _, err = self._replyJoinRaidCheck(playerGBID)
        if err != gameconst.RaidErrno.RAID_OK:
            err = err.initkvbody(source=self._replyJoinRaidCheck.__name__)
            WARNING_MSG('replyJoinRaid:: check failed, {}'.format(err))
            return

        raidUUID = self.raidUUID
        extraProps = {}
        gameengine.getRaidStub(raidUUID).replyJoinRaid(
            self.base, self.gbId, playerGBID, raidUUID, beAgreed, extraProps)

    def _replyJoinRaidCheck(self, playerGBID):
        if not playerGBID:
            return None, gameconst.RaidErrno.RAID_PARAM_ERR.initkvbody(playerGBID=playerGBID)

        if playerGBID == self.gbId:
            return None, gameconst.RaidErrno.UNKNOWN.initkvbody(reason='self-replied')

        if not self.isInRaid():
            return None, gameconst.RaidErrno.RAID_NOT_IN_RAID

        if not self.isRaidLeader() and not self.isRaidDeputy():
            return None, gameconst.RaidErrno.RAID_NOT_RAID_LEADER_OR_DEPUTY
                
        return None, gameconst.RaidErrno.RAID_OK

    @lockRaid(timeout=1)
    def onJoinPlayerReplyJoinRaidLonely(self, srcPlayerGBID, raidUUID, playerGBID, playerJoinProps, extraProps):
        """玩家申请(单人请求)通过后接受回调"""
        INFO_MSG('onJoinPlayerReplyJoinRaidLonely::', srcPlayerGBID, raidUUID, playerGBID, playerJoinProps, extraProps)
        _, err = self._onJoinPlayerReplyJoinRaidLonelyCheck(raidUUID)
        if err != gameconst.RaidErrno.RAID_OK:
            err = err.initkvbody(source=self._applyJoinRaidLonelyCheck.__name__)
            ERROR_MSG('onJoinPlayerReplyJoinRaidLonely::, check failed, {}'.format(err))
        else:
            playerProps = self._getAvatarPropsForRaid().toSavedDict()
            gameengine.getRaidStub(raidUUID).onReplyJoinRaidLonely(
                srcPlayerGBID, raidUUID, playerGBID, playerProps, extraProps)

        self.raidJoinRecord.pop(raidUUID)

        if err == gameconst.RaidErrno.RAID_OK:
            self.cancelAllTeamAndRaidJoinRequest()
            return True
        return False

    def _onJoinPlayerReplyJoinRaidLonelyCheck(self, raidUUID):
        _errno = gameconst.RaidErrno
        if self.isInRaid():
            return None, _errno.RAID_ALREADY_IN_RAID.initkvbody(raidUUID=raidUUID)
        # if raidUUID not in self.raidJoinRecord:
        #     return None, _errno.RAID_APPLY_JOIN_RECORD_NOT_FOUND.initkvbody(raidUUID=raidUUID)
        return None, _errno.RAID_OK

    def onJoinPlayerHandleReplyJoinRaidReject(self, raidUUID):
        """玩家申请被拒绝后接受回调"""
        INFO_MSG('onJoinPlayerHandleReplyJoinRaidReject::', raidUUID)
        self.raidJoinRecord.pop(raidUUID, None)

    def onJoinPlayerHandleReplyJoinRaidAccept(self, raidUUID):
        """玩家申请同意后接受回调,"""
        INFO_MSG('onJoinPlayerHandleReplyJoinRaidAccept::', raidUUID)
        self.raidJoinRecord.pop(raidUUID, None)
        if self.isCaptain():
            self.cancelAllTeamAndRaidJoinRequest()

    @lockRaid(timeout=1)
    def onJoinPlayerReplyJoinRaidWithTeam(self, srcPlayerGBID, raidUUID, playerJoinProps, extraProps):
        """玩家申请(组队请求)通过后(所有小队)玩家接受回调"""
        INFO_MSG('onJoinPlayerReplyJoinRaidWithTeam', srcPlayerGBID, raidUUID, playerJoinProps, extraProps)
        _, err = self._onJoinPlayerReplyJoinRaidWithTeam(raidUUID, playerJoinProps['joinTeamUUID'])
        if err != gameconst.RaidErrno.RAID_OK:
            err = err.initkvbody(source=self._onJoinPlayerReplyJoinRaidWithTeam.__name__)
            WARNING_MSG('onJoinPlayerReplyJoinRaidWithTeam:: failed, {}'.format(err))
            # when playerProps `bool(playerProps) is False`, stub check will be quickly failed before timeout
            playerProps = {}
        else:
            playerProps = self._getAvatarPropsForRaid().toSavedDict()
        extraProps.update({'memberCheckErrno': err})
        gameengine.getRaidStub(raidUUID).onReplyJoinRaidWithTeam(
            srcPlayerGBID, raidUUID, playerJoinProps['joinTeamUUID'], self.gbId, playerProps, extraProps)

        return False if err != gameconst.RaidErrno.RAID_OK else True

    def _onJoinPlayerReplyJoinRaidWithTeam(self, raidUUID, teamUUID):
        _errno = gameconst.RaidErrno
        if self.isInRaid():
            # 如果已经在团队中, 如果是小队队长, 则无法加入, 如果是普通成员, 则只要在当前团队中, 小队仍然可以加入
            if self.raidInfo.raidUUID != raidUUID or self.isCaptain():
                return None, _errno.RAID_ALREADY_IN_RAID.initkvbody(raidUUID=raidUUID)
        if self.teamInfo.teamId != teamUUID:
            return None, _errno.RAID_TEAM_NOT_FOUND.initkvbody(raidUUID=raidUUID)
        # if self.isCaptain() and raidUUID not in self.raidJoinRecord:
        #     return None, _errno.RAID_APPLY_JOIN_RECORD_NOT_FOUND.initkvbody(raidUUID=raidUUID)
        return None, _errno.RAID_OK

    def _cancelAllRaidJoinRequest(self):
        extraProps = {}
        for raidUUID, raidJoinType in self.raidJoinRecord.items():
            gameengine.getRaidStub(raidUUID).cancelRaidJoinRequest(
                self.base, self.gbId, raidUUID, raidJoinType, extraProps)

    def onCancelRaidJoinRequestSucc(self, raidUUID, raidJoinType, extra):
        INFO_MSG("onCancelRaidJoinRequestSucc::", raidUUID, raidJoinType, extra)
        self.raidJoinRecord.pop(raidUUID, None)

    @utils.isMyself
    @raidPermissionCheck(needPermission=gameconst.RaidPermission.UNKNOWN)
    def tryApplyInviteRaid(self, exposed, playerGBID, playerName):
        """API: 尝试邀请玩家加入团队, 用于AOI外情况无法获取玩家组队信息"""
        INFO_MSG('tryApplyInviteRaid::~', playerGBID, playerName)
        _, err = self._tryApplyInviteRaidLonelyCommonCheck(playerGBID)
        if err != gameconst.RaidErrno.RAID_OK:
            WARNING_MSG('tryApplyInviteRaid:: common check failed, {}'.format(err))
            return

        gameengine.getGlobalBase('PlayerStub').doOnOthersCell(
            (playerGBID, ), 'tryBeInvitedInRaid', (self.base, ),
            self, "tryApplyInviteRaidOffline", (playerName, ))

    def _tryApplyInviteRaidLonelyCommonCheck(self, playerGBID):
        if not playerGBID:
            return None, gameconst.RaidErrno.RAID_PARAM_ERR.initkvbody(playerGBID=playerGBID)
        if playerGBID == self.gbId:
            return None, gameconst.RaidErrno.UNKNOWN.initkvbody(reason='self-invite')
        if self.isInTeam():
            return None, gameconst.RaidErrno.RAID_ALREADY_IN_TEAM
        return None, gameconst.RaidErrno.RAID_OK
    
    def tryBeInvitedInRaid(self, invitedPlayerBox):
        DEBUG_MSG("tryBeInvitedInRaid::")
        _, err = self._tryBeInvitedInRaidCheck()
        if err != gameconst.RaidErrno.RAID_OK:
            WARNING_MSG("tryBeInvitedInRaid:: failed, {}".format(err))
            if err == gameconst.RaidErrno.RAID_ALREADY_IN_RAID:
                invitedPlayerBox.onMessagePre(RAID_CONST.datas["raidInviteFail_alreadyInRaid_msg"]["value"], [])
            return
        invitedPlayerBox.client.onTryBeInvitedInRaid(self.gbId, self.teamId, self.name,
                                                     self.isCaptain())

    def _tryBeInvitedInRaidCheck(self):
        if not self.isUIVisible(dataUtils.getRaidConstDataValue("raidUIVisibleId")):
            return None, gameconst.RaidErrno.RAID_UI_DENIED.initkvbody(level=self.level)
        if self.isInRaid():
            return None, gameconst.RaidErrno.RAID_ALREADY_IN_RAID
        return None, gameconst.RaidErrno.RAID_OK

    def tryApplyInviteRaidOffline(self, playerGBID, playerName):
        WARNING_MSG("tryApplyInviteRaidOffline::", playerGBID, playerName)
        self.showMsg(MMD.datas.raid_applicantOffline, [playerName])

    @utils.isMyself
    @raidPermissionCheck(needPermission=gameconst.RaidPermission.UNKNOWN)
    def applyInviteRaidLonely(self, exposed, playerGBID, playerName):
        """API: 邀请单人加入团队"""
        INFO_MSG('applyInviteRaidLonely::~', playerGBID, playerName)

        err = self.applyInviteRaidLonelyWithLonely(playerGBID, playerName)
        if err == gameconst.RaidErrno.RAID_OK:
            return
        else:
            WARNING_MSG('applyInviteRaidLonelyWithLonely:: common check failed, {}'.format(err))
            
        _, err = self._applyInviteRaidLonelyCommonCheck(playerGBID)
        if err != gameconst.RaidErrno.RAID_OK:
            WARNING_MSG('applyInviteRaidLonely:: common check failed, {}'.format(err))
            return

        if self.isRaidLeader():
            self.raidLeaderApplyInvitedRaidLonely(playerGBID, playerName)
        elif self.isRaidDeputy():
            self.raidDeputyApplyInvitedRaidLonely(playerGBID, playerName)
        else:
            self.raidTeamMemberApplyInviteRaidLonely(playerGBID, playerName)
        '''
        #
        elif self.isRaidCaptain():
            self.raidTeamCaptainApplyInviteRaidLonely(playerGBID, playerName)
        '''

    def applyInviteRaidLonelyWithLonely(self, playerGBID, playerName):
        if not self.isUIVisible(dataUtils.getRaidConstDataValue("raidUIVisibleId")):
            return gameconst.RaidErrno.RAID_UI_DENIED.initkvbody(level=self.level)
        if self.isInRaid():
            return gameconst.RaidErrno.RAID_ALREADY_IN_RAID
        if self.isInTeam():
            return gameconst.RaidErrno.RAID_ALREADY_IN_TEAM
        if not playerGBID or playerGBID == self.gbId:
            return gameconst.RaidErrno.UNKNOWN

        extraProps = {'inviteSource': gameconst.RaidPermission.LEADER}
        gameengine.getGlobalBase('PlayerStub').doOnOthersCell((playerGBID,), 'invitedPlayerOnApplyInvitedRaid', (
                0, self.gbId, self.name, self.name, extraProps), self, 'tryApplyInviteRaidOffline', (playerName, ))
        return gameconst.RaidErrno.RAID_OK

    def _applyInviteRaidLonelyCommonCheck(self, playerGBID):
        if not playerGBID:
            return None, gameconst.RaidErrno.RAID_PARAM_ERR.initkvbody(playerGBID=playerGBID)
        if playerGBID == self.gbId:
            return None, gameconst.RaidErrno.UNKNOWN.initkvbody(reason='self-invite')
        if not self.isInRaid():
            return None, gameconst.RaidErrno.RAID_NOT_IN_RAID
        return None, gameconst.RaidErrno.RAID_OK

    def raidLeaderApplyInvitedRaidLonely(self, playerGBID, playerName):
        """团长邀请单人加入团队"""
        INFO_MSG('raidLeaderApplyInvitedRaidLonely::', playerGBID, playerName)
        raidUUID = self.raidUUID
        extraProps = {'inviteSource': gameconst.RaidPermission.LEADER}
        gameengine.getRaidStub(raidUUID).raidLeaderApplyInvitedRaid(
            self.base, self.gbId, raidUUID, playerGBID, playerName, extraProps)

    def raidDeputyApplyInvitedRaidLonely(self, playerGBID, playerName):
        """副团长邀请单人加入团队"""
        INFO_MSG('raidDeputyApplyInvitedRaidLonely::', playerGBID, playerName)
        raidUUID = self.raidUUID
        extraProps = {'inviteSource': gameconst.RaidPermission.DEPUTY}
        gameengine.getRaidStub(raidUUID).raidDeputyApplyInvitedRaid(
            self.base, self.gbId, raidUUID, playerGBID, playerName, extraProps)
    #
    def raidTeamCaptainApplyInviteRaidLonely(self, playerGBID, playerName):
        """队长邀请单人加入团队"""
        INFO_MSG('raidTeamCaptainApplyInviteRaidLonely::', playerGBID, playerName)
        raidUUID = self.raidUUID
        raidTeamIDX = self.raidInfo.raidTeamIDX
        extraProps = {'raidTeamIDX': raidTeamIDX,
                      'inviteSource': gameconst.RaidPermission.CAPTAIN}
        gameengine.getRaidStub(raidUUID).raidCaptainApplyInvitedRaid(
            self.base, self.gbId, raidUUID, raidTeamIDX, playerGBID, playerName, extraProps)

    def raidTeamMemberApplyInviteRaidLonely(self, playerGBID, playerName):
        """团队成员提议邀请单人加入团队"""
        INFO_MSG('raidTeamMemberApplyInviteRaidLonely::', playerGBID, playerName)
        raidUUID = self.raidUUID
        extraProps = {'inviteSource': gameconst.RaidPermission.MEMBER}
        gameengine.getRaidStub(raidUUID).raidMemberApplyInvitedRaid(
            self.base, self.gbId, raidUUID, playerGBID, playerName, extraProps)

    def invitedPlayerOnApplyInvitedRaid(self, raidUUID, srcPlayerGBID,
                                        srcPlayerName, leaderName, extraProps):
        """邀请单人/组队加入团队流程成功后回调"""
        INFO_MSG('invitedPlayerOnApplyInvitedRaid::',
                 raidUUID, srcPlayerGBID, extraProps, srcPlayerName, leaderName)
        raidTeamIDX = extraProps.get('raidTeamIDX', 0)
        teamUUID = extraProps.get('teamUUID', 0)
        inviteSource = extraProps.get('inviteSource', gameconst.RaidPermission.UNKNOWN)
        recordId, err = self._invitedPlayerOnApplyInvitedRaid(raidUUID, teamUUID, srcPlayerGBID,
                                                              srcPlayerName, leaderName, raidTeamIDX,
                                                              inviteSource)
        if err != gameconst.RaidErrno.RAID_OK:
            err = err.initkvbody(raidUUID=raidUUID, srcPlayerGBID=srcPlayerGBID)
            if err == gameconst.RaidErrno.RAID_NOT_TEAM_CAPTAIN:
                WARNING_MSG('invitedPlayerOnApplyInvitedRaid:: not team captain, errno={}'.format(err))
                gameengine.getGlobalBase('PlayerStub').doOnOthersBase(
                    [srcPlayerGBID, ], 'onMessagePre',
                    (RAID_CONST.datas["raidInviteFail_alreadyInRaid_msg"]["value"], []),
                    None, '', ())

            elif err == gameconst.RaidErrno.RAID_ALREADY_IN_RAID:
                WARNING_MSG('invitedPlayerOnApplyInvitedRaid:: player already in raid, errno={}'.format(err))
                gameengine.getGlobalBase('PlayerStub').doOnOthersBase(
                    [srcPlayerGBID, ], 'onMessagePre',
                    (RAID_CONST.datas["raidInviteFail_alreadyInRaid_msg"]["value"], []),
                    None, '', ())

            elif err == gameconst.RaidErrno.RAID_INVITED_SAME_PLAYER_INCD:
                WARNING_MSG('invitedPlayerOnApplyInvitedRaid:: player which be invited in CD, errno={}'.format(err))
                gameengine.getGlobalBase('PlayerStub').doOnOthersBase(
                    [srcPlayerGBID, ], 'onMessagePre',
                    (RAID_CONST.datas["raid_inviteFail_cooldown_msg"]["value"], []),
                    None, '', ())
            elif err == gameconst.RaidErrno.RAID_UI_DENIED:
                WARNING_MSG('invitedPlayerOnApplyInvitedRaid:: player level too low, errno={}'.format(err))
                gameengine.getGlobalBase('PlayerStub').doOnOthersBase(
                    [srcPlayerGBID, ], 'onMessagePre',
                    (RAID_CONST.datas["raid_inviteFail_cooldown_msg"]["value"], []),
                    None, '', ())
            else:
                ERROR_MSG('invitedPlayerOnApplyInvitedRaid:: failed, {}'.format(err))

            return

        # 【【任务】发送团队邀请后弹出tip反馈】
        gameengine.getGlobalBase('PlayerStub').doOnOthersBase(
            [srcPlayerGBID, ], 'onMessagePre',
            (RAID_CONST.datas["raid_inviteSuccess_msg"]["value"], []), None, '', ())

        # self.base.makeTargetSecSNSGetFlowLog(srcPlayerGBID, None, gametlog.SecSNSGetMode.inviteRaid, "")

        INFO_MSG('invitedPlayerOnApplyInvitedRaid:: set record', raidUUID, recordId)

    def _invitedPlayerOnApplyInvitedRaid(self, raidUUID, teamUUID, srcPlayerGBID,
                                         srcPlayerName, leaderName, raidTeamIDX, inviteSource):
        # 判断玩家等级是否够
        if not self.isUIVisible(dataUtils.getRaidConstDataValue("raidUIVisibleId")):
            return None, gameconst.RaidErrno.RAID_UI_DENIED.initkvbody(level=self.level)

        if self.isInRaid():
            return None, gameconst.RaidErrno.RAID_ALREADY_IN_RAID

        if teamUUID:
            # 传入teamID代表邀请的是组队, 回调者应该是小队队长
            if self.teamInfo.teamId != teamUUID:
                return None, gameconst.RaidErrno.RAID_TEAM_ID_CHANGED.initkvbody(srcTeamUUID=teamUUID,
                                                                                 crtTeamUUID=self.teamInfo.teamId)
            if not self.isCaptain():
                return None, gameconst.RaidErrno.RAID_NOT_TEAM_CAPTAIN.initkvbody(teamUUID=teamUUID,
                                                                                  playerGBID=self.gbId)

        now = utils.getNow()
        recordId = KBEngine.genUUID64()
        inviteType = gameconst.RaidJoinType.TEAM if teamUUID else gameconst.RaidJoinType.SINGLE
        raidBeInvitedRecord = self.raidBeInvitedRecord
        thisRaidBeInvitedRecord = raidBeInvitedRecord.setdefault(raidUUID, {})
        for _recordId, _recordVal in thisRaidBeInvitedRecord.items():
            if _recordVal['inviteT'] + RAID_CONST.datas["raidInviteCooldown"]["value"] > now:
                return None, gameconst.RaidErrno.RAID_INVITED_SAME_PLAYER_INCD

        raidBeInvitedRecord[raidUUID][recordId] = {'srcPlayerGBID': srcPlayerGBID,
                                                   'raidTeamIDX': raidTeamIDX,
                                                   'teamUUID': teamUUID,
                                                   'inviteType': inviteType,
                                                   'inviteT': now}

        if inviteSource == gameconst.RaidPermission.LEADER:
            self.client.onBeInvitedRaidByLeader(raidUUID, recordId, teamUUID, srcPlayerGBID, srcPlayerName, leaderName)
        elif inviteSource == gameconst.RaidPermission.DEPUTY:
            self.client.onBeInvitedRaidByDeputy(raidUUID, recordId, teamUUID, srcPlayerGBID, srcPlayerName, leaderName)
        #elif inviteSource == gameconst.RaidPermission.CAPTAIN:
        #    self.client.onBeInvitedRaidByTeamCaptain(raidUUID, recordId, srcPlayerGBID, srcPlayerName, leaderName, raidTeamIDX)
        elif inviteSource == gameconst.RaidPermission.MEMBER:
            self.client.onBeInvitedRaidByMember(raidUUID, recordId, teamUUID, srcPlayerGBID, srcPlayerName, leaderName)
        else:
            WARNING_MSG('_invitedPlayerOnApplyInvitedRaid:: invite source unknown', raidUUID, teamUUID, inviteSource)

        return recordId, gameconst.RaidErrno.RAID_OK

    @utils.isMyself
    @raidPermissionCheck(needPermission=gameconst.RaidPermission.UNKNOWN, onlyMode=True)
    def replyInviteRaidLonely(self, exposed, raidUUID, recordID, srcPlayerGBID, beInvited):
        """API: 某个玩家点击确认接受团队邀请"""
        INFO_MSG('replyInviteRaidLonely::', raidUUID, recordID, srcPlayerGBID, beInvited)
        record, err = self._replyInviteRaidLonelyCheck(raidUUID, recordID, srcPlayerGBID, beInvited)
        if err != gameconst.RaidErrno.RAID_OK:
            if err == gameconst.RaidErrno.RAID_AVATAR_REJECTED_ACT:
                INFO_MSG('replyInviteRaidLonely:: reject, {}'.format(err))
                gameengine.getGlobalBase('PlayerStub').doOnOthersClient(
                    [srcPlayerGBID, ], 'onMessage',
                    (RAID_CONST.datas['raidInvDeniedMsg']['value'], [self.name]),
                    None, '', ())
            else:
                WARNING_MSG('replyInviteRaidLonely:: check failed, {}'.format(err))
            # reply failed, pop current be invited record
            self.raidBeInvitedRecord.get(raidUUID, {}).pop(recordID, None)
            return

        # if reply succeed, pop all raidUUID be invited records
        self.raidBeInvitedRecord.clear()
        playerProps = self._getAvatarPropsForRaid().toSavedDict()
        extraProps = {}
        if raidUUID > 0:
            gameengine.getRaidStub(raidUUID).replyInviteRaidLonely(
                self.base, self.gbId, playerProps, record['srcPlayerGBID'],
                record['raidTeamIDX'], raidUUID, extraProps)
        else:
            gameengine.getGlobalBase('PlayerStub').doOnOthersCell([srcPlayerGBID], 'onReplyInviteRaidLonelyWithLonely', (
                self.base, self.gbId, playerProps, ), None, '', ())

    def _replyInviteRaidLonelyCheck(self, raidUUID, recordID, srcPlayerGBID, beInvited):
        if not beInvited:
            return None, gameconst.RaidErrno.RAID_AVATAR_REJECTED_ACT.initkvbody(raidUUID=raidUUID)

        if not self.isUIVisible(dataUtils.getRaidConstDataValue("raidUIVisibleId")):
            return None, gameconst.RaidErrno.RAID_UI_DENIED.initkvbody(level=self.level)

        #if not raidUUID:
        #    return None, gameconst.RaidErrno.RAID_PARAM_ERR.initkvbody(raidUUID=raidUUID)

        if self.isInRaid():
            return None, gameconst.RaidErrno.RAID_ALREADY_IN_RAID

        recordDic = self.raidBeInvitedRecord.get(raidUUID, {})
        if not recordDic or recordID not in recordDic:
            return None, gameconst.RaidErrno.RAID_APPLY_BE_INVITED_RECORD_NOT_FOUND

        record = recordDic[recordID]
        if record['inviteType'] != gameconst.RaidJoinType.SINGLE:
            return None, gameconst.RaidErrno.RAID_JOIN_TYPE_NOT_MATCH

        if record['srcPlayerGBID'] != srcPlayerGBID:
            return None, gameconst.RaidErrno.RAID_PLAYER_GBID_NOT_MATCH.initkvbody(
                raidUUID=raidUUID,
                srcPlayerGBID=srcPlayerGBID,
                rcdPlayerGBID=record['srcPlayerGBID'])

        return record, gameconst.RaidErrno.RAID_OK

    def onReplyInviteRaidLonelyWithLonely(self, invitedPlayerBox, invitedPlayerGBID, invitedPlayerProps):
        DEBUG_MSG('onReplyInviteRaidLonelyWithLonely::', invitedPlayerProps)

        _, err = self._createRaidLonelyCheck(dataUtils.getRaidConstDataValue('raidMemberLimit'))
        if err != gameconst.RaidErrno.RAID_OK:
            WARNING_MSG('onReplyInviteRaidLonelyWithLonely:: check failed, {}'.format(
                err.initkvbody(source=self._createRaidLonelyCheck.__name__)))
            if err == gameconst.RaidErrno.RAID_ALREADY_IN_RAID:
                gameengine.getRaidStub(self.raidInfo.raidUUID).replyInviteRaidLonely(
                    invitedPlayerBox, invitedPlayerGBID, invitedPlayerProps, self.gbId,
                    0, self.raidInfo.raidUUID, {})
            return
        
        raidUUID = KBEngine.genUUID64()
        leaderProps = self._getAvatarPropsForRaid().toSavedDict()
        gameengine.getRaidStub(raidUUID).createRaid(
            self.base, self.gbId, raidUUID, dataUtils.getRaidConstDataValue('raidMemberLimit'), [leaderProps], {})
        gameengine.getRaidStub(raidUUID).replyInviteRaidLonely(
                invitedPlayerBox, invitedPlayerGBID, invitedPlayerProps, self.gbId,
                0, raidUUID, {})
        
    @utils.isMyself
    @raidPermissionCheck(needPermission=gameconst.RaidPermission.MEMBER, exclude=())
    def applyInviteRaidWithTeam(self, exposed, playerGBID, teamUUID, playerName):
        """API: 邀请小队加入团队"""
        INFO_MSG('applyInviteRaidWithTeam::', playerGBID, teamUUID, playerName)
        _, err = self._applyInviteRaidWithTeamCheck(playerGBID, teamUUID)
        if err != gameconst.RaidErrno.RAID_OK:
            if err == gameconst.RaidErrno.RAID_INVITE_SELF_TEAM:
                self.showMsg(RAID_CONST.datas["raidInviteFail_memberInviteTeam_msg"]["value"], [])
            elif err == gameconst.RaidErrno.RAID_TEAM_MEMBER_DUOHUN:
                self.showMsg(RAID_CONST.datas["beifenglingwufazudui1"]["value"], [])
            WARNING_MSG('applyInviteRaidWithTeam:: check failed, {}'.format(err))
            return

        if self.isRaidLeader():
            self.raidLeaderApplyInviteRaidWithTeam(playerGBID, teamUUID, playerName)
        elif self.isRaidDeputy():
            self.raidDeputyApplyInviteRaidWithTeam(playerGBID, teamUUID, playerName)
        else:
            self.raidTeamMemberApplyInviteRaidWithTeam(playerGBID, teamUUID, playerName)

    def _applyInviteRaidWithTeamCheck(self, playerGBID, teamUUID):
        if not (playerGBID and teamUUID):
            return None, gameconst.RaidErrno.RAID_PARAM_ERR.initkvbody(playerGBID=playerGBID, teamUUID=teamUUID)

        if playerGBID == self.gbId:
            return None, gameconst.RaidErrno.UNKNOWN.initkvbody(reason='self-invite')

        if not teamUUID or teamUUID == self.teamInfo.teamId:
            return None, gameconst.RaidErrno.RAID_INVITE_SELF_TEAM

        if not self.isInRaid():
            return None, gameconst.RaidErrno.RAID_NOT_IN_RAID

        return None, gameconst.RaidErrno.RAID_OK

    def raidLeaderApplyInviteRaidWithTeam(self, playerGBID, teamUUID, playerName):
        """团长邀请队伍加入团队"""
        INFO_MSG('raidLeaderApplyInviteRaidWithTeam::', playerGBID, teamUUID, playerName)
        raidUUID = self.raidUUID
        extraProps = {'teamUUID': teamUUID,
                      'inviteSource': gameconst.RaidPermission.LEADER}
        gameengine.getRaidStub(raidUUID).raidLeaderApplyInvitedRaid(
            self.base, self.gbId, raidUUID, playerGBID, playerName, extraProps)

    def raidDeputyApplyInviteRaidWithTeam(self, playerGBID, teamUUID, playerName):
        """副团长邀请队伍加入团队"""
        INFO_MSG('raidDeputyApplyInviteRaidWithTeam::', playerGBID, teamUUID, playerName)
        raidUUID = self.raidUUID
        extraProps = {'teamUUID': teamUUID,
                      'inviteSource': gameconst.RaidPermission.DEPUTY}
        gameengine.getRaidStub(raidUUID).raidDeputyApplyInvitedRaid(
            self.base, self.gbId, raidUUID, playerGBID, playerName, extraProps)

    def raidTeamMemberApplyInviteRaidWithTeam(self, playerGBID, teamUUID, playerName):
        """团队成员提议邀请队伍加入团队"""
        INFO_MSG('raidTeamMemberApplyInviteRaidWithTeam::', playerGBID, teamUUID, playerName)
        raidUUID = self.raidUUID
        extraProps = {'teamUUID': teamUUID,
                      'inviteSource': gameconst.RaidPermission.MEMBER}
        gameengine.getRaidStub(raidUUID).raidMemberApplyInvitedRaid(
            self.base, self.gbId, raidUUID, playerGBID, playerName, extraProps)

    @utils.isMyself
    @raidPermissionCheck(needPermission=gameconst.RaidPermission.UNKNOWN, onlyMode=True)
    def replyInviteRaidWithTeam(self, exposed, raidUUID, recordID, srcPlayerGBID, beInvited):
        """API: 某个小队(队长)点击确认接受团队邀请"""
        INFO_MSG('replyInviteRaidWithTeam::', raidUUID, recordID, srcPlayerGBID, beInvited)
        record, err = self._replyInviteRaidWithTeamCheck(raidUUID, recordID, srcPlayerGBID, beInvited)
        if err != gameconst.RaidErrno.RAID_OK:
            if err == gameconst.RaidErrno.RAID_AVATAR_REJECTED_ACT:
                INFO_MSG('replyInviteRaidWithTeam:: reject, {}'.format(err))
                gameengine.getGlobalBase('PlayerStub').doOnOthersClient(
                    [srcPlayerGBID, ], 'onMessage',
                    (RAID_CONST.datas['raidInvDeniedMsg']['value'], [self.name]),
                    None, '', ())
            elif err == gameconst.RaidErrno.RAID_TEAM_MEMBER_OFFLINE:
                gameengine.getTeamStub(self.teamId).onReplyInviteRaidWithTeamFail(
                    self.base, self.gbId, 0, srcPlayerGBID, self.teamId, err.errno, {})
            elif err == gameconst.RaidErrno.RAID_ALREADY_IN_RAID:
                gameengine.getGlobalBase('PlayerStub').doOnOthersBase(
                    [srcPlayerGBID, ], 'onMessagePre',
                    (MMD.datas.raid_teamInvitationCheck_sectionTeam, []))

            WARNING_MSG('replyInviteRaidWithTeam:: check failed, {}'.format(err))
            # reply failed, pop current be invited record
            self.raidBeInvitedRecord.get(raidUUID, {}).pop(recordID, None)
            return

        # if reply succeed, pop all raidUUID be invited records
        self.raidBeInvitedRecord.pop(raidUUID)
        teamUUID = record['teamUUID']
        teamMemberNum = len(self.teamInfo.teamPlayerDic)
        playerProps = self._getAvatarPropsForRaid().toSavedDict()
        self._doReplyInviteRaidWithTeam(raidUUID, recordID, teamUUID, playerProps,
                                        teamMemberNum, srcPlayerGBID, isCaptain=True)
        self.teamInfo.allMembersCellDo('tryReplyInviteRaidFollowTeamCaptain',
                                       (raidUUID, recordID, teamUUID, teamMemberNum, srcPlayerGBID))

    def _replyInviteRaidWithTeamCheck(self, raidUUID, recordID, srcPlayerGBID, beInvited):
        if not beInvited:
            return None, gameconst.RaidErrno.RAID_AVATAR_REJECTED_ACT.initkvbody(raidUUID=raidUUID)

        if not raidUUID:
            return None, gameconst.RaidErrno.RAID_PARAM_ERR.initkvbody(raidUUID=raidUUID)

        if self.isInRaid():
            return None, gameconst.RaidErrno.RAID_ALREADY_IN_RAID

        recordDic = self.raidBeInvitedRecord.get(raidUUID, {})
        if not recordDic or recordID not in recordDic:
            return None, gameconst.RaidErrno.RAID_APPLY_BE_INVITED_RECORD_NOT_FOUND

        record = recordDic[recordID]
        if record['teamUUID'] != self.teamInfo.teamId:
            return None, gameconst.RaidErrno.RAID_TEAM_ID_CHANGED.initkvbody(srcTeamUUID=record['teamUUID'],
                                                                             crtTeamUUID=self.teamInfo.teamId)

        if record['inviteType'] != gameconst.RaidJoinType.TEAM:
            return None, gameconst.RaidErrno.RAID_JOIN_TYPE_NOT_MATCH

        if record['srcPlayerGBID'] != srcPlayerGBID:
            return None, gameconst.RaidErrno.RAID_PLAYER_GBID_NOT_MATCH.initkvbody(
                raidUUID=raidUUID,
                srcPlayerGBID=srcPlayerGBID,
                rcdPlayerGBID=record['srcPlayerGBID'])

        if self.teamInfo.offlineMembers():
            return None, gameconst.RaidErrno.RAID_TEAM_MEMBER_OFFLINE

        return record, gameconst.RaidErrno.RAID_OK

    def _doReplyInviteRaidWithTeam(self, raidUUID, recordID, teamUUID, playerProps,
                                   teamMemberNum, srcPlayerGBID, isCaptain=False, extraProps=None):
        INFO_MSG('doReplyInviteRaidWithTeam::', raidUUID, recordID, teamUUID,
                 teamMemberNum, isCaptain, playerProps)
        if extraProps is None:
            extraProps = {}
        gameengine.getRaidStub(raidUUID).replyInviteRaidWithTeam(
            self.base, self.gbId, raidUUID, recordID, teamUUID, teamMemberNum,
            playerProps, isCaptain, srcPlayerGBID, extraProps)

    def tryReplyInviteRaidFollowTeamCaptain(self, raidUUID, recordID, teamUUID, teamMemberNum, srcPlayerGBID):
        """队长确认后需要所有小队队员再次检查一次条件后在RaidStub处汇总"""
        INFO_MSG('tryReplyInviteRaidFollowTeamCaptain', raidUUID, recordID, teamUUID, teamMemberNum)
        _, err = self._tryReplyInviteRaidFollowTeamCaptain(raidUUID, teamUUID)
        if err != gameconst.RaidErrno.RAID_OK:
            WARNING_MSG('tryReplyInviteRaidFollowTeamCaptain:: failed && to be ignored, {}'.format(err))
            playerProps = {}
            if err == gameconst.RaidErrno.RAID_ALREADY_IN_RAID:
                gameengine.getGlobalBase('PlayerStub').doOnOthersBase(
                    [srcPlayerGBID, ], 'onMessagePre',
                    (MMD.datas.raid_teamInvitationCheck_sectionTeam, []),
                    None, "", ())

            if err == gameconst.RaidErrno.RAID_ALREADY_BE_TEAM_CAPTAIN:
                return

        else:
            playerProps = self._getAvatarPropsForRaid().toSavedDict()
        # always callback to raidStub
        self._doReplyInviteRaidWithTeam(raidUUID, recordID, teamUUID, playerProps,
                                        teamMemberNum, srcPlayerGBID, isCaptain=False)

    def _tryReplyInviteRaidFollowTeamCaptain(self, raidUUID, teamUUID):
        if self.isInRaid():
            # 如果已经在团队中, 如果是小队队长, 则无法加入, 如果是普通成员, 则只要在当前团队中, 小队仍然可以加入
            if self.raidInfo.raidUUID != raidUUID:
                return None, gameconst.RaidErrno.RAID_ALREADY_IN_RAID.initkvbody(raidUUID=raidUUID)
            if self.isCaptain():
                return None, gameconst.RaidErrno.RAID_ALREADY_BE_TEAM_CAPTAIN
        if self.teamInfo.teamId != teamUUID:
            return None, gameconst.RaidErrno.RAID_TEAM_ID_CHANGED
        return None, gameconst.RaidErrno.RAID_OK

    @utils.isMyself
    @raidPermissionCheck(needPermission=gameconst.RaidPermission.MEMBER)
    def leaveRaid(self, exposed):
        """API: 任意成员离开团队"""
        INFO_MSG('leaveRaid::~')
        _, err = self._leaveRaidCheck()
        if err != gameconst.RaidErrno.RAID_OK:
            ERROR_MSG('leaveRaid:: check failed, {}'.format(err))
            return

        raidUUID = self.raidUUID
        extraProps = {}
        gameengine.getRaidStub(raidUUID).leaveRaid(self.base, self.gbId, raidUUID, extraProps)

    def _leaveRaidCheck(self):
        if not self.isInRaid():
            return None, gameconst.RaidErrno.RAID_NOT_IN_RAID
        return None, gameconst.RaidErrno.RAID_OK

    def onLeaveRaid(self, raidUUID, extraProps):
        INFO_MSG('onLeaveRaid::', raidUUID, extraProps)
        if raidUUID != self.raidUUID:
            WARNING_MSG('onLeaveRaid:: raidUUID not match, skip clear cache', raidUUID, self.raidUUID)
            return
        self._onLeaveRaid()

    def _onLeaveRaid(self):
        # reset raidInfo && refresh self to clear
        self.raidInfo.reset()
        self.onRefreshPlayerRaidCacheVal(self.raidInfo)

        # 【【任务】在团本中退出团队，会被传送出去，同小队】
        # 需求: 团队副本中A玩家离开团队, 将该玩家踢出副本
        if self.isInRaidDungeon():
            INFO_MSG('_onLeaveRaid:: player leave dungeon {}'.format(self.spaceNo))
            self.selfLeaveRaidDungeon(dungeonSrc.BasicDungeonSrc())

    @utils.isMyself
    @raidPermissionCheck(needPermission=gameconst.RaidPermission.DEPUTY)
    def kickOutRaidMember(self, exposed, raidTeamIDX, playerGBID):
        """API: 团长/队长踢出玩家"""
        INFO_MSG('kickOutRaidMember::', raidTeamIDX, playerGBID)

        def _commonCheck():
            if not (raidTeamIDX and playerGBID):
                return None, gameconst.RaidErrno.RAID_PARAM_ERR.initkvbody(raidTeamIDX=raidTeamIDX, playerGBID=playerGBID)
            if not self.isInRaid():
                return None, gameconst.RaidErrno.RAID_NOT_IN_RAID
            if playerGBID == self.gbId:
                return None, gameconst.RaidErrno.RAID_KICKOUT_SELF
            return None, gameconst.RaidErrno.RAID_OK

        _, err = _commonCheck()
        if err != gameconst.RaidErrno.RAID_OK:
            WARNING_MSG('kickOutRaidMember:: common-check failed, {}'.format(err))
            return

        extraProps = {}
        if self.isRaidLeader():
            self._raidLeaderKickOutRaidMember(raidTeamIDX, playerGBID, extraProps)
        elif self.isRaidDeputy():
            self._raidDeputyKickOutRaidMember(raidTeamIDX, playerGBID, extraProps)
        '''
        #
        elif self.isRaidCaptain():
            self._raidTeamCaptainKickOutRaidMember(raidTeamIDX, playerGBID, extraProps)
        '''

    def _raidLeaderKickOutRaidMember(self, raidTeamIDX, playerGBID, extraProps):
        DEBUG_MSG('_raidLeaderKickOutRaidMember::', raidTeamIDX, playerGBID)
        raidUUID = self.raidUUID
        gameengine.getRaidStub(raidUUID).raidLeaderKickOutRaidMember(
            self.base, self.gbId, raidUUID, raidTeamIDX, playerGBID, extraProps)

    def _raidDeputyKickOutRaidMember(self, raidTeamIDX, playerGBID, extraProps):
        DEBUG_MSG('_raidDeputyKickOutRaidMember::', raidTeamIDX, playerGBID)
        raidUUID = self.raidUUID
        gameengine.getRaidStub(raidUUID).raidDeputyKickOutRaidMember(
            self.base, self.gbId, raidUUID, raidTeamIDX, playerGBID, extraProps)
    #
    def _raidTeamCaptainKickOutRaidMember(self, raidTeamIDX, playerGBID, extraProps):
        DEBUG_MSG('_raidTeamCaptainKickOutRaidMember::', raidTeamIDX, playerGBID)
        raidUUID = self.raidUUID
        gameengine.getRaidStub(raidUUID).raidTeamCaptainKickOutRaidMember(
            self.base, self.gbId, raidUUID, raidTeamIDX, playerGBID, extraProps)

    def onRaidLeaderKickOutRaidMember(self, raidUUID, koPlayerRaidTeamIDX, koPlayerGBID, extra):
        INFO_MSG('onRaidLeaderKickOutRaidMember::', raidUUID, koPlayerRaidTeamIDX, koPlayerGBID, extra)

    def onBeKickedOutRaidByRaidLeader(self, raidUUID, extraProps):
        INFO_MSG('onBeKickedOutRaidByRaidLeader::', raidUUID, extraProps)
        if raidUUID != self.raidUUID:
            WARNING_MSG('onBeKickedOutRaidByRaidLeader:: '
                        'raidUUID not match, skip clear cache', raidUUID, self.raidUUID)
            return
        self._onLeaveRaid()

    def onRaidDeputyKickOutRaidMember(self, raidUUID, koPlayerRaidTeamIDX, koPlayerGBID, extra):
        INFO_MSG('onRaidDeputyKickOutRaidMember::', raidUUID, koPlayerRaidTeamIDX, koPlayerGBID, extra)

    def onBeKickedOutRaidByRaidDeputy(self, raidUUID, extraProps):
        INFO_MSG('onBeKickedOutRaidByRaidDeputy::', raidUUID, extraProps)
        if raidUUID != self.raidUUID:
            WARNING_MSG('onBeKickedOutRaidByRaidDeputy:: '
                        'raidUUID not match, skip clear cache', raidUUID, self.raidUUID)
            return
        self._onLeaveRaid()
    #
    def onRaidTeamCaptainKickOutRaidMember(self, raidUUID, koPlayerRaidTeamIDX, koPlayerGBID, extra):
        INFO_MSG('onRaidTeamCaptainKickOutRaidMember::', raidUUID, koPlayerRaidTeamIDX, koPlayerGBID, extra)
    #
    def onBeKickedOutRaidByRaidTeamCaptain(self, raidUUID, extraProps):
        INFO_MSG('onBeKickedOutRaidByRaidTeamCaptain::', raidUUID, extraProps)
        if raidUUID != self.raidUUID:
            WARNING_MSG('onBeKickedOutRaidByRaidTeamCaptain:: '
                        'raidUUID not match, skip clear cache', raidUUID, self.raidUUID)
            return
        self._onLeaveRaid()

    @utils.isMyself
    @raidPermissionCheck(needPermission=gameconst.RaidPermission.LEADER, onlyMode=True)
    def transferRaidLeader(self, exposed, toPlayerGBID):
        """API: 团长变更"""
        INFO_MSG('transferRaidLeader::', toPlayerGBID)
        _, err = self._transferRaidLeaderCheck(toPlayerGBID)
        if err != gameconst.RaidErrno.RAID_OK:
            WARNING_MSG('transferRaidLeader:: check failed, {}'.format(err))
            return

        extraProps = {}
        raidUUID = self.raidUUID
        gameengine.getRaidStub(raidUUID).transferRaidLeader(
            self.base, self.gbId, raidUUID, toPlayerGBID, extraProps)

    def _transferRaidLeaderCheck(self, toPlayerGBID):
        if not toPlayerGBID:
            return None, gameconst.RaidErrno.RAID_PARAM_ERR.initkvbody(toPlayerGBID=toPlayerGBID)
        if not self.isInRaid():
            return None, gameconst.RaidErrno.RAID_NOT_IN_RAID
        if not self.isRaidLeader():
            return None, gameconst.RaidErrno.RAID_NOT_RAID_LEADER
        if toPlayerGBID == self.raidInfo.raidLeaderGBID:
            return None, gameconst.RaidErrno.RAID_IS_SAME_PLAYER.initkvbody(toPlayerGBID=toPlayerGBID)
        return None, gameconst.RaidErrno.RAID_OK

    @utils.isMyself
    @raidPermissionCheck(needPermission=gameconst.RaidPermission.LEADER, onlyMode=True)
    def transferRaidDeputy(self, exposed, toPlayerGBID):
        """API: 副团长变更"""
        INFO_MSG('transferRaidDeputy::', toPlayerGBID)
        _, err = self._transferRaidDeputyCheck(toPlayerGBID)
        if err != gameconst.RaidErrno.RAID_OK:
            WARNING_MSG('transferRaidDeputy:: check failed, {}'.format(err))
            return

        extraProps = {}
        raidUUID = self.raidUUID
        gameengine.getRaidStub(raidUUID).transferRaidDeputy(
            self.base, self.gbId, raidUUID, toPlayerGBID, extraProps)

    def _transferRaidDeputyCheck(self, toPlayerGBID):
        if not self.isInRaid():
            return None, gameconst.RaidErrno.RAID_NOT_IN_RAID
        if not self.isRaidLeader():
            return None, gameconst.RaidErrno.RAID_NOT_RAID_LEADER
        if toPlayerGBID == self.raidInfo.raidDeputyGBID:
            return None, gameconst.RaidErrno.RAID_IS_SAME_PLAYER.initkvbody(toPlayerGBID=toPlayerGBID)
        if toPlayerGBID == self.raidInfo.raidLeaderGBID:
            return None, gameconst.RaidErrno.RAID_NOT_RAID_LEADER.initkvbody(toPlayerGBID=toPlayerGBID)
        return None, gameconst.RaidErrno.RAID_OK
    #
    @utils.isMyself
    @raidPermissionCheck(needPermission=gameconst.RaidPermission.CAPTAIN, onlyMode=True)
    def transferRaidTeamCaptain(self, exposed, toPlayerGBID):
        """API: 小队队长(除团长所在小队)更换相应队长"""
        INFO_MSG('transferRaidTeamCaptain::', toPlayerGBID)
        _, err = self._transferRaidTeamCaptainCheck(toPlayerGBID)
        if err != gameconst.RaidErrno.RAID_OK:
            WARNING_MSG('transferRaidTeamCaptain:: check failed, {}'.format(err))
            return

        extraProps = {}
        raidUUID = self.raidUUID
        gameengine.getRaidStub(raidUUID).transferRaidTeamCaptain(
            self.base, self.gbId, raidUUID, toPlayerGBID, extraProps)
    #
    def _transferRaidTeamCaptainCheck(self, toPlayerGBID):
        if not toPlayerGBID:
            return None, gameconst.RaidErrno.RAID_PARAM_ERR.initkvbody(toPlayerGBID=toPlayerGBID)
        if not self.isInRaid():
            return None, gameconst.RaidErrno.RAID_NOT_IN_RAID
        if self.isInRaidLeaderTeam():
            return None, gameconst.RaidErrno.RAID_LEADER_TEAM_CANT_TRANS_CAPTAIN
        if not self.isRaidCaptain():
            return None, gameconst.RaidErrno.RAID_NOT_TEAM_CAPTAIN
        return None, gameconst.RaidErrno.RAID_OK

    def onTransferRaidLeaderAllMemberNotify(self, raidUUID, srcPlayerGBID, toPlayerGBID, toPlayerTeamIDX, extraProps):
        INFO_MSG('onTransferRaidLeaderAllMemberNotify::', raidUUID, srcPlayerGBID, toPlayerGBID, toPlayerTeamIDX, extraProps)
        _, err = self._onTransferRaidLeaderAllMemberNotify(raidUUID, srcPlayerGBID, toPlayerGBID, toPlayerTeamIDX)
        if err != gameconst.RaidErrno.RAID_OK:
            WARNING_MSG('onTransferRaidLeaderAllMemberNotify:: refresh cache failed, {}'.format(err))
            self.forceRefreshRaidCache()

        # 【【团队】跟随状态下，更换团长，跟随状态没有清除】
        self._cancelFollowTeamCaptain()

    def _onTransferRaidLeaderAllMemberNotify(self, raidUUID, srcPlayerGBID, toPlayerGBID, toPlayerTeamIDX):
        if raidUUID != self.raidInfo.raidUUID:
            return None, gameconst.RaidErrno.RAID_RAID_ID_NOT_FOUND

        if toPlayerTeamIDX not in self.raidInfo.raidTeamDic:
            return None, gameconst.RaidErrno.RAID_TEAM_IDX_NOT_FOUND

        teamCacheVal = self.raidInfo.raidTeamDic[toPlayerTeamIDX]
        if toPlayerGBID not in teamCacheVal.teamPlayerDic:
            return None, gameconst.RaidErrno.RAID_TEAM_MEMBER_NOT_MATCH

        # refresh team captain GBID
        # teamCacheVal.teamCaptainGBID = toPlayerGBID
        #if self.raidInfo.raidTeamIDX == toPlayerTeamIDX:
        #    # 相同小队刷新raidInfo上小队队长缓存
        #    self.raidInfo.raidCaptainGBID = toPlayerGBID
        # refresh raid leader GBID
        self.raidInfo.raidLeaderGBID = toPlayerGBID
        self.raidInfo.raidLeaderTeamIDX = toPlayerTeamIDX
        # 【【程序自主】团队中团员职务暴露给所有客户端】
        self.raidAuth = self.raidPermission

        return None, gameconst.RaidErrno.RAID_OK

    def onTransferRaidDeputyAllMemberNotify(self, raidUUID, srcPlayerGBID, toPlayerGBID, toPlayerTeamIDX, extraProps):
        INFO_MSG('onTransferRaidDeputyAllMemberNotify::', raidUUID, srcPlayerGBID, toPlayerGBID, toPlayerTeamIDX, extraProps)
        _, err = self._onTransferRaidDeputyAllMemberNotify(raidUUID, srcPlayerGBID, toPlayerGBID, toPlayerTeamIDX)
        if err != gameconst.RaidErrno.RAID_OK:
            WARNING_MSG('onTransferRaidDeputyAllMemberNotify:: refresh cache failed, {}'.format(err))
            self.forceRefreshRaidCache()

        # 【【团队】跟随状态下，更换团长，跟随状态没有清除】
        self._cancelFollowTeamCaptain()

    def _onTransferRaidDeputyAllMemberNotify(self, raidUUID, srcPlayerGBID, toPlayerGBID, toPlayerTeamIDX):
        if raidUUID != self.raidInfo.raidUUID:
            return None, gameconst.RaidErrno.RAID_RAID_ID_NOT_FOUND

        # refresh team captain GBID
        # teamCacheVal.teamCaptainGBID = toPlayerGBID
        #if self.raidInfo.raidTeamIDX == toPlayerTeamIDX:
        #    # 相同小队刷新raidInfo上小队队长缓存
        #    self.raidInfo.raidCaptainGBID = toPlayerGBID
        # refresh raid leader GBID
        self.raidInfo.raidDeputyGBID = toPlayerGBID
        self.raidInfo.raidDeputyTeamIDX = toPlayerTeamIDX
        # 【【程序自主】团队中团员职务暴露给所有客户端】
        self.raidAuth = self.raidPermission

        return None, gameconst.RaidErrno.RAID_OK
    #
    def onTransferRaidTeamCaptainAllMemberNotify(self, raidUUID, teamIDX, srcPlayerGBID, toPlayerGBID, extraProps):
        """转移队长成功后受到回调, 所有团队中玩家都收到该回调"""
        INFO_MSG('onTransferRaidTeamCaptainAllMemberNotify::', raidUUID, teamIDX, srcPlayerGBID, toPlayerGBID, extraProps)
        _, err = self._onTransferRaidTeamCaptainAllMemberNotify(raidUUID, teamIDX, srcPlayerGBID, toPlayerGBID)
        if err != gameconst.RaidErrno.RAID_OK:
            WARNING_MSG('onTransferRaidTeamCaptainAllMemberNotify:: refresh cache failed, {}'.format(err))
            self.forceRefreshRaidCache()
    #
    def _onTransferRaidTeamCaptainAllMemberNotify(self, raidUUID, teamIDX, srcPlayerGBID, toPlayerGBID):
        if raidUUID != self.raidInfo.raidUUID:
            return None, gameconst.RaidErrno.RAID_RAID_ID_NOT_MATCH

        if teamIDX not in self.raidInfo.raidTeamDic:
            return None, gameconst.RaidErrno.RAID_TEAM_IDX_NOT_FOUND

        teamCacheVal = self.raidInfo.raidTeamDic[teamIDX]
        if srcPlayerGBID not in teamCacheVal.teamPlayerDic or toPlayerGBID not in teamCacheVal.teamPlayerDic:
            return None, gameconst.RaidErrno.RAID_TEAM_MEMBER_NOT_MATCH

        teamCacheVal.teamCaptainGBID = toPlayerGBID
        if self.raidInfo.raidTeamIDX == teamIDX:
            # 相同小队刷新raidInfo上小队队长缓存
            self.raidInfo.raidCaptainGBID = toPlayerGBID
        # 【【程序自主】团队中团员职务暴露给所有客户端】
        self.raidAuth = self.raidPermission

        return None, gameconst.RaidErrno.RAID_OK
    #
    @utils.isMyself
    @raidPermissionCheck(needPermission=gameconst.RaidPermission.LEADER)
    def awardRaidTeamCaptain(self, expsoed, awardRaidTeamIDX, toPlayerGBID):
        """API: 团长任命队长"""
        INFO_MSG('awardRaidTeamCaptain::', awardRaidTeamIDX, toPlayerGBID)
        _, err = self._awardRaidTeamCaptainCheck(awardRaidTeamIDX, toPlayerGBID)
        if err != gameconst.RaidErrno.RAID_OK:
            WARNING_MSG('awardRaidTeamCaptain:: check failed, {}'.format(err))
            return

        extraProps = {}
        raidUUID = self.raidUUID
        gameengine.getRaidStub(raidUUID).awardRaidTeamCaptain(
            self.base, self.gbId, raidUUID, awardRaidTeamIDX, toPlayerGBID, extraProps)
    #
    def _awardRaidTeamCaptainCheck(self, awardRaidTeamID, toPlayerGBID):
        if not (awardRaidTeamID and toPlayerGBID):
            return None, gameconst.RaidErrno.RAID_PARAM_ERR.initkvbody(awardRaidTeamID=awardRaidTeamID, toPlayerGBID=toPlayerGBID)
        if not self.isInRaid():
            return None, gameconst.RaidErrno.RAID_NOT_IN_RAID
        if awardRaidTeamID not in self.raidInfo.raidTeamDic:
            return None, gameconst.RaidErrno.RAID_TEAM_IDX_NOT_FOUND
        if awardRaidTeamID == self.raidInfo.raidLeaderTeamIDX:
            return None, gameconst.RaidErrno.RAID_AWARD_SELF_TEAM
        return None, gameconst.RaidErrno.RAID_OK
    #
    def onAwardRaidTeamCaptainAllMemberNotify(self, raidUUID, srcPlayerGBID, fromCaptainGBID,
                                              toRaidTeamIDX, toPlayerGBID, extra):
        """团长冲洗任命小队队长后所有玩家的回调"""
        INFO_MSG('onAwardRaidTeamCaptainAllMemberNotify::', raidUUID, srcPlayerGBID, fromCaptainGBID,
                 toRaidTeamIDX, toPlayerGBID, extra)
        _, err = self._onAwardRaidTeamCaptainAllMemberNotify(raidUUID, srcPlayerGBID, fromCaptainGBID,
                                                             toRaidTeamIDX, toPlayerGBID)
        if err != gameconst.RaidErrno.RAID_OK:
            WARNING_MSG('onAwardRaidTeamCaptainAllMemberNotify:: refresh cache failed, {}'.format(err))
            self.forceRefreshRaidCache()
    #
    def _onAwardRaidTeamCaptainAllMemberNotify(self, raidUUID, srcPlayerGBID, fromCaptainGBID,
                                               toRaidTeamIDX, toPlayerGBID):
        if raidUUID != self.raidInfo.raidUUID:
            return None, gameconst.RaidErrno.RAID_RAID_ID_NOT_MATCH

        if toRaidTeamIDX not in self.raidInfo.raidTeamDic:
            return None, gameconst.RaidErrno.RAID_TEAM_IDX_NOT_FOUND

        teamCacheVal = self.raidInfo.raidTeamDic[toRaidTeamIDX]
        teamPlayerDic = teamCacheVal.teamPlayerDic
        if fromCaptainGBID not in teamPlayerDic or toPlayerGBID not in teamPlayerDic:
            return None, gameconst.RaidErrno.RAID_TEAM_MEMBER_NOT_MATCH

        teamCacheVal.teamCaptainGBID = toPlayerGBID
        if self.raidInfo.raidTeamIDX == toRaidTeamIDX:
            # 相同小队刷新raidInfo上小队队长缓存
            self.raidInfo.raidCaptainGBID = toPlayerGBID
        # 【【程序自主】团队中团员职务暴露给所有客户端】
        self.raidAuth = self.raidPermission

        return None, gameconst.RaidErrno.RAID_OK

    @utils.isMyself
    @raidPermissionCheck(needPermission=gameconst.RaidPermission.DEPUTY)
    def moveRaidTeamMember(self, exposed, fromPlayerTeamIDX, fromPlayerGBID, toPlayerTeamIDX, toPlayerGBID):
        """API: 团长移动队员"""
        INFO_MSG('moveRaidTeamMember::', fromPlayerTeamIDX, fromPlayerGBID, toPlayerTeamIDX, toPlayerGBID)
        _, err = self._moveRaidTeamMemberCheck(fromPlayerTeamIDX, fromPlayerGBID, toPlayerTeamIDX, toPlayerGBID)
        if err != gameconst.RaidErrno.RAID_OK:
            WARNING_MSG('moveRaidTeamMember, check failed, {}'.format(err))
            return

        # 团长移动自己,则走团长任命
        if self.isRaidLeader() and (fromPlayerGBID == self.gbId or toPlayerGBID == self.gbId):
            self.transferRaidLeader(exposed, toPlayerGBID if fromPlayerGBID == self.gbId else fromPlayerGBID)
            return
        # 其余都走移动团员
        raidUUID = self.raidUUID
        extraProps = {}
        gameengine.getRaidStub(raidUUID).moveRaidTeamMember(self.base, self.gbId, raidUUID,
                                                            fromPlayerTeamIDX, fromPlayerGBID,
                                                            toPlayerTeamIDX, toPlayerGBID, extraProps)

    def _moveRaidTeamMemberCheck(self, fromPlayerTeamIDX, fromPlayerGBID, toPlayerTeamIDX, toPlayerGBID):
        if not (fromPlayerTeamIDX and fromPlayerGBID and toPlayerTeamIDX):
            return None, gameconst.RaidErrno.RAID_PARAM_ERR.initkvbody(fromPlayerTeamIDX=fromPlayerTeamIDX,
                                                                       fromPlayerGBID=fromPlayerGBID,
                                                                       toPlayerTeamIDX=toPlayerTeamIDX)

        if not self.isInRaid():
            return None, gameconst.RaidErrno.RAID_NOT_IN_RAID

        if not self.isRaidLeader() and not self.isRaidDeputy():
            return None, gameconst.RaidErrno.RAID_NOT_RAID_LEADER_OR_DEPUTY

        if fromPlayerTeamIDX == toPlayerTeamIDX and not toPlayerGBID:
            return None, gameconst.RaidErrno.RAID_IS_SAME_TEAM

        if fromPlayerGBID == toPlayerGBID:
            return None, gameconst.RaidErrno.RAID_IS_SAME_PLAYER
        # 副团长不能移动团长
        if self.isRaidDeputy() and (fromPlayerGBID == self.raidInfo.raidLeaderGBID or toPlayerGBID == self.raidInfo.raidLeaderGBID):
            return None, gameconst.RaidErrno.RAID_NOT_RAID_CANNOT_MOVE_LEADER

        return None, gameconst.RaidErrno.RAID_OK

    def onMoveRaidTeamMemberSucc(self, srcPlayerGBID, raidUUID, fromPlayerTeamIDX,
                                 fromPlayerGBID, toPlayerTeamIDX, toPlayerGBID, extraProps):
        INFO_MSG('onMoveRaidTeamMemberSucc::', srcPlayerGBID, raidUUID, fromPlayerTeamIDX,
                 fromPlayerGBID, toPlayerTeamIDX, toPlayerTeamIDX, toPlayerGBID, extraProps)
        if self.gbId == fromPlayerGBID:
            DEBUG_MSG('onMoveRaidTeamMemberSucc:: A(org) --> B(*)')
        elif self.gbId == toPlayerGBID:
            DEBUG_MSG('onMoveRaidTeamMemberSucc:: A(*) <-- B(org)')
        elif self.gbId == srcPlayerGBID:
            DEBUG_MSG('onMoveRaidTeamMemberSucc:: src~')
        else:
            DEBUG_MSG('onMoveRaidTeamMemberSucc:: only refresh data~')

    @utils.isMyself
    @raidPermissionCheck(needPermission=gameconst.RaidPermission.LEADER)
    def setRaidTarget(self, exposed, minLevel, minScore, recuitInfo, password, isAutoExpedition):
        DEBUG_MSG("setRaidTarget, ", minLevel, minScore, recuitInfo, password, isAutoExpedition)
        """API: 团长设置全团目标"""
        if not self.isInRaid():
            ERROR_MSG("setRaidTarget, not in team")
            return
        if not self.isRaidLeader():
            ERROR_MSG("setRaidTarget, not raid leader")
            return
        
        raidTarget = self.raidInfo.raidTarget
        raidTargetInfo = TMACTD.datas.get(raidTarget)
        if raidTargetInfo is None:
            ERROR_MSG("setRaidTarget, misssing teamTarget", raidTarget)
            return
        
        if raidTarget > 1:
            actData = AC_ADD.datas.get(int(raidTargetInfo['pareActivity']))
            if not actData or gameconst.ActivityControlType.RAID != int(actData['needTeam']):
                ERROR_MSG("setRaidTarget, wrong activity control need team type", raidTarget, minLevel, minScore)
                return
        
        cfgMinLv = raidTargetInfo['minLevel']
        if minLevel < cfgMinLv:
            ERROR_MSG("setRaidTarget, minLevel not enough", raidTarget, minLevel, cfgMinLv)
            return

        cfgMinScore = raidTargetInfo['minScore']
        if minScore < cfgMinScore:
            ERROR_MSG("setRaidTarget, minScore not enough", raidTarget, minScore, cfgMinScore)
            return

        if self.getTotalScore() < minScore:
            ERROR_MSG("setRaidTarget, totalScore not enough", raidTarget, self.getTotalScore(), minScore, cfgMinScore)
            return
        
        gameengine.getRaidStub(self.raidUUID).setRaidTarget(self.base, self.gbId, self.raidUUID, raidTarget, minLevel, minScore, recuitInfo, password, isAutoExpedition)
        return
    
    def onSetRaidTargetAllMemberNotify(self, srcPlayerGBID, raidUUID, newTargetId, minLevel, minScore, recruitInfo, password, isAutoExpedition):
        """设置全团目标后全团回调"""
        INFO_MSG('onSetRaidTargetAllMemberNotify::', srcPlayerGBID, raidUUID, newTargetId, minLevel, minScore, recruitInfo, password, isAutoExpedition)

        def _check():
            if not self.isInRaid():
                return None, gameconst.RaidErrno.RAID_NOT_IN_RAID

            if self.raidInfo.raidUUID != raidUUID:
                return None, gameconst.RaidErrno.RAID_RAID_ID_NOT_MATCH

            return None, gameconst.RaidErrno.RAID_OK

        _, err = _check()
        if err != gameconst.RaidErrno.RAID_OK:
            WARNING_MSG('onSetRaidTargetAllMemberNotify:: failed, {}'.format(err))
            return

        self.raidInfo.raidTarget = newTargetId
        self.raidInfo.raidMinLevel = minLevel
        self.raidInfo.raidMinScore = minScore
        self.raidInfo.recruitInfo = recruitInfo
        self.raidInfo.password = password
        self.raidInfo.isAutoExpedition = isAutoExpedition
        
    @utils.isMyself
    @raidPermissionCheck(needPermission=gameconst.RaidPermission.DEPUTY)
    def startRaidStandbyChecker(self, exposed):
        """API: 团长发起全团检查"""
        INFO_MSG('startRaidStandbyChecker::~')

        # def _check():
        #     if not self.isInRaid():
        #         return None, gameconst.RaidErrno.RAID_NOT_IN_RAID
        #     if not self.isRaidLeader() and not self.isRaidDeputy():
        #         return None, gameconst.RaidErrno.RAID_NOT_RAID_LEADER_OR_DEPUTY
            
        #     return None, gameconst.RaidErrno.RAID_OK

        # _, err = _check()
        # if err != gameconst.RaidErrno.RAID_OK:
        #     ERROR_MSG('startRaidStandbyChecker:: failed, {}'.format(err))
        #     return

        # raidUUID = self.raidUUID
        # extraProps = {}
        # gameengine.getRaidStub(raidUUID).startRaidStandbyChecker(
        #     self.base, self.gbId, raidUUID, extraProps)

    @utils.isMyself
    @raidPermissionCheck(needPermission=gameconst.RaidPermission.MEMBER)
    def replyRaidStandbyChecker(self, exposed, raidUUID, beAgreed):
        """API: 团队成员回应团长检查"""
        INFO_MSG('replyRaidStandbyChecker::', raidUUID, beAgreed)

        # def _check():
        #     if not self.isInRaid():
        #         return None, gameconst.RaidErrno.RAID_NOT_IN_RAID
        #     if raidUUID != self.raidInfo.raidUUID:
        #         return None, gameconst.RaidErrno.RAID_RAID_ID_NOT_MATCH
        #     return None, gameconst.RaidErrno.RAID_OK

        # _, err = _check()
        # if err != gameconst.RaidErrno.RAID_OK:
        #     ERROR_MSG('replyRaidStandbyChecker:: failed, {}'.format(err))
        #     return

        # raidUUID = self.raidUUID
        # extraProps = {}
        # gameengine.getRaidStub(raidUUID).replyRaidStandbyChecker(
        #     self.base, self.gbId, raidUUID, beAgreed, extraProps)

    # --------------------------------------------------------------------
    # RAID MICS
    @gamedecorator.crossServer
    @utils.isMyself
    @raidPermissionCheck(needPermission=gameconst.RaidPermission.LEADER)
    def switchRaidMicsMode(self, exposed, mode):
        """API: 开启团队麦功能"""
        INFO_MSG("switchRaidMicsMode~")
        _, err = self._switchRaidMicsModeCheck(mode)
        if err != gameconst.RaidErrno.RAID_OK:
            ERROR_MSG("switchRaidMicsMode::failed, errno={}".format(err))
            return

        self.base.switchRaidMicsModeBase(self.raidUUID, mode)


    def _switchRaidMicsModeCheck(self, mode):
        if not self.isInRaid():
            return None, gameconst.RaidErrno.RAID_NOT_IN_RAID

        if mode not in gameconst.RaidMicsMode.COLL_ALL:
            return None, gameconst.RaidErrno.RAID_MICS_MODE_ERR
        return None, gameconst.RaidErrno.RAID_OK

    @gamedecorator.crossServer
    @utils.isMyself
    @raidPermissionCheck(needPermission=gameconst.RaidPermission.MEMBER)
    def turnOnRaidMics(self, exposed):
        """API: 团队成员打开麦克风"""
        INFO_MSG("turnOnRaidMics::~")
        _, err = self._turnOnRaidMicsCheck()
        if err != gameconst.RaidErrno.RAID_OK:
            ERROR_MSG("turnOnRaidMics::failed, errno={}".format(err))
            return

        self.base.turnOnRaidMicsBase(self.raidUUID)

    def _turnOnRaidMicsCheck(self):
        if not self.isInRaid():
            return None, gameconst.RaidErrno.RAID_NOT_IN_RAID
        return None, gameconst.RaidErrno.RAID_OK

    def turnOffRaidMicsByForbidVoiceChat(self):
        DEBUG_MSG("turnOffRaidMicsByForbidVoiceChat ")
        _, err = self._turnOffRaidMicsCheck()
        if err != gameconst.RaidErrno.RAID_OK:
            return
        raidUUID = self.raidUUID
        extraProps = {}
        gameengine.getRaidStub(raidUUID).turnOffRaidMics(self.base, self.gbId, raidUUID, self.gbId, extraProps)

    @gamedecorator.crossServer
    @utils.isMyself
    @raidPermissionCheck(needPermission=gameconst.RaidPermission.MEMBER)
    def turnOffRaidMics(self, exposed):
        """API: 团队成员关闭麦克风"""
        INFO_MSG("turnOffRaidMics::~")
        _, err = self._turnOffRaidMicsCheck()
        if err != gameconst.RaidErrno.RAID_OK:
            ERROR_MSG("turnOffRaidMics::failed, errno={}".format(err))
            return

        raidUUID = self.raidUUID
        extraProps = {}
        gameengine.getRaidStub(raidUUID).turnOffRaidMics(
            self.base, self.gbId, raidUUID, self.gbId, extraProps)

    def _turnOffRaidMicsCheck(self):
        if not self.isInRaid():
            return None, gameconst.RaidErrno.RAID_NOT_IN_RAID
        return None, gameconst.RaidErrno.RAID_OK

    @utils.isMyself
    @raidPermissionCheck(needPermission=gameconst.RaidPermission.LEADER)
    def turnOnRaidMemberMics(self, exposed, playerGBID):
        """API: 打开特定成员麦克风"""
        INFO_MSG("turnOnRaidMemberMics::~")
        _, err = self._turnOnRaidMemberMicsCheck()
        if err != gameconst.RaidErrno.RAID_OK:
            ERROR_MSG("turnOnRaidMemberMics::failed, errno={}".format(err))
            return

        raidUUID = self.raidUUID
        extraProps = {}
        gameengine.getRaidStub(raidUUID).turnOnRaidMics(
            self.base, self.gbId, raidUUID, playerGBID, extraProps)

    def _turnOnRaidMemberMicsCheck(self):
        if not self.isInRaid():
            return None, gameconst.RaidErrno.RAID_NOT_IN_RAID
        return None, gameconst.RaidErrno.RAID_OK

    @utils.isMyself
    @raidPermissionCheck(needPermission=gameconst.RaidPermission.LEADER)
    def turnOffRaidMemberMics(self, exposed, playerGBID):
        """API: 关闭特定成员麦克风"""
        INFO_MSG("turnOffRaidMemberMics::~", playerGBID)
        _, err = self._turnOffRaidMemberMicsCheck()
        if err != gameconst.RaidErrno.RAID_OK:
            ERROR_MSG("turnOffRaidMemberMics::failed, errno={}".format(err))
            return

        raidUUID = self.raidUUID
        extraProps = {}
        gameengine.getRaidStub(raidUUID).turnOffRaidMics(
            self.base, self.gbId, raidUUID, playerGBID, extraProps)

    def _turnOffRaidMemberMicsCheck(self):
        if not self.isInRaid():
            return None, gameconst.RaidErrno.RAID_NOT_IN_RAID
        return None, gameconst.RaidErrno.RAID_OK

    @utils.isMyself
    @raidPermissionCheck(needPermission=gameconst.RaidPermission.LEADER)
    def blockRaidMemberMics(self, exposed, teamIDX, playerGBID):
        """API: 团长禁言团员"""
        INFO_MSG("blockRaidMemberMics::~")
        _, err = self._blockRaidMemberMicsCheck(teamIDX, playerGBID)
        if err != gameconst.RaidErrno.RAID_OK:
            ERROR_MSG("blockRaidMemberMics::failed, errno={}".format(err))
            return

        raidUUID = self.raidUUID
        extraProps = {}
        gameengine.getRaidStub(raidUUID).blockRaidMemberMics(
            self.base, self.gbId, raidUUID, teamIDX, playerGBID, extraProps)

    def _blockRaidMemberMicsCheck(self, teamIDX, playerGBID):
        if not self.isInRaid():
            return None, gameconst.RaidErrno.RAID_NOT_IN_RAID
        if not self.isRaidLeader():
            return None, gameconst.RaidErrno.RAID_NOT_RAID_LEADER
        return None, gameconst.RaidErrno.RAID_OK

    @utils.isMyself
    @raidPermissionCheck(needPermission=gameconst.RaidPermission.LEADER)
    def unblockRaidMemberMics(self, exposed, teamIDX, playerGBID):
        """API: 团长解除团员禁言"""
        INFO_MSG("unblockRaidMemberMics::~")
        _, err = self._unblockRaidMemberMicsCheck(teamIDX, playerGBID)
        if err != gameconst.RaidErrno.RAID_OK:
            ERROR_MSG("unblockRaidMemberMics::failed, errno={}".format(err))
            return

        raidUUID = self.raidUUID
        extraProps = {}
        gameengine.getRaidStub(raidUUID).unblockRaidMemberMics(
            self.base, self.gbId, raidUUID, teamIDX, playerGBID, extraProps)

    def _unblockRaidMemberMicsCheck(self, teamIDX, playerGBID):
        if not self.isInRaid():
            return None, gameconst.RaidErrno.RAID_NOT_IN_RAID
        if not self.isRaidLeader():
            return None, gameconst.RaidErrno.RAID_NOT_RAID_LEADER
        return None, gameconst.RaidErrno.RAID_OK

    @utils.isMyself
    @gamedecorator.limitcall(1)
    @raidPermissionCheck(needPermission=gameconst.RaidPermission.LEADER)
    def blockAllRaidMemberMics(self, exposed):
        """API: 团长全员禁麦"""
        INFO_MSG("blockAllRaidMemberMics::~")
        _, err = self._blockAllRaidMemberMics()
        if err != gameconst.RaidErrno.RAID_OK:
            ERROR_MSG("blockAllRaidMemberMics::failed, errno={}".format(err))
            return

        raidUUID = self.raidUUID
        extraProps = {}
        gameengine.getRaidStub(raidUUID).blockAllRaidMemberMics(
            self.base, self.gbId, raidUUID, extraProps)

    def _blockAllRaidMemberMics(self):
        if not self.isInRaid():
            return None, gameconst.RaidErrno.RAID_NOT_IN_RAID
        if not self.isRaidLeader():
            return None, gameconst.RaidErrno.RAID_NOT_RAID_LEADER
        return None, gameconst.RaidErrno.RAID_OK

    @utils.isMyself
    @gamedecorator.limitcall(1)
    @raidPermissionCheck(needPermission=gameconst.RaidPermission.LEADER)
    def unblockAllRaidMemberMics(self, exposed):
        """API: 团长全员禁麦"""
        INFO_MSG("unblockAllRaidMemberMics::~")
        _, err = self._unblockAllRaidMemberMics()
        if err != gameconst.RaidErrno.RAID_OK:
            ERROR_MSG("unblockAllRaidMemberMics::failed, errno={}".format(err))
            return

        raidUUID = self.raidUUID
        extraProps = {}
        gameengine.getRaidStub(raidUUID).unblockAllRaidMemberMics(
            self.base, self.gbId, raidUUID, extraProps)

    def _unblockAllRaidMemberMics(self):
        if not self.isInRaid():
            return None, gameconst.RaidErrno.RAID_NOT_IN_RAID
        if not self.isRaidLeader():
            return None, gameconst.RaidErrno.RAID_NOT_RAID_LEADER
        return None, gameconst.RaidErrno.RAID_OK


    # --------------------------------------------------------------------

    # --------------------------------------------------------------------
    # RAID FOLLOW
    def becomeRaidLeader(self):
        self.setFollowCaptain(False)

    def loseRaidLeader(self):
        self.setFollowCaptain(False)
    # --------------------------------------------------------------------

    ############################### 团队活动 洞府之争 start ##########################################################
    def raidReqEnterDongfuDungeon(self, enterType, create=False):
        DEBUG_MSG('in raidReqEnterDongfuDungeon:', enterType, self.raidUUID)
        if not self.raidUUID:
            WARNING_MSG('   in raidReqEnterDongfuDungeon, no raidUUID')
            self.showMsg(MMD.datas.dfzz_enterWithRaid, [])
            return

        if create and not self.raidInfo.isRaidLeader(self.gbId):
            self.showMsg(MMD.datas.dfzz_open_notRaidLeader, [])
            WARNING_MSG('   in raidReqEnterDongfuDungeon, no permition')
            return

        raidPlayers = self.raidInfo.getAllPlayerGBIDList()
        self.base.baseEnterDongfuDungeon(enterType, self.raidUUID, raidPlayers, create)

    def raidCloseDongfuDungeon(self, confirmClose):
        DEBUG_MSG('in raidCloseDongfuDungeon:', self.raidUUID, confirmClose)
        if not self.raidUUID:
            WARNING_MSG('   in raidCloseDongfuDungeon')
            self.showMsg(MMD.datas.dfzz_enterWithRaid, [])
            return

        if not self.raidInfo.isRaidLeader(self.gbId):
            self.showMsg(MMD.datas.dfzz_open_notRaidLeader, [])
            WARNING_MSG('   in raidCloseDongfuDungeon, no permition')
            return
        self.base.baseCloseDongfuWarDungeon(self.raidUUID, confirmClose)

    ############################### 团队活动 洞府之争 end ##########################################################


    # --------------------------------------------------------------------
    # TEAM CROSS SERVER
    def reCreateRaidInCrossServer(self, raidId):
        INFO_MSG("reCreateRaidInCrossServer", raidId)
        if raidId > 0:
            capacity = RAID_CONST.datas["raidMemberLimit"]["value"]
            leaderProps = self._getAvatarPropsForRaid().toSavedDict()
            gameengine.getRaidStub(raidId).reCreateOrJoinRaid(
                self.base, self.gbId, raidId, capacity, [leaderProps, ])

    # --------------------------------------------------------------------

    @utils.isMyself
    @raidPermissionCheck(needPermission=gameconst.RaidPermission.UNKNOWN, onlyMode=True)
    def reqRaidPlayerAutoMatch(self, exposed, target):
        DEBUG_MSG('in reqRaidPlayerAutoMatch')

        if target == 0 or target == 1:
            WARNING_MSG("reqRaidPlayerAutoMatch target error", target)
            return
        
        if self.isInTeam(self.gbId):
            WARNING_MSG('   in reqRaidPlayerAutoMatch, already in a team:', self.teamId)
            return
        
        if self.isInRaid():
            WARNING_MSG('   in reqRaidPlayerAutoMatch, already in a raid:', self.raidUUID)
            return

        raidTargetInfo = TMACTD.datas.get(target)
        if raidTargetInfo is None:
            ERROR_MSG("reqRaidPlayerAutoMatch, misssing teamTarget", target)
            return
        
        actData = AC_ADD.datas.get(int(raidTargetInfo['pareActivity']))
        if not actData or gameconst.ActivityControlType.RAID != int(actData['needTeam']):
            ERROR_MSG("reqRaidPlayerAutoMatch, wrong activity control need team type", target)
            return
        
        if not self.isReachTeamMemMinLevel():
            WARNING_MSG('   in reqRaidPlayerAutoMatch, level cond failed:', self.level)
            return

        if not self.isReachTeamMemMinScore(target):
            WARNING_MSG('   in reqRaidPlayerAutoMatch, score cond failed:', self.getTotalScore())
            return
        
        playerMatchDic = {
            'target' : target,
            'playerGbId': self.gbId,
            'playerBox': self.base,
            'playerName': self.name,
            'level': self.level,
            'school': self.school,
            'sex': self.sex,
            'picFrameId': self.appearance.outfitData.picFrameId,
            'bFollow': False,
            'bOnline': True,
            'spaceNo': self.spaceNo,
            'position': self.position,
            'hp': self.hp,
            'fullHp': self.fullHp,
            'score': self.getTotalScore(),
            'hpkScore': 0,
            'mountState': 0,
            'equipSetLv': 0,
            'raidUUID': self.raidUUID,
            'enableMics': True,
            'isBlockMics': False,
            'isDead': False,
            'openId': "openId",
        }
        gameengine.getGlobalBase('RaidMatchStub').raidPlayerAutoMatch(playerMatchDic)
        return
    
    @utils.isMyself
    def reqRaidPlayerStopAutoMatch(self, exposed):
        INFO_MSG('reqRaidPlayerStopAutoMatch::~')
        self.autoRaidMatchStartTime = 0
        self.autoRaidMatchTarget = 0
        gameengine.getGlobalBase('RaidMatchStub').raidPlayerStopAutoMatch(self.gbId)

    @utils.isMyself
    @raidPermissionCheck(needPermission=gameconst.RaidPermission.LEADER, onlyMode=True)
    def reqRaidAutoMatch(self, exposed):
        DEBUG_MSG('in reqRaidAutoMatch')
        if 0 == self.raidUUID:
            WARNING_MSG('   in reqRaidAutoMatch, not has a raid, self.raidUUID:', self.raidUUID)
            return
        if not self.isRaidLeader():
            WARNING_MSG('   in reqRaidAutoMatch, not raid leader')
            return

        gameengine.getRaidStub(self.raidUUID).raidPrepareAutoMatch(self.raidUUID)

    @utils.isMyself
    @raidPermissionCheck(needPermission=gameconst.RaidPermission.LEADER, onlyMode=True)
    def reqRaidStopAutoMatch(self, exposed):
        DEBUG_MSG('in reqRaidStopAutoMatch')
        if 0 == self.raidUUID:
            WARNING_MSG('   in reqRaidStopAutoMatch, not has a raid, self.raidUUID:', self.raidUUID)
            return
        if not self.isRaidLeader():
            WARNING_MSG('   in reqRaidStopAutoMatch, not raid leader')
            return
        
        gameengine.getRaidStub(self.raidUUID).raidPrepareStopAutoMatch(self.raidUUID)

    def onMemJoinRaidByAutoMatch(self, gbID):
        self._doSendOneMemberFollowAsk(gbID)

    def onCellRaidPlayerStartAutoMatch(self, startMatchTime, target):
        self.autoRaidMatchStartTime = startMatchTime
        self.autoRaidMatchTarget = target
        self.client.onRaidPlayerStartAutoMatch()
    
    def onCellRaidPlayerMatchedSucc(self):
        self.autoRaidMatchStartTime = 0
        self.autoRaidMatchTarget = 0
        self.client.onRaidPlayerStopAutoMatch()
        return
    
    def onCellRaidPlayerAutoMatchTimeout(self):
        self.autoRaidMatchStartTime = 0
        self.autoRaidMatchTarget = 0
        self.client.onRaidPlayerStopAutoMatch()
        self.showMsg(TMMCD.datas['leaveMatch_timeOverMsg']['value'], [])
        return

    @utils.isMyself
    def reqGetRaidList(self, exposed, lastTime, raidTarget):
        teamTargetInfo = TMACTD.datas.get(raidTarget)
        if teamTargetInfo is None:
            ERROR_MSG("reqGetRaidList, misssing raidTarget", raidTarget)
            return
        
        if raidTarget != 1:
            actData = AC_ADD.datas.get(int(teamTargetInfo['pareActivity']))
            if not actData or gameconst.ActivityControlType.RAID != int(actData['needTeam']):
                ERROR_MSG("reqGetRaidList, wrong activity control need team type", raidTarget)
                return
            
        recordsDic = self.getTempMiscProp(gameconst.AvatarProps.getRaidListRecordData)
        if not recordsDic:
            recordsDic = {}
            self.setTempMiscProp(gameconst.AvatarProps.getRaidListRecordData, recordsDic)

        if raidTarget not in recordsDic:
            recordsDic.setdefault(raidTarget, [0, 0])

        now = utils.getNow()
        lastGetTime = recordsDic[raidTarget][1]
        if lastGetTime+1 >= now:
            WARNING_MSG('Frequently call reqGetRaidList, raidTarget:', raidTarget, recordsDic)
            return
        recordsDic[raidTarget][1] = now

        lastTeamStubIndex = recordsDic[raidTarget][0]
        checkTime = utils.getNow()
        # checkTime 会下发给客户端，客户端根据 checkTime 判断是否是同一次 reqGetRaidList 的查询结果
        if lastTime == checkTime:
            checkTime += 1

        checkTeamstubNum = 0
        sendTeamNum=0
        startTeamStubIndex = lastTeamStubIndex+1
        gameengine.getRaidStub(startTeamStubIndex+checkTeamstubNum).getRaidList(self.base, raidTarget, checkTime,
                                                                       checkTeamstubNum, sendTeamNum, startTeamStubIndex)
    def onGetRaidListFinished(self, lastTeamStubIndex, teamTarget):
        self.client.onGetAllRaidList(teamTarget)
        recordsDic = self.getTempMiscProp(gameconst.AvatarProps.getRaidListRecordData)
        recordsDic[teamTarget][0] = lastTeamStubIndex

    def onPlayerMatchedRaid(self, raidUUID):
        if self.raidUUID > 0:
            WARNING_MSG('in onPlayerMatchedRaid, already join a raid:', self.raidUUID)
            return
        gameengine.getRaidStub(raidUUID).newRaidPlayerMatched(raidUUID, self._getAvatarPropsForRaid().toSavedDict())
        return
    
    def leaveRaidAutoMatch(self):
        DEBUG_MSG("leaveRaidAutoMatch~")
        if self.autoRaidMatchStartTime > 0:
            self.autoRaidMatchStartTime = 0
            self.autoRaidMatchTarget = 0
            gameengine.getGlobalBase('RaidMatchStub').raidPlayerStopAutoMatch(self.gbId)
        if self.raidUUID > 0 and self.isRaidLeader():
            gameengine.getRaidStub(self.raidUUID).raidPrepareStopAutoMatch(self.raidUUID)

    # 标记 begin
    @utils.isMyself
    def reqAddRaidMarkMember(self, exposed, type, index, name, gbId, entId, pos):
        """ API: 加入raid标记 """
        INFO_MSG('reqAddRaidMarkMember: ', type, index, name, gbId, entId, pos)

        # 检查
        if index <= 0 or index > gameconst.TEAM_MARK_MAX_SLOT or self.raidUUID <= 0:
            return
        
        gameengine.getRaidStub(self.raidUUID).reqAddRaidMarkMember(self.raidUUID, self.base, type, index, name, gbId, entId, pos)

    @utils.isMyself
    def reqDelRaidMarkMember(self, exposed, type, index):
        """ API: 移除raid标记 """
        INFO_MSG('reqDelRaidMarkMember: ', self.raidUUID, type, index)

        # 检查
        if index <= 0 or index > gameconst.TEAM_MARK_MAX_SLOT or self.raidUUID <= 0:
            return
        
        gameengine.getRaidStub(self.raidUUID).reqDelRaidMarkMember(self.raidUUID, self.base, type, index)

    @utils.isMyself
    @gamedecorator.limitcall(2)
    def reqChangeRaidOnlyLeader(self, exposed, state):
        """ API: 变更仅leader修改标记的状态 """
        INFO_MSG('reqChangeRaidOnlyLeader: ', state)

        # 检查
        if not self.isRaidLeader():
            DEBUG_MSG('reqChangeRaidOnlyLeader: not leader')
            return
        
        gameengine.getRaidStub(self.raidUUID).reqChangeRaidOnlyLeader(self.raidUUID, self.base, state)

    @utils.isMyself
    @gamedecorator.limitcall(2)
    @raidPermissionCheck(needPermission=gameconst.RaidPermission.UNKNOWN, onlyMode=True)
    def reqJoinRaid(self, exposed, raidUUID, password):
        INFO_MSG('reqJoinRaid::', raidUUID, password)
        _, err = self._onJoinRaidCheck(raidUUID)
        if err != gameconst.RaidErrno.RAID_OK:
            ERROR_MSG('onJoinPlayerReplyJoinRaidLonely::, check failed, {}'.format(err))
            self.client.onJoinRaid(err.errno, raidUUID, password)
        else:
            playerProps = self._getAvatarPropsForRaid().toSavedDict()
            gameengine.getRaidStub(raidUUID).reqJoinRaid(self.base, raidUUID, password, playerProps)
    
    def _onJoinRaidCheck(self):
        _errno = gameconst.RaidErrno
        if self.isInRaid():
            return _errno.RAID_ALREADY_IN_RAID.initkvbody(source='_onJoinRaidCheck')
        if self.isInTeam(self.gbId):
            return _errno.RAID_ALREADY_IN_TEAM.initkvbody(source='_onJoinRaidCheck')

        return _errno.RAID_OK
