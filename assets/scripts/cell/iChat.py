# -*- coding: utf-8 -*-

import KBEngine
from KBEDebug import *

import utils
import gameconst

class IChat(object):

    def handleAvatarChannelMsg(self, channel, avatarInfo, msg):
        if gameconst.ChatChannelEnum.NEARBY == channel:
            for e in self.entitiesInRange(gameconst.DEFAULT_AOI, 'Avatar'):
                if e.id == self.id:
                    continue

                e.client.onRecvAvatarChannelMsg(gameconst.ChatChannelEnum.NEARBY, avatarInfo, msg)

    def handleTeamChannelMatchTeamMsg(self, avatarInfo, channel, msg):
        self.client.onRecvAvatarChannelMsg(channel, avatarInfo, msg)

    def _getChatChannelAvatarInfo(self):
        return utils.buildChatChannelAvatarData(
            self.id, self.gbId, self.school, self.name, self.level, self.sex, self.appearance.outfitData.picFrameId)

    def checkUseTrumpet(self, gridId, itemId, useNum, useItemCtx):
        LOG_DBG('in checkUseTrumpet:', gridId, itemId, useNum, useItemCtx)
        self.setPendingCheckId(gridId, itemId, useNum, useItemCtx, False)
        msg = useItemCtx.argsList[0]
        self.base.checkUseTrumpetBase(useItemCtx.pendingOpId,msg)
        return gameconst.UseItem.PENDING

    def afterCheckTrumpetMsg(self, pendingCheckId, originalMsg):
        LOG_DBG("afterCheckTrumpetMsg", originalMsg)

        pendingIdDict = self.getTempMiscProp(gameconst.EntityPropsEnum.pendingCheckUseItem, {})
        pendingData =pendingIdDict[pendingCheckId]
        if pendingData:
            pendingData[3].argsList = [originalMsg]
        self.onPendingCheckItem(pendingCheckId, gameconst.UseItem.TRUE)
