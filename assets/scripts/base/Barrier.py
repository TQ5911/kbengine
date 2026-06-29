# -*- coding: utf-8 -*-
from KBEDebug import *

import gameconst

import iBaseWithCell

import iFubenSpace

class Barrier(iBaseWithCell.IBaseWithCell, iFubenSpace.IFubenSpace):

    def __init__(self, **kwargs):
        super(Barrier, self).__init__()

    def onLoseCell(self, reason=gameconst.OnLoseCellReasonEnum.DEFAULT):
        if self.isDestroyed:
            return

        self.destroy(writeToDB=False)
