# -*- coding: utf-8 -*-
from KBEDebug import *
import KBEngine
def refreshCell():
    # --auto genterate mark--
    pass
def refreshBase():
    import KBEngine
    import gameconst
    import json
    import gameconfig
    import proto.centralLogin_pb2 as centralLogin
    import functools
    import gamedecorator
    import AuthClsWraper
    import iBindPhone
    @gamedecorator.limitcall(1)
    @AuthClsWraper.onlyHost
    def smsServiceVerifyCode(self, exposed, code, opType):
        LOG_INFO('IBindPhone::smsServiceVerifyCode', code, opType, self.accountEntity.accountType, self.accountName, self.accountEntity.phone)
        if self.accountEntity.accountType != centralLogin.ACCOUNT_OFFICIAL:
            LOG_WARN('IBindPhone::smsServiceVerifyCode accountType error')
            return
        if self.accountEntity.phone == 0:
            LOG_WARN('IBindPhone::smsServiceVerifyCode bind phone first')
            return
        if not self.checkValidVerifyCode(code):
            return
        if self.controlReqSMSServiceLimit(gameconst.EntityPropsEnum.verifySMSServiceTimestamp, 3):
            return
        checkRes, typeStr = self.checkSMSOperationType(opType)
        if not checkRes:
            return
        url = gameconfig.smsServiceVerifyUrl()
        message = json.dumps({'phone': str(self.accountEntity.phone), 'gameId': str(gameconfig.gameId()), 'code': str(code), 'type': str(typeStr)})
        LOG_INFO('IBindPhone::smsServiceVerifyCode url', url, message)
        KBEngine.urlopenv2(url, functools.partial(self._smsServiceVerifyCodeResponse, opType), method='POST', postData=message.encode('utf-8'), headers={'Content-Type': 'application/json', 'satoken': self.accountEntity.webToken}, timeoutSec=5)
    iBindPhone.IBindPhone.smsServiceVerifyCode = smsServiceVerifyCode
    # --auto genterate mark--
    pass
def refreshInterface():
    # --auto genterate mark--
    pass
if KBEngine.component == 'cellapp':
    refreshCell()
else:
    refreshBase()
