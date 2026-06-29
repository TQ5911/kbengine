# -*- coding: utf-8 -*-
from KBEDebug import *

import gameconst
import iBaseWithCell


class Collection(iBaseWithCell.IBaseWithCell):

    def __init__(self):
        super(Collection, self).__init__()

        return

    def onLoseCell(self, reason=gameconst.OnLoseCellReasonEnum.DEFAULT):
        if self.isDestroyed:
            return

        self.destroy(writeToDB=False)
        return


