# -*- coding: utf-8 -*-

import cmath
import gameconst
import functools
import random
import math
import cube_room

import gamePlay_gamePlay as GGD
import decimal
import KBEngine
import mineBattle_miningArea as MBMA
import experience_revenue as ERD

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

def whatSpaceName(spaceNo):
    lineType = getLineType(spaceNo)
    mapCfg = GGD.datas.get(lineType, {})
    return mapCfg.get('name', '')

@functools.lru_cache(1024, typed=False)
def whatSpaceType(spaceNo):
    mapId = getMapId(spaceNo)
    if not mapId:
        return gameconst.SpaceType.UnKownSpaceType

    return GGD.datas[mapId]['type']

@functools.lru_cache(1024, typed=False)
def whatSpaceSubType(spaceNo):
    mapId = getMapId(spaceNo)
    if not mapId:
        return gameconst.SpaceSubType.Yanwu

    return GGD.datas[mapId]['subType']

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
    return bornPosFromData(_data), (0, 0, _data['Dir'] * math.pi / 180)


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
    return cube_room.datas.get(_mapId, {}).get('type') == gameconst.CubeRoomType.READY


def isWonderLandSpace(spaceNo):
    return whatSpaceType(spaceNo) == gameconst.SpaceType.SpaceWonderLand

def isSiegeWarSpace(spaceNo):
    return whatSpaceType(spaceNo) == gameconst.SpaceType.SpaceSiegeWar

def isYanWuSpace(spaceNo):
    return whatSpaceType(spaceNo) == gameconst.SpaceType.SpaceLine and whatSpaceSubType(spaceNo) == gameconst.SpaceSubType.Yanwu

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
    elif dungeonEnterType == gameconst.DungeonEnterType.GUILD:
        return 'dungeon_{}_g'.format(dungeonNo)
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
    for i, num in enumerate(intList):
        if not num:
            continue
        # 使用位运算查找置位的比特位，比字符串操作更快
        while num:
            # 找到最低位的1的位置
            bit_pos = (num & -num).bit_length() - 1
            # 计算全局索引
            bit_index = bit_pos + i * 64
            bitList.append(bit_index)
            # 清除当前最低位的1
            num &= num - 1
    return bitList


def test_getInt64VectorOnIndexes():
    """
    测试getInt64VectorOnIndexes函数的正确性
    """
    # 测试单个数组元素
    assert getInt64VectorOnIndexes([0x1]) == [0]
    assert getInt64VectorOnIndexes([0x2]) == [1]
    assert getInt64VectorOnIndexes([0x3]) == [0, 1]
    assert getInt64VectorOnIndexes([0x8000000000000000]) == [63]

    # 测试多个数组元素
    assert getInt64VectorOnIndexes([0x0, 0x1]) == [64]
    assert getInt64VectorOnIndexes([0x1, 0x1]) == [0, 64]
    assert getInt64VectorOnIndexes([0x3, 0x5]) == [0, 1, 64, 66]

    # 测试全1的情况
    assert len(getInt64VectorOnIndexes([0xFFFFFFFFFFFFFFFF])) == 64
    assert getInt64VectorOnIndexes([0xFFFFFFFFFFFFFFFF]) == list(range(64))

    print("All tests passed!")


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
                                      gameconst.SpaceType.SpaceNormalDungeon,
                                      gameconst.SpaceType.SpaceGuild)

def isMineWarSpace(spaceNo):
    return getMapId(spaceNo) in MBMA.datas.keys() and getLineNo(spaceNo) == 0

def getMineWarMineArea(spaceNo):
    mapId = getMapId(spaceNo)
    for line, data in MBMA.datas.items():
        if mapId in data['sceneList']:
            return data['sceneList']
    return []

def getMineWarBattleArea(spaceNo):
    sceneList = getMineWarMineArea(spaceNo)
    return sceneList[-1] if sceneList else 0

def isMineWarMineArea(spaceNo):
    return getMineWarBattleArea(spaceNo) > 0

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

def isGuildBossDungeonSpace(spaceNo):
    if not isDungeonSpace(spaceNo):
        return False
    dungeonNo = getDungeonNoBySpaceNo(spaceNo)
    spaceType = GGD.datas[dungeonNo].get('type', gameconst.DungeonSpaceType.UNKNOWN)
    enterType = GGD.datas[dungeonNo].get('enterType', gameconst.DungeonEnterType.UNKNOWN)
    if spaceType == gameconst.DungeonSpaceType.GUILD_BOSS \
        and enterType == gameconst.DungeonEnterType.GUILD:
        return True
    return False

def getKillMonsterRewardConfig(monsterLevel, playerLevel):
        maxLevel = (ERD.maxKey - 1) // 2
        deltaLevel = monsterLevel - playerLevel
        if deltaLevel >= 0:
            levelDelta = min(deltaLevel, maxLevel)
        else:
            levelDelta = max(deltaLevel, -maxLevel)

        config = ERD.revenueLevelGapDic[levelDelta]
        return config
