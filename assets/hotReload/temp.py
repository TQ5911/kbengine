# -*- coding: utf-8 -*-
from KBEDebug import *
import KBEngine
def refreshCell():
    import Avatar
    def checkSpecialVisible(self, name, type, funcList, *args):
        LOG_DBG('checkSpecialVisible cell', name, type, funcList, *args)
        for func in funcList:
            if not func:
                continue
            if not hasattr(self, func):
                continue
            if getattr(self, func)(*args):
                continue
            LOG_DBG('checkSpecialVisible cell false', func)
            return False
        LOG_DBG('checkSpecialVisible cell success')
        return True
    Avatar.Avatar.checkSpecialVisible = checkSpecialVisible
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
