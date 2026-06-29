# -*- coding: utf-8 -*-
from KBEDebug import *
import KBEngine

import gameconst
import iFubenSpace
import iBaseWithCell

class Monster(iBaseWithCell.IBaseWithCell, iFubenSpace.IFubenSpace):

    def __init__(self, **kwargs):
        super(Monster, self).__init__()

    def onLoseCell(self, reason=gameconst.OnLoseCellReasonEnum.DEFAULT):
        if self.isDestroyed:
            return

        self.destroy(writeToDB=False)
