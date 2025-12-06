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
forwardCommand = gmCommand.forwardCommand
callApps = gmCommand._callApps

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
        ERROR_MSG('doOnAccounOfflineSafeByDbId error: %s' % err)
        return

    _accountName = ret[0][0].decode('utf-8')
    DEBUG_MSG('doOnAccounOfflineSafeByDbId: accountName: %s, func: %s, args: %s' % (_accountName, ctx.func, ctx.args))
    gamesql.recordAccountOfflineCallback(_accountName, ctx.func, ctx.args)


def doOnAccounOfflineSafeAfterGetBox(ctx, box):
    if box == False:
        WARNING_MSG('doOnAccounOfflineSafeAfterGetBox error: box is False')
        return

    elif box == True:
        # 角色已经离线，执行离线安全操作
        _sql = f'SELECT sm_accountName FROM tbl_Account WHERE id = {ctx.dbId}'
        DEBUG_MSG('doOnAccounOfflineSafeAfterGetBox: sql: %s' % _sql)
        KBEngine.executeRawDatabaseCommand(_sql, functools.partial(doOnAccounOfflineSafeByDbId, ctx))
        return

    getattr(box, ctx.func)(*ctx.args)


def doOnAccounOfflineSafeByGbIdAfterGetParentId(ctx, ret, num, insertId, err):
    if err or not ret:
        ERROR_MSG('doOnAccounOfflineSafeByGbIdAfterGetParentId error: %s' % err)
        return

    _dbId = int(ret[0][0])
    ctx.setDbId(_dbId)
    DEBUG_MSG('doOnAccounOfflineSafeByGbIdAfterGetParentId: dbId: %s, func: %s, args: %s' % (_dbId, ctx.func, ctx.args))
    KBEngine.lookUpEntityByDBID('Account', _dbId, functools.partial(doOnAccounOfflineSafeAfterGetBox, ctx))

def doOnAccounOfflineSafeByGbId(gbId, func, args):
    ctx = DoFuncOfflineSafeCtx(func, args, gbId)
    _sql = "SELECT parentID FROM game_account_characters WHERE gbID = {}".format(ctx.gbId)
    KBEngine.executeRawDatabaseCommand(_sql, functools.partial(doOnAccounOfflineSafeByGbIdAfterGetParentId, ctx))


@gm_cmd('$banAvatar', (Int('gbId'), Int('endTime')), RONE, BASE, '封禁角色', ALLSIDE, DEV_GROUPS)
def banAvatar(su, gbId, endTime):
    DEBUG_MSG('banAvatar', gbId, endTime)
    doOnAccounOfflineSafeByGbId(gbId, 'banAvatar', (gbId, endTime))
    return True, '执行成功'


@gm_cmd('$disbanAvatar', (Int('gbId'),), RONE, BASE, '封禁角色', ALLSIDE, DEV_GROUPS)
def disbanAvatar(su, gbId):
    DEBUG_MSG('disbanAvatar', gbId)
    doOnAccounOfflineSafeByGbId(gbId, 'disbanAvatar', (gbId,))
    return True, '执行成功'

