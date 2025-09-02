# -*- coding: utf-8 -*-
import json

import gameconst
import gameglobal
import gmAdmin
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
