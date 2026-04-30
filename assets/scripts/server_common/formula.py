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
def fetchMapId(spaceNo):
    if spaceNo >= gameconst.COPIED_SPACE_NO_START:
        return spaceNo // gameconst.SPACE_NO_INTERVAL
    return spaceNo


def getSpaceMap(spaceNo):
    mapId = fetchMapId(spaceNo)

    if inLineScene(spaceNo):
        _ = gameconst.gSpaceDict[mapId]
    elif mapId in gameconst.gSpaceDict:
        _ = gameconst.gSpaceDict[mapId]
    elif mapId in GGD.datas:
        spaceType = GGD.datas[mapId]['type']
        if gameconst.DungeonTypeJudge.isBigWorldDungeon(spaceType):
            _ = gameconst.gSpaceDict[gameconst.MapIdDef.mapXinYuanCheng]
        else:
            # in other case, is common dungeon
            _ = gameconst.gSpaceDict[mapId]

    elif mapId == gameconst.MapIdDef.mapSpecial:
        _ = gameconst.gSpaceDict[gameconst.MapIdDef.mapXinYuanCheng]
    else:
        raise TypeError('Unknown spaceNo :{}'.format(spaceNo))

    path = 'spaces/%s' % _['map']
    return path

@functools.lru_cache(1024, typed=False)
def getSpaceType(spaceNo):
    mapId = fetchMapId(spaceNo)
    if not mapId:
        return gameconst.SpaceType.UnKownSpaceType

    return GGD.datas[mapId]['type']

@functools.lru_cache(1024, typed=False)
def getSpaceSubType(spaceNo):
    mapId = fetchMapId(spaceNo)
    if not mapId:
        return gameconst.SpaceSubType.Yanwu

    return GGD.datas[mapId]['subType']

@functools.lru_cache(1024, typed=False)
def getSpaceTypeWithSub(spaceNo):
    mapId = fetchMapId(spaceNo)
    if not mapId:
        return gameconst.SpaceType.UnKownSpaceType, 0

    return GGD.datas[mapId]['type'], GGD.datas[mapId]['subType']


def bornPosFromDunData(d):
    _radius = d.get('Props', {}).get('Radius', 0.0)
    if _radius <= 0:
        return (d['PosX'], d['PosY'], d['PosZ'])

    _radius = random.uniform(0.0, _radius)
    _theta = random.uniform(0.0, 2 * cmath.pi)
    _x = d['PosX'] + _radius * math.cos(_theta)
    _z = d['PosZ'] + _radius * math.sin(_theta)
    return (_x, d['PosY'], _z)


def getSpaceBornPoint(spaceNo):
    mapId = fetchMapId(spaceNo)
    import utils
    dunSData = utils.getDunStructModData(mapId)
    if 'BornPos' not in dunSData:
        return None

    d, *_ = dunSData['BornPos'].values()
    return bornPosFromDunData(d)

def getSpaceBornPosAndDir(mapId):
    import utils
    dunSData = utils.getDunStructModData(mapId)
    if 'BornPos' not in dunSData:
        return None, None

    _data = random.choice(list(dunSData['BornPos'].values()))
    return bornPosFromDunData(_data), (0, 0, _data['Dir'] * math.pi / 180)


def inStaticScene(spaceNo):
    return 0 < spaceNo < gameconst.COPIED_SPACE_NO_START


def inLineScene(spaceNo):
    return getSpaceType(spaceNo) == gameconst.SpaceType.SpaceLine


def inWolrdBossScene(spaceNo):
    _type, _sub = getSpaceTypeWithSub(spaceNo)
    return _type == gameconst.SpaceType.SpaceLine and _sub == gameconst.SpaceSubType.Boss


def checkDuelMapId(mapId):
    _type, _sub = GGD.datas[mapId]['type'], GGD.datas[mapId]['subType']
    return _type == gameconst.SpaceType.SpaceLine and _sub == gameconst.SpaceSubType.Yanwu

def inDuelScene(spaceNo):
    _type, _sub = getSpaceTypeWithSub(spaceNo)
    # 演武场 sub == 2
    if _type == gameconst.SpaceType.SpaceLine and _sub == gameconst.SpaceSubType.Yanwu:
        return True

    return False

def inCubeScene(spaceNo):
    return getSpaceType(spaceNo) == gameconst.SpaceType.SpaceCube


def inCubeReadyScene(spaceNo):
    _mapId = fetchMapId(spaceNo)
    return cube_room.datas.get(_mapId, {}).get('type') == gameconst.CubeRoomType.READY


def inWonderLandScene(spaceNo):
    return getSpaceType(spaceNo) == gameconst.SpaceType.SpaceWonderLand

def inSiegeWarScene(spaceNo):
    return getSpaceType(spaceNo) == gameconst.SpaceType.SpaceSiegeWar

def inYanWuScene(spaceNo):
    return getSpaceType(spaceNo) == gameconst.SpaceType.SpaceLine and getSpaceSubType(spaceNo) == gameconst.SpaceSubType.Yanwu


def checkWorldLineType(lineType):
    return lineType in gameconst.MapIdDef.mapWorldSet


@functools.lru_cache(1024, typed=False)
def inWorldLineScene(spaceNo):
    return checkWorldLineType(parseLineType(spaceNo))

def fetchDungeonStubGlobalName(dungeonNo, dungeonEnterType=gameconst.DungeonEnterTypeEnum.UNKNOWN):
    if dungeonEnterType == gameconst.DungeonEnterTypeEnum.TEAM:
        return 'dungeon_{}_t'.format(dungeonNo)
    elif dungeonEnterType == gameconst.DungeonEnterTypeEnum.SINGLE:
        return 'dungeon_{}_s'.format(dungeonNo)
    elif dungeonEnterType == gameconst.DungeonEnterTypeEnum.RAID:
        return 'dungeon_{}_r'.format(dungeonNo)
    elif dungeonEnterType == gameconst.DungeonEnterTypeEnum.GUILD:
        return 'dungeon_{}_g'.format(dungeonNo)
    else:
        return 'dungeon_%s' % dungeonNo

def combineLineSpaceNo(lineType, lineNo=-1):
    import utils
    if lineNo < 0:
        lineNo = random.randint(0, utils.fetchLineMaxNumber(lineType) - 1)
    return lineType * gameconst.SPACE_NO_INTERVAL + lineNo


def parseLineNo(spaceNo):
    if not (inLineScene(spaceNo) or inCubeScene(spaceNo)):
        return -1

    return spaceNo % gameconst.SPACE_NO_INTERVAL


def parseLineType(spaceNo):
    if not inLineScene(spaceNo):
        return 0

    return spaceNo // gameconst.SPACE_NO_INTERVAL


def parseDungeonNoBySpaceNo(spaceNo):
    if spaceNo >= gameconst.SPACE_NO_INTERVAL:
        return spaceNo // gameconst.SPACE_NO_INTERVAL
    return spaceNo


def bset(x, index, on=True):
    bi = int(index / 8)
    si = index % 8
    qfl = len(x)

    if on and qfl < bi + 1:
        x.extend([0] * (bi - qfl + 1))

    tmp = 1 << si

    if on:
        x[bi] |= tmp
    else:
        if bitGet(x, index):
            x[bi] ^= tmp

    return x


def bitGet(x, index):
    bi = int(index / 8)
    si = index % 8
    if len(x) < bi + 1:
        return False
    else:
        return (x[bi] & (1 << si)) != 0


# 设置int64整数列表表示的bit vector中第index个bit值
def setInt64ListBit(intList, index, on=True):
    ii = index // 64
    bi = index % 64
    if on:
        intList[ii] |= 1 << bi
    else:
        if intList[ii] & (1 << bi):
            intList[ii] ^= 1 << bi
    return intList


# 获得int64整数列表表示的bit vector中第index个bit值
def getInt64ListBit(intList, index):
    ii = index // 64
    bi = index % 64
    return (intList[ii] >> bi) & 1 > 0


# 获得int64整数列表表示的bit vector中所有1所在的bit所在的下标
def getInt64ListOnIndexes(intList):
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


def fetchStubIndex():
    return KBEngine.getComponentGroupOrder()


def calcPosPoolIndex(rId, index):
    return rId * gameconst.ENTITY_POS_POLICY_MAX_NUM + index


def fetchPosPoolIndex(posIndex):
    return posIndex % gameconst.ENTITY_POS_POLICY_MAX_NUM


def inDungeonScene(spaceNo):
    return getSpaceType(spaceNo) in (gameconst.SpaceType.SpaceWorldDungeon,
                                      gameconst.SpaceType.SpaceNormalDungeon,
                                      gameconst.SpaceType.SpaceGuild)

def inMineWarScene(spaceNo):
    return fetchMapId(spaceNo) in MBMA.datas.keys() and parseLineNo(spaceNo) == 0

def getMineWarMineArea(spaceNo):
    mapId = fetchMapId(spaceNo)
    for line, data in MBMA.datas.items():
        if mapId in data['sceneList']:
            return data['sceneList']
    return []

def getMineWarBattleArea(spaceNo):
    sceneList = getMineWarMineArea(spaceNo)
    return sceneList[-1] if sceneList else 0

def isMineWarMineArea(spaceNo):
    return getMineWarBattleArea(spaceNo) > 0

def checkSpaceForbidTeamFollow(spaceNo):
    if not spaceNo:
        return True

    mapId = fetchMapId(spaceNo)
    sceneInfo = GGD.datas.get(mapId, None)
    if sceneInfo and not sceneInfo['ifTeamFollow']:
        return True

    return False

def checkSpaceForbidAutoFight(spaceNo):
    if not spaceNo:
        return True

    mapId = fetchMapId(spaceNo)
    sceneInfo = GGD.datas.get(mapId, None)
    if sceneInfo and not sceneInfo['ifAutoFight']:
        return True

    return False

def isBigWorldNaviCostLikedSpace(spaceNo):
    """打点地图跟大世界场景公用一份，但是不是大世界"""
    _type, _sub = getSpaceTypeWithSub(spaceNo)
    if _type == gameconst.SpaceType.SpaceLine:
        return True

    return False

def inSingleDungeonScene(spaceNo):
    if not inDungeonScene(spaceNo):
        return False
    dungeonNo = parseDungeonNoBySpaceNo(spaceNo)
    enterType = GGD.datas[dungeonNo].get('enterType', gameconst.DungeonEnterTypeEnum.UNKNOWN)
    if enterType == gameconst.DungeonEnterTypeEnum.BOTH:
        dunSpaceStart, dunSpaceEnd = gameconst.SpaceType.getSingleDungeonSpaceRange(dungeonNo)
        return dunSpaceStart <= spaceNo < dunSpaceEnd
    else:
        return enterType == gameconst.DungeonEnterTypeEnum.SINGLE


def inTeamDungeonScene(spaceNo):
    if not inDungeonScene(spaceNo):
        return False
    dungeonNo = parseDungeonNoBySpaceNo(spaceNo)
    enterType = GGD.datas[dungeonNo].get('enterType', gameconst.DungeonEnterTypeEnum.UNKNOWN)
    if enterType == gameconst.DungeonEnterTypeEnum.BOTH:
        dunSpaceStart, dunSpaceEnd = gameconst.SpaceType.getTeamDungeonSpaceRange(dungeonNo)
        return dunSpaceStart <= spaceNo < dunSpaceEnd
    else:
        return enterType == gameconst.DungeonEnterTypeEnum.TEAM

def inRaidDungeonScene(spaceNo):
    if not inDungeonScene(spaceNo):
        return False
    dungeonNo = parseDungeonNoBySpaceNo(spaceNo)
    enterType = GGD.datas[dungeonNo].get('enterType', gameconst.DungeonEnterTypeEnum.UNKNOWN)
    if enterType == gameconst.DungeonEnterTypeEnum.RAID:
        return True
    return False

def inGuildBossDungeonScene(spaceNo):
    if not inDungeonScene(spaceNo):
        return False
    dungeonNo = parseDungeonNoBySpaceNo(spaceNo)
    spaceType = GGD.datas[dungeonNo].get('type', gameconst.DungeonSpaceTypeEnum.UNKNOWN)
    enterType = GGD.datas[dungeonNo].get('enterType', gameconst.DungeonEnterTypeEnum.UNKNOWN)
    if spaceType == gameconst.DungeonSpaceTypeEnum.GUILD_BOSS \
        and enterType == gameconst.DungeonEnterTypeEnum.GUILD:
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
