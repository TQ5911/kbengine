# -*- coding: utf-8 -*-
# 跨服组队副本 cell 侧玩家接入 mixin（跨服组队全覆盖·第二步：自 iCrossTeamCell 迁入，行为不变）：
# - 讨伐客户端入口（applyStartCrossCrusade/applyExitCrossCrusade，已在 iAvatarCrossTeam.def 注册 Exposed）；
# - 进本条件检查的 cell 部分（checkCrossCrusadeConditionCell：系统解锁/等级/战力门槛/
#   副本内实况/传送条件）；
# - 副本落地收尾（onCrossCrusadeSpaceEnter：AOI 队友集合落地灌入；
#   onLogonEnterCrusadeDungeonCB：镜像直进副本收尾 + 挂一次性落地对账标记，
#   首个权威队伍全量包到达时由 _recheckCrossMirrorDungeonTeam 比对归属队并补退）；
# - 退队联动退本（exitCrossTeamDungeonOnTeamLeave：onCrossTeamLeave/onCrossTeamDisband
#   落地回调中调用，仍在副本内时按本服/跨服模式退出副本）；
# - 副本陷阱（trap）：本服模式经 iComplexTeleport._afterEnter_teamDungeon/_afterEnter_raidDungeon
#   传送链启动，跨服服镜像直进不经传送链、在进本收尾处补启动；
#   出界 10s 倒计时强退，超时按模式退出（跨服服走跨服退出链路回本服，本服走本服传送链）。
# - GM 独立创建并进入讨伐副本（gmEnterDungeon，不经过组队中心与正常准入校验）。
# 第四步追加（自旧本服小队/团队副本 cell 模块迁入，方法名保持不变，
# 旧 mixin 从 Avatar 继承列表摘除后无缝接管；注册在 iAvatarCrossTeam.def CellMethods）：
# - 本服模式进本 RPC 终点：doEnterTeamDungeon/readyUseItemAndEnterTeamDungeon（小队线）、
#   doEnterRaidDungeonAfterCheck/_doEnterRaidDungeon（首领线，crossTeamId 放行已成主路径）；
# - 本服模式完成/超时踢人 RPC 终点：selfLeaveTeamDungeon/selfLeaveRaidDungeon
#   （锁检查保留，退出本体复用 _applyExitCrossCrusadeLocal 本服传送链）。
# 队伍缓存/匹配/语音等组队逻辑留在 iCrossTeamCell，本模块只收副本-玩家接入点。

from KBEDebug import *

import KBEngine

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
import dungeonPlayMode
import complexTeleportOption
import gamePlay_gamePlay as GP_GPD

import message_Message_def as MMD
import raidBossChallenge_config as RBC_CFG


class ImpCrossTeamDungeonCell(impDungeonCommon.ImpDungeonCommon):

    # 副本陷阱 timer id（0=无进行中陷阱；类属性给默认值，实例赋值遮蔽，不占 def 属性）
    crossTeamDungeonTrapTimer = 0
    # 镜像直进副本的一次性落地对账标记（0=无待对账；同上的类属性缺省模式）
    crossMirrorRecheckTeamId = 0
    # 跨服服镜像已发起退出的副本 spaceNo（0=未在退出；同上类属性缺省模式）。
    # 镜像退出链路（主动退本/陷阱强退/退队联动）都是直调副本 stub 的 leaveDungeonSpaceSucc，
    # 任一出口发起后置位，供迟到的退队联动推送判重，避免对同一 spaceNo 二次回调
    # （founder 已离岗并被完成流程清理，团队线二次回调必报 20010）；
    # 镜像进本收尾（onLogonEnterCrusadeDungeonCB）复位
    crossTeamDungeonExiting = 0

    # ------------------------------------------------------------------
    # 目标 -> 讨伐副本映射
    # ------------------------------------------------------------------

    def _getCrossTeamDungeonMap(self, target):
        # 目标对应的讨伐副本（teamMatch_activity.enterDunID），建队时带入中心，讨伐进本用
        _targetInfo = TMACTD.datas.get(target)
        if _targetInfo:
            return _targetInfo.get('enterDunID', 0)

        return 0

    def gmEnterDungeon(self, dungeonNo):
        # GM 独立建本：使用临时队伍 ID 复用副本生命周期，但不经过组队中心
        _dVal = GP_GPD.datas.get(dungeonNo)
        if not _dVal:
            return False, '执行失败, 没有找到相应副本ID'

        _dungeonType = _dVal.get('type', 0)
        _dungeonEnterType = _dVal.get('enterType', 0)
        _isRaid = gameconst.DungeonTypeJudge.isRaidDungeon(_dungeonType, _dungeonEnterType)
        _isTeam = gameconst.DungeonTypeJudge.isTeamDungeon(_dungeonType, _dungeonEnterType)
        if not _isRaid and not _isTeam:
            return False, '执行失败, 仅支持魔物讨伐或首领讨伐副本'

        _dungeonUUID = KBEngine.genUUID64()
        if gameconfig.isCrossServer():
            if _isRaid:
                _playMode = dungeonPlayMode.CrossChiefDungeonPlayMode(teamUUID=_dungeonUUID)
            else:
                _playMode = dungeonPlayMode.CrossCrusadeDungeonPlayMode(teamUUID=_dungeonUUID)
        else:
            if _isRaid:
                _playMode = dungeonPlayMode.ChiefDungeonPlayMode(raidUUID=_dungeonUUID)
            else:
                _playMode = dungeonPlayMode.CrusadeDungeonPlayMode(teamUUID=_dungeonUUID)
        _playMode.isGmDungeon = True

        _enterType = gameconst.DungeonEnterTypeEnum.RAID if _isRaid else gameconst.DungeonEnterTypeEnum.TEAM
        _dungeonStub = gameengine.getDungeonStubByDungeonNo(dungeonNo, _enterType)
        if not _dungeonStub:
            return False, '执行失败, 副本Stub不存在'

        # 测试用简化处理：把当前队伍成员一并拉进本（gmMembers 仅带 gbId，成员各自的
        # src/结算展示字段在其 cell 侧入口 gmEnterDungeonAsMember 补齐）
        _memberGbIds = [_g for _g in self.getTeammateGbIdSet() if _g != self.gbId]
        _teamEnterCheckDic = {self.gbId: 1}
        for _g in _memberGbIds:
            _teamEnterCheckDic[_g] = 1

        _extra = {
            'dungeonNo': dungeonNo,
            'dungeonPlayMode': _playMode,
            'crossTeamId': _dungeonUUID,
            'teamUUID': _dungeonUUID,
            'gbId': self.gbId,
            'spaceLevel': 0,
            'maxLevel': 0,
            'createAndEnter': self.gbId,
            'teamEnterCheckDic': _teamEnterCheckDic,
            'gmMembers': _memberGbIds,
            'skipUseNeedItem': True,
            'gmEnter': True,
            'src': dungeonSrc.DungeonFromClientGMSrc(self.base, self.gbId),
            'playerName': self.name,
            'name': self.name,
            'sex': self.sex,
            'school': self.school,
            'level': self.level,
            'eId': self.id,
        }
        _dungeonStub.applyCreateDungeon(
            self.base,
            self.gbId,
            _dungeonUUID,
            _extra
        )
        return True, '执行成功, 正在创建并进入副本'

    def gmEnterDungeonAsMember(self, dungeonNo, isRaid, spaceNo, spaceUUID, spaceBox, spaceMgrBox, extra):
        # GM 建本拉成员入本（测试用简化实现）：CrossTeamDungeonStub._gmEnterDungeon 经
        # PlayerStub.doOnOthersCell 调用；成员各自补齐 src 与结算展示字段后走既有进本链路
        LOG_INFO('gmEnterDungeonAsMember::', dungeonNo, spaceNo)
        extra = dict(extra)
        extra.update({
            'gbId': self.gbId,
            'playerName': self.name,
            'name': self.name,
            'sex': self.sex,
            'school': self.school,
            'level': self.level,
            'eId': self.id,
            'src': dungeonSrc.DungeonFromClientGMSrc(self.base, self.gbId),
        })
        if isRaid:
            self.doEnterRaidDungeonAfterCheck(
                dungeonNo, spaceNo, spaceUUID, spaceBox, spaceMgrBox, extra['src'], extra)
            return
        self.doEnterTeamDungeon(spaceNo, spaceUUID, spaceBox, spaceMgrBox, extra)

    # ------------------------------------------------------------------
    # 客户端入口（已在 iAvatarCrossTeam.def 注册 Exposed），直连本服 CrossTeamStub
    # ------------------------------------------------------------------

    @utils.isMyself
    @gamedecorator.limitcall(0.5)
    def applyStartCrossCrusade(self, exposed):
        # 队长发起讨伐：队长身份在 cell 侧 crossTeamInfo 上校验
        LOG_INFO('applyStartCrossCrusade', self._crossTeamId())
        if not self._crossTeamId():
            return

        if not self._isCrossTeamCaptain():
            LOG_WARN('applyStartCrossCrusade, not captain')
            return

        # 队长侧前置校验：目标玩法未解锁（如魔物巢穴未开启）直接拦截并提示，不上行中心；
        # 全体成员的解锁/等级/战力复核在中心协调检查 checkCrossCrusadeConditionCell 逐个执行
        if not self._isCrossTeamTargetUnlocked(self.crossTeamInfo.target):
            LOG_WARN('applyStartCrossCrusade, target not unlocked', self.crossTeamInfo.target)
            self.showMsg(MMD.datas.functionNotAvailable, [])
            return

        gameengine.getCrossTeamStub(self._crossTeamId()).startCrusade(
            self.base,
            self._crossTeamId(),
            self.gbId
        )

    def _isInCrossTeamDungeonSpace(self, spaceMgr, teamId=0):
        # 当前空间是否为本跨服队的讨伐副本空间：
        # 跨服服空间认 CROSS playMode；本服模式空间 playMode 落本服枚举（CRUSADE/CHIEF，
        # D3-2 修订），以 dungeonPlayMode 上的队伍 ID（teamUUID/raidUUID）比对本服跨服队 ID；
        # teamId 缺省取当前队伍缓存（退队联动退本场景在缓存清空前显式传入旧 teamId）
        _pm = getattr(spaceMgr, 'dungeonPlayMode', None)
        if not _pm:
            # 非副本空间（世界分线/主城等 SpaceMgr 无 dungeonPlayMode）：退队/解散推送
            # 在任意场景可达，不在副本空间即无需联动退本
            return False
        if getattr(_pm, 'isGmDungeon', False):
            return True
        if _pm.playMode in gameconst.DungeonPlayModeEnum.COLL_CROSS:
            return True
        _teamId = teamId or self._crossTeamId()
        if _teamId:
            return _teamId in (getattr(_pm, 'teamUUID', 0), getattr(_pm, 'raidUUID', 0))
        # 兜底：队伍缓存已空（中心重启后重连对账空包重置/跨服镜像全量包未落地）时，
        # 本服模式的跨服组队副本空间（playMode 落本服 CRUSADE/CHIEF 枚举，旧本服组队体系已废弃，
        # 该枚举空间只可能由跨服讨伐创建）直接放行，避免退本出口被锁死/重连守卫误判
        return _pm.playMode in (
            gameconst.DungeonPlayModeEnum.CRUSADE,
            gameconst.DungeonPlayModeEnum.CHIEF
        )

    @utils.isMyself
    @gamedecorator.crossServer
    @gamedecorator.limitcall(1)
    def applyExitCrossCrusade(self, exposed):
        # 客户端主动退出跨服组队副本（主体在 _doExitCrossTeamDungeon，供错入口自动改走复用）。
        # 不加 checkGameconfigEnable：跨服模式在跨服服执行，该服 game_config 不一定有本服开关
        LOG_INFO('applyExitCrossCrusade', self._crossTeamId(), self.spaceNo)
        _src = dungeonSrc.DungeonFromClientSrc(self.base, self.gbId)
        self._doExitCrossTeamDungeon(_src)

    def _doExitCrossTeamDungeon(self, src):
        # 退出跨服组队副本，按本机身份分流：
        # - 跨服模式（跨服服镜像上调用）：直接调副本 stub 的跨服离开分支（founders 离岗；
        #   进行中退出=退跨服队并通知中心；最后一人离开自动完成；随后 gobackServer 回本服），
        #   不走本服副本的传送离开流程（跨服服上没有本服分线可回传，
        #   leaveTeamDungeon 的"回进入前位置"链路在此不适用）；
        # - 本服模式（本服链路，本机本服的跨服组队空间，playMode 落本服枚举）：走旧 team/raid
        #   线退副本的传送链路（回进入前位置/主城），离开空间后由传送回调链
        #   （_afterLeave_teamDungeon/_afterLeave_raidDungeon）单次回调副本 stub
        #   leaveDungeonSpaceSucc（本服分支不 goback）。
        # 调用方：客户端入口 applyExitCrossCrusade；doLeaveSingleDungeon 错入口自动改走（项 37）
        if not self.isCrossServerInOtherServer:
            self._applyExitCrossCrusadeLocal()
            return

        _spaceMgr = self.spaceMgr
        _dungeonPlayMode = getattr(_spaceMgr, 'dungeonPlayMode', None) if _spaceMgr else None
        if not _dungeonPlayMode or _dungeonPlayMode.playMode not in gameconst.DungeonPlayModeEnum.COLL_CROSS:
            LOG_WARN('_doExitCrossTeamDungeon, not in cross dungeon', self.spaceNo)
            return

        # 置位退出标记：供迟到的退队联动推送（exitCrossTeamDungeonOnTeamLeave）判重
        self.crossTeamDungeonExiting = self.spaceNo
        gameengine.getDungeonStubBySpaceNo(self.spaceNo).leaveDungeonSpaceSucc(
            self.spaceNo,
            self.base,
            self.gbId,
            # 队伍缓存未就绪（镜像直进副本）时回落 crossTeamId 属性，避免 teamId=0 上中心
            self._crossTeamId() or self.crossTeamId,
            {'src': src}
        )

    def _applyExitCrossCrusadeLocal(self, teamId=0, src=None):
        # 本服模式退出（本服链路）：对照旧 team/raid 线退副本链路
        # （旧本服小队线/团队线退副本方法）：
        # build src、回进入前位置/主城、doLeaveFromSapceToSpace；
        # 离开空间后由 _afterLeave_teamDungeon/_afterLeave_raidDungeon 单次回调副本 stub
        # leaveDungeonSpaceSucc（本服分支：founders 离岗/进行中退出=退队/末人自动完成，不 goback）；
        # teamId/src 缺省为客户端主动退出场景（取当前队伍缓存 + FROM_CLIENT src），
        # 退队联动退本（exitCrossTeamDungeonOnTeamLeave）显式传入旧 teamId 与服务端 src
        _spaceMgr = self.spaceMgr
        if not _spaceMgr or not self._isInCrossTeamDungeonSpace(_spaceMgr, teamId):
            LOG_WARN('_applyExitCrossCrusadeLocal, not in cross dungeon', self.spaceNo)
            return

        if gameconfig.isCrossServer():
            # 防御：跨服服上的非镜像实体不应走到本服退出链（理论不可达）
            LOG_ERR('_applyExitCrossCrusadeLocal on cross server', self.spaceNo)
            return

        _dungeonNo = formula.fetchMapId(self.spaceNo)
        _spaceType = self._getParamBydungeonNo(_dungeonNo, 'type')
        _teamId = teamId or self._crossTeamId()
        _enterType = gameengine.getDungeonEnterTypeBySpaceNo(self.spaceNo)
        if _enterType == gameconst.DungeonEnterTypeEnum.RAID:
            # 首领线（跨服服 CROSS_CHIEF/本服 CHIEF）：对照旧本服团队线退副本方法；
            # lCtx.raidUUID 位置带跨服 teamId（_afterLeave_raidDungeon 原样传给 leaveDungeonSpaceSucc）
            lCtx = {'raidUUID': _teamId,
                    'spaceMgrBox': _spaceMgr.base,
                    'extra': {}}
        else:
            # 小队线（跨服服 CROSS_CRUSADE/本服 CRUSADE）：对照旧本服小队线退副本方法
            # （teamUUID 带跨服 teamId）
            lCtx = {'teamUUID': _teamId,
                    'spaceMgrBox': _spaceMgr.base,
                    'extra': {}}
        eCtx = {}
        _src = src or dungeonSrc.DungeonFromClientSrc(self.base, self.gbId)
        context = {'e': eCtx, 'l': lCtx, 'src': _src}
        options = complexTeleportOption.ComplexTeleportOpt(teleportType=gameconst.ComplexTeleportEnum.LEAVE)

        _mMapId, _mOutsideRecord = self.tryGetLastTeleportOutesideRecord(self.spaceNo, spaceType=_spaceType)
        _spaceNo = _mOutsideRecord.spaceNo if _mOutsideRecord else formula.combineLineSpaceNo(gameconst.MapIdDef.mapXinYuanCheng)
        self.doLeaveFromSapceToSpace(self.spaceNo, _spaceNo, options, context)

    def exitCrossTeamDungeonOnTeamLeave(self, teamId):
        # 退队联动退本（onCrossTeamLeave/onCrossTeamDisband 落地回调调用；须在
        # crossTeamInfo.reset() 之前调用——本服模式的队伍归属判定依赖旧 teamId，跨服镜像上
        # 无队伍缓存，teamId 一律由推送显式传入）：
        # 仍在本队跨服组队副本空间内时按模式退本——
        # 跨服模式（跨服服镜像）：直接调副本 stub 跨服离开分支（founders 离岗 + 末人自动完成
        # + gobackServer 回本服，同 trap 强退，镜像上没有本服分线可回传）；
        # 本服模式：走本服传送链回进入前位置/主城。
        # src 用 KickoutFromDungeon(FORCE) 而非 FROM_CLIENT：退队已发生，
        # 避免副本 stub"进行中主动退出=退队"分支对中心重复发 leaveTeam
        _spaceMgr = self.spaceMgr
        if not _spaceMgr or not self._isInCrossTeamDungeonSpace(_spaceMgr, teamId):
            return

        LOG_INFO('exitCrossTeamDungeonOnTeamLeave', teamId, self.spaceNo)
        _src = dungeonSrc.KickoutFromDungeon(kickReason=gameconst.DungeonSrcKickReason.FORCE)
        if self.isCrossServerInOtherServer:
            # 判重：镜像已发起过退出（主动退本/陷阱强退）时，本推送是"进行中主动退出=退队"
            # 的迟到联动回调；stub 侧 founder 已离岗并被完成流程清理，二次回调团队线必报
            # 20010（FOUNDER_VAL_NOT_FOUND），直接跳过
            if self.crossTeamDungeonExiting == self.spaceNo:
                LOG_INFO('exitCrossTeamDungeonOnTeamLeave, already exiting', teamId, self.spaceNo)
                return
            self.crossTeamDungeonExiting = self.spaceNo
            gameengine.getDungeonStubBySpaceNo(self.spaceNo).leaveDungeonSpaceSucc(
                self.spaceNo,
                self.base,
                self.gbId,
                teamId,
                {'src': _src}
            )
            return

        self._applyExitCrossCrusadeLocal(teamId, _src)

    def _recheckCrossMirrorDungeonTeam(self):
        # 跨服镜像直进副本的一次性落地对账（首个权威队伍全量包到达时经
        # iCrossTeamCell._applyCrossTeamInfoUpdate 漏斗调用）：镜像直进以 context 标记
        # 归属队（onLogonEnterCrusadeDungeonCB），落地时全量包尚未到达不能立即比对；
        # 迁移途中退队/解散的离队推送若早于镜像创建则无处落地丢失，此处以最新队伍
        # 缓存比对落地归属队，不一致（已退队/换队）按退队语义退出跨服副本回本服
        _teamId = self.crossMirrorRecheckTeamId
        if not _teamId:
            return
        self.crossMirrorRecheckTeamId = 0
        _spaceMgr = self.spaceMgr
        if not _spaceMgr or not self._isInCrossTeamDungeonSpace(_spaceMgr, _teamId):
            return
        if _teamId == self._crossTeamId():
            return
        LOG_WARN('_recheckCrossMirrorDungeonTeam team mismatch, exit cross dungeon',
                 _teamId, self._crossTeamId(), self.spaceNo)
        self.exitCrossTeamDungeonOnTeamLeave(_teamId)

    # ------------------------------------------------------------------
    # 本服模式进本（本服链路）：CrusadeGo 的 crossServerId==本机 serverId 时由
    # CrossTeamStub 逐本服成员驱动，对应跨服模式的 reqCrossServer 迁移链路
    # ------------------------------------------------------------------

    def onCrossCrusadeGoLocal(self, context):
        # 本服模式本地进本（已在 iAvatarCrossTeam.def 注册，CrossTeamStub.onCrusadeGo 本服分支
        # 经 base 调用）：走本服 CrossTeamDungeonStub -> DungeonSpaceMgr cell ->
        # doEnterTeamDungeon（自旧本服小队副本模块迁入本文件）-> readyUseItemAndEnterTeamDungeon
        # -> complexTeleport ENTER 进本链路，
        # 传送锁/teamEnterCheckDic 校验/进入前位置记录由该链路自带；
        # 副本空间为本服 CrossTeamDungeonStub 所建（本服模式 playMode 落本服枚举），
        # spaceBox/spaceMgrBox 为 mailbox 不能经 PY_DICT 携带，故不自组传送 context
        # 而由 stub 链路以 ENTITYCALL 直达；
        # 进本完成后的 founders/结算数据登记由 _afterEnter_teamDungeon/_afterEnter_raidDungeon
        # 的跨服组队分支（认 crossTeamId）回调副本 stub enterDungeonSpaceSuccess 完成（对本服空间自然生效）
        LOG_INFO('onCrossCrusadeGoLocal', context)
        _teamId = context.get('crossTeamId', 0)
        _spaceNo = context.get('spaceNo', 0)
        if not _teamId or not _spaceNo:
            LOG_ERR('onCrossCrusadeGoLocal invalid context', context)
            return

        if _teamId != self._crossTeamId():
            LOG_WARN('onCrossCrusadeGoLocal team not match', _teamId, self._crossTeamId())
            return

        # AOI 队友集合落地灌入（与跨服模式 enterCrusadeSpace 同点处理）
        self.onCrossCrusadeSpaceEnter(context)

        _extra = {
            'dungeonNo': context.get('dungeonNo', 0),
            'teamUUID': _teamId,
            'spaceUUID': context.get('spaceUUID', 0),
            'gbId': self.gbId,
            # 跨服标记：副本 stub 进本失败/进入成功分支识别用（同 CrossTeamStub.enterCrusadeSpace）
            'crossTeamId': _teamId,
            # 传送来源 src：离开场景埋点（cube_leave/wonderland_leave 取 context['src']）
            # 与副本 stub enterDungeonSpaceSuccess 消费，缺省为 None 会在 _afterLeave_cube 抛异常
            'src': dungeonSrc.DungeonFromClientSrc(self.base, self.gbId),
            # 旧 team 线进本必需字段：
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
            LOG_ERR('onCrossCrusadeGoLocal no dungeon stub', _teamId, _spaceNo)
            return
        _dungeonStub.doEnterDungeon(
            self.base,
            self.gbId,
            _teamId,
            _spaceNo,
            _extra
        )

    # ------------------------------------------------------------------
    # 进本 RPC 终点（自旧本服小队/团队副本 cell 模块迁入，方法名与参数签名
    # 保持不变，DungeonSpaceMgr.cell 调用方零改动；旧分支——本服队伍/团队校验、门票道具
    # 检查链、自动匹配池交互——随旧系统删除，成员资格已由中心协调检查）
    # ------------------------------------------------------------------

    def doEnterTeamDungeon(self, spaceNo, spaceUUID, spaceBox, spaceMgrBox, extra):
        # 本服模式小队线进本入口（对照旧本服小队线进本入口）：
        # CrossTeamDungeonStub._teamDoEnterDungeon -> DungeonSpaceMgr.cell.doEnterTeamDungeon -> 本方法
        LOG_INFO('doEnterTeamDungeon::')
        if extra.get('createAndEnter', 0) != self.gbId:
            # lock for team members
            _now = utils.curTS()
            if self.isGlobalTeleportLocked(now=_now):
                LOG_WARN("doEnterTeamDungeon:: teleport locked", self.teleportGlobalLockRlsT)
                return
            self.acquireGlobalTeleportLock(now=_now)

        _teamEnterCheckDic = extra['teamEnterCheckDic']
        if self.gbId not in _teamEnterCheckDic:
            LOG_WARN('doEnterTeamDungeon:: not in check list', _teamEnterCheckDic)
            return
        extra['clientDistinctIdCell'] = self.clientDistinctIdCell
        # enter directly
        self.readyUseItemAndEnterTeamDungeon(0, spaceNo, spaceUUID, spaceBox, spaceMgrBox, extra)

    @gamedecorator.teleportInQueue
    def readyUseItemAndEnterTeamDungeon(self, state, spaceNo, spaceUUID, spaceBox, spaceMgrBox, extra):
        """在这里进入副本（对照旧本服小队线进本方法；
        跨服链路门票检查已由中心协调完成，state 恒为 0）"""
        LOG_INFO('readyUseItemAndEnterTeamDungeon::')
        if state != 0:
            LOG_ERR('Enter TeamDungeon Failed, use item error: code={}, spaceNo={}'.format(state, spaceNo))
            return

        eCtx = {'spaceUUID': spaceUUID,
                    'spaceBox': spaceBox,
                    'spaceMgrBox': spaceMgrBox,
                    'teamUUID': extra['teamUUID'],
                    'extra': extra}
        lCtx = {}
        src = extra.get('src')
        context = {'e': eCtx, 'l': lCtx, 'src': src}
        options = complexTeleportOption.ComplexTeleportOpt(teleportType=gameconst.ComplexTeleportEnum.ENTER)

        canLeave = self.packComplexTeleportLeaveData(lCtx)
        if not canLeave:
            if canLeave.extra not in gameconst.CompleteTeleportLeaveFailReason.COLL_USEROPRERRNO:
                gameengine.panicStack('readyUseItemAndEnterTeamDungeon::fatal error when try to enter team dungeon space', self.spaceNo, spaceNo, context)
            else:
                LOG_WARN("readyUseItemAndEnterTeamDungeon::failed, errno={}".format(canLeave.extra), self.spaceNo, spaceNo, context)
            return

        self.telFromSpaceToSpace(self.spaceNo, spaceNo, options=options, context=context)

    @gamedecorator.teleportInQueue
    def doEnterRaidDungeonAfterCheck(self, dungeonNo, spaceNo, spaceUUID, spaceBox, spaceMgrBox, src, extraProps):
        """--每个团员检查完毕后直接进入团队副本--（对照旧本服团队线进本检查回调：
        CrossTeamDungeonStub._raidDoEnterDungeon -> DungeonSpaceMgr.cell.enterRaidDunDirectly -> 本方法；
        跨服讨伐（首领巢穴）无本服团队，跨服队伍镜像标记 crossTeamId 为唯一放行依据——
        原 inRaid 失败分支中的 crossTeamId 放行已提为主路径）"""
        if extraProps.get('createAndEnter', None) != self.gbId:
            # lock for raid members
            _now = utils.curTS()
            if self.isGlobalTeleportLocked(now=_now):
                LOG_WARN("doEnterRaidDungeonAfterCheck:: teleport locked", self.teleportGlobalLockRlsT)
                return
            self.acquireGlobalTeleportLock(now=_now)

        if not self.crossTeamId and not extraProps.get('gmEnter'):
            LOG_ERR('doEnterRaidDungeonAfterCheck:: not in cross team', dungeonNo, spaceNo)
            return

        _noEnterDungeon = extraProps.get('noEnterDungeon', False)
        if not _noEnterDungeon:
            self._doEnterRaidDungeon(dungeonNo, spaceNo, spaceUUID, spaceBox, src, spaceMgrBox, extraProps)

    def _doEnterRaidDungeon(self, dungeonNo, spaceNo, spaceUUID, spaceBox, src, spaceMgrBox, extra):
        # 对照旧本服团队线进本方法（打包传送数据 -> complexTeleport ENTER）
        LOG_INFO('_doEnterRaidDungeon:', dungeonNo, spaceNo, spaceUUID, spaceBox, src, spaceMgrBox, extra)
        eCtx = {'spaceUUID': spaceUUID,
                    'spaceBox': spaceBox,
                    'spaceMgrBox': spaceMgrBox,
                    'extra': extra}
        lCtx = {}
        context = {'e': eCtx, 'l': lCtx, 'src': src}
        options = complexTeleportOption.ComplexTeleportOpt(teleportType=gameconst.ComplexTeleportEnum.ENTER)

        canLeave = self.packComplexTeleportLeaveData(lCtx)
        if not canLeave:
            if canLeave.extra not in gameconst.CompleteTeleportLeaveFailReason.COLL_USEROPRERRNO:
                gameengine.panicStack('_doEnterRaidDungeon::fatal error when try to enter raid dungeon space', self.spaceNo, spaceNo, context)
            else:
                LOG_WARN("_doEnterRaidDungeon::failed, errno={}".format(canLeave.extra), self.spaceNo, spaceNo, context)
            return
        #首领讨伐
        self.base.completeGuildTask(gameconst.GuildTaskType.ENTERMAP,RBC_CFG.datas['raidBossChallengeActID']['value'],1)

        self.telFromSpaceToSpace(self.spaceNo, spaceNo, options=options, context=context)

    # ------------------------------------------------------------------
    # 退本 RPC 终点（本服模式完成/超时踢人：CrossTeamDungeonStub._kickOutTeamDungeonFounders/
    # _kickOutAllFounders -> 玩家 cell；对照旧本服小队线/团队线强退入口，锁检查保留，退出本体复用本服模式退出链路）
    # ------------------------------------------------------------------

    def selfLeaveTeamDungeon(self, src):
        # 本服模式小队线踢人/强退入口（对照旧本服小队线强退入口：
        # src._extra['spaceNo'] 不匹配当前空间时丢弃——踢人指令发出后玩家可能已自行离开）
        LOG_INFO('selfLeaveTeamDungeon::', src)
        spaceNo = src._extra.get('spaceNo')
        if spaceNo and spaceNo != self.spaceNo:
            LOG_INFO('selfLeaveTeamDungeon, not in same space no', src, self.spaceNo)
            return
        _now = utils.curTS()
        if self.isGlobalTeleportLocked(_now):
            LOG_WARN("selfLeaveTeamDungeon:: teleport locked", src, self.teleportGlobalLockRlsT)
            return
        self.acquireGlobalTeleportLock(now=_now)
        self._applyExitCrossCrusadeLocal(0, src)

    def selfLeaveRaidDungeon(self, src):
        # 本服模式首领线踢人/强退入口（对照旧本服团队线强退入口）
        LOG_INFO("selfLeaveRaidDungeon::", src)
        _now = utils.curTS()
        if self.isGlobalTeleportLocked(now=_now):
            LOG_WARN("selfLeaveRaidDungeon:: teleport locked", src, self.teleportGlobalLockRlsT)
            return
        self.acquireGlobalTeleportLock(now=_now)
        self._applyExitCrossCrusadeLocal(0, src)

    # ------------------------------------------------------------------
    # 条件检查的 cell 部分（中心 CrusadeCheck 下发，base 部分见 impCrossTeamDungeonBase）
    # ------------------------------------------------------------------

    def checkCrossCrusadeConditionCell(self, teamId, dungeonNo, baseReason):
        # 条件检查的 cell 部分（对照旧本服小队线检查链路）：
        # 系统解锁/等级门槛/战力门槛（防协议绕过"带老板"）/传送条件
        LOG_INFO('checkCrossCrusadeConditionCell', teamId, dungeonNo, baseReason)
        _reason = baseReason

        if _reason == gameconst.TeamDunCheckCondErrno.UNKNOWN:
            # 系统解锁判定：按副本线别查对应 UI 解锁位（小队线=魔物巢穴，团队线=首领巢穴），
            # 未解锁的成员禁止进本
            _dVal = GP_GPD.datas.get(dungeonNo, {})
            _isRaid = gameconst.DungeonTypeJudge.isRaidDungeon(
                _dVal.get('type', 0),
                _dVal.get('enterType', 0)
            )
            if not self._isCrossTeamLineUnlocked(_isRaid):
                LOG_WARN('checkCrossCrusadeConditionCell, dungeon line not unlocked', teamId, dungeonNo)
                _reason = gameconst.TeamDunCheckCondErrno.UNLOCK_CHECK_FAIL
                self.showMsg(MMD.datas.functionNotAvailable, [])

        if _reason == gameconst.TeamDunCheckCondErrno.UNKNOWN:
            # 等级/战力门槛复核：以中心同步的队伍设置（crossTeamInfo.minLevel/minScore）为准，
            # 防协议绕过入队门槛把不达标的成员带进本
            _teamInfo = self.crossTeamInfo
            if _teamInfo:
                if self.level < _teamInfo.minLevel:
                    LOG_WARN('checkCrossCrusadeConditionCell, level failed:', self.level, _teamInfo.minLevel)
                    _reason = gameconst.TeamDunCheckCondErrno.SC_LEVEL_CHECK_FAIL
                    self.showMsg(MMD.datas.insufficientConditions, [])
                elif self.getTotalScore() < _teamInfo.minScore:
                    LOG_WARN('checkCrossCrusadeConditionCell, score failed:', self.getTotalScore(), _teamInfo.minScore)
                    _reason = gameconst.TeamDunCheckCondErrno.SCORE_CHECK_FAIL
                    self.showMsg(MMD.datas.teammateScoreNotEnough, [self.name])
            else:
                LOG_WARN('checkCrossCrusadeConditionCell, no team cache', teamId)

        # if _reason == gameconst.TeamDunCheckCondErrno.UNKNOWN:
        #     # 战斗状态检查
        #     if self.hasState(gameconst.StateEnum.Fighting):
        #         _reason = gameconst.TeamDunCheckCondErrno.FIGHTING_FAIL

        if _reason == gameconst.TeamDunCheckCondErrno.UNKNOWN:
            # 副本内禁止再进讨伐本：进本传送与退队/再匹配并发时，协调检查可能在
            # 落地旧副本后才到达；配表 ifEnterDun 对讨伐本图放行
            # （checkCrtMapCanEnterDungeon 拦不住），以当前空间实况兜底
            if formula.inDungeonScene(self.spaceNo):
                LOG_WARN('checkCrossCrusadeConditionCell, already in dungeon', teamId, dungeonNo, self.spaceNo)
                _reason = gameconst.TeamDunCheckCondErrno.TELEPORT_COND_FAIL

        if _reason == gameconst.TeamDunCheckCondErrno.UNKNOWN:
            # 传送条件检查
            if not (self.checkCrtMapCanEnterDungeon() and self.canDoCompleteTeleport(noErrorMsg=True)):
                _reason = gameconst.TeamDunCheckCondErrno.TELEPORT_COND_FAIL

        # failName：成员条件检查失败（次数/解锁/等级/战力）时回带失败成员名
        # （中心 abort 透传，游戏服按 failReason 区分后向队长下发对应提示）
        _failName = ''
        if _reason in (
                gameconst.TeamDunCheckCondErrno.REWARD_NUM_CHECK_FAIL,
                gameconst.TeamDunCheckCondErrno.UNLOCK_CHECK_FAIL,
                gameconst.TeamDunCheckCondErrno.SC_LEVEL_CHECK_FAIL,
                gameconst.TeamDunCheckCondErrno.SCORE_CHECK_FAIL):
            _failName = self.name

        gameengine.getCrossTeamStub(teamId).crusadeCheckResult(
            teamId,
            self.gbId,
            _reason,
            _failName
        )

    # ------------------------------------------------------------------
    # 副本落地收尾（AOI 队友缓存 / 镜像直进副本收尾）
    # ------------------------------------------------------------------

    def onCrossCrusadeSpaceEnter(self, context):
        # 跨服讨伐副本落地：灌 AOI 队友集合——
        # 落地时点镜像的 crossTeamInfo 尚未就绪（镜像直进副本链路不经全量推送），
        # 先用 context 成员快照灌已在视野的队友；之后由跨服缓存落地/成员增删的
        # _refreshAoiCrossTeammates 重建，进出视野由 Avatar.onEnteredView/onLeaveView
        # 经 isTeammate 增量维护
        LOG_INFO('onCrossCrusadeSpaceEnter', context.get('crossTeamId', 0))
        _memberGbIds = set([
            _m.get('gbId', 0)
            for _m in context.get('members', [])
            if _m.get('gbId', 0) and _m.get('gbId', 0) != self.gbId
        ])
        for _e in self.entitiesInView(True):
            if _e.IsAvatar and _e.gbId in _memberGbIds:
                self.teammateEntIdInAoiSet.add(_e.id)

        self.expAddRatioByTeam = utils.getTeamExpBonus(len(self.teammateEntIdInAoiSet))

        # 副本陷阱补启动（镜像直进不经传送链，trap 原有启动点在 _afterEnter_*）；
        # 仅当前已在跨服副本空间内才生效（enterCrusadeSpace 链路的调用点在进本传送前，此处不生效）
        self._startCrossTeamDungeonTrap(context.get('dungeonNo', 0))

    def onLogonEnterCrusadeDungeonCB(self, spaceNo, spaceMgrId, context):
        # 跨服讨伐镜像登录直进副本的收尾（logonCreateCellCB 回调，对照传送进本的
        # _afterEnter_teamDungeon/_afterEnter_raidDungeon 语义）：
        # 跨服队伍镜像 + AOI 队友缓存 + 空间登记/客户端倒计时 + founders 簿记（含结算数据登记）
        LOG_INFO('onLogonEnterCrusadeDungeonCB', spaceNo)
        _teamId = context.get('crossTeamId', 0)
        _dungeonNo = context.get('dungeonNo', 0)

        # 复位退出标记（见 crossTeamDungeonExiting）：镜像进本即未在退出
        self.crossTeamDungeonExiting = 0

        # 挂一次性落地对账标记：队伍全量包尚在途中（落地后 queryPlayerTeam 回包经
        # _applyCrossTeamInfoUpdate 漏斗到达），届时由 _recheckCrossMirrorDungeonTeam
        # 比对归属队——迁移途中退队/解散（离队推送早于镜像创建而丢失）的镜像补退副本
        self.crossMirrorRecheckTeamId = _teamId

        # 镜像标记跨服队伍并构造 AOI 队友缓存（副本内退出/掉线语义用）
        self.onCrossTeamIdChange(_teamId)
        self.onCrossCrusadeSpaceEnter(context)

        # 空间登记 + 客户端副本倒计时（对照 _afterEnter_* 既有处理）
        self.spaceMgrId = spaceMgrId
        _spaceMgr = self.spaceMgr
        if not _spaceMgr:
            LOG_ERR('onLogonEnterCrusadeDungeonCB no spaceMgr', spaceNo, spaceMgrId)
            return
        _spaceMgr.onPlayerEnter(self.id)
        # 结束时间取 spaceMgr 记录的实际值：结算后倒计时已提前，不能回退为 getTEnd 的配置推算值
        _endTime = _spaceMgr.getDungeonActualEndTime(_dungeonNo)
        if _endTime and self.client:
            self.client.changeDungeonRemainTime(spaceNo, _endTime)

        # 进本成功回调副本 stub：founders 簿记 + 结算数据登记（team/raid 两线统一入口）
        # （结算展示字段 name/sex/school/level 由 DungeonExtraData.loadDatas 消费，缺了面板名单会空）
        # 埋点字段 totalNum/joinType 对照传送链 _afterEnter_raidDungeon 补齐
        # （镜像直进不经传送链，onEnterDungeon 埋点消费）
        _extra = {
            'dungeonNo': _dungeonNo,
            'teamUUID': _teamId,
            'spaceUUID': context.get('spaceUUID', 0),
            'gbId': self.gbId,
            'crossTeamId': _teamId,
            'totalNum': self.getActiveTeamMemberCount(),
            'joinType': gameconst.TeamJoinType.DEFAULT,
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
    # 副本陷阱（trap）：出界 10s 倒计时强退（对照旧 _teamDungeonTrapCallback/_raidDungeonTrapCallback；
    # CROSS_CRUSADE 小队线与 CROSS_CHIEF 团队线共用：提示消息相同；
    # 超时按模式退出——跨服服镜像走跨服退出链路回本服，本服模式走本服传送链）
    # 启动点：本服模式经 iComplexTeleport._afterEnter_teamDungeon/_afterEnter_raidDungeon 传送链；
    # 跨服服镜像直进不经传送链，在进本收尾（onLogonEnterCrusadeDungeonCB/onCrossCrusadeSpaceEnter）补启动
    # ------------------------------------------------------------------

    def _startCrossTeamDungeonTrap(self, dunNo):
        # 启动跨服副本陷阱：仅当前已在本跨服队的副本空间内才生效
        # （跨服服认 CROSS playMode，本服模式认 dungeonPlayMode 上的队伍 ID，
        # 见 _isInCrossTeamDungeonSpace；enterCrusadeSpace 链路的调用点在进本传送前，此处不生效）；
        # 幂等：onLogonEnterCrusadeDungeonCB 与 onCrossCrusadeSpaceEnter 都会触达，重复启动先取消旧 timer
        if formula.fetchMapId(self.spaceNo) != dunNo:
            return

        _spaceMgr = self.spaceMgr
        if not _spaceMgr or not self._isInCrossTeamDungeonSpace(_spaceMgr):
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
        # 超时退出按模式分流（_exitCrossTeamDungeonByTrap）：本服模式走本服传送链，
        # 跨服服镜像走跨服退出链路（镜像上没有本服分线可回）
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
        # 陷阱超时退出（src 用服务端来源 BasicDungeonSrc，不触发副本 stub 的
        # "进行中主动退出=退队"分支，对齐旧 trap 只退本不退队的语义）：
        # - 本服模式：走本服传送链回进入前位置/主城（对照旧 selfLeaveTeamDungeon/leaveRaidDungeon
        #   的 trap 强退分支），离开空间后由 _afterLeave_* 回调副本 stub leaveDungeonSpaceSucc；
        # - 跨服模式（跨服服镜像）：调副本 stub 的跨服离开分支（founders 离岗；
        #   最后一人离开自动完成；随后 gobackServer 回本服）
        _src = dungeonSrc.BasicDungeonSrc()
        if not self.isCrossServerInOtherServer:
            self._applyExitCrossCrusadeLocal(0, _src)
            return

        _spaceMgr = self.spaceMgr
        _dungeonPlayMode = getattr(_spaceMgr, 'dungeonPlayMode', None) if _spaceMgr else None
        if not _dungeonPlayMode or _dungeonPlayMode.playMode not in gameconst.DungeonPlayModeEnum.COLL_CROSS:
            LOG_WARN('_exitCrossTeamDungeonByTrap, not in cross dungeon', self.spaceNo)
            return

        # 置位退出标记：供迟到的退队联动推送（exitCrossTeamDungeonOnTeamLeave）判重
        self.crossTeamDungeonExiting = self.spaceNo
        gameengine.getDungeonStubBySpaceNo(self.spaceNo).leaveDungeonSpaceSucc(
            self.spaceNo,
            self.base,
            self.gbId,
            # 队伍缓存未就绪（镜像直进副本）时回落 crossTeamId 属性，避免 teamId=0 上中心
            self._crossTeamId() or self.crossTeamId,
            {'src': _src}
        )
