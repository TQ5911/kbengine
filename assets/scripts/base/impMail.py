# -*- coding: utf-8 -*-

from KBEDebug import *
import utils
import gamesql
import Mail
import gameglobal
import mail_mail as MAMAD
import dropAward
import gameengine
import gameconst
import antiAddictCategory_antiAddictCategory_def as AAC_AACDD
import message_Message_def as MMD
import mail_config as MACF
import mailAssistor
import dataUtils
import gamelog
import gametimer
import re
import gamedecorator
import serverList_serverList as SLSL
import gameconfig
import gametlog
import KBEngine
import gameclass


class ImpMail(object):

    def __init__(self):
        self.mailCacheData = Mail.MailCacheData()
        self.mailInitLockedTime = utils.getNow()+60

    def mailOnLogin(self):
        try:
            self.startCheckAccountMails()
        except Exception as e:
            ERROR_MSG('startCheckAccountMails exception:', e)

    def sendAllMailList(self):
        self.client.onGetMailList(self.mailCacheData.getClientMailList())

    def startCheckAccountMails(self):
        #登陆情况下，依次执行：
        # 1. 从db检查发送给account的邮件
        # 2. 同步离线期间全服邮件
        # 3. 下发邮件列表
        self.mailInitLockedTime = utils.getNow()+60
        mailAssistor.checkAccountMails(self.accountName, self.accountEntity.accountType, self.gbID, self.id)
        return

    def onCheckAccountMailsFinished(self):
        self.startLoadSyncGlobalMailInfo()

    def canReceiveGlobalMail(self, globalMail):
        mailId = globalMail.mailId
        myLevel = self.getAvatarLevel()
        if self.birthInDB < globalMail.minRoleTime or self.birthInDB > globalMail.maxRoleTime:
            return False
        if myLevel < globalMail.minRoleLevel or myLevel > globalMail.maxRoleLevel:
            return False

        return True

    def sendOneGlobalMail(self, globalMail):
        DEBUG_MSG('in sendOneGlobalMail:', globalMail.globalMailGBID)
        if not self.canReceiveGlobalMail(globalMail):
            return
        self.doInsertGlobalMail(0, globalMail)
        return

    def startLoadSyncGlobalMailInfo(self):
        # 首先获得同步过的全服邮件最新信息
        gamesql.loadLastGlobalMailInfo(self.gbID, self.loadLastGlobalMailInfoCallback)

    def loadLastGlobalMailInfoCallback(self, ret, num, insertId, err):
        DEBUG_MSG('loadLastGlobalMailInfoCallback:', ret, num, insertId, err)
        if err:
            gameengine.reportCritical(' loadLastGlobalMailInfoCallback, no lastGlobalMailInfo:', ret, num, insertId, err)
            return
        dbMailRowData = ret[0]
        lastGlobalMailTime = int(dbMailRowData[2].decode())
        myLevel = self.getAvatarLevel()
        if not myLevel:
            gameengine.reportCritical('loadLastGlobalMailInfoCallback, has no avatar level')
            return
        globalMailList = mailAssistor.getMyGlobalsMails(lastGlobalMailTime, self.birthInDB, myLevel, self.hasGotGlobalMails)
        newGlobalMailList = []
        for globalMail in globalMailList:
            if globalMail.globalMailGBID in self.mailCacheData.globalMailsMap:
                gameengine.reportCritical('syncGlobalMails,  reduplicative global mail:', globalMail.__dict__)
                continue
            if not self.canReceiveGlobalMail(globalMail):
                continue
            newGlobalMailList.append(globalMail)

        if newGlobalMailList:
            opUUID = KBEngine.genUUID64()
            globalMail = newGlobalMailList.pop()
            utils.setCallbackTmpInfo(self, opUUID, newGlobalMailList)
            self.doInsertGlobalMail(opUUID, globalMail)
        else:
            #没有新的全服邮件
            INFO_MSG('no global mail, mail init finished')
            self.mailInitFinishedOnLogin()
            self.startLoadMails()
        return

    def doInsertGlobalMail(self, opUUID, globalMail):
        mailAssistor.sendMailToPlayers([self.gbID], globalMail.mailId, extraAttach=globalMail.extraAttach,
                                       despArgs=globalMail.despArgs, globalMailGBID=globalMail.globalMailGBID,
                                       createTime=globalMail.createTime, expiredTime=globalMail.expiredTime, title=globalMail.title,
                                       cont=globalMail.cont, callback=lambda ret, num, insertId, err, mailGBID:
                                    self.insertGlobalMailCallback(ret, num, insertId, err, mailGBID, opUUID, globalMail.createTime))
        return

    def insertGlobalMailCallback(self, ret, num, insertId, err, mailGBID, opUUID, mailCreateTime):
        DEBUG_MSG('insertGlobalMailCallback:', ret, num, insertId, err, mailGBID, opUUID)
        if err:
            gameengine.reportCritical('insertGlobalMailCallback, error:', ret, num, insertId, err)

        self.mailCacheData.setLastGlobalMailTime(mailCreateTime)
        self.hasGotGlobalMails[mailGBID] = utils.getNow()
        insertGlobalMailList = utils.popCallbackTmpInfo(self, opUUID)
        if not insertGlobalMailList:
            INFO_MSG('insert all global mail succ, mail init finished')
            self.mailInitFinishedOnLogin()
            self.startLoadMails()
        else:
            globalMail = insertGlobalMailList.pop()
            utils.setCallbackTmpInfo(self, opUUID, insertGlobalMailList)
            self.doInsertGlobalMail(opUUID, globalMail)
        return

    def onNewMailInsertSucc(self, mailId, mailGBID, title, cont, attachStr, srcType, srcSubType, opUUID, desc, idipSource):
        # 有新普通邮件插入数据库表中
        INFO_MSG('onNewMailInsertSucc:', mailId)
        self.startLoadMails()
        releCacheInfo = gameglobal.roleCache.get(self.id)
        if not releCacheInfo:
            # NOTE(): 这里说明玩家已经下线了
            mailAssistor.doRecordOfflinePlayerMailLog(
                self.gbID, mailId, mailGBID, title, cont, attachStr,
                srcType,srcSubType, opUUID, desc, idipSource)

        else:
            mailAssistor.recordPlayerMailLog(
                self.gbID, mailId, mailGBID, title, cont, attachStr, self.accountEntity.accountName,
                self.accountEntity.accountType, releCacheInfo['name'], releCacheInfo['level'],
                srcType, srcSubType, opUUID, desc, idipSource, self.accountEntity.channelId)

    def mailInitFinishedOnLogin(self):
        INFO_MSG('mailInitFinishedOnLogin')
        self.mailInitLockedTime = 0
        lastGlobalMailTime = mailAssistor.getLastGlobalMailTime()
        if lastGlobalMailTime:
            gamesql.updateLastGlobaMailInfo(self.gbID, lastGlobalMailTime, lambda ret, num, insertId, err:
                                            self._updateLastGlobalMailInfoCallback(ret, num, insertId, err, lastGlobalMailTime))

    def _updateLastGlobalMailInfoCallback(self, ret, num, insertId, err, lastGlobalMailTime):
        DEBUG_MSG('_updateLastGlobalMailInfoCallback:', ret, num, insertId, err, lastGlobalMailTime)

    def delayStartLoadMails(self):
        DEBUG_MSG('delayStartLoadMails')
        self.loadMailTimerId = 0
        self.startLoadMails()

    def startLoadMails(self):
        if utils.getNow() < self.mailInitLockedTime:
            WARNING_MSG('startLoadMails, mail init not finished')
            return

        if self.mailInitLockedTime != 0:
            # 到这里并且self.mailInitLockedTime不为0， 说明邮件初始化流程出错中断
            gameengine.reportCritical('startLoadMails, init mail from db error')

        DEBUG_MSG('startLoadMails:', self.mailCacheData.newestMailCreateTime)
        if utils.getNow() < self.loadMailCDTime:
            if not self.loadMailTimerId:
                self.loadMailTimerId = self._callback(1, 'delayStartLoadMails', (), gametimer.TIMER_TAG_LOAD_MAIL, 'loadMailTimerId')
            return

        self.loadMailCDTime = utils.getNow()+3
        gamesql.loadMailsFromDB(self.gbID, self.mailCacheData.newestMailCreateTime,
                                self.mailCacheData.mailGBIDListAtNewestCreateTime(), self._loadMailsFromDBCallback)

    def _loadMailsFromDBCallback(self, ret, num, insertId, err):
        if self.isDestroying or self.isDestroyed:
            return

        if err:
            ERROR_MSG('     in _loadMailsFromDBCallback, db op error:', ret, num, insertId, err)
            return

        DEBUG_MSG('in _loadMailsFromDBCallback:', len(ret))
        maxMailNum = MACF.datas['mailNumMax']['value']
        validMailList = []
        if len(ret) > maxMailNum:
            # 如果出现当前邮件数量大于maxMailNum，优先保留有附件且未读邮件
            WARNING_MSG('_loadMailsFromDBCallback, mails reach limit:', len(ret))
            validMailGBIDSet = set()
            minMailTime = int(ret[-1][5].decode())
            minMailTiemMailList = []
            for dbMailRowData in ret:
                mailGBID = int(dbMailRowData[2].decode())
                readStat = int(dbMailRowData[4].decode())
                attachStat = int(dbMailRowData[9].decode())
                if attachStat == gameconst.MailAttachState.NotGet or readStat == gameconst.MailReadState.NotRead:
                    createTime = int(dbMailRowData[5].decode())
                    validMailGBIDSet.add(mailGBID)
                    if createTime == minMailTime:
                        minMailTiemMailList.append(mailGBID)
                    if len(validMailGBIDSet) == maxMailNum:
                        break

            delMailGBIDList = []
            leftNum = maxMailNum-len(validMailGBIDSet)
            for dbMailRowData in ret:
                mailGBID = int(dbMailRowData[2].decode())
                if mailGBID in validMailGBIDSet:
                    validMailList.append(dbMailRowData)
                elif leftNum > 0:
                    validMailList.append(dbMailRowData)
                    leftNum-=1
                else:
                    delMailGBIDList.append(mailGBID)

            gamesql.deleteMultiMails(self.gbID, delMailGBIDList, lambda ret, num, insertId, err:
                                     self.deleteExceedMailsCallback(ret, num, insertId, err, delMailGBIDList))
            if len(delMailGBIDList) >= maxMailNum:
                gamesql.deleteOldMails(self.gbID, minMailTime, minMailTiemMailList, lambda ret, num, insertId, err:
                                     self.deleteOldMailsCallback(ret, num, insertId, err, minMailTime))

        hasOldMail = not self.mailCacheData.isEmpty()
        validMailList = validMailList or ret
        exceedNum = len(validMailList) - self.mailCacheData.mailSpaceLeft()
        if exceedNum > 0:
            INFO_MSG('_loadMailsFromDBCallback exceedNum:', exceedNum)
            rmCacheMailList = self.mailCacheData.getReplaceMailList(exceedNum)
            rmMails = self.mailCacheData.deleteMailsCache(rmCacheMailList)
            gamesql.deleteMultiMails(self.gbID, rmCacheMailList, lambda ret, num, insertId, err:
                                     self.deleteMultiMailsCallback(ret, num, insertId, err, rmMails, AAC_AACDD.datas.BONUS_SRC_EXCEED_DELETE_MAIL, 'exceed limit'))

        expiredMailGBIDList = []
        expiredMailObjs = {}
        newMailList = []
        logMailList = []
        for dbMailRowData in validMailList:
            mailObj = Mail.Mail()
            mailObj.initFromDBMailData(dbMailRowData)
            if mailObj.isExpired():
                expiredMailGBIDList.append(mailObj.mailGBID)
                expiredMailObjs[mailObj.mailGBID] = mailObj
                continue
            if self.mailCacheData.addNewMailCache(mailObj):
                if hasOldMail:
                    #有旧邮件，本次load的是新收到的邮件
                    newMailList.append(mailObj.toMailClientDict())
                    logMailList.append(mailObj)
        if not hasOldMail:
            #没有旧邮件，本次load的是全部邮件
            self.sendAllMailList()
            self.recordSecMailFlow(self.mailCacheData.mails.values())
        else:
            self.client.onGetNewMail(newMailList)
            self.recordSecMailFlow(logMailList)

        if expiredMailGBIDList:
            gamesql.deleteMultiMails(self.gbID, expiredMailGBIDList,
                                     lambda ret, num, insertId, err:self.deleteMultiMailsCallback(ret, num, insertId,
                                                                              err, expiredMailObjs, AAC_AACDD.datas.BONUS_SRC_EXPIRE_DELETE_MAIL, 'delete expired'))

    def recordSecMailFlow(self, mailList, delayTimes=0):
        return
        roleInfo = gameglobal.roleCache.get(self.id)
        if delayTimes < 30 and (not roleInfo or 'SecReportData' not in roleInfo or 'battlePoint' not in roleInfo):
            delayTimes += 1
            WARNING_MSG('recordSecMailFlow, delayTimes:', delayTimes)
            self._callback(0.1, 'recordSecMailFlow', (mailList, delayTimes), gametimer.TIMER_TAG_MAIL_LOG)
            return

        lastLogTime = max(self.mailLogInfoDic.keys()) if self.mailLogInfoDic else 0
        self.mailLogInfoDic.setdefault(lastLogTime, set())
        for mail in mailList:
            mailTime = mail.createTime
            if mailTime < lastLogTime:
                # 比较晚的邮件，日志已经记录过了
                continue

            self.mailLogInfoDic.setdefault(mailTime, set())
            if mail.mailGBID in self.mailLogInfoDic[lastLogTime]:
                continue
            self.mailLogInfoDic[mailTime].add(mail.mailGBID)

            #记录日志
            mailData = MAMAD.datas[mail.mailId]
            title = mail.title if mail.title else mailData['title']
            cont = mail.cont if mail.cont else mailData['content']
            # logDataDic = {
            #     'vGameAppid': utils.getGameAppId(self.accountEntity.channelId),
            #     'PlatID': self.accountEntity.devicePlatId,
            #     'AreaID': self.accountEntity.channelId,
            #     'ZoneID': gameconfig.serverId(),
            #     'OpenID': self.accountEntity.accountName,
            #     'ClientVersion': '',
            #     'SecReportData': roleInfo.get('SecReportData',''),
            #     'UserIP': self.getClientIp(),
            #     'RoleID': str(self.gbID),
            #     'RoleName': roleInfo['name'],
            #     'RoleType': roleInfo['school'],
            #     'RoleLevel': roleInfo['level'],
            #     'RoleBattlePoint': roleInfo.get('battlePoint', 0),
            #     'RolePicUrl': '',
            #     'RoleGroupID': str(self.guildUUIDBase),
            #     'RoleGroupName': self.guildNameBase,
            #     'ReceiverOpenID': self.accountEntity.accountName,
            #     'ReceiverRoleID': str(self.gbID),
            #     'ReceiverRoleName': roleInfo['name'],
            #     'ReceiverRoleType': roleInfo['school'],
            #     'ReceiverRoleLevel': roleInfo['level'],
            #     'ReceiverRoleBattlePoint': roleInfo.get('battlePoint', 0),
            #
            #     'MailType': 2 if mailData['type'] == 1 else 1,
            #     'TitleContents': re.sub(gameconst.MAIL_LOG_TEXT_FILTER, '', title),
            #     'ChatContents': re.sub(gameconst.MAIL_LOG_TEXT_FILTER, '', cont),
            #     'MsgType': 0,
            # }
            # gamelog.makeSecMailFlowLog(logDataDic)

        #只保留时间最近的记录
        maxLogTime = max(self.mailLogInfoDic.keys())
        self.mailLogInfoDic = {maxLogTime:self.mailLogInfoDic[maxLogTime]}
        return

    def deleteExceedMailsCallback(self, ret, num, insertId, err, delMailGBIDList):
        if err:
            WARNING_MSG('   deleteExceedMailsCallback failed:', err, delMailGBIDList)
        return

    def deleteOldMailsCallback(self, ret, num, insertId, err, oldMailTime):
        if err:
            WARNING_MSG('   deleteOldMailsCallback failed:', err, oldMailTime)
        return

    def reqReadOneMail(self, mailGBID):
        DEBUG_MSG('in reqReadOneMail:', mailGBID)
        gamesql.setMailHasRead(self.gbID, mailGBID, lambda ret, num, insertId, err, mailGBID=mailGBID:
                                            self.setMailHasReadCallback(ret, num, insertId, err, mailGBID))

    def setMailHasReadCallback(self, ret, num, insertId, err, mailGBID):
        DEBUG_MSG('in setMailHasReadCallback:', ret, num, insertId, err)
        if err:
            WARNING_MSG('setMailHasReadCallback failed:', err)
            return
        self.mailCacheData.readMail(mailGBID)
        self.client.onReadOneMail(mailGBID)

    def reqGetOneMailAttach(self, mailGBID):
        DEBUG_MSG('in reqGetOneMailAttach:', mailGBID)
        mail = self.mailCacheData.getMailByGBID(mailGBID)
        if not mail:
            return
        self.getMailAttachByMailList([mail])

    @gamedecorator.limitcall(2)
    def reqGetAllMailsAttach(self):
        DEBUG_MSG('in reqGetAllMailsAttach')
        mailList = self.mailCacheData.getMailsWithAttachHasNotGet()
        if not mailList:
            WARNING_MSG('   reqGetAllMailsAttach, no mail with attach has not get')
            return
        self.getMailAttachByMailList(mailList)

    def getMailAttachByMailList(self, mailList):
        mailGBIDList = []
        totalWealthVal = dropAward.AwardVal()
        srcType = AAC_AACDD.datas.BONUS_SRC_MAIL_ATTACH
        hasSendSpaceNotEnoughMsg = False
        for mail in mailList:
            if mail.isExpired():
                WARNING_MSG('getMailAttachByMailList mail expired:', mail.expiredTime)
                continue

            if not mail.canGetAttach():
                WARNING_MSG('getMailAttachByMailList, can not get mail attach:', mail.toMailSavedDict())
                continue

            #注意加号'+'前后的wealth顺序不能变
            tryWealthVal = mail.attach.getAwardVal() + totalWealthVal
            tryAddResult = self.canAddWealthVal(srcType, tryWealthVal, bMsg=False, fromMail=True)
            if not tryAddResult:
                if not hasSendSpaceNotEnoughMsg:
                    hasSendSpaceNotEnoughMsg = True
                    if tryAddResult.extra == gameconst.BagOPStat.BAG_OP_NO_SPACE:
                        self.onMessagePre(MMD.datas.bagFullGeneralMessage, [])
                continue
            totalWealthVal = tryWealthVal
            mailGBIDList.append(mail.mailGBID)
        if not mailGBIDList:
            return

        if not self.bagData.tryLockBag(lockDesc='getMailAttachByMailList'):
            return
        #先设置缓存中附件为已领取状态
        for mailGBID in mailGBIDList:
            self.mailCacheData.setAttachHasGet(mailGBID)
        gamesql.setMailHasGetAttach(self.gbID, mailGBIDList, lambda ret, num, insertId, err:
                                      self.setMailAttachHasGetCallback(ret, num, insertId, err, mailGBIDList))

    def setMailAttachHasGetCallback(self, ret, num, insertId, err, mailGBIDList):
        #DEBUG_MSG('in getMailAttachCallback:', ret, num, insertId, err)
        self.unlockBag(gameconst.BagType.BAG_TYPE_NORMAL)
        if err:
            WARNING_MSG('   setMailAttachHasGetCallback failed:', err)
            return

        _mailGBIDs = []
        uniqueId = KBEngine.genUUID64()
        popRewardUUID = KBEngine.genUUID64()
        now = utils.getNow()
        for mailGBID in mailGBIDList:
            mail = self.mailCacheData.getMailByGBID(mailGBID)
            if not mail:
                gameengine.reportCritical('setMailAttachHasGetCallback, no mail:', mailGBID)
                continue

            wealthVal = mail.attach.getAwardVal()
            opUUID = mail.opUUID or uniqueId
            if not self.canAddWealthVal(AAC_AACDD.datas.BONUS_SRC_MAIL_ATTACH, wealthVal, bMsg=True):
                # 正常情况不会走到这里
                gameengine.reportCritical('setMailAttachHasGetCallback, add attach wealthval failed:', mailGBID, mail.mailId)
                self.resetMailAttachState(opUUID, mailGBID, mail.readStat)
                continue
            _mailGBIDs.append(mailGBID)
            mail.setReadState(gameconst.MailReadState.HasRead)
            wealthVal.scrubWealthItemObjs(createTime=now)
            srcType = mail.srcType if mail.srcType else AAC_AACDD.datas.BONUS_SRC_MAIL_ATTACH
            detail = gameclass.AwardDetail(mailGBID=[mailGBID], desc=mail.desc, popRewardUUID=popRewardUUID)
            self.addWealth(srcType, wealthVal, opUUID, detail=detail, srcSubType=mail.srcSubType, idipSource=mail.source, directly=False)

            attachStr = mail.attach.getItemsTLogStr()
            mailAssistor.recordPlayerMailLog(
                self.gbID, mail.mailId, mailGBID, mail.title, mail.cont, attachStr, self.accountEntity.accountName,
                self.accountEntity.accountType, self.getRoleCacheAttr('name', ''), self.getAvatarLevel(),
                srcType, mail.srcSubType, opUUID, mail.desc, mail.source, self.accountEntity.channelId,
                opType = gametlog.PlayerMailOpType.AttachReward)

        self._showPopReward(AAC_AACDD.datas.BONUS_SRC_MAIL_ATTACH, popRewardUUID, gameclass.AwardDetail(mailGBID=_mailGBIDs))
        self.client.onGetMailAttach(_mailGBIDs)
        return

    def resetMailAttachState(self, opUUID, mailGBID, readState):
        INFO_MSG('resetMailAttachState:', opUUID, mailGBID, readState)
        gamesql.resetMailAttachNotState(self.gbID, mailGBID, readState, lambda ret, num, insertId, err, opUUID=opUUID:
                                            self.resetMailAttachStateCallback(ret, num, insertId, err, opUUID))

    def resetMailAttachStateCallback(self, ret, num, insertId, err, opUUID):
        DEBUG_MSG('in resetMailAttachStateCallback:', ret, num, insertId, opUUID)
        mailGBIDList = utils.popCallbackTmpInfo(self, opUUID)
        if err:
            gameengine.reportCritical('     resetMailAttachStateCallback failed:', ret, num, insertId, self.gbID, opUUID, mailGBIDList)
            return

        for mailGBID in mailGBIDList:
            mail = self.mailCacheData.getMailByGBID(mailGBID)
            mail and mail.setAttachState(gameconst.MailAttachState.NotGet)

        INFO_MSG('resetMailAttachStateCallback, reset mail attach state succ:', mailGBIDList)
        return

    def reqDelMails(self, mailGBIDList):
        # 删除选中的邮件
        DEBUG_MSG('in reqDelMails:', mailGBIDList)
        if not mailGBIDList:
            return
        mailGBID = mailGBIDList[0]
        mail = self.mailCacheData.getMailByGBID(mailGBID)
        if not mail:
            WARNING_MSG('reqDelMails, no mail:', mailGBIDList)
            return

        if mail.canGetAttach():
            DEBUG_MSG('reqDelMails, del mail failed, has attach:', mailGBID)
            self.onMessagePre(MMD.datas.mailDelete_Fail, [])
            return

        gamesql.deleteMailByMailGBID(self.gbID, mailGBID, lambda ret, num, insertId, err, mailGBID=mailGBID:
                                            self.deleteMailByMailGBIDCallback(ret, num, insertId, err, mailGBID))
        return

    def deleteMailByMailGBIDCallback(self, ret, num, insertId, err, mailGBID):
        DEBUG_MSG('deleteMailByMailGBIDCallback:', ret, num, insertId, err, mailGBID)
        if err:
            gameengine.reportCritical('   deleteMailByMailGBIDCallback failed:', mailGBID)
            return
        self.onMailsDeleted({mailGBID:self.mailCacheData.getMailByGBID(mailGBID)}, srcType=AAC_AACDD.datas.BONUS_SRC_CLIENT_DELETE_MAIL, desc='from client')
        return

    def reqDelAllMails(self):
        DEBUG_MSG('in reqDelAllMails')
        delMailGBIDList = self.mailCacheData.getMailListCanDelete()
        if not delMailGBIDList:
            WARNING_MSG('reqDelAllMails, no mail can delete')
            return
        rmMails = self.mailCacheData.deleteMailsCache(delMailGBIDList)
        gamesql.deleteMultiMails(self.gbID, delMailGBIDList, lambda ret, num, insertId, err, delMailGBIDList=delMailGBIDList:
                                            self.deleteMultiMailsCallback(ret, num, insertId, err, rmMails, AAC_AACDD.datas.BONUS_SRC_CLIENT_DELETE_MAIL, 'from client'))

    def deleteMultiMailsCallback(self, ret, num, insertId, err, rmMails, srcType, desc):
        if err:
            WARNING_MSG('   deleteMultiMailsCallback failed')
            return
        self.onMailsDeleted(rmMails, srcType, desc=desc)
        return

    def onMailsDeleted(self, rmMails, srcType=0, srcSubType=0, desc='', idipSource=0, sendClient=True):
        mailGBIDList = list(rmMails.keys())
        now = utils.getNow()
        expireDuration = gameconst.ONE_DAY_SECONDS * 60
        for mailGbId in list(self.hasGotGlobalMails.keys()):
            tAdd = self.hasGotGlobalMails[mailGbId]
            if mailGbId not in gameglobal.globalMailsCacheList and now - tAdd > expireDuration:
                self.hasGotGlobalMails.pop(mailGbId, 0)
        self.mailCacheData.deleteMailsCache(mailGBIDList)
        sendClient and self.client.onDelMails(mailGBIDList)
        opUUID = KBEngine.genUUID64()
        for mailGBID, mVal in rmMails.items():
            if not mVal:
                continue
            self.doRecordDeleteMailLog(mVal, opUUID, srcType, srcSubType, desc, idipSource, mailGBID)
        return

    def doRecordDeleteMailLog(self, mail, opUUID, srcType, srcSubType, desc, idipSource, mailGBID):
        attachStr = mail.attach.getItemsTLogStr()
        mailAssistor.recordPlayerMailLog(
                self.gbID, mail.mailId, mailGBID, mail.title, mail.cont, attachStr, self.accountEntity.accountName,
                self.accountEntity.accountType, self.getRoleCacheAttr('name', ''), self.getAvatarLevel(),
                srcType, srcSubType, opUUID, desc, idipSource, self.accountEntity.channelId,
                opType = gametlog.PlayerMailOpType.DeleteMail)
        # mailAssistor.recordDeleteMailLog(self.accountEntity.accountType, self.accountEntity.accountName, self.gbID,
        #  roleInfo['name'], roleInfo['level'], srcType, srcSubType, desc, idipSource, 0, mailGBID, mailVal, self.accountEntity.channelId)

    def leftMailSpace(self):
        return self.mailCacheData.mailSpaceLeft()

    def gmDeleteGlobalMail(self, delGBMailGBID, delTime):
        # 撤回一封可能已经收到的全服邮件
        DEBUG_MSG('gmDeleteGlobalMail:', delGBMailGBID, delTime)
        return
