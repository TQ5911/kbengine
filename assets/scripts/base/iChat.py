# -*- coding: utf-8 -*-

import KBEngine
from KBEDebug import *

import utils
import gameengine
import gameconst
import gameglobal
import gamedecorator
import chatConfig_chatConfig as C_C_DD
import chatConfig_channel as CCCH
import teamMatch_matchConfig as TM_MCD
import teamMatch_activity as TMACTD
import message_Message_def as MMD
import raid_raidConst as RAID_CONST
import message_chatMessage as MCM
import activityControl_activityData as AC_ADD
import auction_auctionConst as AUT_CONST
import chatConfig_hornSet as CHS
import dropAward
import gameclass
import gametimer
import antiAddictCategory_antiAddictCategory_def as AAC_AACDD
import LogTrackingMgr
import gameconfig

class IChat(object):
    def chatOnLogin(self):
        self.updateChatForbiddenState(isGm=False)

    @gamedecorator.crossServer
    def setChatChannel(self, exposed, channel):
        LOG_INFO('setChatChannel', channel)
        if channel >= gameconst.ChatChannelEnum.MAX:
            return

        if self.hasChatChannel(channel):
            return

        _newChannel = self.chatChannel | (1 << channel)
        self.chatChannel = _newChannel

    @gamedecorator.crossServer
    def removeChatChannel(self, exposed, channel):
        LOG_INFO('removeChatChannel', channel)
        if channel >= gameconst.ChatChannelEnum.MAX:
            return

        if not self.hasChatChannel(channel):
            return

        _newChannel = self.chatChannel & (~(1 << channel))
        self.chatChannel = _newChannel

    def hasChatChannel(self, channel):
        if self.chatChannel & (1 << channel):
            return True
        else:
            return False

    def _deductHornItem(self, hornId):
        #减道具
        costItemId = CHS.datas[hornId]['cost']
        deductWealthVal = dropAward.DeductWealthVal()
        deductWealthVal.addWealthByItemId(costItemId, 1)

        res = self.canDeductWealth(deductWealthVal)
        if not res:
            LOG_WARN('sendPaidChatMsg: items not enough:', deductWealthVal, res())
            return False

        detail = gameclass.AwardDetailCls()
        opUUID = KBEngine.genUUID64()
        srcType = AAC_AACDD.datas.BONUS_SRC_COST_HORN
        return self.deductWealth(srcType, deductWealthVal, opUUID, detail)

    @gamedecorator.crossServer
    @gamedecorator.checkGameconfigEnable('chat')
    def sendPaidChatMsg(self, exposed, hornId, msg):
        LOG_DBG('sendPaidChatMsg', hornId, msg)
        if gameconfig.isCrossServer():
            self.syncMethodCallToLocalServerBase('_sendPaidChatMsg', (hornId, msg))
        else:
            self._sendPaidChatMsg(hornId, msg)


    def _sendPaidChatMsg(self, hornId, msg):
        LOG_DBG('_sendPaidChatMsg', hornId, msg)
        if self.isAllServerForbidChat():
            self.onMessagePre(int(C_C_DD.datas['chat_banned']['value']), [str(self.idipBanDict.get(gameconst.IDIPBanType.CHAT, 0))])
            return

        channel = CHS.datas[hornId]['showChannel'][0]
        now = utils.curTS()
        if now < self.sendPaidMsgTime + CHS.datas[hornId]['cd']:
            timeDelta = self.sendPaidMsgTime + CHS.datas[hornId]['cd']-now
            self.onMessagePre(int(C_C_DD.datas['hornMsgCdTip']['value']), [str(timeDelta)])
            return

        if not self._deductHornItem(hornId):
            return

        self.sendPaidMsgTime = now
        self.afterCheckPaidChatMsg(msg, hornId)

        self.syncMethodCallToCrossServerBase("onLocalServerPaidChatMsg", (hornId, msg))

        LogTrackingMgr.LogTrackingMgr.horn_msg(
            self.gbID,
            self.accountEntity.clientDistinctId,
            CHS.datas[hornId]['cost'],
            1,
            len(msg['msg'])
        )
        
    def onLocalServerPaidChatMsg(self, hornId, msg):
        if not self._deductHornItem(hornId):
            gameengine.panicStack('onLocalServerPaidChatMsg: deductHornItem failed', hornId)
        self.sendPaidMsgTime = utils.curTS()
        self.afterCheckPaidChatMsg(msg, hornId)

    def afterCheckPaidChatMsg(self, originalMsg, hornId):
        LOG_INFO("afterCheckPaidChatMsg", originalMsg, hornId)
        self.logChatMsg(originalMsg.get('msgType', 0), 0, gameconst.ChatChannelEnum.WORLD, originalMsg.get('msg',''), self.sendPaidMsgTime)
        baseApp = gameglobal.localBaseApp
        if baseApp:
            baseApp.addAvatarChatMsg(
                'trumpet',
                hornId,
                self._getChatChannelAvatarInfo(),
                originalMsg
            )

    @gamedecorator.crossServer
    @gamedecorator.checkGameconfigEnable('chat')
    def sendWorldChatMsg(self, exposed, msg):
        LOG_DBG('sendWorldChatMsg', msg)
        if self.isAllServerForbidChat():
            self.onMessagePre(int(C_C_DD.datas['chat_banned']['value']), [str(self.idipBanDict.get(gameconst.IDIPBanType.CHAT, 0))])
            return

        now = utils.curTS()
        if now < self.sendWorldMsgTime + CCCH.datas[gameconst.ChatChannelEnum.WORLD]['channelCD']:
            timeDelta = self.sendWorldMsgTime + CCCH.datas[gameconst.ChatChannelEnum.WORLD]['channelCD']-now
            self.onMessagePre(int(C_C_DD.datas['msgId_worldChannelCD']['value']), [str(timeDelta)])
            return

        if gameglobal.roleCache[self.id]['level'] < CCCH.datas[gameconst.ChatChannelEnum.WORLD]['channelMinLevel']:
            return

        self.sendWorldMsgTime = now
        self.afterCheckWorldChatMsg(msg)

    def afterCheckWorldChatMsg(self, originalMsg):
        LOG_DBG("afterCheckWorldChatMsg", originalMsg)
        self.logChatMsg(originalMsg.get('msgType', 0), 0, gameconst.ChatChannelEnum.WORLD, originalMsg.get('msg',''), self.sendWorldMsgTime)
        if self.isSilentChat(gameconst.SilentSpeakScene.ENUM_CHAT):
            self.client.onRecvAvatarChannelMsg(gameconst.ChatChannelEnum.WORLD, self._getChatChannelAvatarInfo(), originalMsg)
            return

        baseApp = gameglobal.localBaseApp
        if baseApp:
            baseApp.addAvatarChatMsg(
                'channel',
                gameconst.ChatChannelEnum.WORLD,
                self._getChatChannelAvatarInfo(),
                originalMsg
            )
        # self.checkAchievementTrigger(gameconst.AchieveTargetType.CHANNEL_SPEAK, gameconst.ChatChannelEnum.WORLD)

    @gamedecorator.crossServer
    @gamedecorator.checkGameconfigEnable('chat')
    def sendSiegeWarChatMsg(self, exposed, msg):
        LOG_DBG('sendSiegeWarChatMsg', msg)
        if self.isAllServerForbidChat():
            self.onMessagePre(int(C_C_DD.datas['chat_banned']['value']), [str(self.idipBanDict.get(gameconst.IDIPBanType.CHAT, 0))])
            return

        now = utils.curTS()
        if now < self.sendSiegeWarMsgTime + CCCH.datas[gameconst.ChatChannelEnum.SIEGE_WAR]['channelCD']:
            timeDelta = self.sendSiegeWarMsgTime + CCCH.datas[gameconst.ChatChannelEnum.SIEGE_WAR]['channelCD']-now
            self.onMessagePre(int(C_C_DD.datas['msgId_worldChannelCD']['value']), [str(timeDelta)])
            return

        self.sendSiegeWarMsgTime = now
        self.logChatMsg(msg.get('msgType', 0), 0, gameconst.ChatChannelEnum.SIEGE_WAR, msg.get('msg',''), self.sendSiegeWarMsgTime)
        gameengine.broadcastBaseapp('broadcastToAllAvatar',
                                    (gameconst.CELL, 'onSiegeWarChatMsg',
                                     (gameconst.ChatChannelEnum.SIEGE_WAR, self._getChatChannelAvatarInfo(), msg, self.cell), ()))

    @gamedecorator.crossServer
    @gamedecorator.checkGameconfigEnable('chat')
    @gamedecorator.forwardToLocal
    def sendGuildChatMsg(self, exposed, msg):
        LOG_DBG('sendGuildChatMsg', msg)
        if self.isAllServerForbidChat():
            self.onMessagePre(int(C_C_DD.datas['chat_banned']['value']), [str(self.idipBanDict.get(gameconst.IDIPBanType.CHAT, 0))])
            return

        self._sendMsgToGuild(msg,True)

    @gamedecorator.crossServer
    @gamedecorator.forwardToLocal
    @gamedecorator.checkGameconfigEnable('chat')
    @gamedecorator.checkGameconfigEnable('guild_union')
    def sendAllianceChatMsg(self, exposed, msg):
        """
        联盟频道发言入口(2026-08-24 联盟频道新增):
          链路: client -> iChat(local) -> Guild.onSendChatMessage
                -> AllianceStub.sendChatMessage -> central service
                -> 广播 ChatMessageBroadcast -> 所有 game server
                -> Guild.broadcastMemberClient -> 玩家客户端
        """
        LOG_DBG('sendAllianceChatMsg', msg)
        if self.isAllServerForbidChat():
            self.onMessagePre(int(C_C_DD.datas['chat_banned']['value']), [str(self.idipBanDict.get(gameconst.IDIPBanType.CHAT, 0))])
            return

        self._sendMsgToAlliance(msg)

    def _sendMsgToGuild(self, msg, includeMe=False, isTeamZhaomu=False):
        _now = utils.curTS()
        if _now < self.sendGuildMsgTime + int(CCCH.datas[gameconst.ChatChannelEnum.GUILD]['channelCD']):
            _timeDelta = self.sendGuildMsgTime + int(CCCH.datas[gameconst.ChatChannelEnum.GUILD]['channelCD']) - _now
            self.onMessagePre(
                int(C_C_DD.datas['msgId_worldChannelCD']['value']),
                [str(_timeDelta)])
            return

        if not self.guildBox:
            LOG_WARN('sendGuildChatMsg failed that not has guild')
            self.onMessagePre(MMD.datas.guildTrain_notInGuild, [])
            return

        self.sendGuildMsgTime = _now
        self.afterCheckGuildChatMsg(includeMe, isTeamZhaomu, False, msg)

    def _sendMsgToAlliance(self, msg):
        """
        联盟频道发言核心逻辑(2026-08-24 新增):
          - CD 校验走 chatConfig_channel.py ALLIANCE(11) 配置
          - 未加入帮会 -> 沿用 sendGuildChatMsg 同款提示(MMD.guildTrain_notInGuild)
          - 加入帮会但未加入联盟 -> 提示 54003192 "您的所属帮会未加入联盟"
          - 通过后委托 Guild.onSendChatMessage,由其转给 AllianceStub
        """
        _now = utils.curTS()
        if _now < self.sendAllianceMsgTime + int(CCCH.datas[gameconst.ChatChannelEnum.ALLIANCE]['channelCD']):
            _timeDelta = self.sendAllianceMsgTime + int(CCCH.datas[gameconst.ChatChannelEnum.ALLIANCE]['channelCD']) - _now
            self.onMessagePre(
                int(C_C_DD.datas['msgId_worldChannelCD']['value']),
                [str(_timeDelta)])
            return

        if not self.guildBox:
            LOG_WARN('sendAllianceChatMsg failed: not has guild')
            self.onMessagePre(MMD.datas.guildTrain_notInGuild, [])
            return

        self.sendAllianceMsgTime = _now
        
        self.guildBox.onSendChatMessage(self.gbID, self._getChatChannelAvatarInfo(), dict(msg), self)

        self.logChatMsg(msg.get('msgType', 0), 0, gameconst.ChatChannelEnum.ALLIANCE, msg.get('msg',''), self.sendAllianceMsgTime)

    def afterCheckGuildChatMsg(self, includeMe, isTeamZhaomu, sendByServer,originalMsg):
        LOG_DBG("afterCheckGuildChatMsg", includeMe, isTeamZhaomu, sendByServer, originalMsg)
        self.logChatMsg(originalMsg.get('msgType', 0), self.guildUUIDBase, gameconst.ChatChannelEnum.GUILD, originalMsg.get('msg',''), self.sendGuildMsgTime)
        if isTeamZhaomu:
            self.onMessagePre(MMD.datas.zhaomuGuildSent, [])

        if includeMe:
            self.localCrossClient.onRecvAvatarChannelMsg(gameconst.ChatChannelEnum.GUILD, self._getChatChannelAvatarInfo(), originalMsg)

        if not self.isSilentChat(gameconst.SilentSpeakScene.ENUM_CHAT):
            self.guildBox.doSendGuildChatMsg(self._getChatChannelAvatarInfo(), originalMsg)

    def onRecvChannelMsg(self, channelID, avatarInfo, msg):
        _gbId = avatarInfo['gbId']
        if self.friendship.isBlock(_gbId):
            return

        self.localCrossClient.onRecvAvatarChannelMsg(channelID, avatarInfo, msg)
    
    def onRecvTrumpet(self, hornId, avatarInfo, msg):
        LOG_INFO("onRecvTrumpet", hornId, avatarInfo, msg)
        
        self.localCrossClient.onRecvTrumpet(hornId, avatarInfo, msg)

    def onRecvChannelMsgBatch(self, msgBatch):
        LOG_DBG('IChat.onRecvChannelMsgBatch', self.id, len(msgBatch))
        for item in msgBatch:
            msgType = item.get('type')
            args = item.get('args', ())
            if msgType == 'channel':
                self.onRecvChannelMsg(*args)
            elif msgType == 'trumpet':
                self.onRecvTrumpet(*args)
            else:
                LOG_WARN('IChat.onRecvChannelMsgBatch unknown msgType', msgType, args)


    def sendGuildPickChatMsg(self, messageId):
        LOG_DBG('sendGuildPickChatMsg', messageId)
        if self.isAllServerForbidChat():
            self.onMessagePre(int(C_C_DD.datas['chat_banned']['value']), [str(self.idipBanDict.get(gameconst.IDIPBanType.CHAT, 0))])
            return

        _now = utils.curTS()
        if _now < self.sendGuildMsgTime + int(CCCH.datas[gameconst.ChatChannelEnum.GUILD]['channelCD']):
            return

        if not self.guildBoxBase:
            LOG_WARN('sendGuildChatMsg failed that not has guild')
            self.onMessagePre(MMD.datas.guildTrain_notInGuild, [])
            return

        self.sendGuildMsgTime = _now
        self.guildBoxBase.doSendGuildPickChatMsg(self,self._getChatChannelAvatarInfo(), messageId)

    @gamedecorator.crossServer
    @gamedecorator.checkGameconfigEnable('chat')
    def sendTeamChatMsg(self, exposed, teamIdDeprecated, msg):
        teamId = self.teamIdBase
        LOG_DBG('sendTeamChatMsg', teamId, msg)
        if not teamId:
            self.onMessagePre(C_C_DD.datas['teamChannel_NotInTeam_msg']['value'], ())
            return

        if self.isAllServerForbidChat():
            self.onMessagePre(int(C_C_DD.datas['chat_banned']['value']), [str(self.idipBanDict.get(gameconst.IDIPBanType.CHAT, 0))])
            return

        self._sendMsgToTeam(teamId, msg, True)

    def _sendMsgToTeam(self, teamId, msg, includeMe=False):
        _now = utils.curTS()
        if _now < self.sendTeamMsgTime + int(CCCH.datas[gameconst.ChatChannelEnum.TEAM]['channelCD']):
            timeDelta = self.sendTeamMsgTime + int(CCCH.datas[gameconst.ChatChannelEnum.TEAM]['channelCD']) - _now
            self.onMessagePre(int(C_C_DD.datas['msgId_worldChannelCD']['value']), [str(timeDelta)])
            return

        self.sendTeamMsgTime = _now
        self.afterCheckTeamChatMsg(teamId, includeMe, msg)

    def afterCheckTeamChatMsg(self, teamId, includeMe, originalMsg):
        self.logChatMsg(originalMsg.get('msgType', 0), teamId, gameconst.ChatChannelEnum.TEAM, originalMsg.get('msg',''), self.sendTeamMsgTime)
        gameengine.getTeamStub(teamId).sendChatMsgFromTeamMember(teamId, self.gbID, self._getChatChannelAvatarInfo(),originalMsg)
        if includeMe:
            self.client.onRecvAvatarChannelMsg(gameconst.ChatChannelEnum.TEAM, self._getChatChannelAvatarInfo(), originalMsg)

        # if not self.isSilentChat(gameconst.SilentSpeakScene.ENUM_CHAT):
        #     self.checkAchievementTrigger(gameconst.AchieveTargetType.CHANNEL_SPEAK, gameconst.ChatChannelEnum.TEAM)

    @gamedecorator.crossServer
    @gamedecorator.checkGameconfigEnable('chat')
    def sendNearbyChatMsg(self, exposed, msg):
        LOG_DBG('sendNearbyChatMsg', msg)
        if self.isAllServerForbidChat():
            self.onMessagePre(int(C_C_DD.datas['chat_banned']['value']), [str(self.idipBanDict.get(gameconst.IDIPBanType.CHAT, 0))])
            return

        now = utils.curTS()
        if now < self.sendNearbyMsgTime + CCCH.datas[gameconst.ChatChannelEnum.NEARBY]['channelCD']:
            timeDelta = self.sendNearbyMsgTime + CCCH.datas[gameconst.ChatChannelEnum.NEARBY]['channelCD'] - now
            self.onMessagePre(int(C_C_DD.datas['msgId_worldChannelCD']['value']), [str(timeDelta)])
            return

        if gameglobal.roleCache[self.id]['level'] < CCCH.datas[gameconst.ChatChannelEnum.NEARBY]['channelMinLevel']:
            return

        self.sendNearbyMsgTime = now
        self.afterCheckNearbyChatMsg(msg)

    def afterCheckNearbyChatMsg(self, originalMsg):
        LOG_DBG("afterCheckNearbyChatMsg", originalMsg)
        self.logChatMsg(originalMsg.get('msgType', 0), 0, gameconst.ChatChannelEnum.NEARBY, originalMsg.get('msg',''), self.sendNearbyMsgTime)
        self.client.onRecvAvatarChannelMsg(gameconst.ChatChannelEnum.NEARBY, self._getChatChannelAvatarInfo(), originalMsg)
        if not self.isSilentChat(gameconst.SilentSpeakScene.ENUM_CHAT):
            self.cell.handleAvatarChannelMsg(gameconst.ChatChannelEnum.NEARBY, self._getChatChannelAvatarInfo(), originalMsg)
            # self.checkAchievementTrigger(gameconst.AchieveTargetType.CHANNEL_SPEAK, gameconst.ChatChannelEnum.NEARBY)

    #@gamedecorator.forwardToLocal
    @gamedecorator.crossServer
    @gamedecorator.checkGameconfigEnable('chat')
    def sendRaidChatMsg(self, exposed, raidUUIDDeprecated, msg):
        raidUUID = self.raidUUIDBase
        LOG_DBG('sendRaidChatMsg::', msg)
        if not raidUUID:
            self.onMessagePre(RAID_CONST.datas["raid_notInRaid_msg"]["value"], [])
            return

        if self.isAllServerForbidChat():
            self.onMessagePre(int(C_C_DD.datas['chat_banned']['value']), [str(self.idipBanDict.get(gameconst.IDIPBanType.CHAT, 0))])
            return

        now = utils.curTS()
        if now < self.sendRaidMsgTime + int(CCCH.datas[gameconst.ChatChannelEnum.RAID]['channelCD']):
            timeDelta = self.sendRaidMsgTime + int(CCCH.datas[gameconst.ChatChannelEnum.RAID]['channelCD']) - now
            self.onMessagePre(int(C_C_DD.datas['msgId_worldChannelCD']['value']), [str(timeDelta)])
            return

        avatarInfo = self._getChatChannelAvatarInfo()
        extraProps = {}
        self.sendRaidMsgTime = now
        self.afterCheckRaidChatMsg(raidUUID, avatarInfo, extraProps, msg)

    def afterCheckRaidChatMsg(self,raidUUID, avatarInfo, extraProps, originalMsg):
        LOG_DBG("afterCheckRaidChatMsg", raidUUID, avatarInfo, extraProps, originalMsg)
        self.logChatMsg(originalMsg.get('msgType', 0), raidUUID, gameconst.ChatChannelEnum.RAID, originalMsg.get('msg',''), self.sendRaidMsgTime)
        self.client.onRecvAvatarChannelMsg(gameconst.ChatChannelEnum.RAID, avatarInfo, originalMsg)
        if not self.isSilentChat(gameconst.SilentSpeakScene.ENUM_CHAT):
            gameengine.getRaidStub(raidUUID).broadRaidChatMsg(self, self.gbID, raidUUID, avatarInfo, originalMsg, extraProps)
            # self.checkAchievementTrigger(gameconst.AchieveTargetType.CHANNEL_SPEAK, gameconst.ChatChannelEnum.RAID)

    def sendReleaseRedbagMsg(self, redbagId, redbagType, channel, money, desc):
        LOG_INFO("sendReleaseRedbagMsg:", redbagId, redbagType, channel, money, desc)
        _avatarInfo = self._getChatChannelAvatarInfo()
        # 发送消息
        if self.isSilentChat(gameconst.SilentSpeakScene.ENUM_CHAT):
            self.client.onReleaseRedBagMsg(redbagId, redbagType, channel, money, desc, _avatarInfo)
        elif channel == gameconst.RedBagChannel.WORLD:
            gameengine.broadcastBaseapp('onBroadcastToAllClients',
                                        ('onReleaseRedBagMsg', (redbagId, redbagType, channel, money, desc, _avatarInfo)))
        elif channel == gameconst.RedBagChannel.GUILD and self.guildBox:
            # self.sendGuildChatMsg()
            self.guildBox.doSendGuildRedBagMsg(redbagId, redbagType, channel, money, desc, _avatarInfo)

    @gamedecorator.crossServer
    def registerItemLink(self, exposed, itemIdList, uniqueIdList):
        LOG_INFO('registerItemLink', itemIdList, uniqueIdList)

    @gamedecorator.crossServer
    def queryItemLink(self, exposed, uniqueId, itemId, gbId):
        LOG_INFO('queryItemLink', uniqueId, itemId, gbId)
        if not gbId:
            LOG_ERR('queryItemLink but invalid gbId', gbId)
            return

        gameengine.getGlobalBase('PlayerStub').doOnOthersBase(
            [gbId], 'sendItemLinkInfo',
            (self, uniqueId, itemId),
            self, 'onFindLinkItemOwnerFail', ())

    def onFindLinkItemOwnerFail(self, gbIds):
        self.onMessagePre(MMD.datas.channel_noItem, [])

    @gamedecorator.crossServer
    def queryPlayerLink(self, exposed, gbId):
        self.getAvatarInterInfo(gbId)

    def _getChatChannelAvatarInfo(self):
        # todo 增加玩家帮会和战力信息
        _roleData = gameglobal.roleCache[self.id]
        return utils.buildChatChannelAvatarData(
            self.id,
            self.gbID,
            _roleData['school'],
            _roleData['name'],
            _roleData['level'],
            _roleData['sex'],
            _roleData['picFrameId'],
        )

    def handleQueryPlayerLink(self, box):
        box.client.onQueryPlayerLink(self._getChatChannelAvatarInfo())

    @gamedecorator.crossServer
    @gamedecorator.checkGameconfigEnable('chat')
    def sendRaidMatchMessage(self, exposed, teamId, content, teamTarget, curNum, channel):
        self._sendMatchMessage(teamId, content, teamTarget, curNum, channel, False)

    @gamedecorator.crossServer
    @gamedecorator.checkGameconfigEnable('chat')
    def sendTeamMatchMessage(self, exposed, teamId, content, teamTarget, curNum, channel):
        self._sendMatchMessage(teamId, content, teamTarget, curNum, channel, True)

    def _sendMatchMessage(self, teamId, content, teamTarget, curNum, channel, isTeam):
        LOG_INFO('in sendTeamMatchMessage:', teamId, content, teamTarget, curNum, channel)
        if self.isAllServerForbidChat():
            self.onMessagePre(int(C_C_DD.datas['chat_banned']['value']), [str(self.idipBanDict.get(gameconst.IDIPBanType.CHAT, 0))])
            return

        # 只处理自身目标和具体活动目标
        if teamTarget < 1:
            LOG_ERR('in sendTeamMatchMessage, teamTarget error 1')
            return

        targetInfo = TMACTD.datas.get(teamTarget)
        if not targetInfo:
            LOG_ERR('in sendTeamMatchMessage, teamTarget error 2')
            return

        if isTeam:
            teamMemberCount = gameconst.TEAM_MEMBER_MAX_NUM
            c = targetInfo['maxPlayer']
            if c > 0:
                teamMemberCount = teamMemberCount if c > teamMemberCount else c
        else:
            teamMemberCount = gameconst.RAID_MEMBER_MAX_NUM
            c = targetInfo['maxPlayer']
            if c > 0:
                teamMemberCount = teamMemberCount if c > teamMemberCount else c

        isRaid = 0 if isTeam else 1
        chatMsgKey = 'teamChannel_applyTeamMsg' if isTeam else 'teamChannel_applyRaidMsg'
        #活动：%s%d-%d级%s的队伍正在招募:<link team name=申请加入 teamId=%d>
        msg = MCM.datas[TM_MCD.datas[chatMsgKey]['value']]['Message'].format(targetInfo['value'], content, curNum, teamMemberCount, teamId, isRaid, teamTarget)

        _now = utils.curTS()
        if gameconst.ChatChannelEnum.GUILD == channel:
            _guildMsgCD = TM_MCD.datas.get('guildChannelCD', {}).get('value', 0)
            if self.sendMatchTeamGuildMsgTime + _guildMsgCD > _now:
                self.onMessagePre(MMD.datas.zhaomuMessageCD, [str(self.sendMatchTeamGuildMsgTime + _guildMsgCD - _now)])
                return
            self.sendMatchTeamGuildMsgTime = _now
            self._sendMsgToGuild({"msg":msg, "code":0, "voiceUrl":"", "msgType":0}, includeMe=True, isTeamZhaomu=True)
        elif gameconst.ChatChannelEnum.RECRUIT == channel or gameconst.ChatChannelEnum.TEAM == channel or gameconst.ChatChannelEnum.RAID == channel \
            or gameconst.ChatChannelEnum.SIEGE_WAR == channel:
            zhaomuChannelCD = TM_MCD.datas.get('zhaomuChannelCD', {}).get('value', 0)
            if self.sendMatchTeamRecruitMsgTime + zhaomuChannelCD > _now:
                self.onMessagePre(MMD.datas.zhaomuMessageCD, [str(self.sendMatchTeamRecruitMsgTime + zhaomuChannelCD - _now)])
                return
            self.sendMatchTeamRecruitMsgTime = _now
            self.sendTeamMatchRecruitMsg(channel, msg)

    def sendTeamMatchRecruitMsg(self, channel, msg):
        self.logChatMsg(0, 0, channel, msg, self.sendMatchTeamRecruitMsgTime)
        if self.isSilentChat(gameconst.SilentSpeakScene.ENUM_CHAT):
            self.cell.handleTeamChannelMatchTeamMsg(self._getChatChannelAvatarInfo(), channel, msg)
        elif gameconst.ChatChannelEnum.SIEGE_WAR == channel:
            gameengine.broadcastBaseapp('broadcastToAllAvatar',
                                        (gameconst.CELL, 'onSiegeWarChatMsg',
                                        (gameconst.ChatChannelEnum.SIEGE_WAR, self._getChatChannelAvatarInfo(), msg, self.cell), ()))
            self.onMessagePre(MMD.datas.zhaomuBattleFieldSent, [])
        else:
            gameengine.broadcastBaseapp('broadcastToAllAvatar',
                                        (gameconst.CELL, 'handleTeamChannelMatchTeamMsg',
                                         (self._getChatChannelAvatarInfo(), channel, msg)))
            self.onMessagePre(MMD.datas.recruitSent, [])

    # 调用前检查对应分享限制条件
    def sendChannelShareMsg(self, channel, msg):
        if channel == gameconst.ChatChannelEnum.WORLD:
            self.sendWorldChatMsg(msg)
        elif channel == gameconst.ChatChannelEnum.GUILD:
            self.sendGuildChatMsg(msg)
        elif channel == gameconst.ChatChannelEnum.TEAM:
            self.sendTeamChatMsg(self.teamIdBase, msg)
        elif channel == gameconst.ChatChannelEnum.RAID:
            self.sendRaidChatMsg(self.raidUUIDBase, msg)
        else:
            LOG_WARN('IChat::sendChannelShareMsg need add share channel !!!')

    def isAllServerForbidChat(self):
        if self.isIDIPBan(gameconst.IDIPBanType.CHAT):
            return True

        return False

    def removeSilentSpeak(self,chatScence):
        if chatScence == gameconst.SilentSpeakScene.ENUM_FRIEND_CHAT:
            self.silentSpeakState = self.silentSpeakState & gameconst.SilentSpeakState.ENUM_REMOVE_FRIEND_CHAT
        elif chatScence == gameconst.SilentSpeakScene.ENUM_CHAT:
            self.silentSpeakState = self.silentSpeakState & gameconst.SilentSpeakState.ENUM_REMOVE_CHAT
        elif chatScence == gameconst.SilentSpeakScene.ENUM_ALL:
            self.silentSpeakState = self.silentSpeakState & gameconst.SilentSpeakState.ENUM_REMOVE_ALL

    def isSilentChat(self,chatState):
        if self.silentSpeakState & 1 << chatState:
            if chatState == gameconst.SilentSpeakScene.ENUM_CHAT and utils.curTS() <= self.silentSpeakTime:
                return True
            elif chatState == gameconst.SilentSpeakScene.ENUM_FRIEND_CHAT and utils.curTS() <= self.silentFriendSpeakTime:
                return True

        return False

    def onNotifyChatForbiddenState(self, gbid, state):
        LOG_DBG("onNotifyChatForbiddenState", gbid, state)
        self.localCrossClient.onNotifyChatForbiddenState(gbid, state)

    def cancelNotifyChatForbiddenTimer(self):
        if not self.notifyChatForbiddenTimer:
            return
        self._cancelDatetimeCallback(self.notifyChatForbiddenTimer, gametimer.TIMER_TAG_NOTIFY_CHAT_FORBIDDEN)
        self.notifyChatForbiddenTimer = 0

    def setNotifyChatForbiddenTimer(self, endTime):
        self.cancelNotifyChatForbiddenTimer()
        LOG_INFO("setNotifyChatForbiddenTimer", endTime)
        self.notifyChatForbiddenTimer = self._datetimeCallback(endTime, 'notifyChatForbiddenTimerCallback', (), gametimer.TIMER_TAG_NOTIFY_CHAT_FORBIDDEN, 'notifyChatForbiddenTimer')

    def notifyChatForbiddenTimerCallback(self):
        LOG_INFO("notifyChatForbiddenTimerCallback", utils.getCurrentTimeFmt())
        gameengine.callBaseApps('gameengine.updateChatForbiddenState', (self.gbID, 0))

    def updateChatForbiddenState(self, isGm=True):
        self.syncMethodCallToCrossServerBase('updateChatForbiddenState', (isGm,))
        LOG_INFO("updateChatForbiddenState1", isGm, gameglobal.chatForbiddenSet)
        if self.isAllServerForbidChat():
            endTime = self.idipBanDict.get(gameconst.IDIPBanType.CHAT, 0)
            self.setNotifyChatForbiddenTimer(endTime)
            LOG_INFO("updateChatForbiddenState2", endTime)
            if not isGm and self.gbID in gameglobal.chatForbiddenSet:
                return
            gameengine.callBaseApps('gameengine.updateChatForbiddenState', (self.gbID, 1))
        else:
            if self.gbID not in gameglobal.chatForbiddenSet:
                return
            self.cancelNotifyChatForbiddenTimer()
            LOG_INFO("updateChatForbiddenState3")
            gameengine.callBaseApps('gameengine.updateChatForbiddenState', (self.gbID, 0))

    def logChatMsg(self, messag_type, receive_gbid, channel_id, content, send_time):
            LogTrackingMgr.LogTrackingMgr.message(
            self.gbID,
            self.accountEntity.clientDistinctId,
            messag_type,
            self.gbID,
            receive_gbid,
            channel_id,
            content,
            send_time,
        )