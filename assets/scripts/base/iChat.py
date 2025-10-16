# -*- coding: utf-8 -*-

import KBEngine
from KBEDebug import *

import utils
import gameengine
import gameconst
import gameglobal
import gamedecorator
import chatConfig_chatConfig as CCD
import chatConfig_channel as CCCH
import teamMatch_matchConfig as TMMCD
import teamMatch_activity as TMACTD
import message_Message_def as MMD
import raid_raidConst as RAID_CONST
import message_Message as MM
import message_chatMessage as MCM
import activityControl_activityData as AC_ADD

class IChat(object):
    def setChatChannel(self, exposed, channel):
        DEBUG_MSG('setChatChannel', channel)
        if channel >= gameconst.ChatChannel.MAX:
            return

        if self.hasChatChannel(channel):
            return

        newChannel = self.chatChannel | (1 << channel)
        self.chatChannel = newChannel

    def removeChatChannel(self, exposed, channel):
        DEBUG_MSG('removeChatChannel', channel)
        if channel >= gameconst.ChatChannel.MAX:
            return

        if not self.hasChatChannel(channel):
            return

        newChannel = self.chatChannel & (~(1 << channel))
        self.chatChannel = newChannel

    def hasChatChannel(self, channel):
        if self.chatChannel & (1 << channel):
            return True
        else:
            return False

    def sendWorldChatMsg(self, exposed, msg):
        DEBUG_MSG('sendWorldChatMsg', msg)
        if self.isAllServerForbidChat():
            self.onMessagePre(int(CCD.datas['chat_banned']['value']), [self.accountEntity.banAllServerPostReason, utils.getBanEndTimeString(self.accountEntity.banAllServerPostTime)])
            self.client.onSendForbidChat(self.accountEntity.banAllServerPostTime, self.accountEntity.banAllServerPostReason)
            return

        now = utils.getNow()
        if now < self.sendWorldMsgTime + CCCH.datas[gameconst.ChatChannel.WORLD]['channelCD']:
            timeDelta = self.sendWorldMsgTime + CCCH.datas[gameconst.ChatChannel.WORLD]['channelCD']-now
            self.onMessagePre(int(CCD.datas['msgId_worldChannelCD']['value']), [str(timeDelta)])
            self.client.onSetChatCD(gameconst.ChatChannel.WORLD,self.sendWorldMsgTime + CCCH.datas[gameconst.ChatChannel.WORLD]['channelCD'])
            return

        if gameglobal.roleCache[self.id]['level'] < CCCH.datas[gameconst.ChatChannel.WORLD]['channelMinLevel']:
            return

        self.sendWorldMsgTime = now
        self.client.onSetChatCD(gameconst.ChatChannel.WORLD,self.sendWorldMsgTime + CCCH.datas[gameconst.ChatChannel.WORLD]['channelCD'])
        self.afterCheckWorldChatMsg(msg)

    def afterCheckWorldChatMsg(self, originalMsg):
        DEBUG_MSG("afterCheckWorldChatMsg", originalMsg)
        if self.isSilentChat(gameconst.SilentSpeakScene.CHAT):
            self.client.onRecvAvatarChannelMsg(gameconst.ChatChannel.WORLD, self._getChatChannelAvatarInfo(), originalMsg)
            return

        gameengine.broadcastBaseapp('broadcastToAllAvatar',
                                    (gameconst.BASE, 'onRecvChannelMsg',
                                     (gameconst.ChatChannel.WORLD, self._getChatChannelAvatarInfo(), originalMsg), ()))
        # self.checkAchievementTrigger(gameconst.AchieveTargetType.CHANNEL_SPEAK, gameconst.ChatChannel.WORLD)

    def sendSiegeWarChatMsg(self, exposed, msg):
        DEBUG_MSG('sendSiegeWarChatMsg', msg)
        if self.isAllServerForbidChat():
            self.onMessagePre(int(CCD.datas['chat_banned']['value']), [self.accountEntity.banAllServerPostReason, utils.getBanEndTimeString(self.accountEntity.banAllServerPostTime)])
            self.client.onSendForbidChat(self.accountEntity.banAllServerPostTime, self.accountEntity.banAllServerPostReason)
            return
        
        now = utils.getNow()
        if now < self.sendSiegeWarMsgTime + CCCH.datas[gameconst.ChatChannel.SIEGE_WAR]['channelCD']:
            timeDelta = self.sendSiegeWarMsgTime + CCCH.datas[gameconst.ChatChannel.SIEGE_WAR]['channelCD']-now
            self.onMessagePre(int(CCD.datas['msgId_worldChannelCD']['value']), [str(timeDelta)])
            self.client.onSetChatCD(gameconst.ChatChannel.SIEGE_WAR,self.sendSiegeWarMsgTime + CCCH.datas[gameconst.ChatChannel.SIEGE_WAR]['channelCD'])
            return

        gameengine.broadcastBaseapp('broadcastToAllAvatar',
                                    (gameconst.CELL, 'onSiegeWarChatMsg',
                                     (gameconst.ChatChannel.SIEGE_WAR, self._getChatChannelAvatarInfo(), msg, self.cell), ()))

    @gamedecorator.forwardToLocal
    def sendGuildChatMsg(self, exposed, msg):
        DEBUG_MSG('sendGuildChatMsg', msg)
        if self.isAllServerForbidChat():
            self.onMessagePre(int(CCD.datas['chat_banned']['value']), [self.accountEntity.banAllServerPostReason,utils.getBanEndTimeString(self.accountEntity.banAllServerPostTime)])
            self.client.onSendForbidChat(self.accountEntity.banAllServerPostTime, self.accountEntity.banAllServerPostReason)
            return

        self._sendMsgToGuild(msg,True)

    def _sendMsgToGuild(self, msg, includeMe=False, isTeamZhaomu=False, sendByServer=False):
        now = utils.getNow()
        if now < self.sendGuildMsgTime + int(CCCH.datas[gameconst.ChatChannel.GUILD]['channelCD']):
            timeDelta = self.sendGuildMsgTime + int(CCCH.datas[gameconst.ChatChannel.GUILD]['channelCD']) - now
            self.onMessagePre(int(CCD.datas['msgId_worldChannelCD']['value']), [str(timeDelta)])
            self.client.onSetChatCD(gameconst.ChatChannel.GUILD, self.sendGuildMsgTime + int(CCCH.datas[gameconst.ChatChannel.GUILD]['channelCD']))
            return

        if not self.guildBox:
            WARNING_MSG('sendGuildChatMsg failed that not has guild')
            self.onMessagePre(MMD.datas.guildTrain_notInGuild, [])
            return

        self.sendGuildMsgTime = now
        self.client.onSetChatCD(gameconst.ChatChannel.GUILD, self.sendGuildMsgTime + int(CCCH.datas[gameconst.ChatChannel.GUILD]['channelCD']))
        self.afterCheckGuildChatMsg(includeMe, isTeamZhaomu, sendByServer, msg)

    def afterCheckGuildChatMsg(self, includeMe, isTeamZhaomu, sendByServer,originalMsg):
        DEBUG_MSG("afterCheckGuildChatMsg", includeMe, isTeamZhaomu, sendByServer, originalMsg)
        move = dict.fromkeys((ord(c) for c in u"\r\n\t |"))

        if isTeamZhaomu:
            self.onMessagePre(MMD.datas.zhaomuGuildSent, [])

        if includeMe:
            self.localCrossClient.onRecvAvatarChannelMsg(gameconst.ChatChannel.GUILD, self._getChatChannelAvatarInfo(), originalMsg)

        if not self.isSilentChat(gameconst.SilentSpeakScene.CHAT):
            self.guildBox.doSendGuildChatMsg(self._getChatChannelAvatarInfo(), originalMsg)
            # if not sendByServer:
                # self.checkAchievementTrigger(gameconst.AchieveTargetType.CHANNEL_SPEAK, gameconst.ChatChannel.GUILD)

    def onRecvChannelMsg(self, channelID, avatarInfo, msg):
        _gbId = avatarInfo['gbId']
        if self.friendship.isBlock(_gbId):
            return

        self.localCrossClient.onRecvAvatarChannelMsg(channelID, avatarInfo, msg)

    def sendGuildPickChatMsg(self, messageId):
        DEBUG_MSG('sendGuildPickChatMsg', messageId)
        if self.isAllServerForbidChat():
            self.onMessagePre(int(CCD.datas['chat_banned']['value']), [self.accountEntity.banAllServerPostReason,utils.getBanEndTimeString(self.accountEntity.banAllServerPostTime)])
            self.client.onSendForbidChat(self.accountEntity.banAllServerPostTime, self.accountEntity.banAllServerPostReason)
            return

        now = utils.getNow()
        if now < self.sendGuildMsgTime + int(CCCH.datas[gameconst.ChatChannel.GUILD]['channelCD']):
            return

        if not self.guildBoxBase:
            WARNING_MSG('sendGuildChatMsg failed that not has guild')
            self.onMessagePre(MMD.datas.guildTrain_notInGuild, [])
            return

        self.sendGuildMsgTime = now
        self.guildBoxBase.doSendGuildPickChatMsg(self,self._getChatChannelAvatarInfo(), messageId)

    def sendTeamChatMsg(self, exposed, teamIdDeprecated, msg):
        teamId = self.teamIdBase
        DEBUG_MSG('sendTeamChatMsg', teamId, msg)
        if not teamId:
            self.onMessagePre(CCD.datas['teamChannel_NotInTeam_msg']['value'], ())
            return

        if self.isAllServerForbidChat():
            self.onMessagePre(int(CCD.datas['chat_banned']['value']), [self.accountEntity.banAllServerPostReason,utils.getBanEndTimeString(self.accountEntity.banAllServerPostTime)])
            self.client.onSendForbidChat(self.accountEntity.banAllServerPostTime, self.accountEntity.banAllServerPostReason)
            return

        self._sendMsgToTeam(teamId, msg, True)

    def _sendMsgToTeam(self, teamId, msg, includeMe=False):
        now = utils.getNow()
        if now < self.sendTeamMsgTime + int(CCCH.datas[gameconst.ChatChannel.TEAM]['channelCD']):
            timeDelta = self.sendTeamMsgTime + int(CCCH.datas[gameconst.ChatChannel.TEAM]['channelCD']) - now
            self.onMessagePre(int(CCD.datas['msgId_worldChannelCD']['value']), [str(timeDelta)])
            self.client.onSetChatCD(gameconst.ChatChannel.TEAM, self.sendTeamMsgTime + int(CCCH.datas[gameconst.ChatChannel.TEAM]['channelCD']))
            return

        self.sendTeamMsgTime = now
        self.client.onSetChatCD(gameconst.ChatChannel.TEAM, self.sendTeamMsgTime + int(CCCH.datas[gameconst.ChatChannel.TEAM]['channelCD']))
        self.afterCheckTeamChatMsg(teamId, includeMe, msg)

    def afterCheckTeamChatMsg(self, teamId, includeMe, originalMsg):
        gameengine.getTeamStub(teamId).sendChatMsgFromTeamMember(teamId, self.gbID, self._getChatChannelAvatarInfo(),originalMsg)
        if includeMe:
            self.client.onRecvAvatarChannelMsg(gameconst.ChatChannel.TEAM, self._getChatChannelAvatarInfo(), originalMsg)

        # if not self.isSilentChat(gameconst.SilentSpeakScene.CHAT):
        #     self.checkAchievementTrigger(gameconst.AchieveTargetType.CHANNEL_SPEAK, gameconst.ChatChannel.TEAM)

    def sendNearbyChatMsg(self, exposed, msg):
        DEBUG_MSG('sendNearbyChatMsg', msg)
        if self.isAllServerForbidChat():
            self.onMessagePre(int(CCD.datas['chat_banned']['value']), [self.accountEntity.banAllServerPostReason,utils.getBanEndTimeString(self.accountEntity.banAllServerPostTime)])
            self.client.onSendForbidChat(self.accountEntity.banAllServerPostTime, self.accountEntity.banAllServerPostReason)
            return

        now = utils.getNow()
        if now < self.sendNearbyMsgTime + CCCH.datas[gameconst.ChatChannel.NEARBY]['channelCD']:
            timeDelta = self.sendNearbyMsgTime + CCCH.datas[gameconst.ChatChannel.NEARBY]['channelCD'] - now
            self.onMessagePre(int(CCD.datas['msgId_worldChannelCD']['value']), [str(timeDelta)])
            self.client.onSetChatCD(gameconst.ChatChannel.NEARBY, self.sendNearbyMsgTime + CCCH.datas[gameconst.ChatChannel.NEARBY]['channelCD'])
            return

        if gameglobal.roleCache[self.id]['level'] < CCCH.datas[gameconst.ChatChannel.NEARBY]['channelMinLevel']:
            return

        self.sendNearbyMsgTime = now
        self.client.onSetChatCD(gameconst.ChatChannel.NEARBY, self.sendNearbyMsgTime + CCCH.datas[gameconst.ChatChannel.NEARBY]['channelCD'])
        self.afterCheckNearbyChatMsg(msg)

    def afterCheckNearbyChatMsg(self, originalMsg):
        DEBUG_MSG("afterCheckNearbyChatMsg", originalMsg)
        self.client.onRecvAvatarChannelMsg(gameconst.ChatChannel.NEARBY, self._getChatChannelAvatarInfo(), originalMsg)
        if not self.isSilentChat(gameconst.SilentSpeakScene.CHAT):
            self.cell.handleAvatarChannelMsg(gameconst.ChatChannel.NEARBY, self._getChatChannelAvatarInfo(), originalMsg)
            # self.checkAchievementTrigger(gameconst.AchieveTargetType.CHANNEL_SPEAK, gameconst.ChatChannel.NEARBY)

    #@gamedecorator.crossServer
    #@gamedecorator.forwardToLocal
    def sendRaidChatMsg(self, exposed, raidUUIDDeprecated, msg):
        raidUUID = self.raidUUIDBase
        DEBUG_MSG('sendRaidChatMsg::', msg)
        if not raidUUID:
            self.onMessagePre(RAID_CONST.datas["raid_notInRaid_msg"]["value"], [])
            return

        if self.isAllServerForbidChat():
            self.onMessagePre(int(CCD.datas['chat_banned']['value']), [self.accountEntity.banAllServerPostReason,utils.getBanEndTimeString(self.accountEntity.banAllServerPostTime)])
            self.client.onSendForbidChat(self.accountEntity.banAllServerPostTime, self.accountEntity.banAllServerPostReason)
            return

        now = utils.getNow()
        if now < self.sendRaidMsgTime + int(CCCH.datas[gameconst.ChatChannel.RAID]['channelCD']):
            timeDelta = self.sendRaidMsgTime + int(CCCH.datas[gameconst.ChatChannel.RAID]['channelCD']) - now
            self.onMessagePre(int(CCD.datas['msgId_worldChannelCD']['value']), [str(timeDelta)])
            self.client.onSetChatCD(gameconst.ChatChannel.RAID, self.sendRaidMsgTime + int(CCCH.datas[gameconst.ChatChannel.RAID]['channelCD']))
            return

        avatarInfo = self._getChatChannelAvatarInfo()
        extraProps = {}
        self.sendRaidMsgTime = now
        self.client.onSetChatCD(gameconst.ChatChannel.RAID, self.sendRaidMsgTime + int(CCCH.datas[gameconst.ChatChannel.RAID]['channelCD']))
        self.afterCheckRaidChatMsg(raidUUID, avatarInfo, extraProps, msg)

    def afterCheckRaidChatMsg(self,raidUUID, avatarInfo, extraProps, originalMsg):
        DEBUG_MSG("afterCheckRaidChatMsg", raidUUID, avatarInfo, extraProps, originalMsg)

        self.client.onRecvAvatarChannelMsg(gameconst.ChatChannel.RAID, avatarInfo, originalMsg)
        if not self.isSilentChat(gameconst.SilentSpeakScene.CHAT):
            gameengine.getRaidStub(raidUUID).broadRaidChatMsg(self, self.gbID, raidUUID, avatarInfo, originalMsg, extraProps)
            # self.checkAchievementTrigger(gameconst.AchieveTargetType.CHANNEL_SPEAK, gameconst.ChatChannel.RAID)

    def useTrumpetItem(self, exposed, itemId, msg):
        DEBUG_MSG('useTrumpetItem', itemId, msg)
        if self.isSilentChat(gameconst.SilentSpeakScene.CHAT):
            self.client.onRecvTrumpetMsg(self._getChatChannelAvatarInfo(), itemId, msg)
        else:
            gameengine.broadcastBaseapp('onBroadcastToAllClients',
                                     ('onRecvTrumpetMsg', (self._getChatChannelAvatarInfo(), itemId, msg)))
            # self.checkAchievementTrigger(gameconst.AchieveTargetType.CHANNEL_SPEAK, gameconst.ChatChannel.WORLD)

    def sendReleaseRedbagMsg(self, redbagId, redbagType, channel, money, desc):
        INFO_MSG("sendReleaseRedbagMsg:", redbagId, redbagType, channel, money, desc)
        _avatarInfo = self._getChatChannelAvatarInfo()
        # 发送消息
        if self.isSilentChat(gameconst.SilentSpeakScene.CHAT):
            self.client.onReleaseRedBagMsg(redbagId, redbagType, channel, money, desc, _avatarInfo)
        elif channel == gameconst.RedBagChannel.WORLD:
            gameengine.broadcastBaseapp('onBroadcastToAllClients',
                                        ('onReleaseRedBagMsg', (redbagId, redbagType, channel, money, desc, _avatarInfo)))
        elif channel == gameconst.RedBagChannel.GUILD and self.guildBox:
            # self.sendGuildChatMsg()
            self.guildBox.doSendGuildRedBagMsg(redbagId, redbagType, channel, money, desc, _avatarInfo)
            

    def checkUseTrumpetBase(self, pendingCheckId,msg):
        DEBUG_MSG("checkUseTrumpetBase ",pendingCheckId)
        if self.isAllServerForbidChat():
            self.onMessagePre(int(CCD.datas['chat_banned']['value']), [self.accountEntity.banAllServerPostReason,utils.getBanEndTimeString(self.accountEntity.banAllServerPostTime)])
            self.client.onSendForbidChat(self.accountEntity.banAllServerPostTime, self.accountEntity.banAllServerPostReason)
            return

        self.cell.afterCheckTrumpetMsg(pendingCheckId, msg)

    def queryPetLink(self, petGbId, gbId):
        DEBUG_MSG('queryPetLink', petGbId)
        # self.getPetDateDetailInfoInternal(gbId, petGbId, '_queryPetLink', ())

    # def _queryPetLink(self, result, data):
    #     if result == gameconst.GetPetDateDetailResult.SUCCESS:
    #         self.client.onQueryPetLink(data)
    #     else:
    #         self.onMessagePre(MMD.datas.channel_noItem, [])

    def registerItemLink(self, exposed, itemIdList, uniqueIdList):
        DEBUG_MSG('registerItemLink', itemIdList, uniqueIdList)

        if len(itemIdList) != len(uniqueIdList):
            return

        # for i in range(len(itemIdList)):
        #     item = self.bagData.getItemByItemIdAndUniqueId(itemIdList[i], uniqueIdList[i])
        #     if item and (item.isLingShouEggItem() or item.isDuoHunItem()):
        #         gameengine.getGlobalBase('ItemLinkStub').uploadItemInfo(uniqueIdList[i], item.toItemSavedDict())

    def queryItemLink(self, exposed, uniqueId, itemId, gbId):
        DEBUG_MSG('queryItemLink', uniqueId, itemId, gbId)
        if not gbId:
            ERROR_MSG('queryItemLink but invalid gbId', gbId)
            return

        # if dataUtils.isLingShouEggItemByItemId(itemId) or dataUtils.isDuoHunItemByItemId(itemId):
        #     gameengine.getGlobalBase('ItemLinkStub').downloadItemInfo(uniqueId, self)
        gameengine.getGlobalBase('PlayerStub').doOnOthersBase([gbId], 'sendItemLinkInfo',
                                                                  (self, uniqueId, itemId),
                                                                  self, 'onFindLinkItemOwnerFailed', ())

    def onFindLinkItemOwnerFailed(self, gbIds):
        self.onMessagePre(MMD.datas.channel_noItem, [])

    @gamedecorator.crossServer
    def queryPlayerLink(self, exposed, gbId):
        self.getAvatarInterInfo(gbId)

    def handleQueryPlayerLink(self, box):
        box.client.onQueryPlayerLink(self._getChatChannelAvatarInfo())

    def _getChatChannelAvatarInfo(self):
        # todo 增加玩家帮会和战力信息
        return utils.buildChatChannelAvatarInfo(
            self.id,
            self.gbID,
            gameglobal.roleCache[self.id]['school'],
            gameglobal.roleCache[self.id]['name'],
            gameglobal.roleCache[self.id]['level'],
            gameglobal.roleCache[self.id]['sex'],
            gameglobal.roleCache[self.id]['picFrameId'])

    # def queryTransportGoodsLink(self, gbId):
    #     DEBUG_MSG('huyf: queryTransportGoodsLink', gbId)
    #     gameengine.getGlobalBase('PlayerStub').doOnOthersBase([gbId], 'handleQueryTransportGoodsLink', (self, 0, gbId, 0, 0), None, '', ())
    #
    # def handleQueryTransportGoodsLink(self, box, actId, gbId, helpNum, guildUUID):
    #     DEBUG_MSG('huyf: handleQueryTransportGoodsLink', box, actId, gbId, helpNum, guildUUID)
    #     # TODO not same guildUUID immediately return  tips message
    #     # 【【货运】点击非同一帮会的玩家的求助信息，没有消息提示，点击求助链接无响应】
    #     if not guildUUID or self.guildUUIDBase != guildUUID:
    #         box.onMessagePre(MMD.datas.guildFreight_notGuildMember, [])
    #         return
    #     self.transportGoodsInfo.lookCurTransportGoods(box, actId, gbId, helpNum)

    def sendTeamMatchMessage(self, exposed, teamId, content, teamTarget, curNum, channel):
        DEBUG_MSG('in sendTeamMatchMessage:', teamId, content, teamTarget, curNum, channel)
        if self.isAllServerForbidChat():
            self.onMessagePre(int(CCD.datas['chat_banned']['value']), [self.accountEntity.banAllServerPostReason,utils.getBanEndTimeString(self.accountEntity.banAllServerPostTime)])
            self.client.onSendForbidChat(self.accountEntity.banAllServerPostTime, self.accountEntity.banAllServerPostReason)
            return

        # 只处理自身目标和具体活动目标
        if teamTarget < 1:
            ERROR_MSG('in sendTeamMatchMessage, teamTarget error 1')
            return
        
        targetInfo = TMACTD.datas.get(teamTarget)
        if not targetInfo:
            ERROR_MSG('in sendTeamMatchMessage, teamTarget error 2')
            return
        
        actData = AC_ADD.datas.get(int(targetInfo['pareActivity']))
        if not actData:
            ERROR_MSG("in sendTeamMatchMessage, cfg is missing in activity control", teamTarget, targetInfo['pareActivity'])
            return
        
        chatMsgKey = ''
        teamMemberCount = 0
        recruitTips = None
        if gameconst.ActivityControlType.TEAM == int(actData['needTeam']):
            chatMsgKey = 'teamChannel_applyTeamMsg'
            teamMemberCount = gameconst.TEAM_MEMBER_MAX_NUM
        elif gameconst.ActivityControlType.RAID == int(actData['needTeam']):
            chatMsgKey = 'teamChannel_applyRaidMsg'
            teamMemberCount = gameconst.RAID_MEMBER_MAX_NUM
        else:
            ERROR_MSG("in sendTeamMatchMessage, cfg is wrong in activity control", teamTarget, targetInfo['pareActivity'], actData['needTeam'])
            return
        
        #活动：%s%d-%d级%s的队伍正在招募:<link team name=申请加入 teamId=%d>
        msg = MCM.datas[TMMCD.datas[chatMsgKey]['value']]['Message'].format(targetInfo['value'], content, curNum, teamMemberCount, teamId)

        now = utils.getNow()
        if gameconst.ChatChannel.GUILD == channel:
            guildMsgCD = TMMCD.datas.get('guildChannelCD', {}).get('value', 0)
            if self.sendMatchTeamGuildMsgTime + guildMsgCD > now:
                self.onMessagePre(MMD.datas.zhaomuMessageCD, [str(self.sendMatchTeamGuildMsgTime + guildMsgCD - now)])
                return
            self.sendMatchTeamGuildMsgTime = now
            self._sendMsgToGuild(msg, includeMe=True, isTeamZhaomu=True)
        elif gameconst.ChatChannel.RECRUIT == channel or gameconst.ChatChannel.TEAM == channel or gameconst.ChatChannel.RAID == channel:
            zhaomuChannelCD = TMMCD.datas.get('zhaomuChannelCD', {}).get('value', 0)
            if self.sendMatchTeamRecruitMsgTime + zhaomuChannelCD > now:
                self.onMessagePre(MMD.datas.zhaomuMessageCD, [str(self.sendMatchTeamRecruitMsgTime + zhaomuChannelCD - now)])
                return
            self.sendMatchTeamRecruitMsgTime = now
            self.sendTeamMatchRecruitMsg(channel, msg)
            self.onMessagePre(MMD.datas.recruitSent, [])

    def sendTeamMatchRecruitMsg(self, channel, msg):
        if self.isSilentChat(gameconst.SilentSpeakScene.CHAT):
            self.cell.handleTeamChannelMatchTeamMsg(self._getChatChannelAvatarInfo(), channel, msg)
        else:
            gameengine.broadcastBaseapp('broadcastToAllAvatar',
                                        (gameconst.CELL, 'handleTeamChannelMatchTeamMsg',
                                         (self._getChatChannelAvatarInfo(), channel, msg)))

    # 调用前检查对应分享限制条件
    def sendChannelShareMsg(self, channel, msg):
        if channel == gameconst.ChatChannel.WORLD:
            self.sendWorldChatMsg(msg)
        elif channel == gameconst.ChatChannel.GUILD:
            self.sendGuildChatMsg(msg)
        elif channel == gameconst.ChatChannel.TEAM:
            self.sendTeamChatMsg(self.teamIdBase, msg)
        elif channel == gameconst.ChatChannel.RAID:
            self.sendRaidChatMsg(self.raidUUIDBase, msg)
        else:
            WARNING_MSG('IChat::sendChannelShareMsg need add share channel !!!')

    # def isForbidVoiceChat(self):
    #     if self.accountEntity.forbidVoiceChatFlag:
    #         if self.accountEntity.forbidVoiceChatType == gameconst.ForbidType.FOREVER_FORBID:
    #             return True
    #         elif self.accountEntity.forbidVoiceChatType == gameconst.ForbidType.SHORT_FORBID:
    #             if utils.getNow() <= self.accountEntity.forbidVoiceChatTime:
    #                 return True
    #
    #     return False
    #
    # def isForbidChat(self):
    #     if self.accountEntity.forbidChatFlag:
    #         if self.accountEntity.forbidChatType == gameconst.ForbidType.FOREVER_FORBID:
    #             return True
    #         elif self.accountEntity.forbidChatType == gameconst.ForbidType.SHORT_FORBID:
    #             if utils.getNow() <= self.accountEntity.forbidChatTime:
    #                 return True
    #
    #     return False

    # def getForbidRestTime(self):
    #     if self.accountEntity.forbidChatType == gameconst.ForbidType.FOREVER_FORBID:
    #         return -1
    #     elif self.accountEntity.forbidChatType == gameconst.ForbidType.SHORT_FORBID:
    #         return self.accountEntity.forbidChatTime - utils.getNow()


    def isAllServerForbidChat(self):
        if self.accountEntity.banAllServerPostTime:
            if self.accountEntity.banAllServerPostTime == -1 or self.accountEntity.banAllServerPostTime>utils.getNow():
                return True

        return False

    def isSilentChat(self,chatState):
        if self.silentSpeakState & 1 << chatState:
            if chatState == gameconst.SilentSpeakScene.CHAT and utils.getNow() <= self.silentSpeakTime:
                return True
            elif chatState == gameconst.SilentSpeakScene.FRIEND_CHAT and utils.getNow() <= self.silentFriendSpeakTime:
                return True

        return False

    def silentSpeak(self,chatScence,endTime):
        if chatScence == gameconst.SilentSpeakScene.FRIEND_CHAT:
            self.silentSpeakState = self.silentSpeakState | gameconst.SilentSpeakState.SET_FRIEND_CHAT
            self.silentFriendSpeakTime = endTime
        elif chatScence == gameconst.SilentSpeakScene.CHAT:
            self.silentSpeakState = self.silentSpeakState | gameconst.SilentSpeakState.SET_CHAT
            self.silentSpeakTime = endTime
        elif chatScence == gameconst.SilentSpeakScene.ALL:
            self.silentSpeakState = self.silentSpeakState | gameconst.SilentSpeakState.SET_ALL
            self.silentFriendSpeakTime = endTime
            self.silentSpeakTime = endTime

    def removeSilentSpeak(self,chatScence):
        if chatScence == gameconst.SilentSpeakScene.FRIEND_CHAT:
            self.silentSpeakState = self.silentSpeakState & gameconst.SilentSpeakState.REMOVE_FRIEND_CHAT
        elif chatScence == gameconst.SilentSpeakScene.CHAT:
            self.silentSpeakState = self.silentSpeakState & gameconst.SilentSpeakState.REMOVE_CHAT
        elif chatScence == gameconst.SilentSpeakScene.ALL:
            self.silentSpeakState = self.silentSpeakState & gameconst.SilentSpeakState.REMOVE_ALL

    def isVoiceChat(self,message):
        return message.startswith('{') and message.endswith('}') and len(message)>128 and message.find('#')>=0

    # 注意：语音消息适用，否则会报异常
    def getVoiceFileID(self, message):
        end = message.index('#')
        return message[1:end]

    # 注意：语音消息适用，否则会报异常
    def getVoiceContent(self, message):
        start = message.index('#')
        start = message.index('#', start+1)
        return message[start:-1]

    def onRecvAvatarChannelMsgPre(self, channel, avatarInfo, msg):
        DEBUG_MSG("onRecvAvatarChannelMsgPre::", channel, avatarInfo, msg)
        self.client.onRecvAvatarChannelMsg(channel, avatarInfo, msg)
        
