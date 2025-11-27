# -*- coding: utf-8 -*-
from KBEDebug import *
import KBEngine
def refreshCell():
    # --auto genterate mark--
    pass
def refreshBase():
    import KBEngine
    import gameengine
    import utils
    import gametimer
    import gameconst
    import gameglobal
    import gameclass
    import iCycleEvent
    import gameconfig
    import Account
    def __init__(self):
        KBEngine.Proxy.__init__(self)
        iCycleEvent.ICycleEvent.__init__(self)
        self.avatarID = 0
        self.shouldAutoBackup = False
        loginJsonData, _ = self.getClientDatas(gameconst.ClientCallChannel.MAIN_CHANNEL)
        clientData = utils.decodeClientData(loginJsonData)
        self.centralServerId = clientData.get('loginServerId', 1)
        self.accountType, self.accountName = utils.getAccountTypeAndName(self.__ACCOUNT_NAME__)
        self.serverId = gameconfig.serverId()
        self.onDailyEvent()
        self._hasLoadData = False
        accountId = clientData.get('accountId', '')
        DEBUG_MSG('ZTQ Account ', accountId)
        devicePlatId = clientData.get('devicePlatId', 0)
        channelId = clientData.get('channelId', 0)
        self.udid = clientData.get('deviceUniqueIdentifier', '')
        self.devicePlatId = devicePlatId
        self.channelId = channelId
        stubs = gameengine.getLoginStubsByAccountName(self.__ACCOUNT_NAME__)
        gameclass.DuplicatedCallList(stubs).onAccountCreated(self.accountName, devicePlatId, self.isNewAccount, channelId)
        if self.isNewAccount:
            self.isNewAccount = False
        gameglobal.localAccountCache[self.__ACCOUNT_NAME__] = self
        if self.isCrossServer:
            crossServerToken = clientData.get('crossServerToken')
            gameengine.getGlobalBase('CrossServerStub').checkCrossServerToken(self.accountName, crossServerToken, self, 'onCheckCrossServerTokenRet', (crossServerToken,))
        self.callbackList = []
        self._callback(0.1, 'loadSwitchServerRecrod', (), gametimer.TIMER_TAG_LOAD_SWITCH_SERVER_RECORD)
        _interval = 5 * 60
        self.pyAddTimer(_interval, _interval, gametimer.ACCOUNT_WRITE_CHAR)
    Account.Account.__init__ = __init__
    # --auto genterate mark--
    pass
def refreshInterface():
    # --auto genterate mark--
    pass
if KBEngine.component == 'cellapp':
    refreshCell()
else:
    refreshBase()
