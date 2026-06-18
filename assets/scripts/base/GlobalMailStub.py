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
        LOG_DBG('GlobalMailStub')
                
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
        self._onTimerTrigger(tid, userArg)
        if utils.isBelongTimerTag(userArg):
            self._onTimerCallback(tid)

    def trySendDelayMails(self):
        if self.delayMailTimerId:
            self.cancelTimerCB(self.delayMailTimerId, gametimer.TIMER_TAG_CHECK_SEND_DELAY_MAILS)
            self.delayMailTimerId = 0

        if not self.delayMailList:
            return
        now = utils.curTS()
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

        LOG_INFO('trySendDelayMails, sendMailList:', [gmail.toGlobalMailDict() for gmail in sendMailList])
        for gmail in sendMailList:
            self.delayMailList.remove(gmail)
        self.addToSendMailDeque(sendMailList)

        if minLeftTime != float('inf'):
            LOG_INFO('trySendDelayMails:', minLeftTime, len(self.delayMailList))
            self.delayMailTimerId = self.addTimerCB(minLeftTime, 'trySendDelayMails', (),
                                                   gametimer.TIMER_TAG_CHECK_SEND_DELAY_MAILS, 'delayMailTimerId')

    def sendGlobalMail(self, mailId, extraAttach:dropAward.MailAttachVal, despArgs, title, cont, 
                       minRoleTime, maxRoleTime, dueTime, minRoleLevel, maxRoleLevel, channel, srcType,
                       mailTag=0):
        LOG_INFO('in sendGlobalMail:', mailId, extraAttach, despArgs, title, cont, minRoleTime, maxRoleTime, dueTime, minRoleLevel, maxRoleLevel, channel, srcType)
        
        if dueTime < 0 or maxRoleTime < 0 or maxRoleLevel < 0 :
            LOG_WARN('sendGlobalMail, maxRoleTime or maxRoleLevel failed:', dueTime, maxRoleTime, maxRoleLevel)
            return

        if minRoleTime > maxRoleTime or minRoleLevel > maxRoleLevel:
            LOG_WARN('sendGlobalMail, args error:', minRoleTime, maxRoleTime, minRoleLevel, maxRoleLevel)
            return

        if len(despArgs) != MAMAD.MailArgsNumMap[mailId]:
            gameengine.panicStack('     sendGlobalMail, despArgs num error:', mailId, despArgs)
            return

        if utils.curTS() <= self.lastSendTime:
            LOG_WARN('   sendGlobalMail, in sendGlobalMail cd, please send later')
            return False

        mailData = MAMAD.datas.get(mailId, None)
        if not mailData:
            LOG_WARN('   in sendGlobalMail, no this mail:', mailId)
            return False

        if mailData['type'] == gameconst.MailType.PLAYER_MAIL:
            LOG_WARN('   in sendGlobalMail, not global mail:', mailData['type'])
            return False

        if not mailData['isOpen']:
            LOG_WARN('   in sendGlobalMail, not opened')
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
            dueTime,
            minRoleLevel, 
            maxRoleLevel,
            channel,
            srcType,
            mailTag
        )

        if globalMail.isExpired():
            LOG_WARN('   in sendGlobalMail, mail expired')
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
            self.cancelTimerCB(self.sendMailTimerId, gametimer.TIMER_TAG_SEND_GLOBAL_MAIL)
            self.sendMailTimerId = 0
        if not self.sendMailDeque:
            return
        curTime = utils.curTS()
        if curTime <= self.lastSendTime:
            self.sendMailTimerId = self.addTimerCB(2, 'startSendGlobalMail', (),
                                                   gametimer.TIMER_TAG_SEND_GLOBAL_MAIL, 'sendMailTimerId')
            return

        globalMail = self.sendMailDeque.popleft()
        self._doSendGlobalMail(curTime, globalMail)
        if self.sendMailDeque:
            LOG_INFO('startSendGlobalMail, left mail num:', len(self.sendMailDeque))
            self.sendMailTimerId = self.addTimerCB(2, 'startSendGlobalMail', (),
                                                   gametimer.TIMER_TAG_SEND_GLOBAL_MAIL, 'sendMailTimerId')

    def _doSendGlobalMail(self, curTime, globalMail):
        LOG_INFO('_doSendGlobalMail:', globalMail.toGlobalMailDict())
        self.lastSendTime = curTime
        globalMail.createTime = curTime
        self.mailList.append(globalMail)
        self.writeToDB(functools.partial(self._onGlobalMailWriteToDB, globalMail.globalMailGBID))

    def delayWriteToDBGlobalMail(self, globalMailGBID):
        self.writeToDB(functools.partial(self._onGlobalMailWriteToDB, globalMailGBID))

    def _onGlobalMailWriteToDB(self, globalMailGBID, saveStatus, baseRef):
        LOG_INFO('_onGlobalMailWriteToDB:', globalMailGBID, saveStatus, baseRef)
        # 引擎里的落库保存时，前一个保存请求还在进行中，需要延迟处理
        if saveStatus == gameconst.WriteToDBResult.ARCHIVING:
            self.addTimerCB(1, 'delayWriteToDBGlobalMail', (globalMailGBID, ), gametimer.TIMER_TAG_GLOBAL_MAIL_WRITE_TO_DB)
            return

        # 引擎里找不到具名的数据库连接，放弃保存了，报个错
        if saveStatus == gameconst.WriteToDBResult.MISSING_DB_INTERFACE:
            self.mailList.remove(globalMail)
            gameengine.panicStack('_onGlobalMailWriteToDB: db interface is missing:', globalMailGBID)
            return
        
        globalMail = self.findGlobalMailByMailGBID(globalMailGBID)
        if not globalMail:
            gameengine.panicStack('_onGlobalMailWriteToDB: not found globamail:', globalMailGBID)
            return

        if not saveStatus:
            self.mailList.remove(globalMail)
            gameengine.panicStack('_onGlobalMailWriteToDB: writeToDB failed')
            return
        # 增加同步全服
        gameengine.broadcastBaseapp('onSyncOneGlobalMail', (globalMail, ))
        # 检查全服存储限制
        self.checkGlobalMailNum()

    def findGlobalMailByMailGBID(self, globalMailGBID):
        for mail in reversed(self.mailList):
            if mail.globalMailGBID == globalMailGBID:
                return mail

    def checkGlobalMailNum(self):
        # 1.处理过期的全服邮件
        expiredMailPosList = []
        for pos, mail in enumerate(self.mailList):
            if mail.isExpired():
                expiredMailPosList.append(pos)

        for pos in reversed(expiredMailPosList):
            self.mailList.pop(pos)

        # 2.检查是否接近上限，报个警
        if len(self.mailList) / gameconst.MailConstEnum.MAX_GLOBAL_MAIL_SAVE_COUNT >= gameconst.MailConstEnum.MAX_GLOBAL_MAIL_OVER_RATE / 100:
            gameengine.panicStack('checkGlobalMailNum, global mail save is closed to up limit ', \
                                        len(self.mailList), \
                                        gameconst.MailConstEnum.MAX_GLOBAL_MAIL_SAVE_COUNT, \
                                        gameconst.MailConstEnum.MAX_GLOBAL_MAIL_OVER_RATE
                                    )
        # 3.正常范围内，正常同步全服
        if len(self.mailList) <= gameconst.MailConstEnum.MAX_GLOBAL_MAIL_SAVE_COUNT:
            expiredMailPosList and self.syncGlobalMailsList()
            return
        
        # 4.处理超过上限，先删除最老的邮件
        self.mailList = self.mailList[-1*gameconst.MailConstEnum.MAX_GLOBAL_MAIL_SAVE_COUNT:]
        # 5.同步全服
        self.syncGlobalMailsList()
        return

    def syncGlobalMailsList(self):
        gameengine.broadcastBaseapp('onSyncGlobalMailsList', (self.mailList,))
        return

    ##################################### gm ##########################################
    def gmGetGlobalMailList(self, box, channelAvatarInfo, mailNum):
        import gameconst
        mailList = [{'maiGBID':mail.globalMailGBID, 'mailId':mail.mailId,
                     'createTime':time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(mail.createTime))}
                     for mail in list(self.mailList)[:-(mailNum+1):-1]]
        LOG_INFO('gmGetGlobalMailList:', str(mailList))
        box.client.onRecvAvatarChannelMsg(gameconst.ChatChannelEnum.WORLD, channelAvatarInfo, {"msg": str(mailList), "code": 0, "voiceUrl": '', "msgType": 0})

    def gmDeleteOneGlobalMail(self, mailGBID):
        return

    ##################################### gm end ##########################################

