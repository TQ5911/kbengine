# -*- coding: utf-8 -*-
import json
import KBEngine
import gameconst
import gameglobal
import functools
import base64
import gmAdmin
import gamesql
import gmCommand
import gameengine
import mailAssistor
from KBEDebug import *
import antiAddictCategory_antiAddictCategory_def as AAC_AACDD
import dropAward
import itemFactory
import utils
import dataUtils
import gameconfig
import _pickle as cPickle

BASE, CELL, ALL, INSIDE, ALLSIDE = gameconst.BASE, gameconst.CELL,\
    gameconst.ALL, gmAdmin.INSIDE, gmAdmin.ALLSIDE


Int, Player, Str, Entity, Float = gmCommand.Int, gmCommand.Player,\
    gmCommand.Str, gmCommand.Entity, gmCommand.Float

PlayerAccount = gmCommand.PlayerAccount

gm_cmd, forwardGMCommand, callOnApps = gmCommand.gm_cmd, gmCommand.forwardGMCommand,\
    gmCommand._callApps

RARG, RSU, RSTUB, RONE, SELF, RALL= gmCommand.RARG, gmCommand.RSU, gmCommand.RSTUB,\
    gmCommand.RONE, gmCommand.SELF, gmCommand.RALL


GOD_GROUPS = gmCommand.GOD_GROUPS
DEVE_GROUPS = gmCommand.DEVE_GROUPS


class Operation:
    REVOKE = 1
    TEST = 2
    PUBLISH = 3


class DoFuncOfflineSafeCtx(object):
    def __init__(self, func, args, gbId):
        self.func = func
        self.args = args
        self.gbId = gbId
        self.dbId = 0

    def setDbId(self, dbId):
        self.dbId = dbId

# ------------------------- 跑马灯 ---------------------------
@gm_cmd('$gmTestMarquee', (Player('gbId or Id', raw=True), Int('mid'), Str('content'), Str('channels')),
        RARG(0), BASE, '测试跑马灯', ALLSIDE, DEVE_GROUPS)
def gmTestMarquee(su, operator, mid, content, channels):
    if mid == 0:
        su.onCommandResult(-1, '跑马灯id为0', {})
        return False, 'id is zero'

    playerGbId = getattr(operator, 'gbID', 0)
    gameglobal.localBaseApp.sendOfficialMessageForTest(playerGbId, content, channels, mid)

    su.onCommandResult(0, '', {})
    return True, 'command success'


#chatType 0表示跑马灯+聊天频道， 1表示只有跑马灯， 2表示只有聊天频道




# ------------------------- 离线安全 ----------
def doOnAccounOfflineSafeByDbId(ctx, ret, num, insertId, err):
    if err or not ret:
        LOG_ERR('doOnAccounOfflineSafeByDbId error: %s' % err)
        return

    _accountName = ret[0][0].decode('utf-8')
    LOG_DBG('doOnAccounOfflineSafeByDbId: accountName: %s, func: %s, args: %s' % (_accountName, ctx.func, ctx.args))
    gamesql.recordAccountOfflineCallback(_accountName, ctx.func, ctx.args)


def doOnAccounOfflineSafeAfterGetBox(ctx, box):
    if box == False:
        LOG_WARN('doOnAccounOfflineSafeAfterGetBox error: box is False')
        return

    elif box == True:
        # 角色已经离线，执行离线安全操作
        _sql = f'SELECT sm_accountName FROM tbl_Account WHERE id = {ctx.dbId}'
        LOG_DBG('doOnAccounOfflineSafeAfterGetBox: sql: %s' % _sql)
        KBEngine.executeRawDatabaseCommand(_sql, functools.partial(doOnAccounOfflineSafeByDbId, ctx))
        return

    getattr(box, ctx.func)(*ctx.args)


def doOnAccounOfflineSafeByGbIdAfterGetParentId(ctx, ret, num, insertId, err):
    if err or not ret:
        LOG_ERR('doOnAccounOfflineSafeByGbIdAfterGetParentId error: %s' % err)
        return

    _dbId = int(ret[0][0])
    ctx.setDbId(_dbId)
    LOG_DBG('doOnAccounOfflineSafeByGbIdAfterGetParentId: dbId: %s, func: %s, args: %s' % (_dbId, ctx.func, ctx.args))
    KBEngine.lookUpEntityByDBID('Account', _dbId, functools.partial(doOnAccounOfflineSafeAfterGetBox, ctx))

def doOnAccounOfflineSafeByGbId(gbId, func, args):
    ctx = DoFuncOfflineSafeCtx(func, args, gbId)
    _sql = "SELECT parentID FROM game_account_characters WHERE gbID = {}".format(ctx.gbId)
    KBEngine.executeRawDatabaseCommand(_sql, functools.partial(doOnAccounOfflineSafeByGbIdAfterGetParentId, ctx))

# 2026-10-09 已迁至 GAME_API.py: _banIDIPAgain, _afterBanIDIP, _onBeginBanIDIP, _setChatForbidden,
# _afterDisbanIDIP, _beginDisbanIDIP, _removeChatForbidden, _afterBanLogin, _banAvatarAgain,
# _onBeginBanLogin, _beginDisbanLogin, _afterDisbanLogin, _onQueryBanInfo, _genBanInfoResp
# （随 21 个 $指令一起搬走）

@gm_cmd('$sendHotfixToPlayer', (Player("gbId or Id"), Str('version')), RARG(0), BASE, '发送热更到玩家', ALLSIDE, GOD_GROUPS)
def sendHotfixToPlayer(su, player, version):
    player.sendHotfix(version)
    return True, 'command success'


# 2026-10-09 已迁至 GAME_API.py: _onModifyCurrency, _genModifyCurrencyInfoResp, _onModifyMulCurrency,
# _genModifyMulCurrencyInfoResp （随 21 个 $指令一起搬走）
# 注意：上面 modifyCurrency 块仍通过 from .GAME_API import 引用这些 helper

# --- OPERATION.py:378-396 (供 sendEquipSoul 调用) ---
def _onModifyCurrency(su, gbId, itemId, ret, num, insertId, err):
    if err:
        LOG_ERR('_onModifyCurrency err:', err)
        return
    if not ret:
        LOG_ERR('_onModifyCurrency: no ret')
        return

    gbId, fieldName, curVale, updateNum, updateOldNum, updateNewdNum = ret[0]
    curVale = int(curVale.decode())
    updateNum = int(updateNum.decode())
    updateOldNum = int(updateOldNum.decode())
    updateNewdNum = int(updateNewdNum.decode())

    resp = {}
    resp.update(_genModifyCurrencyInfoResp(True, itemId, updateNum, curVale + updateOldNum, curVale + updateNewdNum))

    LOG_INFO('_onModifyCurrency: resp', resp)
    return su.onCommandResult(0, f'command success', resp)

# --- OPERATION.py:398-405 (供 sendEquipSoul 和 _onModifyCurrency 调用) ---
def _genModifyCurrencyInfoResp(res, itemId, updateNum, oldNum, newNum):
    return {
            'effective' : int(res),
            'itemId' : itemId,
            'updateNum' : updateNum,
            'oldNum' : oldNum,
            'newNum' : newNum
        }

@gm_cmd('$modifyCurrency', (Player("gbId or Id", raw=True), Int("itemId"), Int("updateNum")), RARG(0), BASE, '修改玩家的货币类道具数量', ALLSIDE, DEVE_GROUPS)
def modifyCurrency(su, player, itemId, updateNum):
    LOG_INFO('modifyCurrency', itemId, updateNum)
    if itemId not in gameconst.ItemIdEnum.GM_MODIFY_CURRENCY_ITEMS:
        return su.onCommandResult(0, f'command failed, currency unsupported', {})
    if updateNum == 0:
        return su.onCommandResult(0, f'command success', {})
    if gmCommand.isRawPlayer(player):
        gbId, name, accountName, dbId = player
        gamesql.recordModifyCurrency(gbId, itemId, updateNum, functools.partial(_onModifyCurrency, su, gbId, itemId))
    else:
        res, oldNum, newNum = player.gmModifyCurrency(itemId, updateNum)
        resp = {}
        resp.update(_genModifyCurrencyInfoResp(res, itemId, newNum - oldNum, oldNum, newNum))
        LOG_INFO('modifyCurrency: resp:', resp)
        return su.onCommandResult(0, f'command success', resp)

#############################################################

# ------------------------- 排行榜 ---------------------------
@gm_cmd('$finalScoreRushRank', (Int('force'),), RONE, BASE, '冲刺战力榜定榜', ALLSIDE, GOD_GROUPS, minArgs=0)
def finalScoreRushRank(su, force=0):
    force = force or 0
    LOG_INFO('finalScoreRushRank', force)
    gameengine.getGlobalBase(
        'LeaderBoardStub' + str(gameconst.LeaderBoardType.AVATAR_SCORE)
    ).gmFinalizeScoreRank(force)

    su.onCommandResult(0, '', {})
    return True, 'command success'


@gm_cmd('$gmRestoreEquip', (Player("gbId or Id", raw=True), Str("equipData"), Str("events"), ), RARG(0), BASE, '恢复装备', ALLSIDE, GOD_GROUPS)
def gmRestoreEquip(su, playerEnt, equipData, events):
    if gmCommand.isRawPlayer(playerEnt):
        su.onCommandResult(-1, '执行失败, 玩家不在线', {"ec": -2})
    else:
        playerEnt.gmRestoreEquip(su, equipData, events)

# ------------------------- 开关状态查询 ---------------------------
@gm_cmd('$gmGetAllSwitchStates', (), RONE, BASE, '获取所有开关状态', ALLSIDE, DEVE_GROUPS)
def gmGetAllSwitchStates(su):
    LOG_INFO('gmGetAllSwitchStates')

    result = {}

    for name, info in gameconfig.CONFIG.items():
        configName, convFunc, default, defaultV, desc, cid, flags = info
        flagNames = []
        if gameconfig.ConfigFlag.FLAG_CLIENT in flags:
            flagNames.append('FLAG_CLIENT')
        if gameconfig.ConfigFlag.CACHE_CONFIG in flags:
            flagNames.append('CACHE_CONFIG')
        if gameconfig.ConfigFlag.ALWAYS_SEND_CLIENT in flags:
            flagNames.append('ALWAYS_SEND_CLIENT')

        result[configName] = {
            'value': KBEngine.globalData['CONFIG'].get(configName, defaultV),
            'default': default,
            'desc': desc,
            'flags': flagNames,
            'persistent': gameconfig.ConfigFlag.CACHE_CONFIG not in flags,
        }

    for name, value in gameconfig.CACHE_DIC.items():
        if name not in result:
            try:
                json.dumps(value)
                result[name] = {'value': value, 'persistent': False}
            except (TypeError, ValueError):
                result[name] = {'value': str(value), 'persistent': False}

    su.onCommandResult(0, 'command success', result)
    return True, 'command success'


# ------------------------- 批量开关设置 ---------------------------
def _resolveCfgCmdName(key):
    info = gameconfig.CONFIG.get(key)
    if info is not None:
        if gameconfig.ConfigFlag.CACHE_CONFIG in info[6]:
            return '$setcachecfg'
        return '$setcfg'
    if key in gameconfig.CACHE_DIC:
        return '$setcachecfg'
    return None


@gm_cmd('$gmBatchSetSwitch', (Str('cfgStr'),), RONE, BASE, '批量设置开关状态(base64编码的json列表)', ALLSIDE, GOD_GROUPS)
def gmBatchSetSwitch(su, cfgStr):
    LOG_INFO('gmBatchSetSwitch')

    try:
        decoded = base64.b64decode(cfgStr.encode('ascii')).decode('utf-8')
        cfgList = json.loads(decoded)
    except Exception as e:
        return False, 'base64或json解析失败: %s' % e

    if not isinstance(cfgList, list):
        return False, '解码后必须是数组'

    results = []
    for idx, item in enumerate(cfgList):
        if not isinstance(item, dict):
            results.append({'index': idx, 'ok': False, 'msg': 'item不是字典'})
            continue

        key = item.get('key')
        value = item.get('value')

        if not key:
            results.append({'index': idx, 'ok': False, 'msg': 'key为空'})
            continue

        cmdName = _resolveCfgCmdName(key)
        if cmdName is None:
            results.append({'index': idx, 'key': key, 'ok': False, 'msg': '未知配置项'})
            continue

        valueStr = str(value) if not isinstance(value, str) else value

        try:
            LOG_WARN('gmBatchSetSwitch', cmdName, key, valueStr)
            forwardGMCommand(su, cmdName, key, valueStr)
            results.append({'index': idx, 'key': key, 'value': valueStr, 'cmd': cmdName, 'ok': True})
        except Exception as e:
            results.append({'index': idx, 'key': key, 'ok': False, 'msg': str(e)})

    successCount = sum(1 for r in results if r.get('ok'))
    su.onCommandResult(0, 'command success', {
        'total': len(results),
        'success': successCount,
        'failed': len(results) - successCount,
        'results': results,
    })
    return True, 'command success'


@gm_cmd('$enterDungeon', (Player("gbId or Id"), Int('dungeonId')), RARG(0), CELL, 'GM创建并进入讨伐副本', ALLSIDE, GOD_GROUPS)
def gm_enterDungeon(superUser, playerEnt, dungeonId):
    return playerEnt.gmEnterDungeon(dungeonId)
