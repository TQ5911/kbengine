import KBEngine, utils, sMath
from KBEDebug import *
import NPC_teleporter as NPC_T, iBaseWithCell
import gameconst

class CityBattleTeleporter(iBaseWithCell.IBaseWithCell):

    def __init__(self):
        pass

    def onLoseCell(self, reason=gameconst.OnLoseCellReason.DEFAULT):
        if self.isDestroyed:
            return

        self.destroy(writeToDB=False)
        return
