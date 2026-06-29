# -*- coding: utf-8 -*-

import KBEngine
from KBEDebug import *

import utils
import gameconst

class IChat(object):

    def handleAvatarChannelMsg(self, channel, avatarInfo, msg):
        if gameconst.ChatChannelEnum.NEARBY == channel:
            for _e in self.entitiesInRange(gameconst.DEFAULT_AOI, 'Avatar'):
                if _e.id == self.id:
                    continue

                _e.client.onRecvAvatarChannelMsg(gameconst.ChatChannelEnum.NEARBY, avatarInfo, msg)

    def handleTeamChannelMatchTeamMsg(self, avatarInfo, channel, msg):
        self.client.onRecvAvatarChannelMsg(channel, avatarInfo, {"msg": msg, "code": 0, "voiceUrl": '', "msgType": 0})

