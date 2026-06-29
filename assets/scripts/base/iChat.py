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
import antiAddictCategory_antiAddictCategory_def as AAC_AACDD

class IChat(object):
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

        if not self.canDeductWealth(deductWealthVal):
            LOG_WARN('sendPaidChatMsg: items not enough:', deductWealthVal)
            return False

        detail = gameclass.AwardDetailCls()
        opUUID = KBEngine.genUUID64()
        srcType = AAC_AACDD.datas.BONUS_SRC_COST_HORN
        return self.deductWealth(srcType, deductWealthVal, opUUID, detail)

    @gamedecorator.crossServer
    @gamedecorator.checkGameconfigEnable('chat')
    def sendPaidChatMsg(self, exposed, hornId, msg):
        LOG_DBG('sendPaidChatMsg', hornId, msg)
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
        self.afterCheckPaidChatMsg(msg, channel)

        self.syncMethodCallToLocalServerBase("onCrossServerPaidChatMsg", (hornId,))
        
    def onCrossServerPaidChatMsg(self, hornId):
        if not self._deductHornItem(hornId):
            gameengine.panicStack('onCrossServerPaidChatMsg: deductHornItem failed', hornId)

    def afterCheckPaidChatMsg(self, originalMsg, channel):
        LOG_DBG("afterCheckPaidChatMsg", originalMsg)
        if self.isSilentChat(gameconst.SilentSpeakScene.ENUM_CHAT):
            self.client.onRecvAvatarChannelMsg(channel, self._getChatChannelAvatarInfo(), originalMsg)
            return

        gameengine.broadcastBaseapp('broadcastToAllAvatar',
                                    (gameconst.BASE, 'onRecvChannelMsg',
                                     (channel, self._getChatChannelAvatarInfo(), originalMsg), ()))

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
        if self.isSilentChat(gameconst.SilentSpeakScene.ENUM_CHAT):
            self.client.onRecvAvatarChannelMsg(gameconst.ChatChannelEnum.WORLD, self._getChatChannelAvatarInfo(), originalMsg)
            return

        gameengine.broadcastBaseapp('broadcastToAllAvatar',
                                    (gameconst.BASE, 'onRecvChannelMsg',
                                     (gameconst.ChatChannelEnum.WORLD, self._getChatChannelAvatarInfo(), originalMsg), ()))
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

    def afterCheckGuildChatMsg(self, includeMe, isTeamZhaomu, sendByServer,originalMsg):
        LOG_DBG("afterCheckGuildChatMsg", includeMe, isTeamZhaomu, sendByServer, originalMsg)
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

        chatMsgKey = 'teamChannel_applyTeamMsg' if isTeam else 'teamChannel_applyRaidMsg'
        teamMemberCount = gameconst.TEAM_MEMBER_MAX_NUM if isTeam else gameconst.RAID_MEMBER_MAX_NUM
        isRaid = 0 if isTeam else 1

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

