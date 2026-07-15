# -*- coding: utf-8 -*-
import random

import KBEngine
from KBEDebug import *

from rpc import RpcChannel

import traceback
import sys
import hashlib

import utils
import gameconst
import gameglobal
import formula
import gameconfig

import cube_room
import wonderLand_floor
import abyss_floor

import gamePlay_gamePlay as GGD
import taskdata as TDD


def isCell():
    return KBEngine.component == 'cellapp'


def isBase():
    return KBEngine.component == 'baseapp'


def setGlobalData(key, value):
    KBEngine.globalData[key] = value
    import game
    game.onGlobalData(key, value)


def getGlobalBase(key, reportErr=True):
    _box = KBEngine.globalData.get(key)

    if _box:
        ent = KBEngine.entities.get(_box.id)
        if ent:
            return ent
        return _box
    else:
        if reportErr:
            panicStack('Warning:Impossible for global stub in baseApp:', key)
        return utils.Swallower()


def getCubeStubBySpaceNo(spaceNo):
    _mapId = formula.fetchMapId(spaceNo)
    return getGlobalBase('CubeStub%d' % cube_room.datas[_mapId]['floor'])


def getCubeStub(floor):
    return getGlobalBase('CubeStub%d' % floor)

def getAbyssStubBySpaceNo(spaceNo):
    _mapId = formula.fetchMapId(spaceNo)
    _floor = abyss_floor.id2floor[_mapId]
    return getGlobalBase('AbyssStub%d' % _floor)

def getWonderLandStubBySpaceNo(spaceNo):
    _mapId = formula.fetchMapId(spaceNo)
    _floor = wonderLand_floor.id2floor[_mapId]
    return getGlobalBase('WonderLandStub%d' % _floor)


def getWonderLandStub(mapId):
    _floor = wonderLand_floor.id2floor[mapId]
    return getGlobalBase('WonderLandStub%d' % _floor)

def getAbyssStub(mapId):
    _floor = abyss_floor.id2floor[mapId]
    return getGlobalBase('AbyssStub%d' % _floor)


def setBaseAppData(key, value):
    if isBase():
        KBEngine.baseAppData[key] = value
        import game
        game.onBaseAppData(key, value)
    elif isCell():
        gameglobal.staticCell.base.setBaseAppData(key, value)


def getBaseAppData(key):
    if isBase():
        return KBEngine.baseAppData.get(key, None)
    else:
        LOG_ERR('cannot get baseapp data on cell')


def setCellAppData(key, value):
    if isBase():
        KBEngine.globalData[key] = value
    elif isCell():
        KBEngine.cellAppData[key] = value
        import game
        game.onCellAppData(key, value)


def getCellAppData(key, defaultVal=None):
    if isCell():
        return KBEngine.cellAppData.get(key, defaultVal)
    else:
        return defaultVal


def delGlobalAppData(key):
    if isBase():
        if key not in KBEngine.globalData:
            return

        del KBEngine.globalData[key]
    elif isCell():
        if key not in KBEngine.globalData:
            return

        del KBEngine.globalData[key]


def delCellAppData(key):
    if isBase():
        KBEngine.delCellAppData(key)
    elif isCell():
        if key not in KBEngine.cellAppData:
            return

        del KBEngine.cellAppData[key]


def delBaseAppData(key):
    if isBase():
        if key not in KBEngine.baseAppData:
            return

        del KBEngine.baseAppData[key]
    elif isCell():
        KBEngine.delBaseAppData(key)


def getAllBaseApps():
    return list(gameglobal.baseAppCache.values())


def howManyBaseApps():
    return len(getAllBaseApps())


def getAllBaseAppName():
    return list(gameglobal.baseAppCache.keys())

def getFirstBaseApp():
    _minEntId = 0
    _retApp = None
    for baseapp in gameglobal.baseAppCache.values():
        if not _minEntId or baseapp.id < _minEntId:
            _minEntId = baseapp.id
            _retApp = baseapp

    return _retApp

def isFirstBaseApp():
    _localBase = gameglobal.localBaseApp
    minEntId = 0
    for _baseapp in gameglobal.baseAppCache.values():
        if not minEntId or _baseapp.id < minEntId:
            minEntId = _baseapp.id

    return _localBase.id == minEntId


def isFirstCellApp():
    _comps = KBEngine.getComponents()
    _cellappGroupOrders = sorted([cellInfo['groupOrder'] for cellInfo in _comps['cellapps']])
    if len(_cellappGroupOrders) == 0:
        return True
    return _cellappGroupOrders[0] == 2


# 查询所有开着的spaceno，包括静态场景和副本场景
def chooseAllSpace():
    return gameglobal.spaceNOIDCache


def panicStack(*args):
    _msg = ' '.join([str(args) for args in args])
    if sys.exc_info()[0]:
        LOG_ERR('{}\n{}'.format(_msg, traceback.format_exc()))
    else:
        LOG_ERR('{}\n{}'.format(_msg, ' '.join(traceback.format_stack())))


RpcChannel.REPORT_ERR_FUNC = panicStack


def chooseGoodBaseApp():
    _bases = []

    for key in KBEngine.globalData.keys():
        if isinstance(key, str) and key.startswith(gameconst.GLOBALDATA_KEY_BASEAPP):
            _bases.append(KBEngine.globalData[key])

    return _bases


def getSpaceBase(spaceNo):
    return KBEngine.globalData[gameconst.GLOBALDATA_KEY_SPACE_TO_BASE + ':' + str(spaceNo)]


def hasSpaceBase(spaceNo):
    return KBEngine.globalData.has_key(gameconst.GLOBALDATA_KEY_SPACE_TO_BASE + ':' + str(spaceNo))


def getSpaceEntity(spaceNo):
    _id = getSpaceBase(spaceNo).id
    return KBEngine.entities[_id]

def getDungeonStubByDungeonNo(dungeonNo, dungeonEnterType):
    return getGlobalBase(formula.fetchDungeonStubGlobalName(dungeonNo, dungeonEnterType))

def getDungeonEnterTypeBySpaceNo(spaceNo):
    _dungeonNo = spaceNo // gameconst.SPACE_NO_HOME_INTERVAL
    dunEnterType = GGD.datas[_dungeonNo].get('enterType', gameconst.DungeonEnterTypeEnum.SINGLE)

    if dunEnterType==gameconst.DungeonEnterTypeEnum.BOTH:
        sStart, sEnd = gameconst.SpaceType.getSingleDungeonSpaceRange(_dungeonNo)
        if sStart <= spaceNo < sEnd:
            return gameconst.DungeonEnterTypeEnum.SINGLE
        else:
            return gameconst.DungeonEnterTypeEnum.TEAM
    else:
        return dunEnterType


def getDungeonStubBySpaceNo(spaceNo):
    et = getDungeonEnterTypeBySpaceNo(spaceNo)
    return getDungeonStubByDungeonNo(formula.fetchMapId(spaceNo), et)


def exceptHook(ty, val, tb):
    localVars = None
    outputMethod = EXCEPT_WARNING_MSG
    outputList = []
    exceptHook = False
    try:
        if tb:
            tag = tb.tb_frame.f_locals.get('__name__')
            if tag and tag == '__main__':
                outputMethod = EXCEPT_WARNING_MSG
                outputList.append('~~~~~~~ TELNET Exception ~~~~~~')
            else:
                outputMethod = LOG_ERR
                outputList.append('~~~~~~~ SCRIPT Exception ~~~~~~')
            _tbNext = tb
            while _tbNext.tb_next:
                _tbNext = _tbNext.tb_next
            if _tbNext.tb_frame.f_locals:
                varDict = {}
                for k, _v in _tbNext.tb_frame.f_locals.items():
                    _sv = str(_v)
                    if len(_sv) > 200:
                        varDict[k] = _sv[:200] + '...(more)'
                    else:
                        varDict[k] = _sv
                varMsg = str(varDict)
                if len(varMsg) > 1500:
                    varMsg = varMsg[:1500] + '...(more)'
                localVars = '\nLocals (only top stack frame):\n%s' % varMsg
                outputList.append(localVars)
        else:
            outputList.append('~~~~~~~ SCRIPT Exception ~~~~~~\n')
            outputMethod = EXCEPT_ERROR_MSG
            stack_frames = traceback.format_stack()
            for index, line in enumerate(stack_frames):
                if index == len(stack_frames) - 1:
                    break
                elif index == len(stack_frames) - 2:
                    outputList.append(line.strip())
                else:
                    outputList.append((line.strip() + '\n'))

    except Exception as e:
        outputMethod = EXCEPT_ERROR_MSG
        exceptHook = True
        outputList.append('~~~~~~~ UNKNOW Exception ~~~~~~ {} {} {}'.format(e, ty, val))

    exceptionLines = traceback.format_exception(ty, val, tb)
    for line in exceptionLines:
        exceptHook = True
        outputList.append(line[:-1])

    outputMethod('\n'.join(outputList), exceptHook=exceptHook)


def callBaseApps(func, args):
    setBaseAppData(gameconst.GLOBALDATA_KEY_APPCALL, (gameglobal.appCallIdx, 'all', func, args))
    gameglobal.appCallIdx += 1


def callBaseApp(pythonServer, func, args):
    setBaseAppData(gameconst.GLOBALDATA_KEY_APPCALL, (gameglobal.appCallIdx, pythonServer, func, args))
    gameglobal.appCallIdx += 1


def callCellApps(func, args):
    setCellAppData(gameconst.GLOBALDATA_KEY_CELLAPP_CALL, (gameglobal.appCallIdx, 'all', func, args))
    gameglobal.appCallIdx += 1


def callCellApp(pythonServer, func, args):
    setCellAppData(gameconst.GLOBALDATA_KEY_CELLAPP_CALL, (gameglobal.appCallIdx, pythonServer, func, args))
    gameglobal.appCallIdx += 1


def callAllApps(func, args):
    setBaseAppData(gameconst.GLOBALDATA_KEY_APPCALL, (gameglobal.appCallIdx, 'all', func, args))
    setCellAppData(gameconst.GLOBALDATA_KEY_CELLAPP_CALL, (gameglobal.appCallIdx, 'all', func, args))
    gameglobal.appCallIdx += 1


def _realCallApp(func, args):
    _fields = func.split('.')
    assert (len(_fields) <= 2)

    if len(_fields) == 1:
        globals()[func](*args)
    else:
        mod = __import__(_fields[0])
        getattr(mod, _fields[1])(*args)


def onAppCall(val):
    _, python_server, func, args = val
    if python_server == 'all' or python_server == utils.getPythonAddr():
        _realCallApp(func, args)


def broadcastBaseapp(funcName, args, exludes=()):
    for _baseapp in getAllBaseApps():
        if exludes and _baseapp.id in exludes:
            continue
        _baseapp.callMethod(funcName, args)


def makeLineStubKey(lineType):
    return 'lineStub_%s' % lineType


def getEntityMethodUID(*args):
    _entType, methodName = '', ''
    if len(args) == 1:
        _entType = args[0]
    elif len(args) == 2:
        _entType, methodName = args
    else:
        return -1

    return KBEngine.getMethodUidMap(_entType).get(methodName, 0)


def getEntityMethodByUID(*args):
    _entType, uid = '', 0
    if len(args) == 1:
        _entType = args[0]
    elif len(args) == 2:
        _entType, uid = args
    else:
        return 'unknow'

    return KBEngine.getAllUidMethodMap(_entType).get(uid, '')


def modifyGlobalExposedFunc(isAdd, func, msgId):
    if isAdd:
        gameglobal.globalBlockExposedFuncName[func] = msgId
    else:
        gameglobal.globalBlockExposedFuncName.pop(func, None)


def getLoginStub(idx):
    if not idx:
        idx = random.randint(1, gameconfig.baseAppCount())
    return getGlobalBase(buildIndexStubName('LoginStub', idx))


def getLoginStubsByAccountName(accountType_Name):
    stubs = []
    nameHash = int(hashlib.md5(accountType_Name.encode('ascii')).hexdigest(), 16)
    for i in range(gameconst.PLAYER_REGISTER_STUB_NUM):
        stubID = (nameHash + i) % gameconfig.baseAppCount() + 1  # 0,1,..n-1->1,2,...n
        stubs.append(getLoginStub(stubID))
    return stubs


def buildLineStubName(lineType):
    stubName = gameconst.lineStubMap()[lineType]['stubName']
    return '%s%s' % (stubName, lineType)


def getLineStub(lineType):
    return getGlobalBase(buildLineStubName(lineType))


def getPlayerStub(idx):
    return getGlobalBase(buildIndexStubName('PlayerStub', idx))


def playerStubHashIdx(gbId):
    return (gbId % gameconfig.baseAppCount()) + 1


def buildIndexStubName(stubName, idx):
    return '%s_%s' % (stubName, idx)

def getTeamStub(teamId):
    id = teamId % gameconst.TEAMSTUB_CONF_NUM
    teamStubName = 'TeamStub' + str(id)
    return getGlobalBase(teamStubName)

def getRaidStub(raidId):
    id = raidId % gameconst.RAIDSTUB_CONFIG_NUM
    raidStubName = gameconst.GLOBAL_BASE_STUB_RAIDSTUB + str(id)
    return getGlobalBase(raidStubName)

def getLeaderStub(leaderBoardType, reportErr=True):
    _leaderStubName = 'LeaderBoardStub' + str(leaderBoardType)
    return getGlobalBase(_leaderStubName, reportErr)

def getStatisticStub(spaceNo):
    id = spaceNo % gameconst.STATISTICSTUB_CONFIG_NUM
    statisticStubName = 'StatisticStub' + str(id)
    return getGlobalBase(statisticStubName)

def resetGlobalActData(globalActData):
    gameglobal.globalActData = globalActData

def modifyGlobalActData(actId, endTime):
    if endTime:
        gameglobal.globalActData[actId] = endTime
    else:
        gameglobal.globalActData.pop(actId, None)

def updateFreeTicketNumConfig(dateNumInfo):
    LOG_INFO("updateFreeTicketNumConfig dateNumInfo", dateNumInfo)
    for subType, dateNumList in dateNumInfo.items():
        expandInfoList = []
        for cfgIdx, cfgInfo in enumerate(dateNumList):
            expandInfoList.append([cfgInfo[0], cfgInfo[1]])
            if cfgIdx + 1 >= len(dateNumList):
                LOG_DBG("updateFreeTicketNumConfig end", expandInfoList[-1])
                break
            nextData = dateNumList[cfgIdx + 1]
            while expandInfoList[-1][0] < nextData[0]:
                adjDataTimestamp = utils.getIntTimestamp(str(expandInfoList[-1][0]) + gameconst.RESOURCE_RECOVER_TIME_POINT_STR)
                adjDataTimestamp += 86400
                adjDataTime = utils.getIntDateTime(adjDataTimestamp)
                if adjDataTime >= nextData[0]:
                    break
                expandInfoList.append([adjDataTime, expandInfoList[-1][1]])
        gameglobal.freeTicketNumConfig[subType] = expandInfoList

        LOG_INFO("updateFreeTicketNumConfig gameglobal.freeTicketNumConfig", subType, expandInfoList)
        gameglobal.localBaseApp.doUpdateFreeTicketNumConfig(subType, expandInfoList)

def updateAntiAddictionData(timeType, nextStartTime):
    gameglobal.antiAddictionData = [timeType, nextStartTime]
    if isBase():
        doBaseAntiAddiction()
    elif isCell():
        doCellAntiAddiction()

def doBaseAntiAddiction():
    #LOG_DBG("doBaseAntiAddiction", gameglobal.antiAddictionData)
    gameglobal.localBaseApp.doAntiAddiction()

def doCellAntiAddiction():
    #LOG_DBG("doCellAntiAddiction", gameglobal.antiAddictionData)
    pass

def resetGuildRelation(relationDic, version):
    gameglobal.guildRelationDic = relationDic
    gameglobal.guildRelationVersion = version

def addGuildRelation(guildUUID1, guildUUID2, relationType, version):
    _pair = utils.getGuildUUIDPair(guildUUID1, guildUUID2)
    gameglobal.guildRelationDic[_pair] = relationType
    gameglobal.guildRelationVersion = version

def removeGuildRelation(guildUUID1, guildUUID2, version):
    _pair = utils.getGuildUUIDPair(guildUUID1, guildUUID2)
    gameglobal.guildRelationDic.pop(_pair, None)
    gameglobal.guildRelationVersion = version


def setMapleServerInfo(serverInfo, alias, serverName):
    gameglobal.curServerAlias = alias
    gameglobal.mapleServerInfo = serverInfo
    gameglobal.curServerName = serverName

    utils.group2ServerIds.cache_clear()


def removeEquipDropDestroyCollection(collectionId, dropEquipId):
    # 因为装备列表太长导致之前的被删掉了，这时候需要删除掉落物
    _ent = KBEngine.entities.get(collectionId)
    if _ent:
        _ent.onEquipDropDestroy(dropEquipId)

# 不要直接使用，请通过 utils.subscribe 使用
def subscribeEvent(tag, eId, func):
    if tag not in gameglobal.hookDict:
        gameglobal.hookDict[tag] = {}
    if eId in gameglobal.hookDict[tag]:
        LOG_ERR('subscribe tag {} box {} already exists'.format(tag, eId))
        return

    LOG_DBG('subscribe tag {} box {} func {}'.format(tag, eId, func))
    gameglobal.hookDict[tag][eId] = func

# 不要直接使用，请通过 utils.unsubscribe 使用
def unsubscribeEvent(tag, eId):
    if tag in gameglobal.hookDict and eId in gameglobal.hookDict[tag]:
        del gameglobal.hookDict[tag][eId]
        
        if len(gameglobal.hookDict[tag]) == 0:
            del gameglobal.hookDict[tag]

# 不要直接使用，请通过 utils.distribute 使用
def callEvent(tag, *args):
    if tag not in gameglobal.hookDict:
        return

    for eId, func in gameglobal.hookDict[tag].items():
        ent = KBEngine.entities.get(eId)
        if not ent:
            continue
        LOG_DBG('callEvent tag {} args {}'.format(tag, *args))
        try:
            hasattr(ent, func) and getattr(ent, func)(*args)
        except Exception as e:
            LOG_ERR('hookOn {} exception: {}'.format(tag, e))
    return
    
def hasBaseEvent(tag):
    if IS_BASE and tag in gameglobal.hookDict:
        return True
    if IS_CELL and tag not in gameglobal.hookDict:
        return True
    return False

def hasCellEvent(tag):
    if IS_CELL and tag in gameglobal.hookDict:
        return True
    if IS_BASE and tag not in gameglobal.hookDict:
        return True
    return False

# 不要直接使用，请通过 utils.distribute 使用
def callAppsByEventTag(tag, *args):
    if hasBaseEvent(tag):
        callBaseApps(
            'gameengine.callEvent',
            (tag, *args),
        )
    if hasCellEvent(tag):
        callCellApps(
            'gameengine.callEvent',
            (tag, *args),
        )

def addForbiddenTaskIds(taskId):
    gameglobal.forbiddenTaskIds[taskId] = True
    LOG_INFO("addForbiddenTaskIds,", taskId, gameglobal.forbiddenTaskIds)

def removeForbiddenTaskIds(taskId):
    gameglobal.forbiddenTaskIds.pop(taskId, None)
    LOG_INFO("removeForbiddenTaskIds,", taskId, gameglobal.forbiddenTaskIds)

def quertForbiddenTaskIds():
    taskIds = list(gameglobal.forbiddenTaskIds.keys())
    LOG_INFO("quertForbiddenTaskIds,", gameglobal.forbiddenTaskIds)
    return taskIds

def checkForbiddenTaskId(taskId):
    return taskId in gameglobal.forbiddenTaskIds

def resetMineGlobalData(mineGlobalData):
    gameglobal.mineGlobalData = mineGlobalData.clone()

def setMineCanAttackBits(bitFlag, isSet):
    # bit Flag = 1 << bit
    if isSet:
        gameglobal.mineCanAttackBits |= bitFlag
    else:
        gameglobal.mineCanAttackBits &= ~bitFlag

def updateChatForbiddenState(gbid, state):
    LOG_DBG("gameengine updateChatForbiddenState", gbid, state, gameglobal.chatForbiddenSet)
    if state:
        gameglobal.chatForbiddenSet.add(gbid)
    else:
        gameglobal.chatForbiddenSet.discard(gbid)
    gameglobal.localBaseApp.broadcastToAllAvatar(gameconst.BASE, 'onNotifyChatForbiddenState', (gbid, state), ())