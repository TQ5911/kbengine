import KBEngine, utils, sMath
from KBEDebug import *
import iBaseWithCell
import gameconst

class CoreAreaFlag(iBaseWithCell.IBaseWithCell):

    def __init__(self):
        pass

    def onLoseCell(self, reason=gameconst.OnLoseCellReason.DEFAULT):
        if self.isDestroyed:
            return

        self.destroy(writeToDB=False)
        return
