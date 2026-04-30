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
from KBEDebug import *

BASE = gameconst.BASE
CELL = gameconst.CELL
ALL = gameconst.ALL
INSIDE = gmAdmin.INSIDE
ALLSIDE = gmAdmin.ALLSIDE

Int = gmCommand.Int
Str = gmCommand.Str
Float = gmCommand.Float
Player = gmCommand.Player
Entity = gmCommand.Entity
PlayerAccount = gmCommand.PlayerAccount

gm_cmd = gmCommand.gm_cmd
forwardGMCommand = gmCommand.forwardGMCommand
callOnApps = gmCommand._callApps

RARG = gmCommand.RARG
RSU = gmCommand.RSU
RSTUB = gmCommand.RSTUB
RONE = gmCommand.RONE
RALL = gmCommand.RALL

GOD_GROUPS = gmCommand.GOD_GROUPS
DEV_GROUPS = gmCommand.DEV_GROUPS


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
@gm_cmd('$gmTestMarquee', (Player('gbId/Id', raw=True), Int('mid'), Str('content'), Str('channels')),
        RARG(0), BASE, '测试跑马灯', ALLSIDE, DEV_GROUPS)
def gmTestMarquee(su, operator, mid, content, channels):
    if mid == 0:
        su.onCommandResult(-1, '跑马灯id为0', {})
        return False, 'id is zero'

    playerGbId = getattr(operator, 'gbID', 0)
    gameglobal.localBaseApp.sendOfficialMessageForTest(playerGbId, content, channels, mid)

    su.onCommandResult(0, '', {})
    return True, '执行成功'


@gm_cmd('$gmPublishMarquee', (Int('mid'), Str('content'), Int('startTime'), Int('endTime'), Int('tick'),
                              Int('priority'), Str('channels')), RALL, BASE, '发布跑马灯', ALLSIDE, DEV_GROUPS)
def gmPublishMarquee(su, mid, content, startTime, endTime, tick, priority, channels):
    if mid == 0:
        su.onCommandResult(-1, '跑马灯id为0', {})
        return False, 'id is zero'
    content = base64.b64decode(content.encode('ascii'), b'_-').decode('utf-8')
    gameglobal.localBaseApp.sendOfficialMessage(startTime, endTime, content, tick, channels, mid, priority)

    su.onCommandResult(0, '', {})
    return True, '执行成功'


@gm_cmd('$gmRevokeMarquee', (Int('mid'),), RALL, BASE, '撤销跑马灯', ALLSIDE, DEV_GROUPS)
def gmRevokeMarquee(su, mid):
    if mid == 0:
        su.onCommandResult(-1, '跑马灯id为0', {})
        return False, 'id is zero'

    gameglobal.localBaseApp.stopOfficialMessage(mid)

    su.onCommandResult(0, '', {})
    return True, '执行成功'


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


def _afterBanLogin(gbId, endTime, ret, num, insertId, err):
    if err:
        LOG_ERR('_afterBanLogin', err, ret)
        return

    KBEngine.addTimer(2, 0, functools.partial(_banAvatarAgain, gbId, endTime))

def _banAvatarAgain(gbId, endTime, *args):
    # 再次封印一次，以防止出现极端情况
    gameengine.getGlobalBase('PlayerStub').doOnOthersBase(
        [gbId],
        'gmBanAvatar',
        (endTime, ),
        None,
        '',
        ())

@gm_cmd('$banAvatar', (Player("gbId/Id", raw=True), Int('endTime')), RONE, BASE, '封禁角色', ALLSIDE, DEV_GROUPS)
def banAvatar(su, player, endTime):
    LOG_IFO('banAvatar', player, endTime)
    if gmCommand.isRawPlayer(player):
        gbId, name, accountName, dbId = player
        gamesql.banLogin(gbId, endTime, functools.partial(_afterBanLogin, gbId, endTime))
    else:
        player.gmBanAvatar(endTime)
    return True, '执行成功'


@gm_cmd('$disbanAvatar', (Int('gbId'),), RONE, BASE, '解除封禁角色', ALLSIDE, DEV_GROUPS)
def disbanAvatar(su, gbId):
    LOG_IFO('disbanAvatar', gbId)
    gamesql.disbanLogin(gbId, lambda *args: LOG_IFO('disbanAvatar success', args))
    return True, '执行成功'


@gm_cmd('$addWhite', (Str('accountName'),), RONE, BASE, '添加白名单', ALLSIDE, DEV_GROUPS)
def addWhite(su, accountName):
    LOG_IFO('addWhite', accountName)
    gamesql.addAccountWhiteList(accountName.split(','))
    return True, '执行成功'

@gm_cmd('$deleteWhite', (Str('accountName'),), RONE, BASE, '移除白名单', ALLSIDE, DEV_GROUPS)
def deleteWhite(su, accountName):
    LOG_IFO('deleteWhite', accountName)
    gamesql.deleteAccountWhiteList(accountName.split(','))
    return True, '执行成功'

@gm_cmd('$sendHotfixToPlayer', (Player("gbId/Id"), Str('version')), RARG(0), BASE, '发送热更到玩家', ALLSIDE, GOD_GROUPS)
def sendHotfixToPlayer(su, player, version):
    player.sendHotfix(version)
    return True, '执行成功'

