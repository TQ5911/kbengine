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

CONFIG = {}
CID2CONFIG = {}
configId = 1
CACHE = {}

CLIENT_CONFIG_DIFF = {}
INTERFACE_CACHE_DIFF = {}


class ConfigFlag(object):
    NONE = 0
    CLIENT = 1
    CACHE_CONFIG = 2
    ALWAYS_SEND_CLIENT = 3


def cache(func):
    def _func():
        global CACHE
        v = CACHE.get(func.__name__)
        if v is None:
            v = func()
            CACHE[func.__name__] = v
            if func.__name__ == "debugLevel":
                saveDebugLevel(func.__name__, v)
        return v

    # 第一次加载先主动读取一次配置
    _func()

    return _func


def Bool(s):
    if s.lower() == 'true':
        return True

    if s.lower() == 'false':
        return False

    if int(s) > 0:
        return True
    else:
        return False

    raise ValueError('cannot convert to bool: %s' % s)


def Str(s):
    return s


def Int(s):
    return int(s)


def Float(s):
    return float(s)


def config(convFunc, default, desc, flags=(ConfigFlag.NONE,)):
    global CONFIG

    flags = (flags,) if type(flags) is int else flags

    def _config(func):
        global configId
        name = func.__name__
        if name not in CONFIG:
            if default is None:
                defaultStr = str(func())
            else:
                defaultStr = default

            if type(defaultStr) is not str:
                raise RuntimeError('Config %s default must be string!' % (name,))

            try:
                defaultv = convFunc(defaultStr)
            except:
                raise RuntimeError('Config %s default value error!' % (name,))

            if ConfigFlag.CLIENT in flags:
                cid = configId
                configId += 1
                CID2CONFIG[cid] = name
                # 默认值从表里读时无法做diff，每次都发给玩家
                if ConfigFlag.ALWAYS_SEND_CLIENT in flags:
                    CLIENT_CONFIG_DIFF[cid] = defaultv
            else:
                cid = 0

            CONFIG[name] = (name, convFunc, defaultStr, defaultv, desc, cid, flags)

        def _func():
            return KBEngine.globalData['CONFIG'][name]

        return _func

    return _config

def initVisibleConfig():
    visibleSet = set()
    for key, data in UVVD.datas.items():
        visibleSet.add(data['type'])
    for key in visibleSet:
        def _config():
            return 1
        _config.__name__ = key
        config(Bool, None, key, (ConfigFlag.CLIENT, ConfigFlag.CACHE_CONFIG, ConfigFlag.ALWAYS_SEND_CLIENT))(_config)
initVisibleConfig()

# ----------------------  自定义配置项,修改后会存到数据库中  ----------------------
def isReady():
    return 'CONFIG' in KBEngine.globalData


@cache
def enableRouterServer():
    try:
        ret = int(ResMgr.getStringContentForPath(ResMgr.kbengineConfig(), 'game/enableRouterServer'))
    except:
        ret = False
    return ret


@cache
def routerServersInfo():
    try:
        routerServers = ResMgr.getStringContentListForPath(ResMgr.kbengineConfig(), 'game/routerServersInfo')
        routerServersInfo = []
        for routerServer in routerServers:
            res = socket.getaddrinfo(routerServer['ip'], None)
            address = res[0][4][0]
            csInfo = {'routerServerId': routerServer['routerServerId'], 'ip': address, 'port': routerServer['port']}
            routerServersInfo.append(csInfo)
    except:
        routerServersInfo = [{'routerServerId': '1', 'ip': '192.168.16.252', 'port': '2070'}]
    return routerServersInfo

@cache
def getCrossServerId():
    try:
        data = ResMgr.getStringContentListForPath(ResMgr.kbengineConfig(), 'game/crossServerInfo')
        return int(data[0]['crossServerId'])
    except:
        WARNING_MSG('[lj]crossServerInfo load fail')
        return 20228

@cache
def crossSiegeWarServerInfo():
    return {
        'crossServerId': getCrossServerId()
    }

def loadCustomConfig(data):
    import utils

    config = {}
    KBEngine.globalData['CONFIG'] = config

    DEBUG_MSG('loadCustomConfig', len(data))

    for name, value in data:
        v = CONFIG.get(utils.getStringFromBytes(name))
        if not v:
            sql = "DELETE FROM game_config WHERE name='%s'" % (utils.getStringFromBytes(name),)
            KBEngine.executeRawDatabaseCommand(sql)
            continue

        configName, convFunc, default, defaultV, desc, cid, flags = v
        config[configName] = convFunc(utils.getStringFromBytes(value))

        if config[configName] != defaultV:
            setCustomConfig(configName, config[configName], isMasterBaseapp=KBEngine.component == 'baseapp',
                            isInitSet=True)

    for k, v in CONFIG.items():
        configName, convFunc, default, defaultV, desc, cid, flags = v

        if configName in config:
            continue

        if ConfigFlag.CACHE_CONFIG not in flags:
            sql = "INSERT INTO game_config (name, value) VALUE(%s, %s)" % \
                  (utils.escape_string(configName), utils.escape_string(str(default)))
            KBEngine.executeRawDatabaseCommand(sql)
        config[configName] = defaultV

    KBEngine.globalData['CONFIG'] = config


def onGameConfigChanged(name, value, fromBaseappGroupdOrder):
    # 从isBootstrap发起，所以bootstrap进程不需要设置
    # 这里触发下回调，有些开关可能打开或关闭一瞬间有操作
    _type = 0
    if name == 'wonderLand':
        _type = gameconst.GAME_CONFIG_TYPE_WONDER_LAND

    elif name == 'square':
        _type = gameconst.GAME_CONFIG_TYPE_SQUARE

    elif name == 'roleAuthorization':
        _type = gameconst.GAME_CONFIG_TYPE_ROLE_AUTHORIZATION

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

    setCustomConfig(name, value, isMasterBaseapp=False)


def gmSetCutomConfig(name, value, isMasterBaseapp=True):
    info = CONFIG.get(name)
    if not info:
        return "cannot find config [%s]" % name, False

    configName, convFunc, default, defaultV, desc, cid, flags = info
    try:
        v = convFunc(value)
    except:
        return "cannot assign [%s] to [%s]" % (value, name), False

    return setCustomConfig(name, v, isMasterBaseapp)


def gmGetCutomConfig(name):
    info = CONFIG.get(name)
    if not info:
        return "cannot find config [%s]" % name, False

    configName, convFunc, default, defaultV, desc, cid, flags = info

    return KBEngine.globalData['CONFIG'][configName]


def setCustomConfig(name, value, isMasterBaseapp=True, isInitSet=False):
    import utils

    INFO_MSG('setCustomConfig', name, value)
    info = CONFIG.get(name)
    if not info:
        return "cannot find config [%s]" % name, False

    configName, convFunc, default, defaultV, desc, cid, flags = info

    if ConfigFlag.CLIENT in flags:
        if value != defaultV or ConfigFlag.ALWAYS_SEND_CLIENT in flags:
            CLIENT_CONFIG_DIFF[cid] = value
        else:
            CLIENT_CONFIG_DIFF.pop(cid, None)

    if isMasterBaseapp:
        if not isInitSet:
            sql = "UPDATE game_config SET value=%s WHERE name=%s" % \
                  (utils.escape_string(str(value)), utils.escape_string(configName))
            KBEngine.executeRawDatabaseCommand(sql)

        KBEngine.globalData['CONFIG'][configName] = value
        KBEngine.globalData['CONFIG'] = KBEngine.globalData['CONFIG']

        gameengine.callBaseApps('gameconfig.onGameConfigChanged', (name, value, KBEngine.getComponentGroupOrder()))
        gameglobal.localBaseApp and gameglobal.localBaseApp.notifyInterfaceConfigChanged(name, str(value))

    elif KBEngine.component == 'interfaces':
        KBEngine.globalData['CONFIG'][configName] = value

    enable = False if not value else True
    cid and gameglobal.localBaseApp and gameglobal.localBaseApp.onBroadcastToAllClients('onGameConfigChanged',
                                                                                        ([CID2CONFIG[cid]], [enable]))

    return 'config [%s] to [%s] success' % (name, value), True


def setCacheConfig(name, value):
    if name == "debugLevel":
        saveDebugLevel(name, value)
    oldVal = CACHE.get(name, '')
    try:
        newVal = type(oldVal)(value)
    except:
        gameengine.reportCritical('cannot set %s to %s, type mismatch' % (name, value))
        return
    CACHE[name] = newVal
    INTERFACE_CACHE_DIFF[name] = newVal


def getCacheConfig(name):
    cfgValue = CACHE.get(name, '')
    return cfgValue


def sendClientConfig(playerBox):
    vList = []
    cfgNameList = []
    #登录时只发关闭的功能
    for cid, v in CLIENT_CONFIG_DIFF.items():
        if not v:
            vList.append(False)
            cfgName = CID2CONFIG[cid]
            cfgNameList.append(cfgName)

    if cfgNameList:
        playerBox.client.onGameConfigChanged(cfgNameList, vList)


def packInterfaceDiffCache():
    nameStr = '|'.join([str(i) for i in INTERFACE_CACHE_DIFF.keys()])
    valueStr = '|'.join([str(i) for i in INTERFACE_CACHE_DIFF.values()])
    return nameStr, valueStr


def unpackInterfaceDiffCache(nameStr, valueStr):
    names = nameStr.split('|')
    values = valueStr.split('|')
    return names, values


@cache
def baseAppCount():
    try:
        strContent = ResMgr.getStringContentForPath(ResMgr.kbengineConfig(), 'game/baseAppCount')
        cnt = int(strContent)
    except:
        cnt = 1

    return cnt


@cache
def cellAppCount():
    try:
        strContent = ResMgr.getStringContentForPath(ResMgr.kbengineConfig(), 'game/cellAppCount')
        cnt = int(strContent)
    except:
        cnt = 1

    return cnt


@cache
def serverId():
    strContent = ResMgr.getStringContentForPath(ResMgr.kbengineConfig(), 'game/serverId')
    if not strContent and KBEngine.component == 'bots':
        return 0
    return int(strContent)


@cache
def gmHostList():
    try:
        gmServers = ResMgr.getStringContentListForPath(ResMgr.kbengineConfig(), 'game/gm')
        addrList = []
        for gmServer in gmServers:
            res = socket.getaddrinfo(gmServer['ip'], None)
            csInfo = {'addr': res[0][4][0], 'port': gmServer['port'], 'httpApi': gmServer['httpApi']}
            addrList.append(csInfo)
    except:
        addrList = [{'addr': '10.219.68.119', 'port': '2040', 'httpApi': '8080'}, ]
    return addrList

@cache
def giftCodeUrl():
    try:
        url = ResMgr.getStringContentForPath(ResMgr.kbengineConfig(), 'game/giftCodeUrl')
    except:
        url = ''
    return url

@cache
def tapTapBindPhoneReqUrl():
    try:
        url = ResMgr.getStringContentForPath(ResMgr.kbengineConfig(), 'game/tapTapBindPhoneReqUrl')
    except:
        url = ''
    return url

@cache
def tapTapBindPhoneVerifyUrl():
    try:
        url = ResMgr.getStringContentForPath(ResMgr.kbengineConfig(), 'game/tapTapBindPhoneVerifyUrl')
    except:
        url = ''
    return url

@cache
def gmHttpAPISecret():
    try:
        secret = ResMgr.getStringContentForPath(ResMgr.kbengineConfig(), 'game/gmHttpSecret')
    except:
        secret = ''
    return secret


@cache
def socialTokenKey():
    try:
        secret = ResMgr.getStringContentForPath(ResMgr.kbengineConfig(), 'game/socialTokenKey')
    except:
        secret = '15a47f73b656e28218684a2ad532f9bb'
    return secret


@cache
def socketConnectServerIP():
    try:
        socketConnectIp = ResMgr.getStringContentForPath(ResMgr.kbengineConfig(), 'game/socketConnect/host')
    except:
        socketConnectIp = '192.168.16.131'
    return socketConnectIp


@cache
def socketConnectServerPort():
    try:
        socketConnectPort = int(ResMgr.getStringContentForPath(ResMgr.kbengineConfig(), 'game/socketConnect/port'))
    except:
        socketConnectPort = 8002
    return socketConnectPort


@cache
def socketConnectIsSendMes():
    try:
        socketConnectIsSendMes = int(
            ResMgr.getStringContentForPath(ResMgr.kbengineConfig(), 'game/socketConnect/isSendMes'))
    except:
        socketConnectIsSendMes = 0
    return socketConnectIsSendMes


@cache
def waitEntityLoading():
    try:
        waitLoading = ResMgr.getStringContentForPath(ResMgr.kbengineConfig(), 'debug/waitEntityLoading')
        waitLoading = int(waitLoading)
    except:
        waitLoading = True
    return waitLoading


@cache
def entityLoadSpeed():
    try:
        _entityLoadSpeed = ResMgr.getStringContentForPath(ResMgr.kbengineConfig(), 'debug/entityLoadSpeed')
        _entityLoadSpeed = int(_entityLoadSpeed)
        if _entityLoadSpeed <= 0:
            _entityLoadSpeed = 5
    except:
        _entityLoadSpeed = 20
    return _entityLoadSpeed


@cache
def needLoadEntity():
    try:
        needLoadEnt = ResMgr.getStringContentForPath(ResMgr.kbengineConfig(), 'debug/loadEntity')
        needLoadEnt = int(needLoadEnt)
    except:
        needLoadEnt = True
    return needLoadEnt


@cache
def enableBotLogin():
    try:
        enableBot = ResMgr.getStringContentForPath(ResMgr.kbengineConfig(), 'debug/enableBotLogin')
        enableBot = int(enableBot)
    except:
        enableBot = False
    return enableBot


@cache
def redisServer():
    try:
        '''
        url = ResMgr.getStringContentForPath(ResMgr.kbengineConfig(), 'game/redisServer')
        res = socket.getaddrinfo(url, None)
        address = res[0][4][0]
        '''
        address = '192.168.10.172'
    except:
        address = '192.168.16.252'
    return address


@cache
def redisPassword():
    try:
        passwd = ResMgr.getStringContentForPath(ResMgr.kbengineConfig(), 'game/redisPassword')
    except:
        passwd = ''
    return passwd


@cache
def redisPort():
    try:
        port = int(ResMgr.getStringContentForPath(ResMgr.kbengineConfig(), 'game/redisPort'))
    except:
        port = 6379
    return port


@cache
def elasticServer():
    try:
        url = ResMgr.getStringContentForPath(ResMgr.kbengineConfig(), 'game/elasticServer')
        res = socket.getaddrinfo(url, None)
        address = res[0][4][0]
    except:
        address = ''
    return address


@cache
def elasticUser():
    try:
        user = ResMgr.getStringContentForPath(ResMgr.kbengineConfig(), 'game/elasticUser')
    except:
        user = ''

    return user


@cache
def elasticAuth():
    try:
        authStr = ResMgr.getStringContentForPath(ResMgr.kbengineConfig(), 'game/elasticAuth')
    except:
        authStr = ''
    return authStr


@cache
def elasticEnable():
    try:
        enable = int(ResMgr.getStringContentForPath(ResMgr.kbengineConfig(), 'game/elasticEnable'))
    except:
        enable = 0
    return enable


@cache
def elasticPort():
    try:
        port = int(ResMgr.getStringContentForPath(ResMgr.kbengineConfig(), 'game/elasticPort'))
    except:
        port = 9200
    return port


@cache
def interfaceRpcHostList():
    try:
        addrList = ResMgr.getStringContentListForPath(ResMgr.kbengineConfig(), 'game/interfaceRpc/host')
    except:
        addrList = [{'addr': '127.0.0.1', 'port': '10080'}, ]
    return addrList


@cache
def permitLogin():
    try:
        permit = int(ResMgr.getStringContentForPath(ResMgr.kbengineConfig(), 'game/permitLogin'))
    except:
        permit = 1
    return permit


@cache
def gmVerifyByGroup():
    try:
        v = int(ResMgr.getStringContentForPath(ResMgr.kbengineConfig(), 'game/gmVerifyByGroup'))
    except:
        v = 0
    return v

@functools.lru_cache(64)
def branchLineCnt(branchType):
    try:
        cnt = int(ResMgr.getStringContentForPath(ResMgr.kbengineConfig(), 'game/branchLineCnt/subType' + str(branchType)))
    except:
        ERROR_MSG('branchLineCnt load fail', branchType)
        cnt = 2
    return cnt

@cache
def combatMsgFlag():
    try:
        v = int(ResMgr.getStringContentForPath(ResMgr.kbengineConfig(), 'debug/combatMsgFlag'))
    except:
        v = 0
    return v


@cache
def centralServersInfo():
    try:
        '''
        centralServers = ResMgr.getStringContentListForPath(ResMgr.kbengineConfig(), 'game/centralServersInfo')
        centralServersInfo = []
        for centralServer in centralServers:
            res = socket.getaddrinfo(centralServer['ip'], None)
            address = res[0][4][0]
            csInfo = {'centralServerId': centralServer['centralServerId'], 'ip': address, 'port': centralServer['port']}
            centralServersInfo.append(csInfo)
        '''
        centralServersInfo = [{'centralServerId': '1', 'ip': '192.168.10.172', 'port': '2030'}]
    except:
        centralServersInfo = [{'centralServerId': '1', 'ip': '10.219.68.119', 'port': '2030'}]
    return centralServersInfo

@cache
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

@cache
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


@cache
def enableCentralLogin():
    try:
        v = int(ResMgr.getStringContentForPath(ResMgr.kbengineConfig(), 'debug/enableCentralLogin'))
    except:
        v = 1
    return v


@config(Bool, None, '是否显示删除按钮')
def showAvatarRemoveButton():
    try:
        ret = int(ResMgr.getStringContentForPath(ResMgr.kbengineConfig(), 'game/showAvatarRemoveButton'))
    except:
        ret = True
    return ret


@cache
def enableViewMgr():
    try:
        ret = int(ResMgr.getStringContentForPath(ResMgr.kbengineConfig(), 'game/enableViewMgr'))
    except:
        ret = True
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
        ret = int(ResMgr.getStringContentForPath(ResMgr.kbengineConfig(), 'game/defaultLimitServerReg'))
    except:
        ret = 8000
    return ret


@config(Int, None, '注册开关配置')
def getServerRegSwitch():
    try:
        ret = int(ResMgr.getStringContentForPath(ResMgr.kbengineConfig(), 'game/defaultEnableServerReg'))
    except:
        ret = 1
    return ret


@cache
def serverOpenTime():
    try:
        openTime = int(ResMgr.getStringContentForPath(ResMgr.kbengineConfig(), 'game/serverOpenTime'))
    except:
        openTime = int(time.time())
    return openTime


@cache
def serverMaximumLoginAccount():
    try:
        _val = int(ResMgr.getStringContentForPath(ResMgr.kbengineConfig(), 'game/maximumLoginAccount'))
    except:
        _val = 200 * cellAppCount()
    return _val



@cache
def shouldCheckAdminCmdSerial():
    try:
        enabled = int(ResMgr.getStringContentForPath(ResMgr.kbengineConfig(), 'game/shouldCheckAdminCmdSerial'))
    except:
        enabled = 1
    return enabled


@cache
def debugLevel():
    try:
        debugLevel = int(ResMgr.getStringContentForPath(ResMgr.kbengineConfig(), 'game/debugLevel'))
    except:
        debugLevel = 1
    return debugLevel


@cache
def serverCountry():
    try:
        country = ResMgr.getStringContentForPath(ResMgr.kbengineConfig(), 'game/serverCountry')
    except:
        country = "中国"
    return country


@cache
def callbackNumThreshold():
    try:
        ret = int(ResMgr.getStringContentForPath(ResMgr.kbengineConfig(), 'debug/callbackNumThreshold'))
    except:
        ret = 50
    return ret


@cache
def enableExposedMethodStats():
    try:
        enabled = ResMgr.getStringContentForPath(ResMgr.kbengineConfig(), 'game/enableExposedMethodStats')
    except:
        enabled = 0
    return enabled


@cache
def wxErrNumPerSecond():
    try:
        ret = ResMgr.getStringContentForPath(ResMgr.kbengineConfig(), 'game/wxErrNumPerSecond')
    except:
        ret = 5
    return int(ret)


@cache
def wxErrFlag():
    try:
        ret = ResMgr.getStringContentForPath(ResMgr.kbengineConfig(), 'game/wxErrFlag')
    except:
        ret = 1
    return int(ret)


@cache
def mapleAllServerUrl():
    try:
        ret = ResMgr.getStringContentForPath(ResMgr.kbengineConfig(), 'game/mapleAllServerUrl')
    except:
        ret = ''
    return ret

@cache
def gameId():
    try:
        ret = ResMgr.getStringContentForPath(ResMgr.kbengineConfig(), 'game/gameId')
    except:
        ret = ''
    return ret


@cache
def tlogFlag():
    try:
        ret = ResMgr.getStringContentForPath(ResMgr.kbengineConfig(), 'game/tlogFlag')
    except:
        ret = 0
    return int(ret)


@cache
def logFlag():
    try:
        ret = ResMgr.getStringContentForPath(ResMgr.kbengineConfig(), 'game/logFlag')
    except:
        ret = 2
    return int(ret)


@cache
def loginLinePlayerNumLimit():
    try:
        ret = ResMgr.getStringContentForPath(ResMgr.kbengineConfig(), 'game/login_line_playernum_limit')
    except:
        ret = 10
    return int(ret)


@cache
def interfaceEnableLogin():
    try:
        ret = int(ResMgr.getStringContentForPath(ResMgr.kbengineConfig(), 'game/interfaceEnableLogin'))
    except:
        ret = 1
    return ret


@cache
def enableRsysLogLog():
    try:
        ret = int(ResMgr.getStringContentForPath(ResMgr.kbengineConfig(), 'game/enableRsysLogLog'))
    except:
        ret = 0

    return ret


@cache
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


@config(Bool, None, '是否开启改名', (ConfigFlag.CLIENT, ConfigFlag.CACHE_CONFIG, ConfigFlag.ALWAYS_SEND_CLIENT))
def enableModifyName():
    return 1


@config(Bool, None, '是否开启邮件', (ConfigFlag.CLIENT, ConfigFlag.CACHE_CONFIG, ConfigFlag.ALWAYS_SEND_CLIENT))
def enableMail():
    return 1


@config(Bool, None, '是否使用注销旧流程', (ConfigFlag.CLIENT, ConfigFlag.CACHE_CONFIG, ConfigFlag.ALWAYS_SEND_CLIENT))
def enableOldLogout():
    return 1


@config(Bool, None, '是否开启切磋')
def enableDuel():
    try:
        ret = int(ResMgr.getStringContentForPath(ResMgr.kbengineConfig(), 'game/enableDuel'))
    except:
        ret = 1
    return ret

@config(Bool, None, '是否开启敌方')
def enableEnemy():
    try:
        ret = int(ResMgr.getStringContentForPath(ResMgr.kbengineConfig(), 'game/enableEnemy'))
    except:
        ret = 1
    return ret

@config(Bool, None, '是否开启伤害统计', (ConfigFlag.CACHE_CONFIG, ))
def enableStatistic():
    try:
        ret = int(ResMgr.getStringContentForPath(ResMgr.kbengineConfig(), 'game/enableStatistic'))
    except:
        ret = 0
    return ret

@config(Bool, None, '是否开启交易行', (ConfigFlag.CLIENT, ConfigFlag.CACHE_CONFIG, ConfigFlag.ALWAYS_SEND_CLIENT))
def enableAuction():
    return 1

@cache
def auctionServerHost():
    try:
        host = ResMgr.getStringContentForPath(ResMgr.kbengineConfig(), 'game/auctionServerHost')
    except:
        host = '192.168.10.31:2010'
    return host

@cache
def isCrossServer():
    return getCrossServerId() == serverId()

@config(Bool, 'true', '是否开启城战')
def enableSiegeWar():
    return True

@cache
def httpCmdIdempotent():
    '''
    http cmd 命令小写
    开放无状态幂等（即收到重复请求，返回数据一样）
    '''
    return ()


@cache
def debugErrorLogHost():
    try:
        host = ResMgr.getStringContentForPath(ResMgr.kbengineConfig(), 'debug/debugErrorLogHost')
    except:
        host = ''

    return host

@cache
def wxReportUrl():
    try:
        '''
        host = ResMgr.getStringContentForPath(ResMgr.kbengineConfig(), 'game/errReportUrl')
        '''
        host = 'https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=e7a6e5a5-18d0-4a5c-be78-01b4827e208b'
    except:
        host = 'https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=92de3ed1-9bfe-4428-afc6-f1488f9bb452'
    return host


@config(Bool, None, '是否开启工坊制造', (ConfigFlag.CLIENT, ConfigFlag.CACHE_CONFIG, ConfigFlag.ALWAYS_SEND_CLIENT))
def enableWorkshop():
    return 1


def visibleConfigEable(configName):
    info = CONFIG.get(configName)
    if not info:
        ERROR_MSG('gameconfig not found:', configName)
        return

    configName, convFunc, default, defaultV, desc, cid, flags = info

    v = KBEngine.globalData['CONFIG'][configName]
    if not v:
        return False

    return True


