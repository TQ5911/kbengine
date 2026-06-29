# -*- coding: utf-8 -*-
import os
import KBEngine
from KBEDebug import *
import LoginManager
import asyncore
import utils
import gamesql
import gameconfig
import InterfaceRpcServer
import gameconst
import time
import login_set as LSD
import message_Message as MMD
import gameglobal
import httpcommon
import proto.centralLogin_pb2 as centralLogin
import urllib

"""
interfaces进程主要处理KBEngine服务端与第三方平台的接入接出工作。
(注意：由于interfaces是一个单线程服务器，如果需要使用python的http服务器库，建议使用异步的（例如：Tornado），否则会卡主线程造成阻塞)
目前支持几种功能:
1: 注册账号
	当客户端请求注册账号后，请求会由loginapp转发到dbmgr，如果dbmgr挂接了interfaces，则dbmgr将请求转发至这里（KBEngine.onRequestCreateAccount）
	此时脚本收到这个请求之后可以使用各种方式与第三方平台通信，可以使用python的http库也能直接使用socket，当与第三方平台交互完毕之后应该将
	交互的结果返回给引擎baseapp层，通过KBEngine.createAccountResponse能够将信息推送到baseapp层。

2：账号登陆
	当客户端请求登陆账号后，请求会由loginapp转发到dbmgr，如果dbmgr挂接了interfaces，则dbmgr将请求转发至这里（KBEngine.onRequestAccountLogin）
	此时脚本收到这个请求之后可以使用各种方式与第三方平台通信，可以使用python的http库也能直接使用socket，当与第三方平台交互完毕之后应该将
	交互的结果返回给引擎baseapp层层，通过KBEngine.accountLoginResponse能够将信息推送到baseapp层。

3：充值计费
	当baseapp上请求计费entity.charge()后，请求会由loginapp转发到dbmgr，如果dbmgr挂接了interfaces，则dbmgr将请求转发至这里（KBEngine.onRequestCharge）
	此时脚本收到这个请求之后可以使用各种方式与第三方平台通信，可以使用python的http库也能直接使用socket，当与第三方平台交互完毕之后应该将
	交互的结果返回给引擎baseapp层，通过KBEngine.chargeResponse能够将信息推送到baseapp层entity.charge时给入的回调或者回调到onLoseChargeCB接口。

	某些平台要求客户端直接与平台请求计费，平台采用回调服务器的方式来完成请求， 参考“平台回调”。

4: 平台回调
	要完成此功能应该在脚本层创建一个socket，
	并将socket挂接到KBEngine中（这样可防止阻塞导致主线程卡），然后监听指定的端口。
	使用KBE的KBEngine.registerReadFileDescriptor()和KBEngine.registerWriteFileDescriptor()，具体查看API文档与Poller.py。
"""

loginManager = None


def onInterfaceAppReady():
    """
    KBEngine method.
    interfaces已经准备好了
    """
    LOG_INFO('onInterfaceAppReady: bootstrapGroupIndex=%s, bootstrapGlobalIndex=%s' % \
             (os.getenv("KBE_BOOTIDX_GROUP"), os.getenv("KBE_BOOTIDX_GLOBAL")))

    KBEngine.globalData = {}

    KBEngine.addTimer(1, 0.1, tickAsyncore)
    KBEngine.addTimer(0, 5, initGameConfig)
    InterfaceRpcServer.startRpcServer()


def tickAsyncore(timerID):
    loginManager and loginManager.connectAllCentralServer()
    asyncore.loop(0, True, None, 1)


def initGameConfig(timerId):
    if not gameconfig.isReady():
        try:
            gamesql.getCustomConfig()
        except:
            pass
    else:
        global loginManager
        loginManager = LoginManager.LoginManager()
        KBEngine.delTimer(timerId)


def onInterfaceAppShutDown():
    """
    KBEngine method.
    这个interfaces被关闭前的回调函数
    """
    LOG_INFO('onInterfaceAppShutDown()')


def onRequestCreateAccount(registerName, password, datas):
    """
    KBEngine method.
    请求创建账号回调
    @param registerName: 客户端请求时所提交的名称
    @type  registerName: string

    @param password: 密码
    @type  password: string

    @param datas: 客户端请求时所附带的数据，可将数据转发第三方平台
    @type  datas: bytes
    """
    LOG_INFO('onRequestCreateAccount: registerName=%s' % (registerName))

    commitName = registerName

    # 默认账号名就是提交时的名
    realAccountName = commitName
    
    # 此处可通过http等手段将请求提交至第三方平台，平台返回的数据也可放入datas
    # datas将会回调至客户端
    # 如果使用http访问，因为interfaces是单线程的，同步http访问容易卡住主线程，建议使用
    # KBEngine.registerReadFileDescriptor()和KBEngine.registerWriteFileDescriptor()结合
    # tornado异步访问。也可以结合socket模拟http的方式与平台交互。

    KBEngine.createAccountResponse(commitName, realAccountName, datas, KBEngine.SERVER_SUCCESS)


def _onCheckBanAccount(result, err, realAccountName, password, dataBytes):
    LOG_INFO('_onCheckBanAccount: registerName', result, realAccountName)
    accountType, accountName = utils.fetchAccountTypeAndName(realAccountName)
    isNewAccount = False
    if len(result) == 0:
        isNewAccount = True
        if not loginManager:
            KBEngine.accountLoginResponse(realAccountName, realAccountName, b'', 0, gameconst.GAME_SERVER_ERR_NO_LOGIN_MGR)
            return

        switch = int(gameconfig.getServerRegSwitch())
        if not switch:
            LOG_INFO('_onCheckBanAccount check server switch error.', switch)
            KBEngine.accountLoginResponse(realAccountName, realAccountName, b'', 0, gameconst.GAME_SERVER_ERR_REG_SWITCH)
            return
    else:
        # forbidLoginFlag = int(result[0][0])
        # forbidLoginType = int(result[0][1])
        # forbidLoginTime = int(result[0][2])
        # forbidLoginReason = str(result[0][3].decode())
        isDelete = int(result[0][0])
        if isDelete:
            LOG_INFO('reject login,account delete', isDelete, realAccountName)
            fmtMessage = MMD.datas[LSD.datas['accountCancellation']['value']]['Message']
            KBEngine.accountLoginResponse(realAccountName, realAccountName, bytes(fmtMessage, encoding='utf-8'), 0,
                                          gameconst.GAME_SERVER_ERR_REJECT_LOGIN)
            return


    isOverRegLimit = isNewAccount and gameglobal.registerCount > int(gameconfig.getServerRegLimit())

    extra = {
        'isOverRegLimit': isOverRegLimit,
    }

    _onCheckPatchAndAppVersion(realAccountName, password, dataBytes, extra)


def onRequestAccountLogin(realAccountName, password, dataBytes):
    """
    KBEngine method.
    请求登陆账号回调
    @param loginName: 客户端请求时所提交的名称
    @type  loginName: string

    @param password: 密码
    @type  password: string

    @param datas: 客户端请求时所附带的数据，可将数据转发第三方平台
    @type  datas: bytes
    """
    LOG_INFO('onRequestAccountLogin: registerName', realAccountName, dataBytes)
    accountType, accountName = utils.fetchAccountTypeAndName(realAccountName)
    _forceCompId = utils.getForceComponentID(realAccountName)

    clientData = utils.decClientData(dataBytes)
    if accountType == centralLogin.ACCOUNT_CROSS_SERVER and clientData.get('crossServerToken'):
        KBEngine.accountLoginResponse(realAccountName, realAccountName, dataBytes, _forceCompId, KBEngine.SERVER_SUCCESS)
        return

    if not gameconfig.interfaceEnableLogin():
        KBEngine.accountLoginResponse(realAccountName, realAccountName, b'', _forceCompId, KBEngine.SERVER_ERR_SRV_STARTING)
        LOG_INFO('reject login, recovring cellapps')
        return

    gamesql.getForbidLoginProp(realAccountName,
                               lambda result, row, insertid, error: _onCheckBanAccount(result, error, realAccountName,
                                                                                       password, dataBytes))

    # 此处可通过http等手段将请求提交至第三方平台，平台返回的数据也可放入datas
    # datas将会回调至客户端
    # 如果使用http访问，因为interfaces是单线程的，同步http访问容易卡住主线程，建议使用
    # KBEngine.registerReadFileDescriptor()和KBEngine.registerWriteFileDescriptor()结合
    # tornado异步访问。也可以结合socket模拟http的方式与平台交互。

    # 如果返回码为KBEngine.SERVER_ERR_LOCAL_PROCESSING则表示验证登陆成功，但dbmgr需要检查账号密码，KBEngine.SERVER_SUCCESS则无需再检查密码
    # KBEngine.accountLoginResponse(commitName, realAccountName, datas, KBEngine.SERVER_SUCCESS)


def _onCheckPatchAndAppVersion(realAccountName, password, dataBytes, extra=None):
    accountType, accountName = utils.fetchAccountTypeAndName(realAccountName)
    if accountType not in (centralLogin.ACCOUNT_UNKNOW, centralLogin.ACCOUNT_BOT,):
        LOG_INFO('_onCheckPatchAndAppVersion1:', realAccountName)
        clientData = utils.decClientData(dataBytes)
        patchVer = clientData.get('patch', '')
        platId = clientData.get('devicePlatId', 0)
        
        patchVersion = gameconfig.patchVersion()
        newPatchVersion = gameglobal.requiredClientVersion.get(platId, patchVersion)
        patchVersion = newPatchVersion if utils.compare4stageversion(patchVersion, newPatchVersion) else patchVersion
        LOG_INFO('_onCheckPatchAndAppVersion2:', clientData, patchVer, platId, patchVersion, gameglobal.requiredClientVersion)
        if utils.compare4stageversion(patchVer, patchVersion):
            KBEngine.accountLoginResponse(realAccountName, realAccountName, 
                    bytes(str(patchVersion), encoding='utf-8'), 
                    0, gameconst.GAME_SERVER_ERR_PATCH_VERSION)
            return

    _requestAccountLogin(realAccountName, password, dataBytes, extra)

def _requestAccountLogin(realAccountName, password, dataBytes, extra=None):
    clientData = utils.decClientData(dataBytes)
    centralServerId = clientData.get('loginServerId', 0)
    if not loginManager:
        KBEngine.accountLoginResponse(realAccountName, realAccountName, b'', 0, gameconst.GAME_SERVER_ERR_NO_LOGIN_MGR2)
        return

    loginManager.checkPlayerLogin(realAccountName, dataBytes, centralServerId, extra)


def onRequestCharge(ordersID, entityDBID, datas):
    """
    KBEngine method.
    请求计费回调
    @param ordersID: 订单的ID
    @type  ordersID: uint64

    @param entityDBID: 提交订单的实体DBID
    @type  entityDBID: uint64

    @param datas: 客户端请求时所附带的数据，可将数据转发第三方平台
    @type  datas: bytes
    """

    # 此处可通过http等手段将请求提交至第三方平台，平台返回的数据也可放入datas
    # datas将会回调至baseapp的订单回调中，具体参考API手册charge
    # 如果使用http访问，因为interfaces是单线程的，同步http访问容易卡住主线程，建议使用
    # KBEngine.registerReadFileDescriptor()和KBEngine.registerWriteFileDescriptor()结合
    # tornado异步访问。也可以结合socket模拟http的方式与平台交互。

    # KBEngine.chargeResponse(ordersID, datas, KBEngine.SERVER_SUCCESS)
    pass
