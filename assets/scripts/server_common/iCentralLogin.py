from rpc import RpcChannel, TcpClient

import gameglobal
from proto.gameServerLogin_pb2 import GameServerInfo, VerifyAccountRequest, GameServer, CentralServer_Stub, \
    VerifyAccountReply, UpdateCharacterInfo, NewCharacterInfo, Void, AccountVal, AccountOfflineVal, AccountOnlineVal, LockLoginSwitchServerVal, UnlockLoginSwitchServerVal,\
    DeleteCharacterRequest

import proto.centralLogin_pb2 as centralLogin
from KBEDebug import *

import KBEngine
import utils
import gameconst
import gameconfig
import gamesql
import json

import time
import urllib.parse
import login_set as LSD
import message_Message as MMD
import antiAddictionSystem_config as AASC
import random
import SwitchServer
import gameclass
import gameengine

class LoginService(GameServer):
    def __init__(self, loginMgr, address, centralServerId):
        self.centralServerId = centralServerId
        self.loginMgr = loginMgr
        self.channel = RpcChannel.RpcChannel(self)
        self.centralServerStub = CentralServer_Stub(self.channel)

        self.channel.connect(address)

    def on_disconnected(self):
        self.loginMgr.onCentralServerDisonnected()

    def on_connected(self):
        self.loginMgr.onCentralServerConnected(self.centralServerId)

    def onVerifyLogin(self, rpc_controller, reply, done):
        accountName = reply.accountName
        accountType = reply.accountType
        channelId = reply.channelId
        banAccountTime = reply.banAccountTime
        banPostTime = reply.banPostTime
        banAccountReason = reply.banAccountReason
        banPostReason = reply.banPostReason
        res = reply.result
        userId = reply.userId
        otherJsonData = reply.otherJsonData
        otherData = json.loads(otherJsonData)
        self.loginMgr.onVerifyPlayerLogin(accountType, userId, accountName, res, channelId, banAccountTime, banPostTime,
                                          banAccountReason, banPostReason, otherData)

    def onKickAccount(self, rpc_controller, reply, done):
        LOG_INFO("onKickAccount", reply.accountName)
        accountType = reply.accountType
        accountName = reply.accountName
        kickReason = reply.kickReason
        stubs = gameengine.getLoginStubsByAccountName(accountName)
        gameclass.DuplicatedCallList(stubs).onKickAccount(accountType, accountName, kickReason)

    def onLockedLogin(self, rpc_controller, reply, done):
        LOG_INFO("onLockedLogin", reply.accountName)

        SwitchServer.SwitchServerUtils.switchServer(
            reply.gbId,
            reply.dbId,
            reply.serverId,
            reply.accountName,
            reply.accountType,
        )

    def activeTickCallback(self, rpc_controller, reply, done):
        return


class CentralServerInfo(object):
    def __init__(self, serverId, ip, port):
        self.serverId = serverId
        self.port = port
        self.ip = ip


class ICentralLogin(object):
    def __init__(self):
        self.accountCache = {}
        self.loginClientDic = {}
        self.centralServerDict = {}

        self.initCentralServers()

    def initCentralServers(self):
        if not (gameconfig.isReady() and gameconfig.enableCentralLogin()):
            return

        _serverId = gameconfig.serverId()
        if not _serverId:
            return

        centralServersInfo = gameconfig.centralServersInfo()
        for _serverInfo in centralServersInfo:
            _centralServerId = int(_serverInfo.get("centralServerId"))
            ip = _serverInfo.get("ip")
            port = int(_serverInfo.get("port"))
            self.centralServerDict[_centralServerId] = CentralServerInfo(_centralServerId, ip, port)
            self.connectCentralServer(_centralServerId)

    def connectAllCentralServer(self):
        for centralServerId, _ in self.centralServerDict.items():
            self.connectCentralServer(centralServerId)

    def connectCentralServer(self, centralServerId):
        if not (gameconfig.isReady() and gameconfig.enableCentralLogin()):
            return

        if centralServerId not in self.centralServerDict:
            LOG_ERR("connectCentralServer centralServerId not in centralServerDict", centralServerId,
                      self.centralServerDict)
            return

        loginClient = self.loginClientDic.get(centralServerId, None)
        if loginClient and loginClient.channel.dispatcher:
            return

        _serverId = gameconfig.serverId()
        if not _serverId:
            return

        csInfo = self.centralServerDict.get(centralServerId)
        LOG_DBG('ICentralLogin connecting central server:', csInfo.ip, csInfo.serverId, csInfo.port)
        self.loginClientDic[centralServerId] = LoginService(self, (csInfo.ip, csInfo.port), csInfo.serverId)

    def onCentralServerDisonnected(self):
        pass

    def onCentralServerConnected(self, centralServerId):
        pass

    def tagTypeCheck(self, otherData, extra, realAccountName):
        tagTypeStr = otherData["tagType"] if "tagType" in otherData else "1"
        tagTypeSet = set(tagTypeStr.split(","))

        # 白名单一律放行
        if str(gameconst.UserTagType.WHITE_LIST) in tagTypeSet:
            return True

        # 注册上限
        if extra and "isOverRegLimit" in extra:
            if extra["isOverRegLimit"]:
                LOG_INFO('check server limit error.')
                KBEngine.accountLoginResponse(realAccountName, realAccountName, b'', 0, gameconst.GAME_SERVER_ERR_MEET_REG_MAX)
                return False
            
        # 未开服
        nowTime = utils.curTS()
        openTime = gameconfig.serverOpenTime()
        if nowTime < openTime:
            LOG_INFO('check server open time limit.', nowTime, openTime, str(openTime - nowTime))
            KBEngine.accountLoginResponse(realAccountName, realAccountName, 
                    bytes(str(openTime - nowTime), encoding='utf-8'), 
                    0, gameconst.GAME_SERVER_ERR_SERVER_OPEN_TIME)
            return False

        tagTypeCode = 0b1
        for tagType in tagTypeSet:
            tagTypeCode |= 1 << (int(tagType) - 1)
        # 激活码用户允许进入封闭服务器
        permitLogin = gameconfig.permitLogin()
        LOG_INFO('check permit login', bin(tagTypeCode), bin(permitLogin), bin((tagTypeCode << 32) | permitLogin))
        if tagTypeCode & permitLogin:
            return True


        KBEngine.accountLoginResponse(realAccountName, realAccountName, bytes(str((tagTypeCode << 32) | permitLogin), encoding='utf-8'), 0, gameconst.GAME_SERVER_ERR_PERMIT)
        return False

    # 将在interfaces进程上执行账号验证相关逻辑
    def onVerifyPlayerLogin(self, accountType, userId, accountName, resCode, channelId=0, banAccountTime=0, banPostTime=0,
                            banAccountReason="", banPostReason="", otherData={}):
        realAccountName = utils.mixRealAccountName(accountType, accountName)
        userInfo = self.accountCache.pop(realAccountName, None)
        if not userInfo:
            return

        LOG_INFO('onVerifyLogin:', accountType, userId, accountName, resCode, userInfo, otherData)

        tid, token, dataBytes, extra = userInfo

        banAccountReason = urllib.parse.unquote(banAccountReason)
        banPostReason = urllib.parse.unquote(banPostReason)
        _clientData = utils.decClientData(dataBytes)
        _clientData.pop("banPostTime", None)
        _clientData.pop("banPostReason", None)
        _clientData.update({"channelId": channelId, "banAccountTime": banAccountTime, "userId": userId, "otherData": otherData})
        if banPostTime != 0:
            _clientData.update({"banPostTime": banPostTime, "banPostReason": banPostReason})
        dataBytes = utils.encClientData(_clientData)

        tid and KBEngine.delTimer(tid)
        _forceCompId = utils.getForceComponentID(realAccountName)

        if banAccountTime and (banAccountTime > utils.curTS() or banAccountTime == -1):
            fmtMessage = MMD.datas[LSD.datas['idip_accountBanned_msg']['value']]['Message']
            if banAccountTime == -1:
                KBEngine.accountLoginResponse(realAccountName, realAccountName, bytes(
                    fmtMessage.format(banAccountReason, LSD.datas['foreverText']['value']), encoding='utf-8'),
                                              _forceCompId,
                                              gameconst.GAME_SERVER_ERR_BAN_FOREVER)
            else:
                KBEngine.accountLoginResponse(realAccountName, realAccountName, bytes(
                    fmtMessage.format(banAccountReason,
                                      time.strftime("%Y年%m月%d日%H时%M分%S秒", time.localtime(banAccountTime))),
                    encoding='utf-8'), _forceCompId, gameconst.GAME_SERVER_ERR_BAN_WITH_TIME)
            return

        curAge = otherData.get('age', gameconst.LEGAL_AGE_OF_MAJORITY)
        antiAddictionSwitch = AASC.datas.get('antiAddictSwitchAge18', {}).get('value', 0)
        LOG_INFO('onVerifyLogin: antiAddictionData', antiAddictionSwitch, gameglobal.antiAddictionData, curAge)
        if utils.isMinorAccount(curAge) and (antiAddictionSwitch or gameglobal.antiAddictionData[0] == gameconst.AntiAddictionTimeType.PROHIBIT):
            #fmtMessage = MMD.datas[AASC.datas['antiAddictForbiddenTime']['value']]['Message']
            fmtMessage = ""
            KBEngine.accountLoginResponse(realAccountName, realAccountName, bytes(fmtMessage, encoding='utf-8'),
                                              _forceCompId,
                                              gameconst.GAME_SERVER_ERR_ANTI_ADDICT)
            return

        #白名单、激活码用户
        if not self.tagTypeCheck(otherData, extra, realAccountName):
            return

        if resCode == VerifyAccountReply.VERIFY_ACCOUNT_OK:

            if accountType == centralLogin.ACCOUNT_PASSWD:
                _responseCode = KBEngine.SERVER_ERR_LOCAL_PROCESSING
            else:
                _responseCode = KBEngine.SERVER_SUCCESS

            KBEngine.accountLoginResponse(realAccountName, realAccountName, dataBytes, _forceCompId, _responseCode)
            return
        KBEngine.accountLoginResponse(realAccountName, realAccountName, b'', _forceCompId, gameconst.GAME_SERVER_ERR_VERIFY_FAIL)

    # 将在interfaces进程上执行账号验证相关逻辑
    def checkPlayerLogin(self, realAccountName, data, centralServerId, extra=None):
        self._checkPlayerLoginOnCentralServer(realAccountName, data, centralServerId, extra)

    def _checkPlayerLoginOnCentralServer(self, realAccountName, data, centralServerId, extra=None):
        _accountType, _accountName = utils.fetchAccountTypeAndName(realAccountName)
        cacheKeyName = utils.mixRealAccountName(_accountType, _accountName)
        if not gameconfig.enableCentralLogin():
            self.accountCache[cacheKeyName] = (0, '', data, extra)
            self.onVerifyPlayerLogin(_accountType, "NOT:"+cacheKeyName, _accountName, VerifyAccountReply.VERIFY_ACCOUNT_OK)
            return

        if _accountType == centralLogin.ACCOUNT_UNKNOW:
            if gameconfig.enableBotLogin():
                self.accountCache[cacheKeyName] = (0, '', data, extra)
                self.onVerifyPlayerLogin(_accountType, "BOT:"+cacheKeyName, _accountName, VerifyAccountReply.VERIFY_ACCOUNT_OK)
                return
            else:
                LOG_ERR('check login err:', _accountName)
                self.accountCache[cacheKeyName] = (0, '', data, extra)
                self.onVerifyPlayerLogin(_accountType, "", _accountName, VerifyAccountReply.VERIFY_ACCOUNT_FAIL)
                return

        clientData = utils.decClientData(data)
        token = clientData.get('token', '')

        self.connectCentralServer(centralServerId)

        verifyRequest = VerifyAccountRequest()
        verifyRequest.accountType = _accountType
        verifyRequest.accountName = _accountName
        verifyRequest.token = token
        verifyRequest.hostId = gameconfig.serverId()

        loginClient = self.loginClientDic.get(centralServerId)
        if not loginClient:
            LOG_ERR("_checkPlayerLoginOnCentralServer:: invalid centralServerId", _accountName, centralServerId,
                      clientData)
            self.accountCache[cacheKeyName] = (0, token, data, extra)
            self.onVerifyPlayerLogin(_accountType, "", _accountName, VerifyAccountReply.VERIFY_ACCOUNT_FAIL)
            return

        loginClient.centralServerStub.verifyLogin(None, verifyRequest, None)

        tid = KBEngine.addTimer(7, 0, lambda tid: self._checkPlayerLoginTimeout(_accountType, _accountName))

        self.accountCache[cacheKeyName] = (tid, token, data, extra)

    # 将在interfaces进程上执行账号验证相关逻辑
    def _checkPlayerLoginTimeout(self, accountType, accountName):
        realAccountName = utils.mixRealAccountName(accountType, accountName)
        userInfo = self.accountCache.pop(realAccountName, None)
        if not userInfo:
            LOG_ERR('_checkPlayerLoginTimeout: invalid accountName', accountName)
            return

        tid, token, data, extra = userInfo
        realAccountName = utils.mixRealAccountName(accountType, accountName)
        KBEngine.accountLoginResponse(realAccountName, realAccountName, b'', 0, gameconst.GAME_SERVER_ERR_VERIFY_TIMEOUT)

    def registerServer(self, centralServerId):
        serverId = gameconfig.serverId()
        if not serverId:
            return

        LOG_INFO('register server on login:', serverId, centralServerId)

        _serverInfo = GameServerInfo()
        _serverInfo.hostId = serverId

        loginClient = self.loginClientDic.get(centralServerId)
        loginClient.centralServerStub.registerServer(None, _serverInfo, None)

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

        for _, _loginClient in self.loginClientDic.items():
            if _loginClient and _loginClient.channel.dispatcher:
                _loginClient.centralServerStub.updateServerInfo(None, serverInfo, None)

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

        _loginClient = self.loginClientDic.get(centralServerId)
        if not _loginClient:
            return
        _loginClient.centralServerStub.updateCharacter(None, info, None)

    def notifyCentralServerCreateAvatar(self, createInfo, centralServerId):
        self.connectCentralServer(centralServerId)

        _accountType, _accountName, _gbId, _name, _school, _sex = createInfo

        # TODO: charactorInfo structure
        info = NewCharacterInfo()
        info.accountType = _accountType
        info.accountName = _accountName
        info.gbId = _gbId
        info.name = _name
        info.level = 1
        info.school = _school
        info.sex = _sex
        info.hostId = gameconfig.serverId()

        loginClient = self.loginClientDic.get(centralServerId)
        loginClient.centralServerStub.onCreateCharacter(None, info, None)

    def _getRandomLoginClient(self):
        if not self.loginClientDic:
            return None

        return random.choice(list(self.loginClientDic.values()))

    def notifyCentralServerLoginComplete(self, accountType, accountName, centralServerId):
        self.connectCentralServer(centralServerId)

        _account = AccountVal()
        _account.accountType = accountType
        _account.accountName = accountName

        loginClient = self.loginClientDic.get(centralServerId)
        loginClient.centralServerStub.onLoginComplete(None, _account, None)

    def notifyCentralServerOnline(self, accountName, accountType, centralServerId, sessionIdStr, userInfoId):
        LOG_INFO("notifyCentralServerOnline", accountName, accountType, centralServerId, sessionIdStr, userInfoId)
        self.connectCentralServer(centralServerId)

        account = AccountOnlineVal()
        account.hostId = gameconfig.serverId()
        account.accountName = accountName
        account.accountType = accountType
        account.sessionIdStr = sessionIdStr
        account.userId = userInfoId

        loginClient = self.loginClientDic.get(centralServerId)
        if not loginClient:
            return
        
        loginClient.centralServerStub.onAccountOnline(None, account, None)

    def notifyCentralServerOffline(self, accountName, accountType, centralServerId, sessionIdStr, userInfoId):
        LOG_INFO("notifyCentralServerOffline", accountName, accountType, centralServerId, sessionIdStr, userInfoId)
        self.connectCentralServer(centralServerId)

        _account = AccountOfflineVal()
        _account.hostId = gameconfig.serverId()
        _account.accountName = accountName
        _account.accountType = accountType
        _account.sessionIdStr = sessionIdStr
        _account.userId = userInfoId

        loginClient = self.loginClientDic.get(centralServerId)
        if not loginClient:
            return

        loginClient.centralServerStub.onAccountOffline(None, _account, None)

    def deleteCharacter(self, gbId, centralServerId):
        """
        通知中心服务器删除角色
        """
        _req = DeleteCharacterRequest()
        _req.gbId = gbId

        _loginClient = self.loginClientDic.get(centralServerId)
        if not _loginClient:
            LOG_ERR("deleteCharacter:: invalid centralServerId", gbId, centralServerId)
            return

        _loginClient.centralServerStub.deleteCharacter(None, _req, None)

    def checkCentralServerActive(self, centralServerId):
        if gameconfig.enableCentralLogin():
            _loginClient = self.loginClientDic.get(centralServerId)
            _loginClient.centralServerStub.activeTick(None, Void(), None)

    def checkAllCentralServerActive(self):
        if gameconfig.enableCentralLogin():
            for _centralServerId, _ in self.centralServerDict.items():
                self.checkCentralServerActive(_centralServerId)

