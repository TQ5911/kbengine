# -*- coding: utf-8 -*-
import gc
# gc.disable()

import KBEngine
from KBEDebug import *

import gameengine
import sys
import gameglobal
import gameconst
import gc
import ResMgr
import asyncore
import gameconfig
import utils
import formula
import kbeUtils

import gamePlay_gamePlay as GGD


def onInit(isReload):
    """
    KBEngine method.
    当引擎启动后初始化完所有的脚本后这个接口被调用
    """
    groupOrder = KBEngine.getComponentGroupOrder()
    LOG_DBG('onInit:', isReload, groupOrder)
    if not isReload:
        sys.excepthook = gameengine.exceptHook

    buildAreaData()
    KBEngine.addTimer(1, 1, initAsyncore)
    KBEngine.addTimer(1, 60, countCellAppAvatar)
    KBEngine.addTimer(1, 10, broadcastCellAvatarCount)

    gameglobal.avatarExposedMethods = utils.fetchExposedMethods()
    KBEngine.addTimer(1800, 1800, outputExposedMethodStats)

def initAsyncore(timerId):
    asyncore.loop(0, True, None, 1)

def countCellAppAvatar(timerId):
    count = 0
    for e in KBEngine.entities.values():
        if e.__class__.__name__ == "Avatar":
            count += 1
    LOG_INFO("CellApp countAvatar", count)
    if gameglobal.cellAvatarCount != count:
        gameglobal.cellAvatarCount = count
        LOG_WARN("CellApp countAvatar changed", gameglobal.cellAvatarCount, count)

def broadcastCellAvatarCount(timerId):
    if gameglobal.lastBroadcastCellAvatarCount != gameglobal.cellAvatarCount:
        LOG_INFO("broadcastCellAvatarCount", KBEngine.getComponentGroupOrder(), gameglobal.cellAvatarCount)
        gameengine.broadcastBaseapp('onSyncCellAvatarCount', (KBEngine.getComponentGroupOrder(), gameglobal.cellAvatarCount))
        gameglobal.lastBroadcastCellAvatarCount = gameglobal.cellAvatarCount

def checkSpecialSpaceOnNewCellappStarted(timerId):
    if not gameglobal.staticCell:
        LOG_INFO('checkSpecialSpaceOnNewCellappStarted:', gameglobal.staticCell)


def onGlobalData(key, value):
    """
    KBEngine method.
    globalData改变
    """
    LOG_DBG('onGlobalData:', key, value)

    if isinstance(key, str):
        if key.startswith(gameconst.GLOBALDATA_KEY_BASEAPP):
            # 每起一个baseapp，都会通知一下全局，记录新起的baseapp名字到其BaseApp的mailbox的映射
            prefix, host, port = key.split(':')
            key = host + ":" + port
            if key not in gameglobal.baseAppCache:
                gameglobal.baseAppCache[key] = value

        elif key == gameconst.GLOBALDATA_KEY_CELLAPP_CALL:
            gameengine.onAppCall(value)


def onGlobalDataDel(key):
    """
    KBEngine method.
    globalData删除
    """
    LOG_DBG('onDelGlobalData:', key)


def onCellAppData(key, value):
    """
    KBEngine method.
    cellAppData改变
    """
    LOG_DBG('onCellAppData:', key, value)
    if key == gameconst.GLOBALDATA_KEY_CELLAPP_CALL:
        gameengine.onAppCall(value)


def onCellAppDataDel(key):
    """
    KBEngine method.
    cellAppData删除
    """
    LOG_DBG('onCellAppDataDel: %s' % key)


def onSpaceData(spaceID, key, value):
    """
    KBEngine method.
    spaceData改变
    @spaceID:  数据被设置在这个spaceID的space中.
    @key:  被设置的key.
    @value:  被设置的值， 如果值被删除则为None.
    """
    LOG_DBG('onSpaceData: spaceID=%s, key=%s, value=%s.' % (spaceID, key, value))


def onSpaceGeometryLoaded(spaceID, mapping):
    """
    KBEngine method.
    space 某部分或所有chunk等数据加载完毕
    具体哪部分需要由cell负责的范围决定
    """
    LOG_DBG('onSpaceGeometryLoaded: spaceID=%s, mapping=%s.' % (spaceID, mapping))


def onAllSpaceGeometryLoaded(spaceID, isBootstrap, mapping):
    """
    KBEngine method.
    space 某部分或所有chunk等数据加载完毕
    具体哪部分需要由cell负责的范围决定
    """
    LOG_DBG('onAllSpaceGeometryLoaded: spaceID=%s, isBootstrap=%i, mapping=%s.' % (spaceID, isBootstrap, mapping))

    if not isBootstrap:
        return

    spaceEnt = gameglobal.localSpaceIDMap.get(spaceID)
    if spaceEnt:
        spaceEnt.base.entireConstruct(spaceID)
    else:
        LOG_ERR('onAllSpaceGeometryLoaded: cannot find space', spaceID, isBootstrap, mapping)

    kbeUtils.processSpaceGeometryTasks(spaceID)


def callGCCollect():
    gc.collect()
    gc.collect()


def onAirWallLoadFinished():
    LOG_DBG('onAirWallLoadFinished')


def outputExposedMethodStats(timerId):
    if gameconfig.enableExposedMethodStats():
        stats = utils.fetchCallStats()
        _outputExposedMethodStats(stats, 0, 20)


def _outputExposedMethodStats(stats, fromIdx, num):
    if fromIdx == 0:
        LOG_INFO('exposed method call stats, onlineNum={} timestamp={}'.format(
            KBEngine.globalData.get(gameconst.GLOBALDATA_KEY_ONLINE_NUM, 0), utils.curTS()))

    endIdx = min(len(stats), fromIdx + num)
    for i in range(fromIdx, endIdx):
        info = stats[i]
        LOG_INFO('call stats: {} {}'.format(info[1], info[0]))

    if endIdx < len(stats):
        KBEngine.addTimer(0.1, 0, lambda tid: _outputExposedMethodStats(stats, endIdx, num))
    else:
        KBEngine.resetAllCallNum('Avatar')


def onInited():
    gorder = KBEngine.getComponentGroupOrder()
    LOG_INFO('cellapp onInited!!!', gorder)
    gameengine.setGlobalData('%s:%s' % (gameconst.GLOBALDATA_KEY_CELLAPP_INITED, gorder), gorder)

    if KBEngine.globalData.get(gameconst.GLOBALDATA_KEY_GAME_READY):
        for lineType in gameconst.lineStubMap().keys():
            gameengine.getLineStub(lineType).onCellappRelive(gorder)

        # cell 重新拉起,广播给所有可用的base
        bases = gameengine.chooseGoodBaseApp()
        for base in bases:
            base.onCellappRelive(gorder)

def buildAreaData():
    if gameglobal.areaData is not None:
        return

    gameglobal.areaData = ResMgr.loadAreaData()
