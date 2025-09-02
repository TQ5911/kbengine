# -*- coding: utf-8 -*-
import builtins
import time
import json
import random
import math
import uuid
import ast
import importlib
import re
import datetime
import gametimer
import hashlib
from decimal import Decimal
from KBEDebug import *

import randomName_robotName as RND
import formula_generalFormula as FGFD
import fightProp_fightTargetType as FPFTTD

import gamePlay_gamePlay as GPGP
import gamePlay_enterScene as GPES
import const_const as CCT
import NPC_teleporter as NTD
import creep_force
import PKData_PKData as PKD
import PKData_moralValueEffect as PKMVE
import performanceLevel_set as PLSD
import teamMatch_matchConfig as TMMCD
import login_set as LGS
import message_Message as MSG
import serverList_serverList as SLSL
import cityBattle_firstTime as CBFT
import cityBattle_config as CBC
import conflict_status_def as C_S_DD
import NPC_Pick as NPD
import creep_base as CBD

import KBEngine
from KBEDebug import *
import crontab
import Math
import sMath
from Crypto.Cipher import AES
import base64

import gameconst
import gameglobal
import gameconfig
import formula
import gameengine
import dataUtils
import functools
import urllib
import urllib.parse
import combatSkill
import localizeConst_localizeConst as LC_LCD

tempTime = time.time
ASCII_LIST = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U',
              'V', 'W', 'X', 'Y', 'Z',
              'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
              'v', 'w', 'x', 'y', 'z',
              '0', '1', '2', '3', '4', '5', '6', '7', '8', '9']


class Swallower(object):
    def __getattribute__(self, name):
        if name.startswith('__') and name.endswith('__'):
            return super().__getattribute__(name)
        return self

    def __call__(self, *args, **kw):
        pass

    def __bool__(self):
        return False


def getNow():
    return int(time.time())

def getTimestamp64(t=None):
    t = t or time.time()
    return int(round(t * 1000))


def getIntTimestamp64(sDate):
    if sDate == '':
        return 0
    timeArr = time.strptime(sDate, "%Y%m%d%H%M%S")
    return int(round(int(time.mktime(timeArr)) * 1000))


def getNowTimeStr(now=None):
    if not now:
        now = time.time()

    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(now))


# 1136185445 -> '20060102150405'
def getTimeStrFromTimeStamp(timeStamp=0):
    timeStamp = timeStamp or int(time.time())
    return time.strftime('%Y%m%d%H%M%S', time.localtime(timeStamp))


def getIntTimestamp(sDate):
    if sDate == '':
        return 0
    timeArr = time.strptime(sDate, "%Y%m%d%H%M%S")
    return int(time.mktime(timeArr))


def getTodayZeroSec():
    today = datetime.date.today()
    return int(time.mktime(today.timetuple()))


def getCurrentTimeFmt():
    curr_time = datetime.datetime.now()
    timestamp = datetime.datetime.strftime(curr_time, '%Y-%m-%d %H:%M:%S')
    return timestamp


def getTodayFiveSec():
    todayFive = getTodayZeroSec() + 18000
    if getNow() < todayFive:
        return todayFive - 24 * 3600
    else:
        return todayFive


__builtin_mapping__ = builtins.__dict__


def getBuiltin(builtinName):
    if builtinName in __builtin_mapping__:
        return __builtin_mapping__[builtinName]


def instanceof(ent, entType):
    return ent.__class__.__name__ == entType


def getPythonServer():
    import socket, struct
    ipInt, port = KBEngine.address()

    return '%s:%s' % (socket.inet_ntoa(struct.pack("I", ipInt)), port)


# |16bit-serverId|22bit-timestamp|26bit-seqId|
def generateUniqGlobalId():
    import gameconfig
    serverId = int(gameconfig.serverId())
    gbId = serverId << gameconst.GLOBAL_SERVER_SHIFT
    nowTime = getNow()

    timestampIdx = int((nowTime - gameconst.GBID_TIME_BASE) / gameconst.GBID_TIME_INTERVAL)
    gbId = gbId + timestampIdx
    gbId = gbId << gameconst.GLOBAL_TIME_SHIFT

    if gameglobal.gbIdTimestampIdx != timestampIdx:
        gameglobal.gbIdSeqId = gameglobal.localBaseApp.getStartGbId()
        gameglobal.gbIdTimestampIdx = timestampIdx

    gameglobal.gbIdSeqId += 1
    return gbId + gameglobal.gbIdSeqId


# |18bit-serverId|6bit-groupOrder|29bit-timestamp|11bit-seqId|
def generateObId():
    import gameconfig
    serverId = int(gameconfig.serverId())
    gid = KBEngine.getComponentGroupOrder()
    ts = getNow() - 1640163600  # seconds since 2021-12-22 17:00
    if gameglobal.genObIdTs != ts:
        gameglobal.genObIdTs = ts
        gameglobal.genObIdSeqId = 0

    gameglobal.genObIdSeqId += 1
    seqId = gameglobal.genObIdSeqId
    if seqId >= 2 ** 11:
        seqId = 2 ** 11 - 1
        ERROR_MSG('generateObId reach max', )

    return int(str(serverId) + str((gid << 40) + (ts << 11) + seqId))


def getEntity(entityClass):
    module = __import__(entityClass)
    clazz = getattr(module, entityClass)
    for k, v in KBEngine.entities.items():
        if type(v).__name__ == clazz.__name__:
            return v


def getEntityList(entityClass):
    module = __import__(entityClass)
    clazz = getattr(module, entityClass)

    res = []
    for k, v in KBEngine.entities.items():
        if type(v).__name__ == clazz.__name__:
            res.append(v)

    return res


def getAllAvatarByGm(su, box):
    res = getEntityList("Avatar")
    data = []
    for ent in res:
        data.append({'entityId': ent.id, 'roleName': ent.getRoleCacheAttr('name'), 'gbId': ent.gbID})
    box.onGetAllPlayer(su, {KBEngine.getComponentGroupOrder(): data})


def getAvatar():
    return getEntity("Avatar")


def getAvatarByGbId(gbId):
    eid = gameglobal.roleGBIDToEntId.get(gbId, 0)
    return KBEngine.entities.get(eid)


def getEntityRealEntity(ent):
    if ent.IsAvatarMirror or ent.IsCreation or ent.IsPet or ent.IsSummon:
        if ent.hostId:
            ent = ent.getHost() or ent

    return ent


def isJoinCombat(entity, src):
    if (src.IsCombatUnit or src.IsCreation) and entity.IsAICombatUnit and entity.bornState not in \
            gameconst.BornStateType.joinCombatTup:
        return False

    if src.hasState(C_S_DD.datas.relive):
        return False

    return True


def turnPos(pos, angle):
    angle = 360 - angle
    angle = angle * math.pi / 180
    cosTheta = math.cos(angle)
    sinTheta = math.sin(angle)
    x, y = pos
    x, y = (cosTheta * x - sinTheta * y, sinTheta * x + cosTheta * y)
    return x, y


# 简单随机下，非均匀
def getRandomPos(center, radii):
    r = radii * random.random()
    theta = 2 * math.pi * random.random()

    return Math.Vector3(center) + Math.Vector3(r * math.sin(theta), 0, r * math.cos(theta))


def _iterPushAroundPoint(position: Math.Vector3, layer: int):
    position.x -= layer
    position.z -= layer
    _orgX = position.x
    _orgZ = position.z
    _layerOffset = layer * 2
    for _xOffset in range(_layerOffset + 1):
        position.x = _orgX + _xOffset
        if 0 < _xOffset < _layerOffset:
            position.z = _orgZ
            yield position
            position.z = _orgZ + _layerOffset
            yield position
        for _zOffset in range(_layerOffset + 1):
            position.z = _orgZ + _zOffset
            yield position


def monsterRandomPos(center, radii, count, idx):
    eachPi = 2 * math.pi / count
    r = radii * math.sqrt(random.random())
    theta = eachPi * idx + eachPi * random.random()
    return Math.Vector3(center) + Math.Vector3(r * math.sin(theta), 0, r * math.cos(theta))


def getStringFromBytes(s, encoding='utf-8'):
    return str(s, encoding)


def getStringFromBytesRedis(s, encoding='utf-8'):
    ret = str(s, encoding)
    if ret == '""':
        return ''
    else:
        return ret


def isHitByRate(rate):
    if rate <= 0 or rate > 1:
        return False
    result = random.uniform(0, 1)
    return result <= rate


def weightChoice(seq, weights, num=1):
    if len(seq) != len(weights):
        return [], []

    if num > len(seq):
        return [], []

    choices = []
    for n in range(num):
        sumP = 0

        for i in range(len(weights)):
            if i in choices:
                continue
            sumP += weights[i]

        randProp = random.randint(1, sumP)
        for i, p in enumerate(weights):
            if i in choices:
                continue

            randProp = randProp - p
            if randProp <= 0:
                choices.append(i)
                break

    return [seq[i] for i in choices], choices


def reloadCls(cls):
    if not hasattr(cls, '__bases__') or not cls.__bases__ or cls.__name__ in gameglobal.reloadedCls \
            or cls.__module__ == 'builtins':
        return

    oldBases = cls.__bases__
    newBases = []
    for bs in oldBases:
        reloadCls(bs)

        mod = importlib.import_module(bs.__module__)
        newBs = getattr(mod, bs.__name__)
        newBases.append(newBs)

    cls.__bases__ = tuple(newBases)
    gameglobal.reloadedCls[cls.__name__] = 1


def resetCls(obj):
    oldCls = obj.__class__
    clsName = oldCls.__name__

    mod = importlib.import_module(oldCls.__module__)

    newCls = getattr(mod, clsName)
    reloadCls(newCls)
    obj.__class__ = newCls


def isInteger(s):
    try:
        int(s)
    except:
        return False
    return True


def isEntityId(s):
    if isInteger(s) and int(s) < gameconst.GBID_BASE:
        return True
    return False


def isGbId(s):
    if isInteger(s) and int(s) > gameconst.GBID_BASE:
        return True
    return False


def isRoleName(player):
    return not isInteger(player) and type(player) is str


def isBaseMailBox(ent):
    return 'baseapp' in str(ent)


def isCellMailBox(ent):
    return 'cellapp' in str(ent)


def getUUID():
    return str(uuid.uuid1())


def generateGameEntityId(orgGameEntityId: int, count: int):
    _id = orgGameEntityId * 1000
    for i in range(count):
        _id += 1
        yield _id

def generateGameEntityIdFrom(orgGameEntityId: int, count: int, fromIdx: int):
    _id = orgGameEntityId * 1000 + fromIdx
    for i in range(count):
        _id += 1
        yield _id

def getGidFromGameEntityId(gameEntityId: int):
    return gameEntityId // 1000


def splitGameEntityId(gameEntityId: int):
    gid = getGidFromGameEntityId(gameEntityId)
    gct = gameEntityId - gid * 1000
    return gid, gct


def randomDelayTime(T, rdmRange=1.0):
    rdmVal = random.random() * rdmRange

    _r = round(T + rdmVal, 2)

    return _r if _r > 0.00 else 0.00


def isDiffDay(nowTime, lastTime, cycleTime):
    # 这里如果-cycleTime,如果碰到lastTime传0,则会变为负值,会导致localTime报错,所以都往后进行推算
    nowTime += gameconst.ONE_DAY_SECONDS - cycleTime
    lastTime += gameconst.ONE_DAY_SECONDS - cycleTime
    stNowTime = time.localtime(nowTime)
    stLastTime = time.localtime(lastTime)
    if stNowTime.tm_year == stLastTime.tm_year and stNowTime.tm_mon == stLastTime.tm_mon and stNowTime.tm_mday == stLastTime.tm_mday:
        return False
    return True


def isDiffWeek(nowTime, lastTime, cycleTime):
    nowTime -= cycleTime
    lastTime -= cycleTime
    stNowTime = time.localtime(nowTime)
    stLastTime = time.localtime(lastTime)
    if time.strftime('%W', stNowTime) == time.strftime('%W', stLastTime):
        return False
    return True


def isDiffMonth(nowTime, lastTime, cycleTime):
    nowTime -= cycleTime
    lastTime -= cycleTime
    stNowTime = time.localtime(nowTime)
    stLastTime = time.localtime(lastTime)
    if stNowTime.tm_year == stLastTime.tm_year and stNowTime.tm_mon == stLastTime.tm_mon:
        return False
    return True


# 从epoch开始到now，计算经历了多少天
def getDayOffsetFromEpoch(now=None):
    now = getNow() if now is None else now
    return now // gameconst.ONE_DAY_SECONDS


# 上面的逆计算
def getTimestampFromDayOffset(dayOffset):
    return dayOffset * gameconst.ONE_DAY_SECONDS


# 获取当月1日0点后offset秒时间戳
def getCurrentMonthTS(now=None, offsetSec=0):
    now = getNow() if now is None else now
    tNow = time.localtime(now)
    ts = now - (
            tNow.tm_mday - 1) * gameconst.ONE_DAY_SECONDS - tNow.tm_hour * gameconst.ONE_HOUR_SECONDES - tNow.tm_min * 60 - tNow.tm_sec + offsetSec
    return ts


# 获取下一月1日0点后offset秒时间戳
def getNextMonthTS(now=None, offsetSec=0):
    now = getNow() if now is None else now
    tNow = time.localtime(now)
    if tNow.tm_mon == 12:
        tRet = (tNow.tm_year + 1, 1, 1, 0, 0, 0, 0, 0, 0)
    else:
        tRet = (tNow.tm_year, tNow.tm_mon + 1, 1, 0, 0, 0, 0, 0, 0)

    return time.mktime(tRet) + offsetSec


# 获取当前的星期[1,7]
def getWeek(now=None):
    now = getNow() if now is None else now
    time_now = time.localtime(now)
    return time_now.tm_wday + 1


# 获取当周周一0点后offset秒时间戳
def getCurrentWeekTS(now=None, offsetSec=0):
    now = getNow() if now is None else now
    tNow = time.localtime(now)
    ts = now - tNow.tm_wday * gameconst.ONE_DAY_SECONDS - tNow.tm_hour * gameconst.ONE_HOUR_SECONDES - tNow.tm_min * 60 - tNow.tm_sec + offsetSec
    return ts


# 获取当日0点后offset秒时间戳
def getCurrentDayTS(now=None, offsetSec=0):
    now = getNow() if now is None else now
    tNow = time.localtime(now)
    ts = now - tNow.tm_hour * gameconst.ONE_HOUR_SECONDES - tNow.tm_min * 60 - tNow.tm_sec + offsetSec
    return ts


# 获取当前小时0分0秒后offset秒时间戳
def getCurrentHourTS(now=None, offsetSec=0):
    now = getNow() if now is None else now
    return gameconst.ONE_HOUR_SECONDES * (now // gameconst.ONE_HOUR_SECONDES) + offsetSec


# 获取当前时间戳(按游戏偏移量)归属年,月
def getNowYearMonth(now=None):
    now = getNow() if now is None else now
    tNow = time.localtime(now - 3600 * 5)
    return tNow.tm_year, tNow.tm_mon


def getTsFiveSec(ts):
    day_time = ts - ts % 86400 + time.timezone
    day_time += gameconst.COMMON_CYCLE_TIME
    return day_time


def countIntersDay(startTs):
    days = 0
    if not isDiffDay(startTs, getNow(), gameconst.COMMON_CYCLE_TIME):
        days = 1
    else:
        openFiveTs = getCurrentDayTS(startTs, gameconst.COMMON_CYCLE_TIME)
        todayFiveTs = getCurrentDayTS(getNow(), gameconst.COMMON_CYCLE_TIME)
        tNow = time.localtime(getNow())

        days = (todayFiveTs - openFiveTs) // 86400
        INFO_MSG('countIntersDay', todayFiveTs, openFiveTs, days)
        if tNow.tm_hour >= gameconst.GAME_REFRESH_OCLOCK:
            days += 1
        INFO_MSG('countIntersDay111', todayFiveTs, openFiveTs, days)
    return days


def getAccountAge(birthDate):
    if birthDate == 19000101:  # 1900010为默认生日值 可认为无生日
        return None
    birthYear = birthDate // 10000
    birthMon = (birthDate % 10000) // 100
    birthDay = birthDate % 100

    stNow = time.localtime(getNow())
    age = stNow.tm_year - birthYear
    if stNow.tm_mon == birthMon:
        if stNow.tm_mday < birthDay:
            age -= 1
    elif stNow.tm_mon < birthMon:
        age -= 1

    return age


def getAgeRangeData(age):
    import buyCredit_underAgeLimit as BCUAL
    ageRange = ''
    for key, ualDatas in BCUAL.datas.items():
        if age >= ualDatas['minAge'] and age < ualDatas['maxAge']:
            ageRange = key
            break
    return ageRange


def getRandomName(sex=gameconst.Sex.FEMALE):
    surnameList = RND.datas.get('surname')
    index = random.randint(0, len(surnameList) - 1)
    surname = surnameList[index]

    if sex == gameconst.Sex.FEMALE:
        secondNameList = RND.datas.get('femaleName')
    else:
        secondNameList = RND.datas.get('maleName')
    index = random.randint(0, len(secondNameList) - 1)
    secondName = secondNameList[index]
    return surname + secondName


def getRandomSex():
    sexes = [gameconst.Sex.MALE, gameconst.Sex.FEMALE]
    return random.choice(sexes)


unichr = chr
_escape_table = [unichr(x) for x in range(128)]
_escape_table[0] = u'\\0'
_escape_table[ord('\\')] = u'\\\\'
_escape_table[ord('\n')] = u'\\n'
_escape_table[ord('\r')] = u'\\r'
_escape_table[ord('\032')] = u'\\Z'
_escape_table[ord('"')] = u'\\"'
_escape_table[ord("'")] = u"\\'"


def escape_string(value, mapping=None):
    """escapes *value* without adding quote.

    Value should be unicode
    """
    return "'%s'" % value.translate(_escape_table)


def isMyself(fn):
    @functools.wraps(fn)
    def __(self, *args, **kwargs):
        if self.id != args[0]:
            return
        return fn(self, *args, **kwargs)

    return __


def needInTeam(fn):
    @functools.wraps(fn)
    def __(self, *args, **kwargs):
        if not hasattr(self, 'teamId'):
            ERROR_MSG('AttributeError, no teamId in instance.')
            return

        if self.teamId:
            return fn(self, *args, **kwargs)
        else:
            WARNING_MSG('Called fn must in a team: {}'.format(fn))
            return

    return __


def checkBagLocked(fn):
    @functools.wraps(fn)
    def __(bag, *args, **kwargs):
        if bag.isLocked():
            ERROR_MSG('bag is locked:', fn.__name__, bag.lockedTime, bag.lockDesc)
            return
        else:
            return fn(bag, *args, **kwargs)

    return __


def getRaycastPos(spaceId, srcPosition, dstPosition, includeFollowEdge=False):
    posList = KBEngine.raycast(spaceId, gameconst.SpaceLayer.DEFAULT, srcPosition, dstPosition)
    if not posList:
        return dstPosition

    for pos in posList:
        if sMath.postion3DTo2DCell(pos) == sMath.postion3DTo2DCell(dstPosition):
            realDstPos = dstPosition
            break
    else:
        realDstPos = sMath.getNearestPoint(dstPosition, posList)
        if sMath.postion3DTo2DCell(realDstPos) == sMath.postion3DTo2DCell(dstPosition):
            realDstPos = dstPosition

    return realDstPos

def getSurfacePos(spaceId, srcPosition, x=10, y=20, z=10):
    posList = KBEngine.getSurface(spaceId, gameconst.SpaceLayer.DEFAULT, srcPosition, x, y, z)
    if not posList:
        WARNING_MSG('getSurfacePos not find surface', spaceId, srcPosition, x, y, z)
        return srcPosition
    if posList[0][1] == 0:
        WARNING_MSG('getSurfacePos y is zero', spaceId, srcPosition, x, y, z)
        return srcPosition
    return posList[0]

def getNaviDistance(owner, dstPosition, includeBorder=True):
    m_posList = owner.navigatePathPoints(dstPosition, 100, gameconst.SpaceLayer.DEFAULT, includeBorder)
    if not m_posList:
        return float('inf')

    m_dis = 0
    m_seedPos = owner.position
    for i_pos in m_posList:
        m_dis += sMath.distance2D(m_seedPos, i_pos)
        m_seedPos = i_pos

    return m_dis


def getMinNaviDistance(owner, dstPositionList, includeBorder=True):
    assert dstPositionList
    minIdx, minDis = None, float('inf')
    for idx, dstPosition in enumerate(dstPositionList):
        if not dstPosition:
            continue
        _dis = getNaviDistance(owner, dstPosition, includeBorder=includeBorder)
        if minIdx is None or _dis < minDis:
            minIdx, minDis = idx, _dis

    return minIdx, minDis


def getMinDirectDistance(position, dstPositionList):
    assert dstPositionList
    minIdx, minDis = None, float('inf')
    for idx, dstPosition in enumerate(dstPositionList):
        _dis = sMath.distance2DToCompareFrom3DPosition(position, dstPosition)
        if minIdx is None or _dis < minDis:
            minIdx, minDis = idx, _dis

    return minIdx


def getRandomGoodPosition(ownerPosition, targetPosition, skillRange):
    randomDistance = random.random() * skillRange
    randomYaw = random.random() * math.pi - math.pi / 2  # -pi/2~pi/2
    target2selfYaw = sMath.getYawFromPoints(ownerPosition, targetPosition)
    dstYaw = target2selfYaw + randomYaw

    dir = sMath.getDirFromYaw(dstYaw)

    dstPos = sMath.posByOffset(targetPosition, dir * randomDistance)
    return dstPos


def isDunFlowModuleDataExist(dungeonNo: int):
    return _isDunXModuleDataExist(dungeonNo, 'e')


def _isDunXModuleDataExist(dungeonNo: int, suffix: str = ''):
    if not dungeonNo or dungeonNo < 0:
        raise TypeError('dungeonNo must be value higher than zero, got {}'.format(dungeonNo))

    try:
        __import__(_getDunXModuleName(dungeonNo, suffix)).datas
        return True
    except (ImportError, AttributeError) as err:
        return False


def getDunModuleData(dungeonNo: int):
    """get module datas in dun_xxx"""
    return _getDunXModuleData(dungeonNo)


def getDunFLowModuleData(dungeonNo: int):
    """get module datas in dun_xxx_e"""
    return _getDunXModuleData(dungeonNo, 'e')

def isDunGroupModuleDataExist(dungeonNo: int):
    return _isDunXModuleDataExist(dungeonNo, 'g')

def getDunGroupModuleData(dungeonNo: int):
    """get module datas in dun_xxx_g"""
    return _getDunXModuleData(dungeonNo, 'g')


def getDunStructureModuleData(dungeonNo: int, actId: int = 0):
    """get module datas in dun_xxx_s"""
    if actId:
        key = 'Act%s' % actId
    else:
        key = 'SpaceConfig'

    datas = _getDunXModuleData(dungeonNo, 's', False)
    return datas[key]


getGamePlayModuleData = getDunModuleData
getGamePlayFlowModuleData = getDunFLowModuleData
getGamePlayStructureModuleData = getDunStructureModuleData


def _getDunXModuleData(dungeonNo: int, suffix: str = '', showErrMsg=True):
    if not dungeonNo or dungeonNo < 0:
        raise TypeError('dungeonNo must be value higher than zero, got {}'.format(dungeonNo))

    try:
        return __import__(_getDunXModuleName(dungeonNo, suffix)).datas
    except (ImportError, AttributeError) as err:
        showErrMsg and ERROR_MSG('_getDunXModuleData::', dungeonNo, suffix, err)
        return {}


def getDunModuleName(dungeonNo: int):
    return _getDunXModuleName(dungeonNo)


def getDunFlowModuleName(dungeonNo: int):
    return _getDunXModuleName(dungeonNo, 'e')


def getDunStructureModuleName(dungeonNo: int):
    return _getDunXModuleName(dungeonNo, 's')


def _getDunXModuleName(dungeonNo: int, suffix: str = ''):
    module_template = 'dun_{{}}_{}'.format(suffix) if suffix else 'dun_{}'

    # if formula.spaceInWorldLine(dungeonNo):
    #     module_name = module_template.format('bigWorld')
    # else:
    module_name = module_template.format(dungeonNo)

    return module_name


def getEntitiesByIds(entIdList):
    ents = []
    for eid in entIdList:
        e = KBEngine.entities.get(eid)
        if e and not e.isDestroyed:
            ents.append(e)
    return ents


def getBuffEffectKey(effectId, effectIndex):
    return effectId * 100 + effectIndex


def mustInSpecialSpace(type_):
    def _wrapper(fn):
        @functools.wraps(fn)
        def __wrapper(self, *args, **kwargs):
            if formula.whatSpaceType(self.spaceNo) != type_:
                ERROR_MSG('must call this function in special type', type_)
                return
            return fn(self, *args, **kwargs)

        return __wrapper

    return _wrapper


_severFormulaComplie = re.compile(r'formula:\s*(\d{8})')


def _getFuncByFormula(formulaStr, *args):
    """根据公式计算结构

    Arguments:
        formulaStr {str} -- 公式ID, 传入格式 "formula:[formulaId, 8]', e.g. formula:12345678
        default {python} -- 默认值, 传入后如果没有取值则返回默认值, 否则抛出异常

    Raises:
        TypeError: 没有在配表里找到对应的公式

    Returns:
        obj -- 公式计算结果
    """
    raiseExc = True
    if len(args) > 0:
        default = args[0]
        raiseExc = False

    try:
        idStr = _severFormulaComplie.search(formulaStr)
        return FGFD.datas[int(idStr.group(1))]['serverFormula']
    except Exception as e:
        if not raiseExc:
            WARNING_MSG(
                f"_getFuncByFormula::use default value, formula={formulaStr}, default={args[0]}, exc={type(e).__name__}: {e}")
            return default
        raise e


def getValByFormula(formulaStr, param, *default):
    fn = _getFuncByFormula(formulaStr, *default)
    if not callable(fn):
        WARNING_MSG("getValByFormula:: value not callable", formulaStr, fn, default)
        return fn

    return fn(param)


def calcFormulaValue(formulaStr, params, *default):
    fn = _getFuncByFormula(formulaStr, *default)
    if not callable(fn):
        WARNING_MSG("calcFormulaValue:: value not callable", formulaStr, fn, default)
        return fn

    return fn(*params)


def randomByWeight(weight_list):
    sumWeight = sum(weight_list)
    randomWeight = random.uniform(0, sumWeight)
    flagVal = 0
    for idx, weight in enumerate(weight_list):
        flagVal += weight
        if randomWeight < flagVal:
            return idx
    return None


def man_gm_cmds():
    max_name_len = max_desc_len = 0

    def __yield():
        nonlocal max_desc_len, max_name_len

        for cmd in gameglobal.GM_CMDS.values():
            name = cmd.name
            if "_" in name:
                continue
            desc = cmd.desc
            args = ((i.__class__.__name__, i.desc) for i in cmd.args)

            len_name = len(name)
            len_desc = len(desc)
            max_name_len = len_name if len_name > max_name_len else max_name_len
            max_desc_len = len_desc if len_desc > max_desc_len else max_desc_len

            yield name, desc, args

    data = [_ for _ in __yield()]
    # tmp = '{{:{}}} | {{:{}}} | {{}}'.format(max_name_len, max_desc_len * 2)
    result = []
    for i in data:
        args = i[2]
        _args = ['{}({})'.format(i[1], i[0]) for i in args]
        # print(tmp.format(i[0], i[1], _args))
        tmp = {"name": i[0], "desc": i[1], "args": _args}

        result.append(tmp)
    return result


def getRealAvatarEnt(ent, height=2):
    orgEnt = ent
    for _ in range(height):
        if not ent:
            return None, True

        if ent.IsAvatar:
            return ent, False

        if ent.IsAvatarMirror and (ent.isNoOnwerMirror() or ent.isBot()):
            return ent, True

        if not hasattr(ent, 'hostId'):
            return None, True

        ent = ent.getHost()
    else:
        ERROR_MSG('getRealAvatarEnt:: ent not found', orgEnt, height)
        return None, True


def bytes2hex(bVal):
    bVal = ''.join(['%02x' % b for b in bVal])
    return '0x' + bVal


def getMyDeleteGlobalsMails(lastGBMailTime):
    DEBUG_MSG('in getMyDeleteGlobalsMails, lastGBMailTime:', lastGBMailTime)
    delGBMailList = []
    for (gbMailGBID, delTime) in reversed(gameglobal.globalDeleteMailsCacheList):
        if lastGBMailTime >= delTime:
            break
        delGBMailList.append((gbMailGBID, delTime))
    return delGBMailList


mask1 = 0x00550055
d1 = 5
mask2 = 0x0000cccc
d2 = 10

d3 = 3
d4 = 6


def encodeGuildShuffle(x):
    t = (x ^ (x >> d3)) & mask1;
    u = x ^ t ^ (t << d3);
    t = (u ^ (u >> d4)) & mask2;
    y = u ^ t ^ (t << d4);
    return y


def decodeGuildShuffle(y):
    t = (y ^ (y >> d4)) & mask2;
    u = y ^ t ^ (t << d4);
    t = (u ^ (u >> d3)) & mask1;
    z = u ^ t ^ (t << d3);
    return z


def encodeShuffle(x):
    t = (x ^ (x >> d1)) & mask1;
    u = x ^ t ^ (t << d1);
    t = (u ^ (u >> d2)) & mask2;
    y = u ^ t ^ (t << d2);
    return y


def decodeShuffle(y):
    t = (y ^ (y >> d2)) & mask2;
    u = y ^ t ^ (t << d2);
    t = (u ^ (u >> d1)) & mask1;
    z = u ^ t ^ (t << d1);
    return z


def encodeParity(x):
    t = (x ^ (x >> 1)) & 0x44444444
    u = (x ^ (x << 2)) & 0xcccccccc
    y = ((x & 0x88888888) >> 3) | (t >> 1) | u
    return y


def decodeParity(y):
    t = ((y & 0x11111111) << 3) | (((y & 0x11111111) << 2) ^ ((y & 0x22222222) << 1));
    z = t | ((t >> 2) ^ ((y >> 2) & 0x33333333));
    return z


OB_ADD_NUM = 10000000


# 最大不能超4194304

def obfuscateGuild(dbid):
    return encodeParity(encodeGuildShuffle(dbid)) + OB_ADD_NUM


def restoreGuild(dbid):
    return decodeGuildShuffle(decodeParity(dbid - OB_ADD_NUM))


def obfuscateDBID(dbid):
    return encodeParity(encodeShuffle(dbid))


def restoreDBID(dbid):
    return decodeShuffle(decodeParity(dbid))


def transferDBID(dbid):
    import gameconfig

    return int(str(gameconfig.serverId()) + '%05d' % obfuscateDBID(dbid))


def reTransferDBID(obid):
    import gameconfig

    id = int(str(obid)[len(str(gameconfig.serverId())):])
    return restoreDBID(id)


def getAreaId(mapId, position, scaleSize=1):
    if not gameglobal.areaData or not position:
        return 0

    x = int(position[0])//scaleSize
    z = int(position[2])//scaleSize

    curAreaDataInfo = gameglobal.areaData.get(mapId)
    if not curAreaDataInfo:
        return 0

    height, areaData = curAreaDataInfo

    return areaData.get(z*height+x, 0)


def getSvrOpenDayFiveTS():
    import gameconfig
    svrOpenTime = gameconfig.serverOpenTime()
    timeArr = list(time.localtime(svrOpenTime))
    if 0 <= timeArr[3] < 5:
        offset = gameconst.ONE_DAY_SECONDS
    else:
        offset = 0
    timeArr[3] = 5
    timeArr[4] = 0
    timeArr[5] = 0
    return int(time.mktime(tuple(timeArr))) - offset


def getSvrOpenDays(now=None):
    svrOpenTime = getSvrOpenDayFiveTS()
    return math.ceil(((now or getNow()) - svrOpenTime) / gameconst.ONE_DAY_SECONDS)


def getIntervalDaysFromTime(tLastOffline):
    # 指定时间到今天凌晨5点的间隔天数
    if tLastOffline == 0:
        return 0
    return max((getTodayFiveSec() - tLastOffline) // (3600 * 24), 0)


def getHostEntity(entity):
    if not entity:
        return
    target = entity
    if entity.IsAvatarMirror or entity.IsCreation or entity.IsPet or entity.IsSummon:
        if entity.hostId:
            target = entity.getHost() or entity

    return target


def parseCrontabPattern(express):
    ct = crontab.CronTab(express)
    return [sorted(list(c.allowed)) for c in ct.matchers[:5]]


def getLastDayOfMonth(year, month):
    nextMonth = month + 1 if 0 < month < 12 else 1
    t = time.mktime((year, nextMonth, 1, 0, 0, 0, 0, 0, 0))

    tplSec = time.localtime(t - 3600 * 24)

    return tplSec[2]


def timeTupleIsAny(tp):
    if not any(tp):
        return True
    return False


allMinutes = range(60)
allHours = range(24)
allMonths = range(1, 13)
allWeekdays = range(7)


# tp: parseCrontabPattern return value
def nextByTimeTuple(tp, now=None):
    if len(tp) not in (5, 6):
        return sys.maxsize

    if timeTupleIsAny(tp):
        return 0

    now = now or getNow()
    nowDatetime = datetime.datetime.fromtimestamp(now)
    tplSec = nowDatetime.timetuple()
    curYear, curMonth, curDay, curHour, curMin, curSec, curWeekDay = tplSec[0:7]
    years = []
    if len(tp) == 5:
        minutes, hours, days, months, weekdays = tp
    else:
        minutes, hours, days, months, weekdays, years = tp

    if days and weekdays:
        return sys.maxsize

    minutes = minutes or allMinutes
    hours = hours or allHours
    months = months or allMonths
    weekdays = weekdays or allWeekdays
    # years = years or allYears

    if not years or curYear in years:
        for month in months:
            if month < curMonth:
                continue

            allDays = range(1, getLastDayOfMonth(curYear, month) + 1)
            mDays = days or allDays
            if mDays[-1] > allDays[-1]:
                return sys.maxsize

            for day in mDays:
                if month == curMonth and day < curDay:
                    continue

                dt = datetime.datetime(curYear, month, day)
                if dt.isoweekday() % 7 not in weekdays:
                    continue

                for hour in hours:
                    if month == curMonth and day == curDay and hour < curHour:
                        continue
                    for minute in minutes:
                        dt = datetime.datetime(curYear, month, day, hour, minute)
                        if dt > nowDatetime:
                            return (dt - nowDatetime).total_seconds()

    years = years or range(curYear + 1, curYear + 10)
    for year in years:
        if year <= curYear:
            continue

        for month in months:
            allDays = range(1, getLastDayOfMonth(curYear, month) + 1)
            mDays = days or allDays
            for day in mDays:
                dt = datetime.datetime(curYear + 1, month, day)
                if dt.isoweekday() % 7 not in weekdays:
                    continue

                dt = datetime.datetime(year, month, day, hours[0], minutes[0])
                return (dt - nowDatetime).total_seconds()

    return sys.maxsize


def previousByTimeTuple(tp, now=None):
    if len(tp) not in (5, 6):
        return sys.maxsize

    if timeTupleIsAny(tp):
        return 0

    now = now or getNow()
    nowDatetime = datetime.datetime.fromtimestamp(now)
    tplSec = nowDatetime.timetuple()
    curYear, curMonth, curDay, curHour, curMin, curSec, curWeekDay = tplSec[0:7]
    years = []
    if len(tp) == 5:
        minutes, hours, days, months, weekdays = tp
    else:
        minutes, hours, days, months, weekdays, years = tp

    if days and weekdays:
        return sys.maxsize

    minutes = minutes or allMinutes
    hours = hours or allHours
    months = months or allMonths
    weekdays = weekdays or allWeekdays
    # years = years or allYears

    if not years or curYear in years:
        for month in reversed(months):
            if month > curMonth:
                continue

            allDays = range(1, getLastDayOfMonth(curYear, month) + 1)
            mDays = days or allDays
            if mDays[-1] > allDays[-1]:
                return sys.maxsize

            for day in reversed(mDays):
                if month == curMonth and day > curDay:
                    continue

                dt = datetime.datetime(curYear, month, day)
                if dt.isoweekday() % 7 not in weekdays:
                    continue

                for hour in reversed(hours):
                    if month == curMonth and day == curDay and hour > curHour:
                        continue
                    for minute in reversed(minutes):
                        dt = datetime.datetime(curYear, month, day, hour, minute)
                        if dt <= nowDatetime:
                            return (nowDatetime - dt).total_seconds()

    years = years or range(curYear - 10, curYear)
    for year in reversed(years):
        if year >= curYear:
            continue
        for month in reversed(months):
            allDays = range(1, getLastDayOfMonth(curYear, month) + 1)
            mDays = days or allDays
            for day in reversed(mDays):
                dt = datetime.datetime(year, month, day)
                if dt.isoweekday() % 7 not in weekdays:
                    continue

                dt = datetime.datetime(year, month, day, hours[-1], minutes[-1])
                return (nowDatetime - dt).total_seconds()

    return sys.maxsize


def nextByTimeTupleList(tps, now=None):
    nextStart = -1
    cronTuple = None
    for i, tp in enumerate(tps):
        tNext = nextByTimeTuple(tp, now)
        if nextStart < 0 or tNext < nextStart:
            nextStart = tNext
            cronTuple = tp

    return nextStart, cronTuple


# start: parseCrontabPattern return value
# end: parseCrontabPattern return value
_TFLAG_SRT = 1
_TFLAG_END = 2


def _inTimeTupleRange(srt, end, now):
    tNextSrt = nextByTimeTuple(srt, now)
    tNextEnd = nextByTimeTuple(end, now)
    tPrevSrt = previousByTimeTuple(srt, now)
    tPrevEnd = previousByTimeTuple(end, now)
    timeline = sorted(((now - tPrevSrt if tPrevSrt < sys.maxsize else math.inf, _TFLAG_SRT),
                       (now - tPrevEnd if tPrevEnd < sys.maxsize else math.inf, _TFLAG_END),
                       (now + tNextSrt if tNextSrt < sys.maxsize else math.inf, _TFLAG_SRT),
                       (now + tNextEnd if tNextEnd < sys.maxsize else math.inf, _TFLAG_END)),
                      key=lambda x: x[0])
    # | TIMELINE: -------- a --- b --- c --- d -----
    # | NOW:      ----------- x --------------------
    # L&R Closed Interval
    DEBUG_MSG("_inTimeTupleRange::", srt, end, now, timeline)
    if now > timeline[-1][0]:
        return timeline[-1][1] == _TFLAG_SRT

    for i in reversed(range(len(timeline) - 1)):
        if timeline[i][0] <= now:
            if timeline[i][1] == _TFLAG_SRT:
                return True
            if timeline[i][1] == _TFLAG_END:
                return False
            return False

    if now < timeline[0][0]:
        return timeline[0][1] == _TFLAG_END

    return False


def inTimeTupleRange(srt, end, now=None):
    now = now if now is not None else getNow()
    DEBUG_MSG("inTimeTupleRange::START", srt, end, now)
    r = _inTimeTupleRange(srt, end, now)
    DEBUG_MSG("inTimeTupleRange::ENDED", r, srt, end, now)
    return r


# starts: list of parseCrontabPattern return value
# ends: list of parseCrontabPattern return value
def inTimeTuplesRange(starts, ends, now=None):
    if not starts or not ends or len(starts) != len(ends):
        return False

    for idx, startCron in enumerate(starts):
        endCron = ends[idx]
        if inTimeTupleRange(startCron, endCron, now):
            return True

    return False


def inCrontabRange(start, end, now=None):
    now = now or getNow()
    startCT = crontab.CronTab(start)
    endCT = crontab.CronTab(end)

    sNext = startCT.next(now)
    eNext = endCT.next(now)
    if not eNext:
        return False

    if not sNext:
        return True

    if sNext < eNext:
        return False

    return True


def inCrontabsRange(starts, ends, now=None):
    now = now or getNow()
    nextStartTime = min([crontab.CronTab(s).next(now) for s in starts])
    nextEndTime = min([crontab.CronTab(s).next(now) for s in ends])

    if nextStartTime < nextEndTime:
        return False
    return True


MINUTE = 0
HOUR = 1
DAY = 2
MONTH = 3
WEEKEND = 4
YEAR = 5

TRANS_TAB = {
    MINUTE: 4,
    HOUR: 3,
    DAY: 2,
    MONTH: 1,
    WEEKEND: 6,
    YEAR: 0,
}


# matchList: parseCrontabPattern返回的格式
def checkCrontabs(current, matchList):
    timeWrap = time.localtime(current)

    if matchList is None:
        return False

    match = True
    for index, matchedList in enumerate(matchList):

        if len(matchedList) == 0:
            continue
        if index == 4:
            result = timeWrap[TRANS_TAB[index]] + 1 % 7
        else:
            result = timeWrap[TRANS_TAB[index]]

        if result not in matchedList:
            match = False
            break

    return match


def getTodayFiveSec():
    todayFive = getTodayZeroSec() + 18000
    if getNow() < todayFive:
        return todayFive - 24 * 3600
    else:
        return todayFive


def getIntervalDaysFromTime(tLastOffline):
    # 指定时间到今天凌晨5点的间隔天数
    if tLastOffline == 0:
        return 0
    return max((getTodayFiveSec() - tLastOffline) // (3600 * 24), 0)


def getRemainTimeStr(timestamp):
    hours = timestamp // gameconst.ONE_HOUR_SECONDES
    mins = timestamp % gameconst.ONE_HOUR_SECONDES // 60
    seconds = timestamp % 60
    if hours:
        return '{}小时{}分{}秒'.format(hours, mins, seconds)

    if mins:
        return '{}分{}秒'.format(mins, seconds)

    return '{}秒'.format(seconds)


def immutableMeta(name, bases, dct):
    class MetaCls(type):
        def __init__(cls, name, bases, dct):
            type.__init__(cls, name, bases, dct)

        def __setattr__(cls, attr, value):
            raise AttributeError("Cannot assign attributes to this class")

        def __getattr__(cls, name):
            try:
                return cls.__dict__[name]
            except:
                WARNING_MSG('%s is not defined, return 0 instead.' % name)
                return 0

    return MetaCls(name, bases, dct)


def isBeyondOneDay(timestamp):
    return timestamp + gameconst.ONE_DAY_SECONDS < getNow()


def decodeClientData(dataBytes):
    try:
        data = json.loads(dataBytes.decode('utf-8'), encoding='utf-8')
    except:
        data = {}

    return data


def encodeClientData(clientData):
    try:
        dataBytes = json.dumps(clientData).encode('utf-8')
    except:
        dataBytes = ''

    return dataBytes


def getRealAccountName(accountType, accountName):
    import proto.centralLogin_pb2 as centralLogin
    if accountType == centralLogin.ACCOUNT_UNKNOW:
        return accountName
    return '%s:%s' % (accountType, accountName)


def getAccountTypeAndName(accountName):
    import proto.centralLogin_pb2 as centralLogin
    parts = accountName.split(':')
    if len(parts) > 1:
        return int(parts[0]), parts[1]
    return centralLogin.ACCOUNT_UNKNOW, parts[0]


def checkAvatarNameLength(name):
    if not LC_LCD.datas['playerNameMinLength']['value'] <= len(name) <= LC_LCD.datas['playerNameMaxLength']['value']:
        return False
    return True


def checkAvatarName(name):
    if not gameconst.RE_VALIDATE_AVATAR_NAME_COMPILE.fullmatch(name):
        return False
    return True


def getPlayerMaxLevel():
    return CCT.datas['maxLevel']['value']


def getPlayerBornInfo():
    posList = CCT.datas['createConst_BornPos']['value']
    pos = random.choice(posList)
    return pos[0], pos[1]

def getPlayerBornMapId():
    return CCT.datas['createConst_BornGamePlayID']['value']

def getPlayerBreakAwayStuckPos(spaceNo, position):
    mapId = formula.getMapId(spaceNo)
    data = GPGP.datas.get(mapId, {})
    posList = data.get('breakAwayStuckPos', [])
    if posList:
        _telList = []
        for pos in posList:
            _telList.append(pos)

        _telList.sort(key=lambda x: sMath.distance2DToCompareFrom3DPosition(position, x))
        return _telList[0]
    return None


def getGeneratorEntItems(spaceNo, keyName, entName="", actId=0, dictLayer=3):
    entItems = {}
    datas = getDunStructureModuleData(formula.getMapId(spaceNo), actId)
    for k, v in datas[keyName].items():
        if not entName or v.get('ClassName', "") == entName:
            if dictLayer == 3:
                for eId, eItem in v.items():
                    entItems[eItem["ID"]] = eItem
            else:
                entItems[v["ID"]] = v
    return entItems


def getCrtMapCanEnterDungeonFlag(mapId):
    """是否可以进入副本"""
    return GPGP.datas.get(mapId, {}).get(
        'ifEnterDun', gameconst.GamePlayMapCheckEnum.DENY)


# --------------------------------------------------------------------------
# todo, 编写自定义比较规则,调用时读取策划所配置的相关属性进行按规则排序
def specialCmpToKey(reverseRule=None):
    def specialSortCmp(x, y, reverseRule=reverseRule):
        """
        根据 specialSortCmp 自定义的排序规则
        :param x:
        :param y:
        :param reverseRule: 用来排序的key:reverse (1:升序 -1:倒序 0:默认)读取策划所配置
        :return: x > y: 1, x < y: -1, x == y: 0

        """
        for (attr, rule) in reverseRule:
            if getattr(x, attr, 0) == getattr(y, attr, 0):
                continue
            elif getattr(x, attr, 0) > getattr(y, attr, 0):
                return rule
            else:
                return -rule
        return rule

    return specialSortCmp


def isNeedUpdateTopList(primaryKeyValue, curValue, ts, valueRule, tsRule, tailValue, tailTs, topListDt):
    # 已经在队列中
    if primaryKeyValue in topListDt:
        return True
    else:
        # 非序列tail成员
        # 降序
        if valueRule == -1:
            if curValue > tailValue:
                return True
            elif curValue == tailValue:
                # 降序
                if tsRule == -1:
                    if ts > tailTs:
                        return True
                # 升序
                elif tsRule == 1:
                    if ts < tailTs:
                        return True
        # 升序
        elif valueRule == 1:
            if curValue < tailValue:
                return True
            elif curValue == tailValue:
                # 降序
                if tsRule == -1:
                    if ts > tailTs:
                        return True
                # 升序
                elif tsRule == 1:
                    if ts < tailTs:
                        return True
        return False

def canIterable(val):
    return hasattr(val, '__iter__') or hasattr(val, '__getitem__')


def parseCommEventParams(paramStr):
    parsmsList = paramStr.split(';')
    args = parsmsList[0].split(',') if parsmsList[0] else []
    kwargs = {}
    if len(parsmsList) == 2:
        kwargs = json.loads(parsmsList[1])
    return args, kwargs


def deduplicateList(m):
    return functools.reduce(lambda x, y: x if y in x else x + [y], [[], ] + m)


def isBoxOffline(box):
    # 先删除isDestroying判断，正常情况应该在下线销毁时就从stub注销自己，而不是持有一个isDestroyed的对象再判断
    if isinstance(box, KBEngine.Proxy):
        if box.isDestroyed:
            gameengine.reportCritical('use of destroyed box')
        return box.isDestroyed

    return box is None


def getSpaceNameBySpaceNo(spaceNo, default=""):
    return GPGP.datas.get(formula.getDungeonNoBySpaceNo(spaceNo), {}).get("name", default)


def getRecordLogData(owner, dataKey, default=None):
    return owner.getPersistentMiscProp(gameconst.AvatarProps.RecordLogData, {}).get(dataKey, default)


def setRecordLogData(owner, dataKey, dataVal):
    logDataDic = owner.getPersistentMiscProp(gameconst.AvatarProps.RecordLogData)
    if not logDataDic:
        logDataDic = {}
        owner.setPersistentMiscProp(gameconst.AvatarProps.RecordLogData, logDataDic)
    logDataDic[dataKey] = dataVal
    return


def getTimeStr(now):
    tTime = time.localtime(now)
    return ' {}年{}月{}日 {:0>2d}:{:0>2d} '.format(tTime.tm_year, tTime.tm_mon, tTime.tm_mday, tTime.tm_hour,
                                                   tTime.tm_min)


def setCallbackTmpInfo(owner, opUUID, callbackData):
    callbackInfoDic = owner.getTempMiscProp(gameconst.AvatarProps.callbackTmpInfo)
    if not callbackInfoDic:
        callbackInfoDic = {}
    callbackInfoDic[opUUID] = callbackData
    owner.setTempMiscProp(gameconst.AvatarProps.callbackTmpInfo, callbackInfoDic)
    return


def getCallbackTmpInfo(owner, opUUID, default=None):
    return owner.getTempMiscProp(gameconst.AvatarProps.callbackTmpInfo, {}).get(opUUID, default)


def popCallbackTmpInfo(owner, opUUID):
    callbackInfoDic = owner.getTempMiscProp(gameconst.AvatarProps.callbackTmpInfo)
    if not callbackInfoDic:
        return None
    return callbackInfoDic.pop(opUUID, None)


def getSpaceEnterScene(crtSpaceType, enterSpaceType, default=gameconst.SpaceEnterScene.DENY):
    return GPES.datas.get(crtSpaceType, {}).get(str(enterSpaceType), default)


def getMonsterAttrKey(attrId):
    return 'attr_{}'.format(attrId)


# key不能为-1
def getRankBySortedList(sortList, keyFunc):
    rank = 0
    curRank = 0
    lastVal = -1
    for i in sortList:
        rank += 1
        val = keyFunc(i)
        if val != lastVal:
            lastVal = val
            curRank = rank

        yield curRank


def getLineMaxNumber(lineType):
    return gameconst.lineStubMap.get(lineType, {}).get('lineCount', 0)


def isInWorldLinePKSafeAreaByAreaId(areaId):
    import worldConfig_Area

    if not areaId:
        return False
    areaConf = worldConfig_Area.datas.get(areaId, None)
    if not areaConf:
        return False

    if not areaConf['ifSafeArea']:
        return False

    return True

def addResourceVal(oldVal, delta, valType):
    newVal = oldVal + delta
    if valType == gameconst.ReourceValType.UINT32:
        maxVal = 0xFFFFFFFF
    elif valType == gameconst.ReourceValType.INT32:
        maxVal = 0x7FFFFFFF
    elif valType == gameconst.ReourceValType.UINT64:
        maxVal = 0xFFFFFFFFFFFFFFFF
    elif valType == gameconst.ReourceValType.INT64:
        maxVal = 0x7FFFFFFFFFFFFFFF
    elif valType == gameconst.ReourceValType.UINT8:
        maxVal = 0xFF
    else:
        return newVal

    if newVal < 0:
        if valType in (
                gameconst.ReourceValType.UINT32, gameconst.ReourceValType.UINT64, gameconst.ReourceValType.UINT8,):
            gameengine.reportCritical('checkResourceValLimit, minus source val:', newVal, valType)
            newVal = 0
    elif newVal > maxVal:
        gameengine.reportCritical('checkResourceValLimit, exceed max val:', newVal, valType, maxVal)
        newVal = maxVal
    return newVal


def getFraction(val, len=100):
    return int(round(val - int(val), 2) * len)


def addFraction(val, addVal, maxValue=gameconst.UINT8_MAX):
    if val + addVal > maxValue:
        return (val + addVal) - maxValue - 1, 1
    else:
        return val + addVal, 0


def getPlantGid(plantType, slot):
    return plantType * 1000 + slot


def getAccountTypeByPlatId(platId):
    import proto.centralLogin_pb2 as centralLogin

    if platId == gameconst.TssAccountPlatId.TSSPLAT_ID_IOS:
        accountType = centralLogin.ACCOUNT_MSDK_IOS
    elif platId == gameconst.TssAccountPlatId.TSSPLAT_ID_ANDROID:
        accountType = centralLogin.ACCOUNT_MSDK_ANDROID
    elif platId == gameconst.TssAccountPlatId.TSSPLAT_ID_UNKNOWN:
        accountType = centralLogin.ACCOUNT_UNKNOW
    else:
        accountType = centralLogin.ACCOUNT_PASSWD

    return accountType


def getPlatIdByAccountType(accountType):
    import proto.centralLogin_pb2 as centralLogin

    if accountType == centralLogin.ACCOUNT_MSDK_IOS:
        return gameconst.TssAccountPlatId.TSSPLAT_ID_IOS
    elif accountType == centralLogin.ACCOUNT_MSDK_ANDROID:
        return gameconst.TssAccountPlatId.TSSPLAT_ID_ANDROID
    else:
        return gameconst.TssAccountPlatId.TSSPLAT_ID_UNKNOWN


def getGameAppId(channelId):
    return ""


@functools.lru_cache(maxsize=1)
def getShowCompleteModelNum():
    return PLSD.datas["showCompleteModelNum"].get("value")


@functools.lru_cache(maxsize=1)
def getShowNameNum():
    return PLSD.datas["showNameNum"].get("value")


@functools.lru_cache(maxsize=1)
def getShowCompletePetModelNum():
    return PLSD.datas["showCompletePetModelNum"].get("value")


def _testCheckAvatarName():
    _tests = [('asdASD', True),  # 英文
              ('你好', True),  # 中文
              ('あ', True),  # 平假名
              ('ウ', True),  # 片假名
              ('0123456789', True),  # 数字
              ('你好0123HJzasHJd9Sライオ1oOン', True),
              ('asd 你好', False),
              ('ちほり', True),
              ('asd-dkk', False),
              ('你好 世界', False),
              ('你好，世界', False),
              ('你好　世界', False)]

    for k, v in _tests:
        _r = checkAvatarName(k)
        assert _r is v


# _testCheckAvatarName()


def bitSet(val, bit):
    return val | (1 << bit)


def hasBit(val, bit):
    return val & (1 << bit)


def bitReset(val, bit):
    return val & (~(1 << bit))


def getWholeBits(*bits):
    val = 0
    for bit in bits:
        val = bitSet(val, bit)

    return val


def getBanEndTimeString(banTime):
    if banTime == -1:
        return LGS.datas['foreverText']['value']
    else:
        return time.strftime("%Y年%m月%d日%H时%M分%S秒", time.localtime(banTime))


def checkIDIPModifyName(name):
    if not checkAvatarNameLength(name):
        return False

    if not checkAvatarName(name):
        return False

    if name.isdigit():
        return False

    return True


def getTlogHeaderList(avatar):
    import serverList_serverList as SLSL
    import gameconfig
    roleInfo = gameglobal.roleCache[avatar.id]
    return [
        getGameAppId(avatar.accountEntity.channelId),
        avatar.accountEntity.devicePlatId,
        gameconfig.serverId(),
        avatar.accountName,
        avatar.gbID,
        roleInfo['name'],
        roleInfo['level'],
        0,  # vip level
        roleInfo['battlePoint'],
    ]


def getSecTlogHeaderList(avatar):
    roleInfo = gameglobal.roleCache[avatar.id]
    import serverList_serverList as SLSL
    import gameconfig
    return [
        getGameAppId(avatar.accountEntity.channelId),
        avatar.accountEntity.devicePlatId,
        avatar.accountEntity.channelId,
        gameconfig.serverId(),
        avatar.accountEntity.accountName,
        '',
        roleInfo.get('SecReportData', ''),
        avatar.getClientIp(),
        str(avatar.gbID),
        roleInfo['name'],
        roleInfo['school'],
        roleInfo['level'],
        roleInfo.get('battlePoint', 0),
        '',
        str(avatar.guildUUIDBase),
        avatar.guildNameBase,
    ]


def calcSpaceWeight(playerNum, withPet, otherEntNumPerPlayer, baseWeight=0):
    """
    :param playerNum: 本地图最大玩家数量
    :param withPet: 本地图是否能带宠物
    :param otherEntNumPerPlayer: 表示预估平均每个玩家在AOI内能看到的怪物数量；比如单人副本就是AOI内的所有怪物数量，组队本就是AOI内所有怪物数量除以组队人数（5）
    :param baseWeight: 地图创建就带的默认权重，用于大世界分线
    """
    spaceWeight = baseWeight + playerNum * (1 + otherEntNumPerPlayer)
    if withPet:
        spaceWeight += playerNum
    return int(spaceWeight)


def getServerLevel():
    serverLevelInfo = KBEngine.globalData.get(gameconst.GLOBALDATA_KEY_DAILY_SERVER_LEVEL_DATA)
    if not serverLevelInfo:
        gameengine.reportCritical('getServerLevel, no serverLevelInfo')
        return 1
    return serverLevelInfo[1]


######## AES begin ########
aes_pad = lambda s, bs: s + chr(bs - len(s) % bs) * (bs - len(s) % bs)
aes_unpad = lambda s: s[:-ord(s[len(s) - 1:])]


def encryptAES(data: str, key: str):
    cipher = AES.new(key.encode('utf-8'), AES.MODE_ECB)
    data = aes_pad(data, cipher.block_size)
    return base64.b64encode(cipher.encrypt(data.encode('utf-8'))).decode('utf-8')


def decryptAES(data: str, key: str):
    cipher = AES.new(key.encode('utf-8'), AES.MODE_ECB)
    data = base64.b64decode(data.encode('utf-8'))
    return aes_unpad(cipher.decrypt(data)).decode('utf-8')


def encryptAES_CBC(data: str, key: str, vi: str):
    cipher = AES.new(key.encode('utf-8'), AES.MODE_CBC, vi.encode('utf-8'))
    data = aes_pad(data, cipher.block_size)
    return base64.b64encode(cipher.encrypt(data.encode('utf-8'))).decode('utf-8')


def decryptAES_CBC(data: str, key: str, vi: str):
    cipher = AES.new(key.encode('utf-8'), AES.MODE_CBC, vi.encode('utf-8'))
    data = base64.b64decode(data.encode('utf-8'))
    return aes_unpad(cipher.decrypt(data)).decode('utf-8')


######## AES end ########

def getExposedMethods():
    methods = KBEngine.getExposedMethods('Avatar')
    uidMethodMap = KBEngine.getUidMethodMap('Avatar')
    methodUidMap = {v: k for k, v in uidMethodMap.items()}
    result = {}
    for m in methods:
        result[methodUidMap[m]] = m

    return result


def getCallStats():
    results = []
    for uid, methodName in gameglobal.avatarExposedMethods.items():
        num = KBEngine.getCallNum('Avatar', uid)
        if num:
            results.append((num, methodName))

    results.sort(reverse=True)
    return results


def _onGetAvatarInfos(ctx, ret, num, insertId, err):
    import redisUtils
    if type(err) is str and err:
        ERROR_MSG('_onGetAvatarInfos error:', err, ctx)
        return

    for gbId, dbId, obId in ret:
        gbId = int(gbId)
        dbId = int(dbId)
        obId = int(obId)

        redisUtils.RedisUtils.onRemoveAvatar(gbId, obId)


def miscCheckUserInput(msg, func):
    KBEngine.checkUserInput(
        1,
        'accountName',
        1,
        'roleName',
        1,
        gameconst.CheckUserInputContentType.CONTENT_CATEGORY_MATERIAL,
        msg,
        func,
        0,
        1,
        0,
        gameconfig.serverId(),
        ''
    )


def changeTextInJune():
    """
    每年六月有个时间段不能改名字
    :return:
    """
    _start = 1654257600  # 2022/6/3 20:00:00
    _end = 1654430400  # 2022/6/5 20:00:00
    return _start < getNow() < _end


def judgeHitWithProbabilityArr(valOrderArr, valMax, valMin=0):
    randomVal = random.randint(valMin, valMax)
    for i in range(len(valOrderArr)):
        if randomVal <= valOrderArr[i]:
            return i
    return -1


def cellGetLineStubIdx(spaceNo):
    spaceEnt = gameglobal.localSpaceNoMap.get(spaceNo)
    if not spaceEnt:
        ERROR_MSG('cannot get spaceNo:', spaceNo)
        return -1

    return spaceEnt.lineStubIdx


@functools.lru_cache(100)
def parseTimeStr(timeStr):
    return int(time.mktime(time.strptime(timeStr, '%Y%m%d%H%M%S')))


@functools.lru_cache(100)
def parseDayCycleTimeStr(timeStr):
    _ = timeStr.split(':')  # timeStr : '20:00:00'
    return int(_[0]) * gameconst.ONE_HOUR_SECONDES + int(_[1]) * gameconst.ONE_MINUTE_SECONDS + int(_[2])


def parseDayTimeStr(timeStr, now=None):
    tss = parseDayCycleTimeStr(timeStr)
    return getCurrentDayTS(now, tss)


chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
chars += chars.lower()
chars += '0123456789'


def getRandStr(length=10):
    ret = ''
    for i in range(length):
        ret += random.choice(chars)
    return ret


def isDuringTimeRange(startTime, endTime):
    tStart = parseTimeStr(startTime)
    tEnd = parseTimeStr(endTime)
    return tStart <= time.time() < tEnd


REWARD_SCORE_TS_BASE = 1669356500


def numberToBase(n, b):
    if n == 0:
        return [0]
    digits = []
    while n:
        digits.append(int(n % b))
        n //= b
    return digits[::-1]


def intToEncodedStr(n, chars=ASCII_LIST):
    arr = numberToBase(n, len(chars))
    arrBytes = [chars[x] for x in arr]
    return ''.join(arrBytes)


@functools.lru_cache(1000)
def getCharIndex(char, charListStr):
    charList = list(charListStr)
    if char in charList:
        return charList.index(char)
    return -1


def encodedStrToInt(codeStr, chars=ASCII_LIST):
    base = len(chars)
    gbId = 0
    for i, ch in enumerate(reversed(codeStr)):
        idx = getCharIndex(ch, ''.join(chars))
        if idx < 0:
            return 0
        gbId += (base ** i) * idx

    return gbId


# num 有小数位保留N为小数位
# 超过N位,不采用4舍5入
def keepFloat(num, n):
    numStr = str(num)
    numArr = numStr.split('.')
    if len(numArr) == 2:
        if len(numArr[1]) >= n:
            return float(numArr[0] + '.' + numArr[1][:n])
        else:
            return num
    else:
        return num


# ts = 20101010
def isAdult(birth):
    birthStr = str(birth)
    birthYear = int(birthStr[:4])
    birthMon = int(birthStr[4:6])
    birthDay = int(birthStr[6:8])

    now = getNow()
    nDate = time.localtime(now)

    DEBUG_MSG('isAdult', birthYear, birthMon, birthDay, nDate)
    if nDate.tm_year - birthYear > 18:
        return True
    elif nDate.tm_year - birthYear < 18:
        return False
    else:
        if nDate.tm_mon > birthMon:
            return True
        elif nDate.tm_mon < birthMon:
            return False
        else:
            return nDate.tm_mday >= birthDay


def countNumWithSum(arr, sum):
    _sum = 0
    for i, n in enumerate(arr):
        _sum += n
        if _sum >= sum:
            return i + 1
    return 0


def encodeEquityJson(uniqueId, serialNumber):
    extra = {
        'uniqueId': uniqueId,
        'serialNumber': serialNumber,
    }
    extraJsonStr = json.dumps(extra, separators=(',', ':')).encode('utf-8')
    extraJson = bytes.hex(extraJsonStr)
    DEBUG_MSG('encodeEquityJson--', extraJson)
    return extraJson


def emptyJsonStr():
    extraJsonStr = json.dumps('', separators=(',', ':')).encode('utf-8')
    extraJson = bytes.hex(extraJsonStr)
    return extraJson


def decodeHexJson(jsonStr):
    extraJosnStr = bytes.fromhex(jsonStr).decode('utf-8')
    extraJson = json.loads(extraJosnStr)
    return extraJson


def encodeHexJson(dataDict):
    extraJsonStr = json.dumps(dataDict, separators=(',', ':')).encode('utf-8')
    extraJson = bytes.hex(extraJsonStr)
    return extraJson


def isEnemyInBigWorldDuel(src, target, includeEnded=False):
    src, target = getEntityRealEntity(src), getEntityRealEntity(target)
    if src.IsAvatar and target.IsAvatar and \
            src.bigWorldDuelCacheInfo.duelUUID == target.bigWorldDuelCacheInfo.duelUUID:
        return _isEnemyInBigWorldDuel(src, target, includeEnded=includeEnded)
    return False


def _isEnemyInBigWorldDuel(src, target, includeEnded=False):
    if src.bigWorldDuelCacheInfo.isInFighting(includeEnded) and target.bigWorldDuelCacheInfo.isInFighting(includeEnded):
        if src.bigWorldDuelCacheInfo.duelSide != target.bigWorldDuelCacheInfo.duelSide:
            return True
    return False


def getGuildUUIDPair(guildUUID1, guildUUID2):
    if guildUUID1 < guildUUID2:
        return (guildUUID1, guildUUID2)
    else:
        return (guildUUID2, guildUUID1)


def isEnemyInPK(src, target):
    if target.gbId in src.challengeAvatars:
        return not (src.inPKSafeArea() or target.inPKSafeArea())

    if src.pkModel == gameconst.PKModel.PEACE:
        return False
        # if not (CCT.datas['greenCanAttackGrey']['value']):
        #     return False

    if src.inPKSafeArea() or target.inPKSafeArea():
        return False

    if src.inPKProtect(target):
        return False

    if src.pkModel == gameconst.PKModel.JUSTICE:
        return target.inRedName() or target.isGreyName()
    
    elif src.pkModel == gameconst.PKModel.ENEMY:
        if target.inRedName() or target.isGreyName():
            return True

        _relation = getGuildRelation(src.guildUUID, target.guildUUID)
        return _relation == gameconst.GuildRelationType.ENEMY

    return True


_isEnemyFuncDic = {}


def getEntityRealEntity(ent):
    if ent.IsAvatarMirror or ent.IsCreation or ent.IsPet or ent.IsSummon:
        if ent.hostId:
            ent = ent.getHost() or ent

    return ent


def isEnemy(src, target):
    if src.isDestroyed or target.isDestroyed:
        return False

    if src.id == target.id:
        return False

    # if (src.IsAvatar and src.isCrossServerInLocalServer) or (target.IsAvatar and target.isCrossServerInLocalServer):
    #     return False

    if src.IsAvatar and src.guildRelationVersion != gameglobal.guildRelationVersion:
        src.resetAllTargetTypeCache()

    if target.id in src.enemyCacheSet:
        return True

    elif target.id in src.notEnemyCacheSet:
        return False

    if not (src.isReal() and target.isReal()):
        return False

    bIsEnemy = _isEnemy(src, target)
    if bIsEnemy:
        src.enemyCacheSet.add(target.id)
    else:
        src.notEnemyCacheSet.add(target.id)

    target.cacheSelfSet.add(src.id)

    return bIsEnemy


# 参数顺序很重要，只有target是不可攻击的才不是enemy

def _isEnemy(src, target):
    if (not src.IsCombatUnit and not src.IsCreation) or not target.IsCombatUnit:
        return False

    src, target = getEntityRealEntity(src), getEntityRealEntity(target)
    if src.id == target.id:
        return False
    
    # 切磋状态下，只能攻击切磋对象
    if src.IsAvatar:
        if src.duelAttr.inFight():
            if not target.IsAvatar:
                return False

            return src.duelAttr.isDuelEnemy(target)
    
        elif src.duelAttr.inReady():
            return False
    
    if formula.isSiegeWarSpace(src.spaceNo):
        if formula.isSiegeWarSpace(target.spaceNo):
            if src.IsAvatar and target.IsAvatar:
                if not src.siegeWarCanAttack:
                    return False
            return src.siegeWarCamp != target.siegeWarCamp
    #
    # mapId = formula.getMapId(src.spaceNo)
    #
    # if mapId in _isEnemyFuncDic:
    #     retCode = _isEnemyFuncDic[mapId](src, target)
    #     if retCode == gameconst.IsRelationEnum.TRUE:
    #         return True
    #     elif retCode == gameconst.IsRelationEnum.FALSE:
    #         return False
    #
    # pk规则判断
    if src.IsAvatar and target.IsAvatar:
        # 【野外PK
        # A开戮斗模式攻击B，客户端可以放技能没有伤害，客户端判断能打，但是服务端判断不能打】

        if isEnemyInPK(src, target):
            return True

    # if src.IsMonster and src.belongGbId and target.IsAvatar:
    #     if src.belongGbId != target.gbId:
    #         return False
    # elif src.IsAvatar and target.IsMonster and target.belongGbId:
    #     if target.belongGbId != src.gbId:
    #         return False
    #
    # if src.IsAvatar and target.IsAICombatUnit and target.exclusiveGBID and target.exclusiveGBID != src.gbId:
    #     return False
    #
    # if target.IsAvatar and src.IsAICombatUnit and src.exclusiveGBID and src.exclusiveGBID != target.gbId:
    #     return False
    #
    if getForceRelation(src, target) == gameconst.ForceRelation.Enemy:
        return True

    return False


def isPVP(src, target):
    srcHost = getHostEntity(src)
    targetHost = getHostEntity(target)
    if srcHost and targetHost:
        if srcHost.IsAvatar or (srcHost.IsAvatarMirror and not srcHost.guildLeader):
            if targetHost.IsAvatar or (targetHost.IsAvatarMirror and not targetHost.guildLeader):
                return True

    return False


_isFriendFunDic = {}


def isFriend(src, target):
    if src.isDestroyed or target.isDestroyed:
        return False

    if src.id == target.id:
        return False

    if target.id in src.friendCacheSet:
        return True

    elif target.id in src.notFriendCacheSet:
        return False

    if not (src.isReal() and target.isReal()):
        return False

    bIsFriend = _isFriend(src, target)
    if bIsFriend:
        src.friendCacheSet.add(target.id)
    else:
        src.notFriendCacheSet.add(target.id)

    target.cacheSelfSet.add(src.id)

    return bIsFriend


def _isFriend(src, target):
    if src.id == target.id:
        return False

    src, target = getEntityRealEntity(src), getEntityRealEntity(target)
    if src.id == target.id:
        return True
    
    # 切磋状态下，不能影响任何人
    #     【【切磋】处于切磋中的人放的加血技能可以给非切磋目标加血】
    # https://www.tapd.cn/tapd_fe/59721401/bug/detail/1159721401001002975
    if src.IsAvatar and src.duelAttr.inFight():
        return False

    spaceType = formula.getMapId(src.spaceNo)

    if spaceType in _isFriendFunDic:
        ret = _isFriendFunDic[spaceType](src, target)
        if ret == gameconst.IsRelationEnum.TRUE:
            return True
        elif ret == gameconst.IsRelationEnum.FALSE:
            return False

    if src.IsAvatar and target.IsAvatar:
        # if isEnemyInPK(src, target):
        #     return False
        #
        # if src.isInRaid() and target.isInRaid() and src.raidInfo.raidUUID == target.raidInfo.raidUUID:
        #     # 双方在同一团队则不能攻击
        #     return True

        return not isEnemy(src, target)

    # if getForceRelation(src, target) == gameconst.ForceRelation.Friend:
    #     return True

    return False


def isFriendIncS(src, target):
    if src.id == target.id:
        return True

    return isFriend(src, target)


def getForceRelation(src, target):
    if not src or not target:
        return gameconst.ForceRelation.UnKnownForceRelation

    datas = creep_force.datas
    force = src.force

    if force not in datas:
        return gameconst.ForceRelation.UnKnownForceRelation

    subforceRelation = datas[force]

    targetForceType = gameconst.ForceType.getForceType(target.force)

    if targetForceType in subforceRelation:
        return subforceRelation[targetForceType]
    else:
        return gameconst.ForceRelation.UnKnownForceRelation


def getRaceType(entity):
    if entity.IsAvatar:
        return gameconst.RaceType.avatar

    elif entity.IsMonster:
        return gameconst.RaceType.monster

    elif entity.IsSummon:
        return gameconst.RaceType.summon

    elif entity.IsAvatarMirror:
        if entity.isBot():
            return gameconst.RaceType.bot
        else:
            return gameconst.RaceType.avatar

    else:
        return gameconst.RaceType.none


def entIsAll(src, e, *args):
    return e is not None


def entIsEnemy(src, e, *args):
    return isEnemy(src, e)


def entIsFriend(src, e, *args):
    return isFriend(src, e)


def entIsSelf(src, e, *args):
    return src.id == e.id


def entIsCreationMaster(src, e, *args):
    return src.IsCreation and src.hostId == e.id


def entIsEnemyExTarget(src, e, target):
    return e.id != target.id and isEnemy(src, e)


def entIsCacheEnemy(src, e, *args):
    return True


def entIsCacheFriend(src, e, *args):
    return True


def entIsCacheEnemyExTarget(src, e, target):
    return e.id != target.id


TARGET_FUNC_MAP = {gameconst.CampType.All: entIsAll,
                   gameconst.CampType.Enemy: entIsEnemy,
                   gameconst.CampType.Friend: entIsFriend,
                   gameconst.CampType.Self: entIsSelf,
                   gameconst.CampType.CreationMaster: entIsCreationMaster,
                   gameconst.CampType.EnemyExTarget: entIsEnemyExTarget}

CACHE_TARGET_FUNC_MAP = {gameconst.CampType.All: entIsAll,
                         gameconst.CampType.Enemy: entIsCacheEnemy,
                         gameconst.CampType.Friend: entIsCacheFriend,
                         gameconst.CampType.Self: entIsSelf,
                         gameconst.CampType.CreationMaster: entIsCreationMaster,
                         gameconst.CampType.EnemyExTarget: entIsCacheEnemyExTarget}


@functools.lru_cache(16)
def getFightTargetTypeCfgData(typeName):
    return FPFTTD.datas.get(typeName, {}).get('value')


# 可能涉及三方关系，所以可能需要三个entity参数，例如选择敌人周围的敌人
def checkTargetType(typeName, src, e, target=None):
    if typeName == 'Any' or typeName == 'None':
        return True

    if not target:
        target = e

    if not e.isAttackable(src):
        return False
    value = getFightTargetTypeCfgData(typeName)
    if not value or len(value) < 3:
        ERROR_MSG('checkTargetType err in fightProp_fightTargetType', typeName)
        return False

    for targetType in value[2]:
        if TARGET_FUNC_MAP[targetType](src, e, target):
            break
    else:
        return False

    if 1 in value[1] and not e.isDie():
        return False
    if 2 in value[1] and e.isDie():
        return False

    if 0 not in value[0] and getRaceType(e) not in value[0]:
        return False

    return True


# 可能涉及三方关系，所以可能需要三个entity参数，例如选择敌人周围的敌人
def checkCachedTargetType(typeName, src, e, target=None):
    if typeName == 'Any' or typeName == 'None':
        return True

    if not target:
        target = e

    if not e.isAttackable(src):
        return False

    value = getFightTargetTypeCfgData(typeName)
    if not value or len(value) < 3:
        ERROR_MSG('checkTargetType err in fightProp_fightTargetType', typeName)
        return False

    for targetType in value[2]:
        if CACHE_TARGET_FUNC_MAP[targetType](src, e, target):
            break
    else:
        return False

    if 1 in value[1] and not e.isDie():
        return False
    if 2 in value[1] and e.isDie():
        return False

    if 0 not in value[0] and getRaceType(e) not in value[0]:
        return False

    return True

@functools.lru_cache(1024, typed=False)
def hasSkillTag(skillId, tag):
    tags = combatSkill.SkillBase.getTag(skillId)
    if not tags:
        return False

    if tag in tags:
        return True
    return False

def initBaseProperties(entity, propCurveID=0):
    if not propCurveID:
        propCurveID = entity.getConfigData().get('propCurveID')

    if not propCurveID:
        raise RuntimeError('creep base entity must set propCurveID, {}'.format(entity.creepBaseId))

    # import monsterStandardProp_prop as MSPD
    import monsterStandardProp_propCurve as MSPCD
    import prop_fightprop as PFPD
    import creep_base as CBD

    creepData = CBD.datas.get(entity.creepBaseId)
    propId = creepData.get('propID')
    if propId:
        propType = creepData.get('propType')
        if propType == 1:
           propId = propId + entity.level - 1

        propData = PFPD.datas.get(propId)
        cfgPropType = propData.get('type')
        if propType != cfgPropType:
            ERROR_MSG('initBaseProperties propType error', entity.creepBaseId, propType, cfgPropType)
            return

        propList = propData.get('propList')
        for prop, val in propList.items():
            setattr(entity, prop, val)

    entity.baseSpeed = float(entity.getConfigData().get('baseSpeed', 0))
    entity.jobHealModify = entity.getConfigData().get('jobHealModify', 0.0)
    entity.jobAvoidanceModify = entity.getConfigData().get('jobAvoidanceModify', 0.0)
    entity.baseStateRate = entity.getConfigData().get('baseStateRate', 0.0)
    entity.shareMasterDmg = entity.getConfigData().get('shareMasterDmg', 0.0)

    entity.speedStateRatio = gameconst.SpeedState.Normal

def getSpaceEnterSceneBySpaceNo(crtSpaceNo, enterSpaceNo, default=gameconst.SpaceEnterScene.DENY):
    _crtSpaceType = GPGP.datas.get(
        formula.getDungeonNoBySpaceNo(crtSpaceNo), {}).get(
            'type', gameconst.SpaceType.UnKownSpaceType)
    _enterSpaceType = GPGP.datas.get(
        formula.getDungeonNoBySpaceNo(enterSpaceNo), {}).get(
            'type', gameconst.SpaceType.UnKownSpaceType)
    return getSpaceEnterScene(_crtSpaceType, _enterSpaceType, default)


def isComplexTeleportAllowed(fromSpaceNo, toSpaceNo):
    r = getSpaceEnterSceneBySpaceNo(fromSpaceNo, toSpaceNo)
    if r == gameconst.SpaceEnterScene.DENY:
        return False
    return True


def getTeleporterByID(teleportId, spaceNo, default=None):
    telIds = gameglobal.teleporterGIDToEntIdMap.get(spaceNo, {}).get(
        teleportId, None)
    if telIds is not None:
        return KBEngine.entities.get(telIds[0], default)
    return default


def isComplexTeleportNeedCast(fromSpaceNo, toSpaceNo, teleportType, src, owner):
    if owner.isDie():
        return False

    if fromSpaceNo == toSpaceNo:
        return False

    if src and src.srcId == gameconst.DungeonSrcEnum.FROM_FOLLOW_CAPTAIN:
        return src.needCast

    if teleportType == gameconst.ComplexTeleportType.LEAVE and formula.isDungeonSpace(fromSpaceNo):
        return False

    r = getSpaceEnterSceneBySpaceNo(fromSpaceNo, toSpaceNo)
    if r == gameconst.SpaceEnterScene.ALLOW_CAST:
        return True

    return False

def getLineTypeFromCfgGameEntityId(cfgGameEntityId):
    return cfgGameEntityId // 10000

def getMoralLevel(moralValue):
    for k, v in PKMVE.datas.items():
        if moralValue >= v['lowerLimit'] and moralValue <= v['upperLimit']:
            DEBUG_MSG('getMoralLevel, level:', k, 'moralValue:', moralValue)
            return k
    WARNING_MSG('getMoralLevel, level not found:', moralValue)
    return 0

def getExpDecayRate(level):
    if level in PKMVE.datas:
        DEBUG_MSG('getExpDecayRate, level:', level, 'rate:', 1-PKMVE.datas[level]['ExpGainReduced'])
        return 1-PKMVE.datas[level]['ExpGainReduced']
    else:
        WARNING_MSG('getExpDecayRate, level not found:', level)
        return 1.0

def getTeamExpBonus(teammateNum):
    if teammateNum < 1:
        return 0
    teamExpBonus = TMMCD.datas['teamExperienceBonus']['value']
    return teamExpBonus[teammateNum-1]

def buildChatChannelAvatarInfo(entityId, playerGBID, school, name, level, sex, picFrameId, *args):
    return {
        'id': entityId,
        'gbId': playerGBID,
        'school': school,
        'name': name,
        'level': level,
        'sex': sex,
        'picFrameId': picFrameId}

def getConfirmMessageCooldown(mid, default=-1):
    _md = MSG.datas.get(mid, {})
    _to1 = _md.get('minDisplayTime', 0)
    if _to1 > 0:
        return _to1

    if _md['DisplayMode'] in gameconst.MessageType.COLL_BUTTON_MESSAGE:
        _to2 = _md.get('defaultCountdown', 0)
        if _to2 > 0:
            return _to2

    return default

def getDistanceSquare(pos1, pos2):
    return (pos1[0] - pos2[0]) ** 2 + (pos1[2] - pos2[2]) ** 2


def getNeedTranslateMsgId(msgId):
    msgId |= (1 << 30)
    return msgId

def decodeTranslateMsgId(msgId):
    msgId &= ~(1 << 30)
    return msgId

def getNeedTranslateArg(arg):
    return '^{}'.format(arg)


# 二分找到第一个大于target的位置
def binarySearchFirstGreater(arr, target):
    left, right = 0, len(arr) - 1

    while left <= right:
        mid = (left + right) // 2
        val = arr[mid]

        if val <= target:
            left = mid + 1
        else:
            right = mid - 1

    return left


def isActOpen(actId):
    return actId in gameglobal.globalActData


def checkCanChangeSceneAndShowMsg(avatar, fromSpaceNo, toSpaceNo):
    if fromSpaceNo == 0 and gameconfig.isCrossServer():
        return True
    _fromMapId = formula.getMapId(fromSpaceNo)
    _toMapId = formula.getMapId(toSpaceNo)
    _fromSceneType = GPGP.datas[_fromMapId]['sceneType']
    _toSceneType = GPGP.datas[_toMapId]['sceneType']

    if not GPES.datas[_fromSceneType][str(_toSceneType)]:
        avatar.showMsg(CCT.datas['leaveTheScene']['value'], [])
        return False
    
    return True

def getSkillLvParam(skillId):
    return combatSkill.SkillBase.getSkillLvParam(skillId)

def getSiegeWarFirstTimeInfo():
    firstTime = 0
    firstTimeValid = False
    if not gameconfig.serverId() in SLSL.datas:
        WARNING_MSG('[lj]get siege war first time info, server id not found:', gameconfig.serverId())
        return firstTime, firstTimeValid, 0
    crossServerGroupID = SLSL.datas[gameconfig.serverId()]['groupID']
    GroupServerList = SLSL.group2ServerIds[crossServerGroupID]
    GroupServerOpenTimes = []
    lastestOpenTime = 0 #group内开服最晚时间
    for serverID in GroupServerList:
        _openTime = int(SLSL.datas[int(serverID)]['startTime'])
        GroupServerOpenTimes.append(int(_openTime))
        if _openTime > lastestOpenTime:
            lastestOpenTime = _openTime
    
    if CBFT.datas.get(crossServerGroupID, None) is None:
        ERROR_MSG('[lj]cross siege war start time not found group id:', crossServerGroupID)
        firstTimeValid = False
    else:
        _startTimeStr = str(CBFT.datas[crossServerGroupID]['StartTime'])
        y = _startTimeStr[:4]
        m = _startTimeStr[4:6]
        d = _startTimeStr[6:8]
        #第一次活动开启时间
        firstTime = int(time.mktime(datetime.datetime(int(y), int(m), int(d), 0, 0, 0).timetuple()))

    #开服限制天数
    limitDay = CBC.datas['cityBattle_serverTimeLimit']['value']
    #在这之前不会开城战
    limitTime = lastestOpenTime + limitDay * 24 * 60 * 60
    #检查第一次是否合法
    if firstTime < limitTime:
        WARNING_MSG('[lj]first time config warning, first time:', time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(firstTime)), 'limit time:', time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(limitTime)))
        firstTimeValid = False
    else:
        firstTimeValid = True
    
    return firstTime, firstTimeValid, limitTime


def getSiegeWarMonthlyStartTime(monthAdd):
    now = getNow()
    startDayEveryMonth = CBC.datas['cityBattle_FirstStartTime']['value']
    y, m, d = time.strftime("%Y-%m-%d", time.localtime(now)).split('-')
    m = int(m) + monthAdd
    if m > 12:
        y = int(y) + 1
        m = m - 12
    if m < 1:
        y = int(y) - 1
        m = 12 + m
    nowStartTime = int(time.mktime(datetime.datetime(int(y), int(m), startDayEveryMonth, 0, 0, 0).timetuple()))
    return nowStartTime

def getNextSiegeWarMonthlyExpireTime(addTime):
    now = getNow()
    
    for i in (-1, 0, 1):
        t = getSiegeWarMonthlyStartTime(i) + addTime
        if now < t:
            return t
    ERROR_MSG('[lj]getNextSiegeWarMonthlyExpireTime failed, now:', now, 'addTime:', addTime)
    return getSiegeWarMonthlyStartTime(1) + addTime

def getNextBiddingStartTime():
    now = getNow()
    firstTime, firstTimeValid, limitTime = getSiegeWarFirstTimeInfo()
    if firstTimeValid and now < firstTime:
        return firstTime
    
    if now < getSiegeWarMonthlyStartTime(0):
        return getSiegeWarMonthlyStartTime(0)
    
    return getSiegeWarMonthlyStartTime(1)

def getSiegeWarBiddingEndTime():
    if gameglobal.globalSiegeWarData.get('expireTime', None) is not None:
        if getNow() < gameglobal.globalSiegeWarData['expireTime']:
            return gameglobal.globalSiegeWarData['expireTime']
    
    firstTime, firstTimeValid, limitTime = getSiegeWarFirstTimeInfo()
    addTime = CBC.datas['cityBattle_biddingTime']['value'] * 24 * 60 * 60 + CBC.datas['cityBattle_biddingDelayed']['value'][2] * 60 + CBC.datas['cityBattle_BiddingEndTime']['value'] * 60 * 60
    if firstTimeValid:
        expireTime = firstTime + addTime
        if getNow() < expireTime:
            gameglobal.globalSiegeWarData['expireTime'] = expireTime
            return expireTime
        
    t = getNextSiegeWarMonthlyExpireTime(addTime)
    gameglobal.globalSiegeWarData['expireTime'] = t
    return t

def isInSiegeWarBiddingTime():
    return getSiegeWarItemExpireTime() != 0

def getSiegeWarItemExpireTime():
    t = getSiegeWarBiddingEndTime()
    addTime = CBC.datas['cityBattle_biddingTime']['value'] * 24 * 60 * 60 + CBC.datas['cityBattle_biddingDelayed']['value'][2] * 60 + CBC.datas['cityBattle_BiddingEndTime']['value'] * 60 * 60
    biddingStartTime = t - addTime
    #竞拍时间外直接过期
    if getNow() < biddingStartTime:
        return 0
    return t

def getGuildRelation(guildUUID1, guildUUID2):
    _pair = getGuildUUIDPair(guildUUID1, guildUUID2)
    return gameglobal.guildRelationDic.get(_pair, gameconst.GuildRelationType.NONE)

def getCustomIdAndGid(spaceNo, gameEntityId):
    _mapId = formula.getMapId(spaceNo)
    _dunData = getDunModuleData(_mapId)
    if not _dunData:
        ERROR_MSG("[lj]getSiegeWarEntityCustomId: _dunData is None")
        return None, None

    gid, gct = splitGameEntityId(gameEntityId)
    gid = str(gid)
    if gid not in _dunData:
        return None, None
    if 'CustomID' not in _dunData[gid]:
        return None, None
    return _dunData[gid]['CustomID'], gid

def getGuildUUIDsByRelationType(guildUUID, relationType):
    _guildUUIDs = []
    for _guildUUIDPair, _relationType in gameglobal.guildRelationDic.items():
        if _relationType != relationType:
            continue

        if guildUUID == _guildUUIDPair[0]:
            _guildUUIDs.append(_guildUUIDPair[1])
        elif guildUUID == _guildUUIDPair[1]:
            _guildUUIDs.append(_guildUUIDPair[0])

    return _guildUUIDs


def iterGuildAndRelation(guildUUID):
    for _guildUUIDPair, _relationType in gameglobal.guildRelationDic.items():
        if _guildUUIDPair[0] == guildUUID:
            yield _guildUUIDPair[1], _relationType
        elif _guildUUIDPair[1] == guildUUID:
            yield _guildUUIDPair[0], _relationType


def transformPosesToSkillArgs(pos1, pos2, skillRange, direction):
    dist = sMath.distance2D(pos1, pos2)
    percent = float(sMath.limit(dist / skillRange, 0, 1)) if skillRange else 1.0
    arr = list(direction)
    arr.append(percent)
    return arr


def getRandomPositionFromMultiRegion(randomRegion, entityIDs=[], gid=0, RandomRegionAtLeastInfo=[]):
    chooseRegion = []
    chooseRadii = []
    chooseRegionWeight = []
    chooseIndex = -1
    i = 0
    for region in randomRegion:
        i = i + 1
        if not (type(region) is list and len(region) >= 5):
            continue

        chooseRegion.append((region[0], region[1], region[2]))
        chooseRadii.append(region[3])
        chooseRegionWeight.append(region[4])
        atleastnum = 0
        if len(region) > 5:
            atleastnum = int(region[5])

        if not (atleastnum > 0 and len(entityIDs) > 1):
            continue

        #初始化随机区域保底信息
        if gid in RandomRegionAtLeastInfo:
            if i not in RandomRegionAtLeastInfo[gid]:
                RandomRegionAtLeastInfo[gid][i] = 0
        else:
            RandomRegionAtLeastInfo[gid] = { i:0,}

        if RandomRegionAtLeastInfo[gid][i] < atleastnum:
            RandomRegionAtLeastInfo[gid][i] += 1
            chooseIndex = i - 1
            break

    if len(chooseRegion) != 0:
        if chooseIndex != -1 and chooseIndex < len(chooseRegion):
            index = chooseIndex
        else:
            index = randomByWeight(chooseRegionWeight)

    return getRandomPos(chooseRegion[index], chooseRadii[index])
 
def loadLineReadyEntities(spaceNo, entityIDs, readyEntitiesList):
    if not entityIDs:
        return

    RandomRegionAtLeastInfo = {}
    for gameEntityId in entityIDs:
        gid, gct = splitGameEntityId(gameEntityId)
        datas = getDunModuleData(formula.getMapId(spaceNo))

        if str(gid) not in datas:
            continue

        _mPrm = datas[str(gid)]
        className = _mPrm['ClassName']
        bornPosition = (_mPrm['PosX'], _mPrm['PosY'], _mPrm['PosZ'])

        if 'Dir' in _mPrm:
            bornDirection = (0.0, 0.0, _mPrm['Dir'] * math.pi / 180)
        else:
            bornDirection = gameconst.DEFAULT_DIRECTION

        tmpProps = {'createIndex': gct}

        params = {
            'spaceNo': spaceNo,
            'spaceno': spaceNo,
            'gameEntityId': gameEntityId,
            'direction': bornDirection,
            'position': bornPosition,
            'tmpProps': tmpProps,
        }

        if 'Props' in _mPrm:
            _pP = _mPrm['Props']

            if 'liveTimer' in _pP:
                params['liveTime'] = _pP['liveTimer']

            if 'Radius' in _pP:
                radius = params['bornRadius'] = float(_pP['Radius'])
                tmpProps['createRadius'] = radius

            if 'RefreshNum' in _pP:
                count = int(_pP['RefreshNum'])
                tmpProps['createCount'] = count

                if count == 0:
                    continue

                if count > 1000:
                    raise TypeError('Monster count must lower than 1000')

            if 'RefreshTime' in _pP:
                #刷新时间为列表时随机时间
                refreshTime = _pP['RefreshTime']
                if type(refreshTime) is list:
                    if len(refreshTime) == 1:
                        params['refreshTime'] = int(int(refreshTime[0]))
                    else:
                        params['refreshTime'] = int(random.randint(int(refreshTime[0]), int(refreshTime[1])))
                else:
                    params['refreshTime'] = int(_pP['RefreshTime'])

            if 'PathID' in _pP and _pP['PathID']:
                params['pathId'] = int(_pP['PathID'])

            if 'Level' in _pP:
                params['level'] = int(_pP['Level'])

            if 'RandomRegion' in _pP and _pP.get('IsForSkill', 0):
                #存在随机区域，则改变出生位置
                randomRegion = _pP['RandomRegion']
                
                bornPosition = getRandomPositionFromMultiRegion(randomRegion, entityIDs, gid, RandomRegionAtLeastInfo)
                params.update({
                    'position': bornPosition,
                })

        if className == 'Monster':
            _monsterId = int(_mPrm['EntityID'])
            params.update({
                'monsterId': _monsterId,
                'name': _mPrm['DisplayName'],
            })

        elif className == 'Teleporter':
            teleporterId = _mPrm['EntityID']
            params.update({
                'name': _mPrm['DisplayName'],
                'teleporterId': teleporterId,
                'teleportType': _mPrm.get('Props', {}).get('GateType', 0),
            })

        elif className == 'Npc':
            _isOpen = _mPrm.get('Props', {}).get('IsOpen', 1)
            if not _isOpen:
                continue

            _npcId = _mPrm['EntityID']
            params.update({
                'npcId': _npcId,
                'name': _mPrm['DisplayName'],
            })

        elif className == 'Collection':
            _isOpen = _mPrm.get('Props', {}).get('IsOpen', 1)
            if not _isOpen:
                continue

            collectionId = _mPrm['EntityID']
            collectionType = NPD.datas.get(collectionId, {}).get('type', gameconst.CollectionType.NORMAL)
            params.update({
                'name': _mPrm['DisplayName'],
                'collectionId': collectionId,
                'type': collectionType,
            })
        elif className == 'MonsterGrp':
            _groupId = _mPrm['EntityID']
            params.update({
                'name': _mPrm['DisplayName'],
                'groupId': _groupId,
            })
            radius = _mPrm.get('Props', {}).get('Radius', 0)
            if radius:
                params['bornRadius'] = radius
        elif className in ('Barrier', 'AirWall'):
            className = 'Barrier'
            _barrierId = _mPrm['ID']
            params.update({
                'name': _mPrm['DisplayName'],
                'barrierId': _barrierId,
            })
        elif className == 'CityBattleTeleporter':
            teleporterId = _mPrm['EntityID']
            params.update({
                'name': _mPrm['DisplayName'],
                'teleporterId': teleporterId,
                'cbID': _mPrm['ID'],
            })
        elif className == 'Creation':
            #Gm控制是否创建创生物
            if not gameconfig.loadCreation():
                continue
            _creationId = _mPrm['EntityID']
            params.update({
                'creationId': _creationId,
            })


        needCreateBase = 0
        data = (gameEntityId, spaceNo, className, needCreateBase, bornPosition, bornDirection, params, 0)
        DEBUG_MSG("loadLineEntities for single ", spaceNo, className, gameEntityId)
        readyEntitiesList.append(data)


def isBelongTimerTag(timerTag):
    return gametimer.TIMER_TAG_START <= timerTag < gametimer.TIMER_TAG_END

def isBelongTimerIdTag(timerIdTag):
    return gametimer.TIMER_ID_START <= timerIdTag < gametimer.TIMER_ID_END

def checkCombatRangeY(src, target):
    heightLimit = CCT.datas['damageHeightLimit'].get('value')
    host = getHostEntity(src)
    if src.IsMonster:
        attackHeightLimit = CBD.datas[src.monsterId]['attackHeightLimit']
        if attackHeightLimit:
            heightLimit = attackHeightLimit
    if host.IsAvatar and target.IsMonster:
        underAttackHeightLimit = CBD.datas[target.monsterId]['underAttackHeightLimit']
        if underAttackHeightLimit:
            heightLimit = underAttackHeightLimit
    return abs(src.position[1] - target.position[1]) <= heightLimit


def getCollisionDistance(creepBaseId, default=0):
    return CBD.datas[creepBaseId].get('collisionDistance', default)

def getMarkLimit():
    limitConf = CCT.datas['teamMarkLimit']['value']
    return gameconst.MARK_OTHER_MAX_NUM if limitConf < gameconst.MARK_OTHER_MAX_NUM else limitConf
