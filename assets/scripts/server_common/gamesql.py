# -*- coding: utf-8 -*-
import functools
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
    # _sql = "CALL gamesp_createindex('tbl_Avatar_inv_item','invItemIdIndex', 'sm_id', 0)"
    #
    # KBEngine.executeRawDatabaseCommand(_sql)
    pass


def onSqlCallback(ret, num, insertId, err, msg):
    if err:
        LOG_ERR('onSqlCallback error:', err, msg)


def getCustomConfig(callback=None):
    _sql = "SELECT name, value from game_config"
    KBEngine.executeRawDatabaseCommand(_sql, lambda result, rows, iid, err: _onGetCustomConfig(result, rows, iid, err,
                                                                                              callback))


def _onGetCustomConfig(result, rows, insertid, error, callback):
    LOG_DBG('_onGetCustomConfig', error)
    if error:
        if KBEngine.component != 'interfaces':
            LOG_ERR('_onGetCustomConfig error:', error)
        return
    gameconfig.loadCustomConfig(result)

    if callback:
        callback()


def checkAdminCmdSerial(cmdSerial, callback):
    _sql = 'SELECT `tWhen`, `result`,`retErrMsg`, `retStr` FROM `game_admin_cmds` WHERE cmdSerial="%s" limit 1' % (
        cmdSerial,)
    KBEngine.executeRawDatabaseCommand(_sql, callback)


def recordAdminCmdSucc(cmdSerial, result, retErrMsg, resultBytes):
    def _onRecordAdminCmd(ret, num, insertId, err):
        if err:
            LOG_ERR("recordAdminCmdSucc error", ret, num, insertId, err)

    resutlStr = resultBytes.decode('utf-8')
    _sql = 'INSERT INTO `game_admin_cmds` (`cmdSerial`, `tWhen`, `result`, `retErrMsg`, `retStr`) VALUES ("%s", %s, %s, %s, %s)' % (
        cmdSerial,
        utils.curTS(), result, utils.escape_string(retErrMsg), utils.escape_string(resutlStr))
    LOG_DBG("recordAdminCmdSucc", _sql)
    KBEngine.executeRawDatabaseCommand(_sql, _onRecordAdminCmd)


def deleteExpiredAdminCmdSerial():
    _sql = 'DELETE FROM `game_admin_cmds` WHERE `tWhen`<%s' % (utils.curTS() - gameconst.ONE_WEEK_COST_SECONDS,)
    KBEngine.executeRawDatabaseCommand(_sql)


def recordEntityDBID(entityType, dbid):
    if gameglobal.entityTypeToDBIDDic and entityType in gameglobal.entityTypeToDBIDDic:
        if dbid != gameglobal.entityTypeToDBIDDic[entityType]:
            raise Exception('error while recording entity dbid: %s %s' % (entityType, dbid))
        return
    _sql = 'INSERT INTO `game_entity_dbid` (entityType, entityDBID) VALUES ("%s", %s) ON DUPLICATE KEY UPDATE entityDBID=VALUES(entityDBID)' % (
        entityType, dbid)
    KBEngine.executeRawDatabaseCommand(
        _sql, functools.partial(_onRecordEntityDBID, entityType, dbid))


def deleteEntityDBID(entityType):
    _sql = 'DELETE FROM `game_entity_dbid` WHERE entityType="%s"' % (entityType,)
    KBEngine.executeRawDatabaseCommand(_sql)


def _onRecordEntityDBID(entityType, dbid, ret, num, insertId, err):
    if type(err) is str and err:
        raise Exception('_onRecordEntityDBID error: %s %s %s' % (err, dbid, entityType))


def getAvatarBasicInfoByPlayerNameOrGBIDOrObID(playerNameOrGBIDOrObID, callback):
    if utils.isGbId(playerNameOrGBIDOrObID):
        _sql = """SELECT sm_gbID, sm_name, sm_accountName, id FROM tbl_Avatar WHERE sm_gbID = %s""" % playerNameOrGBIDOrObID
    elif utils.checkRoleName(playerNameOrGBIDOrObID):
        _sql = """SELECT sm_gbID, sm_name, sm_accountName, id FROM tbl_Avatar WHERE sm_name = BINARY %s""" % utils.escape_string(
            playerNameOrGBIDOrObID)
    else:
        LOG_ERR('in getAvatarBasicInfoByPlayerNameOrGBID, playerNameOrGBID error:', playerNameOrGBIDOrObID)
        return
    KBEngine.executeRawDatabaseCommand(_sql, callback)

def getAvatarBasicInfoByPlayerNameList(playerNameList, callback):
    nameListStr = ','.join(utils.escape_string(name) for name in playerNameList)
    _sql = """SELECT sm_gbID, sm_name, sm_accountName, sm_school, id FROM tbl_Avatar WHERE BINARY sm_name in (%s)""" % nameListStr
    KBEngine.executeRawDatabaseCommand(_sql, callback)

def loadLastGlobalMailInfo(playerGbId, callback):
    _sql = '''CALL gamesp_load_last_global_mail_info(%s,%s)'''%(playerGbId, 0)
    KBEngine.executeRawDatabaseCommand(_sql, callback)

def updateLastGlobaMailInfo(playerGBID, lastGlobalMailTime, callback):
    _sql = """UPDATE game_last_global_mail_info SET lastGlobalMailTime=%s where gbId=%s and lastGlobalMailTime<%s"""%(
        lastGlobalMailTime, playerGBID, lastGlobalMailTime)
    KBEngine.executeRawDatabaseCommand(_sql, callback)

def sendMailByGBID(toGBID, mailId, mailGBID, globalMailGBID, readStat, dueTime,\
                   createTime, expiredTime, fromGBID, attach,\
                   attachStat, despArgs, title, cont, opUUID,\
                   srcType, srcSubType, desc, idipSource, callback):
    # 按照类型走序列化
    datas = attach.toMailWealthDict()
    attach = utils.bytesToHex(cPickle.dumps(datas))
    despArgs = utils.bytesToHex(cPickle.dumps(despArgs))
    _sql = '''CALL gamesp_send_mail(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,'%s','%s',%s,%s,%s,'%s',%s)'''%\
          (toGBID, mailId, mailGBID, globalMailGBID, readStat, dueTime, createTime, expiredTime, fromGBID, attach,
                attachStat, despArgs, title, cont, opUUID, srcType, srcSubType, desc, idipSource)
    LOG_DBG('gamesql::sendMailByGBID:', _sql)
    KBEngine.executeRawDatabaseCommand(_sql, callback)

def loadMailsFromDB(gbId, fromTime, isGlobal, excludeMailList, callback):
    maxMailNum = MACF.datas['mailNumMax']['value'] + MACF.datas['mailNumMax2']['value']
    fields = '''toGBID,mailId,mailGBID,globalMailGBID,readStat,dueTime,createTime,expiredTime,fromGBID,attach,attachStat,despArgs,title,cont, opUUID,srcType,srcSubType,desp,idipSource'''
    if excludeMailList:
        mailGBIDStr = ','.join([str(mailGBID) for mailGBID in excludeMailList])
        if isGlobal:
            _sql = """SELECT %s FROM %s WHERE toGBID=%s and globalMailGBID>0 and createTime>=%s and mailGBID not in (%s) ORDER BY createTime DESC limit %s""" % (
                fields, gameconst.TABLE_NAME_GAME_MAIL, gbId, fromTime, mailGBIDStr, maxMailNum * 2)
        else:
            _sql = """SELECT %s FROM %s WHERE toGBID=%s and globalMailGBID=0 and createTime>=%s and mailGBID not in (%s) ORDER BY createTime DESC limit %s""" % (
                fields, gameconst.TABLE_NAME_GAME_MAIL, gbId, fromTime, mailGBIDStr, maxMailNum * 2)
    else:
        if isGlobal:
            _sql = """SELECT %s FROM %s WHERE toGBID=%s and globalMailGBID>0 and createTime>=%s ORDER BY createTime DESC limit %s""" % (
                fields, gameconst.TABLE_NAME_GAME_MAIL, gbId, fromTime, maxMailNum * 2)
        else:
            _sql = """SELECT %s FROM %s WHERE toGBID=%s and globalMailGBID=0 and createTime>=%s ORDER BY createTime DESC limit %s""" % (
                fields, gameconst.TABLE_NAME_GAME_MAIL, gbId, fromTime, maxMailNum * 2)
    LOG_DBG('in loadMailsFromDB, _sql:', isGlobal, _sql)
    KBEngine.executeRawDatabaseCommand(_sql, callback)

def loadMailByMailGBID(gbId, mailGBID, callback):
    _fields = '''toGBID,mailId,mailGBID,globalMailGBID,readStat,createTime,expiredTime,fromGBID,attach,attachStat,despArgs,title,cont, opUUID,srcType,srcSubType,desp,idipSource'''
    _sql = """SELECT %s FROM %s WHERE toGBID=%s and mailGBID=%s""" % (
        _fields, gameconst.TABLE_NAME_GAME_MAIL, gbId, mailGBID)
    KBEngine.executeRawDatabaseCommand(_sql, callback)

def setMailHasRead(toGBID, mailGBID, callback):
    _sql = """UPDATE %s SET readStat=%s where toGBID=%s and mailGBID=%s""" % (gameconst.TABLE_NAME_GAME_MAIL,
                                                                             gameconst.MailReadState.HasRead, toGBID,
                                                                             mailGBID)
    # LOG_DBG('in setMultiMailsHasRead, _sql:', _sql)
    KBEngine.executeRawDatabaseCommand(_sql, callback)


def setMultiMailsHasRead(toGBID, mailGBIDList, callback):
    mailGBIDStr = ','.join([str(mailGBID) for mailGBID in mailGBIDList])
    _sql = """UPDATE %s SET readStat=%s where toGBID=%s and mailGBID in (%s)""" % (gameconst.TABLE_NAME_GAME_MAIL,
                                                                                  gameconst.MailReadState.HasRead,
                                                                                  toGBID, mailGBIDStr)
    KBEngine.executeRawDatabaseCommand(_sql, callback)


def setMailHasGetAttach(toGBID, mailGBIDList, callback):
    # 设置附件已领取及邮件已读
    mailGBIDStr = ','.join([str(mailGBID) for mailGBID in mailGBIDList])
    _sql = """UPDATE %s SET attachStat=%s, readStat=%s where toGBID=%s and mailGBID in (%s)""" % (
        gameconst.TABLE_NAME_GAME_MAIL,
        gameconst.MailAttachState.HasGET, gameconst.MailReadState.HasRead, toGBID, mailGBIDStr)
    # LOG_DBG('in setMailHasGetAttach, _sql:', _sql)
    KBEngine.executeRawDatabaseCommand(_sql, callback)


def resetMailAttachNotState(toGBID, mailGBID, readState, callback):
    _sql = """UPDATE %s SET attachStat=%s, readStat=%s where toGBID=%s and mailGBID=%s""" % (
        gameconst.TABLE_NAME_GAME_MAIL,
        gameconst.MailAttachState.NotGet, readState, toGBID, mailGBID)
    # LOG_DBG('in setMailHasGetAttach, _sql:', _sql)
    KBEngine.executeRawDatabaseCommand(_sql, callback)


def deleteMailByMailGBID(toGBID, mailGBID, callback):
    _sql = """DELETE FROM %s WHERE toGBID=%s AND mailGBID=%s""" % (gameconst.TABLE_NAME_GAME_MAIL, toGBID, mailGBID)
    LOG_DBG('in deleteMailByMailGBID, _sql:', _sql)
    KBEngine.executeRawDatabaseCommand(_sql, callback)


def deleteOldMails(toGBID, minMailTime, minMailTiemMailList, isGlobal, callback):
    if minMailTiemMailList:
        mailGBIDStr = ','.join([str(mailGBID) for mailGBID in minMailTiemMailList])
        if isGlobal:
            _sql = """DELETE FROM %s WHERE toGBID=%s and globalMailGBID>0 AND createTime <= %s and mailGBID not in (%s)""" % (
                gameconst.TABLE_NAME_GAME_MAIL, toGBID, minMailTime, mailGBIDStr)
        else:
            _sql = """DELETE FROM %s WHERE toGBID=%s and globalMailGBID=0 AND createTime <= %s and mailGBID not in (%s)""" % (
                gameconst.TABLE_NAME_GAME_MAIL, toGBID, minMailTime, mailGBIDStr)
    else:
        if isGlobal:
            _sql = """DELETE FROM %s WHERE toGBID=%s and globalMailGBID>0 AND createTime<%s""" % (
                gameconst.TABLE_NAME_GAME_MAIL, toGBID, minMailTime)
        else:
            _sql = """DELETE FROM %s WHERE toGBID=%s and globalMailGBID=0 AND createTime<%s""" % (
                gameconst.TABLE_NAME_GAME_MAIL, toGBID, minMailTime)
    LOG_DBG('in deleteOldMails, _sql:', _sql)
    KBEngine.executeRawDatabaseCommand(_sql, callback)


def deleteMultiMails(toGBID, mailGBIDList, callback):
    mailGBIDStr = ','.join([str(mailGBID) for mailGBID in mailGBIDList])
    _sql = """DELETE FROM %s WHERE toGBID=%s AND mailGBID in (%s)""" % (
        gameconst.TABLE_NAME_GAME_MAIL, toGBID, mailGBIDStr)
    LOG_DBG('in deleteMultiMails, _sql:', _sql)
    KBEngine.executeRawDatabaseCommand(_sql, callback)

def updateMultiMails(toGBID, mailGBIDList, callback):
    mailGBIDStr = ','.join([str(mailGBID) for mailGBID in mailGBIDList])
    _sql = """UPDATE %s set dueTime=0 WHERE toGBID=%s AND mailGBID in (%s)""" % (
        gameconst.TABLE_NAME_GAME_MAIL, toGBID, mailGBIDStr)
    LOG_DBG('in updateMultiMails, _sql:', _sql)
    KBEngine.executeRawDatabaseCommand(_sql, callback)

def sendMailToAccount(accountName, accountType, mailId, attachStr,\
                      despArgsStr, title, cont, opUUID, srcType,\
                      srcSubType, desc, idipSource, callback):
    _sql = """INSERT INTO game_account_mails (accountName,accountType,mailId,sendTime,attachStr,despStr,title,cont,opUUID,srcType,srcSubType,desp,idipSource) VALUES('%s',%s,%s,%s,'%s','%s','%s','%s',%s,%s,%s,'%s',%s)""" % \
          (accountName, accountType, mailId, utils.curTS(), attachStr, despArgsStr, title, cont, opUUID, srcType,
           srcSubType, desc, idipSource)
    LOG_DBG('in sendMailToAccount, _sql:', _sql)
    KBEngine.executeRawDatabaseCommand(_sql, callback)


def loadMailByAccountInfo(accountName, accountType, playerGBID, callback):
    _sql = """CALL gamesp_load_account_mails('%s',%s,%s)""" % (accountName, accountType, playerGBID)
    # LOG_DBG('in loadMailByAccountInfo, _sql:', _sql)
    KBEngine.executeRawDatabaseCommand(_sql, callback)


def getAvatarInfoFromDB(gbIds, callback):
    if len(gbIds) == 1:
        _str = '= {}'.format(gbIds[0])
    else:
        _str = 'in ({})'.format(','.join((str(gbId) for gbId in gbIds)))

    _sql = """SELECT a.sm_gbID, a.sm_name, a.sm_school, a.sm_sex, a.sm_level, a.sm_accountName, a.sm_totalScore, a.id, \
        a.sm_tsLastOfflineBase, a.sm_avatarFlag, a.sm_appearance_outfitData_picFrameId, a.sm_accountType, a.sm_obId, c.sm_channelId\
        FROM tbl_Avatar a left join tbl_Account c on a.sm_accountDBID = c.id WHERE a.sm_gbID %s""" % _str
    KBEngine.executeRawDatabaseCommand(_sql, callback)

def setServerStateInfo(name, value, callback):
    _sql = """REPLACE INTO game_state_info (name, value) VALUES ('%s', %d)""" % (name, value)
    KBEngine.executeRawDatabaseCommand(_sql, callback)


def checkAccountWhiteList(accountName, callback):
    _sql = "select id from game_login_white_list where accountName=%s" % utils.escape_string(accountName)
    KBEngine.executeRawDatabaseCommand(_sql, callback)


def addAccountWhiteList(accountNameList):
    valueList = [f"({utils.escape_string(accountName)}, 0)" for accountName in accountNameList]
    valueStr = ",".join(valueList)
    addMultAccountWhiteList(valueStr)

def addMultAccountWhiteList(valueStr):
    _sql = "insert ignore into game_login_white_list (accountName, accountGmMode) values %s;" % (valueStr)
    LOG_DBG('addMultAccountWhiteList', _sql)
    KBEngine.executeRawDatabaseCommand(_sql)


def deleteAccountWhiteList(accountNameList):
    valueList = [f"{utils.escape_string(accountName)}" for accountName in accountNameList]
    valueStr = ",".join(valueList)
    deleteMultAccountWhiteList(valueStr)

def deleteMultAccountWhiteList(valueStr):
    _sql = "DELETE FROM game_login_white_list where accountName in (%s);" % (valueStr)
    LOG_DBG('deleteMultAccountWhiteList', _sql)
    KBEngine.executeRawDatabaseCommand(_sql)

def loadAvatarAppearanceDataFromDB(gbIdList, callback):
    gbIdStr = ','.join([str(gbId) for gbId in gbIdList])
    _sql = 'select id, sm_gbID, sm_birthInDB, sm_school, sm_sex, sm_level, sm_appearance_weapon, ' \
          'sm_appearance_breast, sm_appearance_faceData_suitId,' \
          'sm_appearance_faceData_hairIdFaceId, sm_appearance_faceData_hairColorIdSkinColorId, ' \
          'sm_appearance_outfitData_hairId, sm_appearance_outfitData_clothesId, ' \
          'sm_appearance_outfitData_picFrameId, sm_appearance_outfitData_wingId, ' \
          'sm_appearance_outfitData_mountId from tbl_Avatar where sm_gbID in (%s)' % (gbIdStr,)
    KBEngine.executeRawDatabaseCommand(_sql, callback)
    return

def loadAvatarOutfitDataFromDB(parentIDList, callback):
    parentIDStr = ','.join([str(parentID) for parentID in parentIDList])
    _sql = 'select parentID, sm_outfitType, sm_outfitId, sm_expireTime from tbl_Avatar_outfitInfo_outfitList where parentID in (%s)' % (
        parentIDStr,)
    KBEngine.executeRawDatabaseCommand(_sql, callback)
    return


def updateCharacterParentID(accountName, targetAvatarGbId):
    _sql = "update tbl_Account_characters_characters set parentID = (select entityDBID from kbe_accountinfos where accountName = '%s') WHERE sm_gbId = %s" % (
        accountName, targetAvatarGbId)
    KBEngine.executeRawDatabaseCommand(_sql)


def countCharacterNum(accountName, callback):
    _sql = "select b.accountName,a.sm_name from tbl_Account_characters_characters a right join kbe_accountinfos b on a.parentID = b.entityDBID where b.accountName = {} ".format(
        utils.escape_string(accountName))
    KBEngine.executeRawDatabaseCommand(_sql, callback)


# def forbidLogin(accountName, forbidType, forbidTime, forbidReason):
#     _sql = "update tbl_Account set sm_forbidLoginFlag = {},sm_forbidLoginType = {},sm_forbidLoginTime = {},sm_forbidLoginReason = {} WHERE id = (select entityDBID from kbe_accountinfos where accountName = {})".format(
#         1, forbidType, forbidTime, utils.escape_string(forbidReason), utils.escape_string(accountName))
#     KBEngine.executeRawDatabaseCommand(_sql)


def getForbidLoginProp(accountName, callback):
    _sql = "select sm_isDelete from tbl_Account WHERE id = (select entityDBID from kbe_accountinfos where accountName = {})".format(
        utils.escape_string(accountName))
    KBEngine.executeRawDatabaseCommand(_sql, callback)


# def unforbidLogin(accountName):
#     _sql = "update tbl_Account set sm_forbidLoginFlag = 0 WHERE id = (select entityDBID from kbe_accountinfos where accountName = {})".format(
#         utils.escape_string(accountName))
#     KBEngine.executeRawDatabaseCommand(_sql)


def forbidVoiceChat(accountName, forbidType, forbidTime, forbidReason):
    _sql = "update tbl_Account set sm_forbidVoiceChatFlag = 1,sm_forbidVoiceChatType = {},sm_forbidVoiceChatTime = {},sm_forbidVoiceChatReason = {} WHERE id = (select entityDBID from kbe_accountinfos where accountName = {}) ".format(
        forbidType, forbidTime, utils.escape_string(forbidReason), utils.escape_string(accountName))
    KBEngine.executeRawDatabaseCommand(_sql)


def unforbidVoiceChat(accountName):
    _sql = "update tbl_Account set sm_forbidVoiceChatFlag = 0 WHERE id = (select entityDBID from kbe_accountinfos where accountName = {}) ".format(
        utils.escape_string(accountName))
    KBEngine.executeRawDatabaseCommand(_sql)


def forbidChat(accountName, forbidType, forbidTime, forbidReason):
    _sql = "update tbl_Account set sm_forbidChatFlag = 1,sm_forbidChatType = {},sm_forbidChatTime = {},sm_forbidChatReason = {} WHERE id = (select entityDBID from kbe_accountinfos where accountName = {}) ".format(
        forbidType, forbidTime, utils.escape_string(forbidReason), utils.escape_string(accountName))
    KBEngine.executeRawDatabaseCommand(_sql)


def unforbidChat(accountName):
    _sql = "update tbl_Account set sm_forbidChatFlag = 0 WHERE id = (select entityDBID from kbe_accountinfos where accountName = {}) ".format(
        utils.escape_string(accountName))
    KBEngine.executeRawDatabaseCommand(_sql)


def queryAccountDBID(platId, accountName, callback):
    accountType = utils.fetchAccountTypeByPlatId(platId)
    _sql = f"select entityDBID from kbe_accountinfos where accountName = '{accountType}:{accountName}'"
    KBEngine.executeRawDatabaseCommand(_sql, callback)


def deleteAccountEntity(platId, accountName, callback):
    accountType = utils.fetchAccountTypeByPlatId(platId)
    _sql = f"delete from kbe_accountinfos where accountName = '{accountType}:{accountName}'"
    KBEngine.executeRawDatabaseCommand(_sql, callback)


# region coinAuction.auction


def queryAvatarLoginTimeByAccountName(accountName, callback):
    _sql = f"select sm_tLoginBase from tbl_Avatar where sm_accountName = '{accountName}'"
    LOG_INFO(_sql)
    KBEngine.executeRawDatabaseCommand(_sql, callback)


def queryAvatarGBIDByAccountName(accountName, callback):
    _sql = f"select sm_gbId from tbl_Avatar where sm_accountName = '{accountName}'"
    LOG_INFO(_sql)
    KBEngine.executeRawDatabaseCommand(_sql, callback)


def queryCountAccountNum(callback):
    _sql = 'select count(id) from tbl_Account'
    LOG_INFO(_sql)
    KBEngine.executeRawDatabaseCommand(_sql, callback)


def queryAvatarObId(gbId, callback):
    _sql = f'select sm_obId from tbl_Avatar where sm_gbID={gbId}'
    KBEngine.executeRawDatabaseCommand(_sql, callback)


def deleteCrossServerGameAccountInfo(entityDBID):
    _sql = f"DELETE FROM `kbe_accountinfos` WHERE entityDBID={entityDBID}"
    KBEngine.executeRawDatabaseCommand(_sql)


def _onRecordOfflineCallback(ret, num, insertId, err, gbId, callbackName, args):
    if err:
        LOG_ERR('_onRecordOfflineCallback error:', err, gbId, callbackName, args)
        return

    nCallback = int(ret[0][0])
    if nCallback > 1000:
        LOG_ERR('_onRecordOfflineCallback: too many calbacks', nCallback, gbId, callbackName, args)


def recordAvatarOfflineCallback(gbId, callbackName, args):
    data = cPickle.dumps(args)
    if len(data) > 1024 * 60:
        LOG_ERR('offline callback data overflow:', gbId, callbackName, data.hex())
        return
    _sql = 'CALL gamesp_record_avatar_offline_callbacks(%s, %s, 0x%s)' % (
        gbId, utils.escape_string(callbackName), data.hex())
    KBEngine.executeRawDatabaseCommand(_sql,
                                       lambda ret, num, insertId, err: _onRecordOfflineCallback(ret, num, insertId, err,
                                                                                                gbId, callbackName,
                                                                                                args))


def _onLoadOfflineCallback(cbData, num, insertId, err, entId, gbId, finishCallback):
    if err:
        LOG_ERR('_onLoadOfflineCallback err', err, gbId)
        return

    if cbData:
        def _onDeleteCallbacks(err1):
            avatar = KBEngine.entities.get(entId)
            if not avatar or avatar.isDestroyed:
                LOG_WARN('_onLoadOfflineCallback: player is offline. ', entId, gbId, cbData)
                return

            if err1:
                LOG_ERR('_onDeleteCallbacks err', err, gbId)
                return

            for _id, callbackName, argData in cbData:
                try:
                    args = cPickle.loads(bytes.fromhex(argData.decode('ascii')))
                    funcName = callbackName.decode('ascii')
                    func = getattr(avatar, funcName)
                    if not getattr(func, 'offlineCall', False):
                        LOG_ERR('function is not offline callable:', entId, gbId, callbackName, argData)
                        continue
                    func(*args)
                except Exception as e:
                    LOG_ERR('avatar offline callback error:', gbId, callbackName, argData, e)

            finishCallback and finishCallback()

        delIds = []
        for _id, callbackName, argData in cbData:
            delIds.append(_id.decode('ascii'))
        delSql = 'delete from game_avatar_offline_callbacks where id in (%s)' % (','.join(delIds))
        KBEngine.executeRawDatabaseCommand(delSql, lambda ret, num, insertId, err1: _onDeleteCallbacks(err1))
    else:
        finishCallback and finishCallback()


def loadOfflineCallback(avatar, finishCallback):
    _sql = 'SELECT `id`, `callbackName`, hex(`args`) FROM `game_avatar_offline_callbacks` where gbId=%s order by id limit 2000' % avatar.gbID
    KBEngine.executeRawDatabaseCommand(_sql,
                                       lambda ret, num, insertId, err: _onLoadOfflineCallback(ret, num, insertId, err,
                                                                                              avatar.id, avatar.gbID,
                                                                                              finishCallback))


def _sendMailCallback(ret, num, insertId, err, toGBID, mailVal, onSendCallback):
    if err:
        LOG_ERR('_sendMailCallback', err, toGBID, mailVal.mailId, mailVal.mailUUID, mailVal.srcType, mailVal.detail,
                  mailVal.title)
        return

    if onSendCallback:
        onSendCallback(toGBID, mailVal)
    else:
        if toGBID:
            stub = gameengine.getGlobalBase('PlayerStub')

            stub.playerRecvMail(toGBID, mailVal)


def queryAccountDid(gbid, callback):
    _sql = f'select sm_did from tbl_Account a join tbl_Avatar b on a.id=b.sm_accountDBID where b.sm_gbID={gbid};'
    LOG_INFO('_sql')
    KBEngine.executeRawDatabaseCommand(_sql, lambda ret, num, insertId, err: callback(ret, err))


def delAccountClearDB(realAccount, callback):
    accountType, accountName = utils.fetchAccountTypeAndName(realAccount)
    _sql = f'update tbl_Account set sm_userName="", sm_identityCard="", sm_isDelete=1 where sm_accountType={accountType} and \
        sm_accountName="{accountName}")'
    LOG_INFO('delAccountClearDB', _sql)
    KBEngine.executeRawDatabaseCommand(_sql, callback)


def recoverAccountDB(realAccount, callback):
    accountType, accountName = utils.fetchAccountTypeAndName(realAccount)
    _sql = f'update tbl_Account set sm_isDelete=0 where sm_accountType={accountType} and sm_accountName="{accountName}")'
    LOG_INFO('recoverAccountDB', _sql)
    KBEngine.executeRawDatabaseCommand(_sql, callback)


def checkOfflineDeductWealth(gbId, itemId, deductNum, checkCallback):
    def _onGetItemsInfo(ret, num, insertId, err, alreadyRemovedNum, needDeduct):
        if err:
            checkCallback(gameconst.GMCommandErr.GM_RET_DB_OP_ERR, 0, alreadyRemovedNum, needDeduct)
            return

        if not ret:
            checkCallback(gameconst.GMCommandErr.GM_RET_TARGET_NOT_EXISTS, 0, alreadyRemovedNum, needDeduct)
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

            LOG_INFO(f'checkOfflineDeductWealth: {gbId} need remove {needDeductTotal} {coinVal}')

            itemData = dataUtils.getCommItemData(itemId)
            if not itemData:
                checkCallback(gameconst.GMCommandErr.GM_RET_INTERNAL_ERROR, 0, alreadyRemovedNum, needDeduct)
                return
            if itemData['type'] == gameconst.ItemEnum.Normal:
                for itDic in bagItemList:
                    if itDic.get('itemId') == itemId:
                        hasNum += itDic.get('itemNum', 0)

                if hasNum < needDeductTotal:
                    checkCallback(gameconst.GMCommandErr.GM_RET_INSUFFICIENT, hasNum, alreadyRemovedNum, needDeduct)
                    return
            elif itemId == gameconst.ItemIdEnum.COIN:
                hasNum = coinVal
                if wealthVal.coin.data and wealthVal.coin.data > coinVal:
                    checkCallback(gameconst.GMCommandErr.GM_RET_INSUFFICIENT, coinVal, alreadyRemovedNum, needDeduct)
                    return

            checkCallback(0, hasNum, alreadyRemovedNum, needDeduct)

    def _onGetRemoved(ret, num, insertId, err):
        if err:
            checkCallback and checkCallback(gameconst.GMCommandErr.GM_RET_INTERNAL_ERROR, 0, 0, deductNum)
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

        LOG_DBG(f'already del {removedNum}, need del {deductNum}')
        checkLeftSql = 'select sm_coin, sm_coinFraction, sm_auspiciousCoin, sm_auspiciousCoinFraction, hex(sm_bagData_itemsList) from tbl_Avatar where sm_gbID=%s' % gbId
        KBEngine.executeRawDatabaseCommand(checkLeftSql,
                                           lambda _ret, _num, _insertId, _err: _onGetItemsInfo(_ret, _num, _insertId,
                                                                                               _err, removedNum,
                                                                                               deductNum))

    _sql = 'select hex(args) from game_avatar_offline_callbacks where gbId=%s and callbackName="gmDeleteItems"' % gbId
    KBEngine.executeRawDatabaseCommand(_sql, _onGetRemoved)


def getAccountDid(gbid, callback):
    _sql = f'select sm_did from tbl_Account a join tbl_Avatar b on a.sm_avatarGBID=b.sm_gbID where b.sm_gbID={gbid};'
    LOG_INFO(f'getAccountDid, gbid:{gbid}')
    KBEngine.executeRawDatabaseCommand(_sql, callback)


def queryForbiddenInfo(gbId, callback):
    selectSql = f'select `sm_forbiddenExpireTime`, `sm_forbiddenCount` from `tbl_Avatar` where `sm_gbID`= {gbId}'
    KBEngine.executeRawDatabaseCommand(selectSql, callback)


def queryAvatarOnline(entityType, dbId, callback):
    _sql = f'select entityID from kbe_entitylog where entityType={entityType} and entityDBID={dbId}'
    KBEngine.executeRawDatabaseCommand(_sql, callback)


def queryFriendsNum(gbId, callback):
    _sql = f'select count(*) from game_friends where sGbId={gbId} union all select count(*) from game_friends where bGbId={gbId}'
    KBEngine.executeRawDatabaseCommand(_sql, callback)


def queryTwoFriendsNum(gbId1, gbId2, callback):
    _sql = f"""
SELECT COUNT(*) FROM game_friends WHERE sGbId={gbId1}
UNION ALL
SELECT COUNT(*) FROM game_friends WHERE bGbId={gbId1}
UNION ALL
SELECT COUNT(*) FROM game_friends WHERE sGbId={gbId2}
UNION ALL
SELECT COUNT(*) FROM game_friends WHERE bGbId={gbId2}
    """
    KBEngine.executeRawDatabaseCommand(_sql, callback)


def loadFriends(gbId, callback):
    _sql = f'''
select bGbId from game_friends where sGbId={gbId}
union all
select sGbId from game_friends where bGbId={gbId}'''
    KBEngine.executeRawDatabaseCommand(_sql, callback)

def removeAllFriends(gbId, callback):
    _sql = f'delete from game_friends where sGbId={gbId} or bGbId={gbId}'
    KBEngine.executeRawDatabaseCommand(_sql, callback)


def _onRecordAccountOfflineCallback(ret, num, insertId, err, accountName, callbackName, args):
    if err:
        LOG_ERR('_onRecordAccountOfflineCallback error:', err, accountName, callbackName, args)
        return


def recordAccountOfflineCallback(accountName, callbackName, args):
    """
    记录账号离线回调
    """
    data = cPickle.dumps(args)
    if len(data) > 1024 * 60:
        LOG_ERR('offline callback data overflow:', accountName, callbackName, data.hex())
        return

    _sql = 'INSERT INTO game_account_offline_callbacks (accountName, callbackName, args) VALUES (%s, %s, 0x%s)' % (
        utils.escape_string(accountName), utils.escape_string(callbackName), data.hex())
    KBEngine.executeRawDatabaseCommand(
        _sql,
        lambda ret, num, insertId, err: _onRecordAccountOfflineCallback(
            ret, num, insertId, err,
            accountName, callbackName,
            args))


def loadAccountOfflineCallbacks(accountName, callback):
    """
    加载账号离线回调
    """
    _sql = 'SELECT `id`, `callbackName`, hex(`args`) FROM `game_account_offline_callbacks` where accountName=%s order by id limit 2000' % utils.escape_string(accountName)
    KBEngine.executeRawDatabaseCommand(_sql, callback)


def makeFriends(gbId1, gbId2, callback):
    if gbId1 < gbId2:
        sGbId = gbId1
        bGbId = gbId2
    else:
        sGbId = gbId2
        bGbId = gbId1

    _sql = f'insert into game_friends (sGbId, bGbId) values ({sGbId}, {bGbId})'
    KBEngine.executeRawDatabaseCommand(_sql, callback)

def removeFriends(gbId1, gbId2, callback):
    if gbId1 < gbId2:
        sGbId = gbId1
        bGbId = gbId2
    else:
        sGbId = gbId2
        bGbId = gbId1

    _sql = f'delete from game_friends where sGbId={sGbId} and bGbId={bGbId}'
    KBEngine.executeRawDatabaseCommand(_sql, callback)


def searchFriendTemp(callback):
    _sql = 'select sm_gbID from tbl_Avatar limit 100'
    KBEngine.executeRawDatabaseCommand(_sql, callback)


def getLevelData(tableName, callback):
    _sql = f'show tables like "{tableName}%"'
    KBEngine.executeRawDatabaseCommand(_sql, callback)


def loadColumns(tableName, callback):
    _sql = f'show columns from {tableName}'
    KBEngine.executeRawDatabaseCommand(_sql, callback)


def loadTableData(columnsStr, tblName, condition, callback):
    # _sql = f'SELECT {columnsStr} FROM {tblName} WHERE {idName} IN ({ids})'
    _sql = f'SELECT {columnsStr} FROM {tblName} WHERE {condition}'
    KBEngine.executeRawDatabaseCommand(_sql, callback)


def saveTableData(tblName, columns, values, callback):
    _sql = f'INSERT INTO {tblName} ({columns}) VALUES {values}'
    LOG_DBG('saveTableData', _sql)
    KBEngine.executeRawDatabaseCommand(_sql, callback)


def getAvatarGbIdByDbId(dbId, callback):
    _sql = f'select sm_gbID from tbl_Avatar where id={dbId}'
    KBEngine.executeRawDatabaseCommand(_sql, callback)


def addSwitchServerRecord(accountName, newDbId, callback):
    _sql = f'insert into game_switch_server (account, dbid) values ("{accountName}", {newDbId})'
    KBEngine.executeRawDatabaseCommand(_sql, callback)


def loadSwitchServerRecord(accountName, callback):
    _sql = f'select dbid from game_switch_server where account="{accountName}"'
    KBEngine.executeRawDatabaseCommand(_sql, callback)


def clearSwitchServerRecord(accountName, callback):
    _sql = f'delete from game_switch_server where account="{accountName}"'
    KBEngine.executeRawDatabaseCommand(_sql, callback)


def loadSwitchServerAvatarInfo(dbIds, callback):
    dbIdStr = ','.join(str(dbId) for dbId in dbIds)
    _sql = f'SELECT id, sm_gbID, sm_school, sm_sex, sm_name, sm_level, sm_birthInDB FROM tbl_Avatar WHERE id in ({dbIdStr})'
    KBEngine.executeRawDatabaseCommand(_sql, callback)


def afterSwitchServerModifyGbId(oldGbId, newGbId, callback):
    _sql = f'update tbl_Avatar set sm_gbID={newGbId} where sm_gbID={oldGbId}'
    KBEngine.executeRawDatabaseCommand(_sql, callback)


def addGuildAvatar(guildUUID, gbId, callback):
    _sql = f'insert into game_guild_avatar (guildUUID, gbId) values ("{guildUUID}", {gbId})'
    KBEngine.executeRawDatabaseCommand(_sql, callback)


def delGuildAvatar(guildUUID, gbId, callback):
    _sql = f'delete from game_guild_avatar where guildUUID={guildUUID} and gbId={gbId}'
    KBEngine.executeRawDatabaseCommand(_sql, callback)


def loadAvatarGuildInfo(gbId, callback):
    _sql = f'select guildUUID from game_guild_avatar where gbId={gbId}'
    KBEngine.executeRawDatabaseCommand(_sql, callback)


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
    _a1, _a2 = utils.getAvatarFieldsDOTStr()
    _eq = utils.getEquipSQLStr()

    _sql = f"""SELECT {_a1},{_eq}
        FROM tbl_Avatar_bodyEquipData_bodyEquipList eq
        RIGHT JOIN (SELECT id, {_a2}
		FROM tbl_Avatar WHERE sm_gbID={gbId}) a ON a.id = eq.parentID"""

    LOG_DBG('getAvatarPersonalInfo', _sql)
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
    _sql = f'SELECT id, gbId, {SELECT_PARAMS} FROM game_account_characters WHERE parentID={parentID}'
    KBEngine.executeRawDatabaseCommand(_sql, callback)


def loadBorrowedCharacterFromDB(authDbId, callback):
    _sql = f'SELECT id, parentID, gbId, {SELECT_PARAMS} FROM game_account_characters WHERE authDbId={authDbId}'
    KBEngine.executeRawDatabaseCommand(_sql, callback)


def removeCharaterFromDB(dbid, callback):
    _sql = f'DELETE FROM game_account_characters WHERE id={dbid}'
    KBEngine.executeRawDatabaseCommand(_sql, callback)


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


def resetExpireAuth(dbid, now, callback):
    _sql = f'UPDATE game_account_characters SET authDbId=0, authExpire=0 WHERE parentID={dbid} and authDbId>0 and authExpire<={now}'
    KBEngine.executeRawDatabaseCommand(_sql, callback)


def getAvatarMoraAndBanLoginlValue(gbId, callback):
    _sql = f'SELECT sm_moralValue, sm_banLogin FROM tbl_Avatar WHERE sm_gbID={gbId}'
    KBEngine.executeRawDatabaseCommand(_sql, callback)

def getBanLogin(gbId, callback):
    _sql = f'SELECT sm_banLogin FROM tbl_Avatar WHERE sm_gbID={gbId}'
    KBEngine.executeRawDatabaseCommand(_sql, callback)

def beginBanLogin(gbId, callback):
    _sql = f'SELECT sm_autoBanLoginFlag, sm_banLogin FROM tbl_Avatar WHERE sm_gbID={gbId}'
    KBEngine.executeRawDatabaseCommand(_sql, callback)

def banLogin(gbId, autoFlag, endTime, callback):
    _sql = f'UPDATE tbl_Avatar SET sm_autoBanLoginFlag={autoFlag}, sm_banLogin={endTime} WHERE sm_gbID={gbId}'
    KBEngine.executeRawDatabaseCommand(_sql, callback)

def beginDisbanLogin(gbId, callback):
    _sql = f'SELECT sm_autoBanLoginFlag, sm_banLogin FROM tbl_Avatar WHERE sm_gbID={gbId}'
    KBEngine.executeRawDatabaseCommand(_sql, callback)

def disbanLogin(gbId, callback):
    _sql = f'UPDATE tbl_Avatar SET sm_autoBanLoginFlag=-1, sm_banLogin=0 WHERE sm_gbID={gbId}'
    KBEngine.executeRawDatabaseCommand(_sql, callback)


def beginBanIDIP(gbId, callback):
    _sql = f'SELECT sm_idipBanDict, sm_idipBanDataDict FROM tbl_Avatar WHERE sm_gbID={gbId}'
    KBEngine.executeRawDatabaseCommand(_sql, callback)

def banIDIP(gbId, idipBanDict, idipBanDataDict, callback):
    idipBanDict = cPickle.dumps(idipBanDict)
    idipBanDataDict = cPickle.dumps(idipBanDataDict)
    _sql = f'UPDATE tbl_Avatar SET sm_idipBanDict=0x{idipBanDict.hex()}, sm_idipBanDataDict=0x{idipBanDataDict.hex()} WHERE sm_gbID={gbId}'
    KBEngine.executeRawDatabaseCommand(_sql, callback)

def beginDisbanIDIP(gbId, callback):
    _sql = f'SELECT sm_idipBanDict, sm_idipBanDataDict FROM tbl_Avatar WHERE sm_gbID={gbId}'
    KBEngine.executeRawDatabaseCommand(_sql, callback)

def disbanIDIP(gbId, idipBanDict, idipBanDataDict, callback):
    idipBanDict = cPickle.dumps(idipBanDict)
    idipBanDataDict = cPickle.dumps(idipBanDataDict)
    _sql = f'UPDATE tbl_Avatar SET sm_idipBanDict=0x{idipBanDict.hex()}, sm_idipBanDataDict=0x{idipBanDataDict.hex()} WHERE sm_gbID={gbId}'
    KBEngine.executeRawDatabaseCommand(_sql, callback)

def queryBanInfo(gbId, callback):
    _sql = f'SELECT sm_autoBanLoginFlag, sm_banLogin, sm_idipBanDict, sm_idipBanDataDict FROM tbl_Avatar WHERE sm_gbID={gbId}'
    KBEngine.executeRawDatabaseCommand(_sql, callback)

def getAvatarAuthOfflineTime(gbId, callback):
    _sql = f'SELECT sm_gbID, sm_authStatistics_authOffline, sm_tsLastOfflineBase FROM tbl_Avatar WHERE sm_gbID={gbId}'
    KBEngine.executeRawDatabaseCommand(_sql, callback)

def recordModifyCurrency(gbId, itemId, itemNum, callback):
    dic = {
        gameconst.ItemIdEnum.MONEY          : "sm_money",
        gameconst.ItemIdEnum.BIND_MONEY     : "sm_bindMoney",
        gameconst.ItemIdEnum.COIN           : "sm_coin",
        gameconst.ItemIdEnum.DARK_IRON      : "sm_darkIron",
        gameconst.ItemIdEnum.GUILD_CONTRIB  : "sm_guildContrib",
    }
    fieldStr = dic[itemId]
    _sql = '''CALL gamesp_record_modify_currency(%s, %s, %s)'''%(gbId, utils.escape_string(fieldStr), itemNum)
    KBEngine.executeRawDatabaseCommand(_sql, callback)

def recordMulModifyCurrency(gbId, updateNumListStr, callback):
    fieldListStr = "sm_money, sm_bindMoney, sm_coin, sm_darkIron, sm_guildContrib"
    _sql = '''CALL gamesp_record_mul_modify_currency(%s, %s, %s)'''%(gbId, utils.escape_string(fieldListStr), utils.escape_string(updateNumListStr))
    KBEngine.executeRawDatabaseCommand(_sql, callback)

def loadModifyCurrency(avatar, callback):
    _sql = '''CALL gamesp_load_modify_currency(%s)'''%(avatar.gbID)
    KBEngine.executeRawDatabaseCommand(_sql, callback)
# --------------------------- auth avatar end --------------------------------

# =========================== SAFE BOX ======================================

def loadSafeBoxUnclaimed(gbId, limit, callback):
    _sql = (
        f'SELECT id, itemId, itemCount, itemPrice, claimed, '
        f'claimTime, orderId, orderTime '
        f'FROM {gameconst.TABLE_NAME_GAME_SAFE_BOX} '
        f'WHERE gbId={gbId} AND claimed=0 '
        f'ORDER BY orderTime DESC, id DESC '
        f'LIMIT {limit}'
    )
    KBEngine.executeRawDatabaseCommand(_sql, callback)


def loadSafeBoxRecentClaimed(gbId, limit, callback):
    _sql = (
        f'SELECT id, itemId, itemCount, itemPrice, claimed, '
        f'claimTime, orderId, orderTime '
        f'FROM {gameconst.TABLE_NAME_GAME_SAFE_BOX} '
        f'WHERE gbId={gbId} AND claimed=1 '
        f'ORDER BY claimTime DESC, id DESC '
        f'LIMIT {limit}'
    )
    KBEngine.executeRawDatabaseCommand(_sql, callback)


def loadMoreUnclaimedSafeBox(gbId, cursorOrderTime, cursorId, limit, callback):
    _sql = (
        f'SELECT id, itemId, itemCount, itemPrice, claimed, '
        f'claimTime, orderId, orderTime '
        f'FROM {gameconst.TABLE_NAME_GAME_SAFE_BOX} '
        f'WHERE gbId={gbId} AND claimed=0 AND '
        f'(orderTime < {cursorOrderTime} OR '
        f'(orderTime = {cursorOrderTime} AND id < {cursorId})) '
        f'ORDER BY orderTime DESC, id DESC '
        f'LIMIT {limit}'
    )
    KBEngine.executeRawDatabaseCommand(_sql, callback)


def insertSafeBoxItem(gbId, itemId, itemCount, itemPrice, orderId, orderTime, callback):
    _sql = (
        f'INSERT INTO {gameconst.TABLE_NAME_GAME_SAFE_BOX} '
        f'(gbId, itemId, itemCount, itemPrice, claimed, claimTime, orderId, orderTime) '
        f'VALUES ({gbId}, {itemId}, {itemCount}, {itemPrice}, {gameconst.SafeBoxClaimState.INIT}, {0}, {utils.escape_string(orderId)}, {orderTime})'
    )
    KBEngine.executeRawDatabaseCommand(_sql, lambda ret, num, insertId, err: callback(ret, num, insertId, err))


def claimSafeBoxItem(safeBoxId, claimTime, callback):
    _sql = f'UPDATE {gameconst.TABLE_NAME_GAME_SAFE_BOX} SET claimed={gameconst.SafeBoxClaimState.CLAIMED}, claimTime={claimTime} WHERE id={safeBoxId}'
    KBEngine.executeRawDatabaseCommand(_sql, lambda ret, num, insertId, err: callback(ret, num, insertId, err))

def deleteSafeBoxItem(safeBoxId, callback=None):
    _sql = f'DELETE FROM {gameconst.TABLE_NAME_GAME_SAFE_BOX} WHERE id={safeBoxId}'
    KBEngine.executeRawDatabaseCommand(_sql, callback or (lambda ret, num, insertId, err: None))


def checkOrderExists(orderId, callback):
    _sql = (
        f'SELECT id FROM {gameconst.TABLE_NAME_GAME_SAFE_BOX_IDEMPOTENT} '
        f'WHERE orderId="{utils.escape_string(orderId)}" '
        f'LIMIT 1'
    )
    KBEngine.executeRawDatabaseCommand(_sql, callback)

def recordOrderId(orderId, callback):
    _sql = (
        f'INSERT INTO {gameconst.TABLE_NAME_GAME_SAFE_BOX_IDEMPOTENT} '
        f'(orderId) '
        f'VALUES ({utils.escape_string(orderId)})'
    )
    KBEngine.executeRawDatabaseCommand(_sql, callback)
