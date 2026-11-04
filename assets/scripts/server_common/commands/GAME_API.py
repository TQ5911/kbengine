# -*- coding: utf-8 -*-
import KBEngine
from KBEDebug import *

import json
import functools
import base64
import _pickle as cPickle

import gameconst
import gameglobal
import gmAdmin
import gamesql
import gmCommand
import gameengine
import mailAssistor
import dropAward
import itemFactory
import utils
import dataUtils
import gameconfig

from commands.CMD_COMMON import *

import antiAddictCategory_antiAddictCategory_def as AAC_AACDD
import petData_petData as PDPD
import petData_petGear as PDPGD
import petData_set as PDSD
import randomSynthesis_synthetic as RSSD
import achievement_details as A_DD
import gacha_gachaPool as GGP
import gacha_gachaSet as GGS
import gameclass
import guild_guildUpgrade as G_GUD
import guildWarEquipment_warEquipmentUpgrate as G_WED
import guildTrain_guildTrain as GT_GTD
import guildTrain_guildTrainUpgrade as GT_GTUD

# ============================================================================
# 2026-10-09 helper 迁自 OPERATION.py/SYSTEM.py（随 21 个 $指令一起搬到 GAME_API.py）
# 顺序按依赖关系：被引用者在前；每段前标注原文件位置
# ============================================================================

# --- OPERATION.py:119-127 (供 _afterBanIDIP 调用) ---
def _banIDIPAgain(gbId, banType, endTime, isAuto, *args):
    # 再次封印一次，以防止出现极端情况
    gameengine.getGlobalBase('PlayerStub').doOnOthersBase(
        [gbId],
        'IDIPBanState',
        (banType, endTime, isAuto),
        None,
        '',
        ())

# --- OPERATION.py:129-138 (供 _onBeginBanIDIP 调用) ---
def _afterBanIDIP(gbId, banType, endTime, isAuto, ret, num, insertId, err):
    if err:
        LOG_ERR('_afterBanIDIP', err, ret)
        return

    state = 1 if endTime > utils.curTS() else 0
    if banType == gameconst.IDIPBanType.CHAT:
        LOG_INFO("_afterBanIDIP", gbId, state)
        gameengine.callBaseApps('gameengine.updateChatForbiddenState', (gbId, state))
    KBEngine.addTimer(2, 0, functools.partial(_banIDIPAgain, gbId, banType, endTime, isAuto))

# --- OPERATION.py:140-199 (供 _setChatForbidden 调用) ---
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

    banType = gameconst.IDIPBanType.CHAT
    if isAuto:
        isBan = False
        lastIsAuto = False
        if banType in idipBanDict:
            if idipBanDict[banType] >= utils.curTS():
                isBan = True
                lastIsAuto = idipBanDataDict[banType]['isAuto']
        LOG_INFO('IDIPBanState auto:', banType, isBan, lastIsAuto)

        # 当前没被封直接封
        if not isBan:
            idipBanDict[banType] = endTime
            idipBanDataDict[banType] = {'isAuto': isAuto}
            LOG_INFO('IDIPBanState auto but not isBan', idipBanDict, idipBanDataDict)
            gamesql.banIDIP(gbId, idipBanDict, idipBanDataDict, functools.partial(_afterBanIDIP, gbId, banType, endTime, isAuto))
            su.onCommandResult(gameconst.ChatSysGMErr.OK, 'command success', {"effective": 1, "banExpireTime": endTime, "isAuto": 1 if isAuto else 0, "banType": gameconst.WebBanType.CHAT})
            return True

        # 当前封禁中，并且是自动ban，如果时间更久，则覆盖
        if lastIsAuto:
            if endTime > idipBanDict[banType]:
                idipBanDict[banType] = endTime
                idipBanDataDict[banType] = {'isAuto': isAuto}
                LOG_INFO('IDIPBanState auto but isBan and lastIsAuto', idipBanDict, idipBanDataDict)
                gamesql.banIDIP(gbId, idipBanDict, idipBanDataDict, functools.partial(_afterBanIDIP, gbId, banType, endTime, isAuto))
                su.onCommandResult(gameconst.ChatSysGMErr.OK, 'command success', {"effective": 1, "banExpireTime": endTime, "isAuto": 1 if isAuto else 0, "banType": gameconst.WebBanType.CHAT})
                return True

        # 当前封禁中，并且是手动ban，要报警
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

# --- OPERATION.py:201-212 (供 banAvatar 调用) ---
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
        playerEnt.updateChatForbiddenState()

# --- OPERATION.py:214-221 (供 _beginDisbanIDIP 调用) ---
def _afterDisbanIDIP(superUser, gbId, banType, ret, num, insertId, err):
    if err:
        LOG_ERR('_afterDisbanIDIP err:', err)
        return

    if banType == gameconst.IDIPBanType.CHAT:
        LOG_INFO("_afterDisbanIDIP")
        gameengine.callBaseApps('gameengine.updateChatForbiddenState', (gbId, 0))

# --- OPERATION.py:223-241 (供 _removeChatForbidden 调用) ---
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
        gamesql.disbanIDIP(gbId, idipBanDict, idipBanDataDict, functools.partial(_afterDisbanIDIP, superUser, gbId, gameconst.IDIPBanType.CHAT))
    else:
        superUser.onCommandResult(gameconst.ChatSysGMErr.OK, 'command success', {"wasBanned": 0, "previousBanExpireTime": 0, "isAuto": 0, "banType": 0})

# --- OPERATION.py:243-254 (供 disbanAvatar 调用) ---
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
        playerEnt.updateChatForbiddenState()

# --- OPERATION.py:256-261 (供 _onBeginBanLogin 调用) ---
def _afterBanLogin(gbId, endTime, isAuto, ret, num, insertId, err):
    if err:
        LOG_ERR('_afterBanLogin', err, ret)
        return

    KBEngine.addTimer(2, 0, functools.partial(_banAvatarAgain, gbId, endTime, isAuto))

# --- OPERATION.py:263-271 (供 _afterBanLogin 调用) ---
def _banAvatarAgain(gbId, endTime, isAuto, *args):
    # 再次封印一次，以防止出现极端情况
    gameengine.getGlobalBase('PlayerStub').doOnOthersBase(
        [gbId],
        'gmBanAvatar',
        (endTime, isAuto),
        None,
        '',
        ())

# --- OPERATION.py:273-303 (供 banAvatar 调用) ---
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
        # 当前封禁中并且是手动的，自动ban不能覆盖，且要报错
        if banLogin >= utils.curTS() and autoBanFlag == gameconst.AutoBanType.MANUAL:
            LOG_WARN('gmBanAvatar but autoBanLoginFlag is MANUAL')
            su.onCommandResult(0, 'gmBanAvatar but autoBanLoginFlag is MANUAL', {"effective": 0, "banExpireTime": banLogin, "isAuto": 1, "banType": 1})
            return
        # 自动ban时间更久，才覆盖
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


# --- OPERATION.py:306-316 (供 disbanAvatar 调用) ---
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

# --- OPERATION.py:318-328 (供 _beginDisbanLogin 调用) ---
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


# --- OPERATION.py:333-353 (供 queryAvatarBanInfo 调用) ---
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

# --- OPERATION.py:355-367 (供 queryAvatarBanInfo 和 _onQueryBanInfo 调用) ---
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


# --- OPERATION.py:425-449 (供 modifyMulCurrency 调用) ---
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

# --- OPERATION.py:451-457 (供 modifyMulCurrency 和 _onModifyMulCurrency 调用) ---
def _genModifyMulCurrencyInfoResp(res, updateNumList, oldNumList, newNumList):
    return {
            'effective' : int(res),
            'updateNumList' : updateNumList,
            'oldNumList' : oldNumList,
            'newNumList' : newNumList
        }


# --- SYSTEM.py:206-226 (供 kickaccount 调用；依赖未搬走的 _kickAccountAfterLook) ---
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

    box.kickAccountSingleGm(ctx['subReason'])
    ctx['su'].onCommandResult(0, f'command success', {
        'effective': 1,
    })


# --- 2026-10-09 迁自 MISC.py line 955-972 (EMAIL_PLAYER_SEND) ---
@gm_cmd('$sendB64MailByGBIDNoMailId', (Player("gbId or Id", raw=True), Int('dueTime'), Str('attachStr'), Str('title'), Str('cont')), RARG(0), BASE,
        '向指定玩家发送一封自定义邮件, base64编码', ALLSIDE, GOD_GROUPS)
def gm_sendB64MailByGBIDNoMailId(superUser, playerEnt, dueTime, attachStr, b64title, b64cont):
    LOG_DBG('sendB64MailByGBIDNoMailId:', dueTime, attachStr, b64title, b64cont)
    _title = base64.b64decode(b64title.encode('ascii'), b'_-').decode('utf-8')
    cont = base64.b64decode(b64cont.encode('ascii'), b'_-').decode('utf-8')
    LOG_DBG('sendMailByGBIDNoMailId:', attachStr, _title, cont)
    if gmCommand.isRawPlayer(playerEnt):
        _toGBID = gmCommand.fetchGbIdFromRawPlayer(playerEnt)
    else:
        _toGBID = playerEnt.gbID

    _toGBID = int(_toGBID)
    _attach = mailAssistor.parseAttachStr(attachStr)
    _title = _title.strip("[] ")
    cont = cont.strip("[] ")
    mailAssistor.sendIDIPMailByGBID(superUser, _toGBID, dueTime, _attach, _title, cont, AAC_AACDD.datas.BONUS_SRC_GM, 0, ())
    return True, 'command success'

# --- 2026-10-09 迁自 MISC.py line 987-998 (EMAIL_GLOBAL_SEND) ---
@gm_cmd('$sendglobalmail', (Int('mail id'), Str('attachStr'), Str('despArgs str'), Str('title'), Str('cont'), Int('minRoleTime'), Int('maxRoleTime'),
                            Int('dueTime'),Int('minRoleLevel'), Int('maxRoleLevel'), Int('channel'), Int("mailTag")),
        RONE, gameconst.BASE, '发一封全服邮件', ALLSIDE, GOD_GROUPS)
def gm_gmSendGlobalMail(superUser, mailId, attachStr, despArgsStr, title, cont, minRoleTime, maxRoleTime, dueTime, minRoleLevel, maxRoleLevel, channel, mailTag):
    # attachStr: 多个物品用分号';'分隔; 每个物品有itemId, itemNum，若有绑定属性配置在第三个位置，例如：[30000001,100; 30001031,1,1]
    _attach = mailAssistor.parseAttachStr(attachStr)
    despArgs = mailAssistor.parseDespStr(despArgsStr)
    title = base64.b64decode(title.encode('ascii'), b'_-').decode('utf-8')
    cont = base64.b64decode(cont.encode('ascii'), b'_-').decode('utf-8')
    gameengine.getGlobalBase('GlobalMailStub').sendGlobalMail(mailId, _attach, despArgs, title, cont, minRoleTime, maxRoleTime, 
                                                              dueTime, minRoleLevel, maxRoleLevel, channel, AAC_AACDD.datas.BONUS_SRC_GM, mailTag)
    return True, 'command success'

# --- 2026-10-09 迁自 OPERATION.py line 74-85 (MARQUEE_PUBLISH) ---
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

# --- 2026-10-09 迁自 OPERATION.py line 88-97 (MARQUEE_REVOKE) ---
@gm_cmd('$gmRevokeMarquee', (Int('mid'),), RALL, BASE, '撤销跑马灯', ALLSIDE, DEVE_GROUPS)
def gmRevokeMarquee(su, mid):
    if mid == 0:
        su.onCommandResult(-1, '跑马灯id为0', {})
        return False, 'id is zero'

    gameglobal.localBaseApp.stopOfficialMessage(mid)

    su.onCommandResult(0, '', {})
    return True, 'command success'

# --- 2026-10-09 迁自 OPERATION.py line 327-336 (ROLE_BAN) ---
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

# --- 2026-10-09 迁自 OPERATION.py line 363-372 (ROLE_UNBAN) ---
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

# --- 2026-10-09 迁自 SYSTEM.py line 242-258 (ROLE_KICK) ---
@gm_cmd('$kickavatar', (Player("gbId or Id", raw=True), Int('subReason')), RARG(0), BASE, '踢玩家下线', ALLSIDE, GOD_GROUPS,minArgs=1)
def kickAvatar(su, player, subReason):
    if gmCommand.isRawPlayer(player):
        return su.onCommandResult(0, f'command success', {
            'effective': 1
        })

    if not player.gmMode:
        player.client and player.client.onAvatarOfflineClient(gameconst.OFFLINE_REASON_GMKICK_SUB_FROM+subReason)
        player.destroySelf(gameconst.OFFLINE_REASON_GMKICK)
        return su.onCommandResult(0, f'command success', {
            'effective': 1
        })

    return su.onCommandResult(0, f'avatar is gm', {
        'effective': 0
    })

# --- 2026-10-09 迁自 SYSTEM.py line 229-239 (ACCOUNT_KICK) ---
@gm_cmd('$kickaccount', (Str("accountName"), Int('subReason')), RONE, BASE, '踢账号下线', ALLSIDE, GOD_GROUPS)
def kickaccount(su, accountName, subReason):
    _ctx = {
        'subReason': subReason,
        'accountName': accountName,
        'su': su,
    }
    gamesql.queryAccountDBID(
        accountName,
        functools.partial(_kickaccount, _ctx)
    )

# --- 2026-10-09 迁自 OPERATION.py line 546-577 (ASSET_DEDUCTION) ---
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



# --- 2026-10-09 迁自 OPERATION.py line 590-604 (ITEM_DEDUCTION) ---
@gm_cmd('$gmDeductItem', (Player("gbId or Id", raw=True), Int("itemId"), Int("bindNum"), Int("unbindNum"), Int("ignoreBindNum"), Int("debtBindNum"), Int("debtUnbindNum")), RARG(0), BASE, '扣除道具/装备，不够的可以欠债', ALLSIDE,
        GOD_GROUPS)
def gmDeductItem(superUser, playerEnt, itemId, bindNum, unbindNum, ignoreBindNum, debtBindNum, debtUnbindNum):
    if gameconfig.isCrossServer():
        return False, '跨服禁止执行'
    if not dataUtils.getCommItemData(itemId) and not dataUtils.isEquipItemByItemId(itemId):
        return False, '执行失败, 道具不存在'

    if gmCommand.isRawPlayer(playerEnt):
        gbId, name, accountName, dbId = playerEnt
        gamesql.recordAvatarOfflineCallback(gbId, 'gmDeductItem', (itemId, bindNum, unbindNum, ignoreBindNum, debtBindNum, debtUnbindNum))
    else:
        playerEnt.gmDeductItem(itemId, bindNum, unbindNum, ignoreBindNum, debtBindNum, debtUnbindNum)

    return True, 'command success'

# --- 2026-10-09 迁自 OPERATION.py line 616-623 (ITEM_QUERY) ---
@gm_cmd('$gmGetItemNum', (Player("gbId or Id", raw=True), Int("itemId"), ), RARG(0), BASE, '获取玩家道具数量（包括仓库）', ALLSIDE,
        GOD_GROUPS)
def gmGetItemNum(su, playerEnt, itemId):
    if gmCommand.isRawPlayer(playerEnt):
        su.onCommandResult(-1, '执行失败, 玩家不在线', {"ec": -2, "itemId": itemId, "bagBindNum": 0, "bagUnbindNum": 0, "warehouseBindNum": 0, "warehouseUnbindNum": 0})
    else:
        playerEnt.gmGetItemNum(su, itemId)


# --- 2026-10-09 迁自 OPERATION.py line 624-631 (EQUIPMENT_QUERY) ---
@gm_cmd('$gmQueryEquip', (Player("gbId or Id", raw=True), Int("itemId"), Int("EquipID"), ), RARG(0), BASE, '查询装备', ALLSIDE,
        GOD_GROUPS)
def gmQueryEquip(superUser, playerEnt, itemId, equipId):
    if gmCommand.isRawPlayer(playerEnt):
        superUser.onCommandResult(-1, '执行失败, 玩家不在线', {"ec": -2})
    else:
        playerEnt.gmQueryEquip(superUser, itemId, equipId)


# --- 2026-10-09 迁自 OPERATION.py line 606-615 (EQUIPMENT_DEDUCTION) ---
@gm_cmd('$gmDeductEquip', (Player("gbId or Id", raw=True), Int("itemId"), Int("EquipID"), ), RARG(0), BASE, '扣除装备，装身上的会卸下', ALLSIDE,
        GOD_GROUPS)
def gmDeductEquip(superUser, playerEnt, itemId, equipId):
    if gameconfig.isCrossServer():
        superUser.onCommandResult(-1, '执行失败, 跨服禁止执行', {"ec": -3})
    elif gmCommand.isRawPlayer(playerEnt):
        superUser.onCommandResult(-1, '执行失败, 玩家不在线', {"ec": -2})
    else:
        playerEnt.gmDeductEquip(superUser, itemId, equipId)


# --- 2026-10-09 迁自 OPERATION.py line 639-662 (MONTH_CARD_DEDUCTION) ---
@gm_cmd('$gmDeductMonthCard', (Player("gbId or Id", raw=True), Int("monthCardId 1大月卡2小月卡"), Int("seconds 扣除秒数")), RARG(0), BASE, '扣除月卡时间', ALLSIDE,
        GOD_GROUPS)
def gmDeductMonthCard(su, playerEnt, monthCardId, seconds):
    LOG_INFO('gmDeductMonthCard', playerEnt, monthCardId, seconds)
    if gameconfig.isCrossServer():
        su.onCommandResult(-1, '执行失败, 跨服禁止执行', {"ec": -3})
        return
    if monthCardId not in gameconst.PremiumType.VALID_TYPES:
        su.onCommandResult(-1, '执行失败, 月卡类型错误(1大月卡 2小月卡)', {"ec": -1, "monthCardId": monthCardId})
        return
    if seconds <= 0:
        su.onCommandResult(-1, '执行失败, 扣除秒数必须大于0', {"ec": -1, "seconds": seconds})
        return

    if gmCommand.isRawPlayer(playerEnt):
        gbId, name, accountName, dbId = playerEnt
        gamesql.recordAvatarOfflineCallback(gbId, 'gmDeductMonthCard', (monthCardId, seconds))
        su.onCommandResult(0, 'command success', {"ec": 0, "offline": 1, "gbId": gbId, "monthCardId": monthCardId, "seconds": seconds})
    else:
        ok, oldExpire, newExpire = playerEnt.gmDeductMonthCard(monthCardId, seconds)
        if not ok:
            su.onCommandResult(-1, '执行失败, 月卡已过期', {"ec": -4, "gbId": playerEnt.gbID, "monthCardId": monthCardId, "oldExpire": oldExpire})
            return
        su.onCommandResult(0, 'command success', {"ec": 0, "offline": 0, "gbId": playerEnt.gbID, "monthCardId": monthCardId, "seconds": seconds, "oldExpire": oldExpire, "newExpire": newExpire})

# --- 2026-10-09 迁自 MISC.py line 1848-1858 (ROLE_FORCE_RENAME) ---
@gm_cmd('$modifyName', (Player("gbId or Id", raw=True), Str('newName')), RARG(0), BASE, '改名', ALLSIDE, GOD_GROUPS)
def gm_modifyName(su, playerEnt, newName):
    LOG_INFO('in gm_modifyName:', playerEnt, newName)
    if gmCommand.isRawPlayer(playerEnt):
        gbId, name, accountName, dbId = playerEnt
        gamesql.recordAvatarOfflineCallback(gbId, 'IDIPModifyName', (newName,))
    else:
        playerEnt.IDIPModifyName(newName)

    su.onCommandResult(0, 'command success', {})
    return True, 'command success'

# --- 2026-10-09 迁自 OPERATION.py line 678-699 (SAFE_BOX_ITEM_DEDUCTION) ---
@gm_cmd('$gmDeleteSafeBoxItem', (Player("gbId or Id", raw=True), Str('orderId')), RARG(0), BASE, '删除保险箱', ALLSIDE, DEVE_GROUPS)
def gmDeleteSafeBoxItem(su, player, orderId):
    LOG_INFO('deleteSafeBoxItem', player, orderId)
    if gmCommand.isRawPlayer(player):
        gbId, name, accountName, dbId = player
        def onCheckSafeBoxExistsResult(ret, num, insertId, err, gbId, orderId):
            if err:
                su.onCommandResult(-1, 'db error', {"gbId":gbId, "orderId": orderId})
                return
            if ret:
                su.onCommandResult(0, 'command success', {"gbId":gbId, "orderId": orderId})
                gamesql.recordAvatarOfflineCallback(gbId, 'deleteSafeBoxItemOffline', (orderId, int(ret[0][0])))
                return
            su.onCommandResult(-2, 'order id is not existed', {"gbId":gbId, "orderId": orderId})
        
        gamesql.checkSafeBoxExists(
            orderId,
            lambda ret, num, insertId, err, gbId=gbId, orderId=orderId:
                onCheckSafeBoxExistsResult(ret, num, insertId, err, gbId, orderId))
    else:
        player.gmDeleteSafeBoxItem(su, orderId)


# --- 2026-10-09 迁自 OPERATION.py line 421-432 (ROLE_CONTROL_STATUS_QUERY) ---
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

# --- 2026-10-09 迁自 OPERATION.py line 374-383 (MAIL_TAG_BAN) ---
@gm_cmd('$banMail', (Player("gbId or Id", raw=True), Int('endTime'), Int('banType')), RARG(0), BASE, '封禁邮件', ALLSIDE, DEVE_GROUPS)
def banMail(su, player, endTime, banType):
    LOG_INFO('banMail', player, endTime, banType)
    _args = (utils.curTS(), endTime, banType)
    if gmCommand.isRawPlayer(player):
        gbId, name, accountName, dbId = player
        gamesql.recordAvatarOfflineCallback(gbId, 'gmBanMail', _args)
    else:
        player.gmBanMail(*_args)
    return True, 'command success'

# --- 2026-10-09 迁自 OPERATION.py line 434-438 (WHITELIST_ADD) ---
@gm_cmd('$addWhite', (Str('accountName'),), RONE, BASE, '添加白名单', ALLSIDE, DEVE_GROUPS)
def addWhite(su, accountName):
    LOG_INFO('addWhite', accountName)
    gamesql.addAccountWhiteList(accountName.split(','))
    return True, 'command success'

# --- 2026-10-09 迁自 OPERATION.py line 440-444 (WHITELIST_DELETE) ---
@gm_cmd('$deleteWhite', (Str('accountName'),), RONE, BASE, '移除白名单', ALLSIDE, DEVE_GROUPS)
def deleteWhite(su, accountName):
    LOG_INFO('deleteWhite', accountName)
    gamesql.deleteAccountWhiteList(accountName.split(','))
    return True, 'command success'

# --- 2026-10-09 迁自 OPERATION.py line 451-463 (EQUIP_SOUL_SEND) ---
@gm_cmd('$sendEquipSoul', (Str("toGBID"), Int("itemId"), Int("bindType"), Str("rollProps")), RONE, BASE, '向指定玩家发一封邮件', ALLSIDE, DEVE_GROUPS)
def gm_sendEquipSoul(superUser, toGBID, itemId, bindType, rollProps):
    _toGBID = int(toGBID)
    _addVal = dropAward.MailAttachVal()
    rollProps = json.loads(rollProps)
    item = itemFactory.ItemFactory.createItem(itemId, 1, bindType, rollProps=rollProps)
    _addVal.addWealthByObjList([item])
    opUUID = KBEngine.genUUID64()
    mailAssistor.sendMailToPlayers([_toGBID], 37002017, extraAttach=_addVal,
                                    srcType=AAC_AACDD.datas.BONUS_SRC_GM, opUUID=opUUID)
    return True, 'command success'

@gm_cmd('$gmAddBindYuanBao', (Player("gbId or Id", raw=True), Int("count 道具数量")), RARG(0), BASE, '增加绑定元宝', ALLSIDE, GOD_GROUPS)
def gmAddBindYuanBao(su, player, count):
    LOG_INFO('gmAddBindYuanBao', player, gameconst.ItemIdEnum.BIND_MONEY, count)
    if gameconfig.isCrossServer():
        su.onCommandResult(-1, '执行失败, 跨服禁止执行gmAddBindYuanBao', {"errCode": -1, "offline": 0, "gbId": 0, "count": count})
        return

    if count <= 0:
        su.onCommandResult(-1, '执行失败, 数量不合法', {"errCode": -2, "offline": 0, "gbId": 0, "count": count})
        return
    
    detail = 'gm_cmd:$gmAddBindYuanBao %s %s %s' % (gameconst.ItemIdEnum.BIND_MONEY, count, gameconst.ItemBindType.BIND)
    if gmCommand.isRawPlayer(player):
        gbId, name, accountName, dbId = player
        gamesql.recordAvatarOfflineCallback(gbId, 'gmAddItems', (0, gameconst.ItemIdEnum.BIND_MONEY, count, detail, gameconst.ItemBindType.BIND))
        su.onCommandResult(0, '执行成功', {"errCode": 0, "offline": 1, "gbId": gbId, "count": count})
    else:
        player.gmAddItems(0, gameconst.ItemIdEnum.BIND_MONEY, count, detail, gameconst.ItemBindType.BIND)
        su.onCommandResult(0, '执行成功', {"errCode": 0, "offline": 0, "gbId": player.gbID, "count": count})

@gm_cmd('$gmSetPromoter', (PlayerAccount("accountName", raw=True), Int("cdTime 特权有效期")), RARG(0), BASE, '给账号设置推广者权限', ALLSIDE, GOD_GROUPS)
def gmSetPromoter(su, account, cdTime):
    LOG_INFO('gmSetPromoter', account, cdTime)
    if gameconfig.isCrossServer():
        su.onCommandResult(-1, '执行失败, 跨服禁止执行gmSetPromoter', {"errCode": -1, "offline": 0, "account": '', "cdTime": cdTime})
        return

    if cdTime <= utils.curTS():
        su.onCommandResult(-1, '执行失败, cd时间不合法', {"errCode": -2, "offline": 0, "account": '', "cdTime": cdTime})
        return
    
    if type(account) is str:
        gamesql.recordAccountOfflineCallback(account, 'gmSetPromoter', (cdTime, True))
        su.onCommandResult(0, '执行成功', {"errCode": 0, "offline": 1, "account": account, "cdTime": cdTime})
    else:
        account.gmSetPromoter(cdTime, False)
        su.onCommandResult(0, '执行成功', {"errCode": 0, "offline": 0, "account": account.accountName, "cdTime": cdTime})

@gm_cmd('$setEquipEnhance', (Player("gbId or Id", raw=True), Int("itemId"), Int("EquipID"), Int("enhanceLv 目标强化等级"), Int("bindEnhanceCost 强化绑定值,-1不修改"), Int("syncMaxLv 回退时是否同步下调历史最高强化等级,0否1是")), RARG(0), BASE, '设置装备强化等级和强化绑定值(背包/仓库/身上)', ALLSIDE,
        GOD_GROUPS, minArgs=4)
def gmSetEquipEnhance(su, playerEnt, itemId, equipId, enhanceLv, bindEnhanceCost=-1, syncMaxLv=0):
    LOG_INFO('gmSetEquipEnhance', playerEnt, itemId, equipId, enhanceLv, bindEnhanceCost, syncMaxLv)
    if gameconfig.isCrossServer():
        su.onCommandResult(gameconst.GMCommandErr.GM_RET_CROSS_SERVER_FORBIDDEN, '执行失败, 跨服禁止执行', {"ec": gameconst.GMCommandErr.GM_RET_CROSS_SERVER_FORBIDDEN})
        return
    if not dataUtils.isEquipItemByItemId(itemId):
        su.onCommandResult(gameconst.GMCommandErr.GM_RET_ARGS_ERR, '执行失败, 装备不存在', {"ec": gameconst.GMCommandErr.GM_RET_ARGS_ERR, "itemId": itemId})
        return
    if enhanceLv < 0:
        su.onCommandResult(gameconst.GMCommandErr.GM_RET_ARGS_ERR, '执行失败, 强化等级不能小于0', {"ec": gameconst.GMCommandErr.GM_RET_ARGS_ERR, "enhanceLv": enhanceLv})
        return

    if gmCommand.isRawPlayer(playerEnt):
        su.onCommandResult(gameconst.GMCommandErr.GM_RET_TARGET_OFFLINE, '执行失败, 玩家不在线', {"ec": gameconst.GMCommandErr.GM_RET_TARGET_OFFLINE})
    else:
        playerEnt.gmSetEquipEnhance(su, itemId, equipId, enhanceLv, bindEnhanceCost, syncMaxLv)

@gm_cmd('$setEquipGrade', (Player("gbId or Id", raw=True), Int("itemId"), Int("EquipID"), Int("grade 目标升阶等级"), Int("bindValue 升阶绑定值,-1不修改")), RARG(0), BASE, '设置装备升阶等级和升阶绑定值(背包/仓库/身上)', ALLSIDE,
        GOD_GROUPS, minArgs=4)
def gmSetEquipGrade(su, playerEnt, itemId, equipId, grade, bindValue=-1):
    LOG_INFO('gmSetEquipGrade', playerEnt, itemId, equipId, grade, bindValue)
    if gameconfig.isCrossServer():
        su.onCommandResult(gameconst.GMCommandErr.GM_RET_CROSS_SERVER_FORBIDDEN, '执行失败, 跨服禁止执行', {"ec": gameconst.GMCommandErr.GM_RET_CROSS_SERVER_FORBIDDEN})
        return
    if not dataUtils.isEquipItemByItemId(itemId):
        su.onCommandResult(gameconst.GMCommandErr.GM_RET_ARGS_ERR, '执行失败, 装备不存在', {"ec": gameconst.GMCommandErr.GM_RET_ARGS_ERR, "itemId": itemId})
        return
    if grade < 1:
        su.onCommandResult(gameconst.GMCommandErr.GM_RET_ARGS_ERR, '执行失败, 升阶等级不能小于1', {"ec": gameconst.GMCommandErr.GM_RET_ARGS_ERR, "grade": grade})
        return

    if gmCommand.isRawPlayer(playerEnt):
        su.onCommandResult(gameconst.GMCommandErr.GM_RET_TARGET_OFFLINE, '执行失败, 玩家不在线', {"ec": gameconst.GMCommandErr.GM_RET_TARGET_OFFLINE})
    else:
        playerEnt.gmSetEquipGrade(su, itemId, equipId, grade, bindValue)

@gm_cmd('$setEquipSpirit', (Player("gbId or Id", raw=True), Int("itemId"), Int("EquipID"), Int("spiritPos 附灵槽位(组)序号"), Str("affixIds 词缀列表,格式affixId:affixVal逗号分隔,空串清空该槽位"), Int("bindType 槽位绑定状态,-1不修改,0非绑,1绑定")), RARG(0), BASE, '设置装备附灵词缀和附灵绑定状态(背包/仓库/身上)', ALLSIDE,
        GOD_GROUPS, minArgs=5)
def gmSetEquipSpirit(su, playerEnt, itemId, equipId, spiritPos, affixIds, bindType=-1):
    LOG_INFO('gmSetEquipSpirit', playerEnt, itemId, equipId, spiritPos, affixIds, bindType)
    if gameconfig.isCrossServer():
        su.onCommandResult(gameconst.GMCommandErr.GM_RET_CROSS_SERVER_FORBIDDEN, '执行失败, 跨服禁止执行', {"ec": gameconst.GMCommandErr.GM_RET_CROSS_SERVER_FORBIDDEN})
        return
    if not dataUtils.isEquipItemByItemId(itemId):
        su.onCommandResult(gameconst.GMCommandErr.GM_RET_ARGS_ERR, '执行失败, 装备不存在', {"ec": gameconst.GMCommandErr.GM_RET_ARGS_ERR, "itemId": itemId})
        return
    if spiritPos < 0:
        su.onCommandResult(gameconst.GMCommandErr.GM_RET_ARGS_ERR, '执行失败, 附灵槽位序号不能小于0', {"ec": gameconst.GMCommandErr.GM_RET_ARGS_ERR, "spiritPos": spiritPos})
        return
    if bindType not in (-1, gameconst.ItemBindType.NORMAL, gameconst.ItemBindType.BIND):
        su.onCommandResult(gameconst.GMCommandErr.GM_RET_ARGS_ERR, '执行失败, 绑定状态不合法', {"ec": gameconst.GMCommandErr.GM_RET_ARGS_ERR, "bindType": bindType})
        return

    if gmCommand.isRawPlayer(playerEnt):
        su.onCommandResult(gameconst.GMCommandErr.GM_RET_TARGET_OFFLINE, '执行失败, 玩家不在线', {"ec": gameconst.GMCommandErr.GM_RET_TARGET_OFFLINE})
    else:
        playerEnt.gmSetEquipSpirit(su, itemId, equipId, spiritPos, affixIds, bindType)

@gm_cmd('$setEquipGlyph', (Player("gbId or Id", raw=True), Int("itemId"), Int("EquipID"), Int("glyphPos 铭文槽位"), Str("affixIds 词缀列表,格式affixId:affixVal逗号分隔,空串清空该槽位"), Int("bindType 槽位绑定状态,-1不修改,0非绑,1绑定")), RARG(0), BASE, '设置装备铭文词缀和铭文绑定状态(背包/仓库/身上)', ALLSIDE,
        GOD_GROUPS, minArgs=5)
def gmSetEquipGlyph(su, playerEnt, itemId, equipId, glyphPos, affixIds, bindType=-1):
    LOG_INFO('gmSetEquipGlyph', playerEnt, itemId, equipId, glyphPos, affixIds, bindType)
    if gameconfig.isCrossServer():
        su.onCommandResult(gameconst.GMCommandErr.GM_RET_CROSS_SERVER_FORBIDDEN, '执行失败, 跨服禁止执行', {"ec": gameconst.GMCommandErr.GM_RET_CROSS_SERVER_FORBIDDEN})
        return
    if not dataUtils.isEquipItemByItemId(itemId):
        su.onCommandResult(gameconst.GMCommandErr.GM_RET_ARGS_ERR, '执行失败, 装备不存在', {"ec": gameconst.GMCommandErr.GM_RET_ARGS_ERR, "itemId": itemId})
        return
    if glyphPos < 0:
        su.onCommandResult(gameconst.GMCommandErr.GM_RET_ARGS_ERR, '执行失败, 铭文槽位不能小于0', {"ec": gameconst.GMCommandErr.GM_RET_ARGS_ERR, "glyphPos": glyphPos})
        return
    if bindType not in (-1, gameconst.ItemBindType.NORMAL, gameconst.ItemBindType.BIND):
        su.onCommandResult(gameconst.GMCommandErr.GM_RET_ARGS_ERR, '执行失败, 绑定状态不合法', {"ec": gameconst.GMCommandErr.GM_RET_ARGS_ERR, "bindType": bindType})
        return

    if gmCommand.isRawPlayer(playerEnt):
        su.onCommandResult(gameconst.GMCommandErr.GM_RET_TARGET_OFFLINE, '执行失败, 玩家不在线', {"ec": gameconst.GMCommandErr.GM_RET_TARGET_OFFLINE})
    else:
        playerEnt.gmSetEquipGlyph(su, itemId, equipId, glyphPos, affixIds, bindType)

@gm_cmd('$setEquipBless', (Player("gbId or Id", raw=True), Int("itemId"), Int("EquipID"), Int("luckyVal 目标幸运值"), Int("maxBlessLv 历史最高幸运值,-1不修改"), Int("blessLvRate 保底回溯进度,-1不修改"), Int("bindBlessCost 祝福绑定值,-1不修改")), RARG(0), BASE, '设置装备祝福幸运值/历史最高/保底进度/绑定值(背包/仓库/身上)', ALLSIDE,
        GOD_GROUPS, minArgs=4)
def gmSetEquipBless(su, playerEnt, itemId, equipId, luckyVal, maxBlessLv=-1, blessLvRate=-1, bindBlessCost=-1):
    LOG_INFO('gmSetEquipBless', playerEnt, itemId, equipId, luckyVal, maxBlessLv, blessLvRate, bindBlessCost)
    if gameconfig.isCrossServer():
        su.onCommandResult(gameconst.GMCommandErr.GM_RET_CROSS_SERVER_FORBIDDEN, '执行失败, 跨服禁止执行', {"ec": gameconst.GMCommandErr.GM_RET_CROSS_SERVER_FORBIDDEN})
        return
    if not dataUtils.isEquipItemByItemId(itemId):
        su.onCommandResult(gameconst.GMCommandErr.GM_RET_ARGS_ERR, '执行失败, 装备不存在', {"ec": gameconst.GMCommandErr.GM_RET_ARGS_ERR, "itemId": itemId})
        return
    if luckyVal < 0:
        su.onCommandResult(gameconst.GMCommandErr.GM_RET_ARGS_ERR, '执行失败, 幸运值不能小于0', {"ec": gameconst.GMCommandErr.GM_RET_ARGS_ERR, "luckyVal": luckyVal})
        return

    if gmCommand.isRawPlayer(playerEnt):
        su.onCommandResult(gameconst.GMCommandErr.GM_RET_TARGET_OFFLINE, '执行失败, 玩家不在线', {"ec": gameconst.GMCommandErr.GM_RET_TARGET_OFFLINE})
    else:
        playerEnt.gmSetEquipBless(su, itemId, equipId, luckyVal, maxBlessLv, blessLvRate, bindBlessCost)

@gm_cmd('$deductExp', (Player("gbId or Id", raw=True), Int("deductVal 扣除数量, 传负数等于加经验(会先抵偿经验负债)")), RARG(0), BASE, '扣除玩家经验, 当前经验不足部分记入经验负债(仅支持在线玩家)', ALLSIDE,
        GOD_GROUPS)
def gmDeductExp(su, playerEnt, deductVal):
    LOG_INFO('gmDeductExp', deductVal)
    if gameconfig.isCrossServer():
        su.onCommandResult(gameconst.GMCommandErr.GM_RET_CROSS_SERVER_FORBIDDEN, '执行失败, 跨服禁止执行, 请回本服执行', {"ec": gameconst.GMCommandErr.GM_RET_CROSS_SERVER_FORBIDDEN})
        return
    if deductVal == 0:
        su.onCommandResult(gameconst.GMCommandErr.GM_RET_ARGS_ERR, '执行失败, 扣除数量不能为0', {"ec": gameconst.GMCommandErr.GM_RET_ARGS_ERR, "deductVal": deductVal})
        return
    if gmCommand.isRawPlayer(playerEnt):
        su.onCommandResult(gameconst.GMCommandErr.GM_RET_TARGET_OFFLINE, '执行失败, 玩家不在线', {"ec": gameconst.GMCommandErr.GM_RET_TARGET_OFFLINE})
        return

    opUUID = KBEngine.genUUID64()
    detail = 'gm_cmd:$deductExp deductVal=%s' % (deductVal,)
    playerEnt.cell.gmDeductExp(deductVal, opUUID, AAC_AACDD.datas.BONUS_SRC_GM, detail)
    su.onCommandResult(gameconst.GMCommandErr.GM_RET_OK, 'command success', {"ec": gameconst.GMCommandErr.GM_RET_OK, "gbId": playerEnt.gbID, "deductVal": deductVal})

@gm_cmd('$setPetEquip', (Player("gbId or Id", raw=True), Int("petId 精灵id"), Int("slotId 装备槽位"), Int("itemId 精灵装备itemId,0表示卸下")), RARG(0), BASE, '设置精灵穿戴装备(不经背包,跳过换装规则;注意:该指令生成的装备之后走回收会发进背包)', ALLSIDE,
        GOD_GROUPS)
def gmSetPetEquip(su, playerEnt, petId, slotId, itemId):
    LOG_INFO('gmSetPetEquip', playerEnt, petId, slotId, itemId)
    if gameconfig.isCrossServer():
        su.onCommandResult(gameconst.GMCommandErr.GM_RET_CROSS_SERVER_FORBIDDEN, '执行失败, 跨服禁止执行', {"ec": gameconst.GMCommandErr.GM_RET_CROSS_SERVER_FORBIDDEN})
        return
    if petId not in PDPD.datas:
        su.onCommandResult(gameconst.GMCommandErr.GM_RET_ARGS_ERR, '执行失败, 精灵id不存在', {"ec": gameconst.GMCommandErr.GM_RET_ARGS_ERR, "petId": petId})
        return
    gearNum = dataUtils.getPetGearNum(petId)
    if slotId < 0 or slotId >= gearNum:
        su.onCommandResult(gameconst.GMCommandErr.GM_RET_ARGS_ERR, '执行失败, 装备槽位越界', {"ec": gameconst.GMCommandErr.GM_RET_ARGS_ERR, "petId": petId, "slotId": slotId, "gearNum": gearNum})
        return
    if itemId != 0 and itemId not in PDPGD.datas:
        su.onCommandResult(gameconst.GMCommandErr.GM_RET_ARGS_ERR, '执行失败, 精灵装备itemId不存在', {"ec": gameconst.GMCommandErr.GM_RET_ARGS_ERR, "petId": petId, "itemId": itemId})
        return

    if gmCommand.isRawPlayer(playerEnt):
        su.onCommandResult(gameconst.GMCommandErr.GM_RET_TARGET_OFFLINE, '执行失败, 玩家不在线', {"ec": gameconst.GMCommandErr.GM_RET_TARGET_OFFLINE})
    else:
        ok, oldItemId, errMsg = playerEnt.gmSetPetEquip(petId, slotId, itemId)
        if not ok:
            su.onCommandResult(gameconst.GMCommandErr.GM_RET_ARGS_ERR, '执行失败, %s' % errMsg, {"ec": gameconst.GMCommandErr.GM_RET_ARGS_ERR, "gbId": playerEnt.gbID, "petId": petId, "slotId": slotId, "itemId": itemId})
            return
        su.onCommandResult(gameconst.GMCommandErr.GM_RET_OK, 'command success', {"ec": gameconst.GMCommandErr.GM_RET_OK, "offline": 0, "gbId": playerEnt.gbID, "petId": petId, "slotId": slotId, "itemId": itemId, "oldItemId": oldItemId})

@gm_cmd('$setPetLevelExp', (Player("gbId or Id", raw=True), Int("petId 精灵id"), Int("level 目标等级"), Int("exp 目标经验,满级时强制为0")), RARG(0), BASE, '设置精灵等级和经验(支持降级)', ALLSIDE,
        GOD_GROUPS)
def gmSetPetLevelExp(su, playerEnt, petId, level, exp):
    LOG_INFO('gmSetPetLevelExp', playerEnt, petId, level, exp)
    if gameconfig.isCrossServer():
        su.onCommandResult(gameconst.GMCommandErr.GM_RET_CROSS_SERVER_FORBIDDEN, '执行失败, 跨服禁止执行', {"ec": gameconst.GMCommandErr.GM_RET_CROSS_SERVER_FORBIDDEN})
        return
    if petId not in PDPD.datas:
        su.onCommandResult(gameconst.GMCommandErr.GM_RET_ARGS_ERR, '执行失败, 精灵id不存在', {"ec": gameconst.GMCommandErr.GM_RET_ARGS_ERR, "petId": petId})
        return
    leveUpExps = dataUtils.getPetLevelUpExp(petId)
    if not leveUpExps:
        su.onCommandResult(gameconst.GMCommandErr.GM_RET_ARGS_ERR, '执行失败, 精灵升级经验配置缺失', {"ec": gameconst.GMCommandErr.GM_RET_ARGS_ERR, "petId": petId})
        return
    petMinLevel = int(PDSD.datas['petMinLevel']['value'])
    topLevel = min(int(PDSD.datas['petMaxLevel']['value']), len(leveUpExps) + 1)
    if level < petMinLevel or level > topLevel:
        su.onCommandResult(gameconst.GMCommandErr.GM_RET_ARGS_ERR, '执行失败, 等级超出范围', {"ec": gameconst.GMCommandErr.GM_RET_ARGS_ERR, "petId": petId, "level": level, "minLevel": petMinLevel, "maxLevel": topLevel})
        return
    if level < topLevel and (exp < 0 or exp >= leveUpExps[level - 1]):
        su.onCommandResult(gameconst.GMCommandErr.GM_RET_ARGS_ERR, '执行失败, 经验超出当前级上限', {"ec": gameconst.GMCommandErr.GM_RET_ARGS_ERR, "petId": petId, "level": level, "exp": exp, "levelUpExp": leveUpExps[level - 1]})
        return

    if gmCommand.isRawPlayer(playerEnt):
        su.onCommandResult(gameconst.GMCommandErr.GM_RET_TARGET_OFFLINE, '执行失败, 玩家不在线', {"ec": gameconst.GMCommandErr.GM_RET_TARGET_OFFLINE})
    else:
        ok, oldLevel, oldExp, newLevel, newExp, errMsg = playerEnt.gmSetPetLevelExp(petId, level, exp)
        if not ok:
            su.onCommandResult(gameconst.GMCommandErr.GM_RET_ARGS_ERR, '执行失败, %s' % errMsg, {"ec": gameconst.GMCommandErr.GM_RET_ARGS_ERR, "gbId": playerEnt.gbID, "petId": petId, "level": level, "exp": exp})
            return
        su.onCommandResult(gameconst.GMCommandErr.GM_RET_OK, 'command success', {"ec": gameconst.GMCommandErr.GM_RET_OK, "offline": 0, "gbId": playerEnt.gbID, "petId": petId, "oldLevel": oldLevel, "oldExp": oldExp, "newLevel": newLevel, "newExp": newExp})

@gm_cmd('$deductPetExp', (Player("gbId or Id", raw=True), Int("petId 精灵id"), Int("exp 扣除经验值,不足时自动降级,最低降到1级0经验")), RARG(0), BASE, '扣除精灵经验(支持降级)', ALLSIDE,
        GOD_GROUPS)
def gmDeductPetExp(su, playerEnt, petId, exp):
    LOG_INFO('gmDeductPetExp', playerEnt, petId, exp)
    if gameconfig.isCrossServer():
        su.onCommandResult(gameconst.GMCommandErr.GM_RET_CROSS_SERVER_FORBIDDEN, '执行失败, 跨服禁止执行', {"ec": gameconst.GMCommandErr.GM_RET_CROSS_SERVER_FORBIDDEN})
        return
    if petId not in PDPD.datas:
        su.onCommandResult(gameconst.GMCommandErr.GM_RET_ARGS_ERR, '执行失败, 精灵id不存在', {"ec": gameconst.GMCommandErr.GM_RET_ARGS_ERR, "petId": petId})
        return
    if exp <= 0:
        su.onCommandResult(gameconst.GMCommandErr.GM_RET_ARGS_ERR, '执行失败, 扣除经验必须大于0', {"ec": gameconst.GMCommandErr.GM_RET_ARGS_ERR, "petId": petId, "exp": exp})
        return

    if gmCommand.isRawPlayer(playerEnt):
        su.onCommandResult(gameconst.GMCommandErr.GM_RET_TARGET_OFFLINE, '执行失败, 玩家不在线', {"ec": gameconst.GMCommandErr.GM_RET_TARGET_OFFLINE})
    else:
        ok, oldLevel, oldExp, newLevel, newExp, errMsg = playerEnt.gmDeductPetExp(petId, exp)
        if not ok:
            su.onCommandResult(gameconst.GMCommandErr.GM_RET_ARGS_ERR, '执行失败, %s' % errMsg, {"ec": gameconst.GMCommandErr.GM_RET_ARGS_ERR, "gbId": playerEnt.gbID, "petId": petId, "exp": exp})
            return
        su.onCommandResult(gameconst.GMCommandErr.GM_RET_OK, 'command success', {"ec": gameconst.GMCommandErr.GM_RET_OK, "offline": 0, "gbId": playerEnt.gbID, "petId": petId, "oldLevel": oldLevel, "oldExp": oldExp, "newLevel": newLevel, "newExp": newExp})

@gm_cmd('$deactivatePet', (Player("gbId or Id", raw=True), Int("petId 精灵id")), RARG(0), BASE, '反激活精灵(精灵及其穿戴装备一并移除,装备不返还;依赖客户端onRemoveLingShou协议)', ALLSIDE,
        GOD_GROUPS)
def gmDeactivatePet(su, playerEnt, petId):
    LOG_INFO('gmDeactivatePet', playerEnt, petId)
    if gameconfig.isCrossServer():
        su.onCommandResult(gameconst.GMCommandErr.GM_RET_CROSS_SERVER_FORBIDDEN, '执行失败, 跨服禁止执行', {"ec": gameconst.GMCommandErr.GM_RET_CROSS_SERVER_FORBIDDEN})
        return
    if petId not in PDPD.datas:
        su.onCommandResult(gameconst.GMCommandErr.GM_RET_ARGS_ERR, '执行失败, 精灵id不存在', {"ec": gameconst.GMCommandErr.GM_RET_ARGS_ERR, "petId": petId})
        return

    if gmCommand.isRawPlayer(playerEnt):
        su.onCommandResult(gameconst.GMCommandErr.GM_RET_TARGET_OFFLINE, '执行失败, 玩家不在线', {"ec": gameconst.GMCommandErr.GM_RET_TARGET_OFFLINE})
    else:
        ok, oldLevel, oldEquipList, errMsg = playerEnt.gmDeactivatePet(petId)
        if not ok:
            su.onCommandResult(gameconst.GMCommandErr.GM_RET_ARGS_ERR, '执行失败, %s' % errMsg, {"ec": gameconst.GMCommandErr.GM_RET_ARGS_ERR, "gbId": playerEnt.gbID, "petId": petId})
            return
        # 踢下线
        playerEnt.destroySelf(gameconst.OFFLINE_REASON_GMKICK)
        su.onCommandResult(gameconst.GMCommandErr.GM_RET_OK, 'command success', {"ec": gameconst.GMCommandErr.GM_RET_OK, "offline": 0, "gbId": playerEnt.gbID, "petId": petId, "oldLevel": oldLevel, "oldEquipList": oldEquipList})

@gm_cmd('$gmSetMeridianSlot', (Player("gbId or Id", raw=True), Int("slotId 目标经脉层数1~21, 21表示全部贯通")), RARG(0), BASE, '设置经脉层数(低于目标层的穴位全满并贯通, 目标层0级未贯通, 更高层删除;仅支持在线玩家)', ALLSIDE,
        GOD_GROUPS)
def gmSetMeridianSlot(su, playerEnt, slotId):
    LOG_INFO('gmSetMeridianSlot', playerEnt, slotId)
    if gameconfig.isCrossServer():
        su.onCommandResult(gameconst.GMCommandErr.GM_RET_CROSS_SERVER_FORBIDDEN, '执行失败, 跨服禁止执行', {"ec": gameconst.GMCommandErr.GM_RET_CROSS_SERVER_FORBIDDEN})
        return

    if gmCommand.isRawPlayer(playerEnt):
        su.onCommandResult(gameconst.GMCommandErr.GM_RET_TARGET_OFFLINE, '执行失败, 玩家不在线', {"ec": gameconst.GMCommandErr.GM_RET_TARGET_OFFLINE})
    else:
        ok, errMsg = playerEnt.gmSetMeridianSlot(slotId)
        if not ok:
            su.onCommandResult(gameconst.GMCommandErr.GM_RET_ARGS_ERR, '执行失败, %s' % errMsg, {"ec": gameconst.GMCommandErr.GM_RET_ARGS_ERR, "gbId": playerEnt.gbID, "slotId": slotId})
            return
        su.onCommandResult(gameconst.GMCommandErr.GM_RET_OK, 'command success', {"ec": gameconst.GMCommandErr.GM_RET_OK, "offline": 0, "gbId": playerEnt.gbID, "slotId": slotId})

@gm_cmd('$gmSetMeridianPoint', (Player("gbId or Id", raw=True), Int("slotId 经脉层数"), Int("pointId 穴位1~8"), Int("level 穴位等级0~5")), RARG(0), BASE, '设置指定经脉穴位等级(支持降级;已贯通经脉不允许降低穴位等级,请先用$gmSetMeridianSlot整层回退;仅支持在线玩家)', ALLSIDE,
        GOD_GROUPS)
def gmSetMeridianPoint(su, playerEnt, slotId, pointId, level):
    LOG_INFO('gmSetMeridianPoint', playerEnt, slotId, pointId, level)
    if gameconfig.isCrossServer():
        su.onCommandResult(gameconst.GMCommandErr.GM_RET_CROSS_SERVER_FORBIDDEN, '执行失败, 跨服禁止执行', {"ec": gameconst.GMCommandErr.GM_RET_CROSS_SERVER_FORBIDDEN})
        return

    if gmCommand.isRawPlayer(playerEnt):
        su.onCommandResult(gameconst.GMCommandErr.GM_RET_TARGET_OFFLINE, '执行失败, 玩家不在线', {"ec": gameconst.GMCommandErr.GM_RET_TARGET_OFFLINE})
    else:
        ok, errMsg = playerEnt.gmSetMeridianPoint(slotId, pointId, level)
        if not ok:
            su.onCommandResult(gameconst.GMCommandErr.GM_RET_ARGS_ERR, '执行失败, %s' % errMsg, {"ec": gameconst.GMCommandErr.GM_RET_ARGS_ERR, "gbId": playerEnt.gbID, "slotId": slotId, "pointId": pointId, "level": level})
            return
        su.onCommandResult(gameconst.GMCommandErr.GM_RET_OK, 'command success', {"ec": gameconst.GMCommandErr.GM_RET_OK, "offline": 0, "gbId": playerEnt.gbID, "slotId": slotId, "pointId": pointId, "level": level})

@gm_cmd('$gmResetMeridian', (Player("gbId or Id", raw=True),), RARG(0), BASE, '重置经脉系统(回退全部经脉属性与评分;仅支持在线玩家)', ALLSIDE,
        GOD_GROUPS)
def gmResetMeridian(su, playerEnt):
    LOG_INFO('gmResetMeridian', playerEnt)
    if gameconfig.isCrossServer():
        su.onCommandResult(gameconst.GMCommandErr.GM_RET_CROSS_SERVER_FORBIDDEN, '执行失败, 跨服禁止执行', {"ec": gameconst.GMCommandErr.GM_RET_CROSS_SERVER_FORBIDDEN})
        return

    if gmCommand.isRawPlayer(playerEnt):
        su.onCommandResult(gameconst.GMCommandErr.GM_RET_TARGET_OFFLINE, '执行失败, 玩家不在线', {"ec": gameconst.GMCommandErr.GM_RET_TARGET_OFFLINE})
    else:
        ok, errMsg = playerEnt.gmResetMeridian()
        if not ok:
            su.onCommandResult(gameconst.GMCommandErr.GM_RET_ARGS_ERR, '执行失败, %s' % errMsg, {"ec": gameconst.GMCommandErr.GM_RET_ARGS_ERR, "gbId": playerEnt.gbID})
            return
        su.onCommandResult(gameconst.GMCommandErr.GM_RET_OK, 'command success', {"ec": gameconst.GMCommandErr.GM_RET_OK, "offline": 0, "gbId": playerEnt.gbID})

@gm_cmd('$setCollectGrid', (Player("gbId or Id", raw=True), Int("collectId 收集项id"), Int("gridId 格子序号,-1表示整项"), Int("op 0清除/1完成")), RARG(0), BASE, '设置收集项格子状态(支持回退,集齐状态翻转时同步回收/补发属性;收藏位不动;仅支持在线玩家)', ALLSIDE,
        GOD_GROUPS)
def gmSetCollectGrid(su, playerEnt, collectId, gridId, op):
    LOG_INFO('gmSetCollectGrid', playerEnt, collectId, gridId, op)
    if gameconfig.isCrossServer():
        su.onCommandResult(gameconst.GMCommandErr.GM_RET_CROSS_SERVER_FORBIDDEN, '执行失败, 跨服禁止执行', {"ec": gameconst.GMCommandErr.GM_RET_CROSS_SERVER_FORBIDDEN})
        return

    if gmCommand.isRawPlayer(playerEnt):
        su.onCommandResult(gameconst.GMCommandErr.GM_RET_TARGET_OFFLINE, '执行失败, 玩家不在线', {"ec": gameconst.GMCommandErr.GM_RET_TARGET_OFFLINE})
    else:
        ok, errMsg = playerEnt.gmSetCollectGrid(collectId, gridId, op)
        if not ok:
            su.onCommandResult(gameconst.GMCommandErr.GM_RET_ARGS_ERR, '执行失败, %s' % errMsg, {"ec": gameconst.GMCommandErr.GM_RET_ARGS_ERR, "gbId": playerEnt.gbID, "collectId": collectId, "gridId": gridId, "op": op})
            return
        su.onCommandResult(gameconst.GMCommandErr.GM_RET_OK, 'command success', {"ec": gameconst.GMCommandErr.GM_RET_OK, "offline": 0, "gbId": playerEnt.gbID, "collectId": collectId, "gridId": gridId, "op": op})

@gm_cmd('$resetCollect', (Player("gbId or Id", raw=True), Int("collectId 收集项id,0表示全部")), RARG(0), BASE, '重置收集项(清掉全部进度位并回收已集齐属性;收藏位不动;仅支持在线玩家)', ALLSIDE,
        GOD_GROUPS)
def gmResetCollect(su, playerEnt, collectId):
    LOG_INFO('gmResetCollect', playerEnt, collectId)
    if gameconfig.isCrossServer():
        su.onCommandResult(gameconst.GMCommandErr.GM_RET_CROSS_SERVER_FORBIDDEN, '执行失败, 跨服禁止执行', {"ec": gameconst.GMCommandErr.GM_RET_CROSS_SERVER_FORBIDDEN})
        return

    if gmCommand.isRawPlayer(playerEnt):
        su.onCommandResult(gameconst.GMCommandErr.GM_RET_TARGET_OFFLINE, '执行失败, 玩家不在线', {"ec": gameconst.GMCommandErr.GM_RET_TARGET_OFFLINE})
    else:
        ok, errMsg = playerEnt.gmResetCollect(collectId)
        if not ok:
            su.onCommandResult(gameconst.GMCommandErr.GM_RET_ARGS_ERR, '执行失败, %s' % errMsg, {"ec": gameconst.GMCommandErr.GM_RET_ARGS_ERR, "gbId": playerEnt.gbID, "collectId": collectId})
            return
        su.onCommandResult(gameconst.GMCommandErr.GM_RET_OK, 'command success', {"ec": gameconst.GMCommandErr.GM_RET_OK, "offline": 0, "gbId": playerEnt.gbID, "collectId": collectId})

@gm_cmd('$setSkillLevel', (Player("gbId or Id", raw=True), Int("skillId 技能id(铭文替换技能需传原技能id)"), Int("targetLevel 目标等级")), RARG(0), BASE, '设置技能等级(支持回退,不返还消耗;召唤职业降级可能降低召唤槽位并击杀当前出战召唤兽;仅支持在线玩家)', ALLSIDE,
        GOD_GROUPS)
def gmSetSkillLevel(su, playerEnt, skillId, targetLevel):
    LOG_INFO('gmSetSkillLevel', playerEnt, skillId, targetLevel)
    if gameconfig.isCrossServer():
        su.onCommandResult(gameconst.GMCommandErr.GM_RET_CROSS_SERVER_FORBIDDEN, '执行失败, 跨服禁止执行', {"ec": gameconst.GMCommandErr.GM_RET_CROSS_SERVER_FORBIDDEN})
        return

    if gmCommand.isRawPlayer(playerEnt):
        su.onCommandResult(gameconst.GMCommandErr.GM_RET_TARGET_OFFLINE, '执行失败, 玩家不在线', {"ec": gameconst.GMCommandErr.GM_RET_TARGET_OFFLINE})
    else:
        ok, oldLevel, newLevel, errMsg = playerEnt.gmSetSkillLevel(skillId, targetLevel)
        if not ok:
            su.onCommandResult(gameconst.GMCommandErr.GM_RET_ARGS_ERR, '执行失败, %s' % errMsg, {"ec": gameconst.GMCommandErr.GM_RET_ARGS_ERR, "gbId": playerEnt.gbID, "skillId": skillId, "targetLevel": targetLevel})
            return
        su.onCommandResult(gameconst.GMCommandErr.GM_RET_OK, 'command success', {"ec": gameconst.GMCommandErr.GM_RET_OK, "offline": 0, "gbId": playerEnt.gbID, "skillId": skillId, "oldLevel": oldLevel, "newLevel": newLevel})

@gm_cmd('$deactiveMount', (Player("gbId or Id", raw=True), Int("mountId 坐骑id")), RARG(0), BASE, '反激活坐骑(删除记录并回退属性/评分,骑着则下骑;依赖客户端onRemoveOutfit协议;仅支持在线玩家)', ALLSIDE,
        GOD_GROUPS)
def gmDeactiveMount(su, playerEnt, mountId):
    LOG_INFO('gmDeactiveMount', playerEnt, mountId)
    if gameconfig.isCrossServer():
        su.onCommandResult(gameconst.GMCommandErr.GM_RET_CROSS_SERVER_FORBIDDEN, '执行失败, 跨服禁止执行', {"ec": gameconst.GMCommandErr.GM_RET_CROSS_SERVER_FORBIDDEN})
        return

    if gmCommand.isRawPlayer(playerEnt):
        su.onCommandResult(gameconst.GMCommandErr.GM_RET_TARGET_OFFLINE, '执行失败, 玩家不在线', {"ec": gameconst.GMCommandErr.GM_RET_TARGET_OFFLINE})
    else:
        ok, errMsg = playerEnt.gmDeactiveMount(mountId)
        if not ok:
            su.onCommandResult(gameconst.GMCommandErr.GM_RET_ARGS_ERR, '执行失败, %s' % errMsg, {"ec": gameconst.GMCommandErr.GM_RET_ARGS_ERR, "gbId": playerEnt.gbID, "mountId": mountId})
            return
        # 踢下线
        playerEnt.destroySelf(gameconst.OFFLINE_REASON_GMKICK)
        su.onCommandResult(gameconst.GMCommandErr.GM_RET_OK, 'command success', {"ec": gameconst.GMCommandErr.GM_RET_OK, "offline": 0, "gbId": playerEnt.gbID, "mountId": mountId})

@gm_cmd('$deactiveOutfit', (Player("gbId or Id", raw=True), Int("outfitType 外观类型1翅膀2发型3衣服4头像框"), Int("outfitId 外观id")), RARG(0), BASE, '反激活外观(若正穿戴则卸下,同步回收关联外观属性;依赖客户端onRemoveOutfit协议;仅支持在线玩家)', ALLSIDE,
        GOD_GROUPS)
def gmDeactiveOutfit(su, playerEnt, outfitType, outfitId):
    LOG_INFO('gmDeactiveOutfit', playerEnt, outfitType, outfitId)
    if gameconfig.isCrossServer():
        su.onCommandResult(gameconst.GMCommandErr.GM_RET_CROSS_SERVER_FORBIDDEN, '执行失败, 跨服禁止执行', {"ec": gameconst.GMCommandErr.GM_RET_CROSS_SERVER_FORBIDDEN})
        return

    if gmCommand.isRawPlayer(playerEnt):
        su.onCommandResult(gameconst.GMCommandErr.GM_RET_TARGET_OFFLINE, '执行失败, 玩家不在线', {"ec": gameconst.GMCommandErr.GM_RET_TARGET_OFFLINE})
    else:
        ok, errMsg = playerEnt.gmDeactiveOutfit(outfitType, outfitId)
        if not ok:
            su.onCommandResult(gameconst.GMCommandErr.GM_RET_ARGS_ERR, '执行失败, %s' % errMsg, {"ec": gameconst.GMCommandErr.GM_RET_ARGS_ERR, "gbId": playerEnt.gbID, "outfitType": outfitType, "outfitId": outfitId})
            return
        # 踢下线
        playerEnt.destroySelf(gameconst.OFFLINE_REASON_GMKICK)
        su.onCommandResult(gameconst.GMCommandErr.GM_RET_OK, 'command success', {"ec": gameconst.GMCommandErr.GM_RET_OK, "offline": 0, "gbId": playerEnt.gbID, "outfitType": outfitType, "outfitId": outfitId})

@gm_cmd('$setSynthesisUpgradeNum', (Player("gbId or Id", raw=True), Int("mainType 物品主类型"), Int("subType 物品子类型"), Int("quality 品质"), Int("num 保底进度,0表示清零")), RARG(0), BASE, '设置随机合成保底进度(仅支持在线玩家;设值达到保底次数不会自动升档,仍需玩家手动兑换)', ALLSIDE,
        GOD_GROUPS)
def gmSetSynthesisUpgradeNum(su, playerEnt, mainType, subType, quality, num):
    LOG_INFO('gmSetSynthesisUpgradeNum', playerEnt, mainType, subType, quality, num)
    if gameconfig.isCrossServer():
        su.onCommandResult(gameconst.GMCommandErr.GM_RET_CROSS_SERVER_FORBIDDEN, '执行失败, 跨服禁止执行', {"ec": gameconst.GMCommandErr.GM_RET_CROSS_SERVER_FORBIDDEN})
        return
    synthesisKey = mainType * gameconst.SynthesusDataKeys.SYNTHESIS_KEY_MAIN_TYPE_FACTOR + subType
    cfgData = RSSD.datas.get(synthesisKey, None)
    if not cfgData:
        su.onCommandResult(gameconst.GMCommandErr.GM_RET_ARGS_ERR, '执行失败, 合成类型不存在', {"ec": gameconst.GMCommandErr.GM_RET_ARGS_ERR, "mainType": mainType, "subType": subType})
        return
    upgradeNumList = cfgData['upgradeNum']
    if quality < 0 or quality >= len(upgradeNumList) or not upgradeNumList[quality]:
        su.onCommandResult(gameconst.GMCommandErr.GM_RET_ARGS_ERR, '执行失败, 该品质无保底配置', {"ec": gameconst.GMCommandErr.GM_RET_ARGS_ERR, "mainType": mainType, "subType": subType, "quality": quality})
        return
    if num < 0:
        su.onCommandResult(gameconst.GMCommandErr.GM_RET_ARGS_ERR, '执行失败, 保底进度不能小于0', {"ec": gameconst.GMCommandErr.GM_RET_ARGS_ERR, "num": num})
        return

    if gmCommand.isRawPlayer(playerEnt):
        su.onCommandResult(gameconst.GMCommandErr.GM_RET_TARGET_OFFLINE, '执行失败, 玩家不在线', {"ec": gameconst.GMCommandErr.GM_RET_TARGET_OFFLINE})
    else:
        ok, oldNum, newNum, errMsg = playerEnt.gmSetSynthesisUpgradeNum(mainType, subType, quality, num)
        if not ok:
            su.onCommandResult(gameconst.GMCommandErr.GM_RET_ARGS_ERR, '执行失败, %s' % errMsg, {"ec": gameconst.GMCommandErr.GM_RET_ARGS_ERR, "gbId": playerEnt.gbID, "mainType": mainType, "subType": subType, "quality": quality, "num": num})
            return
        su.onCommandResult(gameconst.GMCommandErr.GM_RET_OK, 'command success', {"ec": gameconst.GMCommandErr.GM_RET_OK, "offline": 0, "gbId": playerEnt.gbID, "mainType": mainType, "subType": subType, "quality": quality, "oldNum": oldNum, "newNum": newNum})

@gm_cmd('$getSynthesisUpgradeNum', (Player("gbId or Id", raw=True),), RARG(0), BASE, '查询玩家当前全部合成保底进度(仅支持在线玩家)', ALLSIDE,
        GOD_GROUPS)
def gmGetSynthesisUpgradeNum(su, playerEnt):
    LOG_INFO('gmGetSynthesisUpgradeNum', playerEnt)
    if gameconfig.isCrossServer():
        su.onCommandResult(gameconst.GMCommandErr.GM_RET_CROSS_SERVER_FORBIDDEN, '执行失败, 跨服禁止执行', {"ec": gameconst.GMCommandErr.GM_RET_CROSS_SERVER_FORBIDDEN})
        return

    if gmCommand.isRawPlayer(playerEnt):
        su.onCommandResult(gameconst.GMCommandErr.GM_RET_TARGET_OFFLINE, '执行失败, 玩家不在线', {"ec": gameconst.GMCommandErr.GM_RET_TARGET_OFFLINE})
    else:
        infoList = playerEnt.gmGetSynthesisUpgradeNum()
        su.onCommandResult(gameconst.GMCommandErr.GM_RET_OK, 'command success', {"ec": gameconst.GMCommandErr.GM_RET_OK, "offline": 0, "gbId": playerEnt.gbID, "list": infoList})

@gm_cmd('$resetAchievement', (Player("gbId or Id", raw=True), Int("achieveId 成就id"), Int("resetStep 0保留进度仅清完成标记/1进度清零(已领取的进度无法恢复,恒回到未开始)")), RARG(0), BASE, '重置成就为未完成状态(只回退成就状态,不回收已发奖励;属性查询型成就重置后再次触发会立即重新完成;不级联处理子成就;仅支持在线玩家)', ALLSIDE,
        GOD_GROUPS)
def gmResetAchievement(su, playerEnt, achieveId, resetStep):
    LOG_INFO('gmResetAchievement', playerEnt, achieveId, resetStep)
    if gameconfig.isCrossServer():
        su.onCommandResult(gameconst.GMCommandErr.GM_RET_CROSS_SERVER_FORBIDDEN, '执行失败, 跨服禁止执行', {"ec": gameconst.GMCommandErr.GM_RET_CROSS_SERVER_FORBIDDEN})
        return
    if achieveId not in A_DD.datas:
        su.onCommandResult(gameconst.GMCommandErr.GM_RET_ARGS_ERR, '执行失败, 成就id不存在', {"ec": gameconst.GMCommandErr.GM_RET_ARGS_ERR, "achieveId": achieveId})
        return
    if resetStep not in (0, 1):
        su.onCommandResult(gameconst.GMCommandErr.GM_RET_ARGS_ERR, '执行失败, resetStep只能为0或1', {"ec": gameconst.GMCommandErr.GM_RET_ARGS_ERR, "resetStep": resetStep})
        return

    if gmCommand.isRawPlayer(playerEnt):
        su.onCommandResult(gameconst.GMCommandErr.GM_RET_TARGET_OFFLINE, '执行失败, 玩家不在线', {"ec": gameconst.GMCommandErr.GM_RET_TARGET_OFFLINE})
    else:
        ok, errMsg, oldState, oldStep = playerEnt.gmResetAchievement(achieveId, resetStep)
        if not ok:
            su.onCommandResult(gameconst.GMCommandErr.GM_RET_ARGS_ERR, '执行失败, %s' % errMsg, {"ec": gameconst.GMCommandErr.GM_RET_ARGS_ERR, "gbId": playerEnt.gbID, "achieveId": achieveId})
            return
        su.onCommandResult(gameconst.GMCommandErr.GM_RET_OK, 'command success', {"ec": gameconst.GMCommandErr.GM_RET_OK, "offline": 0, "gbId": playerEnt.gbID, "achieveId": achieveId, "resetStep": resetStep, "oldState": oldState, "oldStep": oldStep, "sumPoint": playerEnt.achievementInfo.sumPoint})

@gm_cmd('$setDrawCardPity', (Player("gbId or Id", raw=True), Int("pool 卡池id(同组多池共享保底,服务端按poolGroupId映射)"), Int("num 保底进度,-1不修改;设到>=保底次数不会立即结算,下次抽卡才转成保底份数"), Int("guaranteed 保底份数,-1不修改,超出maxStack自动钳制")), RARG(0), BASE, '设置抽卡保底进度/保底份数(不动抽卡历史;仅支持在线玩家)', ALLSIDE,
        GOD_GROUPS, minArgs=3)
def gmSetDrawCardPity(su, playerEnt, pool, num, guaranteed=-1):
    LOG_INFO('gmSetDrawCardPity', playerEnt, pool, num, guaranteed)
    if gameconfig.isCrossServer():
        su.onCommandResult(gameconst.GMCommandErr.GM_RET_CROSS_SERVER_FORBIDDEN, '执行失败, 跨服禁止执行', {"ec": gameconst.GMCommandErr.GM_RET_CROSS_SERVER_FORBIDDEN})
        return
    poolData = GGP.datas.get(pool, None)
    if not poolData:
        su.onCommandResult(gameconst.GMCommandErr.GM_RET_ARGS_ERR, '执行失败, 卡池id不存在', {"ec": gameconst.GMCommandErr.GM_RET_ARGS_ERR, "pool": pool})
        return
    if num < -1 or guaranteed < -1:
        su.onCommandResult(gameconst.GMCommandErr.GM_RET_ARGS_ERR, '执行失败, 参数不能小于-1', {"ec": gameconst.GMCommandErr.GM_RET_ARGS_ERR, "num": num, "guaranteed": guaranteed})
        return

    if gmCommand.isRawPlayer(playerEnt):
        su.onCommandResult(gameconst.GMCommandErr.GM_RET_TARGET_OFFLINE, '执行失败, 玩家不在线', {"ec": gameconst.GMCommandErr.GM_RET_TARGET_OFFLINE})
    else:
        ok, errMsg, poolGroupId, oldNum, newNum, oldGuaranteed, newGuaranteed = playerEnt.gmSetDrawCardPity(pool, num, guaranteed)
        if not ok:
            su.onCommandResult(gameconst.GMCommandErr.GM_RET_ARGS_ERR, '执行失败, %s' % errMsg, {"ec": gameconst.GMCommandErr.GM_RET_ARGS_ERR, "gbId": playerEnt.gbID, "pool": pool})
            return
        su.onCommandResult(gameconst.GMCommandErr.GM_RET_OK, 'command success', {"ec": gameconst.GMCommandErr.GM_RET_OK, "offline": 0, "gbId": playerEnt.gbID, "pool": pool, "poolGroupId": poolGroupId, "oldNum": oldNum, "newNum": newNum, "oldGuaranteed": oldGuaranteed, "newGuaranteed": newGuaranteed})

@gm_cmd('$getDrawCardPity', (Player("gbId or Id", raw=True),), RARG(0), BASE, '查询玩家当前全部卡池保底进度(仅支持在线玩家)', ALLSIDE,
        GOD_GROUPS)
def gmGetDrawCardPity(su, playerEnt):
    LOG_INFO('gmGetDrawCardPity', playerEnt)
    if gameconfig.isCrossServer():
        su.onCommandResult(gameconst.GMCommandErr.GM_RET_CROSS_SERVER_FORBIDDEN, '执行失败, 跨服禁止执行', {"ec": gameconst.GMCommandErr.GM_RET_CROSS_SERVER_FORBIDDEN})
        return

    if gmCommand.isRawPlayer(playerEnt):
        su.onCommandResult(gameconst.GMCommandErr.GM_RET_TARGET_OFFLINE, '执行失败, 玩家不在线', {"ec": gameconst.GMCommandErr.GM_RET_TARGET_OFFLINE})
    else:
        infoList = playerEnt.gmGetDrawCardPity()
        su.onCommandResult(gameconst.GMCommandErr.GM_RET_OK, 'command success', {"ec": gameconst.GMCommandErr.GM_RET_OK, "offline": 0, "gbId": playerEnt.gbID, "list": infoList})

@gm_cmd('$setDungeonTicket', (Player("gbId or Id", raw=True), Int("dungeonType 1混沌回廊/2天劫崖/3归墟/4魔物巢穴/5首领巢穴"), Int("freeNum 免费剩余次数,-1不修改"), Int("paidNum 付费剩余次数,-1不修改")), RARG(0), BASE, '设置副本剩余进入次数(讨伐类按分桶语义:freeNum=默认免费桶,paidNum=金币购买桶;仅支持在线玩家,玩家在跨服中拒绝)', ALLSIDE,
        GOD_GROUPS, minArgs=3)
def gmSetDungeonTicket(su, playerEnt, dungeonType, freeNum, paidNum=-1):
    LOG_INFO('gmSetDungeonTicket', playerEnt, dungeonType, freeNum, paidNum)
    if gameconfig.isCrossServer():
        su.onCommandResult(gameconst.GMCommandErr.GM_RET_CROSS_SERVER_FORBIDDEN, '执行失败, 跨服禁止执行', {"ec": gameconst.GMCommandErr.GM_RET_CROSS_SERVER_FORBIDDEN})
        return
    if dungeonType not in gameconst.RecoveryTicketSubType.VALID_SUB_TYPE:
        su.onCommandResult(gameconst.GMCommandErr.GM_RET_ARGS_ERR, '执行失败, 副本类型不合法(1混沌回廊/2天劫崖/3归墟/4魔物巢穴/5首领巢穴)', {"ec": gameconst.GMCommandErr.GM_RET_ARGS_ERR, "dungeonType": dungeonType})
        return
    if freeNum < -1 or paidNum < -1:
        su.onCommandResult(gameconst.GMCommandErr.GM_RET_ARGS_ERR, '执行失败, 次数不能小于-1', {"ec": gameconst.GMCommandErr.GM_RET_ARGS_ERR, "freeNum": freeNum, "paidNum": paidNum})
        return

    if gmCommand.isRawPlayer(playerEnt):
        su.onCommandResult(gameconst.GMCommandErr.GM_RET_TARGET_OFFLINE, '执行失败, 玩家不在线', {"ec": gameconst.GMCommandErr.GM_RET_TARGET_OFFLINE})
    else:
        ok, errMsg, newInfo = playerEnt.gmSetDungeonTicket(dungeonType, freeNum, paidNum)
        if not ok:
            su.onCommandResult(gameconst.GMCommandErr.GM_RET_ARGS_ERR, '执行失败, %s' % errMsg, {"ec": gameconst.GMCommandErr.GM_RET_ARGS_ERR, "gbId": playerEnt.gbID, "dungeonType": dungeonType})
            return
        su.onCommandResult(gameconst.GMCommandErr.GM_RET_OK, 'command success', {"ec": gameconst.GMCommandErr.GM_RET_OK, "offline": 0, "gbId": playerEnt.gbID, "dungeonType": dungeonType, "info": newInfo})

@gm_cmd('$getDungeonTicket', (Player("gbId or Id", raw=True), Int("dungeonType 1混沌回廊/2天劫崖/3归墟/4魔物巢穴/5首领巢穴")), RARG(0), BASE, '查询副本剩余进入次数与当日可购余量(仅支持在线玩家)', ALLSIDE,
        GOD_GROUPS)
def gmGetDungeonTicket(su, playerEnt, dungeonType):
    LOG_INFO('gmGetDungeonTicket', playerEnt, dungeonType)
    if gameconfig.isCrossServer():
        su.onCommandResult(gameconst.GMCommandErr.GM_RET_CROSS_SERVER_FORBIDDEN, '执行失败, 跨服禁止执行', {"ec": gameconst.GMCommandErr.GM_RET_CROSS_SERVER_FORBIDDEN})
        return
    if dungeonType not in gameconst.RecoveryTicketSubType.VALID_SUB_TYPE:
        su.onCommandResult(gameconst.GMCommandErr.GM_RET_ARGS_ERR, '执行失败, 副本类型不合法(1混沌回廊/2天劫崖/3归墟/4魔物巢穴/5首领巢穴)', {"ec": gameconst.GMCommandErr.GM_RET_ARGS_ERR, "dungeonType": dungeonType})
        return

    if gmCommand.isRawPlayer(playerEnt):
        su.onCommandResult(gameconst.GMCommandErr.GM_RET_TARGET_OFFLINE, '执行失败, 玩家不在线', {"ec": gameconst.GMCommandErr.GM_RET_TARGET_OFFLINE})
    else:
        info = playerEnt.gmGetDungeonTicketInfo(dungeonType)
        su.onCommandResult(gameconst.GMCommandErr.GM_RET_OK, 'command success', {"ec": gameconst.GMCommandErr.GM_RET_OK, "offline": 0, "gbId": playerEnt.gbID, "dungeonType": dungeonType, "info": info})

# ============================================================================
# 帮会相关（帮会侧按帮会UUID定位,走 GuildStub -> guildBox RPC,不要求玩家在线;
# 成员侧走 RARG(0) 直调 Avatar,仅支持在线玩家）
# ============================================================================
def _gmFindGuildByUUID(guildStub, guildUUID):
    """按帮会UUID定位帮会缓存。返回 GuildCacheVal 或 None。"""
    return guildStub.guildDic.get(guildUUID, None)

@gm_cmd('$setGuildLevel', (Str("帮会UUID"), Int("level 目标等级"), Int("exp 经验,-1不修改")), RSTUB('GuildStub'), BASE, '设置帮会等级/经验(支持降级;不要求玩家在线)', ALLSIDE,
        GOD_GROUPS, minArgs=2)
def gmSetGuildLevel(su, guildStub, guildKey, level, exp=-1):
    LOG_INFO('gmSetGuildLevel', guildKey, level, exp)
    maxLevel = max(G_GUD.datas.keys())
    if level < 1 or level > maxLevel:
        su.onCommandResult(gameconst.GMCommandErr.GM_RET_ARGS_ERR, '执行失败, 等级超出范围', {"ec": gameconst.GMCommandErr.GM_RET_ARGS_ERR, "level": level, "maxLevel": maxLevel})
        return
    if exp < -1:
        su.onCommandResult(gameconst.GMCommandErr.GM_RET_ARGS_ERR, '执行失败, 经验不能小于-1', {"ec": gameconst.GMCommandErr.GM_RET_ARGS_ERR, "exp": exp})
        return

    try:
        guildUUID = int(guildKey)
    except (ValueError, TypeError):
        guildUUID = 0
    gcVal = _gmFindGuildByUUID(guildStub, guildUUID)
    if not gcVal:
        su.onCommandResult(gameconst.GMCommandErr.GM_RET_TARGET_NOT_EXISTS, '执行失败, 帮会不存在', {"ec": gameconst.GMCommandErr.GM_RET_TARGET_NOT_EXISTS, "guildKey": guildKey})
        return

    opUUID = KBEngine.genUUID64()
    detail = gameclass.AwardDetailCls(gm_cmd='$setGuildLevel', level=level, exp=exp)
    gcVal.guildBox.gmSetGuildLevel(level, exp, AAC_AACDD.datas.BONUS_SRC_GM, opUUID, detail)
    su.onCommandResult(gameconst.GMCommandErr.GM_RET_OK, 'command success', {"ec": gameconst.GMCommandErr.GM_RET_OK, "guildUUID": gcVal.guildUUID, "guildName": gcVal.guildName, "oldLevel": gcVal.guildLevel, "level": level, "exp": exp})

@gm_cmd('$setJunXuQixie', (Str("帮会UUID"), Int("qixieType 器械类型"), Int("level 目标等级"), Int("exp 进度,-1不修改")), RSTUB('GuildStub'), BASE, '设置军需处器械等级/进度(支持降级;全帮广播并同步城战/矿战;不要求玩家在线)', ALLSIDE,
        GOD_GROUPS, minArgs=3)
def gmSetJunXuQixie(su, guildStub, guildKey, qixieType, level, exp=-1):
    LOG_INFO('gmSetJunXuQixie', guildKey, qixieType, level, exp)
    levelDic = G_WED.typeLevelDic.get(qixieType, None)
    if not levelDic:
        su.onCommandResult(gameconst.GMCommandErr.GM_RET_ARGS_ERR, '执行失败, 器械类型不存在', {"ec": gameconst.GMCommandErr.GM_RET_ARGS_ERR, "qixieType": qixieType})
        return
    maxLevel = max(levelDic.keys())
    if level < 1 or level > maxLevel:
        su.onCommandResult(gameconst.GMCommandErr.GM_RET_ARGS_ERR, '执行失败, 等级超出范围', {"ec": gameconst.GMCommandErr.GM_RET_ARGS_ERR, "qixieType": qixieType, "level": level, "maxLevel": maxLevel})
        return
    if exp < -1:
        su.onCommandResult(gameconst.GMCommandErr.GM_RET_ARGS_ERR, '执行失败, 进度不能小于-1', {"ec": gameconst.GMCommandErr.GM_RET_ARGS_ERR, "exp": exp})
        return

    try:
        guildUUID = int(guildKey)
    except (ValueError, TypeError):
        guildUUID = 0
    gcVal = _gmFindGuildByUUID(guildStub, guildUUID)
    if not gcVal:
        su.onCommandResult(gameconst.GMCommandErr.GM_RET_TARGET_NOT_EXISTS, '执行失败, 帮会不存在', {"ec": gameconst.GMCommandErr.GM_RET_TARGET_NOT_EXISTS, "guildKey": guildKey})
        return

    opUUID = KBEngine.genUUID64()
    gcVal.guildBox.gmSetJunXuQixie(qixieType, level, exp, opUUID)
    su.onCommandResult(gameconst.GMCommandErr.GM_RET_OK, 'command success', {"ec": gameconst.GMCommandErr.GM_RET_OK, "guildUUID": gcVal.guildUUID, "guildName": gcVal.guildName, "qixieType": qixieType, "level": level, "exp": exp})

@gm_cmd('$setGuildContrib', (Player("gbId or Id", raw=True), Int("num 目标帮贡")), RARG(0), BASE, '设置玩家帮会贡献(增加时会同步累加成员历史贡献;仅支持在线玩家)', ALLSIDE,
        GOD_GROUPS)
def gmSetGuildContrib(su, playerEnt, num):
    LOG_INFO('gmSetGuildContrib', playerEnt, num)
    if gameconfig.isCrossServer():
        su.onCommandResult(gameconst.GMCommandErr.GM_RET_CROSS_SERVER_FORBIDDEN, '执行失败, 跨服禁止执行', {"ec": gameconst.GMCommandErr.GM_RET_CROSS_SERVER_FORBIDDEN})
        return
    if num < 0:
        su.onCommandResult(gameconst.GMCommandErr.GM_RET_ARGS_ERR, '执行失败, 帮贡不能小于0', {"ec": gameconst.GMCommandErr.GM_RET_ARGS_ERR, "num": num})
        return

    if gmCommand.isRawPlayer(playerEnt):
        su.onCommandResult(gameconst.GMCommandErr.GM_RET_TARGET_OFFLINE, '执行失败, 玩家不在线', {"ec": gameconst.GMCommandErr.GM_RET_TARGET_OFFLINE})
    else:
        opUUID = KBEngine.genUUID64()
        detail = gameclass.AwardDetailCls(gm_cmd='$setGuildContrib', num=num)
        ok, oldNum, newNum, errMsg = playerEnt.gmSetGuildContrib(num, opUUID, AAC_AACDD.datas.BONUS_SRC_GM, detail)
        if not ok:
            su.onCommandResult(gameconst.GMCommandErr.GM_RET_ARGS_ERR, '执行失败, %s' % errMsg, {"ec": gameconst.GMCommandErr.GM_RET_ARGS_ERR, "gbId": playerEnt.gbID, "num": num})
            return
        su.onCommandResult(gameconst.GMCommandErr.GM_RET_OK, 'command success', {"ec": gameconst.GMCommandErr.GM_RET_OK, "offline": 0, "gbId": playerEnt.gbID, "oldNum": oldNum, "newNum": newNum})

@gm_cmd('$setGuildTrainLv', (Player("gbId or Id", raw=True), Int("trainId 修炼id,0表示全部"), Int("level 目标等级,0表示清除该修炼")), RARG(0), BASE, '设置帮会修炼等级(支持降级,不返还消耗;仅支持在线玩家)', ALLSIDE,
        GOD_GROUPS)
def gmSetGuildTrainLv(su, playerEnt, trainId, level):
    LOG_INFO('gmSetGuildTrainLv', playerEnt, trainId, level)
    if gameconfig.isCrossServer():
        su.onCommandResult(gameconst.GMCommandErr.GM_RET_CROSS_SERVER_FORBIDDEN, '执行失败, 跨服禁止执行', {"ec": gameconst.GMCommandErr.GM_RET_CROSS_SERVER_FORBIDDEN})
        return
    if trainId and trainId not in GT_GTD.datas:
        su.onCommandResult(gameconst.GMCommandErr.GM_RET_ARGS_ERR, '执行失败, 修炼id不存在', {"ec": gameconst.GMCommandErr.GM_RET_ARGS_ERR, "trainId": trainId})
        return
    maxLevel = max(GT_GTUD.datas.keys())
    if level < 0 or level > maxLevel:
        su.onCommandResult(gameconst.GMCommandErr.GM_RET_ARGS_ERR, '执行失败, 等级超出范围', {"ec": gameconst.GMCommandErr.GM_RET_ARGS_ERR, "level": level, "maxLevel": maxLevel})
        return

    if gmCommand.isRawPlayer(playerEnt):
        su.onCommandResult(gameconst.GMCommandErr.GM_RET_TARGET_OFFLINE, '执行失败, 玩家不在线', {"ec": gameconst.GMCommandErr.GM_RET_TARGET_OFFLINE})
    else:
        ok, errMsg = playerEnt.gmSetGuildTrainLevel(trainId, level)
        if not ok:
            su.onCommandResult(gameconst.GMCommandErr.GM_RET_ARGS_ERR, '执行失败, %s' % errMsg, {"ec": gameconst.GMCommandErr.GM_RET_ARGS_ERR, "gbId": playerEnt.gbID, "trainId": trainId, "level": level})
            return
        su.onCommandResult(gameconst.GMCommandErr.GM_RET_OK, 'command success', {"ec": gameconst.GMCommandErr.GM_RET_OK, "offline": 0, "gbId": playerEnt.gbID, "trainId": trainId, "level": level})

@gm_cmd('$deactivateBattlePass', (Player("gbId or Id", raw=True), Int("passId")), RARG(0), BASE, '清除战令付费档激活状态并使特权失效, passId=0清全部', ALLSIDE, GOD_GROUPS)
def gmDeactivateBattlePass(su, playerEnt, passId):
    LOG_INFO('gmDeactivateBattlePass', playerEnt, passId)
    if gameconfig.isCrossServer():
        su.onCommandResult(-1, '执行失败, 跨服禁止执行', {"ec": -3})
        return
    if gmCommand.isRawPlayer(playerEnt):
        gbId, name, accountName, dbId = playerEnt
        gamesql.recordAvatarOfflineCallback(gbId, 'gmDeactivateBattlePass', (passId,))
        su.onCommandResult(0, 'command success', {"ec": 0, "offline": 1, "gbId": gbId, "passId": passId})
    else:
        msg = playerEnt.gmDeactivateBattlePass(passId)
        if msg == 'fail':
            su.onCommandResult(1, '执行失败', {"ec": 1, "offline": 0, "gbId": playerEnt.gbID, "passId": passId, "msg": msg})
        else:
            su.onCommandResult(0, 'command success', {"ec": 0, "offline": 0, "gbId": playerEnt.gbID, "passId": passId, "msg": msg})


# ============================================================================
# 组队副本进入开关（生产运维GM：副本维护/紧急关停用）
# 临时开关：只写 CrossTeamStub 各分片内存（gmSetForbidEnterDungeons），重启/分片重建即失效；
# 判定在 CrossTeamStub.onCrusadeCheck（手动发起与人满自动进本必经），已创建的副本空间不受影响。
# ============================================================================

def _gmWriteAllCrossTeamStub(dungeonNos, isBan):
    # 写入全部 CrossTeamStub 分片（teamId % crossTeamStubNum 分片，可能落在不同 baseapp，需全部写到）
    _total = gameconfig.crossTeamStubNum()
    _okNum = 0
    for _i in range(_total):
        _stubName = gameconst.GLOBAL_BASE_STUB_CROSSTEAMSTUB + str(_i)
        _stubBox = gameengine.getGlobalBase(_stubName)
        if not _stubBox:
            LOG_ERR('_gmWriteAllCrossTeamStub stub not ready', _stubName)
            continue
        _stubBox.gmSetForbidEnterDungeons(dungeonNos, isBan)
        _okNum += 1
    return _okNum, _total


@gm_cmd('$banEnterDungeon', (Str('dungeonNos 副本id,多个以英文逗号分隔'),), RONE, BASE,
        '禁止进入指定组队副本(临时生效,重启后失效;已创建的副本不受影响;玩家进本提示54003534)', ALLSIDE, GOD_GROUPS)
def gmBanEnterDungeon(su, dungeonNosStr):
    LOG_INFO('gmBanEnterDungeon', dungeonNosStr)
    _dungeonNos = [int(_s) for _s in dungeonNosStr.split(',') if _s.strip().isdigit()]
    if not _dungeonNos:
        su.onCommandResult(
            gameconst.GMCommandErr.GM_RET_ARGS_ERR, 
            '执行失败, 未输入有效副本id',
            {"ec": gameconst.GMCommandErr.GM_RET_ARGS_ERR}
        )
        return

    _okNum, _total = _gmWriteAllCrossTeamStub(_dungeonNos, True)
    su.onCommandResult(
        gameconst.GMCommandErr.GM_RET_OK,
        'command success',
        {"ec": gameconst.GMCommandErr.GM_RET_OK, "dungeonNos": _dungeonNos, "stubNum": '%d/%d' % (_okNum, _total)}
    )


@gm_cmd('$disbanEnterDungeon', (Str('dungeonNos 副本id,多个以英文逗号分隔'),), RONE, BASE,
        '解除指定组队副本的禁止进入限制(参数同$banEnterDungeon)', ALLSIDE, GOD_GROUPS)
def gmDisbanEnterDungeon(su, dungeonNosStr):
    LOG_INFO('gmDisbanEnterDungeon', dungeonNosStr)
    _dungeonNos = [int(_s) for _s in dungeonNosStr.split(',') if _s.strip().isdigit()]
    if not _dungeonNos:
        su.onCommandResult(
            gameconst.GMCommandErr.GM_RET_ARGS_ERR, 
            '执行失败, 未输入有效副本id', 
            {"ec": gameconst.GMCommandErr.GM_RET_ARGS_ERR}
        )
        return

    _okNum, _total = _gmWriteAllCrossTeamStub(_dungeonNos, False)
    su.onCommandResult(
        gameconst.GMCommandErr.GM_RET_OK, 
        'command success',
        {"ec": gameconst.GMCommandErr.GM_RET_OK, "dungeonNos": _dungeonNos, "stubNum": '%d/%d' % (_okNum, _total)}
    )
