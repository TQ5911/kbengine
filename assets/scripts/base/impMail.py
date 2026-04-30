# -*- coding: utf-8 -*-

from KBEDebug import *
import functools
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
import gameconfig
import KBEngine
import gameclass
import itemData_set as IDSD
import itemData_itemData_set as IDIDS
import agent_agentFunction as A_AFD
import AuthClsWraper
import LogTrackingMgr

class ImpMail(object):

    def __init__(self):
        self.mailCacheData = Mail.MailCacheData()
        self.mailInitLockedTime = utils.curTS()+60
        self.loadMailType = gameconst.MailLoadType.DEFAULT
        self.loadFinishedCount = 0
        self.hasOldMails = False
        self.hasDeleteMails = False
        self.newMails = []

    def mailOnLogin(self):
        try:
            self.startCheckAccountMails()
        except Exception as e:
            LOG_ERR('startCheckAccountMails exception:', e)

    def sendAllMailList(self):
        self.client.onGetMailList(self.mailCacheData.getClientMailList(), self.mailCacheData.playerMailSpaceLeft(), self.mailCacheData.systemMailSpaceLeft())

    def startCheckAccountMails(self):
        #登陆情况下，依次执行：
        # 1. 从db检查发送给account的邮件
        # 2. 同步离线期间全服邮件
        # 3. 下发邮件列表
        self.mailInitLockedTime = utils.curTS()+60
        mailAssistor.checkAccountMails(self.accountName, self.accountEntity.accountType, self.gbID, self.id)
        return

    def onCheckAccountMailsFinished(self):
        self.startLoadSyncGlobalMailInfo()

    def checkGlobalMail(self, globalMail):
        return mailAssistor.checkGlobalMailConds(globalMail, self.accountEntity.accountType, self.getAvatarLevel(), self.birthInDB, self.tLoginBase)

    def sendOneGlobalMail(self, globalMail):
        LOG_IFO('in sendOneGlobalMail:', globalMail.globalMailGBID)
        if not self.checkGlobalMail(globalMail):
            return
        self.doInsertGlobalMail(0, globalMail)
        return

    def startLoadSyncGlobalMailInfo(self):
        # 首先获得同步过的全服邮件最新信息
        gamesql.loadLastGlobalMailInfo(self.gbID, self.loadLastGlobalMailInfoCallback)

    def loadLastGlobalMailInfoCallback(self, ret, num, insertId, err):
        LOG_IFO('loadLastGlobalMailInfoCallback:', ret, num, insertId, err)
        if err:
            gameengine.panicStack(' loadLastGlobalMailInfoCallback, no lastGlobalMailInfo:', ret, num, insertId, err)
            return
        dbMailRowData = ret[0]
        lastGlobalMailTime = int(dbMailRowData[2].decode())
        myLevel = self.getAvatarLevel()
        if not myLevel:
            gameengine.panicStack('loadLastGlobalMailInfoCallback, has no avatar level')
            return
        globalMailList = mailAssistor.getMyGlobalsMails(lastGlobalMailTime, self.accountEntity.accountType, self.birthInDB, self.tLoginBase, myLevel, self.hasGotGlobalMails)
        newGlobalMailList = []
        for globalMail in globalMailList:
            if globalMail.globalMailGBID in self.mailCacheData.globalMailsMap:
                gameengine.panicStack('syncGlobalMails,  reduplicative global mail:', globalMail.__dict__)
                continue
            if not self.checkGlobalMail(globalMail):
                continue
            newGlobalMailList.append(globalMail)

        if newGlobalMailList:
            opUUID = KBEngine.genUUID64()
            globalMail = newGlobalMailList.pop()
            utils.setCallbackTmpInfo(self, opUUID, newGlobalMailList)
            self.doInsertGlobalMail(opUUID, globalMail, True)
        else:
            #没有新的全服邮件
            LOG_IFO('no global mail, mail init finished')
            self.mailInitFinishedOnLogin()
            self.startLoadMails(gameconst.MailLoadType.GLOBAL_AND_PLAYER_MAIL)
        return

    def doInsertGlobalMail(self, opUUID, globalMail, isLogin = False):
        mailAssistor.sendMailToPlayers([self.gbID], globalMail.mailId, extraAttach=globalMail.extraAttach,
                                       despArgs=globalMail.despArgs, globalMailGBID=globalMail.globalMailGBID,
                                       createTime=globalMail.createTime, expiredTime=globalMail.expiredTime, title=globalMail.title,
                                       cont=globalMail.cont, srcType=globalMail.srcType, callback=lambda ret, num, insertId, err, mailGBID:
                                    self.insertGlobalMailCallback(ret, num, insertId, err, mailGBID, opUUID, globalMail.createTime, isLogin), isGlobal = True)
        return

    def insertGlobalMailCallback(self, ret, num, insertId, err, mailGBID, opUUID, mailCreateTime, isLogin):
        LOG_IFO('insertGlobalMailCallback:', ret, num, insertId, err, mailGBID, opUUID, mailCreateTime, isLogin)
        if err:
            gameengine.panicStack('insertGlobalMailCallback, error:', ret, num, insertId, err)

        self.hasGotGlobalMails[mailGBID] = utils.curTS()
        insertGlobalMailList = utils.popCallbackTmpInfo(self, opUUID)
        if not insertGlobalMailList:
            LOG_IFO('insert all global mail succ, mail init finished')
            self.mailInitFinishedOnLogin()
            mailLoadType = gameconst.MailLoadType.GLOBAL_MAIL
            if isLogin:
                mailLoadType = gameconst.MailLoadType.GLOBAL_AND_PLAYER_MAIL
            self.startLoadMails(mailLoadType)
        else:
            globalMail = insertGlobalMailList.pop()
            utils.setCallbackTmpInfo(self, opUUID, insertGlobalMailList)
            self.doInsertGlobalMail(opUUID, globalMail, isLogin)
        return

    def onNewMailInsertSucc(self, mailId, mailGBID, title, cont, attachStr, srcType, srcSubType, opUUID, desc, idipSource, isGlobal):
        # 有新普通邮件插入数据库表中
        LOG_IFO('onNewMailInsertSucc:', mailId, isGlobal)
        mailLoadType = gameconst.MailLoadType.PLAYER_MAIL
        if isGlobal:
            mailLoadType = gameconst.MailLoadType.GLOBAL_MAIL
        self.startLoadMails(mailLoadType)

    def mailInitFinishedOnLogin(self):
        LOG_IFO('mailInitFinishedOnLogin')
        self.mailInitLockedTime = 0
        lastGlobalMailTime = mailAssistor.getLastGlobalMailTime()
        if lastGlobalMailTime:
            gamesql.updateLastGlobaMailInfo(self.gbID, lastGlobalMailTime, lambda ret, num, insertId, err:
                                            self._updateLastGlobalMailInfoCallback(ret, num, insertId, err, lastGlobalMailTime))

    def _updateLastGlobalMailInfoCallback(self, ret, num, insertId, err, lastGlobalMailTime):
        LOG_IFO('_updateLastGlobalMailInfoCallback:', ret, num, insertId, err, lastGlobalMailTime)

    def delayStartLoadMails(self, mailLoadType):
        LOG_IFO('delayStartLoadMails', mailLoadType)
        self.loadMailTimerId = 0
        self.startLoadMails(mailLoadType)

    def startLoadMails(self, mailLoadType):
        if utils.curTS() < self.mailInitLockedTime:
            LOG_WARN('startLoadMails, mail init not finished')
            return

        if self.mailInitLockedTime != 0:
            # 到这里并且self.mailInitLockedTime不为0， 说明邮件初始化流程出错中断
            gameengine.panicStack('startLoadMails, init mail from db error')

        LOG_IFO('startLoadMails:', mailLoadType, self.mailCacheData.lastPlayerMailTime, self.mailCacheData.lastGlobalMailTime)
        if utils.curTS() < self.loadMailCDTime:
            if not self.loadMailTimerId:
                self.loadMailTimerId = self.addTimerCB(1, 'delayStartLoadMails', (mailLoadType,), gametimer.TIMER_TAG_LOAD_MAIL, 'loadMailTimerId')
            return
        
        self.loadMailCDTime = utils.curTS()+5
        self.loadMailType = mailLoadType
        self.hasOldMail = not self.mailCacheData.isEmpty()

        if mailLoadType == gameconst.MailLoadType.GLOBAL_AND_PLAYER_MAIL \
            or mailLoadType == gameconst.MailLoadType.PLAYER_MAIL:
            gamesql.loadMailsFromDB(self.gbID, self.mailCacheData.lastPlayerMailTime, False,
                                    self.mailCacheData.mailGBIDListAtNewestCreateTime(False), functools.partial(self._loadMailsFromDBCallback, False, mailLoadType))

        if mailLoadType == gameconst.MailLoadType.GLOBAL_AND_PLAYER_MAIL \
            or mailLoadType == gameconst.MailLoadType.GLOBAL_MAIL:    
            gamesql.loadMailsFromDB(self.gbID, self.mailCacheData.lastGlobalMailTime, True,
                                    self.mailCacheData.mailGBIDListAtNewestCreateTime(True), functools.partial(self._loadMailsFromDBCallback, True, mailLoadType))

    def _loadMailsFromDBCallback(self, isGlobal, mailLoadType, ret, num, insertId, err):
        if self.isDestroying or self.isDestroyed:
            return
        if err:
            LOG_ERR('     in _loadMailsFromDBCallback, db op error:', isGlobal, ret, num, insertId, err)
            return

        LOG_IFO('in _loadMailsFromDBCallback:', isGlobal, mailLoadType, len(ret))
        maxMailNum = MACF.datas['mailNumMax']['value']
        if isGlobal:
            maxMailNum = MACF.datas['mailNumMax2']['value']
        validMailList = []
        if len(ret) > maxMailNum:
            # 如果出现当前邮件数量大于maxMailNum，优先保留有附件且未读邮件
            LOG_WARN('_loadMailsFromDBCallback, mails reach limit:', len(ret), maxMailNum, isGlobal)
            validMailGBIDSet = set()
            minMailTime = int(ret[-1][5].decode())
            minMailTiemMailList = []
            for dbMailRowData in ret:
                mailGBID = int(dbMailRowData[2].decode())
                readStat = int(dbMailRowData[4].decode())
                attachStat = int(dbMailRowData[10].decode())
                if attachStat == gameconst.MailAttachState.NotGet or readStat == gameconst.MailReadState.NotRead:
                    createTime = int(dbMailRowData[6].decode())
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

            if len(delMailGBIDList) > 0:
                gamesql.deleteMultiMails(self.gbID, delMailGBIDList, lambda ret, num, insertId, err:
                                            self.deleteExceedMailsCallback(ret, num, insertId, err, delMailGBIDList))
            if len(delMailGBIDList) >= maxMailNum:
                gamesql.deleteOldMails(self.gbID, minMailTime, minMailTiemMailList, isGlobal, lambda ret, num, insertId, err:
                                        self.deleteOldMailsCallback(ret, num, insertId, err, minMailTime))

        updateDueTimeGBIDList = []
        expiredMailObjs = {}
        expiredMailGBIDList = []
        validMailList = validMailList or ret
        for dbMailRowData in validMailList:
            mailObj = Mail.Mail()
            mailObj.initFromDBMailData(dbMailRowData)
            # 判断过期或者不在登录窗口有效期内
            if mailObj.isExpired() or not mailObj.isInLoginWindow(self.tLoginBase):
                expiredMailGBIDList.append(mailObj.mailGBID)
                expiredMailObjs[mailObj.mailGBID] = mailObj
                continue
            dueTime = mailObj.getDueTime()
            if self.mailCacheData.addNewMailCache(self, mailObj):
                #有旧邮件，本次load的是新收到的邮件
                self.newMails.append(mailObj.toMailClientDict())
                if dueTime > 0:
                    updateDueTimeGBIDList.append(mailObj.mailGBID)
        
        if len(updateDueTimeGBIDList) > 0:
            gamesql.updateMultiMails(self.gbID, updateDueTimeGBIDList, lambda ret, num, insertId, err:
                                    self.updateMultiMailsCallback(ret, num, insertId, err, updateDueTimeGBIDList, AAC_AACDD.datas.BONUS_SRC_MAIL_CLEAR_DUETIME, 'clear due time'))
            
        LOG_IFO('_loadMailsFromDBCallback:', isGlobal)
        rmCacheMailList = self.mailCacheData.getReplaceMailList(isGlobal)
        rmMails = self.mailCacheData.deleteMailsCache(rmCacheMailList)
        needDelete = False
        if len(rmCacheMailList) > 0:
            needDelete = True
            gamesql.deleteMultiMails(self.gbID, rmCacheMailList, lambda ret, num, insertId, err:
                                    self.deleteMultiMailsCallback(ret, num, insertId, err, rmMails, AAC_AACDD.datas.BONUS_SRC_EXCEED_DELETE_MAIL, 'exceed limit'))


        self.doAfterLoadMails(mailLoadType, needDelete)

        if expiredMailGBIDList:
            gamesql.deleteMultiMails(self.gbID, expiredMailGBIDList,
                                     lambda ret, num, insertId, err:self.deleteMultiMailsCallback(ret, num, insertId,
                                                                              err, expiredMailObjs, AAC_AACDD.datas.BONUS_SRC_EXPIRE_DELETE_MAIL, 'delete expired'))

    def deleteExceedMailsCallback(self, ret, num, insertId, err, delMailGBIDList):
        if err:
            LOG_WARN('   deleteExceedMailsCallback failed:', err, delMailGBIDList)
        return

    def deleteOldMailsCallback(self, ret, num, insertId, err, oldMailTime):
        if err:
            LOG_WARN('   deleteOldMailsCallback failed:', err, oldMailTime)
        return

    def updateMultiMailsCallback(self, ret, num, insertId, err, updateMailGBIDList, srcType, desc):
        if err:
            LOG_WARN('   updateMultiMailsCallback failed:', err, updateMailGBIDList, srcType, desc)
        return
    
    def doAfterLoadMails(self, finishedMailType, needDelete):
        if needDelete:
            if not self.hasDeleteMails:
                self.hasDeleteMails = needDelete
        LOG_DBG("doAfterLoadMails~  0", finishedMailType, needDelete, self.hasDeleteMails)
        self.loadFinishedCount += 1
        if finishedMailType == gameconst.MailLoadType.GLOBAL_MAIL \
            or finishedMailType == gameconst.MailLoadType.PLAYER_MAIL:
            if self.loadFinishedCount == 1:
                self.loadFinishedCount = 0
                self.loadMailType = gameconst.MailLoadType.DEFAULT
            if not self.hasOldMail or self.hasDeleteMails:
                #没有旧邮件，本次load的是全部邮件
                LOG_DBG("doAfterLoadMails~  1", finishedMailType)
                self.sendAllMailList()
            else:
                LOG_DBG("doAfterLoadMails~  2", finishedMailType)
                self.client and self.client.onGetNewMail(self.newMails, self.mailCacheData.playerMailSpaceLeft(), self.mailCacheData.systemMailSpaceLeft())
            self.resetLoadMails()
        elif finishedMailType == gameconst.MailLoadType.GLOBAL_AND_PLAYER_MAIL:
            if self.loadFinishedCount == 2:
                if not self.hasOldMail or self.hasDeleteMails:
                    LOG_DBG("doAfterLoadMails~  3", finishedMailType)
                    #没有旧邮件，本次load的是全部邮件
                    self.sendAllMailList()
                else:
                    LOG_DBG("doAfterLoadMails~  4", finishedMailType)
                    self.client and self.client.onGetNewMail(self.newMails, self.mailCacheData.playerMailSpaceLeft(), self.mailCacheData.systemMailSpaceLeft())
                self.resetLoadMails()

    def resetLoadMails(self):
        LOG_DBG("resetLoadMails~")
        self.loadFinishedCount = 0
        self.hasOldMail = False
        self.hasDeleteMails = False
        self.loadMailType = gameconst.MailLoadType.DEFAULT
        self.newMails = []

    @gamedecorator.checkGameconfigEnable('mail')
    def reqReadOneMail(self, exposed, mailGBID):
        LOG_IFO('in reqReadOneMail:', mailGBID)
        gamesql.setMailHasRead(self.gbID, mailGBID, lambda ret, num, insertId, err, mailGBID=mailGBID:
                                            self.setMailHasReadCallback(ret, num, insertId, err, mailGBID))

    def setMailHasReadCallback(self, ret, num, insertId, err, mailGBID):
        LOG_IFO('in setMailHasReadCallback:', ret, num, insertId, err)
        if err:
            LOG_WARN('setMailHasReadCallback failed:', err)
            return
        self.mailCacheData.readMail(self, mailGBID)
        self.client.onReadOneMail(mailGBID)

    @gamedecorator.checkGameconfigEnable('mail')
    @AuthClsWraper.authWithPermission(A_AFD.UIMailPanel)
    def reqGetOneMailAttach(self, exposed, mailGBID):
        LOG_IFO('in reqGetOneMailAttach:', mailGBID)
        mail = self.mailCacheData.getMailByGBID(mailGBID)
        if not mail:
            return
        self.getMailAttachByMailList([mail])

    @gamedecorator.checkGameconfigEnable('mail')
    @AuthClsWraper.authWithPermission(A_AFD.UIMailPanel)
    @gamedecorator.limitcall(2)
    def reqGetAllMailsAttach(self, exposed):
        LOG_IFO('in reqGetAllMailsAttach')
        mailList = self.mailCacheData.getMailsWithAttachHasNotGet()
        if not mailList:
            LOG_WARN('   reqGetAllMailsAttach, no mail with attach has not get')
            return
        self.getMailAttachByMailList(mailList)

    def getMailAttachByMailList(self, mailList):
        mailGBIDList = []
        totalWealthVal = dropAward.AwardVal()
        srcType = AAC_AACDD.datas.BONUS_SRC_MAIL_ATTACH
        hasSendSpaceNotEnoughMsg = False
        hasSendPotionMaxLimitMsg = False
        for mail in mailList:
            if mail.isExpired():
                LOG_WARN('getMailAttachByMailList mail expired:', mail.expiredTime)
                continue

            if not mail.canGetAttach():
                LOG_WARN('getMailAttachByMailList, can not get mail attach:', mail.toMailSavedDict())
                continue

            #注意加号'+'前后的wealth顺序不能变
            tryWealthVal = mail.attach.getAwardVal() + totalWealthVal
            tryAddResult = self.canAddWealthVal(srcType, tryWealthVal, bMsg=False, fromMail=True)
            if not tryAddResult:
                if not hasSendSpaceNotEnoughMsg:
                    hasSendSpaceNotEnoughMsg = True
                    if tryAddResult.extra == gameconst.BagOPStat.OPERATE_BAG_NO_SPACE:
                        self.onMessagePre(MMD.datas.bagFullGeneralMessage, [])
                continue

            # 背包数量限制物品
            if not tryWealthVal.isEmpty():
                totalLimitItemNum = 0
                for item in tryWealthVal.itemWealth.getItemObjs():
                    if item.itemId in IDIDS.categoryDatas.get(gameconst.BAG_LIMIT_ITEM_TYPE_DATA, set()):
                        totalLimitItemNum += item.itemNum
                if totalLimitItemNum != 0 and self.checkBagItemLimitNoItemId(totalLimitItemNum):
                    if not hasSendPotionMaxLimitMsg:
                        hasSendPotionMaxLimitMsg = True
                        self.onMessagePre(IDSD.datas['potionMaxLimitMsgID']['value'], [str(self.drugsQuantityBase)])
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
        #LOG_IFO('in getMailAttachCallback:', ret, num, insertId, err)
        self.unlockBag(gameconst.BagType.BAG_TYPE_NORMAL)
        if err:
            LOG_WARN('   setMailAttachHasGetCallback failed:', err)
            return

        _mailGBIDs = []
        popRewardUUID = KBEngine.genUUID64()
        now = utils.curTS()
        for mailGBID in mailGBIDList:
            mail = self.mailCacheData.getMailByGBID(mailGBID)
            if not mail:
                gameengine.panicStack('setMailAttachHasGetCallback, no mail:', mailGBID)
                continue

            wealthVal = mail.attach.getAwardVal()
            opUUID = mail.opUUID or mail.mailGBID
            if not self.canAddWealthVal(AAC_AACDD.datas.BONUS_SRC_MAIL_ATTACH, wealthVal, bMsg=True):
                # 正常情况不会走到这里
                gameengine.panicStack('setMailAttachHasGetCallback, add attach wealthval failed:', mailGBID, mail.mailId)
                self.resetMailAttachState(opUUID, mailGBID, mail.readStat)
                continue
            _mailGBIDs.append(mailGBID)
            mail.setReadState(gameconst.MailReadState.HasRead)
            wealthVal.scrubWealthItemObjs(createTime=now)
            srcType = mail.srcType if mail.srcType else AAC_AACDD.datas.BONUS_SRC_MAIL_ATTACH
            detail = gameclass.AwardDetail(mailId=mail.mailId, mailGBID=[mailGBID], desc=mail.desc, popRewardUUID=popRewardUUID)
            self.addWealth(srcType, wealthVal, opUUID, detail=detail, srcSubType=mail.srcSubType, idipSource=mail.source, directly=False)

            LogTrackingMgr.LogTrackingMgr.Mail_Get(self.gbID, mail.fromGBID, mail.mailId, mail.mailGBID, mail.globalMailGBID, mail.srcType, mail.srcSubType, mail.opUUID, mail.source, mail.attach)
        self._showPopReward(AAC_AACDD.datas.BONUS_SRC_MAIL_ATTACH, popRewardUUID, gameclass.AwardDetail(mailGBID=_mailGBIDs))
        self.client.onGetMailAttach(_mailGBIDs)
        return

    def resetMailAttachState(self, opUUID, mailGBID, readState):
        LOG_IFO('resetMailAttachState:', opUUID, mailGBID, readState)
        gamesql.resetMailAttachNotState(self.gbID, mailGBID, readState, lambda ret, num, insertId, err, opUUID=opUUID:
                                            self.resetMailAttachStateCallback(ret, num, insertId, err, opUUID))

    def resetMailAttachStateCallback(self, ret, num, insertId, err, opUUID):
        LOG_IFO('in resetMailAttachStateCallback:', ret, num, insertId, opUUID)
        mailGBIDList = utils.popCallbackTmpInfo(self, opUUID)
        if err:
            gameengine.panicStack('     resetMailAttachStateCallback failed:', ret, num, insertId, self.gbID, opUUID, mailGBIDList)
            return

        for mailGBID in mailGBIDList:
            mail = self.mailCacheData.getMailByGBID(mailGBID)
            mail and mail.setAttachState(gameconst.MailAttachState.NotGet)

        LOG_IFO('resetMailAttachStateCallback, reset mail attach state succ:', mailGBIDList)
        return

    @gamedecorator.checkGameconfigEnable('mail')
    @AuthClsWraper.authWithPermission(A_AFD.UIMailPanel)
    def reqDelMails(self, exposed, mailGBIDList):
        # 删除选中的邮件
        LOG_IFO('in reqDelMails:', mailGBIDList)
        if not mailGBIDList:
            return
        mailGBID = mailGBIDList[0]
        mail = self.mailCacheData.getMailByGBID(mailGBID)
        if not mail:
            LOG_WARN('reqDelMails, no mail:', mailGBIDList)
            return

        if mail.canGetAttach():
            LOG_IFO('reqDelMails, del mail failed, has attach:', mailGBID)
            self.onMessagePre(MMD.datas.mailDelete_Fail, [])
            return

        gamesql.deleteMailByMailGBID(self.gbID, mailGBID, lambda ret, num, insertId, err, mailGBID=mailGBID:
                                            self.deleteMailByMailGBIDCallback(ret, num, insertId, err, mailGBID))
        return

    def deleteMailByMailGBIDCallback(self, ret, num, insertId, err, mailGBID):
        LOG_IFO('deleteMailByMailGBIDCallback:', ret, num, insertId, err, mailGBID)
        if err:
            gameengine.panicStack('   deleteMailByMailGBIDCallback failed:', mailGBID)
            return
        self.onMailsDeleted({mailGBID:self.mailCacheData.getMailByGBID(mailGBID)}, srcType=AAC_AACDD.datas.BONUS_SRC_CLIENT_DELETE_MAIL, desc='from client')
        return

    @gamedecorator.checkGameconfigEnable('mail')
    @AuthClsWraper.authWithPermission(A_AFD.UIMailPanel)
    def reqDelAllMails(self, exposed):
        LOG_IFO('in reqDelAllMails')
        delMailGBIDList = self.mailCacheData.getMailListCanDelete()
        if not delMailGBIDList:
            LOG_WARN('reqDelAllMails, no mail can delete')
            return
        rmMails = self.mailCacheData.deleteMailsCache(delMailGBIDList)
        gamesql.deleteMultiMails(self.gbID, delMailGBIDList, lambda ret, num, insertId, err, delMailGBIDList=delMailGBIDList:
                                            self.deleteMultiMailsCallback(ret, num, insertId, err, rmMails, AAC_AACDD.datas.BONUS_SRC_CLIENT_DELETE_MAIL, 'from client'))

    def deleteMultiMailsCallback(self, ret, num, insertId, err, rmMails, srcType, desc):
        if err:
            LOG_WARN('   deleteMultiMailsCallback failed')
            return
        self.onMailsDeleted(rmMails, srcType, desc=desc)
        return

    def onMailsDeleted(self, rmMails, srcType=0, srcSubType=0, desc='', idipSource=0, sendClient=True):
        mailGBIDList = list(rmMails.keys())
        now = utils.curTS()
        expireDuration = gameconst.ONE_DAY_COST_SECONDS * 60
        for mailGbId in list(self.hasGotGlobalMails.keys()):
            tAdd = self.hasGotGlobalMails[mailGbId]
            if mailGbId not in gameglobal.globalMailsCacheList and now - tAdd > expireDuration:
                self.hasGotGlobalMails.pop(mailGbId, 0)
        self.mailCacheData.deleteMailsCache(mailGBIDList)
        sendClient and self.client.onDelMails(mailGBIDList, self.mailCacheData.playerMailSpaceLeft(), self.mailCacheData.systemMailSpaceLeft())
        opUUID = KBEngine.genUUID64()
        for mailGBID, mVal in rmMails.items():
            if not mVal:
                continue
            self.doRecordDeleteMailLog(mVal, opUUID, srcType, srcSubType, desc, idipSource, mailGBID)
        return

    def doRecordDeleteMailLog(self, mail, opUUID, srcType, srcSubType, desc, idipSource, mailGBID):
        LogTrackingMgr.LogTrackingMgr.Mail_Delete(self.gbID, mail.fromGBID, mail.mailId, mail.mailGBID, mail.globalMailGBID, mail.srcType, mail.srcSubType, mail.opUUID, mail.source, mail.attach, srcType)

