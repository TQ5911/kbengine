# -*- coding: utf-8 -*-
import sys
import gc
# gc.disable()

import KBEngine
import Watcher
import gamebase
import gameengine
import gameglobal
import gameconst
import gamesql
import formula
import gameconfig
import utils

from KBEDebug import *
import gc


def onBaseAppReady(isBootstrap):
    """
    KBEngine method.
    baseapp已经准备好了
    @param isBootstrap: 是否为第一个启动的baseapp
    @type isBootstrap: BOOL
    """
    LOG_INFO('onBaseAppReady: isBootstrap=%s' % isBootstrap)

    groupOrder = KBEngine.getComponentGroupOrder()

    # 安装监视器
    Watcher.setup()

    gameglobal.isBootstrap = isBootstrap
    gameglobal.isBaseAppReady = True

    if KBEngine.globalData.get(gameconst.GLOBALDATA_KEY_GAME_READY):
        LOG_INFO('baseapp relive', groupOrder)
        gameglobal.isRelivedBaseapp = True
        checkGameConfigReady()
    elif isBootstrap:
        gamesql.getCustomConfig(onGameConfigLoaded)
        gamesql.deleteExpiredAdminCmdSerial()
    else:
        checkGameConfigReady()


def checkGameConfigReady():
    if not gameconfig.isReady():
        LOG_WARN('gameconfig is not ready, waiting...')
        KBEngine.addTimer(1, 0, lambda tid: checkGameConfigReady())
    else:
        onGameConfigLoaded()


def onGameConfigLoaded():
    baseAppCnt = gameconfig.baseAppCount()
    gameglobal.localBaseApp = KBEngine.createEntityLocally("BaseApp", {})
    gameglobal.localBaseApp.setStartGbId(KBEngine.getComponentGroupOrder(), baseAppCnt)

    # 进程启动后较慢时引擎只会同步globalData，不会调用到onGlobalData,导致监听失效，这里重新触发下
    for k, v in KBEngine.globalData.items():
        onGlobalData(k, v)

    for k, v in KBEngine.baseAppData.items():
        onBaseAppData(k, v)

    gameglobal.avatarExposedMethods = utils.fetchExposedMethods()
    KBEngine.addTimer(1800, 1800, outputExposedMethodStats)


def onReadyForShutDown():
    """
    KBEngine method.
    进程询问脚本层：我要shutdown了，脚本是否准备好了？
    如果返回True，则进程会进入shutdown的流程，其它值会使得进程在过一段时间后再次询问。
    用户可以在收到消息时进行脚本层的数据清理工作，以让脚本层的工作成果不会因为shutdown而丢失。
    """
    LOG_INFO('onReadyForShutDown()')
    return True


def onBaseAppShutDown(state):
    """
    KBEngine method.
    这个baseapp被关闭前的回调函数
    @param state:  0 : 在断开所有客户端之前
                         1 : 在将所有entity写入数据库之前
                         2 : 所有entity被写入数据库之后
    @type state: int
    """
    LOG_INFO('onBaseAppShutDown: state=%i' % state)


def onReadyForLogin(isBootstrap):
    """
    KBEngine method.
    如果返回值大于等于1.0则初始化全部完成, 否则返回准备的进度值0.0~1.0。
    在此可以确保脚本层全部初始化完成之后才开放登录。
    @param isBootstrap: 是否为第一个启动的baseapp
    @type isBootstrap: BOOL
    """

    if isBootstrap and not KBEngine.globalData.get(gameconst.GLOBALDATA_KEY_GAME_READY):
        return 0.0

    LOG_INFO('initProgress: completed!')
    return True


def onBaseAppDeath(groupOrder, compId):
    LOG_INFO('onBaseAppDeath', groupOrder, compId)
    stubIndex = groupOrder

    for k, v in gameglobal.baseAppCache.items():
        if ' component=baseapp[%s]' % compId in str(v):
            LOG_INFO('onBaseAppDeath: remove baseapp cache', k, v)
            gameglobal.baseAppCache.pop(k)
            gameengine.delGlobalAppData(gameconst.GLOBALDATA_KEY_BASEAPP_IDX + ':' + str(stubIndex))
            break
    gameglobal.deadBaseapps[groupOrder] = 1


def onAutoLoadEntityCreate(entityType, dbid):
    """
    KBEngine method.
    自动加载的entity创建方法，引擎允许脚本层重新实现实体的创建，如果脚本不实现这个方法
    引擎底层使用createEntityAnywhereFromDBID来创建实体
    """
    LOG_INFO('onAutoLoadEntityCreate: entityType=%s, dbid=%i' % (entityType, dbid))
    KBEngine.createEntityAnywhereFromDBID(entityType, dbid)


def onInit(isReload):
    """
    KBEngine method.
    当引擎启动后初始化完所有的脚本后这个接口被调用
    @param isReload: 是否是被重写加载脚本后触发的
    @type isReload: bool
    """
    LOG_INFO('onInit::isReload:%s' % isReload)
    if not isReload:
        import gameengine
        sys.excepthook = gameengine.exceptHook


def onFini():
    """
    KBEngine method.
    引擎正式关闭
    """
    LOG_INFO('onFini()')


def onCellAppDeath(addr, cid, groupOrder):
    """
    KBEngine method.
    某个cellapp死亡
    """
    LOG_WARN('onCellAppDeath:', cid, groupOrder, addr)
    if gameglobal.isBootstrap and not KBEngine.globalData.get(gameconst.GLOBALDATA_KEY_GAME_READY):
        LOG_ERR('cellapp dead in starting, shutdown...')
        KBEngine.shutdownServer()
    else:
        for lineType in gameconst.lineStubMap():
            gameengine.getLineStub(lineType).handleCellappDeath(groupOrder)

        gameglobal.localBaseApp.handleCellappDealth(groupOrder)


def onGlobalData(key, val):
    """
    KBEngine method.
    globalData有改变
    """
    LOG_INFO('onGlobalData:', key, val)
    if isinstance(key, str):
        if key.startswith(gameconst.GLOBALDATA_KEY_BASEAPP):
            # 每起一个baseapp，都会通知一下全局，记录新起的baseapp名字到其BaseApp的mailbox的映射
            prefix, host, port = key.split(':')
            key = host + ":" + port
            if key not in gameglobal.baseAppCache:
                gameglobal.baseAppCache[key] = val

        elif key.startswith(gameconst.GLOBALDATA_KEY_SPACENO_TO_SPACEID):
            # 任何静态地图或者副本地图创建了，都会全局通知，记录一下spaceId到spaceNo的映射
            prefix, spaceNo = key.split(':')
            spaceNo = int(spaceNo)
            if spaceNo not in gameglobal.spaceNOIDCache:
                gameglobal.spaceNOIDCache[spaceNo] = val

        elif key.startswith(gameconst.GLOBALDATA_KEY_SPACEID_TO_SPACENO):
            # 记录spaceNo到spaceId的映射
            prefix, spaceID = key.split(':')
            spaceID = int(spaceID)
            if spaceID not in gameglobal.spaceIDNOCache:
                gameglobal.spaceIDNOCache[spaceID] = val

        elif key == gameconst.GLOBALDATA_KEY_BASEAPP_READY:
            gameglobal.readyBaseappOrder.add(val)

        elif key.startswith(gameconst.GLOBALDATA_KEY_BASEAPP_IDX):
            prefix, groupOrderStr = key.split(':')
            groupOrder = int(groupOrderStr)
            if groupOrder in gameglobal.deadBaseapps:
                LOG_INFO('got relived baseapp', groupOrder, val)
                box = val
                hostName = utils.getPythonAddr()
                selfOrder = KBEngine.getComponentGroupOrder()
                accountNum = gameglobal.localLoginStub.accountNumCounter.dataSum
                avatarNum = accountNum
                box.callMethod('sendDataToRelivedBaseapp',
                               (hostName, selfOrder, gameglobal.localBaseApp, accountNum, avatarNum))
                gameglobal.deadBaseapps.pop(groupOrder)
        elif key.startswith(gameconst.GLOBALDATA_KEY_CELLAPP_INITED):
            if gameglobal.localBaseApp:
                if gameconfig.isWaitMapServer():
                    gameglobal.localBaseApp.waitMapAddInitedCellapp(val)
                else:
                    gameglobal.localBaseApp.addInitedCellapp(val)

        if gameglobal.localBaseApp:
            gameglobal.localBaseApp.doGlobalDataCallback(key, val)


def onGlobalDataDel(key):
    """
    KBEngine method.
    globalData有删除
    """

    LOG_INFO('onGlobalDataDel:', key)
    if isinstance(key, str):
        if key.startswith(gameconst.GLOBALDATA_KEY_SPACENO_TO_SPACEID):
            # 任何静态地图或者副本地图创建了，都会全局通知，记录一下spaceId到spaceNo的映射
            prefix, spaceNo = key.split(':')
            spaceNo = int(spaceNo)
            gameglobal.spaceNOIDCache.pop(spaceNo, None)

        elif key.startswith(gameconst.GLOBALDATA_KEY_SPACEID_TO_SPACENO):
            # 记录spaceNo到spaceId的映射
            prefix, spaceID = key.split(':')
            spaceID = int(spaceID)
            gameglobal.spaceIDNOCache.pop(spaceID, 0)
    return


def onBaseAppData(key, value):
    """
    KBEngine method.
    baseAppData有改变
    """
    LOG_DBG('onBaseAppData:', key, value)
    if not type(key) is str:
        return

    if key == gameconst.GLOBALDATA_KEY_APPCALL:
        import gameengine
        gameengine.onAppCall(value)
    elif key == gameconst.GLOBALDATA_KEY_CREATE_BASEAPP:
        if not gameglobal.localBaseApp and gameglobal.isBaseAppReady:
            baseApp = KBEngine.createEntityLocally("BaseApp", {})
            gameglobal.localBaseApp = baseApp

    if gameglobal.localBaseApp:
        gameglobal.localBaseApp.doBaseappDataCallback(key, value)


def onBaseAppDataDel(key):
    """
    KBEngine method.
    baseAppData有删除
    """
    LOG_DBG('onBaseAppDataDel: %s' % key)


def onLoseChargeCB(ordersID, dbid, success, datas):
    """
    KBEngine method.
    有一个不明订单被处理， 可能是超时导致记录被billing
    清除， 而又收到第三方充值的处理回调
    """
    LOG_DBG('onLoseChargeCB: ordersID=%s, dbid=%i, success=%i, datas=%s' % \
              (ordersID, dbid, success, datas))


def callGCCollect():
    LOG_DBG('baseapp: gc.collect():', gc.collect())


def outputExposedMethodStats(timerId):
    if gameconfig.enableExposedMethodStats():
        stats = utils.fetchCallStats()
        _outputExposedMethodStats(stats, 0, 20)


def _outputExposedMethodStats(stats, fromIdx, num):
    if fromIdx == 0:
        LOG_INFO('exposed method call stats, onlineNum={} timestamp={}'.format(
            gameglobal.localLoginStub.getGlobalAccountNum(), utils.curTS()))

    endIdx = min(len(stats), fromIdx + num)
    for i in range(fromIdx, endIdx):
        info = stats[i]
        LOG_INFO('call stats: {} {}'.format(info[1], info[0]))

    if endIdx < len(stats):
        KBEngine.addTimer(0.1, 0, lambda tid: _outputExposedMethodStats(stats, endIdx, num))
    else:
        KBEngine.resetAllCallNum('Avatar')
