# -*- coding: utf-8 -*-
import json

import KBEngine

from KBEDebug import *

import mail_config as MACF
import collections

import gameglobal
import utils
import gameconfig
import _pickle as cPickle
import gameengine
import gameconst
import dataUtils
import dropAward


def createExtraIndex():
    # 创建数据库中某些表的uniq索引
    # sql = "CALL gamesp_createindex('tbl_Avatar_inv_item','invItemIdIndex', 'sm_id', 0)"
    #
    # KBEngine.executeRawDatabaseCommand(sql)
    pass


def onSqlCallback(ret, num, insertId, err, msg):
    if err:
        ERROR_MSG('onSqlCallback error:', err, msg)


def getCustomConfig(callback=None):
    sql = "SELECT name, value from game_config"
    KBEngine.executeRawDatabaseCommand(sql, lambda result, rows, iid, err: _onGetCustomConfig(result, rows, iid, err,
                                                                                              callback))


def _onGetCustomConfig(result, rows, insertid, error, callback):
    DEBUG_MSG('_onGetCustomConfig', error)
    if error:
        if KBEngine.component != 'interfaces':
            ERROR_MSG('_onGetCustomConfig error:', error)
        return
    gameconfig.loadCustomConfig(result)

    if callback:
        callback()


def checkAdminCmdSerial(cmdSerial, callback):
    sql = 'SELECT `tWhen`, `result`,`retErrMsg`, `retStr` FROM `game_admin_cmds` WHERE cmdSerial="%s" limit 1' % (
        cmdSerial,)
    KBEngine.executeRawDatabaseCommand(sql, callback)


def recordAdminCmdSucc(cmdSerial, result, retErrMsg, resultBytes):
    def _onRecordAdminCmd(ret, num, insertId, err):
        if err:
            ERROR_MSG("recordAdminCmdSucc error", ret, num, insertId, err)

    resutlStr = resultBytes.decode('utf-8')
    sql = 'INSERT INTO `game_admin_cmds` (`cmdSerial`, `tWhen`, `result`, `retErrMsg`, `retStr`) VALUES ("%s", %s, %s, %s, %s)' % (
        cmdSerial,
        utils.getNow(), result, utils.escape_string(retErrMsg), utils.escape_string(resutlStr))
    DEBUG_MSG("recordAdminCmdSucc", sql)
    KBEngine.executeRawDatabaseCommand(sql, _onRecordAdminCmd)


def deleteExpiredAdminCmdSerial():
    sql = 'DELETE FROM `game_admin_cmds` WHERE `tWhen`<%s' % (utils.getNow() - gameconst.ONE_WEEK_SECONDS,)
    KBEngine.executeRawDatabaseCommand(sql)


def recordEntityDBID(entityType, dbid):
    if gameglobal.entityTypeToDBID and entityType in gameglobal.entityTypeToDBID:
        if dbid != gameglobal.entityTypeToDBID[entityType]:
            raise Exception('zt: error while recording entity dbid: %s %s' % (entityType, dbid))
        return
    sql = 'INSERT INTO `game_entity_dbid` (entityType, entityDBID) VALUES ("%s", %s) ON DUPLICATE KEY UPDATE entityDBID=VALUES(entityDBID)' % (
        entityType, dbid)
    KBEngine.executeRawDatabaseCommand(sql, lambda ret, num, insertId, err, entityType=entityType,
                                                   dbid=dbid: _onRecordEntityDBID(ret, num, insertId, err, entityType,
                                                                                  dbid))


def deleteEntityDBID(entityType):
    sql = 'DELETE FROM `game_entity_dbid` WHERE entityType="%s"' % (entityType,)
    KBEngine.executeRawDatabaseCommand(sql)


def _onRecordEntityDBID(ret, num, insertId, err, entityType, dbid):
    if type(err) is str and err:
        raise Exception('zt: _onRecordEntityDBID error: %s %s %s' % (err, entityType, dbid))


def getAvatarBasicInfoByPlayerNameOrGBIDOrObID(playerNameOrGBIDOrObID, callback):
    if utils.isGbId(playerNameOrGBIDOrObID):
        sql = """SELECT sm_gbID, sm_name, sm_accountName, id FROM tbl_Avatar WHERE sm_gbID = %s""" % playerNameOrGBIDOrObID
    elif utils.isRoleName(playerNameOrGBIDOrObID):
        sql = """SELECT sm_gbID, sm_name, sm_accountName, id FROM tbl_Avatar WHERE sm_name = BINARY %s""" % utils.escape_string(
            playerNameOrGBIDOrObID)
    else:
        ERROR_MSG('in getAvatarBasicInfoByPlayerNameOrGBID, playerNameOrGBID error:', playerNameOrGBIDOrObID)
        return
    KBEngine.executeRawDatabaseCommand(sql, callback)


def loadLastGlobalMailInfo(playerGbId, callback):
    sql = '''CALL gamesp_load_last_global_mail_info(%s,%s)'''%(playerGbId, 0)
    KBEngine.executeRawDatabaseCommand(sql, callback)

def updateLastGlobaMailInfo(playerGBID, lastGlobalMailTime, callback):
    sql = """UPDATE game_last_global_mail_info SET lastGlobalMailTime=%s where gbId=%s and lastGlobalMailTime<%s"""%(
        lastGlobalMailTime, playerGBID, lastGlobalMailTime)
    KBEngine.executeRawDatabaseCommand(sql, callback)

def sendMailByGBID(toGBID, mailId, mailGBID, globalMailGBID, readStat, createTime, expiredTime, fromGBID, attach,
                   attachStat, despArgs, title, cont, opUUID, srcType, srcSubType, desc, idipSource, callback):
    attach = utils.bytes2hex(cPickle.dumps(attach))
    despArgs = utils.bytes2hex(cPickle.dumps(despArgs))
    sql = '''CALL gamesp_send_mail(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,'%s','%s',%s,%s,%s,'%s',%s)'''%\
          (toGBID, mailId, mailGBID, globalMailGBID, readStat, createTime, expiredTime, fromGBID, attach,
                attachStat, despArgs, title, cont, opUUID, srcType, srcSubType, desc, idipSource)
    DEBUG_MSG('gamesql::sendMailByGBID:', sql)
    KBEngine.executeRawDatabaseCommand(sql, callback)

def loadMailsFromDB(gbId, fromTime, excludeMailList, callback):
    maxMailNum = MACF.datas['mailNumMax']['value']
    fields = '''toGBID,mailId,mailGBID,globalMailGBID,readStat,createTime,expiredTime,fromGBID,attach,attachStat,despArgs,title,cont, opUUID,srcType,srcSubType,desp,idipSource'''
    if excludeMailList:
        mailGBIDStr = ','.join([str(mailGBID) for mailGBID in excludeMailList])
        sql = """SELECT %s FROM %s WHERE toGBID=%s and createTime>=%s and mailGBID not in (%s) ORDER BY createTime DESC limit %s""" % (
            fields, gameconst.TABLE_NAME_GAME_MAIL, gbId, fromTime, mailGBIDStr, maxMailNum * 2)
    else:
        sql = """SELECT %s FROM %s WHERE toGBID=%s and createTime>=%s ORDER BY createTime DESC limit %s""" % (
            fields, gameconst.TABLE_NAME_GAME_MAIL, gbId, fromTime, maxMailNum * 2)
    # DEBUG_MSG('in loadMailsFromDB, sql:', sql)
    KBEngine.executeRawDatabaseCommand(sql, lambda ret, num, insertId, err: callback(ret, num, insertId, err))

def loadMailByMailGBID(gbId, mailGBID, callback):
    fields = '''toGBID,mailId,mailGBID,globalMailGBID,readStat,createTime,expiredTime,fromGBID,attach,attachStat,despArgs,title,cont, opUUID,srcType,srcSubType,desp,idipSource'''
    sql = """SELECT %s FROM %s WHERE toGBID=%s and mailGBID=%s""" % (
        fields, gameconst.TABLE_NAME_GAME_MAIL, gbId, mailGBID)
    #DEBUG_MSG('in loadMailsFromDB, sql:', sql)
    KBEngine.executeRawDatabaseCommand(sql, lambda ret, num, insertId, err:callback(ret,num,insertId,err))

def setMailHasRead(toGBID, mailGBID, callback):
    sql = """UPDATE %s SET readStat=%s where toGBID=%s and mailGBID=%s""" % (gameconst.TABLE_NAME_GAME_MAIL,
                                                                             gameconst.MailReadState.HasRead, toGBID,
                                                                             mailGBID)
    # DEBUG_MSG('in setMultiMailsHasRead, sql:', sql)
    KBEngine.executeRawDatabaseCommand(sql, lambda ret, num, insertId, err: callback(ret, num, insertId, err))


def setMultiMailsHasRead(toGBID, mailGBIDList, callback):
    mailGBIDStr = ','.join([str(mailGBID) for mailGBID in mailGBIDList])
    sql = """UPDATE %s SET readStat=%s where toGBID=%s and mailGBID in (%s)""" % (gameconst.TABLE_NAME_GAME_MAIL,
                                                                                  gameconst.MailReadState.HasRead,
                                                                                  toGBID, mailGBIDStr)
    # DEBUG_MSG('in setMultiMailsHasRead, sql:', sql)
    KBEngine.executeRawDatabaseCommand(sql, lambda ret, num, insertId, err: callback(ret, num, insertId, err))


def setMailHasGetAttach(toGBID, mailGBIDList, callback):
    # 设置附件已领取及邮件已读
    mailGBIDStr = ','.join([str(mailGBID) for mailGBID in mailGBIDList])
    sql = """UPDATE %s SET attachStat=%s, readStat=%s where toGBID=%s and mailGBID in (%s)""" % (
        gameconst.TABLE_NAME_GAME_MAIL,
        gameconst.MailAttachState.HasGET, gameconst.MailReadState.HasRead, toGBID, mailGBIDStr)
    # DEBUG_MSG('in setMailHasGetAttach, sql:', sql)
    KBEngine.executeRawDatabaseCommand(sql, lambda ret, num, insertId, err: callback(ret, num, insertId, err))


def resetMailAttachNotState(toGBID, mailGBID, readState, callback):
    sql = """UPDATE %s SET attachStat=%s, readStat=%s where toGBID=%s and mailGBID=%s""" % (
        gameconst.TABLE_NAME_GAME_MAIL,
        gameconst.MailAttachState.NotGet, readState, toGBID, mailGBID)
    # DEBUG_MSG('in setMailHasGetAttach, sql:', sql)
    KBEngine.executeRawDatabaseCommand(sql, lambda ret, num, insertId, err: callback(ret, num, insertId, err))


def deleteMailByMailGBID(toGBID, mailGBID, callback):
    sql = """DELETE FROM %s WHERE toGBID=%s AND mailGBID=%s""" % (gameconst.TABLE_NAME_GAME_MAIL, toGBID, mailGBID)
    DEBUG_MSG('in deleteMailByMailGBID, sql:', sql)
    KBEngine.executeRawDatabaseCommand(sql, lambda ret, num, insertId, err: callback(ret, num, insertId, err))


def deleteOldMails(toGBID, minMailTime, minMailTiemMailList, callback):
    if minMailTiemMailList:
        mailGBIDStr = ','.join([str(mailGBID) for mailGBID in minMailTiemMailList])
        sql = """DELETE FROM %s WHERE toGBID=%s AND createTime <= %s and mailGBID not in (%s)""" % (
            gameconst.TABLE_NAME_GAME_MAIL, toGBID, minMailTime, mailGBIDStr)
    else:
        sql = """DELETE FROM %s WHERE toGBID=%s AND createTime < %s""" % (
            gameconst.TABLE_NAME_GAME_MAIL, toGBID, minMailTime)
    DEBUG_MSG('in deleteOldMails, sql:', sql)
    KBEngine.executeRawDatabaseCommand(sql, lambda ret, num, insertId, err: callback(ret, num, insertId, err))


def deleteMultiMails(toGBID, mailGBIDList, callback):
    mailGBIDStr = ','.join([str(mailGBID) for mailGBID in mailGBIDList])
    sql = """DELETE FROM %s WHERE toGBID=%s AND mailGBID in (%s)""" % (
        gameconst.TABLE_NAME_GAME_MAIL, toGBID, mailGBIDStr)
    DEBUG_MSG('in deleteMultiMails, sql:', sql)
    KBEngine.executeRawDatabaseCommand(sql, lambda ret, num, insertId, err: callback(ret, num, insertId, err))


def sendMailToAccount(accountName, accountType, mailId, attachStr, despArgsStr, title, cont, opUUID, srcType,
                      srcSubType, desc, idipSource, callback):
    sql = """INSERT INTO game_account_mails (accountName,accountType,mailId,sendTime,attachStr,despStr,title,cont,opUUID,srcType,srcSubType,desp,idipSource) VALUES('%s',%s,%s,%s,'%s','%s','%s','%s',%s,%s,%s,'%s',%s)""" % \
          (accountName, accountType, mailId, utils.getNow(), attachStr, despArgsStr, title, cont, opUUID, srcType,
           srcSubType, desc, idipSource)
    DEBUG_MSG('in sendMailToAccount, sql:', sql)
    KBEngine.executeRawDatabaseCommand(sql, lambda ret, num, insertId, err: callback(ret, num, insertId, err))


def loadMailByAccountInfo(accountName, accountType, playerGBID, callback):
    sql = """CALL gamesp_load_account_mails('%s',%s,%s)""" % (accountName, accountType, playerGBID)
    # DEBUG_MSG('in loadMailByAccountInfo, sql:', sql)
    KBEngine.executeRawDatabaseCommand(sql, lambda ret, num, insertId, err: callback(ret, num, insertId, err))


def getAvatarInfoFromDB(gbIds, callback):
    if len(gbIds) == 1:
        _str = '= {}'.format(gbIds[0])
    else:
        _str = 'in ({})'.format(','.join((str(gbId) for gbId in gbIds)))

    sql = """SELECT a.sm_gbID, a.sm_name, a.sm_school, a.sm_sex, a.sm_level, a.sm_accountName, a.sm_totalScore, a.id, \
        a.sm_tLastOfflineBase, a.sm_avatarFlag, a.sm_appearance_outfitData_picFrameId, a.sm_accountType, a.sm_obId, c.sm_channelId\
        FROM tbl_Avatar a left join tbl_Account c on a.sm_accountDBID = c.id WHERE a.sm_gbID %s""" % _str
    KBEngine.executeRawDatabaseCommand(sql, callback)

def setServerStateInfo(name, value, callback):
    sql = """REPLACE INTO game_state_info (name, value) VALUES ('%s', %d)""" % (name, value)
    KBEngine.executeRawDatabaseCommand(sql, callback)


def checkAccountWhiteList(accountName, callback):
    sql = "select id from game_login_white_list where accountName=%s" % utils.escape_string(accountName)
    KBEngine.executeRawDatabaseCommand(sql, callback)


def addAccountWhiteList(accountName):
    sql = "insert into game_login_white_list (accountName, accountGmMode) values (%s, %s)" % (
        utils.escape_string(accountName), 0)
    KBEngine.executeRawDatabaseCommand(sql)


def deleteAccountWhiteList(accountName):
    sql = """DELETE FROM game_login_white_list where accountName=%s""" % utils.escape_string(accountName)
    KBEngine.executeRawDatabaseCommand(sql)

def loadAvatarAppearanceDataFromDB(gbIdList, callback):
    gbIdStr = ','.join([str(gbId) for gbId in gbIdList])
    sql = 'select id, sm_gbID, sm_birthInDB, sm_school, sm_sex, sm_level, sm_appearance_weapon, ' \
          'sm_appearance_breast, sm_appearance_faceData_suitId,' \
          'sm_appearance_faceData_hairIdFaceId, sm_appearance_faceData_hairColorIdSkinColorId, ' \
          'sm_appearance_outfitData_hairId, sm_appearance_outfitData_clothesId, ' \
          'sm_appearance_outfitData_picFrameId, sm_appearance_outfitData_wingId, ' \
          'sm_appearance_outfitData_mountId from tbl_Avatar where sm_gbID in (%s)' % (gbIdStr,)
    KBEngine.executeRawDatabaseCommand(sql, callback)
    return

def loadAvatarOutfitDataFromDB(parentIDList, callback):
    parentIDStr = ','.join([str(parentID) for parentID in parentIDList])
    sql = 'select parentID, sm_outfitType, sm_outfitId, sm_expireTime from tbl_Avatar_outfitInfo_outfitList where parentID in (%s)' % (
        parentIDStr,)
    KBEngine.executeRawDatabaseCommand(sql, callback)
    return


def updateCharacterParentID(accountName, targetAvatarGbId):
    sql = "update tbl_Account_characters_characters set parentID = (select entityDBID from kbe_accountinfos where accountName = '%s') WHERE sm_gbId = %s" % (
        accountName, targetAvatarGbId)
    KBEngine.executeRawDatabaseCommand(sql)


def countCharacterNum(accountName, callback):
    sql = "select b.accountName,a.sm_name from tbl_Account_characters_characters a right join kbe_accountinfos b on a.parentID = b.entityDBID where b.accountName = {} ".format(
        utils.escape_string(accountName))
    KBEngine.executeRawDatabaseCommand(sql, callback)


# def forbidLogin(accountName, forbidType, forbidTime, forbidReason):
#     sql = "update tbl_Account set sm_forbidLoginFlag = {},sm_forbidLoginType = {},sm_forbidLoginTime = {},sm_forbidLoginReason = {} WHERE id = (select entityDBID from kbe_accountinfos where accountName = {})".format(
#         1, forbidType, forbidTime, utils.escape_string(forbidReason), utils.escape_string(accountName))
#     KBEngine.executeRawDatabaseCommand(sql)


def getForbidLoginProp(accountName, callback):
    sql = "select sm_isDelete from tbl_Account WHERE id = (select entityDBID from kbe_accountinfos where accountName = {})".format(
        utils.escape_string(accountName))
    KBEngine.executeRawDatabaseCommand(sql, callback)


# def unforbidLogin(accountName):
#     sql = "update tbl_Account set sm_forbidLoginFlag = 0 WHERE id = (select entityDBID from kbe_accountinfos where accountName = {})".format(
#         utils.escape_string(accountName))
#     KBEngine.executeRawDatabaseCommand(sql)


def forbidVoiceChat(accountName, forbidType, forbidTime, forbidReason):
    sql = "update tbl_Account set sm_forbidVoiceChatFlag = 1,sm_forbidVoiceChatType = {},sm_forbidVoiceChatTime = {},sm_forbidVoiceChatReason = {} WHERE id = (select entityDBID from kbe_accountinfos where accountName = {}) ".format(
        forbidType, forbidTime, utils.escape_string(forbidReason), utils.escape_string(accountName))
    KBEngine.executeRawDatabaseCommand(sql)


def unforbidVoiceChat(accountName):
    sql = "update tbl_Account set sm_forbidVoiceChatFlag = 0 WHERE id = (select entityDBID from kbe_accountinfos where accountName = {}) ".format(
        utils.escape_string(accountName))
    KBEngine.executeRawDatabaseCommand(sql)


def forbidChat(accountName, forbidType, forbidTime, forbidReason):
    sql = "update tbl_Account set sm_forbidChatFlag = 1,sm_forbidChatType = {},sm_forbidChatTime = {},sm_forbidChatReason = {} WHERE id = (select entityDBID from kbe_accountinfos where accountName = {}) ".format(
        forbidType, forbidTime, utils.escape_string(forbidReason), utils.escape_string(accountName))
    KBEngine.executeRawDatabaseCommand(sql)


def unforbidChat(accountName):
    sql = "update tbl_Account set sm_forbidChatFlag = 0 WHERE id = (select entityDBID from kbe_accountinfos where accountName = {}) ".format(
        utils.escape_string(accountName))
    KBEngine.executeRawDatabaseCommand(sql)


def queryAccountDBID(platId, accountName, callback):
    accountType = utils.getAccountTypeByPlatId(platId)
    sql = f"select entityDBID from kbe_accountinfos where accountName = '{accountType}:{accountName}'"
    KBEngine.executeRawDatabaseCommand(sql, callback)


def deleteAccountEntity(platId, accountName, callback):
    accountType = utils.getAccountTypeByPlatId(platId)
    sql = f"delete from kbe_accountinfos where accountName = '{accountType}:{accountName}'"
    KBEngine.executeRawDatabaseCommand(sql, callback)


# region coinAuction.auction

itemDataSqlKeys = (
    "parentID", "sm_autoLoad", "sm_auctionType", "sm_auctionItemUUID", "sm_addTime", "sm_itemData_itemId",
    "sm_itemData_itemNum", "sm_itemData_createTime", "sm_itemData_expireTime",
    "sm_itemData_uniqueId", "sm_itemData_bindType", "sm_itemData_attrJson", "sm_price",
    "sm_number", "sm_bagType", "sm_source", "sm_status", "sm_locked", "sm_extraInfo", "sm_tCreate")

itemDataSqlKeysSet = set(itemDataSqlKeys)

ItemDataSqlClass = collections.namedtuple('ItemDataSqlClass', itemDataSqlKeys)



def queryAvatarLoginTimeByAccountName(accountName, callback):
    sql = f"select sm_tLoginBase from tbl_Avatar where sm_accountName = '{accountName}'"
    INFO_MSG(sql)
    KBEngine.executeRawDatabaseCommand(sql, callback)


def queryAvatarGBIDByAccountName(accountName, callback):
    sql = f"select sm_gbId from tbl_Avatar where sm_accountName = '{accountName}'"
    INFO_MSG(sql)
    KBEngine.executeRawDatabaseCommand(sql, callback)


def queryCountAccountNum(callback):
    sql = 'select count(id) from tbl_Account'
    INFO_MSG(sql)
    KBEngine.executeRawDatabaseCommand(sql, callback)


def queryAvatarObId(gbId, callback):
    sql = f'select sm_obId from tbl_Avatar where sm_gbID={gbId}'
    KBEngine.executeRawDatabaseCommand(sql, callback)


def deleteCrossServerGameAccountInfo(entityDBID):
    sql = f"DELETE FROM `kbe_accountinfos` WHERE entityDBID={entityDBID}"
    KBEngine.executeRawDatabaseCommand(sql)


def dbCommandCallback(ret, num, insertId, err, detail):
    if err:
        ERROR_MSG('db command error:', err, detail)


def _onRecordOfflineCallback(ret, num, insertId, err, gbId, callbackName, args):
    if err:
        ERROR_MSG('_onRecordOfflineCallback error:', err, gbId, callbackName, args)
        return

    nCallback = int(ret[0][0])
    if nCallback > 1000:
        ERROR_MSG('_onRecordOfflineCallback: too many calbacks', nCallback, gbId, callbackName, args)


def recordAvatarOfflineCallback(gbId, callbackName, args):
    data = cPickle.dumps(args)
    if len(data) > 1024 * 60:
        ERROR_MSG('offline callback data overflow:', gbId, callbackName, data.hex())
        return
    sql = 'CALL gamesp_record_avatar_offline_callbacks(%s, %s, 0x%s)' % (
        gbId, utils.escape_string(callbackName), data.hex())
    KBEngine.executeRawDatabaseCommand(sql,
                                       lambda ret, num, insertId, err: _onRecordOfflineCallback(ret, num, insertId, err,
                                                                                                gbId, callbackName,
                                                                                                args))


def _onLoadOfflineCallback(cbData, num, insertId, err, entId, gbId, finishCallback):
    if err:
        ERROR_MSG('_onLoadOfflineCallback err', err, gbId)
        return

    if cbData:
        def _onDeleteCallbacks(err1):
            avatar = KBEngine.entities.get(entId)
            if not avatar or avatar.isDestroyed:
                WARNING_MSG('_onLoadOfflineCallback: player is offline. ', entId, gbId, cbData)
                return

            if err1:
                ERROR_MSG('_onDeleteCallbacks err', err, gbId)
                return

            for _id, callbackName, argData in cbData:
                try:
                    args = cPickle.loads(bytes.fromhex(argData.decode('ascii')))
                    funcName = callbackName.decode('ascii')
                    func = getattr(avatar, funcName)
                    if not getattr(func, 'offlineCall', False):
                        ERROR_MSG('function is not offline callable:', entId, gbId, callbackName, argData)
                        continue
                    func(*args)
                except Exception as e:
                    ERROR_MSG('avatar offline callback error:', gbId, callbackName, argData, e)

            finishCallback and finishCallback()

        delIds = []
        for _id, callbackName, argData in cbData:
            delIds.append(_id.decode('ascii'))
        delSql = 'delete from game_avatar_offline_callbacks where id in (%s)' % (','.join(delIds))
        KBEngine.executeRawDatabaseCommand(delSql, lambda ret, num, insertId, err1: _onDeleteCallbacks(err1))
    else:
        finishCallback and finishCallback()


def loadOfflineCallback(avatar, finishCallback):
    sql = 'SELECT `id`, `callbackName`, hex(`args`) FROM `game_avatar_offline_callbacks` where gbId=%s order by id limit 2000' % avatar.gbID
    KBEngine.executeRawDatabaseCommand(sql,
                                       lambda ret, num, insertId, err: _onLoadOfflineCallback(ret, num, insertId, err,
                                                                                              avatar.id, avatar.gbID,
                                                                                              finishCallback))


def _sendMailCallback(ret, num, insertId, err, toGBID, mailVal, onSendCallback):
    if err:
        ERROR_MSG('_sendMailCallback', err, toGBID, mailVal.mailId, mailVal.mailUUID, mailVal.srcType, mailVal.detail,
                  mailVal.title)
        return

    if onSendCallback:
        onSendCallback(toGBID, mailVal)
    else:
        if toGBID:
            stub = gameengine.getGlobalBase('PlayerStub')

            stub.playerRecvMail(toGBID, mailVal)


def queryAccountDid(gbid, callback):
    sql = f'select sm_did from tbl_Account a join tbl_Avatar b on a.id=b.sm_accountDBID where b.sm_gbID={gbid};'
    INFO_MSG('sql')
    KBEngine.executeRawDatabaseCommand(sql, lambda ret, num, insertId, err: callback(ret, err))


def delAccountClearDB(realAccount, callback):
    accountType, accountName = utils.getAccountTypeAndName(realAccount)
    sql = f'update tbl_Account set sm_userName="", sm_identityCard="", sm_isDelete=1 where sm_accountType={accountType} and \
        sm_accountName="{accountName}")'
    INFO_MSG('delAccountClearDB', sql)
    KBEngine.executeRawDatabaseCommand(sql, callback)


def recoverAccountDB(realAccount, callback):
    accountType, accountName = utils.getAccountTypeAndName(realAccount)
    sql = f'update tbl_Account set sm_isDelete=0 where sm_accountType={accountType} and sm_accountName="{accountName}")'
    INFO_MSG('recoverAccountDB', sql)
    KBEngine.executeRawDatabaseCommand(sql, callback)


def _onChargebackDBUpdate(ret, num, insertId, err, sql, srcType, callback):
    if err:
        ERROR_MSG('chargeBackExtWealth error:', err, sql)
        callback and callback(False, [], None, 0, 0)
        return

    val = None
    srcKeyList = []
    recordNum = 0
    DEBUG_MSG('_onChargebackUpdate status', ret, sql)
    if ret:
        val = dropAward.AwardVal()
        for bsrcKey, bwealth, _recordNum in ret:
            if int(_recordNum) == -1:
                recordNum = int(_recordNum)
                srcKeyList.append(bsrcKey.decode('ascii'))
            else:
                recordNum += int(_recordNum)
                if not bwealth:
                    continue
                wealthVal = cPickle.loads(bytes.fromhex(bwealth.decode('ascii')))
                srcKeyList.append(bsrcKey.decode('ascii'))
                val += wealthVal
        callback and callback(recordNum != -1, srcKeyList, val, recordNum, srcType)
    else:
        # 没有订单
        callback and callback(True, srcKeyList, val, recordNum, srcType)


def checkOfflineDeductWealth(gbId, itemId, deductNum, checkCallback):
    def _onGetItemsInfo(ret, num, insertId, err, alreadyRemovedNum, needDeduct):
        if err:
            checkCallback(gameconst.GMCommandErr.DB_OP_ERR, 0, alreadyRemovedNum, needDeduct)
            return

        if not ret:
            checkCallback(gameconst.GMCommandErr.TARGET_NOT_EXISTS, 0, alreadyRemovedNum, needDeduct)
        else:
            bcoin, bcoinFrac, baupCoin, baupCoinFrac, bbagData = ret[0]
            coin, coinFrac = int(bcoin.decode('ascii')), int(bcoinFrac.decode('ascii'))
            aupCoin, aupCoinFrac = int(baupCoin.decode('ascii')), int(baupCoinFrac.decode('ascii'))
            bagItemList = cPickle.loads(bytes.fromhex(bbagData.decode('ascii')))

            coinVal = coin + coinFrac * 0.01
            aupCoinVal = aupCoin + aupCoinFrac * 0.01
            needDeductTotal = alreadyRemovedNum + needDeduct
            hasNum = 0
            wealthVal = dropAward.DeductWealthVal().addWealthByItemId(itemId, needDeductTotal)

            INFO_MSG(f'checkOfflineDeductWealth: {gbId} need remove {needDeductTotal} {coinVal}')

            itemData = dataUtils.getCommItemData(itemId)
            if not itemData:
                checkCallback(gameconst.GMCommandErr.INTERNAL_ERROR, 0, alreadyRemovedNum, needDeduct)
                return
            if itemData['type'] == gameconst.ItemType.Normal:
                for itDic in bagItemList:
                    if itDic.get('itemId') == itemId:
                        hasNum += itDic.get('itemNum', 0)

                if hasNum < needDeductTotal:
                    checkCallback(gameconst.GMCommandErr.INSUFFICIENT, hasNum, alreadyRemovedNum, needDeduct)
                    return
            elif itemId == gameconst.ItemId.COIN:
                hasNum = coinVal
                if wealthVal.coin.data and wealthVal.coin.data > coinVal:
                    checkCallback(gameconst.GMCommandErr.INSUFFICIENT, coinVal, alreadyRemovedNum, needDeduct)
                    return

            checkCallback(0, hasNum, alreadyRemovedNum, needDeduct)

    def _onGetRemoved(ret, num, insertId, err):
        if err:
            checkCallback and checkCallback(gameconst.GMCommandErr.INTERNAL_ERROR, 0, 0, deductNum)
            return 0

        removedNum = 0
        if ret:
            for bargs, in ret:
                sargs = bargs.decode('ascii')
                args = cPickle.loads(bytes.fromhex(sargs))
                _itemId = args[0]
                totalNum = args[1]
                if _itemId == itemId:
                    removedNum += totalNum

        DEBUG_MSG(f'already del {removedNum}, need del {deductNum}')
        checkLeftSql = 'select sm_coin, sm_coinFraction, sm_auspiciousCoin, sm_auspiciousCoinFraction, hex(sm_bagData_itemsList) from tbl_Avatar where sm_gbID=%s' % gbId
        KBEngine.executeRawDatabaseCommand(checkLeftSql,
                                           lambda _ret, _num, _insertId, _err: _onGetItemsInfo(_ret, _num, _insertId,
                                                                                               _err, removedNum,
                                                                                               deductNum))

    sql = 'select hex(args) from game_avatar_offline_callbacks where gbId=%s and callbackName="gmDeleteItems"' % gbId
    KBEngine.executeRawDatabaseCommand(sql, _onGetRemoved)


def getAccountDid(gbid, callback):
    sql = f'select sm_did from tbl_Account a join tbl_Avatar b on a.sm_avatarGBID=b.sm_gbID where b.sm_gbID={gbid};'
    INFO_MSG(f'getAccountDid, gbid:{gbid}')
    KBEngine.executeRawDatabaseCommand(sql, callback)


def queryForbiddenInfo(gbId, callback):
    selectSql = f'select `sm_forbiddenExpireTime`, `sm_forbiddenCount` from `tbl_Avatar` where `sm_gbID`= {gbId}'
    KBEngine.executeRawDatabaseCommand(selectSql, callback)


def queryAvatarOnline(entityType, dbId, callback):
    _sql = f'select entityID from kbe_entitylog where entityType={entityType} and entityDBID={dbId}'
    KBEngine.executeRawDatabaseCommand(_sql, callback)


def queryFriendsNum(gbId, callback):
    sql = f'select count(*) from game_friends where sGbId={gbId} union all select count(*) from game_friends where bGbId={gbId}'
    KBEngine.executeRawDatabaseCommand(sql, callback)


def queryTwoFriendsNum(gbId1, gbId2, callback):
    sql = f"""
SELECT COUNT(*) FROM game_friends WHERE sGbId={gbId1}
UNION ALL
SELECT COUNT(*) FROM game_friends WHERE bGbId={gbId1}
UNION ALL
SELECT COUNT(*) FROM game_friends WHERE sGbId={gbId2}
UNION ALL
SELECT COUNT(*) FROM game_friends WHERE bGbId={gbId2}
    """
    KBEngine.executeRawDatabaseCommand(sql, callback)


def loadFriends(gbId, callback):
    sql = f'''
select bGbId from game_friends where sGbId={gbId}
union all
select sGbId from game_friends where bGbId={gbId}'''
    KBEngine.executeRawDatabaseCommand(sql, callback)

def removeAllFriends(gbId, callback):
    sql = f'delete from game_friends where sGbId={gbId} or bGbId={gbId}'
    KBEngine.executeRawDatabaseCommand(sql, callback)


def _onRecordAccountOfflineCallback(ret, num, insertId, err, accountName, callbackName, args):
    if err:
        ERROR_MSG('_onRecordAccountOfflineCallback error:', err, accountName, callbackName, args)
        return


def recordAccountOfflineCallback(accountName, callbackName, args):
    """
    记录账号离线回调
    """
    data = cPickle.dumps(args)
    if len(data) > 1024 * 60:
        ERROR_MSG('offline callback data overflow:', accountName, callbackName, data.hex())
        return

    sql = 'INSERT INTO game_account_offline_callbacks (accountName, callbackName, args) VALUES (%s, %s, 0x%s)' % (
        utils.escape_string(accountName), utils.escape_string(callbackName), data.hex())
    KBEngine.executeRawDatabaseCommand(
        sql,
        lambda ret, num, insertId, err: _onRecordAccountOfflineCallback(
            ret, num, insertId, err,
            accountName, callbackName,
            args))


def loadAccountOfflineCallbacks(accountName, callback):
    """
    加载账号离线回调
    """
    sql = 'SELECT `id`, `callbackName`, hex(`args`) FROM `game_account_offline_callbacks` where accountName=%s order by id limit 2000' % utils.escape_string(accountName)
    KBEngine.executeRawDatabaseCommand(sql, callback)


def makeFriends(gbId1, gbId2, callback):
    if gbId1 < gbId2:
        sGbId = gbId1
        bGbId = gbId2
    else:
        sGbId = gbId2
        bGbId = gbId1

    sql = f'insert into game_friends (sGbId, bGbId) values ({sGbId}, {bGbId})'
    KBEngine.executeRawDatabaseCommand(sql, callback)

def removeFriends(gbId1, gbId2, callback):
    if gbId1 < gbId2:
        sGbId = gbId1
        bGbId = gbId2
    else:
        sGbId = gbId2
        bGbId = gbId1

    sql = f'delete from game_friends where sGbId={sGbId} and bGbId={bGbId}'
    KBEngine.executeRawDatabaseCommand(sql, callback)


def searchFriendTemp(callback):
    sql = 'select sm_gbID from tbl_Avatar limit 100'
    KBEngine.executeRawDatabaseCommand(sql, callback)


def getLevelData(tableName, callback):
    sql = f'show tables like "{tableName}%"'
    KBEngine.executeRawDatabaseCommand(sql, callback)


def loadColumns(tableName, callback):
    sql = f'show columns from {tableName}'
    KBEngine.executeRawDatabaseCommand(sql, callback)


def loadTableData(columnsStr, tblName, condition, callback):
    # _sql = f'SELECT {columnsStr} FROM {tblName} WHERE {idName} IN ({ids})'
    _sql = f'SELECT {columnsStr} FROM {tblName} WHERE {condition}'
    KBEngine.executeRawDatabaseCommand(_sql, callback)


def saveTableData(tblName, columns, values, callback):
    _sql = f'INSERT INTO {tblName} ({columns}) VALUES {values}'
    DEBUG_MSG('saveTableData', _sql)
    KBEngine.executeRawDatabaseCommand(_sql, callback)


def getAvatarGbIdByDbId(dbId, callback):
    sql = f'select sm_gbID from tbl_Avatar where id={dbId}'
    KBEngine.executeRawDatabaseCommand(sql, callback)


def addSwitchServerRecord(accountName, newDbId, callback):
    sql = f'insert into game_switch_server (account, dbid) values ("{accountName}", {newDbId})'
    KBEngine.executeRawDatabaseCommand(sql, callback)


def loadSwitchServerRecord(accountName, callback):
    sql = f'select dbid from game_switch_server where account="{accountName}"'
    KBEngine.executeRawDatabaseCommand(sql, callback)


def clearSwitchServerRecord(accountName, callback):
    sql = f'delete from game_switch_server where account="{accountName}"'
    KBEngine.executeRawDatabaseCommand(sql, callback)


def loadSwitchServerAvatarInfo(dbIds, callback):
    dbIdStr = ','.join(str(dbId) for dbId in dbIds)
    sql = f'SELECT id, sm_gbID, sm_school, sm_sex, sm_name, sm_level, sm_birthInDB FROM tbl_Avatar WHERE id in ({dbIdStr})'
    KBEngine.executeRawDatabaseCommand(sql, callback)


def afterSwitchServerModifyGbId(oldGbId, newGbId, callback):
    sql = f'update tbl_Avatar set sm_gbID={newGbId} where sm_gbID={oldGbId}'
    KBEngine.executeRawDatabaseCommand(sql, callback)


def addGuildAvatar(guildUUID, gbId, callback):
    sql = f'insert into game_guild_avatar (guildUUID, gbId) values ("{guildUUID}", {gbId})'
    KBEngine.executeRawDatabaseCommand(sql, callback)


def delGuildAvatar(guildUUID, gbId, callback):
    sql = f'delete from game_guild_avatar where guildUUID={guildUUID} and gbId={gbId}'
    KBEngine.executeRawDatabaseCommand(sql, callback)


def loadAvatarGuildInfo(gbId, callback):
    sql = f'select guildUUID from game_guild_avatar where gbId={gbId}'
    KBEngine.executeRawDatabaseCommand(sql, callback)


def loadAllGuildEntityInfo(callback):
    _sql = f'SELECT id, sm_guildUUID, sm_guildName, sm_desc from tbl_Guild'
    KBEngine.executeRawDatabaseCommand(_sql, callback)


def guildDissolveModifyDB(guildUUID, callback):
    _sql = f'DELETE FROM game_guild_avatar WHERE guildUUID={guildUUID}'
    KBEngine.executeRawDatabaseCommand(_sql, callback)


def loadAvatarFromGuildUUID(guildUUID, callback):
    _sql = f'SELECT gbId FROM game_guild_avatar WHERE guildUUID={guildUUID}'
    KBEngine.executeRawDatabaseCommand(_sql, callback)


def loadLeaderBoardStubInfos(callback):
    _sql = f'SELECT lbType, value FROM game_leader_board_stub_info'
    KBEngine.executeRawDatabaseCommand(_sql, callback)


def recordLeaderBoardStub(lbType, value, callback):
    _sql = f'INSERT INTO game_leader_board_stub_info (lbType, value) VALUES ("{lbType}", {value})'
    KBEngine.executeRawDatabaseCommand(_sql, callback)


def getAvatarTotalScoreAndSpaceNo(gbId, callback):
    _sql = f'SELECT sm_totalScore, sm_spaceNo FROM tbl_Avatar WHERE sm_gbID={gbId}'
    KBEngine.executeRawDatabaseCommand(_sql, callback)

def getAvatarPersonalInfo(gbId, callback):
    _sql = f"""SELECT a.sm_name, a.sm_level, a.sm_school, a.sm_totalScore, eq.sm_gridId, eq.sm_attrJson, a.sm_sex,
		  a.sm_appearance_weapon, a.sm_appearance_breast, a.sm_appearance_outfitData_hairId, a.sm_appearance_outfitData_clothesId,
		  a.sm_appearance_outfitData_picFrameId, a.sm_appearance_outfitData_wingId, a.sm_appearance_outfitData_mountId, a.sm_appearance_faceData_suitId,
		  a.sm_appearance_faceData_hairIdFaceId, a.sm_appearance_faceData_hairColorIdSkinColorId, eq.sm_itemId, eq.sm_createTime, eq.sm_expireTime,
		  eq.sm_uniqueId, eq.sm_bindType, eq.sm_lockStatus
        FROM tbl_Avatar_bodyEquipData_bodyEquipList eq
        RIGHT JOIN (SELECT id, sm_name, sm_level, sm_school, sm_totalScore, sm_sex, sm_appearance_weapon, sm_appearance_breast, sm_appearance_outfitData_hairId,
		  sm_appearance_outfitData_clothesId, sm_appearance_outfitData_picFrameId, sm_appearance_outfitData_wingId, sm_appearance_outfitData_mountId,
		  sm_appearance_faceData_suitId, sm_appearance_faceData_hairIdFaceId, sm_appearance_faceData_hairColorIdSkinColorId
		   FROM tbl_Avatar WHERE sm_gbID={gbId}) a ON a.id = eq.parentID"""
    KBEngine.executeRawDatabaseCommand(_sql, callback)

# --------------------------- auth avatar start --------------------------------

# CREATE TABLE IF NOT EXISTS `game_account_characters`
# (
# 	`id` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT,
# 	`parentID` bigint(20) UNSIGNED NOT NULL,
# 	`gbId` bigint(20) UNSIGNED NOT NULL DEFAULT '0',
# 	`authDbId` bigint(20) UNSIGNED NOT NULL DEFAULT '0',
# 	`dbId` bigint(20) UNSIGNED NOT NULL DEFAULT '0',
# 	`name` varchar(255) NOT NULL DEFAULT '',
# 	`school` smallint(5) UNSIGNED NOT NULL DEFAULT '0',
# 	`sex` tinyint(3) UNSIGNED NOT NULL DEFAULT '0',
# 	`level` int(10) UNSIGNED NOT NULL DEFAULT '0',
# 	`tLastOnline` int(10) UNSIGNED NOT NULL DEFAULT '0',
#   `authExpire` int(10) UNSIGNED NOT NULL DEFAULT '0',
# 	PRIMARY KEY (`id`),
# 	KEY `idx_parentID` (`parentID`),
# 	KEY `idx_gbId` (`gbId`)
# );

SELECT_PARAMS = 'authDbId, dbId, name, school, sex, level, tLastOnline, authExpire'

def loadCharacterFromDB(parentID, callback):
    sql = f'SELECT id, gbId, {SELECT_PARAMS} FROM game_account_characters WHERE parentID={parentID}'
    KBEngine.executeRawDatabaseCommand(sql, callback)


def loadBorrowedCharacterFromDB(authDbId, callback):
    sql = f'SELECT id, parentID, gbId, {SELECT_PARAMS} FROM game_account_characters WHERE authDbId={authDbId}'
    KBEngine.executeRawDatabaseCommand(sql, callback)


def removeCharaterFromDB(dbid, callback):
    sql = f'DELETE FROM game_account_characters WHERE id={dbid}'
    KBEngine.executeRawDatabaseCommand(sql, callback)


def lendAvatar(gbId, otherDbId, authExpire, callback):
    _sql = f'UPDATE game_account_characters SET authDbId={otherDbId}, authExpire={authExpire} WHERE gbId={gbId} and authDbId=0'
    KBEngine.executeRawDatabaseCommand(_sql, callback)


def stopLendAvatar(gbId, callback):
    _sql = f'UPDATE game_account_characters SET authDbId=0, authExpire=0 WHERE gbId={gbId} and authDbId>0'
    KBEngine.executeRawDatabaseCommand(_sql, callback)


def modifyAuthExpire(gbId, authExpire, callback):
    _sql = f'UPDATE game_account_characters SET authExpire={authExpire} WHERE gbId={gbId} and authDbId>0'
    KBEngine.executeRawDatabaseCommand(_sql, callback)

def getAuthExpire(gbId, callback):
    _sql = f'SELECT authExpire, authDbId, gbId FROM game_account_characters WHERE gbId={gbId}'
    KBEngine.executeRawDatabaseCommand(_sql, callback)


def getAvatarMoralValue(gbId, callback):
    _sql = f'SELECT sm_moralValue FROM tbl_Avatar WHERE sm_gbID={gbId}'
    KBEngine.executeRawDatabaseCommand(_sql, callback)
# --------------------------- auth avatar end --------------------------------
