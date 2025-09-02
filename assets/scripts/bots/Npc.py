# -*- encoding:utf-8 -*-

import KBEngine
from KBEDebug import *
from NpcBase import NpcBase

class Npc(NpcBase):
    def __init__(self):
        KBEngine.Entity.__init__(self)
        DEBUG_MSG("CNpc::__init__:%s." % (self.__dict__))

    def aiChatToPlayer(self, *args):
        pass

    def onBornAction(self, *args):
        pass