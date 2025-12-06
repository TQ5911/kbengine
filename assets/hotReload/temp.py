# -*- coding: utf-8 -*-
from KBEDebug import *
import KBEngine
def refreshCell():
    import iCell
    def onDelayTimerSafeDestroy(self):
        if self.isDestroyed:
            return
        self.delayDestroyTimerID = 0
        self.safeDestroy(forceDestroy=True)
    iCell.ICell.onDelayTimerSafeDestroy = onDelayTimerSafeDestroy
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
