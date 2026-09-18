# -*- coding: utf-8 -*-
# 跨服组队副本 cell 侧玩家接入 mixin（跨服组队全覆盖·第二步：自 iCrossTeamCell 迁入，行为不变）：
# - 讨伐客户端入口（applyStartCrossCrusade/applyExitCrossCrusade，已在 iAvatarCrossTeam.def 注册 Exposed）；
# - 进本条件检查的 cell 部分（checkCrossCrusadeConditionCell：战斗状态/传送条件）；
# - 副本落地收尾（onCrossCrusadeSpaceEnter/onCrossCrusadeSpaceLeave：AOI 队友缓存；
#   onLogonEnterCrusadeDungeonCB：镜像直进副本收尾）；
# - 副本陷阱（trap）：镜像直进走 Space.createCellNearSelf 直接建 cell，不经 iComplexTeleport 传送链
#   （trap 原有启动点在 _afterEnter_teamDungeon/_afterEnter_raidDungeon），在进本收尾处补启动；
#   出界 10s 倒计时强退，超时走跨服退出链路回本服。
# 队伍缓存/匹配/语音等组队逻辑留在 iCrossTeamCell，本模块只收副本-玩家接入点。

from KBEDebug import *

import gameconfig
import gameengine
import gameconst
import gametimer
import formula
import utils

import teamMatch_activity as TMACTD
import gamedecorator
import impDungeonCommon
import dungeonSrc
import complexTeleportOption

import message_Message_def as MMD


class ImpCrossTeamDungeonCell(impDungeonCommon.ImpDungeonCommon):

    # 副本陷阱 timer id（0=无进行中陷阱；类属性给默认值，实例赋值遮蔽，不占 def 属性）
    crossTeamDungeonTrapTimer = 0

    # ------------------------------------------------------------------
    # 目标 -> 讨伐副本映射
    # ------------------------------------------------------------------

    def _getCrossTeamDungeonMap(self, target):
        # 目标对应的讨伐副本（teamMatch_activity.enterDunID），建队时带入中心，讨伐进本用
        _targetInfo = TMACTD.datas.get(target)
        if _targetInfo:
            return _targetInfo.get('enterDunID', 0)

        return 0

    # ------------------------------------------------------------------
    # 客户端入口（已在 iAvatarCrossTeam.def 注册 Exposed），直连本服 CrossTeamStub
    # ------------------------------------------------------------------

    @utils.isMyself
    @gamedecorator.limitcall(0.5)
    def applyStartCrossCrusade(self, exposed):
        # 队长发起讨伐：队长身份在 cell 侧 crossTeamInfo 上校验
        LOG_INFO('applyStartCrossCrusade', self.gbId, self._crossTeamId())
        if not self._crossTeamId():
            return

        if not self._isCrossTeamCaptain():
            LOG_WARN('applyStartCrossCrusade, not captain', self.gbId)
            return

        gameengine.getCrossTeamStub(self._crossTeamId()).startCrusade(
            self.base,
            self._crossTeamId(),
            self.gbId
        )

    def _isInCrossTeamDungeonSpace(self, spaceMgr):
        # 当前空间是否为本跨服队的讨伐副本空间：
        # 跨服服空间认 CROSS playMode；本服模式空间 playMode 落本服枚举（CRUSADE/CHIEF，
        # D3-2 修订），以 dungeonPlayMode 上的队伍 ID（teamUUID/raidUUID）比对本服跨服队 ID
        _pm = spaceMgr.dungeonPlayMode
        if _pm.playMode in gameconst.DungeonPlayModeEnum.COLL_CROSS:
            return True
        _teamId = self._crossTeamId()
        return bool(_teamId) and _teamId in (getattr(_pm, 'teamUUID', 0), getattr(_pm, 'raidUUID', 0))

    @utils.isMyself
    @gamedecorator.crossServer
    @gamedecorator.limitcall(1)
    def applyExitCrossCrusade(self, exposed):
        # 客户端主动退出跨服组队副本，按本机身份分流：
        # - 跨服模式（跨服服镜像上调用）：直接调副本 stub 的跨服离开分支（founders 离岗；
        #   进行中退出=退跨服队并通知中心；最后一人离开自动完成；随后 gobackServer 回本服），
        #   不走本服副本的传送离开流程（跨服服上没有本服分线可回传，
        #   leaveTeamDungeon 的"回进入前位置"链路在此不适用）；
        # - 本服模式（本服链路，本机本服的跨服组队空间，playMode 落本服枚举）：走旧 team/raid
        #   线退副本的传送链路（回进入前位置/主城），离开空间后由传送回调链
        #   （_afterLeave_teamDungeon/_afterLeave_raidDungeon）单次回调副本 stub
        #   leaveDungeonSpaceSucc（本服分支不 goback）。
        # 不加 checkGameconfigEnable：跨服模式在跨服服执行，该服 game_config 不一定有本服开关
        LOG_INFO('applyExitCrossCrusade', self.gbId, self.spaceNo)
        if not self.isCrossServerInOtherServer:
            self._applyExitCrossCrusadeLocal()
            return

        _spaceMgr = self.spaceMgr
        if not _spaceMgr or _spaceMgr.dungeonPlayMode.playMode not in gameconst.DungeonPlayModeEnum.COLL_CROSS:
            LOG_WARN('applyExitCrossCrusade, not in cross dungeon', self.gbId, self.spaceNo)
            return

        _src = dungeonSrc.DungeonFromClientSrc(self.base, self.gbId)
        gameengine.getDungeonStubBySpaceNo(self.spaceNo).leaveDungeonSpaceSucc(
            self.spaceNo,
            self.base,
            self.gbId,
            self._crossTeamId(),
            {'src': _src}
        )

    def _applyExitCrossCrusadeLocal(self):
        # 本服模式退出（本服链路）：对照旧 team/raid 线退副本链路
        # （impTeamDungeon.leaveTeamDungeonCell/_leaveTeamDun、impRaidDungeon._doLeaveRaidDungeon）：
        # build src、回进入前位置/主城、doLeaveFromSapceToSpace；
        # 离开空间后由 _afterLeave_teamDungeon/_afterLeave_raidDungeon 单次回调副本 stub
        # leaveDungeonSpaceSucc（本服分支：founders 离岗/进行中退出=退队/末人自动完成，不 goback）
        _spaceMgr = self.spaceMgr
        if not _spaceMgr or not self._isInCrossTeamDungeonSpace(_spaceMgr):
            LOG_WARN('_applyExitCrossCrusadeLocal, not in cross dungeon', self.gbId, self.spaceNo)
            return

        if gameconfig.isCrossServer():
            # 防御：跨服服上的非镜像实体不应走到本服退出链（理论不可达）
            LOG_ERR('_applyExitCrossCrusadeLocal on cross server', self.gbId, self.spaceNo)
            return

        _dungeonNo = formula.fetchMapId(self.spaceNo)
        _spaceType = self._getParamBydungeonNo(_dungeonNo, 'type')
        _teamId = self._crossTeamId()
        _enterType = gameengine.getDungeonEnterTypeBySpaceNo(self.spaceNo)
        if _enterType == gameconst.DungeonEnterTypeEnum.RAID:
            # 首领线（跨服服 CROSS_CHIEF/本服 CHIEF）：对照 impRaidDungeon._doLeaveRaidDungeon；
            # lCtx.raidUUID 位置带跨服 teamId（_afterLeave_raidDungeon 原样传给 leaveDungeonSpaceSucc）
            lCtx = {'raidUUID': _teamId,
                    'spaceMgrBox': _spaceMgr.base,
                    'extra': {}}
        else:
            # 小队线（跨服服 CROSS_CRUSADE/本服 CRUSADE）：对照 impTeamDungeon._leaveTeamDun
            # （teamUUID 带跨服 teamId）
            lCtx = {'teamUUID': _teamId,
                    'spaceMgrBox': _spaceMgr.base,
                    'extra': {}}
        eCtx = {}
        _src = dungeonSrc.DungeonFromClientSrc(self.base, self.gbId)
        context = {'e': eCtx, 'l': lCtx, 'src': _src}
        options = complexTeleportOption.ComplexTeleportOpt(teleportType=gameconst.ComplexTeleportEnum.LEAVE)

        _mMapId, _mOutsideRecord = self.tryGetLastTeleportOutesideRecord(self.spaceNo, spaceType=_spaceType)
        _spaceNo = _mOutsideRecord.spaceNo if _mOutsideRecord else formula.combineLineSpaceNo(gameconst.MapIdDef.mapXinYuanCheng)
        self.doLeaveFromSapceToSpace(self.spaceNo, _spaceNo, options, context, spaceType=_spaceType)

    # ------------------------------------------------------------------
    # 本服模式进本（本服链路）：CrusadeGo 的 crossServerId==本机 serverId 时由
    # CrossTeamStub 逐本服成员驱动，对应跨服模式的 reqCrossServer 迁移链路
    # ------------------------------------------------------------------

    def onCrossCrusadeGoLocal(self, context):
        # 本服模式本地进本（已在 iAvatarCrossTeam.def 注册，CrossTeamStub.onCrusadeGo 本服分支
        # 经 base 调用）：复用旧 team 线 doEnterDungeon 进本链路（本服 CrossTeamDungeonStub ->
        # DungeonSpaceMgr cell -> impTeamDungeon.doEnterTeamDungeon ->
        # readyUseItemAndEnterTeamDungeon -> complexTeleport ENTER），
        # 传送锁/teamEnterCheckDic 校验/进入前位置记录由该链路自带；
        # 副本空间为本服 CrossTeamDungeonStub 所建（本服模式 playMode 落本服枚举），
        # spaceBox/spaceMgrBox 为 mailbox 不能经 PY_DICT 携带，故不自组传送 context
        # 而由 stub 链路以 ENTITYCALL 直达；
        # 进本完成后的 founders/结算数据登记由 _afterEnter_teamDungeon/_afterEnter_raidDungeon
        # 的跨服组队分支（认 crossTeamId）回调副本 stub enterDungeonSpaceSuccess 完成（对本服空间自然生效）
        LOG_INFO('onCrossCrusadeGoLocal', self.gbId, context)
        _teamId = context.get('crossTeamId', 0)
        _spaceNo = context.get('spaceNo', 0)
        if not _teamId or not _spaceNo:
            LOG_ERR('onCrossCrusadeGoLocal invalid context', self.gbId, context)
            return

        if _teamId != self._crossTeamId():
            LOG_WARN('onCrossCrusadeGoLocal team not match', self.gbId, _teamId, self._crossTeamId())
            return

        # 跨服队友缓存（AOI 刷怪加成/队友保护数据源，与跨服模式 enterCrusadeSpace 同点构造）
        self.onCrossCrusadeSpaceEnter(context)

        _extra = {
            'dungeonNo': context.get('dungeonNo', 0),
            'teamUUID': _teamId,
            'spaceUUID': context.get('spaceUUID', 0),
            'gbId': self.gbId,
            # 跨服标记：副本 stub 进本失败/进入成功分支识别用（同 CrossTeamStub.enterCrusadeSpace）
            'crossTeamId': _teamId,
            # 旧 team 线进本必需字段（impTeamDungeon.doEnterTeamDungeon）：
            # 进本资格名单（context 携带则按其校验）与跳过门票道具检查（条件已由中心协调检查过）
            'teamEnterCheckDic': context.get('teamEnterCheckDic') or {self.gbId: 1},
            'skipUseNeedItem': True,
            # 结算展示字段（DungeonExtraData.loadDatas 消费，缺了结算面板名单会空）
            'playerName': self.name,
            'name': self.name,
            'sex': self.sex,
            'school': self.school,
            'level': self.level,
            'eId': self.id,
        }
        _dungeonStub = gameengine.getDungeonStubBySpaceNo(_spaceNo)
        if not _dungeonStub:
            LOG_ERR('onCrossCrusadeGoLocal no dungeon stub', self.gbId, _teamId, _spaceNo)
            return
        _dungeonStub.doEnterDungeon(
            self.base,
            self.gbId,
            _teamId,
            _spaceNo,
            _extra
        )

    # ------------------------------------------------------------------
    # 条件检查的 cell 部分（中心 CrusadeCheck 下发，base 部分见 impCrossTeamDungeonBase）
    # ------------------------------------------------------------------

    def checkCrossCrusadeConditionCell(self, teamId, dungeonNo, baseReason):
        # 条件检查的 cell 部分（对照 impTeamDungeon 检查链路）：战斗状态/传送条件
        LOG_INFO('checkCrossCrusadeConditionCell', self.gbId, teamId, dungeonNo, baseReason)
        _reason = baseReason

        if _reason == gameconst.TeamDunCheckCondErrno.UNKNOWN:
            # 战斗状态检查
            if self.hasState(gameconst.StateEnum.Fighting):
                _reason = gameconst.TeamDunCheckCondErrno.FIGHTING_FAIL

        if _reason == gameconst.TeamDunCheckCondErrno.UNKNOWN:
            # 传送条件检查
            if not (self.checkCrtMapCanEnterDungeon() and self.canDoCompleteTeleport(noErrorMsg=True)):
                _reason = gameconst.TeamDunCheckCondErrno.TELEPORT_COND_FAIL

        gameengine.getCrossTeamStub(teamId).crusadeCheckResult(
            teamId,
            self.gbId,
            _reason
        )

    # ------------------------------------------------------------------
    # 副本落地收尾（AOI 队友缓存 / 镜像直进副本收尾）
    # ------------------------------------------------------------------

    def onCrossCrusadeSpaceEnter(self, context):
        # 跨服讨伐副本落地：构造跨服队伍的队友缓存——
        # 把 context['members'] 灌入 crossTeammateGbIds，AOI 事件（cell/Avatar.py 的
        # onEnteredView/onLeaveView 跨服分支）据此把队友灌入 teammateEntIdInAoiSet 与
        # expAddRatioByTeam，使 AOI 刷怪加成/队友保护复用现有判定
        LOG_INFO('onCrossCrusadeSpaceEnter', self.gbId, context.get('crossTeamId', 0))
        self.crossTeammateGbIds = set([
            _m.get('gbId', 0)
            for _m in context.get('members', [])
            if _m.get('gbId', 0) and _m.get('gbId', 0) != self.gbId
        ])

        # 已在视野内的队友立即入缓存（参照 TeamCacheValInPlayer.addMemberForPlayer）
        for _e in self.entitiesInView(True):
            if _e.IsAvatar and _e.gbId in self.crossTeammateGbIds:
                self.teammateEntIdInAoiSet.add(_e.id)

        self.expAddRatioByTeam = utils.getTeamExpBonus(len(self.teammateEntIdInAoiSet))

        # 副本陷阱补启动（镜像直进不经传送链，trap 原有启动点在 _afterEnter_*）；
        # 仅当前已在跨服副本空间内才生效（enterCrusadeSpace 链路的调用点在进本传送前，此处不生效）
        self._startCrossTeamDungeonTrap(context.get('dungeonNo', 0))

    def onCrossCrusadeSpaceLeave(self):
        # 离开跨服副本：清理队友缓存（镜像销毁前/被移出队伍时调用）
        self.crossTeammateGbIds = set()
        self.teammateEntIdInAoiSet.clear()
        self.expAddRatioByTeam = 0

    def onLogonEnterCrusadeDungeonCB(self, spaceNo, spaceMgrId, context):
        # 跨服讨伐镜像登录直进副本的收尾（logonCreateCellCB 回调，对照传送进本的
        # _afterEnter_teamDungeon/_afterEnter_raidDungeon 语义）：
        # 跨服队伍镜像 + AOI 队友缓存 + 空间登记/客户端倒计时 + founders 簿记（含结算数据登记）
        LOG_INFO('onLogonEnterCrusadeDungeonCB', self.gbId, spaceNo)
        _teamId = context.get('crossTeamId', 0)
        _dungeonNo = context.get('dungeonNo', 0)

        # 镜像标记跨服队伍并构造 AOI 队友缓存（副本内退出/掉线语义用）
        self.onCrossTeamIdChange(_teamId)
        self.onCrossCrusadeSpaceEnter(context)

        # 空间登记 + 客户端副本倒计时（对照 _afterEnter_* 既有处理）
        self.spaceMgrId = spaceMgrId
        _spaceMgr = self.spaceMgr
        if not _spaceMgr:
            LOG_ERR('onLogonEnterCrusadeDungeonCB no spaceMgr', self.gbId, spaceNo, spaceMgrId)
            return
        _spaceMgr.onPlayerEnter(self.id)
        _endTime = int(_spaceMgr.dungeonPlayMode.getTEnd(_dungeonNo))
        if _endTime and self.client:
            self.client.changeDungeonRemainTime(spaceNo, _endTime)

        # 进本成功回调副本 stub：founders 簿记 + 结算数据登记（team/raid 两线统一入口）
        # （结算展示字段 name/sex/school/level 由 DungeonExtraData.loadDatas 消费，缺了面板名单会空）
        _extra = {
            'dungeonNo': _dungeonNo,
            'teamUUID': _teamId,
            'spaceUUID': context.get('spaceUUID', 0),
            'gbId': self.gbId,
            'crossTeamId': _teamId,
            'playerName': self.name,
            'name': self.name,
            'sex': self.sex,
            'school': self.school,
            'level': self.level,
            'eId': self.id,
        }
        gameengine.getDungeonStubBySpaceNo(spaceNo).enterDungeonSpaceSuccess(
            spaceNo,
            self.base,
            self.gbId,
            _teamId,
            _extra
        )

        if self.base:
            self.base.onEnterDungeon(spaceNo, None, _extra)

        # 副本陷阱补启动（镜像直进收尾，对照 _afterEnter_* 的 trap 启动点）
        self._startCrossTeamDungeonTrap(_dungeonNo)

    # ------------------------------------------------------------------
    # 副本陷阱（trap）：出界 10s 倒计时强退（对照 _teamDungeonTrapCallback/_raidDungeonTrapCallback；
    # CROSS_CRUSADE 小队线与 CROSS_CHIEF 团队线共用：提示消息相同，超时退出统一走跨服退出链路）
    # ------------------------------------------------------------------

    def _startCrossTeamDungeonTrap(self, dunNo):
        # 启动跨服副本陷阱：副本空间只建在跨服服，非跨服环境/不在该跨服副本空间内不启动；
        # 幂等：onLogonEnterCrusadeDungeonCB 与 onCrossCrusadeSpaceEnter 都会触达，重复启动先取消旧 timer
        if not gameconfig.isCrossServer():
            return

        if formula.fetchMapId(self.spaceNo) != dunNo:
            return

        _spaceMgr = self.spaceMgr
        if not _spaceMgr or _spaceMgr.dungeonPlayMode.playMode not in gameconst.DungeonPlayModeEnum.COLL_CROSS:
            return

        if self.crossTeamDungeonTrapTimer:
            self.cancelTimerCB(
                self.crossTeamDungeonTrapTimer,
                gametimer.TIMER_TAG_CROSS_TEAM_DUNGEON_TRAP_CALLBACK
            )
            self.crossTeamDungeonTrapTimer = 0

        self.crossTeamDungeonTrapTimer = self.addTimerCB(
            1,
            '_crossTeamDungeonTrapCallback',
            (dunNo, self.DEFAULT_EXIT_COUNT_NUM),
            gametimer.TIMER_TAG_CROSS_TEAM_DUNGEON_TRAP_CALLBACK
        )

    def _crossTeamDungeonTrapCallback(self, dunNo, exitCount):
        # 对照两个旧 trap 回调：出界 10s 倒计时（出界提示/回区重置）；
        # 超时退出走跨服退出链路（不是本服的 selfLeaveTeamDungeon/leaveRaidDungeon——
        # 跨服镜像上没有本服分线可回）
        self.crossTeamDungeonTrapTimer = 0
        if formula.fetchMapId(self.spaceNo) != dunNo:
            return

        _mapInfo = self._getMapInfoByDungeonNo(dunNo)
        if not _mapInfo:
            return

        if not self._isPlayerInMap(_mapInfo):
            if exitCount <= 0:
                self.showMsg(MMD.datas.crossingDungeonArea, [])
                self._exitCrossTeamDungeonByTrap()
                return

            if exitCount == self.DEFAULT_EXIT_COUNT_NUM:
                self.showMsg(MMD.datas.leavingDungeonArea, [str(exitCount)])

            LOG_INFO('_crossTeamDungeonTrapCallback::outside cross team dungeon range, '
                     'exit in {}s'.format(exitCount * 1))
            exitCount -= 1
        elif self.DEFAULT_EXIT_COUNT_NUM != exitCount:
            exitCount = self.DEFAULT_EXIT_COUNT_NUM

        self.crossTeamDungeonTrapTimer = self.addTimerCB(
            1,
            '_crossTeamDungeonTrapCallback',
            (dunNo, exitCount),
            gametimer.TIMER_TAG_CROSS_TEAM_DUNGEON_TRAP_CALLBACK
        )

    def _exitCrossTeamDungeonByTrap(self):
        # 陷阱超时退出（复用 applyExitCrossCrusade 的内部逻辑，src 改为服务端来源）：
        # 调副本 stub 的跨服离开分支（founders 离岗；进行中退出=退跨服队并通知中心；
        # 最后一人离开自动完成；随后 gobackServer 回本服）
        if not self.isCrossServerInOtherServer:
            return

        _spaceMgr = self.spaceMgr
        if not _spaceMgr or _spaceMgr.dungeonPlayMode.playMode not in gameconst.DungeonPlayModeEnum.COLL_CROSS:
            LOG_WARN('_exitCrossTeamDungeonByTrap, not in cross dungeon', self.gbId, self.spaceNo)
            return

        _src = dungeonSrc.BasicDungeonSrc()
        gameengine.getDungeonStubBySpaceNo(self.spaceNo).leaveDungeonSpaceSucc(
            self.spaceNo,
            self.base,
            self.gbId,
            self._crossTeamId(),
            {'src': _src}
        )
