# coding: utf-8
from rpc import RpcChannel

import KBEngine
from KBEDebug import *
import utils
import iGlobal
import iBaseNoCell
import iTimer
import gametimer
import gameconfig
import gameengine
import iCentralStub
import gameconst

from proto.gameServerAlliance_pb2 import GameClient, \
    AllianceService_Stub, \
    RegisterGameServerRequest, \
    Void, \
    CreateLeagueRequest, DisbandLeagueRequest, ModifyLeagueInfoRequest, \
    GetLeagueListRequest, SearchLeagueRequest, GetLeagueDetailRequest, \
    GetLeagueBasicInfoRequest, \
    GetLeagueSimpleInfoRequest, LeagueSimpleInfo, LeagueSimpleMember, \
    ApplyToJoinRequest, ApproveJoinRequest, RejectJoinRequest, CancelApplyRequest, \
    CheckGuildExistsResult, \
    InviteGuildRequest, AcceptInviteRequest, RejectInviteRequest, AllianceInviteInfo, \
    KickMemberRequest, LeaveLeagueRequest, TransferLeaderRequest, \
    GetApplyListRequest, GetInviteListRequest, GetSentAppliesRequest, \
    DeclareWarRequest, GetEnemyListRequest, GetUnionListRequest, \
    GetEnemyAllianceListRequest, EnemyRowInfo, \
    CheckLeagueRelationRequest, GetGuildAllianceRequest, \
    DonateFundRequest, AidResourceRequest, GetLeagueFundRequest, \
    GetEventListRequest, SendChatMessageRequest, GetChatHistoryRequest, \
    ReportGuildScoreRequest, SyncGuildInfoRequest, CheckLeaveGuildRequest, QueryLeagueUUIDRequest,\
    GuildSimpleInfo, GetGuildSimpleInfoRequest, GetGuildSimpleInfoResult, RecruitLeagueMemberRequest


class AllianceService(GameClient):
    def __init__(self, mgr, address, centralServerId):
        super().__init__()
        self.mgr = mgr
        self.centralServerId = centralServerId
        self.channel = RpcChannel.RpcChannel(self)
        self.asStub = AllianceService_Stub(self.channel)

        self.channel.connect(address)

    def on_disconnected(self):
        self.mgr.onAllianceServiceDisconnected(self.centralServerId)

    def on_connected(self):
        self.mgr.onAllianceServiceConnected(self.centralServerId)

    def activeTickCallback(self, rpc_controller, reply, done):
        pass

    # ---- Core Callbacks ----
    def onCreateLeagueResult(self, rpc_controller, reply, done):
        self.mgr.onCreateLeagueResult(reply)

    def onDisbandLeagueResult(self, rpc_controller, reply, done):
        self.mgr.onDisbandLeagueResult(reply)

    def onModifyLeagueInfoResult(self, rpc_controller, reply, done):
        self.mgr.onModifyLeagueInfoResult(reply)

    def onLeagueListResult(self, rpc_controller, reply, done):
        self.mgr.onLeagueListResult(reply)

    def onSearchLeagueResult(self, rpc_controller, reply, done):
        self.mgr.onSearchLeagueResult(reply)

    def onLeagueDetailResult(self, rpc_controller, reply, done):
        self.mgr.onLeagueDetailResult(reply)

    def onGetLeagueBasicInfoResult(self, rpc_controller, reply, done):
        self.mgr.onGetLeagueBasicInfoResult(reply)

    def onGetLeagueSimpleInfoResult(self, rpc_controller, reply, done):
        self.mgr.onGetLeagueSimpleInfoResult(reply)

    # ---- Member Callbacks ----
    def onApplyLeagueToJoinResult(self, rpc_controller, reply, done):
        self.mgr.onApplyLeagueToJoinResult(reply)

    def onApproveJoinResult(self, rpc_controller, reply, done):
        self.mgr.onApproveJoinResult(reply)

    def checkGuildExists(self, rpc_controller, request, done):
        self.mgr.checkGuildExists(request)

    def onRejectJoinResult(self, rpc_controller, reply, done):
        self.mgr.onRejectJoinResult(reply)

    def onInviteGuildResult(self, rpc_controller, reply, done):
        self.mgr.onInviteGuildResult(reply)

    def onAcceptInviteResult(self, rpc_controller, reply, done):
        self.mgr.onAcceptInviteResult(reply)

    def onRejectInviteResult(self, rpc_controller, reply, done):
        self.mgr.onRejectInviteResult(reply)

    def onKickMemberResult(self, rpc_controller, reply, done):
        self.mgr.onKickMemberResult(reply)

    def onLeaveLeagueResult(self, rpc_controller, reply, done):
        self.mgr.onLeaveLeagueResult(reply)

    def onTransferLeaderResult(self, rpc_controller, reply, done):
        self.mgr.onTransferLeaderResult(reply)

    def onApplyListResult(self, rpc_controller, reply, done):
        self.mgr.onApplyListResult(reply)

    def onInviteListResult(self, rpc_controller, reply, done):
        self.mgr.onInviteListResult(reply)

    def onSentAppliesResult(self, rpc_controller, reply, done):
        self.mgr.onSentAppliesResult(reply)

    # ---- Diplomacy Callbacks ----
    def onDeclareWarResult(self, rpc_controller, reply, done):
        self.mgr.onDeclareWarResult(reply)

    def onEnemyListResult(self, rpc_controller, reply, done):
        self.mgr.onEnemyListResult(reply)

    def onEnemyAllianceListResult(self, rpc_controller, reply, done):
        self.mgr.onEnemyAllianceListResult(reply)

    def onUnionListResult(self, rpc_controller, reply, done):
        self.mgr.onUnionListResult(reply)

    def onCheckLeagueRelationResult(self, rpc_controller, reply, done):
        self.mgr.onCheckLeagueRelationResult(reply)

    def onGetGuildAllianceResult(self, rpc_controller, reply, done):
        self.mgr.onGetGuildAllianceResult(reply)

    # ---- Resource Callbacks ----
    def onDonateFundResult(self, rpc_controller, reply, done):
        self.mgr.onDonateFundResult(reply)

    def onAidResourceResult(self, rpc_controller, reply, done):
        self.mgr.onAidResourceResult(reply)

    def onLeagueFundResult(self, rpc_controller, reply, done):
        self.mgr.onLeagueFundResult(reply)

    # ---- Event & Chat Callbacks ----
    def onEventListResult(self, rpc_controller, reply, done):
        self.mgr.onEventListResult(reply)

    def onSendChatMessageResult(self, rpc_controller, reply, done):
        self.mgr.onSendChatMessageResult(reply)

    def onChatHistoryResult(self, rpc_controller, reply, done):
        self.mgr.onChatHistoryResult(reply)

    # ---- Broadcasts ----
    def onWarStarted(self, rpc_controller, reply, done):
        self.mgr.onWarStarted(reply)

    def onWarEnded(self, rpc_controller, reply, done):
        self.mgr.onWarEnded(reply)

    def onNewEvent(self, rpc_controller, reply, done):
        self.mgr.onNewEvent(reply)

    def onChatMessage(self, rpc_controller, reply, done):
        self.mgr.onChatMessage(reply)

    def onDisbandLeagueNotify(self, rpc_controller, reply, done):
        self.mgr.onDisbandLeagueNotify(reply)

    def onNewApplyNotify(self, rpc_controller, reply, done):
        self.mgr.onNewApplyNotify(reply)

    def onNewInviteNotify(self, rpc_controller, reply, done):
        self.mgr.onNewInviteNotify(reply)

    def onReportGuildScoreResult(self, rpc_controller, reply, done):
        self.mgr.onReportGuildScoreResult(reply)

    def onSyncGuildInfoResult(self, rpc_controller, reply, done):
        self.mgr.onSyncGuildInfoResult(reply)

    def onNewMemberJoined(self, rpc_controller, reply, done):
        self.mgr.onNewMemberJoined(reply)

    def onJoinToAllianceNotify(self, rpc_controller, reply, done):
        self.mgr.onJoinToAllianceNotify(reply)

    def onApplyToJoinResult(self, rpc_controller, reply, done):
        self.mgr.onApplyToJoinResult(reply)

    def onReturnGuildFundNotify(self, rpc_controller, reply, done):
        self.mgr.onReturnGuildFundNotify(reply)
    
    def onGuildAidResourceNotify(self, rpc_controller, reply, done):
        self.mgr.onGuildAidResourceNotify(reply)

    # ---- Guild Simple Info (cross-server query) ----
    def checkGuildSimpleInfo(self, rpc_controller, request, done):
        self.mgr.checkGuildSimpleInfo(request)

    def onGetGuildSimpleInfoResult(self, rpc_controller, reply, done):
        self.mgr.onGetGuildSimpleInfoResult(reply)

    def onLeagueGuildLeave(self, rpc_controller, reply, done):
        self.mgr.onLeagueGuildLeave(reply)

    def onLeagueDisband(self, rpc_controller, reply, done):
        self.mgr.onLeagueDisband(reply)

    def onBroadcastRemoveGuildRelation(self, rpc_controller, reply, done):
        self.mgr.onBroadcastRemoveGuildRelation(reply)

    def onBroadcastAddGuildRelation(self, rpc_controller, reply, done):
        self.mgr.onBroadcastAddGuildRelation(reply)

    def onLeagueGuildEventNotify(self, rpc_controller, reply, done):
        self.mgr.onLeagueGuildEventNotify(reply)
    
    def onLeagueGuildMessageNotify(self, rpc_controller, reply, done):
        self.mgr.onLeagueGuildMessageNotify(reply)
    
    def onLeagueBroadCastMessageNotify(self, rpc_controller, reply, done):
        self.mgr.onLeagueBroadCastMessageNotify(reply)

    def onRecruitLeagueMemberResult(self, rpc_controller, reply, done):
        self.mgr.onRecruitLeagueMemberResult(reply)
     
    def onCheckLeaveGuildResult(self, rpc_controller, reply, done):
        self.mgr.onCheckLeaveGuildResult(reply)

    def onQueryLeagueUUIDResult(self, rpc_controller, reply, done):
        self.mgr.onQueryLeagueUUIDResult(reply)

    def onCancelApplyResult(self, rpc_controller, reply, done):
        self.mgr.onCancelApplyResult(reply)

    def onGuildRelationAll(self, rpc_controller, reply, done):
        self.mgr.onGuildRelationAll(reply)

class AllianceStub(iGlobal.IGlobal, iBaseNoCell.IBaseNoCell, iTimer.ITimer, iCentralStub.ICentralStub):
    SERVICE_CLASS = AllianceService

    def __init__(self):
        LOG_INFO('AllianceStub __init__')
        self.initDatetimeTimerTick()
        self.initCentralServers('allianceServiceInfo', 'allianceServiceId')

        self.remoteCallCache = {}
        self.connectSuccessTimes = 0
        # 联盟数据 100% 以 allianceService 微服务为权威;game server 不做任何联盟数据缓存
        # (approveType/leaderGuildId/leaderServerId/name/memberGuildIds 等都不本地维护)
        # 去重状态属于事件层,不算联盟数据缓存,保留:
        # AllianceChangedBroadcast(changeType=2) 与 onNewApplyNotify(auto+approved)
        # 都可能触发自动同意广播;按 (allianceId, newGuildId) 在窗口期内只发一次
        # key -> ts(秒)
        self._autoAcceptNotifyLog = {}
        self._autoAcceptNotifyWindow = 10  # 10秒内同一对 allianceId+guildId 只发一次

        _interval = 5
        self.pyAddTimer(_interval, _interval, gametimer.ALLIANCE_STUB_CONNECT_TICK)

        self.pyAddTimer(6, 6, gametimer.ALLIANCE_CLEAR_CACHE)

    def onTimer(self, tid, userArg):
        if utils.isBelongTimerTag(userArg):
            self._onTimerCallback(tid)
        elif userArg == gametimer.TIMER_DATETIME_ITIMER_CALLBACK:
            self._onDatetimeTimerTick()
        elif userArg == gametimer.ALLIANCE_STUB_CONNECT_TICK:
            self.connectAll()
        elif userArg == gametimer.ALLIANCE_CLEAR_CACHE:
            self.clearCache()
        else:
            self._onTimerTrigger(tid, userArg)

    def doNext(self):
        LOG_DBG('AllianceStub doNext')
        super().doNext()

    def onAllianceServiceConnected(self, centralServerId):
        LOG_INFO('AllianceStub onAllianceServiceConnected', centralServerId)
        serverId = gameconfig.serverId()

        _req = RegisterGameServerRequest()
        _req.serverId = serverId

        _client = self.csClients[centralServerId]
        _client.asStub.registerGameServer(None, _req, None)

        self.connectSuccessTimes += 1

    def clearCache(self):
        _deleteCacheUUID = []
        _now = utils.curTS()
        for _uuid, _cache in self.remoteCallCache.items():
            _ts = _cache.get('ts')
            if _now - _ts > 10:
                _deleteCacheUUID.append(_uuid)

        for _uuid in _deleteCacheUUID:
            self.remoteCallCache.pop(_uuid, None)

    def sendActiveTick(self):
        for csInfo in self.centralServerDict.values():
            _client = self.csClients.get(csInfo.serverId)
            if not (_client and _client.channel.dispatcher):
                continue
            _client.asStub.activeTick(None, Void(), None)

    def onAllianceServiceDisconnected(self, centralServerId):
        LOG_DBG('AllianceStub onAllianceServiceDisconnected', centralServerId)

    # ---- Helper: RPC call with cache ----
    def _call(self, stubMethod, req, cacheData=None):
        req.uuid = KBEngine.genUUID64()
        _client = self.getRandomClient()
        if not _client:
            LOG_WARN('AllianceStub no client for call')
            return None

        if cacheData:
            cacheData['ts'] = utils.curTS()
            self.remoteCallCache[req.uuid] = cacheData

        stubMethod(_client, req, None)
        return req.uuid

    # ---- Helper: RPC call to a specific server ----
    def _callToServer(self, stubMethod, req, cacheData=None, serverId=0):
        req.uuid = KBEngine.genUUID64()
        _client = self.getRandomClient()
        if not _client:
            LOG_WARN('AllianceStub no client for callToServer')
            return None

        if cacheData:
            cacheData['ts'] = utils.curTS()
            self.remoteCallCache[req.uuid] = cacheData

        stubMethod(_client, req, None)
        return req.uuid

    # ---- Core ----
    def createLeague(self, guildId, serverId, allianceId, name, declaration, approveType, playerGbId, guildBox, avatarBox,
                     leaderName='', leaderLevel=0,
                     leaderServerId=0, leaderProfession=0, leaderGender=0,
                     guildName='', dspFlag=0, guildIcon=0,
                     guildScore=0, guildLevel=0, memberCount=0, maxMemberNum=0):
        _req = CreateLeagueRequest()
        _req.guildId = guildId
        _req.serverId = serverId
        _req.allianceId = allianceId
        _req.name = name
        _req.declaration = declaration
        _req.approveType = approveType
        _req.playerGbId = playerGbId
        _req.leaderName = leaderName
        _req.leaderLevel = leaderLevel
        # === Leader data (盟主数据) ===
        _req.leaderServerId = leaderServerId
        _req.leaderProfession = leaderProfession
        _req.leaderGender = leaderGender
        # === Leader's guild data (盟主所在帮会数据) ===
        _req.guildName = guildName
        _req.dspFlag = dspFlag
        _req.guildIcon = guildIcon
        _req.guildScore = guildScore
        _req.guildLevel = guildLevel
        _req.memberCount = memberCount
        _req.maxMemberNum = maxMemberNum
        self._call(lambda c, r, d: c.asStub.createLeague(None, r, None), _req, {'box': guildBox, 'avatarBox': avatarBox})

    def onCreateLeagueResult(self, reply):
        _cache = self.remoteCallCache.pop(reply.uuid, None)
        if not _cache:
            LOG_ERR('AllianceStub onCreateLeagueResult no cache', reply.uuid)
            return
        _box = _cache.get('box')
        _avatarBox = _cache.get('avatarBox')
        if _box:
            _detail = self._detailToFixedDict(reply.alliance)
            _members = self._memberToFixedDict(reply.members)
            _box.onCreateLeagueResult(reply.errCode, _detail, _members, _avatarBox)

    def disbandLeague(self, allianceId, playerGbId, guildBox, avatarBox):
        _req = DisbandLeagueRequest()
        _req.allianceId = allianceId
        _req.playerGbId = playerGbId
        self._call(lambda c, r, d: c.asStub.disbandLeague(None, r, None), _req, {'box': guildBox, 'avatarBox': avatarBox})

    def onDisbandLeagueResult(self, reply):
        _cache = self.remoteCallCache.pop(reply.uuid, None)
        if not _cache:
            LOG_ERR('AllianceStub onDisbandLeagueResult no cache', reply.uuid)
            return
        _box = _cache.get('box')
        _avatarBox = _cache.get('avatarBox')
        if _box:
            _box.onDisbandLeagueResult(reply.errCode, _avatarBox)

    def recruitLeagueMember(self, leagueUUID, box):
        _req = RecruitLeagueMemberRequest()
        _req.leagueUUID = leagueUUID
        self._call(lambda c, r, d: c.asStub.recruitLeagueMember(None, r, None), _req, {'box': box})

    def modifyLeagueInfo(self, allianceId, playerGbId, name, declaration, approveType, box):
        _req = ModifyLeagueInfoRequest()
        _req.allianceId = allianceId
        _req.playerGbId = playerGbId
        if name is not None:
            _req.name = name
        if declaration is not None:
            _req.declaration = declaration
        if approveType is not None:
            _req.approveType = approveType
        self._call(lambda c, r, d: c.asStub.modifyLeagueInfo(None, r, None), _req, {'box': box})

    def onModifyLeagueInfoResult(self, reply):
        _cache = self.remoteCallCache.pop(reply.uuid, None)
        if not _cache:
            return
        _cache.get('box').onModifyLeagueInfoResult(reply.errCode)

    def getLeagueList(self, serverId, pageIndex, pageSize, box, func=None, args=None):
        _req = GetLeagueListRequest()
        _req.serverId = serverId
        _req.pageIndex = pageIndex
        _req.pageSize = pageSize
        self._call(lambda c, r, d: c.asStub.getLeagueList(None, r, None), _req, {'box': box, 'func': func, 'args': args})

    def onLeagueListResult(self, reply):
        _cache = self.remoteCallCache.pop(reply.uuid, None)
        if not _cache:
            return
        _box = _cache.get('box')
        _func = _cache.get('func')
        _entries = []
        for e in reply.entries:
            _entries.append(self._entryToFixedDict(e))
        if _func and hasattr(_box, _func):
            _args = _cache.get('args') or []
            getattr(_box, _func)(_entries, *_args)
        else:
            _box.onLeagueListResult(_entries, reply.pageIndex, reply.totalPage)

    def searchLeague(self, keyword, serverId, box):
        _req = SearchLeagueRequest()
        _req.keyword = keyword
        _req.serverId = serverId
        self._call(lambda c, r, d: c.asStub.searchLeague(None, r, None), _req, {'box': box})

    def onSearchLeagueResult(self, reply):
        _cache = self.remoteCallCache.pop(reply.uuid, None)
        if not _cache:
            return
        _entries = []
        for e in reply.entries:
            _entries.append(self._entryToFixedDict(e))
        _cache.get('box').onSearchLeagueResult(_entries)

    def getLeagueDetail(self, allianceId, box):
        _req = GetLeagueDetailRequest()
        _req.allianceId = allianceId
        self._call(lambda c, r, d: c.asStub.getLeagueDetail(None, r, None), _req, {'box': box})

    def onLeagueDetailResult(self, reply):
        _cache = self.remoteCallCache.pop(reply.uuid, None)
        if not _cache:
            return
        _alliance = self._detailToFixedDict(reply.alliance)
        _members = self._memberToFixedDict(reply.members)
        _cache.get('box').onLeagueDetailResult(_alliance, _members, reply.errCode)

    # ---- 单独接口: 按 allianceId 拉取基础信息 ----
    def getLeagueBasicInfo(self, allianceId, box):
        _req = GetLeagueBasicInfoRequest()
        _req.allianceId = allianceId
        self._call(lambda c, r, d: c.asStub.getLeagueBasicInfo(None, r, None), _req, {'box': box})

    def onGetLeagueBasicInfoResult(self, reply):
        _cache = self.remoteCallCache.pop(reply.uuid, None)
        if not _cache:
            return
        _info = self._basicInfoToFixedDict(reply.info)
        _cache.get('box').onGetLeagueBasicInfoResult(_info, reply.errCode)

    def _basicInfoToFixedDict(self, info):
        """Convert the focused AllianceBasicInfo pb into a plain dict for box consumption.
        Returned shape (all 9 fields):
          allianceId, declaration, approveType,
          leaderName, leaderGender, leaderLevel,
          leaderServerId, leaderProfession, leaderGbId
        """
        if info is None:
            return {
                'allianceId':       0,
                'declaration':      '',
                'approveType':      0,
                'leaderName':       '',
                'leaderGender':     0,
                'leaderLevel':      0,
                'leaderServerId':   0,
                'leaderProfession': 0,
                'leaderGbId':       0,
            }
        return {
            'allianceId':       info.allianceId,
            'declaration':      info.declaration,
            'approveType':      info.approveType,
            'leaderName':       info.leaderName,
            'leaderGender':     info.leaderGender,
            'leaderLevel':      info.leaderLevel,
            'leaderServerId':   info.leaderServerId,
            'leaderProfession': info.leaderProfession,
            'leaderGbId':       info.leaderGbId,
        }

    # ---- getLeagueSimpleInfo ----
    def getLeagueSimpleInfo(self, allianceId, box):
        _req = GetLeagueSimpleInfoRequest()
        _req.allianceId = allianceId
        self._call(lambda c, r, d: c.asStub.getLeagueSimpleInfo(None, r, None), _req, {'box': box})

    def onGetLeagueSimpleInfoResult(self, reply):
        _cache = self.remoteCallCache.pop(reply.uuid, None)
        if not _cache:
            return
        _info = self._leagueSimpleToFixedDict(reply.info)
        _cache.get('box').onGetLeagueSimpleInfoResult(_info, reply.errCode)

    def _leagueSimpleToFixedDict(self, info):
        if info is None:
            return {
                'allianceId': 0,
                'name':       '',
                'power':      0,
                'members':    [],
            }
        _members = []
        for m in info.members:
            _members.append({
                'guildId':   m.guildId,
                'guildName': m.guildName,
                'guildIcon': m.guildIcon,
                'dspFlag':   m.dspFlag,
            })
        return {
            'allianceId': info.allianceId,
            'name':       info.name,
            'power':      info.totalScore,
            'members':    _members,
        }

    # ---- Member ----
    # applyToJoin carries a full AllianceMemberInfo snapshot (except joinTime,
    # which the central service stamps at insert time) so the auto-approve path
    # can build a complete member row without a follow-up RPC.
    #   memberCount / memberRole / guildIcon / guildLevel / dspFlag / maxMemberNum
    # are sourced from GuildMemberVal on the kbengine side.
    def applyToJoin(self, allianceId, guildId, serverId, guildScore, guildName,
                    memberCount, guildIcon, guildLevel,
                    dspFlag, maxMemberNum, leaderGbId, leaderName, leaderLevel, leaderProfession, leaderGender, playerGbId, box):
        _req = ApplyToJoinRequest()
        _req.allianceId = allianceId
        _req.guildId = guildId
        _req.serverId = serverId
        _req.guildScore = guildScore
        _req.guildName = guildName
        _req.playerGbId = playerGbId
        _req.memberCount = memberCount
        _req.guildIcon = guildIcon
        _req.guildLevel = guildLevel
        _req.dspFlag = dspFlag
        _req.maxMemberNum = maxMemberNum
        _req.leaderGbId = leaderGbId
        _req.leaderName = leaderName
        _req.leaderLevel = leaderLevel
        _req.leaderProfession = leaderProfession
        _req.leaderGender = leaderGender
        self._call(lambda c, r, d: c.asStub.applyToJoin(None, r, None), _req, {'box': box})

    def onApplyLeagueToJoinResult(self, reply):
        _cache = self.remoteCallCache.pop(reply.uuid, None)
        if not _cache:
            return
        # allianceService now returns the alliance card data (id/name/power)
        # so the box can notify the client immediately on success.
        _cache.get('box').onApplyLeagueToJoinResult(
            reply.errCode,
            reply.allianceId,
            reply.allianceName,
            reply.alliancePower,
        )

    def approveJoin(self, playerGbId, box, guildId, allianceId):
        _req = ApproveJoinRequest()
        _req.allianceId = allianceId
        _req.playerGbId = playerGbId
        _req.guildId = guildId
        self._call(lambda c, r, d: c.asStub.approveJoin(None, r, None), _req, {'box': box})

    def onApproveJoinResult(self, reply):
        _cache = self.remoteCallCache.pop(reply.uuid, None)
        if not _cache:
            return
        _cache.get('box').onApproveLeagueJoinResult(reply.errCode, reply.joinedGuildId, reply.guildCD)

    def rejectJoin(self, guildId, playerGbId, box):
        _req = RejectJoinRequest()
        _req.guildId = guildId
        _req.playerGbId = playerGbId
        self._call(lambda c, r, d: c.asStub.rejectJoin(None, r, None), _req, {'box': box})

    def onRejectJoinResult(self, reply):
        _cache = self.remoteCallCache.pop(reply.uuid, None)
        if not _cache:
            return
        _cache.get('box').onRejectLeagueJoinResult(reply.errCode, reply.rejectedGuildId)

    def cancelApply(self, leagueUUID, guildId, box):
        _req = CancelApplyRequest()
        _req.leagueUUID = leagueUUID
        _req.guildId = guildId
        self._call(lambda c, r, d: c.asStub.cancelApply(None, r, None), _req, {'box': box})

    def onCancelApplyResult(self, reply):
        _cache = self.remoteCallCache.pop(reply.uuid, None)
        if not _cache:
            return
        _cache.get('box').onCancelLeagueApplyResult(reply.errCode, reply.allianceId)

    def inviteGuild(self, allianceId, targetGuildId, targetServerId, playerGbId, box):
        _req = InviteGuildRequest()
        _req.allianceId = allianceId
        _req.targetGuildId = targetGuildId
        _req.targetServerId = targetServerId
        _req.playerGbId = playerGbId
        self._call(lambda c, r, d: c.asStub.inviteGuild(None, r, None), _req, {'box': box})

    def onInviteGuildResult(self, reply):
        _cache = self.remoteCallCache.pop(reply.uuid, None)
        if not _cache:
            return
        _cache.get('box').onInviteGuildResult(reply.errCode, reply.targetGuildId, reply.guildCD)

    def acceptInvite(self, allianceId, guildUUID, serverId, guildScore, memberCount, guildIcon, 
                     guildLevel, guildName, dspFlag, maxMemberNum, leaderGbId, leaderName, leaderLevel, leaderProfession, leaderGender, oprGbId, avatarBox):
        _req = AcceptInviteRequest()
        _req.allianceId = allianceId
        _req.guildId = guildUUID
        _req.serverId = serverId
        _req.guildScore = guildScore
        _req.guildName = guildName
        _req.playerGbId = oprGbId
        _req.memberCount = memberCount
        _req.guildIcon = guildIcon
        _req.guildLevel = guildLevel
        _req.dspFlag = dspFlag
        _req.maxMemberNum = maxMemberNum
        _req.leaderGbId = leaderGbId
        _req.leaderName = leaderName
        _req.leaderLevel = leaderLevel
        _req.leaderProfession = leaderProfession
        _req.leaderGender = leaderGender
        self._call(lambda c, r, d: c.asStub.acceptInvite(None, r, None), _req, {'box': avatarBox})

    def onAcceptInviteResult(self, reply):
        _cache = self.remoteCallCache.pop(reply.uuid, None)
        if not _cache:
            return
        _cache.get('box').onAcceptLeagueInviteResult(reply.errCode, reply.allianceId)

    def rejectInvite(self, allianceId, guildId, playerGbId, box):
        _req = RejectInviteRequest()
        _req.guildId = guildId
        _req.playerGbId = playerGbId
        _req.allianceId = allianceId
        self._call(lambda c, r, d: c.asStub.rejectInvite(None, r, None), _req, {'box': box})

    def onRejectInviteResult(self, reply):
        _cache = self.remoteCallCache.pop(reply.uuid, None)
        if not _cache:
            return
        _cache.get('box').onRejectLeagueInviteResult(reply.errCode, reply.allianceId)

    def kickMember(self, allianceId, targetGuildId, playerGbId, box):
        _req = KickMemberRequest()
        _req.allianceId = allianceId
        _req.targetGuildId = targetGuildId
        _req.playerGbId = playerGbId
        self._call(lambda c, r, d: c.asStub.kickMember(None, r, None), _req, {'box': box})

    def onKickMemberResult(self, reply):
        _cache = self.remoteCallCache.pop(reply.uuid, None)
        if not _cache:
            return
        _cache.get('box').onKickMemberResult(reply.errCode)

    def leaveLeague(self, allianceId, guildId, playerGbId, box):
        _req = LeaveLeagueRequest()
        _req.allianceId = allianceId
        _req.guildId = guildId
        _req.playerGbId = playerGbId
        self._call(lambda c, r, d: c.asStub.leaveLeague(None, r, None), _req, {'box': box})

    def onLeaveLeagueResult(self, reply):
        _cache = self.remoteCallCache.pop(reply.uuid, None)
        if not _cache:
            return
        _cache.get('box').onLeaveLeagueResult(reply.errCode)

    def transferLeader(self, allianceId, targetGuildId, playerGbId, box):
        _req = TransferLeaderRequest()
        _req.allianceId = allianceId
        _req.targetGuildId = targetGuildId
        _req.playerGbId = playerGbId
        self._call(lambda c, r, d: c.asStub.transferLeader(None, r, None), _req, {'box': box})

    def onTransferLeaderResult(self, reply):
        LOG_INFO('onTransferLeaderResult ', reply)
        _cache = self.remoteCallCache.pop(reply.uuid, None)
        if not _cache:
            return
        data = self._detailToFixedDict(reply.alliance)

        _cache.get('box').onTransferLeagueLeaderResult(reply.errCode, data)

    def getApplyList(self, allianceId, box):
        _req = GetApplyListRequest()
        _req.allianceId = allianceId
        self._call(lambda c, r, d: c.asStub.getApplyList(None, r, None), _req, {'box': box})

    def onApplyListResult(self, reply):
        _cache = self.remoteCallCache.pop(reply.uuid, None)
        if not _cache:
            return
        _applies = []
        for a in reply.applies:
            _applies.append(self._applyToFixedDict(a))
        _cache.get('box').onLeagueApplyListResult(_applies)

    def getInviteList(self, guildId, box):
        _req = GetInviteListRequest()
        _req.guildId = guildId
        self._call(lambda c, r, d: c.asStub.getInviteList(None, r, None), _req, {'box': box})

    def onInviteListResult(self, reply):
        _cache = self.remoteCallCache.pop(reply.uuid, None)
        if not _cache:
            return
        _invites = self._inviteToFixedDict(reply)
        _cache.get('box').onInviteListResult(_invites)

    def getSentApplies(self, guildId, box):
        _req = GetSentAppliesRequest()
        _req.guildId = guildId
        self._call(lambda c, r, d: c.asStub.getSentApplies(None, r, None), _req, {'box': box})

    def onSentAppliesResult(self, reply):
        _cache = self.remoteCallCache.pop(reply.uuid, None)
        if not _cache:
            return
        _applies = []
        for a in reply.applies:
            _applies.append(self._sentToFixedDict(a))
        _cache.get('box').onLeagueSentAppliesResult(_applies)

    # ---- Diplomacy ----
    def declareWar(self, guildName, playerGbId, attackType, attackId, targetType, targetId, targetServerId, amount, box):
        _req = DeclareWarRequest()
        _req.guildName = guildName
        _req.attackType = attackType
        _req.attackId = attackId
        _req.targetType = targetType
        _req.targetId = targetId
        _req.targetServerId = targetServerId
        _req.playerGbId = playerGbId
        _req.amount = amount
        self._call(lambda c, r, d: c.asStub.declareWar(None, r, None), _req, {'box': box})

    def onDeclareWarResult(self, reply):
        _cache = self.remoteCallCache.pop(reply.uuid, None)
        if not _cache:
            return
        _cache.get('box').onDeclareWarResult(reply.errCode, reply.endTime)

    def getEnemyList(self, guildId, box):
        _req = GetEnemyListRequest()
        _req.guildId = guildId
        self._call(lambda c, r, d: c.asStub.getEnemyList(None, r, None), _req, {'box': box})

    def getUnionList(self, guildId, box):
        _req = GetUnionListRequest()
        _req.guildId = guildId
        self._call(lambda c, r, d: c.asStub.getUnionList(None, r, None), _req, {'box': box})

    def getEnemyAllianceList(self, allianceId, guildId, box):
        _req = GetEnemyAllianceListRequest()
        _req.allianceId = allianceId
        _req.guildId = guildId
        self._call(lambda c, r, d: c.asStub.getEnemyAllianceList(None, r, None), _req, {'box': box})

    def onEnemyListResult(self, reply):
        _cache = self.remoteCallCache.pop(reply.uuid, None)
        if not _cache:
            return
        _enemies = []
        for e in reply.enemies:
            _enemies.append(self._enemyToFixedDict(e))
        _cache.get('box').onLeagueEnemyList(_enemies)

    def onEnemyAllianceListResult(self, reply):
        _cache = self.remoteCallCache.pop(reply.uuid, None)
        if not _cache:
            return
        _enemies = []
        for e in reply.enemies:
            _enemies.append(self._enemyRowToFixedDict(e))
        _cache.get('box').onLeagueEnemyAllianceList(_enemies)

    def onUnionListResult(self, reply):
        _cache = self.remoteCallCache.pop(reply.uuid, None)
        if not _cache:
            return
        _unions = []
        for e in reply.unions:
            _unions.append(e.guildId)
        _cache.get('box').onLeagueUnionList(_unions)

    # ---- Guild Simple Info (cross-server query) ----
    def getGuildSimpleInfo(self, guildId, targetServerId, box):
        _req = GetGuildSimpleInfoRequest()
        _req.guildId = guildId
        _req.serverId = targetServerId
        self._call(lambda c, r, d: c.asStub.getGuildSimpleInfo(None, r, None), _req, {'box': box})

    def onGetGuildSimpleInfoResult(self, reply):
        _cache = self.remoteCallCache.pop(reply.uuid, None)
        if not _cache:
            return
        if reply.info:
            _info = {
                'guildId':    reply.info.guildId,
                'guildName':  reply.info.guildName,
                'guildIcon':  reply.info.guildIcon,
                'dspFlag':    reply.info.dspFlag,
                'score':      reply.info.score,
                'guildLevel': reply.info.guildLevel,
                'memberCnt':  reply.info.memberCnt,
            }
        else:
            _info = {
                'guildId':    0,
                'guildName':  '',
                'guildIcon':  0,
                'dspFlag':    0,
                'score':      0,
                'guildLevel': 0,
                'memberCnt':  0,
            }
        _cache.get('box').onGetGuildSimpleInfoResult(_info, reply.errCode)

    def checkLeagueRelation(self, guildId1, guildId2, box):
        _req = CheckLeagueRelationRequest()
        _req.guildId1 = guildId1
        _req.guildId2 = guildId2
        self._call(lambda c, r, d: c.asStub.checkLeagueRelation(None, r, None), _req, {'box': box})

    def onCheckLeagueRelationResult(self, reply):
        _cache = self.remoteCallCache.pop(reply.uuid, None)
        if not _cache:
            return
        _cache.get('box').onCheckLeagueRelationResult(reply.isSameAlliance, reply.allianceId)

    def getGuildAlliance(self, guildId, box):
        _req = GetGuildAllianceRequest()
        _req.guildId = guildId
        self._call(lambda c, r, d: c.asStub.getGuildAlliance(None, r, None), _req, {'box': box})

    def onGetGuildAllianceResult(self, reply):
        _cache = self.remoteCallCache.pop(reply.uuid, None)
        if not _cache:
            return
        _cache.get('box').onGetGuildAllianceResult(reply.allianceId, reply.errCode)

    # ---- Resource ----
    def donateFund(self, allianceId, guildId, itemId, amount, playerGbId, box):
        _req = DonateFundRequest()
        _req.allianceId = allianceId
        _req.guildId = guildId
        _req.itemId = itemId
        _req.amount = amount
        _req.playerGbId = playerGbId
        self._call(lambda c, r, d: c.asStub.donateFund(None, r, None), _req, {'box': box})

    def onDonateFundResult(self, reply):
        _cache = self.remoteCallCache.pop(reply.uuid, None)
        if not _cache:
            return
        _cache.get('box').onLeagueDonateFundResult(reply.errCode, reply.allianceId, reply.allianceFund)

    def aidResource(self, allianceId, fromGuildId, toGuildId, itemId, amount, playerGbId, box):
        _req = AidResourceRequest()
        _req.allianceId = allianceId
        _req.fromGuildId = fromGuildId
        _req.toGuildId = toGuildId
        _req.itemId = itemId
        _req.amount = amount
        _req.playerGbId = playerGbId
        self._call(lambda c, r, d: c.asStub.aidResource(None, r, None), _req, {'box': box})

    def onAidResourceResult(self, reply):
        _cache = self.remoteCallCache.pop(reply.uuid, None)
        if not _cache:
            return
        _cache.get('box').onAidResourceResult(reply.errCode)

    def getLeagueFund(self, allianceId, box):
        _req = GetLeagueFundRequest()
        _req.allianceId = allianceId
        self._call(lambda c, r, d: c.asStub.getLeagueFund(None, r, None), _req, {'box': box})

    def onLeagueFundResult(self, reply):
        _cache = self.remoteCallCache.pop(reply.uuid, None)
        if not _cache:
            return
        _cache.get('box').onLeagueFundResult(reply.fund)

    # ---- Event & Chat ----
    def getEventList(self, allianceId, box):
        _req = GetEventListRequest()
        _req.allianceId = allianceId
        self._call(lambda c, r, d: c.asStub.getEventList(None, r, None), _req, {'box': box})

    def onEventListResult(self, reply):
        _cache = self.remoteCallCache.pop(reply.uuid, None)
        if not _cache:
            return
        _events = []
        for e in reply.events:
            _events.append(self._eventToFixedDict(e))
        _cache.get('box').onEventListResult(_events)

    def sendChatMessage(self, allianceId, senderGuildId, senderGuildName, senderServerId, content, box):
        _req = SendChatMessageRequest()
        _req.allianceId = allianceId
        _req.senderGuildId = senderGuildId
        _req.senderGuildName = senderGuildName
        _req.senderServerId = senderServerId
        _req.content = content
        self._call(lambda c, r, d: c.asStub.sendChatMessage(None, r, None), _req, {'box': box})

    def onSendChatMessageResult(self, reply):
        _cache = self.remoteCallCache.pop(reply.uuid, None)
        if not _cache:
            return
        _cache.get('box').onSendChatMessageResult(reply.errCode)

    def getChatHistory(self, allianceId, limit, box):
        _req = GetChatHistoryRequest()
        _req.allianceId = allianceId
        _req.limit = limit
        self._call(lambda c, r, d: c.asStub.getChatHistory(None, r, None), _req, {'box': box})

    def onChatHistoryResult(self, reply):
        _cache = self.remoteCallCache.pop(reply.uuid, None)
        if not _cache:
            return
        _msgs = []
        for m in reply.messages:
            _msgs.append(self._chatMsgToFixedDict(m))
        _cache.get('box').onChatHistoryResult(_msgs)

    def reportGuildScore(self, guildId, guildScore):
        _req = ReportGuildScoreRequest()
        _req.guildId = guildId
        _req.guildScore = guildScore
        self._call(lambda c, r, d: c.asStub.reportGuildScore(None, r, None), _req, None)

    def syncGuildInfo(self, guildId, guildName, guildIcon, dspFlag, guildLevel, memberCount, maxMemberCount, 
                      guildScore, leaderGbId, leaderName, leaderLevel, leaderProfession, leaderGender):
        _req = SyncGuildInfoRequest()
        _req.guildId = guildId
        _req.guildName = guildName
        _req.guildIcon = guildIcon
        _req.dspFlag = dspFlag
        _req.guildLevel = guildLevel
        _req.memberCount = memberCount
        _req.maxMemberCount = maxMemberCount
        _req.guildScore = guildScore
        _req.leaderGbId = leaderGbId
        _req.leaderName = leaderName
        _req.leaderLevel = leaderLevel
        _req.leaderProfession = leaderProfession
        _req.leaderGender = leaderGender
        self._call(lambda c, r, d: c.asStub.syncGuildInfo(None, r, None), _req, None)

    def onCheckGuildResult(self, guildId, guildName, uniqueId, ret, cd, checkCD):
        _req = CheckGuildExistsResult()
        _req.guildId = guildId
        _req.guildName = guildName
        _req.exists = ret
        _req.guildCD = cd
        _req.uuid = uniqueId
        _req.checkCD = checkCD
        _client = self.getRandomClient()
        if not _client:
            LOG_WARN('AllianceStub no client for call')
            return None
        _client.asStub.onCheckGuildExistsResult(None, _req, None)

    def onCheckLeaveGuild(self, leagueUUID, guildId, playerGbId, box):
        _req = CheckLeaveGuildRequest()
        _req.leagueUUID = leagueUUID
        _req.guildId = guildId
        _req.playerGbId = playerGbId
        _client = self.getRandomClient()
        if not _client:
            LOG_WARN('AllianceStub no client for call')
            return None
        self._call(lambda c, r, d: c.asStub.checkLeaveGuild(None, r, None), _req, {'box': box})

    def queryLeagueUUID(self, guildUUID):
        _req = QueryLeagueUUIDRequest()
        _req.guildId = guildUUID

        _client = self.getRandomClient()
        if not _client:
            LOG_WARN('AllianceStub no client for call')
            return None
        self._call(lambda c, r, d: c.asStub.queryLeagueUUID(None, r, None), _req, {'box': None})

    def onReportGuildScoreResult(self, reply):
        _cache = self.remoteCallCache.pop(reply.uuid, None)

    def onSyncGuildInfoResult(self, reply):
        _cache = self.remoteCallCache.pop(reply.uuid, None)

    def onNewMemberJoined(self, reply):
        memberData = self._memberToFixedDictWithSingle(reply.member)
        gameengine.getGlobalBase('PlayerStub').doOnOthersClient(
                                        [reply.playerGbId, ], 'onNewMemberJoined', (memberData,),
                                        None, '', ())
        
    def onJoinToAllianceNotify(self, reply):
        leagueUUID = reply.allianceId
        guildUUID = reply.guildUUID
        gameengine.getGlobalBase('GuildStub').callOnGuild(guildUUID, 'onSetLeagueUUID', (leagueUUID,), None, '', ())

    # ---- Broadcasts (dispatched to all guilds) ----
    def onWarStarted(self, reply):
        gameengine.getGlobalBase('GuildStub').broadcastToAllGuild('onAllianceWarStarted', (self._warEnemyToFixedDict(reply.enemy),))

    def onWarEnded(self, reply):
        gameengine.getGlobalBase('GuildStub').broadcastToAllGuild('onAllianceWarEnded', (self._warEndedToFixedDict(reply),))

    # ---- Guild Relation Broadcasts (ported from CrossDataStub) ----
    def onGuildRelationAll(self, reply):
        LOG_INFO('AllianceStub onGuildRelationAll', reply)
        _relationDic = {}
        for _relationData in reply.relations:
            _pair = utils.getGuildUUIDPair(_relationData.guildUUID1, _relationData.guildUUID2)
            _relationDic[_pair] = _relationData.relationType
        gameengine.callAllApps('gameengine.resetGuildRelation', (_relationDic, reply.version))

    def onBroadcastAddGuildRelation(self, reply):
        LOG_INFO('AllianceStub onBroadcastGuildAddRelation', reply)
        gameengine.callAllApps(
            'gameengine.addGuildRelation',
            (reply.guildUUID1, reply.guildUUID2, reply.relationType, reply.version))
        gameengine.getGlobalBase('GuildStub').broadcastGuildMemberClient(
            [reply.guildUUID1], 'onAddGuildRelationClient',
            (reply.guildUUID2, reply.relationType, reply.version))
        gameengine.getGlobalBase('GuildStub').broadcastGuildMemberClient(
            [reply.guildUUID2], 'onAddGuildRelationClient',
            (reply.guildUUID1, reply.relationType, reply.version))

    def onBroadcastRemoveGuildRelation(self, reply):
        LOG_INFO('AllianceStub onBroadcastRemoveGuildRelation', reply)
        gameengine.callAllApps(
            'gameengine.removeGuildRelation',
            (reply.guildUUID1, reply.guildUUID2, reply.version))
        gameengine.getGlobalBase('GuildStub').broadcastGuildMemberClient(
            [reply.guildUUID1], 'onRemoveGuildRelationClient',
            (reply.guildUUID2,))
        gameengine.getGlobalBase('GuildStub').broadcastGuildMemberClient(
            [reply.guildUUID2], 'onRemoveGuildRelationClient',
            (reply.guildUUID1,))
        
    def onNewEvent(self, reply):
        # central service 已按 serverId 预分组,reply.guildIds 仅为本服中属于
        # 该联盟的帮会;逐一 callOnGuild 转发,避免给无关帮会推事件
        _d = self._eventToFixedDict(reply.event)
        for _gid in reply.guildIds:
            gameengine.getGlobalBase('GuildStub').callOnGuild(_gid, 'onAllianceNewEvent', (_d,), None, '', ())

    def onChatMessage(self, reply):
        _d = {
            'allianceId': reply.allianceId,
            'message': self._chatMsgToFixedDict(reply.message),
        }
        gameengine.getGlobalBase('GuildStub').broadcastToAllGuild('onAllianceChatMessage', (_d,))

    def onDisbandLeagueNotify(self, reply):
        # 不缓存联盟数据,无需清理;仅通知 reply.guildIds 中的帮会
        _guildStub = gameengine.getGlobalBase('GuildStub')
        if not _guildStub:
            return
        for _gid in reply.guildIds:
            _guildStub.callOnGuild(_gid, 'onLeagueDisbanded', (reply.allianceId,), None, '', ())

    def onNewApplyNotify(self, reply):
        # allianceService 推送的 NewApplyNotify 仅含 5 个字段:
        #   guildUUID / guildName / guildIcon / dspFlag / power
        # (原 AllianceApplyInfo 的 leaderGuildId 已移除 → 不再按 leaderGuildId 路由)
        # 这里把 5 字段打包交给 mgr(iLeague),由 mgr 决定如何通知客户端:
        #   - 旧: callOnGuild(leaderGuildId, 'onNewApplyNotify', ...) → Guild 实体
        #   - 新: 直接 self.mgr.onNewApplyNotify(_apply)
        _apply = self._newApplyToFixedDict(reply)
        LOG_INFO('AllianceStub onNewApplyNotify', reply)
        gameengine.getGlobalBase('PlayerStub').doOnOthersBase(
            [reply.leaderGbId],
            'onLeagueNewApplyNotify',
            (_apply, ),
            None,
            '',
            ())

    def _newApplyToFixedDict(self, n):
        if not n:
            return {
                'guildUUID': 0,
                'guildName': '',
                'guildIcon': 0,
                'dspFlag':   0,
                'power':     0,
                'applyTime': 0,
            }
        else:
            return {
                'guildUUID': n.guildUUID,
                'guildName': n.guildName,
                'guildIcon': n.guildIcon,
                'dspFlag':   n.dspFlag,
                'power':     n.power,
                'applyTime': n.applyTime,
            }

    def onNewInviteNotify(self, reply):
        """联盟新邀请通知:将 reply(AllianceInviteInfo) 转为 dict 后路由到目标帮会,
        由 Guild.onNewInviteNotify 转发给帮主客户端。
        """
        _invite = self._inviteToSingleFixedDict(reply)
        _targetGuildId = reply.guildId
        if not _targetGuildId:
            LOG_WARN('AllianceStub onNewInviteNotify: missing guildId in reply', _invite)
            return
        gameengine.getGlobalBase('GuildStub').callOnGuild(_targetGuildId, 'onNewInviteNotify', (_invite,), None, '', ())

    def checkGuildExists(self, reply):
        gameengine.getGlobalBase('GuildStub').checkGuildExists(reply.guildId, reply.uuid, reply.checkCD)

    def checkGuildSimpleInfo(self, request):
        _guildId = request.guildId
        _uuid = request.uuid

        gameengine.getGlobalBase('GuildStub').callOnGuild(_guildId, 'getGuildSimpleInfo', (self, 'onGetGuildSimpleInfoResultAsync', (0, _uuid)), self, 'onGetGuildSimpleInfoResultAsync', ({}, 1, _uuid))


    def onGetGuildSimpleInfoResultAsync(self, info, errCode, _uuid):
        _result = GetGuildSimpleInfoResult()
        _result.uuid = _uuid
        _result.errCode = errCode
        if errCode == 0:
            _result.info.guildId = info['guildId']
            _result.info.guildName = info['guildName']
            _result.info.guildIcon = info['guildIcon']
            _result.info.dspFlag = info['dspFlag']
            _result.info.score = info['score']
            _result.info.guildLevel = info['guildLevel']
            _result.info.memberCnt = info['memberCnt']
            
        _client = self.getRandomClient()
        if _client:
            _client.asStub.onCheckGuildSimpleInfoResult(None, _result, None)

    def onApplyToJoinResult(self, reply):
        _cache = self.remoteCallCache.pop(reply.uuid, None)
        if not _cache:
            return
        _cache.get('box').onApplyLeagueToJoinResult(reply.errCode, reply.allianceId, reply.allianceName, reply.alliancePower)
    
    def onReturnGuildFundNotify(self, reply):
        gameengine.getGlobalBase('GuildStub').callOnGuild(reply.guildId, 'onReturnBackFund', (reply.srcType, reply.itemType, reply.itemNum), None, '', ())
    
    def onGuildAidResourceNotify(self, reply):
        gameengine.getGlobalBase('GuildStub').callOnGuild(reply.guildId, 'onGuildAidResource', (reply.srcType, reply.itemType, reply.itemNum), None, '', ())
    
    def onLeagueGuildLeave(self, reply):
        for guildId in reply.memberGuildIds:
            gameengine.getGlobalBase('GuildStub').callOnGuild(guildId, 'onLeagueGuildLeave', (reply.guildId, guildId), None, '', ())

    def onLeagueDisband(self, reply):
        for guildId in reply.memberGuildIds:
            gameengine.getGlobalBase('GuildStub').callOnGuild(guildId, 'onSetLeagueUUID', (0,), None, '', ())

    def onLeagueGuildEventNotify(self, reply):
        guildId = reply.guildId
        messageId = reply.messageId
        messageArgs = []
        for messageArg in reply.messageArgs:
            messageArgs.append(messageArg)
        gameengine.getGlobalBase('GuildStub').callOnGuild(guildId, 'addGuildEvent', (messageId, messageArgs), None, '', ())

    def onLeagueGuildMessageNotify(self, reply):
        guildId = reply.guildId
        messageId = reply.messageId
        messageArgs = []
        for messageArg in reply.messageArgs:
            messageArgs.append(messageArg)
        gameengine.getGlobalBase('GuildStub').callOnGuild(guildId, 'broadcastMsg', (messageId, messageArgs), None, '', ())

    def onLeagueBroadCastMessageNotify(self, reply):
        messageId = reply.messageId
        messageArgs = []
        for messageArg in reply.messageArgs:
            messageArgs.append(messageArg)
        gameengine.broadcastBaseapp(
                    'broadcastToAllAvatar',
                    (
                        gameconst.BASE,
                        'onMessagePre',
                        (messageId, messageArgs),
                        (),
                    )
                )
    
    def onRecruitLeagueMemberResult(self, reply):
        _cache = self.remoteCallCache.pop(reply.uuid, None)
        if not _cache:
            return
        _cache.get('box').onRecruitLeagueMemberResult(reply.errCode, reply.leagueUUID)

    def onCheckLeaveGuildResult(self, reply):
        _cache = self.remoteCallCache.pop(reply.uuid, None)
        if not _cache:
            return
        gameengine.getGlobalBase('GuildStub').callOnGuild(reply.guildId, 'exitGuildDone', (reply.ret, reply.playerGbId, _cache.get('box')), None, '', ())

    def onQueryLeagueUUIDResult(self, reply):
        _cache = self.remoteCallCache.pop(reply.uuid, None)
        if not _cache:
            return
        gameengine.getGlobalBase('GuildStub').callOnGuild(reply.guildId, 'onQueryLeagueUUID', (reply.leagueUUID, reply.ret), None, '', ())

    # ---- Broadcast Converter ----
    def _warEnemyToFixedDict(self, b):
        if not b:
            return {
                'attackType': 0,
                'attackId': 0,
                'attackServerId': 0,
                'targetType': 0,
                'targetId': 0,
                'targetServerId': 0,
                'endTime': 0,
            }
        else:
            return {
                'attackType': b.attackType,
                'attackId': b.attackId,
                'attackServerId': b.attackServerId,
                'targetType': b.targetType,
                'targetId': b.targetId,
                'targetServerId': b.targetServerId,
                'endTime': b.endTime,
            }

    def _warEndedToFixedDict(self, b):
        if not b:
            return {
                'attackType': 0,
                'attackId': 0,
                'targetType': 0,
                'targetId': 0,
            } 
        else:
            return {
                'attackType': b.attackType,
                'attackId': b.attackId,
                'targetType': b.targetType,
                'targetId': b.targetId,
            }

    # ---- Data Converters ----
    def _entryToFixedDict(self, e):
        # AllianceListEntry → dict;
        # 联盟基础信息 + members(帮会级简版:guildId/guildName/guildIcon/
        # dspFlag/serverId/score)
        _members = []
        for _m in e.members:
            _members.append({
                'guildId': _m.guildId,
                'guildName': _m.guildName,
                'guildIcon': _m.guildIcon,
                'dspFlag': _m.dspFlag,
                'serverId': _m.serverId,
                'score': _m.score,
            })
        return {
            'allianceId': e.allianceId,
            'name': e.name,
            'serverId': e.serverId,
            'members': _members,
        }

    def _sentToFixedDict(self, a):
        return {
            'leagueUUID': a.allianceId,
            'leagueName': a.allianceName,
            'serverId': a.serverId,
            'power': a.totalScore,
            'sendTime': a.createdAt,
        }
    
    def _applyToFixedDict(self, a):
        # AllianceApplyInfo → dict;
        # leaderGuildId 由 allianceService 推送时填上(供 game server 路由到盟主帮会)
        # 当前 proto 中该字段可能尚未扩展,用 getattr 兜底,扩展后即生效
        return {
            'guildUUID': a.guildId,
            'guildName': a.guildName,
            'guildIcon': a.guildIcon,
            'dspFlag': a.dspFlag,
            'power': a.guildScore,
            'applyTime': a.createdAt,
        }

    def _inviteToFixedDict(self, i):
        invites = []
        for invite in i.invites:
            d = {
                'leagueUUID': invite.allianceId,
                'leagueName': invite.allianceName,
                'power': invite.power,
            }
            members = []
            for member in invite.members:
                e = {
                    'guildUUID': member.guildUUID,
                    'guildName': member.guildName,
                    'guildIcon': member.guildIcon,
                    'dspFlag': member.dspFlag,
                }
                members.append(e)
            d['members'] = members
            invites.append(d)
        return invites

    def _inviteToSingleFixedDict(self, i):
        d = {
            'leagueUUID': i.allianceId,
            'leagueName': i.allianceName,
            'power': i.power,
        }
        members = []
        for member in i.members:
            e = {
                'guildUUID': member.guildUUID,
                'guildName': member.guildName,
                'guildIcon': member.guildIcon,
                'dspFlag': member.dspFlag,
            }
            members.append(e)
        d['members'] = members
        return d

    def _enemyToFixedDict(self, e):
        return {
            'guildId': e.guildId,
            'endTime': e.endTime,
        }
    
    def _enemyRowToFixedDict(self, e):
        return {
            'attackId': e.attackId,
            'attackType': e.attackType,
            'attackServerId': e.attackServerId,
            'targetId': e.targetId,
            'targetType': e.targetType,
            'targetServerId': e.targetServerId,
            'endTime': e.endTime,
        }
    
    def _unionToFixedDict(self, e):
        return {
            'guildId': e.guildId,
        }

    def _eventToFixedDict(self, e):
        eventArgs = []
        for eventArg in e.eventArgs:
            eventArgs.append(eventArg)
        return {
            'eventId': e.eventId,
            'eventType': e.eventType,
            'eventArgs': eventArgs,
            'createdAt': e.createdAt,
        }

    def _chatMsgToFixedDict(self, m):
        return {
            'senderGuildId': m.senderGuildId,
            'senderGuildName': m.senderGuildName,
            'senderServerId': m.senderServerId,
            'content': m.content,
            'sendTime': m.sendTime,
        }

    def _detailToFixedDict(self, d):
        if not d:
            return {
                'allianceId': 0,
                'name': '',
                'declaration': '',
                'approveType': 0,
                'leaderGuildId': 0,
                'leaderGuildName': '',
                'leaderServerId': 0,
                'totalScore': 0,
                'memberCount': 0,
                'fund': 0,
                'leaderGbId': 0,
                'leaderName': '',
                'leaderLevel': 0,
                'leaderProfession': 0,
                'leaderGender': 0,
                'createdAt': 0,
                'serverId': 0,
            }
        else:
            return {
                'allianceId': d.allianceId,
                'name': d.name,
                'declaration': d.declaration,
                'approveType': d.approveType,
                'leaderGuildId': d.leaderGuildId,
                'leaderGuildName': d.leaderGuildName,
                'leaderServerId': d.leaderServerId,
                'totalScore': d.totalScore,
                'memberCount': d.memberCount,
                'fund': d.fund,
                'leaderGbId': d.leaderGbId,
                'leaderName': d.leaderName,
                'leaderLevel': d.leaderLevel,
                'leaderProfession': d.leaderProfession,
                'leaderGender': d.leaderGender,
                'createdAt': d.createdAt,
                'serverId': d.serverId,
            }

    def _memberToFixedDict(self, members):
        if not members:
            return []
        else:
            datas = []
            for member in members:
                datas.append(self._memberToFixedDictWithSingle(member))
        return datas
    
    def _memberToFixedDictWithSingle(self, member):
        if not member:
            return {
                    'guildId': 0,
                    'guildName': '',
                    'guildScore': 0,
                    'serverId': 0,
                    'joinTime': 0,
                    'memberCount': 0,
                    'maxMemberNum': 0,
                    'dspFlag': 0,
                    'guildIcon': 0,
                    'guildLevel': 0,
                    'role': 0,
                }
        else:
            return {
                    'guildId': member.guildId,
                    'guildName': member.guildName,
                    'guildScore': member.guildScore,
                    'serverId': member.serverId,
                    'joinTime': member.joinTime,
                    'memberCount': member.memberCount,
                    'maxMemberNum': member.maxMemberNum,
                    'dspFlag': member.dspFlag,
                    'guildIcon': member.guildIcon,
                    'guildLevel': member.guildLevel,
                    'role': member.role,
                }
    