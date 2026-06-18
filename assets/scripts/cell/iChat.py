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
        self.client.onRecvAvatarChannelMsg(channel, avatarInfo, {"msg": msg, "code": 0, "voiceUrl": '', "msgType": 0})

    def _getChatChannelAvatarInfo(self):
        return utils.buildChatChannelAvatarData(
            self.id, self.gbId, self.school, self.name, self.level, self.sex, self.appearance.outfitData.picFrameId)