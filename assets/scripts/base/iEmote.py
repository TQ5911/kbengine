# coding: utf-8

from KBEDebug import *
import KBEngine
import gamedecorator

class IEmote(object):
    def __init__(self):
        LOG_DBG("IEmote::__init__")

    def checkPlayEmoteCond(self, emoteId):
        LOG_DBG("IEmote::checkPlayEmoteCond", emoteId)

        # 目前都开放的,到时候检测玩家是否拥有
        #if False:
        # self.onMessagePre(, [])
        self.cell.onCheckPlayEmoteCond(emoteId)
