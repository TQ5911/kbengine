# -*- coding: utf-8 -*-

import KBEngine
from KBEDebug import *
import functools
import gameengine
import gametimer
import iBaseNoCell
import iGlobal
import iTimer
import Mail
import mail_mail as MAMAD
import mail_config as MACF
import time
import utils
import dataUtils
import dropAward
import gameconst
import mailAssistor
import collections
import gameglobal

class GlobalMailStub(iGlobal.IGlobal, iBaseNoCell.IBaseNoCell, iTimer.ITimer):
    def __init__(self):
        super(GlobalMailStub, self).__init__()
        self.delayMailTimerId = 0
        self.sendMailTimerId = 0
        self.sendMailDeque = collections.deque()

    def postReloadScript(self):
        super(GlobalMailStub, self).postReloadScript()
        for globalMail in self.mailList:
            globalMail.reloadScript()

        for globalMail in self.sendMailDeque:
            globalMail.reloadScript()

    def doNext(self):
        self.syncGlobalMailsList()
        gameglobal.localBaseApp.fullPrepare(self.classname())
        self.trySendDelayMails()

    def onTimer(self, tid, userArg):
        self._onTimer(tid, userArg)
        if utils.isBelongTimerTag(userArg):
            self._onTimerCallback(tid)

    def trySendDelayMails(self):
        if self.delayMailTimerId:
            self._cancelCallback(self.delayMailTimerId, gametimer.TIMER_TAG_CHECK_SEND_DELAY_MAILS)
            self.delayMailTimerId = 0

        if not self.delayMailList:
            return
        now = utils.getNow()
        sendMailList = []
        minLeftTime = float('inf')
        for mail in self.delayMailList:
            if mail.isExpired():
                continue
            if mail.createTime <= now:
                sendMailList.append(mail)
                continue
            if mail.createTime-now < minLeftTime:
                minLeftTime = mail.createTime-now

        INFO_MSG('trySendDelayMails, sendMailList:', [gmail.toGlobalMailDict() for gmail in sendMailList])
        for gmail in sendMailList:
            self.delayMailList.remove(gmail)
        self.addToSendMailDeque(sendMailList)

        if minLeftTime != float('inf'):
            INFO_MSG('trySendDelayMails:', minLeftTime, len(self.delayMailList))
            self.delayMailTimerId = self._callback(minLeftTime, 'trySendDelayMails', (),
                                                   gametimer.TIMER_TAG_CHECK_SEND_DELAY_MAILS, 'delayMailTimerId')

    def sendIDIPGlobalMail(self, su, cmdId, attachStr, title, cont, beginTime, endTime, serial, idipSource, mailId,
                           minRoleTime, maxRoleTime, minRoleLevel, maxRoleLevel, idipMailType):
        INFO_MSG('sendIDIPGlobalMail:', cmdId, attachStr, title, cont, beginTime, endTime, serial, idipSource)
        # if idipMailType == gameconst.IDIPMailType.IDIP_SERVER_ITEM_MAIL:
        #     respClass = idipDef.IDIP_DO_SEND_SERVER_ITEM_MAIL_RSP
        # elif idipMailType == gameconst.IDIPMailType.IDIP_LINK_MAIL:
        #     respClass = idipDef.IDIP_DO_SEND_MAIL_WITH_LINKS_RSP
        # elif idipMailType == gameconst.IDIPMailType.IDIP_SERVER_PRE_MAIL:
        #     respClass = idipDef.IDIP_DO_PRE_SEND_SERVER_MAIL_RSP
        # else:
        #     ERROR_MSG('sendIDIPGlobalMail, idipType error:', idipMailType)
        #     return

        # if minRoleTime < 0 or minRoleLevel < 0:
        #     WARNING_MSG('sendIDIPGlobalMail, minRoleTime or minRoleLevel failed:', minRoleTime, minRoleLevel)
        #     retCode = gameconst.IDIPErr.ARGS_ERR
        #     errMsg = 'minRoleTime or minRoleLevel invalid'
        #     su.sendIDIPResponse(retCode, errMsg, respClass(retCode, errMsg))
        #     return
        #
        # if maxRoleTime <= 0 or maxRoleLevel <=0:
        #     WARNING_MSG('sendIDIPGlobalMail, maxRoleTime or maxRoleLevel failed:', maxRoleTime, maxRoleLevel)
        #     retCode = gameconst.IDIPErr.ARGS_ERR
        #     errMsg = 'maxRoleTime or maxRoleLevel invalid'
        #     su.sendIDIPResponse(retCode, errMsg, respClass(retCode, errMsg))
        #     return
        #
        # if minRoleTime>=maxRoleTime or minRoleLevel>maxRoleLevel:
        #     WARNING_MSG('sendIDIPGlobalMail, args error:', minRoleTime, maxRoleTime, minRoleLevel, maxRoleLevel)
        #     retCode = gameconst.IDIPErr.ARGS_ERR
        #     errMsg = 'minRoleTime, maxRoleTime, minRoleLevel, maxRoleLevel invalid'
        #     su.sendIDIPResponse(retCode, errMsg, respClass(retCode, errMsg))
        #     return
        #
        # attach = mailAssistor.parseAttachStr(attachStr)
        # now = utils.getNow()
        # if endTime != 0 and endTime < now:
        #     WARNING_MSG('sendIDIPGlobalMail, endTime time error:', beginTime, now)
        #     retCode = gameconst.IDIPErr.ARGS_ERR
        #     su.sendIDIPResponse(retCode, 'EndTime expired', respClass(retCode, 'EndTime expired'))
        #     return
        #
        # if endTime != 0 and beginTime >= endTime:
        #     WARNING_MSG('sendIDIPGlobalMail, beginTime and endTime time error:', beginTime, endTime, now)
        #     retCode = gameconst.IDIPErr.ARGS_ERR
        #     su.sendIDIPResponse(retCode, 'BeginTime greater EndTime',  respClass(retCode, 'BeginTime greater EndTime'))
        #     return
        #
        # if attach.mailWealthExceedUplimit():
        #     WARNING_MSG('sendIDIPGlobalMail, mailWealthExceedUplimit')
        #     retCode = gameconst.IDIPErr.ARGS_ERR
        #     su.sendIDIPResponse(retCode, 'item count limit', respClass(retCode, 'item count limit'))
        #     return
        #
        # globalMail = Mail.GlobalMail()
        # globalMail.initNewGlobalMail(mailId, attach, (), title, cont, minRoleTime, maxRoleTime, minRoleLevel, maxRoleLevel)
        # if endTime:
        #     globalMail.expiredTime = endTime
        #
        # globalMail.createTime = now if beginTime <= now else beginTime
        # self.delayMailList.append(globalMail)
        # self.trySendDelayMails()
        # su.sendIDIPResponse(0, '', respClass(0, ''))
        return

    def sendGlobalMail(self, mailId, extraAttach:dropAward.MailWealthVal, 
                       despArgs, title, cont, minRoleTime, maxRoleTime,
                       minRoleLevel, maxRoleLevel, channel, srcType):
        INFO_MSG('in sendGlobalMail:', mailId, extraAttach, despArgs, title, cont, minRoleTime, maxRoleTime, minRoleLevel, maxRoleLevel, channel, srcType)
        
        if maxRoleTime <= 0 or maxRoleLevel <=0 :
            WARNING_MSG('sendGlobalMail, maxRoleTime or maxRoleLevel failed:', maxRoleTime, maxRoleLevel)
            return

        if minRoleTime>maxRoleTime or minRoleLevel>maxRoleLevel:
            WARNING_MSG('sendIDIPGlobalMail, args error:', minRoleTime, maxRoleTime, minRoleLevel, maxRoleLevel)
            return

        if len(despArgs) != MAMAD.MailArgsNumMap[mailId]:
            gameengine.reportCritical('     sendGlobalMail, despArgs num error:', mailId, despArgs)
            return

        if utils.getNow() <= self.lastSendTime:
            WARNING_MSG('   sendGlobalMail, in sendGlobalMail cd, please send later')
            return False

        mailData = MAMAD.datas.get(mailId, None)
        if not mailData:
            WARNING_MSG('   in sendOneGlobalMail, no this mail:', mailId)
            return False

        if mailData['type'] == gameconst.MailType.PLAYER_MAIL:
            WARNING_MSG('   in sendOneGlobalMail, not global mail:', mailData['type'])
            return False

        if not mailData['isOpen']:
            WARNING_MSG('   in sendOneGlobalMail, not opened')
            return False

        title = title or ''
        cont = cont or ''
        globalMail = Mail.GlobalMail()
        globalMail.initNewGlobalMail(
            mailId, 
            extraAttach, 
            despArgs, 
            title, 
            cont, 
            minRoleTime, 
            maxRoleTime, 
            minRoleLevel, 
            maxRoleLevel,
            channel,
            srcType
        )

        if globalMail.isExpired():
            WARNING_MSG('   in sendGlobalMail, mail expired')
            return False
        self.addToSendMailDeque([globalMail])
        return True

    def addToSendMailDeque(self, mailList):
        if not mailList:
            return
        self.sendMailDeque.extend(mailList)
        self.startSendGlobalMail()

    def startSendGlobalMail(self):
        if self.sendMailTimerId:
            self._cancelCallback(self.sendMailTimerId, gametimer.TIMER_TAG_SEND_GLOBAL_MAIL)
            self.sendMailTimerId = 0
        if not self.sendMailDeque:
            return
        if utils.getNow() <= self.lastSendTime:
            self.sendMailTimerId = self._callback(2, 'startSendGlobalMail', (),
                                                   gametimer.TIMER_TAG_SEND_GLOBAL_MAIL, 'sendMailTimerId')
            return

        globalMail = self.sendMailDeque.popleft()
        self._doSendGlobalMail(globalMail)
        if self.sendMailDeque:
            INFO_MSG('startSendGlobalMail, left mail num:', len(self.sendMailDeque))
            self.sendMailTimerId = self._callback(2, 'startSendGlobalMail', (),
                                                   gametimer.TIMER_TAG_SEND_GLOBAL_MAIL, 'sendMailTimerId')

    def _doSendGlobalMail(self, globalMail):
        INFO_MSG('_doSendGlobalMail:', globalMail.toGlobalMailDict())
        self.lastSendTime = utils.getNow()
        globalMail.createTime = utils.getNow()
        self.mailList.append(globalMail)
        self.writeToDB(functools.partial(self._onGlobalMailWriteToDB, globalMail.globalMailGBID))

    def delayWriteToDBGlobalMail(self, globalMailGBID):
        self.writeToDB(functools.partial(self._onGlobalMailWriteToDB, globalMailGBID))

    def _onGlobalMailWriteToDB(self, globalMailGBID, isSuccess, baseRef):
        INFO_MSG('_onGlobalMailWriteToDB:', globalMailGBID, isSuccess, baseRef)
        if isinstance(isSuccess, int) and isSuccess == gameconst.WriteToDBResult.ARCHIVING:
            self._callback(1, 'delayWriteToDBGlobalMail', (globalMailGBID, ), gametimer.TIMER_TAG_GLOBAL_MAIL_WRITE_TO_DB)
            return

        globalMail = self.findGlobalMailByMailGBID(globalMailGBID)
        if not globalMail:
            gameengine.reportCritical('_onGlobalMailWriteToDB not found globamail:', globalMailGBID)
            return

        if not isSuccess:
            gameengine.reportCritical('_onGlobalMailWriteToDB writeToDB failed')
            self.mailList.remove(globalMail)
            return

        gameengine.broadcastBaseapp('onSyncOneGlobalMail', (globalMail, ))
        self.checkGlobalMailNum()
        self.makeGlobalMailLog(globalMail)

    def makeGlobalMailLog(self, globalMail):
        attachStr = globalMail.extraAttach.getItemsTLogStr()
        showAttachStr = ''
        attachList = attachStr.split(';')
        for attachItemStr in attachList:
            if not attachItemStr:
                continue
            itemId, itemNum = attachItemStr.split(',')
            itemName = dataUtils.getItemSpecialDetailData(int(itemId))['name']
            showAttachStr += itemName + ':' + itemNum + ';'
        if showAttachStr:
            showAttachStr = showAttachStr.strip(';')

    def findGlobalMailByMailGBID(self, globalMailGBID):
        for mail in reversed(self.mailList):
            if mail.globalMailGBID == globalMailGBID:
                return mail

    def checkGlobalMailNum(self):
        expiredMailPosList = []
        for pos, mail in enumerate(self.mailList):
            if mail.isExpired() or mail.isTracebackTimeOut():
                expiredMailPosList.append(pos)

        for pos in reversed(expiredMailPosList):
            self.mailList.pop(pos)

        mailMaxNum = MACF.datas['mailNumMax']['value']
        if len(self.mailList) <= mailMaxNum:
            expiredMailPosList and self.syncGlobalMailsList()
            return

        canDeleteMailPosList = []
        for pos, mail in enumerate(self.mailList):
            mailData = MAMAD.datas[mail.mailId]
            if mailData['type'] == gameconst.MailType.GLOBAL_MAIL_EXCLUDE_NEW_PLAYERS:
                canDeleteMailPosList.append(pos)

        deleteNum = len(canDeleteMailPosList)-mailMaxNum
        deletePosList = []
        if deleteNum > 0:
            deletePosList = canDeleteMailPosList[:deleteNum]
            for pos in reversed(deletePosList):
                self.mailList.pop(pos)

        if expiredMailPosList or deletePosList:
            self.syncGlobalMailsList()
        return

    def syncGlobalMailsList(self):
        gameengine.broadcastBaseapp('onSyncGlobalMailsList', (self.mailList, self.deleteMailsList))
        return

    ##################################### gm ##########################################
    def gmGetGlobalMailList(self, box, channelAvatarInfo, mailNum):
        import gameconst
        mailList = [{'maiGBID':mail.globalMailGBID, 'mailId':mail.mailId,
                     'createTime':time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(mail.createTime))}
                     for mail in list(self.mailList)[:-(mailNum+1):-1]]
        INFO_MSG('gmGetGlobalMailList:', str(mailList))
        box.client.onRecvAvatarChannelMsg(gameconst.ChatChannel.WORLD, channelAvatarInfo, str(mailList))

    def gmDeleteOneGlobalMail(self, mailGBID):
        return

    ##################################### gm end ##########################################

