# coding: utf-8
# 跨服组队本服代理：
# - 本服与跨服服务器均部署，teamId % M 分片（照搬 TeamStub 创建/路由模式）；
# - 与组队中心 crossTeamServer 保持长连接（配置 + 单点连接 + 5s 重连 + 心跳，照 LeaseStub 模式）；
# - 纯转发层：不维护队伍数据缓存，下行推送的本服成员路由一律使用中心随推送下发的
#   receiverGbIds / 全量成员列表（含 serverId），全量数据由 pb 直接转 streamDict 下发；
# - 例外（问题记录#5）：队伍列表按 target 缓存 CROSS_TEAM_LIST_CACHE_SECONDS 秒
#   （json+gzip 后的 blob），命中期查询直接经 base streamStringProxy 分片回缓存数据；
# - 聚合本服成员状态 3s 定时上报中心（stateReportCache 为短周期缓冲）；
# - 登录恢复已移除（离线即退队）：客户端可经 reqQueryCrossTeamInfo 主动全量查询，
#   回包按 uuid 经 remoteCallCache 原路回调。
# 注意：推送给 Avatar 的方法（onCrossTeamInfoUpdate 等）在阶段 4 下半注册 iAvatarCrossTeam.def，
#       异步回包经缓存的 box/method 直接回调（目标为 cell 时存 box.cell，base 时存 base box），
#       广播推送按目标分别经 PlayerStub.doOnOthersBase/Cell/Client 路由。
# 讨伐副本：副本空间由对应 dungeonNo 的 CrossTeamDungeonStub 管理（每 dungeonNo 一个 owner stub，
# 跨服服上的空间 dungeonPlayMode 落 CROSS_CRUSADE/CROSS_CHIEF，本服模式落 CRUSADE/CHIEF，
# 跨服队伍归属统一走 SpaceVal.crossTeamId 判定）；
# 本 Stub 只承担中心 RPC 中转（建空间触发/就绪回报/完成复位/退队/离线）与 teamId->空间 的
# 短周期簿记（crusadeDungeonCache/crusadeSpaceCache）。

from rpc import RpcChannel

import gzip
import json

import KBEngine
from KBEDebug import *
import utils
import iGlobal
import iBaseNoCell
import iTimer
import gametimer
import gameconfig
import gameengine
import gameconst
import dungeonPlayMode
import crossTeam
import gameglobal
import gamedecorator

import gamePlay_gamePlay as DDI
import teamMatch_matchConfig as TMMCD

from proto.gameServerCrossTeam_pb2 import GameServer, CrossTeamServer_Stub, RegisterGameServerRequest, Void, CreateTeamRequest,\
    JoinApplyRequest, ReqJoinRequest, ClearApplyListRequest, SetDeputyRequest, ReplyApplyRequest, InviteRequest, ReplyInviteRequest, LeaveTeamRequest, KickRequest, TransferCaptainRequest,\
    DisbandRequest, SetTeamSettingsRequest, SetAutoMatchRequest, GetTeamListRequest, EnterMatchPoolRequest, LeaveMatchPoolRequest, MatchJoinRequest,\
    ReportMemberStateRequest, TeamChatMsgRequest, QueryTeamRequest, MemberOfflineRequest, SetMicsModeRequest, BlockMicRequest,\
    AdjustMemberPosRequest, AdjustMemberPosPushMsg, SetVoiceStateRequest, GetApplyListRequest,\
    ApplyBecomeCaptainRequest, ReplyBecomeCaptainRequest,\
    MemberJoinPushMsg, MemberLeavePushMsg, CaptainChangePushMsg, DeputyChangePushMsg, TeamDisbandPushMsg,\
    TeamSettingsChangePushMsg, TeamAutoMatchChangePushMsg, TeamMicsModeChangePushMsg, MemberMicBlockPushMsg,\
    StartCrusadeRequest, CrusadeCheckResultRequest, CrusadeSpaceReadyRequest, CrusadeFinishedRequest,\
    DungeonCDRefreshPushMsg, AddMarkRequest, DelMarkRequest, SetOnlyCaptainMarkRequest, FollowAskRequest


class CrossTeamService(GameServer):
    def __init__(self, mgr, address):
        super().__init__()
        self.mgr = mgr
        self.channel = RpcChannel.RpcChannel(self)
        self.serviceStub = CrossTeamServer_Stub(self.channel)

        _address = address.split(':')
        self.channel.connect((_address[0], int(_address[1])))

    def on_disconnected(self):
        self.mgr.onCrossTeamServerDisconnected()

    def on_connected(self):
        self.mgr.onCrossTeamServerConnected()

    def activeTickCallback(self, rpc_controller, reply, done):
        pass

    def teamOpResult(self, rpc_controller, reply, done):
        self.mgr.onTeamOpResult(reply)

    def replyApplyNotify(self, rpc_controller, reply, done):
        if not self.mgr._isMyTeam(reply.teamId):
            return
        self.mgr.onReplyApplyNotify(reply)

    def teamCreateSuccessPush(self, rpc_controller, reply, done):
        if not self.mgr._isMyTeam(reply.team.teamId):
            return
        self.mgr.onTeamCreateSuccessPush(reply)

    def teamJoinSuccessPush(self, rpc_controller, reply, done):
        if not self.mgr._isMyTeam(reply.team.teamId):
            return
        self.mgr.onTeamJoinSuccessPush(reply)

    def memberJoinPush(self, rpc_controller, reply, done):
        if not self.mgr._isMyTeam(reply.teamId):
            return
        self.mgr.onMemberJoinPush(reply)

    def memberLeavePush(self, rpc_controller, reply, done):
        if not self.mgr._isMyTeam(reply.teamId):
            return
        self.mgr.onMemberLeavePush(reply)

    def captainChangePush(self, rpc_controller, reply, done):
        if not self.mgr._isMyTeam(reply.teamId):
            return
        self.mgr.onCaptainChangePush(reply)

    def deputyChangePush(self, rpc_controller, reply, done):
        if not self.mgr._isMyTeam(reply.teamId):
            return
        self.mgr.onDeputyChangePush(reply)

    def becomeCaptainApplyPush(self, rpc_controller, reply, done):
        if not self.mgr._isMyTeam(reply.teamId):
            return
        self.mgr.onBecomeCaptainApplyPush(reply)

    def teamDisbandPush(self, rpc_controller, reply, done):
        if not self.mgr._isMyTeam(reply.teamId):
            return
        self.mgr.onTeamDisbandPush(reply)

    def teamSettingsChangePush(self, rpc_controller, reply, done):
        if not self.mgr._isMyTeam(reply.teamId):
            return
        self.mgr.onTeamSettingsChangePush(reply)

    def teamAutoMatchChangePush(self, rpc_controller, reply, done):
        if not self.mgr._isMyTeam(reply.teamId):
            return
        self.mgr.onTeamAutoMatchChangePush(reply)

    def teamMicsModeChangePush(self, rpc_controller, reply, done):
        if not self.mgr._isMyTeam(reply.teamId):
            return
        self.mgr.onTeamMicsModeChangePush(reply)

    def memberMicBlockPush(self, rpc_controller, reply, done):
        if not self.mgr._isMyTeam(reply.teamId):
            return
        self.mgr.onMemberMicBlockPush(reply)

    def adjustMemberPosPush(self, rpc_controller, reply, done):
        if not self.mgr._isMyTeam(reply.teamId):
            return
        self.mgr.onAdjustMemberPosPush(reply)

    def teamListResult(self, rpc_controller, reply, done):
        self.mgr.onTeamListResult(reply)

    def matchSuccess(self, rpc_controller, reply, done):
        if not self.mgr._isMyTeam(reply.teamId):
            return
        self.mgr.onMatchSuccess(reply)

    def matchTimeout(self, rpc_controller, reply, done):
        if not self.mgr._isMyGbId(reply.gbId):
            return
        self.mgr.onMatchTimeout(reply)

    def broadcastMemberState(self, rpc_controller, reply, done):
        if not self.mgr._isMyTeam(reply.teamId):
            return
        self.mgr.onBroadcastMemberState(reply)

    def teamChatBatch(self, rpc_controller, reply, done):
        if not self.mgr._isMyTeam(reply.teamId):
            return
        self.mgr.onTeamChatBatch(reply)

    def crusadeCheck(self, rpc_controller, reply, done):
        if not self.mgr._isMyTeam(reply.teamId):
            return
        self.mgr.onCrusadeCheck(reply)

    def crusadeGo(self, rpc_controller, reply, done):
        if not self.mgr._isMyTeam(reply.teamId):
            return
        self.mgr.onCrusadeGo(reply)

    def crusadeAbort(self, rpc_controller, reply, done):
        if not self.mgr._isMyTeam(reply.teamId):
            return
        self.mgr.onCrusadeAbort(reply)

    def createCrusadeSpace(self, rpc_controller, reply, done):
        if not self.mgr._isMyTeam(reply.teamId):
            return
        self.mgr.onCreateCrusadeSpace(reply)

    def teamDataResp(self, rpc_controller, reply, done):
        # 客户端主动查询回包：单播（中心已按 uuid 路由回请求来源连接），直接处理
        self.mgr.onTeamDataResp(reply)

    def queryTeamCrossResp(self, rpc_controller, reply, done):
        # 跨服讨伐进本前校验：单播回包（中心已按 teamId 路由到本服对应 Stub），直接处理
        self.mgr.onQueryTeamCrossResp(reply)

    def joinApplyNotify(self, rpc_controller, reply, done):
        if not self.mgr._isMyTeam(reply.teamId):
            return
        self.mgr.onJoinApplyNotify(reply)

    def inviteNotify(self, rpc_controller, reply, done):
        if not self.mgr._isMyTeam(reply.teamId):
            return
        self.mgr.onInviteNotify(reply)

    def memberVoiceStatePush(self, rpc_controller, reply, done):
        if not self.mgr._isMyTeam(reply.teamId):
            return
        self.mgr.onMemberVoiceStatePush(reply)

    def matchStart(self, rpc_controller, reply, done):
        if not self.mgr._isMyGbId(reply.gbId):
            return
        self.mgr.onMatchStart(reply)

    def matchStop(self, rpc_controller, reply, done):
        if not self.mgr._isMyGbId(reply.gbId):
            return
        self.mgr.onMatchStop(reply)

    def applyListPush(self, rpc_controller, reply, done):
        # 申请列表应答：单播（中心已按 uuid 路由回请求来源连接），直接处理
        self.mgr.onApplyListPush(reply)

    def applyRemoveNotify(self, rpc_controller, reply, done):
        if not self.mgr._isMyTeam(reply.teamId):
            return
        self.mgr.onApplyRemoveNotify(reply)

    def dungeonCDRefreshPush(self, rpc_controller, reply, done):
        if not self.mgr._isMyTeam(reply.teamId):
            return
        self.mgr.onDungeonCDRefreshPush(reply)

    def markChangePush(self, rpc_controller, reply, done):
        if not self.mgr._isMyTeam(reply.teamId):
            return
        self.mgr.onMarkChangePush(reply)

    def followAskPush(self, rpc_controller, reply, done):
        if not self.mgr._isMyTeam(reply.teamId):
            return
        self.mgr.onFollowAskPush(reply)


class CrossTeamStub(iGlobal.IGlobal, iBaseNoCell.IBaseNoCell, iTimer.ITimer):
    SERVICE_CLASS = CrossTeamService

    def __init__(self):
        LOG_INFO('CrossTeamStub __init__')
        self.crossTeamService = None
        self.initDatetimeTimerTick()

        self.remoteCallCache    = {} # rpc 回调缓存
        self.stateReportCache   = {} # 高频状态同步缓冲
        # 队伍列表缓存（问题记录#5）：{target: {'data': gzip blob, 'ts': 生成时间戳}}，
        # 命中期（CROSS_TEAM_LIST_CACHE_SECONDS 秒）内查询直接回缓存，过期才向中心拉取
        self.teamListCache      = {}
        # 是否曾连上过中心：仅断连重连才触发全服重查对账，首连（进程重启）不触发
        self._hasConnectedBefore = False

    def _fullPrepare(self):
        self.pyAddTimer(1, 1, gametimer.CROSS_TEAM_STUB_CONNECT_TICK)
        self.pyAddTimer(10, 10, gametimer.CROSS_TEAM_STUB_ACTIVE_TICK)

        self.pyAddTimer(
            gameconst.CROSS_TEAM_REPORT_STATE_INTERVAL,
            gameconst.CROSS_TEAM_REPORT_STATE_INTERVAL,
            gametimer.CROSS_TEAM_REPORT_STATE_TICK
        )

        # 异步 RPC 回包缓存清理（5 分钟一次，30 分钟过期）
        self.pyAddTimer(300, 300, gametimer.CROSS_TEAM_CLEAR_REMOTE_CALL_CACHE)

    def onTimer(self, tid, userArg):
        if utils.isBelongTimerTag(userArg):
            self._onTimerCallback(tid)
        elif userArg == gametimer.TIMER_DATETIME_ITIMER_CALLBACK:
            self._onDatetimeTimerTick()
        elif userArg == gametimer.CROSS_TEAM_STUB_CONNECT_TICK:
            self.connectCrossTeamCenter()
        elif userArg == gametimer.CROSS_TEAM_STUB_ACTIVE_TICK:
            self.sendActiveTick()
        elif userArg == gametimer.CROSS_TEAM_REPORT_STATE_TICK:
            self.reportMemberStates()
        elif userArg == gametimer.CROSS_TEAM_CLEAR_REMOTE_CALL_CACHE:
            self._clearRemoteCallCache()
        else:
            self._onTimerTrigger(tid, userArg)

    def doNext(self):
        LOG_DBG('CrossTeamStub doNext, stubIdx=%s' % getattr(self, 'stubIdx', 0))
        self._fullPrepare()
        gameglobal.localBaseApp.fullPrepare(self.classname())

    # ------------------------------------------------------------------
    # 分片判断：中心服按 serverId 广播到本服全部 stub，本层按 teamId/gbId 过滤
    # ------------------------------------------------------------------

    def _myStubIdx(self):
        return getattr(self, 'stubIdx', 0)

    def _isMyTeam(self, teamId):
        return teamId % gameconst.CROSS_TEAMSTUB_CONF_NUM == self._myStubIdx()

    def _isMyGbId(self, gbId):
        return gbId % gameconst.CROSS_TEAMSTUB_CONF_NUM == self._myStubIdx()

    # ------------------------------------------------------------------
    # 连接管理
    # ------------------------------------------------------------------

    def connectCrossTeamCenter(self):
        if not gameconfig.enableCrossTeam(): return

        _address = gameconfig.crossTeamServerAddress()
        if not _address:
            LOG_WARN('CrossTeamStub _connectCrossTeamCenter no config')
            return

        if not (self.crossTeamService and self.crossTeamService.channel.dispatcher):
            LOG_INFO('connect crossTeamCenter---------:', _address)
            self.crossTeamService = CrossTeamService(self, _address)

    def onCrossTeamServerConnected(self):
        LOG_INFO('CrossTeamStub onCrossTeamServerConnected')
        serverId = gameconfig.serverId()

        _req = RegisterGameServerRequest()
        _req.serverId = serverId

        if self.crossTeamService and self.crossTeamService.channel.dispatcher:
            self.crossTeamService.serviceStub.registerGameServer(None, _req, None)

        # 断连重连：广播全服在队玩家向中心重查队伍数据对账（按本分片 gbId 半区过滤）。
        # 中心数据未丢（抖动）则全量刷新并补齐断连期丢失的推送；已丢（中心重启）则空回包重置。
        # 首次连接（Stub/进程重启）中心数据未丢，不广播
        if self._hasConnectedBefore:
            LOG_INFO('CrossTeamStub broadcast requery after reconnect', self._myStubIdx())
            gameengine.broadcastBaseapp(
                'broadcastToAllAvatar',
                (gameconst.CELL, 'onCrossTeamCenterReconnected', (self._myStubIdx(),), ())
            )
        self._hasConnectedBefore = True

    def onCrossTeamServerDisconnected(self):
        LOG_INFO('CrossTeamStub onCrossTeamServerDisconnected')

    def sendActiveTick(self):
        if not (self.crossTeamService and self.crossTeamService.channel.dispatcher):
            return

        self.crossTeamService.serviceStub.activeTick(None, Void(), None)

    def _getService(self, funcName):
        _service = self.crossTeamService
        if not (_service and _service.channel.dispatcher):
            LOG_WARN('CrossTeamStub %s no service' % funcName)
            return None
        return _service

    def _cacheRemoteCall(self, uuid, box, method, args=None):
        # 缓存异步 RPC 回包所需上下文：box/method/args/ts
        self.remoteCallCache[uuid] = {
            'box': box,
            'method': method,
            'args': args or (),
            'ts': utils.curTS(),
        }

    def _clearRemoteCallCache(self):
        _now = utils.curTS()
        _expired = [_uuid for _uuid, _cache in self.remoteCallCache.items() if _now - _cache.get('ts', _now) > 1800]
        for _uuid in _expired:
            self.remoteCallCache.pop(_uuid, None)
        if _expired:
            LOG_DBG('CrossTeamStub _clearRemoteCallCache removed', len(_expired))

        # 列表缓存同周期清理（30 分钟过期，不再被查询的 target 残留回收）
        _expiredTargets = [_target for _target, _cache in self.teamListCache.items() if _now - _cache.get('ts', _now) > 1800]
        for _target in _expiredTargets:
            self.teamListCache.pop(_target, None)

    # ------------------------------------------------------------------
    # 本服成员通知：统一经 PlayerStub 路由到本服玩家 base/cell。
    # 本服成员名单不再由本地缓存维护，一律取中心推送里的 receiverGbIds
    # ------------------------------------------------------------------

    # ------------------------------------------------------------------
    # 上行：Avatar -> Stub -> 中心（方法已在 CrossTeamStub.def 注册）
    # ------------------------------------------------------------------

    def createTeam(self, box, teamId, target, minLevel, minScore, password, intro, autoMatch, maxNum, dungeonMap, autoEnter, memberInfo):
        LOG_INFO('CrossTeamStub createTeam', teamId, target, dungeonMap, autoEnter, memberInfo.get('gbId'))
        _service = self._getService('createTeam')
        if not _service:
            return

        _req = CreateTeamRequest()
        _req.uuid = KBEngine.genUUID64()
        _req.teamId = teamId
        _req.target = target
        _req.minLevel = minLevel
        _req.minScore = minScore
        _req.password = password
        _req.intro = intro
        _req.autoMatch = autoMatch
        _req.maxNum = maxNum
        _req.dungeonMap = dungeonMap
        _req.autoEnter = autoEnter
        # 本服链路（第三步）：isCross/dunServer 由建队 cell 读配表/gameconfig 算出后
        # 借 memberInfo（PY_DICT）透传，此处取出上行中心（创建时固化，中心与配置解耦仅识别字段）
        _req.isCross = bool(memberInfo.get('isCross', True))
        _req.dunServer = memberInfo.get('dunServer', 0)
        _req.captain.gbId = memberInfo.get('gbId', 0)
        _req.captain.serverId = gameconfig.serverId()
        _req.captain.name = memberInfo.get('playerName', '')
        _req.captain.level = memberInfo.get('level', 0)
        _req.captain.school = memberInfo.get('school', 0)
        _req.captain.score = memberInfo.get('score', 0)
        _req.captain.sex = memberInfo.get('sex', 0)
        _req.captain.picFrameId = memberInfo.get('picFrameId', 0)
        _req.captain.openId = memberInfo.get('openId', '')

        self._cacheRemoteCall(_req.uuid, box.cell, 'onCrossTeamOpResult')
        _service.serviceStub.createTeam(None, _req, None)

    def applyJoinTeam(self, box, teamId, password, memberInfo, applySource):
        LOG_INFO('CrossTeamStub applyJoinTeam', teamId, memberInfo.get('gbId'), applySource)
        _service = self._getService('applyJoinTeam')
        if not _service:
            return

        _req = JoinApplyRequest()
        _req.uuid = KBEngine.genUUID64()
        _req.teamId = teamId
        _req.password = password
        _req.applySource = applySource
        _req.applicant.gbId = memberInfo.get('gbId', 0)
        _req.applicant.serverId = gameconfig.serverId()
        _req.applicant.name = memberInfo.get('playerName', '')
        _req.applicant.level = memberInfo.get('level', 0)
        _req.applicant.school = memberInfo.get('school', 0)
        _req.applicant.score = memberInfo.get('score', 0)
        _req.applicant.sex = memberInfo.get('sex', 0)
        _req.applicant.picFrameId = memberInfo.get('picFrameId', 0)
        _req.applicant.openId = memberInfo.get('openId', '')

        # 申请结果（成功/失败）统一经中心 replyApplyNotify 主动通知申请人，
        # 不再走 TeamOpResult uuid 回执，故无需注册 remoteCallCache
        _service.serviceStub.joinApply(None, _req, None)

    def reqJoinTeam(self, box, teamId, password, memberInfo):
        # 免审批快速入队（本服 reqJoinTeam 对应）：不落地申请记录，中心校验通过直接入队；
        # 结果同审批流统一经 replyApplyNotify 主动通知申请人，不走 uuid 回执
        LOG_INFO('CrossTeamStub reqJoinTeam', teamId, memberInfo.get('gbId'))
        _service = self._getService('reqJoin')
        if not _service:
            return

        _req = ReqJoinRequest()
        _req.uuid = KBEngine.genUUID64()
        _req.teamId = teamId
        _req.password = password
        _req.applicant.gbId = memberInfo.get('gbId', 0)
        _req.applicant.serverId = gameconfig.serverId()
        _req.applicant.name = memberInfo.get('playerName', '')
        _req.applicant.level = memberInfo.get('level', 0)
        _req.applicant.school = memberInfo.get('school', 0)
        _req.applicant.score = memberInfo.get('score', 0)
        _req.applicant.sex = memberInfo.get('sex', 0)
        _req.applicant.picFrameId = memberInfo.get('picFrameId', 0)
        _req.applicant.openId = memberInfo.get('openId', '')

        _service.serviceStub.reqJoin(None, _req, None)

    def clearApplyList(self, box, teamId, captainGbId):
        # 一键清空申请列表（本服 clearApplyJoinDic 对应，队长操作）：
        # 申请人逐个按"被拒绝"通知、队长收空列表；操作结果经 uuid 回执 onCrossTeamOpResult
        LOG_INFO('CrossTeamStub clearApplyList', teamId, captainGbId)
        _service = self._getService('clearApplyList')
        if not _service:
            return

        _req = ClearApplyListRequest()
        _req.uuid = KBEngine.genUUID64()
        _req.teamId = teamId
        _req.captainGbId = captainGbId

        self._cacheRemoteCall(_req.uuid, box.cell, 'onCrossTeamOpResult')
        _service.serviceStub.clearApplyList(None, _req, None)

    def reqSetDeputy(self, box, teamId, captainGbId, deputyGbId):
        # 任命/取消副团长（本服 transferRaidDeputy 对应，队长操作）：
        # 中心校验（队长/成员/取消须有副团长）后全队推送 deputyChangePush，
        # 操作结果经 uuid 回执 onCrossTeamOpResult（成功也回，操作者 UI 闭环）
        LOG_INFO('CrossTeamStub reqSetDeputy', teamId, captainGbId, deputyGbId)
        _service = self._getService('reqSetDeputy')
        if not _service:
            return

        _req = SetDeputyRequest()
        _req.uuid = KBEngine.genUUID64()
        _req.teamId = teamId
        _req.captainGbId = captainGbId
        _req.deputyGbId = deputyGbId

        self._cacheRemoteCall(_req.uuid, box.cell, 'onCrossTeamOpResult')
        _service.serviceStub.setDeputy(None, _req, None)

    # ------------------------------------------------------------------
    # 队伍标记三件套上行（本服 reqAddMarkMember/reqDelMarkMember/reqChangeOnlyCaptain 对应）：
    # 数据存中心，变更经中心 markChangePush 单条增量下发（只发队长当前所在服）；
    # 对齐本服静默语义：不走 uuid 回执，校验失败仅中心日志
    # ------------------------------------------------------------------

    def reqAddCrossMark(self, box, teamId, operatorGbId, markType, markIdx, markName, markGbId,
                        markEntityId, markPos, spaceNo, serverId):
        LOG_INFO('CrossTeamStub reqAddCrossMark', teamId, operatorGbId, markType, markIdx,
                 markName, markGbId, markEntityId, markPos, spaceNo, serverId)
        _service = self._getService('addMark')
        if not _service:
            return

        _req = AddMarkRequest()
        _req.uuid = KBEngine.genUUID64()
        _req.teamId = teamId
        _req.operatorGbId = operatorGbId
        _req.mark.type = markType
        _req.mark.index = markIdx
        _req.mark.name = markName
        _req.mark.gbId = markGbId
        _req.mark.entId = markEntityId
        _req.mark.posX, _req.mark.posY, _req.mark.posZ = markPos
        _req.mark.spaceNo = spaceNo
        _req.mark.serverId = serverId

        _service.serviceStub.addMark(None, _req, None)

    def reqDelCrossMark(self, box, teamId, operatorGbId, markType, markIdx):
        LOG_INFO('CrossTeamStub reqDelCrossMark', teamId, operatorGbId, markType, markIdx)
        _service = self._getService('delMark')
        if not _service:
            return

        _req = DelMarkRequest()
        _req.uuid = KBEngine.genUUID64()
        _req.teamId = teamId
        _req.operatorGbId = operatorGbId
        _req.type = markType
        _req.index = markIdx

        _service.serviceStub.delMark(None, _req, None)

    def reqChangeCrossOnlyCaptainMark(self, box, teamId, captainGbId, onlyCaptain):
        # 仅队长可标记开关（队长操作；cell 已校验队长，中心复核）
        LOG_INFO('CrossTeamStub reqChangeCrossOnlyCaptainMark', teamId, captainGbId, onlyCaptain)
        _service = self._getService('setOnlyCaptainMark')
        if not _service:
            return

        _req = SetOnlyCaptainMarkRequest()
        _req.uuid = KBEngine.genUUID64()
        _req.teamId = teamId
        _req.captainGbId = captainGbId
        _req.onlyCaptain = onlyCaptain

        _service.serviceStub.setOnlyCaptainMark(None, _req, None)

    def onCrossMarkMonsterDead(self, teamId, markIdx):
        # 被标怪物死亡自动摘除上行（Monster.onDead 调用）：无操作者免校验、无回执
        LOG_INFO('CrossTeamStub onCrossMarkMonsterDead', teamId, markIdx)
        _service = self._getService('markMonsterDead')
        if not _service:
            return

        _req = DelMarkRequest()
        _req.uuid = KBEngine.genUUID64()
        _req.teamId = teamId
        _req.type = gameconst.TeamMarkType.MARK_ENEMY
        _req.index = markIdx

        _service.serviceStub.delMark(None, _req, None)

    def replyJoinApply(self, box, teamId, captainGbId, applicantGbId, bAgree):
        LOG_INFO('CrossTeamStub replyJoinApply', teamId, applicantGbId, bAgree)
        _service = self._getService('replyJoinApply')
        if not _service:
            return

        _req = ReplyApplyRequest()
        _req.uuid = KBEngine.genUUID64()
        _req.teamId = teamId
        _req.captainGbId = captainGbId
        _req.applicantGbId = applicantGbId
        _req.agree = bAgree

        self._cacheRemoteCall(_req.uuid, box.cell, 'onCrossTeamOpResult')
        _service.serviceStub.replyApply(None, _req, None)

    def inviteMember(self, box, teamId, inviterGbId, inviteeGbId, inviteeServerId):
        LOG_INFO('CrossTeamStub inviteMember', teamId, inviterGbId, inviteeGbId)
        _service = self._getService('inviteMember')
        if not _service:
            return

        _req = InviteRequest()
        _req.uuid = KBEngine.genUUID64()
        _req.teamId = teamId
        _req.inviterGbId = inviterGbId
        _req.inviteeGbId = inviteeGbId
        _req.inviteeServerId = inviteeServerId

        self._cacheRemoteCall(_req.uuid, box.cell, 'onCrossTeamOpResult')
        _service.serviceStub.invite(None, _req, None)

    def replyInvite(self, box, teamId, inviteeInfo, bAgree, inviteType):
        LOG_INFO('CrossTeamStub replyInvite', teamId, inviteeInfo.get('gbId'), bAgree, inviteType)
        _service = self._getService('replyInvite')
        if not _service:
            return

        _req = ReplyInviteRequest()
        _req.uuid = KBEngine.genUUID64()
        _req.teamId = teamId
        _req.invitee.gbId = inviteeInfo.get('gbId', 0)
        _req.invitee.serverId = gameconfig.serverId()
        _req.invitee.name = inviteeInfo.get('playerName', '')
        _req.invitee.level = inviteeInfo.get('level', 0)
        _req.invitee.school = inviteeInfo.get('school', 0)
        _req.invitee.score = inviteeInfo.get('score', 0)
        _req.invitee.sex = inviteeInfo.get('sex', 0)
        _req.invitee.picFrameId = inviteeInfo.get('picFrameId', 0)
        _req.invitee.openId = inviteeInfo.get('openId', '')
        _req.agree = bAgree
        _req.inviteType = inviteType

        self._cacheRemoteCall(_req.uuid, box.cell, 'onCrossTeamOpResult')
        _service.serviceStub.replyInvite(None, _req, None)

    def leaveTeam(self, box, teamId, gbId):
        LOG_INFO('CrossTeamStub leaveTeam', teamId, gbId)
        _service = self._getService('leaveTeam')
        if not _service:
            return

        _req = LeaveTeamRequest()
        _req.uuid = KBEngine.genUUID64()
        _req.teamId = teamId
        _req.gbId = gbId

        self._cacheRemoteCall(_req.uuid, box.cell, 'onCrossTeamOpResult')
        _service.serviceStub.leaveTeam(None, _req, None)

    def kickMember(self, box, teamId, kickedGbId, captainGbId):
        LOG_INFO('CrossTeamStub kickMember', teamId, kickedGbId, captainGbId)
        _service = self._getService('kickMember')
        if not _service:
            return

        _req = KickRequest()
        _req.uuid = KBEngine.genUUID64()
        _req.teamId = teamId
        _req.kickedGbId = kickedGbId
        _req.captainGbId = captainGbId

        self._cacheRemoteCall(_req.uuid, box.cell, 'onCrossTeamOpResult')
        _service.serviceStub.kick(None, _req, None)

    def transferCaptain(self, box, teamId, newCaptainGbId, captainGbId):
        LOG_INFO('CrossTeamStub transferCaptain', teamId, newCaptainGbId, captainGbId)
        _service = self._getService('transferCaptain')
        if not _service:
            return

        _req = TransferCaptainRequest()
        _req.uuid = KBEngine.genUUID64()
        _req.teamId = teamId
        _req.newCaptainGbId = newCaptainGbId
        _req.captainGbId = captainGbId

        self._cacheRemoteCall(_req.uuid, box.cell, 'onCrossTeamOpResult')
        _service.serviceStub.transferCaptain(None, _req, None)

    def applyBecomeCaptain(self, box, teamId, gbId):
        # 申请成为队长：成员发起，中心推送队长确认（申请人展示信息由中心成员数据带出）
        LOG_INFO('CrossTeamStub applyBecomeCaptain', teamId, gbId)
        _service = self._getService('applyBecomeCaptain')
        if not _service:
            return

        _req = ApplyBecomeCaptainRequest()
        _req.uuid = KBEngine.genUUID64()
        _req.teamId = teamId
        _req.gbId = gbId

        self._cacheRemoteCall(_req.uuid, box.cell, 'onCrossTeamOpResult')
        _service.serviceStub.applyBecomeCaptain(None, _req, None)

    def replyBecomeCaptain(self, box, teamId, captainGbId, applicantGbId, bAgree):
        # 队长应答"申请成为队长"
        LOG_INFO('CrossTeamStub replyBecomeCaptain', teamId, captainGbId, applicantGbId, bAgree)
        _service = self._getService('replyBecomeCaptain')
        if not _service:
            return

        _req = ReplyBecomeCaptainRequest()
        _req.uuid = KBEngine.genUUID64()
        _req.teamId = teamId
        _req.captainGbId = captainGbId
        _req.applicantGbId = applicantGbId
        _req.agree = bAgree

        self._cacheRemoteCall(_req.uuid, box.cell, 'onCrossTeamOpResult')
        _service.serviceStub.replyBecomeCaptain(None, _req, None)

    def disbandTeam(self, box, teamId, captainGbId):
        LOG_INFO('CrossTeamStub disbandTeam', teamId, captainGbId)
        _service = self._getService('disbandTeam')
        if not _service:
            return

        _req = DisbandRequest()
        _req.uuid = KBEngine.genUUID64()
        _req.teamId = teamId
        _req.captainGbId = captainGbId

        self._cacheRemoteCall(_req.uuid, box.cell, 'onCrossTeamOpResult')
        _service.serviceStub.disband(None, _req, None)

    def setTeamSettings(self, box, teamId, minLevel, minScore, intro, autoEnter, captainGbId, password):
        LOG_INFO('CrossTeamStub setTeamSettings', teamId, autoEnter, captainGbId)
        _service = self._getService('setTeamSettings')
        if not _service:
            return

        _req = SetTeamSettingsRequest()
        _req.uuid = KBEngine.genUUID64()
        _req.teamId = teamId
        _req.minLevel = minLevel
        _req.minScore = minScore
        _req.intro = intro
        _req.autoEnter = autoEnter
        _req.captainGbId = captainGbId
        _req.password = password

        self._cacheRemoteCall(_req.uuid, box.cell, 'onCrossTeamOpResult')
        _service.serviceStub.setTeamSettings(None, _req, None)

    def setAutoMatch(self, box, teamId, autoMatch, captainGbId):
        LOG_INFO('CrossTeamStub setAutoMatch', teamId, autoMatch, captainGbId)
        _service = self._getService('setAutoMatch')
        if not _service:
            return

        _req = SetAutoMatchRequest()
        _req.uuid = KBEngine.genUUID64()
        _req.teamId = teamId
        _req.autoMatch = autoMatch
        _req.captainGbId = captainGbId

        self._cacheRemoteCall(_req.uuid, box.cell, 'onCrossTeamOpResult')
        _service.serviceStub.setAutoMatch(None, _req, None)

    def getTeamList(self, box, target):
        # 队伍列表查询（一波全量，问题记录#5）：命中 target 缓存直接回缓存数据，
        # 否则向中心拉取（回包在 onTeamListResult 填缓存并下发）；box 为请求者 base 邮箱
        _now = utils.curTS()
        _cache = self.teamListCache.get(target)
        if _cache and _now - _cache['ts'] < gameconst.CROSS_TEAM_LIST_CACHE_SECONDS:
            box.streamStringProxy(_cache['data'], '', gameconst.StreamStringID.CROSS_TEAM_LIST_DATA)
            return

        _service = self._getService('getTeamList')
        if not _service:
            return

        _req = GetTeamListRequest()
        _req.uuid = KBEngine.genUUID64()
        _req.target = target
        # 本服链路（第三步）：请求方本服 id 上行，中心据此过滤本服目标队伍
        # （isCross=false 的队伍仅当 dunServer == serverId 时返回）
        _req.serverId = gameconfig.serverId()

        self._cacheRemoteCall(_req.uuid, box, '', ())
        _service.serviceStub.getTeamList(None, _req, None)

    def enterMatchPool(self, box, target, playerInfo):
        _gbId = playerInfo.get('gbId', 0)
        LOG_INFO('CrossTeamStub enterMatchPool', target, _gbId)

        _service = self._getService('enterMatchPool')
        if not _service:
            return

        _req = EnterMatchPoolRequest()
        _req.uuid = KBEngine.genUUID64()
        _req.target = target
        _req.player.gbId = _gbId
        _req.player.serverId = gameconfig.serverId()
        _req.player.name = playerInfo.get('playerName', '')
        _req.player.level = playerInfo.get('level', 0)
        _req.player.score = playerInfo.get('score', 0)
        # 匹配超时下带配表 maxMatchTime（决策 D5，注记 4），读不到回退中心默认（0）
        _req.timeoutSeconds = TMMCD.datas.get('maxMatchTime', {}).get('value', 0)

        _service.serviceStub.enterMatchPool(None, _req, None)

    def leaveMatchPool(self, box, gbId):
        LOG_INFO('CrossTeamStub leaveMatchPool', gbId)

        _service = self._getService('leaveMatchPool')
        if not _service:
            return

        _req = LeaveMatchPoolRequest()
        _req.uuid = KBEngine.genUUID64()
        _req.gbId = gbId
        _service.serviceStub.leaveMatchPool(None, _req, None)

    def syncMemberState(self, teamId, gbId, stateDict):
        # Avatar 状态变化时同步（血量/spaceNo+position 等），Stub 聚合后 3s 定时上报中心
        stateDict['teamId'] = teamId
        self.stateReportCache[gbId] = stateDict

    def memberOffline(self, teamId, gbId):
        # 本服检测到成员离线（离线即退队，中心直接移出）
        LOG_INFO('CrossTeamStub memberOffline', teamId, gbId)
        self.stateReportCache.pop(gbId, None)

        _service = self._getService('memberOffline')
        if not _service:
            return

        _req = MemberOfflineRequest()
        _req.teamId = teamId
        _req.gbId = gbId
        _service.serviceStub.memberOffline(None, _req, None)

    # 客户端主动全量查询：向中心按 gbId 反查，回包经 uuid 从 remoteCallCache 原路回调
    def queryPlayerTeam(self, box, gbId):
        _service = self._getService('queryPlayerTeam')
        if not _service:
            return

        _req = QueryTeamRequest()
        _req.uuid = KBEngine.genUUID64()
        _req.gbId = gbId

        self._cacheRemoteCall(_req.uuid, box.cell, 'onCrossTeamInfoUpdate')
        _service.serviceStub.queryTeam(None, _req, None)

    def queryTeamById(self, box, teamId):
        # 队伍预览（决策 D4）：queryTeam 的 teamId 直查路径，
        # 回包 QueryTeamCrossRespMsg 按 uuid 从 remoteCallCache 回调 cell.onCrossTeamPreview
        LOG_INFO('CrossTeamStub queryTeamById', teamId)
        _service = self._getService('queryTeamById')
        if not _service:
            return

        _req = QueryTeamRequest()
        _req.uuid = KBEngine.genUUID64()
        _req.teamId = teamId

        self._cacheRemoteCall(_req.uuid, box.cell, 'onCrossTeamPreview')
        _service.serviceStub.queryTeam(None, _req, None)

    def setVoiceState(self, box, teamId, gbId, enableMics, enableSpeaker, inVoiceRoom):
        # 成员语音状态同步（客户端位图已在 cell 解包为三态；中心只存不解读，
        # 变更经 memberVoiceStatePush 广播回全队后由各服 cell 落地缓存）
        LOG_INFO('CrossTeamStub setVoiceState', teamId, gbId, enableMics, enableSpeaker, inVoiceRoom)
        _service = self._getService('setVoiceState')
        if not _service:
            return

        _req = SetVoiceStateRequest()
        _req.uuid = KBEngine.genUUID64()
        _req.teamId = teamId
        _req.gbId = gbId
        _req.enableMics = enableMics
        _req.enableSpeaker = enableSpeaker
        _req.inVoiceRoom = inVoiceRoom

        self._cacheRemoteCall(_req.uuid, box.cell, 'onCrossTeamOpResult')
        _service.serviceStub.setVoiceState(None, _req, None)

    def getApplyList(self, box, teamId, gbId):
        # 申请列表拉取（中心仅接受队长拉取；回包 ApplyListPushMsg 单播，
        # 按 uuid 从 remoteCallCache 回调 cell.onCrossTeamApplyList）
        LOG_INFO('CrossTeamStub getApplyList', teamId, gbId)
        _service = self._getService('getApplyList')
        if not _service:
            return

        _req = GetApplyListRequest()
        _req.uuid = KBEngine.genUUID64()
        _req.teamId = teamId
        _req.gbId = gbId

        self._cacheRemoteCall(_req.uuid, box.cell, 'onCrossTeamApplyList')
        _service.serviceStub.getApplyList(None, _req, None)

    def sendTeamChat(self, teamId, senderGbId, senderName, msgData, senderInfo):
        # 敏感词检查在发送方本服完成，中心只做转发；
        # 上行完整 CHAT_MSG_DATA 与拼 CHAT_CHANNEL_AVATAR_INFO 所需发送者信息（语音消息修复）
        _service = self._getService('sendTeamChat')
        if not _service:
            return

        _req = TeamChatMsgRequest()
        _req.teamId = teamId
        _req.senderGbId = senderGbId
        _req.senderName = senderName
        _req.content = msgData.get('msg', '')
        _req.msgType = msgData.get('msgType', 0)
        _req.voiceUrl = msgData.get('voiceUrl', '')
        _req.code = msgData.get('code', 0)
        _req.senderSchool = senderInfo.get('school', 0)
        _req.senderLevel = senderInfo.get('level', 0)
        _req.senderSex = senderInfo.get('sex', 0)
        _req.senderPicFrameId = senderInfo.get('picFrameId', 0)
        _req.ts = utils.curTS()
        _service.serviceStub.teamChatMsg(None, _req, None)

    def setMicsMode(self, box, teamId, micsMode, captainGbId):
        # 切换语音麦模式（队长操作，队长身份在 Avatar 侧已校验）
        LOG_INFO('CrossTeamStub setMicsMode', teamId, micsMode, captainGbId)
        _service = self._getService('setMicsMode')
        if not _service:
            return

        _req = SetMicsModeRequest()
        _req.uuid = KBEngine.genUUID64()
        _req.teamId = teamId
        _req.micsMode = micsMode
        _req.captainGbId = captainGbId

        self._cacheRemoteCall(_req.uuid, box.cell, 'onCrossTeamOpResult')
        _service.serviceStub.setMicsMode(None, _req, None)

    def blockMic(self, box, teamId, targetGbId, blocked, captainGbId):
        # 禁麦/解除禁麦（队长操作）
        LOG_INFO('CrossTeamStub blockMic', teamId, targetGbId, blocked, captainGbId)
        _service = self._getService('blockMic')
        if not _service:
            return

        _req = BlockMicRequest()
        _req.uuid = KBEngine.genUUID64()
        _req.teamId = teamId
        _req.targetGbId = targetGbId
        _req.blocked = blocked
        _req.captainGbId = captainGbId

        self._cacheRemoteCall(_req.uuid, box.cell, 'onCrossTeamOpResult')
        _service.serviceStub.blockMic(None, _req, None)

    def adjustMemberPos(self, box, teamId, srcGbId, srcGroupIdx, dstGbId, dstGroupIdx, captainGbId):
        # 成员位置调整（队长操作）：交换两个成员位置，或将 src 移动到 dstGroupIdx 组末尾
        LOG_INFO('CrossTeamStub adjustMemberPos', teamId, srcGbId, srcGroupIdx, dstGbId, dstGroupIdx, captainGbId)
        _service = self._getService('adjustMemberPos')
        if not _service:
            return

        _req = AdjustMemberPosRequest()
        _req.uuid = KBEngine.genUUID64()
        _req.teamId = teamId
        _req.captainGbId = captainGbId
        _req.srcGbId = srcGbId
        _req.srcGroupIdx = srcGroupIdx
        _req.dstGbId = dstGbId
        _req.dstGroupIdx = dstGroupIdx

        self._cacheRemoteCall(_req.uuid, box.cell, 'onCrossTeamOpResult')
        _service.serviceStub.adjustMemberPos(None, _req, None)

    def askAllCrossTeamMemberFollow(self, box, teamId, captainGbId, spaceNo, position):
        # 召集上行（本服 sendAllMemberFollowAsk 对应，队长操作；跟随本体由客户端实现，
        # 服务端仅转发）：中心复核队长后 followAskPush 广播队长当前所在服（全队除队长）；
        # 对齐本服静默语义：不走 uuid 回执，校验失败仅中心日志
        LOG_INFO('CrossTeamStub askAllCrossTeamMemberFollow', teamId, captainGbId, spaceNo)
        _service = self._getService('followAsk')
        if not _service:
            return

        _req = FollowAskRequest()
        _req.teamId = teamId
        _req.captainGbId = captainGbId
        _req.spaceNo = spaceNo
        _req.posX, _req.posY, _req.posZ = position

        _service.serviceStub.followAsk(None, _req, None)

    # ------------------------------------------------------------------
    # 讨伐
    # ------------------------------------------------------------------

    def startCrusade(self, box, teamId, gbId):
        LOG_INFO('CrossTeamStub startCrusade', teamId, gbId)
        _service = self._getService('startCrusade')
        if not _service:
            return

        _req = StartCrusadeRequest()
        _req.uuid = KBEngine.genUUID64()
        _req.teamId = teamId
        _req.gbId = gbId

        self._cacheRemoteCall(_req.uuid, box.cell, 'onCrossTeamOpResult')
        _service.serviceStub.startCrusade(None, _req, None)

    def crusadeCheckResult(self, teamId, gbId, reasonCode):
        # 本服成员条件检查结果回报中心（成员 Avatar 检查链路终点）
        _service = self._getService('crusadeCheckResult')
        if not _service:
            return

        _req = CrusadeCheckResultRequest()
        _req.teamId = teamId
        _req.gbId = gbId
        _req.ok = (reasonCode == gameconst.TeamDunCheckCondErrno.UNKNOWN)
        _req.reason = str(reasonCode)
        _service.serviceStub.crusadeCheckResult(None, _req, None)

    def onCrusadeCheck(self, reply):
        # 中心下发条件检查：对本服成员逐个走 Avatar 检查链路（次数/门票在 base，战斗/传送在 cell）
        LOG_INFO('CrossTeamStub onCrusadeCheck', reply.teamId, reply.dungeonNo, list(reply.gbIds))
        self.crusadeDungeonCache[reply.teamId] = reply.dungeonNo

        _gbIds = [gbid for gbid in reply.gbIds]
        if _gbIds:
            gameengine.getGlobalBase('PlayerStub').doOnOthersBase(
                _gbIds, 'checkCrossCrusadeCondition',
                (reply.teamId, reply.dungeonNo,),
                None, '', ()
            )

    def onCrusadeGo(self, reply):
        # 全员检查通过、副本空间就绪：组装 CrossCrusadeContext，本服成员逐个跨服迁移
        # （Stub 不维护队伍缓存，maxNum/全体成员由中心随推送下发）
        LOG_INFO('CrossTeamStub onCrusadeGo', reply.teamId, reply.crossServerId, reply.spaceUUID)
        _serverId = gameconfig.serverId()
        _dungeonNo = self.crusadeDungeonCache.pop(reply.teamId, 0)
        _context = {
            'crossTeamId': reply.teamId,
            'dungeonNo': _dungeonNo,
            'dunLevel': 0,  # TODO(阶段6)：难度读配表
            'spaceUUID': reply.spaceUUID,
            'crossServerId': reply.crossServerId,
            'maxNum': reply.maxNum,
            'members': [
                {'gbId': _m.gbId, 'serverId': _m.serverId}
                for _m in reply.members
            ],
        }

        if reply.crossServerId == _serverId:
            # 本服链路（第三步）：副本空间建在本服（dunServer=本服），成员不跨服迁移，
            # 逐本服成员驱动 cell 本地进本（onCrossCrusadeGoLocal，走本服传送链）
            _cache = self.crusadeSpaceCache.get(reply.teamId)
            if not _cache or not _cache.get('spaceNo'):
                LOG_ERR('onCrusadeGo local mode no space', reply.teamId)
                return
            _context['spaceNo'] = _cache['spaceNo']
            for _m in reply.members:
                if _m.serverId != _serverId:
                    continue
                gameengine.getGlobalBase('PlayerStub').doOnOthersCell(
                    [_m.gbId], 'onCrossCrusadeGoLocal', (_context,), None, '', ())
            return

        for _m in reply.members:
            if _m.serverId != _serverId:
                continue
            gameengine.getGlobalBase('PlayerStub').doOnOthersBase([_m.gbId], 'crossCrusadeGo', (_context,), None, '', ())

    def onCrusadeAbort(self, reply):
        # 讨伐中止：通知本服成员（文案 message id 留阶段 6，先下发原因码）
        LOG_INFO('CrossTeamStub onCrusadeAbort', reply.teamId, reply.reason)
        self.crusadeDungeonCache.pop(reply.teamId, None)
        self.crusadeSpaceCache.pop(reply.teamId, None)
        _gbIds = list(reply.receiverGbIds)
        if _gbIds:
            gameengine.getGlobalBase('PlayerStub').doOnOthersClient(
                _gbIds, 'onCrossCrusadeAbort', (reply.reason,), None, '', ()
            )

    # ------------------------------------------------------------------
    # 讨伐副本（中心经本 Stub 中转建空间；跨服模式在跨服服调用，本服模式在本服调用）：
    # 副本空间由对应 dungeonNo 的 CrossTeamDungeonStub 管理（跨服队伍归属走 SpaceVal.crossTeamId；
    # 空间 dungeonPlayMode 跨服服落 CROSS_CRUSADE/CROSS_CHIEF，本服落 CRUSADE/CHIEF），
    # 本 Stub 只保留 teamId->空间 簿记（crusadeSpaceCache）与中心回报。
    # ------------------------------------------------------------------

    def onCreateCrusadeSpace(self, reply):
        # 中心经本 Stub 中转创建副本空间：按 gamePlay 表进入类型决定 team/raid 线与玩法枚举，
        # 然后转发对应 dungeonNo 的副本 stub 走通用创建链路
        _teamId = reply.teamId
        _dungeonNo = reply.dungeonNo
        LOG_INFO('CrossTeamStub onCreateCrusadeSpace', _teamId, _dungeonNo)

        _dVal = DDI.datas.get(_dungeonNo)
        if not _dVal:
            LOG_ERR('onCreateCrusadeSpace invalid dungeonNo', _dungeonNo)
            self._reportCrusadeSpaceReady(_teamId, 0, False)
            return

        _isRaid = gameconst.DungeonTypeJudge.isRaidDungeon(
            _dVal.get('type', 0),
            _dVal.get('enterType', 0)
        )
        # playMode 按本机身份落枚举（问题记录#6/#7，D3-2 修订）：
        # - 本机跨服服：跨服 playMode（CROSS_CRUSADE/CROSS_CHIEF），结算/退出走跨服链路；
        # - 本机本服（本服模式，dunServer=本服）：直接落本服 playMode（CRUSADE/CHIEF），
        #   结算/完成自动退出/客户端结算面板全量复用本服旧链路；
        #   跨服队伍归属改由 SpaceVal.crossTeamId 判定（isCrossDungeon 不再依赖 playMode）
        if gameconfig.isCrossServer():
            if _isRaid:
                _playMode = dungeonPlayMode.CrossChiefDungeonPlayMode(teamUUID=_teamId)
            else:
                _playMode = dungeonPlayMode.CrossCrusadeDungeonPlayMode(teamUUID=_teamId)
        else:
            if _isRaid:
                _playMode = dungeonPlayMode.ChiefDungeonPlayMode(raidUUID=_teamId)
            else:
                _playMode = dungeonPlayMode.CrusadeDungeonPlayMode(teamUUID=_teamId)

        self.crusadeSpaceCache[_teamId] = {
            'dungeonNo': _dungeonNo,
            'spaceNo': 0,
            'spaceUUID': 0,
            'isRaid': _isRaid,
        }

        _extra = {
            'dungeonPlayMode': _playMode,
            'crossTeamId': _teamId,
            # 空间等级/最高等级先按 0 处理（配表接入后按队伍等级与配表计算）
            'spaceLevel': 0,
            'maxLevel': 0,
        }
        _enterType = gameconst.DungeonEnterTypeEnum.RAID if _isRaid else gameconst.DungeonEnterTypeEnum.TEAM
        _dungeonStub = gameengine.getDungeonStubByDungeonNo(_dungeonNo, _enterType)
        if not _dungeonStub:
            # 跨服服上对应 dungeonNo 的副本 stub 未就位（启动未完成/配表缺失），回报中心失败
            LOG_ERR('onCreateCrusadeSpace no dungeon stub', _dungeonNo, _enterType)
            self.crusadeSpaceCache.pop(_teamId, None)
            self._reportCrusadeSpaceReady(_teamId, 0, False)
            return
        _dungeonStub.applyCreateDungeon(
            None,
            0,
            _teamId,
            _extra
        )

    def onCrossCrusadeSpaceReady(self, teamId, spaceNo, spaceUUID, ok, spaceBox, spaceMgrBox):
        # 副本 stub 建空间结果回报：就绪则更新簿记并上报中心；失败清簿记
        # （spaceBox/spaceMgrBox 随簿记保存，镜像登录直进副本建 cell 用）
        LOG_INFO('CrossTeamStub onCrossCrusadeSpaceReady', teamId, spaceNo, ok)
        if not ok:
            self.crusadeSpaceCache.pop(teamId, None)
            self._reportCrusadeSpaceReady(teamId, 0, False)
            return

        _cache = self.crusadeSpaceCache.get(teamId)
        if not _cache:
            LOG_ERR('onCrossCrusadeSpaceReady no cache', teamId, spaceNo)
            return

        _cache['spaceNo'] = spaceNo
        _cache['spaceUUID'] = spaceUUID
        _cache['spaceBox'] = spaceBox
        _cache['spaceMgrBox'] = spaceMgrBox
        self._reportCrusadeSpaceReady(teamId, spaceUUID, True)

    def logonEnterCrusadeDungeon(self, box, gbId, context):
        # 跨服讨伐镜像登录直进副本：查簿记把空间实体盒交给镜像 base 直接建 cell；
        # 簿记缺失（空间已销毁/已结算）时回退出生图分线落地收容镜像
        _teamId = context.get('crossTeamId', 0)
        LOG_INFO('CrossTeamStub logonEnterCrusadeDungeon', _teamId, gbId)
        _cache = self.crusadeSpaceCache.get(_teamId)
        if not _cache or not _cache.get('spaceNo') or not _cache.get('spaceBox'):
            LOG_ERR('logonEnterCrusadeDungeon no space', _teamId, gbId)
            box.onCrossCrusadeLogonEnterFail()
            return

        box.enterCrusadeDungeonOnLogon(
            _cache['spaceBox'],
            _cache['spaceMgrBox'],
            _cache['spaceNo'],
            context
        )

    def enterCrusadeSpace(self, box, teamId, gbId, context):
        # 跨服 Avatar 落地且队伍校验通过后进入副本空间
        LOG_INFO('CrossTeamStub enterCrusadeSpace', teamId, gbId)
        _cache = self.crusadeSpaceCache.get(teamId)
        if not _cache or not _cache.get('spaceNo'):
            LOG_ERR('enterCrusadeSpace no space', teamId, gbId)
            return

        _dungeonNo = _cache['dungeonNo']
        _spaceNo = _cache['spaceNo']

        # 镜像 cell 标记跨服队伍并构造 AOI 队友缓存（副本内退出/掉线语义用）
        if box.cell:
            box.cell.onCrossTeamIdChange(teamId)
            box.cell.onCrossCrusadeSpaceEnter(context)

        _extra = {
            'dungeonNo': _dungeonNo,
            'teamUUID': teamId,
            'spaceUUID': _cache['spaceUUID'],
            'gbId': gbId,
            # 跨服标记：副本 stub 进本失败/进入成功分支识别用
            'crossTeamId': teamId,
            # 本服进本链路的必需字段（cell/impTeamDungeon.doEnterTeamDungeon）：
            # 进本资格名单与跳过门票道具检查（条件已在讨伐发起时由中心协调检查过）
            'teamEnterCheckDic': {gbId: 1},
            'skipUseNeedItem': True,
        }
        _enterType = gameconst.DungeonEnterTypeEnum.RAID if _cache.get('isRaid') else gameconst.DungeonEnterTypeEnum.TEAM
        _dungeonStub = gameengine.getDungeonStubByDungeonNo(_dungeonNo, _enterType)
        if not _dungeonStub:
            LOG_ERR('enterCrusadeSpace no dungeon stub', _dungeonNo, teamId, gbId)
            return
        _dungeonStub.doEnterDungeon(
            box,
            gbId,
            teamId,
            _spaceNo,
            _extra
        )

    def _reportCrusadeSpaceReady(self, teamId, spaceUUID, ok):
        _service = self._getService('crusadeSpaceReady')
        if not _service:
            return

        _req = CrusadeSpaceReadyRequest()
        _req.teamId = teamId
        _req.spaceUUID = str(spaceUUID)
        _req.ok = ok
        _service.serviceStub.crusadeSpaceReady(None, _req, None)

    def crusadeFinished(self, teamId, result):
        # 副本完成（跨服讨伐副本 stub 在完成回调中调用）：清空间缓存并通知中心复位 InDungeon
        LOG_INFO('CrossTeamStub crusadeFinished', teamId, result)
        self.crusadeSpaceCache.pop(teamId, None)
        self.crusadeDungeonCache.pop(teamId, None)

        _service = self._getService('crusadeFinished')
        if not _service:
            return

        _req = CrusadeFinishedRequest()
        _req.teamId = teamId
        _req.result = result
        _service.serviceStub.crusadeFinished(None, _req, None)

    def onDungeonCDRefreshPush(self, reply):
        # 重进 CD 刷新（中心 crusadeFinished 写入后全推）：value 为 CD 截止时刻，
        # 语义同本服 onRefreshLastDungeonFinishedTime（完成时刻 + raid_rejoinCdTime）
        LOG_INFO('CrossTeamStub onDungeonCDRefreshPush', reply.teamId, reply.lastDungeonFinishedTime)
        _receivers = list(reply.receiverGbIds)
        if _receivers:
            gameengine.getGlobalBase('PlayerStub').doOnOthersCell(
                _receivers,
                'onCrossTeamRefreshDungeonCD',
                (reply.lastDungeonFinishedTime,),
                None,
                '',
                ()
            )

    # ------------------------------------------------------------------
    # 成员状态聚合上报（3s 定时）
    # ------------------------------------------------------------------

    def reportMemberStates(self):
        if not self.stateReportCache:
            return

        _service = self._getService('reportMemberStates')
        if not _service:
            return

        _serverId = gameconfig.serverId()
        _teamStates = {}
        for _gbId, _state in self.stateReportCache.items():
            _teamId = _state.get('teamId', 0)
            if _teamId == 0:
                continue
            _teamStates.setdefault(_teamId, []).append((_gbId, _state))

        for _teamId, _members in _teamStates.items():
            _req = ReportMemberStateRequest()
            _req.teamId = _teamId
            _req.serverId = _serverId
            _req.reportTS = utils.curTS()
            for _gbId, _state in _members:
                _memberState = _req.members.add()
                _memberState.gbId = _gbId
                _memberState.hp = _state.get('hp', 0)
                _memberState.maxHp = _state.get('maxHp', 0)
                _memberState.level = _state.get('level', 0)
                _memberState.score = _state.get('score', 0)
                _memberState.spaceNo = _state.get('spaceNo', 0)
                _position = _state.get('position', (0, 0, 0))
                _memberState.posX = _position[0]
                _memberState.posY = _position[1]
                _memberState.posZ = _position[2]

            _service.serviceStub.reportMemberState(None, _req, None)

    # ------------------------------------------------------------------
    # 下行：中心 -> Stub -> 本服成员
    # ------------------------------------------------------------------

    def onTeamOpResult(self, reply):
        # 队伍操作结果：uuid 非 0 为请求回执（必须由发起请求的 Avatar 所在 stub 持有 uuid 缓存，
        # 原路回调）；uuid=0 为中心主动推送（撮合入队作废/队长申请结果等异步事件），按 gbId 路由
        if reply.uuid:
            _cache = self.remoteCallCache.pop(reply.uuid, None)
            if _cache is None:
                LOG_ERR('CrossTeamStub onTeamOpResult no cache', reply.uuid, reply.teamId, reply.gbId)
                return

            _box = _cache['box']
            _method = _cache['method']
            getattr(_box, _method)(reply.resultCode, reply.teamId, reply.gbId, reply.target)
            return

        LOG_INFO('CrossTeamStub onTeamOpResult push', reply.teamId, reply.gbId, reply.resultCode, reply.target)
        gameengine.getGlobalBase('PlayerStub').doOnOthersCell(
            [reply.gbId],
            'onCrossTeamOpResult',
            (reply.resultCode, reply.teamId, reply.gbId, reply.target),
            None,
            '',
            ()
        )

    def onReplyApplyNotify(self, reply):
        # 入队申请结果主动通知：纯转发直发申请人客户端（doOnOthersClient，不绕 cell），
        # 携带目标/门槛/密码/申请来源，供客户端失败交互
        LOG_INFO('CrossTeamStub onReplyApplyNotify', reply.teamId, reply.applicantGbId, reply.resultCode)
        gameengine.getGlobalBase('PlayerStub').doOnOthersClient(
            [reply.applicantGbId],
            'onCrossTeamApplyJoinResult',
            (
                reply.resultCode,
                reply.teamId,
                reply.target,
                reply.requireLevel,
                reply.requireScore,
                reply.password,
                reply.applySource,
            ),
            None, '', ()
        )

    def onBecomeCaptainApplyPush(self, reply):
        # 申请成为队长提示：转发队长客户端（申请人基本身份信息，对齐本服 onApplyBecomeCaptainMsg）
        LOG_INFO('CrossTeamStub onBecomeCaptainApplyPush', reply.teamId, reply.applicant.gbId)
        _receivers = list(reply.receiverGbIds)
        if _receivers:
            _applicant = reply.applicant
            gameengine.getGlobalBase('PlayerStub').doOnOthersClient(
                _receivers, 'onCrossBecomeCaptainAsk',
                ({
                    'gbId': _applicant.gbId,
                    'serverId': _applicant.serverId,
                    'playerName': _applicant.name,
                    'sex': _applicant.sex,
                    'school': _applicant.school,
                    'score': _applicant.score,
                    # CROSS_TEAM_BASIC_INFO_VAL 补 level（问题记录#4 结构对齐）
                    'level': _applicant.level,
                },),
                None, '', ()
            )

    # 创建队伍成功：分发到 onCrossTeamCreateSuccess（仅创建人本人，中心经 receiverGbIds 指定）
    def onTeamCreateSuccessPush(self, reply):
        LOG_DBG('onTeamCreateSuccessPush', reply.team.teamId, len(reply.team.members))
        _gbIds = list(reply.receiverGbIds)
        if _gbIds:
            gameengine.getGlobalBase('PlayerStub').doOnOthersCell(
                _gbIds, 'onCrossTeamCreateSuccess',
                (crossTeam.teamInfoPbToStreamDict(reply.team),),
                None, '', ()
            )

    # 新成员加入成功：分发到 onCrossTeamJoinSuccess（仅新成员本人，中心经 receiverGbIds 指定）
    def onTeamJoinSuccessPush(self, reply):
        LOG_DBG('onTeamJoinSuccessPush', reply.team.teamId, len(reply.team.members))
        _gbIds = list(reply.receiverGbIds)
        if _gbIds:
            gameengine.getGlobalBase('PlayerStub').doOnOthersCell(
                _gbIds, 'onCrossTeamJoinSuccess',
                (crossTeam.teamInfoPbToStreamDict(reply.team),),
                None, '', ()
            )

    def onMemberJoinPush(self, reply):
        # 进队：新成员本人由 teamJoinSuccessPush 全量覆盖，其余本服成员收"新增成员"增量
        _gbId = reply.member.gbId if reply.HasField('member') else 0
        LOG_INFO('CrossTeamStub onMemberJoinPush', reply.teamId, _gbId)
        _receivers = list(reply.receiverGbIds)
        _localGbIds = [gbid for gbid in _receivers if gbid != _gbId]
        if _localGbIds:
            gameengine.getGlobalBase('PlayerStub').doOnOthersCell(
                _localGbIds, 'onCrossTeamMemberAdd',
                (crossTeam.memberInfoPbToStreamDict(reply.member),),
                None, '', ()
            )

    def onMemberLeavePush(self, reply):
        # 离队/被踢/离线退出：被移出者走 onCrossTeamLeave（附带原因），其余本服成员收"移除成员"增量
        _gbId = reply.gbId
        _reason = reply.reason
        # proto reason: 1=主动离队, 2=被踢, 3=离线; 客户端历史 changeType: 2=离队, 3=被踢, 6=离线
        _changeType = {1: 2, 2: 3, 3: 6}.get(_reason, _reason)
        LOG_INFO('CrossTeamStub onMemberLeavePush', reply.teamId, _gbId, _changeType)
        _receivers = list(reply.receiverGbIds)
        self.stateReportCache.pop(_gbId, None)
        gameengine.getGlobalBase('PlayerStub').doOnOthersCell(
            [_gbId], 'onCrossTeamLeave',
            (reply.teamId, _changeType,),
            None, '', ()
        )
        _localGbIds = [gbid for gbid in _receivers if gbid != _gbId]
        if _localGbIds:
            gameengine.getGlobalBase('PlayerStub').doOnOthersCell(
                _localGbIds, 'onCrossTeamMemberRemove',
                (_gbId, _changeType,),
                None, '', ()
            )

    def onCaptainChangePush(self, reply):
        LOG_INFO('CrossTeamStub onCaptainChangePush', reply.teamId, reply.newCaptainGbId)
        _receivers = list(reply.receiverGbIds)
        if _receivers:
            gameengine.getGlobalBase('PlayerStub').doOnOthersCell(
                _receivers, 'onCrossTeamCaptainChange',
                (reply.newCaptainGbId,),
                None, '', ()
            )

    def onDeputyChangePush(self, reply):
        # 副团长变更推送（任命/取消，全队；deputyGbId=0 表示取消）：
        # 转发成员 cell 落地缓存并透传客户端 onCrossTeamDeputyChange
        LOG_INFO('CrossTeamStub onDeputyChangePush', reply.teamId, reply.deputyGbId)
        _receivers = list(reply.receiverGbIds)
        if _receivers:
            gameengine.getGlobalBase('PlayerStub').doOnOthersCell(
                _receivers, 'onCrossTeamDeputyChange',
                (reply.deputyGbId,),
                None, '', ()
            )

    def onMarkChangePush(self, reply):
        # 队伍标记变更推送（单条增量，中心只发队长当前所在服）：
        # 转发本服成员 cell 落地镜像并透传客户端 onCrossTeamMarkChange；
        # markDict 键名对齐 CLIENT_TEAM_MARK_VAL（DELETE 时仅 type/index 有效，CAPTAIN 时为空表）
        LOG_INFO('CrossTeamStub onMarkChangePush', reply.teamId, reply.changeType)
        _receivers = list(reply.receiverGbIds)
        if not _receivers:
            return

        _markDict = crossTeam.markInfoPbToStreamDict(reply.mark) if reply.HasField('mark') else {}
        gameengine.getGlobalBase('PlayerStub').doOnOthersCell(
            _receivers, 'onCrossTeamMarkChange',
            (reply.changeType, _markDict, reply.onlyCaptainCanMark, min(*_receivers)),
            None, '', ()
        )

    def onFollowAskPush(self, reply):
        # 召集推送（本服 onFollowTeamCaptainAsk 对应，中心只发队长当前所在服，
        # receiverGbIds 不含队长）：转发本服成员 cell 透传客户端
        # onCrossTeamFollowCaptainAsk（跟随本体由客户端实现）
        LOG_INFO('CrossTeamStub onFollowAskPush', reply.teamId, len(reply.receiverGbIds))
        _receivers = list(reply.receiverGbIds)
        if _receivers:
            gameengine.getGlobalBase('PlayerStub').doOnOthersCell(
                _receivers, 'onCrossTeamFollowCaptainAsk',
                (reply.spaceNo, (reply.posX, reply.posY, reply.posZ)),
                None, '', ()
            )

    def onTeamDisbandPush(self, reply):
        LOG_INFO('CrossTeamStub onTeamDisbandPush', reply.teamId)
        _receivers = list(reply.receiverGbIds)
        for _g in _receivers:
            self.stateReportCache.pop(_g, None)
        if _receivers:
            gameengine.getGlobalBase('PlayerStub').doOnOthersCell(
                _receivers,
                'onCrossTeamDisband',
                (reply.teamId,),
                None, '', ()
            )

    def onTeamSettingsChangePush(self, reply):
        LOG_INFO('CrossTeamStub onTeamSettingsChangePush', reply.teamId, reply.autoEnter)
        _receivers = list(reply.receiverGbIds)
        if _receivers:
            gameengine.getGlobalBase('PlayerStub').doOnOthersCell(
                _receivers, 'onCrossTeamSettingsChange',
                ({
                    'minLevel': reply.minLevel,
                    'minScore': reply.minScore,
                    'intro': reply.intro,
                    'autoEnter': reply.autoEnter,
                    'password': reply.password,
                },),
                None, '', ()
            )

    def onTeamAutoMatchChangePush(self, reply):
        LOG_INFO('CrossTeamStub onTeamAutoMatchChangePush', reply.teamId, reply.autoMatch)
        _receivers = list(reply.receiverGbIds)
        if _receivers:
            gameengine.getGlobalBase('PlayerStub').doOnOthersCell(
                _receivers, 'onCrossTeamAutoMatchChange',
                (reply.autoMatch,),
                None, '', ()
            )

    def onTeamMicsModeChangePush(self, reply):
        LOG_INFO('CrossTeamStub onTeamMicsModeChangePush', reply.teamId, reply.micsMode)
        _receivers = list(reply.receiverGbIds)
        if _receivers:
            gameengine.getGlobalBase('PlayerStub').doOnOthersCell(
                _receivers, 'onCrossTeamMicsModeChange',
                (reply.micsMode,),
                None, '', ()
            )

    def onMemberMicBlockPush(self, reply):
        LOG_INFO('CrossTeamStub onMemberMicBlockPush', reply.teamId, reply.gbId, reply.blocked)
        _receivers = list(reply.receiverGbIds)
        if _receivers:
            gameengine.getGlobalBase('PlayerStub').doOnOthersCell(
                _receivers, 'onCrossTeamMicBlockChange',
                (reply.gbId, reply.blocked,),
                None, '', ()
            )

    def onAdjustMemberPosPush(self, reply):
        # 位置调整推送：转发到相关成员 cell，由 cell 通知客户端刷新全量
        LOG_INFO('CrossTeamStub onAdjustMemberPosPush', reply.teamId, reply.srcGbId, reply.srcGroupIdx, reply.dstGbId, reply.dstGroupIdx)
        _receivers = list(reply.receiverGbIds)
        if not _receivers:
            return

        gameengine.getGlobalBase('PlayerStub').doOnOthersCell(
            _receivers,
            'onCrossTeamMemberPosChange',
            (reply.srcGbId, reply.srcGroupIdx, reply.dstGbId, reply.dstGroupIdx),
            None, '', ()
        )

    def onTeamChatBatch(self, reply):
        _gbIds = list(reply.receiverGbIds)
        if not _gbIds:
            return

        # 完整聊天内容（msgType/voiceUrl/code）与拼 avatarInfo 所需发送者信息
        # （CROSS_TEAM_CHAT_MSG_VAL，base 侧据此走本服队伍频道链路下发）
        _msgList = []
        for _msg in reply.msgs:
            _msgList.append({
                'senderGbId': _msg.senderGbId,
                'senderName': _msg.senderName,
                'content': _msg.content,
                'ts': _msg.ts,
                'senderSchool': _msg.senderSchool,
                'senderLevel': _msg.senderLevel,
                'senderSex': _msg.senderSex,
                'senderPicFrameId': _msg.senderPicFrameId,
                'msgType': _msg.msgType,
                'voiceUrl': _msg.voiceUrl,
                'code': _msg.code,
            })

        gameengine.getGlobalBase('PlayerStub').doOnOthersBase(
            _gbIds,
            'onCrossTeamChatBatch',
            (_msgList,),
            None,
            '',
            ()
        )

    def onAdjustMemberPosPush(self, reply):
        # 位置调整推送：转发到相关成员 cell，由 cell 通知客户端刷新全量
        LOG_INFO('CrossTeamStub onAdjustMemberPosPush', reply.teamId, reply.srcGbId, reply.srcGroupIdx, reply.dstGbId, reply.dstGroupIdx)
        _receivers = list(reply.receiverGbIds)
        if not _receivers:
            return

        gameengine.getGlobalBase('PlayerStub').doOnOthersCell(
            _receivers,
            'onCrossTeamMemberPosChange',
            (reply.srcGbId, reply.srcGroupIdx, reply.dstGbId, reply.dstGroupIdx),
            None, '', ()
        )

    def onBroadcastMemberState(self, reply):
        # 状态快照直接广播到客户端，省去 cell 中转（Stub 不维护队伍缓存，无回写）
        _stateDicts = []
        for _state in reply.members:
            _stateDicts.append({
                'gbId': _state.gbId,
                'hp': _state.hp,
                'maxHp': _state.maxHp,
                'level': _state.level,
                'score': _state.score,
                'spaceNo': _state.spaceNo,
                'position': (_state.posX, _state.posY, _state.posZ),
                'routeServerId': _state.routeServerId,
            })

        _gbIds = list(reply.receiverGbIds)
        if _gbIds:
            gameengine.getGlobalBase('PlayerStub').doOnOthersClient(
                _gbIds, 'onCrossTeamMemberState', (reply.teamId, _stateDicts,), None, '', ()
            )

    def onMatchSuccess(self, reply):
        # 两段式入队第一段：转发到 Avatar cell 做二次检查（是否仍在匹配/是否已入队等），
        # cell 检查通过后再回调本 Stub.doMatchJoin 向中心发 MatchJoin。
        _gbId = reply.gbId
        LOG_INFO('CrossTeamStub onMatchSuccess', reply.teamId, _gbId)
        gameengine.getGlobalBase('PlayerStub').doOnOthersCell(
            [_gbId],
            'onCrossTeamMatchSuccess',
            (reply.teamId, reply.target),
            None, '', ()
        )

    def doMatchJoin(self, teamId, target, memberInfo):
        # Avatar cell 二次检查通过后回调：向中心发 MatchJoin 完成两段式入队第二段
        _gbId = memberInfo.get('gbId', 0)
        LOG_INFO('CrossTeamStub doMatchJoin', teamId, target, _gbId)

        _service = self._getService('doMatchJoin')
        if not _service:
            return

        _req = MatchJoinRequest()
        _req.uuid = KBEngine.genUUID64()
        _req.teamId = teamId
        _req.target = target
        _req.member.gbId = _gbId
        _req.member.serverId = gameconfig.serverId()
        _req.member.name = memberInfo.get('playerName', '')
        _req.member.level = memberInfo.get('level', 0)
        _req.member.school = memberInfo.get('school', 0)
        _req.member.score = memberInfo.get('score', 0)
        _req.member.sex = memberInfo.get('sex', 0)
        _req.member.picFrameId = memberInfo.get('picFrameId', 0)
        _req.member.openId = memberInfo.get('openId', '')
        _service.serviceStub.matchJoin(None, _req, None)

    def onMatchTimeout(self, reply):
        LOG_INFO('CrossTeamStub onMatchTimeout', reply.gbId, reply.target)
        gameengine.getGlobalBase('PlayerStub').doOnOthersCell(
            [reply.gbId], 'onCrossTeamMatchTimeout',
            (reply.target,),
            None, '', ()
        )

    def onTeamListResult(self, reply):
        _cache = self.remoteCallCache.pop(reply.uuid, None)
        if not _cache:
            LOG_ERR('CrossTeamStub onTeamListResult no cache', reply.uuid)
            return

        _teams = []
        for _team in reply.teams:
            _captain = _team.captain
            _teams.append({
                'teamId': _team.teamId,
                'target': _team.target,
                'minLevel': _team.minLevel,
                'minScore': _team.minScore,
                'memberCnt': _team.memberCnt,
                'maxNum': _team.maxNum,
                'intro': _team.intro,
                'isPublish': _team.isPublish,
                'autoMatchTime': _team.autoMatchTime,
                # 队长预览信息（问题记录#4，键名对齐 CROSS_TEAM_BASIC_INFO_VAL）
                'captain': {
                    'gbId': _captain.gbId,
                    'serverId': _captain.serverId,
                    'playerName': _captain.name,
                    'sex': _captain.sex,
                    'school': _captain.school,
                    'score': _captain.score,
                    'level': _captain.level,
                },
            })

        # 一波全量下发（问题记录#5）：json+gzip 后经请求者 base streamStringProxy 分片推给客户端；
        # 同 target 结果缓存 CROSS_TEAM_LIST_CACHE_SECONDS 秒，命中期查询直接回缓存（getTeamList）
        _zStr = gzip.compress(json.dumps({'target': reply.target, 'teams': _teams}).encode('ascii'))
        self.teamListCache[reply.target] = {'data': _zStr, 'ts': utils.curTS()}
        _cache['box'].streamStringProxy(_zStr, '', gameconst.StreamStringID.CROSS_TEAM_LIST_DATA)

    def onTeamDataResp(self, reply):
        # 客户端主动查询回包：按 uuid 回调缓存的 box/method（无队/查询失败回空 dict）
        _cache = self.remoteCallCache.pop(reply.uuid, None)
        if not _cache:
            LOG_ERR('CrossTeamStub onTeamDataResp no cache', reply.uuid)
            return

        _teamDict = crossTeam.teamInfoPbToStreamDict(reply.team) if reply.success else {}
        _box = _cache['box']
        _method = _cache['method']
        getattr(_box, _method)(_teamDict)

    def onQueryTeamCrossResp(self, reply):
        # teamId 直查回包（队伍预览 onCrossTeamPreview / 跨服进本前校验）：
        # 单播，按 uuid 从 remoteCallCache 取缓存的 box/method 原路回调
        _cache = self.remoteCallCache.pop(reply.uuid, None)
        if not _cache:
            LOG_ERR('CrossTeamStub onQueryTeamCrossResp no cache', reply.uuid)
            return

        _teamDict = crossTeam.teamInfoPbToStreamDict(reply.team) if reply.success else {}
        _box = _cache['box']
        _method = _cache['method']
        _args = _cache.get('args', ())
        getattr(_box, _method)(_teamDict, *_args)

    def onMemberVoiceStatePush(self, reply):
        # 成员语音状态变更（决策 2 独立推送）：组位图转发成员 cell，
        # 位定义与本服对称（user_type/team.py _buildVoiceFlags）：
        # 0x01=inVoiceRoom, 0x02=enableMics, 0x04=enableSpeaker, 0x08=isBlockMics
        LOG_INFO('CrossTeamStub onMemberVoiceStatePush', reply.teamId, reply.gbId)
        _voiceFlags = 0
        if reply.inVoiceRoom:
            _voiceFlags |= 0x01
        if reply.enableMics:
            _voiceFlags |= 0x02
        if reply.enableSpeaker:
            _voiceFlags |= 0x04
        if reply.isBlockMics:
            _voiceFlags |= 0x08

        _receivers = list(reply.receiverGbIds)
        if _receivers:
            gameengine.getGlobalBase('PlayerStub').doOnOthersCell(
                _receivers, 'onCrossTeamMemberVoiceState',
                (reply.gbId, _voiceFlags,),
                None, '', ()
            )

    def onMatchStart(self, reply):
        # 入池成功通知：单播转发（客户端匹配 UI 开始倒计时，enterTS 为入池时间）
        LOG_INFO('CrossTeamStub onMatchStart', reply.gbId, reply.target, reply.enterTS)
        gameengine.getGlobalBase('PlayerStub').doOnOthersCell(
            [reply.gbId], 'onCrossTeamMatchStart',
            (reply.enterTS,),
            None, '', ()
        )

    def onMatchStop(self, reply):
        # 取消匹配确认通知：单播转发（撮合成功/超时分别走 MatchSuccessMsg/MatchTimeoutMsg）
        LOG_INFO('CrossTeamStub onMatchStop', reply.gbId, reply.target)
        gameengine.getGlobalBase('PlayerStub').doOnOthersCell(
            [reply.gbId], 'onCrossTeamMatchStop',
            (),
            None, '', ()
        )

    def onApplyListPush(self, reply):
        # 申请列表应答：按 uuid 回调缓存的 box/method（CROSS_TEAM_APPLY_VAL 列表）
        _cache = self.remoteCallCache.pop(reply.uuid, None)
        if not _cache:
            LOG_ERR('CrossTeamStub onApplyListPush no cache', reply.uuid)
            return

        _applyList = []
        for _app in reply.applicants:
            _m = _app.member
            _applyList.append({
                'teamId': reply.teamId,
                # ApplyInfo 未携带队伍目标（客户端申请列表展示不依赖），置 0
                'target': 0,
                'gbId': _m.gbId,
                'serverId': _m.serverId,
                'playerName': _m.name,
                'school': _m.school,
                'level': _m.level,
                'score': _m.score,
                'sex': _m.sex,
                'applySource': _app.applySource,
            })

        _box = _cache['box']
        _method = _cache['method']
        getattr(_box, _method)(_applyList)

    def onApplyRemoveNotify(self, reply):
        # 申请移除通知：转发队长（副团长功能期扩展），客户端从申请列表移除
        LOG_INFO('CrossTeamStub onApplyRemoveNotify', reply.teamId, reply.applicantGbId)
        _receivers = list(reply.receiverGbIds)
        if _receivers:
            gameengine.getGlobalBase('PlayerStub').doOnOthersCell(
                _receivers, 'onCrossTeamApplyRemove',
                (reply.applicantGbId,),
                None, '', ()
            )

    def onJoinApplyNotify(self, reply):
        LOG_DBG('onJoinApplyNotify:', reply)
        # 入队申请提示：转发队长
        _applicant = reply.applicant
        gameengine.getGlobalBase('PlayerStub').doOnOthersClient(
            [reply.captainGbId], 'onCrossTeamJoinApply',
            ({
                'teamId': reply.teamId,
                'target': reply.target,
                'gbId': _applicant.gbId,
                'serverId':_applicant.serverId,
                'playerName':_applicant.name,
                'school': _applicant.school,
                'level': _applicant.level,
                'score': _applicant.score,
                # 客户端接口对齐补充（1.5）：性别与申请来源
                'sex': _applicant.sex,
                'applySource': reply.applySource,
            },),
            None, '', ()
        )

    def onInviteNotify(self, reply):
        # 组队邀请：转发被邀请人
        _inviter = reply.inviter
        gameengine.getGlobalBase('PlayerStub').doOnOthersClient(
            [reply.inviteeGbId], 'onCrossTeamInvite',
            ({
                'teamId': reply.teamId,
                'target': reply.target,
                'gbId': _inviter.gbId,
                'serverId': _inviter.serverId,
                'playerName': _inviter.name,
                'school': _inviter.school,
                'level': _inviter.level,
                'score': _inviter.score,
                # 客户端接口对齐补充（1.5）：邀请类型与性别
                'inviteType': reply.inviteType,
                'sex': _inviter.sex,
            },),
            None, '', ()
        )
