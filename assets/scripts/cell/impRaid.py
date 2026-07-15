# coding: utf-8
from KBEDebug import *
import KBEngine

import functools

import gamedecorator
import gameengine
import gameconst
import gametimer
import dataUtils
import utils
import gameconfig

import message_Message_def as M_M_DD
import raid_raidConst as R_RCD
import activityControl_activityData as AC_ADD
import teamMatch_activity as TMACTD
import teamMatch_matchConfig as TM_MCD

import raid
import dungeonSrc
import formula


def raidPermissionCheck(needPermission=gameconst.RaidPermissionEnum.UNKNOWN, onlyMode=False, exclude=()):
    def _raidPermission(fn):
        @functools.wraps(fn)
        def _wrapper(self, *args, **kwargs):
            _selfPermission = self.raidPermissionVal
            if not gameconst.RaidPermissionEnum.haveRaidPermission(_selfPermission, needPermission,
                                                           onlyMode=onlyMode, exluce=exclude):
                LOG_WARN('wrapper::raidPermissionVal::{}, permission denied'.format(fn.__name__),
                            _selfPermission, needPermission)
                return
            return fn(self, *args, **kwargs)
        return _wrapper
    return _raidPermission


def lockRaid(timeout=3):
    assert timeout > 0
    def _lockRaid(fn):
        @functools.wraps(fn)
        def _wrapper(self, *args, **kwargs):
            _m_lockedSucc = self._lockRaidProcess(timeout=timeout)
            if not _m_lockedSucc:
                LOG_ERR("lockRaid::", fn.__name__, args, kwargs)
                return
            _r = fn(self, *args, **kwargs)
            if not _r:
                LOG_WARN(f"lockRaid::{fn.__name__}:: auto fail unlocked")
                self._unlockRaidProcess()
        return _wrapper
    return _lockRaid


def unlockRaid(fn):
    @functools.wraps(fn)
    def _wrapper(self, *args, **kwargs):
        self._unlockRaidProcess()
        return fn(self, *args, **kwargs)
    return _wrapper


class ImpRaid(object):

    # ---------------------------------------------------------------
    # Cache Lock

    def _lockRaidProcess(self, timeout):
        if self.isRaidLocked():
            return False
        else:
            self.raidProcessLock = utils.curTS() + timeout
            return True

    def _unlockRaidProcess(self):
        self.raidProcessLock = 0

    def isRaidLocked(self):
        if utils.curTS() > self.raidProcessLock:
            return False
        else:
            return True

    # --------------------------------------------------------------

    @property
    def createRaidWithTeamCheckRecord(self) -> dict:
        if not self.hasTempMiscProp(gameconst.EntityPropsEnum.raidCreateRaidTeamCheck):
            self.setTempMiscProp(gameconst.EntityPropsEnum.raidCreateRaidTeamCheck, {})
        return self.getTempMiscProp(gameconst.EntityPropsEnum.raidCreateRaidTeamCheck)

    @createRaidWithTeamCheckRecord.setter
    def createRaidWithTeamCheckRecord(self, newValue):
        self.setTempMiscProp(gameconst.EntityPropsEnum.raidCreateRaidTeamCheck, newValue)

    def clearCreateRaidWithTeamCheckRecord(self):
        self.createRaidWithTeamCheckRecord.clear()

    def inRaid(self):
        return self.raidInfo.raidUUID > 0

    def isInRaidLeaderTeam(self):
        return self.raidInfo.raidTeamIDX == self.raidInfo.raidLeaderTeamIDX

    def isRaidLeader(self):
        return self.raidInfo.raidLeaderGBID and self.gbId == self.raidInfo.raidLeaderGBID

    def isRaidDeputy(self):
        return self.raidInfo.raidDeputyGBID and self.gbId == self.raidInfo.raidDeputyGBID

    def isInSameRaidTeam(self, target):
        return self.raidId\
            and self.raidId == target.raidId\
            and self.raidInfo.raidTeamIDX == target.raidInfo.raidTeamIDX

    def isRaidCaptain(self):
        return self.gbId == self.raidInfo.raidCaptainGBID

    def getRaidLeaderGBID(self):
        return self.raidInfo.raidLeaderGBID

    def forceRefreshRaidCache(self):
        LOG_WARN('forceRefreshRaidCache:: ~')
        if not self.inRaid():
            LOG_ERR('forceRefreshRaidCache::, failed, {}'.format(gameconst.RaidErrno.ENUM_RAID_NOT_IN_RAID))
            return None, gameconst.RaidErrno.ENUM_RAID_NOT_IN_RAID
        extraProps = {}
        raidUUID = self.raidUUID
        gameengine.getRaidStub(raidUUID)\
            .refreshRaidCache(raidUUID, [self.gbId], extraProps)

    def onRefreshPlayerRaidCacheVal(self, newRaidCacheVal: raid.PlayerRaidCacheVal):
        LOG_INFO('onRefreshPlayerRaidCacheVal::', newRaidCacheVal)
        for teamVal in self.raidInfo.raidTeamDic.values():
            playerInfo = teamVal.teamPlayerDict.get(self.gbId, None)
            if not playerInfo:
                continue
            self.raidInfo.raidTeamIDX = teamVal.teamIDX
            self.joinType = playerInfo.joinType
            break
        self.raidInfo = newRaidCacheVal
        self.joinType = gameconst.TeamJoinType.DEFAULT

        if formula.inLineScene(self.spaceNo):
            isLeader = self.gbId == self.raidInfo.raidCaptainGBID
            _lineType = formula.fetchMapId(self.spaceNo)
            lineNo = formula.parseLineNo(self.spaceNo)
            gameengine.getLineStub(_lineType).updateLinePlayerInfo(
                lineNo, 
                self.base, 
                self.gbId, 
                {
                    'changeTeam':(self.raidId, newRaidCacheVal.raidUUID, isLeader),
                }
            )

        self.raidUUID = newRaidCacheVal.raidUUID
        # 【【程序自主】团队中团员职务暴露给所有客户端】
        self.raidAuth = self.raidPermissionVal
        '''
        if oldRaidUUID != self.raidUUID:
            self.checkEliteInvRaidUUID(oldRaidUUID, self.raidUUID)
        '''

    def onRefreshPlayerRaidMemberCacheVal(self, raidUUID, teamIDX, playerGBID, propsDic, needDel):
        LOG_DBG('onRefreshPlayerRaidMemberCacheVal::', raidUUID, teamIDX, playerGBID, needDel)
        _, err = self._onRefreshPlayerRaidMemberCacheVal(raidUUID, teamIDX, playerGBID, propsDic, needDel)
        if err != gameconst.RaidErrno.ENUM_RAID_OK:
            LOG_WARN('onRefreshPlayerRaidMemberCacheVal:: failed, {}'.format(err))

    def _onRefreshPlayerRaidMemberCacheVal(self, raidUUID, teamIDX, playerGBID, newRaidTeamMemberCacheValDic, needDel):
        _errno = gameconst.RaidErrno
        if raidUUID != self.raidInfo.raidUUID:
            return None, _errno.ENUM_RAID_RAID_ID_NOT_MATCH.initkvbody(
                source='_onRefreshPlayerRaidMemberCacheVal',
                orgRaidUUID=self.raidInfo.raidUUID,
                crtRaidUUID=raidUUID)

        _raidTeamVal = self.raidInfo.raidTeamDic.get(teamIDX, None)
        if not _raidTeamVal:
            return None, _errno.ENUM_RAID_TEAM_IDX_NOT_FOUND.initkvbody(source='_onRefreshPlayerRaidMemberCacheVal',
                                                                  raidUUID=raidUUID,
                                                                  teamIDX=teamIDX)

        raidTeamMemberVal = _raidTeamVal.teamPlayerDict.get(playerGBID, None)
        if not raidTeamMemberVal:
            return None, _errno.ENUM_RAID_PLAYER_GBID_NOT_FOUND.initkvbody(source='_onRefreshPlayerRaidMemberCacheVal',
                                                                     raidUUID=raidUUID,
                                                                     teamIDX=teamIDX,
                                                                     playerGBID=playerGBID)

        if needDel:
            _raidTeamVal.teamPlayerDict.pop(playerGBID, None)
        else:
            raidTeamMemberVal.updateAttr(newRaidTeamMemberCacheValDic)

        return raidTeamMemberVal, _errno.ENUM_RAID_OK

    def __init__(self):
        if not hasattr(self, 'raidId'):
            # 团队ID, 固化ID, ALL_CLIENTS
            # NOTE: DO NOT USE 'raidId' directly, try use property 'raidUUID'
            self.raidId = 0

        if not hasattr(self, 'raidInfo'):
            # 团队在Avatar身上的缓存, cell私有
            self.raidInfo = raid.PlayerRaidCacheVal()

        if not hasattr(self, 'raidAuth'):
            # 团队权限, ALL_CLIENTS
            self.raidAuth = self.raidPermissionVal

    @property
    def raidBeInvitedRecordDic(self) -> dict:
        """受到团队(团长/队长)邀请记录"""
        if not self.hasTempMiscProp(gameconst.EntityPropsEnum.raidBeInvitedRecordDic):
            self.setTempMiscProp(gameconst.EntityPropsEnum.raidBeInvitedRecordDic, {})
        return self.getTempMiscProp(gameconst.EntityPropsEnum.raidBeInvitedRecordDic)

    @property
    def raidJoinRecord(self) -> dict:
        """申请加入团队记录"""
        if not self.hasTempMiscProp(gameconst.EntityPropsEnum.raidJoinRecord):
            self.setTempMiscProp(gameconst.EntityPropsEnum.raidJoinRecord, {})
        return self.getTempMiscProp(gameconst.EntityPropsEnum.raidJoinRecord)

    @property
    def raidUUID(self):
        return self.raidId

    @property
    def raidAvatarPropsCache(self) -> dict:
        """玩家属性缓存, 用于raidTick刷新raidStub缓存"""
        if not self.hasTempMiscProp(gameconst.EntityPropsEnum.raidAvatarPropsCache):
            self.setTempMiscProp(gameconst.EntityPropsEnum.raidAvatarPropsCache, {})
        return self.getTempMiscProp(gameconst.EntityPropsEnum.raidAvatarPropsCache)

    @raidUUID.setter
    def raidUUID(self, newRaidUUID):
        self._autoCtrlRaidTimer(self.raidId, newRaidUUID)
        _oldRaidId = self.raidId
        if _oldRaidId != newRaidUUID:
            self.raidId = newRaidUUID
            self.resetAllTargetTypeCache()

        if not _oldRaidId and newRaidUUID:
            self._unlockRaidProcess()
            self._onJoinNewRaid()

        self.base.onRaidChanged(self.raidId)

    def _onJoinNewRaid(self):
        if self._isCanLeaveTeamInAvatar():
            gameengine.getTeamStub(self.teamId).leaveTeam(
                self.spaceNo, self.base, self.teamId, self.gbId, True)

        self.stopTeamMatch()

    @property
    def raidTickTimerId(self):
        return self.getTempMiscProp(gameconst.EntityPropsEnum.raidTickTimerId, 0)

    @raidTickTimerId.setter
    def raidTickTimerId(self, newTimerId):
        self.setTempMiscProp(gameconst.EntityPropsEnum.raidTickTimerId, newTimerId)

    @property
    def raidPermissionVal(self):
        """获取团队权限"""
        if not self.inRaid():
            return gameconst.RaidPermissionEnum.UNKNOWN

        if self.isRaidLeader():
            return gameconst.RaidPermissionEnum.LEADER

        elif self.isRaidDeputy():
            return gameconst.RaidPermissionEnum.DEPUTY
        '''
        #
        elif self.isRaidCaptain():
            return gameconst.RaidPermissionEnum.CAPTAIN
        '''
        return gameconst.RaidPermissionEnum.MEMBER

    def raidTick(self):
        """刷新团队成员在raidStub上的一些缓存"""
        if not self.inRaid():
            LOG_ERR('raidTick:: not in raid')
            self.stopRaidTimer()
            return

        modified = False
        _lastRecord = self.raidAvatarPropsCache

        if 'level' not in _lastRecord or _lastRecord['level'] != self.level:
            _lastRecord['level'] = self.level
            modified = True
        pos = tuple(self.position)
        if 'spaceNo' not in _lastRecord or _lastRecord['spaceNo'] != self.spaceNo or 'position' not in _lastRecord or _lastRecord['position'] != pos:
            _lastRecord['spaceNo'] = self.spaceNo
            _lastRecord['position'] = pos
            modified = True
        if 'hp' not in _lastRecord or _lastRecord['hp'] != self.hp or 'fullHp' not in _lastRecord or _lastRecord['fullHp'] != self.fullHp:
            _lastRecord['hp'] = self.hp
            _lastRecord['fullHp'] = self.fullHp
            modified = True

        oldScore = _lastRecord.get('score', 0)
        newScore = self.getTotalScore()

        if 'score' not in _lastRecord or oldScore != newScore:
            LOG_DBG("in raidTick, score updated:", oldScore, newScore)
            _lastRecord['score'] = newScore
            modified = True

        if modified:
            excludedPlayerIDs = (self.gbId,)
            if 'spaceNo' in _lastRecord and 'position' in _lastRecord:
                for teamIDX, memberGBID, memberVal in self.raidInfo.iterGetRaidMember():
                    if memberGBID == self.gbId or not memberVal.playerBox:
                        continue
                    # 当只有spaceNo和position两个一起更新时，做一下筛选，视野范围内的就不需要通知了
                    if 'spaceNo' in _lastRecord and 'position' in _lastRecord and len(_lastRecord) == 2:
                        if self.checkInView(memberVal.playerBox.id):
                            excludedPlayerIDs += (memberGBID,)
            _lastRecord['excludedGbIDs'] = excludedPlayerIDs
            gameengine.getRaidStub(self.raidId).updateRaidMemberCacheVal(self.raidId, self.base, self.gbId, _lastRecord)

    def clearRaidCacheBoxOnOffline(self):
        if self.raidUUID <= 0:
            return

        LOG_INFO('clearRaidCacheBoxOnOffline set all playerBox to None')
        for _, _, memberVal in self.raidInfo.iterGetRaidMember():
            memberVal.playerBox = None

    def stopRaidTimer(self):
        if not self.raidTickTimerId:
            return

        LOG_INFO('stopRaidTimer::~')
        self.pyDelTimer(self.raidTickTimerId, gametimer.RAID_TICK)
        self.raidTickTimerId = 0

    def startRaidTimer(self):
        LOG_INFO('startRaidTimer~')
        self.stopRaidTimer()
        _dur = 1
        self.raidTickTimerId = self.pyAddTimer(_dur, _dur, gametimer.RAID_TICK)
        self._clearRaidJoinRecords()

    def _autoCtrlRaidTimer(self, crtRaidUUID, newRaidUUID):
        LOG_INFO('_autoCtrlRaidTimer::~ ', crtRaidUUID, newRaidUUID)
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
        return raid.RaidAndTeamMemberVal(
            playerGbId=self.gbId, playerBox=self.base, playerName=self.name,\
            level=self.level, school=self.school, sex=self.sex,\
            picFrameId=self.appearance.outfitData.picFrameId,\
            bOnline=True, spaceNo=self.spaceNo, position=self.position,\
            hp=self.hp, fullHp=self.fullHp, score=self.getTotalScore(),\
            openId="openId", siegeWarCamp=self.siegeWarCamp)

    @gamedecorator.checkGameconfigEnable('raid')
    @gamedecorator.crossServer
    @utils.isMyself
    @raidPermissionCheck(needPermission=gameconst.RaidPermissionEnum.MEMBER)
    def getRaidAllMembersAttrs(self, exposed, memberList):
        # LOG_INFO('getRaidAllMembersAttrs~')

        def _check():
            if not self.inRaid():
                return None, gameconst.RaidErrno.ENUM_RAID_NOT_IN_RAID
            return None, gameconst.RaidErrno.ENUM_RAID_OK

        _, err = _check()
        if err != gameconst.RaidErrno.ENUM_RAID_OK:
            LOG_ERR('getRaidAllMembersAttrs:: check failed, {}'.format(err))
            return

        _raidUUID = self.raidUUID
        extraProps = {}
        gameengine.getRaidStub(_raidUUID).getRaidAllMembersAttrs(
            self.base, self.gbId, _raidUUID, memberList, extraProps)

    @gamedecorator.checkGameconfigEnable('raid')
    @utils.isMyself
    @raidPermissionCheck(needPermission=gameconst.RaidPermissionEnum.DEPUTY)
    @gamedecorator.crossServer
    def getRaidApplyJoinDic(self, exposed):
        LOG_INFO('getRaidApplyJoinDic::~')

        def _check():
            if not self.inRaid():
                return None, gameconst.RaidErrno.ENUM_RAID_NOT_IN_RAID
            if not self.isRaidLeader() and not self.isRaidDeputy():
                return None, gameconst.RaidErrno.ENUM_RAID_NOT_RAID_LEADER_OR_DEPUTY
            return None, gameconst.RaidErrno.ENUM_RAID_OK

        _, err = _check()
        if err != gameconst.RaidErrno.ENUM_RAID_OK:
            LOG_ERR('getRaidApplyJoinRaidDic:: failed, {}'.format(err))
            return

        _raidUUID = self.raidUUID
        gameengine.getRaidStub(_raidUUID).getRaidApplyJoinDic(self.base, self.gbId, _raidUUID)

    @gamedecorator.checkGameconfigEnable('raid')
    @utils.isMyself
    @raidPermissionCheck(needPermission=gameconst.RaidPermissionEnum.DEPUTY)
    @gamedecorator.crossServer
    def clearRaidApplyJoinDic(self, exposed):
        LOG_INFO('clearRaidApplyJoinDic::~')
        _, err = self._clearRaidApplyJoinDicCheck()
        if err != gameconst.RaidErrno.ENUM_RAID_OK:
            LOG_ERR('clearRaidApplyJoinDic::, check failed, {}'.format(err))
            return
        _raidUUID = self.raidUUID
        gameengine.getRaidStub(self._raidUUID).clearRaidApplyJoinDic(self.base, self.gbId, _raidUUID)

    def _clearRaidApplyJoinDicCheck(self):
        if not self.inRaid():
            return None, gameconst.RaidErrno.ENUM_RAID_NOT_IN_RAID
        if not self.isRaidLeader() and not self.isRaidDeputy():
            return None, gameconst.RaidErrno.ENUM_RAID_NOT_RAID_LEADER_OR_DEPUTY
        return None, gameconst.RaidErrno.ENUM_RAID_OK

    def onJoinListPlayerClearRaidApplyJoinDic(self, raidUUID, joinType, teamUUID):
        LOG_INFO('onJoinListPlayerClearRaidApplyJoinDic::', raidUUID, joinType, teamUUID)
        _raidJoinRecord = self.raidJoinRecord
        if raidUUID not in _raidJoinRecord:
            LOG_WARN('onJoinListPlayerClearRaidApplyJoinDic:: raid cache missing', raidUUID)
            return

        cacheJoinType = _raidJoinRecord[raidUUID]
        if cacheJoinType != joinType:
            LOG_WARN('onJoinListPlayerClearRaidApplyJoinDic:: cache joinType not match', raidUUID, cacheJoinType, joinType)
            return

        if cacheJoinType == gameconst.RaidJoinTypeEnum.TEAM and teamUUID != self.teamInfo.teamId:
            LOG_WARN('onJoinListPlayerClearRaidApplyJoinDic:: teamUUID not match', raidUUID, self.teamInfo.teamId, teamUUID)
            return

        _raidJoinRecord.pop(raidUUID)

    def _clearRaidJoinRecords(self, withJoinTypes=()):
        _raidStubDic = {}
        for raidId, joinType in self.raidJoinRecord.items():
            if withJoinTypes and joinType not in withJoinTypes:
                continue
            _raidStubDic.setdefault(raidId, [])
            _raidStubDic[raidId].append((raidId, joinType))

        for raidId, raidIdList in _raidStubDic.items():
            _raidStub = gameengine.getRaidStub(raidId)
            _raidStub.clearRaidJoinRecords(self.base, self.gbId, raidIdList)

    def onClearRaidJoinRecords(self, clearRaidList):
        LOG_INFO('onClearRaidJoinRecords::', clearRaidList)
        raidJoinRecord = self.raidJoinRecord
        for raidUUID, joinType in clearRaidList:
            if joinType != raidJoinRecord.get(raidUUID):
                continue

            raidJoinRecord.pop(raidUUID, None)

    @gamedecorator.checkGameconfigEnable('raid')
    @utils.isMyself
    @lockRaid(timeout=3)
    @gamedecorator.crossServer
    def createRaidWithTeam(self, exposed, capacity):
        """API: 创建一个团队(小队)"""
        LOG_INFO('createRaidWithTeam::~', capacity)
        _, _err = self._createRaidWithTeamCheck(capacity)
        if _err != gameconst.RaidErrno.ENUM_RAID_OK:
            if _err == gameconst.RaidErrno.ENUM_RAID_TEAM_MEMBER_OFFLINE:
                LOG_WARN("createRaidWithTeam:: some player offline")
                gameengine.getTeamStub(self.teamId).onReplyInviteRaidAndTeamFail(
                    self.base, self.gbId, 0, self.gbId, self.teamId, _err.errno, {})

            elif _err == gameconst.RaidErrno.ENUM_RAID_UI_DENIED:
                LOG_WARN("createRaidWithTeam:: player check level failed", self.level)
                self.showMsg(R_RCD.datas["raidPartyInivte_underLevel_msg"]["value"], [])

            else:
                LOG_ERR('createRaidWithTeam:: check failed, {}'.format(_err))

            return

        extraProps = {'target':1}
        self.createRaidWithTeamCheckRecord = {i: (None, None) for i in self.teamInfo.teamPlayerDict}
        # timeout值要小于limitcall的值
        self.asyncCallbackAfter(1).clearCreateRaidWithTeamCheckRecord()
        self.checkTeamMembers(
            gameconst.CheckMemberReasonEnum.CHECK_MEMBER_FOR_RAID_DUNGEON_CREATE, 
            False, 
            gameconst.CELL, 
            (capacity, extraProps)
        )

        self._onCheckedMemberCreateRaidWithTeam(
            self.gbId, 
            gameconst.RaidErrno.ENUM_RAID_OK, 
            capacity, 
            extraProps)

        return True

    def _createRaidWithTeamCheck(self, capacity):
        errno = gameconst.RaidErrno

        if not self.isInTeam(self.gbId):
            return None, errno.ENUM_RAID_NOT_IN_TEAM.initkvbody(source='_createRaidWithTeamCheck')

        if not self.isCaptain():
            return None, errno.ENUM_RAID_NOT_TEAM_CAPTAIN.initkvbody(source='_createRaidWithTeamCheck')

        if self.inRaid():
            return None, errno.ENUM_RAID_ALREADY_IN_RAID.initkvbody(source='_createRaidWithTeamCheck')

        if not dataUtils.isRaidCapacityValidate(capacity):
            return None, errno.ENUM_RAID_UNKNOWN_CAPACITY.initkvbody(source='_createRaidWithTeamCheck')

        if self.teamInfo.offlineMembers():
            return None, errno.ENUM_RAID_TEAM_MEMBER_OFFLINE.initkvbody(source='_createRaidWithTeamCheck')

        if not self._isUIVisibleStrCell(dataUtils.getRaidConstDataValue("raidUIVisibleId"), True) \
            or not self._isUIVisibleStrCell(dataUtils.getRaidConstDataValue("raidDungeonUIVisibleId"), True):
            return None, errno.ENUM_RAID_UI_DENIED.initkvbody(source='_createRaidWithTeamCheck', level=self.level)

        return None, errno.ENUM_RAID_OK

    def _checkCreateRaidWithTeamMemberConditions(self, capacity, extra):
        """小队转化为团队: 小队成员检查条件"""
        LOG_INFO('_checkCreateRaidWithTeamMemberConditions::', capacity, extra)

        def _check():
            if self.inRaid():
                return None, gameconst.RaidErrno.ENUM_RAID_ALREADY_IN_RAID.initkvbody(
                    source='_checkCreateRaidWithTeamMemberConditions')
            if not self._isUIVisibleStrCell(dataUtils.getRaidConstDataValue("raidUIVisibleId"), True) \
                or not self._isUIVisibleStrCell(dataUtils.getRaidConstDataValue("raidDungeonUIVisibleId"), True):
                return None, gameconst.RaidErrno.ENUM_RAID_UI_DENIED.initkvbody(
                    source='_checkCreateRaidWithTeamMemberConditions', level=self.level)
            return None, gameconst.RaidErrno.ENUM_RAID_OK

        _, _err = _check()
        if _err != gameconst.RaidErrno.ENUM_RAID_OK:
            LOG_WARN('_createRaidWithTeamCheck:: member check failed, {}'.format(_err))
            return True, (_err, capacity, extra), ()

        return False, (_err, capacity, extra), ()

    def _onCheckedMemberCreateRaidWithTeam(self, memberGBID, err, capacity, extraDic):
        LOG_INFO('_onCheckedMemberCreateRaidWithTeam::', memberGBID, capacity, extraDic, err)
        _record = self.createRaidWithTeamCheckRecord
        if err != gameconst.RaidErrno.ENUM_RAID_OK:
            err.initkvbody(memberGBID=memberGBID)
            LOG_WARN('_onCheckedMemberCreateRaidWithTeam:: member check failed, {}'.format(err))
            _record[memberGBID] = (False, err)
        else:
            _record[memberGBID] = (True, err)

        checkResult = True
        if self.teamInfo.offlineMembers():
            checkResult = False

        if checkResult:
            for _, (result, _err) in _record.items():
                if result is None:
                    LOG_DBG('_onCheckedMemberCreateRaidWithTeam:: skill checking')
                    return
                elif not result:
                    err = _err
                    checkResult = False
                    break

        # clear if all checked
        self.clearCreateRaidWithTeamCheckRecord()

        if not checkResult:
            LOG_WARN('_onCheckedMemberCreateRaidWithTeam:: check failed', _record)
            if err == gameconst.RaidErrno.ENUM_RAID_ALREADY_IN_RAID:
                self.showMsg(M_M_DD.datas.raid_teamInvitationCheck_sectionTeam, [])
            elif err == gameconst.RaidErrno.ENUM_RAID_UI_DENIED:
                self.showMsg(R_RCD.datas["raidPartyInivte_underLevel_msg"]["value"], [])
            self._unlockRaidProcess()
            return

        self.doCreateRaidWithTeam(capacity, extraDic)

    def doCreateRaidWithTeam(self, capacity, extraProps):
        LOG_INFO('doCreateRaidWithTeam::', capacity, extraProps)
        _needCreatedRaidUUID = KBEngine.genUUID64()
        gameengine.getTeamStub(self.teamId).createRaidWithTeam(
            self.base, self.gbId, self.teamId, _needCreatedRaidUUID, capacity, extraProps)

    @gamedecorator.checkGameconfigEnable('raid')
    @utils.isMyself
    @raidPermissionCheck(needPermission=gameconst.RaidPermissionEnum.UNKNOWN, onlyMode=True)
    @lockRaid(timeout=3)
    @gamedecorator.limitcall(3)
    @gamedecorator.crossServer
    def createRaidLonely(self, exposed, capacity, raidTarget, minLevel, minScore, recruitInfo, password, isAutoExpedition):
        """API: 创建一个团队(单人)"""
        LOG_INFO('createRaidLonely::~', capacity, raidTarget, minLevel, minScore, recruitInfo, password, isAutoExpedition)
        if utils.formula.inTeamDungeonScene(self.spaceNo):
            LOG_ERR("createRaidLonely, current space check fail")
            return
        if not dataUtils.checkTeamPassword(password):
            LOG_ERR("createRaidLonely, illegal password", password)
            return
        _, err = self._createRaidLonelyCheck(capacity)
        if err != gameconst.RaidErrno.ENUM_RAID_OK:
            LOG_ERR('createRaidLonely:: check failed, {}'.format(
                err.initkvbody(source=self._createRaidLonelyCheck.__name__)))
            return

        if raidTarget <=0:
            LOG_ERR("createRaidLonely, illegal teamTarget", raidTarget)
            return

        teamTargetInfo = TMACTD.datas.get(raidTarget)
        if teamTargetInfo is None:
            LOG_ERR("createRaidLonely, misssing teamTarget", raidTarget)
            return

        if raidTarget > gameconst.PARE_ACTIVITY_ID:
            actData = AC_ADD.datas.get(int(teamTargetInfo['pareActivity']))
            if not actData or gameconst.ActivityControlType.RAID != int(actData['needTeam']):
                LOG_ERR("createRaidLonely, wrong activity control need team type", raidTarget)
                return
            if not self._isUIVisibleStrCell(dataUtils.getRaidConstDataValue("raidUIVisibleId"), True) \
                or not self._isUIVisibleStrCell(dataUtils.getRaidConstDataValue("raidDungeonUIVisibleId"), True):
                LOG_WARN("createRaidLonely, func is locked")
                return

        if not self.checkTeamCond(raidTarget, minLevel, minScore):
            return

        raidUUID = KBEngine.genUUID64()
        LOG_INFO('createRaidLonely::raidUUID: ', raidUUID)
        leaderProps = self._getAvatarPropsForRaid().toStreamSavedDic()
        leaderProps['joinType'] = gameconst.TeamJoinType.CREATE
        gameengine.getRaidStub(raidUUID).createRaidLonely(
            self.base, self.gbId, raidUUID, capacity, [leaderProps, ], {}, raidTarget, minLevel, minScore, recruitInfo, password, isAutoExpedition)
        return True

    def _createRaidLonelyCheck(self, capacity):
        errno = gameconst.RaidErrno
        if not dataUtils.isRaidCapacityValidate(capacity):
            return None, errno.ENUM_RAID_UNKNOWN_CAPACITY

        if self.inRaid():
            return None, errno.ENUM_RAID_ALREADY_IN_RAID

        if self.isInTeam(self.gbId):
            return None, errno.ENUM_RAID_ALREADY_IN_TEAM

        return None, errno.ENUM_RAID_OK

    @gamedecorator.checkGameconfigEnable('raid')
    @utils.isMyself
    @raidPermissionCheck(needPermission=gameconst.RaidPermissionEnum.LEADER, onlyMode=True)
    @gamedecorator.crossServer
    def disbandRaid(self, exposed):
        """API: 解散一个团队"""
        LOG_INFO('disbandRaid::~')
        _, err = self._disbandRaidCheck()
        if err != gameconst.RaidErrno.ENUM_RAID_OK:
            LOG_ERR('disbandRaid:: check failed, {}'.format(err))
            return
        
        #主动离开team会清空怪物上的首刀归属者标记
        for e in self.entitiesInView(True):
            if e.IsMonster:
                e.clearFirstBlood(self.id)

        gameengine.getRaidStub(self.raidInfo.raidUUID).disbandRaid(
            self.base, self.gbId, self.raidInfo.raidUUID, {})

    def _disbandRaidCheck(self):
        if not self.inRaid():
            return None, gameconst.RaidErrno.ENUM_RAID_NOT_IN_RAID.initkvbody(source='_disbandRaidCheck')

        if not self.isRaidLeader():
            return None, gameconst.RaidErrno.ENUM_RAID_NOT_RAID_LEADER.initkvbody(source='_disbandRaidCheck')

        return None, gameconst.RaidErrno.ENUM_RAID_OK

    @gamedecorator.checkGameconfigEnable('raid')
    @utils.isMyself
    @gamedecorator.crossServer
    def applyJoinRaidLonely(self, exposed, raidUUID, password, applySource):
        """API: 申请加入一个团队"""
        LOG_INFO('applyJoinRaidLonely::', raidUUID, password, applySource)
        if applySource not in gameconst.ApplySource.VALID_APPLY_SOURCE:
            LOG_ERR("applyJoinRaidLonely:: not valid apply source", applySource)
            return
        if not dataUtils.checkTeamPassword(password):
            LOG_ERR('applyJoinRaidLonely:: illegal password', password)
            return
        _, err = self._applyJoinRaidLonelyCheck(raidUUID, applySource)
        if err != gameconst.RaidErrno.ENUM_RAID_OK:
            err = err.initkvbody(source=self._applyJoinRaidLonelyCheck.__name__)
            LOG_WARN('applyJoinRaidLonely:: check failed, {}'.format(err))
            return
        
        extraProps = {}
        extraProps['isRaidUIVisibleId'] = self._isUIVisibleStrCell(dataUtils.getRaidConstDataValue("raidUIVisibleId"), False)
        extraProps['isRaidDungeonUIVisibleId'] = self._isUIVisibleStrCell(dataUtils.getRaidConstDataValue("raidDungeonUIVisibleId"), False)
        
        joinProps = self._getAvatarPropsForRaid().toStreamSavedDic()
        gameengine.getRaidStub(raidUUID).applyJoinRaidLonely(self.base, self.gbId, joinProps, raidUUID, extraProps, password, False, applySource)

    def _applyJoinRaidLonelyCheck(self, raidUUID, applySource):
        _errno = gameconst.RaidErrno
        if not raidUUID:
            return None, _errno.ENUM_RAID_PARAM_ERR.initkvbody(raidUUID=raidUUID)

        if self.inRaid():
            self.client and self.client.onApplyJoinRaidLonelyFailed(gameconst.TeamApplyResult.RAID_APPLY_IS_IN_RAID, 0, 0, 0, '', applySource)
            return None, _errno.ENUM_RAID_ALREADY_IN_RAID.initkvbody(raidUUID=raidUUID)

        if self.isInTeam():
            self.client and self.client.onApplyJoinRaidLonelyFailed(gameconst.TeamApplyResult.RAID_APPLY_IS_IN_TEAM, 0, 0, 0, '', applySource)
            return None, _errno.ENUM_RAID_ALREADY_IN_TEAM.initkvbody(teamId=self.teamId)
        
        if raidUUID in self.raidJoinRecord and self.raidJoinRecord[raidUUID] == gameconst.RaidJoinTypeEnum.SINGLE:
            self.client and self.client.onApplyJoinRaidLonelyFailed(gameconst.TeamApplyResult.RAID_APPLY_IS_APPLIED, 0, 0, 0, '', applySource)
            return None, _errno.ENUM_RAID_ALREADY_APPLY_JOIN.initkvbody(raidUUID=raidUUID)

        return None, _errno.ENUM_RAID_OK

    def onLeaderProcessApplyJoinRaidLonely(self, joinedPlayerBox, joinedPlayerGbId,
                                           joinedPlayerProps, raidUUID, extraProps):
        """成功申请团队后, 团长获得回调"""
        LOG_INFO('onLeaderProcessApplyJoinRaidLonely::', joinedPlayerBox,
                 joinedPlayerGbId, raidUUID, joinedPlayerProps, extraProps)
        self.client and self.client.beNotifiedApplyJoinRaid(raidUUID, joinedPlayerGbId, joinedPlayerProps)

    def onApplyJoinRaidLonelySucc(self, playerGBID, raidUUID, extraProps):
        """成功申请团队后, 申请者获得回调"""
        LOG_INFO('onApplyJoinRaidLonelySucc::', playerGBID, raidUUID, extraProps)
        self.raidJoinRecord[raidUUID] = gameconst.RaidJoinTypeEnum.SINGLE
        self.showMsg(R_RCD.datas["raid_applySent_msg"]["value"], [])

    @gamedecorator.checkGameconfigEnable('raid')
    @utils.isMyself
    @gamedecorator.crossServer
    def applyJoinRaidWithTeam(self, exposed, raidUUID):
        """API: 申请加入一个团队(小队加入)"""
        LOG_INFO('applyJoinRaidWithTeam::', raidUUID)
        _, err = self._applyJoinRaidWithTeamCheck(raidUUID)
        if err != gameconst.RaidErrno.ENUM_RAID_OK:
            LOG_WARN('applyJoinRaidWithTeam:: check failed, {}'.format(
                err.initkvbody(source=self._applyJoinRaidWithTeamCheck.__name__)))
            if err == gameconst.RaidErrno.ENUM_RAID_ALREADY_APPLY_JOIN:
                self.showMsg(R_RCD.datas["raid_applySent_msg"]["value"], [])
            return

        gameengine.getTeamStub(self.teamId).applyJoinRaidWithTeam(
            self.base, self.gbId, self.teamId, raidUUID, {})

    def _applyJoinRaidWithTeamCheck(self, raidUUID):
        _errno = gameconst.RaidErrno
        if not self._isUIVisibleStrCell(dataUtils.getRaidConstDataValue("raidUIVisibleId"), True) \
            or not self._isUIVisibleStrCell(dataUtils.getRaidConstDataValue("raidDungeonUIVisibleId"), True):
            return None, _errno.ENUM_RAID_UI_DENIED.initkvbody(level=self.level)

        if not raidUUID:
            return None, _errno.ENUM_RAID_PARAM_ERR.initkvbody(raidUUID=raidUUID)

        if self.inRaid():
            return None, _errno.ENUM_RAID_ALREADY_IN_RAID.initkvbody(raidUUID=raidUUID)

        if raidUUID in self.raidJoinRecord and self.raidJoinRecord[raidUUID] == gameconst.RaidJoinTypeEnum.TEAM:
            return None, _errno.ENUM_RAID_ALREADY_APPLY_JOIN.initkvbody(raidUUID=raidUUID)

        if not self.isInTeam(self.gbId):
            return None, _errno.ENUM_RAID_NOT_IN_TEAM.initkvbody(raidUUID=raidUUID)

        if not self.isCaptain():
            return None, _errno.ENUM_RAID_NOT_TEAM_CAPTAIN.initkvbody(raidUUID=raidUUID)

        return None, _errno.ENUM_RAID_OK

    def onLeaderProcessApplyJoinRaidWithTeam(self, joinCaptainBox, joinedCaptainGBID, joinedPlayersProps,
                                             teamUUID, raidUUID, extraProps):
        """组队成功申请团队后, 团长获得回调"""
        LOG_INFO('onLeaderProcessApplyJoinRaidWithTeam::',
                 joinCaptainBox, joinedCaptainGBID, 
                 joinedPlayersProps, teamUUID, extraProps, raidUUID)

        if self.client:
            self.client.beNotifiedApplyJoinRaid(raidUUID, joinedCaptainGBID, joinedPlayersProps)

    def onApplyJoinRaidWithTeamSucc(self, joinedCaptainGBID, teamUUID, raidUUID, extraProps):
        """组队成功申请团队后, 申请者获得回调"""
        LOG_INFO('onApplyJoinRaidWithTeamSucc::', joinedCaptainGBID, teamUUID, raidUUID, extraProps)
        self.raidJoinRecord[raidUUID] = gameconst.RaidJoinTypeEnum.TEAM
        self.showMsg(R_RCD.datas["raid_applySent_msg"]["value"], [])

    @gamedecorator.checkGameconfigEnable('raid')
    @utils.isMyself
    @raidPermissionCheck(needPermission=gameconst.RaidPermissionEnum.DEPUTY)
    @gamedecorator.crossServer
    def replyJoinRaid(self, exposed, playerGBID, beAgreed):
        """API: 确认某个申请的玩家/小队加入团队"""
        LOG_INFO('replyJoinRaid::', playerGBID, beAgreed)
        _, err = self._replyJoinRaidCheck(playerGBID)
        if err != gameconst.RaidErrno.ENUM_RAID_OK:
            err = err.initkvbody(source=self._replyJoinRaidCheck.__name__)
            LOG_WARN('replyJoinRaid:: check failed, {}'.format(err))
            return

        _raidUUID = self.raidUUID
        gameengine.getRaidStub(_raidUUID).replyJoinRaid(
            self.base, self.gbId, playerGBID, _raidUUID, beAgreed, {})

    def _replyJoinRaidCheck(self, playerGBID):
        if not playerGBID:
            return None, gameconst.RaidErrno.ENUM_RAID_PARAM_ERR.initkvbody(playerGBID=playerGBID)

        if playerGBID == self.gbId:
            return None, gameconst.RaidErrno.ENUM_UNKNOWN.initkvbody(reason='self-replied')

        if not self.inRaid():
            return None, gameconst.RaidErrno.ENUM_RAID_NOT_IN_RAID

        if not self.isRaidLeader() and not self.isRaidDeputy():
            return None, gameconst.RaidErrno.ENUM_RAID_NOT_RAID_LEADER_OR_DEPUTY

        return None, gameconst.RaidErrno.ENUM_RAID_OK

    @lockRaid(timeout=1)
    def onJoinPlayerReplyJoinRaidLonely(self, srcPlayerGbId, raidUUID, playerGBID, playerJoinProps, extraProps, applySource):
        """玩家申请(单人请求)通过后接受回调"""
        LOG_INFO('onJoinPlayerReplyJoinRaidLonely::', srcPlayerGbId, raidUUID, playerGBID, playerJoinProps, extraProps)
        inviteType = extraProps.get('inviteType', gameconst.InviteType.DEFAULT)
        needMsg = inviteType != gameconst.InviteType.GUILD
        _, err = self._onJoinPlayerReplyJoinRaidLonelyCheck(srcPlayerGbId, raidUUID, extraProps.get('raidTarget', 0), needMsg)
        if err != gameconst.RaidErrno.ENUM_RAID_OK:
            err = err.initkvbody(source=self._applyJoinRaidLonelyCheck.__name__)
            LOG_ERR('onJoinPlayerReplyJoinRaidLonely::, check failed, {}'.format(err))
        else:
            playerProps = self._getAvatarPropsForRaid().toStreamSavedDic()
            joinType = gameconst.TeamJoinType.DEFAULT
            if applySource == gameconst.ApplySource.RECRUIT:
                joinType = gameconst.TeamJoinType.RECRUIT
            elif applySource == gameconst.ApplySource.APPLY:
                joinType = gameconst.TeamJoinType.APPLY

            playerProps['joinType'] = joinType
            gameengine.getRaidStub(raidUUID).onReplyJoinRaidLonely(
                srcPlayerGbId, raidUUID, playerGBID, playerProps, extraProps)

        self.raidJoinRecord.pop(raidUUID)

        if err == gameconst.RaidErrno.ENUM_RAID_OK:
            self.cancelAllTeamRaidJoinRequest()
            return True
        return False

    def _onJoinPlayerReplyJoinRaidLonelyCheck(self, srcPlayerGbId, raidUUID, raidTarget, needMsg):
        LOG_INFO('_onJoinPlayerReplyJoinRaidLonelyCheck::', srcPlayerGbId, raidUUID, raidTarget, needMsg)
        _errno = gameconst.RaidErrno
        if self.inRaid():
            return None, _errno.ENUM_RAID_ALREADY_IN_RAID.initkvbody(raidUUID=raidUUID)
        if self.isInTeam(self.gbId):
            return None, _errno.ENUM_RAID_ALREADY_IN_TEAM.initkvbody(raidUUID=raidUUID)
        if raidTarget > gameconst.PARE_ACTIVITY_ID:
            if not self._isUIVisibleStrCell(dataUtils.getRaidConstDataValue("raidUIVisibleId"), False) \
                or not self._isUIVisibleStrCell(dataUtils.getRaidConstDataValue("raidDungeonUIVisibleId"), False):
                if needMsg:
                    gameengine.getGlobalBase('PlayerStub').doOnOthersBase([srcPlayerGbId], 'onMessagePre',
                        (TM_MCD.datas['teamInviteQuestMsg']['value'], [self.name]), None, '', ())
                    return None, gameconst.RaidErrno.ENUM_RAID_UI_DENIED.initkvbody(level=self.level)
        return None, _errno.ENUM_RAID_OK

    def onJoinPlayerHandleReplyJoinRaidReject(self, raidUUID):
        """玩家申请被拒绝后接受回调"""
        LOG_INFO('onJoinPlayerHandleReplyJoinRaidReject::', raidUUID)
        self.raidJoinRecord.pop(raidUUID, None)

    def onJoinPlayerHandleReplyJoinRaidAccept(self, raidUUID):
        """玩家申请同意后接受回调,"""
        LOG_INFO('onJoinPlayerHandleReplyJoinRaidAccept::', raidUUID)
        self.raidJoinRecord.pop(raidUUID, None)
        if self.isCaptain():
            self.cancelAllTeamRaidJoinRequest()

    @lockRaid(timeout=1)
    def onJoinPlayerReplyJoinRaidWithTeam(self, srcPlayerGbId, raidUUID, playerJoinProps, extraProps):
        """玩家申请(组队请求)通过后(所有小队)玩家接受回调"""
        LOG_INFO('onJoinPlayerReplyJoinRaidWithTeam', srcPlayerGbId, raidUUID, playerJoinProps, extraProps)
        _, err = self._onJoinPlayerReplyJoinRaidWithTeam(raidUUID, playerJoinProps['joinTeamUUID'])
        if err != gameconst.RaidErrno.ENUM_RAID_OK:
            err = err.initkvbody(source=self._onJoinPlayerReplyJoinRaidWithTeam.__name__)
            LOG_WARN('onJoinPlayerReplyJoinRaidWithTeam:: failed, {}'.format(err))
            # when playerProps `bool(playerProps) is False`, stub check will be quickly failed before timeout
            _playerProps = {}
        else:
            _playerProps = self._getAvatarPropsForRaid().toStreamSavedDic()
            
        extraProps.update({'memberCheckErrno': err})
        gameengine.getRaidStub(raidUUID).onReplyJoinRaidWithTeam(
            srcPlayerGbId, raidUUID, playerJoinProps['joinTeamUUID'], 
            self.gbId, _playerProps, extraProps)

        return False if err != gameconst.RaidErrno.ENUM_RAID_OK else True

    def _onJoinPlayerReplyJoinRaidWithTeam(self, raidUUID, teamUUID):
        _errno = gameconst.RaidErrno
        if self.inRaid():
            # 如果已经在团队中, 如果是小队队长, 则无法加入, 如果是普通成员, 则只要在当前团队中, 小队仍然可以加入
            if self.raidInfo.raidUUID != raidUUID or self.isCaptain():
                return None, _errno.ENUM_RAID_ALREADY_IN_RAID.initkvbody(raidUUID=raidUUID)
        if self.teamInfo.teamId != teamUUID:
            return None, _errno.ENUM_RAID_TEAM_NOT_FOUND.initkvbody(raidUUID=raidUUID)
        # if self.isCaptain() and raidUUID not in self.raidJoinRecord:
        #     return None, _errno.ENUM_RAID_APPLY_JOIN_RECORD_NOT_FOUND.initkvbody(raidUUID=raidUUID)
        return None, _errno.ENUM_RAID_OK

    def _cancelAllRaidJoinRequest(self):
        for _raidUUID, raidJoinType in self.raidJoinRecord.items():
            gameengine.getRaidStub(_raidUUID).cancelRaidJoinRequest(
                self.base, self.gbId, _raidUUID, raidJoinType, {})

    def onCancelRaidJoinRequestSucc(self, raidUUID, raidJoinType, extra):
        LOG_INFO("onCancelRaidJoinRequestSucc::", raidUUID, raidJoinType, extra)
        self.raidJoinRecord.pop(raidUUID, None)

    @gamedecorator.checkGameconfigEnable('raid')
    @utils.isMyself
    @raidPermissionCheck(needPermission=gameconst.RaidPermissionEnum.UNKNOWN)
    @gamedecorator.crossServer
    def tryApplyInviteRaid(self, exposed, gbId, playerName):
        """API: 尝试邀请玩家加入团队, 用于AOI外情况无法获取玩家组队信息"""
        LOG_INFO('tryApplyInviteRaid::~', gbId, playerName)

        self.base.doInviteCheck(gbId, gameconst.InviteType.DEFAULT, gameconst.TeamType.RAID, True)
        
    def doTryApplyInviteRaid(self, playerGBID, playerName, inviteType):
        LOG_INFO('doTryApplyInviteRaid::~', playerGBID, playerName, inviteType)
        _, err = self._tryApplyInviteRaidLonelyCommonCheck(playerGBID)
        if err != gameconst.RaidErrno.ENUM_RAID_OK:
            # GUILD 批量邀请不打印错误日志，不影响其他成员
            if inviteType != gameconst.InviteType.GUILD:
                LOG_WARN('doTryApplyInviteRaid:: common check failed, {}'.format(err))
            return

        extraProps = {
            'siegeWarCamp': self.siegeWarCamp,
            'srcPlayerGbId': self.gbId,
            'inviteType': inviteType,
        }
        needMsg = inviteType != gameconst.InviteType.GUILD
        if needMsg:
            gameengine.getGlobalBase('PlayerStub').doOnOthersCell(
                (playerGBID, ), 'tryBeInvitedInRaid', (self.base, extraProps),
                self, "tryApplyInviteRaidOffline", (playerName, ))
        else:
            gameengine.getGlobalBase('PlayerStub').doOnOthersCell(
                (playerGBID, ), 'tryBeInvitedInRaid', (self.base, extraProps),
                None, "", ())

    def _tryApplyInviteRaidLonelyCommonCheck(self, playerGBID):
        if not playerGBID:
            return None, gameconst.RaidErrno.ENUM_RAID_PARAM_ERR.initkvbody(playerGBID=playerGBID)
        if playerGBID == self.gbId:
            return None, gameconst.RaidErrno.ENUM_UNKNOWN.initkvbody(reason='self-invite')
        if self.isInTeam():
            return None, gameconst.RaidErrno.ENUM_RAID_ALREADY_IN_TEAM
        return None, gameconst.RaidErrno.ENUM_RAID_OK

    def tryBeInvitedInRaid(self, invitedPlayerBox, extraProps):
        LOG_INFO("tryBeInvitedInRaid::")
        srcPlayerGbId = extraProps['srcPlayerGbId']
        inviteType = extraProps['inviteType']
        needMsg = inviteType != gameconst.InviteType.GUILD
        _, err = self._tryBeInvitedInRaidCheck(srcPlayerGbId)
        if err != gameconst.RaidErrno.ENUM_RAID_OK:
            LOG_WARN("tryBeInvitedInRaid:: failed, {}".format(err))
            if err == gameconst.RaidErrno.ENUM_RAID_ALREADY_IN_RAID:
                if needMsg:
                    invitedPlayerBox.onMessagePre(R_RCD.datas["raidInviteFail_alreadyInRaid_msg"]["value"], [])
            return
        if gameconfig.isCrossServer():
            if self.siegeWarCamp != 0 and extraProps['siegeWarCamp'] != 0 and self.siegeWarCamp != extraProps['siegeWarCamp']:
                if needMsg:
                    invitedPlayerBox.onMessagePre(M_M_DD.datas.teamMatch_differentFactions, [])
                return

        invitedPlayerBox.client.onTryBeInvitedInRaid(self.gbId, self.teamId, self.name,
                                                     self.isCaptain(), inviteType)

    def _tryBeInvitedInRaidCheck(self, srcPlayerGbId):
        if self.inRaid():
            return None, gameconst.RaidErrno.ENUM_RAID_ALREADY_IN_RAID
        return None, gameconst.RaidErrno.ENUM_RAID_OK

    def tryApplyInviteRaidOffline(self, playerGBID, playerName):
        LOG_WARN("tryApplyInviteRaidOffline::", playerGBID, playerName)
        self.showMsg(M_M_DD.datas.raid_applicantOffline, [playerName])

    @gamedecorator.checkGameconfigEnable('raid')
    @utils.isMyself
    @raidPermissionCheck(needPermission=gameconst.RaidPermissionEnum.UNKNOWN)
    @gamedecorator.crossServer
    def applyInviteRaidLonely(self, exposed, playerGBID, playerName, inviteType):
        """API: 邀请单人加入团队"""
        LOG_INFO('applyInviteRaidLonely::~', playerGBID, playerName, inviteType)

        err = self.applyInviteRaidLonelyWithLonely(playerGBID, playerName, inviteType)
        if err == gameconst.RaidErrno.ENUM_RAID_OK:
            return

        _, err = self._applyInviteRaidLonelyCommonCheck(playerGBID)
        if err != gameconst.RaidErrno.ENUM_RAID_OK:
            LOG_WARN('applyInviteRaidLonely:: common check failed, {}'.format(err))
            return

        if self.isRaidLeader():
            self.raidLeaderApplyInvitedRaidLonely(playerGBID, playerName, inviteType)
        elif self.isRaidDeputy():
            self.raidDeputyApplyInvitedRaidLonely(playerGBID, playerName, inviteType)
        else:
            self.raidTeamMemberApplyInviteRaidLonely(playerGBID, playerName, inviteType)
        '''
        #
        elif self.isRaidCaptain():
            self.raidTeamCaptainApplyInviteRaidLonely(playerGBID, playerName)
        '''
    def applyInviteRaidLonelyWithLonely(self, playerGBID, playerName, inviteType):
        if self.inRaid():
            return gameconst.RaidErrno.ENUM_RAID_ALREADY_IN_RAID
        if self.isInTeam():
            return gameconst.RaidErrno.ENUM_RAID_ALREADY_IN_TEAM
        if not playerGBID or playerGBID == self.gbId:
            return gameconst.RaidErrno.ENUM_UNKNOWN

        extraProps = {}
        extraProps['inviteSource'] = gameconst.RaidPermissionEnum.LEADER
        extraProps['inviteType'] = inviteType
        needMsg = inviteType != gameconst.InviteType.GUILD
        if needMsg:
            gameengine.getGlobalBase('PlayerStub').doOnOthersCell((playerGBID,), 'invitedPlayerOnApplyInvitedRaid', (
                    0, 0, self.gbId, self.name, self.name, 0, 0, extraProps), self, 'tryApplyInviteRaidOffline', (playerName, ))
        else:
            gameengine.getGlobalBase('PlayerStub').doOnOthersCell((playerGBID,), 'invitedPlayerOnApplyInvitedRaid', (
                    0, 0, self.gbId, self.name, self.name, 0, 0, extraProps), None, '', ())
        return gameconst.RaidErrno.ENUM_RAID_OK
    
    def _applyInviteRaidLonelyCommonCheck(self, playerGBID):
        if not playerGBID:
            return None, gameconst.RaidErrno.ENUM_RAID_PARAM_ERR.initkvbody(playerGBID=playerGBID)
        if playerGBID == self.gbId:
            return None, gameconst.RaidErrno.ENUM_UNKNOWN.initkvbody(reason='self-invite')
        if not self.inRaid():
            return None, gameconst.RaidErrno.ENUM_RAID_NOT_IN_RAID
        return None, gameconst.RaidErrno.ENUM_RAID_OK

    def raidLeaderApplyInvitedRaidLonely(self, playerGBID, playerName, inviteType):
        """团长邀请单人加入团队"""
        LOG_INFO('raidLeaderApplyInvitedRaidLonely::', playerGBID, playerName, inviteType)
        raidUUID = self.raidUUID
        extraProps = {'inviteSource': gameconst.RaidPermissionEnum.LEADER}
        extraProps['inviteType'] = inviteType
        gameengine.getRaidStub(raidUUID).raidLeaderApplyInvitedRaid(
            self.base, self.gbId, raidUUID, playerGBID, playerName, extraProps)

    def raidDeputyApplyInvitedRaidLonely(self, playerGBID, playerName, inviteType):
        """副团长邀请单人加入团队"""
        LOG_INFO('raidDeputyApplyInvitedRaidLonely::', playerGBID, playerName, inviteType)
        raidUUID = self.raidUUID
        extraProps = {'inviteSource': gameconst.RaidPermissionEnum.DEPUTY}
        extraProps['inviteType'] = inviteType
        gameengine.getRaidStub(raidUUID).raidDeputyApplyInvitedRaid(
            self.base, self.gbId, raidUUID, playerGBID, playerName, extraProps)
    #
    def raidTeamCaptainApplyInviteRaidLonely(self, playerGBID, playerName):
        """队长邀请单人加入团队"""
        LOG_INFO('raidTeamCaptainApplyInviteRaidLonely::', playerGBID, playerName)
        _raidUUID = self.raidUUID
        raidTeamIDX = self.raidInfo.raidTeamIDX
        extraProps = {'raidTeamIDX': raidTeamIDX,
                      'inviteSource': gameconst.RaidPermissionEnum.CAPTAIN}
        gameengine.getRaidStub(_raidUUID).raidCaptainApplyInvitedRaid(
            self.base, self.gbId, _raidUUID, raidTeamIDX, playerGBID, playerName, extraProps)

    def raidTeamMemberApplyInviteRaidLonely(self, playerGBID, playerName, inviteType):
        """团队成员提议邀请单人加入团队"""
        LOG_INFO('raidTeamMemberApplyInviteRaidLonely::', playerGBID, playerName, inviteType)
        _raidUUID = self.raidUUID
        extraProps = {'inviteSource': gameconst.RaidPermissionEnum.MEMBER}
        extraProps['inviteType'] = inviteType
        gameengine.getRaidStub(_raidUUID).raidMemberApplyInvitedRaid(
            self.base, self.gbId, _raidUUID, playerGBID, playerName, extraProps)

    def invitedPlayerOnApplyInvitedRaid(self, raidUUID, raidTarget, srcPlayerGbId,
                                        srcPlayerName, leaderName, raidScore, raidLevel, extraProps):
        """邀请单人/组队加入团队流程成功后回调"""
        LOG_INFO('invitedPlayerOnApplyInvitedRaid::',
                 raidUUID, raidTarget, srcPlayerGbId, extraProps, 
                 srcPlayerName, leaderName, raidScore, raidLevel)

        _raidTeamIDX = extraProps.get('raidTeamIDX', 0)
        _teamUUID = extraProps.get('teamUUID', 0)
        inviteSource = extraProps.get('inviteSource', gameconst.RaidPermissionEnum.UNKNOWN)
        inviteType = extraProps.get('inviteType', gameconst.InviteType.DEFAULT)
        needMsg = inviteType != gameconst.InviteType.GUILD
        recordId, _err = self._invitedPlayerOnApplyInvitedRaid(
            raidUUID, _teamUUID, raidTarget, srcPlayerGbId, srcPlayerName, 
            leaderName, _raidTeamIDX, inviteSource, raidScore, raidLevel, inviteType)
        if _err != gameconst.RaidErrno.ENUM_RAID_OK:
            _err = _err.initkvbody(raidUUID=raidUUID, srcPlayerGbId=srcPlayerGbId)
            if _err == gameconst.RaidErrno.ENUM_RAID_UI_DENIED:
                LOG_WARN('invitedPlayerOnApplyInvitedRaid:: func is locked, errno={}'.format(_err))
                if needMsg:
                    gameengine.getGlobalBase('PlayerStub').doOnOthersBase([srcPlayerGbId], 'onMessagePre',
                    (TM_MCD.datas['teamInviteQuestMsg']['value'], [self.name]), None, '', ())
                
            elif _err == gameconst.RaidErrno.ENUM_RAID_NOT_TEAM_CAPTAIN:
                LOG_WARN('invitedPlayerOnApplyInvitedRaid:: not team captain, errno={}'.format(_err))
                if needMsg:
                    gameengine.getGlobalBase('PlayerStub').doOnOthersBase(
                        [srcPlayerGbId, ], 'onMessagePre',
                        (R_RCD.datas["raidInviteFail_alreadyInRaid_msg"]["value"], []),
                        None, '', ())

            elif _err == gameconst.RaidErrno.ENUM_RAID_ALREADY_IN_RAID:
                LOG_WARN('invitedPlayerOnApplyInvitedRaid:: player already in raid, errno={}'.format(_err))
                if needMsg:
                    gameengine.getGlobalBase('PlayerStub').doOnOthersBase(
                        [srcPlayerGbId, ], 'onMessagePre',
                        (R_RCD.datas["raidInviteFail_alreadyInRaid_msg"]["value"], []),
                        None, '', ())

            elif _err == gameconst.RaidErrno.ENUM_RAID_INVITED_SAME_PLAYER_INCD:
                LOG_WARN('invitedPlayerOnApplyInvitedRaid:: player which be invited in CD, errno={}'.format(_err))
                if needMsg:
                    gameengine.getGlobalBase('PlayerStub').doOnOthersBase(
                        [srcPlayerGbId, ], 'onMessagePre',
                        (R_RCD.datas["raid_inviteFail_cooldown_msg"]["value"], []),
                        None, '', ())
            elif _err == gameconst.RaidErrno.ENUM_RAID_UI_DENIED:
                LOG_WARN('invitedPlayerOnApplyInvitedRaid:: ui is denied, errno={}'.format(_err))
                if needMsg:
                    gameengine.getGlobalBase('PlayerStub').doOnOthersBase(
                        [srcPlayerGbId, ], 'onMessagePre',
                        (R_RCD.datas["raid_inviteFail_cooldown_msg"]["value"], []),
                        None, '', ())
            elif _err == gameconst.RaidErrno.ENUM_RAID_LEVEL_IS_ILLEGAL:
                LOG_WARN('invitedPlayerOnApplyInvitedRaid:: player level too low, errno={}'.format(_err))
                if needMsg:
                    gameengine.getGlobalBase('PlayerStub').doOnOthersBase([srcPlayerGbId], 'onMessagePre',
                        (int(TM_MCD.datas['teamInviteLevelMsg']['value']), [self.name]), None, '', ())
            elif _err == gameconst.RaidErrno.ENUM_RAID_SOCRE_IS_ILLEGAL:
                LOG_WARN('invitedPlayerOnApplyInvitedRaid:: player score too low, errno={}'.format(_err))
                if needMsg:
                    gameengine.getGlobalBase('PlayerStub').doOnOthersBase([srcPlayerGbId], 'onMessagePre',
                        (int(TM_MCD.datas['teamInviteScoreMsg']['value']), [self.name]), None, '', ())
            elif _err == gameconst.RaidErrno.ENUM_RAID_IN_CROSS_STATE:
                LOG_WARN('invitedPlayerOnApplyInvitedRaid:: player is in cross state, errno={}'.format(_err))
                if needMsg:
                    gameengine.getGlobalBase('PlayerStub').doOnOthersBase([srcPlayerGbId], 'onMessagePre',
                        (int(TM_MCD.datas['teamInviteMapMsg']['value']), []), None, '', ())
            elif _err == gameconst.RaidErrno.ENUM_RAID_ALREADY_IN_DUNGEON:
                LOG_WARN('invitedPlayerOnApplyInvitedRaid:: player is in dungeon state, errno={}'.format(_err))
                if needMsg:
                    gameengine.getGlobalBase('PlayerStub').doOnOthersBase([srcPlayerGbId], 'onMessagePre',
                    (TM_MCD.datas['team_inCopyScene']['value'], []), None, '', ())
            else:
                LOG_ERR('invitedPlayerOnApplyInvitedRaid:: failed, {}'.format(_err))

            return
        if needMsg:
            # 【【任务】发送团队邀请后弹出tip反馈】
            gameengine.getGlobalBase('PlayerStub').doOnOthersBase(
                [srcPlayerGbId, ], 'onMessagePre',
                (R_RCD.datas["raid_inviteSuccess_msg"]["value"], []), None, '', ())

        LOG_INFO('invitedPlayerOnApplyInvitedRaid:: set record', raidUUID, recordId)

    def _invitedPlayerOnApplyInvitedRaid(self, raidUUID, teamUUID, raidTarget, srcPlayerGbId, srcPlayerName, 
                                         leaderName, raidTeamIDX, inviteSource, raidScore, raidLevel, inviteType):
        if raidTarget > gameconst.PARE_ACTIVITY_ID:
            if not self._isUIVisibleStrCell(dataUtils.getRaidConstDataValue("raidUIVisibleId"), False) \
                or not self._isUIVisibleStrCell(dataUtils.getRaidConstDataValue("raidDungeonUIVisibleId"), False):
                return None, gameconst.RaidErrno.ENUM_RAID_UI_DENIED.initkvbody(level=self.level)
        if formula.inDungeonScene(self.spaceNo):
            return None, gameconst.RaidErrno.ENUM_RAID_ALREADY_IN_DUNGEON
        
        if self.inRaid():
            return None, gameconst.RaidErrno.ENUM_RAID_ALREADY_IN_RAID
        
        if self.isInTeam(self.gbId):
            return None, gameconst.RaidErrno.ENUM_RAID_ALREADY_IN_TEAM

        if self.level < raidLevel:
            return None, gameconst.RaidErrno.ENUM_RAID_LEVEL_IS_ILLEGAL
        
        if self.getTotalScore() < raidScore:
            return None, gameconst.RaidErrno.ENUM_RAID_SOCRE_IS_ILLEGAL
        
        # 我在跨服，告诉对方，不能邀请
        if self.isCrossServer:
            return None, gameconst.RaidErrno.ENUM_RAID_IN_CROSS_STATE
        
        if teamUUID:
            # 传入teamID代表邀请的是组队, 回调者应该是小队队长
            if self.teamInfo.teamId != teamUUID:
                return None, gameconst.RaidErrno.ENUM_RAID_TEAM_ID_CHANGED.initkvbody(
                    srcTeamUUID=teamUUID,
                    crtTeamUUID=self.teamInfo.teamId,
                )

            if not self.isCaptain():
                return None, gameconst.RaidErrno.ENUM_RAID_NOT_TEAM_CAPTAIN.initkvbody(teamUUID=teamUUID,
                                                                                  playerGBID=self.gbId)

        now = utils.curTS()
        recordId = KBEngine.genUUID64()
        if teamUUID:
            inviteType = gameconst.RaidJoinTypeEnum.TEAM 
        else:
            inviteType = gameconst.RaidJoinTypeEnum.SINGLE

        raidBeInvitedRecordDic = self.raidBeInvitedRecordDic
        thisRaidBeInvitedRecord = raidBeInvitedRecordDic.setdefault(raidUUID, {})
        for _, _recordVal in thisRaidBeInvitedRecord.items():
            if _recordVal['inviteT'] + R_RCD.datas["raidInviteCooldown"]["value"] > now:
                return None, gameconst.RaidErrno.ENUM_RAID_INVITED_SAME_PLAYER_INCD

        raidBeInvitedRecordDic[raidUUID][recordId] = {'srcPlayerGbId': srcPlayerGbId,
                                                   'raidTeamIDX': raidTeamIDX,
                                                   'teamUUID': teamUUID,
                                                   'inviteType': inviteType,
                                                   'inviteT': now}

        if inviteSource == gameconst.RaidPermissionEnum.LEADER:
            self.client.onBeInvitedRaidByLeader(raidUUID, raidTarget, recordId, teamUUID, srcPlayerGbId, srcPlayerName, leaderName, inviteType)
        elif inviteSource == gameconst.RaidPermissionEnum.MEMBER:
            self.client.onBeInvitedRaidByMember(raidUUID, raidTarget, recordId, teamUUID, srcPlayerGbId, srcPlayerName, leaderName, inviteType)
        else:
            LOG_WARN('_invitedPlayerOnApplyInvitedRaid:: invite source unknown', raidUUID, teamUUID, raidTarget, inviteSource)

        return recordId, gameconst.RaidErrno.ENUM_RAID_OK

    @gamedecorator.checkGameconfigEnable('raid')
    @utils.isMyself
    @raidPermissionCheck(needPermission=gameconst.RaidPermissionEnum.UNKNOWN, onlyMode=True)
    @gamedecorator.crossServer
    def replyInviteRaidLonely(self, exposed, raidUUID, recordID, srcPlayerGbId, beInvited, inviteType):
        """API: 某个玩家点击确认接受团队邀请"""
        LOG_INFO('replyInviteRaidLonely::', raidUUID, recordID, srcPlayerGbId, beInvited, inviteType)
        record, _err = self._replyInviteRaidLonelyCheck(raidUUID, recordID, srcPlayerGbId, beInvited)
        if _err != gameconst.RaidErrno.ENUM_RAID_OK:
            if _err == gameconst.RaidErrno.ENUM_RAID_AVATAR_REJECTED_ACT:
                LOG_INFO('replyInviteRaidLonely:: reject, {}'.format(_err))
                needMsg = inviteType != gameconst.InviteType.GUILD
                if needMsg:
                    gameengine.getGlobalBase('PlayerStub').doOnOthersClient(
                        [srcPlayerGbId, ], 'onMessage',
                        (R_RCD.datas['raidInvDeniedMsg']['value'], [self.name]),
                        None, '', ())
            else:
                LOG_WARN('replyInviteRaidLonely:: check failed, {}'.format(_err))
            # reply failed, pop current be invited record
            self.raidBeInvitedRecordDic.get(raidUUID, {}).pop(recordID, None)
            return

        # if reply succeed, pop all raidUUID be invited records
        self.raidBeInvitedRecordDic.clear()
        _playerProps = self._getAvatarPropsForRaid().toStreamSavedDic()
        extraProps = {}
        extraProps['inviteType'] = inviteType
        if raidUUID > 0:
            _playerProps['joinType'] = gameconst.TeamJoinType.RECRUIT
            gameengine.getRaidStub(raidUUID).replyInviteRaidLonely(
                self.base, self.gbId, _playerProps, record['srcPlayerGbId'],
                record['raidTeamIDX'], raidUUID, extraProps)
        else:
            gameengine.getGlobalBase('PlayerStub').doOnOthersCell([srcPlayerGbId], 'onReplyInviteRaidLonelyWithLonely', (
                self.base, self.gbId, _playerProps, extraProps), None, '', ())

    def _replyInviteRaidLonelyCheck(self, raidUUID, recordID, srcPlayerGbId, beInvited):
        if not beInvited:
            return None, gameconst.RaidErrno.ENUM_RAID_AVATAR_REJECTED_ACT.initkvbody(raidUUID=raidUUID)

        if self.inRaid():
            return None, gameconst.RaidErrno.ENUM_RAID_ALREADY_IN_RAID

        recordDic = self.raidBeInvitedRecordDic.get(raidUUID, {})
        if not recordDic or recordID not in recordDic:
            return None, gameconst.RaidErrno.ENUM_RAID_APPLY_BE_INVITED_RECORD_NOT_FOUND

        record = recordDic[recordID]
        if record['inviteType'] != gameconst.RaidJoinTypeEnum.SINGLE:
            return None, gameconst.RaidErrno.ENUM_RAID_JOIN_TYPE_NOT_MATCH

        if record['srcPlayerGbId'] != srcPlayerGbId:
            return None, gameconst.RaidErrno.ENUM_RAID_PLAYER_GBID_NOT_MATCH.initkvbody(
                raidUUID=raidUUID,
                srcPlayerGbId=srcPlayerGbId,
                rcdPlayerGBID=record['srcPlayerGbId'])

        return record, gameconst.RaidErrno.ENUM_RAID_OK

    def onReplyInviteRaidLonelyWithLonely(self, invitedPlayerBox, invitedPlayerGbId, invitedPlayerProps, extraProps):
        LOG_INFO('onReplyInviteRaidLonelyWithLonely::', invitedPlayerProps)
        inviteType = extraProps.get('inviteType', gameconst.InviteType.DEFAULT)
        _, err = self._createRaidLonelyCheck(dataUtils.getRaidConstDataValue('raidMemberLimit'))
        if err != gameconst.RaidErrno.ENUM_RAID_OK:
            LOG_WARN('onReplyInviteRaidLonelyWithLonely:: check failed, {}'.format(
                err.initkvbody(source=self._createRaidLonelyCheck.__name__)))
            if err == gameconst.RaidErrno.ENUM_RAID_ALREADY_IN_RAID:
                gameengine.getRaidStub(self.raidInfo.raidUUID).replyInviteRaidLonely(
                    invitedPlayerBox, invitedPlayerGbId, invitedPlayerProps, self.gbId,
                    0, self.raidInfo.raidUUID, extraProps)
            return

        raidUUID = KBEngine.genUUID64()
        leaderProps = self._getAvatarPropsForRaid().toStreamSavedDic()
        leaderProps['joinType'] = gameconst.TeamJoinType.CREATE
        gameengine.getRaidStub(raidUUID).createRaid(
            self.base, self.gbId, raidUUID, dataUtils.getRaidConstDataValue('raidMemberLimit'), [leaderProps], {})
        gameengine.getRaidStub(raidUUID).replyInviteRaidLonely(
                invitedPlayerBox, invitedPlayerGbId, invitedPlayerProps, self.gbId,
                0, raidUUID, extraProps)

    @gamedecorator.checkGameconfigEnable('raid')
    @utils.isMyself
    @raidPermissionCheck(needPermission=gameconst.RaidPermissionEnum.MEMBER, exclude=())
    @gamedecorator.crossServer
    def applyInviteRaidWithTeam(self, exposed, gbId, teamUUID, playerName):
        """API: 邀请小队加入团队"""
        LOG_INFO('applyInviteRaidWithTeam::', gbId, teamUUID, playerName)
        _, err = self._applyInviteRaidWithTeamCheck(gbId, teamUUID)
        if err != gameconst.RaidErrno.ENUM_RAID_OK:
            if err == gameconst.RaidErrno.ENUM_RAID_INVITE_SELF_TEAM:
                self.showMsg(R_RCD.datas["raidInviteFail_memberInviteTeam_msg"]["value"], [])
            elif err == gameconst.RaidErrno.ENUM_RAID_TEAM_MEMBER_DUOHUN:
                self.showMsg(R_RCD.datas["beifenglingwufazudui1"]["value"], [])
            LOG_WARN('applyInviteRaidWithTeam:: check failed, {}'.format(err))
            return

        if self.isRaidLeader():
            self.raidLeaderApplyInviteRaidWithTeam(gbId, teamUUID, playerName)
        elif self.isRaidDeputy():
            self.raidDeputyApplyInviteRaidWithTeam(gbId, teamUUID, playerName)
        else:
            self.raidTeamMemberApplyInviteRaidWithTeam(gbId, teamUUID, playerName)

    def _applyInviteRaidWithTeamCheck(self, gbId, teamUUID):
        if not (gbId and teamUUID):
            return None, gameconst.RaidErrno.ENUM_RAID_PARAM_ERR.initkvbody(
                playerGBID=gbId, teamUUID=teamUUID)

        if gbId == self.gbId:
            return None, gameconst.RaidErrno.ENUM_UNKNOWN.initkvbody(reason='self-invite')

        if not teamUUID or teamUUID == self.teamInfo.teamId:
            return None, gameconst.RaidErrno.ENUM_RAID_INVITE_SELF_TEAM

        if not self.inRaid():
            return None, gameconst.RaidErrno.ENUM_RAID_NOT_IN_RAID

        return None, gameconst.RaidErrno.ENUM_RAID_OK

    def raidLeaderApplyInviteRaidWithTeam(self, playerGBID, teamUUID, playerName):
        """团长邀请队伍加入团队"""
        LOG_INFO('raidLeaderApplyInviteRaidWithTeam::', playerGBID, teamUUID, playerName)
        raidUUID = self.raidUUID
        extraProps = {'teamUUID': teamUUID,
                      'inviteSource': gameconst.RaidPermissionEnum.LEADER}
        gameengine.getRaidStub(raidUUID).raidLeaderApplyInvitedRaid(
            self.base, self.gbId, raidUUID, playerGBID, playerName, extraProps)

    def raidDeputyApplyInviteRaidWithTeam(self, playerGBID, teamUUID, playerName):
        """副团长邀请队伍加入团队"""
        LOG_INFO('raidDeputyApplyInviteRaidWithTeam::', playerGBID, teamUUID, playerName)
        raidUUID = self.raidUUID
        extraProps = {'teamUUID': teamUUID,
                      'inviteSource': gameconst.RaidPermissionEnum.DEPUTY}
        gameengine.getRaidStub(raidUUID).raidDeputyApplyInvitedRaid(
            self.base, self.gbId, raidUUID, playerGBID, playerName, extraProps)

    def raidTeamMemberApplyInviteRaidWithTeam(self, gbId, teamUUID, playerName):
        """团队成员提议邀请队伍加入团队"""
        LOG_INFO('raidTeamMemberApplyInviteRaidWithTeam::', gbId, teamUUID, playerName)
        raidUUID = self.raidUUID
        extraProps = {'teamUUID': teamUUID,
                      'inviteSource': gameconst.RaidPermissionEnum.MEMBER}
        gameengine.getRaidStub(raidUUID).raidMemberApplyInvitedRaid(
            self.base, self.gbId, raidUUID, gbId, playerName, extraProps)

    @gamedecorator.checkGameconfigEnable('raid')
    @utils.isMyself
    @raidPermissionCheck(needPermission=gameconst.RaidPermissionEnum.UNKNOWN, onlyMode=True)
    @gamedecorator.crossServer
    def replyInviteRaidWithTeam(self, exposed, raidUUID, recordID, srcPlayerGbId, beInvited):
        """API: 某个小队(队长)点击确认接受团队邀请"""
        LOG_INFO('replyInviteRaidWithTeam::', raidUUID, recordID, srcPlayerGbId, beInvited)
        record, err = self._replyInviteRaidWithTeamCheck(raidUUID, recordID, srcPlayerGbId, beInvited)
        if err != gameconst.RaidErrno.ENUM_RAID_OK:
            if err == gameconst.RaidErrno.ENUM_RAID_AVATAR_REJECTED_ACT:
                LOG_INFO('replyInviteRaidWithTeam:: reject, {}'.format(err))
                gameengine.getGlobalBase('PlayerStub').doOnOthersClient(
                    [srcPlayerGbId, ], 'onMessage',
                    (R_RCD.datas['raidInvDeniedMsg']['value'], [self.name],),
                    None, '', ())
            elif err == gameconst.RaidErrno.ENUM_RAID_TEAM_MEMBER_OFFLINE:
                gameengine.getTeamStub(self.teamId).onReplyInviteRaidAndTeamFail(
                    self.base, self.gbId, 0, srcPlayerGbId, self.teamId, err.errno, {})
            elif err == gameconst.RaidErrno.ENUM_RAID_ALREADY_IN_RAID:
                gameengine.getGlobalBase('PlayerStub').doOnOthersBase(
                    [srcPlayerGbId, ], 'onMessagePre',
                    (M_M_DD.datas.raid_teamInvitationCheck_sectionTeam, []))

            LOG_WARN('replyInviteRaidWithTeam:: check failed, {}'.format(err))
            # reply failed, pop current be invited record
            self.raidBeInvitedRecordDic.get(raidUUID, {}).pop(recordID, None)
            return

        # if reply succeed, pop all raidUUID be invited records
        self.raidBeInvitedRecordDic.pop(raidUUID)
        teamUUID = record['teamUUID']
        teamMemberNum = len(self.teamInfo.teamPlayerDict)
        playerProps = self._getAvatarPropsForRaid().toStreamSavedDic()
        self._doReplyInviteRaidWithTeam(raidUUID, recordID, teamUUID, playerProps,
                                        teamMemberNum, srcPlayerGbId, isCaptain=True)
        self.teamInfo.allMembersCellDo('tryReplyInviteRaidFollowTeamCaptain',
                                       (raidUUID, recordID, teamUUID, teamMemberNum, srcPlayerGbId))

    def _replyInviteRaidWithTeamCheck(self, raidUUID, recordID, srcPlayerGbId, beInvited):
        if not beInvited:
            return None, gameconst.RaidErrno.ENUM_RAID_AVATAR_REJECTED_ACT.initkvbody(raidUUID=raidUUID)

        if not raidUUID:
            return None, gameconst.RaidErrno.ENUM_RAID_PARAM_ERR.initkvbody(raidUUID=raidUUID)

        if self.inRaid():
            return None, gameconst.RaidErrno.ENUM_RAID_ALREADY_IN_RAID

        recordDic = self.raidBeInvitedRecordDic.get(raidUUID, {})
        if not recordDic or recordID not in recordDic:
            return None, gameconst.RaidErrno.ENUM_RAID_APPLY_BE_INVITED_RECORD_NOT_FOUND

        record = recordDic[recordID]
        if record['teamUUID'] != self.teamInfo.teamId:
            return None, gameconst.RaidErrno.ENUM_RAID_TEAM_ID_CHANGED.initkvbody(srcTeamUUID=record['teamUUID'],
                                                                             crtTeamUUID=self.teamInfo.teamId)

        if record['inviteType'] != gameconst.RaidJoinTypeEnum.TEAM:
            return None, gameconst.RaidErrno.ENUM_RAID_JOIN_TYPE_NOT_MATCH

        if record['srcPlayerGbId'] != srcPlayerGbId:
            return None, gameconst.RaidErrno.ENUM_RAID_PLAYER_GBID_NOT_MATCH.initkvbody(
                raidUUID=raidUUID,
                srcPlayerGbId=srcPlayerGbId,
                rcdPlayerGBID=record['srcPlayerGbId'])

        if self.teamInfo.offlineMembers():
            return None, gameconst.RaidErrno.ENUM_RAID_TEAM_MEMBER_OFFLINE

        return record, gameconst.RaidErrno.ENUM_RAID_OK

    def _doReplyInviteRaidWithTeam(self, raidUUID, recordID, teamUUID, playerProps,
                                   teamMemberNum, srcPlayerGbId, isCaptain=False, extraProps=None):
        LOG_INFO('doReplyInviteRaidWithTeam::', raidUUID, recordID, teamUUID,
                 teamMemberNum, isCaptain, playerProps)
        if extraProps is None:
            extraProps = {}
        gameengine.getRaidStub(raidUUID).replyInviteRaidWithTeam(
            self.base, self.gbId, raidUUID, recordID, teamUUID, teamMemberNum,
            playerProps, isCaptain, srcPlayerGbId, extraProps)

    def tryReplyInviteRaidFollowTeamCaptain(self, raidUUID, recordID, teamUUID, teamMemberNum, srcPlayerGbId):
        """队长确认后需要所有小队队员再次检查一次条件后在RaidStub处汇总"""
        LOG_INFO('tryReplyInviteRaidFollowTeamCaptain', raidUUID, recordID, teamUUID, teamMemberNum)
        _, _err = self._tryReplyInviteRaidFollowTeamCaptain(raidUUID, teamUUID)
        if _err != gameconst.RaidErrno.ENUM_RAID_OK:
            LOG_WARN('tryReplyInviteRaidFollowTeamCaptain:: failed && to be ignored, {}'.format(_err))
            _playerProps = {}
            if _err == gameconst.RaidErrno.ENUM_RAID_ALREADY_IN_RAID:
                gameengine.getGlobalBase('PlayerStub').doOnOthersBase(
                    [srcPlayerGbId, ], 'onMessagePre',
                    (M_M_DD.datas.raid_teamInvitationCheck_sectionTeam, []),
                    None, "", ())

            if _err == gameconst.RaidErrno.ENUM_RAID_ALREADY_BE_TEAM_CAPTAIN:
                return

        else:
            _playerProps = self._getAvatarPropsForRaid().toStreamSavedDic()
        # always callback to raidStub
        self._doReplyInviteRaidWithTeam(raidUUID, recordID, teamUUID, _playerProps,
                                        teamMemberNum, srcPlayerGbId, isCaptain=False)

    def _tryReplyInviteRaidFollowTeamCaptain(self, raidUUID, teamUUID):
        if self.inRaid():
            # 如果已经在团队中, 如果是小队队长, 则无法加入, 如果是普通成员, 则只要在当前团队中, 小队仍然可以加入
            if self.raidInfo.raidUUID != raidUUID:
                return None, gameconst.RaidErrno.ENUM_RAID_ALREADY_IN_RAID.initkvbody(raidUUID=raidUUID)
            if self.isCaptain():
                return None, gameconst.RaidErrno.ENUM_RAID_ALREADY_BE_TEAM_CAPTAIN
        if self.teamInfo.teamId != teamUUID:
            return None, gameconst.RaidErrno.ENUM_RAID_TEAM_ID_CHANGED
        return None, gameconst.RaidErrno.ENUM_RAID_OK

    @gamedecorator.checkGameconfigEnable('raid')
    @utils.isMyself
    @raidPermissionCheck(needPermission=gameconst.RaidPermissionEnum.MEMBER)
    @gamedecorator.crossServer
    def leaveRaid(self, exposed):
        """API: 任意成员离开团队"""
        LOG_INFO('leaveRaid::~')
        _, err = self._leaveRaidCheck()
        if err != gameconst.RaidErrno.ENUM_RAID_OK:
            LOG_ERR('leaveRaid:: check failed, {}'.format(err))
            return
        
        _raidUUID = self.raidUUID
        extraProps = {}
        gameengine.getRaidStub(_raidUUID).leaveRaid(self.base, self.gbId, _raidUUID, extraProps)
            
        #主动离开team会清空怪物上的首刀归属者标记
        for e in self.entitiesInView(True):
            if e.IsMonster:
                e.clearFirstBlood(self.id)

    def _leaveRaidCheck(self):
        if not self.inRaid():
            return None, gameconst.RaidErrno.ENUM_RAID_NOT_IN_RAID
        return None, gameconst.RaidErrno.ENUM_RAID_OK

    def onLeaveRaid(self, raidUUID, extraProps):
        LOG_INFO('onLeaveRaid::', raidUUID, extraProps)
        if raidUUID != self.raidUUID:
            LOG_WARN('onLeaveRaid:: raidUUID not match, skip clear cache', raidUUID, self.raidUUID)
            return
        self._onLeaveRaid()

    def _onLeaveRaid(self):
        # 把自己cell的raid缓存清一遍
        self.raidInfo.reset()
        self.onRefreshPlayerRaidCacheVal(self.raidInfo)
        self.raidmateEntIdInAoiSet.clear()
        # 判断下是否在团队副本内
        if self.isInRaidDungeon():
            src = dungeonSrc.KickoutFromDungeon(kickReason=gameconst.DungeonSrcKickReason.FORCE)
            self.selfLeaveRaidDungeon(src)

    @gamedecorator.checkGameconfigEnable('raid')
    @utils.isMyself
    @raidPermissionCheck(needPermission=gameconst.RaidPermissionEnum.DEPUTY)
    @gamedecorator.crossServer
    def kickOutRaidMember(self, exposed, raidTeamIDX, playerGBID):
        """API: 团长/队长踢出玩家"""
        LOG_INFO('kickOutRaidMember::', raidTeamIDX, playerGBID)

        def _commonCheck():
            if not (raidTeamIDX and playerGBID):
                return None, gameconst.RaidErrno.ENUM_RAID_PARAM_ERR.initkvbody(raidTeamIDX=raidTeamIDX, playerGBID=playerGBID)
            if not self.inRaid():
                return None, gameconst.RaidErrno.ENUM_RAID_NOT_IN_RAID
            if playerGBID == self.gbId:
                return None, gameconst.RaidErrno.ENUM_RAID_KICKOUT_SELF
            return None, gameconst.RaidErrno.ENUM_RAID_OK

        _, err = _commonCheck()
        if err != gameconst.RaidErrno.ENUM_RAID_OK:
            LOG_WARN('kickOutRaidMember:: common-check failed, {}'.format(err))
            return

        if self.isRaidLeader():
            self._raidLeaderKickOutRaidMember(raidTeamIDX, playerGBID, {})
        elif self.isRaidDeputy():
            self._raidDeputyKickOutRaidMember(raidTeamIDX, playerGBID, {})

    def _raidLeaderKickOutRaidMember(self, raidTeamIDX, playerGBID, extraProps):
        LOG_INFO('_raidLeaderKickOutRaidMember::', raidTeamIDX, playerGBID)
        _raidUUID = self.raidUUID
        gameengine.getRaidStub(_raidUUID).raidLeaderKickOutRaidMember(
            self.base, self.gbId, _raidUUID, raidTeamIDX, playerGBID, extraProps)

    def _raidDeputyKickOutRaidMember(self, raidTeamIDX, playerGBID, extraProps):
        LOG_INFO('_raidDeputyKickOutRaidMember::', raidTeamIDX, playerGBID)
        _raidUUID = self.raidUUID
        gameengine.getRaidStub(_raidUUID).raidDeputyKickOutRaidMember(
            self.base, self.gbId, _raidUUID, raidTeamIDX, playerGBID, extraProps)
    #
    def _raidTeamCaptainKickOutRaidMember(self, raidTeamIDX, playerGBID, extraProps):
        LOG_INFO('_raidTeamCaptainKickOutRaidMember::', raidTeamIDX, playerGBID)
        _raidUUID = self.raidUUID
        gameengine.getRaidStub(_raidUUID).raidTeamCaptainKickOutRaidMember(
            self.base, self.gbId, _raidUUID, raidTeamIDX, playerGBID, extraProps)

    def onRaidLeaderKickOutRaidMember(self, raidUUID, koPlayerRaidTeamIDX, koPlayerGBID, extra):
        LOG_INFO('onRaidLeaderKickOutRaidMember::', raidUUID, koPlayerRaidTeamIDX, koPlayerGBID, extra)

    def onBeKickedOutRaidByRaidLeader(self, raidUUID, extraProps):
        LOG_INFO('onBeKickedOutRaidByRaidLeader::', raidUUID, extraProps)
        if raidUUID != self.raidUUID:
            LOG_WARN('onBeKickedOutRaidByRaidLeader:: '
                        'raidUUID not match, skip clear cache', raidUUID, self.raidUUID)
            return
        self._onLeaveRaid()

    def onRaidDeputyKickOutRaidMember(self, raidUUID, koPlayerRaidTeamIDX, koPlayerGBID, extra):
        LOG_INFO('onRaidDeputyKickOutRaidMember::', raidUUID, koPlayerRaidTeamIDX, koPlayerGBID, extra)

    def onBeKickedOutRaidByRaidDeputy(self, raidUUID, extraProps):
        LOG_INFO('onBeKickedOutRaidByRaidDeputy::', raidUUID, extraProps)
        if raidUUID != self.raidUUID:
            LOG_WARN('onBeKickedOutRaidByRaidDeputy:: '
                        'raidUUID not match, skip clear cache', raidUUID, self.raidUUID)
            return
        self._onLeaveRaid()
    #
    def onRaidCaptainKickOutRaidMember(self, raidUUID, koPlayerRaidTeamIDX, koPlayerGBID, extra):
        LOG_INFO('onRaidCaptainKickOutRaidMember::', raidUUID, koPlayerRaidTeamIDX, koPlayerGBID, extra)
    #
    def onBeKickedOutRaidByRaidTeamCaptain(self, raidUUID, extraProps):
        LOG_INFO('onBeKickedOutRaidByRaidTeamCaptain::', raidUUID, extraProps)
        if raidUUID != self.raidUUID:
            LOG_WARN('onBeKickedOutRaidByRaidTeamCaptain:: '
                        'raidUUID not match, skip clear cache', raidUUID, self.raidUUID)
            return
        self._onLeaveRaid()

    @gamedecorator.checkGameconfigEnable('raid')
    @utils.isMyself
    @raidPermissionCheck(needPermission=gameconst.RaidPermissionEnum.LEADER, onlyMode=True)
    @gamedecorator.crossServer
    def transferRaidLeader(self, exposed, toPlayerGBID):
        """API: 团长变更"""
        LOG_INFO('transferRaidLeader::', toPlayerGBID)
        _, err = self._transferRaidLeaderCheck(toPlayerGBID)
        if err != gameconst.RaidErrno.ENUM_RAID_OK:
            LOG_WARN('transferRaidLeader:: check failed, {}'.format(err))
            return

        extraProps = {}
        _raidUUID = self.raidUUID
        gameengine.getRaidStub(_raidUUID).transferRaidLeader(
            self.base, self.gbId, _raidUUID, toPlayerGBID, extraProps, True)

    def _transferRaidLeaderCheck(self, toPlayerGBID):
        if not toPlayerGBID:
            return None, gameconst.RaidErrno.ENUM_RAID_PARAM_ERR.initkvbody(toPlayerGBID=toPlayerGBID)
        if not self.inRaid():
            return None, gameconst.RaidErrno.ENUM_RAID_NOT_IN_RAID
        if not self.isRaidLeader():
            return None, gameconst.RaidErrno.ENUM_RAID_NOT_RAID_LEADER
        if toPlayerGBID == self.raidInfo.raidLeaderGBID:
            return None, gameconst.RaidErrno.ENUM_RAID_IS_SAME_PLAYER.initkvbody(toPlayerGBID=toPlayerGBID)
        return None, gameconst.RaidErrno.ENUM_RAID_OK

    @gamedecorator.checkGameconfigEnable('raid')
    @utils.isMyself
    @raidPermissionCheck(needPermission=gameconst.RaidPermissionEnum.LEADER, onlyMode=True)
    @gamedecorator.crossServer
    def transferRaidDeputy(self, exposed, toPlayerGBID):
        """API: 副团长变更"""
        LOG_INFO('transferRaidDeputy::', toPlayerGBID)
        _, err = self._transferRaidDeputyCheck(toPlayerGBID)
        if err != gameconst.RaidErrno.ENUM_RAID_OK:
            LOG_WARN('transferRaidDeputy:: check failed, {}'.format(err))
            return

        extraProps = {}
        raidUUID = self.raidUUID
        gameengine.getRaidStub(raidUUID).transferRaidDeputy(
            self.base, self.gbId, raidUUID, toPlayerGBID, extraProps, True, True)

    def _transferRaidDeputyCheck(self, toPlayerGBID):
        if not self.inRaid():
            return None, gameconst.RaidErrno.ENUM_RAID_NOT_IN_RAID
        if not self.isRaidLeader():
            return None, gameconst.RaidErrno.ENUM_RAID_NOT_RAID_LEADER
        if toPlayerGBID == self.raidInfo.raidDeputyGBID:
            return None, gameconst.RaidErrno.ENUM_RAID_IS_SAME_PLAYER.initkvbody(toPlayerGBID=toPlayerGBID)
        if toPlayerGBID == self.raidInfo.raidLeaderGBID:
            return None, gameconst.RaidErrno.ENUM_RAID_NOT_RAID_LEADER.initkvbody(toPlayerGBID=toPlayerGBID)
        return None, gameconst.RaidErrno.ENUM_RAID_OK
    
    @gamedecorator.checkGameconfigEnable('raid')
    @utils.isMyself
    @raidPermissionCheck(needPermission=gameconst.RaidPermissionEnum.CAPTAIN, onlyMode=True)
    @gamedecorator.crossServer
    def transferRaidTeamCaptain(self, exposed, toPlayerGBID):
        """API: 小队队长(除团长所在小队)更换相应队长"""
        LOG_INFO('transferRaidTeamCaptain::', toPlayerGBID)
        _, err = self._transferRaidTeamCaptainCheck(toPlayerGBID)
        if err != gameconst.RaidErrno.ENUM_RAID_OK:
            LOG_WARN('transferRaidTeamCaptain:: check failed, {}'.format(err))
            return

        _raidUUID = self.raidUUID
        gameengine.getRaidStub(_raidUUID).transferRaidTeamCaptain(
            self.base, self.gbId, _raidUUID, toPlayerGBID, {})
    #
    def _transferRaidTeamCaptainCheck(self, toPlayerGBID):
        if not toPlayerGBID:
            return None, gameconst.RaidErrno.ENUM_RAID_PARAM_ERR.initkvbody(toPlayerGBID=toPlayerGBID)
        if not self.inRaid():
            return None, gameconst.RaidErrno.ENUM_RAID_NOT_IN_RAID
        if self.isInRaidLeaderTeam():
            return None, gameconst.RaidErrno.ENUM_RAID_LEADER_TEAM_CANT_TRANS_CAPTAIN
        if not self.isRaidCaptain():
            return None, gameconst.RaidErrno.ENUM_RAID_NOT_TEAM_CAPTAIN
        return None, gameconst.RaidErrno.ENUM_RAID_OK

    def onTransferRaidLeaderAllMemberNotify(self, raidUUID, srcPlayerGbId, toPlayerGBID, toPlayerTeamIdx, extraProps):
        LOG_INFO('onTransferRaidLeaderAllMemberNotify::', raidUUID, srcPlayerGbId, toPlayerGBID, toPlayerTeamIdx, extraProps)
        _, err = self._onTransferRaidLeaderAllMemberNotify(raidUUID, srcPlayerGbId, toPlayerGBID, toPlayerTeamIdx)
        if err != gameconst.RaidErrno.ENUM_RAID_OK:
            LOG_WARN('onTransferRaidLeaderAllMemberNotify:: refresh cache failed, {}'.format(err))
            self.forceRefreshRaidCache()

    def _onTransferRaidLeaderAllMemberNotify(self, raidUUID, srcPlayerGbId, toPlayerGBID, toPlayerTeamIdx):
        if raidUUID != self.raidInfo.raidUUID:
            return None, gameconst.RaidErrno.ENUM_RAID_RAID_ID_NOT_FOUND

        if toPlayerTeamIdx not in self.raidInfo.raidTeamDic:
            return None, gameconst.RaidErrno.ENUM_RAID_TEAM_IDX_NOT_FOUND

        teamCacheVal = self.raidInfo.raidTeamDic[toPlayerTeamIdx]
        if toPlayerGBID not in teamCacheVal.teamPlayerDict:
            return None, gameconst.RaidErrno.ENUM_RAID_TEAM_MEMBER_NOT_MATCH

        # refresh team captain GBID
        # teamCacheVal.teamCaptainGBID = toPlayerGBID
        #if self.raidInfo.raidTeamIDX == toPlayerTeamIdx:
        #    # 相同小队刷新raidInfo上小队队长缓存
        #    self.raidInfo.raidCaptainGBID = toPlayerGBID
        # refresh raid leader GBID
        self.raidInfo.raidLeaderGBID = toPlayerGBID
        self.raidInfo.raidLeaderTeamIDX = toPlayerTeamIdx
        # 【【程序自主】团队中团员职务暴露给所有客户端】
        self.raidAuth = self.raidPermissionVal

        return None, gameconst.RaidErrno.ENUM_RAID_OK

    def onTransferRaidDeputyAllMemberNotify(self, raidUUID, srcPlayerGbId, toPlayerGBID, toPlayerTeamIdx, extraProps):
        LOG_INFO('onTransferRaidDeputyAllMemberNotify::', raidUUID, srcPlayerGbId, toPlayerGBID, toPlayerTeamIdx, extraProps)
        _, err = self._onTransferRaidDeputyAllMemberNotify(raidUUID, srcPlayerGbId, toPlayerGBID, toPlayerTeamIdx)
        if err != gameconst.RaidErrno.ENUM_RAID_OK:
            LOG_WARN('onTransferRaidDeputyAllMemberNotify:: refresh cache failed, {}'.format(err))
            self.forceRefreshRaidCache()

    def _onTransferRaidDeputyAllMemberNotify(self, raidUUID, srcPlayerGbId, toPlayerGBID, toPlayerTeamIdx):
        if raidUUID != self.raidInfo.raidUUID:
            return None, gameconst.RaidErrno.ENUM_RAID_RAID_ID_NOT_FOUND

        # refresh team captain GBID
        # teamCacheVal.teamCaptainGBID = toPlayerGBID
        #if self.raidInfo.raidTeamIDX == toPlayerTeamIdx:
        #    # 相同小队刷新raidInfo上小队队长缓存
        #    self.raidInfo.raidCaptainGBID = toPlayerGBID
        # refresh raid leader GBID
        self.raidInfo.raidDeputyGBID = toPlayerGBID
        self.raidInfo.raidDeputyTeamIDX = toPlayerTeamIdx
        # 【【程序自主】团队中团员职务暴露给所有客户端】
        self.raidAuth = self.raidPermissionVal

        return None, gameconst.RaidErrno.ENUM_RAID_OK
    #
    def onTransferRaidTeamCaptainAllMemberNotify(self, raidUUID, teamIDX, srcPlayerGbId, toPlayerGBID, extraProps):
        """转移队长成功后受到回调, 所有团队中玩家都收到该回调"""
        LOG_INFO('onTransferRaidTeamCaptainAllMemberNotify::', raidUUID, teamIDX, srcPlayerGbId, toPlayerGBID, extraProps)
        _, err = self._onTransferRaidTeamCaptainAllMemberNotify(raidUUID, teamIDX, srcPlayerGbId, toPlayerGBID)
        if err != gameconst.RaidErrno.ENUM_RAID_OK:
            LOG_WARN('onTransferRaidTeamCaptainAllMemberNotify:: refresh cache failed, {}'.format(err))
            self.forceRefreshRaidCache()
    #
    def _onTransferRaidTeamCaptainAllMemberNotify(self, raidUUID, teamIDX, srcPlayerGbId, toPlayerGBID):
        if raidUUID != self.raidInfo.raidUUID:
            return None, gameconst.RaidErrno.ENUM_RAID_RAID_ID_NOT_MATCH

        if teamIDX not in self.raidInfo.raidTeamDic:
            return None, gameconst.RaidErrno.ENUM_RAID_TEAM_IDX_NOT_FOUND

        teamCacheVal = self.raidInfo.raidTeamDic[teamIDX]
        if srcPlayerGbId not in teamCacheVal.teamPlayerDict or toPlayerGBID not in teamCacheVal.teamPlayerDict:
            return None, gameconst.RaidErrno.ENUM_RAID_TEAM_MEMBER_NOT_MATCH

        #变成团长
        if self.gbId == toPlayerGBID:
            if formula.inLineScene(self.spaceNo):
                _lineType = formula.fetchMapId(self.spaceNo)
                lineNo = formula.parseLineNo(self.spaceNo)
                gameengine.getLineStub(_lineType).updateLinePlayerInfo(
                    lineNo, self.base, self.gbId, {'changeTeam':(self.raidId, self.raidId, True)})
        elif self.gbId == srcPlayerGbId:
            if formula.inLineScene(self.spaceNo):
                _lineType = formula.fetchMapId(self.spaceNo)
                lineNo = formula.parseLineNo(self.spaceNo)
                gameengine.getLineStub(_lineType).updateLinePlayerInfo(
                    lineNo, self.base, self.gbId, {'changeTeam':(self.raidId, self.raidId, False)})

        teamCacheVal.teamCaptainGBID = toPlayerGBID
        if self.raidInfo.raidTeamIDX == teamIDX:
            # 相同小队刷新raidInfo上小队队长缓存
            self.raidInfo.raidCaptainGBID = toPlayerGBID
        # 【【程序自主】团队中团员职务暴露给所有客户端】
        self.raidAuth = self.raidPermissionVal

        return None, gameconst.RaidErrno.ENUM_RAID_OK
    #
    @gamedecorator.checkGameconfigEnable('raid')
    @utils.isMyself
    @raidPermissionCheck(needPermission=gameconst.RaidPermissionEnum.LEADER)
    def awardRaidTeamCaptain(self, expsoed, awardRaidTeamIDX, toPlayerGBID):
        """API: 团长任命队长"""
        LOG_INFO('awardRaidTeamCaptain::', awardRaidTeamIDX, toPlayerGBID)
        _, err = self._awardRaidTeamCaptainCheck(awardRaidTeamIDX, toPlayerGBID)
        if err != gameconst.RaidErrno.ENUM_RAID_OK:
            LOG_WARN('awardRaidTeamCaptain:: check failed, {}'.format(err))
            return

        _raidUUID = self.raidUUID
        gameengine.getRaidStub(_raidUUID).awardRaidTeamCaptain(
            self.base, self.gbId, _raidUUID, awardRaidTeamIDX, toPlayerGBID, {})
    #
    def _awardRaidTeamCaptainCheck(self, awardRaidTeamID, toPlayerGBID):
        if not (awardRaidTeamID and toPlayerGBID):
            return None, gameconst.RaidErrno.ENUM_RAID_PARAM_ERR.initkvbody(awardRaidTeamID=awardRaidTeamID, toPlayerGBID=toPlayerGBID)
        if not self.inRaid():
            return None, gameconst.RaidErrno.ENUM_RAID_NOT_IN_RAID
        if awardRaidTeamID not in self.raidInfo.raidTeamDic:
            return None, gameconst.RaidErrno.ENUM_RAID_TEAM_IDX_NOT_FOUND
        if awardRaidTeamID == self.raidInfo.raidLeaderTeamIDX:
            return None, gameconst.RaidErrno.ENUM_RAID_AWARD_SELF_TEAM
        return None, gameconst.RaidErrno.ENUM_RAID_OK
    #
    def onAwardRaidTeamCaptainAllMemberNotify(self, raidUUID, srcPlayerGbId, fromCaptainGBID,
                                              toRaidTeamIDX, toPlayerGBID, extra):
        """团长冲洗任命小队队长后所有玩家的回调"""
        LOG_INFO('onAwardRaidTeamCaptainAllMemberNotify::', raidUUID, srcPlayerGbId, fromCaptainGBID,
                 toRaidTeamIDX, toPlayerGBID, extra)
        _, err = self._onAwardRaidTeamCaptainAllMemberNotify(raidUUID, srcPlayerGbId, fromCaptainGBID,
                                                             toRaidTeamIDX, toPlayerGBID)
        if err != gameconst.RaidErrno.ENUM_RAID_OK:
            LOG_WARN('onAwardRaidTeamCaptainAllMemberNotify:: refresh cache failed, {}'.format(err))
            self.forceRefreshRaidCache()
    #
    def _onAwardRaidTeamCaptainAllMemberNotify(self, raidUUID, srcPlayerGbId, fromCaptainGBID,
                                               toRaidTeamIDX, toPlayerGBID):
        if raidUUID != self.raidInfo.raidUUID:
            return None, gameconst.RaidErrno.ENUM_RAID_RAID_ID_NOT_MATCH

        if toRaidTeamIDX not in self.raidInfo.raidTeamDic:
            return None, gameconst.RaidErrno.ENUM_RAID_TEAM_IDX_NOT_FOUND

        teamCacheVal = self.raidInfo.raidTeamDic[toRaidTeamIDX]
        teamPlayerDict = teamCacheVal.teamPlayerDict
        if fromCaptainGBID not in teamPlayerDict or toPlayerGBID not in teamPlayerDict:
            return None, gameconst.RaidErrno.ENUM_RAID_TEAM_MEMBER_NOT_MATCH

        teamCacheVal.teamCaptainGBID = toPlayerGBID
        if self.raidInfo.raidTeamIDX == toRaidTeamIDX:
            # 相同小队刷新raidInfo上小队队长缓存
            self.raidInfo.raidCaptainGBID = toPlayerGBID
        # 【【程序自主】团队中团员职务暴露给所有客户端】
        self.raidAuth = self.raidPermissionVal

        return None, gameconst.RaidErrno.ENUM_RAID_OK
    
    @gamedecorator.checkGameconfigEnable('raid')
    @utils.isMyself
    @raidPermissionCheck(needPermission=gameconst.RaidPermissionEnum.DEPUTY)
    @gamedecorator.crossServer
    def moveRaidTeamMember(self, exposed, fromPlayerTeamIdx, fromPlayerGBID, toPlayerTeamIdx, toPlayerGBID):
        """API: 团长移动队员"""
        LOG_INFO('moveRaidTeamMember::', fromPlayerTeamIdx, fromPlayerGBID, toPlayerTeamIdx, toPlayerGBID)
        _, err = self._moveRaidTeamMemberCheck(fromPlayerTeamIdx, fromPlayerGBID, toPlayerTeamIdx, toPlayerGBID)
        if err != gameconst.RaidErrno.ENUM_RAID_OK:
            LOG_WARN('moveRaidTeamMember, check failed, {}'.format(err))
            return

        # 团长移动自己,则走团长任命
        if self.isRaidLeader() and (fromPlayerGBID == self.gbId or toPlayerGBID == self.gbId):
            self.transferRaidLeader(exposed, toPlayerGBID if fromPlayerGBID == self.gbId else fromPlayerGBID)
            return
        # 其余都走移动团员
        raidUUID = self.raidUUID
        extraProps = {}
        gameengine.getRaidStub(raidUUID).moveRaidTeamMember(self.base, self.gbId, raidUUID,
                                                            fromPlayerTeamIdx, fromPlayerGBID,
                                                            toPlayerTeamIdx, toPlayerGBID, extraProps)

    def _moveRaidTeamMemberCheck(self, fromPlayerTeamIdx, fromPlayerGBID, toPlayerTeamIdx, toPlayerGBID):
        if not (fromPlayerTeamIdx and fromPlayerGBID and toPlayerTeamIdx):
            return None, gameconst.RaidErrno.ENUM_RAID_PARAM_ERR.initkvbody(fromPlayerTeamIdx=fromPlayerTeamIdx,
                                                                       fromPlayerGBID=fromPlayerGBID,
                                                                       toPlayerTeamIdx=toPlayerTeamIdx)

        if not self.inRaid():
            return None, gameconst.RaidErrno.ENUM_RAID_NOT_IN_RAID

        if not self.isRaidLeader() and not self.isRaidDeputy():
            return None, gameconst.RaidErrno.ENUM_RAID_NOT_RAID_LEADER_OR_DEPUTY

        if fromPlayerTeamIdx == toPlayerTeamIdx and not toPlayerGBID:
            return None, gameconst.RaidErrno.ENUM_RAID_IS_SAME_TEAM

        if fromPlayerGBID == toPlayerGBID:
            return None, gameconst.RaidErrno.ENUM_RAID_IS_SAME_PLAYER
        # 副团长不能移动团长
        if self.isRaidDeputy() and (fromPlayerGBID == self.raidInfo.raidLeaderGBID or toPlayerGBID == self.raidInfo.raidLeaderGBID):
            return None, gameconst.RaidErrno.ENUM_RAID_NOT_RAID_CANNOT_MOVE_LEADER

        return None, gameconst.RaidErrno.ENUM_RAID_OK

    def onMoveRaidTeamMemberSucc(self, srcPlayerGbId, raidUUID, fromPlayerTeamIdx,
                                 fromPlayerGBID, toPlayerTeamIdx, toPlayerGBID, extraProps):
        LOG_INFO('onMoveRaidTeamMemberSucc::', srcPlayerGbId, raidUUID, fromPlayerTeamIdx,
                 fromPlayerGBID, toPlayerTeamIdx, toPlayerTeamIdx, toPlayerGBID, extraProps)
        if self.gbId == fromPlayerGBID:
            LOG_INFO('onMoveRaidTeamMemberSucc:: A(org) --> B(*)')
        elif self.gbId == toPlayerGBID:
            LOG_INFO('onMoveRaidTeamMemberSucc:: A(*) <-- B(org)')
        elif self.gbId == srcPlayerGbId:
            LOG_INFO('onMoveRaidTeamMemberSucc:: src~')
        else:
            LOG_INFO('onMoveRaidTeamMemberSucc:: only refresh data~')

    @gamedecorator.checkGameconfigEnable('raid')
    @utils.isMyself
    @raidPermissionCheck(needPermission=gameconst.RaidPermissionEnum.LEADER)
    @gamedecorator.crossServer
    def setRaidTarget(self, exposed, minLevel, minScore, recuitInfo, password, isAutoExpedition):
        LOG_INFO("setRaidTarget, ", minLevel, minScore, recuitInfo, password, isAutoExpedition)
        """API: 团长设置全团目标"""
        if not self.inRaid():
            LOG_ERR("setRaidTarget, not in team")
            return
        if not self.isRaidLeader():
            LOG_ERR("setRaidTarget, not raid leader")
            return

        raidTarget = self.raidInfo.raidTarget
        raidTargetInfo = TMACTD.datas.get(raidTarget)
        if raidTargetInfo is None:
            LOG_ERR("setRaidTarget, misssing teamTarget", raidTarget)
            return

        if raidTarget > gameconst.PARE_ACTIVITY_ID:
            actData = AC_ADD.datas.get(int(raidTargetInfo['pareActivity']))
            if not actData or gameconst.ActivityControlType.RAID != int(actData['needTeam']):
                LOG_ERR("setRaidTarget, wrong activity control need team type", raidTarget, minLevel, minScore)
                return

        if not self.checkBaseTeamCond(raidTarget, minScore, minLevel):
            return
        
        gameengine.getRaidStub(self.raidUUID).setRaidTarget(self.base, self.gbId, self.raidUUID, raidTarget, minLevel, minScore, recuitInfo, password, isAutoExpedition)
        return

    def onSetRaidTargetAllMemberNotify(self, srcPlayerGbId, raidUUID, newTargetId, minLevel, minScore, recruitInfo, password, isAutoExpedition):
        """设置全团目标后全团回调"""
        LOG_INFO('onSetRaidTargetAllMemberNotify::', srcPlayerGbId, raidUUID, newTargetId, minLevel, minScore, recruitInfo, password, isAutoExpedition)

        def _check():
            if not self.inRaid():
                return None, gameconst.RaidErrno.ENUM_RAID_NOT_IN_RAID

            if self.raidInfo.raidUUID != raidUUID:
                return None, gameconst.RaidErrno.ENUM_RAID_RAID_ID_NOT_MATCH

            return None, gameconst.RaidErrno.ENUM_RAID_OK

        _, err = _check()
        if err != gameconst.RaidErrno.ENUM_RAID_OK:
            LOG_WARN('onSetRaidTargetAllMemberNotify:: failed, {}'.format(err))
            return

        self.raidInfo.raidTarget = newTargetId
        self.raidInfo.raidMinLevel = minLevel
        self.raidInfo.raidMinScore = minScore
        self.raidInfo.recruitInfo = recruitInfo
        self.raidInfo.password = password
        self.raidInfo.isAutoExpedition = isAutoExpedition

    @gamedecorator.checkGameconfigEnable('raid')
    @utils.isMyself
    @raidPermissionCheck(needPermission=gameconst.RaidPermissionEnum.DEPUTY)
    @gamedecorator.crossServer
    def startRaidStandbyChecker(self, exposed):
        """API: 团长发起全团检查"""
        LOG_INFO('startRaidStandbyChecker::~')

        # def _check():
        #     if not self.inRaid():
        #         return None, gameconst.RaidErrno.ENUM_RAID_NOT_IN_RAID
        #     if not self.isRaidLeader() and not self.isRaidDeputy():
        #         return None, gameconst.RaidErrno.ENUM_RAID_NOT_RAID_LEADER_OR_DEPUTY

        #     return None, gameconst.RaidErrno.ENUM_RAID_OK

        # _, err = _check()
        # if err != gameconst.RaidErrno.ENUM_RAID_OK:
        #     LOG_ERR('startRaidStandbyChecker:: failed, {}'.format(err))
        #     return

        # raidUUID = self.raidUUID
        # extraProps = {}
        # gameengine.getRaidStub(raidUUID).startRaidStandbyChecker(
        #     self.base, self.gbId, raidUUID, extraProps)

    @gamedecorator.checkGameconfigEnable('raid')
    @utils.isMyself
    @raidPermissionCheck(needPermission=gameconst.RaidPermissionEnum.MEMBER)
    @gamedecorator.crossServer
    def replyRaidStandbyChecker(self, exposed, raidUUID, beAgreed):
        """API: 团队成员回应团长检查"""
        LOG_INFO('replyRaidStandbyChecker::', raidUUID, beAgreed)

        # def _check():
        #     if not self.inRaid():
        #         return None, gameconst.RaidErrno.ENUM_RAID_NOT_IN_RAID
        #     if raidUUID != self.raidInfo.raidUUID:
        #         return None, gameconst.RaidErrno.ENUM_RAID_RAID_ID_NOT_MATCH
        #     return None, gameconst.RaidErrno.ENUM_RAID_OK

        # _, err = _check()
        # if err != gameconst.RaidErrno.ENUM_RAID_OK:
        #     LOG_ERR('replyRaidStandbyChecker:: failed, {}'.format(err))
        #     return

        # raidUUID = self.raidUUID
        # extraProps = {}
        # gameengine.getRaidStub(raidUUID).replyRaidStandbyChecker(
        #     self.base, self.gbId, raidUUID, beAgreed, extraProps)

    # --------------------------------------------------------------------
    # RAID MICS
    @gamedecorator.checkGameconfigEnable('raid')
    @gamedecorator.crossServer
    @utils.isMyself
    @raidPermissionCheck(needPermission=gameconst.RaidPermissionEnum.LEADER)
    def switchRaidMicsMode(self, exposed, mode):
        """API: 开启团队麦功能"""
        LOG_INFO("switchRaidMicsMode~")
        _, _err = self._switchRaidMicsModeCheck(mode)
        if _err != gameconst.RaidErrno.ENUM_RAID_OK:
            LOG_ERR("switchRaidMicsMode::failed, errno={}".format(_err))
            return

        self.base.switchRaidMicsModeBase(self.raidUUID, mode)

    def _switchRaidMicsModeCheck(self, mode):
        if not self.inRaid():
            return None, gameconst.RaidErrno.ENUM_RAID_NOT_IN_RAID

        if mode not in gameconst.RaidMicsModeEnum.COLL_ALL:
            return None, gameconst.RaidErrno.ENUM_RAID_MICS_MODE_ERR
        return None, gameconst.RaidErrno.ENUM_RAID_OK

    @gamedecorator.checkGameconfigEnable('raid')
    @gamedecorator.crossServer
    @utils.isMyself
    @raidPermissionCheck(needPermission=gameconst.RaidPermissionEnum.MEMBER)
    def turnOnRaidMics(self, exposed):
        """API: 团队成员打开麦克风"""
        LOG_INFO("turnOnRaidMics::~")
        _, err = self._turnOnRaidMicsCheck()
        if err != gameconst.RaidErrno.ENUM_RAID_OK:
            LOG_ERR("turnOnRaidMics::failed, errno={}".format(err))
            return

        self.base.turnOnRaidMicsBase(self.raidUUID)

    def _turnOnRaidMicsCheck(self):
        if not self.inRaid():
            return None, gameconst.RaidErrno.ENUM_RAID_NOT_IN_RAID
        return None, gameconst.RaidErrno.ENUM_RAID_OK

    def turnOffRaidMicsByForbidVoiceChat(self):
        LOG_INFO("turnOffRaidMicsByForbidVoiceChat ")
        _, err = self._turnOffRaidMicsCheck()
        if err != gameconst.RaidErrno.ENUM_RAID_OK:
            return
        _raidUUID = self.raidUUID
        gameengine.getRaidStub(_raidUUID).turnOffRaidMics(self.base, self.gbId, _raidUUID, self.gbId, {})

    @gamedecorator.checkGameconfigEnable('raid')
    @gamedecorator.crossServer
    @utils.isMyself
    @raidPermissionCheck(needPermission=gameconst.RaidPermissionEnum.MEMBER)
    def turnOffRaidMics(self, exposed):
        """API: 团队成员关闭麦克风"""
        LOG_INFO("turnOffRaidMics::~")
        _, err = self._turnOffRaidMicsCheck()
        if err != gameconst.RaidErrno.ENUM_RAID_OK:
            LOG_ERR("turnOffRaidMics::failed, errno={}".format(err))
            return

        _raidUUID = self.raidUUID
        extraProps = {}
        gameengine.getRaidStub(_raidUUID).turnOffRaidMics(
            self.base, self.gbId, _raidUUID, self.gbId, extraProps)

    def _turnOffRaidMicsCheck(self):
        if not self.inRaid():
            return None, gameconst.RaidErrno.ENUM_RAID_NOT_IN_RAID
        return None, gameconst.RaidErrno.ENUM_RAID_OK

    @gamedecorator.checkGameconfigEnable('raid')
    @utils.isMyself
    @raidPermissionCheck(needPermission=gameconst.RaidPermissionEnum.LEADER)
    @gamedecorator.crossServer
    def blockRaidMemberMics(self, exposed, teamIDX, playerGBID):
        """API: 团长禁言团员"""
        LOG_INFO("blockRaidMemberMics::~")
        _, err = self._blockRaidMemberMicsCheck(teamIDX, playerGBID)
        if err != gameconst.RaidErrno.ENUM_RAID_OK:
            LOG_ERR("blockRaidMemberMics::failed, errno={}".format(err))
            return

        _raidUUID = self.raidUUID
        extraProps = {}
        gameengine.getRaidStub(_raidUUID).blockRaidMemberMics(
            self.base, self.gbId, _raidUUID, teamIDX, playerGBID, extraProps)

    def _blockRaidMemberMicsCheck(self, teamIDX, playerGBID):
        if not self.inRaid():
            return None, gameconst.RaidErrno.ENUM_RAID_NOT_IN_RAID
        if not self.isRaidLeader():
            return None, gameconst.RaidErrno.ENUM_RAID_NOT_RAID_LEADER
        return None, gameconst.RaidErrno.ENUM_RAID_OK

    @gamedecorator.checkGameconfigEnable('raid')
    @utils.isMyself
    @raidPermissionCheck(needPermission=gameconst.RaidPermissionEnum.LEADER)
    @gamedecorator.crossServer
    def unblockRaidMemberMics(self, exposed, teamIDX, playerGBID):
        """API: 团长解除团员禁言"""
        LOG_INFO("unblockRaidMemberMics::~")
        _, err = self._unblockRaidMemberMicsCheck(teamIDX, playerGBID)
        if err != gameconst.RaidErrno.ENUM_RAID_OK:
            LOG_ERR("unblockRaidMemberMics::failed, errno={}".format(err))
            return

        _raidUUID = self.raidUUID
        extraProps = {}
        gameengine.getRaidStub(_raidUUID).unblockRaidMemberMics(
            self.base, self.gbId, _raidUUID, teamIDX, playerGBID, extraProps)

    def _unblockRaidMemberMicsCheck(self, teamIDX, playerGBID):
        if not self.inRaid():
            return None, gameconst.RaidErrno.ENUM_RAID_NOT_IN_RAID
        if not self.isRaidLeader():
            return None, gameconst.RaidErrno.ENUM_RAID_NOT_RAID_LEADER
        return None, gameconst.RaidErrno.ENUM_RAID_OK

    # --------------------------------------------------------------------

    # --------------------------------------------------------------------
    # RAID FOLLOW
    def becomeRaidLeader(self):
        pass

    def loseRaidLeader(self):
        pass
    # --------------------------------------------------------------------

    ############################### 团队活动 洞府之争 start ##########################################################
    def raidReqEnterDongfuDungeon(self, enterType, create=False):
        LOG_INFO('in raidReqEnterDongfuDungeon:', enterType, self.raidUUID)
        if not self.raidUUID:
            LOG_WARN('   in raidReqEnterDongfuDungeon, no raidUUID')
            self.showMsg(M_M_DD.datas.dfzz_enterWithRaid, [])
            return

        if create and not self.raidInfo.isRaidLeader(self.gbId):
            self.showMsg(M_M_DD.datas.dfzz_open_notRaidLeader, [])
            LOG_WARN('   in raidReqEnterDongfuDungeon, no permition')
            return

        _raidPlayers = self.raidInfo.getAllPlayerGBIDList()
        self.base.baseEnterDongfuDungeon(enterType, self.raidUUID, _raidPlayers, create)

    def raidCloseDongfuDungeon(self, confirmClose):
        LOG_INFO('in raidCloseDongfuDungeon:', self.raidUUID, confirmClose)
        if not self.raidUUID:
            LOG_WARN('   in raidCloseDongfuDungeon')
            self.showMsg(M_M_DD.datas.dfzz_enterWithRaid, [])
            return

        if not self.raidInfo.isRaidLeader(self.gbId):
            self.showMsg(M_M_DD.datas.dfzz_open_notRaidLeader, [])
            LOG_WARN('   in raidCloseDongfuDungeon, no permition')
            return
        self.base.baseCloseDongfuWarDungeon(self.raidUUID, confirmClose)

    ############################### 团队活动 洞府之争 end ##########################################################

    # --------------------------------------------------------------------
    @gamedecorator.checkGameconfigEnable('raid')
    @utils.isMyself
    @raidPermissionCheck(needPermission=gameconst.RaidPermissionEnum.UNKNOWN, onlyMode=True)
    @gamedecorator.crossServer
    def reqRaidPlayerAutoMatch(self, exposed, target):
        LOG_INFO('in reqRaidPlayerAutoMatch')
        if not self._isUIVisibleStrCell(dataUtils.getRaidConstDataValue("raidUIVisibleId"), True) \
            or not self._isUIVisibleStrCell(dataUtils.getRaidConstDataValue("raidDungeonUIVisibleId"), True):
            LOG_WARN("reqRaidPlayerAutoMatch, func is locked")
            return
        if target == 0 or target == 1:
            LOG_WARN("reqRaidPlayerAutoMatch target error", target)
            return

        if self.isInTeam(self.gbId):
            LOG_WARN('reqRaidPlayerAutoMatch, already in a team:', self.teamId)
            return

        if self.inRaid():
            LOG_WARN('reqRaidPlayerAutoMatch, already in a raid:', self.raidUUID)
            return

        raidTargetInfo = TMACTD.datas.get(target)
        if raidTargetInfo is None:
            LOG_ERR("reqRaidPlayerAutoMatch, misssing teamTarget", target)
            return

        actData = AC_ADD.datas.get(int(raidTargetInfo['pareActivity']))
        if not actData or gameconst.ActivityControlType.RAID != int(actData['needTeam']):
            LOG_ERR("reqRaidPlayerAutoMatch, wrong activity control need team type", target)
            return

        if not self.isReachTeamMinCond(target):
            LOG_WARN('   in reqRaidPlayerAutoMatch, cond failed:', self.getTotalScore(), self.level)
            return

        # 取消队伍匹配
        self.stopTeamMatch()

        # 取消团队匹配
        self.stopRaidMatch()

        _playerMatchDic = {
            'playerGbId': self.gbId,
            'target' : target,
            'playerName': self.name,
            'playerBox': self.base,
            'school': self.school,
            'level': self.level,
            'picFrameId': self.appearance.outfitData.picFrameId,
            'sex': self.sex,
            'bOnline': True,
            'spaceNo': self.spaceNo,
            'position': self.position,
            'hp': self.hp,
            'fullHp': self.fullHp,
            'score': self.getTotalScore(),
            'mountState': 0,
            'raidUUID': self.raidUUID,
            'enableMics': True,
            'isBlockMics': False,
            'isDead': False,
            'openId': "openId",
        }
        gameengine.getGlobalBase('RaidMatchStub').raidPlayerAutoMatch(_playerMatchDic)

    @gamedecorator.checkGameconfigEnable('raid')
    @utils.isMyself
    @gamedecorator.crossServer
    def reqRaidPlayerStopAutoMatch(self, exposed):
        LOG_INFO('reqRaidPlayerStopAutoMatch::~')
        self.stopRaidMatch()

    def stopRaidMatch(self):
        if self.autoRaidMatchStartTime > 0:
            LOG_INFO('in stopRaidMatch')
            self.autoRaidMatchStartTime = 0
            self.autoRaidMatchTarget = 0
            gameengine.getGlobalBase('RaidMatchStub').raidPlayerStopAutoMatch(self.gbId)

    @gamedecorator.checkGameconfigEnable('raid')
    @utils.isMyself
    @raidPermissionCheck(needPermission=gameconst.RaidPermissionEnum.LEADER, onlyMode=True)
    @gamedecorator.crossServer
    def reqRaidAutoMatch(self, exposed):
        LOG_INFO('in reqRaidAutoMatch')
        if 0 == self.raidUUID:
            LOG_WARN('   in reqRaidAutoMatch, not has a raid, self.raidUUID:', self.raidUUID)
            return
        if not self.isRaidLeader():
            LOG_WARN('   in reqRaidAutoMatch, not raid leader')
            return

        gameengine.getRaidStub(self.raidUUID).raidPrepareAutoMatch(self.raidUUID)

    @gamedecorator.checkGameconfigEnable('raid')
    @utils.isMyself
    @raidPermissionCheck(needPermission=gameconst.RaidPermissionEnum.LEADER, onlyMode=True)
    @gamedecorator.crossServer
    def reqRaidStopAutoMatch(self, exposed):
        LOG_INFO('in reqRaidStopAutoMatch')
        if 0 == self.raidUUID:
            LOG_WARN('   in reqRaidStopAutoMatch, not has a raid, self.raidUUID:', self.raidUUID)
            return
        if not self.isRaidLeader():
            LOG_WARN('   in reqRaidStopAutoMatch, not raid leader')
            return

        gameengine.getRaidStub(self.raidUUID).raidPrepareStopAutoMatch(self.raidUUID)

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
        self.showMsg(TM_MCD.datas['leaveMatch_timeOverMsg']['value'], [])
        return

    @gamedecorator.checkGameconfigEnable('raid')
    @utils.isMyself
    @gamedecorator.crossServer
    def reqGetRaidList(self, exposed, lastTime, raidTarget):
        teamTargetInfo = TMACTD.datas.get(raidTarget)
        if teamTargetInfo is None:
            LOG_ERR("reqGetRaidList, misssing raidTarget", raidTarget)
            return

        if raidTarget == 0 or raidTarget > gameconst.PARE_ACTIVITY_ID:
            actData = AC_ADD.datas.get(int(teamTargetInfo['pareActivity']))
            if not actData or gameconst.ActivityControlType.RAID != int(actData['needTeam']):
                LOG_ERR("reqGetRaidList, wrong activity control need team type", raidTarget)
                return

        recordsDic = self.getTempMiscProp(gameconst.EntityPropsEnum.getRaidListRecordData)
        if not recordsDic:
            recordsDic = {}
            self.setTempMiscProp(gameconst.EntityPropsEnum.getRaidListRecordData, recordsDic)

        if raidTarget not in recordsDic:
            recordsDic.setdefault(raidTarget, [0, 0])

        now = utils.curTS()
        lastGetTime = recordsDic[raidTarget][1]
        if lastGetTime+1 >= now:
            LOG_WARN('Frequently call reqGetRaidList, raidTarget:', raidTarget, recordsDic)
            return
        recordsDic[raidTarget][1] = now

        lastTeamStubIndex = recordsDic[raidTarget][0]
        checkTime = utils.curTS()
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
        recordsDic = self.getTempMiscProp(gameconst.EntityPropsEnum.getRaidListRecordData)
        recordsDic[teamTarget][0] = lastTeamStubIndex

    def onPlayerMatchedRaid(self, raidUUID):
        if self.raidUUID > 0:
            LOG_WARN('in onPlayerMatchedRaid, already join a raid:', self.raidUUID)
            return
        gameengine.getRaidStub(raidUUID).newRaidPlayerMatched(raidUUID, self._getAvatarPropsForRaid().toStreamSavedDic())
        return

    def leaveRaidAuto(self):
        LOG_INFO("leaveRaidAuto~")
        if self.autoRaidMatchStartTime > 0:
            self.autoRaidMatchStartTime = 0
            self.autoRaidMatchTarget = 0
            gameengine.getGlobalBase('RaidMatchStub').raidPlayerStopAutoMatch(self.gbId)

        if self.raidUUID > 0 and self.isRaidLeader():
            gameengine.getRaidStub(self.raidUUID).raidPrepareStopAutoMatch(self.raidUUID)

        if self.inRaid():
            _raidUUID = self.raidUUID
            extraProps = {}
            gameengine.getRaidStub(_raidUUID).leaveRaid(self.base, self.gbId, _raidUUID, extraProps)

    # 标记 begin
    @gamedecorator.checkGameconfigEnable('raid')
    @utils.isMyself
    @gamedecorator.crossServer
    def reqAddRaidMarkMember(self, exposed, type, index, name, gbId, entId, pos):
        """ API: 加入raid标记 """
        LOG_INFO('reqAddRaidMarkMember: ', type, index, name, gbId, entId, pos)

        # 检查
        if index <= 0 or index > gameconst.TEAM_MARK_MAX_SLOT or self.raidUUID <= 0:
            return

        ent = KBEngine.entities.get(entId)
        gameengine.getRaidStub(self.raidUUID).reqAddRaidMarkMember(self.raidUUID, self.base, type, index, name, gbId, entId, pos, ent)

    @gamedecorator.checkGameconfigEnable('raid')
    @utils.isMyself
    @gamedecorator.crossServer
    def reqDelRaidMarkMember(self, exposed, type, index):
        """ API: 移除raid标记 """
        LOG_INFO('reqDelRaidMarkMember: ', self.raidUUID, type, index)

        # 检查
        if index <= 0 or index > gameconst.TEAM_MARK_MAX_SLOT or self.raidUUID <= 0:
            return

        gameengine.getRaidStub(self.raidUUID).reqDelRaidMarkMember(self.raidUUID, self.base, type, index)

    @gamedecorator.checkGameconfigEnable('raid')
    @utils.isMyself
    @gamedecorator.limitcall(2)
    @gamedecorator.crossServer
    def reqChangeRaidOnlyLeader(self, exposed, state):
        """ API: 变更仅leader修改标记的状态 """
        LOG_INFO('reqChangeRaidOnlyLeader: ', state)

        # 检查
        if not self.isRaidLeader():
            LOG_INFO('reqChangeRaidOnlyLeader: not leader')
            return

        gameengine.getRaidStub(self.raidUUID).reqChangeRaidOnlyLeader(self.raidUUID, self.base, state)

    @gamedecorator.checkGameconfigEnable('raid')
    @utils.isMyself
    @gamedecorator.limitcall(2)
    @gamedecorator.crossServer
    @raidPermissionCheck(needPermission=gameconst.RaidPermissionEnum.UNKNOWN, onlyMode=True)
    def reqJoinRaid(self, exposed, raidUUID, password):
        LOG_INFO('reqJoinRaid::', raidUUID, password)
        _, err = self._onJoinRaidCheck(raidUUID)
        if err != gameconst.RaidErrno.ENUM_RAID_OK:
            LOG_ERR('onJoinPlayerReplyJoinRaidLonely::, check failed, {}'.format(err))
        else:
            playerProps = self._getAvatarPropsForRaid().toStreamSavedDic()
            gameengine.getRaidStub(raidUUID).reqJoinRaid(self.base, raidUUID, password, playerProps)

    def _onJoinRaidCheck(self):
        _errno = gameconst.RaidErrno
        if self.inRaid():
            return _errno.ENUM_RAID_ALREADY_IN_RAID.initkvbody(source='_onJoinRaidCheck')
        if self.isInTeam(self.gbId):
            return _errno.ENUM_RAID_ALREADY_IN_TEAM.initkvbody(source='_onJoinRaidCheck')

        return _errno.ENUM_RAID_OK

    def onRaidAddNewMember(self, entId):
        # LOG_INFO('onRaidMember:: add', self.id, entId)
        if self.id == entId:
            return
        raidMember = KBEngine.entities.get(entId)
        if raidMember and raidMember in self.entitiesInView(True):
            self.raidmateEntIdInAoiSet.add(entId)
            raidMember.raidmateEntIdInAoiSet.add(self.id)

    def onRaidRemoveMember(self, entId):
        # LOG_INFO('onRaidMember:: remove', self.id, entId)
        if self.id == entId:
            return
        if entId in self.raidmateEntIdInAoiSet:
            self.raidmateEntIdInAoiSet.discard(entId)

    def getAllRaidMemberGbIdSet(self):
        if not self.inRaid():
            return set()
        _set = set()
        for teamIDX, memberGBID, memberVal in self.raidInfo.iterGetRaidMember():
            _set.add(memberGBID)
        return _set

    @utils.isMyself
    @gamedecorator.crossServer
    def tryApplyInviteGuild(self, exposed, inviteType, teamType):
        LOG_INFO('impRaid::tryApplyInviteGuild,', exposed, inviteType, teamType)
        if inviteType not in gameconst.InviteType.VALID_TYPES:
            LOG_ERR("impRaid::tryApplyInviteGuild, wrong invite type ", inviteType)
            return
        if teamType not in gameconst.TeamType.VALID_TYPES:
            LOG_ERR("impRaid::tryApplyInviteGuild, wrong team type ", teamType)
            return
        if teamType == gameconst.TeamType.TEAM:
            ret = gamedecorator.doCheckGameConfig(self, 'raid', False)
            if not ret:
                LOG_ERR("impRaid::tryApplyInviteGuild, raid is not open ", teamType)
                return  
        elif teamType == gameconst.TeamType.RAID:
            ret = gamedecorator.doCheckGameConfig(self, 'team', False)
            if not ret:
                LOG_ERR("impRaid::tryApplyInviteGuild, team is not open ", teamType)
                return
        else:
            return
        
        if inviteType == gameconst.InviteType.GUILD:
            if not self.guildUUID:
                LOG_WARN("impRaid::tryApplyInviteGuild not in guild 1")
                return
            if not self.guildBoxCell:
                LOG_WARN("impRaid::tryApplyInviteGuild not in guild 2")
                return
            self.guildBoxCell.tryApplyInviteGuild(self.gbId, inviteType, teamType)
