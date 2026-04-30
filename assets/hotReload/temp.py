# -*- coding: utf-8 -*-
from KBEDebug import *
import KBEngine
def refreshCell():
    import gameconst
    from BountyInfo import bountyItem
    import iBounty
    def setPreyInfo(self, preyDict):
        INFO_MSG('IBounty::setPreyInfo1', preyDict)
        preyItem = bountyItem()
        preyItem.initFromSyncDict(preyDict)
        self.preyFlag = preyItem.flag
        if preyItem.state in gameconst.BountyState.INVALID_CELL_SET_PREY_TYPE:
            DEBUG_MSG('IBounty::setPreyInfo set none', self.cellPreyInfo)
            preyItem = None
        self.cellPreyInfo = preyItem
        INFO_MSG('IBounty::setPreyInfo2', self.cellPreyInfo)
    iBounty.IBounty.setPreyInfo = setPreyInfo
    # --auto genterate mark--
    pass
def refreshBase():
    # --auto genterate mark--
    pass
def refreshInterface():
    # --auto genterate mark--
    pass
if KBEngine.component == 'cellapp':
    refreshCell()
else:
    refreshBase()
