# -*- coding: utf-8 -*-
from KBEDebug import *
import KBEngine
def refreshCell():
    # --auto genterate mark--
    pass
def refreshBase():
    import gameconfig
    import gamedecorator
    import iBag
    @gamedecorator.checkGameconfigEnable('bag')
    @gamedecorator.limitcall(1)
    @gamedecorator.crossServer
    def reqBagSort(self, exposed, bagType):
        if gameconfig.isCrossServer():
            self.syncMethodCallToLocalServerBase('_reqBagSort', (exposed, bagType))
        else:
            self._reqBagSort(exposed, bagType)
    iBag.IBag.reqBagSort = reqBagSort
    # --auto genterate mark--
    pass
def refreshInterface():
    # --auto genterate mark--
    pass
if KBEngine.component == 'cellapp':
    refreshCell()
else:
    refreshBase()
