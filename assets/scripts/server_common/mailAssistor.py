# -*- coding: utf-8 -*-

import KBEngine
from KBEDebug import *
import dropAward
import mail_mail as M_MD
import mail_config as MACF
import gameengine
import utils
import gamesql
import gameconst
import time
import gameglobal
import dataUtils
# import idipDef

import LogTrackingMgr


MAIL_EXPIRED_TIME_DEFAULT = 2145888000  #2038年
SEND_NUM_PER_TIMES = 50


def calcMailExpiredTime(mailId, createTime, mailData=None):
    if not mailData:
        mailData = M_MD.datas[mailId]
    _expired = mailData.get('period', '')
    if not _expired:
        return MAIL_EXPIRED_TIME_DEFAULT
    if _expired.isdigit():
        return createTime + 3600 * int(_expired)
    else:
        return int(time.mktime(time.strptime(_expired, "%Y-%m-%d-%H-%M")))

def parseAttachStr(attachStr):
    _attach = dropAward.MailAttachVal()
    _attachStr = attachStr.replace(' ', '')
    _attachStr = _attachStr.strip('[]();')
    if _attachStr:
        itemStrList = _attachStr.split(';')
        for _oneItemStr in itemStrList:
            oneItemList = _oneItemStr.split(',')
            _itemId = int(oneItemList[0])
            _itemNum = int(oneItemList[1])
            if len(oneItemList) == 3:
                _bindType = int(oneItemList[2])
            else:
                _bindType = dataUtils.getItemDefaultBindType()
            _attach.addWealthByItemId(_itemId, _itemNum, _bindType)
    return _attach

def parseDespStr(despArgsString):
    despArgsString = despArgsString.replace(' ', '')
    despArgsString = despArgsString.strip('[]()')
    if despArgsString:
        despArgs=despArgsString.split(',')
    else:
        despArgs=()
    return despArgs


def sendMailToPlayers(toGBIDList, mailId, extraAttach: dropAward.MailAttachVal=None, 
                      despArgs=(), fromGBID=0, globalMailGBID=0, createTime=0,\
                      expiredTime=0, title=None, cont=None, srcType=0, srcSubType=0,\
                      opUUID=0, desc='', idipSource=0, callback=None, isGlobal=False, dueTime=0):
    
    LOG_INFO('sendMailToPlayers:', len(toGBIDList), mailId)

    if not toGBIDList:
        callback and callback(None, None, None, "sendMailToPlayers no target", mailId)
        return

    mailData = M_MD.datas.get(mailId, None)
    if not mailData:
        callback and callback(None, None, None, "sendMailToPlayers not config", mailId)
        return

    toGBIDList = toGBIDList[:]
    title = title or ''
    cont = cont or ''
    # 兼容下系统全服邮件被当作个人邮件发出来的问题
    if mailData['type'] == gameconst.MailType.GLOBAL_MAIL_EXCLUDE_NEW_PLAYERS \
        or mailData['type'] == gameconst.MailType.GLOBAL_MAIL_INCLUDE_NEW_PLAYERS:
        if globalMailGBID <= 0:
            globalMailGBID = KBEngine.genUUID64()
        isGlobal = True
    # 分批次发送    
    for _ in range(SEND_NUM_PER_TIMES):
        if not toGBIDList:
            break
        toGBID = toGBIDList.pop()
        _sendMailToSinglePlayer(
            toGBID, mailId, dueTime, extraAttach, despArgs, title, cont, fromGBID, globalMailGBID,
            createTime, expiredTime, srcType, srcSubType, opUUID, desc, idipSource, isGlobal, callback)

    if toGBIDList:
        KBEngine.addTimer(
            0.1, 
            0, 
            lambda timerId :sendMailToPlayers(\
                toGBIDList, mailId, extraAttach,\
                despArgs, fromGBID,\
                globalMailGBID, createTime, expiredTime,\
                title, cont, srcType, srcSubType, opUUID,\
                desc, idipSource, callback, isGlobal, dueTime))


def _sendMailToSinglePlayer(toGBID, mailId, dueTime, extraAttach:dropAward.MailAttachVal, despArgs, title, cont, fromGBID,
                      globalMailGBID, createTime, expiredTime, srcType, srcSubType, opUUID, desc, idipSource, isGlobal, callback):
    LOG_INFO('_sendMailToSinglePlayer:', toGBID, mailId, dueTime, globalMailGBID, isGlobal)
    if len(despArgs) != M_MD.MailArgsNumMap[mailId]:
        gameengine.panicStack(' _sendMailToSinglePlayer, despArgs num error:', mailId, despArgs)
        callback and callback(None, None, None, "_sendMailToSinglePlayer despArgs err", mailId)
        return

    _mailData = M_MD.datas.get(mailId, None)
    if not _mailData:
        callback and callback(None, None, None, "_sendMailToSinglePlayer not config", mailId)
        return False

    if not _mailData['isOpen']:
        callback and callback(None, None, None, "_sendMailToSinglePlayer not isOpen", mailId)
        return False

    mailGBID = globalMailGBID if globalMailGBID else KBEngine.genUUID64()
    rewardId = _mailData.get('rewardId')
    _attach = dropAward.MailAttachVal()
    if rewardId > 0:
        _attach.addWealthByRewardId(rewardId)

    if extraAttach:
        _attach += extraAttach

    if _attach.mailWealthExceedUplimit():
        callback and callback(None, None, None, "_sendMailToSinglePlayer mailWealthExceedUplimit", mailId)
        _attach.reduceItemToMaxNum()

    if _attach.isEmpty():
        _attachStat = gameconst.MailAttachState.HasGET
    else:
        _attachStat = gameconst.MailAttachState.NotGet

    readStat = gameconst.MailReadState.NotRead
    createTime = createTime or utils.curTS()
    expiredTime = expiredTime if expiredTime else calcMailExpiredTime(mailId, createTime, _mailData)
    despArgs = [str(arg) for arg in despArgs]
    _title = title.strip(' ')
    cont = cont.strip(' ')

    attachStr = _attach.getItemsTLogStr()

    _sendMailCallback = lambda ret, num, insertId, err:\
        _sendMailToPlayerCallback(ret, num, insertId, err, toGBID, mailId, mailGBID, _title, cont, attachStr, srcType, srcSubType,
                                  opUUID, desc, idipSource, isGlobal, callback, dueTime)
    gamesql.sendMailByGBID(toGBID, mailId, mailGBID, globalMailGBID, readStat, dueTime, createTime, expiredTime, fromGBID,
           _attach, _attachStat, despArgs, _title, cont, opUUID, srcType, srcSubType, desc, idipSource, _sendMailCallback)


def _sendMailToPlayerCallback(ret, num, insertId, err, toGBID, mailId,\
                              mailGBID, title, cont, attachStr, srcType, srcSubType,\
                              opUUID, desc, idipSource, isGlobal,\
                              senderCallback=None, dueTime = 0):
    LOG_INFO('_sendMailToPlayerCallback:', ret, num, insertId, err, toGBID, mailId, isGlobal, dueTime)
    if senderCallback:
        senderCallback(ret, num, insertId, err, mailGBID)

    if err:
        gameengine.panicStack('_sendMailToPlayerCallback:', err, toGBID)
        return
    _onSendMailByGBIDSucc(
        toGBID, mailId, mailGBID, title, cont, attachStr, srcType, srcSubType,\
        opUUID, desc, idipSource, isGlobal)

def _onSendMailByGBIDSucc(toGBID, mailId, mailGBID, title, cont, attachStr, srcType, srcSubType, opUUID, desc, idipSource, isGlobal):
    _entId = gameglobal.roleGBIDToEntId.get(toGBID, 0)
    _avatarEnt = KBEngine.entities.get(_entId)
    if _avatarEnt:
        #在线
        if gameengine.isCell():
            _avatarEnt.base.onInsertNewMailSucc(mailId, mailGBID, title, cont, attachStr, srcType, srcSubType, opUUID, desc, idipSource, isGlobal)
        else:
            _avatarEnt.onInsertNewMailSucc(mailId, mailGBID, title, cont, attachStr, srcType, srcSubType, opUUID, desc, idipSource, isGlobal)
    else:
        gameengine.getGlobalBase('PlayerStub').doOnOthersBase(
            [toGBID], 
            'onInsertNewMailSucc',
            (
                mailId, mailGBID, title, cont, attachStr, srcType, srcSubType, 
                opUUID, desc, idipSource, isGlobal,
            ),
            None, '', ())

    mailData = M_MD.datas[mailId]
    result = []
    if ',' in attachStr:
        tmp = {int(k): int(v) for k, v in (pair.split(',') for pair in attachStr.split(';'))}
        for itemId, itemCount in tmp.items():
            result.append({'item_id':itemId, 'item_count':itemCount, 'item_quality':dataUtils.getItemQuality(itemId)})
    LogTrackingMgr.LogTrackingMgr.mail_send('Mail', '', toGBID, mailId, mailData['type'], mailGBID, srcType, srcSubType, opUUID, idipSource, result) 

def getMyGlobalsMails(lastGBMailTime, roleChannel, roleRegTime, roleLoginTime, roleLevel, hasGotGlobalMails):
    LOG_INFO('in getMyGlobalsMails, lastGBMailTime:', lastGBMailTime, roleChannel, roleRegTime, roleLoginTime, roleLevel)
    gbMails = []
    mailMaxNum = MACF.datas['mailNumMax2']['value']
    for mail in reversed(gameglobal.globalMailsCacheList):
        if mail.globalMailGBID in hasGotGlobalMails:
            continue
        if not checkGlobalMailConds(mail, roleChannel, roleLevel, roleRegTime, roleLoginTime):
            continue
        gbMails.append(mail)
        if len(gbMails) >= mailMaxNum:
            #最多同步最新的mailMaxNum封全服邮件
            break
    return gbMails

def checkGlobalMailConds(mail, roleChannel, roleLevel, roleRegTime, roleLoginTime):
    if mail.isExpired():
        return False

    if mail.channel > 0 and mail.channel != roleChannel:
        return False

    if mail.maxRoleTime > 0:   
        if roleRegTime < mail.minRoleTime or roleRegTime > mail.maxRoleTime:
            return False

    # 这里做下兼容，旧的全局邮件minEffectTime和minEffectTime都为0
    if mail.dueTime > 0 and roleLoginTime > mail.dueTime:
        return False
    
    if mail.maxRoleLevel > 0:
        if roleLevel < mail.minRoleLevel or roleLevel > mail.maxRoleLevel:
            return False
    return True

def getLastGlobalMailTime():
    return gameglobal.globalMailsCacheList[-1].createTime if gameglobal.globalMailsCacheList else 0

g_AccountMailNumDic = {}

def checkAccountMails(accountName, accountType, playerGBID, entityId):
    LOG_INFO('checkAccountMails:', accountName, accountType, entityId, playerGBID)
    gamesql.loadMailByAccountInfo(
        accountName,accountType,playerGBID,
        lambda ret, num, insertId, err, playerGBID=playerGBID, entityId=entityId:
                _checkAccountMailsCB(ret, num, insertId, err, playerGBID, entityId))

def _checkAccountMailsCB(ret, num, insertId, err, playerGBID, entityId):
    LOG_INFO('_checkAccountMailsCB:', ret, num, insertId, err, playerGBID, entityId)
    if err:
        gameengine.panicStack('_checkAccountMailsCB:', err, playerGBID, entityId)
        _onCheckAccountMailFinished(entityId)
        return

    if 0 == len(ret):
        _onCheckAccountMailFinished(entityId)
        return

    LOG_INFO('_checkAccountMailsCB, found account mail:', ret)
    g_AccountMailNumDic[playerGBID] = len(ret)
    for accountMailData in ret:
        _mailId = int(accountMailData[1].decode())
        _mailData = M_MD.datas[_mailId]
        if _mailData['type'] != gameconst.MailType.GLOBAL_MAIL_ACCOUNT:
            continue
        _attachStr = accountMailData[3].decode()
        _despArgsStr = accountMailData[4].decode()
        _title = accountMailData[5].decode()
        _cont = accountMailData[6].decode()
        _opUUID = int(accountMailData[7].decode())
        _srcType = int(accountMailData[8].decode())
        _srcSubType = int(accountMailData[9].decode())
        desc = accountMailData[10].decode()
        _idipSource = int(accountMailData[11].decode())
        attach = parseAttachStr(_attachStr)
        despArgs = parseDespStr(_despArgsStr)
        globalMailGBID = KBEngine.genUUID64()
        sendMailToPlayers(
            [playerGBID], 
            _mailId, 
            extraAttach=attach, 
            despArgs=despArgs,title=_title,cont=_cont,
            srcType=_srcType, srcSubType=_srcSubType, opUUID=_opUUID, desc=desc, idipSource=_idipSource, globalMailGBID=globalMailGBID,
            callback=lambda ret, num, insertId, err, mailGBID:\
                            _sendAccountMailToPlayerCallback(ret, num, insertId, err, mailGBID, playerGBID, entityId))

def _sendAccountMailToPlayerCallback(ret, num, insertId, err, mailGBID, playerGBID, entityId):
    LOG_INFO('_sendAccountMailCallback:', ret, num, insertId, err, mailGBID, playerGBID, entityId)
    if err:
        LOG_ERR('_sendAccountMailCallback:', ret, num, insertId, err, mailGBID, playerGBID, entityId)

    g_AccountMailNumDic[playerGBID] = g_AccountMailNumDic.get(playerGBID, 0)-1
    if g_AccountMailNumDic[playerGBID] > 0:
        return
    g_AccountMailNumDic.pop(playerGBID)
    _onCheckAccountMailFinished(entityId)

def _onCheckAccountMailFinished(entityId):
    _avatarEnt = KBEngine.entities.get(entityId)
    if not _avatarEnt or _avatarEnt.isDestroying :
        return
    _avatarEnt.onCheckAccountMailsFinished()

def sendIDIPMailByGBID(su, toGBID, dueTime, extraAttach, title, cont, srcType, srcSubType, desc):
    mailId = dataUtils.getConstVal('customizedMail')
    sendMailToPlayers([toGBID], mailId, extraAttach, dueTime=dueTime, title=title, cont=cont, srcType=srcType, srcSubType=srcSubType,
                      desc=desc, callback=lambda ret, num, insertId, err, mailID:
                                                _sendIDIPMailByGBIDCallback(ret, num, insertId, err, su, mailID,
                                                                            toGBID))
    return

def _sendIDIPMailByGBIDCallback(ret, num, insertId, err, su, mailGBID, toGBID):
    LOG_INFO('_sendIDIPMailByGBIDCallback, mailGBID:', mailGBID)
    if err:
        gameengine.panicStack('_sendIDIPMailByGBIDCallback:', err, toGBID)
        su.onCommandResult(gameconst.GMCommandErr.GM_RET_SEND_MAIL_ERR, err, {'gbID': toGBID, 'mailID': mailGBID})
    else:
        su.onCommandResult(gameconst.GMCommandErr.GM_RET_OK, '', {})
