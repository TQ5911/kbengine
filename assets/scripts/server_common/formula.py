# -*- coding: utf-8 -*-

import cmath
import gameconst
import functools
import random
import math

import gamePlay_gamePlay as GGD
import decimal
import KBEngine


@functools.lru_cache(maxsize=1024)
def getMapId(spaceNo):
    if spaceNo >= gameconst.COPIED_SPACE_NO_START:
        return spaceNo // gameconst.SPACE_NO_INTERVAL
    return spaceNo


def whatSpaceMap(spaceNo):
    mapId = getMapId(spaceNo)

    if isLineSpace(spaceNo):
        _ = gameconst.spaceDict[mapId]
    elif mapId in gameconst.spaceDict:
        _ = gameconst.spaceDict[mapId]
    elif mapId in GGD.datas:
        spaceType = GGD.datas[mapId]['type']
        if gameconst.DungeonType.isBigWorldDungeon(spaceType):
            _ = gameconst.spaceDict[gameconst.MapIdDef.mapXinYuanCheng]
        else:
            # in other case, is common dungeon
            _ = gameconst.spaceDict[mapId]

    elif mapId == gameconst.MapIdDef.mapSpecial:
        _ = gameconst.spaceDict[gameconst.MapIdDef.mapXinYuanCheng]
    else:
        raise TypeError('Unknown spaceNo :{}'.format(spaceNo))

    path = 'spaces/%s' % _['map']
    return path


@functools.lru_cache(1024, typed=False)
def whatSpaceType(spaceNo):
    mapId = getMapId(spaceNo)
    if not mapId:
        return gameconst.SpaceType.UnKownSpaceType

    return GGD.datas[mapId]['type']


@functools.lru_cache(1024, typed=False)
def whatSpaceTypeWithSub(spaceNo):
    mapId = getMapId(spaceNo)
    if not mapId:
        return gameconst.SpaceType.UnKownSpaceType, 0

    return GGD.datas[mapId]['type'], GGD.datas[mapId]['subType']


def bornPosFromData(d):
    _radius = d.get('Props', {}).get('Radius', 0.0)
    if _radius <= 0:
        return (d['PosX'], d['PosY'], d['PosZ'])

    _radius = random.uniform(0.0, _radius)
    _theta = random.uniform(0.0, 2 * cmath.pi)
    _x = d['PosX'] + _radius * math.cos(_theta)
    _z = d['PosZ'] + _radius * math.sin(_theta)
    return (_x, d['PosY'], _z)


def whatSpaceBornPoint(spaceNo):
    mapId = getMapId(spaceNo)
    import utils
    dunSData = utils.getDunStructureModuleData(mapId)
    if 'BornPos' not in dunSData:
        return None

    d, *_ = dunSData['BornPos'].values()
    return bornPosFromData(d)

def whatSpaceBornPosAndDir(mapId):
    import utils
    dunSData = utils.getDunStructureModuleData(mapId)
    if 'BornPos' not in dunSData:
        return None, None

    _data = random.choice(list(dunSData['BornPos'].values()))
    return bornPosFromData(_data), (0, 0, _data['Dir'])


def range2D(p1, p2):
    return cmath.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)


def range3D(p1, p2):
    return cmath.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2 + (p1[2] - p2[2]) ** 2)


def isStaticSpace(spaceNo):
    return 0 < spaceNo < gameconst.COPIED_SPACE_NO_START or spaceInSpecial(spaceNo)


def isLineSpace(spaceNo):
    return whatSpaceType(spaceNo) == gameconst.SpaceType.SpaceLine


def isWolrdBossSpace(spaceNo):
    _type, _sub = whatSpaceTypeWithSub(spaceNo)
    return _type == gameconst.SpaceType.SpaceLine and _sub == gameconst.SpaceSubType.Boss


def isDuelMapId(mapId):
    _type, _sub = GGD.datas[mapId]['type'], GGD.datas[mapId]['subType']
    return _type == gameconst.SpaceType.SpaceLine and _sub == gameconst.SpaceSubType.Yanwu

def isDuelGround(spaceNo):
    _type, _sub = whatSpaceTypeWithSub(spaceNo)
    # 演武场 sub == 2
    if _type == gameconst.SpaceType.SpaceLine and _sub == gameconst.SpaceSubType.Yanwu:
        return True

    return False

def isCubeSpace(spaceNo):
    return whatSpaceType(spaceNo) == gameconst.SpaceType.SpaceCube


def isCubeReady(spaceNo):
    _mapId = getMapId(spaceNo)
    return _mapId == 3100


def isWonderLandSpace(spaceNo):
    return whatSpaceType(spaceNo) == gameconst.SpaceType.SpaceWonderLand

def isSiegeWarSpace(spaceNo):
    return whatSpaceType(spaceNo) == gameconst.SpaceType.SpaceSiegeWar

def getCubeSpaceNo(mapId):
    return getLineSpaceNo(mapId, 0)


def isWorldLineType(lineType):
    return lineType in gameconst.MapIdDef.mapWorldSet


def spaceInSpecial(spaceNo):
    return False


@functools.lru_cache(1024, typed=False)
def spaceInWorldLine(spaceNo):
    return isWorldLineType(getLineType(spaceNo))

def getDungeonStubGlobalName(dungeonNo, dungeonEnterType=gameconst.DungeonEnterType.UNKNOWN):
    if dungeonEnterType == gameconst.DungeonEnterType.TEAM:
        return 'dungeon_{}_t'.format(dungeonNo)
    elif dungeonEnterType == gameconst.DungeonEnterType.SINGLE:
        return 'dungeon_{}_s'.format(dungeonNo)
    elif dungeonEnterType == gameconst.DungeonEnterType.RAID:
        return 'dungeon_{}_r'.format(dungeonNo)
    else:
        return 'dungeon_%s' % dungeonNo

def getLineSpaceNo(lineType, lineNo=-1):
    import utils
    if lineNo < 0:
        lineNo = random.randint(0, utils.getLineMaxNumber(lineType) - 1)
    return lineType * gameconst.SPACE_NO_INTERVAL + lineNo


def getLineNo(spaceNo):
    if not isLineSpace(spaceNo):
        return -1

    return spaceNo % gameconst.SPACE_NO_INTERVAL


def getLineType(spaceNo):
    if not isLineSpace(spaceNo):
        return 0

    return spaceNo // gameconst.SPACE_NO_INTERVAL


def getDungeonNoBySpaceNo(spaceNo):
    if spaceNo >= gameconst.SPACE_NO_INTERVAL:
        return spaceNo // gameconst.SPACE_NO_INTERVAL
    return spaceNo


def setBit(x, index, on=True):
    bi = int(index / 8)
    si = index % 8
    qfl = len(x)

    if on and qfl < bi + 1:
        x.extend([0] * (bi - qfl + 1))

    tmp = 1 << si

    if on:
        x[bi] |= tmp
    else:
        if getBit(x, index):
            x[bi] ^= tmp

    return x


def getBit(x, index):
    bi = int(index / 8)
    si = index % 8
    if len(x) < bi + 1:
        return False
    else:
        return (x[bi] & (1 << si)) != 0


# 设置int64整数列表表示的bit vector中第index个bit值
def setInt64VectorBit(intList, index, on=True):
    ii = index // 64
    bi = index % 64
    if on:
        intList[ii] |= 1 << bi
    else:
        if intList[ii] & (1 << bi):
            intList[ii] ^= 1 << bi
    return intList


# 获得int64整数列表表示的bit vector中第index个bit值
def getInt64VectorBit(intList, index):
    ii = index // 64
    bi = index % 64
    return (intList[ii] >> bi) & 1 > 0


# 获得int64整数列表表示的bit vector中所有1所在的bit所在的下标
def getInt64VectorOnIndexes(intList):
    bitList = []
    i = 0
    for staBit in intList:
        if not staBit:
            continue
        binStrRev = bin(staBit)[2:][::-1]
        idx = binStrRev.find('1')
        while idx != -1:
            bitList.append(int(idx + i * 64))
            idx = binStrRev.find('1', idx + 1)
        i += 1
    return bitList


def hashableJsonHook(obj):
    for v in obj.values():
        hash(v)
    return obj


def round2(number, ndigit=None):
    if ndigit and ndigit < 0:
        return round(number, ndigit)
    if ndigit is None:
        TWOPLACES = decimal.Decimal()
    else:
        TWOPLACES = decimal.Decimal(10) ** (-ndigit)
    r = decimal.Decimal(str(number)).quantize(TWOPLACES, rounding=decimal.ROUND_HALF_UP)
    if ndigit is None:
        return int(r)
    else:
        return float(r)


def getStubIndex():
    return KBEngine.getComponentGroupOrder()


def calcPosPoolIndex(rId, index):
    return rId * gameconst.ENTITY_POS_POLICY_MAX_NUM + index


def getPosPoolIndex(posIndex):
    return posIndex % gameconst.ENTITY_POS_POLICY_MAX_NUM


def getGameEntityId(entId):
    return entId * 1000


def getEntityId(gameEntityId):
    return gameEntityId // 1000

def isDungeonSpace(spaceNo):
    return whatSpaceType(spaceNo) in (gameconst.SpaceType.SpaceWorldDungeon,
                                      gameconst.SpaceType.SpaceNormalDungeon)

def spaceForbidTeamFollow(spaceNo):
    if not spaceNo:
        return True

    mapId = getMapId(spaceNo)
    sceneInfo = GGD.datas.get(mapId, None)
    if sceneInfo and not sceneInfo['ifTeamFollow']:
        return True

    return False

def spaceForbidAutoFight(spaceNo):
    if not spaceNo:
        return True

    mapId = getMapId(spaceNo)
    sceneInfo = GGD.datas.get(mapId, None)
    if sceneInfo and not sceneInfo['ifAutoFight']:
        return True

    return False

def isBigWorldNaviCostLikedSpace(spaceNo):
    """打点地图跟大世界场景公用一份，但是不是大世界"""
    _type, _sub = whatSpaceTypeWithSub(spaceNo)
    # if _type == gameconst.SpaceType.SpaceWorldDungeon:
    #     return True

    if _type == gameconst.SpaceType.SpaceLine:
        return True

    return False

def isSingleDungeonSpace(spaceNo):
    if not isDungeonSpace(spaceNo):
        return False
    dungeonNo = getDungeonNoBySpaceNo(spaceNo)
    enterType = GGD.datas[dungeonNo].get('enterType', gameconst.DungeonEnterType.UNKNOWN)
    if enterType == gameconst.DungeonEnterType.BOTH:
        dunSpaceStart, dunSpaceEnd = gameconst.SpaceType.getSingleDungeonSpaceNoRange(dungeonNo)
        return dunSpaceStart <= spaceNo < dunSpaceEnd
    else:
        return enterType == gameconst.DungeonEnterType.SINGLE


def isTeamDungeonSpace(spaceNo):
    if not isDungeonSpace(spaceNo):
        return False
    dungeonNo = getDungeonNoBySpaceNo(spaceNo)
    enterType = GGD.datas[dungeonNo].get('enterType', gameconst.DungeonEnterType.UNKNOWN)
    if enterType == gameconst.DungeonEnterType.BOTH:
        dunSpaceStart, dunSpaceEnd = gameconst.SpaceType.getTeamDungeonSpaceNoRange(dungeonNo)
        return dunSpaceStart <= spaceNo < dunSpaceEnd
    else:
        return enterType == gameconst.DungeonEnterType.TEAM

def isRaidDungeonSpace(spaceNo):
    if not isDungeonSpace(spaceNo):
        return False
    dungeonNo = getDungeonNoBySpaceNo(spaceNo)
    enterType = GGD.datas[dungeonNo].get('enterType', gameconst.DungeonEnterType.UNKNOWN)
    if enterType == gameconst.DungeonEnterType.RAID:
        return True
    return False
