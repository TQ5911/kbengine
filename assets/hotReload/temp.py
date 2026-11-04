# -*- coding: utf-8 -*-
from KBEDebug import *
import KBEngine
def refreshCell():
    # --auto genterate mark--
    pass
def refreshBase():
    import gameconfig
    import iBindPhone
    def sendSecondaryPasswordInfo(self):
        LOG_DBG('IBindPhone::sendSecondaryPasswordInfo1', self.getSecondaryPwdInfo())
        LOG_INFO('IBindPhone::sendSecondaryPasswordInfo2', self.getSecondaryPwdInfo().toStreamClientDic())
        if self.isCrossServerInLocalServer:
            self.syncMethodCallToCrossClient('sendSecondaryPasswordInfo', (self.getSecondaryPwdInfo().toStreamClientDic(),))
        elif gameconfig.isCrossServer():
            self.syncMethodCallToLocalServerBase('sendSecondaryPasswordInfo', ())
        else:
            self.client.sendSecondaryPasswordInfo(self.getSecondaryPwdInfo().toStreamClientDic())
    iBindPhone.IBindPhone.sendSecondaryPasswordInfo = sendSecondaryPasswordInfo
    # --auto genterate mark--
    pass
def refreshInterface():
    # --auto genterate mark--
    pass
if KBEngine.component == 'cellapp':
    refreshCell()
else:
    refreshBase()
