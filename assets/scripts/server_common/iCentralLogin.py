from rpc import RpcChannel, TcpClient

import gameglobal
from proto.gameServerLogin_pb2 import GameServerInfo, VerifyAccountRequest, GameServer, CentralServer_Stub, \
    VerifyAccountReply, UpdateCharacterInfo, NewCharacterInfo, Void, AccountVal, AccountOfflineVal, LockLoginSwitchServerVal, UnlockLoginSwitchServerVal
import proto.centralLogin_pb2 as centralLogin
from KBEDebug import *

import KBEngine
import utils
import gameconst
import gameconfig
import gamesql
import json

import hashlib
import time
import urllib.parse
import login_set as LSD
import message_Message as MMD
import antiAddictionSystem_config as AASC
import random
import SwitchServer


class LoginService(GameServer):
    def __init__(self, loginMgr, address, centralServerId):
        self.loginMgr = loginMgr
        self.centralServerId = centralServerId
        self.channel = RpcChannel.RpcChannel(self)
        self.centralServerStub = CentralServer_Stub(self.channel)

        self.channel.connect(address)

    def on_connected(self):
        self.loginMgr.onCentralServerConnected(self.centralServerId)

    def on_disconnected(self):
        self.loginMgr.onCentralServerDisonnected()

    def onVerifyLogin(self, rpc_controller, reply, done):
        accountType = reply.accountType
        accountName = reply.accountName
        channelId = reply.channelId
        banAccountTime = reply.banAccountTime
        banPostTime = reply.banPostTime
        banAccountReason = reply.banAccountReason
        banPostReason = reply.banPostReason
        res = reply.result
        accountId = reply.accountId
        otherJsonData = reply.otherJsonData
        otherData = json.loads(otherJsonData)
        self.loginMgr.onVerifyPlayerLogin(accountType, accountId, accountName, res, channelId, banAccountTime, banPostTime,
                                          banAccountReason, banPostReason, otherData)

    def onKickAccount(self, rpc_controller, reply, done):
        INFO_MSG("onKickAccount", reply.accountName)
        accountType = reply.accountType
        accountName = reply.accountName
        kickReason = reply.kickReason
        self.loginMgr.onKickAccount(accountType, accountName, kickReason)

    def onLockedLogin(self, rpc_controller, reply, done):
        INFO_MSG("onLockedLogin", reply.accountName)

        SwitchServer.SwitchServerUtils.switchServer(
            reply.gbId,
            reply.dbId,
            reply.serverId,
            reply.accountName,
            reply.accountType,
        )

    def activeTickCallback(self, rpc_controller, reply, done):
        pass


class CentralServerInfo(object):
    def __init__(self, serverId, ip, port):
        self.serverId = serverId
        self.ip = ip
        self.port = port


class ICentralLogin(object):
    def __init__(self):
        self.accountCache = {}
        self.loginClientDic = {}
        self.centralServerDic = {}

        self.initCentralServers()

    def initCentralServers(self):
        if gameconfig.isReady() and not gameconfig.enableCentralLogin():
            return

        serverId = gameconfig.serverId()
        if not serverId:
            return

        centralServersInfo = gameconfig.centralServersInfo()
        for serverInfo in centralServersInfo:
            centralServerId = int(serverInfo.get("centralServerId"))
            ip = serverInfo.get("ip")
            port = int(serverInfo.get("port"))
            self.centralServerDic[centralServerId] = CentralServerInfo(centralServerId, ip, port)
            self.connectCentralServer(centralServerId)

    def connectAllCentralServer(self):
        for centralServerId, _ in self.centralServerDic.items():
            self.connectCentralServer(centralServerId)

    def connectCentralServer(self, centralServerId):
        if gameconfig.isReady() and not gameconfig.enableCentralLogin():
            return

        if centralServerId not in self.centralServerDic:
            ERROR_MSG("connectCentralServer centralServerId not in centralServerDic", centralServerId,
                      self.centralServerDic)
            return

        loginClient = self.loginClientDic.get(centralServerId, None)
        if loginClient and loginClient.channel.dispatcher:
            return

        serverId = gameconfig.serverId()
        if not serverId:
            return

        csInfo = self.centralServerDic.get(centralServerId)
        DEBUG_MSG('ICentralLogin connecting central server:', csInfo.ip, csInfo.port, csInfo.serverId)
        self.loginClientDic[centralServerId] = LoginService(self, (csInfo.ip, csInfo.port), csInfo.serverId)

    def onCentralServerConnected(self, centralServerId):
        pass

    def onCentralServerDisonnected(self):
        pass

    # 将在interfaces进程上执行账号验证相关逻辑
    def onVerifyPlayerLogin(self, accountType, accountId, accountName, resCode, channelId=0, banAccountTime=0, banPostTime=0,
                            banAccountReason="", banPostReason="", otherData={}):
        realAccountName = utils.getRealAccountName(accountType, accountName)
        userInfo = self.accountCache.pop(realAccountName, None)
        if not userInfo:
            return

        INFO_MSG('onVerifyLogin:', accountType, accountId, accountName, resCode, userInfo, otherData)

        tid, token, dataBytes = userInfo

        banAccountReason = urllib.parse.unquote(banAccountReason)
        banPostReason = urllib.parse.unquote(banPostReason)
        clientData = utils.decodeClientData(dataBytes)
        clientData.pop("banPostTime", None)
        clientData.pop("banPostReason", None)
        clientData.update({"channelId": channelId, "banAccountTime": banAccountTime, "accountId": accountId, "otherData": otherData})
        if banPostTime != 0:
            clientData.update({"banPostTime": banPostTime, "banPostReason": banPostReason})
        dataBytes = utils.encodeClientData(clientData)

        tid and KBEngine.delTimer(tid)
        _forceCompId = utils.getForceComponentID(realAccountName)

        if banAccountTime and (banAccountTime > utils.getNow() or banAccountTime == -1):
            fmtMessage = MMD.datas[LSD.datas['idip_accountBanned_msg']['value']]['Message']
            if banAccountTime == -1:
                KBEngine.accountLoginResponse(realAccountName, realAccountName, bytes(
                    fmtMessage.format(banAccountReason, LSD.datas['foreverText']['value']), encoding='utf-8'),
                                              _forceCompId,
                                              KBEngine.SERVER_ERR_USER3)
            else:
                KBEngine.accountLoginResponse(realAccountName, realAccountName, bytes(
                    fmtMessage.format(banAccountReason,
                                      time.strftime("%Y年%m月%d日%H时%M分%S秒", time.localtime(banAccountTime))),
                    encoding='utf-8'), _forceCompId, KBEngine.SERVER_ERR_USER3)
            return

        curAge = otherData.get('age', gameconst.LEGAL_AGE_OF_MAJORITY)
        INFO_MSG('onVerifyLogin: antiAddictionData', gameglobal.antiAddictionData, curAge)
        if utils.isMinorAccount(curAge):#一测 and gameglobal.antiAddictionData[0] == gameconst.AntiAddictionTimeType.PROHIBIT:
            #fmtMessage = MMD.datas[AASC.datas['antiAddictForbiddenTime']['value']]['Message']
            fmtMessage = ""
            KBEngine.accountLoginResponse(realAccountName, realAccountName, bytes(fmtMessage, encoding='utf-8'),
                                              _forceCompId,
                                              KBEngine.SERVER_ERR_USER8)
            return

        if resCode == VerifyAccountReply.VERIFY_ACCOUNT_OK:

            if accountType == centralLogin.ACCOUNT_PASSWD:
                responseCode = KBEngine.SERVER_ERR_LOCAL_PROCESSING
            else:
                responseCode = KBEngine.SERVER_SUCCESS

            KBEngine.accountLoginResponse(realAccountName, realAccountName, dataBytes, _forceCompId, responseCode)
            return
        KBEngine.accountLoginResponse(realAccountName, realAccountName, b'', _forceCompId, KBEngine.SERVER_ERR_USER7)

    # 将在interfaces进程上执行账号验证相关逻辑
    def checkPlayerLogin(self, realAccountName, data, centralServerId):
        self._checkPlayerLoginOnCentralServer(realAccountName, data, centralServerId)

    def _checkPlayerLoginOnCentralServer(self, realAccountName, data, centralServerId):
        accountType, accountName = utils.getAccountTypeAndName(realAccountName)
        cacheKeyName = utils.getRealAccountName(accountType, accountName)
        if not gameconfig.enableCentralLogin():
            self.accountCache[cacheKeyName] = (0, '', data)
            self.onVerifyPlayerLogin(accountType, "NOT:"+cacheKeyName, accountName, VerifyAccountReply.VERIFY_ACCOUNT_OK)
            return

        if accountType == centralLogin.ACCOUNT_UNKNOW:
            if gameconfig.enableBotLogin():
                self.accountCache[cacheKeyName] = (0, '', data)
                self.onVerifyPlayerLogin(accountType, "BOT:"+cacheKeyName, accountName, VerifyAccountReply.VERIFY_ACCOUNT_OK)
                return
            else:
                ERROR_MSG('check login err:', accountName)
                self.accountCache[cacheKeyName] = (0, '', data)
                self.onVerifyPlayerLogin(accountType, "", accountName, VerifyAccountReply.VERIFY_ACCOUNT_FAIL)
                return

        clientData = utils.decodeClientData(data)
        token = clientData.get('token', '')

        self.connectCentralServer(centralServerId)

        verifyRequest = VerifyAccountRequest()
        verifyRequest.accountType = accountType
        verifyRequest.accountName = accountName
        verifyRequest.token = token
        verifyRequest.hostId = gameconfig.serverId()

        loginClient = self.loginClientDic.get(centralServerId)
        if not loginClient:
            ERROR_MSG("_checkPlayerLoginOnCentralServer:: invalid centralServerId", accountName, centralServerId,
                      clientData)
            self.accountCache[cacheKeyName] = (0, token, data)
            self.onVerifyPlayerLogin(accountType, "", accountName, VerifyAccountReply.VERIFY_ACCOUNT_FAIL)
            return

        loginClient.centralServerStub.verifyLogin(None, verifyRequest, None)

        tid = KBEngine.addTimer(7, 0, lambda tid: self._checkPlayerLoginTimeout(accountType, accountName))

        self.accountCache[cacheKeyName] = (tid, token, data)

    # 将在interfaces进程上执行账号验证相关逻辑
    def _checkPlayerLoginTimeout(self, accountType, accountName):
        realAccountName = utils.getRealAccountName(accountType, accountName)
        userInfo = self.accountCache.pop(realAccountName, None)
        if not userInfo:
            ERROR_MSG('_checkPlayerLoginTimeout: invalid accountName', accountName)
            return

        tid, token, data = userInfo
        realAccountName = utils.getRealAccountName(accountType, accountName)
        KBEngine.accountLoginResponse(realAccountName, realAccountName, b'', 0, KBEngine.SERVER_ERR_USER4)

    def registerServer(self, centralServerId):
        serverId = gameconfig.serverId()
        if not serverId:
            return

        INFO_MSG('register server on login:', serverId, centralServerId)

        serverInfo = GameServerInfo()
        serverInfo.hostId = serverId

        loginClient = self.loginClientDic.get(centralServerId)
        loginClient.centralServerStub.registerServer(None, serverInfo, None)

    def lockLoginSwitchServer(self, gbId, dbId, serverId, accountName, accountType):
        _req = LockLoginSwitchServerVal()
        _req.gbId = gbId
        _req.dbId = dbId
        _req.serverId = serverId
        _req.accountName = accountName
        _req.accountType = accountType

        _loginClient = self._getRandomLoginClient()
        _loginClient.centralServerStub.lockLoginSwitchServer(None, _req, None)

    def unlockLoginSwitchServer(self, accountName):
        _req = UnlockLoginSwitchServerVal()
        _req.accountName = accountName

        _loginClient = self._getRandomLoginClient()
        _loginClient.centralServerStub.unlockLoginSwitchServer(None, _req, None)

    def updateServerInfo(self):
        serverInfo = GameServerInfo()
        serverInfo.hostId = gameconfig.serverId()
        serverInfo.onlineNum = gameglobal.localLoginStub.getGlobalAccountNum()

        for _, loginClient in self.loginClientDic.items():
            if loginClient and loginClient.channel.dispatcher:
                loginClient.centralServerStub.updateServerInfo(None, serverInfo, None)

    def updateCharacterInfo(self, updateInfo, centralServerId):
        self.connectCentralServer(centralServerId)

        # 如果level是0就删除角色
        gbId, name, tLastLogin, delete, school, level, sex = updateInfo
        # TODO X: info structure
        info = UpdateCharacterInfo()
        info.gbId = gbId
        info.name = name
        info.level = level
        info.sex = sex
        info.school = school
        info.tLastLogin = tLastLogin
        info.delete = delete

        loginClient = self.loginClientDic.get(centralServerId)
        if not loginClient:
            return
        loginClient.centralServerStub.updateCharacter(None, info, None)

    def notifyCentralServerCreateAvatar(self, createInfo, centralServerId):
        self.connectCentralServer(centralServerId)

        accountType, accountName, gbId, name, school, sex = createInfo

        # TODO: charactorInfo structure
        info = NewCharacterInfo()
        info.accountType = accountType
        info.accountName = accountName
        info.gbId = gbId
        info.name = name
        info.level = 1
        info.school = school
        info.sex = sex
        info.hostId = gameconfig.serverId()

        loginClient = self.loginClientDic.get(centralServerId)
        loginClient.centralServerStub.onCreateCharacter(None, info, None)

    def _getRandomLoginClient(self):
        if not self.loginClientDic:
            return None

        return random.choice(list(self.loginClientDic.values()))

    def notifyCentralServerLoginComplete(self, accountType, accountName, centralServerId):
        self.connectCentralServer(centralServerId)

        account = AccountVal()
        account.accountType = accountType
        account.accountName = accountName

        loginClient = self.loginClientDic.get(centralServerId)
        loginClient.centralServerStub.onLoginComplete(None, account, None)

    def notifyCentralServerOffline(self, accountName, accountType, centralServerId):
        INFO_MSG("notifyCentralServerOffline", accountName, accountType, centralServerId)
        self.connectCentralServer(centralServerId)

        account = AccountOfflineVal()
        account.hostId = gameconfig.serverId()
        account.accountName = accountName
        account.accountType = accountType

        loginClient = self.loginClientDic.get(centralServerId)
        if not loginClient:
            return

        loginClient.centralServerStub.onAccountOffline(None, account, None)

    def checkCentralServerActive(self, centralServerId):
        if gameconfig.enableCentralLogin():
            loginClient = self.loginClientDic.get(centralServerId)
            loginClient.centralServerStub.activeTick(None, Void(), None)

    def checkAllCentralServerActive(self):
        if gameconfig.enableCentralLogin():
            for centralServerId, _ in self.centralServerDic.items():
                self.checkCentralServerActive(centralServerId)
