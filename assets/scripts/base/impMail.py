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
import antiAddictCategory_antiAddictCategory_def as AAC_AAC_DD
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

    def onCheckAccountMailsFinished(self):
        self.startLoadSyncGlobalMailInfo()

    def checkGlobalMail(self, globalMail):
        # 检查是否被ban无法收到此类型邮件
        LOG_DBG("checkGlobalMail", self.banMail, globalMail.createTime)
        if self.banMail and globalMail.mailTag in self.banMail:
            startTime, endTime = self.banMail[globalMail.mailTag]
            createTime = globalMail.createTime
            if createTime > startTime and createTime < endTime:
                return False
        return mailAssistor.checkGlobalMailConds(globalMail, self.accountEntity.accountType, self.getAvatarLevel(), self.birthInDB, self.tLoginBase)

    def sendOneGlobalMail(self, globalMail):
        LOG_INFO('in sendOneGlobalMail:', globalMail.globalMailGBID)
        if not self.checkGlobalMail(globalMail):
            return
        self.doInsertGlobalMail(0, globalMail)

    def loadLastGlobalMailInfoCallback(self, ret, num, insertId, err):
        LOG_INFO('loadLastGlobalMailInfoCallback:', ret, num, insertId, err)
        if err:
            gameengine.panicStack(' loadLastGlobalMailInfoCallback, no lastGlobalMailInfo:', ret, num, insertId, err)
            return
        mailRowData = ret[0]
        lastGlobalMailTime = int(mailRowData[2].decode())
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
            _opUUID = KBEngine.genUUID64()
            globalMail = newGlobalMailList.pop()
            utils.setCallbackTmpInfo(self, _opUUID, newGlobalMailList)
            self.doInsertGlobalMail(_opUUID, globalMail, True)
        else:
            #没有新的全服邮件
            LOG_INFO('no global mail, mail init finished')
            self.mailInitFinishedOnLogin()
            self.startLoadMails(gameconst.MailLoadType.GLOBAL_AND_PLAYER_MAIL)

    def startLoadSyncGlobalMailInfo(self):
        # 首先获得同步过的全服邮件最新信息
        gamesql.loadLastGlobalMailInfo(self.gbID, self.loadLastGlobalMailInfoCallback)

    def doInsertGlobalMail(self, opUUID, globalMail, isLogin = False):
        mailAssistor.sendMailToPlayers(
            [self.gbID], 
            globalMail.mailId, 
            extraAttach=globalMail.extraAttach,
            despArgs=globalMail.despArgs, 
            createTime=globalMail.createTime, 
            globalMailGBID=globalMail.globalMailGBID,
            title=globalMail.title,
            expiredTime=globalMail.expiredTime, 
            cont=globalMail.cont, 
            srcType=globalMail.srcType, 
            callback=functools.partial(self.insertGlobalMailCallback, opUUID, globalMail.createTime, isLogin),
            isGlobal = True)

    def insertGlobalMailCallback(self, opUUID, mailCreateTime, isLogin, ret, num, insertId, err, mailGBID):
        LOG_INFO('insertGlobalMailCallback:', ret, num, insertId, err, mailGBID, opUUID, mailCreateTime, isLogin)
        if err:
            gameengine.panicStack('insertGlobalMailCallback, error:', ret, num, insertId, err)

        self.hasGotGlobalMails[mailGBID] = utils.curTS()
        insertGlobalMailList = utils.popCallbackTmpInfo(self, opUUID)
        if not insertGlobalMailList:
            LOG_INFO('insert all global mail succ, mail init finished')
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

    def onInsertNewMailSucc(self, mailId, mailGBID, title, cont, attachStr, srcType, srcSubType, opUUID, desc, idipSource, isGlobal):
        # 有新普通邮件插入数据库表中
        LOG_INFO('onInsertNewMailSucc:', mailId, isGlobal)
        mailLoadType = gameconst.MailLoadType.PLAYER_MAIL
        if isGlobal:
            mailLoadType = gameconst.MailLoadType.GLOBAL_MAIL
        self.startLoadMails(mailLoadType)

    def mailInitFinishedOnLogin(self):
        LOG_INFO('mailInitFinishedOnLogin')
        self.mailInitLockedTime = 0
        _lastGlobalMailTime = mailAssistor.getLastGlobalMailTime()
        if _lastGlobalMailTime:
            gamesql.updateLastGlobaMailInfo(
                self.gbID, 
                _lastGlobalMailTime, 
                lambda ret, num, insertId, err:
                                            self._updateLastGlobalMailInfoCallback(ret, num, insertId, err, _lastGlobalMailTime))

    def _updateLastGlobalMailInfoCallback(self, ret, num, insertId, err, lastGlobalMailTime):
        LOG_INFO('_updateLastGlobalMailInfoCallback:', ret, num, insertId, err, lastGlobalMailTime)

    def delayStartLoadMails(self, mailLoadType):
        LOG_INFO('delayStartLoadMails', mailLoadType)
        self.loadMailTimerId = 0
        self.startLoadMails(mailLoadType)

    def startLoadMails(self, mailLoadType):
        if gameconfig.isCrossServer():
            return
            
        if utils.curTS() < self.mailInitLockedTime:
            LOG_WARN('startLoadMails, mail init not finished')
            return

        if self.mailInitLockedTime != 0:
            # 到这里并且self.mailInitLockedTime不为0， 说明邮件初始化流程出错中断
            gameengine.panicStack('startLoadMails, init mail from db error')

        LOG_INFO('startLoadMails:', mailLoadType, self.mailCacheData.lastPlayerMailTime, self.mailCacheData.lastGlobalMailTime)
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

        LOG_INFO('in _loadMailsFromDBCallback:', isGlobal, mailLoadType, len(ret))
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
            for mailRowData in ret:
                mailGBID = int(mailRowData[2].decode())
                readStat = int(mailRowData[4].decode())
                attachStat = int(mailRowData[10].decode())
                if attachStat == gameconst.MailAttachState.NotGet or readStat == gameconst.MailReadState.NotRead:
                    _createTime = int(mailRowData[6].decode())
                    validMailGBIDSet.add(mailGBID)
                    if _createTime == minMailTime:
                        minMailTiemMailList.append(mailGBID)
                    if len(validMailGBIDSet) == maxMailNum:
                        break

            _delMailGBIDList = []
            leftNum = maxMailNum-len(validMailGBIDSet)
            for mailRowData in ret:
                mailGBID = int(mailRowData[2].decode())
                if mailGBID in validMailGBIDSet:
                    validMailList.append(mailRowData)
                elif leftNum > 0:
                    validMailList.append(mailRowData)
                    leftNum-=1
                else:
                    _delMailGBIDList.append(mailGBID)

            if len(_delMailGBIDList) > 0:
                gamesql.deleteMultiMails(self.gbID, _delMailGBIDList, lambda ret, num, insertId, err:
                                            self.deleteExceedMailsCallback(ret, num, insertId, err, _delMailGBIDList))
            if len(_delMailGBIDList) >= maxMailNum:
                gamesql.deleteOldMails(self.gbID, minMailTime, minMailTiemMailList, isGlobal, lambda ret, num, insertId, err:
                                        self.deleteOldMailsCallback(ret, num, insertId, err, minMailTime))

        updateDueTimeGBIDList = []
        expiredMailObjs = {}
        expiredMailGBIDList = []
        validMailList = validMailList or ret
        for mailRowData in validMailList:
            mailObj = Mail.Mail()
            mailObj.initFromDBMailData(mailRowData)
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
                                    self.updateMultiMailsCallback(ret, num, insertId, err, updateDueTimeGBIDList, AAC_AAC_DD.datas.BONUS_SRC_MAIL_CLEAR_DUETIME, 'clear due time'))
            
        LOG_INFO('_loadMailsFromDBCallback:', isGlobal)
        rmCacheMailList = self.mailCacheData.getReplaceMailList(isGlobal)
        rmMails = self.mailCacheData.deleteMailsCache(rmCacheMailList)
        needDelete = False
        if len(rmCacheMailList) > 0:
            needDelete = True
            gamesql.deleteMultiMails(
                self.gbID,
                rmCacheMailList,
                functools.partial(
                    self.deleteMultiMailsCallback, 
                    rmMails, 
                    AAC_AAC_DD.datas.BONUS_SRC_EXCEED_DELETE_MAIL, 
                    'exceed limit'),
            )


        self.doAfterLoadMails(mailLoadType, needDelete)

        if expiredMailGBIDList:
            gamesql.deleteMultiMails(
                self.gbID, 
                expiredMailGBIDList,
                functools.partial(
                    self.deleteMultiMailsCallback,
                    expiredMailObjs, 
                    AAC_AAC_DD.datas.BONUS_SRC_EXPIRE_DELETE_MAIL, 
                    'delete expired'
                ),
            )

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
        LOG_INFO('in reqReadOneMail:', mailGBID)
        gamesql.setMailHasRead(
            self.gbID, 
            mailGBID,
            functools.partial(self.setMailHasReadCallback, mailGBID),
        )

    def setMailHasReadCallback(self, mailGBID, ret, num, insertId, err):
        LOG_INFO('in setMailHasReadCallback:', ret, num, insertId, err)
        if err:
            LOG_WARN('setMailHasReadCallback failed:', err)
            return
        self.mailCacheData.readMail(self, mailGBID)
        self.client.onReadOneMail(mailGBID)

    @gamedecorator.checkGameconfigEnable('mail')
    @AuthClsWraper.authWithPermission(A_AFD.UIMailPanel)
    def reqGetOneMailAttach(self, exposed, mailGBID):
        LOG_INFO('in reqGetOneMailAttach:', mailGBID)
        _mail = self.mailCacheData.getMailByGBID(mailGBID)
        if not _mail:
            return
        self.getMailAttachByMailList([_mail])

    @gamedecorator.checkGameconfigEnable('mail')
    @AuthClsWraper.authWithPermission(A_AFD.UIMailPanel)
    @gamedecorator.limitcall(2)
    def reqGetAllMailsAttach(self, exposed):
        LOG_INFO('in reqGetAllMailsAttach')
        _mailList = self.mailCacheData.getMailsWithAttachHasNotGet()
        if not _mailList:
            LOG_WARN('   reqGetAllMailsAttach, no mail with attach has not get')
            return
        self.getMailAttachByMailList(_mailList)

    def getMailAttachByMailList(self, mailList):
        _mailGBIDList = []
        totalWealthVal = dropAward.AwardVal()
        srcType = AAC_AAC_DD.datas.BONUS_SRC_MAIL_ATTACH
        hasSendSpaceNotEnoughMsg = False
        hasSendPotionMaxLimitMsg = False
        for mail in mailList:
            if mail.isExpired():
                LOG_WARN('getMailAttachByMailList mail expired:', mail.expiredTime)
                continue

            if not mail.coudlGetAttach():
                LOG_WARN('getMailAttachByMailList, can not get mail attach:', mail.toMailSavedDict())
                continue

            #注意加号'+'前后的wealth顺序不能变
            _tryWealthVal = mail.attach.getAwardVal() + totalWealthVal
            tryAddResult = self.canAddWealthVal(srcType, _tryWealthVal, bMsg=False, fromMail=True)
            if not tryAddResult:
                if not hasSendSpaceNotEnoughMsg:
                    hasSendSpaceNotEnoughMsg = True
                    if tryAddResult.extra == gameconst.BagOPStat.OPERATE_BAG_NO_SPACE:
                        self.onMessagePre(MMD.datas.bagFullGeneralMessage, [])
                continue

            # 背包数量限制物品
            if not _tryWealthVal.isEmpty():
                totalLimitItemNum = 0
                for item in _tryWealthVal.itemWealth.getItemObjs():
                    if item.itemId in IDIDS.categoryDatas.get(gameconst.BAG_LIMIT_ITEM_TYPE_DATA, set()):
                        totalLimitItemNum += item.itemNum
                if totalLimitItemNum != 0 and self.checkBagItemLimitNoItemId(totalLimitItemNum):
                    if not hasSendPotionMaxLimitMsg:
                        hasSendPotionMaxLimitMsg = True
                        self.onMessagePre(IDSD.datas['potionMaxLimitMsgID']['value'], [str(self.drugsQuantityBase)])
                    continue

            totalWealthVal = _tryWealthVal
            _mailGBIDList.append(mail.mailGBID)
        if not _mailGBIDList:
            return

        if not self.bagData.tryLockBag(lockDesc='getMailAttachByMailList'):
            return
        #先设置缓存中附件为已领取状态
        for mailGBID in _mailGBIDList:
            self.mailCacheData.setAttachHasGet(mailGBID)
        gamesql.setMailHasGetAttach(self.gbID, _mailGBIDList, lambda ret, num, insertId, err:
                                      self.setMailAttachHasGetCallback(ret, num, insertId, err, _mailGBIDList))

    def setMailAttachHasGetCallback(self, ret, num, insertId, err, mailGBIDList):
        self.unlockBag(gameconst.BagTypeEnum.BAG_TYPE_NORMAL)
        if err:
            LOG_WARN('   setMailAttachHasGetCallback failed:', err)
            return

        _mailGBIDs = []
        popRewardUUID = KBEngine.genUUID64()
        now = utils.curTS()
        for mailGBID in mailGBIDList:
            _mail = self.mailCacheData.getMailByGBID(mailGBID)
            if not _mail:
                gameengine.panicStack('setMailAttachHasGetCallback, no mail:', mailGBID)
                continue

            wealthVal = _mail.attach.getAwardVal()
            opUUID = _mail.opUUID or _mail.mailGBID
            if not self.canAddWealthVal(AAC_AAC_DD.datas.BONUS_SRC_MAIL_ATTACH, wealthVal, bMsg=True):
                # 正常情况不会走到这里
                gameengine.panicStack('setMailAttachHasGetCallback, add attach wealthval failed:', mailGBID, _mail.mailId)
                self.resetMailAttachState(opUUID, mailGBID, _mail.readStat)
                continue
            _mailGBIDs.append(mailGBID)
            _mail.setReadState(gameconst.MailReadState.HasRead)
            wealthVal.scrubWealthItemObjs(createTime=now)
            srcType = _mail.srcType if _mail.srcType else AAC_AAC_DD.datas.BONUS_SRC_MAIL_ATTACH
            detail = gameclass.AwardDetailCls(mailId=_mail.mailId, mailGBID=[mailGBID], desc=_mail.desc, popRewardUUID=popRewardUUID)
            self.addWealth(srcType, wealthVal, opUUID, detail=detail, srcSubType=_mail.srcSubType, idipSource=_mail.source, directly=False)

            result = []
            attachStr = _mail.attach.getItemsTLogStr()
            if ',' in attachStr:
                tmp = {int(k): int(v) for k, v in (pair.split(',') for pair in attachStr.split(';'))}
                for itemId, itemCount in tmp.items():
                    result.append({'item_id':itemId, 'item_count':itemCount, 'item_quality':dataUtils.getItemQuality(itemId)})
            LogTrackingMgr.LogTrackingMgr.mail_get(
                self.gbID, 
                self.accountEntity.clientDistinctId, 
                self.gbID, 
                _mail.fromGBID, 
                _mail.mailId, 
                _mail.mailGBID, 
                _mail.globalMailGBID, 
                _mail.srcType, 
                _mail.srcSubType, 
                _mail.opUUID, 
                _mail.source, 
                result)

        self._showPopReward(AAC_AAC_DD.datas.BONUS_SRC_MAIL_ATTACH, popRewardUUID, gameclass.AwardDetailCls(mailGBID=_mailGBIDs))
        self.client.onGetMailAttach(_mailGBIDs)

    def resetMailAttachState(self, opUUID, mailGBID, readState):
        LOG_INFO('resetMailAttachState:', opUUID, mailGBID, readState)
        gamesql.resetMailAttachNotState(
            self.gbID, 
            mailGBID, 
            readState, 
            functools.partial(self.resetMailAttachStateCallback, opUUID)
        )

    def resetMailAttachStateCallback(self, opUUID, ret, num, insertId, err):
        LOG_INFO('in resetMailAttachStateCallback:', ret, num, insertId, opUUID)
        mailGBIDList = utils.popCallbackTmpInfo(self, opUUID)
        if err:
            gameengine.panicStack('     resetMailAttachStateCallback failed:', ret, num, insertId, self.gbID, opUUID, mailGBIDList)
            return

        for mailGBID in mailGBIDList:
            _mail = self.mailCacheData.getMailByGBID(mailGBID)
            if _mail:
                _mail.setAttachState(gameconst.MailAttachState.NotGet)

        LOG_INFO('resetMailAttachStateCallback, reset mail attach state succ:', mailGBIDList)

    @gamedecorator.checkGameconfigEnable('mail')
    @AuthClsWraper.authWithPermission(A_AFD.UIMailPanel)
    def reqDelMails(self, exposed, mailGBIDList):
        # 删除选中的邮件
        LOG_INFO('in reqDelMails:', mailGBIDList)
        if not mailGBIDList:
            return
        mailGBID = mailGBIDList[0]
        _mail = self.mailCacheData.getMailByGBID(mailGBID)
        if not _mail:
            LOG_WARN('reqDelMails, no _mail:', mailGBIDList)
            return

        if _mail.coudlGetAttach():
            LOG_INFO('reqDelMails, del _mail failed, has attach:', mailGBID)
            self.onMessagePre(MMD.datas.mailDelete_Fail, [])
            return

        gamesql.deleteMailByMailGBID(
            self.gbID, 
            mailGBID, 
            functools.partial(self.deleteMailByMailGBIDCallback, mailGBID),
        )

    def deleteMailByMailGBIDCallback(self, mailGBID, ret, num, insertId, err):
        LOG_INFO('deleteMailByMailGBIDCallback:', ret, num, insertId, err, mailGBID)
        if err:
            gameengine.panicStack('   deleteMailByMailGBIDCallback failed:', mailGBID)
            return

        self.onMailsDeleted(
            {mailGBID: self.mailCacheData.getMailByGBID(mailGBID)}, 
            srcType=AAC_AAC_DD.datas.BONUS_SRC_CLIENT_DELETE_MAIL, 
            desc='from client')

    @gamedecorator.checkGameconfigEnable('mail')
    @AuthClsWraper.authWithPermission(A_AFD.UIMailPanel)
    def reqDelAllMails(self, exposed):
        LOG_INFO('in reqDelAllMails')
        delMailGBIDList = self.mailCacheData.getMailListCanDelete()
        if not delMailGBIDList:
            LOG_WARN('reqDelAllMails, no mail can delete')
            return
        rmMails = self.mailCacheData.deleteMailsCache(delMailGBIDList)
        gamesql.deleteMultiMails(
            self.gbID, 
            delMailGBIDList, 
            functools.partial(
                self.deleteMultiMailsCallback,
                rmMails, 
                AAC_AAC_DD.datas.BONUS_SRC_CLIENT_DELETE_MAIL, 
                'from client'
            ),
        )

    def deleteMultiMailsCallback(self, rmMails, srcType, desc, ret, num, insertId, err):
        if err:
            LOG_WARN('   deleteMultiMailsCallback failed')
            return
        self.onMailsDeleted(rmMails, srcType, desc=desc)

    def onMailsDeleted(self, rmMails, srcType=0, srcSubType=0, desc='', idipSource=0, sendClient=True):
        _mailGBIDList = list(rmMails.keys())
        now = utils.curTS()
        expireDuration = gameconst.ONE_DAY_COST_SECONDS * 60
        for mailGbId in list(self.hasGotGlobalMails.keys()):
            tAdd = self.hasGotGlobalMails[mailGbId]
            if mailGbId not in gameglobal.globalMailsCacheList and now - tAdd > expireDuration:
                self.hasGotGlobalMails.pop(mailGbId, 0)
        self.mailCacheData.deleteMailsCache(_mailGBIDList)
        if sendClient:
            self.client.onDelMails(
                _mailGBIDList,
                self.mailCacheData.playerMailSpaceLeft(),
                self.mailCacheData.systemMailSpaceLeft()
            )

        _opUUID = KBEngine.genUUID64()
        for mailGBID, mVal in rmMails.items():
            if not mVal:
                continue
            self.doRecordDeleteMailLog(mVal, _opUUID, srcType, srcSubType, desc, idipSource, mailGBID)

    def doRecordDeleteMailLog(self, mail, opUUID, srcType, srcSubType, desc, idipSource, mailGBID):
        result = []
        attachStr = mail.attach.getItemsTLogStr()
        if ',' in attachStr:
            tmp = {int(k): int(v) for k, v in (pair.split(',') for pair in attachStr.split(';'))}
            for itemId, itemCount in tmp.items():
                result.append({'item_id':itemId, 'item_count':itemCount, 'item_quality':dataUtils.getItemQuality(itemId)})
        LogTrackingMgr.LogTrackingMgr.mail_delete(self.gbID, self.accountEntity.clientDistinctId, self.gbID, mail.fromGBID, mail.mailId, mail.mailGBID, mail.globalMailGBID, mail.srcType, mail.srcSubType, mail.opUUID, mail.source, result, srcType)

