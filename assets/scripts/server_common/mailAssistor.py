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
                      opUUID=0, desc='', idipSource=0, callback=None):
    if not toGBIDList:
        return
    INFO_MSG('sendMailToPlayers:', len(toGBIDList), mailId)
    toGBIDList = toGBIDList[:]
    title = title or ''
    cont = cont or ''
    for _ in range(SEND_NUM_PER_TIME):
        if not toGBIDList:
            break
        toGBID = toGBIDList.pop()
        _sendMailToSinglePlayer(toGBID, mailId, extraAttach, despArgs, title, cont, fromGBID, globalMailGBID,
                                createTime, expiredTime, srcType, srcSubType, opUUID, desc, idipSource, callback)
    if toGBIDList:
        KBEngine.addTimer(0.1, 0, lambda timerId :sendMailToPlayers(toGBIDList, mailId, extraAttach, despArgs, fromGBID,
                        globalMailGBID, createTime, expiredTime, title, cont, srcType, srcSubType, opUUID, desc, idipSource, callback))
    return


def _sendMailToSinglePlayer(toGBID, mailId, extraAttach:dropAward.MailWealthVal, despArgs, title, cont, fromGBID,
                      globalMailGBID, createTime, expiredTime, srcType, srcSubType, opUUID, desc, idipSource, callback):
    INFO_MSG('_sendMailToSinglePlayer:', toGBID, mailId)
    if len(despArgs) != MAMAD.MailArgsNumMap[mailId]:
        gameengine.reportCritical(' _sendMailToSinglePlayer, despArgs num error:', mailId, despArgs)
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
    createTime = createTime or utils.getNow()
    expiredTime = expiredTime if expiredTime else calcMailExpiredTime(mailId, createTime, mailData)
    despArgs = [str(arg) for arg in despArgs]
    title = title.strip(' ')
    cont = cont.strip(' ')

    attachStr = attach.getItemsTLogStr()

    sendMailCallback = lambda ret, num, insertId, err:\
        _sendMailToPlayerCallback(ret, num, insertId, err, toGBID, mailId, mailGBID, title, cont, attachStr, srcType, srcSubType,
                                  opUUID, desc, idipSource, callback)
    gamesql.sendMailByGBID(toGBID, mailId, mailGBID, globalMailGBID, readStat, createTime, expiredTime, fromGBID,
           attach, attachStat, despArgs, title, cont, opUUID, srcType, srcSubType, desc, idipSource, sendMailCallback)
    return

def _sendMailToPlayerCallback(ret, num, insertId, err, toGBID, mailId, mailGBID, title, cont, attachStr, srcType, srcSubType,
                              opUUID, desc, idipSource, senderCallback=None):
    INFO_MSG('_sendMailToPlayerCallback:', ret, num, insertId, err, toGBID, mailId)
    senderCallback and senderCallback(ret, num, insertId, err, mailGBID)
    if err:
        gameengine.reportCritical('_sendMailToPlayerCallback:', err, toGBID)
        return
    _onSendMailByGBIDSucc(toGBID, mailId, mailGBID, title, cont, attachStr, srcType, srcSubType, opUUID, desc, idipSource)

def _onSendMailByGBIDSucc(toGBID, mailId, mailGBID, title, cont, attachStr, srcType, srcSubType, opUUID, desc, idipSource):
    entId = gameglobal.roleGBIDToEntId.get(toGBID, 0)
    avatarEnt = KBEngine.entities.get(entId)
    if avatarEnt:
        #在线
        if gameengine.isCell():
            avatarEnt.base.onNewMailInsertSucc(mailId, mailGBID, title, cont, attachStr, srcType, srcSubType, opUUID, desc, idipSource)
        else:
            avatarEnt.onNewMailInsertSucc(mailId, mailGBID, title, cont, attachStr, srcType, srcSubType, opUUID, desc, idipSource)
    else:
        failedBox = random.choice(gameengine.getAllBaseApps())
        failedArgs = (mailId, mailGBID, title, cont, attachStr, srcType, srcSubType, opUUID, desc, idipSource)
        gameengine.getGlobalBase('PlayerStub').doOnOthersBase([toGBID], 'onNewMailInsertSucc',
                                        (mailId, mailGBID, title, cont, attachStr, srcType, srcSubType, opUUID, desc, idipSource),
                                                              failedBox, 'recordOfflinePlayerMailLog', failedArgs)
    LogTrackingMgr.LogTrackingMgr.Mail_Send(toGBID, mailId, mailGBID, srcType, srcSubType, opUUID, idipSource, attachStr)

def doRecordOfflinePlayerMailLog(toGBID, mailId, mailGBID, title, cont, attachStr, srcType, srcSubType, opUUID, desc, idipSource):
    #sql = "select sm_accountName, sm_accountType, sm_name, sm_level from tbl_Avatar where sm_gbID=%s" % toGBID
    sql = "select Avatar.sm_accountName, Avatar.sm_accountType, Avatar.sm_name, Avatar.sm_level, Account.sm_channelId "\
          "from tbl_Avatar as Avatar left join tbl_Account as Account on Avatar.sm_accountDBID=Account.id where "\
          "Avatar.sm_gbID=%s" % toGBID
    KBEngine.executeRawDatabaseCommand(sql, lambda ret, num, insertId, err: _loadOfflinePlayerDataCallback(ret, num,
                           insertId, err, toGBID, mailId, mailGBID, title, cont, attachStr, srcType, srcSubType, opUUID, desc, idipSource))

def _loadOfflinePlayerDataCallback(ret, num, insertId, err, toGBID, mailId, mailGBID, title, cont, attachStr,
                                    srcType, srcSubType, opUUID, desc, idipSource):
    if err:
        gameengine.reportCritical('_loadOfflinePlayerDataCallback:', err, toGBID)
        return

    if not ret:
        INFO_MSG('_loadOfflinePlayerDataCallback, no ret', toGBID)
        return
    return

def getMyGlobalsMails(lastGBMailTime, roleRegTime, roleLevel, hasGotGlobalMails):
    INFO_MSG('in getMyGlobalsMails, lastGBMailTime:', lastGBMailTime, roleRegTime, roleLevel)
    gbMails = []
    mailMaxNum = MACF.datas['mailNumMax']['value']
    for mail in reversed(gameglobal.globalMailsCacheList):
        if mail.isExpired() or mail.isTracebackTimeOut():
            continue
        if roleRegTime < mail.minRoleTime or roleRegTime > mail.maxRoleTime:
            continue
        if roleLevel < mail.minRoleLevel or roleLevel > mail.maxRoleLevel:
            continue
        if mail.globalMailGBID in hasGotGlobalMails:
            continue
        # if lastGBMailTime >= mail.createTime:
        #     break
        gbMails.append(mail)
        if len(gbMails) >= mailMaxNum:
            #最多同步最新的mailMaxNum封全服邮件
            break
    return gbMails

def getLastGlobalMailTime():
    return gameglobal.globalMailsCacheList[-1].createTime if gameglobal.globalMailsCacheList else 0

AccountMailNumDic = {}

def checkAccountMails(accountName, accountType, playerGBID, entityId):
    INFO_MSG('checkAccountMails:', accountName, accountType, playerGBID, entityId)
    gamesql.loadMailByAccountInfo(accountName,accountType,playerGBID,
    lambda ret, num, insertId, err, playerGBID=playerGBID, entityId=entityId:
                _checkAccountMailsCallback(ret, num, insertId, err, playerGBID, entityId))

def _checkAccountMailsCallback(ret, num, insertId, err, playerGBID, entityId):
    INFO_MSG('_checkAccountMailsCallback:', ret, num, insertId, err, playerGBID, entityId)
    if err:
        gameengine.reportCritical('_checkAccountMailsCallback:', err, playerGBID, entityId)
        _onCheckAccountMailFinished(entityId)
        return

    if 0 == len(ret):
        _onCheckAccountMailFinished(entityId)
        return

    INFO_MSG('_checkAccountMailsCallback, found account mail:', ret)
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
        sendMailToPlayers([playerGBID], mailId, extraAttach=attach, despArgs=despArgs,title=title,cont=cont,
                          srcType=srcType, srcSubType=srcSubType, opUUID=opUUID, desc=desc, idipSource=idipSource,
                          callback=lambda ret, num, insertId, err, mailGBID:
                            _sendAccountMailToPlayerCallback(ret, num, insertId, err, mailGBID, playerGBID, entityId))
    return

def _sendAccountMailToPlayerCallback(ret, num, insertId, err, mailGBID, playerGBID, entityId):
    INFO_MSG('_sendAccountMailCallback:', ret, num, insertId, err, mailGBID, playerGBID, entityId)
    if err:
        ERROR_MSG('_sendAccountMailCallback:', ret, num, insertId, err, mailGBID, playerGBID, entityId)

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

def sendIDIPMailByGBID(su, toGBID, extraAttach, title, cont, srcType, srcSubType, desc):
    mailId = dataUtils.getConstVal('customizedMail')
    sendMailToPlayers([toGBID], mailId, extraAttach, title=title, cont=cont, srcType=srcType, srcSubType=srcSubType,
                      desc=desc, callback=lambda ret, num, insertId, err, mailID:
                                                _sendIDIPMailByGBIDCallback(ret, num, insertId, err, su, mailID,
                                                                            toGBID))
    return

def _sendIDIPMailByGBIDCallback(ret, num, insertId, err, su, mailGBID, toGBID):
    INFO_MSG('_sendIDIPMailByGBIDCallback, mailGBID:', mailGBID)
    if err:
        gameengine.reportCritical('_sendIDIPMailByGBIDCallback:', err, toGBID)
        su.onCommandResult(gameconst.GMCommandErr.SEND_MAIL_ERR, err, {'gbID': toGBID, 'mailID': mailGBID})
    else:
        su.onCommandResult(gameconst.GMCommandErr.OK, '', {})
