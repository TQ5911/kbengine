# -*- coding: utf-8 -*-
from KBEDebug import *

import gameengine
import utils
import gameglobal
import gameconst

import iBaseWithCell

import iFubenSpace

class RebornPos(iBaseWithCell.IBaseWithCell, iFubenSpace.IFubenSpace):

    def __init__(self):
        super(RebornPos, self).__init__()


        return

    def onLoseCell(self, reason=gameconst.OnLoseCellReason.DEFAULT):
        if self.isDestroyed:
            return

        self.destroy(writeToDB=False)
        return
