# -*- coding: utf-8 -*-

# 获取并缓存配置信息

import KBEngine
import ResMgr
import gameengine
import gameglobal
import time
import socket
import gameconst
import visible_visible as UVVD
from KBEDebug import *
import buyCredit_buyCredit

CID2CONFIG = {}
CONFIG = {}
CACHE_DIC = {}
configId = 1

INTERFACE_CACHE_DIFF = {}
CLIENT_CONFIG_DIFF_DIC = {}


class ConfigFlag(object):
    FLAG_NONE = 0
    FLAG_CLIENT = 1
    CACHE_CONFIG = 2
    ALWAYS_SEND_CLIENT = 3


def cache_wraper(func):
    def _innerFunc():
        global CACHE_DIC
        v = CACHE_DIC.get(func.__name__)
        if v is None:
            v = func()
            CACHE_DIC[func.__name__] = v
            if func.__name__ == "debugLevel":
                saveDebugLevel(func.__name__, v)
        return v

    # 第一次加载先主动读取一次配置
    _innerFunc()

    return _innerFunc


def Bool(s):
    if s.lower() == 'true':
        return True

    elif s.lower() == 'false':
        return False

    elif int(s) > 0:
        return True

    else:
        return False


def Int(s):
    return int(s)


def Str(s):
    return s


def Float(s):
    return float(s)


def config(convFunc, default, desc, flags=(ConfigFlag.FLAG_NONE,)):
    global CONFIG

    if isinstance(flags, int):
        flags = (flags,)

    def _config(func):
        global configId
        _name = func.__name__
        if _name not in CONFIG:
            if default is None:
                defaultStr = str(func())
            else:
                defaultStr = default

            if not isinstance(defaultStr, str):
                raise RuntimeError('Config %s default must be string!' % (_name,))

            try:
                defaultv = convFunc(defaultStr)
            except:
                raise RuntimeError('Config %s default value error!' % (_name,))

            if ConfigFlag.FLAG_CLIENT in flags:
                cid = configId
                configId += 1
                CID2CONFIG[cid] = _name
                # 默认值从表里读时无法做diff，每次都发给玩家
                if ConfigFlag.ALWAYS_SEND_CLIENT in flags:
                    CLIENT_CONFIG_DIFF_DIC[cid] = defaultv
            else:
                cid = 0

            CONFIG[_name] = (_name, convFunc, defaultStr, defaultv, desc, cid, flags)

        def _func():
            return KBEngine.globalData['CONFIG'][_name]

        return _func

    return _config

def initVisibleConfig():
    visibleSet = set()
    for key, data in UVVD.datas.items():
        visibleSet.add(data['type'])
    for key, data in buyCredit_buyCredit.datas.items():
        visibleSet.add("pay" + str(key))
        visibleSet.add("buyCreditType" + str(data['type']))
    for key in visibleSet:
        def _config():
            return 1
        _config.__name__ = key
        config(Bool, None, key, (ConfigFlag.FLAG_CLIENT, ConfigFlag.CACHE_CONFIG, ConfigFlag.ALWAYS_SEND_CLIENT))(_config)
initVisibleConfig()

# ----------------------  自定义配置项,修改后会存到数据库中  ----------------------
def isReady():
    return 'CONFIG' in KBEngine.globalData


@cache_wraper
def enableRouterServer():
    try:
        ret = int(ResMgr.getStringContentFromPath(ResMgr.kbengineConfig(), 'game/enableRouterServer'))
    except:
        ret = False
    return ret


@cache_wraper
def routerServersInfo():
    try:
        _routerServers = ResMgr.getStringContentListForPath(ResMgr.kbengineConfig(), 'game/routerServersInfo')
        _routerServersInfo = []
        for routerServer in _routerServers:
            _res = socket.getaddrinfo(routerServer['ip'], None)
            _address = _res[0][4][0]
            _csInfo = {'routerServerId': routerServer['routerServerId'], 'ip': _address, 'port': routerServer['port']}
            _routerServersInfo.append(_csInfo)
    except:
        _routerServersInfo = [{'routerServerId': '1', 'ip': '192.168.16.252', 'port': '2070'}]
    return _routerServersInfo

@cache_wraper
def getCrossServerId():
    try:
        data = ResMgr.getStringContentListForPath(ResMgr.kbengineConfig(), 'game/crossServerInfo')
        return int(data[0]['crossServerId'])
    except:
        LOG_WARN('[lj]crossServerInfo load fail')
        return 99999

@cache_wraper
def crossSiegeWarServerInfo():
    return {
        'crossServerId': getCrossServerId()
    }

def loadCustomConfig(data):
    import utils

    _config = {}
    KBEngine.globalData['CONFIG'] = _config

    LOG_DBG('loadCustomConfig', len(data))

    for name, value in data:
        v = CONFIG.get(utils.bytesToString(name))
        if not v:
            _sql = "DELETE FROM game_config WHERE name='%s'" % (utils.bytesToString(name),)
            KBEngine.executeRawDatabaseCommand(_sql)
            continue

        configName, convFunc, default, defaultV, desc, cid, flags = v
        _config[configName] = convFunc(utils.bytesToString(value))

        if _config[configName] != defaultV:
            setCustomCfg(configName, _config[configName], isMasterBaseapp=KBEngine.component == 'baseapp',
                            isInitSet=True)

    for v in CONFIG.values():
        configName, convFunc, default, defaultV, desc, cid, flags = v

        if configName in _config:
            continue

        if ConfigFlag.CACHE_CONFIG not in flags:
            _sql = "INSERT INTO game_config (name, value) VALUE(%s, %s)" % \
                  (utils.escape_string(configName), utils.escape_string(str(default)))
            KBEngine.executeRawDatabaseCommand(_sql)
        _config[configName] = defaultV

    KBEngine.globalData['CONFIG'] = _config


def onGameCfgChanged(name, value, fromBaseappGroupdOrder):
    # 从isBootstrap发起，所以bootstrap进程不需要设置
    # 这里触发下回调，有些开关可能打开或关闭一瞬间有操作
    _type = 0
    if name == 'wonderLand':
        _type = gameconst.GAME_CONFIG_TYPE_WONDER_LAND

    elif name == 'square':
        _type = gameconst.GAME_CONFIG_TYPE_SQUARE

    elif name == 'roleAuthorization':
        _type = gameconst.GAME_CONFIG_TYPE_ROLE_AUTHORIZATION

    elif name == 'autoCombat':
        _type = gameconst.GAME_CONFIG_TYPE_AUTO_COMBAT

    elif name == 'hotfixVersion' and gameglobal.localBaseApp:
        gameglobal.localBaseApp.broadcastToAllAvatar(
            gameconst.BASE,
            'sendHotfix',
            (value,)
        )

    if _type and gameglobal.localBaseApp:
        gameglobal.localBaseApp.broadcastToAllAvatar(
            gameconst.BASE,
            'onGameConfigChangedBase',
            (_type, value)
        )

    if KBEngine.getComponentGroupOrder() == fromBaseappGroupdOrder:
        return

    setCustomCfg(name, value, isMasterBaseapp=False)


def gmSetCutomConfig(name, value, isMasterBaseapp=True):
    _info = CONFIG.get(name)
    if not _info:
        return "cannot find config [%s]" % name, False

    configName, convFunc, *_ = _info
    try:
        v = convFunc(value)
    except:
        return "cannot assign [%s] to [%s]" % (value, name), False

    return setCustomCfg(name, v, isMasterBaseapp)


def gmGetCutomConfig(name):
    _info = CONFIG.get(name)
    if not _info:
        return "cannot find config [%s]" % name, False

    configName, convFunc, default, defaultV, desc, cid, flags = _info

    return KBEngine.globalData['CONFIG'][configName]


def setCustomCfg(name, value, isMasterBaseapp=True, isInitSet=False):
    import utils

    LOG_INFO('setCustomCfg', name, value)
    info = CONFIG.get(name)
    if not info:
        return "cannot find config [%s]" % name, False

    _configName, convFunc, default, _defaultV, desc, cid, flags = info

    if ConfigFlag.FLAG_CLIENT in flags:
        if value != _defaultV or ConfigFlag.ALWAYS_SEND_CLIENT in flags:
            CLIENT_CONFIG_DIFF_DIC[cid] = value
        else:
            CLIENT_CONFIG_DIFF_DIC.pop(cid, None)

    if isMasterBaseapp:
        if not isInitSet:
            _sql = "UPDATE game_config SET value=%s WHERE name=%s" % \
                  (utils.escape_string(str(value)), utils.escape_string(_configName))
            KBEngine.executeRawDatabaseCommand(_sql)

        KBEngine.globalData['CONFIG'][_configName] = value
        KBEngine.globalData['CONFIG'] = KBEngine.globalData['CONFIG']

        gameengine.callBaseApps('gameconfig.onGameCfgChanged', (name, value, KBEngine.getComponentGroupOrder()))
        if gameglobal.localBaseApp:
            gameglobal.localBaseApp.notifyInterfaceConfigChanged(name, str(value))

    elif KBEngine.component == 'interfaces':
        KBEngine.globalData['CONFIG'][_configName] = value

    enable = False if not value else True
    if cid and gameglobal.localBaseApp:
        gameglobal.localBaseApp.onBroadcastToAllClients(
            'onGameConfigChanged',
            ([CID2CONFIG[cid]], [enable]))

    return 'config [%s] to [%s] success' % (name, value), True


def getCacheConfig(name):
    cfgValue = CACHE_DIC.get(name, '')
    return cfgValue


def setCacheConfig(name, value):
    if name == "debugLevel":
        saveDebugLevel(name, value)
    oldVal = CACHE_DIC.get(name, '')
    try:
        newVal = type(oldVal)(value)
    except:
        gameengine.panicStack('cannot set %s to %s, type mismatch' % (name, value))
        return
    CACHE_DIC[name] = newVal
    INTERFACE_CACHE_DIFF[name] = newVal


def sendClientConfig(playerBox):
    vList = []
    cfgNameList = []
    #登录时只发关闭的功能
    for cid, v in CLIENT_CONFIG_DIFF_DIC.items():
        if not v:
            vList.append(False)
            cfgName = CID2CONFIG[cid]
            cfgNameList.append(cfgName)

    if cfgNameList:
        playerBox.client.onGameConfigChanged(cfgNameList, vList)


def unpackInterfaceDiffCache(nameStr, valueStr):
    names = nameStr.split('|')
    values = valueStr.split('|')
    return names, values


def packInterfaceDiffCache():
    _nameStr = '|'.join([str(i) for i in INTERFACE_CACHE_DIFF.keys()])
    _valueStr = '|'.join([str(i) for i in INTERFACE_CACHE_DIFF.values()])
    return _nameStr, _valueStr


@cache_wraper
def baseAppCount():
    try:
        strContent = ResMgr.getStringContentFromPath(ResMgr.kbengineConfig(), 'game/baseAppCount')
        cnt = int(strContent)
    except:
        cnt = 1

    return cnt


@cache_wraper
def cellAppCount():
    try:
        strContent = ResMgr.getStringContentFromPath(ResMgr.kbengineConfig(), 'game/cellAppCount')
        cnt = int(strContent)
    except:
        cnt = 1

    return cnt


@cache_wraper
def serverId():
    strContent = ResMgr.getStringContentFromPath(ResMgr.kbengineConfig(), 'game/serverId')
    if not strContent and KBEngine.component == 'bots':
        return 0
    return int(strContent)


@cache_wraper
def gmHostList():
    try:
        _gmServers = ResMgr.getStringContentListForPath(ResMgr.kbengineConfig(), 'game/gm')
        addrList = []
        for _gmServer in _gmServers:
            res = socket.getaddrinfo(_gmServer['ip'], None)
            csInfo = {'addr': res[0][4][0], 'port': _gmServer['port'], 'httpApi': _gmServer['httpApi']}
            addrList.append(csInfo)
    except:
        addrList = [{'addr': '10.219.68.119', 'port': '2040', 'httpApi': '8080'}, ]
    return addrList

@cache_wraper
def giftCodeUrl():
    try:
        url = ResMgr.getStringContentFromPath(ResMgr.kbengineConfig(), 'game/giftCodeUrl')
    except:
        url = ''
    return url

@cache_wraper
def tapTapBindPhoneReqUrl():
    try:
        url = ResMgr.getStringContentFromPath(ResMgr.kbengineConfig(), 'game/tapTapBindPhoneReqUrl')
    except:
        url = ''
    return url

@cache_wraper
def tapTapBindPhoneVerifyUrl():
    try:
        url = ResMgr.getStringContentFromPath(ResMgr.kbengineConfig(), 'game/tapTapBindPhoneVerifyUrl')
    except:
        url = ''
    return url

@cache_wraper
def reportUrl():
    try:
        url = ResMgr.getStringContentFromPath(ResMgr.kbengineConfig(), 'game/reportUrl')
    except:
        url = ''
    return url

@cache_wraper
def queryRechargeUrl():
    try:
        url = ResMgr.getStringContentFromPath(ResMgr.kbengineConfig(), 'game/queryRechargeUrl')
    except:
        url = ''
    return url

@cache_wraper
def patchVersion():
    try:
        versionStr = ResMgr.getStringContentFromPath(ResMgr.kbengineConfig(), 'game/patchVersion')
    except:
        versionStr = '0.0.0.0'
    return versionStr

@cache_wraper
def appVersion():
    try:
        versionStr = ResMgr.getStringContentFromPath(ResMgr.kbengineConfig(), 'game/appVersion')
    except:
        versionStr = '0.0.0.0'
    return versionStr

@cache_wraper
def gmHttpAPISecret():
    try:
        secret = ResMgr.getStringContentFromPath(ResMgr.kbengineConfig(), 'game/gmHttpSecret')
    except:
        secret = ''
    return secret


@cache_wraper
def socialTokenKey():
    try:
        secret = ResMgr.getStringContentFromPath(ResMgr.kbengineConfig(), 'game/socialTokenKey')
    except:
        secret = '15a47f73b656e28218684a2ad532f9bb'
    return secret


@cache_wraper
def socketConnectServerIP():
    try:
        socketConnectIp = ResMgr.getStringContentFromPath(ResMgr.kbengineConfig(), 'game/socketConnect/host')
    except:
        socketConnectIp = '192.168.16.131'
    return socketConnectIp


@cache_wraper
def socketConnectServerPort():
    try:
        socketConnectPort = int(ResMgr.getStringContentFromPath(ResMgr.kbengineConfig(), 'game/socketConnect/port'))
    except:
        socketConnectPort = 8002
    return socketConnectPort


@cache_wraper
def socketConnectIsSendMes():
    try:
        socketConnectIsSendMes = int(
            ResMgr.getStringContentFromPath(ResMgr.kbengineConfig(), 'game/socketConnect/isSendMes'))
    except:
        socketConnectIsSendMes = 0
    return socketConnectIsSendMes


@cache_wraper
def waitEntityLoading():
    try:
        waitLoading = ResMgr.getStringContentFromPath(ResMgr.kbengineConfig(), 'debug/waitEntityLoading')
        waitLoading = int(waitLoading)
    except:
        waitLoading = True
    return waitLoading


@cache_wraper
def entityLoadSpeed():
    try:
        _entityLoadSpeed = ResMgr.getStringContentFromPath(ResMgr.kbengineConfig(), 'debug/entityLoadSpeed')
        _entityLoadSpeed = int(_entityLoadSpeed)
        if _entityLoadSpeed <= 0:
            _entityLoadSpeed = 5
    except:
        _entityLoadSpeed = 20
    return _entityLoadSpeed


@cache_wraper
def needLoadEntity():
    try:
        needLoadEnt = ResMgr.getStringContentFromPath(ResMgr.kbengineConfig(), 'debug/loadEntity')
        needLoadEnt = int(needLoadEnt)
    except:
        needLoadEnt = True
    return needLoadEnt


@cache_wraper
def enableBotLogin():
    try:
        enableBot = ResMgr.getStringContentFromPath(ResMgr.kbengineConfig(), 'debug/enableBotLogin')
        enableBot = int(enableBot)
    except:
        enableBot = False
    return enableBot


@cache_wraper
def redisServer():
    try:
        '''
        url = ResMgr.getStringContentFromPath(ResMgr.kbengineConfig(), 'game/redisServer')
        res = socket.getaddrinfo(url, None)
        _address = res[0][4][0]
        '''
        _address = '192.168.10.172'
    except:
        _address = '192.168.10.13'
    return _address


@cache_wraper
def redisUsername():
    try:
        passwd = ResMgr.getStringContentFromPath(ResMgr.kbengineConfig(), 'game/redisUsername')
    except:
        passwd = ''
    return passwd


@cache_wraper
def redisPassword():
    try:
        passwd = ResMgr.getStringContentFromPath(ResMgr.kbengineConfig(), 'game/redisPassword')
    except:
        passwd = ''
    return passwd


@cache_wraper
def redisPort():
    try:
        port = int(ResMgr.getStringContentFromPath(ResMgr.kbengineConfig(), 'game/redisPort'))
    except:
        port = 6379
    return port


@cache_wraper
def elasticServer():
    try:
        url = ResMgr.getStringContentFromPath(ResMgr.kbengineConfig(), 'game/elasticServer')
        res = socket.getaddrinfo(url, None)
        _address = res[0][4][0]
    except:
        _address = ''
    return _address


@cache_wraper
def elasticUser():
    try:
        user = ResMgr.getStringContentFromPath(ResMgr.kbengineConfig(), 'game/elasticUser')
    except:
        user = ''

    return user


@cache_wraper
def elasticAuth():
    try:
        authStr = ResMgr.getStringContentFromPath(ResMgr.kbengineConfig(), 'game/elasticAuth')
    except:
        authStr = ''
    return authStr


@cache_wraper
def elasticEnable():
    try:
        enable = int(ResMgr.getStringContentFromPath(ResMgr.kbengineConfig(), 'game/elasticEnable'))
    except:
        enable = 0
    return enable


@cache_wraper
def elasticPort():
    try:
        port = int(ResMgr.getStringContentFromPath(ResMgr.kbengineConfig(), 'game/elasticPort'))
    except:
        port = 9200
    return port


@cache_wraper
def interfaceRpcHostList():
    try:
        _addrList = ResMgr.getStringContentListForPath(ResMgr.kbengineConfig(), 'game/interfaceRpc/host')
    except:
        _addrList = [{'addr': '127.0.0.1', 'port': '10080'}, ]
    return _addrList


@cache_wraper
def permitLogin():
    try:
        permit = int(ResMgr.getStringContentFromPath(ResMgr.kbengineConfig(), 'game/permitLogin'))
    except:
        permit = 1
    return permit


@cache_wraper
def gmVerifyByGroup():
    try:
        v = int(ResMgr.getStringContentFromPath(ResMgr.kbengineConfig(), 'game/gmVerifyByGroup'))
    except:
        v = 0
    return v

@functools.lru_cache(64)
def branchLineCnt(branchType):
    try:
        cnt = int(ResMgr.getStringContentFromPath(ResMgr.kbengineConfig(), 'game/branchLineCnt/subType' + str(branchType)))
    except:
        LOG_ERR('branchLineCnt load fail', branchType)
        cnt = 2
    return cnt

@cache_wraper
def combatMsgFlag():
    try:
        v = int(ResMgr.getStringContentFromPath(ResMgr.kbengineConfig(), 'debug/combatMsgFlag'))
    except:
        v = 0
    return v


@cache_wraper
def centralServersInfo():
    try:
        '''
        _centralServers = ResMgr.getStringContentListForPath(ResMgr.kbengineConfig(), 'game/centralServersInfo')
        centralServersInfo = []
        for _centralServer in _centralServers:
            res = socket.getaddrinfo(_centralServer['ip'], None)
            _address = res[0][4][0]
            csInfo = {'centralServerId': _centralServer['centralServerId'], 'ip': _address, 'port': _centralServer['port']}
            centralServersInfo.append(csInfo)
        '''
        centralServersInfo = [{'centralServerId': '1', 'ip': '192.168.10.172', 'port': '2030'}]
    except:
        centralServersInfo = [{'centralServerId': '1', 'ip': '10.219.68.119', 'port': '2030'}]
    return centralServersInfo

@cache_wraper
def dropServersInfo():
    try:
        dropServers = ResMgr.getStringContentListForPath(ResMgr.kbengineConfig(), 'game/dropServersInfo')
        dropServersInfo = []
        for ds in dropServers:
            res = socket.getaddrinfo(ds['ip'], None)
            address = res[0][4][0]
            info = {'dropServerId': ds['dropServerId'], 'ip': address, 'port': int(ds['port'])}
            dropServersInfo.append(info)
    except:
        dropServersInfo = []

    return dropServersInfo

@cache_wraper
def crossDataServerInfo():
    try:
        crossDataServers = ResMgr.getStringContentListForPath(ResMgr.kbengineConfig(), 'game/crossDataServerInfo')
        crossDataServersInfo = []
        for ds in crossDataServers:
            res = socket.getaddrinfo(ds['ip'], None)
            address = res[0][4][0]
            info = {'crossDataServerId': ds['crossDataServerId'], 'ip': address, 'port': int(ds['port'])}
            crossDataServersInfo.append(info)
    except:
        crossDataServersInfo = []

    return crossDataServersInfo


# 这里和服务端约定好格式为 android_version;ios_version;windows_version
@config(Str, '', 'hotfix version')
def hotfixVersion():
    return ''


@config(Bool, 'true', '是否连接admin')
def enableAdminServer():
    pass


@config(Bool, 'true', '是否允许GMT发起的命令')
def enableOutsideCommand():
    pass


@cache_wraper
def enableCentralLogin():
    try:
        v = int(ResMgr.getStringContentFromPath(ResMgr.kbengineConfig(), 'debug/enableCentralLogin'))
    except:
        v = 1
    return v


@config(Bool, None, '是否显示删除按钮')
def showAvatarRemoveButton():
    try:
        ret = int(ResMgr.getStringContentFromPath(ResMgr.kbengineConfig(), 'game/showAvatarRemoveButton'))
    except:
        ret = True
    return ret


@cache_wraper
def enableViewMgr():
    try:
        ret = int(ResMgr.getStringContentFromPath(ResMgr.kbengineConfig(), 'game/enableViewMgr'))
    except:
        ret = False

    return ret


@config(Bool, 'false', '是否开启战斗调试日志')
def enableCombatDebugLog():
    return True

@config(Bool, 'true', '是否开启场景生成创生物')
def loadCreation():
    return True

@config(Int, None, '注册人数配置')
def getServerRegLimit():
    try:
        _ret = int(ResMgr.getStringContentFromPath(ResMgr.kbengineConfig(), 'game/defaultLimitServerReg'))
    except:
        _ret = 8000
    return _ret


@config(Int, None, '注册开关配置')
def getServerRegSwitch():
    try:
        ret = int(ResMgr.getStringContentFromPath(ResMgr.kbengineConfig(), 'game/defaultEnableServerReg'))
    except:
        ret = 1
    return ret


@cache_wraper
def serverOpenTime():
    try:
        openTime = int(ResMgr.getStringContentFromPath(ResMgr.kbengineConfig(), 'game/serverOpenTime'))
    except:
        openTime = int(time.time())
    return openTime


@cache_wraper
def serverMaximumLoginAccount():
    try:
        _val = int(ResMgr.getStringContentFromPath(ResMgr.kbengineConfig(), 'game/maximumLoginAccount'))
    except:
        _val = 200 * cellAppCount()
    return _val

@cache_wraper
def maxCellAvatarCount():
    try:
        _val = int(ResMgr.getStringContentFromPath(ResMgr.kbengineConfig(), 'game/maxCellAvatarCount'))
    except:
        _val = 500
    return _val

@cache_wraper
def switchLineUselastLineNo():
    try:
        _val = int(ResMgr.getStringContentFromPath(ResMgr.kbengineConfig(), 'game/switchLineUselastLineNo'))
    except:
        _val = 1
    return _val

@cache_wraper
def shouldCheckAdminCmdSerial():
    try:
        enabled = int(ResMgr.getStringContentFromPath(ResMgr.kbengineConfig(), 'game/shouldCheckAdminCmdSerial'))
    except:
        enabled = 1
    return enabled


@cache_wraper
def debugLevel():
    try:
        debugLevel = int(ResMgr.getStringContentFromPath(ResMgr.kbengineConfig(), 'game/debugLevel'))
    except:
        debugLevel = 1
    return debugLevel


@cache_wraper
def serverCountry():
    try:
        country = ResMgr.getStringContentFromPath(ResMgr.kbengineConfig(), 'game/serverCountry')
    except:
        country = "中国"
    return country


@cache_wraper
def callbackNumThreshold():
    try:
        ret = int(ResMgr.getStringContentFromPath(ResMgr.kbengineConfig(), 'debug/callbackNumThreshold'))
    except:
        ret = 50
    return ret


@cache_wraper
def enableExposedMethodStats():
    try:
        enabled = ResMgr.getStringContentFromPath(ResMgr.kbengineConfig(), 'game/enableExposedMethodStats')
    except:
        enabled = 0
    return enabled


@cache_wraper
def wxErrNumPerSecond():
    try:
        ret = ResMgr.getStringContentFromPath(ResMgr.kbengineConfig(), 'game/wxErrNumPerSecond')
    except:
        ret = 5
    return int(ret)


@cache_wraper
def wxErrFlag():
    try:
        ret = ResMgr.getStringContentFromPath(ResMgr.kbengineConfig(), 'game/wxErrFlag')
    except:
        ret = 1
    return int(ret)


@cache_wraper
def mapleAllServerUrl():
    try:
        ret = ResMgr.getStringContentFromPath(ResMgr.kbengineConfig(), 'game/mapleAllServerUrl')
    except:
        ret = ''
    return ret

def getYidunData(tail):
    try:
        ret = ResMgr.getStringContentFromPath(ResMgr.kbengineConfig(), 'yidun/' + tail)
    except:
        ret = ''
        LOG_ERR("getYidunData fail", tail)
    return ret

#默认都是开易盾，私服不开
def getYidunEnable():
    try:
        ret = ResMgr.getStringContentFromPath(ResMgr.kbengineConfig(), 'yidun/enable')
    except:
        ret = 1
    return ret

@cache_wraper
def gameId():
    try:
        ret = ResMgr.getStringContentFromPath(ResMgr.kbengineConfig(), 'game/gameId')
    except:
        ret = 'fengyan'
    return ret


@cache_wraper
def tlogFlag():
    try:
        ret = ResMgr.getStringContentFromPath(ResMgr.kbengineConfig(), 'game/tlogFlag')
    except:
        ret = 0
    return int(ret)


@cache_wraper
def logFlag():
    try:
        ret = ResMgr.getStringContentFromPath(ResMgr.kbengineConfig(), 'game/logFlag')
    except:
        ret = 2
    return int(ret)


@cache_wraper
def loginLinePlayerNumLimit():
    try:
        ret = ResMgr.getStringContentFromPath(ResMgr.kbengineConfig(), 'game/login_line_playernum_limit')
    except:
        ret = 10
    return int(ret)


@cache_wraper
def interfaceEnableLogin():
    try:
        ret = int(ResMgr.getStringContentFromPath(ResMgr.kbengineConfig(), 'game/interfaceEnableLogin'))
    except:
        ret = 1
    return ret


@cache_wraper
def enableRsysLogLog():
    try:
        ret = int(ResMgr.getStringContentFromPath(ResMgr.kbengineConfig(), 'game/enableRsysLogLog'))
    except:
        ret = 0

    return ret


@cache_wraper
def feishuIp():
    feishuInfoList = []
    try:
        feishuInfo = ResMgr.getStringContentListForPath(ResMgr.kbengineConfig(), 'game/feishu')
        for ipInfo in feishuInfo:
            print(ipInfo)
            res = socket.getaddrinfo(ipInfo['ip'], None)
            address = res[0][4][0]
            feishuInfoList.append(address + ":" + ipInfo['port'])
    except:
        feishuInfoList = ['192.168.11.132:8010', ]
    return feishuInfoList


@config(Bool, None, '是否开启改名', (ConfigFlag.FLAG_CLIENT, ConfigFlag.CACHE_CONFIG, ConfigFlag.ALWAYS_SEND_CLIENT))
def enableModifyName():
    return 1


@config(Bool, None, '是否开启邮件', (ConfigFlag.FLAG_CLIENT, ConfigFlag.CACHE_CONFIG, ConfigFlag.ALWAYS_SEND_CLIENT))
def enableMail():
    return 1


@config(Bool, None, '是否使用注销旧流程', (ConfigFlag.FLAG_CLIENT, ConfigFlag.CACHE_CONFIG, ConfigFlag.ALWAYS_SEND_CLIENT))
def enableOldLogout():
    return 1


@config(Bool, None, '是否开启伤害统计', (ConfigFlag.CACHE_CONFIG, ))
def enableStatistic():
    try:
        ret = int(ResMgr.getStringContentFromPath(ResMgr.kbengineConfig(), 'game/enableStatistic'))
    except:
        ret = 0
    return ret

@config(Bool, None, '是否开启交易行', (ConfigFlag.FLAG_CLIENT, ConfigFlag.CACHE_CONFIG, ConfigFlag.ALWAYS_SEND_CLIENT))
def enableAuction():
    return 1

@cache_wraper
def auctionServerHost():
    try:
        host = ResMgr.getStringContentFromPath(ResMgr.kbengineConfig(), 'game/auctionServerHost')
    except:
        host = '192.168.10.31:2010'
    return host

@cache_wraper
def leaseServerAddress():
    try:
        host = ResMgr.getStringContentFromPath(ResMgr.kbengineConfig(), 'game/leaseServerHost')
    except:
        host = '127.0.0.1:2015'
    return host

@config(Bool, None, '是否开启租赁行', (ConfigFlag.FLAG_CLIENT, ConfigFlag.CACHE_CONFIG, ConfigFlag.ALWAYS_SEND_CLIENT))
def enableLease():
    return 1

@cache_wraper
def isCrossServer():
    return getCrossServerId() == serverId()

@config(Bool, 'true', '是否开启城战')
def enableSiegeWar():
    return True

@cache_wraper
def httpCmdIdempotent():
    '''
    http cmd 命令小写
    开放无状态幂等（即收到重复请求，返回数据一样）
    '''
    return ()


@cache_wraper
def enableDrawCube():
    """
    是否开启向客户端下发调试协议，用来展示服务端打击位置
    """
    try:
        val = ResMgr.getStringContentFromPath(ResMgr.kbengineConfig(), 'debug/enableDrawCube')
    except:
        val = 0

    return int(val)


@cache_wraper
def debugErrorLogHost():
    try:
        '''
        host = ResMgr.getStringContentFromPath(ResMgr.kbengineConfig(), 'debug/debugErrorLogHost')
        '''
        # 往我的 wxReportUrl里发
        host = ''
    except:
        host = ''

    return host

@cache_wraper
def wxReportUrl():
    try:
        '''
        host = ResMgr.getStringContentFromPath(ResMgr.kbengineConfig(), 'game/errReportUrl')
        '''
        host = 'https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=e7a6e5a5-18d0-4a5c-be78-01b4827e208b'
    except:
        host = 'https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=92de3ed1-9bfe-4428-afc6-f1488f9bb452'
    return host


@config(Bool, None, '是否开启工坊制造', (ConfigFlag.FLAG_CLIENT, ConfigFlag.CACHE_CONFIG, ConfigFlag.ALWAYS_SEND_CLIENT))
def enableWorkshop():
    return 1


def visibleConfigEnabled(configName):
    info = CONFIG.get(configName)
    if not info:
        LOG_ERR('gameconfig not found:', configName)
        return

    configName, convFunc, default, defaultV, desc, cid, flags = info

    v = KBEngine.globalData['CONFIG'][configName]
    if not v:
        return False

    return True


def payConfigEnable(code, buyCreditId):
    name = code + str(buyCreditId)
    info = CONFIG.get(name)
    if not info:
        return True

    configName, convFunc, default, defaultV, desc, cid, flags = info

    v = KBEngine.globalData['CONFIG'][configName]
    if not v:
        return False

    return True

@cache_wraper
def speedStatConditions():
    return [5.0, 10.0, 15.0, 20.0, 25.0, 30.0, 35.0, 40.0, 45.0, 50.0, 55.0, 60.0, 65.0, 70.0, 75.0, 80.0, 85.0, 90.0, 95.0, 100.0]

@cache_wraper
def orderServerHost():
    try:
        host = ResMgr.getStringContentFromPath(ResMgr.kbengineConfig(), 'game/orderServerHost')
    except:
        host = '192.168.10.13:2011'
    return host

@config(Bool, None, '是否开启订单服务', (ConfigFlag.FLAG_CLIENT, ConfigFlag.CACHE_CONFIG, ConfigFlag.ALWAYS_SEND_CLIENT))
def enableOrderService():
    return 1

@cache_wraper
def overSpeedCheckSwitch():
    return 1


@cache_wraper
def isWaitMapServer():
    try:
        val = ResMgr.getStringContentFromPath(ResMgr.kbengineConfig(), 'game/isWaitMapServer')
        return Bool(val)
    except:
        return False


@cache_wraper
def waitMapMaxOnline():
    try:
        val = ResMgr.getStringContentFromPath(ResMgr.kbengineConfig(), 'game/waitMapMaxOnline')
        return int(val)
    except:
        return 2000
