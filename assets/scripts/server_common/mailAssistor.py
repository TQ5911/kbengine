# -*- coding: utf-8 -*-

import KBEngine
from KBEDebug import *
import dropAward
import mail_mail as MAMAD
import mail_config as MACF
import gameengine
import utils
import gamesql
import gameconst
import time
import gameglobal
import dataUtils
# import idipDef
import gamelog
import gameconfig
import random

import LogTrackingMgr


MAIL_EXPIRED_TIME_DEFAULT = 2145888000  #2038年
SEND_NUM_PER_TIME = 50


def calcMailExpiredTime(mailId, createTime, mailData=None):
    if not mailData:
        mailData = MAMAD.datas[mailId]
    expired = mailData.get('period', '')
    if not expired:
        return MAIL_EXPIRED_TIME_DEFAULT
    if expired.isdigit():
        return createTime + 3600 * int(expired)
    else:
        return int(time.mktime(time.strptime(expired, "%Y-%m-%d-%H-%M")))

def parseAttachStr(attachStr):
    attach = dropAward.MailWealthVal()
    attachStr = attachStr.replace(' ', '')
    attachStr = attachStr.strip('[]();')
    if attachStr:
        itemStrList = attachStr.split(';')
        for oneItemStr in itemStrList:
            oneItemList = oneItemStr.split(',')
            itemId = int(oneItemList[0])
            itemNum = int(oneItemList[1])
            if len(oneItemList) == 3:
                bindType = int(oneItemList[2])
            else:
                bindType = dataUtils.getItemDefaultBindType()
            attach.addWealthByItemId(itemId, itemNum, bindType)
    return attach

def parseDespStr(despArgsStr):
    despArgsStr = despArgsStr.replace(' ', '')
    despArgsStr = despArgsStr.strip('[]()')
    if despArgsStr:
        despArgs=despArgsStr.split(',')
    else:
        despArgs=()
    return despArgs


def sendMailToPlayers(toGBIDList, mailId, extraAttach: dropAward.MailWealthVal=None, despArgs=(), fromGBID=0,
                      globalMailGBID=0, createTime=0, expiredTime=0, title=None, cont=None, srcType=0, srcSubType=0,
                      opUUID=0, desc='', idipSource=0, callback=None, isGlobal=False, dueTime=0):
    
    LOG_INFO('sendMailToPlayers:', len(toGBIDList), mailId)

    if not toGBIDList:
        callback and callback(None, None, None, "sendMailToPlayers no target", mailId)
        return

    mailData = MAMAD.datas.get(mailId, None)
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
    for _ in range(SEND_NUM_PER_TIME):
        if not toGBIDList:
            break
        toGBID = toGBIDList.pop()
        _sendMailToSinglePlayer(toGBID, mailId, dueTime, extraAttach, despArgs, title, cont, fromGBID, globalMailGBID,
                                createTime, expiredTime, srcType, srcSubType, opUUID, desc, idipSource, isGlobal, callback)
    if toGBIDList:
        KBEngine.addTimer(0.1, 0, lambda timerId :sendMailToPlayers(toGBIDList, mailId, extraAttach, despArgs, fromGBID,
                        globalMailGBID, createTime, expiredTime, title, cont, srcType, srcSubType, opUUID, desc, idipSource, callback, isGlobal, dueTime))
    return


def _sendMailToSinglePlayer(toGBID, mailId, dueTime, extraAttach:dropAward.MailWealthVal, despArgs, title, cont, fromGBID,
                      globalMailGBID, createTime, expiredTime, srcType, srcSubType, opUUID, desc, idipSource, isGlobal, callback):
    LOG_INFO('_sendMailToSinglePlayer:', toGBID, mailId, dueTime, globalMailGBID, isGlobal)
    if len(despArgs) != MAMAD.MailArgsNumMap[mailId]:
        gameengine.panicStack(' _sendMailToSinglePlayer, despArgs num error:', mailId, despArgs)
        callback and callback(None, None, None, "_sendMailToSinglePlayer despArgs err", mailId)
        return

    mailData = MAMAD.datas.get(mailId, None)
    if not mailData:
        callback and callback(None, None, None, "_sendMailToSinglePlayer not config", mailId)
        return False

    if not mailData['isOpen']:
        callback and callback(None, None, None, "_sendMailToSinglePlayer not isOpen", mailId)
        return False

    mailGBID = globalMailGBID if globalMailGBID else KBEngine.genUUID64()
    rewardId = mailData.get('rewardId')
    attach = dropAward.MailWealthVal()
    if rewardId > 0:
        attach.addWealthByRewardId(rewardId)

    if extraAttach:
        attach += extraAttach

    if attach.mailWealthExceedUplimit():
        callback and callback(None, None, None, "_sendMailToSinglePlayer mailWealthExceedUplimit", mailId)
        attach.reduceItemToMaxNum()
        #return False

    if attach.isEmpty():
        attachStat = gameconst.MailAttachState.HasGET
    else:
        attachStat = gameconst.MailAttachState.NotGet

    readStat = gameconst.MailReadState.NotRead
    createTime = createTime or utils.curTS()
    expiredTime = expiredTime if expiredTime else calcMailExpiredTime(mailId, createTime, mailData)
    despArgs = [str(arg) for arg in despArgs]
    title = title.strip(' ')
    cont = cont.strip(' ')

    attachStr = attach.getItemsTLogStr()

    sendMailCallback = lambda ret, num, insertId, err:\
        _sendMailToPlayerCallback(ret, num, insertId, err, toGBID, mailId, mailGBID, title, cont, attachStr, srcType, srcSubType,
                                  opUUID, desc, idipSource, isGlobal, callback, dueTime)
    gamesql.sendMailByGBID(toGBID, mailId, mailGBID, globalMailGBID, readStat, dueTime, createTime, expiredTime, fromGBID,
           attach, attachStat, despArgs, title, cont, opUUID, srcType, srcSubType, desc, idipSource, sendMailCallback)
    return

def _sendMailToPlayerCallback(ret, num, insertId, err, toGBID, mailId, mailGBID, title, cont, attachStr, srcType, srcSubType,
                              opUUID, desc, idipSource, isGlobal, senderCallback=None, dueTime = 0):
    LOG_INFO('_sendMailToPlayerCallback:', ret, num, insertId, err, toGBID, mailId, isGlobal, dueTime)
    senderCallback and senderCallback(ret, num, insertId, err, mailGBID)
    if err:
        gameengine.panicStack('_sendMailToPlayerCallback:', err, toGBID)
        return
    _onSendMailByGBIDSucc(toGBID, mailId, mailGBID, title, cont, attachStr, srcType, srcSubType, opUUID, desc, idipSource, isGlobal)

def _onSendMailByGBIDSucc(toGBID, mailId, mailGBID, title, cont, attachStr, srcType, srcSubType, opUUID, desc, idipSource, isGlobal):
    entId = gameglobal.roleGBIDToEntId.get(toGBID, 0)
    avatarEnt = KBEngine.entities.get(entId)
    if avatarEnt:
        #在线
        if gameengine.isCell():
            avatarEnt.base.onNewMailInsertSucc(mailId, mailGBID, title, cont, attachStr, srcType, srcSubType, opUUID, desc, idipSource, isGlobal)
        else:
            avatarEnt.onNewMailInsertSucc(mailId, mailGBID, title, cont, attachStr, srcType, srcSubType, opUUID, desc, idipSource, isGlobal)
    else:
        gameengine.getGlobalBase('PlayerStub').doOnOthersBase([toGBID], 'onNewMailInsertSucc',
                                        (mailId, mailGBID, title, cont, attachStr, srcType, srcSubType, opUUID, desc, idipSource, isGlobal),
                                                              None, '', ())
    mailData = MAMAD.datas[mailId]
    LogTrackingMgr.LogTrackingMgr.Mail_Send(toGBID, mailId, mailData['type'], mailGBID, srcType, srcSubType, opUUID, idipSource, attachStr) 

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

AccountMailNumDic = {}

def checkAccountMails(accountName, accountType, playerGBID, entityId):
    LOG_INFO('checkAccountMails:', accountName, accountType, playerGBID, entityId)
    gamesql.loadMailByAccountInfo(accountName,accountType,playerGBID,
    lambda ret, num, insertId, err, playerGBID=playerGBID, entityId=entityId:
                _checkAccountMailsCallback(ret, num, insertId, err, playerGBID, entityId))

def _checkAccountMailsCallback(ret, num, insertId, err, playerGBID, entityId):
    LOG_INFO('_checkAccountMailsCallback:', ret, num, insertId, err, playerGBID, entityId)
    if err:
        gameengine.panicStack('_checkAccountMailsCallback:', err, playerGBID, entityId)
        _onCheckAccountMailFinished(entityId)
        return

    if 0 == len(ret):
        _onCheckAccountMailFinished(entityId)
        return

    LOG_INFO('_checkAccountMailsCallback, found account mail:', ret)
    AccountMailNumDic[playerGBID] = len(ret)
    for accountMailData in ret:
        #accountName = accountMailData[0].decode()
        mailId = int(accountMailData[1].decode())
        mailData = MAMAD.datas[mailId]
        if mailData['type'] != gameconst.MailType.GLOBAL_MAIL_ACCOUNT:
            continue
        #sendTime = int(accountMailData[2].decode())
        attachStr = accountMailData[3].decode()
        despArgsStr = accountMailData[4].decode()
        title = accountMailData[5].decode()
        cont = accountMailData[6].decode()
        opUUID = int(accountMailData[7].decode())
        srcType = int(accountMailData[8].decode())
        srcSubType = int(accountMailData[9].decode())
        desc = accountMailData[10].decode()
        idipSource = int(accountMailData[11].decode())
        attach = parseAttachStr(attachStr)
        despArgs = parseDespStr(despArgsStr)
        globalMailGBID = KBEngine.genUUID64()
        sendMailToPlayers([playerGBID], mailId, extraAttach=attach, despArgs=despArgs,title=title,cont=cont,
                          srcType=srcType, srcSubType=srcSubType, opUUID=opUUID, desc=desc, idipSource=idipSource, globalMailGBID=globalMailGBID,
                          callback=lambda ret, num, insertId, err, mailGBID:
                            _sendAccountMailToPlayerCallback(ret, num, insertId, err, mailGBID, playerGBID, entityId))
    return

def _sendAccountMailToPlayerCallback(ret, num, insertId, err, mailGBID, playerGBID, entityId):
    LOG_INFO('_sendAccountMailCallback:', ret, num, insertId, err, mailGBID, playerGBID, entityId)
    if err:
        LOG_ERR('_sendAccountMailCallback:', ret, num, insertId, err, mailGBID, playerGBID, entityId)

    AccountMailNumDic[playerGBID] = AccountMailNumDic.get(playerGBID, 0)-1
    if AccountMailNumDic[playerGBID] > 0:
        return
    AccountMailNumDic.pop(playerGBID)
    _onCheckAccountMailFinished(entityId)
    return

def _onCheckAccountMailFinished(entityId):
    avatarEnt = KBEngine.entities.get(entityId)
    if not avatarEnt or avatarEnt.isDestroying :
        return
    avatarEnt.onCheckAccountMailsFinished()
    return

def recordDeleteMailLog(accountType, accountName, vRoleID, vRoleName, iLevel, srcType, srcSubType, desc, idipSource,
                        Sequence, MailGBID, attachStr, accountChannelId):
    logDataDic = {
        'vGameAppid': utils.getGameAppId(accountChannelId),
        'PlatID': utils.getPlatIdByAccountType(accountType),
        'iZoneAreaID': gameconfig.serverId(),
        'vOpenID': accountName,
        'vRoleID': vRoleID,
        'vRoleName': vRoleName,
        'iLevel': iLevel,
        'iVipLevel': 0,
        'Reason': srcType,
        'SubReason': srcSubType,
        'Detail': desc,
        'IDIPSource': idipSource,
        'Sequence': Sequence,
        'MailGBID': MailGBID,
    }
    gamelog.makePlayerDeleteMailLog(logDataDic)

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
