# -*- coding: utf-8 -*-
import gameconst
import gmAdmin
import gmCommand
import functools
import importlib
import gameglobal
import gamesql
import gameconfig
import redisUtils
import KBEngine
from KBEDebug import *
from commands.CMD_COMMON import *

import login_set as LGSD
from server_common import gameengine

BASE, CELL, ALL, INSIDE, ALLSIDE = gameconst.BASE, gameconst.CELL,\
    gameconst.ALL, gmAdmin.INSIDE, gmAdmin.ALLSIDE

gm_cmd, forwardGMCommand, callOnApps = gmCommand.gm_cmd, gmCommand.forwardGMCommand,\
    gmCommand._callApps

Int = gmCommand.Int
Player = gmCommand.Player

RARG, RSU, RSTUB, RONE, RALL= gmCommand.RARG, gmCommand.RSU, gmCommand.RSTUB,\
    gmCommand.RONE, gmCommand.RALL

GOD_GROUPS = gmCommand.GOD_GROUPS

@gm_cmd('$objcheck', (Int('auto fixed'), ), RONE, BASE, 'do obj check', ALLSIDE, GOD_GROUPS)
def gmObjcheck(su, autofixed):
    forwardGMCommand(su, '$_objcheck-cell', autofixed)
    forwardGMCommand(su, '$_objcheck-base', autofixed)
    return True, 'objcheck 完成'

@gm_cmd('$_objcheck-cell', (Int('auto fixed'), ), RALL, CELL, 'do obj check', ALLSIDE, GOD_GROUPS)
def objcheckCell(su, autofixed):
    LOG_DBG('begin objcheckCell')
    import gamerefresh
    gamerefresh.mismathObjectCheck(autoFixed=autofixed, debug=True)

@gm_cmd('$_objcheck-base', (Int('auto fixed'), ), RALL, BASE, 'do obj check', ALLSIDE, GOD_GROUPS)
def objcheckBase(su, autofixed):
    LOG_DBG('begin objcheckBase')
    import gamerefresh
    gamerefresh.mismathObjectCheck(autoFixed=autofixed, debug=True)

@gm_cmd('$refresh', (), RONE, BASE, 'gm refresh', ALLSIDE, GOD_GROUPS)
def refresh(su):
    forwardGMCommand(su, '$_refresh-cell')
    forwardGMCommand(su, '$_refresh-base')
    return True, 'refresh完成'

@gm_cmd('$_refresh-cell', (), RALL, CELL, 'gm refresh cell', ALLSIDE, GOD_GROUPS)
def refreshCell(su):
    LOG_DBG('begin refreshCell')
    import gamerefresh
    gamerefresh.refreshScript()

@gm_cmd('$_refresh-base', (), RALL, BASE, 'gm refresh base', ALLSIDE, GOD_GROUPS)
def refreshBase(su):
    LOG_DBG('begin refresh base')
    import gamerefresh
    gamerefresh.refreshScript()

@gm_cmd('$reloaddata', (), RONE, BASE, 'reload data', ALLSIDE, GOD_GROUPS)
def reloadData(su):
    forwardGMCommand(su, '$_reloaddata-cell')
    forwardGMCommand(su, '$_reloaddata-base')
    gameglobal.localBaseApp.notifyInterfaceDataReload([])
    return True, 'reload data done'

@gm_cmd('$_reloaddata-cell', (), RALL, CELL, 'reload data cell', ALLSIDE, GOD_GROUPS)
def reloadDataCell(su):
    LOG_DBG('begin reloadDataCell')
    import gamerefresh
    gamerefresh.refreshData()

@gm_cmd('$_reloaddata-base', (), RALL, BASE, 'reload data base', ALLSIDE, GOD_GROUPS)
def reloadDataBase(su):
    LOG_DBG('begin reloadDataBase')
    import gamerefresh
    gamerefresh.refreshData()


def _recoverAfterGetDBID(ctx, ret, num, insertId, err):
    if err:
        LOG_ERR('_recoverAfterGetDBID', err)
        ctx['su'].onCommandResult(0, f'meet error', {
            'effective': 0,
            'err': err,
        })
        return

    if not ret:
        LOG_ERR('_recoverAfterGetDBID not found account')
        ctx['su'].onCommandResult(0, f'not found account', {
            'effective': 0,
        })
        return

    _dbid = int(ret[0][0])
    gamesql.takeOverAccount(ctx['selfAccount'], _dbid)
    ctx['su'].onCommandResult(0, f'command success', {
        'effective': 1,
    })


@gm_cmd('$recoverTakeOver', (Str("accountName"), ), RONE, BASE, '恢复账号接管', ALLSIDE, GOD_GROUPS)
def recoverTakeOver(su, selfAccount):
    _ctx = {
        'selfAccount': selfAccount,
        'su': su,
    }
    gamesql.getTakeOverOriginDBID(
        selfAccount,
        functools.partial(_recoverAfterGetDBID, _ctx)
    )


def _afterQueryOtherAccount(ctx, ret, num, insertId, err):
    if err:
        LOG_ERR('_afterQueryOtherAccount', err)
        ctx['su'].onCommandResult(0, f'meet err', {
            'effective': 0,
            'err': err,
        })
        return

    if not ret:
        LOG_ERR('_afterQueryOtherAccount not found account')
        ctx['su'].onCommandResult(0, f'not found account', {
            'effective': 0,
        })
        return

    _otherDBID = int(ret[0][0])
    gamesql.recordTakeOver(ctx['selfAccount'], ctx['selfDBID'])
    gamesql.takeOverAccount(ctx['selfAccount'], _otherDBID)
    ctx['su'].onCommandResult(0, f'command success', {
        'effective': 1,
    })


def _afterQuerySelfAccount(ctx, ret, num, insertId, err):
    if err:
        LOG_ERR('_afterQuerySelfAccount', err)
        ctx['su'].onCommandResult(0, f'meet error', {
            'effective': 0,
            'err': err,
        })
        return

    if not ret:
        LOG_ERR('_afterQuerySelfAccount not found account')
        ctx['su'].onCommandResult(0, f'not found account', {
            'effective': 0,
        })
        return

    _selfDBID = int(ret[0][0])
    ctx['selfDBID'] = _selfDBID
    gamesql.queryAccountDBID(
        ctx['otherAccount'], 
        functools.partial(_afterQueryOtherAccount, ctx)
    )


@gm_cmd('$takeOverAccount', (Str("selfAccountName"), Str('otherAccountName')), RONE, BASE, '接管other的账号', ALLSIDE, GOD_GROUPS)
def takeOverAccount(su, selfAccount, otherAccount):
    _ctx = {
        'selfAccount': selfAccount,
        'otherAccount': otherAccount,
        'su': su,
    }

    gamesql.queryAccountDBID(
        selfAccount, 
        functools.partial(_afterQuerySelfAccount, _ctx)
    )


def _kickAccountAfterLook(ctx, box):
    if box is False:
        LOG_ERR('_kickAccountAfterLook not online', ctx['accountName'])
        ctx['su'].onCommandResult(0, f'not online', {
            'effective': 0,
        })
        return

    elif box is True:
        LOG_INFO('_kickAccountAfterLook already offline', ctx['accountName'])
        ctx['su'].onCommandResult(0, f'command success', {
            'effective': 0,
        })
        return 

    box.kickAccountSingleGm(ctx['msgCont'])
    ctx['su'].onCommandResult(0, f'command success', {
        'effective': 1,
    })


def _kickaccount(ctx, ret, num, insertId, err):
    if err:
        LOG_ERR('_kickaccount', err)
        ctx['su'].onCommandResult(0, f'meet error', {
            'effective': 0,
            'err': err
        })
        return

    if not ret:
        LOG_WARN('_kickaccount not found', ret)
        ctx['su'].onCommandResult(0, f'not found', {
            'effective': 0,
        })
        return

    KBEngine.lookUpEntityByDBID(
        'Account',
        int(ret[0][0]),
        functools.partial(_kickAccountAfterLook, ctx)
    )


@gm_cmd('$kickaccount', (Str("accountName"), Str('msg content')), RONE, BASE, '踢账号下线', ALLSIDE, GOD_GROUPS)
def kickaccount(su, accountName, msgContent):
    _ctx = {
        'msgCont': msgContent,
        'accountName': accountName,
        'su': su,
    }
    gamesql.queryAccountDBID(
        accountName,
        functools.partial(_kickaccount, _ctx)
    )


@gm_cmd('$kickavatar', (Player("gbId or Id", raw=True), Str('msg content')), RARG(0), BASE, '踢玩家下线', ALLSIDE, GOD_GROUPS,minArgs=1)
def kickAvatar(su, player, msgContent):
    if gmCommand.isRawPlayer(player):
        return su.onCommandResult(0, f'command success', {
            'effective': 1
        })

    if not player.gmMode:
        player.onMessagePre(LGSD.datas['forceLogout']['value'], [msgContent])
        player.destroySelf(gameconst.OFFLINE_REASON_GMKICK)
        return su.onCommandResult(0, f'command success', {
            'effective': 1
        })

    return su.onCommandResult(0, f'avatar is gm', {
        'effective': 0
    })

def _kickAllAccount(msgId, *args):
    import gameengine
    gameengine.broadcastBaseapp(
        'broadcastToAllAccount',
        ('kickAccountGm', (msgId, )))

@gm_cmd('$killallavatar', (Int('msgId'),), RONE, BASE, '踢玩家下线', ALLSIDE, GOD_GROUPS,minArgs=0)
def killAllAvatar(su,msgId=0):
    import gameglobal

    if msgId == 0:
        msgId = LGSD.datas['login_serverClosed']['value']

    callOnApps(gameconst.BASE, 'gameconfig.setCacheConfig', ('permitLogin', '0'))
    callOnApps(gameconst.CELL, 'gameconfig.setCacheConfig', ('permitLogin', '0'))
    gameglobal.localBaseApp.notifyInterfaceCacheConfigChanged('permitLogin', '0')

    key = gameconst.RedisKey.SERVER_OPEN_STATE + str(gameconfig.serverId())
    redisUtils.RedisUtils.cmdSet(key, "0")
    LOG_INFO('update redis server open state when kill all avatar: ', key, "0")
    import KBEngine
    KBEngine.addTimer(5, 0, functools.partial(_kickAllAccount, msgId))


@gm_cmd('$hotreload', (), RONE, BASE, 'hot reload', ALLSIDE, GOD_GROUPS)
def gmHotreload(su):
    import hotReload
    importlib.reload(hotReload)
    forwardGMCommand(su, '$_hotreload-cell')
    forwardGMCommand(su, '$_hotreload-base')
    gameglobal.localBaseApp.notifyInterfaceReload()

@gm_cmd('$hotreloadCell', (), RONE, BASE, 'hot reload cell', ALLSIDE, GOD_GROUPS)
def hotreloadCell(su):
    import hotReload
    importlib.reload(hotReload)
    forwardGMCommand(su, '$_hotreload-cell')

@gm_cmd('$hotreloadBase', (), RONE, BASE, 'hot reload base', ALLSIDE, GOD_GROUPS)
def hotreloadBase(su):
    import hotReload
    importlib.reload(hotReload)
    forwardGMCommand(su, '$_hotreload-base')

@gm_cmd('$hotreloadInterface', (), RONE, BASE, 'hot reload interface', ALLSIDE, GOD_GROUPS)
def hotreloadInterface(su):
    gameglobal.localBaseApp.notifyInterfaceReload()
    return True, 'hotReload interface done'

@gm_cmd('$_hotreload-cell', (), RALL, CELL, 'hot reload cell', ALLSIDE, GOD_GROUPS)
def _hotReloadCell(su):
    LOG_INFO('begin _hotReloadCell')
    import hotReload
    importlib.reload(hotReload)
    hotReload.refreshCell()

@gm_cmd('$_hotreload-base', (), RALL, BASE, 'hot reload base', ALLSIDE, GOD_GROUPS)
def _hotReloadBase(su):
    LOG_INFO('begin _hotReloadBase')
    import hotReload
    importlib.reload(hotReload)
    hotReload.refreshBase()

@gm_cmd('$hotfix', (), RALL, BASE, 'do hotfix', ALLSIDE, GOD_GROUPS)
def hotfix(su):
    gameglobal.localBaseApp.readhotfix()

@gm_cmd('$setrequiredclientversion', (Int('plat'), Str('version'),), RALL, BASE, '设置强更版本号', ALLSIDE, GOD_GROUPS)
def setRequiredClientVersion(su, platId, verStr):
    if not utils.check4stageversion(verStr):
        return
    gameglobal.requiredClientVersion[platId] = verStr
    import gameengine
    gameglobal.localBaseApp.updateRequiredClientVersion(platId, verStr)
    gameglobal.localBaseApp.broadcastToAllAccountPatchVersion(platId, verStr)

def _setGameConstInternal(su, className, field, val):
    if className=='""' or not className:
        obj = gameconst
    else:
        obj = getattr(gameconst, className, None)

    if not obj:
        su.onCommandResult(gameconst.GMCommandErr.GM_RET_ARGS_ERR, 'invalid class name:%s'%className, {})
        return

    if hasattr(obj, field):
        setattr(obj, field, type(getattr(obj, field))(val))
    else:
        setattr(obj, field, val)

    su.onCommandResult(0, '', {})

@gm_cmd('$setconstbase', (Str('class'), Str('field'), Str('val')), RALL, BASE, '设置gameconst常量值BASE', ALLSIDE, GOD_GROUPS)
def setGameconstValBase(su, className, field, val):
    _setGameConstInternal(su, className, field, val)

@gm_cmd('$setconstcell', (Str('class'), Str('field'), Str('val')), RALL, CELL, '设置gameconst常量值CELL', ALLSIDE, GOD_GROUPS)
def setGameconstValCell(su, className, field, val):
    _setGameConstInternal(su, className, field, val)
