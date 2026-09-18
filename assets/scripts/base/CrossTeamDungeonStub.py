# coding: utf-8
import KBEngine
from KBEDebug import *

import gameengine
import gameconst
import gametimer
import gameglobal

import iDungeonStub
import iDungeonStubMonster

import gameconfig
import userType
import dungeon
import team
import dungeonSrc

import DungeonSettlement

import formula
import utils

import gamePlay_gamePlay as DDI


class _Record(userType.UserSingleType):
    """团队线副本创建锁记录（照抄自 RaidDungeonStub，新类自包含，不从旧类 import）"""
    def __init__(self, raidUUID, playerGBID):
        self.raidUUID = raidUUID
        self.timerId = 0
        self.playerGBID = playerGBID


class RaidDungeonCreatingMixin(object):
    """团队线副本创建锁（照抄自 RaidDungeonStub；旧类终态删除后本文件为唯一实现）"""

    def __init__(self):
        self.creatingRaidDict = {}

    def checkRaidDungeonCreating(self, raidUUID):
        return raidUUID in self.creatingRaidDict

    def addRaidDungeonCreatingRecord(self, raidUUID, playerGBID, timeout=3):
        if raidUUID in self.creatingRaidDict:
            LOG_WARN('addRaidDungeonCreatingRecord:: overwrite creating record',
                        raidUUID, self.creatingRaidDict[playerGBID], playerGBID)
        self.creatingRaidDict[raidUUID] = _Record(raidUUID, playerGBID)
        if timeout:
            self.asyncCallbackAfter(3)._releaseRaidDungeonCreatingLockTimeout(raidUUID)

    def _releaseRaidDungeonCreatingLockTimeout(self, raidUUID):
        LOG_WARN('_rmRaidDungeonCreatingRecordTimeout:: timeout rm timerId', raidUUID)
        self.releaseRaidDungeonCreatingLock(raidUUID)

    def popRaidDungeonCreatingRecord(self, raidUUID, default=None):
        return self.creatingRaidDict.pop(raidUUID, default)

    def getRaidDungeonCreatingLock(self, raidUUID, playerGBID, timeout=3):
        """获得raidCreating锁"""
        LOG_INFO('lockRaidCreating::', raidUUID, playerGBID, timeout)
        if self.checkRaidDungeonCreating(raidUUID):
            return 0
        self.addRaidDungeonCreatingRecord(raidUUID, playerGBID)
        return raidUUID

    def releaseRaidDungeonCreatingLock(self, raidUUID):
        """释放raidCreating锁"""
        LOG_INFO('unlockRaidCreating::', raidUUID)
        self.popRaidDungeonCreatingRecord(raidUUID, None)


class CrossTeamDungeonStub(iDungeonStub.IDungeonStub, iDungeonStubMonster.IDungeonStubMonster, RaidDungeonCreatingMixin):
    """跨服组队副本 Stub：完整承接 TeamDungeonStub（小队线）与 RaidDungeonStub（团队线）的职责并集。

    实例按创建 props 传入的 dungeonEnterType（TEAM=2/RAID=4，gameconst.DungeonEnterTypeEnum）
    确定线别，内部按线分支：本服 TeamStub/RaidStub 联动分支与跨服组队分支（认
    SpaceVal.isCrossDungeon：跨服服空间 playMode 为 CROSS_CRUSADE/CROSS_CHIEF，本服模式空间
    playMode 落本服 CRUSADE/CHIEF、以 crossTeamId 识别）均从旧两文件原样搬入；
    两线差异（销毁流/检查流/SpaceVal/创建锁）本期不做统一，
    按线分支各自保留。以与旧 stub 相同的全局名（dungeon_<no>_t / dungeon_<no>_r）注册。
    """

    def __init__(self):
        LOG_INFO('CrossTeamDungeonStub::__init__')
        iDungeonStub.IDungeonStub.__init__(self)
        RaidDungeonCreatingMixin.__init__(self)

        if not hasattr(self, 'creatingRaidDict'):
            self.creatingRaidDict = {}   # type: dict[int, _Record]
        if not hasattr(self, 'spaces'):
            # type: dict[int, dungeon.TeamDungeonSpaceVal / dungeon.RaidDungeonSpaceVal]
            self.spaces = {}
        if not hasattr(self, 'dungeonNo'):
            self.dungeonNo = 0

    def _isTeamLine(self):
        """小队线（承接 TeamDungeonStub）"""
        return self.dungeonEnterType == gameconst.DungeonEnterTypeEnum.TEAM

    def _isRaidLine(self):
        """团队线（承接 RaidDungeonStub）"""
        return self.dungeonEnterType == gameconst.DungeonEnterTypeEnum.RAID

    def _fullPrepare(self):
        # add check destroy cycle tick
        self.pyAddTimer(30, 30, gametimer.TIMER_DUNGEON_CHECK_DESTROY)

    @property
    def delayDestroyTimeout(self):
        return 60

    def doNext(self):
        LOG_INFO('CrossTeamDungeonStub::doNext')
        self._fullPrepare()
        gameglobal.localBaseApp.fullPrepare(self.classname())

    def onTimer(self, tid, userArg):
        self._onTimerTrigger(tid, userArg)
        if userArg == gametimer.TIMER_DUNGEON_CHECK_DESTROY:
            self._checkDungeonSpaceDestroy()
        else:
            super(CrossTeamDungeonStub, self).onTimer(tid, userArg)

    # ============================================================
    # 销毁轮询（30s sweep）：小队线=跨服跳过+TeamStub.destroyTeamDungeonDelay 咨询；
    # 团队线=本地 tryDestroy 批量异步
    # ============================================================
    def _checkDungeonSpaceDestroy(self):
        if self._isTeamLine():
            self._teamCheckDungeonSpaceDestroy()
            return
        self._raidCheckDungeonSpaceDestroy()

    def _teamCheckDungeonSpaceDestroy(self):
        # 对照 TeamDungeonStub._checkDungeonSpaceDestroy
        now = utils.curTS()
        needDestroyList = []
        realDestroyList = []
        for spaceNo, _sVal in self.spaces.items():
            if _sVal.nDestoryCnt>3:
                LOG_ERR('_checkDungeonSpaceDestroy: cannot destory space', spaceNo)
                continue

            if _sVal.markCreate:
                # new dungeon, skip destroy once
                _sVal.markCreate = False
                continue

            if _sVal.markDestroy:
                if _sVal.markDestroy < now:
                    realDestroyList.append((spaceNo, _sVal.spaceUUID, 'time destory'))
                continue

            # 跨服讨伐空间无本服 TeamStub 队伍缓存可咨询，仅按完成/标记流程销毁
            if _sVal.isCrossDungeon():
                continue

            # extra kwargs in `team.TeamDungeonSpaceCacheVal.isDungeonSpaceCanBeDestoried`
            extraInfo = {'tCreate': _sVal.tCreate,
                         'tState': _sVal.state}

            needDestroyList.append((_sVal.teamUUID,
                                    self.dungeonNo,
                                    spaceNo,
                                    'delay timeout destory',
                                    extraInfo))

        for _nArgs in needDestroyList:
            _teamStub = gameengine.getTeamStub(_nArgs[0])
            _teamStub.destroyTeamDungeonDelay(*_nArgs)

        for _rArgs in realDestroyList:
            self.destoryDungeonSpace(*_rArgs)

    def _raidCheckDungeonSpaceDestroy(self):
        # 对照 RaidDungeonStub._checkDungeonSpaceDestroy
        now = utils.curTS()
        _needDestroyList = []
        realDestroyList = []
        for spaceNo, _sVal in self.spaces.items():
            # CASE_1: 超过最大清理次數, 報錯
            if _sVal.nDestoryCnt > 3:
                LOG_WARN('_checkDungeonSpaceDestroy:: cannot destroy space currently', spaceNo)
                # reset nDestoryCnt
                _sVal.nDestoryCnt = 0
                continue

            # CASE_2: 副本已经被标记删除
            if _sVal.isToDestory():
                # CASE_2.1: 副本需要被真正删除
                if _sVal.tMarkDestroy < now:
                    realDestroyList.append((spaceNo, _sVal.spaceUUID, 'time destroy'))
                continue

            _needDestroyList.append((spaceNo, _sVal.spaceUUID, 'time delay destroy'))

        self.asyncCallbackAfter(0.1)._checkTryMarkDestroyDungeonSpaces(_needDestroyList)
        self.asyncCallbackAfter(0.2)._checkRealDestroyDungeonSpaces(realDestroyList)

    def _checkRealDestroyDungeonSpaces(self, realDestroyList):
        for _rArgs in realDestroyList:
            self.destoryDungeonSpace(*_rArgs)

    def _checkTryMarkDestroyDungeonSpaces(self, needDestroyList):
        for _nArgs in needDestroyList:
            self.tryDestroyRaidDungeonDelay(*_nArgs)

    # ============================================================
    # cellapp 宕机空间丢失
    # ============================================================
    def onDungeonSpaceGone(self, spaceNo, reason):
        if self._isTeamLine():
            self._teamOnDungeonSpaceGone(spaceNo, reason)
            return
        self._raidOnDungeonSpaceGone(spaceNo, reason)

    def _teamOnDungeonSpaceGone(self, spaceNo, reason):
        # 对照 TeamDungeonStub.onDungeonSpaceGone
        if reason == gameconst.OnLoseCellReasonEnum.CELLAPP_DEATH:
            LOG_ERR("TeamDungeonStub::onDungeonSpaceGone::", spaceNo, reason)
            if spaceNo in self.spaces:
                _sVal = self.spaces[spaceNo]
                _sVal.cancelCompleteTimer(self, gametimer.TIMER_TAG_ON_TEAM_DUNGEON_COMPLETED_CALLBACK)
                _sVal.spaceMgr.cell.cancelCompleteDelayNotifyTimer(_sVal.spaceMgr.cell, gametimer.TIMER_TAG_ON_DUNGEON_COMPLETED_DELAY_CALLBACK)
                if not _sVal.isCrossDungeon():
                    # 跨服讨伐空间无本服 TeamStub 联动，仅本地清理
                    _teamStub = gameengine.getTeamStub(_sVal.teamUUID)
                    _teamStub.onDestroyTeamDungeon(_sVal.teamUUID, self.dungeonNo, spaceNo, _sVal.spaceUUID)

                self.cancelSpaceEntitiesLoadingProcess(spaceNo)

                _sVal.spaceBox.doEntireDestroy(False, False)
                self.spaces.pop(spaceNo)

    def _raidOnDungeonSpaceGone(self, spaceNo, reason):
        # 对照 RaidDungeonStub.onDungeonSpaceGone
        if reason == gameconst.OnLoseCellReasonEnum.CELLAPP_DEATH:
            LOG_ERR("RaidDungeonStub::onDungeonSpaceGone::", spaceNo, reason)
            if spaceNo in self.spaces:
                _spaceVal = self.spaces[spaceNo]
                _spaceVal.cancelCompleteTimer(self, gametimer.TIMER_TAG_ON_SINGLE_DUNGEON_COMPLETED_CALLBACK)
                _spaceVal.spaceMgr.cell.cancelCompleteDelayNotifyTimer(_spaceVal.spaceMgr.cell, gametimer.TIMER_TAG_ON_DUNGEON_COMPLETED_DELAY_CALLBACK)
                if not _spaceVal.isCrossDungeon():
                    # 跨服讨伐空间无本服 RaidStub 联动，仅本地清理
                    _raidStub = gameengine.getRaidStub(_spaceVal.raidUUID)
                    _raidStub.clearRaidDungeonInfo(_spaceVal.raidUUID, self.dungeonNo, spaceNo, _spaceVal.spaceUUID)

                self.cancelSpaceEntitiesLoadingProcess(spaceNo)

                _spaceVal.spaceBox.doEntireDestroy(False, False)
                self.spaces.pop(spaceNo)

    # ============================================================
    # 销毁：小队线两阶段 mark/real + 跨服真销毁前 founders 逐个 goback；
    # 团队线 _destroyRaidDungeonSpace + founders 门禁 + _kickOutAllFounders
    # + tryDestroyRaidDungeonDelay 系列
    # ============================================================
    def destoryDungeonSpace(self, spaceNo, spaceUUID, reason):
        if self._isTeamLine():
            self._teamDestoryDungeonSpace(spaceNo, spaceUUID, reason)
            return
        self._raidDestoryDungeonSpace(spaceNo, spaceUUID, reason)

    def _teamDestoryDungeonSpace(self, spaceNo, spaceUUID, reason):
        # 对照 TeamDungeonStub.destoryDungeonSpace
        LOG_INFO('destoryDungeonSpace', spaceNo, reason)
        if spaceNo not in self.spaces:
            LOG_WARN('wl: destoryDungeonSpace cannot find space:', spaceNo)
            return

        _sVal = self.spaces[spaceNo]
        if spaceUUID and _sVal.spaceUUID!=spaceUUID:
            LOG_WARN('destoryDungeonSpace:: spaceUUID not match {}!={}'.format(_sVal.spaceUUID, spaceUUID))
            return

        now = utils.curTS()
        if not _sVal.markDestroy:
            # delay destroy space
            _sVal.markDestroy = utils.curTS() + 60
            # 【副本服务端报错】
            # 销毁时停止所有该space的completeCallback
            # 【【上灵试炼】组队进入单人副本，打完boss后再次进入副本，会出现报错】
            # 提前cancel的时机到markDestroy
            _sVal.cancelCompleteTimer(self, gametimer.TIMER_TAG_ON_TEAM_DUNGEON_COMPLETED_CALLBACK)
            _sVal.spaceMgr.cell.cancelCompleteDelayNotifyTimer(_sVal.spaceMgr.cell, gametimer.TIMER_TAG_ON_DUNGEON_COMPLETED_DELAY_CALLBACK)
            _sVal.toDestoryDungeon()

            LOG_INFO('destoryDungeonSpace::space will be destroyed in next check,', spaceNo, _sVal.markDestroy)
            if not _sVal.isCrossDungeon():
                # 跨服讨伐空间无本服 TeamStub 联动，仅本地清理
                _teamStub = gameengine.getTeamStub(_sVal.teamUUID)
                _teamStub.onDestroyTeamDungeon(_sVal.teamUUID, self.dungeonNo, spaceNo, spaceUUID)
            return

        # real destroy dungeon
        elif _sVal.markDestroy < now:

            # 【大量机器人新号登录后立刻下线后副本报错】
            self.cancelSpaceEntitiesLoadingProcess(spaceNo)

            if _sVal.isCrossDungeon() and gameconfig.isCrossServer():
                # 跨服讨伐：销毁前先把仍在副本内的成员逐个送回本服
                # （否则镜像 cell 随空间销毁走 SPACE_GONE 离线，本服会进
                # offlineFromCrossServer 的下线销毁流程，回程中的客户端登录失败）；
                # 本服链路（第三步）：本服模式玩家本就在本服，无需送回
                # （异常残留的本服玩家随空间销毁走本服默认回出生图流程）
                for _gbId, _founderVal in _sVal.founders.items():
                    if _founderVal.isEnter and _founderVal.playerBox:
                        _founderVal.playerBox.gobackServer(gameconst.CrossServerCBComponent.ENUM_NONE, '', ())

            _sVal.spaceBox.doEntireDestroy(False, False)
            self.spaces.pop(spaceNo)

    def _raidDestoryDungeonSpace(self, spaceNo, spaceUUID, reason):
        # 对照 RaidDungeonStub.destoryDungeonSpace
        LOG_INFO('destoryDungeonSpace::', spaceNo, spaceUUID, reason)
        _spaceVal, err = self._destroyRaidDungeonSpace(spaceNo, spaceUUID)
        if err == gameconst.RaidDunErrno.ENUM_RAIDDUN_OK:
            if not _spaceVal.isCrossDungeon():
                # 强制清除raid中副本cache(如果有的话)（跨服讨伐无本服 RaidStub 缓存）
                gameengine.getRaidStub(_spaceVal.raidUUID).clearRaidDungeonInfo(
                    _spaceVal.raidUUID, self.dungeonNo, spaceNo, spaceUUID)

        elif err == gameconst.RaidDunErrno.ENUM_RAIDDUN_FOUNDER_IN_DUNGEON:
            self._kickOutAllFounders(spaceNo)

        else:
            LOG_ERR(f'destoryDungeonSpace[raid]:: failed, {err}')

    def _destroyRaidDungeonSpace(self, spaceNo, spaceUUID):
        if spaceNo not in self.spaces:
            return None, gameconst.RaidDunErrno.ENUM_RAIDDUN_DUNGEON_VAL_NOT_FOUND

        spaceVal = self.spaces[spaceNo]
        if spaceVal.spaceUUID != spaceUUID:
            return None, gameconst.RaidDunErrno.ENUM_RAIDDUN_SPACE_UUID_NOT_MATCH

        if not spaceVal.founders.isNoFounders():
            LOG_WARN('_destroyRaidDungeonSpace:: founders in space', self.dungeonNo, spaceNo)
            spaceVal.nDestoryCnt += 1
            return spaceVal, gameconst.RaidDunErrno.ENUM_RAIDDUN_FOUNDER_IN_DUNGEON

        # 【大量机器人新号登录后立刻下线后副本报错】
        self.cancelSpaceEntitiesLoadingProcess(spaceNo)

        spaceVal.spaceBox.doEntireDestroy(False, False)
        del self.spaces[spaceNo]
        return spaceVal, gameconst.RaidDunErrno.ENUM_RAIDDUN_OK

    def tryDestroyRaidDungeonDelay(self, spaceNo, spaceUUID, reason):
        LOG_DBG('tryDestroyRaidDungeonDelay::', spaceNo, spaceUUID, reason)
        _spaceVal, err = self._tryDestroyRaidDungeonDelay(spaceNo, spaceUUID)
        if err not in (gameconst.RaidDunErrno.ENUM_RAIDDUN_OK, gameconst.RaidDunErrno.ENUM_RAIDDUN_SKIP):
            gameengine.panicStack('tryDestroyRaidDungeonDelay:: failed, {}'.format(err), spaceNo, spaceUUID)
            return

        if err == gameconst.RaidDunErrno.ENUM_RAIDDUN_OK:
            # 强制踢出所有玩家
            self._kickOutAllFounders(spaceNo)

            # 【副本服务端报错】
            # 销毁时停止所有该space的completeCallback
            # 【【上灵试炼】组队进入单人副本，打完boss后再次进入副本，会出现报错】
            # 提前cancel的时机到markDestroy
            _spaceVal.cancelCompleteTimer(self, gametimer.TIMER_TAG_ON_RAID_DUNGEON_COMPLETED_CALLBACK)
            _spaceVal.spaceMgr.cell.cancelCompleteDelayNotifyTimer(_spaceVal.spaceMgr.cell, gametimer.TIMER_TAG_ON_DUNGEON_COMPLETED_DELAY_CALLBACK)
            if not _spaceVal.isCrossDungeon():
                # 跨服讨伐空间无本服 RaidStub 缓存可清
                gameengine.getRaidStub(_spaceVal.raidUUID).clearRaidDungeonInfo(
                    _spaceVal.raidUUID, self.dungeonNo, spaceNo, spaceUUID)

    def _tryDestroyRaidDungeonDelay(self, spaceNo, spaceUUID):
        if spaceNo not in self.spaces:
            return None, gameconst.RaidDunErrno.ENUM_RAIDDUN_DUNGEON_VAL_NOT_FOUND

        spaceVal = self.spaces[spaceNo]
        if spaceVal.spaceUUID != spaceUUID:
            return None, gameconst.RaidDunErrno.ENUM_RAIDDUN_SPACE_UUID_NOT_MATCH

        if spaceVal.isToDestory():
            LOG_WARN('_tryDestroyRaidDungeonDelay:: already mark destroyed', spaceNo, spaceUUID)
            return spaceVal, gameconst.RaidDunErrno.ENUM_RAIDDUN_SKIP

        if spaceVal.isCompleted():
            spaceVal.tMarkDestroy = utils.curTS() + self.delayDestroyTimeout
            spaceVal.toDestoryDungeon()
            return spaceVal, gameconst.RaidDunErrno.ENUM_RAIDDUN_OK

        return spaceVal, gameconst.RaidDunErrno.ENUM_RAIDDUN_SKIP

    def _kickOutAllFounders(self, spaceNo):
        LOG_INFO('RaidDungeonStub _kickOutAllFounders:: kickout', spaceNo)
        spaceVal = self.spaces[spaceNo]     # type: dungeon.RaidDungeonSpaceVal
        _needDestoryGBIDs = []
        src = dungeonSrc.KickoutFromDungeon(kickReason=gameconst.DungeonSrcKickReason.TIMEOUT)
        for gbId, founderVal in spaceVal.founders.items():
            base = founderVal.playerBox
            if founderVal.hasAvatar() and base and not utils.checkBoxOffline(base) and base.cell:
                LOG_INFO('RaidDungeonStub _kickoutAllFounders:: kickout', founderVal.playerGBID)
                founderVal.playerBox.cell.selfLeaveRaidDungeon(src)
            else:
                LOG_INFO('RaidDungeonStub _kickoutAllFounders:: destroy', founderVal.playerGBID)
                _needDestoryGBIDs.append(gbId)
        for i in _needDestoryGBIDs:
            spaceVal.founders.destoryFounder(i)

    def _kickOutTeamDungeonFounders(self, spaceNo):
        # 小队线副本完成踢人（对照 TeamStub._kickoutPlayer）：逐个 selfLeaveTeamDungeon
        # 传送回进入前位置/主城；仅本服模式跨服组队空间在完成回调中调用（跨服服不走传送链）
        LOG_INFO('CrossTeamDungeonStub _kickOutTeamDungeonFounders:: kickout', spaceNo)
        _sVal = self.spaces[spaceNo]    # type: dungeon.TeamDungeonSpaceVal
        _src = dungeonSrc.KickoutFromDungeon(kickReason=gameconst.DungeonSrcKickReason.TIMEOUT)
        _src._extra['spaceNo'] = spaceNo
        for _gbId, _fVal in _sVal.founders.items():
            _base = _fVal.playerBox
            if _fVal.isEnter and _base and not utils.checkBoxOffline(_base) and _base.cell:
                LOG_INFO('_kickOutTeamDungeonFounders:: kickout', _gbId)
                _base.cell.selfLeaveTeamDungeon(_src)

    # ============================================================
    # 离开副本：小队线=跨服 _leaveCrossDungeonSpaceSucc / 本服 TeamStub.leaveTeamDungeon；
    # 团队线=_leaveDungeonSpaceSucc + 本服 RaidStub.leaveRaid / 跨服 leaveTeam
    # + 末人自动完成 + goback
    # ============================================================
    def leaveDungeonSpaceSucc(self, spaceNo, playerBox, playerGbId, dungeonUUID, extra):
        if self._isTeamLine():
            self._teamLeaveDungeonSpaceSucc(spaceNo, playerBox, playerGbId, dungeonUUID, extra)
            return
        self._raidLeaveDungeonSpaceSucc(spaceNo, playerBox, playerGbId, dungeonUUID, extra)

    def _teamLeaveDungeonSpaceSucc(self, spaceNo, playerBox, playerGbId, teamUUID, extra):
        # 对照 TeamDungeonStub.leaveDungeonSpaceSucc
        LOG_INFO("leaveDungeonSpaceSucc::", spaceNo, playerBox, playerGbId, teamUUID, extra)
        if spaceNo not in self.spaces:
            LOG_ERR('leaveDungeonSpaceSucc::cannot get space', spaceNo)
            return
        sVal = self.spaces[spaceNo]

        if sVal.isCrossDungeon():
            self._leaveCrossDungeonSpaceSucc(spaceNo, playerBox, playerGbId, teamUUID, extra)
            return

        leaveTeam = False
        src = extra.get('src', None)
        # 来自客户端的主动退出
        if src and src.srcId==gameconst.DunSrcEnum.FROM_CLIENT:
            # 副本还在进行中退出的，直接退出队伍
            if sVal.completedReasonType == gameconst.DunegonCompleteReasonType.DEFAULT:
                leaveTeam = True

        _teamStub = gameengine.getTeamStub(sVal.teamUUID)
        _teamStub.leaveTeamDungeon(playerBox, playerGbId, sVal.teamUUID, self.dungeonNo, leaveTeam)

    def _leaveCrossDungeonSpaceSucc(self, spaceNo, playerBox, playerGbId, teamUUID, extra):
        # 跨服讨伐离开副本（对照本服 TeamStub.leaveTeamDungeon 语义）：
        # founders 离岗 + 进行中主动退出=退队（通知中心）+ 最后一人离开自动完成 + 返回本服
        _sVal = self.spaces[spaceNo]
        _founderVal = _sVal.founders.getFounderVal(playerGbId)
        if _founderVal:
            _founderVal.tLeave = utils.curTS()
            _founderVal.isEnter = False
            _founderVal.playerBox = None

        src = (extra or {}).get('src', None)
        if src and src.srcId == gameconst.DunSrcEnum.FROM_CLIENT:
            if _sVal.completedReasonType == gameconst.DunegonCompleteReasonType.DEFAULT:
                # 进行中主动退出 = 退出跨服小队（通知中心）
                gameengine.getCrossTeamStub(teamUUID).leaveTeam(playerBox, teamUUID, playerGbId)

        # 最后一人离开自动完成副本
        if _sVal.isActive() and not any([_f.isEnter for _f in _sVal.founders.values()]):
            self.completeTeamDungeon(spaceNo, teamUUID, False, 0, gameconst.DunegonCompleteReasonType.LEAVE)

        # 退出副本后返回本服（队伍不解散），仅跨服服执行
        # （本服链路：本服模式玩家本就在本服，退出走本服传送链回进入前位置/主城，无需 goback）；
        # 用 ENUM_NONE：onCrossServerEnd 对 ENUM_BASE 会直接 getattr(self, '') 分发，
        # 空方法名会抛 AttributeError（归墟回程即用 ENUM_NONE 无回调形态）
        if gameconfig.isCrossServer():
            playerBox.gobackServer(gameconst.CrossServerCBComponent.ENUM_NONE, '', ())

    def _raidLeaveDungeonSpaceSucc(self, spaceNo, playerBox, playerGbId, raidUUID, extra):
        # 对照 RaidDungeonStub.leaveDungeonSpaceSucc
        """团队成员离开副本成功后回调"""
        LOG_INFO('leaveDungeonSpaceSucc::', spaceNo, playerBox, playerGbId, raidUUID, extra)
        dungeonVal, founderVla, err = self._leaveDungeonSpaceSucc(spaceNo, playerBox, playerGbId, raidUUID)
        if err != gameconst.RaidDunErrno.ENUM_RAIDDUN_OK:
            LOG_ERR('leaveDungeonSpaceSucc:: failed, {}'.format(err))
            return

        _isCross = dungeonVal.isCrossDungeon()
        src = extra.get('src', None)
        # 来自客户端的主动退出
        if src and src.srcId==gameconst.DunSrcEnum.FROM_CLIENT:
            # 副本还在进行中退出的，直接退出队伍
            if dungeonVal.completedReasonType == gameconst.DunegonCompleteReasonType.DEFAULT:
                if _isCross:
                    # 跨服讨伐：进行中主动退出 = 退出跨服小队（通知中心）
                    gameengine.getCrossTeamStub(raidUUID).leaveTeam(playerBox, raidUUID, playerGbId)
                else:
                    # 退出团队
                    extraProps = {'leaveDungen':True}
                    gameengine.getRaidStub(raidUUID).leaveRaid(playerBox, playerGbId, raidUUID, extraProps)

        if _isCross:
            # 跨服讨伐：最后一人离开自动完成副本；退出副本后返回本服（队伍不解散），
            # goback 仅跨服服执行（本服链路：本服模式玩家本就在本服，
            # 退出走本服传送链回进入前位置/主城，无需 goback）。
            # 用 ENUM_NONE：onCrossServerEnd 对 ENUM_BASE 会直接 getattr(self, '') 分发，
            # 空方法名会抛 AttributeError（归墟回程即用 ENUM_NONE 无回调形态）
            if dungeonVal.isActive() and dungeonVal.founders.isNoFounders():
                self.completeRaidDungeon(spaceNo, raidUUID, False, 0, gameconst.DunegonCompleteReasonType.LEAVE)
            if gameconfig.isCrossServer():
                playerBox.gobackServer(gameconst.CrossServerCBComponent.ENUM_NONE, '', ())

    def _leaveDungeonSpaceSucc(self, spaceNo, playerBox, playerGBID, raidUUID):
        if spaceNo not in self.spaces:
            return None, gameconst.RaidDunErrno.ENUM_RAIDDUN_DUNGEON_VAL_NOT_FOUND
        dungeonVal = self.spaces[spaceNo]
        founderVal = dungeonVal.founders.getFounderVal(playerGBID)  # type: dungeon.RaidDungeonFounderVal
        if not founderVal:
            return None, gameconst.RaidDunErrno.ENUM_RAIDDUN_FOUNDER_VAL_NOT_FOUND
        founderVal.onAvatarLeave(playerGBID, isOffline=False)
        return dungeonVal, founderVal, gameconst.RaidDunErrno.ENUM_RAIDDUN_OK

    # ============================================================
    # 副本内掉线：小队线=跨服 memberOffline / 本服 TeamStub.onAvatarOffline；
    # 团队线=founderVal.onAvatarLeave + 跨服 memberOffline
    # ============================================================
    def onAvatarOffline(self, spaceNo, playerGbId):
        if self._isTeamLine():
            self._teamOnAvatarOffline(spaceNo, playerGbId)
            return
        self._raidOnAvatarOffline(spaceNo, playerGbId)

    def _teamOnAvatarOffline(self, spaceNo, playerGbId):
        # 对照 TeamDungeonStub.onAvatarOffline
        LOG_INFO('onAvatarOffline::', spaceNo, playerGbId)
        if spaceNo not in self.spaces:
            LOG_ERR('onAvatarOffline::cannot get space', spaceNo)
            return
        _sVal = self.spaces[spaceNo]
        if _sVal.isCrossDungeon():
            # 跨服讨伐副本内掉线 = 离线退队（通知中心移除成员）；重连回本服不回副本
            gameengine.getCrossTeamStub(_sVal.teamUUID).memberOffline(_sVal.teamUUID, playerGbId)
            return
        _teamStub = gameengine.getTeamStub(_sVal.teamUUID)
        _teamStub.onAvatarOffline(playerGbId, _sVal.teamUUID, self.dungeonNo)

    def _raidOnAvatarOffline(self, spaceNo, playerGbId):
        # 对照 RaidDungeonStub.onAvatarOffline
        """玩家下线时回调"""
        LOG_INFO('onAvatarOffline::', spaceNo, playerGbId)

        def _check():
            if spaceNo not in self.spaces:
                return None, gameconst.RaidDunErrno.ENUM_RAIDDUN_DUNGEON_VAL_NOT_FOUND
            return None, gameconst.RaidDunErrno.ENUM_RAIDDUN_OK

        _, err = _check()
        if err != gameconst.RaidDunErrno.ENUM_RAIDDUN_OK:
            LOG_ERR('onAvatarOffline:: check failed, {}'.format(err))
            return

        sVal = self.spaces[spaceNo]
        founderVal = sVal.founders.getFounderVal(playerGbId)    # type: dungeon.RaidDungeonFounderVal
        if founderVal:
            founderVal.onAvatarLeave(playerGbId, isOffline=True)

        if sVal.isCrossDungeon():
            # 跨服讨伐副本内掉线 = 离线退队（通知中心移除成员）；重连回本服不回副本
            gameengine.getCrossTeamStub(sVal.raidUUID).memberOffline(sVal.raidUUID, playerGbId)

    def onReliveInDungeon(self, spaceNo, playerBox, playerGbId, reliveType, reliveHp):
        return self._onReliveInDungeon(spaceNo, playerBox, playerGbId, reliveType, reliveHp)

    def onDungeonStarted(self, spaceNo, tCreate):
        LOG_INFO('onDungeonStarted::', spaceNo, tCreate)
        if spaceNo not in self.spaces:
            LOG_ERR('onDungeonStarted::cannot get space', spaceNo)
            return

        sVal = self.spaces[spaceNo]
        sVal.tCreate = tCreate or utils.curTS()
        sVal.spaceMgr.cell.onDungeonStarted(sVal.tCreate)

    # ============================================================
    # 完成（小队线全套，承接 TeamDungeonStub）
    # ============================================================
    def completeTeamDungeon(self, spaceNo, teamUUID, win, delay, reasonType):
        return self._onTeamDungeonCompleted(spaceNo, teamUUID, win, delay, reasonType)

    def _onTeamDungeonCompleted(self, spaceNo, teamUUID, win, delay, reasonType):
        LOG_INFO('in completeTeamDungeon:', spaceNo, teamUUID, win, delay, reasonType)

        if spaceNo not in self.spaces:
            if teamUUID:
                LOG_WARN('completeTeamDungeon:: cannot get space', spaceNo, teamUUID)
            else:
                LOG_ERR('completeTeamDungeon:: cannot get space', spaceNo)
            return

        _sVal = self.spaces[spaceNo]
        if _sVal.completeDungeonTimer:
            LOG_WARN('_onTeamDungeonCompleted:: finishing dungeon, skipped...', spaceNo, win, delay)
            return

        if _sVal.markDestroy:
            LOG_WARN("_onTeamDungeonCompleted:: dungeon already mark destroy", spaceNo, teamUUID, win, delay)
            return

        if not _sVal.isActive():
            LOG_WARN('_onTeamDungeonCompleted:: already complete', spaceNo, _sVal.state)
            return

        if not teamUUID:
            LOG_WARN("_onTeamDungeonCompleted:: skip teamUUID check", spaceNo, teamUUID, _sVal.teamUUID, win, delay)

        elif _sVal.teamUUID != teamUUID:
            LOG_WARN("_onTeamDungeonCompleted:: taemUUID not match", spaceNo, _sVal.teamUUID, teamUUID)
            return

        _isCross = _sVal.isCrossDungeon()
        if not _isCross:
            gameengine.getTeamStub(teamUUID).setInDungeon(teamUUID, False)

        _sVal.spaceMgr.cell.destroyAllEntities()
        _sVal.completedReasonType = reasonType
        _sVal.spaceMgr.cell.onTeamDungeonCompleted(spaceNo, teamUUID, win, delay, _sVal.getElapsedTime(), 0, _sVal.completedReasonType)
        # 跨服讨伐无本服公会副本任务联动
        if win and not _isCross:
            _sVal.spaceMgr.cell.finishGuildDungeonTask()

        if delay:
            if not _isCross:
                lastDungeonFinishedTime = utils.curTS() + delay
                _teamStub = gameengine.getTeamStub(_sVal.teamUUID)
                _teamStub.refreshLastDungeonFinishedTime(_sVal.teamUUID, lastDungeonFinishedTime)
            _sVal.completeDungeonTimer = self.addTimerCB(
                delay, '_onTeamDungeonCompletedCallback',
                (spaceNo, _sVal.spaceUUID, 'dungeon complete', win), gametimer.TIMER_TAG_ON_TEAM_DUNGEON_COMPLETED_CALLBACK)
        else:
            self._onTeamDungeonCompletedCallback(spaceNo, _sVal.spaceUUID, 'dungeon complete', win)

    def _onTeamDungeonCompletedCallback(self, spaceNo, spaceUUID, reason, win):
        LOG_INFO('_onTeamDungeonCompletedCallback::', spaceNo, spaceUUID, reason, win)
        if spaceNo not in self.spaces:
            LOG_ERR('_onTeamDungeonCompletedCallback::cannot get space', spaceNo)
            return

        _sVal = self.spaces[spaceNo]
        _sVal.completeDungeonTimer = 0
        if _sVal.spaceUUID != spaceUUID:
            LOG_ERR('_onTeamDungeonCompletedCallback:: spaceUUID not match', _sVal.spaceUUID, spaceUUID)
            return

        if not _sVal.isActive():
            LOG_WARN('_onTeamDungeonCompletedCallback:: already complete', spaceNo, _sVal.state)
            return

        # 【副本服务端报错】
        # completecallback后取消其他completecallback回调
        _sVal.clearCompleteTimer()

        _sVal.completeDungeon(win)

        if _sVal.isCrossDungeon():
            # 跨服组队：通知中心复位 InDungeon（队伍不解散），空间销毁由本 stub 自行处理
            # （本服线由 TeamStub.onTeamDungeonCompletedCB 负责后续销毁）
            gameengine.getCrossTeamStub(_sVal.teamUUID).crusadeFinished(_sVal.teamUUID, 1 if win else 0)
            if not gameconfig.isCrossServer():
                # 本服模式（问题记录#7）：对齐本服旧链路的完成自动退出
                # （TeamStub.onTeamDungeonCompletedCB -> _kickoutPlayer 语义，
                # 逐个 selfLeaveTeamDungeon 传送回进入前位置/主城）；
                # 跨服服模式维持现状：残留镜像在真销毁时由 _teamDestoryDungeonSpace 逐个 goback
                self._kickOutTeamDungeonFounders(spaceNo)
            self.destoryDungeonSpace(spaceNo, spaceUUID, reason)
            return

        extra = {
            'tCreate': _sVal.tCreate,
            'tState': _sVal.state,
            'forceDestroy': True,
            }

        gameengine.getTeamStub(_sVal.teamUUID).onTeamDungeonCompletedCB(_sVal.teamUUID, self.dungeonNo, spaceNo, reason, extra)

    # ============================================================
    # 完成（团队线全套，承接 RaidDungeonStub）
    # ============================================================
    def completeRaidDungeon(self, spaceNo, raidUUID, win, delay, reasonType):
        return self._onRaidDungeonCompleted(spaceNo, raidUUID, win, delay, reasonType)

    def _onRaidDungeonCompleted(self, spaceNo, raidUUID, win, delay, reasonType):
        LOG_INFO('_onRaidDungeonCompleted:', spaceNo, raidUUID, win, delay, reasonType)
        def _check():
            if spaceNo not in self.spaces:
                return None, gameconst.RaidDunErrno.ENUM_RAIDDUN_DUNGEON_VAL_NOT_FOUND
            return None, gameconst.RaidDunErrno.ENUM_RAIDDUN_OK

        _, err = _check()
        if err != gameconst.RaidDunErrno.ENUM_RAIDDUN_OK:
            if raidUUID:
                LOG_WARN('_onRaidDungeonCompleted:: check failed, {} {}'.format(err, raidUUID))
            else:
                LOG_ERR('_onRaidDungeonCompleted:: check failed, {}'.format(err))
            return

        _sVal = self.spaces[spaceNo]
        if _sVal.completeDungeonTimer:
            LOG_WARN('_onRaidDungeonCompleted:: finishing dungeon, skipped...', spaceNo, win, delay)
            return
        if not _sVal.isActive():
            LOG_WARN('_onRaidDungeonCompleted:: already complete', spaceNo, _sVal.state)
            return
        if not raidUUID:
            LOG_WARN('_onRaidDungeonCompleted:: skip raidUUID check', spaceNo, raidUUID, _sVal.raidUUID, win, delay)
        elif _sVal.raidUUID != raidUUID:
            LOG_WARN("_onRaidDungeonCompleted:: raidUUID not match", spaceNo, _sVal.raidUUID, raidUUID)
            return

        _isCross = _sVal.isCrossDungeon()
        if not _isCross:
            gameengine.getRaidStub(raidUUID).setInDungeon(raidUUID, False)

        _sVal.spaceMgr.cell.destroyAllEntities()
        _sVal.completedReasonType = reasonType
        _sVal.spaceMgr.cell.onRaidDungeonCompleted(
            spaceNo,
            raidUUID,
            win,
            delay,
            _sVal.dungeonCreepBaseKillDic,
            _sVal.getAllPlayerGbidAndNamePair(),
            _sVal.getElapsedTime(),
            0,
            _sVal.completedReasonType)

        # 副本完成后倒计时
        if delay > 0:
            if not _isCross:
                lastDungeonFinishedTime = utils.curTS() + delay
                _raidStub = gameengine.getRaidStub(_sVal.raidUUID)
                _raidStub.refreshLastDungeonFinishedTime(_sVal.raidUUID, lastDungeonFinishedTime)
            _sVal.completeDungeonTimer = self.addTimerCB(
                delay, '_onRaidDungeonCompletedCallback',
                (spaceNo, _sVal.spaceUUID, 'dungeon complete', win), gametimer.TIMER_TAG_ON_RAID_DUNGEON_COMPLETED_CALLBACK)
        else:
            self._onRaidDungeonCompletedCallback(spaceNo, _sVal.spaceUUID, 'dungeon complete', win)

    def _onRaidDungeonCompletedCallback(self, spaceNo, spaceUUID, reason, win):
        LOG_INFO('_onRaidDungeonCompletedCallback::', spaceNo, spaceUUID, reason, win)
        if spaceNo not in self.spaces:
            LOG_ERR('_onRaidDungeonCompletedCallback::cannot get space', spaceNo)
            return

        sVal = self.spaces[spaceNo]
        sVal.completeDungeonTimer = 0
        if sVal.spaceUUID != spaceUUID:
            LOG_ERR('_onRaidDungeonCompletedCallback:: spaceUUID not match', sVal.spaceUUID, spaceUUID)
            return

        if not sVal.isActive():
            LOG_WARN('_onRaidDungeonCompletedCallback:: already complete', spaceNo, sVal.state)
            return

        sVal.clearCompleteTimer()
        sVal.completeDungeon(win)
        sVal.toDestoryDungeon()
        self._kickOutAllFounders(spaceNo)
        if sVal.isCrossDungeon():
            # 跨服讨伐：通知中心复位 InDungeon（队伍不解散），无本服 RaidStub 联动
            gameengine.getCrossTeamStub(sVal.raidUUID).crusadeFinished(sVal.raidUUID, 1 if win else 0)
            return
        gameengine.getRaidStub(sVal.raidUUID).onRaidDungeonCompletedCB(sVal.raidUUID, self.dungeonNo, spaceNo, sVal.spaceUUID)

    # ============================================================
    # 进本：小队线=spaceMgr.cell.doEnterTeamDungeon / 失败 TeamStub 回退
    # / 跨服仅记录；团队线=跨服 enterRaidDunDirectly / 本服 DeprecationWarning 死路径
    # ============================================================
    def doEnterDungeon(self, box, gbId, dungeonUUID, spaceNo, extra):
        if self._isTeamLine():
            self._teamDoEnterDungeon(box, gbId, dungeonUUID, spaceNo, extra)
            return
        self._raidDoEnterDungeon(box, gbId, dungeonUUID, spaceNo, extra)

    def _teamDoEnterDungeon(self, box, gbId, teamUUID, spaceNo, extra):
        # 对照 TeamDungeonStub.doEnterDungeon
        if spaceNo not in self.spaces:
            LOG_ERR(f'spaceNo "{spaceNo}" not found in spaces')
            if extra and extra.get('crossTeamId'):
                # 跨服讨伐进本失败：无本服 TeamStub 可回退，仅记录（镜像由中心中止/超时流程回收）
                return
            _teamStub = gameengine.getTeamStub(teamUUID)
            _teamStub.onEnterDungeonFailedSpaceNotFound(box, gbId, teamUUID, self.dungeonNo, spaceNo, extra)
            return

        _spaceVal = self.spaces[spaceNo]

        if _spaceVal.isCompleted():
            LOG_ERR("space already completed", spaceNo, _spaceVal.spaceUUID)
            return

        if _spaceVal.markDestroy:
            LOG_ERR('spaceNo "{}" already be destroy delay'.format(spaceNo))
            return

        spaceBox = _spaceVal.spaceBox
        spaceMgr = _spaceVal.spaceMgr
        spaceMgr.cell.doEnterTeamDungeon(box, gbId, _spaceVal.spaceUUID, spaceBox, extra)

    def _raidDoEnterDungeon(self, box, gbId, raidUUID, spaceNo, extra):
        # 对照 RaidDungeonStub.doEnterDungeon
        """玩家执行进入副本时调用"""
        _spaceVal = self.spaces.get(spaceNo)
        if _spaceVal and _spaceVal.isCrossDungeon():
            # 跨服讨伐-首领巢穴（CROSS_CHIEF）：进本不经本服 RaidStub，由本 stub 直接进
            if _spaceVal.isCompleted():
                LOG_ERR('cross chief space already completed', spaceNo, _spaceVal.spaceUUID)
                return

            if _spaceVal.isToDestory():
                LOG_ERR('cross chief space destroying', spaceNo)
                return

            _spaceVal.spaceMgr.cell.enterRaidDunDirectly(
                box,
                gbId,
                _spaceVal.spaceUUID,
                _spaceVal.spaceBox,
                None,
                extra
            )
            return
        if extra and extra.get('crossTeamId'):
            # 跨服讨伐-首领巢穴进本失败（空间不存在/归属不符），仅记录（镜像由中心中止/超时流程回收）
            LOG_ERR('cross chief doEnterDungeon space not found', spaceNo, raidUUID)
            return
        raise DeprecationWarning('In raid dungeon, doEnterDungeon logic move to raidStub')

    # ============================================================
    # 进本成功登记：小队线仅跨服分支 founders+结算数据登记；
    # 团队线全分支 founders+结算数据登记（src pop 容错）
    # ============================================================
    def enterDungeonSpaceSuccess(self, spaceNo, playerBox, playerGbId, dungeonUUID, extra):
        if self._isTeamLine():
            self._teamEnterDungeonSpaceSuccess(spaceNo, playerBox, playerGbId, dungeonUUID, extra)
            return
        self._raidEnterDungeonSpaceSuccess(spaceNo, playerBox, playerGbId, dungeonUUID, extra)

    def _teamEnterDungeonSpaceSuccess(self, spaceNo, playerBox, playerGbId, teamUUID, extra):
        # 对照 TeamDungeonStub.enterDungeonSpaceSuccess
        # 本服 team 线成员登记由 TeamStub.onEnterTeamDungeon 完成（不走这里）；
        # 仅跨服组队空间（跨服服/本服模式，认 isCrossDungeon）需要：founders 簿记
        # （最后一人离开自动完成用）+ 结算数据登记（对照本服 DungeonSpaceMgr.doEnterTeamDungeon
        # 的 notifyDungeonExtarData；直进副本路径不经过 doEnterTeamDungeon，统一在这里补登记）
        _sVal = self.spaces.get(spaceNo)
        if not _sVal or not _sVal.isCrossDungeon():
            return

        _sVal.founders.addFounder(spaceNo, playerGbId, playerBox)
        _founderVal = _sVal.founders.getFounderVal(playerGbId)
        _founderVal.tEnter = utils.curTS()
        _founderVal.tLeave = 0
        _founderVal.isEnter = True

        _data = DungeonSettlement.DungeonExtraData()
        _data.loadDatas(extra or {})
        _sVal.spaceMgr.cell.notifyDungeonExtarData(playerGbId, _data)

    def _raidEnterDungeonSpaceSuccess(self, spaceNo, playerBox, playerGbId, raidUUID, extra):
        # 对照 RaidDungeonStub.enterDungeonSpaceSuccess
        """团队成员进入副本成功后回调"""
        LOG_INFO('enterDungeonSpaceSuccess::', spaceNo, playerBox, playerGbId, raidUUID, extra)
        _src = extra.pop('src', None)  # 本服进本一定带 dungeonSrc；跨服讨伐无 src（资格已由中心协调检查）
        founderVal, err = self._enterDungeonSpaceSucc(spaceNo, playerBox, playerGbId, raidUUID, _src)
        if err != gameconst.RaidDunErrno.ENUM_RAIDDUN_OK:
            LOG_ERR('enterDungeonSpaceSuccess:: failed, {}'.format(err))
            # NOTE: 进入团队副本后出现问题, 执行离开逻辑
            # （跨服讨伐无本服回退链路，仅记录；镜像由中心中止/超时流程回收）
            if not extra.get('crossTeamId'):
                playerBox.cell.leaveRaidDungeon()
        else:
            founderVal.playerName = extra.pop('playerName', '')

            dungeonVal = self.spaces[spaceNo]

            # 把数据带过去
            data = DungeonSettlement.DungeonExtraData()
            data.loadDatas(extra)
            dungeonVal.spaceMgr.cell.notifyDungeonExtarData(playerGbId, data)

    def _enterDungeonSpaceSucc(self, spaceNo, playerBox, playerGBID, _, src):
        if spaceNo not in self.spaces:
            return None, gameconst.RaidDunErrno.ENUM_RAIDDUN_DUNGEON_VAL_NOT_FOUND

        dungeonVal = self.spaces[spaceNo]
        if not dungeonVal.isActive():
            return None, gameconst.RaidDunErrno.ENUM_RAIDDUN_DUNGEON_IS_NOT_ACTIVE

        _founderVal = dungeonVal.founders.getFounderVal(playerGBID)  # type: dungeon.RaidDungeonFounderVal
        if not _founderVal:
            dungeonVal.founders.addFounder(spaceNo, dungeonVal.spaceUUID, playerGBID, playerBox)
            _founderVal = dungeonVal.founders.getFounderVal(playerGBID)
        _founderVal.onAvatarEnter(playerGBID)
        _founderVal.playerBox = playerBox

        return _founderVal, gameconst.RaidDunErrno.ENUM_RAIDDUN_OK

    # ============================================================
    # SpaceVal：小队线 TeamDungeonSpaceVal（本服无 founders，跨服组队挂 founders/crossTeamId）；
    # 团队线 RaidDungeonSpaceVal（自带 founders，跨服组队挂 crossTeamId）
    # ============================================================
    def _getDungeonSpaceVal(self, spaceNo, playerBox, playerGbId, dungeonUUID, extra):
        if self._isTeamLine():
            return self._teamGetDungeonSpaceVal(spaceNo, playerBox, playerGbId, dungeonUUID, extra)
        return self._raidGetDungeonSpaceVal(spaceNo, playerBox, playerGbId, dungeonUUID, extra)

    def _teamGetDungeonSpaceVal(self, spaceNo, playerBox, _, teamUUID, extra):
        # 对照 TeamDungeonStub._getDungeonSpaceVal
        _spaceVal = dungeon.TeamDungeonSpaceVal(
            spaceNo=spaceNo,
            spaceUUID=0,
            spaceMgr=None,
            spaceBox=None,
            teamUUID=teamUUID,
            spaceLevel=extra['spaceLevel'],
            extraDic={
                'maxLevel':extra['maxLevel'],
            }
        )
        # 跨服组队空间（本服/跨服服模式同构）：跨服队伍标记记到 SpaceVal 供 isCrossDungeon
        # 判定；founders 簿记挂 SpaceVal（本服线 founders 在 TeamStub 侧，跨服无 TeamStub）
        if extra.get('crossTeamId'):
            _spaceVal.crossTeamId = extra['crossTeamId']
            _spaceVal.founders = team.TeamDungeonFounders()
        return _spaceVal

    def _raidGetDungeonSpaceVal(self, spaceNo, _, playerGbId, raidUUID, extra):
        # 对照 RaidDungeonStub._getDungeonSpaceVal
        spaceVal = dungeon.RaidDungeonSpaceVal(
            spaceNo=spaceNo,
            spaceUUID=0,
            spaceMgr=None,
            spaceBox=None,
            raidUUID=raidUUID,
            spaceLevel=extra.get('spaceLevel', 1))
        # 跨服组队空间（本服/跨服服模式同构）：跨服队伍标记记到 SpaceVal 供 isCrossDungeon
        # 判定（founders 复用 RaidDungeonSpaceVal 自带容器）
        if extra.get('crossTeamId'):
            spaceVal.crossTeamId = extra['crossTeamId']
        return spaceVal

    # ============================================================
    # 建空间：小队线直建；团队线带 RaidDungeonCreatingMixin 创建锁
    # ============================================================
    def applyCreateDungeon(self, box, gbId, dungeonUUID, extra):
        if self._isTeamLine():
            self._teamApplyCreateDungeon(box, gbId, dungeonUUID, extra)
            return
        self._raidApplyCreateDungeon(box, gbId, dungeonUUID, extra)

    def _teamApplyCreateDungeon(self, box, gbId, teamUUID, extra):
        # 对照 TeamDungeonStub.applyCreateDungeon
        self.createDungeonSpaceRemote(box, gbId, teamUUID, extra)

    def _raidApplyCreateDungeon(self, box, gbId, raidUUID, extra):
        # 对照 RaidDungeonStub.applyCreateDungeon
        """真正创建副本时调用"""
        # TRY GETTING LOCK ------------------------------------------------
        if not self.getRaidDungeonCreatingLock(raidUUID, gbId):
            LOG_ERR('applyCreateDungeon:: creating...', raidUUID)
            return
        # -----------------------------------------------------------------
        self.createDungeonSpaceRemote(box, gbId, raidUUID, extra)

    def getDungeonSpaceRange(self):
        if self._isTeamLine():
            # 对照 TeamDungeonStub.getDungeonSpaceRange：BOTH→team 段否则 cloned 段
            enterType = DDI.datas[self.dungeonNo].get('enterType', gameconst.DungeonEnterTypeEnum.SINGLE)
            if enterType==gameconst.DungeonEnterTypeEnum.BOTH:
                return gameconst.SpaceType.getTeamDungeonSpaceRange(self.dungeonNo)
            else:
                return gameconst.SpaceType.getClonedSpaceNoRange(self.dungeonNo)
        # 对照 RaidDungeonStub.getDungeonSpaceRange：cloned 段
        return gameconst.SpaceType.getClonedSpaceNoRange(self.dungeonNo)

    def _getDungeonSpaceWeight(self, enterNum=0) -> int:
        # 小队线默认 enterNum=5（TeamDungeonStub），团队线默认 40（RaidDungeonStub）
        if not enterNum:
            enterNum = 5 if self._isTeamLine() else 40
        return utils.calcSpaceWeight(enterNum, False, gameconst.EntNumPerPlayerInAOI.teamDungeon)

    # ============================================================
    # 空间就绪：跨服→CrossTeamStub.onCrossCrusadeSpaceReady；
    # 本服各自 TeamStub.afterCreateTeamDungeon / RaidStub.onLoadRaidDungeonSpaceReady。
    # 注：两线旧签名不同（小队 (playerBox, spaceNo, teamUUID, extra)，
    # 团队 (playerBox, playerGBID, spaceNo, raidUUID, extra)），本类内统一为
    # (playerBox, playerGbId, spaceNo, dungeonUUID, extra) 再按线分支
    # （onLoadDungeonSpaceReady 仅 stub 内部调用，无外部调用方）
    # ============================================================
    def _loadDungeonSpaceEntities(self, spaceNo, playerBox, playerGbId, dungeonUUID, extraData):
        if self._isTeamLine():
            # 对照 TeamDungeonStub._loadDungeonSpaceEntities：ready first
            self.onLoadDungeonSpaceReady(playerBox, playerGbId, spaceNo, dungeonUUID, extraData)
            # use iCreateDungeonMonster function
            return super(CrossTeamDungeonStub, self)._loadDungeonSpaceEntities(
                spaceNo, playerBox, playerGbId, dungeonUUID, extraData)
        # 对照 RaidDungeonStub._loadDungeonSpaceEntities
        self.onLoadDungeonSpaceReady(playerBox, playerGbId, spaceNo, dungeonUUID, extraData)

    def onLoadDungeonSpaceReady(self, playerBox, playerGbId, spaceNo, dungeonUUID, extra):
        LOG_INFO('onLoadDungeonSpaceReady::')
        if self._isTeamLine():
            self._teamOnLoadDungeonSpaceReady(playerBox, spaceNo, dungeonUUID, extra)
            return
        self._raidOnLoadDungeonSpaceReady(playerBox, playerGbId, spaceNo, dungeonUUID, extra)

    def _teamOnLoadDungeonSpaceReady(self, playerBox, spaceNo, teamUUID, extra):
        # 对照 TeamDungeonStub.onLoadDungeonSpaceReady
        _spaceVal = self.spaces[spaceNo]
        if _spaceVal.isCrossDungeon():
            # 跨服讨伐：回报 CrossTeamStub（更新簿记并上报中心），不走本服 TeamStub；
            # spaceBox/spaceMgrBox 随簿记保存（镜像登录直进副本建 cell 用）
            gameengine.getCrossTeamStub(teamUUID).onCrossCrusadeSpaceReady(
                teamUUID,
                spaceNo,
                _spaceVal.spaceUUID,
                True,
                _spaceVal.spaceBox,
                _spaceVal.spaceMgr
            )
            return
        _teamStub = gameengine.getTeamStub(teamUUID)
        _teamStub.afterCreateTeamDungeon(teamUUID, self.dungeonNo, spaceNo, _spaceVal.spaceUUID, playerBox, extra)

    def _raidOnLoadDungeonSpaceReady(self, playerBox, playerGBID, spaceNo, raidUUID, extra):
        # 对照 RaidDungeonStub.onLoadDungeonSpaceReady
        """团队副本准备完毕后回调"""
        _spaceVal = self.spaces[spaceNo]
        if _spaceVal.isCrossDungeon():
            # 跨服讨伐：回报 CrossTeamStub（更新簿记并上报中心），不走本服 RaidStub；
            # spaceBox/spaceMgrBox 随簿记保存（镜像登录直进副本建 cell 用）
            gameengine.getCrossTeamStub(raidUUID).onCrossCrusadeSpaceReady(
                raidUUID,
                spaceNo,
                _spaceVal.spaceUUID,
                True,
                _spaceVal.spaceBox,
                _spaceVal.spaceMgr
            )
            return
        spaceUUID = _spaceVal.spaceUUID
        spaceBox = _spaceVal.spaceBox
        _spaceMgrBox = _spaceVal.spaceMgr
        gameengine.getRaidStub(raidUUID).onLoadRaidDungeonSpaceReady(
            playerBox, playerGBID, raidUUID, self.dungeonNo,
            spaceNo, spaceUUID, spaceBox, _spaceMgrBox, extra)

    # ============================================================
    # 死代码保留（疑似无调用方，照抄自旧类）
    # ============================================================
    def leaveTeamDungeon(self, spaceNo, teamID, src, playerBox):
        # 疑似无调用方（对照 TeamDungeonStub.leaveTeamDungeon 原样保留）
        LOG_INFO("leaveTeamDungeon~ ", spaceNo, teamID, src, playerBox)
        if spaceNo not in self.spaces:
            LOG_ERR('leaveTeamDungeon:: failed, missing space data', spaceNo, src, playerBox)
            return
        dungeonVal = self.spaces[spaceNo]
        founders = len(dungeonVal.founders)
        if founders <= 1:
            self.completeTeamDungeon(spaceNo, teamID, False, 0, gameconst.DunegonCompleteReasonType.LEAVE)
        else:
            playerBox.cell.selfLeaveTeamDungeon(src)

    def leaveRaidDungeon(self, spaceNo, raidUUID, src, playerBox):
        # 疑似无调用方（对照 RaidDungeonStub.leaveRaidDungeon 原样保留）
        LOG_INFO("leaveRaidDungeon~ ", spaceNo, raidUUID, src, playerBox)
        if spaceNo not in self.spaces:
            LOG_ERR('leaveRaidDungeon:: failed, missing space data', spaceNo, src, playerBox)
            return
        dungeonVal = self.spaces[spaceNo]
        founders = len(dungeonVal.founders)
        if founders <= 1:
            self.completeRaidDungeon(spaceNo, raidUUID, False, 0, gameconst.DunegonCompleteReasonType.LEAVE)
        else:
            playerBox.cell.selfLeaveRaidDungeon(src)
