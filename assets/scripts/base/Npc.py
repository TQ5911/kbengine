# -*- coding: utf-8 -*-
from KBEDebug import *
import KBEngine

import gameconst

import iBaseWithCell
import iFubenSpace


class Npc(iBaseWithCell.IBaseWithCell, iFubenSpace.IFubenSpace):

    def __init__(self):
        super(Npc, self).__init__()
        LOG_DBG("--------create npc", self.id)
        return

    def onLoseCell(self, reason=gameconst.OnLoseCellReason.DEFAULT):
        if self.isDestroyed:
            return

        self.destroy(writeToDB=False)
        return

