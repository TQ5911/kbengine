# -*- coding: utf-8 -*-
# 跨服组队副本 base 侧玩家接入 mixin（跨服组队全覆盖·第二步：自 iCrossTeamBase 迁入，行为不变）：
# - 讨伐条件检查的 base 部分（奖励次数/门票），跨服迁移与落地（reqCrossServer 体系）；
# - 跨服镜像登录直进副本（空间先于迁移创建，createCell 讨伐分支）与失败兜底。
# 跨服队伍聊天与 Stub 下行中继等组队逻辑留在 iCrossTeamBase，本模块只收副本-玩家接入点。

from KBEDebug import *

import utils
import gameengine
import gameconst
import gameconfig
import formula


class ImpCrossTeamDungeonBase(object):

    # ------------------------------------------------------------------
    # 讨伐（无确认弹窗：条件检查全部通过即进本）
    # ------------------------------------------------------------------

    def checkCrossCrusadeCondition(self, teamId, dungeonNo):
        # 中心下发的条件检查：base 部分（奖励次数/门票）后转 cell 部分（战斗状态/传送条件）
        LOG_INFO('checkCrossCrusadeCondition', self.gbID, teamId, dungeonNo)
        _baseReason = gameconst.TeamDunCheckCondErrno.UNKNOWN

        # 奖励次数检查（对照 impTeamDungeon.getCurrentActRewardStatus 的 CRUSADE 分支）
        self.onTryAddUseCoinTimesFreeTicket(gameconst.RecoveryTicketSubType.CRUSADE)
        if not self.crusadeInfo.isCanTakeReward():
            _baseReason = gameconst.TeamDunCheckCondErrno.REWARD_NUM_CHECK_FAIL

        if self.cell:
            self.cell.checkCrossCrusadeConditionCell(teamId, dungeonNo, _baseReason)
        else:
            gameengine.getCrossTeamStub(teamId).crusadeCheckResult(
                teamId,
                self.gbID,
                _baseReason
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
