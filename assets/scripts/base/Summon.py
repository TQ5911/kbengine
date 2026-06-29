# -*- coding: utf-8 -*-
from KBEDebug import *

import gameconst

import iBaseWithCell
import iFubenSpace

class Summon(iBaseWithCell.IBaseWithCell, iFubenSpace.IFubenSpace):

    def __init__(self, **kwargs):
        super(Summon, self).__init__()

    def onLoseCell(self, reason=gameconst.OnLoseCellReasonEnum.DEFAULT):
        if self.isDestroyed:
            return

        self.destroy(writeToDB=False)
