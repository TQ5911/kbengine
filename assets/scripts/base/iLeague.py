# coding: utf-8
from KBEDebug import *
import utils
import gameengine
import gameconfig
import gameconst
import gamedecorator

import guild_guildConst as G_GCD
import agent_agentFunction as A_AFD
import AuthClsWraper
import GuildStub

class ILeague:
    def _inGuild(self):
        ret = self.guildUUIDBase > 0 and self.guildBox is not None
        if not ret:
           LOG_ERR('iLeague::申请联盟先加入帮会 ', self.gbID)
           self.client.onLeagueOpResult(gameconst.LeagueOpResult.NOT_IN_GUILD)
        return ret
    # ---- Core (forward to guild) ----
    @gamedecorator.checkGameconfigEnable('guild_union')
    def createLeague(self, exposed, name, declaration, approveType):
        LOG_INFO('iLeague::createLeague', exposed, name, self.gbID)
        if not self._inGuild():
            return
        if approveType not in gameconst.LeagueOpType.VALID_TYPES:
            self.client.onLeagueOpResult(gameconst.LeagueOpResult.INVALID_OP_TYPE)
            return
        nameMin = G_GCD.datas['guild_unionNameMinLength']['value']
        nameMax = G_GCD.datas['guild_unionNameMaxLength']['value']
        nameLen = len(name)
        if not (nameMin <= nameLen <= nameMax):
            self.client.onLeagueOpResult(gameconst.LeagueOpResult.LEAGUE_NAME_TOO_LONG)
            LOG_ERR("iLeague::createLeague: len(name) > nameLen.", nameLen)
            return
        declarationLimit = G_GCD.datas['guild_unionCreedMaxLength']['value']
        declarationLen = len(declaration)
        if not (declarationLen <= declarationLimit):
            self.client.onLeagueOpResult(gameconst.LeagueOpResult.LEAGUE_DECALATION_TOO_LONG)
            LOG_ERR("iLeague::createLeague: len(declaration) > declarationLimit.", declarationLimit)
            return
        self.guildBox.onCreateLeague(self.gbID, name, declaration, approveType, self)

    @gamedecorator.checkGameconfigEnable('guild_union')
    def disbandLeague(self, exposed):
        LOG_INFO('iLeague::disbandLeague', exposed, self.gbID)
        if not self._inGuild():
            return
        self.guildBox.onDisbandLeague(self.gbID, self)

    @gamedecorator.checkGameconfigEnable('guild_union')
    def modifyLeagueInfo(self, exposed, name=None, declaration=None, approveType=None):
        LOG_INFO('iLeague::modifyLeagueInfo', exposed, self.gbID)
        if not self._inGuild():
            return
        self.guildBox.onModifyLeagueInfo(self.gbID, name, declaration, approveType, self)

    @gamedecorator.checkGameconfigEnable('guild_union')
    def getLeagueList(self, exposed, pageIndex):
        LOG_INFO('iLeague::getLeagueList', exposed, pageIndex, self.gbID)
        if not self._inGuild():
            return
        self.guildBox.onGetLeagueList(self.gbID, pageIndex, 5, self)

    @gamedecorator.checkGameconfigEnable('guild_union')
    def searchLeague(self, exposed, keyword):
        LOG_INFO('iLeague::searchLeague', exposed, keyword, self.gbID)
        if not self._inGuild():
            return
        self.guildBox.onSearchLeague(self.gbID, keyword, self)

    @gamedecorator.checkGameconfigEnable('guild_union')
    def getLeagueBasicInfo(self, exposed, allianceId):
        LOG_INFO('iLeague::getLeagueBasicInfo', exposed, allianceId, self.gbID)
        if not self._inGuild():
            return
        self.guildBox.onGetLeagueBasicInfo(self.gbID, allianceId, self)

    @gamedecorator.checkGameconfigEnable('guild_union')
    def getLeagueSimpleInfo(self, exposed, allianceId):
        LOG_INFO('iLeague::getLeagueSimpleInfo', exposed, allianceId, self.gbID)
        if not self._inGuild():
            return
        self.guildBox.onGetLeagueSimpleInfo(self.gbID, allianceId, self)

    @gamedecorator.checkGameconfigEnable('guild_union')
    def getGuildSimpleInfo(self, exposed, guildId, serverId):
        LOG_INFO('iLeague::getGuildSimpleInfo', exposed, guildId, serverId, self.gbID)
        if not self._inGuild():
            return
        if serverId == gameconfig.serverId():
            gameengine.getGlobalBase('GuildStub').callOnGuild(guildId, 'getGuildSimpleInfo', (self, 'onGetGuildSimpleInfoResult', (0,)), self, 'onGetGuildSimpleInfoResult', ({},1))
        else:
            gameengine.getGlobalBase('AllianceStub').getGuildSimpleInfo(guildId, serverId, self)

    @gamedecorator.checkGameconfigEnable('guild_union')
    def getLeagueDetail(self, exposed, allianceId):
        LOG_INFO('iLeague::getLeagueDetail', exposed, allianceId, self.gbID)
        if not self._inGuild():
            return
        self.guildBox.onGetLeagueDetail(self.gbID, allianceId, self)

    @gamedecorator.checkGameconfigEnable('guild_union')
    def getLeagueDetailByGuild(self, exposed, guildId):
        LOG_INFO('iLeague::getLeagueDetailByGuild', exposed, guildId, self.gbID)
        if not self._inGuild():
            return
        self.guildBox.onGetLeagueDetailByGuild(self.gbID, guildId, self)

    # ---- Member (forward to guild) ----
    @gamedecorator.checkGameconfigEnable('guild_union')
    def applyLeagueToJoin(self, exposed, allianceId):
        LOG_INFO('iLeague::applyLeagueToJoin', exposed, allianceId, self.gbID)
        if not self._inGuild():
            return
        self.guildBox.onApplyLeagueToJoin(self.gbID, allianceId, self)

    @gamedecorator.checkGameconfigEnable('guild_union')
    def approveLeagueJoin(self, exposed, guildId):
        LOG_INFO('iLeague::approveLeagueJoin', exposed, guildId, self.gbID)
        if not self._inGuild():
            return
        self.guildBox.onApproveLeagueJoin(self.gbID, guildId, self)

    @gamedecorator.checkGameconfigEnable('guild_union')
    def rejectLeagueJoin(self, exposed, guildId):
        LOG_INFO('iLeague::rejectLeagueJoin', exposed, guildId, self.gbID)
        if not self._inGuild():
            return
        self.guildBox.onRejectJoin(self.gbID, guildId, self)

    @gamedecorator.checkGameconfigEnable('guild_union')
    def cancelLeagueApply(self, exposed, leagueUUID):
        LOG_INFO('iLeague::cancelLeagueApply', exposed, leagueUUID, self.gbID)
        if not self._inGuild():
            return
        self.guildBox.onCancelLeagueApply(self.gbID, leagueUUID, self)

    @gamedecorator.checkGameconfigEnable('guild_union')
    def inviteLeagueGuild(self, exposed, targetGuildId, targetServerId):
        LOG_INFO('iLeague::inviteLeagueGuild', exposed, targetGuildId, targetServerId, self.gbID)
        if not self._inGuild():
            return
        self.guildBox.onInviteGuild(self.gbID, targetGuildId, targetServerId, self)

    @gamedecorator.checkGameconfigEnable('guild_union')
    def acceptLeagueInvite(self, exposed, allianceId):
        LOG_INFO('iLeague::acceptLeagueInvite', exposed, allianceId, self.gbID)
        if not self._inGuild():
            return
        self.guildBox.onAcceptInvite(self.gbID, allianceId, self)

    @gamedecorator.checkGameconfigEnable('guild_union')
    def rejectLeagueInvite(self, exposed, leagueUUID):
        LOG_INFO('iLeague::rejectLeagueInvite', exposed, leagueUUID, self.gbID)
        if not self._inGuild():
            return
        self.guildBox.onRejectInvite(self.gbID, leagueUUID, self)

    @gamedecorator.checkGameconfigEnable('guild_union')
    def kickLeagueMember(self, exposed, allianceId, targetGuildId):
        LOG_INFO('iLeague::kickLeagueMember', exposed, allianceId, targetGuildId, self.gbID)
        if not self._inGuild():
            return
        self.guildBox.onKickMember(self.gbID, allianceId, targetGuildId, self)

    @gamedecorator.checkGameconfigEnable('guild_union')
    def leaveLeague(self, exposed):
        LOG_INFO('iLeague::leaveLeague', exposed, self.gbID)
        if not self._inGuild():
            return
        self.guildBox.onLeaveLeague(self.gbID, self)

    @gamedecorator.checkGameconfigEnable('guild_union')
    def transferLeagueLeader(self, exposed, targetGuildId):
        LOG_INFO('iLeague::transferLeagueLeader', exposed, targetGuildId, self.gbID)
        if not self._inGuild():
            return
        self.guildBox.onTransferLeader(self.gbID, targetGuildId, self)

    @gamedecorator.checkGameconfigEnable('guild_union')
    def getLeagueApplyList(self, exposed):
        LOG_INFO('iLeague::getLeagueApplyList', exposed, self.gbID)
        if not self._inGuild():
            return
        self.guildBox.onGetLeagueApplyList(self.gbID, self)

    @gamedecorator.checkGameconfigEnable('guild_union')
    def getLeagueInviteList(self, exposed):
        LOG_INFO('iLeague::getLeagueInviteList', exposed, self.gbID)
        if not self._inGuild():
            return
        self.guildBox.onGetInviteList(self.gbID, self)

    @gamedecorator.checkGameconfigEnable('guild_union')
    def getLeagueSentApplies(self, exposed):
        LOG_INFO('iLeague::getLeagueSentApplies', exposed, self.gbID)
        if not self._inGuild():
            return
        self.guildBox.onGetLeagueSentApplies(self.gbID, self)

    # ---- Diplomacy (forward to guild) ----
    @gamedecorator.checkGameconfigEnable('guild_union')
    def declareLeagueWar(self, exposed, attackType, targetType, targetId, targetServerId):
        LOG_INFO('iLeague::declareLeagueWar', exposed, attackType, targetType, targetId, targetServerId, self.gbID)
        if not self._inGuild():
            return
        if attackType not in gameconst.EnemyActionType.VALID_TYPES or targetType not in gameconst.EnemyActionType.VALID_TYPES:
            LOG_ERR('iLeague::declareLeagueWar, wrong args', exposed, attackType, targetType, targetId, targetServerId, self.gbID)
            return
        
        #// 注意！！！非同个服务器的联盟宣战，暂时禁止
        if gameconfig.serverId() != targetServerId:
            LOG_WARN('iLeague::declareLeagueWar, not same server id', gameconfig.serverId(), targetServerId)
            self.client.onMessage(G_GCD.datas['guild_crossServerDeclareLimit']['value'], [])
            return
        
        self.guildBox.onDeclareLeagueWar(self.gbID, attackType, targetType, targetId, targetServerId, self)

    @gamedecorator.checkGameconfigEnable('guild_union')
    def getLeagueEnemyList(self, exposed):
        LOG_INFO('iLeague::getLeagueEnemyList', exposed, self.gbID)
        if not self._inGuild():
            return
        self.guildBox.onGetEnemyList(self.gbID, self.guildUUIDBase, self)

    @gamedecorator.checkGameconfigEnable('guild_union')
    def getLeagueEnemyAllianceList(self, exposed):
        LOG_INFO('iLeague::getLeagueEnemyAllianceList', exposed, self.gbID)
        if not self._inGuild():
            return
        self.guildBox.onGetEnemyAllianceList(self.gbID, self)

    @gamedecorator.checkGameconfigEnable('guild_union')
    def getLeagueUnionList(self, exposed):
        LOG_INFO('iLeague::getLeagueUnionList', exposed, self.gbID)
        if not self._inGuild():
            return
        self.guildBox.onGetUnionList(self.gbID, self.guildUUIDBase, self)

    @gamedecorator.checkGameconfigEnable('guild_union')
    def checkLeagueRelation(self, exposed, guildId1, guildId2):
        LOG_INFO('iLeague::checkLeagueRelation', exposed, guildId1, guildId2, self.gbID)
        if not self._inGuild():
            return
        self.guildBox.onCheckLeagueRelation(self.gbID, guildId1, guildId2, self)

    @gamedecorator.checkGameconfigEnable('guild_union')
    def getGuildAllianceId(self, exposed, guildId):
        LOG_INFO('iLeague::getGuildAllianceId', exposed, guildId, self.gbID)
        if not self._inGuild():
            return
        self.guildBox.onGetGuildAllianceId(self.gbID, guildId, self)

    # ---- Resource (forward to guild) ----
    @gamedecorator.checkGameconfigEnable('guild_union')
    def donateLeagueFund(self, exposed, amount):
        LOG_INFO('iLeague::donateLeagueFund', exposed, amount, self.gbID)
        if not self._inGuild():
            return
        if amount <= 0:
            return
        self.guildBox.onDonateFund(self.gbID, amount, self)

    @gamedecorator.checkGameconfigEnable('guild_union')
    def aidLeagueResource(self, exposed, toGuildId, amount):
        LOG_INFO('iLeague::aidLeagueResource', exposed, toGuildId, amount, self.gbID)
        if not self._inGuild():
            return
        if amount <= 0:
            return
        self.guildBox.onAidResource(self.gbID, toGuildId, amount, self)

    @gamedecorator.checkGameconfigEnable('guild_union')
    def getLeagueFund(self, exposed, allianceId):
        LOG_INFO('iLeague::getLeagueFund', exposed, allianceId, self.gbID)
        if not self._inGuild():
            return
        self.guildBox.onGetLeagueFund(self.gbID, allianceId, self)

    @gamedecorator.checkGameconfigEnable('guild_union')
    def getLeagueEventList(self, exposed):
        LOG_INFO('iLeague::getLeagueEventList', exposed, self.gbID)
        if not self._inGuild():
            return
        self.guildBox.onGetEventList(self.gbID, self)

    @gamedecorator.checkGameconfigEnable('guild_union')
    def recruitLeagueMember(self, exposed):
        LOG_INFO('iLeague::recruitLeagueMember', exposed, self.gbID)
        if not self._inGuild():
            return
        self.guildBox.onRecruitLeagueMember(self.gbID, self)

    def onModifyLeagueInfoResult(self, errCode):
        LOG_INFO('iLeague::onModifyLeagueInfoResult', errCode, self.gbID)
        if errCode == 0:
            self.client.onModifyLeagueInfoSuccess()
        else:
            self.client.onLeagueOpResult(gameconst.LeagueOpResult.MODIFY_LEAGUE_INFO_FAIL)

    def onApplyLeagueToJoinResult(self, errCode, allianceId, allianceName, alliancePower):
        LOG_INFO('iLeague::onApplyLeagueToJoinResult', errCode, allianceId, allianceName, alliancePower, self.gbID)
        if errCode == gameconst.LeagueErrCode.ErrCodeSuccess:
            self.client.onApplyLeagueSuccess(allianceId, allianceName, alliancePower)
        else:
            if errCode == gameconst.LeagueErrCode.ErrCodeGuildInWar:
                self.client.onMessage(G_GCD.datas['guild_unionJoinLimit3']['value'], [])
            self.client.onLeagueOpResult(gameconst.LeagueOpResult.APPLY_LEAGUE_FAIL)

    def onApproveLeagueJoinResult(self, errCode, joinedGuildId, guildCD):
        LOG_INFO('iLeague::onApproveLeagueJoinResult', errCode, joinedGuildId, self.gbID, guildCD)
        if errCode == 0:
            self.client.onLeagueOpResult(gameconst.LeagueOpResult.APPROVE_LEAGURE_SUCCESS)
        else:
            if errCode == gameconst.LeagueErrCode.ErrCodeGuildNotFound:
                if guildCD > 0:
                    self.client.onMessage(G_GCD.datas['guild_unionExitLimit2']['value'], [str(guildCD)])
                else:
                    self.client.onMessage(G_GCD.datas['guild_dismissed']['value'], [str(guildCD)])
            else:
                self.client.onLeagueOpResult(gameconst.LeagueOpResult.APPROVE_LEAGURE_FAIL)
        self.client.onApproveLeagueJoinResult(joinedGuildId)

    def onRejectLeagueJoinResult(self, errCode, rejectedGuildUUID):
        LOG_INFO('iLeague::onRejectLeagueJoinResult', errCode, self.gbID, rejectedGuildUUID)
        if errCode != 0:
            self.client.onLeagueOpResult(gameconst.LeagueOpResult.REJECT_LEAGURE_FAIL)
        self.client.onRejectLeagueJoinResult(rejectedGuildUUID)

    def onCancelLeagueApplyResult(self, errCode, leagueUUID):
        LOG_INFO('iLeague::onCancelLeagueApplyResult', errCode, self.gbID, leagueUUID)
        if errCode != 0:
            self.client.onLeagueOpResult(gameconst.LeagueOpResult.CANCEL_LEAGURE_FAIL)
        self.client.onCancelLeagueApplyResult(leagueUUID)
        
    def onInviteGuildResult(self, errCode, guildId, guildCD):
        LOG_INFO('iLeague::onInviteGuildResult', errCode, self.gbID, guildId, guildCD)
        if errCode == gameconst.LeagueErrCode.ErrCodeSuccess or errCode == gameconst.LeagueErrCode.ErrCodeAlreadyInvited:
            self.client.onMessage(G_GCD.datas['guildInviteCooldownMsg']['value'], [])
        else:
            if errCode == gameconst.LeagueErrCode.ErrCodeGuildNotFound:
                if guildCD > 0:
                    self.client.onMessage(G_GCD.datas['guild_unionExitLimit2']['value'], [str(guildCD)])
            elif errCode == gameconst.LeagueErrCode.ErrCodeGuildInWar:
                self.client.onMessage(G_GCD.datas['guild_unionJoinLimit3']['value'], [])
            self.client.onLeagueOpResult(gameconst.LeagueOpResult.LEAGUE_INVITE_FAIL)
        
        self.client.onInviteGuildResult(guildId)

    def onAcceptLeagueInviteResult(self, errCode, leagueUUID):
        LOG_INFO('iLeague::onAcceptLeagueInviteResult', errCode, self.gbID, leagueUUID)
        if errCode != 0:
            self.client.onLeagueOpResult(gameconst.LeagueOpResult.ACCEPT_LEAGUE_INVITE_FAIL)
        self.client.onAcceptLeagueInviteResult(leagueUUID)

    def onRejectLeagueInviteResult(self, errCode, leagueUUID):
        LOG_INFO('iLeague::onRejectLeagueInviteResult', errCode, self.gbID, leagueUUID)
        if errCode != 0:
            self.client.onLeagueOpResult(gameconst.LeagueOpResult.REJECT_LEAGUE_INVITE_FAIL)
        self.client.onRejectLeagueInviteResult(leagueUUID)

    def onKickMemberResult(self, errCode):
        LOG_INFO('iLeague::onKickMemberResult', errCode, self.gbID)

    def onLeaveLeagueResult(self, errCode):
        LOG_INFO('iLeague::onLeaveLeagueResult', errCode, self.gbID)
        if errCode == gameconst.LeagueErrCode.ErrCodeYouAreLeader:
            self.client.onMessage(G_GCD.datas['guild_presidentLeave2']['value'], [])
            
    def onTransferLeagueLeaderResult(self, errCode, data):
        LOG_INFO('iLeague::onTransferLeagueLeaderResult', errCode, self.gbID)
        self.client.onTransferLeagueLeaderResult(data)

    def onDeclareWarResult(self, errCode, endTime):
        LOG_INFO('iLeague::onDeclareWarResult', errCode, endTime, self.gbID)
        if errCode != gameconst.LeagueErrCode.ErrCodeSuccess:
            if errCode == gameconst.LeagueErrCode.ErrCodeAllianceNotFound:
                self.client.onMessage(G_GCD.datas['guild_unionDismissed']['value'], [])
            elif errCode == gameconst.LeagueErrCode.ErrCodeGuildNotFound:
                self.client.onMessage(G_GCD.datas['guild_dismissed']['value'], [])
            elif errCode == gameconst.LeagueErrCode.ErrCodeInsufficientFund:
                self.client.onMessage(G_GCD.datas['guild_unionNoFund']['value'], [])
            elif errCode == gameconst.LeagueErrCode.ErrCodeDifferentServerInDeclareWarIsForbidden:
                self.client.onMessage(G_GCD.datas['guild_crossServerDeclareLimit']['value'], [])
            else:
                self.client.onLeagueOpResult(gameconst.LeagueOpResult.DECLARE_WAR_FAIL)

    def onLeagueDonateFundResult(self, errCode, allianceId, allianceFund):
        LOG_INFO('iLeague::onLeagueDonateFundResult', errCode, allianceId, allianceFund, self.gbID)
        if errCode == gameconst.LeagueErrCode.ErrCodeSuccess:
            self.client.onMessage(G_GCD.datas['guild_unionDonateFund']['value'], [])
        else:
            self.client.onLeagueOpResult(gameconst.LeagueOpResult.DONATE_LEAGUE_FUND_FAIL)
        self.client.onLeagueDonateFundResult(allianceId, allianceFund)

    def onAidResourceResult(self, errCode):
        LOG_INFO('iLeague::onAidResourceResult', errCode, self.gbID)

    def onLeagueFundResult(self, fund):
        LOG_INFO('iLeague::onLeagueFundResult', fund, self.gbID)
        self.client.onLeagueFundResult(fund)

    def onSendChatMessageResult(self, errCode):
        LOG_INFO('iLeague::onSendChatMessageResult', errCode, self.gbID)

    # ---- List/Query result handlers (AllianceStub → avatar → client) ----
    def onLeagueListResult(self, entries, pageIndex, totalPage):
        LOG_INFO('iLeague::onLeagueListResult', len(entries), pageIndex, totalPage)
        self.client.onLeagueListResult(entries, pageIndex, totalPage)

    def onSearchLeagueResult(self, entries):
        LOG_INFO('iLeague::onSearchLeagueResult', len(entries) if entries else 0, self.gbID)
        self.client.onSearchLeagueResult(entries)

    def onLeagueDetailResult(self, alliance, members, errCode):
        LOG_INFO('iLeague::onLeagueDetailResult', errCode, self.gbID)
        self.client.onLeagueDetailResult(alliance, members)

    def onGetLeagueBasicInfoResult(self, info, errCode):
        """独立接口: 根据 allianceId 拉取联盟基础信息(declaration + approval + 盟主身份).
        info 为 None 表示 allianceService 找不到该 allianceId.
        """
        LOG_INFO('iLeague::onGetLeagueBasicInfoResult', errCode, self.gbID)
        self.client.onGetLeagueBasicInfoResult(info)

    def onGetLeagueSimpleInfoResult(self, info, errCode):
        LOG_INFO('iLeague::onGetLeagueSimpleInfoResult', errCode, self.gbID)
        self.client.onGetLeagueSimpleInfoResult(info)

    def onGetGuildSimpleInfoResult(self, info, errCode):
        LOG_INFO('iLeague::onGetGuildSimpleInfoResult', errCode, self.gbID)
        self.client.onGetGuildSimpleInfoResult(info)

    def onLeagueApplyListResult(self, applies):
        LOG_INFO('iLeague::onLeagueApplyListResult', len(applies), self.gbID)
        self.client.onLeagueApplyListResult(applies)

    def onInviteListResult(self, invites):
        LOG_INFO('iLeague::onInviteListResult', len(invites), self.gbID)
        self.client.onLeagueInviteListResult(invites)

    def onLeagueSentAppliesResult(self, applies):
        LOG_INFO('iLeague::onLeagueSentAppliesResult', len(applies), self.gbID)
        self.client.onLeagueSentAppliesResult(applies)

    def onLeagueEnemyList(self, enemies):
        LOG_INFO('iLeague::onLeagueEnemyList', len(enemies), self.gbID)
        self.client.onLeagueEnemyList(enemies)
    
    def onLeagueEnemyAllianceList(self, enemies):
        LOG_INFO('iLeague::onLeagueEnemyAllianceList', len(enemies), self.gbID)
        self.client.onLeagueEnemyAllianceList(enemies)

    def onLeagueUnionList(self, leagueUUIDs):
        LOG_INFO('iLeague::onLeagueUnionList', leagueUUIDs, len(leagueUUIDs), self.gbID)
        self.client.onLeagueUnionList(leagueUUIDs)

    def onCheckLeagueRelationResult(self, isSameAlliance, allianceId):
        LOG_INFO('iLeague::onCheckLeagueRelationResult', isSameAlliance, allianceId, self.gbID)
        self.client.onCheckLeagueRelationResult(isSameAlliance, allianceId)

    def onGetGuildAllianceResult(self, allianceId, errCode):
        LOG_INFO('iLeague::onGetGuildAllianceResult', allianceId, errCode, self.gbID)
        self.client.onGetGuildAllianceResult(allianceId)

    def onEventListResult(self, events):
        LOG_INFO('iLeague::onEventListResult', len(events) if events else 0, self.gbID)
        self.client.onEventListResult(events)

    def onChatHistoryResult(self, messages):
        LOG_INFO('iLeague::onChatHistoryResult', len(messages) if messages else 0, self.gbID)
        self.client.onChatHistoryResult(messages)

    def onLeagueNewApplyNotify(self, applyInfo):
        LOG_INFO('iLeague::onLeagueNewApplyNotify', self.gbID)
        self.client.onLeagueNewApplyNotify(applyInfo)

    def onRecruitLeagueMemberResult(self, errCode, leagueUUID):
        LOG_INFO('iLeague::onRecruitLeagueMemberResult', self.gbID, errCode, leagueUUID)
