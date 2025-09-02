# -*- coding: utf-8 -*-
from KBEDebug import *
import KBEngine

import gameconst
import iBaseWithCell
import iFubenSpace

class Creation(iBaseWithCell.IBaseWithCell, iFubenSpace.IFubenSpace):

    def __init__(self):
        super(Creation, self).__init__()

        return

    def onLoseCell(self, reason=gameconst.OnLoseCellReason.DEFAULT):
        if self.isDestroyed:
            return

        self.destroy(writeToDB=False)
        return
