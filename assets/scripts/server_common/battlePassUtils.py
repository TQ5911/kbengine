# coding: utf-8
import datetime
import time
import utils
import gameconfig
import gameconst
import battlePass_passGroup as BP_PGD
import battlePass_taskGroup as BP_TGD
import battlePass_battlePass as BP_BPD
import battlePass_rewardGroup as BP_RGD
import battlePass_config as BP_CFG
import buyCredit_premiumGoods as BCBPGD
from KBEDebug import *

_CATCHUP_TENTHS = {}
_CATCHUP_BASE_TENTHS = 10

RESET_DAILY, RESET_WEEKLY, RESET_SEASON = 1, 2, 3
# passType：1 绝对时间；2 开服第 serverStartTime 天 serverStartTimePoint 起，持续 periodDays 天，到 serverEndTimePoint 止
PASS_SERVER = 2
# 配表 taskType：31击杀 32召唤 33道具 34悬赏 35门票
TASK_KILL, TASK_GACHA, TASK_ITEM, TASK_BOUNTY, TASK_TICKET = 31, 32, 33, 34, 35
# privilege：(直升等级, 交易行格子, 背包格子)
PRIV_LV, PRIV_STALL, PRIV_BAG = 0, 1, 2


def parseTime(s):
    s = str(s or '')
    if not s:
        return 0
    if len(s) == 12:
        s += '00'
    return utils.getIntTimestamp(s)


def getCfg(groupId):
    cfg = BP_PGD.datas.get(groupId)
    if cfg:
        return cfg
    try:
        return BP_PGD.datas.get(int(groupId))
    except (TypeError, ValueError):
        return None


def periodRange(cfg):
    """返回闭区间 [startTs, endTs]，当前时间落在区间内则该战令进行中。"""
    if not cfg:
        return 0, 0
    if cfg['passType'] == PASS_SERVER:
        startDay = int(cfg.get('serverStartTime') or 0)
        period = int(cfg.get('periodDays') or 0)
        if startDay <= 0 or period <= 0:
            return 0, 0
        startTs = utils.getSvrOpenDayFiveTS() + (startDay - 1) * gameconst.ONE_DAY_COST_SECONDS
        endTs = startTs + (period - 1) * gameconst.ONE_DAY_COST_SECONDS
        sp = str(BP_CFG.datas['serverStartTimePoint']['value'])
        ep = str(BP_CFG.datas['serverEndTimePoint']['value'])
        startTs += int(sp[:2]) * 3600 + int(sp[2:4]) * 60 - gameconst.GAME_REFRESH_OCLOCK * 3600
        endTs += int(ep[:2]) * 3600 + int(ep[2:4]) * 60 - gameconst.GAME_REFRESH_OCLOCK * 3600
        return startTs, endTs
    return parseTime(cfg.get('startTime')), parseTime(cfg.get('endTime'))


def isActive(cfg, now=None):
    now = utils.curTS() if now is None else now
    startTs, endTs = periodRange(cfg)
    return startTs > 0 and endTs >= startTs and startTs <= now <= endTs


def groupName(cfg):
    return cfg.get('name') or ''


def endTimeText(cfg):
    if cfg['passType'] != PASS_SERVER:
        s = str(cfg.get('endTime') or '')
        if len(s) < 12:
            return s
        return '%s-%s %s:%s' % (int(s[4:6]), int(s[6:8]), s[8:10], s[10:12])
    _, endTs = periodRange(cfg)
    if endTs <= 0:
        return ''
    t = time.localtime(endTs + 1)
    return '%s-%s %02d:%02d' % (t.tm_mon, t.tm_mday, t.tm_hour, t.tm_min)


def inNoticeWindow(cfg, now=None):
    now = utils.curTS() if now is None else now
    _, endTs = periodRange(cfg)
    days = int(cfg.get('settleNoticeDays') or 0)
    return endTs > 0 and days > 0 and endTs - days * 86400 <= now <= endTs


def iterActive(now=None):
    now = utils.curTS() if now is None else now
    for gid, cfg in BP_PGD.datas.items():
        if isActive(cfg, now):
            yield gid, cfg


def needExp(cfg, lv):
    need = 0
    for item in cfg.get('levelGradient') or ():
        if lv >= item[0]:
            need = item[1]
    return need


def buyLvCost(cfg, lv):
    itemId, price = 0, 0
    for item in cfg.get('levelGradient') or ():
        if lv >= item[0]:
            itemId, price = int(item[2]), int(item[3])
    return itemId, price


def _toDate(ts):
    t = time.localtime(int(ts))
    return datetime.date(t.tm_year, t.tm_mon, t.tm_mday)


def catchupDays(cfg, openTs=None):
    if not cfg:
        return 0
    openTs = gameconfig.serverOpenTime() if openTs is None else int(openTs)
    startTs, endTs = periodRange(cfg)
    refTs = max(int(openTs or 0), int(startTs or 0))
    if refTs <= 0 or endTs <= 0 or refTs > endTs:
        return 0
    if cfg['passType'] == PASS_SERVER:
        return ((endTs + 1) - refTs + gameconst.ONE_DAY_COST_SECONDS - 1) // gameconst.ONE_DAY_COST_SECONDS
    ref = _toDate(refTs)
    end = _toDate(endTs)
    if ref > end:
        return 0
    return (end - ref).days + 1


def _calcCatchupMulTenths(cfg, openTs):
    if not int(cfg.get('catchupEnabled') or 0):
        return _CATCHUP_BASE_TENTHS
    designDays = int(cfg.get('designTaskDays') or 0)
    if designDays <= 0:
        return _CATCHUP_BASE_TENTHS
    r = catchupDays(cfg, openTs)
    if r <= 0 or r >= designDays:
        return _CATCHUP_BASE_TENTHS
    tenths = (designDays * 10 + r - 1) // r
    cap = int(cfg.get('catchupMax') or 5)
    if cap <= 0:
        cap = 5
    tenths = min(max(tenths, _CATCHUP_BASE_TENTHS), cap * 10)
    LOG_INFO('battlePass catchup snapshot', cfg.get('GroupID'), openTs, 'R', r, 'designDays', designDays, 'M', tenths / 10.0)
    return tenths


def catchupMulTenths(cfg, openTs=None):
    if not cfg:
        return _CATCHUP_BASE_TENTHS
    openTs = gameconfig.serverOpenTime() if openTs is None else int(openTs)
    key = (cfg.get('GroupID'), int(openTs or 0))
    cached = _CATCHUP_TENTHS.get(key)
    if cached is not None:
        return cached
    tenths = _calcCatchupMulTenths(cfg, openTs)
    _CATCHUP_TENTHS[key] = tenths
    return tenths


def applyCatchupExp(cfg, exp):
    exp = int(exp)
    if exp <= 0:
        return 0
    tenths = catchupMulTenths(cfg)
    if tenths <= _CATCHUP_BASE_TENTHS:
        return exp
    return exp * tenths // 10


def iterTasks(groupId, taskType=None, key=None):
    cfg = getCfg(groupId)
    if not cfg:
        return
    bucket = BP_TGD.typeDic.get(cfg.get('taskGroupID')) or {}
    t = 0 if taskType is None else int(taskType)
    ids = bucket.get(t)
    if not ids:
        return
    if t == TASK_ITEM:
        if key is None:
            ids = [tid for taskIds in ids.values() for tid in taskIds]
        else:
            ids = ids.get(int(key)) or ()
    for taskId in ids:
        yield taskId, BP_TGD.datas[taskId]


def hasTaskType(taskType, now=None):
    t = int(taskType)
    for gid, cfg in iterActive(now):
        if (BP_TGD.typeDic.get(cfg.get('taskGroupID')) or {}).get(t):
            return True
    return False


def matchTask(cfg, key=0, src=0):
    ttype = int(cfg.get('taskType') or 0)
    filters = cfg.get('filters') or ()
    if ttype == TASK_ITEM:
        return not filters or int(src) in filters
    if ttype == TASK_BOUNTY:
        return True
    return not filters or int(key) in filters


def getPremium(passId):
    cfg = BCBPGD.datas.get(passId)
    if cfg and cfg.get('passGroupID'):
        return cfg
    return None


def isPaidPass(passId):
    return getPremium(passId) is not None


def isFreePass(passId):
    cfg = BP_BPD.datas.get(passId)
    return int((cfg or {}).get('tier') or 0) == 1


def iterPasses(groupId):
    for pid, pcfg in BP_BPD.datas.items():
        if pcfg.get('passGroupID') == groupId:
            yield pid, pcfg


def getPassIdByActivateItem(itemId):
    for pid, gcfg in BCBPGD.datas.items():
        if gcfg.get('passGroupID') and gcfg.get('activateItem') == itemId:
            return pid
    return 0


def activateRewardId(passId):
    cfg = getPremium(passId)
    return cfg.get('reward', 0) if cfg else 0


def privilege(passId):
    cfg = BP_BPD.datas.get(passId)
    p = (cfg.get('privilege') if cfg else None) or (0, 0, 0)
    return p[0], p[1], p[2]


def rewardRow(cfg, lv):
    maxLv = cfg.get('maxLevel') or 0
    return maxLv + 1 if maxLv and lv > maxLv else lv


def rewardId(rewardGroupID, lv):
    return (BP_RGD.lvDic.get(rewardGroupID) or {}).get(lv) or 0
