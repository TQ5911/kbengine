# -*- coding: utf-8 -*-
import builtins
import time
import json
import random
import math
import uuid
import ast
import utils
import importlib
import re
import datetime
import gametimer
import hashlib
import copy
from decimal import Decimal
from KBEDebug import *
from types import ModuleType, FunctionType
import sys
import pickle

import randomName_robotName as RND
import formula_generalFormula as FGFD
import fightProp_fightTargetType as FPFTTD
import fightProp_define

import gamePlay_gamePlay as GPGP
import gamePlay_enterScene as GPES
import const_const as CCT
import creep_force
import PKData_PKData as PKD
import PKData_moralValueEffect as PKMVE
import performanceLevel_set as PLSD
import teamMatch_matchConfig as TMMCD
import login_set as LGS
import message_Message as M_MD
import cityBattle_firstTime as CBFT
import cityBattle_config as CBC
import conflict_status_def as C_S_DD
import NPC_Pick as NPD
import creep_base as CBD
import gacha_gachaPool as GGP
import creep_coefficient as C_CD
import branchData_set as BDS
import cube_config
import wonderLand_config
import abyss_config
import soul_soul
import affix_affix
import character_charData

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

import mineBattle_config as MBC
import antiAddictionSystem_config as AASC
import gameconst
import experience_config as EC
import experience_global_EXP_Multiplier as EGM
import visible_visible as V_VD
import mall_coinPrice as MCP
import mall_mallConst as MMC
import branchData_branchData as B_BD
import traceback

tempTime = time.time
ASCII_LIST = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U',
              'V', 'W', 'X', 'Y', 'Z',
              'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
              'v', 'w', 'x', 'y', 'z',
              '0', '1', '2', '3', '4', '5', '6', '7', '8', '9']


class Swallower(object):
    def __getattribute__(self, name):
        if name.endswith('__') and name.startswith('__'):
            return super().__getattribute__(name)
        return self

    def __bool__(self):
        return False

    def __call__(self, *args, **kw):
        return


def curTS():
    return int(time.time())

def getTimestamp64(t=None):
    t = t or time.time()
    return int(round(t * 1000))


def getIntTimestamp64(sDate):
    if sDate == '':
        return 0
    _timeArr = time.strptime(sDate, "%Y%m%d%H%M%S")
    return int(round(int(time.mktime(_timeArr)) * 1000))


def getNowTimeStr(now=None):
    if not now:
        now = time.time()

    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(now))


# 1136185445 -> '20060102150405'
def getCommonTimeStrFromTimeStamp(timeStamp=0):
    timeStamp = timeStamp or int(time.time())
    return time.strftime('%Y%m%d%H%M%S', time.localtime(timeStamp))


def getIntTimestamp(sDate):
    if sDate == '':
        return 0
    _timeArr = time.strptime(sDate, "%Y%m%d%H%M%S")
    return int(time.mktime(_timeArr))


def getTodayZeroSec():
    today = datetime.date.today()
    return int(time.mktime(today.timetuple()))


def getCurrentTimeFmt():
    curr_time = datetime.datetime.now()
    timestamp = datetime.datetime.strftime(curr_time, '%Y-%m-%d %H:%M:%S')
    return timestamp


def getTodayFiveSec():
    _todayFive = getTodayZeroSec() + 18000
    if curTS() < _todayFive:
        return _todayFive - 24 * 3600
    else:
        return _todayFive


def isinstanceof(ent, entType):
    return ent.__class__.__name__ == entType


def getPythonAddr():
    import socket, struct
    _ipInt, _port = KBEngine.address()
    return '%s:%s' % (socket.inet_ntoa(struct.pack("I", _ipInt)), _port)


# |16bit-serverId|22bit-timestamp|26bit-seqId|
def generateUniqGlobalId():
    import gameconfig
    serverId = int(gameconfig.serverId())
    gbId = serverId << gameconst.SERVER_ID_BIT_SHIFT
    nowTime = curTS()

    timestampIdx = int((nowTime - gameconst.GBID_TIME_BASE) / gameconst.GBID_TIME_INTERVAL)
    gbId = gbId + timestampIdx
    gbId = gbId << gameconst.SERVER_TIMESTAMP_BIT_SHIFT

    if gameglobal.gbIdTSIdx != timestampIdx:
        gameglobal.gbIdSeqId = gameglobal.localBaseApp.getStartGbId()
        gameglobal.gbIdTSIdx = timestampIdx

    gameglobal.gbIdSeqId += 1
    return gbId + gameglobal.gbIdSeqId


# |18bit-serverId|6bit-groupOrder|29bit-timestamp|11bit-seqId|
def generateObId():
    import gameconfig
    serverId = int(gameconfig.serverId())
    _gid = KBEngine.getComponentGroupOrder()
    _ts = curTS() - 1640163600  # seconds since 2021-12-22 17:00
    if gameglobal.globalObIdTs != _ts:
        gameglobal.globalObIdTs = _ts
        gameglobal.globalObIdSeqId = 0

    gameglobal.globalObIdSeqId += 1
    seqId = gameglobal.globalObIdSeqId
    if seqId >= 2 ** 11:
        seqId = 2 ** 11 - 1
        LOG_ERR('genObId reach max', )

    return int(str(serverId) + str((_gid << 40) + (_ts << 11) + seqId))


def getEntity(entityClass):
    module = __import__(entityClass)
    _class = getattr(module, entityClass)
    for k, _v in KBEngine.entities.items():
        if type(_v).__name__ == _class.__name__:
            return _v


def getEntityList(entityClass):
    module = __import__(entityClass)
    _class = getattr(module, entityClass)

    res = []
    for k, _v in KBEngine.entities.items():
        if type(_v).__name__ == _class.__name__:
            res.append(_v)

    return res


def getAllAvatarByGm(su, box):
    res = getEntityList("Avatar")
    data = []
    groupOrder = KBEngine.getComponentGroupOrder()
    for ent in res:
        data.append({'entityId': ent.id, 'roleName': ent.getRoleCacheAttr('name'), 'gbId': str(ent.gbID), 'componentInfo': "baseapp%s-%s" % (groupOrder, str(ent.cell))})
    box.onGetAllPlayer(su, {groupOrder: data})


def getAvatar():
    return getEntity("Avatar")


def getAvatarByGbId(gbId):
    eid = gameglobal.roleGBIDToEntId.get(gbId, 0)
    return KBEngine.entities.get(eid)

def bset(val, bit):
    return (1 << bit) | val


def bhas(val, bit):
    return (1 << bit) & val


def breset(val, bit):
    return (~(1 << bit)) & val

def bgetIdxs(val):
    idxList = []
    idx = 0
    while val > 0:
        if val & 1:
            idxList.append(idx)
        val = val >> 1
        idx += 1
    return idxList


def isJoinCombat(entity, src):
    if (src.IsCombatUnit or src.IsCreation) and entity.IsAICombatUnit and entity.bornState not in \
            gameconst.BornStateEnum.joinCombatTup:
        return False

    if entity.IsAICombatUnit\
            and entity.aiController\
            and entity.aiController.stateMachine.speialAICombatTup\
            and entity.bornState in gameconst.BornStateEnum.speialAIInvalidCombatTup\
            and bhas(entity.cellFlags, gameconst.CELL_FLAGS_IS_SPECIAL_AI):
        return False

    if entity.hasState(C_S_DD.datas.relive) or src.hasState(C_S_DD.datas.relive):
        return False

    return True


def getRandomPos(center, radii):
    _r = radii * random.random()
    _theta = 2 * math.pi * random.random()

    return Math.Vector3(center) + Math.Vector3(_r * math.sin(_theta), 0, _r * math.cos(_theta))


def bytesToString(s, encoding='utf-8'):
    return str(s, encoding)


def bytesToStringRedis(origin, encoding='utf-8'):
    _ret = str(origin, encoding)
    if _ret == '""':
        return ''
    else:
        return _ret


def weightChoices(seq, weights, num=1):
    """
    带权重的不放回随机选择
    :param seq: 候选元素列表
    :param weights: 每个元素对应的权重（权重越大，选中概率越高）
    :param num: 要随机选择的数量，默认1
    :return: (选中的元素列表, 选中的下标列表)，参数非法时返回空列表
    """
    if len(seq) != len(weights):
        return [], []

    if num > len(seq):
        return [], []

    _choices = []
    for _ in range(num):
        _sumP = 0

        for i in range(len(weights)):
            if i in _choices:
                continue
            _sumP += weights[i]

        _randProp = random.randint(1, _sumP)
        for i, p in enumerate(weights):
            if i in _choices:
                continue

            _randProp = _randProp - p
            if _randProp <= 0:
                _choices.append(i)
                break

    return [seq[i] for i in _choices], _choices


def reloadCls(cls):
    if not hasattr(cls, '__bases__') \
            or not cls.__bases__ \
            or cls.__name__ in gameglobal.reloadedCls \
            or cls.__module__ == 'builtins':
        return

    _oldBases = cls.__bases__
    _newBases = []
    for bs in _oldBases:
        reloadCls(bs)

        _mod = importlib.import_module(bs.__module__)
        _newBs = getattr(_mod, bs.__name__)
        _newBases.append(_newBs)

    cls.__bases__ = tuple(_newBases)
    gameglobal.reloadedCls[cls.__name__] = 1


def resetClass(obj):
    _oldCls = obj.__class__
    _clsName = _oldCls.__name__

    __mod = importlib.import_module(_oldCls.__module__)

    _newCls = getattr(__mod, _clsName)
    reloadCls(_newCls)
    obj.__class__ = _newCls


def isInteger(intStr):
    try:
        int(intStr)
    except:
        return False
    return True


def isEntityId(intStr):
    if isInteger(intStr) and int(intStr) < gameconst.GBID_BASE:
        return True
    return False


def isGbId(intStr):
    if isInteger(intStr) and int(intStr) > gameconst.GBID_BASE:
        return True
    else:
        return False


def checkRoleName(player):
    return not isInteger(player) and type(player) is str


def checkBaseMailBox(ent):
    return 'baseapp' in str(ent)


def checkCellMailBox(ent):
    return 'cellapp' in str(ent)


def generateUUID():
    return str(uuid.uuid1())


def genGameEntityId(orgGameEntityId: int, count: int):
    _id = orgGameEntityId * 1000
    for i in range(count):
        _id += 1
        yield _id

def genGameEntityIdFrom(orgGameEntityId: int, count: int, fromIdx: int):
    _id = orgGameEntityId * 1000 + fromIdx
    for _ in range(count):
        _id += 1
        yield _id

def parseGidFromGameEntityId(gameEntityId: int):
    return gameEntityId // 1000


def splitFromGameEntityId(gameEntityId: int):
    _gid = parseGidFromGameEntityId(gameEntityId)
    _gct = gameEntityId - _gid * 1000
    return _gid, _gct


def randDelayTime(T, rdmRange=1.0):
    _rdmVal = random.random() * rdmRange
    _r = round(T + _rdmVal, 2)
    return _r if _r > 0.00 else 0.00


def checkDiffHour(nowTime, lastTime, cycleTime):
    stLastTime = time.localtime(lastTime + gameconst.ONE_HOUR_COST_SECONDES - cycleTime)
    stNowTime = time.localtime(nowTime + gameconst.ONE_HOUR_COST_SECONDES - cycleTime)
    if stNowTime.tm_hour == stLastTime.tm_hour:
        return False
    return True


def checkDiffDay(nowTime, lastTime, cycleTime):
    stLastTime = time.localtime(lastTime + gameconst.ONE_DAY_COST_SECONDS - cycleTime)
    stNowTime = time.localtime(nowTime + gameconst.ONE_DAY_COST_SECONDS - cycleTime)
    if stNowTime.tm_year == stLastTime.tm_year \
            and stNowTime.tm_mon == stLastTime.tm_mon \
            and stNowTime.tm_mday == stLastTime.tm_mday:
        return False
    return True


def checkDiffWeek(nowTime, lastTime, cycleTime):
    stLastTime = time.localtime(lastTime - cycleTime)
    stNowTime = time.localtime(nowTime - cycleTime)
    if time.strftime('%W', stNowTime) == time.strftime('%W', stLastTime):
        return False
    return True


def checkDiffMonth(nowTime, lastTime, cycleTime):
    stNowTime = time.localtime(nowTime - cycleTime)
    stLastTime = time.localtime(lastTime - cycleTime)
    if stNowTime.tm_year == stLastTime.tm_year and stNowTime.tm_mon == stLastTime.tm_mon:
        return False
    return True


def getCurrentMonthTS(now=None, offsetSec=0):
    if now is None:
        now = curTS()

    _tNow = time.localtime(now)
    ts = now - (
            _tNow.tm_mday - 1) * gameconst.ONE_DAY_COST_SECONDS - _tNow.tm_hour * gameconst.ONE_HOUR_COST_SECONDES - _tNow.tm_min * 60 - _tNow.tm_sec + offsetSec
    return ts


def getNextMonthTS(now=None, offsetSec=0):
    now = curTS() if now is None else now
    _tNow = time.localtime(now)
    if _tNow.tm_mon == 12:
        _tRet = (_tNow.tm_year + 1, 1, 1, 0, 0, 0, 0, 0, 0)
    else:
        _tRet = (_tNow.tm_year, _tNow.tm_mon + 1, 1, 0, 0, 0, 0, 0, 0)

    return time.mktime(_tRet) + offsetSec



def getCurWeekTS(now=None, offsetSec=0):
    now = curTS() if now is None else now
    _tNow = time.localtime(now)
    ts = now - _tNow.tm_wday * gameconst.ONE_DAY_COST_SECONDS - _tNow.tm_hour * gameconst.ONE_HOUR_COST_SECONDES - _tNow.tm_min * 60 - _tNow.tm_sec + offsetSec
    return ts

def getCurDayTS(now=None, offsetSec=0):
    now = curTS() if now is None else now
    _tNow = time.localtime(now)
    ts = now - _tNow.tm_hour * gameconst.ONE_HOUR_COST_SECONDES - _tNow.tm_min * 60 - _tNow.tm_sec + offsetSec
    return ts

def getNextDayTS(now=None, offsetSec=0):
    now = curTS() if now is None else now
    _tNow = time.localtime(now)
    ts = now + gameconst.ONE_DAY_COST_SECONDS - _tNow.tm_hour * gameconst.ONE_HOUR_COST_SECONDES - _tNow.tm_min * 60 - _tNow.tm_sec + offsetSec
    return ts

def getCurHourTS(now=None, offsetSec=0):
    now = curTS() if now is None else now
    return gameconst.ONE_HOUR_COST_SECONDES * (now // gameconst.ONE_HOUR_COST_SECONDES) + offsetSec


def getNowYearMonth(now=None):
    now = curTS() if now is None else now
    _tNow = time.localtime(now - 3600 * 5)
    return _tNow.tm_year, _tNow.tm_mon


def getTsFiveSec(ts):
    dayTime = ts - ts % 86400 + time.timezone
    dayTime += gameconst.GENERAL_CYCLE_TIME
    return dayTime


def countIntersDay(startTs):
    days = 0
    if not checkDiffDay(startTs, curTS(), gameconst.GENERAL_CYCLE_TIME):
        days = 1
    else:
        openFiveTs = getCurDayTS(startTs, gameconst.GENERAL_CYCLE_TIME)
        todayFiveTs = getCurDayTS(curTS(), gameconst.GENERAL_CYCLE_TIME)
        _tNow = time.localtime(curTS())

        days = (todayFiveTs - openFiveTs) // 86400
        LOG_INFO('countIntersDay', todayFiveTs, openFiveTs, days)
        if _tNow.tm_hour >= gameconst.GAME_REFRESH_OCLOCK:
            days += 1
        LOG_INFO('countIntersDay111', todayFiveTs, openFiveTs, days)
    return days


def getRandomName(sex=gameconst.Sex.FEMALE):
    _surnamesList = RND.datas.get('surname')
    _index = random.randint(0, len(_surnamesList) - 1)
    _surname = _surnamesList[_index]

    if sex == gameconst.Sex.FEMALE:
        _secondNameList = RND.datas.get('femaleName')
    else:
        _secondNameList = RND.datas.get('maleName')
    _index = random.randint(0, len(_secondNameList) - 1)
    _secondName = _secondNameList[_index]
    return _surname + _secondName


def getRandomSex():
    _sexes = [gameconst.Sex.MALE, gameconst.Sex.FEMALE]
    return random.choice(_sexes)


unichr = chr
_ESCAPE_TABLE = [unichr(x) for x in range(128)]
_ESCAPE_TABLE[0] = u'\\0'
_ESCAPE_TABLE[ord('\\')] = u'\\\\'
_ESCAPE_TABLE[ord('\n')] = u'\\n'
_ESCAPE_TABLE[ord('\r')] = u'\\r'
_ESCAPE_TABLE[ord('\032')] = u'\\Z'
_ESCAPE_TABLE[ord('"')] = u'\\"'
_ESCAPE_TABLE[ord("'")] = u"\\'"


def escape_string(val, mapping=None):
    return "'%s'" % val.translate(_ESCAPE_TABLE)


def isMyself(fn):
    @functools.wraps(fn)
    def _inner(self, *args, **kwargs):
        if self.id != abs(args[0]):
            return
        return fn(self, *args, **kwargs)

    return _inner


def needInTeam(fn):
    @functools.wraps(fn)
    def _inner(self, *args, **kwargs):
        if not hasattr(self, 'teamId'):
            LOG_ERR('AttributeError, no teamId in instance.')
            return None

        if self.teamId:
            return fn(self, *args, **kwargs)
        else:
            LOG_WARN('Called fn must in a team: {}'.format(fn))
            return None

    return _inner


def checkBagLocked(fn):
    @functools.wraps(fn)
    def _inner(bag, *args, **kwargs):
        if bag.isLocked():
            LOG_ERR('bag is locked:', fn.__name__, bag.lockedTime, bag.lockDesc)
            return None
        else:
            return fn(bag, *args, **kwargs)

    return _inner


def getRaycastPosition(spaceId, srcPosition, dstPosition, includeFollowEdge=False):
    posList = KBEngine.raycast(spaceId, gameconst.SpaceLayer.DEFAULT, srcPosition, dstPosition)
    if not posList:
        return dstPosition

    for pos in posList:
        if sMath.postion3DTo2DCell(pos) == sMath.postion3DTo2DCell(dstPosition):
            return pos

    else:
        realDstPos = sMath.getNearestPoint(dstPosition, posList)

    return realDstPos

def getSurfacePos(spaceId, srcPosition, x=10, y=20, z=10):
    posList = KBEngine.getSurface(spaceId, gameconst.SpaceLayer.DEFAULT, srcPosition, x, y, z)
    if not posList:
        LOG_WARN('getSurfacePos not find surface', spaceId, srcPosition, x, y, z)
        return srcPosition
    if posList[0][1] == 0:
        LOG_WARN('getSurfacePos y is zero', spaceId, srcPosition, x, y, z)
        return srcPosition
    return posList[0]


def checkDunFlowModuleDataExist(dunNo: int):
    return _checkDunXModuleDataExist(dunNo, 'e')


def _checkDunXModuleDataExist(dunNo: int, suffix: str = ''):
    if not dunNo or dunNo < 0:
        raise TypeError('dunNo must be value higher than zero, got {}'.format(dunNo))

    try:
        __import__(_getDunXModuleName(dunNo, suffix)).datas
        return True
    except (ImportError, AttributeError) as err:
        return False


def getDunModuleData(dunNo: int):
    """get module datas in dun_xxx"""
    return _getDunXModuleData(dunNo)


def getDunFLowModuleData(dunNo: int):
    """get module datas in dun_xxx_e"""
    return _getDunXModuleData(dunNo, 'e')

def isDunGroupModuleDataExist(dunNo: int):
    return _checkDunXModuleDataExist(dunNo, 'g')

def getDunGroupModuleData(dunNo: int):
    """get module datas in dun_xxx_g"""
    return _getDunXModuleData(dunNo, 'g')

def getAirWallModuleData(dunNo: int):
    """get module datas in dun_xxx_g"""
    return _getDunXModuleData(dunNo, 'a', showErrMsg=False)

def getDunStructModData(dunNo: int, actId: int = 0):
    """get module datas in dun_xxx_s"""
    if actId:
        key = 'Act%s' % actId
    else:
        key = 'SpaceConfig'

    datas = _getDunXModuleData(dunNo, 's', False)
    return datas[key]


def _getDunXModuleData(dunNo: int, suffix: str = '', showErrMsg=True):
    if not dunNo or dunNo < 0:
        raise TypeError('dunNo must be value higher than zero, got {}'.format(dunNo))

    try:
        return __import__(_getDunXModuleName(dunNo, suffix)).datas
    except (ImportError, AttributeError) as err:
        showErrMsg and LOG_ERR('_getDunXModuleData::', dunNo, suffix, err)
        return {}


def getDunModuleName(dunNo: int):
    return _getDunXModuleName(dunNo)


def _getDunXModuleName(dunNo: int, suffix: str = ''):
    module_template = 'dun_{{}}_{}'.format(suffix) if suffix else 'dun_{}'
    module_name = module_template.format(dunNo)

    return module_name

def getEntityBoxGroupId(gameEntityId, spaceNo):
    _dunData = getDunModuleData(formula.fetchMapId(spaceNo))
    _gid = parseGidFromGameEntityId(gameEntityId)
    _params = _dunData.get(str(_gid), None)
    if not _params:
        return 0
    _chestGroupID = _params['Props'].get('ChestGroupID', 0) or 0
    return _chestGroupID


def getEntitiesByIds(entIdList):
    _ents = []
    for _eid in entIdList:
        _ent = KBEngine.entities.get(_eid)
        if _ent and not _ent.isDestroyed:
            _ents.append(_ent)
    return _ents


def fetchBuffEffectKey(effectId, effectIndex):
    return effectId * 100 + effectIndex


_severFormulaComplie = re.compile(r'formula:\s*(\d{8})')


def _getFuncByFormula(formulaStr):
    try:
        _idStr = _severFormulaComplie.search(formulaStr)
        return FGFD.datas[int(_idStr.group(1))]['serverFormula']
    except Exception as e:
        raise e


def getValByFormula(formulaStr, param):
    fn = _getFuncByFormula(formulaStr)
    if not callable(fn):
        LOG_WARN("getValByFormula:: value not callable", formulaStr, fn)
        return fn

    return fn(param)


def calcFormulaValue(formulaId, params):
    _fn = FGFD.datas[formulaId]['serverFormula']
    if not callable(_fn):
        LOG_WARN("calcFormulaValue:: value not callable", formulaId, _fn)
        return _fn

    return _fn(*params)


def randomByWeight(weight_list):
    _sumWeight = sum(weight_list)
    _randomWeight = random.uniform(0, _sumWeight)
    _flagVal = 0
    for _idx, _weight in enumerate(weight_list):
        _flagVal += _weight
        if _randomWeight < _flagVal:
            return _idx
    return None


def man_outside_gm_cmds():
    import gmAdmin
    _max_name_len = _max_desc_len = 0

    def __yield():
        nonlocal _max_desc_len, _max_name_len

        for _cmd in gameglobal.GM_CMDS.values():
            _name = _cmd.name
            if "_" in _name:
                continue
            if not _cmd.checkSide(gmAdmin.OUTSIDE):
                continue
            _desc = _cmd.desc
            args = ((i.__class__.__name__, i.fetchDesc()) for i in _cmd.args)

            _len_name = len(_name)
            _len_desc = len(_desc)
            _max_name_len = _len_name if _len_name > _max_name_len else _max_name_len
            _max_desc_len = _len_desc if _len_desc > _max_desc_len else _max_desc_len

            yield _name, _desc, args

    _data = [_ for _ in __yield()]
    _result = []
    for i in _data:
        _args = i[2]
        _args = ['{}({})'.format(i[1], i[0]) for i in _args]
        _tmp = {"name": i[0], "desc": i[1], "args": _args}

        _result.append(_tmp)
    return _result


def getRealAvatarEntity(entity, height=2):
    orgEnt = entity
    for _ in range(height):
        if not entity:
            return None, True

        if entity.IsAvatar:
            return entity, False

        if not hasattr(entity, 'hostId'):
            return None, True

        entity = entity.getHost()

    LOG_ERR('getRealAvatarEntity:: ent not found', orgEnt, height)
    return None, True


def bytesToHex(bytesVal):
    bytesVal = ''.join(['%02x' % b for b in bytesVal])
    return '0x' + bytesVal


def getAreaId(mapId, pos, scaleSize=1):
    if not gameglobal.areaData or not pos:
        return 0

    _x = int(pos[0])//scaleSize
    _z = int(pos[2])//scaleSize

    _curAreaDataInfo = gameglobal.areaData.get(mapId)
    if not _curAreaDataInfo:
        return 0

    _height, _areaData = _curAreaDataInfo

    return _areaData.get(_z * _height + _x, 0)


def getSvrOpenDayFiveTS():
    import gameconfig
    svrOpenTime = gameconfig.serverOpenTime()
    _timeArr = list(time.localtime(svrOpenTime))
    if 0 <= _timeArr[3] < 5:
        offset = gameconst.ONE_DAY_COST_SECONDS
    else:
        offset = 0
    _timeArr[3] = 5
    _timeArr[4] = 0
    _timeArr[5] = 0
    return int(time.mktime(tuple(_timeArr))) - offset


def getSvrOpenDays(now=None):
    svrOpenTime = getSvrOpenDayFiveTS()
    return math.floor(((now or curTS()) - svrOpenTime) / gameconst.ONE_DAY_COST_SECONDS) + 1


def getHostEntity(entity):
    if not entity:
        return

    _target = entity
    if not (entity.IsCreation or entity.IsSummon):
        return _target

    if not entity.hostId:
        return _target

    return entity.getHost() or entity


def parseCrontabPattern(express):
    _ct = crontab.CronTab(express)
    return [sorted(list(_c.allowed)) for _c in _ct.matchers[:5]]


def fetchLastDayOfMonth(year, month):
    _nextMonth = month + 1 if 0 < month < 12 else 1
    _t = time.mktime((year, _nextMonth, 1, 0, 0, 0, 0, 0, 0))

    __tplSec = time.localtime(_t - 3600 * 24)

    return __tplSec[2]


_ALL_MINUTES = range(60)
_ALL_HOURS = range(24)
_ALL_MONTHS = range(1, 13)
_ALL_WEEK_DAYS = range(7)


def nextByTimeTuple(tup, now=None):
    if len(tup) not in (5, 6):
        return sys.maxsize

    if not any(tup):
        return 0

    now = now or curTS()
    _nowDatetime = datetime.datetime.fromtimestamp(now)
    _tplSec = _nowDatetime.timetuple()
    curYear, _curMonth, _curDay, _curHour, curMin, curSec, curWeekDay = _tplSec[0:7]
    _years = []
    if len(tup) == 5:
        _minutes, _hours, _days, _months, _weekdays = tup
    else:
        _minutes, _hours, _days, _months, _weekdays, _years = tup

    if _days and _weekdays:
        return sys.maxsize

    _minutes = _minutes or _ALL_MINUTES
    _hours = _hours or _ALL_HOURS
    _months = _months or _ALL_MONTHS
    _weekdays = _weekdays or _ALL_WEEK_DAYS
    # _years = _years or allYears

    if not _years or curYear in _years:
        for month in _months:
            if month < _curMonth:
                continue

            allDays = range(1, fetchLastDayOfMonth(curYear, month) + 1)
            _mDays = _days or allDays
            if _mDays[-1] > allDays[-1]:
                return sys.maxsize

            for day in _mDays:
                if month == _curMonth and day < _curDay:
                    continue

                dt = datetime.datetime(curYear, month, day)
                if dt.isoweekday() % 7 not in _weekdays:
                    continue

                for hour in _hours:
                    if month == _curMonth and day == _curDay and hour < _curHour:
                        continue
                    for minute in _minutes:
                        dt = datetime.datetime(curYear, month, day, hour, minute)
                        if dt > _nowDatetime:
                            return (dt - _nowDatetime).total_seconds()

    _years = _years or range(curYear + 1, curYear + 10)
    for year in _years:
        if year <= curYear:
            continue

        for month in _months:
            allDays = range(1, fetchLastDayOfMonth(curYear, month) + 1)
            _mDays = _days or allDays
            for day in _mDays:
                dt = datetime.datetime(curYear + 1, month, day)
                if dt.isoweekday() % 7 not in _weekdays:
                    continue

                dt = datetime.datetime(year, month, day, _hours[0], _minutes[0])
                return (dt - _nowDatetime).total_seconds()

    return sys.maxsize


def previousByTimeTuple(tup, now=None):
    if len(tup) not in (5, 6):
        return sys.maxsize

    if not any(tup):
        return 0

    now = now or curTS()
    _nowDatetime = datetime.datetime.fromtimestamp(now)
    _tplSec = _nowDatetime.timetuple()
    curYear, _curMonth, _curDay, _curHour, curMin, curSec, curWeekDay = _tplSec[0:7]
    _years = []
    if len(tup) == 5:
        _minutes, _hours, _days, _months, _weekdays = tup
    else:
        _minutes, _hours, _days, _months, _weekdays, _years = tup

    if _days and _weekdays:
        return sys.maxsize

    _minutes = _minutes or _ALL_MINUTES
    _hours = _hours or _ALL_HOURS
    _months = _months or _ALL_MONTHS
    _weekdays = _weekdays or _ALL_WEEK_DAYS
    # _years = _years or allYears

    if not _years or curYear in _years:
        for month in reversed(_months):
            if month > _curMonth:
                continue

            allDays = range(1, fetchLastDayOfMonth(curYear, month) + 1)
            _mDays = _days or allDays
            if _mDays[-1] > allDays[-1]:
                return sys.maxsize

            for day in reversed(_mDays):
                if month == _curMonth and day > _curDay:
                    continue

                dt = datetime.datetime(curYear, month, day)
                if dt.isoweekday() % 7 not in _weekdays:
                    continue

                for hour in reversed(_hours):
                    if month == _curMonth and day == _curDay and hour > _curHour:
                        continue
                    for minute in reversed(_minutes):
                        dt = datetime.datetime(curYear, month, day, hour, minute)
                        if dt <= _nowDatetime:
                            return (_nowDatetime - dt).total_seconds()

    _years = _years or range(curYear - 10, curYear)
    for year in reversed(_years):
        if year >= curYear:
            continue
        for month in reversed(_months):
            allDays = range(1, fetchLastDayOfMonth(curYear, month) + 1)
            _mDays = _days or allDays
            for day in reversed(_mDays):
                dt = datetime.datetime(year, month, day)
                if dt.isoweekday() % 7 not in _weekdays:
                    continue

                dt = datetime.datetime(year, month, day, _hours[-1], _minutes[-1])
                return (_nowDatetime - dt).total_seconds()

    return sys.maxsize


def nextByCronTupleList(tps, now=None):
    _nextStart = -1
    _cronTuple = None
    for _, tp in enumerate(tps):
        tNext = nextByTimeTuple(tp, now)
        if _nextStart < 0 or tNext < _nextStart:
            _nextStart = tNext
            _cronTuple = tp

    return _nextStart, _cronTuple


_TFLAG_START = 1
_TFLAG_END = 2


def _inTimeTupleRange(start, end, now):
    _tNextSrt = nextByTimeTuple(start, now)
    _tNextEnd = nextByTimeTuple(end, now)
    _tPrevSrt = previousByTimeTuple(start, now)
    _tPrevEnd = previousByTimeTuple(end, now)
    _timeline = sorted(((now - _tPrevSrt if _tPrevSrt < sys.maxsize else math.inf, _TFLAG_START),
                       (now - _tPrevEnd if _tPrevEnd < sys.maxsize else math.inf, _TFLAG_END),
                       (now + _tNextSrt if _tNextSrt < sys.maxsize else math.inf, _TFLAG_START),
                       (now + _tNextEnd if _tNextEnd < sys.maxsize else math.inf, _TFLAG_END)),
                      key=lambda x: x[0])
    # | _TIMELINE: -------- a --- b --- c --- d -----
    # | NOW:      ----------- x --------------------
    # L&R Closed Interval
    LOG_DBG("_inTimeTupleRange::", start, end, now, _timeline)
    if now > _timeline[-1][0]:
        return _timeline[-1][1] == _TFLAG_START

    for i in reversed(range(len(_timeline) - 1)):
        if _timeline[i][0] <= now:
            if _timeline[i][1] == _TFLAG_START:
                return True
            if _timeline[i][1] == _TFLAG_END:
                return False
            return False

    if now < _timeline[0][0]:
        return _timeline[0][1] == _TFLAG_END

    return False


def inTimeTupleRange(start, end, now=None):
    now = now if now is not None else curTS()
    LOG_DBG("inTimeTupleRange::START", start, end, now)
    r = _inTimeTupleRange(start, end, now)
    LOG_DBG("inTimeTupleRange::ENDED", r, start, end, now)
    return r


def inTimeTuplesRange(startsList, endsList, now=None):
    if not startsList or not endsList or len(startsList) != len(endsList):
        return False

    for idx, startCron in enumerate(startsList):
        endCron = endsList[idx]
        if inTimeTupleRange(startCron, endCron, now):
            return True

    return False


def getRemainTimeStr(timestamp):
    hours = timestamp // gameconst.ONE_HOUR_COST_SECONDES
    mins = timestamp % gameconst.ONE_HOUR_COST_SECONDES // 60
    seconds = timestamp % 60
    if hours:
        return '{}小时{}分{}秒'.format(hours, mins, seconds)

    if mins:
        return '{}分{}秒'.format(mins, seconds)

    return '{}秒'.format(seconds)


def isBeyondOneDay(timestamp):
    return timestamp + gameconst.ONE_DAY_COST_SECONDS < curTS()


def decClientData(dataBytes):
    try:
        _data = json.loads(dataBytes.decode('utf-8'), encoding='utf-8')
    except:
        _data = {}

    return _data


def encClientData(clientData):
    try:
        _dataBytes = json.dumps(clientData).encode('utf-8')
    except:
        _dataBytes = ''

    return _dataBytes


def mixRealAccountName(accountType, accountName):
    import proto.centralLogin_pb2 as centralLogin
    if accountType == centralLogin.ACCOUNT_UNKNOW:
        return accountName
    else:
        return '%s:%s' % (accountType, accountName)


def fetchAccountTypeAndName(accountName):
    import proto.centralLogin_pb2 as centralLogin
    _parts = accountName.split(':')
    if len(_parts) > 1:
        return int(_parts[0]), _parts[1]
    return centralLogin.ACCOUNT_UNKNOW, _parts[0]


def checkAvatarNameLength(name):
    if not LC_LCD.datas['playerNameMinLength']['value'] <= len(name) <= LC_LCD.datas['playerNameMaxLength']['value']:
        return False
    return True


def checkAvatarName(name):
    if not gameconst.RE_VALIDATE_AVATAR_NAME_COMPILE.fullmatch(name):
        return False
    return True


def getMaxPlayerLevel():
    return CCT.datas['maxLevel']['value']


def getPlayerBornInfo():
    posList = CCT.datas['createConst_BornPos']['value']
    pos = random.choice(posList)
    return pos[0], pos[1]

def getPlayerBornMapId():
    return CCT.datas['createConst_BornGamePlayID']['value']

def getPlayerBreakAwayStuckPos(spaceNo, position, needBornPos=False):
    mapId = formula.fetchMapId(spaceNo)
    data = getDunStructModData(mapId)
    posDatas = data.get('BreakAwayStuckPos', {})
    if not posDatas or needBornPos:
        posDatas = data.get('BornPos', {})
    if not posDatas:
        return None, None
    resList = []
    for _, posData in posDatas.items():
        pos = (posData["PosX"], posData["PosY"], posData["PosZ"])
        direction = posData["Dir"]
        resList.append((pos, direction))
    if not resList:
        return None, None
    return random.choice(resList)


def fetchCrtMapCanEnterDungeonFlag(mapId):
    """是否可以进入副本"""
    return GPGP.datas\
        .get(mapId, {})\
        .get('ifEnterDun', gameconst.GamePlayMapCheckEnum.DENY)


def checkCanIterable(val):
    return hasattr(val, '__iter__') or hasattr(val, '__getitem__')


def parseCommEventParams(paramStr):
    _parsmsList = paramStr.split(';')
    _args = _parsmsList[0].split(',') if _parsmsList[0] else []
    _kwargs = {}
    if len(_parsmsList) == 2:
        _kwargs = json.loads(_parsmsList[1])
    return _args, _kwargs


def checkBoxOffline(box):
    # 先删除isDestroying判断，正常情况应该在下线销毁时就从stub注销自己，而不是持有一个isDestroyed的对象再判断
    if isinstance(box, KBEngine.Proxy):
        if box.isDestroyed:
            gameengine.panicStack('use of destroyed box')
        return box.isDestroyed

    return box is None


def getCommonTimeStr(now):
    tTime = time.localtime(now)
    return ' {}年{}月{}日 {:0>2d}:{:0>2d} '.format(tTime.tm_year, tTime.tm_mon, tTime.tm_mday, tTime.tm_hour,
                                                   tTime.tm_min)


def setCallbackTmpInfo(owner, opUUID, callbackData):
    _callbackInfoDic = owner.getTempMiscProp(gameconst.EntityPropsEnum.callbackTmpInfo)
    if not _callbackInfoDic:
        _callbackInfoDic = {}
    _callbackInfoDic[opUUID] = callbackData
    owner.setTempMiscProp(gameconst.EntityPropsEnum.callbackTmpInfo, _callbackInfoDic)
    return


def popCallbackTmpInfo(owner, opUUID):
    _callbackInfoDic = owner.getTempMiscProp(gameconst.EntityPropsEnum.callbackTmpInfo)
    if not _callbackInfoDic:
        return None
    return _callbackInfoDic.pop(opUUID, None)


def fetchSpaceEnterScene(crtSpaceTp, enterSpaceTp, default=gameconst.SpaceEnterScene.DENY):
    return GPES.datas.get(crtSpaceTp, {}).get(str(enterSpaceTp), default)


def fetchLineMaxNumber(lineType):
    return gameconst.lineStubMap()\
        .get(lineType, {})\
        .get('lineCount', 0)


def isInWorldPKSafeAreaByAreaId(areaId):
    import worldConfig_Area

    if not areaId:
        return False

    _areaData = worldConfig_Area.datas.get(areaId, None)
    if not _areaData:
        return False

    if not _areaData['ifSafeArea']:
        return False

    return True


def addResourceVal(oldVal, delta, valType):
    _newVal = oldVal + delta
    if valType == gameconst.ReourceValType.UINT32:
        _maxVal = 0xFFFFFFFF
    elif valType == gameconst.ReourceValType.INT32:
        _maxVal = 0x7FFFFFFF
    elif valType == gameconst.ReourceValType.UINT64:
        _maxVal = 0xFFFFFFFFFFFFFFFF
    elif valType == gameconst.ReourceValType.INT64:
        _maxVal = 0x7FFFFFFFFFFFFFFF
    elif valType == gameconst.ReourceValType.UINT8:
        _maxVal = 0xFF
    else:
        return _newVal

    if _newVal < 0:
        if valType in (
                gameconst.ReourceValType.UINT32, gameconst.ReourceValType.UINT64, gameconst.ReourceValType.UINT8,):
            gameengine.panicStack('add checkResourceValLimit, minus source val:', _newVal, valType)
            _newVal = 0
    elif _newVal > _maxVal:
        gameengine.panicStack('add checkResourceValLimit, exceed max val:', _newVal, valType, _maxVal)
        _newVal = _maxVal
    return _newVal

def deductResourceVal(oldVal, delta, valType):
    _newVal = oldVal + delta
    if valType == gameconst.ReourceValType.UINT32:
        _minVal = 0
    elif valType == gameconst.ReourceValType.INT32:
        _minVal = -0x80000000
    elif valType == gameconst.ReourceValType.UINT64:
        _minVal = 0
    elif valType == gameconst.ReourceValType.INT64:
        _minVal = -0x8000000000000000
    elif valType == gameconst.ReourceValType.UINT8:
        _minVal = 0
    else:
        return _newVal

    if _newVal < 0:
        if valType in (
                gameconst.ReourceValType.UINT32, gameconst.ReourceValType.UINT64, gameconst.ReourceValType.UINT8,):
            gameengine.panicStack('deduct checkResourceValLimit, minus source val:', _newVal, valType)
            _newVal = 0
    elif _newVal < _minVal:
        gameengine.panicStack('deduct checkResourceValLimit, exceed max val:', _newVal, valType, _minVal)
        _newVal = _minVal
    return _newVal

def getFraction(val, len=100):
    return int(round(val - int(val), 2) * len)


def addFraction(val, addVal, maxValue=gameconst.UINT8_MAX):
    if val + addVal > maxValue:
        return (val + addVal) - maxValue - 1, 1
    else:
        return val + addVal, 0


def fetchAccountTypeByPlatId(platId):
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
def fetchShowCompleteModelNum():
    return PLSD.datas["showCompleteModelNum"].get("value")


@functools.lru_cache(maxsize=1)
def fetchShowNameNum():
    return PLSD.datas["showNameNum"].get("value")


def fetchBanEndTimeString(banTime):
    if banTime != -1:
        return time.strftime("%Y年%m月%d日%H时%M分%S秒", time.localtime(banTime))
    else:
        return LGS.datas['foreverText']['value']


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
        gameengine.panicStack('getServerLevel, no serverLevelInfo')
        return 1
    return serverLevelInfo[1]


def fetchExposedMethods():
    _methods = KBEngine.getExposedMethods('Avatar')
    _uidMethodMap = KBEngine.getUidMethodMap('Avatar')
    _methodUidMap = {v: k for k, v in _uidMethodMap.items()}
    _result = {}
    for m in _methods:
        _result[_methodUidMap[m]] = m

    return _result


def fetchCallStats():
    _results = []
    for uid, methodName in gameglobal.avatarExposedMethods.items():
        num = KBEngine.getCallNum('Avatar', uid)
        if num:
            _results.append((num, methodName))

    _results.sort(reverse=True)
    return _results


@functools.lru_cache(100)
def parseTimeStr(timeStr):
    return int(time.mktime(time.strptime(timeStr, '%Y%m%d%H%M%S')))


@functools.lru_cache(100)
def parseDayCycleTimeStr(timeStr):
    _ = timeStr.split(':')  # timeStr : '20:00:00'
    return int(_[0]) * gameconst.ONE_HOUR_COST_SECONDES + int(_[1]) * gameconst.ONE_MINUTE_COST_SECONDS + int(_[2])


def parseDayTimeStr(timeStr, now=None):
    tss = parseDayCycleTimeStr(timeStr)
    return getCurDayTS(now, tss)


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

    now = curTS()
    nDate = time.localtime(now)

    LOG_DBG('isAdult', birthYear, birthMon, birthDay, nDate)
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
    LOG_DBG('encodeEquityJson--', extraJson)
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


def getGuildUUIDPair(guildUUID1, guildUUID2):
    if guildUUID1 < guildUUID2:
        return (guildUUID1, guildUUID2)
    else:
        return (guildUUID2, guildUUID1)


def isEnemyInPK(src, target):
    if src.pkModel == gameconst.PKModelEnum.PEACE:
        return False

    if utils.bhas(src.cellFlags, gameconst.CELL_FLAGS_PK_SAFE) or utils.bhas(target.cellFlags, gameconst.CELL_FLAGS_PK_SAFE):
        return False

    if src.inPKProtect(target):
        return False

    if src.pkModel == gameconst.PKModelEnum.JUSTICE:
        return target.inRedName() or target.isGreyName()

    elif src.pkModel == gameconst.PKModelEnum.ENEMY:
        if target.inRedName() or target.isGreyName():
            return True

        _relation = getGuildRelation(src.guildUUID, target.guildUUID)
        return _relation == gameconst.GuildRelationType.ENEMY

    return True


def getEntityRealEntity(entity):
    if entity and (entity.IsCreation or entity.IsSummon):
        if entity.hostId:
            entity = entity.getHost() or entity

    return entity


def isEnemy(src, tgt):
    if src.isDestroyed or tgt.isDestroyed:
        return False

    if src.id == tgt.id:
        return False

    if src.IsAvatar and src.guildRelationVersion != gameglobal.guildRelationVersion:
        src.resetAllTargetTypeCache()

    if tgt.id in src.enemiesCacheSet:
        return True

    elif tgt.id in src.notEnemiesCacheSet:
        return False

    if not (src.isReal() and tgt.isReal()):
        return False

    _bIsEnemy = _isEnemy(src, tgt)
    if _bIsEnemy:
        src.enemiesCacheSet.add(tgt.id)
    else:
        src.notEnemiesCacheSet.add(tgt.id)

    tgt.cacheSelfSet.add(src.id)

    return _bIsEnemy


def _isEnemy(src, tgt):
    if (not src.IsCombatUnit and not src.IsCreation) or not tgt.IsCombatUnit:
        return False

    src, tgt = getEntityRealEntity(src), getEntityRealEntity(tgt)
    if src.id == tgt.id:
        return False

    # 切磋状态下，只能攻击切磋对象
    if src.IsAvatar:
        if src.duelAttr.inFight():
            if not tgt.IsAvatar:
                return False

            return src.duelAttr.isDuelEnemy(tgt)

        elif src.duelAttr.inReady():
            return False

    if formula.inSiegeWarScene(src.spaceNo):
        if formula.inSiegeWarScene(tgt.spaceNo):
            if src.IsAvatar and tgt.IsAvatar:
                if not src.siegeWarCanAttack:
                    return False
            return src.siegeWarCamp != tgt.siegeWarCamp

    _enemy, needReturn = isMineWarEnemy(src, tgt)
    if needReturn:
        return _enemy

    # pk规则判断
    if src.IsAvatar and tgt.IsAvatar:
        # 【野外PK
        # A开戮斗模式攻击B，客户端可以放技能没有伤害，客户端判断能打，但是服务端判断不能打】

        if isEnemyInPK(src, tgt):
            return True

    if fetchForceRelation(src, tgt) == gameconst.ForceRelation.Enemy:
        return True

    return False

def isMineWarEnemy(src, target):
    if utils.bhas(src.cellFlags, gameconst.CELL_FLAGS_IS_MINE_WAR_SPACE):
        if utils.bhas(target.cellFlags, gameconst.CELL_FLAGS_IS_MINE_WAR_SPACE):
            if target.IsMonster:
                if not target.mineWarCanAttack:
                    return False, True
                if src.IsAvatar:
                    if src.guildUUID == 0 and target.mineWarMonsterFlag == gameconst.MineWarMonsterFlag.MINE_CORE:
                        return False, True
                    return src.mineWarCamp != target.mineWarCamp, True
            if src.IsAvatar and target.IsAvatar and src.mineWarCanAttack and target.mineWarCanAttack:
                if src.guildUUID > 0 and (src.guildUUID == target.guildUUID or getGuildRelation(src.guildUUID, target.guildUUID) == gameconst.GuildRelationType.UNION):
                    result = False
                else:
                    result = True
                return result, True
            if src.IsCreation and target.IsAvatar:
                return True, True
    return False, False

def isPVP(src, tgt):
    _srcHost = getHostEntity(src)
    _targetHost = getHostEntity(tgt)
    if _srcHost and _targetHost:
        if _srcHost.IsAvatar:
            if _targetHost.IsAvatar:
                return True

    return False


_isFriendFunDic = {}


def isFriend(src, tgt):
    if src.isDestroyed or tgt.isDestroyed:
        return False

    if src.id == tgt.id:
        return False

    if tgt.id in src.friendsCacheSet:
        return True

    elif tgt.id in src.notFriendsCacheSet:
        return False

    if not (src.isReal() and tgt.isReal()):
        return False

    bIsFriend = _isFriend(src, tgt)
    if bIsFriend:
        src.friendsCacheSet.add(tgt.id)
    else:
        src.notFriendsCacheSet.add(tgt.id)

    tgt.cacheSelfSet.add(src.id)

    return bIsFriend


def _isFriend(src, tgt):
    if src.id == tgt.id:
        return False

    src, tgt = getEntityRealEntity(src), getEntityRealEntity(tgt)
    if src.id == tgt.id:
        return True

    # 切磋状态下，不能影响任何人
    #     【【切磋】处于切磋中的人放的加血技能可以给非切磋目标加血】
    # https://www.tapd.cn/tapd_fe/59721401/bug/detail/1159721401001002975
    if src.IsAvatar and src.duelAttr.inFight():
        return False

    spaceType = formula.fetchMapId(src.spaceNo)

    if spaceType in _isFriendFunDic:
        ret = _isFriendFunDic[spaceType](src, tgt)
        if ret == gameconst.IsRelationEnum.TRUE:
            return True
        elif ret == gameconst.IsRelationEnum.FALSE:
            return False

    if src.IsAvatar and tgt.IsAvatar:
        return not isEnemy(src, tgt)

    return False


def isFriendIncS(src, tgt):
    if src.id == tgt.id:
        return True

    return isFriend(src, tgt)


def fetchForceRelation(src, tgt):
    if not src or not tgt:
        return gameconst.ForceRelation.UnKnownForceRelation

    _datas = creep_force.datas
    _force = src.force

    if _force not in _datas:
        return gameconst.ForceRelation.UnKnownForceRelation

    _subforceRelation = _datas[_force]

    _targetForceType = gameconst.ForceTypeEnum.getForceType(tgt.force)

    if _targetForceType in _subforceRelation:
        return _subforceRelation[_targetForceType]
    else:
        return gameconst.ForceRelation.UnKnownForceRelation


def getRaceTypeEnum(entity):
    if entity.IsAvatar:
        return gameconst.RaceTypeEnum.avatar

    elif entity.IsMonster:
        return gameconst.RaceTypeEnum.monster

    elif entity.IsSummon:
        return gameconst.RaceTypeEnum.summon

    elif entity.IsAvatarReplica:
        return gameconst.RaceTypeEnum.avatarReplica

    else:
        return gameconst.RaceTypeEnum.none


def _entIsAll(src, e, *args):
    return e is not None


def _entIsEnemy(src, e, *args):
    return isEnemy(src, e)


def _entIsFriend(src, e, *args):
    return isFriend(src, e)


def _entIsSelf(src, e, *args):
    return src.id == e.id


def _entIsCreationMaster(src, e, *args):
    return src.IsCreation and src.hostId == e.id


def _entIsEnemyExTarget(src, e, tgt):
    return e.id != tgt.id and isEnemy(src, e)


def _entIsCacheEnemy(src, e, *args):
    return True


def _entIsCacheFriend(src, e, *args):
    return True


def _entIsCacheEnemyExTarget(src, e, tgt):
    return e.id != tgt.id

def _entIsTeam(src, e, tgt):
    # 不包括自己
    if src.id == tgt.id:
        return False

    src = getEntityRealEntity(src)
    if src.id == tgt.id:
        return True

    if not (src.isReal() and tgt.isReal()):
        return False

    if src.IsAvatar and tgt.IsAvatar:
        if isEnemy(src, tgt):
            return False

        if src.teamId != 0 and src.teamId == tgt.teamId:
            return True

    return False

def _entIsRaid(src, e, tgt):
    # 不包括自己
    if src.id == tgt.id:
        return False

    src = getEntityRealEntity(src)
    if src.id == tgt.id:
        return True

    if not (src.isReal() and tgt.isReal()):
        return False

    if src.IsAvatar and tgt.IsAvatar:
        if isEnemy(src, tgt):
            return False

        if src.raidId != 0 and src.raidId == tgt.raidId:
            return True

    return False

def _entIsSelfCamp(src, e, tgt):
    # 包括自己
    if src.id == tgt.id:
        return True

    src = getEntityRealEntity(src)
    if src.id == tgt.id:
        return True
    
    if not (src.isReal() and tgt.isReal()):
        return False
    
    return False

TEAM_TARGET_FUNC_MAP = {
    gameconst.TeamCampType.Self: _entIsSelfCamp,
    gameconst.TeamCampType.Team: _entIsTeam,
    gameconst.TeamCampType.Raid: _entIsRaid,
}

TARGET_FUNC_MAP = {gameconst.CampType.All: _entIsAll,
                   gameconst.CampType.Enemy: _entIsEnemy,
                   gameconst.CampType.Friend: _entIsFriend,
                   gameconst.CampType.Self: _entIsSelf,
                   gameconst.CampType.CreationMaster: _entIsCreationMaster,
                   gameconst.CampType.EnemyExTarget: _entIsEnemyExTarget,
                   gameconst.CampType.Team: _entIsTeam}

CACHE_TARGET_FUNC_MAP = {gameconst.CampType.All: _entIsAll,
                         gameconst.CampType.Enemy: _entIsCacheEnemy,
                         gameconst.CampType.Friend: _entIsCacheFriend,
                         gameconst.CampType.Self: _entIsSelf,
                         gameconst.CampType.CreationMaster: _entIsCreationMaster,
                         gameconst.CampType.EnemyExTarget: _entIsCacheEnemyExTarget,
                         gameconst.CampType.Team: _entIsTeam}


@functools.lru_cache(16)
def getFightTargetTypeFromCfgData(typeName):
    return FPFTTD.datas.get(typeName, {}).get('value')


def checkTargetTypeValid(typeName, src, e, tgt=None):
    if typeName == 'Any' or typeName == 'None':
        return True

    if not tgt:
        tgt = e

    if not e.canAttackable(src):
        return False
    _value = getFightTargetTypeFromCfgData(typeName)
    if not _value or len(_value) < 3:
        LOG_ERR('checkTargetTypeValid err in fightProp_fightTargetType', typeName)
        return False

    for targetType in _value[2]:
        if TARGET_FUNC_MAP[targetType](src, e, tgt):
            break
    else:
        return False
    
    if len(_value) > 3:
        for targetType in _value[3]:
            func = TEAM_TARGET_FUNC_MAP.get(targetType, None)
            if not func or func(src, e, tgt):
                break
        else:
            return False

    if 1 in _value[1] and not e.isDie():
        return False
    if 2 in _value[1] and e.isDie():
        return False

    if 0 not in _value[0] and getRaceTypeEnum(e) not in _value[0]:
        return False

    return True


# 可能涉及三方关系，所以可能需要三个entity参数，例如选择敌人周围的敌人
def checkCachedTargetType(typeName, src, e, tgt=None):
    if typeName == 'Any' or typeName == 'None':
        return True

    if not tgt:
        tgt = e

    if not e.canAttackable(src):
        return False

    _value = getFightTargetTypeFromCfgData(typeName)
    if not _value or len(_value) < 3:
        LOG_ERR('checkTargetTypeValid err in fightProp_fightTargetType', typeName)
        return False

    for targetType in _value[2]:
        if CACHE_TARGET_FUNC_MAP[targetType](src, e, tgt):
            break
    else:
        return False

    if len(_value) > 3:
        for targetType in _value[3]:
            func = TEAM_TARGET_FUNC_MAP.get(targetType, None)
            if not func or func(src, e, tgt):
                break
        else:
            return False

    if 1 in _value[1] and not e.isDie():
        return False
    if 2 in _value[1] and e.isDie():
        return False

    if 0 not in _value[0] and getRaceTypeEnum(e) not in _value[0]:
        return False

    return True

@functools.lru_cache(1024, typed=False)
def hasSkillTagById(skillId, tag):
    _tags = combatSkill.SkillBaseClass.getTag(skillId)
    if not _tags:
        return False

    if tag in _tags:
        return True
    return False

def doInitBaseProperties(entity, propCurveId=0):
    if not propCurveId:
        propCurveId = entity.getCreepData().get('propCurveID')

    if not propCurveId:
        raise RuntimeError('creep base entity must set propCurveId, {} spaceNo:{}, gid:{}'.format(
            entity.creepbaseId, entity.spaceNo, entity.gameEntityId))

    import prop_fightprop as PFPD
    import creep_base as CBD

    creepData = CBD.datas.get(entity.creepbaseId)
    propId = creepData.get('propID')
    if propId:
        propType = creepData.get('propType')
        if propType == 1:
           propId = propId + entity.level - 1
        elif propType == 2:
            if formula.inSiegeWarScene(entity.spaceNo):
                if entity.siegeWarMonsterPropId:
                    propId = entity.siegeWarMonsterPropId
            if formula.inMineWarScene(entity.spaceNo):
                if entity.junxuPropId:
                    propId = entity.junxuPropId

        propData = PFPD.datas.get(propId)
        cfgPropType = propData.get('type')
        if propType != cfgPropType:
            LOG_ERR('doInitBaseProperties propType error', entity.creepbaseId, propType, cfgPropType)
            return

        _coefficientType = creepData['coefficientType']
        _coefficientDic = C_CD.datas.get(_coefficientType, {})

        propList = propData.get('propList')
        for prop, val in propList.items():
            _oldVal = getattr(entity, prop)
            _func = type(_oldVal)
            setattr(entity, prop, _func(val * _coefficientDic.get(prop, 1)))

    entity.baseSpeed = float(entity.getCreepData().get('baseSpeed', 0))
    entity.baseStateRate = entity.getCreepData().get('baseStateRate', 0.0)

    entity.speedStateRatio = gameconst.SpeedState.Normal

def fetchSpaceEnterSceneBySpaceNo(crtSpaceNo, enterSpaceNo, default=gameconst.SpaceEnterScene.DENY):
    _crtSpaceType = GPGP.datas.get(
        formula.parseDungeonNoBySpaceNo(crtSpaceNo), {}).get(
            'sceneType', 0)
    _enterSpaceType = GPGP.datas.get(
        formula.parseDungeonNoBySpaceNo(enterSpaceNo), {}).get(
            'sceneType', 0)
    return fetchSpaceEnterScene(_crtSpaceType, _enterSpaceType, default)


def isComplexTeleportAllowed(fromSpaceNo, toSpaceNo):
    r = fetchSpaceEnterSceneBySpaceNo(fromSpaceNo, toSpaceNo)
    if r == gameconst.SpaceEnterScene.DENY:
        return False
    return True


def getTeleporterByID(teleportId, spaceNo):
    telIds = gameglobal.teleporterGIDToEntIdMap\
        .get(spaceNo, {})\
        .get(teleportId, None)

    if telIds is not None:
        return KBEngine.entities.get(telIds[0], None)

    return None


def checkComplexTeleportNeedCast(fromSpaceNo, toSpaceNo, teleportType, src, owner):
    if owner.isDie():
        return False

    if fromSpaceNo == toSpaceNo:
        return False

    if teleportType == gameconst.ComplexTeleportEnum.LEAVE and formula.inDungeonScene(fromSpaceNo):
        return False

    r = fetchSpaceEnterSceneBySpaceNo(fromSpaceNo, toSpaceNo)
    if r == gameconst.SpaceEnterScene.ALLOW_CAST:
        return True

    return False

def getLineTypeFromCfgGameEntityId(cfgGameEntityId):
    return cfgGameEntityId // 10000

def getMoralLevel(moralValue):
    for k, v in PKMVE.datas.items():
        if moralValue >= v['lowerLimit'] and moralValue <= v['upperLimit']:
            LOG_DBG('getMoralLevel, level:', k, 'moralValue:', moralValue)
            return k
    LOG_WARN('getMoralLevel, level not found:', moralValue)
    return 0

def getWorldLevelRatio(playerLevel, worldLevelDelta, src):
    worldLevelRatio = 1.0
    if getSvrOpenDays() < EC.datas["activateWorldLevel"]["value"] or src not in EC.datas["bonus_EXP_Sources"]["value"] \
        or worldLevelDelta <= 0 or playerLevel < V_VD.datas["worldLevel"]["level"] or gameconfig.isCrossServer():
        worldLevelRatio = 1.0
    else:
        for i in range(1, EGM.maxKey+1):
            if worldLevelDelta <= EGM.datas[i]['levelDifference']:
                worldLevelRatio = 1.0 + EGM.datas[i]['multiplier']
                break
    return worldLevelRatio

def getExpDecayRate(level, playerLevel, worldLevelDelta, src):
    LOG_INFO("getExpDecayRate", level, playerLevel, worldLevelDelta, src)

    datas = PKMVE.datas.get(level, None)
    if datas:
        worldLevelRatio = getWorldLevelRatio(playerLevel, worldLevelDelta, src)
        expRate = 1 - datas['ExpGainReduced']
        expRate *= worldLevelRatio
        LOG_INFO('getExpDecayRate, level:', level, 'rate:', expRate, 'worldLevelRatio:', worldLevelRatio)
        return expRate
    else:
        LOG_WARN('getExpDecayRate, level not found:', level)
        return 1.0

def getTeamExpBonus(teammateNum):
    if teammateNum < 1:
        return 0
    teamExpBonus = TMMCD.datas['teamExperienceBonus']['value']
    return teamExpBonus[teammateNum-1]

def buildChatChannelAvatarData(entityId, playerGBID, school, name, level, sex, picFrameId, *args):
    return {
        'id': entityId,
        'sex': sex,
        'name': name,
        'gbId': playerGBID,
        'level': level,
        'school': school,
        'picFrameId': picFrameId
    }

def getConfirmMsgCooldown(mid, default=-1):
    _messageData = M_MD.datas.get(mid, {})
    _to1 = _messageData.get('minDisplayTime', 0)
    if _to1 > 0:
        return _to1

    if _messageData['DisplayMode'] in gameconst.MessageType.COLL_BUTTON_MESSAGE:
        _to2 = _messageData.get('defaultCountdown', 0)
        if _to2 > 0:
            return _to2

    return default

def getDisSquare(pos1, pos2):
    return (pos1[0] - pos2[0]) ** 2 + (pos1[2] - pos2[2]) ** 2


def getTranslatedMsgId(msgId):
    msgId |= (1 << 30)
    return msgId

def getTranslatedArg(arg):
    return '^{}'.format(arg)


def binarySearchFirstGreater(arr, tgt):
    left, right = 0, len(arr) - 1

    while left <= right:
        mid = (left + right) // 2
        val = arr[mid]

        if val <= tgt:
            left = mid + 1
        else:
            right = mid - 1

    return left


def isActOpen(actId):
    return actId in gameglobal.globalActData


def checkCanChangeSceneAndShowMsg(avatar, fromSpaceNo, toSpaceNo):
    LOG_DBG('checkCanChangeSceneAndShowMsg 0 ', fromSpaceNo, toSpaceNo)
    # 1. 任何一个副本可以进组队副本，团队副本除外
    isRaidFromSpace = formula.inRaidDungeonScene(fromSpaceNo)
    isTeamToSpace = formula.inTeamDungeonScene(toSpaceNo)
    LOG_DBG('checkCanChangeSceneAndShowMsg 1 ', fromSpaceNo, toSpaceNo)
    if isRaidFromSpace and isTeamToSpace:
        return False
    if isTeamToSpace:
        return True

    # 2. 任何一个副本可以进团队副本，组队副本除外
    isTeamFromSpace = formula.inTeamDungeonScene(fromSpaceNo)
    isRaidToSpace = formula.inRaidDungeonScene(toSpaceNo)
    LOG_DBG('checkCanChangeSceneAndShowMsg 2 ', fromSpaceNo, toSpaceNo)
    if isTeamFromSpace and isRaidToSpace:
        return False
    if isRaidToSpace:
        return True

    # 进跨服
    if fromSpaceNo == 0 and gameconfig.isCrossServer():
        return True


    _fromMapId = formula.fetchMapId(fromSpaceNo)
    _toMapId = formula.fetchMapId(toSpaceNo)

    # 相同地图不同分线
    if _fromMapId == _toMapId:
        return True

    _fromSceneType = GPGP.datas[_fromMapId]['sceneType']
    _toSceneType = GPGP.datas[_toMapId]['sceneType']

    if not GPES.datas[_fromSceneType][str(_toSceneType)]:
        avatar.showMsg(CCT.datas['leaveTheScene']['value'], [])
        return False

    return True

def getSkillLvParam(skillId):
    return combatSkill.SkillBaseClass.getSkillLvParam(skillId)

def checkDrawCardPoolTimeLimit(curTimestamp, checkType):
    poolsInfo = {}
    if checkType == gameconst.DrawCardPoolMacro.CHECK_TIME_LIMIT_TYPE_LOGIN:
        poolsInfo = copy.deepcopy(gameglobal.expiredDrawCardPoolCache)
    elif checkType == gameconst.DrawCardPoolMacro.CHECK_TIME_LIMIT_TYPE_TIMER:
        for pool, poolData in GGP.datas.items():
            if pool in gameglobal.expiredDrawCardPoolCache:
                continue
            if not poolData.get('timeLimit', 0):
                continue
            startTimestamp = getIntTimestamp(poolData['startTime'])
            endTimestamp = getIntTimestamp(poolData['endTime'])
            #LOG_DBG('poolData id:%i, groupId:%i, timeLimit:%i, startTime:%s(%i), endTime:%s(%i)' %
            #            (pool, poolData['poolGroupId'],  poolData['timeLimit'],
            #            getNowTimeStr(startTimestamp), startTimestamp,
            #            getNowTimeStr(endTimestamp), endTimestamp))
            if not startTimestamp and not endTimestamp:
                #LOG_DBG('checkDrawCardPoolTimeLimit not TimeLimit', curTimestamp, pool, endTimestamp)
                continue
            if startTimestamp <= curTimestamp and curTimestamp <= endTimestamp:
                #LOG_DBG('checkDrawCardPoolTimeLimit in TimeLimit', curTimestamp, pool, endTimestamp)
                continue

            if startTimestamp > curTimestamp:
                #LOG_DBG('checkDrawCardPoolTimeLimit before TimeLimit', curTimestamp, pool, endTimestamp)
                continue

            LOG_INFO('checkDrawCardPoolTimeLimit after TimeLimit', curTimestamp, pool, endTimestamp)
            poolsInfo[pool] = endTimestamp

        gameglobal.expiredDrawCardPoolCache.update(poolsInfo)
    #LOG_DBG('checkDrawCardPoolTimeLimit', curTimestamp, poolsInfo, gameglobal.expiredDrawCardPoolCache, checkType)
    return poolsInfo

def getSiegeWarFirstTimeInfo():
    firstTime = 0
    firstTimeValid = False
    if not gameconfig.serverId() in gameglobal.mapleServerInfo:
        LOG_WARN('[lj]get siege war first time info, server id not found:', gameconfig.serverId())
        return firstTime, firstTimeValid, 0
    crossServerGroupID = gameglobal.mapleServerInfo[gameconfig.serverId()]['server_group']
    GroupServerList = utils.group2ServerIds(crossServerGroupID)
    GroupServerOpenTimes = []
    lastestOpenTime = 0 #group内开服最晚时间
    for serverID in GroupServerList:
        _openTime = int(gameglobal.mapleServerInfo[int(serverID)]['start_time'])
        GroupServerOpenTimes.append(int(_openTime))
        if _openTime > lastestOpenTime:
            lastestOpenTime = _openTime

    if CBFT.datas.get(crossServerGroupID, None) is None:
        LOG_ERR('[lj]cross siege war start time not found group id:', crossServerGroupID)
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
        LOG_WARN('[lj]first time config warning, first time:', time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(firstTime)), 'limit time:', time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(limitTime)))
        firstTimeValid = False
    else:
        firstTimeValid = True

    return firstTime, firstTimeValid, limitTime


def getSiegeWarMonthlyStartTime(monthAdd):
    now = curTS()
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
    now = curTS()

    for i in (-1, 0, 1):
        t = getSiegeWarMonthlyStartTime(i) + addTime
        if now < t:
            return t
    LOG_ERR('[lj]getNextSiegeWarMonthlyExpireTime failed, now:', now, 'addTime:', addTime)
    return getSiegeWarMonthlyStartTime(1) + addTime

def getNextBiddingStartTime():
    now = curTS()
    firstTime, firstTimeValid, limitTime = getSiegeWarFirstTimeInfo()
    if firstTimeValid and now < firstTime:
        return firstTime

    if now < getSiegeWarMonthlyStartTime(0):
        return getSiegeWarMonthlyStartTime(0)

    return getSiegeWarMonthlyStartTime(1)

def getSiegeWarBiddingEndTime():
    if gameglobal.globalSiegeWarData.get('expireTime', None) is not None:
        if curTS() < gameglobal.globalSiegeWarData['expireTime']:
            return gameglobal.globalSiegeWarData['expireTime']

    firstTime, firstTimeValid, limitTime = getSiegeWarFirstTimeInfo()
    addTime = CBC.datas['cityBattle_biddingTime']['value'] * 24 * 60 * 60 + CBC.datas['cityBattle_biddingDelayed']['value'][2] * 60 + CBC.datas['cityBattle_BiddingEndTime']['value'] * 60 * 60
    if firstTimeValid:
        expireTime = firstTime + addTime
        if curTS() < expireTime:
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
    if curTS() < biddingStartTime:
        return 0
    return t

def getGuildRelation(guildUUID1, guildUUID2):
    _pair = getGuildUUIDPair(guildUUID1, guildUUID2)
    return gameglobal.guildRelationDic.get(_pair, gameconst.GuildRelationType.NONE)

def getCustomIdAndGid(spaceNo, gameEntityId):
    _mapId = formula.fetchMapId(spaceNo)
    _dunData = getDunModuleData(_mapId)
    if not _dunData:
        LOG_ERR("[lj]getSiegeWarEntityCustomId: _dunData is None")
        return None, None

    gid, gct = splitFromGameEntityId(gameEntityId)
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

def getForceComponentID(accountName):
    _cache = gameglobal.accountCompIdCache.get(accountName)
    if not _cache:
        return 0

    if curTS() > _cache[0]:
        return 0

    return _cache[1]

def loadLineReadyEntities(spaceNo, entityIDs, readyEntitiesList, isRefresh = False):
    if not entityIDs:
        return

    RandomRegionAtLeastInfo = {}
    for gameEntityId in entityIDs:
        gid, gct = splitFromGameEntityId(gameEntityId)
        datas = getDunModuleData(formula.fetchMapId(spaceNo))

        if str(gid) not in datas:
            continue

        _mPrm = datas[str(gid)]
        className = _mPrm['ClassName']
        _bornPosition = (_mPrm['PosX'], _mPrm['PosY'], _mPrm['PosZ'])

        if 'Dir' in _mPrm:
            _bornDirection = (0.0, 0.0, _mPrm['Dir'] * math.pi / 180)
        else:
            _bornDirection = gameconst.DEFAULT_DIRECTION

        _tmpProps = {'createIndex': gct}

        _params = {
            'spaceNo': spaceNo,
            'spaceno': spaceNo,
            'gameEntityId': gameEntityId,
            'direction': _bornDirection,
            'position': _bornPosition,
            'tmpProps': _tmpProps,
        }

        if 'Props' in _mPrm:
            _pP = _mPrm['Props']
            # 非刷新情况下
            if not isRefresh:
                # 初始不加载
                initLoad = _pP.get('InitLoad', None)
                if initLoad is not None and initLoad == 0:
                    continue

            if 'liveTimer' in _pP:
                _params['liveTime'] = _pP['liveTimer']

            if 'Radius' in _pP:
                radius = _params['bornRadius'] = float(_pP['Radius'])
                _tmpProps['createRadius'] = radius

            if 'RefreshNum' in _pP:
                count = int(_pP['RefreshNum'])
                _tmpProps['createCount'] = count

                if count > 1000:
                    raise TypeError('Monster count must lower than 1000')

            if 'RefreshTime' in _pP:
                #刷新时间为列表时随机时间
                refreshTime = _pP['RefreshTime']
                if type(refreshTime) is list:
                    if len(refreshTime) == 1:
                        _params['refreshTime'] = int(int(refreshTime[0]))
                    else:
                        _params['refreshTime'] = int(random.randint(int(refreshTime[0]), int(refreshTime[1])))
                else:
                    _params['refreshTime'] = int(_pP['RefreshTime'])

            if 'PathID' in _pP and _pP['PathID']:
                _params['pathId'] = int(_pP['PathID'])

            if 'Level' in _pP:
                _params['level'] = int(_pP['Level'])

            if 'RandomRegion' in _pP \
                    and not (_pP.get('IsForSkill', 0) \
                             or _mPrm.get('CustomID') == gameconst.DunCustomId.POS_FOR_SKILL):
                #存在随机区域，则改变出生位置
                randomRegion = _pP['RandomRegion']

                _bornPosition = getRandomPositionFromMultiRegion(randomRegion, entityIDs, gid, RandomRegionAtLeastInfo)
                _params.update({
                    'position': _bornPosition,
                })

            if 'LightPillar' in _pP:
                if _pP['LightPillar']:
                    _params.update({
                        'lightPillar': int(_pP['LightPillar']),
                    })

            if 'IsOnGround' in _pP:
                _params['isOnGround'] = bool(_pP['IsOnGround'])

            if 'MapEntityType' in _pP:
                _params['mapEntityType'] = int(_pP['MapEntityType'])

        if className == 'Monster':
            _monsterId = int(_mPrm['EntityID'])
            if not _monsterId:
                LOG_ERR('策划记得把这个monsterId配置上', gameEntityId)
                continue

            if formula.fetchMapId(spaceNo) in B_BD.datas:
                lineNo = formula.parseLineNo(spaceNo)
                nameSuffixID = -1
                if _monsterId in CBD.datas:
                    nameSuffixID = CBD.datas[_monsterId]['nameSuffixID']

                if nameSuffixID in BDS.datas["Branch_creepNotRefresh"]["value"] and lineNo != 0 and lineNo != -1:
                    LOG_DBG("skip create monster", spaceNo, _monsterId, nameSuffixID, lineNo)
                    continue
            
            _params.update({
                'monsterId': _monsterId,
                'name': _mPrm['DisplayName'],
                'instanceId': _mPrm['ID'],
            })

        elif className == 'Teleporter':
            teleporterId = _mPrm['EntityID']
            _params.update({
                'name': _mPrm['DisplayName'],
                'teleporterId': teleporterId,
                'teleportType': _mPrm.get('Props', {}).get('GateType', 0),
            })

        elif className == 'Npc':
            _isOpen = _mPrm.get('Props', {}).get('IsOpen', 1)
            if not _isOpen:
                continue

            _npcId = _mPrm['EntityID']
            if not _npcId:
                LOG_ERR('快联系策划，这个npc没有配置EntityID :', gameEntityId)
                continue

            _params.update({
                'npcId': _npcId,
                'name': _mPrm['DisplayName'],
            })

        elif className == 'Collection':
            _isOpen = _mPrm.get('Props', {}).get('IsOpen', 1)
            if not _isOpen:
                continue

            collectionId = _mPrm['EntityID']
            collectionType = NPD.datas.get(collectionId, {}).get('type', gameconst.CollectionType.NORMAL)
            _params.update({
                'name': _mPrm['DisplayName'],
                'collectionId': collectionId,
                'type': collectionType,
            })
        elif className == 'MonsterGrp':
            _groupId = _mPrm['EntityID']
            _params.update({
                'name': _mPrm['DisplayName'],
                'groupId': _groupId,
            })
            radius = _mPrm.get('Props', {}).get('Radius', 0)
            if radius:
                _params['bornRadius'] = radius
        elif className in ('Barrier', 'AirWall'):
            className = 'Barrier'
            _barrierId = _mPrm['ID']
            _params.update({
                'name': _mPrm['DisplayName'],
                'barrierId': _barrierId,
            })
        elif className == 'CityBattleTeleporter':
            teleporterId = _mPrm['EntityID']
            _params.update({
                'name': _mPrm['DisplayName'],
                'teleporterId': teleporterId,
                'cbID': _mPrm['ID'],
            })
        elif className == 'Creation':
            #Gm控制是否创建创生物
            if not gameconfig.loadCreation():
                continue
            _creationId = _mPrm['EntityID']
            _params.update({
                'creationId': _creationId,
            })
        elif className == 'RebornPos':
            _RebornPosId = _mPrm['EntityID']
            _params.update({
                'name': _mPrm['DisplayName'],
                'rebornPosId': _RebornPosId,
            })

        else:
            LOG_WARN('could not create entity type', className)
            continue

        needCreateBase = 0
        data = (gameEntityId, spaceNo, className, needCreateBase, _bornPosition, _bornDirection, _params, 0)
        LOG_DBG("loadLineEntities for single ", spaceNo, className, gameEntityId)
        readyEntitiesList.append(data)


def isBelongTimerTag(timerTag):
    return gametimer.TIMER_TAG_START <= timerTag < gametimer.TIMER_TAG_END

def isBelongTimerIdTag(timerIdTag):
    return gametimer.TIMER_ID_START <= timerIdTag < gametimer.TIMER_ID_END


def getCollisionDistance(creepbaseId, default=0):
    return CBD.datas[creepbaseId].get('collisionDistance', default)

def getMarkLimit():
    limitConf = CCT.datas['teamMarkLimit']['value']
    return gameconst.MARK_OTHER_MAX_NUM if limitConf < gameconst.MARK_OTHER_MAX_NUM else limitConf


def getTimeZoneOffset():
    now = datetime.datetime.now().astimezone()
    offset = now.utcoffset()
    return offset.total_seconds() /3600

def checkInCombatArea(monsterID, srcPos, propsData):
    areaCentralPosition = propsData[0]
    areaCentralRotation = propsData[1]
    areaType = propsData[2]
    if areaType == gameconst.DungeonCustomAreaType.CIRCLE:
        radius = propsData[3]
        return calculatePointIn2DCircle(monsterID, srcPos[0], srcPos[2], areaCentralPosition[0], areaCentralPosition[2], radius)
    elif areaType == gameconst.DungeonCustomAreaType.RECTANGLE:
        length = propsData[3]
        width = propsData[4]
        return calculatePointIn2DRectangle(monsterID, srcPos[0], srcPos[2], areaCentralPosition[0], areaCentralPosition[2], length, width, areaCentralRotation)
    return True

def calculatePointIn2DCircle(monsterID, x, z, x1, z1, r, precision=1e-10):
    dx = x-x1
    dz = z-z1
    r1 = (dx *dx + dz * dz)
    r2 = (r * r - precision)
    LOG_DBG("calculatePointIn2DCircle ", monsterID, x, z, x1, z1, r, precision, r1, r2)
    return r1 < r2

def calculatePointIn2DRectangle(monsterID, x, z, x1, z1, l, w, t, precision=1e-10):
    dx = x - x1
    dz = z - z1

    cos_angle = math.cos(-t)
    sin_angle = math.sin(-t)
    rotated_x = dx * cos_angle - dz * sin_angle
    rotated_z = dx * sin_angle + dz * cos_angle

    half_length = l / 2.0 - precision
    half_width = w / 2.0 - precision

    absX = abs(rotated_x)
    absZ = abs(rotated_z)
    LOG_DBG("calculatePointIn2DRectangle ", monsterID, x, z, x1, z1, l, w, t, precision, absX, absZ, half_length, half_width)
    return absX < half_length and absZ < half_width

@functools.lru_cache(maxsize=256)
def getInscriptionKey(skillId, inscriptionType):
    return skillId * 100 * 1000 + inscriptionType

@functools.lru_cache(maxsize=256)
def splitInscriptionKey(dataKey):
    skillId = dataKey // (1000 * 100)
    inscriptionType = dataKey - skillId * 1000 * 100
    return skillId, inscriptionType


@functools.lru_cache(maxsize=256)
def group2ServerIds(groupId):
    _serverIds = []
    for _serverId, _data in gameglobal.mapleServerInfo.items():
        _grp = _data['server_group']
        if _grp == groupId:
            _serverIds.append(_serverId)

    return _serverIds

def getMineWarStartOffsetSec():
    warStartWeekDay = MBC.datas['mineBattle_startTime']['value'][0]  # 每周几
    warStartHour = MBC.datas['mineBattle_startTime']['value'][1]  // 100   # 几点开始
    warStartMin = MBC.datas['mineBattle_startTime']['value'][1]  % 100    # 几分开始
    offset = ((warStartWeekDay - 1) * 24 + warStartHour) * 3600 + warStartMin * 60
    return offset

def getMineWarEndOffsetSec():
    warStartWeekDay = MBC.datas['mineBattle_startTime']['value'][0]  # 每周几
    warEndHour = MBC.datas['mineBattle_startTime']['value'][2]  // 100   # 几点结束
    warEndMin = MBC.datas['mineBattle_startTime']['value'][2]  % 100    # 几分结束
    offset = ((warStartWeekDay - 1) * 24 + warEndHour) * 3600 + warEndMin * 60
    return offset

def getMineWarPrepareNeedSec():
    return MBC.datas['mineBattle_interfacePromptTime']['value'] * 60    # 准备时间需要提前多少时间

def getNextHoursTimestamp(curTimestamp):
    m = datetime.datetime.fromtimestamp(curTimestamp).minute
    s = datetime.datetime.fromtimestamp(curTimestamp).second
    if (m == 0 or m == 30) and s == 0:
        return curTimestamp
    if m < 30:
        return (curTimestamp//3600+0.5)*3600
    return (curTimestamp//3600+1)*3600


def callLimitAdd(callType):
    _ts, _times = gameglobal.callLimitDic.get(callType, (0, 0))
    _now = curTS()
    if _ts == _now:
        gameglobal.callLimitDic[callType] = (_now, _times+1)
    else:
        gameglobal.callLimitDic[callType] = (_now, 1)


def getCallLimitNum(callType):
    _ts, _times = gameglobal.callLimitDic.get(callType, (0, 0))
    _now = curTS()
    if _ts == _now:
        return _times
    else:
        return 0

def getCrtMapNeedStatisticFlag(spaceNo):
    mapId = formula.fetchMapId(spaceNo)
    mapData = GPGP.datas.get(mapId, {})
    return mapData.get('dpsActive', 0) == 1


def isAttackArea(tgt, center, radius):
    if tgt.IsMonster:
        radius += tgt.getCreepData().get('attackDistanceCompensation', 0)

    distance = sMath.distance2DToCompareFrom3DPosition(tgt.position, center)
    return distance <= radius * radius

def isMinorAccount(userAge):
    adultAge = AASC.datas.get('userAge', {}).get('value', gameconst.LEGAL_AGE_OF_MAJORITY)
    return userAge < adultAge

def sizeof(obj, seen=None):
    if seen is None:
        seen = set()
    obj_id = id(obj)
    if obj_id in seen:
        return 0
    seen.add(obj_id)
    size = sys.getsizeof(obj)
    try:
        if hasattr(obj, '__dict__'):
            for k, v in obj.__dict__.items():
                size += sizeof(k, seen)
                size += sizeof(v, seen)
        if hasattr(obj, '__slots__'):
            if not isinstance(obj.__slots__, int):
                for slot in obj.__slots__:
                    if hasattr(obj, slot):
                        size += sizeof(getattr(obj, slot), seen)
        if isinstance(obj, dict):
            for k, v in list(obj.items()):
                size += sizeof(k, seen)
                size += sizeof(v, seen)
        elif isinstance(obj, (list, tuple, set)):
            for item in list(obj):
                size += sizeof(item, seen)
        elif isinstance(obj, (ModuleType, FunctionType)):
            return 0
    except ModuleNotFoundError as e:
        pass
    return size


def printMemUsage(memList, sumSet, warnLow):
    _sumSize = 0
    _cnt = 0
    for i, val in enumerate(memList):
        _size = sizeof(val, sumSet)
        _sumSize += _size
        if _size > warnLow:
            LOG_WARN('[memDebug]mem beyond warnLow', i, _size)
        _cnt += 1

        yield True

    LOG_WARN('[memDebug]sum size is ', _sumSize, _cnt)


def _debugMemOnce(memIter, batchNum, *args):
    for i in range(batchNum):
        _next = next(memIter, None)
        if _next is None:
            return

    KBEngine.addTimer(1, 0, functools.partial(_debugMemOnce, memIter, batchNum))

def debugMemUsage(memList, sumSet, warnLow, batchNum):
    LOG_WARN('[memDebug]sum len is ', len(memList))
    _iter = printMemUsage(memList, sumSet, warnLow)
    _debugMemOnce(_iter, batchNum)


def emptyFunc(*args, **kwargs):
    pass

def checkPosValid(pos):
    if not pos:
        return False

    if pos[0] is None:
        return False

    if pos[1] is None:
        return False

    if pos[2] is None:
        return False

    return True


def isInAttackLine(targetPos, vCenter, direction, length, width, fixCenter=False):
    """
    :param fixCenter: 是否修正中心点坐标
    """
    # 1. 归一化方向向量（如果能保证传入时已归一化，可省略）
    direction.normalise()
    
    # 2. 获取目标相对于攻击中心的偏移向量 (2D 空间：x, z)
    if fixCenter:
        dx = targetPos.x - (vCenter.x + direction.x * length / 2)
        dz = targetPos.z - (vCenter.z + direction.z * length / 2)
    else:
        dx = targetPos.x - vCenter.x
        dz = targetPos.z - vCenter.z
    
    # 3. 计算目标在方向向量上的投影长度（点积）
    # 假设方向向量 D = (dirX, dirZ)
    dirX, dirZ = direction.x, direction.z
    
    # 目标在攻击方向上的偏移 (Forward offset)
    # 利用点积公式：proj_L = v · dir
    projL = dx * dirX + dz * dirZ
    
    # 4. 快速范围判断
    halfLen = length / 2
    if projL > halfLen or projL < -halfLen:
        return False
        
    # 5. 计算目标在垂直方向上的偏移 (Side offset)
    # 垂直向量为 (-dirZ, dirX)
    projW = dx * (-dirZ) + dz * dirX
    
    halfWid = width / 2
    if projW > halfWid or projW < -halfWid:
        return False
        
    return True


def itemListToBriefList(itemList):
    _dic = {}
    for it in itemList:
        _key = (it.itemId, it.bindType)
        _dic[_key] = _dic.get(_key, 0) + it.itemNum

    _result = []
    for k, v in _dic.items():
        _result.append(
            {
                'itemId': k[0],
                'bindType': k[1],
                'itemNum': v,
            }
        )

    return _result


def isInAttackLineWithRadius(targetPos, startPos, direction, length, width, targetRadius):
    """
    判断目标是否在矩形攻击范围内（支持目标半径）
    :param targetPos: 目标位置 (Math.Vector3)
    :param startPos: 攻击起始位置 (Math.Vector3)
    :param direction: 攻击方向 (Math.Vector3)，内部会归一化
    :param length: 矩形长度
    :param width: 矩形宽度
    :param targetRadius: 目标半径（用于碰撞检测）
    :return: bool
    """
    # 1. 归一化方向向量
    dirMagnitude = math.sqrt(direction.x * direction.x + direction.z * direction.z)
    if dirMagnitude <= 0.000001:
        # 方向向量无效，无法确定矩形方向
        unitDirX = 0.0
        unitDirZ = 0.0
    else:
        unitDirX = direction.x / dirMagnitude
        unitDirZ = direction.z / dirMagnitude

    # 2. 计算目标相对于起始点的向量
    dx = targetPos.x - startPos.x
    dz = targetPos.z - startPos.z

    # 3. 计算目标在攻击方向上的投影长度 (Forward offset)
    # projL = v · dir
    projL = dx * unitDirX + dz * unitDirZ

    # 4. 计算目标在垂直方向上的投影长度 (Side offset)
    # 垂直向量为 (-unitDirZ, unitDirX)
    # projW = v · perpDir
    projW = dx * (-unitDirZ) + dz * unitDirX

    # 5. 核心判断逻辑
    
    # 矩形半宽
    halfWidth = width / 2.0

    # 情况 A: 目标半径为 0 (纯点与矩形检测)
    if targetRadius <= 0:
        if projL < 0 or projL > length:
            return False
        if projW < -halfWidth or projW > halfWidth:
            return False
        return True

    # 情况 B: 目标有半径 (圆与矩形检测)
    # 将问题转化为：点 (projL, projW) 到矩形 (0, -halfWidth) -> (length, halfWidth) 的距离 <= targetRadius

    # Clamped Point (矩形内离目标最近的点)
    # clamp projL to [0, length]
    closestL = projL
    if closestL < 0:
        closestL = 0
    elif closestL > length:
        closestL = length

    # clamp projW to [-halfWidth, halfWidth]
    closestW = projW
    if closestW < -halfWidth:
        closestW = -halfWidth
    elif closestW > halfWidth:
        closestW = halfWidth

    # 计算目标点到最近点的距离平方
    diffL = projL - closestL
    diffW = projW - closestW
    distSq = diffL * diffL + diffW * diffW

    return distSq <= (targetRadius * targetRadius)

# 事件订阅，任意组件的实体都可以使用
# 注意：
#   1. avatar的cell上不要使用，传送时可能跨进程，导致数据同步问题
#   2. 如果在avatar(base)等动态创建的entity上使用，务必在destroy时调用 unsubscribe
#   3. 由于是跨进程调用，注意确认下时序问题
def subscribe(tag, box, func):
    if IS_BASE:
        gameengine.callBaseApps(
            'gameengine.subscribeEvent',
            (tag, box.id, func),
        )
    else:
        # avatar 的cell上不要使用
        if box and box.IsAvatar:
            LOG_ERR('subscribe event failed, avatar in cell  cannot use:', box, tag)
            return
        gameengine.callCellApps(
            'gameengine.subscribeEvent',
            (tag, box.id, func),
        )
def unsubscribe(tag, box):
    if IS_BASE:
        gameengine.callBaseApps(
            'gameengine.unsubscribeEvent',
            (tag, box.id),
        )
    else:
        gameengine.callCellApps(
            'gameengine.unsubscribeEvent',
            (tag, box.id),
        )
        
# 分发事件，任意组件的实体都可以使用
# 注意：
#   1. 不要传复杂的结构化数据
def distribute(tag, *args):
    gameengine.callAppsByEventTag(tag, *args)


@functools.lru_cache(1)
def getAvatarFieldsInfo():
    _fields = []
    _kv = {}
    for _idx, _val in enumerate(gameconst.AvatarFieldsEnum):
        _kv[_val.name] = _idx
        _fields.append(_val.value)

    return {
        'kv': _kv,
        'fields': _fields
    }


def getAvatarFieldVal(name, data):
    _dic = getAvatarFieldsInfo()
    _idx = _dic['kv'][name]
    return data[_idx]

@functools.lru_cache(1)
def getAvatarFieldsDOTStr():
    """
    _str1: a.sm_name, a.sm_level, a.sm_school ...
    _str2: sm_name, sm_level, sm_school ...
    """

    _fields = getAvatarFieldsInfo()['fields']
    _str1 = ','.join('a.{}'.format(i) for i in _fields)
    _str2 = ','.join(_fields)

    return _str1, _str2


@functools.lru_cache(1)
def getEquipSqlInfo():
    _fields = []
    _kv = {}
    for _idx, _val in enumerate(gameconst.EquipFieldsEnum):
        _kv[_val.name] = _idx
        _fields.append(_val.value)

    return {
        'fields': _fields,
        'kv': _kv
    }


def getEquipFieldsVal(name, data):
    _idx = getEquipSqlInfo()['kv'][name]
    return data[_idx + len(getAvatarFieldsInfo()['fields'])]


@functools.lru_cache(1)
def getEquipSQLStr():
    _fields = getEquipSqlInfo()['fields']
    return ','.join('eq.{}'.format(i) for i in _fields)


"""
    从 posList 中选出 m 个点，使得选出的点两两距离不小于 radius。
    如果无法找到足够的点，则随机补充直到有 m 个点。
"""
def select_positions(posList, m, radius):
    n = len(posList)
    if m > n:
        gameengine.panicStack('select_positions: not enough points to select', m, n)
        return []
    
    maxVaildNum = 0
    vaildList = None
    shuffled = posList[:]
    for i in range(5):
        # 随机打乱列表以便随机选择
        random.shuffle(shuffled)
        selected = []

        if radius <= 0:
            return shuffled[:m]
        
        # 贪心选择：遍历打乱后的点，如果某个点与已选点距离都大于 radius，则选中
        for point in shuffled:
            if len(selected) >= m:
                break
            valid = True
            for selected_point in selected:
                dist = sMath.distance3D(point, selected_point)
                if dist < radius:
                    valid = False
                    break
            if valid:
                selected.append(point)
        
        vaildNum = len(selected)
        # 如果已选点数不足 m，从剩余点中随机补充
        if len(selected) < m:
            LOG_DBG('select_positions: not enough valid points, selected:', len(selected), 'need:', m, 'all:', len(shuffled))
            # 找出未被选中的点
            remaining = [p for p in shuffled if p not in selected]
            # 如果剩余点数不够，从所有点中补充（包括已选点，避免重复使用同一个点）
            if len(remaining) < m - len(selected):
                # 但题目要求从 n 个中选 m 个，且 n>m，所以理论上不会发生
                # 这里为了安全，从原始列表中重新选（排除已选点）
                all_points = posList[:]
                available = [p for p in all_points if p not in selected]
                # 随机选择需要的点数
                num_needed = m - len(selected)
                additional = random.sample(available, num_needed)
                selected.extend(additional)
            else:
                num_needed = m - len(selected)
                additional = random.sample(remaining, num_needed)
                selected.extend(additional)
        else:
            return selected

        if vaildNum > maxVaildNum:
            maxVaildNum = vaildNum
            vaildList = selected
    
    return vaildList

def compare4stageversion(clientStr, serverStr):
    if not clientStr:
        return True
    if not serverStr:
        return True

    cliStage = clientStr.split('.')
    serStage = serverStr.split('.')

    if len(cliStage) != 4:
        return True
    if len(serStage) != 4:
        return True

    for i in range(len(serStage)):
        stage1 = int(cliStage[i]) if cliStage[i].isdigit() else 0
        stage2 = int(serStage[i]) if serStage[i].isdigit() else 0

        if stage1 != stage2:
            return stage1 < stage2

    return False

def check4stageversion(verStr):
    if not verStr:
        return False
    verStage = verStr.split('.')
    if len(verStage) != 4:
        return False
    for state in verStage:
        if not state.isdigit():
            return False
    return True

def getCubeCoinCostByTimes(times):
    costCfg = cube_config.datas['cubeNumCoinCost'].get('value', ())
    for costInfo in costCfg:
        if times + 1 == costInfo[0]:
            return costInfo[1], costInfo[2]
    return 0, 0

def getCubeAddTimesTypeByitemId(itemId):
    if itemId == cube_config.datas['cubeNumItem']['value']:
        return gameconst.CUBE_ADD_TIMES_TYPE_ITEM
    costCfg = cube_config.datas['cubeNumCoinCost'].get('value', ())
    for costInfo in costCfg:
        if itemId != costInfo[1]:
            continue
        return gameconst.CUBE_ADD_TIMES_TYPE_COIN
    
    return gameconst.CUBE_ADD_TIMES_TYPE_NULL

def getWonderLandCoinCostByTimes(times):
    costCfg = wonderLand_config.datas['wonderLandNumCoinCost'].get('value', ())
    totalCnt = wonderLand_config.datas['wonderLandNumCoinDailyLimit']['value']
    for costInfo in costCfg:
        if totalCnt - times + 1 == costInfo[0]:
            return costInfo[1], costInfo[2]
    return 0, 0

def getWonderLandAddTimesTypeByitemId(itemId):
    if itemId == wonderLand_config.datas['wonderLandNumItem']['value']:
        return gameconst.CUBE_ADD_TIMES_TYPE_ITEM
    costCfg = wonderLand_config.datas['wonderLandNumCoinCost'].get('value', ())
    for costInfo in costCfg:
        if itemId != costInfo[1]:
            continue
        return gameconst.CUBE_ADD_TIMES_TYPE_COIN
    
    return gameconst.CUBE_ADD_TIMES_TYPE_NULL

def getAbyssCoinCostByTimes(times):
    costCfg = abyss_config.datas['abyssNumCoinCost'].get('value', ())
    totalCnt = abyss_config.datas['abyssNumCoinDailyLimit']['value']
    for costInfo in costCfg:
        if totalCnt - times + 1 == costInfo[0]:
            return costInfo[1], costInfo[2]
    return 0, 0

def getAbyssAddTimesTypeByitemId(itemId):
    if itemId == abyss_config.datas['abyssNumItem']['value']:
        return gameconst.CUBE_ADD_TIMES_TYPE_ITEM
    costCfg = abyss_config.datas['abyssNumCoinCost'].get('value', ())
    for costInfo in costCfg:
        if itemId != costInfo[1]:
            continue
        return gameconst.CUBE_ADD_TIMES_TYPE_COIN
    
    return gameconst.CUBE_ADD_TIMES_TYPE_NULL

def debugSoulData(data):
    LOG_DBG("debugSoulData:")
    for v in data:
        LOG_INFO("--")
        LOG_INFO("类型:", affix_affix.datas[v[0]]["prop"])
        LOG_INFO("品质:", v[1])
        LOG_INFO("数值:", v[2])

def isValidProp(propId, schoolId):
    propName = affix_affix.datas[propId]['prop']
    propType = fightProp_define.datas[propName]['propType']
    excludePropType = character_charData.datas[schoolId]['excludePropType']
    #LOG_INFO("isValidprop: propId:", propId, "schoolId:", schoolId, "propType:", propType, "excludePropType:", excludePropType)
    return excludePropType != propType

def rollEquipSoulProps(itemId, schoolId):
    soulSoulData = soul_soul.datas[itemId]

    #随数量
    numCount = []
    numWeight = []
    for numData in soulSoulData['propertyNum']:
        numCount.append(numData[0])
        numWeight.append(numData[1])
    numRes = random.choices(numCount, weights=numWeight, k=1)[0]
    #LOG_INFO("rollEquipSoulProps: num: %s" % numRes)
    
    #随词条(基础词条可重复，稀有词条不重复)
    normalPropIds = []
    normalPropWeight = []
    rarePropIds = []
    rarePropWeight = []
    
    if soulSoulData['baseProp']:
        for propData in soulSoulData['baseProp']:
            if isValidProp(propData[0], schoolId):
                normalPropIds.append(propData[0])
                normalPropWeight.append(propData[1])
    if soulSoulData['rareProp']:
        for propData in soulSoulData['rareProp']:
            if isValidProp(propData[0], schoolId):
                if numRes < 3 and affix_affix.datas[propData[0]]['prop'] == 'adjAtkBless':
                    continue
                rarePropIds.append(propData[0])
                rarePropWeight.append(propData[1])
        
    propRes = []
    rarePropSet = set()
    for _ in range(numRes):
        res = random.choices(normalPropIds + rarePropIds, weights=normalPropWeight + rarePropWeight, k=1)[0]
        propRes.append(res)
        if res in rarePropIds:
            rarePropWeight[rarePropIds.index(res)] = 0
            rarePropSet.add(res)
    #LOG_INFO("rollEquipSoulProps: prop: %s" % propRes)

    #随品质 and 具体数值
    qualityRes = []
    valueRes = []
    qualityWeightData = soul_soul.datas[itemId]['qualityWeight']
    luckyWeightData = soul_soul.datas[itemId]['LuckyWeight']
    for propId in propRes:
        qualityIds = []
        qualityWeight = []
        weightData = luckyWeightData if affix_affix.datas[propId]['prop'] == 'adjAtkBless' else qualityWeightData
        for qualityData in weightData:
            qualityId = qualityData[0] - 1
            qualityValue = affix_affix.datas[propId]['qualityValue'][qualityId]
            # 属性区间是0到0则不参与随机(幸运词条只有紫和金)
            if qualityValue[0] == 0 and qualityValue[1] == 0:
                continue

            if qualityId >= numRes and propId in rarePropSet:
                continue
            qualityIds.append(qualityId)
            qualityWeight.append(qualityData[1])
        res = random.choices(qualityIds, weights=qualityWeight, k=1)[0]
        qualityRes.append(res)

        # 随机具体数值
        qualityValue = affix_affix.datas[propId]['qualityValue'][res]
        valueRes.append(random.randint(qualityValue[0], qualityValue[1]))

    finalRes = []
    for i in range(len(propRes)):
        finalRes.append([propRes[i], qualityRes[i], valueRes[i]])
    return finalRes

def rollItemProps(itemId, itemSubType, schoolId):
    if itemSubType in gameconst.ItemSubEnum.EQUIP_SOUL_TYPE:
        return rollEquipSoulProps(itemId, schoolId)
    return []

def getIntDateTime(now, offsetSeconds=gameconst.GENERAL_CYCLE_TIME):
    now -= offsetSeconds
    dateTimeStr = utils.getCommonTimeStrFromTimeStamp(now)
    return int(dateTimeStr[0:8])

def updateMallItemPriceCache(stub, itemId, avgPrice):
    now = curTS()
    if not checkDiffDay(gameglobal.mallItemLastUpdateTime.get(itemId, 0), now, 0):
        return
    
    servOpenDay = getSvrOpenDays()
    gameglobal.mallItemLastUpdateTime[itemId] = now
    stub.mallItemLastUpdateTime[itemId] = now
    mallIdList = MCP.itemId2ID.get(itemId, [])
    for mallId in mallIdList:
        data = MCP.datas[mallId]
        if data['type'] == gameconst.MallItemType.DYNAMIC_PRICE:
            price = data['costItem'][0][1]
            lastPrice = data['costItem'][0][1]
            if servOpenDay > data['serverDay']:
                if mallId in gameglobal.mallItemPriceCache:
                    lastPrice = gameglobal.mallItemPriceCache[mallId]
                price = avgPrice * MMC.datas['dynGoodsWeight']['value']
                upLimit = lastPrice * (1 + MMC.datas['dynGoodsUpLimit']['value'])
                downLimit = lastPrice * (1 - MMC.datas['dynGoodsDownLimit']['value'])
                if price > upLimit:
                    price = upLimit
                elif price < downLimit:
                    price = downLimit
                price = math.ceil(price)
            
            if price < MMC.datas['dynGoodsDefaultPrice']['value']:
                price = MMC.datas['dynGoodsDefaultPrice']['value']
            LOG_INFO("updateMallItemPriceCache id:", mallId, "price:", lastPrice, "->", price)
            gameglobal.mallItemPriceCache[mallId] = price
            stub.mallItemPriceDict[mallId] = price

def isPremiumMonthCard(tp):
    return tp in (gameconst.PremiumType.BIG_MONTH_CARD, gameconst.PremiumType.SMALL_MONTH_CARD)

def checkGmSoulProp(rollProps):
    LOG_INFO("checkGmSoulProp", rollProps)
    for prop in rollProps:
        max_v = affix_affix.datas[prop[0]]['qualityValue'][-1][-1]
        if prop[2] > max_v:
            LOG_ERR("checkGmSoulProp fail! ", max_v, prop)
            return False
    return True

def debugFullStack():
    import inspect
    # skip=1 跳过当前print_full_stack函数自身栈帧，context读取源码行
    frame_list = inspect.stack(context=100)[1:]
    LOG_INFO("====================【完整调用栈 START】====================\n")

    for idx, frame_info in enumerate(frame_list):
        frame, fname, line_no, func_name, source_lines, _ = frame_info
        LOG_INFO(f"Frame {idx}: File {fname}, line {line_no}, func={func_name}|")

    LOG_INFO("====================【完整调用栈 END】====================\n")

def safe_str_to_int(s, default=0):
    s_clean = str(s).strip()
    if not s_clean:
        return default
    if s_clean.startswith("-"):
        if s_clean[1:].isdigit():
            return int(s_clean)
    else:
        if s_clean.isdigit():
            return int(s_clean)
    return default

def checkInTimePeriod(curTime, deadTimePeriod, comp=0):
    startTimeCron, _ = nextByCronTupleList(deadTimePeriod[0], curTime)
    startTime = startTimeCron + curTime
    endTimeCron, _ = nextByCronTupleList(deadTimePeriod[1], curTime)
    endTime = endTimeCron + curTime
    if startTime >= endTime:
        startTime -= 86400
    if comp == 0:
        return startTime <= curTime and curTime < endTime
    elif comp == 1:
        return startTime < curTime and curTime <= endTime
    elif comp == 2:
        return startTime < curTime and curTime < endTime
    elif comp == 3:
        return startTime <= curTime and curTime <= endTime
    

@functools.lru_cache(1)
def getWaitmapMaxOnline():
    cellMaxOneline = gameconfig.maxCellAvatarCount()
    cellNum = gameconfig.cellAppCount()
    return cellMaxOneline * cellNum


class FNV1a64:
    # FNV-1a 64 官方标准参数
    FNV_OFFSET_BASIS: int = 14695981039346656037
    FNV_PRIME: int = 1099511628211
    # 64位无符号掩码
    MASK64: int = 0xFFFFFFFFFFFFFFFF

    def __init__(self):
        self._hash = self.FNV_OFFSET_BASIS

    def update_bytes(self, data: bytes) -> None:
        """输入原始字节流更新哈希"""
        b: int
        for b in data:
            self._hash ^= b
            self._hash *= self.FNV_PRIME
            # 强制约束为 uint64，防止Python大整数溢出不一致
            self._hash &= self.MASK64

    def update_int(self, value: int, byte_length: int = 8, big_endian: bool = True) -> None:
        """写入整数，默认转8字节大端序"""
        order = "big" if big_endian else "little"
        b = value.to_bytes(byte_length, byteorder=order, signed=False)
        self.update_bytes(b)

    def update_str(self, text: str, encoding: str = "utf-8") -> None:
        """写入字符串"""
        self.update_bytes(text.encode(encoding))

    def digest_uint64(self) -> int:
        """直接返回uint64整型结果，存数据库最方便"""
        return self._hash & self.MASK64

    def digest_hex(self) -> str:
        """返回16位小写十六进制字符串，等价md5.hexdigest风格"""
        return f"{self.digest_uint64():016x}"

    def digest_raw(self) -> bytes:
        """返回8字节二进制bytes"""
        return self.digest_uint64().to_bytes(8, byteorder="big", signed=False)

    def reset(self) -> None:
        """重置哈希状态，复用对象"""
        self._hash = self.FNV_OFFSET_BASIS