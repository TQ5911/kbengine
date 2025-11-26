# -*- coding: utf-8 -*-
import random

import KBEngine
from KBEDebug import *

import traceback
import sys
import hashlib

import utils
import gameconst
import gameglobal
import formula
import gamePlay_gamePlay as GGD
import cube_room
import wonderLand_floor
import gameconfig
from rpc import RpcChannel


def isBase():
    return KBEngine.component == 'baseapp'


def isCell():
    return KBEngine.component == 'cellapp'


def setGlobalData(key, val):
    KBEngine.globalData[key] = val
    import game
    game.onGlobalData(key, val)


def getGlobalBase(key, reportErr=True):
    box = KBEngine.globalData.get(key)

    if box:
        ent = KBEngine.entities.get(box.id)
        if ent:
            return ent
        return box
    else:
        reportErr and reportCritical('Warning:Impossible for global stub in baseApp:', key)
        return utils.Swallower()


def getCubeStubBySpaceNo(spaceNo):
    _mapId = formula.getMapId(spaceNo)
    return getGlobalBase('CubeStub%d' % cube_room.datas[_mapId]['floor'])


def getCubeStub(floor):
    return getGlobalBase('CubeStub%d' % floor)


def getWonderLandStubBySpaceNo(spaceNo):
    _mapId = formula.getMapId(spaceNo)
    _floor = wonderLand_floor.id2floor[_mapId]
    return getGlobalBase('WonderLandStub%d' % _floor)


def getWonderLandStub(mapId):
    _floor = wonderLand_floor.id2floor[mapId]
    return getGlobalBase('WonderLandStub%d' % _floor)


def getSiegeWarStubBySpaceNo(spaceNo):
    _mapId = formula.getMapId(spaceNo)
    return getGlobalBase('SiegeWarSpaceStub')


def setBaseAppData(key, val):
    if isBase():
        KBEngine.baseAppData[key] = val
        import game
        game.onBaseAppData(key, val)
    elif isCell():
        gameglobal.staticCell.base.setBaseAppData(key, val)


def getBaseAppData(key):
    if isBase():
        return KBEngine.baseAppData.get(key, None)
    else:
        ERROR_MSG('cannot get baseapp data on cell')


def setCellAppData(key, val):
    if isBase():
        KBEngine.globalData[key] = val
    elif isCell():
        KBEngine.cellAppData[key] = val
        import game
        game.onCellAppData(key, val)


def getCellAppData(key, default=None):
    if isCell():
        return KBEngine.cellAppData.get(key, default)
    else:
        return default


def delGlobalAppData(key):
    if isBase():
        if key in KBEngine.globalData:
            del KBEngine.globalData[key]
    elif isCell():
        if key in KBEngine.globalData:
            del KBEngine.globalData[key]


def delBaseAppData(key):
    if isBase():
        if key in KBEngine.baseAppData:
            del KBEngine.baseAppData[key]
    elif isCell():
        KBEngine.delBaseAppData(key)


def delCellAppData(key):
    if isBase():
        KBEngine.delCellAppData(key)
    elif isCell():
        if key in KBEngine.cellAppData:
            del KBEngine.cellAppData[key]


def howManyBaseApps():
    return len(getAllBaseApps())


def getAllBaseApps():
    return list(gameglobal.baseAppCache.values())


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
    localBase = gameglobal.localBaseApp
    minEntId = 0
    for baseapp in gameglobal.baseAppCache.values():
        if not minEntId or baseapp.id < minEntId:
            minEntId = baseapp.id

    return localBase.id == minEntId


def isFirstCellApp():
    comps = KBEngine.getComponents()
    cellappGroupOrders = sorted([cellInfo['groupOrder'] for cellInfo in comps['cellapps']])
    if len(cellappGroupOrders) == 0:
        return True
    return cellappGroupOrders[0] == 2


# 查询所有开着的spaceno，包括静态场景和副本场景
def chooseAllSpace():
    return gameglobal.spaceNOIDCache


def reportCritical(*args):
    msg = ' '.join([str(args) for args in args])
    if sys.exc_info()[0]:
        ERROR_MSG('{}\n{}'.format(msg, traceback.format_exc()))
    else:
        ERROR_MSG('{}\n{}'.format(msg, ' '.join(traceback.format_stack())))


RpcChannel.REPORT_ERR_FUNC = reportCritical


def chooseGoodBaseApp():
    bases = []

    for key in KBEngine.globalData.keys():
        if isinstance(key, str) and key.startswith(gameconst.GLOBALDATA_KEY_BASEAPP):
            bases.append(KBEngine.globalData[key])

    return bases


def hasSpaceBase(spaceNo):
    return KBEngine.globalData.has_key(gameconst.GLOBALDATA_KEY_SPACE_TO_ITS_BASE + ':' + str(spaceNo))


def getSpaceBase(spaceNo):
    return KBEngine.globalData[gameconst.GLOBALDATA_KEY_SPACE_TO_ITS_BASE + ':' + str(spaceNo)]


def getSpaceEntity(spaceNo):
    id_ = getSpaceBase(spaceNo).id
    return KBEngine.entities[id_]

def getDungeonStubByDungeonNo(dungeonNo, dungeonEnterType):
    return getGlobalBase(formula.getDungeonStubGlobalName(dungeonNo, dungeonEnterType))

def getDungeonEnterTypeBySpaceNo(spaceNo):
    dungeonNo = spaceNo // gameconst.SPACE_NO_HOME_INTERVAL
    dunEnterType = GGD.datas[dungeonNo].get('enterType', gameconst.DungeonEnterType.SINGLE)

    if dunEnterType==gameconst.DungeonEnterType.BOTH:
        sStart, sEnd = gameconst.SpaceType.getSingleDungeonSpaceNoRange(dungeonNo)
        if sStart <= spaceNo < sEnd:
            return gameconst.DungeonEnterType.SINGLE
        else:
            return gameconst.DungeonEnterType.TEAM
    else:
        return dunEnterType


def getDungeonStubBySpaceNo(spaceNo):
    et = getDungeonEnterTypeBySpaceNo(spaceNo)
    return getDungeonStubByDungeonNo(formula.getMapId(spaceNo), et)

def _fromTelnetException(trace):
    for msg in trace.strip().split('\n'):
        if msg.startswith('  File') and not msg.startswith('  File "<string>"'):
            return False

    return True


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
                outputMethod = ERROR_MSG
                outputList.append('~~~~~~~ SCRIPT Exception ~~~~~~')
            tbNext = tb
            while tbNext.tb_next:
                tbNext = tbNext.tb_next
            if tbNext.tb_frame.f_locals:
                varDict = {}
                for k, v in tbNext.tb_frame.f_locals.items():
                    # if v.__class__.__name__ == 'roDict' or v.__class__.__name__ == 'roTuple':
                    sv = str(v)
                    if len(sv) > 200:
                        varDict[k] = sv[:200] + '...(more)'
                    else:
                        varDict[k] = sv
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
    setBaseAppData(gameconst.GLOBALDATA_KEY_APPCALL, ('all', func, args))


def callBaseApp(pythonServer, func, args):
    setBaseAppData(gameconst.GLOBALDATA_KEY_APPCALL, (pythonServer, func, args))


def callCellApps(func, args):
    setCellAppData(gameconst.GLOBALDATA_KEY_CELLAPP_CALL, ('all', func, args))


def callCellApp(pythonServer, func, args):
    setCellAppData(gameconst.GLOBALDATA_KEY_CELLAPP_CALL, (pythonServer, func, args))


def callAllApps(func, args):
    setBaseAppData(gameconst.GLOBALDATA_KEY_APPCALL, ('all', func, args))
    setCellAppData(gameconst.GLOBALDATA_KEY_CELLAPP_CALL, ('all', func, args))


def _realCallApp(func, args):
    fields = func.split('.')
    assert (len(fields) <= 2)

    if len(fields) == 1:
        globals()[func](*args)
    else:
        mod = __import__(fields[0])
        getattr(mod, fields[1])(*args)


def onAppCall(val):
    python_server, func, args = val
    if python_server == 'all' or python_server == utils.getPythonServer():
        _realCallApp(func, args)


def broadcastBaseapp(funcName, args, exludes=()):
    for baseapp in getAllBaseApps():
        if exludes and baseapp.id in exludes:
            continue
        # getattr(baseapp, funcName)(*args)
        baseapp.callMethod(funcName, args)


def makeLineStubKey(lineType):
    return 'lineStub_%s' % lineType


def getEntityMethodUID(*args):
    entType, methodName = '', ''
    if len(args) == 1:
        entType = args[0]
    elif len(args) == 2:
        entType, methodName = args
    else:
        return -1

    return KBEngine.getMethodUidMap(entType).get(methodName, 0)


def getEntityMethodByUID(*args):
    entType, uid = '', 0
    if len(args) == 1:
        entType = args[0]
    elif len(args) == 2:
        entType, uid = args
    else:
        return 'unknow'

    return KBEngine.getAllUidMethodMap(entType).get(uid, '')


def modifyGlobalExposedFunc(isAdd, funcName, msgId):
    if isAdd:
        gameglobal.globalBlockExposedFuncName[funcName] = msgId
    else:
        gameglobal.globalBlockExposedFuncName.pop(funcName, None)


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
    stubName = gameconst.lineStubMap[lineType]['stubName']
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
    id = teamId % gameconst.TEAMSTUB_CONFIG_NUM
    teamStubName = 'TeamStub' + str(id)
    return getGlobalBase(teamStubName)

def getRaidStub(raidId):
    id = raidId % gameconst.RAIDSTUB_CONFIG_NUM
    raidStubName = gameconst.GLOBAL_BASE_STUB_RAIDSTUB + str(id)
    return getGlobalBase(raidStubName)

def getLeaderStub(leaderBoardType, reportErr=True):
    _leaderStubName = 'LeaderBoardStub' + str(leaderBoardType)
    return getGlobalBase(_leaderStubName, reportErr)


def resetGlobalActData(globalActData):
    gameglobal.globalActData = globalActData


def modifyGlobalActData(actId, endTime):
    if endTime:
        gameglobal.globalActData[actId] = endTime
    else:
        gameglobal.globalActData.pop(actId, None)

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
