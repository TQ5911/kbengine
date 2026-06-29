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
@gm_cmd('$gmPublishMarquee', (Int('mid'), Str('content'), Int('startTime'), Int('endTime'), Int('tick'),
                              Int('priority'), Str('channels'), Str('chatChannelList'), Int('chatType')), RALL, BASE, '发布跑马灯', ALLSIDE, DEVE_GROUPS)
def gmPublishMarquee(su, mid, content, startTime, endTime, tick, priority, channels, chatChannelList, chatType):
    LOG_INFO('gmPublishMarquee', mid, content, startTime, endTime, tick, priority, channels, chatChannelList, chatType)
    if mid == 0:
        su.onCommandResult(-1, '跑马灯id为0', {})
        return False, 'id is zero'
    content = base64.b64decode(content.encode('ascii'), b'_-').decode('utf-8')
    gameglobal.localBaseApp.sendOfficialMessage(startTime, endTime, content, tick, channels, mid, priority, chatChannelList, chatType)

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

def _banIDIPAgain(gbId, banType, endTime, isAuto, *args):
    # 再次封印一次，以防止出现极端情况
    gameengine.getGlobalBase('PlayerStub').doOnOthersBase(
        [gbId],
        'IDIPBanState',
        (banType, endTime, isAuto),
        None,
        '',
        ())

def _afterBanIDIP(gbId, banType, endTime, isAuto, ret, num, insertId, err):
    if err:
        LOG_ERR('_afterBanIDIP', err, ret)
        return

    KBEngine.addTimer(2, 0, functools.partial(_banIDIPAgain, gbId, banType, endTime, isAuto))

def _onBeginBanIDIP(su, gbId, endTime, isAuto, ret, num, insertId, err):
    if err:
        LOG_ERR('_onBeginBanIDIP err:', err)
        su.onCommandResult(1, '_onBeginBanIDIP: err', {})
        return

    if not ret:
        LOG_ERR('_onBeginBanLogin: not found')
        su.onCommandResult(1, '_onBeginBanIDIP: not found', {})
        return

    idipBanDictData, idipBanDataDictData = ret[0]
    idipBanDict = cPickle.loads(idipBanDictData)
    idipBanDataDict = cPickle.loads(idipBanDataDictData)
    
    LOG_INFO('_onBeginBanIDIP: idipBanDict:', idipBanDict, 'idipBanDataDict:', idipBanDataDict)

    if isAuto:
        isBan = False
        lastIsAuto = False
        banType = gameconst.IDIPBanType.CHAT
        if banType in idipBanDict:
            if idipBanDict[banType] >= utils.curTS():
                isBan = True
                lastIsAuto = idipBanDataDict[banType]['isAuto']
        LOG_INFO('IDIPBanState auto:', banType, isBan, lastIsAuto)
        
        #当前没被封直接封
        if not isBan:
            idipBanDict[banType] = endTime
            idipBanDataDict[banType] = {'isAuto': isAuto}
            LOG_INFO('IDIPBanState auto but not isBan', idipBanDict, idipBanDataDict)
            gamesql.banIDIP(gbId, idipBanDict, idipBanDataDict, functools.partial(_afterBanIDIP, gbId, banType, endTime, isAuto))
            su.onCommandResult(gameconst.ChatSysGMErr.OK, 'command success', {"effective": 1, "banExpireTime": endTime, "isAuto": 1 if isAuto else 0, "banType": gameconst.WebBanType.CHAT})
            return True

        #当前封禁中，并且是自动ban，如果时间更久，则覆盖
        if lastIsAuto:
            if endTime > idipBanDict[banType]:
                idipBanDict[banType] = endTime
                idipBanDataDict[banType] = {'isAuto': isAuto}
                LOG_INFO('IDIPBanState auto but isBan and lastIsAuto', idipBanDict, idipBanDataDict)
                gamesql.banIDIP(gbId, idipBanDict, idipBanDataDict, functools.partial(_afterBanIDIP, gbId, banType, endTime, isAuto))
                su.onCommandResult(gameconst.ChatSysGMErr.OK, 'command success', {"effective": 1, "banExpireTime": endTime, "isAuto": 1 if isAuto else 0, "banType": gameconst.WebBanType.CHAT})
                return True
        
        #当前封禁中，并且是手动ban，要报警
        if not lastIsAuto:
            LOG_ERR('IDIPBanState but autoBanLoginFlag is MANUAL', idipBanDict, idipBanDataDict)
            su.onCommandResult(gameconst.ChatSysGMErr.FAIL, 'IDIPBanState but autoBanLoginFlag is MANUAL', {})
            return False
    else:
        LOG_INFO('IDIPBanState but autoBanLoginFlag is MANUAL')
        idipBanDict[banType] = endTime
        idipBanDataDict[banType] = {'isAuto': isAuto}
        gamesql.banIDIP(gbId, idipBanDict, idipBanDataDict, functools.partial(_afterBanIDIP, gbId, banType, endTime, isAuto))
        su.onCommandResult(gameconst.ChatSysGMErr.OK, 'command success', {"effective": 1, "banExpireTime": endTime, "isAuto": 1 if isAuto else 0, "banType": gameconst.WebBanType.CHAT})
        return True
    su.onCommandResult(gameconst.ChatSysGMErr.OK, 'command success', {"effective": 0, "banExpireTime": idipBanDict[banType], "isAuto": 1 if isAuto else 0, "banType": gameconst.WebBanType.CHAT})
    return True

def _setChatForbidden(superUser, playerEnt, endTime, isAuto, banType):
    # 离线玩家处理
    if gmCommand.isRawPlayer(playerEnt):
        gbId, name, accountName, dbId = playerEnt
        LOG_INFO(f"gm offline setChatForbidden, gbID:{gbId}")
        gamesql.beginBanIDIP(gbId, functools.partial(_onBeginBanIDIP, superUser, gbId, endTime, isAuto))
        superUser.onCommandResult(gameconst.ChatSysGMErr.OK, 'command success', {"effective": 1, "banExpireTime": endTime, "isAuto": 1 if isAuto else 0, "banType": 2})
    # 在线玩家处理
    else:
        LOG_INFO("gm online setChatForbidden")
        playerEnt.IDIPBanState(superUser, gameconst.IDIPBanType.CHAT, endTime, isAuto)

def _afterDisbanIDIP(superUser, gbId, ret, num, insertId, err):
    if err:
        LOG_ERR('_afterDisbanIDIP err:', err)
        return

def _beginDisbanIDIP(superUser, gbId, ret, num, insertId, err):
    if err:
        LOG_ERR('_beginDisbanIDIP err:', err)
        superUser.onCommandResult(1, '_beginDisbanIDIP err:', {})
        return
    
    idipBanDict, idipBanDataDict = ret[0]
    idipBanDict = cPickle.loads(idipBanDict)
    idipBanDataDict = cPickle.loads(idipBanDataDict)
    LOG_INFO('_beginDisbanIDIP: idipBanDict:', idipBanDict, 'idipBanDataDict:', idipBanDataDict)

    if gameconst.IDIPBanType.CHAT in idipBanDict:
        superUser.onCommandResult(gameconst.ChatSysGMErr.OK, 'command success', {"wasBanned": 1, "previousBanExpireTime": idipBanDict[gameconst.IDIPBanType.CHAT],\
            "isAuto": idipBanDataDict[gameconst.IDIPBanType.CHAT]['isAuto'], "banType": 2})
        idipBanDict.pop(gameconst.IDIPBanType.CHAT)
        idipBanDataDict.pop(gameconst.IDIPBanType.CHAT)
        gamesql.disbanIDIP(gbId, idipBanDict, idipBanDataDict, functools.partial(_afterDisbanIDIP, superUser, gbId))
    else:
        superUser.onCommandResult(gameconst.ChatSysGMErr.OK, 'command success', {"wasBanned": 0, "previousBanExpireTime": 0, "isAuto": 0, "banType": 0})

def _removeChatForbidden(superUser, playerEnt):
    # 离线玩家处理
    if gmCommand.isRawPlayer(playerEnt):
        gbId, name, accountName, dbId = playerEnt
        LOG_INFO(f"gm offline removeChatForbidden, gbID:{gbId}")
        gamesql.beginDisbanIDIP(gbId, functools.partial(_beginDisbanIDIP, superUser, gbId))
        superUser.onCommandResult(gameconst.ChatSysGMErr.OK, 'command success', {"wasBanned": 1, "previousBanExpireTime": 0, "isAuto": 1, "banType": 2})
    # 在线玩家处理
    else:
        LOG_INFO(f"gm online removeChatForbidden")
        playerEnt.IDIPRemoveBanState(superUser, gameconst.IDIPBanType.CHAT)

def _afterBanLogin(gbId, endTime, isAuto, ret, num, insertId, err):
    if err:
        LOG_ERR('_afterBanLogin', err, ret)
        return

    KBEngine.addTimer(2, 0, functools.partial(_banAvatarAgain, gbId, endTime, isAuto))

def _banAvatarAgain(gbId, endTime, isAuto, *args):
    # 再次封印一次，以防止出现极端情况
    gameengine.getGlobalBase('PlayerStub').doOnOthersBase(
        [gbId],
        'gmBanAvatar',
        (endTime, isAuto),
        None,
        '',
        ())

def _onBeginBanLogin(su, gbId, endTime, isAuto, ret, num, insertId, err):
    if err:
        LOG_ERR('_onBeginBanLogin err:', err)
        su.onCommandResult(1, '_onBeginBanLogin err:', {})
        return

    if not ret:
        LOG_ERR('_onBeginBanLogin: not found')
        su.onCommandResult(1, '_onBeginBanLogin: not found', {})
        return
    autoBanFlag, banLogin = ret[0]
    autoBanFlag = int(autoBanFlag.decode())
    banLogin = int(banLogin.decode())
    LOG_INFO('_onBeginBanLogin: autoBanFlag:', autoBanFlag, 'banLogin:', banLogin)
    if isAuto:
        #当前封禁中并且是手动的，自动ban不能覆盖，且要报错
        if banLogin >= utils.curTS() and autoBanFlag == gameconst.AutoBanType.MANUAL:
            LOG_ERR('gmBanAvatar but autoBanLoginFlag is MANUAL')
            su.onCommandResult(1, 'gmBanAvatar but autoBanLoginFlag is MANUAL', {})
            return
        #自动ban时间更久，才覆盖
        if endTime > banLogin:
            LOG_INFO('gmBanAvatar but autoBanLoginFlag is AUTO, and endTime is more than banLogin', endTime, banLogin)
            gamesql.banLogin(gbId, gameconst.AutoBanType.AUTO, endTime, functools.partial(_afterBanLogin, gbId, endTime, isAuto))
            su.onCommandResult(0, 'command success', {"effective": 1, "banExpireTime": endTime, "isAuto": 1, "banType": 1})
        else:
            su.onCommandResult(0, 'command success', {"effective": 0, "banExpireTime": banLogin, "isAuto": 1, "banType": 1})
    else:
        LOG_INFO('gmBanAvatar but banType is MANUAL', endTime)
        gamesql.banLogin(gbId, gameconst.AutoBanType.MANUAL, endTime, functools.partial(_afterBanLogin, gbId, endTime, isAuto))
        su.onCommandResult(0, 'command success', {"effective": 1, "banExpireTime": endTime, "isAuto": 0, "banType": 1})

@gm_cmd('$banAvatar', (Player("gbId or Id", raw=True), Int('endTime'), Int('isAuto'), Int('banType')), RARG(0), BASE, '封禁角色', ALLSIDE, DEVE_GROUPS)
def banAvatar(su, player, endTime, isAuto, banType):
    LOG_INFO('banAvatar', player, endTime, isAuto, banType)
    if banType == gameconst.WebBanType.CHAT:
        return _setChatForbidden(su, player, endTime, isAuto, banType)
    if gmCommand.isRawPlayer(player):
        gbId, name, accountName, dbId = player
        gamesql.beginBanLogin(gbId, functools.partial(_onBeginBanLogin, su, gbId, endTime, isAuto))
    else:
        player.gmBanAvatar(su, endTime, isAuto)

def _beginDisbanLogin(su, gbId, ret, num, insertId, err):
    if err:
        LOG_ERR('_beginDisbanLogin err:', err)
        su.onCommandResult(1, '_beginDisbanLogin err:', {})
        return

    autoBanFlag, banLogin = ret[0]
    autoBanFlag = int(autoBanFlag.decode())
    banLogin = int(banLogin.decode())
    LOG_INFO('_beginDisbanLogin: autoBanFlag:', autoBanFlag, 'banLogin:', banLogin)
    gamesql.disbanLogin(gbId, functools.partial(_afterDisbanLogin, su, gbId, banLogin, autoBanFlag))

def _afterDisbanLogin(su, gbId, banLogin, autoBanFlag, ret, num, insertId, err):
    if err:
        LOG_ERR('_afterDisbanLogin err:', err)
        su.onCommandResult(1, '_afterDisbanLogin err:', {})
        return

    wasBanned = 1 if banLogin > utils.curTS() else 0
    if wasBanned:
        su.onCommandResult(0, 'command success', {"wasBanned": wasBanned, "previousBanExpireTime": banLogin, "isAuto": 1 if autoBanFlag == gameconst.AutoBanType.AUTO else 0, "banType": 1})
    else:
        su.onCommandResult(0, 'command success', {"wasBanned": 0, "previousBanExpireTime": 0, "isAuto": 0, "banType": 0})


@gm_cmd('$disbanAvatar', (Player("gbId or Id", raw=True), Int('banType')), RARG(0), BASE, '解除封禁角色', ALLSIDE, DEVE_GROUPS)
def disbanAvatar(su, player, banType):
    LOG_INFO('disbanAvatar', player, banType)
    if banType == gameconst.WebBanType.CHAT:
        return _removeChatForbidden(su, player)
    if gmCommand.isRawPlayer(player):
        gbId, name, accountName, dbId = player
        gamesql.beginDisbanLogin(gbId, functools.partial(_beginDisbanLogin, su, gbId))
    else:
        LOG_ERR('disbanAvatar error, player is online!!!!!!!', player)

@gm_cmd('$banMail', (Player("gbId or Id", raw=True), Int('endTime'), Int('banType')), RARG(0), BASE, '封禁邮件', ALLSIDE, DEVE_GROUPS)
def banMail(su, player, endTime, banType):
    LOG_INFO('banMail', player, endTime, banType)
    _args = (endTime, banType)
    if gmCommand.isRawPlayer(player):
        gbId, name, accountName, dbId = player
        gamesql.recordAvatarOfflineCallback(gbId, 'gmBanMail', _args)
    else:
        player.gmBanMail(*_args)
    return True, 'command success'

def _onQueryBanInfo(su, gbId, ret, num, insertId, err):
    if err:
        LOG_ERR('_onQueryBanInfo err:', err)
        return

    if not ret:
        LOG_ERR('_onQueryBanInfo: not found')
        return
    autoBanFlag, banLogin, idipBanDict, idipBanDataDict = ret[0]
    autoBanFlag = int(autoBanFlag.decode())
    banLogin = int(banLogin.decode())
    idipBanDict = cPickle.loads(idipBanDict)
    idipBanDataDict = cPickle.loads(idipBanDataDict)

    resp = {}
    resp.update(_genBanInfoResp(gameconst.WebBanType.LOGIN, banLogin, autoBanFlag))
    resp.update(_genBanInfoResp(gameconst.WebBanType.CHAT, 
                                idipBanDict.get(gameconst.IDIPBanType.CHAT, 0), 
                                idipBanDataDict.get(gameconst.IDIPBanType.CHAT, {}).get('isAuto', 0)))
    LOG_INFO('_onQueryBanInfo: resp', resp)
    return su.onCommandResult(0, f'command success', resp)

def _genBanInfoResp(banType, expireTime, isAuto):
    webBanType2Key = {
        gameconst.WebBanType.LOGIN : 'ban',
        gameconst.WebBanType.CHAT : 'mute',
    }
    effective = 1 if expireTime > utils.curTS() else 0
    return {
        webBanType2Key[banType] : {
            'effective' : effective,
            'expireTime' : expireTime if effective else 0,
            'isAuto' : isAuto if effective else 0,
        }
    }

@gm_cmd('$queryAvatarBanInfo', (Player("gbId or Id", raw=True), ), RARG(0), BASE, '查询封禁信息', ALLSIDE, DEVE_GROUPS)
def queryAvatarBanInfo(su, player):
    LOG_INFO('queryAvatarBanInfo', player)
    if gmCommand.isRawPlayer(player):
        gbId, name, accountName, dbId = player
        gamesql.queryBanInfo(gbId, functools.partial(_onQueryBanInfo, su, gbId))
    else:
        resp = {}
        resp.update(_genBanInfoResp(gameconst.WebBanType.LOGIN, player.banLogin, player.autoBanLoginFlag))
        resp.update(_genBanInfoResp(gameconst.WebBanType.CHAT, player.idipBanDict.get(gameconst.IDIPBanType.CHAT, 0), player.idipBanDataDict.get(gameconst.IDIPBanType.CHAT, {}).get('isAuto', 0)))
        LOG_INFO('queryAvatarBanInfo: resp:', resp)
        return su.onCommandResult(0, f'command success', resp)

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
    _addVal = dropAward.MailAttachVal()
    rollProps = json.loads(rollProps)
    if not utils.checkGmSoulProp(rollProps):
        return False, '执行失败, 灵魂属性错误'
    item = itemFactory.ItemFactory.createItem(itemId, 1, bindType, rollProps=rollProps)
    _addVal.addWealthByObjList([item])
    opUUID = KBEngine.genUUID64()
    mailAssistor.sendMailToPlayers([_toGBID], 37002017, extraAttach=_addVal,
                                    srcType=AAC_AACDD.datas.BONUS_SRC_GM, opUUID=opUUID)
    return True, 'command success'

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
def _onModifyMulCurrency(su, gbId, ret, num, insertId, err):
    if err:
        LOG_ERR('_onModifyMulCurrency err:', err)
        return
    if not ret:
        LOG_ERR('_onModifyMulCurrency: no ret')
        return

    oldNumList = []
    newNumList = []
    updateNumList = []
    for (_, _, curVale, updateNum, updateOldNum, updateNewdNum) in ret:
        curVale = int(curVale.decode())
        updateNum = int(updateNum.decode())
        updateOldNum = int(updateOldNum.decode())
        updateNewdNum = int(updateNewdNum.decode())
        updateNumList.append(updateNum)
        oldNumList.append(curVale + updateOldNum)
        newNumList.append(curVale + updateNewdNum)

    resp = {}
    resp.update(_genModifyMulCurrencyInfoResp(True, updateNumList, oldNumList, newNumList))

    LOG_INFO('_onModifyMulCurrency: resp', resp)
    return su.onCommandResult(0, f'command success', resp)

def _genModifyMulCurrencyInfoResp(res, updateNumList, oldNumList, newNumList):
    return {
            'effective' : int(res),
            'updateNumList' : updateNumList,
            'oldNumList' : oldNumList,
            'newNumList' : newNumList
        }

@gm_cmd('$modifyMulCurrency', (Player("gbId or Id", raw=True), Str("modifyInfoStr")), RARG(0), BASE, '修改玩家的货币类道具数量', ALLSIDE, DEVE_GROUPS)
def modifyMulCurrency(su, player, modifyInfoStr):
    LOG_INFO('modifyMulCurrency', modifyInfoStr)

    modifyInfoList = modifyInfoStr.split(',')
    modifyNumList = []
    for updateNumStr in modifyInfoList:
        updateNum = utils.safe_str_to_int(updateNumStr)
        modifyNumList.append(updateNum)
    if len(modifyNumList) != len(gameconst.ItemIdEnum.GM_MODIFY_CURRENCY_ITEMS):
        return su.onCommandResult(0, f'command failed, modifyInfo len not match {modifyNumList}, {gameconst.ItemIdEnum.GM_MODIFY_CURRENCY_ITEMS}', {})
    
    LOG_INFO('modifyMulCurrency: modifyNumList:', modifyNumList)
    if gmCommand.isRawPlayer(player):
        gbId, name, accountName, dbId = player
        modifyNumListStr = ','.join(str(x) for x in modifyNumList)
        gamesql.recordMulModifyCurrency(gbId, modifyNumListStr, functools.partial(_onModifyMulCurrency, su, gbId))
    else:
        oldNumList = []
        newNumList = []
        updateNumList = []
        for idx, itemId in enumerate(gameconst.ItemIdEnum.GM_MODIFY_CURRENCY_ITEMS):
            _, oldNum, newNum = player.gmModifyCurrency(itemId, modifyNumList[idx])
            updateNumList.append(newNum - oldNum)
            oldNumList.append(oldNum)
            newNumList.append(newNum)
        resp = {}
        resp.update(_genModifyMulCurrencyInfoResp(True, updateNumList, oldNumList, newNumList))
        LOG_INFO('modifyMulCurrency: resp:', resp)
        return su.onCommandResult(0, f'command success', resp)

