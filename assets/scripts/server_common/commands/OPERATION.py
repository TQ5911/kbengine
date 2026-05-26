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


@gm_cmd('$gmPublishMarquee', (Int('mid'), Str('content'), Int('startTime'), Int('endTime'), Int('tick'),
                              Int('priority'), Str('channels')), RALL, BASE, '发布跑马灯', ALLSIDE, DEVE_GROUPS)
def gmPublishMarquee(su, mid, content, startTime, endTime, tick, priority, channels):
    if mid == 0:
        su.onCommandResult(-1, '跑马灯id为0', {})
        return False, 'id is zero'
    content = base64.b64decode(content.encode('ascii'), b'_-').decode('utf-8')
    gameglobal.localBaseApp.sendOfficialMessage(startTime, endTime, content, tick, channels, mid, priority)

    su.onCommandResult(0, '', {})
    return True, 'command success'


@gm_cmd('$gmRevokeMarquee', (Int('mid'),), RALL, BASE, '撤销跑马灯', ALLSIDE, DEVE_GROUPS)
def gmRevokeMarquee(su, mid):
    if mid == 0:
        su.onCommandResult(-1, '跑马灯id为0', {})
        return False, 'id is zero'

    gameglobal.localBaseApp.stopOfficialMessage(mid)

    su.onCommandResult(0, '', {})
    return True, 'command success'


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

@gm_cmd('$banAvatar', (Player("gbId or Id", raw=True), Int('endTime')), RONE, BASE, '封禁角色', ALLSIDE, DEVE_GROUPS)
def banAvatar(su, player, endTime):
    LOG_INFO('banAvatar', player, endTime)
    if gmCommand.isRawPlayer(player):
        gbId, name, accountName, dbId = player
        gamesql.banLogin(gbId, endTime, functools.partial(_afterBanLogin, gbId, endTime))
    else:
        player.gmBanAvatar(endTime)
    return True, 'command success'


@gm_cmd('$disbanAvatar', (Int('gbId'),), RONE, BASE, '解除封禁角色', ALLSIDE, DEVE_GROUPS)
def disbanAvatar(su, gbId):
    LOG_INFO('disbanAvatar', gbId)
    gamesql.disbanLogin(gbId, lambda *args: LOG_INFO('disbanAvatar success', args))
    return True, 'command success'


@gm_cmd('$addWhite', (Str('accountName'),), RONE, BASE, '添加白名单', ALLSIDE, DEVE_GROUPS)
def addWhite(su, accountName):
    LOG_INFO('addWhite', accountName)
    gamesql.addAccountWhiteList(accountName.split(','))
    return True, 'command success'

@gm_cmd('$deleteWhite', (Str('accountName'),), RONE, BASE, '移除白名单', ALLSIDE, DEVE_GROUPS)
def deleteWhite(su, accountName):
    LOG_INFO('deleteWhite', accountName)
    gamesql.deleteAccountWhiteList(accountName.split(','))
    return True, 'command success'

@gm_cmd('$sendHotfixToPlayer', (Player("gbId or Id"), Str('version')), RARG(0), BASE, '发送热更到玩家', ALLSIDE, GOD_GROUPS)
def sendHotfixToPlayer(su, player, version):
    player.sendHotfix(version)
    return True, 'command success'

@gm_cmd('$sendEquipSoul', (Str("toGBID"), Int("itemId"), Int("bindType"), Str("rollProps")), RONE, BASE, '向指定玩家发一封邮件', ALLSIDE, DEVE_GROUPS)
def gm_sendEquipSoul(superUser, toGBID, itemId, bindType, rollProps):
    _toGBID = int(toGBID)
    _addVal = dropAward.MailWealthVal()
    rollProps = json.loads(rollProps)
    item = itemFactory.ItemFactory.createItem(itemId, 1, bindType, rollProps=rollProps)
    _addVal.addWealthByObjList([item])
    opUUID = KBEngine.genUUID64()
    mailAssistor.sendMailToPlayers([_toGBID], 37000003, extraAttach=_addVal,
                                    srcType=AAC_AACDD.datas.BONUS_SRC_GM, opUUID=opUUID)
    return True, 'command success'