# -*- coding: utf-8 -*-
# 跨服组队副本 base 侧玩家接入 mixin（跨服组队全覆盖·第二步：自 iCrossTeamBase 迁入，行为不变）：
# - 讨伐条件检查的 base 部分（奖励次数/门票），跨服迁移与落地（reqCrossServer 体系）；
# - 跨服镜像登录直进副本（空间先于迁移创建，createCell 讨伐分支）与失败兜底；
# - 进本落地埋点与活动计数（onTrackTeamDungeonEnter，旧组队下线的埋点补回）。
# 跨服队伍聊天与 Stub 下行中继等组队逻辑留在 iCrossTeamBase，本模块只收副本-玩家接入点。

from KBEDebug import *

import utils
import gameengine
import gameconst
import gameconfig
import formula
import LogTrackingMgr

import gamePlay_gamePlay as GP_GPD
import teamDunChallenge_config as TDC_CFG
import raidBossChallenge_config as RBC_CFG


class ImpCrossTeamDungeonBase(object):

    # ------------------------------------------------------------------
    # 讨伐（无确认弹窗：条件检查全部通过即进本）
    # ------------------------------------------------------------------

    def checkCrossCrusadeCondition(self, teamId, dungeonNo):
        # 中心下发的条件检查：base 部分（奖励次数/门票）后转 cell 部分
        # （系统解锁/等级/战力门槛/传送条件）
        LOG_INFO('checkCrossCrusadeCondition', self.gbID, teamId, dungeonNo)
        _baseReason = gameconst.TeamDunCheckCondErrno.UNKNOWN

        # 奖励次数检查：按 gamePlay 表进入类型区分小队线（魔物巢穴 CRUSADE，对照
        # 旧本服小队副本线的奖励次数检查）与团队线（首领巢穴 CHIEF，对照
        # 旧本服团队副本线的进本前成员预检查），
        # 线路判定与 CrossTeamStub.onCreateCrusadeSpace 的 playMode 落地保持一致
        _dVal = GP_GPD.datas.get(dungeonNo, {})
        _isRaid = gameconst.DungeonTypeJudge.isRaidDungeon(
            _dVal.get('type', 0),
            _dVal.get('enterType', 0)
        )
        if _isRaid:
            self.onTryAddUseCoinTimesFreeTicket(gameconst.RecoveryTicketSubType.CHIEF)
            if not self.chiefInfo.isCanTakeReward():
                _baseReason = gameconst.TeamDunCheckCondErrno.REWARD_NUM_CHECK_FAIL
        else:
            self.onTryAddUseCoinTimesFreeTicket(gameconst.RecoveryTicketSubType.CRUSADE)
            if not self.crusadeInfo.isCanTakeReward():
                _baseReason = gameconst.TeamDunCheckCondErrno.REWARD_NUM_CHECK_FAIL

        # 挑战次数不足：同步通知成员本人客户端（对照旧链 onMemberNoRewardNum；
        # 该原因只由上方 base 部分次数检查产生，cell 部分失败不触发）
        if _baseReason == gameconst.TeamDunCheckCondErrno.REWARD_NUM_CHECK_FAIL and self.client:
            self.client.onMemberNoRewardNum(dungeonNo)

        if self.cell:
            self.cell.checkCrossCrusadeConditionCell(teamId, dungeonNo, _baseReason)
        else:
            # failName：挑战次数不足时携带失败成员名（中心 abort 透传，
            # 游戏服据此向队长下发 onLackChallengeNum）
            _failName = ''
            if _baseReason == gameconst.TeamDunCheckCondErrno.REWARD_NUM_CHECK_FAIL:
                _failName = self.getRoleCacheAttr('name', '')
            gameengine.getCrossTeamStub(teamId).crusadeCheckResult(
                teamId,
                self.gbID,
                _baseReason,
                _failName
            )

    def crossCrusadeGo(self, context):
        # 全员检查通过：走通用跨服流程迁入跨服服（复用 reqCrossServer/token/超时机制）
        LOG_INFO('crossCrusadeGo', self.gbID, context)
        _reasonNo = gameconst.CrossServerReasonNo.ENTER_CROSS_CRUSADE
        if context.get('maxNum', 0) > 5:
            _reasonNo = gameconst.CrossServerReasonNo.ENTER_CROSS_CHIEF

        # dungeonNo 即副本场景 mapId：客户端凭此显示副本 loading 图
        # （onCrossServerResp 经 fetchMapId 解析）；镜像落地后经 createCell 讨伐分支
        # 直进副本克隆空间（见 _logonEnterCrossCrusadeDungeon）
        self.reqCrossServer(
            context.get('crossServerId', 0),
            _reasonNo,
            gameconst.CrossServerCBComponent.ENUM_BASE,
            'onEnterCrossCrusadeSpaceRemotely',
            (gameconfig.serverId(), context),
            context.get('dungeonNo', 0),
            0,
            context
        )

    def onEnterCrossCrusadeSpaceRemotely(self, serverId, context):
        # 跨服落地后调用（跨服服上的 Avatar 镜像）：
        LOG_INFO('onEnterCrossCrusadeSpaceRemotely', serverId, context)
        _teamId = context.get('crossTeamId', 0)
        if not _teamId:
            LOG_ERR('onEnterCrossCrusadeSpaceRemotely no teamId', context)
            # 用 ENUM_NONE：onCrossServerEnd 对 ENUM_BASE 会直接 getattr(self, '') 分发，
            # 空方法名会抛 AttributeError（归墟回程即用 ENUM_NONE 无回调形态）
            self.gobackServer(gameconst.CrossServerCBComponent.ENUM_NONE, '', ())
            return

        # 登录直进副本（createCell 讨伐分支）成功的镜像已在副本空间内，跳过重复进本
        if formula.inDungeonScene(self.baseSpaceNo) and \
                formula.fetchMapId(self.baseSpaceNo) == context.get('dungeonNo', 0):
            LOG_INFO('onEnterCrossCrusadeSpaceRemotely already in crusade space', self.baseSpaceNo)
            return

        gameengine.getCrossTeamStub(context.get('crossTeamId', 0)).enterCrusadeSpace(
            self,
            _teamId,
            self.gbID,
            context
        )

    # ------------------------------------------------------------------
    # 讨伐：跨服镜像登录直进副本（空间先于迁移创建，见 createCell 讨伐分支）
    # ------------------------------------------------------------------

    def _logonEnterCrossCrusadeDungeon(self):
        # 跨服讨伐镜像登录：直接落已建好的副本克隆空间，跳过出生图分线落地；
        # cell 由 CrossTeamStub 反查簿记后经 Space.createCellNearSelf 创建
        # （照新手锁副本 _enterNewbieDungeon 的异步落地模式）
        _context = self.getPersistentMiscProp(gameconst.EntityPropsEnum.crossServerExtra, None) or {}
        _teamId = _context.get('crossTeamId', 0)
        if not _teamId or not _context.get('dungeonNo'):
            return False

        LOG_INFO('logon enter cross crusade dungeon direct', _teamId, _context.get('dungeonNo'))
        gameengine.getCrossTeamStub(_teamId).logonEnterCrusadeDungeon(
            self,
            self.gbID,
            _context
        )
        return True

    def enterCrusadeDungeonOnLogon(self, spaceBox, spaceMgrBox, spaceNo, context):
        # CrossTeamStub 查得簿记后回调：cellData 指向副本克隆空间并借 Space 实体直接建 cell，
        # 进本收尾（镜像设置/空间登记/founders 簿记）由 cell 登录回调 onLogonEnterCrusadeDungeonCB 完成
        LOG_INFO('enterCrusadeDungeonOnLogon', spaceNo)
        self.cellData['spaceNo'] = spaceNo
        _pos, _dir = formula.getSpaceBornPosAndDir(formula.fetchMapId(spaceNo))
        self.cellData['position'] = _pos
        self.cellData['direction'] = _dir
        self.addCreateCellCB(
            'onLogonEnterCrusadeDungeonCB',
            (spaceNo, spaceMgrBox.id, context)
        )
        spaceBox.createCellNearSelf(self)

    def onCrossCrusadeLogonEnterFail(self):
        # 直进副本失败兜底（簿记缺失：空间已销毁/已结算，多为中心中止与迁移的竞态）：
        # 落出生图分线收容镜像（与跨服迁移前的老落地路径一致），
        # 后续由跨服 map check 超时踢回本服
        LOG_ERR('onCrossCrusadeLogonEnterFail', self.gbID)
        _lineType = utils.getPlayerBornMapId()
        _extra = {'isLogin': 1, 'position': self.cellData.get('position')}
        gameengine.getLineStub(_lineType).autoSwitchLine(
            self,
            self.gbID,
            0,
            _extra,
            'onLogonGetLineNo',
            (_lineType, _extra)
        )

    # ------------------------------------------------------------------
    # 讨伐：进本落地埋点与活动计数（旧组队系统下线时随 iCrusade.onEnterCrusadeDungeon/
    # iChief.onEnterChiefDungeon 删除，现挂到统一进本入口 Avatar.onEnterDungeon 补回）
    # ------------------------------------------------------------------

    def onTrackTeamDungeonEnter(self, spaceNo, extra):
        # 第一道过滤：非跨服组队线（单人副本等 extra 无 crossTeamId）直接放行
        if not extra or not extra.get('crossTeamId'):
            return

        # 小队线/首领线按副本配置判定（镜像登录直进链 extra 无 raidId，不能靠它区分）
        dungeonNo = formula.parseDungeonNoBySpaceNo(spaceNo)
        _dVal = GP_GPD.datas.get(dungeonNo, {})
        _isRaid = gameconst.DungeonTypeJudge.isRaidDungeon(
            _dVal.get('type', 0),
            _dVal.get('enterType', 0)
        )
        _isTeam = gameconst.DungeonTypeJudge.isTeamDungeon(
            _dVal.get('type', 0),
            _dVal.get('enterType', 0)
        )
        if not _isRaid and not _isTeam:
            return

        # 跨服服镜像一律回本服 base 执行（与 Dungeon_Settlement 口径一致）：
        # 本服为门票/活动计数权威，且镜像上 accountEntity 为 None 取不到 distinctId
        if gameconfig.isCrossServer():
            self.syncMethodCallToLocalServerBase('onTrackTeamDungeonEnter', (spaceNo, extra))
            return

        LOG_INFO('onTrackTeamDungeonEnter', spaceNo, dungeonNo, extra.get('crossTeamId'))

        # unique_id 口径：旧链小队线取 teamUUID、首领线取 raidId，新链三者均等于 crossTeamId
        _uniqueId = extra.get('raidId') or extra.get('teamUUID') or extra.get('crossTeamId')
        if _isRaid:
            _playMode = gameconst.DungeonPlayModeEnum.CHIEF
            _ticketType = self.chiefInfo.getUsedTicketType()
            _ticketNum = self.chiefInfo.rewardNumber
            self.activityComplete(RBC_CFG.datas['raidBossChallengeActID']['value'])
        else:
            _playMode = gameconst.DungeonPlayModeEnum.CRUSADE
            _ticketType = self.crusadeInfo.getUsedTicketType()
            _ticketNum = self.crusadeInfo.rewardNumber
            self.activityComplete(TDC_CFG.datas['teamDunChallengeActID']['value'])

        # dungeon_type 恒落旧口径 CRUSADE/CHIEF（本服/跨服统一，不传 CROSS_*）；
        # ticket_num 为进本时点拥有的门票总数（未扣票）；
        # 门票消耗埋点（Dungeon_Ticket_Consume）已移至结算扣票成功点上报
        LogTrackingMgr.LogTrackingMgr.Dungeon_Entrance(
            self.gbID,
            self.accountEntity.clientDistinctId,
            _uniqueId,
            _playMode,
            dungeonNo,
            extra.get('spaceUUID'),
            spaceNo,
            self.gbID,
            _ticketType,
            _ticketNum,
            extra.get('joinType'),
            self.getTotalScore(),
            self.getRoleCacheAttr('level'),
            self.getRoleCacheAttr('name')
        )
