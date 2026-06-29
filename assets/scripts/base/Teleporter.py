# -*- coding: utf-8 -*-
from KBEDebug import *

import gameconst

import iBaseWithCell



class Teleporter(iBaseWithCell.IBaseWithCell):

    def __init__(self):
        super(Teleporter, self).__init__()

    def onLoseCell(self, reason=gameconst.OnLoseCellReasonEnum.DEFAULT):
        if self.isDestroyed:
            return

        self.destroy(writeToDB=False)
        return
