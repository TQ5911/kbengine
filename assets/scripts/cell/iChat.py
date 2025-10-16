# -*- coding: utf-8 -*-

import KBEngine
from KBEDebug import *

import utils
import gameconst

class IChat(object):

    def handleAvatarChannelMsg(self, channel, avatarInfo, msg):
        if gameconst.ChatChannel.NEARBY == channel:
            for e in self.entitiesInRange(gameconst.DEFAULT_AOI, 'Avatar'):
                if e.id == self.id:
                    continue

                e.client.onRecvAvatarChannelMsg(gameconst.ChatChannel.NEARBY, avatarInfo, msg)

    def handleTeamChannelMatchTeamMsg(self, avatarInfo, channel, msg):
        self.client.onRecvAvatarChannelMsg(channel, avatarInfo, msg)

    def _getChatChannelAvatarInfo(self):
        return utils.buildChatChannelAvatarInfo(
            self.id, self.gbId, self.school, self.name, self.level, self.sex, self.appearance.outfitData.picFrameId)

    def checkUseTrumpet(self, gridId, itemId, useNum, useItemCtx):
        DEBUG_MSG('in checkUseTrumpet:', gridId, itemId, useNum, useItemCtx)
        self.setPendingCheckId(gridId, itemId, useNum, useItemCtx, False)
        msg = useItemCtx.argsList[0]
        self.base.checkUseTrumpetBase(useItemCtx.pendingOpId,msg)
        return gameconst.UseItem.PENDING

    def afterCheckTrumpetMsg(self, pendingCheckId, originalMsg):
        DEBUG_MSG("afterCheckTrumpetMsg", originalMsg)

        pendingIdDict = self.getTempMiscProp(gameconst.AvatarProps.pendingCheckUseItem, {})
        pendingData =pendingIdDict[pendingCheckId]
        if pendingData:
            pendingData[3].argsList = [originalMsg]
        self.onPendingCheckItem(pendingCheckId, gameconst.UseItem.TRUE)
