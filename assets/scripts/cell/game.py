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
    DEBUG_MSG('onInit:', isReload, groupOrder)
    if not isReload:
        sys.excepthook = gameengine.exceptHook

    buildAreaData()
    KBEngine.addTimer(1, 1, initAsyncore)

    gameglobal.avatarExposedMethods = utils.getExposedMethods()
    KBEngine.addTimer(1800, 1800, outputExposedMethodStats)


def initAsyncore(timerId):
    asyncore.loop(0, True, None, 1)


def checkSpecialSpaceOnNewCellappStarted(timerId):
    if not gameglobal.staticCell:
        INFO_MSG('checkSpecialSpaceOnNewCellappStarted:', gameglobal.staticCell)


def onGlobalData(key, value):
    """
    KBEngine method.
    globalData改变
    """
    DEBUG_MSG('onGlobalData:', key, value)

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
    DEBUG_MSG('onDelGlobalData:', key)


def onCellAppData(key, value):
    """
    KBEngine method.
    cellAppData改变
    """
    DEBUG_MSG('onCellAppData:', key, value)
    if key == gameconst.GLOBALDATA_KEY_CELLAPP_CALL:
        gameengine.onAppCall(value)


def onCellAppDataDel(key):
    """
    KBEngine method.
    cellAppData删除
    """
    DEBUG_MSG('onCellAppDataDel: %s' % key)


def onSpaceData(spaceID, key, value):
    """
    KBEngine method.
    spaceData改变
    @spaceID:  数据被设置在这个spaceID的space中.
    @key:  被设置的key.
    @value:  被设置的值， 如果值被删除则为None.
    """
    DEBUG_MSG('onSpaceData: spaceID=%s, key=%s, value=%s.' % (spaceID, key, value))


def onSpaceGeometryLoaded(spaceID, mapping):
    """
    KBEngine method.
    space 某部分或所有chunk等数据加载完毕
    具体哪部分需要由cell负责的范围决定
    """
    DEBUG_MSG('onSpaceGeometryLoaded: spaceID=%s, mapping=%s.' % (spaceID, mapping))


def onAllSpaceGeometryLoaded(spaceID, isBootstrap, mapping):
    """
    KBEngine method.
    space 某部分或所有chunk等数据加载完毕
    具体哪部分需要由cell负责的范围决定
    """
    DEBUG_MSG('onAllSpaceGeometryLoaded: spaceID=%s, isBootstrap=%i, mapping=%s.' % (spaceID, isBootstrap, mapping))

    if not isBootstrap:
        return

    spaceEnt = gameglobal.localSpaceIDMap.get(spaceID)
    if spaceEnt:
        spaceEnt.base.entireConstruct(spaceID)
    else:
        ERROR_MSG('onAllSpaceGeometryLoaded: cannot find space', spaceID, isBootstrap, mapping)

    kbeUtils.processSpaceGeometryTasks(spaceID)


def callGCCollect():
    gc.collect()
    gc.collect()


def onAirWallLoadFinished():
    DEBUG_MSG('onAirWallLoadFinished')


def outputExposedMethodStats(timerId):
    if gameconfig.enableExposedMethodStats():
        stats = utils.getCallStats()
        _outputExposedMethodStats(stats, 0, 20)


def _outputExposedMethodStats(stats, fromIdx, num):
    if fromIdx == 0:
        INFO_MSG('exposed method call stats, onlineNum={} timestamp={}'.format(
            KBEngine.globalData.get(gameconst.GLOBALDATA_KEY_ONLINE_NUM, 0), utils.getNow()))

    endIdx = min(len(stats), fromIdx + num)
    for i in range(fromIdx, endIdx):
        info = stats[i]
        INFO_MSG('call stats: {} {}'.format(info[1], info[0]))

    if endIdx < len(stats):
        KBEngine.addTimer(0.1, 0, lambda tid: _outputExposedMethodStats(stats, endIdx, num))
    else:
        KBEngine.resetAllCallNum('Avatar')


def onInited():
    gorder = KBEngine.getComponentGroupOrder()
    INFO_MSG('cellapp onInited!!!', gorder)
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
