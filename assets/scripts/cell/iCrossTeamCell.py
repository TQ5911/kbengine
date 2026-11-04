# -*- coding: utf-8 -*-
# 跨服组队 cell 侧 mixin：
# - 客户端入口（applyCreateCrossTeam 等）：本地校验（互斥/门槛/密码）后直连本服 CrossTeamStub
#   （照旧本服组队 cell 直连队伍 stub 的模式，不再绕行 Avatar base）；
# - 承接本服 CrossTeamStub 下行（onCrossTeamInfoUpdate 等），维护 crossTeamInfo 属性
#   （CELL_PRIVATE，全量/增量变更均经结构化 ClientMethods 下发），事件类消息经 ClientMethods 下发；
# - 互斥：仅校验是否已在其他跨服队伍（crossTeamId 镜像；本服组队/组团体系已删除）；
# - 状态同步：在队期间 1s 定时检查自身状态（血量/spaceNo+position 等），与上次上报快照
#   对比有实质变动（血量变动超阈值/位置移动超阈值/其余字段变化）才同步本服 Stub，由 Stub 聚合上报中心；
# - 离线即退队：_offline 时上报 memberOffline；登录自动恢复
# 讨伐副本接入（发起/退出入口、条件检查应答、落地收尾与 trap）已迁至 cell/impCrossTeamDungeonCell.py（跨服组队全覆盖·第二步）。

import KBEngine
from KBEDebug import *

import time

import gameengine
import gameconst
import gametimer
import gameconfig
import dataUtils
import utils

import teamMatch_activity as TMACTD
import teamMatch_matchConfig as TM_MCD
import message_Message_def as MMD
import gamedecorator
import crossTeam
import dungeonSrc
import formula


class ICrossTeamCell(object):
    def sendTeamInfo(self, isRelogin):
        gameengine.getCrossTeamStub(self.gbId).queryPlayerTeam(self.base, self.gbId)

    # ------------------------------------------------------------------
    # 通用校验/信息/属性工具
    # ------------------------------------------------------------------

    def _crossTeamId(self):
        return self.crossTeamInfo.teamId if self.crossTeamInfo else 0

    def _isCrossTeamCaptain(self):
        return self._crossTeamId() != 0 and self.crossTeamInfo.captainGbId == self.gbId

    def _checkCrossTeamMutex(self):
        # 互斥校验：已在其他跨服队伍时禁止操作（本服组队/组团体系已删除，旧队恒不存在）
        if self._crossTeamId():
            LOG_WARN('cross team mutex check fail, already in cross team', self._crossTeamId())
            return False

        return True

    def _getTeamUpCreating(self):
        # 无队邀请组队内存状态（user_type/crossTeam.py TeamUpCreating）惰性创建：
        # Avatar cell 初始化路径多，不预初始化；离队/解散时整体置 None 清残留
        # （onCrossTeamLeave/onCrossTeamDisband）
        _tuc = getattr(self, 'teamUpCreating', None)
        if _tuc is None:
            _tuc = crossTeam.TeamUpCreating()
            self.teamUpCreating = _tuc
        return _tuc

    def _sendCrossTeamMsg(self, msgKey, args):
        # 队伍频道/事件消息：经 cell 的 showMsg 按 message_chatMessage 频道配置下发。
        # 队伍事件在每个成员的 cell 上各自落地一次，天然等价旧本服组队的全员广播
        if not self.client:
            return
        self.showMsg(TM_MCD.datas[msgKey]['value'], args)

    def _getCrossTeamPlayerInfoDic(self):
        return {
            'gbId': self.gbId,
            'playerName': self.name,
            'score': self.getTotalScore(),
            'level': self.level,
            'school': self.school,
            # 血量快照随入队请求上行，作为中心首个全量数据（后续由状态上报覆盖）
            'hp': self.hp,
            'maxHp': self.fullHp,
            # 聊天 avatarInfo/成员展示字段（客户端接口对齐补充）；
            # openId 照旧本服组队现状占位
            'sex': self.sex,
            'picFrameId': self.appearance.outfitData.picFrameId,
            'openId': 'openId',
        }

    def _getCrossTeamMaxNum(self, target):
        _default = 5
        _targetInfo = TMACTD.datas.get(target)
        if _targetInfo:
            return _targetInfo.get('crossMaxPlayer', _default)

        return _default

    def _isCrossTeamLineUnlocked(self, isRaid):
        # 按队伍线别查对应 UI 解锁位（小队线=组队+魔物巢穴，团队线=团队+首领巢穴）
        if isRaid:
            _uiId = dataUtils.getRaidConstDataValue("raidUIVisibleId")
            _dungeonUiId = dataUtils.getRaidConstDataValue("raidDungeonUIVisibleId")
        else:
            _uiId = dataUtils.getRaidConstDataValue("teamUIVisibleId")
            _dungeonUiId = dataUtils.getRaidConstDataValue("teamDungeonUIVisibleId")

        return self._isUIVisibleStrCell(_uiId, False) and self._isUIVisibleStrCell(_dungeonUiId, False)

    def _isCrossTeamTargetUnlocked(self, target):
        # 组队目标对应玩法的系统解锁判定（邀请/发起进本共用口径）：
        # 自设目标（<=PARE_ACTIVITY_ID）不做解锁判定，其余按队伍线别判定
        if target <= gameconst.PARE_ACTIVITY_ID:
            return True

        _isRaid = self._getCrossTeamMaxNum(target) > gameconst.TEAM_MEMBER_NUM_VS_RAID
        return self._isCrossTeamLineUnlocked(_isRaid)

    def _buildCrossTeamInfoProp(self, teamInfoDict):
        # Stub 下发的队伍缓存 dict -> crossTeamInfo 属性对象（CrossTeamCacheVal）
        _cacheVal = crossTeam.CrossTeamCacheVal()
        _cacheVal.fromStreamDict(teamInfoDict)
        return _cacheVal

    # ------------------------------------------------------------------
    # 统一队伍访问层（第四步 D4-1）
    # 本服组队/组团体系已废弃，"当前生效队伍"只取跨服队（crossTeamInfo 缓存）
    # ------------------------------------------------------------------

    def getActiveTeamType(self):
        # 当前生效队伍类型：在跨服队返回 TeamType.CROSS_TEAM，否则 TeamType.DEFAULT
        if self._crossTeamId():
            return gameconst.TeamType.CROSS_TEAM
        return gameconst.TeamType.DEFAULT

    def getActiveTeamId(self):
        # 统一队伍 ID：跨服队 crossTeamId，不在队返回 0
        return self._crossTeamId()

    def getTeammateGbIdSet(self):
        # 全队成员 gbId 集合（含本人，是否排除自己由消费方自行处理），不在队返回空 set
        if not self._crossTeamId():
            return set()
        return set(self.crossTeamInfo.memberDict.keys())

    def isTeammate(self, gbId):
        # 统一队友判定（友军保护/技能目标/首刀归属等用）
        if not self._crossTeamId():
            return False
        return self.crossTeamInfo.isInTeam(gbId)

    def getActiveCaptainGbId(self):
        # 队长 gbId，不在队返回 0
        if not self._crossTeamId():
            return 0
        return self.crossTeamInfo.captainGbId

    def getActiveTeamMemberCount(self):
        # 全队人数，不在队返回 0
        if not self._crossTeamId():
            return 0
        return self.crossTeamInfo.howManyMember()

    def getActiveTeamMemberLevels(self):
        # 全队成员等级 {gbId: level}（组队任务难度用），不在队返回空 dict
        if not self._crossTeamId():
            return {}
        return {_gbId: _m.level for _gbId, _m in self.crossTeamInfo.memberDict.items()}

    def inCrossTeam(self, gbid = 0):
        # 跨服小队判定：在队且人数上限<=5（经验/掉落分摊等按队/团区分需求的门控）
        targetGbid = (gbid or self.gbId)
        if not self.crossTeamInfo or self.crossTeamInfo.maxNum > gameconst.TEAM_MEMBER_NUM_VS_RAID:
            return False

        return targetGbid in self.crossTeamInfo.memberDict

    def inCrossRaid(self, gbid = 0):
        # 跨服团队判定：在队且人数上限>5（对齐本服团线别，D4-2）
        targetGbid = (gbid or self.gbId)
        if not self.crossTeamInfo or self.crossTeamInfo.maxNum <= gameconst.TEAM_MEMBER_NUM_VS_RAID:
            return False

        return targetGbid in self.crossTeamInfo.memberDict

    def broadcastToTeammates(self, comp, func, args, excludeGbIds=()):
        # 访问层"广播给队友"通道：名单取本地跨服缓存，经本服 PlayerStub 按 gbId 路由
        # 到成员 base/cell。仅覆盖成员当前所在服=本服的场景（副本内全队真实迁移同服，
        # 必然覆盖；成员分散各服时他服成员收不到）
        _gbIds = self.getTeammateGbIdSet() - set(excludeGbIds)
        if not _gbIds:
            return

        _stub = gameengine.getGlobalBase('PlayerStub')
        if comp == gameconst.BASE:
            _stub.doOnOthersBase(list(_gbIds), func, args, None, '', ())
        else:
            _stub.doOnOthersCell(list(_gbIds), func, args, None, '', ())

    # ------------------------------------------------------------------
    # 对外数据供给（base 经 RPC 调用，已在 iAvatarCrossTeam.def 注册）
    # ------------------------------------------------------------------

    def onGetCrossAvatarInterInfo(self, box, myAccountName):
        # 玩家详情组包（承接旧本服组队的玩家详情接口）：
        # 小队填 team*、大队填 raid*；客户端 teamId 分支显示优先，
        # 大队若同时填 teamId 会被误按 5 人队展示
        _props = {
            'school': self.school,
            'gbId': self.gbId,
            'sex': self.sex,
            'level': self.level,
            'picFrameId': self.appearance.outfitData.picFrameId,
            'name': self.name,
            'openId': myAccountName,
            'offlineTime': 0,
            'id': self.id,
        }

        _inTeam = self.inCrossTeam()
        _inRaid = self.inCrossRaid()
        _props.update({
            'teamId': self.getActiveTeamId() if _inTeam else 0,
            'teamAmount': self.getActiveTeamMemberCount() if _inTeam else 0,
            'teamTarget': self.crossTeamInfo.target if _inTeam else 0,
            'raidTarget': self.crossTeamInfo.target if _inRaid else 0,
            'isRaidLeader': _inRaid and self.getActiveCaptainGbId() == self.gbId,
            'raidId': self.getActiveTeamId() if _inRaid else 0,
            'raidAmount': self.getActiveTeamMemberCount() if _inRaid else 0,
            'guildName': self.guildName,
            'bountyId': self.cellPreyInfo.uuid if self.cellPreyInfo else 0,
            'fromServerId': self.fromServerId,
            'curServerId': gameconfig.serverId(),
        })
        LOG_DBG('onGetCrossAvatarInterInfo ', _props)
        box.getInterInfoOnline(_props)

    def checkCrossTeamInviteCondition(self, inviterBox, target, minLevel, minScore):
        # 邀请条件判定（在被邀请人 cell 上执行，经 PlayerStub 路由；发起人 base 邮箱随参带入，
        # 结果经 inviterBox.cell 回调）：功能未解锁/等级不足/战力不足分别对应
        # teamInviteQuestMsg/teamInviteLevelMsg/teamInviteScoreMsg，全部通过回 0
        # （镜像本服 procInviteTeamMsg 的判定口径，门槛取发起人队伍设置的 minLevel/minScore）
        _msgId = 0
        if not self._isCrossTeamTargetUnlocked(target):
            _msgId = int(TM_MCD.datas['teamInviteQuestMsg']['value'])

        if not _msgId and self.level < minLevel:
            LOG_WARN('checkCrossTeamInviteCondition, level failed:', self.level, minLevel)
            _msgId = int(TM_MCD.datas['teamInviteLevelMsg']['value'])

        if not _msgId:
            _totalScore = self.getTotalScore()
            if _totalScore < minScore:
                LOG_WARN('checkCrossTeamInviteCondition, score failed:', _totalScore, minScore)
                _msgId = int(TM_MCD.datas['teamInviteScoreMsg']['value'])

        inviterBox.cell.onCrossTeamInviteCheckResult(self.gbId, self.name, _msgId)

    def onCrossTeamInviteCheckResult(self, gbId, name, msgId):
        # 邀请条件判定回调（被邀请人 cell -> 发起人 cell）：
        # 不通过提示对应 msg（附被邀请人名字）；通过则复核仍在队后正常发中心
        LOG_INFO('onCrossTeamInviteCheckResult', gbId, msgId)
        if msgId:
            self.showMsg(msgId, [name])
            return

        if not self._crossTeamId():
            LOG_WARN('onCrossTeamInviteCheckResult, not in cross team')
            return

        # 目前仅支持邀请本服玩家
        gameengine.getCrossTeamStub(self._crossTeamId()).inviteMember(
            self.base,
            self._crossTeamId(),
            self.gbId,
            gbId,
            gameconfig.serverId()
        )

    # ------------------------------------------------------------------
    # 客户端入口（已在 iAvatarCrossTeam.def 注册 Exposed），直连本服 CrossTeamStub
    # ------------------------------------------------------------------

    @utils.isMyself
    @gamedecorator.crossServer
    @gamedecorator.limitcall(0.5)
    def applyCreateCrossTeam(self, exposed, target, minLevel, minScore, password, intro, autoEnter):
        LOG_INFO('applyCreateCrossTeam', target, minLevel, minScore, autoEnter)
        self._doCreateCrossTeam(target, minLevel, minScore, password, intro, autoEnter)

    def _doCreateCrossTeam(self, target, minLevel, minScore, password, intro, autoEnter):
        # 建队主体（Exposed 入口与无队邀请流程自动建队 _teamUpAutoCreate 共用）：
        # 互斥校验保留在本体内，自动建队不绕过
        if not self._checkCrossTeamMutex():
            return

        _matchData = TMACTD.datas.get(target)
        if not _matchData:
            LOG_WARN('applyCreateCrossTeam, invalid target', target)
            return

        # 本服链路（第三步）：isCross 读配表固化（跨服走迁移链路，本服走本服链路）；
        # dunServer 为副本创建目标服：跨服=跨服服 id，本服=本服 id（创建后不可改）
        _isCross = bool(_matchData.get('isCrossServer'))
        if _isCross:
            _dunServer = gameconfig.getCrossServerId()
        else:
            _dunServer = gameconfig.serverId()

        if not dataUtils.checkTeamPassword(password):
            LOG_WARN('applyCreateCrossTeam, illegal password', password)
            return

        # 优先复用无队邀请流程预分配的 teamId（本 cell 一切建队含流程外手动建队）；
        # 多份接受触发的重复建队打在同一个 id 上，中心 DUPLICATED_TEAM 天然去重
        _tuc = self._getTeamUpCreating()
        _teamId = _tuc.teamId or KBEngine.genUUID64()
        # 公开队伍默认开启自动匹配（私密队伍不进列表/匹配池）
        _autoMatch = (password == '')
        _memberInfo = self._getCrossTeamPlayerInfoDic()
        # isCross/dunServer 借 memberInfo（PY_DICT）随 createTeam 透传到 Stub
        # （CrossTeamStub.def 的 createTeam 签名不变，Stub 组 CreateTeamRequest 时取出上行）
        _memberInfo['isCross'] = _isCross
        _memberInfo['dunServer'] = _dunServer
        gameengine.getCrossTeamStub(_teamId).createTeam(
            self.base,
            _teamId,
            target,
            minLevel,
            minScore,
            password,
            intro,
            _autoMatch,
            self._getCrossTeamMaxNum(target),
            self._getCrossTeamDungeonMap(target),
            autoEnter,
            _memberInfo
        )

    @utils.isMyself
    @gamedecorator.crossServer
    @gamedecorator.limitcall(0.5)
    def applyJoinCrossTeam(self, exposed, teamId, password, applySource):
        LOG_INFO('applyJoinCrossTeam', teamId, applySource)
        if not self._checkCrossTeamMutex():
            return

        if not dataUtils.checkTeamPassword(password):
            LOG_WARN('applyJoinCrossTeam, illegal password', password)
            return

        gameengine.getCrossTeamStub(teamId).applyJoinTeam(
            self.base,
            teamId,
            password,
            self._getCrossTeamPlayerInfoDic(),
            applySource
        )

    @utils.isMyself
    @gamedecorator.crossServer
    def replyCrossTeamJoin(self, exposed, gbId, bAgree):
        LOG_INFO('replyCrossTeamJoin', gbId, bAgree)
        if not self._crossTeamId():
            LOG_WARN('replyCrossTeamJoin, not in cross team')
            return

        # 队长身份由中心复核（replyApply 校验 captainGbId）
        gameengine.getCrossTeamStub(self._crossTeamId()).replyJoinApply(
            self.base,
            self._crossTeamId(),
            self.gbId,
            gbId,
            bAgree
        )

    @utils.isMyself
    @gamedecorator.crossServer
    @gamedecorator.limitcall(0.5)
    def applyInviteCrossTeam(self, exposed, gbId, name):
        LOG_INFO('applyInviteCrossTeam', gbId, name)
        if self._crossTeamId():
            # 在队：走现有条件判定链路（等级/战力/功能是否解锁），
            # 结果回调 onCrossTeamInviteCheckResult：通过才发中心，不通过提示 msg；
            # 目标不在线（PlayerStub 路由失败）的场景不处理
            gameengine.getGlobalBase('PlayerStub').doOnOthersCell(
                [gbId],
                'checkCrossTeamInviteCondition',
                (self.base, self.crossTeamInfo.target,
                 self.crossTeamInfo.minLevel, self.crossTeamInfo.minScore),
                None, '', ()
            )
            return

        # 无队邀请组队（方案 §4.2-1，仅限同服邀请）：中心纯透传，对方应答同意后服务端自动建队闭环；
        # 无队分支不做对 B 的条件预判（功能解锁/挂机/副本中由 B 客户端弹窗层自动拒绝；
        # B 离线仅记日志，不给邀请人提示，决策 7）
        if gbId == self.gbId:
            LOG_WARN('applyInviteCrossTeam, invite myself', gbId)
            return

        if not self._checkCrossTeamMutex():
            return

        # 首次发起时预分配 teamId（本 cell 后续建队优先复用）；同一 id 继续邀其他人（先到先得）
        _tuc = self._getTeamUpCreating()
        if not _tuc.teamId:
            _tuc.teamId = KBEngine.genUUID64()
        _tuc.invitees[gbId] = utils.curTS()
        gameengine.getCrossTeamStub(self.gbId).teamUpInvite(
            self.base,
            _tuc.teamId,
            self._getCrossTeamPlayerInfoDic(),
            gbId
        )

    @utils.isMyself
    @gamedecorator.crossServer
    @gamedecorator.limitcall(0.5)
    def replyCrossTeamInvite(self, exposed, teamId, bAgree, inviterGbId, inviteType):
        LOG_INFO('replyCrossTeamInvite', teamId, bAgree, inviterGbId, inviteType)
        if inviteType == gameconst.InviteType.GUILD:
            # 帮会邀请（游戏服自闭环广播，中心无邀请记录，不进中心 replyInvite）：
            # 拒绝直接丢弃；同意转申请入队审批流（队长审批，applySource=招募）
            if bAgree:
                self.applyJoinCrossTeam(self.id, teamId, '', gameconst.TeamJoinType.RECRUIT)
            return

        if inviteType == gameconst.InviteType.TEAM_UP:
            # 无队邀请应答（方案 §4.2-2）：inviteIns 记录校验（无记录/teamId 不一致直接丢弃，
            # 防伪造/重复应答），消费后先发应答（拒绝给 A 提示；同意触发 A 自动建队），
            # 同意再凭预分配 teamId 先试直进（队已建好则秒进，无需等就绪通知）
            _tuc = self._getTeamUpCreating()
            _rec = _tuc.inviteIns.pop(inviterGbId, None)
            if _rec is None or _rec[0] != teamId:
                LOG_WARN('replyCrossTeamInvite, no/invalid team-up invite record', teamId, inviterGbId)
                return

            if bAgree:
                if not self._checkCrossTeamMutex():
                    return
                _tuc.accepted[teamId] = (inviterGbId, utils.curTS())

            gameengine.getCrossTeamStub(self.gbId).replyTeamUpInvite(
                self.base,
                teamId,
                inviterGbId,
                self._getCrossTeamPlayerInfoDic(),
                bAgree,
                inviteType,
                gameconst.TeamUpReplyReason.REJECT
            )
            if bAgree:
                gameengine.getCrossTeamStub(teamId).teamUpReqJoin(
                    self.base,
                    teamId,
                    self._getCrossTeamPlayerInfoDic()
                )
            return

        if bAgree and not self._checkCrossTeamMutex():
            return

        gameengine.getCrossTeamStub(teamId).replyInvite(
            self.base,
            teamId,
            self._getCrossTeamPlayerInfoDic(),
            bAgree,
            inviteType
        )

    @utils.isMyself
    @gamedecorator.crossServer
    @gamedecorator.limitcall(0.5)
    def tryApplyInviteCrossGuild(self, exposed):
        # 邀请帮会成员入团（对应旧本服帮会邀请入团接口，执行清单问题 13）：
        # 仅团队线可发起；游戏服自闭环广播（帮会成员本服可达），不经组队中心；
        # 被邀请人接受后走 applyJoinCrossTeam 申请审批流（replyCrossTeamInvite 按 inviteType 分流）
        LOG_INFO('tryApplyInviteCrossGuild', self._crossTeamId())
        if not self.inCrossRaid():
            LOG_WARN('tryApplyInviteCrossGuild, not in cross raid')
            return

        if self.crossTeamInfo.inDungeon:
            LOG_WARN('tryApplyInviteCrossGuild, in dungeon')
            return

        if not self.guildUUID or not self.guildBoxCell:
            LOG_WARN('tryApplyInviteCrossGuild, not in guild')
            return

        # 邀请弹窗信息（CROSS_TEAM_INVITE_VAL 同构）：邀请人信息 + 队伍 teamId/target
        _info = self._getCrossTeamPlayerInfoDic()
        _inviteInfo = {
            'teamId': self._crossTeamId(),
            'target': self.crossTeamInfo.target,
            'gbId': self.gbId,
            'serverId': gameconfig.serverId(),
            'playerName': _info['playerName'],
            'school': _info['school'],
            'level': _info['level'],
            'score': _info['score'],
            'sex': _info['sex'],
            'inviteType': gameconst.InviteType.GUILD,
        }
        self.guildBoxCell.tryApplyInviteCrossGuild(self.gbId, _inviteInfo)

    def doApplyCrossGuildInvite(self, inviteInfo):
        # 帮会邀请入团落地（Guild base 链路）：复核不在队后弹邀请窗；
        # 被邀请人接受后回 replyCrossTeamInvite（inviteType=GUILD），服务端分流走申请审批流
        if self._crossTeamId():
            return

        if self.client:
            self.client.onCrossTeamInvite(inviteInfo)

    @utils.isMyself
    @gamedecorator.crossServer
    @gamedecorator.limitcall(0.5)
    def applyLeaveCrossTeam(self, exposed):
        LOG_INFO('applyLeaveCrossTeam', self._crossTeamId())
        if not self._crossTeamId():
            return

        gameengine.getCrossTeamStub(self._crossTeamId()).leaveTeam(
            self.base,
            self._crossTeamId(),
            self.gbId
        )

    @utils.isMyself
    @gamedecorator.crossServer
    @gamedecorator.limitcall(0.5)
    def applyKickCrossTeamMember(self, exposed, gbId):
        LOG_INFO('applyKickCrossTeamMember', gbId)
        if not self._crossTeamId():
            return

        # 队长身份在中心复核前的本服校验由本服 cell 完成（非队长直接拦截）
        if not self._isCrossTeamCaptain():
            LOG_WARN('applyKickCrossTeamMember, not captain')
            return

        gameengine.getCrossTeamStub(self._crossTeamId()).kickMember(
            self.base,
            self._crossTeamId(),
            gbId,
            self.gbId
        )

    @utils.isMyself
    @gamedecorator.crossServer
    @gamedecorator.limitcall(0.5)
    def applyTransferCrossCaptain(self, exposed, gbId):
        LOG_INFO('applyTransferCrossCaptain', gbId)
        if not self._crossTeamId():
            return

        if not self._isCrossTeamCaptain():
            LOG_WARN('applyTransferCrossCaptain, not captain')
            return

        gameengine.getCrossTeamStub(self._crossTeamId()).transferCaptain(
            self.base,
            self._crossTeamId(),
            gbId,
            self.gbId
        )

    @utils.isMyself
    @gamedecorator.crossServer
    @gamedecorator.limitcall(0.5)
    def applyBecomeCrossCaptain(self, exposed, gbId):
        # 申请成为队长（本服 applyBecomeCaptain 对应）：gbId 为客户端回传占位，以本人 gbId 为准；
        # 中心不留存待应答记录，校验通过后直接把申请提示推给队长（onCrossBecomeCaptainAsk）
        LOG_INFO('applyBecomeCrossCaptain', gbId)
        if not self._crossTeamId():
            return

        if self._isCrossTeamCaptain():
            LOG_WARN('applyBecomeCrossCaptain, already captain')
            return

        gameengine.getCrossTeamStub(self._crossTeamId()).applyBecomeCaptain(
            self.base,
            self._crossTeamId(),
            self.gbId
        )

    @utils.isMyself
    @gamedecorator.crossServer
    @gamedecorator.limitcall(0.5)
    def replyBecomeCrossCaptain(self, exposed, gbId, bAgree):
        # 队长应答"申请成为队长"（本服 replyBecomeCaptain 对应）：gbId=申请人；
        # 队长身份中心复核（本服缓存可能失效）
        LOG_INFO('replyBecomeCrossCaptain', gbId, bAgree)
        if not self._crossTeamId():
            return

        if not self._isCrossTeamCaptain():
            LOG_WARN('replyBecomeCrossCaptain, not captain')
            return

        gameengine.getCrossTeamStub(self._crossTeamId()).replyBecomeCaptain(
            self.base,
            self._crossTeamId(),
            self.gbId,
            gbId,
            bAgree
        )

    @utils.isMyself
    @gamedecorator.crossServer
    @gamedecorator.limitcall(0.5)
    def applyDisbandCrossTeam(self, exposed):
        LOG_INFO('applyDisbandCrossTeam', self._crossTeamId())
        if not self._crossTeamId():
            return

        if not self._isCrossTeamCaptain():
            LOG_WARN('applyDisbandCrossTeam, not captain')
            return

        gameengine.getCrossTeamStub(self._crossTeamId()).disbandTeam(
            self.base,
            self._crossTeamId(),
            self.gbId
        )

    @utils.isMyself
    @gamedecorator.crossServer
    @gamedecorator.limitcall(0.5)
    def applyConvertCrossTeamToRaid(self, exposed, target):
        # 小队转团队（本服 createRaidWithTeam 对应）：本地校验队长/小队线/非副本中/新目标合法，
        # 中心复核同口径；转换语义 = 退役旧小队 + 以新 teamId 登记新团队，
        # 成功后全员收全量 onCrossTeamInfoUpdate（含新 teamId/target/maxNum）
        LOG_INFO('applyConvertCrossTeamToRaid', self._crossTeamId(), target)
        if not self._crossTeamId():
            return

        if not self._isCrossTeamCaptain():
            LOG_WARN('applyConvertCrossTeamToRaid, not captain')
            return

        # 仅小队线可转（团队不可再转/降级）
        if not self.inCrossTeam():
            LOG_WARN('applyConvertCrossTeamToRaid, not squad line')
            return

        if self.crossTeamInfo.inDungeon:
            LOG_WARN('applyConvertCrossTeamToRaid, in dungeon')
            return

        if target == self.crossTeamInfo.target:
            LOG_WARN('applyConvertCrossTeamToRaid, same target', target)
            return

        _matchData = TMACTD.datas.get(target)
        if not _matchData:
            LOG_WARN('applyConvertCrossTeamToRaid, invalid target', target)
            return

        # 新目标须为团队线（人数上限>5，配表缺失时按默认 5 即拒绝）
        _maxNum = self._getCrossTeamMaxNum(target)
        if _maxNum <= gameconst.TEAM_MEMBER_NUM_VS_RAID:
            LOG_WARN('applyConvertCrossTeamToRaid, not raid target', target, _maxNum)
            return

        # isCross/dunServer 按新目标配表重算（同 createTeam 口径），与旧队一致性由中心复核
        _isCross = bool(_matchData.get('isCrossServer'))
        if _isCross:
            _dunServer = gameconfig.getCrossServerId()
        else:
            _dunServer = gameconfig.serverId()

        _newTeamId = KBEngine.genUUID64()
        gameengine.getCrossTeamStub(self._crossTeamId()).convertTeamToRaid(
            self.base,
            self._crossTeamId(),
            _newTeamId,
            target,
            _maxNum,
            self._getCrossTeamDungeonMap(target),
            _isCross,
            _dunServer,
            self.gbId
        )

    @utils.isMyself
    @gamedecorator.crossServer
    @gamedecorator.limitcall(0.5)
    def reqSetCrossTeamSettings(self, exposed, minLevel, minScore, intro, autoEnter, password):
        # 队伍设置：门槛/介绍/满员自动进本/密码（目标创建后不可改，不在本接口范围内）；
        # autoMatch 修改频率高，走 reqSetCrossTeamAutoMatch
        LOG_INFO('reqSetCrossTeamSettings', self._crossTeamId(), minLevel, minScore, autoEnter)
        if not self._crossTeamId():
            return

        if not dataUtils.checkTeamPassword(password):
            LOG_WARN('reqSetCrossTeamSettings, illegal password', password)
            return

        gameengine.getCrossTeamStub(self._crossTeamId()).setTeamSettings(
            self.base,
            self._crossTeamId(),
            minLevel,
            minScore,
            intro,
            autoEnter,
            self.gbId,
            password
        )

    @utils.isMyself
    @gamedecorator.crossServer
    @gamedecorator.limitcall(0.5)
    def reqSetCrossTeamAutoMatch(self, exposed, autoMatch):
        # 自动匹配开关（修改频率高，与队伍目标拆分）；队长身份由中心复核
        LOG_INFO('reqSetCrossTeamAutoMatch', self._crossTeamId(), autoMatch)
        if not self._crossTeamId():
            return

        gameengine.getCrossTeamStub(self._crossTeamId()).setAutoMatch(
            self.base,
            self._crossTeamId(),
            autoMatch,
            self.gbId
        )

    @utils.isMyself
    @gamedecorator.crossServer
    @gamedecorator.limitcall(0.5)
    def reqCrossTeamMatch(self, exposed, target):
        LOG_INFO('reqCrossTeamMatch', target)
        # 本服匹配状态判重（第一道拦截，中心 pool map 查重兜底）
        if self.crossTeamMatchTarget:
            LOG_WARN('reqCrossTeamMatch, already matching', self.crossTeamMatchTarget)
            return

        if not self._checkCrossTeamMutex():
            return

        if target <= 0 or target not in TMACTD.datas:
            LOG_WARN('reqCrossTeamMatch, invalid target', target)
            return

        self.crossTeamMatchTarget = target
        gameengine.getCrossTeamStub(self.gbId).enterMatchPool(
            self.base,
            target,
            self._getCrossTeamPlayerInfoDic()
        )

    @utils.isMyself
    @gamedecorator.crossServer
    @gamedecorator.limitcall(0.5)
    def reqStopCrossTeamMatch(self, exposed):
        LOG_INFO('reqStopCrossTeamMatch', self.crossTeamMatchTarget)
        if not self.crossTeamMatchTarget:
            return

        self.crossTeamMatchTarget = 0
        gameengine.getCrossTeamStub(self.gbId).leaveMatchPool(
            self.base,
            self.gbId
        )

    @utils.isMyself
    @gamedecorator.crossServer
    @gamedecorator.limitcall(0.5)
    def reqGetCrossTeamList(self, exposed, target):
        # 一波全量下发（问题记录#5）：回包由 Stub 经 base streamStringProxy 分片下发，不再经 cell
        LOG_INFO('reqGetCrossTeamList', target)
        gameengine.getCrossTeamStub(self.gbId).getTeamList(
            self.base,
            target
        )

    @utils.isMyself
    @gamedecorator.crossServer
    @gamedecorator.limitcall(0.5)
    def switchCrossTeamMicsMode(self, exposed, mode):
        # 麦模式切换（队长操作，队长身份校验在 cell 侧 crossTeamInfo 上完成）
        LOG_INFO('switchCrossTeamMicsMode', self._crossTeamId(), mode)
        if not self._isCrossTeamCaptain():
            LOG_WARN('switchCrossTeamMicsMode, not captain')
            return

        gameengine.getCrossTeamStub(self._crossTeamId()).setMicsMode(
            self.base,
            self._crossTeamId(),
            mode,
            self.gbId
        )

    @utils.isMyself
    @gamedecorator.crossServer
    @gamedecorator.limitcall(0.5)
    def reqSetCrossTeamMemberMicBlock(self, exposed, gbId, blocked):
        # 禁麦/解除禁麦（队长操作）：block/unblock 合并为一个入口，blocked=True 禁麦
        LOG_INFO('reqSetCrossTeamMemberMicBlock', self._crossTeamId(), gbId, blocked)
        if not self._isCrossTeamCaptain():
            LOG_WARN('reqSetCrossTeamMemberMicBlock, not captain')
            return

        gameengine.getCrossTeamStub(self._crossTeamId()).blockMic(
            self.base,
            self._crossTeamId(),
            gbId,
            blocked,
            self.gbId
        )

    @utils.isMyself
    @gamedecorator.crossServer
    @gamedecorator.limitcall(0.5)
    def reqAdjustCrossTeamMemberPos(self, exposed, srcGbId, srcGroupIdx, dstGbId, dstGroupIdx):
        # 成员位置调整（队长操作）：srcGbId/srcGroupIdx 为被调整成员，dstGbId/dstGroupIdx
        # 为目标成员/目标小组；dstGbId==0 表示移动到 dstGroupIdx 组末尾
        LOG_INFO('reqAdjustCrossTeamMemberPos', self._crossTeamId(),
                 srcGbId, srcGroupIdx, dstGbId, dstGroupIdx)
        if not self._crossTeamId():
            return
        if not self._isCrossTeamCaptain():
            LOG_WARN('reqAdjustCrossTeamMemberPos, not captain')
            return

        gameengine.getCrossTeamStub(self._crossTeamId()).adjustMemberPos(
            self.base,
            self._crossTeamId(),
            srcGbId,
            srcGroupIdx,
            dstGbId,
            dstGroupIdx,
            self.gbId
        )

    @utils.isMyself
    @gamedecorator.crossServer
    @gamedecorator.limitcall(0.1)
    def setCrossTeamWatchGroups(self, exposed, groupIdxs):
        # 客户端设置跨服队伍成员状态关注列表（小组下标，0 起始；空列表=不再更新成员状态）：
        # 每秒轮询（syncCrossTeamState）按此过滤，减少常态下行数据量。
        # 无符号字节再过滤，非法下标在中心过滤时天然不命中
        self.crossTeamWatchGroups = sorted({_g & 0x7f for _g in groupIdxs})
        LOG_INFO('setCrossTeamWatchGroups', self.gbId, self.crossTeamWatchGroups)

    # ------------------------------------------------------------------
    # 客户端接口对齐补充：新入口（跨服组队客户端接口对齐梳理.md §2.1）
    # ------------------------------------------------------------------

    def _setCrossTeamVoiceState(self, enableMics=None, enableSpeaker=None, inVoiceRoom=None):
        # 经本服 Stub 向中心同步自身语音状态；SetVoiceStateRequest 为三态全量写，
        # 未指定的维度带当前缓存值（中心只存不解读，变更经推送回全队后落地本地缓存）
        _member = self.crossTeamInfo.memberDict.get(self.gbId) if self.crossTeamInfo else None
        if enableMics is None:
            enableMics = _member.enableMics if _member else False
        if enableSpeaker is None:
            enableSpeaker = _member.enableSpeaker if _member else False
        if inVoiceRoom is None:
            inVoiceRoom = _member.inVoiceRoom if _member else False

        gameengine.getCrossTeamStub(self._crossTeamId()).setVoiceState(
            self.base,
            self._crossTeamId(),
            self.gbId,
            enableMics,
            enableSpeaker,
            inVoiceRoom
        )

    @utils.isMyself
    @gamedecorator.crossServer
    @gamedecorator.limitcall(0.5)
    def reqGetCrossTeamPreview(self, exposed, teamId):
        # 队伍预览（决策 D4）：按需查询指定队伍成员列表，不随列表下发；
        # 经 Stub 走 queryTeam 的 teamId 直查路径，回包走 onCrossTeamPreview
        LOG_INFO('reqGetCrossTeamPreview', teamId)
        if teamId <= 0:
            return

        gameengine.getCrossTeamStub(teamId).queryTeamById(
            self.base,
            teamId
        )

    @utils.isMyself
    @gamedecorator.crossServer
    @gamedecorator.limitcall(0.5)
    def turnOnCrossTeamMics(self, exposed):
        # 成员自己开麦（本服 turnOnTeamMics 对应）
        LOG_INFO('turnOnCrossTeamMics', self._crossTeamId())
        if not self._crossTeamId():
            return

        # 队长麦（LEADER）模式下仅队长可开麦
        # （语义照本服 user_type/team.py turnOnTeamMemberMics 的 LEADER 分支）
        if self.crossTeamInfo.micsMode == gameconst.TeamMicsModeEnum.LEADER and \
                not self._isCrossTeamCaptain():
            LOG_WARN('turnOnCrossTeamMics, leader mics mode limit')
            return

        self._setCrossTeamVoiceState(enableMics=True)

    @utils.isMyself
    @gamedecorator.crossServer
    @gamedecorator.limitcall(0.5)
    def turnOffCrossTeamMics(self, exposed):
        # 成员自己关麦（本服 turnOffTeamMics 对应）
        LOG_INFO('turnOffCrossTeamMics', self._crossTeamId())
        if not self._crossTeamId():
            return

        self._setCrossTeamVoiceState(enableMics=False)

    @utils.isMyself
    @gamedecorator.crossServer
    @gamedecorator.limitcall(0.5)
    def reqUpdateCrossTeamVoiceRoomState(self, exposed, teamId, voiceFlags):
        # 语音房状态位图同步（旧本服语音房状态接口已随旧组队删除，跨服走此链路）；
        # 位定义与旧本服一致：
        # 0x01=inVoiceRoom, 0x02=enableMics, 0x04=enableSpeaker
        LOG_INFO('reqUpdateCrossTeamVoiceRoomState', teamId, voiceFlags)
        if teamId <= 0 or teamId != self._crossTeamId():
            return

        self._setCrossTeamVoiceState(
            enableMics=(voiceFlags & 0x02) != 0,
            enableSpeaker=(voiceFlags & 0x04) != 0,
            inVoiceRoom=(voiceFlags & 0x01) != 0
        )

    @utils.isMyself
    @gamedecorator.crossServer
    @gamedecorator.limitcall(0.5)
    def reqGetCrossTeamApplyList(self, exposed):
        # 申请列表拉取（仅队长；断线/换队长后重建），回包走 onCrossTeamApplyList
        LOG_INFO('reqGetCrossTeamApplyList', self._crossTeamId())
        if not self._isCrossTeamCaptain():
            LOG_WARN('reqGetCrossTeamApplyList, not captain')
            return

        gameengine.getCrossTeamStub(self._crossTeamId()).getApplyList(
            self.base,
            self._crossTeamId(),
            self.gbId
        )

    @utils.isMyself
    @gamedecorator.crossServer
    @gamedecorator.limitcall(0.5)
    def reqJoinCrossTeam(self, exposed, teamId, password):
        # 免审批快速加入（本服 reqJoinTeam 对应）：不落地申请记录，中心校验通过直接入队；
        # 有密码的队凭密码直入（未携带->需要密码/不匹配->密码错误，细分码与审批流一致）
        LOG_INFO('reqJoinCrossTeam', teamId)
        if not self._checkCrossTeamMutex():
            return

        if not dataUtils.checkTeamPassword(password):
            LOG_WARN('reqJoinCrossTeam, illegal password', password)
            return

        gameengine.getCrossTeamStub(teamId).reqJoinTeam(
            self.base,
            teamId,
            password,
            self._getCrossTeamPlayerInfoDic()
        )

    @utils.isMyself
    @gamedecorator.crossServer
    @gamedecorator.limitcall(0.5)
    def clearCrossApplyJoinDic(self, exposed):
        # 一键清空申请列表（本服 clearApplyJoinDic 对应，仅队长）：
        # 队长侧逐个 applyRemoveNotify 剔除（申请人侧不再通知），结果回 onCrossTeamOpResult
        LOG_INFO('clearCrossApplyJoinDic', self._crossTeamId())
        if not self._isCrossTeamCaptain():
            LOG_WARN('clearCrossApplyJoinDic, not captain')
            return

        gameengine.getCrossTeamStub(self._crossTeamId()).clearApplyList(
            self.base,
            self._crossTeamId(),
            self.gbId
        )

    @utils.isMyself
    @gamedecorator.crossServer
    @gamedecorator.limitcall(0.5)
    def reqSetCrossTeamDeputy(self, exposed, deputyGbId):
        # 任命/取消副团长（0=取消；仅队长，本服 transferRaidDeputy 对应）：
        # 全队唯一名额，任命新副团长中心直接覆盖旧的；变更经中心 deputyChangePush
        # 全推后各成员 cell onCrossTeamDeputyChange 落地缓存并透传客户端，
        # 操作结果经 uuid 回执 onCrossTeamOpResult（成功也回）
        LOG_INFO('reqSetCrossTeamDeputy', deputyGbId)
        if not self._isCrossTeamCaptain():
            LOG_WARN('reqSetCrossTeamDeputy, not captain')
            return

        gameengine.getCrossTeamStub(self._crossTeamId()).reqSetDeputy(
            self.base,
            self._crossTeamId(),
            self.gbId,
            deputyGbId
        )

    # ------------------------------------------------------------------
    # 队伍标记三件套（本服 reqAddMarkMember/reqDelMarkMember/reqChangeOnlyCaptain 对应）：
    # 数据存中心，变更经中心 markChangePush 单条增量下发（只发队长当前所在服）；
    # 对齐本服静默语义：本地校验不过即丢弃，中心权威复核，均无回执
    # ------------------------------------------------------------------

    @utils.isMyself
    @gamedecorator.crossServer
    @gamedecorator.limitcall(0.5)
    def reqAddCrossMarkMember(self, exposed, markType, markIdx, markName, markGbId, markEntityId, markPos):
        """API: 请求增加跨服队伍标记（仅副本内可用，客户端入口自行控制）"""
        LOG_INFO('reqAddCrossMarkMember', markType, markIdx, markGbId)
        if not self._crossTeamId():
            return
        if markIdx <= 0 or markIdx > gameconst.TEAM_MARK_MAX_SLOT:
            return
        # 仅队长开关（本服 addMarkMember 同口径：非队长操作静默丢弃；中心权威复核）
        if self.crossTeamInfo.teamMarkInfo.get('onlyCaptainCanMark') and not self._isCrossTeamCaptain():
            LOG_INFO('reqAddCrossMarkMember blocked by onlyCaptainCanMark')
            return

        # serverId：标队友时取其在中心登记的归属服；怪物/场景点填本服（空间所在服）
        _serverId = gameconfig.serverId()
        _member = self.crossTeamInfo.memberDict.get(markGbId)
        if _member:
            _serverId = _member.serverId

        gameengine.getCrossTeamStub(self._crossTeamId()).reqAddCrossMark(
            self.base, self._crossTeamId(), self.gbId, markType, markIdx, markName, markGbId,
            markEntityId, markPos, self.spaceNo, _serverId)

    @utils.isMyself
    @gamedecorator.crossServer
    @gamedecorator.limitcall(0.5)
    def reqDelCrossMarkMember(self, exposed, markType, markIdx):
        """API: 请求删除跨服队伍标记（按 type+index 摘除）"""
        LOG_INFO('reqDelCrossMarkMember', markType, markIdx)
        if not self._crossTeamId():
            return
        if markIdx <= 0 or markIdx > gameconst.TEAM_MARK_MAX_SLOT:
            return
        if self.crossTeamInfo.teamMarkInfo.get('onlyCaptainCanMark') and not self._isCrossTeamCaptain():
            LOG_INFO('reqDelCrossMarkMember blocked by onlyCaptainCanMark')
            return

        gameengine.getCrossTeamStub(self._crossTeamId()).reqDelCrossMark(
            self.base, self._crossTeamId(), self.gbId, markType, markIdx)

    @utils.isMyself
    @gamedecorator.crossServer
    @gamedecorator.limitcall(0.5)
    def reqChangeCrossOnlyCaptain(self, exposed, onlyCaptain):
        """API: 请求改变仅队长可标记开关（仅队长）"""
        LOG_INFO('reqChangeCrossOnlyCaptain', onlyCaptain)
        if not self._isCrossTeamCaptain():
            LOG_WARN('reqChangeCrossOnlyCaptain, not captain')
            return

        gameengine.getCrossTeamStub(self._crossTeamId()).reqChangeCrossOnlyCaptainMark(
            self.base, self._crossTeamId(), self.gbId, onlyCaptain)

    @utils.isMyself
    @gamedecorator.crossServer
    @gamedecorator.limitcall(int(TM_MCD.datas['assembleTeammatesCD']['value']))
    def sendCrossAllMemberFollowAsk(self, exposed):
        # 召集（本服 sendAllMemberFollowAsk 对应，队长操作；跟随本体由客户端实现，
        # 服务端仅转发）：经中心 followAskPush 广播队长当前所在服的全队成员（不含队长），
        # 成员 cell 透传客户端 onCrossTeamFollowCaptainAsk；静默语义无回执
        LOG_INFO('sendCrossAllMemberFollowAsk')
        if not self._isCrossTeamCaptain():
            LOG_WARN('sendCrossAllMemberFollowAsk, not captain')
            return

        gameengine.getCrossTeamStub(self._crossTeamId()).askAllCrossTeamMemberFollow(
            self.base,
            self._crossTeamId(),
            self.gbId,
            self.spaceNo,
            tuple(self.position)
        )

    # ------------------------------------------------------------------
    # CrossTeamStub -> Avatar cell 下行
    # ------------------------------------------------------------------

    def _applyCrossTeamInfoUpdate(self, teamInfoDict):
        # 全量队伍缓存更新（空 dict = 已不在任何跨服队伍）；同步协议在调用方单独下发
        self.crossTeamInfo = self._buildCrossTeamInfoProp(teamInfoDict)

        # 同步 cell 镜像（互斥校验/状态同步用）与 base 镜像（聊天用）
        self.onCrossTeamIdChange(self._crossTeamId())

        # 全量落地后重建 AOI 队友集合（登录恢复/入队/对账刷新；空包重置由
        # onCrossTeamIdChange 清理），目标判定缓存（isEnemy/isFriend）随队伍变更重建
        self._refreshAoiCrossTeammates()
        self.resetAllTargetTypeCache()

        # 入队后若仍在匹配中，清掉本服匹配状态（中心已强制出池）
        if self._crossTeamId() and self.crossTeamMatchTarget:
            self.crossTeamMatchTarget = 0

        # 跨服镜像直进副本的一次性落地对账（无待对账标记时内部直接返回，
        # 见 impCrossTeamDungeonCell._recheckCrossMirrorDungeonTeam）
        self._recheckCrossMirrorDungeonTeam()

    def onCrossTeamInfoUpdate(self, teamInfoDict):
        # 登录恢复/全量队伍缓存刷新，经结构化协议下发客户端
        LOG_INFO('onCrossTeamInfoUpdate', teamInfoDict.get('teamId', 0))
        self._applyCrossTeamInfoUpdate(teamInfoDict)
        if self.client:
            self.client.onCrossTeamInfoUpdate(self.crossTeamInfo.toStreamDict())

        # 进服拿到全量组队数据（登录/回程重连查询回包、建队/入队/转团推送均经此漏斗）：
        # 即时上报一次刷新中心推送路由——中心仅在状态上报时刷新 RouteServerId，
        # 差分抑制下进跨服副本/退出副本回本服后路由可能滞留在旧服
        _teamId = self._crossTeamId()
        if _teamId:
            self._reportCrossTeamStateNow()
            # 全量队伍包之后再主动对账高频状态，补齐回程时序中丢失的成员状态更新
            # （空关注列表=全量，对账语义）
            # 这里不需要了，上报之后等下一个轮询就好了
            # gameengine.getCrossTeamStub(_teamId).queryTeamMemberState(
            #     self.base,
            #     _teamId,
            #     self.gbId,
            #     []
            # )

    def onCrossTeamCenterReconnected(self, stubIdx):
        # 与中心断连重连后的全服对账（CrossTeamStub 经 broadcastToAllAvatar 广播）：
        # 按 gbId 分片过滤（两分片各自重连都会广播，避免重复重查）；
        # 在队玩家以中心当前数据为准全量重查——数据未丢（抖动）则刷新并补齐
        # 断连期丢失的推送，已丢（中心重启）则空回包重置，与登录自愈共用同一链路
        if self.gbId % gameconfig.crossTeamStubNum() != stubIdx:
            return

        if not self._crossTeamId():
            return

        if (self.isCrossServer or
                (self.crossTeamInfo and self.crossTeamInfo.inDungeon) or
                self._isInCrossTeamDungeonSpace(self.spaceMgr)):
            # 玩家在跨服服上（跨服服镜像/本服残影链路）或正在跨服副本中：跳过，
            # 回本走重连经 onClientEnabled 自愈；保留副本内队伍 HUD/AOI/加成。
            # 本服模式副本的 inDungeon 本地不置真（仅中心全量包携带，进本不推送更新），
            # 改用空间事实兜底判定，避免本服模式副本进行中被对账空包重置
            return

        LOG_INFO('onCrossTeamCenterReconnected requery', self._crossTeamId())
        gameengine.getCrossTeamStub(self.gbId).queryPlayerTeam(self.base, self.gbId)

    def onCrossTeamCreateSuccess(self, teamInfoDict):
        LOG_INFO('onCrossTeamCreateSuccess', teamInfoDict.get('teamId', 0))
        self._applyCrossTeamInfoUpdate(teamInfoDict)
        self._sendCrossTeamMsg('teamChannel_createTeamMsg', [])
        if self.client:
            self.client.onCrossTeamCreateSuccess(self.crossTeamInfo.toStreamDict())

        # 无队邀请流程：本流程建队成功（teamId 命中预分配 id）→ 复位建队在途标记，
        # 并向被邀请人逐个发队伍就绪通知（已接受者命中 accepted 进队，未接受者无记录直接丢弃）
        _tuc = self._getTeamUpCreating()
        if _tuc.teamId and self._crossTeamId() == _tuc.teamId:
            _tuc.creating = False
            for _gbId in _tuc.invitees:
                gameengine.getCrossTeamStub(self._crossTeamId()).teamUpJoinNotify(
                    self.base,
                    self._crossTeamId(),
                    self.gbId,
                    _gbId
                )

    def onCrossTeamJoinSuccess(self, teamInfoDict):
        # 加入队伍成功：复用全量更新逻辑，并额外回调客户端做加入成功表现
        LOG_INFO('onCrossTeamJoinSuccess', teamInfoDict.get('teamId', 0))
        self._applyCrossTeamInfoUpdate(teamInfoDict)
        # 本人也收"加入了队伍"频道消息（对齐旧本服组队入队广播含新人本人）
        self._sendCrossTeamMsg('teamChannel_enterTeamMsg', [self.name, str(self.gbId)])
        if self.client:
            self.client.onCrossTeamJoinSuccess(self.crossTeamInfo.toStreamDict())

    def onCrossTeamOpResult(self, resultCode, teamId, gbId, target):
        # 无队邀请流程自动建队失败回执（叠加观察，不影响既有透传逻辑）：复位建队在途标记，
        # 记日志静默结束（决策 1/2）
        _tuc = self._getTeamUpCreating()
        if _tuc.creating and teamId == _tuc.teamId and resultCode != gameconst.CROSS_TEAM_RESULT_SUCCESS:
            _tuc.creating = False
            LOG_WARN('teamUpAutoCreate failed', resultCode, teamId)

        LOG_INFO('onCrossTeamOpResult', resultCode, teamId, target)
        if resultCode == gameconst.CROSS_TEAM_RESULT_MATCH_JOIN_INVALID:
            # 撮合入队作废：清本服匹配状态，提示重新发起
            self.crossTeamMatchTarget = 0

        if resultCode == gameconst.CROSS_TEAM_RESULT_SERVER_MISMATCH:
            # 同意邀请被中心同服校验拒绝：邀请链路无招募来源，仅按当前所在服区分提示
            self._showCrossTeamServerMismatchMsg(gameconst.TeamJoinType.DEFAULT)

        if self.client:
            self.client.onCrossTeamOpResult(resultCode, teamId, target)

    def onCrossTeamApplyJoinResult(self, resultCode, teamId, target, requireLevel, requireScore, password, applySource):
        # 入队申请受理回调（中心 uuid 回执经 Stub 原路返回）：纯透传客户端做失败交互
        # （密码输入面板/原因提示）
        LOG_INFO('onCrossTeamApplyJoinResult', resultCode, teamId, target)
        if resultCode == gameconst.CROSS_TEAM_RESULT_SERVER_MISMATCH:
            self._showCrossTeamServerMismatchMsg(applySource)
        if self.client:
            self.client.onCrossTeamApplyJoinResult(
                resultCode,
                teamId,
                target,
                requireLevel,
                requireScore,
                password,
                applySource
            )

    def _showCrossTeamServerMismatchMsg(self, applySource):
        # 中心同服校验（SERVER_MISMATCH）拒绝的分场景提示（客户端对该错误码无处理，由服务端直接发 msg）：
        # 在归墟（跨服服）被拒 → 目标为本服队伍，跨服场景中不可加入（54003531）；
        # 本服点击跨服帮会招募链接被拒 → 招募专用提示（54003532）；
        # 本服其他入口被拒 → 目标为归墟中组建的队伍，返回本服后不可加入（54003530）
        if not self.client:
            return
        if gameconfig.isCrossServer():
            self.showMsg(MMD.datas.crossServerApplyMsg2, [])
        elif applySource == gameconst.TeamJoinType.RECRUIT:
            self.showMsg(MMD.datas.crossServerApplyMsg3, [])
        else:
            self.showMsg(MMD.datas.crossServerApplyMsg, [])

    def onCrossTeamMatchTimeout(self, target):
        LOG_INFO('onCrossTeamMatchTimeout', target)
        self.crossTeamMatchTarget = 0
        if self.client:
            self.client.onCrossTeamMatchTimeout(target)

    def onCrossTeamMatchSuccess(self, teamId, target):
        # 两段式入队第一段：中心撮合成功后回调，cell 侧做最终检查并取玩家信息回调 Stub.doMatchJoin
        LOG_INFO('onCrossTeamMatchSuccess', teamId, target, self.crossTeamMatchTarget)

        if self.crossTeamMatchTarget != target:
            LOG_WARN('onCrossTeamMatchSuccess but not matching', self.crossTeamMatchTarget, target)
            return

        if not self._checkCrossTeamMutex():
            # 互斥条件已不满足（在本服队伍/团队/跨服队伍中），无法继续匹配，清状态
            LOG_WARN('onCrossTeamMatchSuccess mutex check fail')
            self.crossTeamMatchTarget = 0
            return

        gameengine.getCrossTeamStub(teamId).doMatchJoin(teamId, target, self._getCrossTeamPlayerInfoDic())

    # ------------------------------------------------------------------
    # 无队邀请组队（InviteType.TEAM_UP）：Stub 经 PlayerStub 路由的下行与流程内部回执。
    # 客户端只有邀请/应答两个动作，建队/就绪通知/进队全部服务端闭环，失败一律静默+日志
    # ------------------------------------------------------------------

    def onTeamUpInvite(self, inviteInfo):
        # 无队邀请到达（B 侧）：记录待答，透传客户端弹窗
        # （inviteInfo 为 CROSS_TEAM_INVITE_VAL 同构 dict，teamId 为邀请人预分配 id）
        LOG_INFO('onTeamUpInvite', inviteInfo.get('teamId', 0), inviteInfo.get('gbId', 0))
        _tuc = self._getTeamUpCreating()
        _tuc.inviteIns[inviteInfo['gbId']] = (inviteInfo['teamId'], utils.curTS())
        if self.client:
            self.client.onCrossTeamInvite(inviteInfo)

    def onTeamUpInviteReply(self, replyInfo):
        # 无队邀请应答到达（A 侧，服务端闭环驱动点）：拒绝仅透传客户端提示；
        # 同意则透传提示（纯展示），且自己仍无队、未在建队在途时自动建队
        LOG_INFO('onTeamUpInviteReply', replyInfo.get('gbId', 0), replyInfo.get('agree', False),
                 replyInfo.get('reason', 0))
        _tuc = self._getTeamUpCreating()
        _rec = _tuc.invitees.get(replyInfo['gbId'])
        if _rec is None:
            LOG_WARN('onTeamUpInviteReply, no invite record', replyInfo.get('gbId', 0))
            return

        if not replyInfo['agree']:
            if self.client:
                self.client.onTeamUpInviteReply(replyInfo)
            return

        if not self.client:
            # 僵尸 cell 不建队（更贴合决策 2：A 不在线不建队，静默失败仅留日志）
            LOG_INFO('onTeamUpInviteReply, no client, skip auto create', replyInfo.get('gbId', 0))
            return

        self.client.onTeamUpInviteReply(replyInfo)
        if not self._crossTeamId() and not _tuc.creating:
            self._teamUpAutoCreate()

    def _teamUpAutoCreate(self):
        # 无队邀请流程自动建队（内部方法）：target 固定自由队，无门槛/密码/介绍/满员自动进本；
        # teamId 复用预分配 id（_doCreateCrossTeam 内取），多份接受触发的重复建队打在同一个
        # id 上，creating 标记与中心 DUPLICATED_TEAM 双重去重；失败回执经 onCrossTeamOpResult
        # 叠加观察复位 creating，静默结束（决策 1/2）
        LOG_INFO('_teamUpAutoCreate')
        _tuc = self._getTeamUpCreating()
        _tuc.creating = True
        self._doCreateCrossTeam(gameconst.TEAM_UP_TARGET, 0, 0, '', '', False)

    def onTeamUpTeamReady(self, teamId, captainGbId):
        # 队伍就绪通知（B 侧）：命中已答应记录（邀请人一致）才自动进队，
        # 防伪造就绪通知乱入队；记录消费后回执到达时 accepted 无此 teamId，仅记日志
        LOG_INFO('onTeamUpTeamReady', teamId, captainGbId)
        _tuc = self._getTeamUpCreating()
        _rec = _tuc.accepted.pop(teamId, None)
        if _rec is None or _rec[0] != captainGbId:
            LOG_WARN('onTeamUpTeamReady, no/invalid accepted record', teamId, captainGbId)
            return

        if not self._checkCrossTeamMutex():
            return

        gameengine.getCrossTeamStub(teamId).teamUpReqJoin(
            self.base,
            teamId,
            self._getCrossTeamPlayerInfoDic()
        )

    def onTeamUpAutoJoinResult(self, resultCode, teamId, target, requireLevel, requireScore, password, applySource):
        # 流程内部进队（teamUpReqJoin）的专用受理回执：与用户主动 reqJoin 的客户端透传通道
        # onCrossTeamApplyJoinResult 隔离，全部静默+日志；参数口径与中心回包固定结构一致，
        # 本流程只用 resultCode/teamId
        _tuc = self._getTeamUpCreating()
        if teamId not in _tuc.accepted:
            # 就绪通知路径已先消费记录，其迟到回执仅留日志（失败不通知，决策 1）
            LOG_INFO('onTeamUpAutoJoinResult, no accepted record', resultCode, teamId)
            return

        if resultCode == gameconst.CROSS_TEAM_RESULT_SUCCESS:
            del _tuc.accepted[teamId]
        elif resultCode == gameconst.CROSS_TEAM_RESULT_TEAM_NOT_FOUND:
            # 队还没建好：保留记录等就绪通知（A 建队成功后逐个通知）
            LOG_INFO('onTeamUpAutoJoinResult, team not found, wait ready notify', teamId)
        else:
            del _tuc.accepted[teamId]
            LOG_WARN('onTeamUpAutoJoinResult, join fail', resultCode, teamId)

    # ------------------------------------------------------------------
    # 申请审批同意自证入队：队长 replyApply 同意后中心标记 Approved 并通知本服，
    # Stub 经 PlayerStub 路由到申请人 cell 自动进队；受理回执走专用通道静默收口
    # ------------------------------------------------------------------

    def onCrossTeamApplyApproved(self, teamId):
        # 审批同意到达（申请人侧）：本地二次检查（互斥）后自动进队，
        # 中心侧为带 Approved 记录的申请人跳过密码与门槛校验；检查不通过静默收口
        LOG_INFO('onCrossTeamApplyApproved', teamId)
        if not self._checkCrossTeamMutex():
            return

        gameengine.getCrossTeamStub(teamId).approvedReqJoin(
            self.base,
            teamId,
            self._getCrossTeamPlayerInfoDic()
        )

    def onTeamApprovedJoinResult(self, resultCode, teamId, target, requireLevel, requireScore, password, applySource):
        # 自证入队（approvedReqJoin）的专用受理回执：与用户主动 reqJoin 的客户端透传通道
        # onCrossTeamApplyJoinResult 隔离，全部静默+日志；参数口径与中心回包固定结构一致，
        # 成功无需处理（入队成功推送走现有 onCrossTeamJoinSuccess 通道落地 crossTeamInfo）
        if resultCode == gameconst.CROSS_TEAM_RESULT_SUCCESS:
            LOG_DBG('onTeamApprovedJoinResult, join success', teamId)
        else:
            LOG_WARN('onTeamApprovedJoinResult, join fail', resultCode, teamId)

    # ------------------------------------------------------------------
    # 增量推送处理（直接调用 CrossTeamCacheVal 辅助函数修改当前缓存对象）
    # ------------------------------------------------------------------

    def onCrossTeamMemberAdd(self, memberDict):
        # 进队增量：新成员本人走全量（不在队伍时不处理），老成员追加成员条目
        if not self._crossTeamId():
            return

        _memberData = dict(memberDict)
        _memberData.setdefault('hp', 0)
        _memberData.setdefault('maxHp', 0)
        self.crossTeamInfo.addMember(_memberData)

        self._sendCrossTeamMsg(
            'teamChannel_enterTeamMsg',
            [_memberData.get('playerName', ''), str(_memberData.get('gbId', 0))]
        )

        # 新队友可能已在视野内（本服场景），补灌 AOI 队友集合；目标判定缓存随队伍变更重建
        self._refreshAoiCrossTeammates()
        self.resetAllTargetTypeCache()

        if self.client:
            self.client.onCrossTeamMemberAdd(memberDict)

    def onCrossTeamMemberRemove(self, gbId, changeType):
        LOG_INFO('onCrossTeamMemberRemove', gbId, changeType)
        if not self._crossTeamId():
            return

        # 频道消息需先取离队者名字（removeMember 后缓存即失效）
        _memberVal = self.crossTeamInfo.memberDict.get(gbId)
        _memberName = _memberVal.playerName if _memberVal else ''
        self.crossTeamInfo.removeMember(gbId)
        # 剔除已非队友的 AOI 成员；目标判定缓存随队伍变更重建
        self._refreshAoiCrossTeammates()
        self.resetAllTargetTypeCache()
        # changeType: 2=主动离队, 3=被踢, 6=离线；离线沿用主动离队文案
        if changeType == 3:
            self._sendCrossTeamMsg('teamChannel_kickedMsg', [_memberName, str(gbId)])
        else:
            self._sendCrossTeamMsg('teamChannel_initiativeLeaveTeamMsg', [_memberName, str(gbId)])
        if self.client:
            self.client.onCrossTeamMemberRemove(gbId, changeType)

    def onCrossTeamLeave(self, teamId, reason):
        # 自己被移出队伍：清空本地缓存并通知客户端离队原因
        LOG_INFO('onCrossTeamLeave', teamId, reason)
        # 离队放弃自己对视野内怪物的首刀归属（对齐旧本服组队离队逻辑；
        # 旧轨被踢不清，跨服轨在此统一补齐）
        for _e in self.entitiesInView(True):
            if _e.IsMonster:
                _e.clearFirstBlood(self.id)
        # 退队联动退本：仍在本队副本空间内时同时退出副本（须在 crossTeamInfo.reset() 之前，
        # 本服模式的副本归属判定依赖旧 teamId）
        self.exitCrossTeamDungeonOnTeamLeave(teamId)
        if self.crossTeamInfo:
            self.crossTeamInfo.reset()
        self.resetAllTargetTypeCache()
        self.onCrossTeamIdChange(0)
        # 被踢者本人提示（对齐旧本服组队 kickFromTeamMsg）；reason: 2=离队, 3=被踢, 6=离线
        if reason == 3:
            self._sendCrossTeamMsg('kickFromTeamMsg', [])
        if self.client:
            self.client.onCrossTeamLeave(teamId, reason)
        # 离队清空无队邀请组队状态（防残留预分配 teamId 被无关建队复用）
        self.teamUpCreating = None

    def onCrossTeamCaptainChange(self, newCaptainGbId):
        if not self._crossTeamId():
            return

        _oldCaptainGbId = self.crossTeamInfo.captainGbId
        self.crossTeamInfo.setCaptain(newCaptainGbId)
        # 分线聚合的队长标志修正：仅新旧队长本人上报
        # （对齐本服 becomeTeamCaptain/onLoseTeamCaptain）
        if self.gbId == newCaptainGbId or self.gbId == _oldCaptainGbId:
            _teamId = self._crossTeamId()
            self._reportLineTeamChange(_teamId, _teamId, self.gbId == newCaptainGbId)
        # 队长变更频道消息全员可见；新队长本人另收"你已成为队长"提示
        _captainVal = self.crossTeamInfo.memberDict.get(newCaptainGbId)
        _captainName = _captainVal.playerName if _captainVal else ''
        self._sendCrossTeamMsg('teamChannel_becomeCaptainMsg', [_captainName, str(newCaptainGbId)])
        if self.gbId == newCaptainGbId:
            self._sendCrossTeamMsg('beCaptainMsg', [])
        if self.client:
            self.client.onCrossTeamCaptainChange(newCaptainGbId)

    def onCrossTeamBecomeCaptainApplyMsg(self, applicantGbId, applicantName):
        # "申请成为队长"队伍频道消息：中心的申请推送只发队长本人，故仅队长可见
        self._sendCrossTeamMsg(
            'teamChannel_applyCaptainMsg',
            [applicantName, self.name, str(applicantGbId), str(self.gbId)]
        )

    def onCrossTeamSettingsChange(self, settingsDict):
        if not self._crossTeamId():
            return

        self.crossTeamInfo.updateSettings(settingsDict)
        if self.client:
            self.client.onCrossTeamSettingsChange(settingsDict)

    def onCrossTeamAutoMatchChange(self, autoMatch):
        # 自动匹配开关变更推送（已从目标变更推送拆分）
        if not self._crossTeamId():
            return

        self.crossTeamInfo.setAutoMatch(autoMatch)
        if self.client:
            self.client.onCrossTeamAutoMatchChange(autoMatch)

    def onCrossTeamMicsModeChange(self, micsMode):
        if not self._crossTeamId():
            return

        self.crossTeamInfo.setMicsMode(micsMode)
        if self.client:
            self.client.onCrossTeamMicsModeChange(micsMode)

    def onCrossTeamMicBlockChange(self, gbId, blocked):
        if not self._crossTeamId():
            return

        self.crossTeamInfo.setMicBlock(gbId, blocked)
        if self.client:
            self.client.onCrossTeamMicBlockChange(gbId, blocked)

    def onCrossTeamMemberPosChange(self, srcGbId, srcGroupIdx, dstGbId, dstGroupIdx):
        # 位置调整推送：服务端内部位置已变更，客户端收到后刷新全量队伍信息
        LOG_INFO('onCrossTeamMemberPosChange', self._crossTeamId(),
                 srcGbId, srcGroupIdx, dstGbId, dstGroupIdx)
        if not self._crossTeamId():
            return

        if self.client:
            self.client.onCrossTeamMemberPosChange(srcGbId, srcGroupIdx, dstGbId, dstGroupIdx)

    def onCrossTeamDisband(self, teamId):
        # 解散：清空队伍缓存并通知客户端
        # 解散放弃自己对视野内怪物的首刀归属（全员都收推送，各自清自己的；
        # 旧本服轨只清队长，跨服轨在此补齐）
        for _e in self.entitiesInView(True):
            if _e.IsMonster:
                _e.clearFirstBlood(self.id)
        # 退队联动退本：仍在本队副本空间内时同时退出副本（须在 crossTeamInfo.reset() 之前，
        # 本服模式的副本归属判定依赖旧 teamId）；解散时全员各自退本，末人离开触发副本完成
        self.exitCrossTeamDungeonOnTeamLeave(teamId)
        if self.crossTeamInfo:
            self.crossTeamInfo.reset()
        self.resetAllTargetTypeCache()
        self.onCrossTeamIdChange(0)
        if self.client:
            self.client.onCrossTeamDisband(teamId)
        # 解散清空无队邀请组队状态（防残留预分配 teamId 被无关建队复用）
        self.teamUpCreating = None

    # ------------------------------------------------------------------
    # 接口对齐补充：Stub -> cell 下行推送（对齐梳理 §3）
    # ------------------------------------------------------------------

    def onCrossTeamPreview(self, teamInfoDict):
        # 队伍预览回包（决策 D4/注记 5）：只下发客户端预览，不灌入自身队伍缓存；
        # 查询失败/队伍不存在回 teamId=0 的完整空结构（FIXED_DICT 键齐全）
        LOG_INFO('onCrossTeamPreview', teamInfoDict.get('teamId', 0) if teamInfoDict else 0)
        if self.client:
            if not teamInfoDict or not teamInfoDict.get('teamId', 0):
                teamInfoDict = crossTeam.CrossTeamCacheVal().toStreamDict()
            self.client.onCrossTeamPreview(teamInfoDict)

    def onCrossTeamApplyList(self, applyList):
        # 申请列表回包（仅队长可拉取；CROSS_TEAM_APPLY_VAL 列表）
        LOG_INFO('onCrossTeamApplyList', len(applyList) if applyList else 0)
        if self.client:
            self.client.onCrossTeamApplyList(applyList or [])

    def onCrossTeamApplyRemove(self, gbId):
        # 申请移除通知（申请被同意/拒绝/超时清理），客户端从申请列表移除
        if self.client:
            self.client.onCrossTeamApplyRemove(gbId)

    def onCrossTeamMatchStart(self, enterTS):
        # 入池成功确认（客户端匹配 UI 读配表 maxMatchTime 倒计时，决策 D5）；
        # 本地匹配状态（crossTeamMatchTarget）在 reqCrossTeamMatch 时已置位
        LOG_INFO('onCrossTeamMatchStart', self.crossTeamMatchTarget, enterTS)
        if self.client:
            self.client.onCrossTeamMatchStart(enterTS)

    def onCrossTeamMatchStop(self):
        # 取消匹配确认（撮合成功/超时分别走 onCrossTeamMatchSuccess/onCrossTeamMatchTimeout）
        LOG_INFO('onCrossTeamMatchStop', self.crossTeamMatchTarget)
        self.crossTeamMatchTarget = 0
        if self.client:
            self.client.onCrossTeamMatchStop()

    def onCrossTeamMemberVoiceState(self, gbId, voiceFlags):
        # 成员语音状态变更（决策 2 独立推送）：更新缓存成员四态并转发客户端；
        # 位定义与本服对称（user_type/team.py _buildVoiceFlags）：
        # 0x01=inVoiceRoom, 0x02=enableMics, 0x04=enableSpeaker,
        # 0x08=isBlockMics（中心按 blockedMembers 判定带出）
        if not self._crossTeamId():
            return

        self.crossTeamInfo.updateMemberVoiceState(gbId, {
            'inVoiceRoom': (voiceFlags & 0x01) != 0,
            'enableMics': (voiceFlags & 0x02) != 0,
            'enableSpeaker': (voiceFlags & 0x04) != 0,
            'isBlockMics': (voiceFlags & 0x08) != 0,
        })
        if self.client:
            self.client.onCrossTeamMemberVoiceState(gbId, voiceFlags)

    def onCrossTeamMemberRename(self, teamId, gbId, name):
        # 成员改名广播落地（中心 renameMember 后 memberRenamePush 经 Stub 转发）：
        # Stub 下行统一经 cell 校验当前队伍，防换队/离队后旧推送落客户端
        if teamId != self._crossTeamId():
            return

        self.crossTeamInfo.updateMemberName(gbId, name)
        if self.client:
            self.client.onCrossTeamMemberRename(gbId, name)

    def onCrossTeamDeputyChange(self, deputyGbId):
        # 副团长变更（中心 setDeputy 后经 deputyChangePush 全推；deputyGbId=0 表示取消）：
        # 更新 crossTeamInfo 缓存并透传客户端
        if not self._crossTeamId():
            return

        self.crossTeamInfo.setDeputy(deputyGbId)
        if self.client:
            self.client.onCrossTeamDeputyChange(deputyGbId)

    def onCrossTeamMarkChange(self, changeType, markInfoDict, onlyCaptainCanMark):
        LOG_DBG('onCrossTeamMarkChange', changeType, markInfoDict, onlyCaptainCanMark)
        # 队伍标记单条增量变更（中心 markChangePush 经本服 Stub 转发）：
        # 落地本地镜像 + 透传客户端；MARK_ENEMY 增删时仅队长 cell 同步怪物 cell 记录
        # （怪物死亡自动摘除的依赖；被标记怪物在队长所在场景，其余成员忽略避免重复写；
        # 找不到实体说明怪物不在本进程，跳过即可）
        if not self._crossTeamId():
            return

        self.crossTeamInfo.applyMarkChange(changeType, markInfoDict, onlyCaptainCanMark)
        if self.client:
            self.client.onCrossTeamMarkChange(changeType, markInfoDict, onlyCaptainCanMark)

        if markInfoDict.get('type') != gameconst.TeamMarkType.MARK_ENEMY:
            return

        if not self.crossTeamInfo.isCaptain(self.gbId):
            return

        _ent = KBEngine.entities.get(markInfoDict.get('entId', 0))
        if not _ent or not hasattr(_ent, 'onBeMarkedAsEnemy'):
            return

        if changeType == gameconst.TeamMarkChangeType.ADD:
            _ent.onBeMarkedAsEnemy(self._crossTeamId(), gameconst.TeamType.CROSS_TEAM, markInfoDict.get('index', 0))
        elif changeType == gameconst.TeamMarkChangeType.DELETE:
            _ent.delBeMarkedAsEnemy(self._crossTeamId(), gameconst.TeamType.CROSS_TEAM)

    def onCrossTeamFollowCaptainAsk(self, spaceNo, position):
        # 召集下行（本服 onFollowTeamCaptainAsk 对应）：中心 followAskPush 经本服 Stub
        # 转发，透传客户端（跟随本体由客户端实现）；
        # 对齐本服发送期过滤（TeamVal.askAllMemberFollow）：禁跟随场景的成员不收召集
        if formula.checkSpaceForbidTeamFollow(self.spaceNo):
            return

        if self.client:
            self.client.onCrossTeamFollowCaptainAsk(spaceNo, position)

    def onCrossTeamRefreshDungeonCD(self, lastDungeonFinishedTime):
        # 重进 CD 刷新（中心 crusadeFinished 写 CD 截止时刻后全推，dungeonCDRefreshPush 链路）；
        # value 语义同本服 onRefreshLastDungeonFinishedTime 线上值 = 完成时刻 + raid_rejoinCdTime
        if self._crossTeamId():
            self.crossTeamInfo.lastDungeonFinishedTime = lastDungeonFinishedTime
        if self.client:
            self.client.onCrossTeamRefreshDungeonCD(lastDungeonFinishedTime)

    # ------------------------------------------------------------------
    # base -> cell 检查转发 / 镜像同步 / 登录恢复 / 离线
    # ------------------------------------------------------------------

    def _reportLineTeamChange(self, oldTeamUUID, newTeamUUID, isLeader):
        # 分线聚合登记（对齐旧本服组队的 LineStub.updateLinePlayerInfo changeTeam 上报）：
        # 分线队伍聚合表（teamPlayersDic）用于选线跟队与高负载线队友放行；
        # 非分线场景（副本/跨服镜像等）无需登记
        if not formula.inLineScene(self.spaceNo):
            return

        _lineType = formula.fetchMapId(self.spaceNo)
        _lineNo = formula.parseLineNo(self.spaceNo)
        gameengine.getLineStub(_lineType).updateLinePlayerInfo(
            _lineNo,
            self.base,
            self.gbId,
            {'changeTeam': (oldTeamUUID, newTeamUUID, isLeader)}
        )

    def onCrossTeamIdChange(self, teamId):
        # 队伍镜像更新；在队期间开启状态检查定时器（快照对比有变动才上报 Stub），
        # 周期取 gameconfig.crossTeamStateQueryCacheSeconds（GM 可在线调整，仅对新建定时器生效）；
        # 同步 base 镜像（聊天用）；
        # 分线场景向 LineStub 登记队伍变更（建队/进队/登录恢复/离队/解散的共同漏斗）
        LOG_INFO('onCrossTeamIdChange', self.crossTeamId, '->', teamId)
        _oldTeamId = self.crossTeamId
        self.crossTeamId = teamId
        if self.base:
            self.base.syncCrossTeamIdToBase(teamId)

        if teamId:
            if not self.crossTeamStateSyncTimer:
                _interval = gameconfig.crossTeamStateQueryCacheSeconds()
                self.crossTeamStateSyncTimer = self.pyAddTimer(_interval, _interval, gametimer.CROSS_TEAM_AVATAR_STATE_TICK)
        elif self.crossTeamStateSyncTimer:
            self.pyDelTimer(self.crossTeamStateSyncTimer, gametimer.CROSS_TEAM_AVATAR_STATE_TICK)
            self.crossTeamStateSyncTimer = 0

        if not teamId:
            # 被移出跨服队伍：清理 AOI 队友集合/经验加成
            self._clearAoiCrossTeammates()

        if _oldTeamId != teamId:
            # 队伍变更：清状态上报快照，下个 tick 无条件全量上报一次新队状态
            self._crossTeamStateSnap = None
            _isLeader = False
            if teamId and self.crossTeamInfo:
                _isLeader = self.crossTeamInfo.captainGbId == self.gbId
            self._reportLineTeamChange(_oldTeamId, teamId, _isLeader)

    def _isCrossTeamStateDirty(self, stateDict):
        # 与上一次上报快照对比（快照存 cell 普通属性，不落库）：
        # 血量变动超阈值 / 位置移动距离超阈值（平方比较，免开方）视为脏；
        # spaceNo/level/score/maxHp 变动低频但语义关键（副本跨空间/展示刷新），
        # 任何变化也上报；改名不走本链路（renameMember 独立协议即时上行）
        _snap = getattr(self, '_crossTeamStateSnap', None)
        if _snap is None:
            return True

        if abs(stateDict['hp'] - _snap['hp']) > gameconst.CROSS_TEAM_STATE_HP_DELTA:
            return True

        _pos = stateDict['position']
        _oldPos = _snap['position']
        _distSq = ((_pos[0] - _oldPos[0]) ** 2 +
                   (_pos[1] - _oldPos[1]) ** 2 +
                   (_pos[2] - _oldPos[2]) ** 2)
        if _distSq > gameconst.CROSS_TEAM_STATE_POS_DIST_SQ:
            return True

        return (stateDict['spaceNo'] != _snap['spaceNo'] or
                stateDict['level'] != _snap['level'] or
                stateDict['score'] != _snap['score'] or
                stateDict['maxHp'] != _snap['maxHp'])

    def syncCrossTeamState(self):
        # 每秒一次 RPC 合并完成两件事（脏检查未通过时上行空 stateDict，由 Stub 侧跳过上报）：
        # 1) 上行：自身状态快照脏检查后向当前所在服 Stub 同步（由 Stub 聚合后定时上报中心；
        #    跨服副本中由跨服服上的镜像执行，中心据此刷新成员路由）
        # 2) 下行（推送模型）：中心 1s tick 把脏队伍全量快照推送到 Stub 写本地缓存并递增
        #    version，本调用按关注列表读缓存，Stub 按版本号去重（version 未前进不重发），
        #    有更新才剪裁后经 box.client 直发客户端（不再经本 cell 中转，队伍有效性由客户端校验）
        # teamId 取队伍缓存，缓存为空（跨服镜像直进副本、全量包尚未落地）时回落
        # crossTeamId 属性（进本时已显式写入），尽早上报刷新中心推送路由
        _teamId = self._crossTeamId() or self.crossTeamId
        if not _teamId:
            return

        if self.isCrossServerInLocalServer:
            # 本服镜像（玩家已迁往跨服服，客户端不在本服）：停止上报与下行读缓存，
            # 否则陈旧数据会覆盖跨服镜像的真实上报，并把中心推送路由拉回本服
            return

        _stateDict = {
            'hp': self.hp,
            'maxHp': self.fullHp,
            'level': self.level,
            'score': self.getTotalScore(),
            'spaceNo': self.spaceNo,
            'position': tuple(self.position),
        }
        if self._isCrossTeamStateDirty(_stateDict):
            self._crossTeamStateSnap = _stateDict
        else:
            _stateDict = {}

        gameengine.getCrossTeamStub(_teamId).syncMemberState(
            self.base,
            _teamId,
            self.gbId,
            _stateDict,
            self._crossTeamWatchGroups()
        )

    def _crossTeamWatchGroups(self):
        # 客户端未设置过（None）时回落默认关注本组（gameconst.CROSS_TEAM_WATCH_GROUPS_DEFAULT）
        _groups = self.crossTeamWatchGroups
        if not _groups:
            return list(gameconst.CROSS_TEAM_WATCH_GROUPS_DEFAULT)
        return _groups

    def reportCrossTeamRename(self, newName):
        # 改名事件即时上行（低频；改名卡/GM/IDIP 统一经 base._doModifyName ->
        # cell.afterModifyName 收口调用）：中心更新成员名后 memberRenamePush 全队广播。
        # 成员名唯一变更通道（MemberState 不再携带 name）
        _teamId = self._crossTeamId() or self.crossTeamId
        if not _teamId:
            return

        if self.isCrossServerInLocalServer:
            # 本服残影不上报（口径同 syncCrossTeamState）
            return

        gameengine.getCrossTeamStub(_teamId).renameMember(_teamId, self.gbId, newName)

    def _reportCrossTeamStateNow(self):
        # 即时全量上报一次自身状态（绕过差分脏检查与定时聚合，经本服 Stub 单成员直发中心）：
        # 中心仅在状态上报时刷新成员推送路由（RouteServerId），差分抑制下进跨服副本/
        # 退出副本回本服后，若空间/位置/血量恰好无变化，路由会长期滞留在旧服，
        # 离队/解散等推送因此投错服；进服拿到全量组队数据时调用本方法即时刷新
        if not self._crossTeamId():
            return

        if self.isCrossServerInLocalServer:
            # 本服残影不上报（同 _syncCrossTeamState），否则会把中心路由拉回本服
            return

        _stateDict = {
            'hp': self.hp,
            'maxHp': self.fullHp,
            'level': self.level,
            'score': self.getTotalScore(),
            'spaceNo': self.spaceNo,
            'position': tuple(self.position),
        }
        gameengine.getCrossTeamStub(self._crossTeamId()).reportMemberStateNow(
            self._crossTeamId(),
            self.gbId,
            _stateDict
        )
        self._crossTeamStateSnap = _stateDict

    def _clearCrossTeamStateReportCache(self):
        # 迁移换路由前丢弃当前服未上报旧快照，避免其迟于新服即时上报到达中心
        _teamId = self._crossTeamId()
        if not _teamId:
            return

        gameengine.getCrossTeamStub(_teamId).clearMemberStateReport(
            _teamId,
            self.gbId
        )

    def leaveCrossTeamAuto(self, reason=None):
        LOG_INFO('leaveCrossTeamAuto', self._crossTeamId(), reason)
        # 离线：上报中心移出队伍（离线即退队）
        # 保护：跨服副本结束返回本服时，镜像 cell 走 offline 流程并非真实掉线，
        # 此时不应上报 memberOffline，否则结算后回到本服会被错误移出跨服队伍。
        # 副本中主动退出（未结算）的退队由旧本服副本 stub 的 leaveDungeonSpaceSucc
        # 跨服分支中的 leaveTeam 负责，不依赖此处重复上报。
        if reason == gameconst.OFFLINE_REASON_END_CROSS_SERVER:
            self._clearCrossTeamStateReportCache()
            LOG_INFO('leaveCrossTeamAuto skip cross server return', self._crossTeamId())
            return

        # 本地队伍缓存可能滞后（入队全量包未落地即下线），teamId 允许为 0 上报：
        # 中心持有权威 gbId->teamId 索引，收到 0 时按 gbId 反查，无队则不处理；
        # 无 teamId 时分片路由按惯例传 gbId
        _teamId = self._crossTeamId()
        gameengine.getCrossTeamStub(_teamId or self.gbId).memberOffline(
            _teamId,
            self.gbId
        )

    # ------------------------------------------------------------------
    # AOI 队友集合维护（teammateEntIdInAoiSet / expAddRatioByTeam）
    # 在队判定统一走访问层 isTeammate；进出视野的增量维护在
    # Avatar.onEnteredView/onLeaveView，此处为全量重建与清空
    # ------------------------------------------------------------------

    def _refreshAoiCrossTeammates(self):
        # 重建 AOI 队友集合并重算组队经验加成（本服组队/团已废弃，集合只承载跨服队友）；
        # 跨服队全量落地/成员增删时调用：视野内已是队友的补灌、已非队友的剔除
        _newSet = set()
        for _e in self.entitiesInView(True):
            if _e.IsAvatar and self.isTeammate(_e.gbId):
                _newSet.add(_e.id)

        if _newSet == self.teammateEntIdInAoiSet:
            return

        self.teammateEntIdInAoiSet.clear()
        self.teammateEntIdInAoiSet.update(_newSet)
        self.expAddRatioByTeam = utils.getTeamExpBonus(len(_newSet))

    def _clearAoiCrossTeammates(self):
        # 离队/解散时清空 AOI 队友集合与组队经验加成
        if self.teammateEntIdInAoiSet:
            self.teammateEntIdInAoiSet.clear()
        if self.expAddRatioByTeam:
            self.expAddRatioByTeam = 0
