# -*- coding: utf-8 -*-
import gameconst
import gmAdmin
import gmCommand
import importlib
import gameglobal
from KBEDebug import *
from commands.CMD_COMMON import *

import login_set as LGS

BASE = gameconst.BASE
CELL = gameconst.CELL
ALL = gameconst.ALL
INSIDE = gmAdmin.INSIDE
ALLSIDE = gmAdmin.ALLSIDE

gm_cmd = gmCommand.gm_cmd
forwardCommand = gmCommand.forwardCommand
callApps = gmCommand._callApps

Int = gmCommand.Int
Player = gmCommand.Player

RARG = gmCommand.RARG
RSU = gmCommand.RSU
RSTUB = gmCommand.RSTUB
RONE = gmCommand.RONE
RALL = gmCommand.RALL

GOD_GROUPS = gmCommand.GOD_GROUPS

@gm_cmd('$objcheck', (Int('autoFixed'), ), RONE, BASE, 'objcheck', ALLSIDE, GOD_GROUPS)
def objcheck(su, autoFixed):
    forwardCommand(su, '$_objcheck-cell', autoFixed)
    forwardCommand(su, '$_objcheck-base', autoFixed)
    return True, 'objcheck 完成'

@gm_cmd('$_objcheck-cell', (Int('autoFixed'), ), RALL, CELL, 'objcheck', ALLSIDE, GOD_GROUPS)
def objcheckCell(su, autoFixed):
    DEBUG_MSG('begin objcheckCell')
    import gamerefresh
    gamerefresh.mismathObjectCheck(autoFixed=autoFixed, debug=True)

@gm_cmd('$_objcheck-base', (Int('autoFixed'), ), RALL, BASE, 'objcheck', ALLSIDE, GOD_GROUPS)
def objcheckBase(su, autoFixed):
    DEBUG_MSG('begin objcheckBase')
    import gamerefresh
    gamerefresh.mismathObjectCheck(autoFixed=autoFixed, debug=True)

@gm_cmd('$refresh', (), RONE, BASE, 'refresh', ALLSIDE, GOD_GROUPS)
def refresh(su):
    forwardCommand(su, '$_refresh-cell')
    forwardCommand(su, '$_refresh-base')
    return True, 'refresh完成'

@gm_cmd('$_refresh-cell', (), RALL, CELL, 'refresh', ALLSIDE, GOD_GROUPS)
def refreshCell(su):
    DEBUG_MSG('begin refreshCell')
    import gamerefresh
    gamerefresh.refreshScript()

@gm_cmd('$_refresh-base', (), RALL, BASE, 'refresh', ALLSIDE, GOD_GROUPS)
def refreshBase(su):
    DEBUG_MSG('begin refreshBase')
    import gamerefresh
    gamerefresh.refreshScript()

@gm_cmd('$reloaddata', (), RONE, BASE, 'reload数据', ALLSIDE, GOD_GROUPS)
def reloadData(su):
    forwardCommand(su, '$_reloaddata-cell')
    forwardCommand(su, '$_reloaddata-base')
    gameglobal.localBaseApp.notifyInterfaceDataReload([])
    return True, 'reload data完成'

@gm_cmd('$_reloaddata-cell', (), RALL, CELL, 'reload数据', ALLSIDE, GOD_GROUPS)
def reloadDataCell(su):
    DEBUG_MSG('begin reloadDataCell')
    import gamerefresh
    gamerefresh.refreshData()

@gm_cmd('$_reloaddata-base', (), RALL, BASE, 'reload数据', ALLSIDE, GOD_GROUPS)
def reloadDataBase(su):
    DEBUG_MSG('begin reloadDataBase')
    import gamerefresh
    gamerefresh.refreshData()

@gm_cmd('$kickavatar', (Player("gbId/Id"),Int('messageId')), RARG(0), BASE, '踢玩家下线', ALLSIDE, GOD_GROUPS,minArgs=1)
def kickAvatar(su, player,messageId):
    if messageId == 0:
        messageId=LGS.datas['login_serverClosed']['value']
    if not player.gmMode :
        player.onMessagePre(messageId, [])
        ret = player.destroySelf(gameconst.AVATAR_OFFLINE_REASON_GMKICK)

        return ret, '执行完成：%s,%s'% (ret,messageId)

@gm_cmd('$killallavatar', (Int('messageId'),), RONE, BASE, '踢玩家下线', ALLSIDE, GOD_GROUPS,minArgs=0)
def killAllAvatar(su,messageId=0):
    import gameengine
    import gameglobal

    if messageId == 0:
        messageId=LGS.datas['login_serverClosed']['value']

    callApps(gameconst.BASE, 'gameconfig.setCacheConfig', ('permitLogin', '0'))
    callApps(gameconst.CELL, 'gameconfig.setCacheConfig', ('permitLogin', '0'))
    gameglobal.localBaseApp.notifyInterfaceCacheConfigChanged('permitLogin', '0')

    gameengine.broadcastBaseapp('broadcastToAllAvatar',
                                    (gameconst.CELL, 'kickGm',
                                     (gameconst.AVATAR_OFFLINE_REASON_GMKICK,messageId )))


@gm_cmd('$hotreload', (), RONE, BASE, 'hotreload', ALLSIDE, GOD_GROUPS)
def hotreload(su):
    import hotReload
    importlib.reload(hotReload)
    forwardCommand(su, '$_hotreload-cell')
    forwardCommand(su, '$_hotreload-base')
    gameglobal.localBaseApp.notifyInterfaceReload()

@gm_cmd('$hotreloadCell', (), RONE, BASE, 'hotreload', ALLSIDE, GOD_GROUPS)
def hotreloadCell(su):
    import hotReload
    importlib.reload(hotReload)
    forwardCommand(su, '$_hotreload-cell')

@gm_cmd('$hotreloadBase', (), RONE, BASE, 'hotreload', ALLSIDE, GOD_GROUPS)
def hotreloadBase(su):
    import hotReload
    importlib.reload(hotReload)
    forwardCommand(su, '$_hotreload-base')

@gm_cmd('$hotreloadInterface', (), RONE, BASE, 'hotreload', ALLSIDE, GOD_GROUPS)
def hotreloadInterface(su):
    gameglobal.localBaseApp.notifyInterfaceReload()
    return True, 'hotReload interface完成'

@gm_cmd('$_hotreload-cell', (), RALL, CELL, 'hotreload', ALLSIDE, GOD_GROUPS)
def _hotReloadCell(su):
    INFO_MSG('begin _hotReloadCell')
    import hotReload
    importlib.reload(hotReload)
    hotReload.refreshCell()

@gm_cmd('$_hotreload-base', (), RALL, BASE, 'hotreload', ALLSIDE, GOD_GROUPS)
def _hotReloadBase(su):
    INFO_MSG('begin _hotReloadBase')
    import hotReload
    importlib.reload(hotReload)
    hotReload.refreshBase()

@gm_cmd('$hotfix', (), RALL, BASE, 'hotfix', ALLSIDE, GOD_GROUPS)
def hotfix(su):
    gameglobal.localBaseApp.readhotfix()

@gm_cmd('$setrequiredclientversion', (Int('plat'), Str('version'),), RALL, BASE, '设置强更版本号', ALLSIDE, GOD_GROUPS)
def setRequiredClientVersion(su, platId, verStr):
    gameglobal.requiredClientVersion[platId] = verStr
    avatarFilter = lambda a:a.accountEntity.devicePlatId==platId
    gameglobal.localBaseApp.onBroadcastToAllClients('onSendRequiredVersion', (verStr,), filter=avatarFilter)

def _setGameConstInternal(su, className, field, val):
    if className=='""' or not className:
        obj = gameconst
    else:
        obj = getattr(gameconst, className, None)

    if not obj:
        su.onCommandResult(gameconst.GMCommandErr.ARGS_ERR, 'invalid class name:%s'%className, {})
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