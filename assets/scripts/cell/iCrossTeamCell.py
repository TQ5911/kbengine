# -*- coding: utf-8 -*-
# 跨服组队 cell 侧 mixin：
# - 客户端入口（applyCreateCrossTeam 等）：本地校验（互斥/门槛/密码）后直连本服 CrossTeamStub
#   （照本服组队 cell 直连 TeamStub 的模式，不再绕行 Avatar base）；
# - 承接本服 CrossTeamStub 下行（onCrossTeamInfoUpdate 等），维护 crossTeamInfo 属性
#   （CELL_PRIVATE，全量/增量变更均经结构化 ClientMethods 下发），事件类消息经 ClientMethods 下发；
# - 互斥：仅与本服组队/组团互斥（isInTeam/inRaid + crossTeamId 镜像）；
# - 状态同步：在队期间 3s 定时向本服 Stub 同步自身状态（血量/spaceNo+position 等），由 Stub 聚合上报中心；
# - 离线即退队：_offline 时上报 memberOffline；登录自动恢复
# 讨伐副本接入（发起/退出入口、条件检查应答、落地收尾与 trap）已迁至 cell/impCrossTeamDungeonCell.py（跨服组队全覆盖·第二步）。

import KBEngine
from KBEDebug import *

import gameengine
import gameconst
import gametimer
import gameconfig
import dataUtils
import utils

import teamMatch_activity as TMACTD
import teamMatch_matchConfig as TM_MCD
import gamedecorator
import crossTeam
import dungeonSrc
import formula


class ICrossTeamCell(object):

    # ------------------------------------------------------------------
    # 通用校验/信息/属性工具
    # ------------------------------------------------------------------

    def _crossTeamId(self):
        return self.crossTeamInfo.teamId if self.crossTeamInfo else 0

    def _isCrossTeamCaptain(self):
        return self._crossTeamId() != 0 and self.crossTeamInfo.captainGbId == self.gbId

    def _checkCrossTeamMutex(self):
        # 互斥校验：已在本服队伍/团队或其他跨服队伍时禁止操作
        if self.isInTeam():
            LOG_WARN('cross team mutex check fail, already in team', self.gbId)
            return False

        if self.inRaid():
            LOG_WARN('cross team mutex check fail, already in raid', self.gbId)
            return False

        if self._crossTeamId():
            LOG_WARN('cross team mutex check fail, already in cross team', self.gbId, self._crossTeamId())
            return False

        return True

    def _getCrossTeamPlayerInfoDic(self):
        return {
            'gbId': self.gbId,
            'playerName': self.name,
            'score': self.getTotalScore(),
            'level': self.level,
            'school': self.school,
            # 聊天 avatarInfo/成员展示字段（客户端接口对齐补充）；
            # openId 照本服组队现状占位（impTeam.py _getTeamPlayerInfoDic）
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

    def _buildCrossTeamInfoProp(self, teamInfoDict):
        # Stub 下发的队伍缓存 dict -> crossTeamInfo 属性对象（CrossTeamCacheVal）
        _cacheVal = crossTeam.CrossTeamCacheVal()
        _cacheVal.fromStreamDict(teamInfoDict)
        return _cacheVal

    # ------------------------------------------------------------------
    # 客户端入口（已在 iAvatarCrossTeam.def 注册 Exposed），直连本服 CrossTeamStub
    # ------------------------------------------------------------------

    @utils.isMyself
    @gamedecorator.limitcall(0.5)
    def applyCreateCrossTeam(self, exposed, target, minLevel, minScore, password, intro, autoEnter):
        LOG_INFO('applyCreateCrossTeam', target, minLevel, minScore, autoEnter)
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

        _teamId = KBEngine.genUUID64()
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
    @gamedecorator.limitcall(0.5)
    def applyJoinCrossTeam(self, exposed, teamId, password, applySource):
        LOG_INFO('applyJoinCrossTeam', self.gbId, teamId, applySource)
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
    @gamedecorator.limitcall(0.5)
    def replyCrossTeamJoin(self, exposed, gbId, bAgree):
        LOG_INFO('replyCrossTeamJoin', self.gbId, gbId, bAgree)
        if not self._crossTeamId():
            LOG_WARN('replyCrossTeamJoin, not in cross team', self.gbId)
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
    @gamedecorator.limitcall(0.5)
    def applyInviteCrossTeam(self, exposed, gbId, name):
        LOG_INFO('applyInviteCrossTeam', self.gbId, gbId, name)
        if not self._crossTeamId():
            LOG_WARN('applyInviteCrossTeam, not in cross team', self.gbId)
            return

        # 目前仅支持邀请本服玩家（inviteeServerId 取本服；跨服邀请需要 gbId->serverId 解析，留待后续）
        import gameconfig
        gameengine.getCrossTeamStub(self._crossTeamId()).inviteMember(
            self.base,
            self._crossTeamId(),
            self.gbId,
            gbId,
            gameconfig.serverId()
        )

    @utils.isMyself
    @gamedecorator.limitcall(0.5)
    def replyCrossTeamInvite(self, exposed, teamId, bAgree, inviterGbId, inviteType):
        LOG_INFO('replyCrossTeamInvite', self.gbId, teamId, bAgree, inviterGbId, inviteType)
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
    @gamedecorator.limitcall(0.5)
    def applyLeaveCrossTeam(self, exposed):
        LOG_INFO('applyLeaveCrossTeam', self.gbId, self._crossTeamId())
        if not self._crossTeamId():
            return

        gameengine.getCrossTeamStub(self._crossTeamId()).leaveTeam(
            self.base,
            self._crossTeamId(),
            self.gbId
        )

    @utils.isMyself
    @gamedecorator.limitcall(0.5)
    def applyKickCrossTeamMember(self, exposed, gbId):
        LOG_INFO('applyKickCrossTeamMember', self.gbId, gbId)
        if not self._crossTeamId():
            return

        # 队长身份在中心复核前的本服校验由本服 cell 完成（非队长直接拦截）
        if not self._isCrossTeamCaptain():
            LOG_WARN('applyKickCrossTeamMember, not captain', self.gbId)
            return

        gameengine.getCrossTeamStub(self._crossTeamId()).kickMember(
            self.base,
            self._crossTeamId(),
            gbId,
            self.gbId
        )

    @utils.isMyself
    @gamedecorator.limitcall(0.5)
    def applyTransferCrossCaptain(self, exposed, gbId):
        LOG_INFO('applyTransferCrossCaptain', self.gbId, gbId)
        if not self._crossTeamId():
            return

        if not self._isCrossTeamCaptain():
            LOG_WARN('applyTransferCrossCaptain, not captain', self.gbId)
            return

        gameengine.getCrossTeamStub(self._crossTeamId()).transferCaptain(
            self.base,
            self._crossTeamId(),
            gbId,
            self.gbId
        )

    @utils.isMyself
    @gamedecorator.limitcall(0.5)
    def applyBecomeCrossCaptain(self, exposed, gbId):
        # 申请成为队长（本服 applyBecomeCaptain 对应）：gbId 为客户端回传占位，以本人 gbId 为准；
        # 中心不留存待应答记录，校验通过后直接把申请提示推给队长（onCrossBecomeCaptainAsk）
        LOG_INFO('applyBecomeCrossCaptain', self.gbId, gbId)
        if not self._crossTeamId():
            return

        if self._isCrossTeamCaptain():
            LOG_WARN('applyBecomeCrossCaptain, already captain', self.gbId)
            return

        gameengine.getCrossTeamStub(self._crossTeamId()).applyBecomeCaptain(
            self.base,
            self._crossTeamId(),
            self.gbId
        )

    @utils.isMyself
    @gamedecorator.limitcall(0.5)
    def replyBecomeCrossCaptain(self, exposed, gbId, bAgree):
        # 队长应答"申请成为队长"（本服 replyBecomeCaptain 对应）：gbId=申请人；
        # 队长身份中心复核（本服缓存可能失效）
        LOG_INFO('replyBecomeCrossCaptain', self.gbId, gbId, bAgree)
        if not self._crossTeamId():
            return

        if not self._isCrossTeamCaptain():
            LOG_WARN('replyBecomeCrossCaptain, not captain', self.gbId)
            return

        gameengine.getCrossTeamStub(self._crossTeamId()).replyBecomeCaptain(
            self.base,
            self._crossTeamId(),
            self.gbId,
            gbId,
            bAgree
        )

    @utils.isMyself
    @gamedecorator.limitcall(0.5)
    def applyDisbandCrossTeam(self, exposed):
        LOG_INFO('applyDisbandCrossTeam', self.gbId, self._crossTeamId())
        if not self._crossTeamId():
            return

        if not self._isCrossTeamCaptain():
            LOG_WARN('applyDisbandCrossTeam, not captain', self.gbId)
            return

        gameengine.getCrossTeamStub(self._crossTeamId()).disbandTeam(
            self.base,
            self._crossTeamId(),
            self.gbId
        )

    @utils.isMyself
    @gamedecorator.limitcall(0.5)
    def reqSetCrossTeamSettings(self, exposed, minLevel, minScore, intro, autoEnter, password):
        # 队伍设置：门槛/介绍/满员自动进本/密码（目标创建后不可改，不在本接口范围内）；
        # autoMatch 修改频率高，走 reqSetCrossTeamAutoMatch
        LOG_INFO('reqSetCrossTeamSettings', self.gbId, self._crossTeamId(), autoEnter)
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
    @gamedecorator.limitcall(0.5)
    def reqSetCrossTeamAutoMatch(self, exposed, autoMatch):
        # 自动匹配开关（修改频率高，与队伍目标拆分）；队长身份由中心复核
        LOG_INFO('reqSetCrossTeamAutoMatch', self.gbId, self._crossTeamId(), autoMatch)
        if not self._crossTeamId():
            return

        gameengine.getCrossTeamStub(self._crossTeamId()).setAutoMatch(
            self.base,
            self._crossTeamId(),
            autoMatch,
            self.gbId
        )

    @utils.isMyself
    @gamedecorator.limitcall(0.5)
    def reqCrossTeamMatch(self, exposed, target):
        LOG_INFO('reqCrossTeamMatch', self.gbId, target)
        # 本服匹配状态判重（第一道拦截，中心 pool map 查重兜底）
        if self.crossTeamMatchTarget:
            LOG_WARN('reqCrossTeamMatch, already matching', self.gbId, self.crossTeamMatchTarget)
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
    @gamedecorator.limitcall(0.5)
    def reqStopCrossTeamMatch(self, exposed):
        LOG_INFO('reqStopCrossTeamMatch', self.gbId)
        if not self.crossTeamMatchTarget:
            return

        self.crossTeamMatchTarget = 0
        gameengine.getCrossTeamStub(self.gbId).leaveMatchPool(
            self.base,
            self.gbId
        )

    @utils.isMyself
    @gamedecorator.limitcall(0.5)
    def reqGetCrossTeamList(self, exposed, target):
        # 一波全量下发（问题记录#5）：回包由 Stub 经 base streamStringProxy 分片下发，不再经 cell
        gameengine.getCrossTeamStub(self.gbId).getTeamList(
            self.base,
            target
        )

    @utils.isMyself
    @gamedecorator.limitcall(0.5)
    def switchCrossTeamMicsMode(self, exposed, mode):
        # 麦模式切换（队长操作，队长身份校验在 cell 侧 crossTeamInfo 上完成）
        if not self._isCrossTeamCaptain():
            LOG_WARN('switchCrossTeamMicsMode, not captain', self.gbId)
            return

        gameengine.getCrossTeamStub(self._crossTeamId()).setMicsMode(
            self.base,
            self._crossTeamId(),
            mode,
            self.gbId
        )

    @utils.isMyself
    @gamedecorator.limitcall(0.5)
    def reqSetCrossTeamMemberMicBlock(self, exposed, gbId, blocked):
        # 禁麦/解除禁麦（队长操作）：block/unblock 合并为一个入口，blocked=True 禁麦
        if not self._isCrossTeamCaptain():
            LOG_WARN('reqSetCrossTeamMemberMicBlock, not captain', self.gbId)
            return

        gameengine.getCrossTeamStub(self._crossTeamId()).blockMic(
            self.base,
            self._crossTeamId(),
            gbId,
            blocked,
            self.gbId
        )

    @utils.isMyself
    @gamedecorator.limitcall(0.5)
    def reqAdjustCrossTeamMemberPos(self, exposed, srcGbId, srcGroupIdx, dstGbId, dstGroupIdx):
        # 成员位置调整（队长操作）：srcGbId/srcGroupIdx 为被调整成员，dstGbId/dstGroupIdx
        # 为目标成员/目标小组；dstGbId==0 表示移动到 dstGroupIdx 组末尾
        LOG_INFO('reqAdjustCrossTeamMemberPos', self.gbId, self._crossTeamId(),
                 srcGbId, srcGroupIdx, dstGbId, dstGroupIdx)
        if not self._crossTeamId():
            return
        if not self._isCrossTeamCaptain():
            LOG_WARN('reqAdjustCrossTeamMemberPos, not captain', self.gbId)
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
    @gamedecorator.limitcall(0.5)
    def reqGetCrossTeamPreview(self, exposed, teamId):
        # 队伍预览（决策 D4）：按需查询指定队伍成员列表，不随列表下发；
        # 经 Stub 走 queryTeam 的 teamId 直查路径，回包走 onCrossTeamPreview
        LOG_INFO('reqGetCrossTeamPreview', self.gbId, teamId)
        if teamId <= 0:
            return

        gameengine.getCrossTeamStub(teamId).queryTeamById(
            self.base,
            teamId
        )

    @utils.isMyself
    @gamedecorator.limitcall(0.5)
    def turnOnCrossTeamMics(self, exposed):
        # 成员自己开麦（本服 turnOnTeamMics 对应）
        LOG_INFO('turnOnCrossTeamMics', self.gbId, self._crossTeamId())
        if not self._crossTeamId():
            return

        # 队长麦（LEADER）模式下仅队长可开麦
        # （语义照本服 user_type/team.py turnOnTeamMemberMics 的 LEADER 分支）
        if self.crossTeamInfo.micsMode == gameconst.TeamMicsModeEnum.LEADER and \
                not self._isCrossTeamCaptain():
            LOG_WARN('turnOnCrossTeamMics, leader mics mode limit', self.gbId)
            return

        self._setCrossTeamVoiceState(enableMics=True)

    @utils.isMyself
    @gamedecorator.limitcall(0.5)
    def turnOffCrossTeamMics(self, exposed):
        # 成员自己关麦（本服 turnOffTeamMics 对应）
        LOG_INFO('turnOffCrossTeamMics', self.gbId, self._crossTeamId())
        if not self._crossTeamId():
            return

        self._setCrossTeamVoiceState(enableMics=False)

    @utils.isMyself
    @gamedecorator.limitcall(0.5)
    def reqUpdateCrossTeamVoiceRoomState(self, exposed, teamId, voiceFlags):
        # 语音房状态位图同步（本服 reqUpdateTeamVoiceRoomState 对应，cell/Avatar.py:1984）；
        # 位定义与本服一致（出处 base/TeamStub.py:1556 reqUpdateVoiceRoomState）：
        # 0x01=inVoiceRoom, 0x02=enableMics, 0x04=enableSpeaker
        LOG_INFO('reqUpdateCrossTeamVoiceRoomState', self.gbId, teamId, voiceFlags)
        if teamId <= 0 or teamId != self._crossTeamId():
            return

        self._setCrossTeamVoiceState(
            enableMics=(voiceFlags & 0x02) != 0,
            enableSpeaker=(voiceFlags & 0x04) != 0,
            inVoiceRoom=(voiceFlags & 0x01) != 0
        )

    @utils.isMyself
    @gamedecorator.limitcall(0.5)
    def reqGetCrossTeamApplyList(self, exposed):
        # 申请列表拉取（仅队长；断线/换队长后重建），回包走 onCrossTeamApplyList
        LOG_INFO('reqGetCrossTeamApplyList', self.gbId, self._crossTeamId())
        if not self._isCrossTeamCaptain():
            LOG_WARN('reqGetCrossTeamApplyList, not captain', self.gbId)
            return

        gameengine.getCrossTeamStub(self._crossTeamId()).getApplyList(
            self.base,
            self._crossTeamId(),
            self.gbId
        )

    @utils.isMyself
    @gamedecorator.limitcall(0.5)
    def reqJoinCrossTeam(self, exposed, teamId, password):
        # 免审批快速加入（本服 reqJoinTeam 对应）：不落地申请记录，中心校验通过直接入队；
        # 有密码的队凭密码直入（未携带->需要密码/不匹配->密码错误，细分码与审批流一致）
        LOG_INFO('reqJoinCrossTeam', self.gbId, teamId)
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
    @gamedecorator.limitcall(0.5)
    def clearCrossApplyJoinDic(self, exposed):
        # 一键清空申请列表（本服 clearApplyJoinDic 对应，仅队长）；
        # 申请人逐个按"被拒绝"通知、队长收空列表，结果回 onCrossTeamOpResult
        LOG_INFO('clearCrossApplyJoinDic', self.gbId)
        if not self._isCrossTeamCaptain():
            LOG_WARN('clearCrossApplyJoinDic, not captain', self.gbId)
            return

        gameengine.getCrossTeamStub(self._crossTeamId()).clearApplyList(
            self.base,
            self._crossTeamId(),
            self.gbId
        )

    @utils.isMyself
    @gamedecorator.limitcall(0.5)
    def reqSetCrossTeamDeputy(self, exposed, deputyGbId):
        # 任命/取消副团长（0=取消；仅队长，本服 transferRaidDeputy 对应）：
        # 全队唯一名额，任命新副团长中心直接覆盖旧的；变更经中心 deputyChangePush
        # 全推后各成员 cell onCrossTeamDeputyChange 落地缓存并透传客户端，
        # 操作结果经 uuid 回执 onCrossTeamOpResult（成功也回）
        LOG_INFO('reqSetCrossTeamDeputy', self.gbId, deputyGbId)
        if not self._isCrossTeamCaptain():
            LOG_WARN('reqSetCrossTeamDeputy, not captain', self.gbId)
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
    @gamedecorator.limitcall(0.5)
    def reqAddCrossMarkMember(self, exposed, markType, markIdx, markName, markGbId, markEntityId, markPos):
        """API: 请求增加跨服队伍标记（仅副本内可用，客户端入口自行控制）"""
        LOG_INFO('reqAddCrossMarkMember', self.gbId, markType, markIdx, markName, markGbId, markEntityId, markPos)
        if not self._crossTeamId():
            return
        if markIdx <= 0 or markIdx > gameconst.TEAM_MARK_MAX_SLOT:
            return
        # 仅队长开关（本服 addMarkMember 同口径：非队长操作静默丢弃；中心权威复核）
        if self.crossTeamInfo.teamMarkInfo.get('onlyCaptainCanMark') and not self._isCrossTeamCaptain():
            LOG_INFO('reqAddCrossMarkMember blocked by onlyCaptainCanMark', self.gbId)
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
    @gamedecorator.limitcall(0.5)
    def reqDelCrossMarkMember(self, exposed, markType, markIdx):
        """API: 请求删除跨服队伍标记（按 type+index 摘除）"""
        LOG_INFO('reqDelCrossMarkMember', self.gbId, markType, markIdx)
        if not self._crossTeamId():
            return
        if markIdx <= 0 or markIdx > gameconst.TEAM_MARK_MAX_SLOT:
            return
        if self.crossTeamInfo.teamMarkInfo.get('onlyCaptainCanMark') and not self._isCrossTeamCaptain():
            LOG_INFO('reqDelCrossMarkMember blocked by onlyCaptainCanMark', self.gbId)
            return

        gameengine.getCrossTeamStub(self._crossTeamId()).reqDelCrossMark(
            self.base, self._crossTeamId(), self.gbId, markType, markIdx)

    @utils.isMyself
    @gamedecorator.limitcall(0.5)
    def reqChangeCrossOnlyCaptain(self, exposed, onlyCaptain):
        """API: 请求改变仅队长可标记开关（仅队长）"""
        LOG_INFO('reqChangeCrossOnlyCaptain', self.gbId, onlyCaptain)
        if not self._isCrossTeamCaptain():
            LOG_WARN('reqChangeCrossOnlyCaptain, not captain', self.gbId)
            return

        gameengine.getCrossTeamStub(self._crossTeamId()).reqChangeCrossOnlyCaptainMark(
            self.base, self._crossTeamId(), self.gbId, onlyCaptain)

    @utils.isMyself
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

        # 入队后若仍在匹配中，清掉本服匹配状态（中心已强制出池）
        if self._crossTeamId() and self.crossTeamMatchTarget:
            self.crossTeamMatchTarget = 0

    def onCrossTeamInfoUpdate(self, teamInfoDict):
        # 登录恢复/全量队伍缓存刷新，经结构化协议下发客户端
        LOG_INFO('onCrossTeamInfoUpdate', teamInfoDict.get('teamId', 0))
        self._applyCrossTeamInfoUpdate(teamInfoDict)
        if self.client:
            self.client.onCrossTeamInfoUpdate(self.crossTeamInfo.toStreamDict())

    def onCrossTeamCenterReconnected(self, stubIdx):
        # 与中心断连重连后的全服对账（CrossTeamStub 经 broadcastToAllAvatar 广播）：
        # 按 gbId 分片过滤（两分片各自重连都会广播，避免重复重查）；
        # 在队玩家以中心当前数据为准全量重查——数据未丢（抖动）则刷新并补齐
        # 断连期丢失的推送，已丢（中心重启）则空回包重置，与登录自愈共用同一链路
        if self.gbId % gameconst.CROSS_TEAMSTUB_CONF_NUM != stubIdx:
            return

        if not self._crossTeamId():
            return

        if self.isCrossServer or self.crossTeammateGbIds:
            # 玩家在跨服服上（本服为残影）或正在跨服副本中：跳过，
            # 回本走重连经 onClientEnabled 自愈；保留副本内队伍 HUD/AOI/加成
            return

        LOG_INFO('onCrossTeamCenterReconnected requery', self.gbId, self._crossTeamId())
        if self.base:
            self.base.queryCrossTeamInfo()

    def onCrossTeamCreateSuccess(self, teamInfoDict):
        LOG_INFO('onCrossTeamCreateSuccess', teamInfoDict.get('teamId', 0))
        self._applyCrossTeamInfoUpdate(teamInfoDict)
        if self.client:
            self.client.onCrossTeamCreateSuccess(self.crossTeamInfo.toStreamDict())

    def onCrossTeamJoinSuccess(self, teamInfoDict):
        # 加入队伍成功：复用全量更新逻辑，并额外回调客户端做加入成功表现
        LOG_INFO('onCrossTeamJoinSuccess', teamInfoDict.get('teamId', 0))
        self._applyCrossTeamInfoUpdate(teamInfoDict)
        if self.client:
            self.client.onCrossTeamJoinSuccess(self.crossTeamInfo.toStreamDict())

    def onCrossTeamOpResult(self, resultCode, teamId, gbId, target):
        LOG_INFO('onCrossTeamOpResult', resultCode, teamId, target)
        if resultCode == gameconst.CROSS_TEAM_RESULT_MATCH_JOIN_INVALID:
            # 撮合入队作废：清本服匹配状态，提示重新发起
            self.crossTeamMatchTarget = 0

        if self.client:
            self.client.onCrossTeamOpResult(resultCode, teamId, target)

    def onCrossTeamMatchTimeout(self, target):
        LOG_INFO('onCrossTeamMatchTimeout', self.gbId, target)
        self.crossTeamMatchTarget = 0
        if self.client:
            self.client.onCrossTeamMatchTimeout(target)

    def onCrossTeamMatchSuccess(self, teamId, target):
        # 两段式入队第一段：中心撮合成功后回调，cell 侧做最终检查并取玩家信息回调 Stub.doMatchJoin
        LOG_INFO('onCrossTeamMatchSuccess', self.gbId, teamId, target, self.crossTeamMatchTarget)

        if self.crossTeamMatchTarget != target:
            LOG_WARN('onCrossTeamMatchSuccess but not matching', self.gbId, self.crossTeamMatchTarget, target)
            return

        if not self._checkCrossTeamMutex():
            # 互斥条件已不满足（在本服队伍/团队/跨服队伍中），无法继续匹配，清状态
            LOG_WARN('onCrossTeamMatchSuccess mutex check fail', self.gbId)
            self.crossTeamMatchTarget = 0
            return

        gameengine.getCrossTeamStub(teamId).doMatchJoin(teamId, target, self._getCrossTeamPlayerInfoDic())

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

        if self.client:
            self.client.onCrossTeamMemberAdd(memberDict)

    def onCrossTeamMemberRemove(self, gbId, changeType):
        if not self._crossTeamId():
            return

        self.crossTeamInfo.removeMember(gbId)
        if self.client:
            self.client.onCrossTeamMemberRemove(gbId, changeType)

    def onCrossTeamLeave(self, teamId, reason):
        # 自己被移出队伍：清空本地缓存并通知客户端离队原因
        LOG_INFO('onCrossTeamLeave', self.gbId, teamId, reason)
        if self.crossTeamInfo:
            self.crossTeamInfo.reset()
        self.onCrossTeamIdChange(0)
        if self.client:
            self.client.onCrossTeamLeave(teamId, reason)

    def onCrossTeamCaptainChange(self, newCaptainGbId):
        if not self._crossTeamId():
            return

        self.crossTeamInfo.setCaptain(newCaptainGbId)
        if self.client:
            self.client.onCrossTeamCaptainChange(newCaptainGbId)

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
        LOG_INFO('onCrossTeamMemberPosChange', self.gbId, self._crossTeamId(),
                 srcGbId, srcGroupIdx, dstGbId, dstGroupIdx)
        if not self._crossTeamId():
            return

        if self.client:
            self.client.onCrossTeamMemberPosChange(srcGbId, srcGroupIdx, dstGbId, dstGroupIdx)

    def onCrossTeamDisband(self, teamId):
        # 解散：清空队伍缓存并通知客户端
        if self.crossTeamInfo:
            self.crossTeamInfo.reset()
        self.onCrossTeamIdChange(0)
        if self.client:
            self.client.onCrossTeamDisband(teamId)

    # ------------------------------------------------------------------
    # 接口对齐补充：Stub -> cell 下行推送（对齐梳理 §3）
    # ------------------------------------------------------------------

    def onCrossTeamPreview(self, teamInfoDict):
        # 队伍预览回包（决策 D4/注记 5）：只下发客户端预览，不灌入自身队伍缓存；
        # 查询失败/队伍不存在回 teamId=0 的完整空结构（FIXED_DICT 键齐全）
        LOG_INFO('onCrossTeamPreview', self.gbId, teamInfoDict.get('teamId', 0) if teamInfoDict else 0)
        if self.client:
            if not teamInfoDict or not teamInfoDict.get('teamId', 0):
                teamInfoDict = crossTeam.CrossTeamCacheVal().toStreamDict()
            self.client.onCrossTeamPreview(teamInfoDict)

    def onCrossTeamApplyList(self, applyList):
        # 申请列表回包（仅队长可拉取；CROSS_TEAM_APPLY_VAL 列表）
        LOG_INFO('onCrossTeamApplyList', self.gbId, len(applyList) if applyList else 0)
        if self.client:
            self.client.onCrossTeamApplyList(applyList or [])

    def onCrossTeamApplyRemove(self, gbId):
        # 申请移除通知（申请被同意/拒绝/超时清理），客户端从申请列表移除
        if self.client:
            self.client.onCrossTeamApplyRemove(gbId)

    def onCrossTeamMatchStart(self, enterTS):
        # 入池成功确认（客户端匹配 UI 读配表 maxMatchTime 倒计时，决策 D5）；
        # 本地匹配状态（crossTeamMatchTarget）在 reqCrossTeamMatch 时已置位
        LOG_INFO('onCrossTeamMatchStart', self.gbId, self.crossTeamMatchTarget, enterTS)
        if self.client:
            self.client.onCrossTeamMatchStart(enterTS)

    def onCrossTeamMatchStop(self):
        # 取消匹配确认（撮合成功/超时分别走 onCrossTeamMatchSuccess/onCrossTeamMatchTimeout）
        LOG_INFO('onCrossTeamMatchStop', self.gbId, self.crossTeamMatchTarget)
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

    def onCrossTeamDeputyChange(self, deputyGbId):
        # 副团长变更（中心 setDeputy 后经 deputyChangePush 全推；deputyGbId=0 表示取消）：
        # 更新 crossTeamInfo 缓存并透传客户端
        if not self._crossTeamId():
            return

        self.crossTeamInfo.setDeputy(deputyGbId)
        if self.client:
            self.client.onCrossTeamDeputyChange(deputyGbId)

    def onCrossTeamMarkChange(self, changeType, markInfoDict, onlyCaptainCanMark, dealMonGbid):
        # 队伍标记单条增量变更（中心 markChangePush 经本服 Stub 转发）：
        # 落地本地镜像 + 透传客户端；MARK_ENEMY 增删时同步怪物 cell 记录
        # （怪物死亡自动摘除的依赖；找不到实体说明怪物不在本进程，跳过即可）
        if not self._crossTeamId():
            return

        self.crossTeamInfo.applyMarkChange(changeType, markInfoDict, onlyCaptainCanMark)
        if self.client:
            self.client.onCrossTeamMarkChange(changeType, markInfoDict, onlyCaptainCanMark)

        if markInfoDict.get('type') == gameconst.TeamMarkType.MARK_ENEMY and self.gbId == dealMonGbid:
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

    def onCrossTeamIdChange(self, teamId):
        # 队伍镜像更新；在队期间开启 3s 状态同步定时器；同步 base 镜像（聊天用）
        LOG_INFO('onCrossTeamIdChange', self.gbId, self.crossTeamId, '->', teamId)
        self.crossTeamId = teamId
        if self.base:
            self.base.syncCrossTeamIdToBase(teamId)

        if teamId:
            if not self. crossTeamStateSyncTimer:
                self.crossTeamStateSyncTimer = self.pyAddTimer(1, 1, gametimer.CROSS_TEAM_AVATAR_STATE_TICK)
        elif self.crossTeamStateSyncTimer:
            self.pyDelTimer(self.crossTeamStateSyncTimer, gametimer.CROSS_TEAM_AVATAR_STATE_TICK)
            self.crossTeamStateSyncTimer = 0

        if not teamId and self.crossTeammateGbIds:
            # 被移出跨服队伍：清理副本队友缓存
            self.onCrossCrusadeSpaceLeave()

    def _syncCrossTeamState(self):
        # 向当前所在服 Stub 同步自身状态（由 Stub 聚合后 3s 上报中心；
        # 跨服副本中由跨服服上的镜像执行，中心据此把推送路由切换到跨服服）
        if not self._crossTeamId():
            return

        if self.isCrossServerInLocalServer:
            # 本服镜像（玩家已迁往跨服服，客户端不在本服）：停止上报，
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
        gameengine.getCrossTeamStub(self._crossTeamId()).syncMemberState(
            self._crossTeamId(),
            self.gbId,
            _stateDict
        )

    def leaveCrossTeamAuto(self, reason=None):
        LOG_INFO('leaveCrossTeamAuto', self.gbId, self._crossTeamId(), reason)
        # 离线：上报中心移出队伍（离线即退队）
        # 保护：跨服副本结束返回本服时，镜像 cell 走 offline 流程并非真实掉线，
        # 此时不应上报 memberOffline，否则结算后回到本服会被错误移出跨服队伍。
        # 副本中主动退出（未结算）的退队由 TeamDungeonStub/RaidDungeonStub.leaveDungeonSpaceSucc
        # 跨服分支中的 leaveTeam 负责，不依赖此处重复上报。
        if reason == gameconst.OFFLINE_REASON_END_CROSS_SERVER:
            LOG_INFO('leaveCrossTeamAuto skip cross server return', self.gbId, self._crossTeamId())
            return

        if not self._crossTeamId():
            return

        gameengine.getCrossTeamStub(self._crossTeamId()).memberOffline(
            self._crossTeamId(),
            self.gbId
        )

    # ------------------------------------------------------------------
    # 跨服副本内队友缓存（AOI 刷怪加成/队友保护数据源）
    # ------------------------------------------------------------------

    def isCrossTeammate(self, gbId):
        # 跨服讨伐队友判定（副本内 AOI/目标选择用）
        return gbId in self.crossTeammateGbIds
